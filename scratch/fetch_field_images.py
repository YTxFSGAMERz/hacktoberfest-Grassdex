import json
import os
import urllib.parse
import urllib.request
from PIL import Image

OUT_DIR = os.path.abspath("scratch/field_test_photos")
os.makedirs(OUT_DIR, exist_ok=True)

TARGETS = [
    ("01_pigeon", "Common pigeon at Waterlow Park", "bird", "Pigeon", 0),
    ("02_red_rose", "red rose flower garden", "plant", "Red Rose", 1),
    ("03_green_foliage", "green foliage leaves sun", "plant", "Foliage Leaves", 2),
    ("04_butterfly", "monarch butterfly flower", "bug", "Butterfly", 3),
    ("05_wooden_sign", "wooden sign trail park", "other", "Wooden Sign", 4),
    ("06_dandelion", "dandelion flower lawn", "plant", "Dandelion", None),
    ("07_tree_bark", "oak tree bark texture", "plant", "Tree Bark", None),
    ("08_honeybee", "honeybee flower macro", "bug", "Honeybee", None),
    ("09_ant", "ant wood forest", "bug", "Ant", None),
    ("10_crow", "crow bird grass park", "bird", "Crow", None),
    ("11_duck", "mallard duck pond", "bird", "Mallard Duck", None),
    ("12_mushroom", "agaricus campestris mushroom grass", "fungus", "Wild Mushroom", None),
    ("13_bracket_fungus", "bracket fungus tree bark", "fungus", "Bracket Fungus", None),
    ("14_spider", "garden spider web", "bug", "Spider", None),
    ("15_fern", "fern frond forest", "plant", "Fern", None),
    ("16_bench", "park bench stone concrete", "other", "Park Bench", 7),
]

def search_wikimedia_image(query):
    try:
        q = urllib.parse.quote(query)
        search_url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={q}&srnamespace=6&srlimit=5"
        req = urllib.request.Request(search_url, headers={"User-Agent": "GrassdexDataset/1.0 (devchallenge@example.org)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("query", {}).get("search", [])
            for res in results:
                title = res.get("title")
                if not title: continue
                # Query imageinfo
                info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
                req2 = urllib.request.Request(info_url, headers={"User-Agent": "GrassdexDataset/1.0 (devchallenge@example.org)"})
                with urllib.request.urlopen(req2, timeout=10) as resp2:
                    d2 = json.loads(resp2.read().decode("utf-8"))
                    pages = d2.get("query", {}).get("pages", {})
                    for page in pages.values():
                        info = page.get("imageinfo", [])
                        if info and info[0].get("url"):
                            u = info[0]["url"]
                            clean_u = u.split("?")[0].lower()
                            if any(clean_u.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                                return u
    except Exception as e:
        print(f"  Error searching for {query}: {e}")
    return None

def download_and_clean(url, out_path):
    req = urllib.request.Request(url, headers={"User-Agent": "GrassdexDataset/1.0 (devchallenge@example.org)"})
    raw_path = out_path + ".raw"
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(raw_path, "wb") as f:
                f.write(resp.read())
        
        # Open with PIL, strip EXIF metadata, resize to max 1024px dimension
        with Image.open(raw_path) as img:
            rgb = img.convert("RGB")
            rgb.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            rgb.save(out_path, "JPEG", quality=85)
        
        if os.path.exists(raw_path):
            os.remove(raw_path)
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        if os.path.exists(raw_path):
            os.remove(raw_path)
        return False

print("Fetching field test candidate photos...")
downloaded = []
for item in TARGETS:
    tag, query, kind, name, sq = item
    out_file = os.path.join(OUT_DIR, f"{tag}.jpg")
    print(f"[{tag}] Query: '{query}'")
    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
        print("  Already exists, skipping download.")
        downloaded.append((out_file, kind, name, sq))
        continue
    
    img_url = search_wikimedia_image(query)
    if img_url:
        print(f"  Found URL: {img_url}")
        if download_and_clean(img_url, out_file):
            print(f"  Saved clean EXIF-stripped image to {out_file} ({os.path.getsize(out_file)} bytes)")
            downloaded.append((out_file, kind, name, sq))
        else:
            print("  Download failed.")
    else:
        print("  No image found.")

print(f"\nDone! Successfully prepared {len(downloaded)} field test images in {OUT_DIR}")
