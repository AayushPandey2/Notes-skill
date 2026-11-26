# Visuals and Media

Before drafting, identify where seeing a contrast, mechanism, topology, or geometry immediately removes guesswork. Place visuals at exact **conceptual inflection points**—never dumped in a trailing gallery and never forced as decorative stock images.

For each core concept in substantive notes, decide which representation makes the mechanism inspectable. Record the learning question, exact example or state, placement, and outcome in the concept plan. Give geometry and spatial transformations a figure when a suitable permitted asset can be inspected. A table may be the best representation for a discrete comparison or exact trace. When a figure is valuable but unavailable or prohibited, use a permitted fallback and disclose what it cannot show. A missing essential relationship remains a gap. Prefer complementary views that let the reader predict a changed outcome, and remove illustrations that provide no evidence for the nearby explanation.

## 1. Visual Necessity Classification & Source Hierarchy

Classify each concept by educational visual necessity rather than treating visuals as optional embellishments or forcing an arbitrary fixed count:

| Concept Type | Visual Policy |
|---|---|
| **Structural / architectural** | Normally include an appropriate structure, topology, or component diagram |
| **Geometric / spatial** | Normally include a geometric representation (partitions, margins, projections) |
| **Sequential / iterative algorithms** | Include a visual flow or state-transition diagram (or structured step trace when figures are unavailable) |
| **Mathematical functions & optimization** | Include plots or curves showing function behavior, approximations (e.g., first- vs. second-order), loss surfaces, slopes, or learning curves |
| **Quantitative relationships** | Use plots when they reveal trends, tradeoffs, or threshold behavior more clearly than a table |
| **Simple definitions / verbal distinctions** | No image needed unless it actively resolves a misleading contrast |

When visuals are educationally expected and permitted (`source_policy != strict`), actively attempt available host capabilities in priority order **before** falling back to prose, tables, or reference links—never silently emit zero visuals on a visual-heavy topic without attempting permitted acquisition or disclosing the unavailability:
1. **Supplied source figure:** Exact diagram/plot from the user's supplied material (`M2` / source-grounded notes).
2. **Exact worked-example representation:** Visual or structured representation matching the note's exact dataset, matrix, circuit, or initial state—using **host-supported native visual/diagram tools** (`generate_image` / host diagram capabilities, without creating custom plotting script engines) when available, falling back to verified external figures or native tables when unavailable.
3. **Verified educational web raster figure:** High-clarity `.png`, `.jpg`, `.webp` searched/acquired locally via permitted web/download tools and visually inspected before embedding.
4. **Native Markdown table or state trace:** Inspectable discrete transitions, truth tables, or numerical traces when visual tools are absent or restricted.
5. **Attributed reference link:** When local acquisition is unavailable or restricted.

**Relevance-Governed Quantity & Source-Only Precedence:** Base visual count on distinct learning needs, not a mechanical quota. When `source_policy = strict`, external web browsing and downloading are **disabled**—use only supplied source figures or native tables/traces. **Never use Mermaid (`mermaid` blocks), ASCII art/diagrams, SVG downloads, or custom HTML/JS plotting scripts.**

## 2. Multi-Representation Selection & Strategic Opportunities

Choose representations according to the **intellectual task** rather than defaulting to generic illustrations:

| What the Learner Must Understand | Best Representation |
|---|---|
| How a variable or loss changes | Function plot / parameter-sensitivity curve |
| How quantities interact spatially | Geometric construction / projection diagram |
| How information or requests flow | Data-flow / request-lifecycle diagram |
| How states transition | State-transition diagram or trace table |
| How an algorithm executes | Sequential worked trace |
| How components & boundaries interact | Architecture / circuit topology diagram |
| How energy or rates evolve | Reaction-coordinate / transient response curve |
| How concepts or evidence differ | Discriminating comparison / argument map |

- **Domain Visual Overlays:** *Electrical:* circuit topology + passive sign + response · *OS/Networking:* address/TLB/page-table maps, packet timelines · *Biology/Chemistry:* 3D structure/binding, pathway, energy profile · *Math/Algorithms:* transforms, function+derivative, pointer/window states · *ML:* failure contrast, foundation curves, sigmoid+derivative, ROC/calibration, $L_1$/$L_2$ geometry, bias–variance.

## 3. Acquisition, Inspection & Native-Visual Lifecycles

Keep the no-Mermaid, no-ASCII-diagram, and no-custom-plotting-script rules intact, and apply the matching lifecycle by visual source:

### Path A — External Downloaded Web Raster Figures
Track `Needed -> Candidate found -> Source checked -> Downloaded (outside final vault first where host tools permit) -> Local image inspected -> Embedded -> Published with accepted notes -> Saved embed checked`:
1. **Check source & rights:** Verify identifiable educational/scientific/institutional/creator sources and reuse rights within active `source_policy`.
2. **Download & inspect before vault publication:** Where native host tools permit, inspect candidate assets outside the final vault directory first before committing them to `<Configured Target>/<Topic>/assets/` (or `assets/scriptorium/<video-id>/` for standalone `/scribe-ytnotes`), avoiding leftover unused files or empty directories if generation is blocked. Save `.png`, `.jpg`, `.jpeg`, or `.webp` with descriptive non-colliding filenames using native tools (never custom downloader scripts, and never deleting preexisting user assets).
3. **Inspect before describing:** Open the saved file (`read_file` or viewer) before citing colors, axes, labels, or values; explain explicitly if an external figure uses a different dataset/notation than the running example.

### Path B — Host-Supported Native / Generated Mathematical Diagrams
Track `Specification defined -> Native tool rendered -> Values/labels inspected -> Attributed as author-created -> Saved embed checked`:
1. **Specify exact parameters:** Anchor axes, units, coordinates, and states to the note's actual running example before generating.
2. **Inspect rendered output:** Verify values, scale labels, geometry, and component relationships visually; disclose honestly if live visual inspection is unavailable.
3. **Attribute cleanly:** Identify the figure as an author-created illustration paired with a meaningful caption and accessible textual explanation.

### Adaptive Width & Multimedia Hygiene (Both Paths)
- Choose display width from legibility, intrinsic dimensions, and layout (`![[assets/<name>.png|650]]` default; compact for small components, wider for dense circuits/graphs). Place explanations beside the element they explain, keep labels/symbols consistent with prose, never rely exclusively on color, omit decorative visual clutter, and separate embed, concise 1-sentence caption, and **ordinary Markdown** attribution (`Source: Exact Source Page Title — <verified-url>. Attribution and license: <verified info>.` formatted as a Markdown link `[Title](<verified-url>)` using the actual verified URL, or `Source: Author-created illustration for this note's running example.` — zero raw HTML) with blank lines.

## 4. Diagram-to-Model Narrative (Scaled to Figure Complexity)

Teach every embedded figure in calm, takeaway-driven prose (avoid commanding phrasing like `"Inspect Figure 4"` and never overclaim what a plot proves), scaling narrative weight cleanly to visual complexity—a simple curve may need two clear sentences connecting axes and shape to the model, whereas a multi-stage architecture or circuit diagram warrants full element decoding, concrete tracing, and a conceptual checkpoint:
1. **Set the question (1–2 sentences):** State what conceptual point the visual clarifies.
2. **Show & attribute:** Embed the inspected image, caption, and ordinary Markdown source line.
3. **Decode elements & diagram-to-model correspondence:** Connect every axis, node, branch, arrow, or curve directly to the underlying variables, equations, or physical/computational mechanism without relying on color alone, bridging any notation shifts.
4. **Trace concrete values:** Walk through specific coordinates, thresholds, or state transitions on the figure.
5. **Connect to formalism & limits:** State the governing principle, whether the data is **illustrative, simulated, measured, or source-provided**, and what the figure **does not prove**.
6. **Check interpretation:** Add a visible `> [!question] Concept Checkpoint` (nested `> > [!success]- Reveal Answer`) where visual reading requires active reasoning.
