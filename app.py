import json, os, random, re, time
from datetime import datetime
from pathlib import Path

import ollama
from flask import Flask, jsonify, request, send_from_directory

MODEL = "gemma4:e4b"  # swap for any vision model you've pulled
THRESHOLD = 40        # confidence threshold to auto-mark square done

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
PHOTOS = DATA_DIR / "photos"
PHOTOS.mkdir(exist_ok=True)
LOG = DATA_DIR / "grassdex.json"
BINGO = DATA_DIR / "bingo.json"
POOL_FILE = Path("bingo_pool.json")

app = Flask(__name__, static_folder="static")

PROMPT = (
    "You are a field guide. Identify the main living thing (plant, bug, bird or fungus) in this photo. "
    "Reply with ONLY JSON: "
    '{"name": "common name", "kind": "plant|bug|bird|fungus|other", '
    '"confidence": 0-100, "fun_fact": "one short sentence"}. '
    "If unsure, say so in the name and give a low confidence."
)

SQUARE_SUFFIX = (
    ' The player is trying to complete this bingo square: "{square}". '
    'Add two keys: "square_match" (true only if the photo clearly satisfies the square) '
    'and "match_reason" (one short sentence).'
)

BINGO_PROMPT = (
    "You write outdoor scavenger-hunt squares for a 3x3 bingo card. Setting: {setting}.\n"
    'Return ONLY JSON: {{"squares": ["...", ...]}} with exactly 9 strings.\n'
    "Each square is 3 to 8 words and can be confirmed from a single photo.\n"
    "It must be photographable from a safe distance, in a public place, in daylight.\n"
    "Mix: 3 colors or shapes, 3 living things (plant, bug, bird), 3 textures, patterns or structures.\n"
    "Never require touching, picking, climbing, entering private property, approaching animals, or photographing people.\n"
    "No duplicates."
)


def warm_up():
    try:
        ollama.chat(model=MODEL, messages=[{"role": "user", "content": "hi"}], keep_alive="30m")
    except Exception as e:
        print("warm-up failed (is Ollama running?):", e)


def load_pool():
    if POOL_FILE.exists():
        try:
            return json.loads(POOL_FILE.read_text())
        except Exception:
            pass
    return [
        "something red", "a yellow flower", "a purple flower",
        "a bird perched on something", "a spider web", "tree bark with deep grooves",
        "moss or lichen", "a seed pod", "a bug on a leaf"
    ]


def load_log():
    return json.loads(LOG.read_text()) if LOG.exists() else []


def save_log(log):
    LOG.write_text(json.dumps(log, indent=2))


def load_bingo():
    if BINGO.exists():
        try:
            return json.loads(BINGO.read_text())
        except Exception:
            pass
    pool = load_pool()
    random.shuffle(pool)
    squares = [{"text": s, "status": "open", "override": False, "photo": None} for s in pool[:9]]
    card = {
        "id": datetime.now().isoformat(timespec="seconds"),
        "setting": "park",
        "squares": squares,
    }
    save_bingo(card)
    return card


def save_bingo(card):
    BINGO.write_text(json.dumps(card, indent=2))


def generate_bingo_card(setting="park"):
    prompt = BINGO_PROMPT.format(setting=setting)
    for attempt in range(3):
        try:
            res = ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0.9},
            )
            content = getattr(res.message, "content", None) or res["message"]["content"]
            m = re.search(r"\{.*\}", content, re.S)
            if m:
                data = json.loads(m.group(0))
                raw_squares = data.get("squares", [])
                if isinstance(raw_squares, list) and len(raw_squares) == 9:
                    clean_squares = []
                    seen = set()
                    valid = True
                    for s in raw_squares:
                        if not isinstance(s, str):
                            valid = False
                            break
                        s = s.strip()
                        if not s or len(s) > 60 or s.lower() in seen:
                            valid = False
                            break
                        seen.add(s.lower())
                        clean_squares.append(s)
                    if valid and len(clean_squares) == 9:
                        squares = [{"text": s, "status": "open", "override": False, "photo": None} for s in clean_squares]
                        card = {
                            "id": datetime.now().isoformat(timespec="seconds"),
                            "setting": setting,
                            "squares": squares,
                        }
                        save_bingo(card)
                        return card
        except Exception as e:
            print(f"Card generation attempt {attempt + 1} failed: {e}")
    # Fallback to pool
    pool = load_pool()
    random.shuffle(pool)
    squares = [{"text": s, "status": "open", "override": False, "photo": None} for s in pool[:9]]
    card = {
        "id": datetime.now().isoformat(timespec="seconds"),
        "setting": setting,
        "squares": squares,
        "fallback": True,
    }
    save_bingo(card)
    return card


def parse(text):
    entry = {"name": "unknown", "kind": "other", "confidence": 0, "fun_fact": "", "parsed": True}
    m = re.search(r"\{.*\}", text, re.S)
    try:
        entry.update(json.loads(m.group(0)))
    except Exception:
        entry["parsed"] = False
        entry["fun_fact"] = text[:120]
    return entry


@app.get("/")
def home():
    return send_from_directory("static", "index.html")


@app.get("/data/photos/<path:filename>")
def serve_photo(filename):
    return send_from_directory(str(PHOTOS), filename)


@app.get("/api/log")
def get_log():
    return jsonify(load_log())


@app.get("/api/bingo")
def get_bingo():
    return jsonify(load_bingo())


@app.post("/api/bingo/new")
def new_bingo():
    data = request.get_json(silent=True) or {}
    setting = data.get("setting", "park")
    card = generate_bingo_card(setting=setting)
    return jsonify(card)


@app.post("/api/bingo/override")
def override_bingo():
    data = request.get_json() or {}
    idx = data.get("square")
    card = load_bingo()
    if idx is not None and 0 <= int(idx) < len(card["squares"]):
        sq = card["squares"][int(idx)]
        sq["status"] = "done"
        sq["override"] = True
        save_bingo(card)
        return jsonify(ok=True, card=card)
    return jsonify(ok=False, error="Invalid square index"), 400


@app.post("/api/identify")
def identify():
    photo = request.files["photo"].read()
    idx_raw = request.form.get("square")
    idx = int(idx_raw) if idx_raw is not None and idx_raw != "" else None

    card = load_bingo() if idx is not None else None
    square_obj = None
    if card and idx is not None and 0 <= idx < len(card["squares"]):
        square_obj = card["squares"][idx]

    prompt = PROMPT
    if square_obj:
        prompt += SQUARE_SUFFIX.format(square=square_obj["text"])

    photo_name = datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{random.randint(100, 999)}.jpg"
    (PHOTOS / photo_name).write_bytes(photo)

    t0 = time.time()
    res = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [photo]}],
        format="json",
        keep_alive="30m",
        options={"temperature": 0.1},
    )
    content = getattr(res.message, "content", None) or res["message"]["content"]
    entry = parse(content)
    entry.update(
        seconds=round(time.time() - t0, 1),
        time=datetime.now().isoformat(timespec="seconds"),
        correct=None,
        photo=photo_name,
    )

    if square_obj is not None:
        entry["square"] = idx
        # Check match criteria
        is_match = bool(entry.get("square_match") is True and entry.get("confidence", 0) >= THRESHOLD)
        if is_match and square_obj["status"] == "open":
            square_obj["status"] = "done"
            square_obj["photo"] = photo_name
            save_bingo(card)

    log = load_log()
    log.append(entry)
    save_log(log)
    return jsonify(entry)


@app.post("/api/mark")
def mark():
    d = request.get_json()
    log = load_log()
    log[d["i"]]["correct"] = d["correct"]
    save_log(log)
    return jsonify(ok=True)


if __name__ == "__main__":
    warm_up()
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=5000)
