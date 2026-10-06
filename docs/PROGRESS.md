# Grassdex progress

| Day | Date | Status | Gate result | Notes |
|---|---|---|---|---|
| 1 | Oct 6 | done | PASSED | Vision gate 5/5 passed; latency baseline recorded (1.4s–5.6s warm); MVP running and hardened; zero remote URLs |
| 2 | Oct 7 | done | PASSED | Dynamic 3x3 bingo generation; single-call ID + verification (6/6 trials passed, 0% false positives); override & win detection; photo persistence; fallback pool verified |
| 3 | Oct 8 | not started | | |
| 4 | Oct 9 | not started | | |
| 5 | Oct 10 | not started | | |
| 6 | Oct 11 | not started | | |

## Environment facts
- Model tag: `gemma4:e4b` (7.5B Q4_K_M, vision clip projector, local 6.6 GB)
- Model placement: 100% GPU offload on NVIDIA GeForce RTX 3050 6GB Laptop GPU (4.77 GB / 6.14 GB VRAM allocated)
- Ollama version: 0.32.6
- Laptop CPU: AMD Ryzen 5 6600H with Radeon Graphics (6 cores, 12 threads)
- Laptop GPU: NVIDIA GeForce RTX 3050 6GB Laptop GPU
- Laptop RAM: 16 GB
- Python: 3.13.13
- Timezone: IST (UTC+5:30)

## Decisions
- 2026-10-06: Verified `gemma4:e4b` exists locally with vision capability; running Ollama locally.
- 2026-10-06: Step 0 rules verified against DEV HF26 hub FAQ and documented in `docs/challenge-faq.md`.
- 2026-10-06: Applied privacy rule: smoke-test photos go to `scratch/` (gitignored); `samples/` reserved for Day 5 stripped photos.
- 2026-10-06: Completed Step 3 vision gate (5/5 correct across leaf, flower, insect, bird, and non-nature mug control).
- 2026-10-06: Completed Step 4 latency baseline (warm latency 1.4s–5.6s, well under 15s threshold; synchronous mode selected).
- 2026-10-06: Completed Step 6 app hardening (`format="json"`, `keep_alive="30m"`, `warm_up()`, `parsed` flag, `HOST` env var).
- 2026-10-06: Verified zero external requests / CDNs in source code.
- 2026-10-06: Added bingo card generator and fallback pool in `bingo_pool.json`.
- 2026-10-06: Merged species identification and square verification into single model call with `THRESHOLD = 40`.
- 2026-10-06: Tested 6 trials for photo vs square verification (100% true-positives, 0% false-positives, documented in `docs/metrics/day2-bingo.md`).
- 2026-10-06: Decided to keep synchronous flow; warm single-call latency (~10–16s) meets interaction goals without async queue complexity.

## Open questions
- None for Day 2. Ready for Day 3 field testing.
