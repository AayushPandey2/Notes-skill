# Visuals and media

Before drafting, review every substantive section: **which part would become easier to understand if the learner could see it?** Identify complementary visual opportunities throughout the file—overall structure, subcomponent, intermediate operation, mathematical behavior, result, failure case, and comparison. Avoid galleries and decorative duplication.

A visually rich substantial note often needs multiple complementary images (for example, 4–8 opportunities as a planning guide); a full lab often needs 7–10 substantive visuals, or 10–15 when complex. Treat ranges as planning prompts, not quotas or ceilings. Count downloaded web images separately from native Mermaid diagrams, Markdown tables, and video frames. A substantial, visually rich note with zero or one downloaded image requires a second review for missed opportunities.

Choose native Mermaid for flows, dependencies, decisions, sequences, and states; an inspected local raster image for geometry, function curves, distributions, apparatus, molecular structures, architectures, decision boundaries, and empirical plots; and a Markdown table for exact values, traces, comparisons, and measurements. Do not create or download SVG assets, export Mermaid to SVG, generate decorative SVGs/pictures, or build HTML viewers or rendering programs.

## Native Mermaid

Write fenced `mermaid` blocks (`flowchart TD`, `flowchart LR`, sequence, or state diagrams). State the question first, quote node labels, use meaningful edge labels and Unicode notation instead of raw LaTeX, and decode the main path, branches/loops, and connection to the lesson in prose afterward. Do not use Mermaid to replace a numerical plot, photograph, or geometry figure it cannot represent accurately. Check syntax manually; report rendering unverified until observed.

## External raster image: acquisition & verification

An image-search result, remote URL in a sample, or planned filename is not a completed image. Track `Needed → Candidate found → Source checked → Downloaded → Local image inspected → Embedded → Saved embed checked`; only the last state completes a local-image obligation.

1. **Check the source & rights.** Use available search tools to find identifiable educational, scientific, institutional, documentation, or creator sources. Open the source page, inspect the actual figure, and confirm relevance, notation, labels, and reuse/attribution rights. Honor source-only limits.
2. **Download locally.** Download a supported raster file (`.png`, `.jpg`, `.jpeg`, `.webp`) using an available download tool or standard file-download command where permitted; never write a custom downloader or script. Save with a descriptive, non-colliding filename beneath `assets/scriptorium/<collection-slug>/`. If acquisition fails, try another suitable source; if an image cannot be reproduced locally, an attributed link-only reference may help the reader, but it remains classified as link-only and does **not** satisfy a required local-image obligation.
3. **Inspect the saved file.** Open the local file in an image viewer (`read_file` or viewer) to confirm it is a valid, legible image showing the intended concept, axes, units, arrows, and legends. Never describe an unseen visual as though inspected.
4. **Embed & check.** Embed the verified vault-relative path `![[assets/scriptorium/<collection-slug>/<descriptive-name>.png]]` (or matching extension) at the point of need. Reopen the saved Markdown to confirm the embed, target file, caption, source, attribution, and narrative. Keep acquisition planning and failure logs outside polished lesson prose.

## Mandatory Six-Phase Visual Narrative

Teach every embedded figure through six connected phases:

1. **Phase 1 — Set the question (before the image, 2–5 sentences):** Establish what remains difficult to understand, what question the image answers, which features to inspect first, and any new vocabulary needed to read it.
2. **Phase 2 — Show the figure:** Place the inspected local raster embed directly at the point of need with descriptive alt text, a figure caption (**Figure N — precise idea illustrated**), source link, and attribution.
3. **Phase 3 — Decode the elements:** Immediately explain visible elements in deliberate viewing order: **orientation → axes, labels, units → colors/shapes → arrows/lines → positions → legend**. Describe arrows/regions by position and direction rather than color alone; align or bridge any notation differences explicitly.
4. **Phase 4 — Trace the change or inference:** Walk through a concrete example: **initial state → operation → intermediate state → final state → interpretation** (or trace concrete coordinates/regions on a plot, or one real input through an architecture).
5. **Phase 5 — Connect to formalism and limits:** State the general principle, equation, or mechanism the visual prepares for. Explicitly state whether the figure is **schematic, illustrative, simulated, measured, or source-provided**, and explain what it **does not prove**.
6. **Phase 6 — Check interpretation:** Pose 1–2 specific questions requiring the reader to read the figure, with reasoning in a separately positioned or collapsed answer (`> [!tip]- Answer`).

Do not replace this six-phase narrative with a caption followed by "as shown above." Keep external reference figures distinct from a lab's own experimental evidence.

## Video notes: web images & timestamps

For `/scribe-ytnotes` video notes, **do not** play the video or capture video frames. Instead, attach clickable `[MM:SS]` or `[HH:MM:SS](https://www.youtube.com/watch?v=<VIDEO_ID>&t=<seconds>s)` links to locatable transcript segments (matching URL `t=<seconds>s` and supporting hour-long videos), and acquire **multiple complementary raster web images** (`.png`, `.jpg`, `.webp`) under `assets/scriptorium/<video-id>/` using the external raster workflow above. Inspect each downloaded file (`read_file` or viewer), credit its source, and teach around it using the six-phase visual narrative.
