import json
import os
import time
import requests

BASE_URL = "http://127.0.0.1:5000"

FIELD_TESTS = [
    # (filename, ground_truth_name, ground_truth_kind, square_idx, note)
    ("01_pigeon.jpg", "Pigeon", "bird", 0, "Columba livia in park"),
    ("02_red_rose.jpg", "Red Rose", "plant", 1, "Vibrant red flower"),
    ("03_green_foliage.jpg", "Foliage Leaves", "plant", 2, "Green leaves in sun"),
    ("04_butterfly.jpg", "Monarch Butterfly", "bug", 3, "Butterfly on blossom"),
    ("05_wooden_sign.jpg", "Wooden Signpost", "other", 4, "Park entrance trail sign"),
    ("06_dandelion.jpg", "Dandelion", "plant", None, "Wild dandelion on lawn"),
    ("07_tree_bark.jpg", "Oak Tree Bark", "plant", None, "Textured tree bark"),
    ("08_honeybee.jpg", "Honeybee", "bug", None, "Bee pollinating flower"),
    ("09_ant.jpg", "Ant", "bug", None, "Wood ant nest / ants"),
    ("10_crow.jpg", "Crow", "bird", None, "Black corvid on grass"),
    ("11_duck.jpg", "Duck", "bird", None, "Mallard ducks near water"),
    ("12_mushroom.jpg", "Field Mushroom", "fungus", None, "Agaricus campestris wild mushroom"),
    ("13_bracket_fungus.jpg", "Bracket Fungus", "fungus", None, "Polypore shelf fungus on log"),
    ("14_spider.jpg", "Spider", "bug", None, "Garden spider on web"),
    ("15_fern.jpg", "Fern", "plant", None, "Fern frond"),
    ("16_bench.jpg", "Park Bench", "other", 7, "Stone / concrete park bench path"),
]

PHOTO_DIR = os.path.abspath("scratch/field_test_photos")

print("=== Starting Grassdex Automated Field Test Run ===")
print(f"Server: {BASE_URL}")

# Check server health
try:
    r = requests.get(f"{BASE_URL}/api/log", timeout=5)
    existing_log = r.json()
    print(f"Initial log entries: {len(existing_log)}")
except Exception as e:
    print(f"Error connecting to Grassdex server: {e}")
    exit(1)

results = []

for idx, (fname, gt_name, gt_kind, sq_idx, note) in enumerate(FIELD_TESTS, 1):
    fpath = os.path.join(PHOTO_DIR, fname)
    if not os.path.exists(fpath):
        print(f"Skipping {fname}: file not found")
        continue

    print(f"\n[{idx}/{len(FIELD_TESTS)}] Testing: {fname} (Ground truth: {gt_name} [{gt_kind}], Target square: {sq_idx})")
    
    with open(fpath, "rb") as f:
        files = {"photo": (fname, f, "image/jpeg")}
        data = {}
        if sq_idx is not None:
            data["square"] = sq_idx

        t0 = time.time()
        resp = requests.post(f"{BASE_URL}/api/identify", files=files, data=data, timeout=60)
        dur = time.time() - t0

    if resp.status_code != 200:
        print(f"  ❌ Request failed with HTTP {resp.status_code}: {resp.text}")
        continue

    entry = resp.json()
    print(f"  ⚡ Gemma response in {entry.get('seconds', dur):.1f}s (Total HTTP: {dur:.1f}s):")
    print(f"     Name:       {entry.get('name')}")
    print(f"     Kind:       {entry.get('kind')}")
    print(f"     Confidence: {entry.get('confidence')}%")
    print(f"     Fun fact:   {entry.get('fun_fact')}")
    
    if sq_idx is not None:
        print(f"     Square {sq_idx} match: {entry.get('square_match')} ({entry.get('match_reason')})")

    # Evaluate ground truth correctness
    pred_name = str(entry.get("name", "")).lower()
    pred_kind = str(entry.get("kind", "")).lower()
    gt_name_l = gt_name.lower()

    rating = False
    if gt_kind in ["plant", "bug", "bird", "fungus"]:
        if pred_kind == gt_kind:
            # Check if name is exact or close
            words = [w for w in gt_name_l.split() if len(w) > 3]
            if any(w in pred_name for w in words):
                rating = True
            else:
                rating = "close" # right kind, reasonable organism
        elif pred_kind in ["plant", "other"] and gt_kind in ["plant", "other"]:
            rating = "close"
        else:
            rating = False
    else: # other / object
        if pred_kind == "other" or any(w in pred_name for w in gt_name_l.split()):
            rating = True
        else:
            rating = "close"

    # Get updated log index to mark
    log_resp = requests.get(f"{BASE_URL}/api/log", timeout=5).json()
    latest_idx = len(log_resp) - 1
    
    # Rate the entry
    rate_resp = requests.post(
        f"{BASE_URL}/api/mark", 
        json={"i": latest_idx, "correct": rating},
        timeout=5
    )
    print(f"     Assigned rating: {rating} (Log index {latest_idx})")

# Test manual override if Square 4 wasn't matched automatically
bingo_resp = requests.get(f"{BASE_URL}/api/bingo", timeout=5).json()
sq4 = bingo_resp["squares"][4]
if sq4["status"] != "done":
    print("\n[Manual Override Test] Simulating player overriding Square 4 (Wooden Signpost)...")
    over_resp = requests.post(f"{BASE_URL}/api/bingo/override", json={"square": 4}, timeout=5)
    print(f"  Override response: HTTP {over_resp.status_code}")

print("\n=== Field Test Run Finished ===")
