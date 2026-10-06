import json, os, re, time
from datetime import datetime
from pathlib import Path

import ollama
from flask import Flask, jsonify, request, send_from_directory

MODEL = "gemma4:e4b"  # swap for any vision model you've pulled
LOG = Path("data/grassdex.json")
LOG.parent.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="static")

PROMPT = (
    "You are a field guide. Identify the main living thing (plant, bug, bird or fungus) in this photo. "
    "Reply with ONLY JSON: "
    '{"name": "common name", "kind": "plant|bug|bird|fungus|other", '
    '"confidence": 0-100, "fun_fact": "one short sentence"}. '
    "If unsure, say so in the name and give a low confidence."
)


def warm_up():
    try:
        ollama.chat(model=MODEL, messages=[{"role": "user", "content": "hi"}], keep_alive="30m")
    except Exception as e:
        print("warm-up failed (is Ollama running?):", e)


def load_log():
    return json.loads(LOG.read_text()) if LOG.exists() else []


def save_log(log):
    LOG.write_text(json.dumps(log, indent=2))


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


@app.get("/api/log")
def get_log():
    return jsonify(load_log())


@app.post("/api/identify")
def identify():
    photo = request.files["photo"].read()
    t0 = time.time()
    res = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT, "images": [photo]}],
        format="json",
        keep_alive="30m",
        options={"temperature": 0.2},
    )
    content = getattr(res.message, "content", None) or res["message"]["content"]
    entry = parse(content)
    entry.update(
        seconds=round(time.time() - t0, 1),
        time=datetime.now().isoformat(timespec="seconds"),
        correct=None,
    )
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

