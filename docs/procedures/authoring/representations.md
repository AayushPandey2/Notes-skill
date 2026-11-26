# Visuals and Media

Before drafting, identify where seeing a contrast, mechanism, topology, or geometry immediately removes guesswork. Place visuals at exact **conceptual inflection points**—never dumped in a trailing gallery and never forced as decorative stock images.

## 1. Visual Source Hierarchy & Relevance Policy

Select visuals from this priority hierarchy rather than over-relying on generic web downloads when an exact representation is stronger:
1. **Supplied source figure:** Exact diagram/plot from the user's supplied material (`M2` / source-grounded notes).
2. **Exact worked-example representation:** Visual or structured representation matching the note's exact dataset, matrix, circuit, or state fixture (when supported by host tools/assets).
3. **Verified educational web raster figure:** High-clarity `.png`, `.jpg`, `.webp` acquired locally and inspected.
4. **Native Markdown table or state trace:** Inspectable discrete transitions, truth tables, or numerical traces.
5. **Attributed reference link:** When local acquisition is unavailable or restricted.

**Relevance-Governed Quantity & Source-Only Precedence:** Base visual count on distinct learning needs, not a mechanical quota (typically `3–5` complementary visuals for rich visual/geometric/empirical/video topics; `0–2` for purely algebraic or compact notes). When `source_policy = strict`, external web browsing and downloading are **disabled**—use only supplied source figures or native tables/traces. **Never use Mermaid (`mermaid` blocks), ASCII art/diagrams, SVG downloads, or custom HTML/JS plotting scripts.**

## 2. Strategic Visual Opportunities Across Disciplines

- **Electrical Engineering:** Circuit topology paired with reference directions, passive sign convention, and transient/frequency response.
- **Operating Systems & Networking:** Virtual-to-physical address/TLB/page-table mappings, process state transitions, encapsulation, and packet/handshake timelines.
- **Biology & Chemistry:** 3D molecular/enzyme structure $\to$ binding/active-site mechanism $\to$ pathway/regulation; reaction coordinate energy profiles and particle-level transitions.
- **Mathematics & Algorithms:** Geometric transformations, function + derivative pairs, constraint boundaries, and data-structure pointer/window state transitions.
- **Machine Learning Overlay:** Failure contrast (linear vs. bounded curve), foundation curves ($\ln x$), sigmoid + derivative, transformed boundaries, ROC/calibration/PR trade-offs, $L_1$/$L_2$ geometry, bias–variance/overfit panels, and prediction pipelines.

## 3. Acquisition, Inspection & Adaptive Sizing

Track `Needed -> Candidate found -> Source checked -> Downloaded -> Local image inspected -> Embedded -> Saved embed checked`.
1. **Check source & rights:** Verify identifiable educational/scientific/institutional/creator sources and reuse rights within active `source_policy`.
2. **Download locally:** Save `.png`, `.jpg`, `.jpeg`, or `.webp` with descriptive non-colliding filenames under `<Configured Target>/<Topic>/assets/` (or `assets/scriptorium/<video-id>/` for standalone `/scribe-ytnotes`) using native tools (never custom downloader scripts).
3. **Inspect before describing:** Open the saved file (`read_file` or viewer) before citing colors, axes, labels, or values; explain explicitly if an external figure uses a different dataset/notation than the running example.
4. **Embed with adaptive width:** Choose display width from legibility, intrinsic dimensions, and layout (`![[assets/<name>.png|650]]` is a sensible default, using compact widths for small symbols/components and wider widths for dense annotated circuits, graphs, or tall diagrams so labels remain crisp). Separate embed, concise 1-sentence caption, and **ordinary Markdown** attribution (`Source: [Exact Source Page Title](url). Attribution and license: <verified info>.` — zero raw HTML) with blank lines.

## 4. Diagram-to-Model Narrative & Six-Phase Visual Teaching

Teach every embedded figure in calm, takeaway-driven prose (avoid commanding phrasing like `"Inspect Figure 4"` and never overclaim what a plot proves):
1. **Set the question (1–2 sentences):** State what conceptual point the visual clarifies.
2. **Show & attribute:** Embed the inspected image, caption, and ordinary Markdown source line.
3. **Decode elements & diagram-to-model correspondence:** Connect every axis, node, branch, arrow, or curve directly to the underlying variables, equations, or physical/computational mechanism without relying on color alone, bridging any notation shifts.
4. **Trace concrete values:** Walk through specific coordinates, thresholds, or state transitions on the figure.
5. **Connect to formalism & limits:** State the governing principle, whether the data is **illustrative, simulated, measured, or source-provided**, and what the figure **does not prove**.
6. **Check interpretation:** Add a visible `> [!question] Concept Checkpoint` (nested `> > [!success]- Reveal Answer`) where visual reading requires active reasoning.
