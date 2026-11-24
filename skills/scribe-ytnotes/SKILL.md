---
name: scribe-ytnotes
description: Create video-grounded Obsidian study notes with downloaded web visuals from a YouTube video, lecture, transcript, or playlist. Use for /scribe-ytnotes or any video-to-notes request.
---

# `/scribe-ytnotes`

Input: a single video URL, lecture, or transcript (or an explicitly requested playlist); an explicit vault path if given. Follow [the video-notes format](../../docs/blueprints/formats/video-notes.md), [Command V](../../docs/procedures/authoring/command-playbooks.md#command-v--video-grounded-notes-scribe-ytnotes--scribe-notes), and [the destination gate](../../docs/procedures/authoring/pre-gen-gate.md) before any write.

**Strict overrides:** One video produces **one** self-contained Markdown note (never split by topic). Playlists produce one note per processed video (never auto-process an entire playlist from a single video link). **Do not** generate a companion experimental lab or force multi-language implementation tracks. **Do not** open, play, or capture frames from the video; instead, download and inspect multiple complementary web raster images via [representations.md](../../docs/procedures/authoring/representations.md) to illustrate the video's concepts.

Acquire the timestamped transcript once into a compact topic/evidence map, compose once using [teaching_core.md](../../core/teaching_core.md) + [math_gates.md](../../core/math_gates.md), and repair omissions locally. Review with [verification-checklist.md](../../docs/procedures/review/verification-checklist.md).
