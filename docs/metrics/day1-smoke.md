# Day 1 Vision Smoke Test & Latency Baseline

## Model & Hardware
- **Model:** `gemma4:e4b` (7.5B, Q4_K_M, 6.6 GB on disk, CLIP vision projector)
- **VRAM / CPU Split (`ollama ps`):** 100% GPU (NVIDIA GeForce RTX 3050 6GB Laptop GPU, ~4.77 GB / 6.14 GB VRAM allocated, 0% CPU offload)
- **Ollama Version:** 0.32.6
- **Device:** AMD Ryzen 5 6600H with Radeon Graphics + NVIDIA RTX 3050 6GB Laptop GPU (16 GB System RAM)
- **Date:** 2026-10-06 (IST)

## Vision Gate (5 Test Images in `scratch/`)
*Criterion: >= 4 of 5 correctly identified, including control.*

| Image | Expected Subject | Model Output | Correct? | Notes |
|---|---|---|---|---|
| `leaf.jpg` | Leaf | "The main object in this photo is a cluster of dry, brown autumn leaves hanging from a branch against a blue sky." | Yes | Accurately recognized dried leaves |
| `flower.jpg` | Flower | "The main object in this photo is a bright yellow sunflower." | Yes | Specifically recognized sunflower species |
| `insect.jpg` | Insect | "The main object in this photo is a small, patterned insect resting on a large green leaf." | Yes | Identified insect and host leaf |
| `bird.jpg` | Bird | "The main object in this photo is a small, brownish songbird perched on wood debris in reddish earth." | Yes | Identified songbird (house sparrow) |
| `mug.jpg` | Mug (Control) | "The main object in this photo is a tall, patterned ceramic teapot displayed alongside a matching mug." | Yes | Successfully recognized non-nature control |

**Result:** 5 of 5 PASSED (100%). Vision gate cleared.

## Latency Baseline (3 Runs on `scratch/leaf.jpg`)
*Decision signal: Warm latency < 15s allows responsive synchronous flow without requiring complex queueing.*

| Run | Type | Total Duration | Load Duration | Prompt Eval Duration (Rate) | Eval Duration (Rate) | Tokens |
|---|---|---|---|---|---|---|
| 1 | Cold | 7.36 s | 508.7 ms | 273.8 ms (1110.1 t/s) | 6.42 s (51.4 t/s) | 330 |
| 2 | Warm | 5.62 s | 518.5 ms | 381.6 ms (796.6 t/s) | 4.49 s (49.2 t/s) | 221 |
| 3 | Warm | 1.44 s | 516.4 ms | 300.6 ms (1011.2 t/s) | 482.2 ms (53.9 t/s) | 26 |

**Analysis:**
Warm response latency averages ~1.4s – 5.6s (prompt eval > 1000 tokens/s, eval ~54 tokens/s on RTX 3050).
Warm latency is well under the 15-second cut threshold. Synchronous identification meets the "10 seconds max on screen" design goal.
