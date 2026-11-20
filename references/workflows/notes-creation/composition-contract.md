# Comprehensive knowledge composition

This contract extends KCP and the existing instructional registry for full-topic
M1 notes. `/scribe-notes` remains the public command. M2–M7 and explicitly narrow
single-note requests retain their current products. Existing nested collections
can retain the legacy layout; do not migrate them implicitly.

## Planning and authoring

Use the configuration gate to establish intent, source policy, scope and audience.
Treat its legacy concept/file preview as a provisional concept inventory for full
topics. Before writing, allocate that inventory to one MOC and five subject-specific
chapters in `6 - Full Notes/<Topic>/`. No nested chapter directories, glossary note,
visual note, additional index, or internal manifest belongs in that folder.
History does not require a mathematics chapter. Keep whole derivations together.
If five chapters cannot serve the agreed scope, resolve that constraint with the
user before exceeding it. An explicitly narrow request can remain a single note.

The agent supplies a JSON specification with `topic`, `source_policy`, `chapters`,
and `concepts`. Each chapter has `id`, `title`, `concepts` (owned IDs), and optional
`sections` (required heading text). Each concept has `id`, `title`, `objectives`,
`prerequisites`, selected `capabilities` (`S01`–`S18`), optional `depth` and `signals`.
Known external prerequisites belong in `known_prerequisites`. Shared symbols belong
in `notation`. Tables and visuals can carry their specifications in the same plan.
See the executable fixture in [examples](../../../examples/adaptive-composition/README.md).

Run `python scripts/scribe.py notes compose --spec <spec.json>` to validate and
inspect the common plan. This performs no retrieval, authoring, or publication.
The registry adds capabilities to existing knowledge-type strategies rather than
replacing the six physical subtemplate documents or ten instructional strategies.

Capability dependency resolution supplies a stable order and assigns each shared
explanation stage one primary owner. Supporting capabilities contribute unique
technical obligations. Use this sequence to write continuous prose with natural
headings. Do not print internal stage labels or concatenate eighteen blocks.
Maintain the seven EIS mechanisms using this same concept plan and notation.
At difficult transitions, explicitly review missing assumptions, symbols,
intermediate steps, examples, and repeated explanations.

## Depth and research

The composition dimensions are independent: conceptual, mathematical, algorithmic,
implementation, research, visual, analytical. Ordinal levels mean: 0 omitted;
1 orientation; 2 working explanation; 3 advanced mechanics and derivation;
4 comprehensive boundaries and alternatives; 5 research-level scrutiny. These
specify obligations, not quality scores or word counts. Objective verbs provide
minimum obligations, while explicit depth and explainable difficulty, novelty,
conflict, consequence, and spatial signals can increase individual dimensions.
Revise the concept specification when reader review discovers a gap; its hash
changes and downstream validation must run again.

Legacy six-dimensional Contract v3 remains intact. In particular, the new
algorithmic dimension is no longer collapsed into its legacy theory alias.
ARRIE R0–R5 semantics and research modes remain unchanged. Use ARRIE to retrieve,
normalize and audit evidence for each pending composition obligation. A verified
assertion must include source and location, supplied-source provenance in strict
mode, primary-source status for paper analysis, and version/check date for APIs.
Contradictions block sufficiency and request escalation. Research depth is effort,
not search count; stop once relevant evidence is sufficient. Strict mode cannot
permit external retrieval even when a concept needs more verification.

The adapter accepts evidence assertions from ARRIE/reviewers. It does not fetch a
URL, prove the assertion, or replace ARRIE's source-policy and freshness checks.
Do not mark records verified merely to pass the publication gate.

## Tables and visuals

`PedagogyEngine.render_table` supports definition, variable, comparison, execution,
complexity, experimental, architecture, failure, decision, evidence, prerequisite,
and formula tables. Require an objective and prose interpretation, complete typed
columns, provenance where applicable, and comparable metrics, units and conditions.
Missing values need an explanation. Table checks detect structural and comparison
errors; they do not verify empirical values against sources.

`select_visual` maps mathematical/distribution relationships to deterministic
scientific figures; workflows/dependencies/states to Mermaid; architectures/tensors
to SVG; source figures to external retrieval; intuition to image generation; and
distinct combined objectives to hybrid composition. Declare unavailable renderers.
Exact claims require equations or reproducible data. External figures need source,
URL and rights. Never use illustrative generated pixels as mathematical evidence.
The standard-library SVG renderer supports supplied numerical series and ordered
architecture blocks, with XML checks. It does not certify tensor correctness or
Mermaid rendering. Host image tools remain optional adapters, not bundled services.

## Publication, checkpoints and repair

Author Markdown bodies keyed by chapter ID in `drafts.json`. Collect evidence keyed
by the plan's obligation IDs and four substantive review records: factual accuracy,
derivation correctness, reader simulation, and cross-chapter coherence. Reviews must
describe checks actually performed, including limits; they are not quality scores.

Run `python scripts/scribe.py notes compose --spec <spec.json> --vault <vault> --drafts <drafts.json> --evidence <evidence.json> --reviews <reviews.json> --publish`.
The CLI builds the existing KCP with the shared composition field and publishes
through E6. The entire collection is checked before writes: evidence, review records,
planned sections, unfinished markers, fences, display-math delimiters, local links,
assets, and exactly `id`, `aliases`, `topic`, `tags`, `nexttopics` in frontmatter.
The MOC contains an ordered path and concept-level Mermaid prerequisite graph.

Manifests, evidence, specifications and per-file checkpoints live under
`.scriptorium/collections/`. E6 atomic writes protect each chapter; the collection
is not a filesystem transaction. On failure, committed checkpoints remain usable
and the result reports partial failure. Identical reruns do not rewrite notes.
Changed existing chapters require reviewed expected hashes via `--expected-hashes`.
Repair only affected chapter bodies, obligations, and dependent references.
Run `python scripts/scribe.py notes compose --spec <spec.json> --vault <vault> --validate`
to recheck publication without writing. It detects modified reviewed chapters,
changed assets, a changed plan identity, and extra files inside the topic folder.

Run existing mathematical, runtime, ARRIE and pedagogical checks as appropriate
before recording reviews. Delimiter checks do not prove mathematics; nonempty
reviews do not prove good teaching. The publisher deliberately requires authored
drafts and never manufactures textbook chapters from a topic name.

## Compatibility, migration and efficiency

`notes generate` directs new M1 hierarchical collections to the composition path.
`--legacy-layout` retains the established nested collection generator. Low-level
legacy APIs remain compatible. The generic scaffolder and update command retain
their legacy Properties policy; do not use them to rewrite five-key chapters.

`VaultEngine.inventory_migration` captures full original text, hashes, code-block
counts, links and discoverable backlinks without mutating anything. Consolidation
still requires chapter mapping, preserved citations/equations/assets, backup,
coverage review and backlink repair. Originals are never automatically deleted.

Resolve only requested capabilities and their dependencies. Reuse the existing
token optimizer and ARRIE cache for source extraction, verified evidence and prompt
components. The specification hash includes source policy, notation, depth and
chapter allocation. It is an invalidation identity, not a new cache service.
Do not report model-token or retrieval savings without actual execution telemetry.
