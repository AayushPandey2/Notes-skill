# Visuals and media

Before drafting, review every concept section: **where will seeing the contrast, mechanism, or geometry immediately remove guesswork?** Place visuals at the exact **conceptual inflection point**—never dumped in a trailing gallery and never forced as decorative stock images.

## Strategic Placement Rules (Where Visuals Teach Best)

Plan **complementary visuals** across a comprehensive note or lab at these specific moments:
1. **Failure contrast:** Show the simpler alternative vs. the target concept side by side right where the simpler method breaks (e.g., unbounded straight line vs. bounded curve).
2. **Foundation curves:** Pair mathematical or physical building-block tables (such as $\ln(x)$ or exponential decay) with their curve plot so asymptotic behavior near boundaries is visible immediately.
3. **Paired function + sensitivity/derivative plots:** Show a curve alongside its rate-of-change plot to make peaks, vanishing gradients, or saturation visually obvious.
4. **Geometric & transformation pairs:** Show original space vs. transformed space (e.g., linear boundary vs. polynomial circle, or non-separable XOR vs. interaction feature) and constraint geometry (e.g., diamond vs. circular penalties).
5. **Metric, threshold & diagnostic visuals:** Pair threshold trade-offs (confusion matrix grid changes), ROC/PR ranking curves, calibration plots, and underfit/good-fit/overfit panels directly with the formulas they explain.
6. **Architecture, workflow & pipeline visuals:** Acquire clear web raster diagrams showing multi-stage prediction flows (`Inputs → Linear Score → Squashing Function → Probability → Decision`), chain-rule paths, training loops, split boundaries, or cross-validation folds.

**Mandatory Web Image Coverage & Zero-Mermaid/ASCII Rule:** Every generated content, deep, study, or video note **must** include **at least 4–5 relevant, high-clarity raster images acquired from the web** (`.png`, `.jpg`, `.webp` saved inside the topic's own `<Configured Target>/<Topic>/assets/` subfolder, or `assets/scriptorium/<video-id>/` for standalone `/scribe-ytnotes` notes), distributed across conceptual inflection points and **taught directly around each image** via the Six-Phase Visual Narrative below. **Never use Mermaid (`mermaid` blocks) or ASCII art/diagrams for graphs, charts, plots, or flows**, and never create or download SVG assets or build HTML/JS viewers. If web search or image download is unavailable in the environment, report the exact access limitation honestly rather than falling back to Mermaid or ASCII.

## External raster image: acquisition & verification

An image-search result, remote URL in a sample, or planned filename is not a completed image. Track `Needed → Candidate found → Source checked → Downloaded → Local image inspected → Embedded → Saved embed checked`; only the last state completes a local-image obligation.

1. **Check the source & rights.** Search identifiable educational, scientific, institutional, documentation, or creator sources. Open the source page, inspect the actual figure, and confirm notation, axes, labels, and reuse/attribution rights. Honor source-only limits.
2. **Download locally.** Download a supported raster file (`.png`, `.jpg`, `.jpeg`, `.webp`) using an available download tool or standard file-download command where permitted; never write a custom downloader or script. Save with a descriptive, non-colliding filename inside `<Configured Target>/<Topic>/assets/` (or `assets/scriptorium/<video-id>/` for standalone `/scribe-ytnotes` notes). If acquisition fails, try another suitable source; if an image cannot be reproduced locally, an attributed link-only reference may help the reader, but it remains classified as link-only and does **not** satisfy a required local-image obligation.
3. **Inspect the saved file.** Open the local file in an image viewer (`read_file` or viewer) before describing exact colors, positions, labels, axes, or values (also checking light/dark-background readability on fine-line diagrams). Never describe an unseen visual as though inspected, and never imply an external figure uses the same dataset as the running example unless it does—explain the relationship explicitly.
4. **Embed & check.** Embed the verified relative path with a controlled width `![[assets/<descriptive-name>.png|650]]` (650–750 px max width) right at the point of need. Separate the image embed, its concise **1-sentence caption**, and its **ordinary Markdown** source line (`Source: [Exact Source Page Title](url). Attribution and license: <verified info>.` — zero raw HTML `<span>` tags; never invent license details) with blank lines. Reopen the saved Markdown to confirm the embed, target file, caption, source, attribution, and narrative.

## Mandatory Six-Phase Visual Narrative

Teach every embedded figure naturally in calm, takeaway-driven prose—**avoid commanding phrasing** (`"Inspect Figure 4 carefully"`, `"Look at Figure 1"`) and avoid spending paragraphs narrating decorative colors or characters unrelated to the concept. Prioritize plotting the **running dataset** and core geometric/trade-off concepts rather than relying solely on unrelated external datasets, and never claim more than the image establishes (e.g., never claim visual smoothness proves better generalization, never attribute narrow regions to memorized noise from a plot alone, and never call across-tree SD bars confidence intervals):
1. **Introduce the question (1–2 sentences):** Explain what conceptual point the figure clarifies before showing it.
2. **Show the figure:** Embed the inspected local raster image with controlled width (`|650`), followed by a blank line, a concise **1-sentence caption** (`*Figure N — concise description.*`), a blank line, and `Source: [Exact Page Title](url). Attribution and license: <verified info>.`
3. **Explain the takeaway & elements:** State what the figure demonstrates conceptually, decoding axes, units, curves, or flows clearly without relying on color alone and bridging any symbol differences.
4. **Trace concrete values:** Walk through specific coordinates, thresholds, or state transitions directly on the figure.
5. **Connect to formalism & limits:** State the equation or principle the visual unlocks, whether it is **illustrative, simulated, measured, or source-provided**, and what it **does not prove**.
6. **Check interpretation:** Include a visible `> [!question] Concept Checkpoint` with a nested collapsed `> > [!success]- Reveal Answer` when reading the plot requires active reasoning.

Never replace this workflow with a detached gallery or "as shown above." Keep external reference figures clearly distinct from a lab's own experiment output.

## Video notes: web images & timestamps

For `/scribe-ytnotes` video notes, **do not** play the video or capture video frames. Attach clickable `[MM:SS]` or `[HH:MM:SS](https://www.youtube.com/watch?v=<VIDEO_ID>&t=<seconds>s)` links to locatable transcript segments (supporting hour-long videos), and acquire **multiple complementary raster web images** (`.png`, `.jpg`, `.webp`) under `assets/scriptorium/<video-id>/` using the external raster workflow and six-phase visual narrative above.
