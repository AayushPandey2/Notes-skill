# Composition integrity contract (KCP version 2)

This is the canonical contract for the audit-derived F01–F25 features. The older
collection-lifecycle F02–F15 names describe existing capabilities, not this audit's
numbering. Both use the existing KCP `composition` field and six E1–E6 facades.
The seven A1–A7 architectures cooperate within these owners.

## Authoring and publication

1. Resolve scope and source policy through `/scribe-notes`. Comprehensive M1 output
   uses one MOC and 5–10 chapters. Other masters and narrow products retain their
   existing layouts and source modes.
2. Supply concepts, single chapter owners, objectives, classified prerequisites,
   independent depth, selected capabilities, and applicable technical records in
   the shared composition specification. Use `notes compose --spec <spec.json>`
   to inspect executable obligations before writing chapters.
3. Author chapters. Use `notes compose --spec <spec.json> --context <concept-id>`
   for the existing selective prompt compiler with only active capabilities,
   prerequisite summaries, relevant subtemplates and verification obligations.
4. Run `notes compose --spec <spec.json> --vault <vault> --drafts <drafts.json> --prepare`.
   This renders assets and inserts declared tables and questions at owned headings.
   Its JSON `drafts` are the exact canonical chapter bodies to review; save that
   mapping for publication. Preparation does not publish Markdown chapters.
5. Perform the applicable checks and record reviews of those actual bodies. Supply
   ARRIE evidence and review receipts to `notes compose --spec <spec.json> --vault <vault> --drafts <drafts.json> --evidence <evidence.json> --reviews <reviews.json> --publish`.
6. Use `notes compose --spec <spec.json> --vault <vault> --validate` to recheck files,
   assets, source snapshots, computations, obligations and recorded review evidence.
   This operation writes nothing and cannot manufacture a missing execution record.

## Shared obligations and reviews

Each consequential objective, nonzero depth dimension, active capability, source
requirement, technical record, visual review/artifact and chapter assessment has
an obligation with `id`, `concept`, `owner`, `chapter`, `section`, `deliverable`,
`dependencies`, `verifier`, `domain`, `severity`, `status`, and `evidence`.
States are planned, ready, generated, verified, blocked, justifiably-omitted, failed.
Generation alone never establishes verification. Critical obligations cannot be
omitted; optional artifacts require a reviewed omission with a reason.

Reviews are structured objects, not strings:

```json
{
  "verifier": "reviewer identity",
  "method": "checks actually performed and the reasoning inspected",
  "result": "pass",
  "limitations": "scope and checks that were unavailable",
  "evidence": [{"chapter": "chapter-id", "hash": "SHA-256 of the prepared body", "excerpt": "exact relevant content"}]
}
```

The review file contains the four named collection reviews (`factual_accuracy`,
`derivation_correctness`, `reader_simulation`, `cross_chapter_coherence`) and an
`obligations` mapping from obligation ID to review object. Collection reviews cover
all chapters; each obligation review covers its owner. Changing a body invalidates
the corresponding reviews. A review is an identified assertion, not independently
authenticated testimony or an automatic proof of its conclusions.

The manifest records separate structural, computational, mathematical, research,
visual and educational outcomes. Every evaluated obligation includes verifier,
method, result, evidence, limitations, errors, cache usage and status history.
Failures persist under `.scriptorium/validation/` before any chapter is published.
Successful publication and per-file checkpoints live in `.scriptorium/collections/`.
Internal records never enter the five-key learner-facing YAML.

## Pedagogy, objectives and prerequisites

Prerequisites may be legacy concept IDs or objects with `id`, `classification`,
and bridge evidence. Classifications are essential, supporting, optional, covered,
assumed, missing. Internal concepts must precede dependents and have one owner;
external assumed prerequisites must be declared in `known_prerequisites`. Missing
prerequisites require a `gap`, an actual `resolved_excerpt` and, when needed, the
dependent `before` excerpt. A bridge placed after the equation fails verification.
Use the concept's `section` to place teaching within its owning chapter.

`terminology` records carry `term`, `definition`, `first_use`; definitions must
occur before use. `gaps` records diagnose missing assumptions, algebra, transitions,
undefined notation or unsupported conclusions and bind their actual resolution.
These explicit checks complement author/reader review; they do not discover every
possible undefined term or reasoning gap in arbitrary prose.

Objective context distinguishes historical tracing, algorithm execution,
derivation, causal explanation, implementation, reproduction and synthesis. An
optional `objective_kinds` mapping from stringified objective index to kind overrides
inference. Historical evolution does not activate algorithm-state depth.

## Mathematical and technical records

Records use stable IDs within their concept. Technical records also identify an
`artifact_excerpt` present in the owning chapter, connecting internal validation to
actual teaching rather than an invisible specification.

| Concept field | Required semantic contract |
|---|---|
| `proofs` | Exact claim, assumptions, domain, intermediate steps, scope, approximations and boundary conditions; each step has lhs/rhs/relation/reason |
| `information_flows` | External inputs and ordered branches: inputs/outputs, accessible/forbidden information, requirements, attention permissions, labels, readout, shared parameters and gradient owner |
| `tensors` | Name, shape/dimension bindings, dtype, role, valid range, gradient owner, indexing, padding, boundaries, tokenizer, label shift and readout |
| `examples` | Authenticity kind, state origin, artifact excerpt, and execution evidence at the claimed level |
| `implementations` | Scope level, backend and assumptions; a full training step additionally requires all input/forward/extraction/labels/loss/reduction/gradient/update/diagnostic/test stages |
| `numerical_tests` | Safe arithmetic expression, variables, expected output, exact/allclose convention and tolerances; explain a stabilizer's near-singular effect |
| `failures` | Symptom, latent property, candidate cause, diagnostic, measurement, evidence status and remediation; a symptom cannot establish a cause |
| `costs` | Tensor size, operations, activation memory, backward cost, padding, kernel, hardware, protocol and theoretical/measured classification |
| `diagnostics` | Operational measurement, controls, evidence, limits and optional actual observations or held-out linear-probe split |

Selected S02 or advanced mathematical depth requires a proof contract. S04 or
advanced implementation depth requires implementation scope; S05 requires flow;
S06 requires exact source claims; S09 requires example authenticity. Tensor-heavy
signals require tensor contracts. Declarations cannot silently bypass deliverables.

The exact verifier normalizes bounded rational polynomial identities. Other proof
steps require explicit assumptions and justification plus artifact-bound review;
unsupported symbolic identities remain blocked. Numerical counterexamples can
refute a claim. Passing samples do not prove a universal proposition. First-order
geometry cannot establish finite-update norm preservation. Singularities, empty
token axes, readout indices and stabilizer changes receive separate checks.

Execution levels distinguish written, syntax_checked, executed, unit_tested,
model_inference, training, reproduced. Evidence includes command, actual displayed
code/hash, runtime, dependencies, inputs, stdout, hardware, seed and limitations.
Model execution/reproduction additionally needs model/tokenizer revisions and
attention backend. A scalar Python execution does not establish model inference.
Validation inspects supplied execution evidence; it never executes arbitrary note
code. Use the existing runtime verifier or an authorized host runner to obtain it.

Representation diagnostics compute centered variability, norms, singular spectrum,
participation ratio, entropy-based effective dimension and optional held-out ridge
predictability for small supplied arrays. They do not establish intrinsic dimension
or causal utility. Larger matrices require a scientific backend.

## Claims and research

`claims` records include exact `text`, classification, origin, source evidence and
limits. Classes are definition, identity, proved_proposition, empirical_observation,
reported_source_claim, engineering_inference, hypothesis, speculation. Origins are
reported, derived, reproduced, inferred, hypothetical, unverified. Consequential
unverified claims block completion. Strong wording requires a scope review.

Reported claims use a versioned source ID and exact location, verification method,
status and limits, plus a vault-contained `snapshot`, its SHA-256 `hash`, and an
actual `excerpt`. The validator verifies that snapshot and excerpt; the reviewer
still determines whether the source entails the claim. Strict mode accepts only
supplied sources. ARRIE remains the retrieval, freshness, contradictions and source
evaluation owner; no duplicate research engine is introduced.

Empirical records distinguish dataset, model, adaptation, metric, protocol,
hyperparameters, model selection, run count, uncertainty, compute, location, value
and units. Missing uncertainty must be explicit as `not_reported`; do not invent
runs or error bars. SD/SE/CI and percentage points/relative percent are distinct.
Capability-level ARRIE evidence also requires claim, classification, version,
verification method and limits in addition to source/location/verified status.

## Visuals

A nonzero visual allocation or S12 requires `visual_review`: objective, learning
difficulty, representation, placement, validation, and a planned visual or a
reasoned omission. Each visual declares ID, owner concept, section, kind and
objective. Scientific plots supply named numerical series or a safe equation/grid,
axis labels, units and interpretation. Architecture and mask SVGs consume validated
flow contracts. Query rows, key columns, causal permissions, boundaries and readouts
come from the same mask builder. `hybrid` specs expand complementary `parts` into
individually obligated representations within the same section.

Every render persists selected/actual renderer, availability, attempted status,
input/code hashes, outcome, failure reason, asset path/hash and fallback under
`.scriptorium/renderers/`. Assets use immutable content-addressed names in the
shared `assets/scriptorium/` vault directory. Exact regeneration verifies SVG
content and the publisher checks its actual embed. Empirical charts require
verified comparable claim IDs and matching values. The built-in renderer rejects
error bars it cannot render. The [representation contract](../workflows/notes-creation/representations.md)
defines twelve logical families sharing bounded SVG, graph, coordinate, native
Mermaid, table, frame-viewer and remote PNG backends. Image generation and other
host adapters remain explicitly unavailable until execution support exists.
A Mermaid-to-SVG fallback requires an explicit validated flow.

## Assessments

Assessment entries carry ID, chapter, objective IDs, task type, question, useful
hint, detailed solution and placement (`chapter_end` or an actual milestone
heading). Four or five final questions require at least three task types and full
chapter objective coverage. Hints and answers use separate native folded callouts.
The manifest explicitly reports that live Obsidian Reading View, Live Preview,
keyboard, mobile, math/code and theme behavior remain untested without that host.

## Repair and optimization

`notes compose --spec <spec.json> --repair <obligation-id>` computes affected
concepts, sections, chapters, assets and unaffected files. Critical proofs, flows
and tensor corrections precede dependent expansion. Changed existing notes still
require their reviewed digests through `--expected-hashes`.

E1's existing `MultiLevelCache` owns validation caching. Keys include verifier code,
active records, prerequisite closure, prepared bodies, relevant source snapshots,
evidence and stable renderer identities. Unrelated chapters can reuse checks;
changed prerequisites invalidate dependents. Template/policy edits also invalidate
the selective-context cache. Immutable assets and identical notes are reused.
Metrics report actual checks, cache hits, file reads and elapsed time. Prompt token
figures remain estimates; actual model tokens/calls, retrieval and training cannot
be inferred from deterministic demo execution.
