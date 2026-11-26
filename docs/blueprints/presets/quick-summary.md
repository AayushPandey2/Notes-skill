# Preset: Verified Source Quick Summary (`M7` / `quick_summary`)

- **Parent Master:** [M7 — Synthesis & Revision](../formats/synthesis-revision.md) (`single_artifact`).
- **Activation Trigger:** `"summarize <source/URL/video>"`, standalone article/docs/video URL, or `/scribe-ytnotes` single-video summary.

## Execution Overrides
1. **Transcript-Only / Text Inputs:** Accept accessed article text, documentation pages, or **video transcript/captions** (plus user-supplied screenshots if provided—never play videos or capture frames). Disclose inaccessible bodies as `[PARTIAL SUMMARY — TRANSCRIPT/TEXT UNAVAILABLE]`.
2. **Proportional Summary Length & Verification Depth:** Scale length (`brief` 150–250 words vs. `standard` 300–500 words) and fact-checking depth to source density and user request, auditing key claims via `Claim in Source | Timestamp or Section | Verification Status | Nuance or Caveat`.
3. **Anchored Links & Follow-Ups:** Link video sections via `` `[MM:SS](https://www.youtube.com/watch?v=<VIDEO_ID>&t=<seconds>s)` `` and articles via `#section-headings`; propose `2–3` passive `/scribe-notes` follow-up topics without running generation.
