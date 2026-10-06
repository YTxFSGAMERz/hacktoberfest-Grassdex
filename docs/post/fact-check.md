# Fact-Check Table

*Every factual claim, model tag, number, and metric in the DEV post must trace to a verified local source file.*

| Claim / Detail | Value in Post | Source File | Status | Notes |
|---|---|---|---|---|
| Model tag | `gemma4:e4b` | `app.py`, `ollama list` | Verified | Open-weight vision model by Google |
| Model parameters & quant | 7.5B, Q4_K_M, CLIP vision projector | `ollama show gemma4:e4b` | Verified | 6.6 GB on disk |
| Model license | Apache 2.0 | `ollama show gemma4:e4b` | Verified | Separate license from app code |
| Runtime & Server | Ollama v0.32.6 + Flask v3.1.3 | `requirements.txt`, `pip list` | Verified | Open-source runtime & web framework |
| Hardware used | AMD Ryzen 5 6600H, RTX 3050 Laptop GPU (6GB VRAM), 16GB RAM | `docs/metrics/day1-smoke.md` | Verified | Hardware baseline |
| Model GPU placement | 100% GPU offload (4.77 GB / 6.14 GB VRAM) | `docs/metrics/day1-smoke.md` | Verified | 0% CPU offload |
| Cold start latency | 7.36 s | `docs/metrics/day1-smoke.md` | Verified | First run from idle |
| Warm identification latency | 1.44 s – 5.62 s | `docs/metrics/day1-smoke.md` | Verified | Prompt eval > 1,000 t/s, eval ~54 t/s |
| Combined vision + bingo latency | 10.5 s – 17.2 s | `docs/metrics/day2-bingo.md` | Verified | Single combined model call |
| Vision gate smoke test | 5 / 5 passed (100%) | `docs/metrics/day1-smoke.md` | Verified | Leaf, sunflower, beetle, sparrow, mug control |
| Verification test trials | 6 / 6 passed (100%) | `docs/metrics/day2-bingo.md` | Verified | 3 match, 3 non-match, 0% false positives |
| Bingo auto-verification threshold | Confidence >= 40% | `app.py` | Verified | `THRESHOLD = 40` in code |
| Offline operation | 0 remote calls, 100% LAN/localhost | `app.py`, `static/index.html` | Verified | Zero external CDNs, fonts, or tracking |
| Privacy | Photos stored locally in `data/photos/` | `app.py`, `.gitignore` | Verified | Photos never leave laptop; EXIF stripped in `samples/` |
| Entry period window | Started Oct 6, 2026 | `git log` | Verified | Repo created within Week 1 window |
| Late commits | None | `README.md`, `git log` | Verified | All commits inside window |
