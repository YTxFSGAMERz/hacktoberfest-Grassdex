import urllib.request
import json
import os

base = "http://127.0.0.1:5000"

# Setup a clean test card in data/bingo.json
test_card = {
    "id": "2026-10-06T20:30:00",
    "setting": "test",
    "squares": [
        {"text": "a yellow flower", "status": "open", "override": False, "photo": None},
        {"text": "a small insect or beetle", "status": "open", "override": False, "photo": None},
        {"text": "a bird on the ground or perched", "status": "open", "override": False, "photo": None},
        {"text": "something red", "status": "open", "override": False, "photo": None},
        {"text": "tree bark", "status": "open", "override": False, "photo": None},
        {"text": "a spider web", "status": "open", "override": False, "photo": None},
        {"text": "green grass", "status": "open", "override": False, "photo": None},
        {"text": "a dry leaf", "status": "open", "override": False, "photo": None},
        {"text": "a smooth pebble", "status": "open", "override": False, "photo": None}
    ]
}
with open("data/bingo.json", "w") as f:
    json.dump(test_card, f, indent=2)

boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"

def identify_square(img_path, square_idx):
    with open(img_path, "rb") as f:
        photo_bytes = f.read()
    filename = os.path.basename(img_path)
    
    header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="photo"; filename="{filename}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8")
    
    sq_part = (
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="square"\r\n\r\n'
        f"{square_idx}\r\n"
    ).encode("utf-8")
    
    footer = f"--{boundary}--\r\n".encode("utf-8")
    body = header + photo_bytes + sq_part + footer

    req = urllib.request.Request(
        f"{base}/api/identify",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

tests = [
    # (image, square_idx, expected_match, description)
    ("scratch/flower.jpg", 0, True, "Sunflower vs 'a yellow flower' (MATCH)"),
    ("scratch/flower.jpg", 1, False, "Sunflower vs 'a small insect' (NON-MATCH)"),
    ("scratch/insect.jpg", 1, True, "Beetle vs 'a small insect or beetle' (MATCH)"),
    ("scratch/insect.jpg", 2, False, "Beetle vs 'a bird' (NON-MATCH)"),
    ("scratch/bird.jpg", 2, True, "Sparrow vs 'a bird' (MATCH)"),
    ("scratch/bird.jpg", 0, False, "Sparrow vs 'a yellow flower' (NON-MATCH)")
]

results = []
for img, sq_idx, expected, desc in tests:
    res = identify_square(img, sq_idx)
    actual = res.get("square_match")
    match_ok = (actual == expected)
    results.append({
        "desc": desc,
        "expected": expected,
        "actual": actual,
        "confidence": res.get("confidence"),
        "reason": res.get("match_reason"),
        "seconds": res.get("seconds"),
        "photo": res.get("photo"),
        "pass": match_ok
    })
    print(f"[{'PASS' if match_ok else 'FAIL'}] {desc}: actual={actual} (expected={expected}) in {res.get('seconds')}s - reason: {res.get('match_reason')}")

with open("scratch/verification_results.json", "w") as f:
    json.dump(results, f, indent=2)
