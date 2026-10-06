import urllib.request
import json

base = "http://127.0.0.1:5000"
settings = ["park", "trail", "campus", "garden", "street"]

forbidden = ["touch", "pick", "climb", "eat", "poison", "person", "people", "face", "private"]

for s in settings:
    data = json.dumps({"setting": s}).encode("utf-8")
    req = urllib.request.Request(f"{base}/api/bingo/new", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        card = json.loads(resp.read().decode("utf-8"))
        squares = [sq["text"] for sq in card["squares"]]
        assert len(squares) == 9
        # Check safety
        violates = [sq for sq in squares if any(f in sq.lower() for f in forbidden)]
        print(f"Setting '{s}' (fallback={card.get('fallback', False)}):")
        for sq in squares:
            print(f"  - {sq}")
        if violates:
            print(f"  WARNING violations: {violates}")
        else:
            print("  Safety check: PASSED (0 violations)")
        print()
