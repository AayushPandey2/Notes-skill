# Video Notes Format (`/scribe-ytnotes`)

Use this authoritative format for `/scribe-ytnotes` and comprehensive video-to-notes requests (`video_notes` in [master-registry.yaml](../../dispatch/master-registry.yaml)). Default artifact policy: `one_note_per_video` (overrides collection splitting and companion-lab generation unless the user explicitly requests another structure).

## 1. Output Cardinality & Scope

- **One video $\to$ one self-contained note (default):** Keep all topics of a single video inside one Markdown file using internal headings and navigation (or honor an explicit user request if they ask for another split).
- **Playlist $\to$ one note per processed video:** Process a full playlist only when requested; preserve playlist order, previous/next links, and identify skipped/inaccessible videos. Never combine multiple videos into one note.

## 2. Transcript-First Processing & Source Limits

**Do not play, watch, or capture frames from the video.** Use the [authoring pipeline](../../../core/runtime_pipeline.md) to load teaching, source and review guidance at the scale of the requested artifact.

- **Check capabilities once & record `access_state`:** Record canonical `access_state` in `{transcript_verified, transcript_partial, metadata_only}` (using `metadata_only` whenever transcripts are unavailable—kept separate from Stage 8 artifact publication states) and stop probing confirmed unavailable routes.
- **Process transcript & handle long videos cleanly:** For long transcripts, process contiguous timestamp-preserving chunks into one compact cumulative concept-coverage map (`| Topic interval | Main explanation | Technical details | Visual need | Uncertainty |`) and draft long notes in coherent staged sections rather than compressing into a shallow summary.
- **Honest transcript-only limitations:** Flag ambiguous auto-caption technical terms; reconstruct only supported equations (labeling additions); consolidate presenter repetition without losing distinctions; preserve presenter errors accurately while separating supported corrections; incorporate user-supplied screenshots or official lesson companions when provided; and **disclose silent/un-narrated diagrams, equations, or code as `[VISUAL CONTENT UNAVAILABLE IN TRANSCRIPT]` right near the affected section** rather than inventing them or implying full lecture coverage.

## 3. Conditional Visual Acquisition

Follow [the visual policy](../../procedures/authoring/representations.md) for relevant visuals permitted by the source mode. Use authorized staging, inspect every acquired image before publishing it under the topic's `assets/scriptorium/<video-id>/`, and credit it as a supplementary reference visual. If visual inspection is unavailable, omit the uninspected asset and disclose the limitation.

## 4. Video-Note Structure & Repair

1. **YAML & Title:** Standard Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type: video-notes`, plus optional `id`, `aliases`, `source_refs`) per [properties-policy.md](../../properties/properties-policy.md) + `# <Video Title>`.
2. **Source Identification & Access Status:** Concise callout with presenter/channel, video URL, duration, and `access_state`.
3. **What the Video Explains:** Brief orientation + internal clickable TOC for longer videos.
4. **Timestamped Topic Sections:** Layered explanations anchored to `[MM:SS]` or `[HH:MM:SS](https://www.youtube.com/watch?v=<VIDEO_ID>&t=<seconds>s)` links, applying [math_gates.md](../../../core/math_gates.md) to timestamped mathematical reasoning units within transcription and source permissions, and keeping honest static-review labels on any code.
5. **Final Synthesis & Reasoning Checks:** Core takeaways + reasoning checks with separately collapsed `> [!success]- Answer`.
6. **References & Playlist Navigation:** Source link, supplementary image attributions, and playlist navigation when applicable.

Publish only what the transcript and source permissions support. Omit original practice questions when additions are prohibited. Without a usable transcript, disclose the access gap and limit delivery to supported source information.
