# Grassdex 🌿

> A zero-cloud, 100% offline nature field guide & touch-grass bingo powered by local open-weight vision models (Gemma 4).

Built for the **DEV Hacktoberfest Open-Source AI Challenge: Week 1** (*Theme: Touch Grass*).

---

## 🎯 What it does

Grassdex is designed around one core idea: **the screen should be the shortest part of an outdoor experience.**

1. **Snap over LAN:** Use your phone camera to snap a photo over your private local hotspot or home Wi-Fi.
2. **Local Vision Inference:** Your laptop running **Gemma 4** (`gemma4:e4b`) via **Ollama** identifies the living thing (plant, insect, bird, fungus) and returns a name, confidence score, and short nature fact.
3. **Touch-Grass Bingo:** A model-generated 3x3 scavenger-hunt card tailored to your setting (*park, trail, campus, garden, street*). A single model call verifies your photo against the target square.
4. **Phone Away:** Fast inference (~1.4s – 10s on local GPU) gets you the result in seconds so you can put your phone back in your pocket and enjoy the outdoors.
5. **Zero External Requests:** No APIs, no cloud tokens, no CDNs, no web fonts, and no analytics. Your photos, location, and data never leave your local machine.

---

## 🛠️ Architecture

```
Phone Browser (Camera) ──LAN HTTP──> Flask Server (Laptop) ──localhost:11434──> Ollama (gemma4:e4b)
                                            │
                                            └──> data/grassdex.json, data/bingo.json, data/photos/
```

- **Backend:** Python / Flask
- **Vision Model:** Google Gemma 4 (`gemma4:e4b`, 7.5B Q4_K_M with CLIP vision projector) via Ollama
- **Frontend:** Single vanilla HTML/CSS/JS file. Zero remote dependencies.
- **Data:** Plain JSON log files and local JPEG storage.

---

## 💻 System Requirements & Measured Performance

Tested and measured on:
- **OS:** Windows 11
- **CPU:** AMD Ryzen 5 6600H (6 cores, 12 threads)
- **GPU:** NVIDIA GeForce RTX 3050 Laptop GPU (6 GB VRAM)
- **RAM:** 16 GB System Memory
- **Python:** 3.10+ (tested on Python 3.13)
- **Ollama:** v0.32.6+ with `gemma4:e4b` model pulled

### Measured Latency Baseline
- **GPU Placement:** 100% GPU offload (allocating ~4.77 GB VRAM, 0% CPU offload)
- **Cold start:** 7.36 s
- **Warm identification latency:** 1.44 s – 5.62 s (eval rate ~54 tokens/s, prompt eval > 1,000 tokens/s)
- **Combined identification + Bingo verification:** ~10 s – 16 s in a single model call

---

## 🚀 Quickstart

### 1. Prerequisites
Install Ollama and pull the vision model:
```powershell
ollama pull gemma4:e4b
```

### 2. Clone and Setup
```powershell
git clone https://github.com/YTxFSGAMERz/hacktoberfest-Grassdex.git
cd hacktoberfest-Grassdex
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Locally (Laptop)
```powershell
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📱 Phone Hotspot Setup (Field Test)

To take Grassdex outside with your phone:
1. Turn on your phone's personal hotspot and connect your laptop to it.
2. Find your laptop's local IPv4 address:
   ```powershell
   ipconfig
   ```
3. Run Grassdex binding to all interfaces on your private hotspot network:
   ```powershell
   $env:HOST = "0.0.0.0"
   python app.py
   ```
4. Open `http://<YOUR_LAPTOP_IP>:5000` on your phone browser.
5. Tap **Snap a photo** to use your phone's native camera.

> **Security Note:** Only bind to `0.0.0.0` on a private, trusted hotspot or home Wi-Fi. Default is `127.0.0.1`.

---

## 📴 Offline Verification Proof

Grassdex runs completely disconnected from the internet:
1. Turn off your Wi-Fi or disconnect Ethernet.
2. Snap photos and generate bingo cards — all inference and logic continue operating seamlessly.
3. Check the DevTools **Network** tab: 100% of network requests stay on `localhost` or the private LAN.
4. Audited code search confirms zero external `http://` or `https://` URLs in `app.py` or `static/index.html`.

---

## 📊 Metrics & Logs

All project experiments and measurements are documented in [`docs/metrics/`](docs/metrics/):
- [`docs/metrics/day1-smoke.md`](docs/metrics/day1-smoke.md): 5-image vision gate & latency baseline.
- [`docs/metrics/day2-bingo.md`](docs/metrics/day2-bingo.md): Single-call verification accuracy (6 trials, 100% match accuracy, 0% false positives) and 5-card safety generation.
- To analyze field-test logs:
  ```powershell
  python scripts/analyze_log.py data/grassdex.json --bingo data/bingo.json --out docs/metrics/field-test.md
  ```

---

## ⚠️ Safety Disclaimer

Grassdex is designed purely for fun and appreciation of the outdoors.
- **Never touch, pick, handle, or ingest any plant, fungus, or creature.**
- **Not for foraging, edibility, medical, or wildlife-safety decisions.**
- Always observe wildlife from a safe, respectful distance.
- Stay on public paths in daylight and watch your footing.

---

## 📅 Entry Period & Commits

- **Challenge:** DEV Hacktoberfest Open-Source AI Challenge: Week 1 (Theme: Touch Grass)
- **Start Date:** October 6, 2026
- **Window:** October 5, 2026 07:00 UTC – October 11, 2026 11:59 PM PDT
- **Late Commits:** All commits fall strictly inside the Week 1 window except: **none**.

---

## 🏆 Prize Categories

- **Best Use of Gemma ($200):** Grassdex runs Google's open-weight Gemma 4 (`gemma4:e4b`) entirely on local hardware using Ollama for vision identification, JSON-structured classification, and dynamic scavenger-hunt bingo card generation.
- **Overall Challenge Submission:** Fulfills the "Touch Grass" theme by deliberately minimizing screen-time to under 10 seconds per interaction.

---

## 🤝 Credits & Acknowledgements

- **Gemma 4:** Open-weight vision-language model by Google.
- **Ollama:** Open-source local model runtime and server.
- **Flask:** Lightweight Python web server framework.
- **DEV Community & Hacktoberfest:** For the challenge and community platform.

### AI Assistance Disclosure
I used an AI coding agent for assistance with boilerplate code, script automation, and line-editing. The project architecture, testing, prompts, and verification results are authentically driven and validated.
