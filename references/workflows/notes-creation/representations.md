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

The dependency-free validators support noninterlaced 8-bit grayscale, RGB and alpha
PNG (scanline reconstruction), sanitized UTF-8 SVG (strict element/attribute allowlist,
no `<script>`, `on*`, `href`, `DOCTYPE`, or `url()`), bounded JPEG (SOF0/SOF2/EOI),
and bounded WebP (`VP8 `/`VP8L`/`VP8X`). Limits are 8 MiB, four million pixels,
maximum dimension 10,000, ten seconds per request and three redirects. Each redirect
must remain HTTPS without credentials or alternate ports. DNS answers must all be
global public addresses; the socket connects to a validated IP with the original TLS
hostname, avoiding a second DNS resolution. HTTP status alone never establishes image validity.

`execute=False` checks saved bytes and receipts without network access or writes.
The publisher hashes all renderer artifacts and media receipts, rejects undeclared
remote Markdown images, and checks actual local image targets. Live remote
availability is observed only at acquisition; later offline validation cannot
promise continued availability. Rights and visual relevance remain editorial
review obligations, not facts inferred by the decoder.
