---
name: scribe-ytnotes
description: Create video-grounded Obsidian study notes with downloaded web visuals from a YouTube video, lecture, transcript, or playlist. Use for /scribe-ytnotes or any video-to-notes request.
---

# `/scribe-ytnotes`

Input: a single video URL, lecture, or transcript (or an explicitly requested playlist); an explicit vault path if given. [video-notes.md](../../docs/blueprints/formats/video-notes.md) is the single authority for video-note structure, output cardinality (`one_note_per_video` default, honoring explicit alternate requests), transcript-first processing, honest disclosure of un-narrated visuals, and conditional web-visual acquisition.

**Never** play, watch, or capture frames from the video. Follow [runtime_pipeline.md](../../core/runtime_pipeline.md) in video-ingestion mode, resolve destination via [pre-gen-gate.md](../../docs/procedures/authoring/pre-gen-gate.md), load the primary subject profile and [teaching_core.md](../../core/teaching_core.md) + [math_gates.md](../../core/math_gates.md), and review saved output against [verification-checklist.md](../../docs/procedures/review/verification-checklist.md).
