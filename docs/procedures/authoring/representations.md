# Visuals and Media

Before drafting—beginning during curriculum discovery and concept organization—actively inspect every major concept for visual-teaching opportunities where seeing a contrast, mechanism, topology, chronology, or geometry immediately removes guesswork. Place visuals at exact teaching transitions—never waited on until the end of drafting as a single token image, never dumped in a trailing gallery, and never forced as decorative stock imagery.

For each core concept in substantive notes, decide which representation makes the mechanism inspectable. Record the learning question, exact example or state, placement, and outcome in the concept plan. Give geometry and spatial transformations a figure when a suitable permitted asset can be inspected. A table may be the best representation for a discrete comparison or exact trace. When a figure is valuable but unavailable or prohibited, use a permitted fallback and disclose what it cannot show. A missing essential relationship remains a gap. Prefer complementary views that let the reader predict a changed outcome, and remove illustrations that provide no evidence for the nearby explanation.

## 1. Visual Specialization, Meaningful Coverage & Source Hierarchy

Select visuals according to their distinct educational function (**Structural, Sequential, Mathematical, Geometrical, Comparative, Diagnostic, Physical/Biological/Experimental, Historical/Geographical**) rather than treating visuals as optional embellishments, forcing an arbitrary fixed count, or treating the absence of a fixed quota as permission to emit only one decorative image on a visually rich chapter. On visually rich topics (across geometry, algorithms, optimization, neural architectures, physics, biology, circuits, or historical geography), actively include multiple complementary visuals when they illuminate genuinely distinct concepts:

| Visual Function & Concept Type | Visual Policy |
|---|---|
| **Structural / Physical / Biological** | Normally include an appropriate structure, topology, apparatus, biological, or component diagram |
| **Mathematical & Geometrical** | Normally include geometric partitions, curves, projections, vectors, transformations, or approximation/loss dynamics |
| **Sequential** | Include a flow or state-transition diagram (or structured step trace when figures are unavailable) |
| **Comparative & Diagnostic** | Use comparative plots or error/failure contrasts when they reveal trends, tradeoffs, or misbehavior more clearly than prose |
| **Historical & Geographical** | Use timelines, causal/spatial maps, or primary archival figures where chronology, space, or evidence governs understanding |
| **Simple definitions / verbal distinctions** | No image needed unless it actively resolves a misleading contrast |

When visuals are educationally expected and permitted (`source_policy != strict`), actively attempt available host capabilities in priority order **before** falling back to prose, tables, or reference links—never silently emit zero visuals or single-image token compliance on a visual-heavy topic without attempting permitted acquisition or disclosing unavailability:
1. **Supplied source figure:** Exact diagram/plot from the user's supplied material (`M2` / source-grounded notes).
2. **Exact worked-example representation:** Visual or structured representation matching the note's exact dataset, matrix, circuit, or initial state—using **host-supported native visual/diagram tools** (`generate_image` / host diagram capabilities, without creating custom plotting script engines) when available, falling back to verified external figures or native tables when unavailable.
3. **Verified educational web raster figure:** High-clarity `.png`, `.jpg`, `.webp` searched/acquired locally via permitted web/download tools and visually inspected before embedding.
4. **Native Markdown table or state trace:** Inspectable discrete transitions, truth tables, or numerical traces when visual tools are absent or restricted.
5. **Attributed reference link:** When local acquisition is unavailable or restricted.

**Relevance-Governed Quantity & Source-Only Precedence:** Base visual count on distinct learning needs, not a mechanical quota. When `source_policy = strict`, external web browsing and downloading are **disabled**—use only supplied source figures or native tables/traces. **Never use Mermaid (`mermaid` blocks), ASCII art/diagrams, SVG downloads, or custom HTML/JS plotting scripts.**

## 2. Multi-Representation Selection & Complementary Modalities

Develop consequential concepts through complementary representations where appropriate (**Verbal, Visual, Geometrical, Mathematical, Numerical, Physical, Computational**)—choosing modalities matched to the intellectual task, ensuring every representation describes the same underlying relationship, explaining the connection between them explicitly, and never forcing inappropriate representations onto a subject:

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

## 4. Visual Planning & Teaching Around Images

For each planned figure, establish in the internal plan: what concept it teaches, what relationship text alone cannot clarify well, the right representation, what the learner needs beforehand, necessary labels, adjacent placement (never in a trailing gallery, never right after a heading without framing, and never after its explanation already finished), and follow-up interpretation. Prefer distinct educational roles rather than multiple figures repeating the same point.

Teach every embedded figure in calm, takeaway-driven prose (avoid commanding phrasing like `"Inspect Figure 4"` and never overclaim what a plot proves), weaving this flexible rhythm to match visual complexity:
1. **Before the figure:** Establish the problem, relevant concept, what the figure represents, and what the reader should look for.
2. **The figure & caption:** Embed the inspected image with readable labels and appropriate width, paired with a descriptive 1-sentence caption explaining what the figure demonstrates (never merely repeating the title) and ordinary Markdown source attribution.
3. **After the figure:** Decode axes, nodes, branches, or curves directly into the underlying variables, equations, or causal mechanism (without relying on color alone and bridging notation shifts); trace concrete values/thresholds on the figure; state what is **illustrative, simulated, measured, or source-provided** plus what the figure **does not prove**; and add a visible `> [!question] Concept Checkpoint` (`> [!success]- Answer`) where visual interpretation needs active reasoning.

## 5. Visual Integrity Verification (Before Acceptance)

Before treating any embedded visual as completed, verify where host tools permit: **(1)** the image file exists at its exact saved path, **(2)** the image opens readably, **(3)** the Markdown path/link matches, **(4)** embed syntax is valid native Obsidian, **(5)** all axis/diagram labels are legible and accurate, **(6)** depicted mathematical relationships are right, **(7)** the figure aligns with the surrounding running example (or bridges any difference explicitly), **(8)** source/author attribution is accurate, **(9)** the graphic does not mislead, and **(10)** it provides distinct teaching value. Never claim successful visual implementation for an unverified path or uninspected image.
