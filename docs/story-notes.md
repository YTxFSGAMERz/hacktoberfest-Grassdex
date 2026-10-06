# Grassdex Story Notes

*Verbatim reflections captured across build sessions for the post narrative.*

## Day 1–2: Smoke Test, Hardware Reality, and Bingo Architecture
- **What surprised me**: I was bracing for a painful GPU/CPU split because my laptop RTX 3050 has only 6 GB VRAM and `gemma4:e4b` is 6.6 GB on disk. But Ollama allocated 4.77 GB directly into VRAM for 100% GPU offload. Pure ID latency dropped to 1.4s–5.6s warm.
- **What broke**: Trying to run interactive Ollama commands in PowerShell hung until we piped inputs properly; also, merging ID and square verification into a single prompt required strict JSON formatting (`format="json"`) so the parser wouldn't choke on conversational markdown.
- **What I'd tell a friend**: If you're building a local-first app, keep your stack dead simple. Flask + 1 HTML file + JSON files gave us zero friction. Don't add databases or React until you actually need them.

## Day 3: Outdoor Field Test and Metric Reality
- **What surprised me**: The quality of Gemma's negative explanations on bingo squares. When evaluating whether a red leaf counted as "green summer foliage", it specifically explained: *"The dominant foliage colors are red and orange, indicating autumn rather than green summer growth."* It actually looked at the scene!
- **What broke**: Scale and small subjects. A photo of tiny ants on a wood mound resulted in the model identifying *"Forest Trees"* because it latched onto the towering background. Also, model confidence is totally uncalibrated: 96% when right, 95% when flat-out wrong.
- **What I'd tell a friend**: Never trust raw model confidence without a calibration layer or human-in-the-loop fallback. That's why the manual override button on Bingo and the Right/Close/Wrong feedback loop are crucial.
