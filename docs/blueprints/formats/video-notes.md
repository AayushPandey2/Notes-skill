# Video Notes Format (`/scribe-ytnotes`)

Use this authoritative format for `/scribe-ytnotes` and any video-to-notes request. It replaces generic textbook/collection splitting and explicitly overrides companion experimental-lab generation and mandatory multi-language implementation tracks.

## 1. Output Cardinality & Scope

- **One video → one self-contained note:** Keep all topics and demonstrations of a single video inside one Markdown file, regardless of video length (use internal headings and navigation for long videos). Never split one video into one file per concept, and **never** create an experimental lab.
- **Playlist → one note per processed video:** Only process a playlist when requested (a video belonging to a playlist does not authorize processing the whole playlist). Create one note per video preserving playlist order, previous/next links, and an optional navigation-only playlist index; identify any skipped or inaccessible videos. Never combine multiple videos into one note.

## 2. Transcript-First Processing Order

**Do not play, watch, or capture frames from the video.** Follow this exact order, loading only this workflow, [teaching_core.md](../../../core/teaching_core.md), [math_gates.md](../../../core/math_gates.md), [representations.md](../../procedures/authoring/representations.md), and source evidence:

```text
Identify video and available sources (metadata, chapters, transcript/captions)
→ Acquire timestamped transcript once
→ Build topic and compact evidence map
→ Plan multiple complementary web-image opportunities across topics
→ Download and inspect local raster web images
→ Compose once from the transcript map and inspected images
→ Repair specific omissions locally
```

- **Check capabilities once:** Identify available routes for metadata, chapters, and timestamped captions/transcripts. Record a concise `access_state` (`transcript_verified`, `transcript_partial`, or `metadata_only`), and stop probing confirmed unavailable routes. Metadata alone cannot support complete notes; mark unavailable transcripts honestly.
- **Read transcript once:** Analyze short transcripts in one pass. For long transcripts, process contiguous timestamp-preserving chunks into one compact cumulative evidence map (`| Topic interval | Main explanation | Technical details | Image need | Uncertainty |`) preserving definitions, equations, numbers, demonstrations, code identifiers, assumptions, and corrections—without creating repeated summary layers or printing raw transcripts/logs.

## 3. Source Fidelity & Content Categories

Separate three categories internally and render them naturally:
- **Video-supported content:** Claims established by accessible video narration, chapters, or official lesson companions.
- **Explanatory reconstruction:** Clearer wording, intermediate reasoning, notation breakdowns, and step-by-step interpretation of the video's material.
- **Additional context:** Prerequisite bridges, verified background, or corrections beyond the video. Label substantial added material concisely (e.g., **Additional explanation**) so it is not mistaken for the presenter's words. If the presenter makes an apparent error, preserve the source claim accurately and explain the correction separately with evidence.

## 4. Multiple Downloaded Web Images (Primary Visuals)

Instead of capturing video frames, follow [representations.md](../../procedures/authoring/representations.md) to download **relevant complementary raster web images** (typically 3–5 for rich visual/technical lectures, fewer for purely verbal/symbolic talks; `.png`, `.jpg`, `.webp`) that directly illustrate the concepts, architectures, equations, plots, or apparatus taught in the video, saved locally under `assets/scriptorium/<video-id>/<descriptive-name>.png` (disabled under `strict` source mode).

Follow [representations.md](../../procedures/authoring/representations.md) for every image: check source and reuse rights, download locally, inspect each saved file (`read_file` or viewer) before writing around it, embed the local path, add caption + source attribution (clearly identifying it as a downloaded reference image supporting the video), and teach directly around each image with **Set question → Show → Decode → Trace → Connect**. Never use Mermaid, ASCII graphs, or SVGs.

## 5. Video-Note Structure & Local Repair

1. **YAML & Title:** Standard Obsidian Properties (`topic`, `tags`, `note_type: video-notes`) + `# <Video Title>`.
2. **Source Identification & Access Status:** Concise callout with presenter/channel, video URL, duration, and `access_state`.
3. **What the Video Explains:** Brief orientation + internal topic navigation for longer videos.
4. **Timestamped Topic Sections:** Image-led, layered explanations anchored to source timestamps (`[MM:SS]` or `[HH:MM:SS](https://www.youtube.com/watch?v=<VIDEO_ID>&t=<seconds>s)`), preserving the presenter's examples, caveats, and conclusions, with `> [!example]- Understand this formula step by step` folds per [math_gates.md](../../../core/math_gates.md) and honest code reconstruction (never claiming unexecuted code ran). Never replace detailed explanations with a short summary in the name of token efficiency.
5. **Final Synthesis & Reasoning Checks:** Core takeaways + reasoning checks with separately collapsed answers (`> [!tip]- Answer`).
6. **References & Playlist Navigation:** Source link, downloaded image attributions, and previous/next playlist links when applicable.

After reviewing against [verification-checklist.md](../../procedures/review/verification-checklist.md), repair only the specific missing element without restarting the full pipeline.
