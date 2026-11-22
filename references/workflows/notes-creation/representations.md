# Representation and media contract

Load this reference only for a selected visual capability. The canonical KCP
`composition.visuals` array supplies owner `concept`, real heading `section`,
stable `id`, learning `objective` and semantic `kind`. Ask what learning difficulty
the artifact resolves before selecting a backend; optional artifacts can have
reviewed omissions, while critical failures block publication.

## Registry and execution

`composition/renderers.py` owns `FAMILIES`, `KINDS`, `BUILTIN_BACKENDS` and
`select_representation(requirement, available=...)`. `BACKENDS` declares each
backend's accepted inputs, domains, output suffix, runtime dependencies,
verification, failure behavior and permitted explicit fallbacks. Families R1–R12 are logical
adapters over shared backends, not twelve independent engines:

| Family | Semantic purpose | Available examples |
|---|---|---|
| R1 mathematical/geometric | equations, geometry | safe numerical plot, equal-scale coordinates |
| R2 scientific/statistical | distributions, measurements | named numerical series, typed table |
| R3 engineering/physical | topology, signals | graph of circuit connections, signal plot |
| R4 AI/ML | tensors, information permissions | flow SVG, attention mask, numerical plot |
| R5 computer science | execution, software structure | graph, native Mermaid, state viewer |
| R6 analytics | time series, comparisons | plot, typed table |
| R7 graphs/networks | dependencies, chronology | directed graph, native Mermaid |
| R8 spatial/structural | coordinates, connectivity | equal-scale point/edge SVG |
| R9 research/evidence | comparisons, provenance | claim-bound plot, graph, verified PNG |
| R10 interactive | supplied states | standalone constrained HTML frame slider |
| R11 external media | source figures | verified PNG; host image generation conditional |
| R12 structured tables | definitions, traces, comparisons | existing typed Markdown table renderer |

Scientific inputs use `data` named x/y series or a bounded `equation`, `x_values`,
parameters, axis labels, units and interpretation. Graphs use `nodes` with unique
safe IDs/labels and `edges` with known `source`/`target`. Coordinates additionally
require finite x/y and units. Self-loops need another adapter. `architecture` uses
an actual validated `flow` or explicitly illustrative labeled `components`.
Native Mermaid uses the same nodes/edges; supplied arbitrary source is not executed.
Tables wrap the existing typed table specification under `table`.
Interactive viewers use 2–200 supplied `frames` (`label`, textual `state`), fixed
JavaScript and a restrictive CSP. They do not run arbitrary code or simulate physics.

`render_visuals` executes, validates and persists artifacts, then inserts exact
`embed` markup at the owned heading. Results contain family, selected/actual
backend, availability, attempt/outcome, input/code hashes, path/hash, fallback,
elapsed time and scoped verification limits. Native Mermaid is source for the
Obsidian renderer, and HTML opens as a standalone artifact. Browser appearance,
Obsidian themes and browser execution require separate host testing. Graphs
communicate supplied topology; a circuit graph does not prove electrical behavior.
Hybrid specs expand into complementary, separately obligated parts.

## Web-image-first policy and SVG fallback gate

For educational illustrations, external image discovery must occur **before** native SVG generation:
1. **Route 1 — Reuse:** Reuse an existing verified local asset from the collection/vault registry.
2. **Route 2 — Discover:** Build an `ImageResearchRequest` (`lavia.build_image_research_request`) and search via host tools for openly licensed educational figures (e.g., Wikimedia Commons, open-access papers).
3. **Route 3 — Download & validate:** Acquire, verify license (`CC0`, `CC BY`, `CC BY-SA`, etc.), validate image bytes, store under `assets/scriptorium/<collection-slug>/...`, and embed locally with caption and attribution.
4. **Route 4 — Documented fallback:** Native SVG (`svg`, `graph`, `mask`, `coordinates`) is permitted only with an explicit `fallback_gate` (`lavia.evaluate_svg_fallback_gate`) recording `SEARCH_UNAVAILABLE` (when search tools are absent) or `NO_IMAGE_EXISTS` (with attempted queries and rejection reasons). Custom numeric plots matching chapter equations/data (`scientific`) are an explicit justified exception.

## Beginner-first visual intelligence (BVIA)

`composition/bvia.py` evaluates candidate cognitive accessibility
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
LAVIA (`composition/lavia.py`) coordinates concept-level visual coverage planning,
collection-organized storage (`assets/scriptorium/<collection-slug>/<name>-<hash>.<ext>`),
canonical manifests (`assets/scriptorium/<collection-slug>/manifest.json`), SHA-256
deduplication, offline embed validation, and targeted dependency-aware repair.
All successful acquisitions create a content-addressed local snapshot and a
specification-bound `.media.json` receipt. `local_preferred` and `offline_only`
always emit local vault embeds (`![[...]]` or relative Markdown paths). Attribution
appears beside the image; provenance stays in internal receipts and the LAVIA manifest.

The dependency-free validators support 8-bit grayscale, RGB, indexed (`PLTE`), and alpha
PNG—both noninterlaced and Adam7 interlaced (scanline reconstruction)—sanitized UTF-8 SVG
(strict element/attribute allowlist, no `<script>`, `on*`, `href`, `DOCTYPE`, or `url()`),
bounded JPEG (SOF0/SOF2/EOI), and bounded WebP (`VP8 `/`VP8L`/`VP8X`). Limits are 8 MiB,
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
