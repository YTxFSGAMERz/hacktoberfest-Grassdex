# Offline Operation Evidence

This document proves that **Grassdex operates 100% locally with zero cloud dependencies, zero external CDNs, zero web fonts, and zero tracking**.

## 1. Network Sockets & Listeners
During active identification and bingo card generation with `gemma4:e4b`:

```text
LocalAddress  : 127.0.0.1
LocalPort     : 11434 (Ollama API)
RemoteAddress : 0.0.0.0
RemotePort    : 0
State         : Listen

LocalAddress  : 127.0.0.1
LocalPort     : 11434
RemoteAddress : 127.0.0.1
RemotePort    : 1791 (Flask process)
State         : Established

LocalAddress  : 127.0.0.1
LocalPort     : 5000 (Grassdex Flask Web App)
RemoteAddress : 0.0.0.0
RemotePort    : 0
State         : Listen
```

All established TCP connections occur strictly over `127.0.0.1` (loopback). There are **zero** outbound external connections.

## 2. Source Code Remote URL Audit
A recursive scan for `http:` and `https:` across all production application files (`app.py`, `static/index.html`, `scripts/analyze_log.py`):

```powershell
Select-String -Path "app.py", "static\index.html", "scripts\analyze_log.py" -Pattern "http:", "https:"
# Result: 0 matches found
```

- **Icons**: Inline SVG paths.
- **Fonts**: System sans-serif stack (`system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto...`).
- **Styles**: Embedded CSS in `static/index.html`.
- **Scripts**: Pure vanilla JavaScript in `static/index.html`.
- **AI Backend**: Local Ollama server bound to `127.0.0.1:11434`.

## 3. Privacy & Data Residency
- All photos captured via phone are stored locally in `data/photos/` on the laptop.
- All logs and bingo states are stored in `data/grassdex.json` and `data/bingo.json`.
- The `data/` and `scratch/` directories are listed in `.gitignore` to prevent any personal camera photos or unstripped GPS coordinates from being committed to source control.
- Sample photos provided for repo testing in `samples/` have all EXIF metadata stripped.
