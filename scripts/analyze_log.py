#!/usr/bin/env python3
"""Summarize a Grassdex field-test log.

Usage:
    python scripts/analyze_log.py data/grassdex.json [--bingo data/bingo.json] [--out docs/metrics/field-test.md]

Each entry's "correct" field is read as:
    true -> right, false -> wrong, "close" -> close, null or missing -> unrated
"""
import argparse
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path

ABSTAIN = re.compile(r"unknown|unsure|not sure|uncertain|unclear|cannot|can't", re.I)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def wilson(k, n, z=1.96):
    """Wilson score interval for k successes out of n."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def pct(xs, q):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] if lo == hi else xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def rating(e):
    c = e.get("correct")
    if c is True:
        return "right"
    if c is False:
        return "wrong"
    if c == "close":
        return "close"
    return "unrated"


def is_abstain(e):
    conf = num(e.get("confidence"))
    return bool(ABSTAIN.search(str(e.get("name", "")))) or (conf is not None and conf <= 10)


def fmt_ci(k, n):
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {100 * k / n:.0f}% (95% CI {100 * lo:.0f}-{100 * hi:.0f}%)"


def mean_conf(entries):
    xs = [num(e.get("confidence")) for e in entries]
    xs = [x for x in xs if x is not None]
    return f"{statistics.mean(xs):.0f}" if xs else "n/a"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--bingo")
    ap.add_argument("--out")
    a = ap.parse_args()

    log = json.loads(Path(a.log).read_text(encoding="utf-8"))
    n = len(log)
    rated = [e for e in log if rating(e) != "unrated"]
    by = {r: [e for e in rated if rating(e) == r] for r in ("right", "close", "wrong")}
    right, close, wrong = len(by["right"]), len(by["close"]), len(by["wrong"])
    abstained = sum(is_abstain(e) for e in log)
    parse_fail = sum(e.get("parsed") is False for e in log)
    secs = [num(e.get("seconds")) for e in log]
    secs = [s for s in secs if s is not None]

    out = ["# Field test results", ""]
    out += ["## Accuracy", ""]
    out += [f"- Snaps logged: {n}, rated: {len(rated)}, unrated: {n - len(rated)}"]
    out += [f"- Right / close / wrong: {right} / {close} / {wrong}"]
    out += [f"- Strict accuracy (right only): {fmt_ci(right, len(rated))}"]
    out += [f"- Lenient accuracy (right or close): {fmt_ci(right + close, len(rated))}"]
    out += [f"- Abstained (unknown, unsure, or confidence 10 or less): {abstained} of {n}"]
    out += [f"- Parse failures (model output was not valid JSON): {parse_fail} of {n}", ""]

    out += ["## Confidence check", ""]
    for label in ("right", "close", "wrong"):
        out += [f"- Mean reported confidence when {label}: {mean_conf(by[label])}"]
    out += ["", "If wrong answers carry similar confidence to right ones, say that confidence is not trustworthy.", ""]

    out += ["## Latency (seconds per snap)", ""]
    if secs:
        out += [f"- Median {pct(secs, 0.5):.1f}, p90 {pct(secs, 0.9):.1f}, max {max(secs):.1f}, min {min(secs):.1f}"]
        out += [f"- First snap {secs[0]:.1f} (cold start is likely)"]
    else:
        out += ["- No timing data"]
    out += [""]

    kinds = defaultdict(list)
    for e in rated:
        kinds[e.get("kind", "other")].append(e)
    out += ["## By kind", "", "| Kind | Rated | Right | Close | Wrong | Strict accuracy |", "|---|---|---|---|---|---|"]
    for kind, es in sorted(kinds.items()):
        r = sum(rating(e) == "right" for e in es)
        c = sum(rating(e) == "close" for e in es)
        w = sum(rating(e) == "wrong" for e in es)
        out += [f"| {kind} | {len(es)} | {r} | {c} | {w} | {100 * r / len(es):.0f}% |"]
    out += [""]

    sq = [e for e in log if e.get("square") is not None]
    if sq or a.bingo:
        out += ["## Bingo", ""]
        out += [f"- Snaps checked against a square: {len(sq)}"]
        out += [f"- Model said the square matched: {sum(e.get('square_match') is True for e in sq)}"]
        if a.bingo and Path(a.bingo).exists():
            card = json.loads(Path(a.bingo).read_text(encoding="utf-8"))
            squares = card.get("squares", [])
            done = [s for s in squares if s.get("status") == "done"]
            over = [s for s in squares if s.get("override")]
            out += [f"- Squares done: {len(done)} of {len(squares)}, of which overridden by the player: {len(over)}"]
        out += [""]

    text = "\n".join(out)
    print(text)
    if a.out:
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
