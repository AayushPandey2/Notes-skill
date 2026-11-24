# Visuals and media

Before drafting, review every concept section: **where will seeing the contrast, mechanism, or geometry immediately remove guesswork?** Place visuals at the exact **conceptual inflection point**—never dumped in a trailing gallery and never forced as decorative stock images.

## Strategic Placement Rules (Where Visuals Teach Best)

Plan **complementary visuals** across a comprehensive note or lab at these specific moments:
1. **Failure contrast:** Show the simpler alternative vs. the target concept side by side right where the simpler method breaks (e.g., unbounded straight line vs. bounded curve).
2. **Foundation curves:** Pair mathematical or physical building-block tables (such as $\ln(x)$ or exponential decay) with their curve plot so asymptotic behavior near boundaries is visible immediately.
3. **Paired function + sensitivity/derivative plots:** Show a curve alongside its rate-of-change plot to make peaks, vanishing gradients, or saturation visually obvious.
4. **Geometric & transformation pairs:** Show original space vs. transformed space (e.g., linear boundary vs. polynomial circle, or non-separable XOR vs. interaction feature) and constraint geometry (e.g., diamond vs. circular penalties).
5. **Metric, threshold & diagnostic visuals:** Pair threshold trade-offs (confusion matrix grid changes), ROC/PR ranking curves, calibration plots, and underfit/good-fit/overfit panels directly with the formulas they explain.
6. **Workflow & dependency diagrams (Native Mermaid):** Use concise `flowchart` / `sequenceDiagram` blocks for multi-stage prediction flows (`Inputs → Linear Score → Squashing Function → Probability → Decision`), chain-rule paths, training loops, split boundaries, and cross-validation folds.

Count downloaded web images separately from native Mermaid diagrams, Markdown tables, and text traces. Visually rich deep notes commonly benefit from **4–8+** complementary visuals distributed across sections (planning guide, not a forced quota); recheck a long, visually rich note with zero or one downloaded raster image. Do not create or download SVG assets, export Mermaid to SVG, or build HTML/JS viewers.

## Native Mermaid

Write fenced `mermaid` blocks (`flowchart TD`, `flowchart LR`, sequence, or state diagrams). State what the flow reveals, quote node labels, use clean edge labels and Unicode symbols instead of raw LaTeX, and walk through the main path, branches, and connection to the next equation or mechanism right beneath it. Never use Mermaid to fake numerical curves, empirical plots, or photographs. Check syntax manually; report rendering unverified until observed.

## External raster image: acquisition & verification

An image-search result, remote URL in a sample, or planned filename is not a completed image. Track `Needed → Candidate found → Source checked → Downloaded → Local image inspected → Embedded → Saved embed checked`; only the last state completes a local-image obligation.

1. **Check the source & rights.** Search identifiable educational, scientific, institutional, documentation, or creator sources. Open the source page, inspect the actual figure, and confirm notation, axes, labels, and reuse/attribution rights. Honor source-only limits.
2. **Download locally.** Download a supported raster file (`.png`, `.jpg`, `.jpeg`, `.webp`) using an available download tool or standard file-download command where permitted; never write a custom downloader or script. Save with a descriptive, non-colliding filename beneath `assets/scriptorium/<collection-slug>/` (or `assets/scriptorium/<video-id>/` for video notes). If acquisition fails, try another suitable source; if an image cannot be reproduced locally, an attributed link-only reference may help the reader, but it remains classified as link-only and does **not** satisfy a required local-image obligation.
3. **Inspect the saved file.** Open the local file in an image viewer (`read_file` or viewer) to confirm it is valid, legible, and matches the concept, axes, units, arrows, and legends. Never describe an unseen visual as though inspected.
4. **Embed & check.** Embed the verified vault-relative path `![[assets/scriptorium/<collection-slug>/<descriptive-name>.png]]` (or standard relative path) right at the point of need. Reopen the saved Markdown to confirm the embed, target file, caption, source, attribution, and narrative.

## Mandatory Six-Phase Visual Narrative

Teach every embedded figure through six tight steps woven naturally into the text:
1. **Set the question (before the image, 1–3 crisp sentences):** Name what remains unclear and tell the reader what to inspect first.
2. **Show the figure:** Embed the inspected local raster image with clear alt text, **Figure N — precise idea illustrated**, source link, and attribution.
3. **Decode the elements:** Explain visible objects in deliberate viewing order (**orientation → axes/labels/units → shapes/curves → arrows/positions → legend**), describing position/direction without relying on color alone and bridging any symbol differences explicitly.
4. **Trace concrete values:** Walk through specific visible coordinates, thresholds, or state transitions (`initial → operation → after`) directly on the figure.
5. **Connect to formalism & limits:** State the equation or principle the visual unlocks, whether it is **illustrative, simulated, measured, or source-provided**, and what it **does not prove**.
6. **Check interpretation:** Include a quick visual check (`> [!tip]- Answer`) when reading the plot requires active reasoning.

Never replace this workflow with a detached gallery or "as shown above." Keep external reference figures clearly distinct from a lab's own experiment output.

## Video notes: web images & timestamps

For `/scribe-ytnotes` video notes, **do not** play the video or capture video frames. Attach clickable `[MM:SS]` or `[HH:MM:SS](https://www.youtube.com/watch?v=<VIDEO_ID>&t=<seconds>s)` links to locatable transcript segments (supporting hour-long videos), and acquire **multiple complementary raster web images** (`.png`, `.jpg`, `.webp`) under `assets/scriptorium/<video-id>/` using the external raster workflow and six-phase visual narrative above.
