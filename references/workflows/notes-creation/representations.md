# Representation and media contract

Load this reference only for a selected visual capability. The canonical KCP
`composition.visuals` array supplies owner `concept`, real heading `section`,
stable `id`, learning `objective` and semantic `kind`. Ask what learning difficulty
the artifact resolves before selecting a backend; optional artifacts can have
reviewed omissions, while critical failures block publication.

## Registry and backends

Programmatic SVG diagram generation is retired. Visual diagram/figure requests route to `external` (web image discovery & local raster download), `mermaid`, `table`, or `interactive` textual sequences:

| Family | Semantic purpose | Active backends |
|---|---|---|
| R1 mathematical/geometric | equations, geometry | external web figure, typed table |
| R2 scientific/statistical | distributions, measurements | external web figure, typed table |
| R3 engineering/physical | topology, signals | external web figure, native Mermaid, typed table |
| R4 computational models | architectures, interactions | external web figure, native Mermaid, typed table |
| R5 computer science | execution, software structure | external web figure, native Mermaid, table, frame viewer |
| R6 analytics | time series, comparisons | external web figure, typed table |
| R7 graphs/networks | dependencies, chronology | external web figure, native Mermaid, typed table |
| R8 spatial/structural | coordinates, connectivity | external web figure, typed table |
| R9 research/evidence | comparisons, provenance | external web figure, typed table |
| R10 interactive | supplied textual states | standalone constrained HTML frame slider |
| R11 external media | source figures & diagrams | verified downloaded raster web figure (`png`/`jpg`/`webp`) |
| R12 structured tables | definitions,traces, comparisons | existing typed Markdown table renderer |

External image candidates supply discovered `url`, original `source`, `rights`,
`alt`, and `relevance` (or `search_queries` for automated discovery via
`lavia.search_web_images`). Graphs and Mermaid diagrams use `nodes` with unique
safe IDs/labels and `edges` with known `source`/`target`. Tables wrap the existing
typed table specification under `table`. Interactive viewers use 2–200 supplied
`frames` (`label`, textual `state`), fixed JavaScript and a restrictive CSP; they
never draw diagrams or run arbitrary code.

`render_visuals` executes web-image search/download, validates bytes, inspects
image content (`media.inspect_image_content`), and inserts grounded embeds at the
owned heading. Results contain family, selected/actual backend, availability,
attempt/outcome, input/code hashes, path/hash, inspection report, elapsed time,
and scoped verification limits. Hybrid specs expand into complementary, separately
obligated parts.

## Web-image-first policy and unmet visual obligations

Programmatic SVG diagram drawing is strictly prohibited. All external visuals follow:
1. **Route 1 — Reuse:** Reuse an existing verified local asset from the collection/vault registry.
2. **Route 2 — Web Search & Accessibility Evaluation:** Generate search queries (`lavia.generate_visual_search_queries`), discover real candidates (`lavia.search_web_images`), check permissive licensing (`media.verify_license_and_rights`), and rank for beginner accessibility (`bvia.rank_image_candidates`).
3. **Route 3 — Download, Validate & Inspect:** Acquire bytes over pinned public HTTPS (`media.fetch_image`), validate format (`validate_image_bytes`), store under `assets/scriptorium/<collection-slug>/...`, inspect pixels/labels (`media.inspect_image_content`), and embed locally with attribution.
4. **Route 4 — Unmet Visual Obligation (no SVG fallback):** When no permitted suitable web image exists (`NO_IMAGE_EXISTS`, `SEARCH_UNAVAILABLE`, `RIGHTS_REJECTED`), call `lavia.record_unmet_visual_obligation`. Never generate a synthetic SVG diagram or invent a URL; report the unmet obligation honestly in validation/readiness state.

## Beginner-first visual intelligence (BVIA)

`composition/bvia.py` -> Beginner-first visual intelligence (BVIA) evaluates candidate cognitive accessibility:
(`evaluate_visual_accessibility`: `beginner_friendly`, `guided_intermediate`,
`advanced_technical`, `unsuitable`), ranks external candidates with technical accuracy
and permissive licensing as hard constraints (`rank_image_candidates`), orders
multi-figure sequences along a progressive visual ladder (`plan_progressive_visuals`,
Levels 0–6: orientation → simple conceptual → component identification → step-by-step
mechanism → technical representation → advanced integrated view → analysis), and emits
canonical visual teaching contracts (`build_visual_teaching_contract`).

Every embedded figure must follow the **`Explain -> Show -> Decode -> Connect`**
walkthrough (`compose_visual_walkthrough` / `validate_explain_show_decode_connect`):
1. **Explain:** Introduce the concept and what to inspect before the embed.
2. **Show:** Embed the verified local asset with a concise, descriptive caption.
3. **Decode:** Walk through labeled components and define every diagram abbreviation or symbol in prose.
4. **Connect:** Link the visual takeaway directly into the chapter's next mechanism or equation.

## Local-first source figures and LAVIA

`source_figure` requires discovered `url`, original `source`, `rights`, `alt` and
`relevance` (except `offline_only` with an explicit `local_fallback`). Do not invent URLs, permission or licensing conclusions. ARRIE and
available discovery tools remain the source-discovery owners; this backend
validates an actual direct resource supplied by that process.
In strict source-only plans, remote acquisition additionally requires the visual's
`origin` to be `supplied`; otherwise use a supplied local offline fallback.

`asset_policy` is `local_preferred` (default), `offline_only`, or `remote_allowed`.
LAVIA coordinates concept-level visual coverage planning, collection-organized
storage (`assets/scriptorium/<collection-slug>/<name>-<hash>.<ext>`),
attribution, and `read_file` inspection before prose composition.
All successful acquisitions create a content-addressed local snapshot and a
specification-bound `.media.json` receipt. `local_preferred` and `offline_only`
always emit local vault embeds (`![[...]]` or relative Markdown paths). Attribution
appears beside the image; provenance stays in internal receipts and the LAVIA manifest.

The dependency-free validators support 8-bit grayscale, RGB, indexed (`PLTE`), and alpha
PNG—both noninterlaced and Adam7 interlaced (scanline reconstruction)—bounded
JPEG (`SOF0`/`SOF2`/`EOI`), and bounded WebP (`VP8 `/`VP8L`/`VP8X`). SVG downloads
are rejected (`image/svg+xml` / `.svg`) for newly acquired assets. Limits are 8 MiB,
8 million pixels (`MAX_PIXELS = 8_000_000`), maximum dimension 10,000, ten seconds per
request, and three redirects. Each redirect
must remain HTTPS without credentials or alternate ports. DNS answers must all be
global public addresses; the socket connects to a validated IP with the original TLS
hostname, avoiding a second DNS resolution. HTTP status alone never establishes image validity.

`execute=False` checks saved bytes and receipts without network access or writes.
The publisher hashes all renderer artifacts and media receipts, rejects undeclared
remote Markdown images, and checks actual local image targets. Live remote
availability is observed only at acquisition; later offline validation cannot
promise continued availability. Rights and visual relevance remain editorial
review obligations, not facts inferred by the decoder.
