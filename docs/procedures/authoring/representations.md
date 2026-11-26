# Visuals and Media (Web-Sourced Images Only)

Before drafting—beginning during section-level curriculum discovery and concept organization—inspect every major section to decide where an existing visual will materially remove guesswork. Place retrieved visuals at exact teaching transitions alongside the relevant explanation—never waited on until the end of drafting as a single token image, never clustered only in the introduction, never dumped in a trailing gallery, and never forced as decorative stock imagery.

**Absolute Prohibition on Image Generation (Non-Negotiable):** The agent must **NEVER create, draw, or generate images under any circumstances** while authoring notes. Strictly prohibit AI-generated images/illustrations, native image-generation tools (`generate_image` or equivalent), programmatic graphs/plots (Python, Matplotlib, Plotly, or any rendering library), custom SVG diagrams, Mermaid diagrams, ASCII diagrams, HTML/CSS/JS visual generation, and redrawing/recreating existing illustrations. **All newly acquired educational images must come from existing web sources.**

## 1. Visual Specialization, Distributed Coverage & 4-Level Source Hierarchy

Select visuals according to distinct educational functions (**Structural, Sequential, Mathematical, Geometrical, Comparative, Diagnostic, Physical/Biological/Experimental, Historical/Geographical**) rather than imposing a fixed universal quota or accepting a single token image as sufficient. On visually rich comprehensive chapters, retrieve and **distribute multiple distinct web-sourced images across different relevant sections**—such as foundational intuition, math/geometry, structure, mechanisms, algorithmic steps, parameter behavior, comparisons, worked examples (where matching figures exist), limitations/failure cases, and advanced concepts. Treat a visually rich comprehensive note containing only one image as a likely educational failure requiring review.

When visuals are warranted and permitted (`source_policy != strict`), actively pursue existing web retrieval across reputable sources (**Wikimedia Commons, university educational resources, OpenStax and open textbooks, official technical documentation, established educational sites, research publications with reuse permissions, reputable scientific organizations**—preferring openly licensed and public-domain works) in this strict **4-level source hierarchy**:

1. **Supplied source figure:** Existing diagram/plot from the user's supplied material (`M2` / source-grounded notes, preserved where permitted).
2. **Verified existing educational web raster figure:** High-clarity `.png`, `.jpg`, `.jpeg`, `.webp` retrieved from reputable web sources via permitted web/download tools, with checked source, reuse rights, and attribution, and visually inspected before embedding. Never confuse an image-search result snippet, webpage URL, or thumbnail with a verified downloadable image.
3. **Clear prose, mathematics, native Markdown tables, or numerical/state traces:** Used **strictly when web image retrieval fails after query refinement or web access is unavailable/prohibited**, paired with an honest disclosure of the visual limitation (**never fall back to image generation**).
4. **Attributed reference link:** When local vault download is unavailable or restricted.

| Visual Function & Concept Type | Visual Policy |
|---|---|
| **Structural / Physical / Biological** | Retrieve an existing structure, topology, apparatus, anatomical, biological, or component diagram |
| **Mathematical & Geometrical** | Retrieve verified existing geometric partitions, curves, projections, vectors, transformations, or approximation/loss figures |
| **Sequential & Algorithmic** | Retrieve an existing flow, tree/graph, or state-transition diagram (or use a structured step trace when unavailable) |
| **Comparative & Diagnostic** | Retrieve comparative plots or error/failure contrasts when they reveal trends, tradeoffs, or misbehavior more clearly than prose |
| **Historical & Geographical** | Retrieve verified timelines, causal/spatial maps, or archival primary figures where chronology, space, or evidence governs understanding |
| **Simple definitions / verbal distinctions** | No image needed unless an existing visual resolves a misleading contrast |

**Source-Only & Forbidden Formats:** When `source_policy = strict`, external web browsing and downloading are **disabled**—use only supplied source figures or prose/tables/traces. **Never use AI/native image generation, custom SVG, Mermaid, ASCII art/diagrams, or programmatic plotting scripts.**

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

## 3. Section-Level Web Retrieval, Failure Protocol & Vault Management

Keep all image-generation prohibitions intact and pursue existing web figures actively throughout authoring via this 7-step section workflow: **(1)** identify the exact concept requiring visualization, **(2)** search reputable educational web sources using targeted queries, **(3)** inspect candidate images directly, **(4)** select the most accurate and beginner-friendly image, **(5)** verify source relevance, licensing, and reuse permissions, **(6)** download into the configured vault attachment folder when authorized, and **(7)** place beside the corresponding theoretical explanation.

### Web Image Acquisition Lifecycle
Track `Needed -> Candidate found -> Source/rights checked -> Downloaded to vault attachments (via staging where permitted) -> Local image inspected -> Embedded -> Published with accepted notes -> Saved embed checked`:
1. **Check source & rights:** Verify identifiable educational/scientific/institutional/openly licensed sources and reuse rights within active `source_policy`. Do not store downloaded educational images or evaluation assets inside the Scriptorium skill repository.
2. **Download & inspect before publication:** Where host tools permit, inspect candidate assets outside the vault first before writing accepted assets to `<Configured Target>/<Topic>/assets/` (or `assets/scriptorium/<video-id>/` for standalone `/scribe-ytnotes`), avoiding leftover unused files or empty directories and never deleting preexisting user assets. Save `.png`, `.jpg`, `.jpeg`, or `.webp` with descriptive filenames using native tools (never custom downloader scripts).
3. **Inspect before describing:** Open the saved local file visually before citing colors, axes, labels, or values; bridge any dataset/notation differences explicitly in prose.

### Image Retrieval Failure Protocol
If the initial search fails to yield a suitable existing image: **(1)** refine search terms, **(2)** search alternative terminology, **(3)** check additional reputable educational sources, and **(4)** look for an equivalent existing illustration. If no suitable existing image can be retrieved (or if web access is unavailable or prohibited), explain the concept through clear prose, mathematics, Markdown tables, or numerical examples and **disclose the significant visual limitation**—**never fall back to image generation**.

### Adaptive Width, Attribution & Multimedia Hygiene
Choose readable display width from intrinsic dimensions and layout (`![[assets/<name>.png|650]]` default; narrower for small components, wider for dense graphs/circuits). Place explanations beside the figure, keep symbols consistent with prose, never rely solely on color, omit decorative clutter, and separate embed, concise 1-sentence caption, and **ordinary Markdown** attribution (`Source: Exact Source Page Title — [Title](<verified-url>). License/attribution: <verified info>.` — zero raw HTML and never an author-created claim) with blank lines.

## 4. Visual Planning & Teaching Around Images

For each planned figure, establish in the internal plan: what concept it teaches, what relationship text alone cannot clarify well, the right representation, what the learner needs beforehand, necessary labels, adjacent placement (never in a trailing gallery, never right after a heading without framing, and never after its explanation already finished), and follow-up interpretation. Prefer distinct educational roles rather than multiple figures repeating the same point.

Teach every embedded figure in calm, takeaway-driven prose (avoid commanding phrasing like `"Inspect Figure 4"` and never overclaim what a plot proves), weaving this flexible rhythm to match visual complexity:
1. **Before the figure:** Establish the problem, relevant concept, what the figure represents, and what the reader should look for.
2. **The figure & caption:** Embed the inspected image with readable labels and appropriate width, paired with a descriptive 1-sentence caption explaining what the figure demonstrates (never merely repeating the title) and ordinary Markdown source attribution.
3. **After the figure:** Decode axes, nodes, branches, or curves directly into the underlying variables, equations, or causal mechanism (without relying on color alone and bridging notation shifts); trace concrete values/thresholds on the figure; state what is **illustrative, simulated, measured, or source-provided** plus what the figure **does not prove**; and add a visible `> [!question] Concept Checkpoint` (`> [!success]- Answer`) where visual interpretation needs active reasoning.

## 5. Strict Visual Acceptance Gate (Before Publication)

Before accepting comprehensive notes, verify: **(1)** multiple relevant sections contain distinct web-sourced visuals where appropriate (not 1 token image on a visually rich chapter), **(2)** all newly acquired images originate strictly from verified existing web sources with zero image-generation tools, AI illustrations, rendering scripts, custom SVG, Mermaid, ASCII, or redrawn figures used, **(3)** images are distributed meaningfully across the learning progression beside relevant prose with **Before / Image / Caption / After** teaching context, **(4)** important visual opportunities were not ignored without running the retrieval failure protocol, **(5)** every embedded image file actually exists at its vault path, opens readably, has valid native Obsidian embed syntax, accurate/legible labels, consistent mathematics, verified attribution/license, and non-misleading educational value, **(6)** images are not unnecessarily repeated, and **(7)** significant retrieval failures or unavailable web access are disclosed honestly. Never treat an unverified path, thumbnail/search link, or placeholder as successful visual implementation.
