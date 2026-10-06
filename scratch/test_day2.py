import urllib.request
import json

base = "http://127.0.0.1:5000"

print("--- 1. Testing GET / ---")
with urllib.request.urlopen(f"{base}/") as r:
    html = r.read().decode("utf-8")
    assert "Bingo" in html and "Dex" in html
    print("GET / passed (status 200, contains Bingo & Dex tabs)")

print("\n--- 2. Testing GET /api/bingo ---")
with urllib.request.urlopen(f"{base}/api/bingo") as r:
    card = json.loads(r.read().decode("utf-8"))
    assert len(card["squares"]) == 9
    print(f"GET /api/bingo passed (card id={card.get('id')}, setting={card.get('setting')}, 9 squares)")
    for i, sq in enumerate(card["squares"]):
        print(f"  Square {i}: {sq['text']} [{sq['status']}]")

print("\n--- 3. Testing POST /api/bingo/new ---")
data = json.dumps({"setting": "garden"}).encode("utf-8")
req = urllib.request.Request(f"{base}/api/bingo/new", data=data, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as r:
    new_card = json.loads(r.read().decode("utf-8"))
    assert len(new_card["squares"]) == 9
    print(f"POST /api/bingo/new passed (setting={new_card.get('setting')}, fallback={new_card.get('fallback', False)})")
    for i, sq in enumerate(new_card["squares"]):
        print(f"  Square {i}: {sq['text']}")

print("\n--- 4. Testing POST /api/bingo/override ---")
ov_data = json.dumps({"square": 4}).encode("utf-8")
req = urllib.request.Request(f"{base}/api/bingo/override", data=ov_data, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as r:
    res = json.loads(r.read().decode("utf-8"))
    assert res["ok"] is True
    assert res["card"]["squares"][4]["status"] == "done"
    assert res["card"]["squares"][4]["override"] is True
    print(f"POST /api/bingo/override passed (square 4 is done and override=True)")

print("\nAll API unit checks passed!")
