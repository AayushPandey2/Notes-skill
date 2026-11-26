---
name: scribe-ytnotes
description: Create video-grounded Obsidian study notes with downloaded web visuals from a YouTube video, lecture, transcript, or playlist. Use for /scribe-ytnotes or any video-to-notes request.
---

# `/scribe-ytnotes`

Input: a single video URL, lecture, or transcript (or an explicitly requested playlist); an explicit vault path if given. [video-notes.md](../../docs/blueprints/formats/video-notes.md) is the single authority for video-note structure, output cardinality (`one_note_per_video` default, honoring explicit alternate requests), transcript-first processing, honest disclosure of un-narrated visuals, and conditional web-visual acquisition.

**Never** play, watch, or capture frames from the video. Use the [root skill](../../SKILL.md) for shared restrictions and the [authoring pipeline](../../core/runtime_pipeline.md) in video mode. Activate math and visual guidance only when the transcript or requested output requires them.
