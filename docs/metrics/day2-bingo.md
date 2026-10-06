# Day 2 Bingo & Single-Call Verification Metrics

## Overview
- **Date:** 2026-10-06 (IST)
- **Model:** `gemma4:e4b` (100% GPU offload on RTX 3050)
- **Pipeline:** Single combined model call (Species identification + Bingo square verification)
- **Threshold for auto-verification:** `THRESHOLD = 40` confidence

## 1. Single-Call Verification Test Results
Tested 3 known photos against 1 matching square and 1 non-matching square (6 total trials):

| Image | Square Prompt | Expected | Model Verdict | Reason / Match Explanation | Latency | Pass? |
|---|---|---|---|---|---|---|
| `flower.jpg` | "a yellow flower" | MATCH | True | "The subject is a vibrant yellow sunflower." | 10.6 s | PASS |
| `flower.jpg` | "a small insect" | NON-MATCH | False | "The photo features a large sunflower plant, not a small insect or beetle." | 10.5 s | PASS |
| `insect.jpg` | "a small insect or beetle" | MATCH | True | "The photo clearly shows a small beetle." | 16.1 s | PASS |
| `insect.jpg` | "a bird" | NON-MATCH | False | "The photo shows an insect (a bug), not a bird." | 16.0 s | PASS |
| `bird.jpg` | "a bird on the ground or perched" | MATCH | True | "The bird is clearly standing on a log resting on the ground." | 17.2 s | PASS |
| `bird.jpg` | "a yellow flower" | NON-MATCH | False | "The photo shows a bird on dirt, not a yellow flower." | 16.6 s | PASS |

- **True Positive Rate:** 3 / 3 (100.0%)
- **False Positive Rate:** 0 / 3 (0.0%)
- **Accuracy:** 6 / 6 (100.0%)

## 2. Card Generation Validation (5 Settings Tested)
- Settings tested: `park`, `trail`, `campus`, `garden`, `street`.
- Generation mode: Text-only call, `temperature = 0.9`, `format = "json"`.
- Results:
  - 5 of 5 cards successfully returned exactly 9 unique, non-empty squares (<60 chars).
  - 0 safety violations (no touching, picking, climbing, eating, or private property required).
  - Variety: balanced mix of 3 living things, 3 colors/shapes, and 3 textures/patterns.
- Fallback pool validation: Simulated model failure; verified fallback to `bingo_pool.json` cleanly selects 9 random squares with `fallback: true` flag.

## 3. Storage & Overrides
- **Photo Persistence:** Every snap saved to `data/photos/<timestamp>-<rand>.jpg` and linked to `grassdex.json`.
- **Manual Override:** Verified `POST /api/bingo/override` sets square status to `done` and `override: true`.
- **Queue Decision:** Retained synchronous flow based on Day 1/2 latency measurements (~10-16s for combined vision + verification on single GPU call). Avoids background complexity while keeping interaction within field-test goals.
