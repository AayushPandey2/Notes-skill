# Scriptorium 3.0 implementation and verification report

This change integrates the unified execution instruction, master architecture and
25 audit-derived features into the existing `/scribe-notes` composition path.
It delivers a locally executable integrity pipeline. Host-dependent checks remain
explicitly limited: live Obsidian UI, independent expert/learner review, general
proof/source entailment, external renderer adapters and model/GPU reproduction are
not certified by this implementation.

## Baseline and preserved architecture

The starting commit was `98d7e43` on `NewApproach`, with a clean working tree.
The working baseline was **381 tests passing in 98.64 seconds**. Python 3.14 lacked
pytest initially; pytest was installed in the interpreter's user environment.
PyYAML was already available. No user vault or installed skill was changed.

The repository already had E1 routing, E2 ARRIE research, E3 knowledge identity,
E4 pedagogy/composition, E5 verification, E6 vault publication, KCP lifecycle,
S01?S18 contributions, seven masters, twelve variants, six physical subtemplates,
seventeen modules and four public commands. All remain supported. The seven A
architectures are cooperating responsibilities within these existing engines.
There are no new agent engines or subject-specific LLM-JEPA requirements.

Canonical implementation owners:

- [Plan and publication](../../scriptorium/engines/composition/__init__.py): shared concept ownership/depth, preparation, KCP transport, scoped context, publication, links and checkpoint validation.
- [KCP obligations](../../scriptorium/engines/composition/contracts.py): executable educational obligations, artifact-bound reviews, assessment placement/coverage, dependency gates and repair.
- [Scoped checks](../../scriptorium/engines/composition/checks.py): proof algebra, numerical boundaries, information flow, tensors, authenticity, execution, claims, uncertainty, diagnostics and cost contracts.
- [Visual execution](../../scriptorium/engines/composition/visuals.py): numerical SVG, flow SVG, mask SVG, immutable asset cache, persisted attempts and embeds.
- [E1 optimizer](../../scriptorium/engines/_token_optimizer.py): existing selective loader/compiler and MultiLevelCache, with selected-template/policy invalidation.
- [Canonical contract](../contracts/composition-integrity.md): author-facing schema and procedures, loaded on the comprehensive path.

## A1?A7 integration map

| Architecture | Integration and actual behavior |
|---|---|
| A1 Pedagogy | Owned prerequisite graph, classifications, term-before-use checks, bridge placement, claim/failure calibration and contextual objective disambiguation; authored prose remains in chapters. |
| A2 Adaptive depth | Seven independent per-concept dimensions become deliverables; advanced math/implementation and active capabilities produce required technical contracts. |
| A3 Composition | Existing S01?S18 strategies retain shared stage ownership; tables, technical artifacts and worked examples use the same concepts/evidence rather than parallel plans. |
| A4 Visual intelligence | Opportunity review, renderer execution/failure, semantic inputs, actual immutable SVG assets, registration and Markdown embeds; hybrid specs retain separate part obligations. |
| A5 Assessment | Four/five final questions, three or more task types, objective coverage, milestone placement and independent folded hints/answers. |
| A6 Verification | Six separate outcome domains, structured artifact-bound evidence, exact/scoped computations, refusal of critical failures and dependency-aware repair. |
| A7 Optimization | Existing context compiler/cache reused; active dependencies only, content-versioned registries/policies, scoped validation cache, immutable assets and no-op chapter reruns. |

## F01?F25 implementation matrix

?Scoped? means the stated deterministic checks execute and artifact-bound review is
required; it does not imply universal natural-language understanding. The regression
IDs below refer to the named tests in [integrity regressions](../../tests/test_composition_integrity.py),
[composition lifecycle tests](../../tests/test_comprehensive_composition.py), and
[existing optimizer tests](../../tests/test_token_efficiency_optimizer.py).

| Feature | Status / canonical owner | Tests and artifact evidence | Limits |
|---|---|---|---|
| F01 Obligations | Implemented, KCP | `valid_yaml_links_and_review_strings`, `targeted_repair_closure`; manifest records objective/depth/capability/source/artifact/assessment states | Reviewer assertions are not authenticated testimony |
| F02 Concept graph | Implemented, Plan/KCP | Ownership/order/cycle regressions; ten meaningful concepts in generated MOC with canonical chapter links | Host chooses conceptual decomposition |
| F03 Gaps/bridges | Scoped, KCP | `missing_prerequisite_before_equation`, `terminology_contract`; actual bridge must precede use | Host diagnoses open-ended prose gaps and authors bridges |
| F04 Claim strength | Scoped, Checks | Exact classification/origin checks and strong-word scope review; pinned Python claim | Does not automatically extract every claim from arbitrary prose |
| F05 Proof obligations | Scoped, Checks | Tangent/finite-step counterexample, stronger-theorem rejection, exact rational polynomial identities, numerical-samples refusal; quadratic derivation | General implications require scoped review; no general theorem prover |
| F06 Failure taxonomy | Implemented, Checks | `diagnostics_cost_and_failure`; generated six-column diagnosis table and conditional cause record | Controlled measurement needed to establish causal claims |
| F07 Information flow | Implemented, Checks/Visual | `isolated_branch_cannot_read_forbidden_input`, `flow_and_mask_render`; transitive provenance and query/key mask | Explicit contracts must accurately describe the real backend |
| F08 Tensors/tokens | Scoped, Checks | `zero_predictor_tokens`; shapes, zero axes, readout, indexing, tokenizer assumptions and tensor-heavy requirement | No model tokenizer/backend is executed by the validator |
| F09 Authentic examples | Implemented, Checks | Stipulated-state refusal, execution code/hash binding; synthetic trace separately classified from executed Python | Model execution requires host evidence |
| F10 Implementation path | Implemented, Checks | Component/full-step refusal and all ten training stages; scalar example explicitly end-to-end within its narrow scope | Does not claim that scalar optimization is neural training |
| F11 Numerical boundaries | Implemented, Checks | Zero tokens, near-zero stabilizer, singular arithmetic, exact vs allclose and real executed scalar boundaries | Tolerances and domains remain explicit inputs |
| F12 Provenance | Implemented, Checks | `versioned_source_snapshot`; exact version/location/excerpt/hash and invalidation after source changes | Snapshot inclusion does not prove semantic entailment |
| F13 Empirical uncertainty | Scoped, Checks/KCP | Benchmark-without-location/uncertainty refusal; run-count/SD/SE/CI checks and comparable chart values | No invented benchmark data; built-in SVG error bars deliberately unsupported |
| F14 Visual review | Implemented, KCP | `visual_depth_without_artifact`; actual difficulty/representation/placement or reviewed omission | Host decides instructional usefulness |
| F15 Persistent execution | Implemented, Visual/Plan | `renderer_selection_without_execution`, `failed_render_attempt`; actual renderer status/hash/path plus embed | Unavailable host adapters stay blocked |
| F16 Visual semantics | Implemented, Visual/Checks | Wrong-equation series refusal; shared mask builder, flow contracts, SVG regeneration and tamper checks | Browser/theme appearance not verified |
| F17 Representation diversity | Implemented, Plan/Visual | Scientific/architecture/mask artifacts, native MOC Mermaid, typed tables and `hybrid_representation` | External images/figures remain host-adapter paths |
| F18 Assessment | Scoped, KCP | Diversity/coverage/hint/solution regressions; twenty authored questions with worked solutions | Correctness includes recorded author review, not independent learner trials |
| F19 Obsidian disclosure | Format implemented; host UI untested | Separate native `[!hint]-` and `[!answer]-` in all generated questions; explicit manifest UI limitation | Reading View, Live Preview, math/code, keyboard, mobile and theme tests require Obsidian |
| F20 Completion integrity | Implemented, KCP/Plan | Valid YAML/links with failing math refuses publication; failed/string/stale/malformed review refusal; six domain outcomes | Each outcome is limited to its actual check method |
| F21 Targeted repair | Implemented, KCP/E1 | Repair closure prioritizes proof/flow/tensor errors, regenerates dependent assets and preserves independent chapter bytes | Host supplies the corrected prose/code; no automatic expert repair |
| F22 Semantic objectives | Implemented, KCP/Plan | Historical-evolution tracing does not raise algorithm-state depth; explicit kind override | Context heuristic can be overridden by author intent |
| F23 Execution evidence | Implemented, Checks | Code/hash/runtime/dependency/input/output/hardware/seed records and execution-level refusal; displayed block actually executed | No GPU, model inference or training reproduced here |
| F24 Resource analysis | Scoped, Checks | Estimate-vs-benchmark refusal and protocol fields; generated scalar operation/storage/backward assumptions | No measured attention-kernel or equal-compute experiment |
| F25 Representation diagnostics | Implemented small-array checks, Checks | Actual norms, centered variability, singular spectrum, effective dimension and held-out ridge probe; 2D-projection overclaim refused | Finite observations, small-matrix budget; no intrinsic-rank/causal-utility certification |

## Actual generated-note and verification evidence

Run `python examples/adaptive-composition/run.py`. The repository-owned runner:

1. Executes its exact displayed Python block and independent scalar closed-form,
   zero-step, one-step, stability-boundary and finite-value assertions.
2. Prepares the trajectory renderer, registers a content-addressed scientific SVG,
   verifies regeneration and inserts its actual embed into the owning chapter.
3. Publishes a MOC plus five substantial authored chapters with exactly five YAML
   keys, ten concept owners/dependencies, twenty diverse questions, independent
   folded hints and detailed answers, typed traces and a qualified failure table.
4. Checks exact rational polynomial steps under stated quadratic assumptions and
   binds the displayed Python isfinite claim to a versioned official excerpt.
5. Reruns with no chapter writes and verifies that an intentionally failed
   mathematical review refuses a subsequent publication attempt.

Inspect [spec](../../examples/adaptive-composition/spec.json),
[prepared bodies](../../examples/adaptive-composition/drafts.json),
[evidence](../../examples/adaptive-composition/evidence.json),
[review receipts](../../examples/adaptive-composition/reviews.json),
[measurements](../../examples/adaptive-composition/measurements.json),
[successful manifest](../../examples/adaptive-composition/vault/.scriptorium/collections/col-gradient-descent.json),
[refusal evidence](../../examples/adaptive-composition/vault/.scriptorium/validation/col-gradient-descent.json),
and [persisted renderer](../../examples/adaptive-composition/vault/.scriptorium/renderers/col-gradient-descent.json).

The learner-facing sample lives in `examples/adaptive-composition/vault/6 - Full Notes/Gradient Descent/`:

- `00 - Map of Contents.md`
- `01 - Why Local Descent Works.md`
- `02 - Deriving the Update and Its Limits.md`
- `03 - Tracing the Algorithm.md`
- `04 - Implementing and Testing Descent.md`
- `05 - Curvature and Failure Analysis.md`

The content concerns exact quadratic descent, not all optimization. Existing
Transformer/quantization/OS selection examples remain selection demonstrations;
their presence does not imply complete research textbooks or experiments.
The Python excerpt was inspected at the official versioned source:
[Python 3.14 math.isfinite](https://docs.python.org/3.14/library/math.html#math.isfinite).
Other old entries in `sources.json` are historical inventory, not new verification.

## Consolidation, movement and instruction safety

The canonical composition code is now organized by responsibility:

- `_composition.py` implementation moved into `composition/__init__.py`.
- `_composition_visuals.py` implementation moved into `composition/visuals.py`.
- Shared obligations and semantic checks live in `composition/contracts.py` and
  `composition/checks.py`, with no 25-module engine proliferation.
- The two historical modules are import aliases to the canonical modules. Existing
  callers, facade methods and monkeypatch-based regression tests continue to work.
- New CLI/contract references use the canonical package where appropriate; old
  imports are compatibility paths, not duplicate policy/implementation owners.

Removed/superseded behavior was established by inspection and regression evidence:
nonempty review strings no longer satisfy publication; renderer selection cannot
stand for execution; nonzero depth/capability declarations cannot substitute for
required contracts; an ambiguous failure-table cause column is replaced by separate
latent property/candidate cause/diagnostic/evidence/remediation columns; stale
registry/template cache reuse is invalidated by content. The corresponding tests
exercise the before/after failure conditions. No rarely used master, research mode,
subtemplate, utility, existing user note or conditional renderer path was deleted.

The existing authoring and composition contracts now link one canonical integrity
contract instead of repeating all schemas. Root/command skills load it only for the
comprehensive path. Legacy metadata remains profile-specific. Duplicate root/index
list numbering and corrupt capability range punctuation were repaired.

The [per-file inventory](redesign-inventory.json) records every tracked/nonignored
file's purpose, static inbound/outbound dependencies, line/byte size, estimated
context cost and KEEP/OPTIMIZE/MOVE disposition. Static reachability alone never
licenses deletion. [Changed files](modified-files.txt) and the
[actual final repository tree](final-tree.txt) are generated from Git-visible paths.
Generated caches are excluded. Repository reorganization concerns code ownership;
existing user vault layout is not automatically migrated or deleted.
Git attributes preserve exact evidence/asset bytes and stable renderer-code line
endings across checkouts, so line-ending conversion cannot corrupt pinned hashes.

## Tests and measurements

[Validation results](validation-results.json) record exact commands, exit results,
test counts and timings for this run. Checks include full regression, all masters/
variants/subtemplates and source-only behavior, narrow/nonmathematical/programming
routes, composition/technical/visual/assessment failures, CLI preparation/publication/
validation/context/repair, inventory/link/authority/registry audit and both skill
validators. The example runner also verifies repeat publication and deliberate
false-completion refusal. The final full suite passed **413 tests in 103.19 seconds**, including 32 new behavioral regressions.

Measured example timing, cold/warm check counts, real context file reads and asset
execution are in `measurements.json`. Actual provider model tokens are unavailable;
compiler token counts are estimates. The runner makes zero model calls and zero
retrieval calls; the separate official-document inspection is not hidden in those
runner metrics. A baseline/final pytest timing pair is not an optimization claim.
This run checked 82 obligations: cold validation took 0.1881s with zero reused checks; warm validation took 0.6843s with 82 reused checks. These are uncontrolled local observations; caching correctness does not establish a runtime improvement. The selected conceptual prompt used 10 actual context file reads and 8324 estimated tokens.

No live token, learning-gain, source-retrieval, GPU or model-performance percentage
is claimed. Canonical receipt references avoid duplicating full evidence in every
validation result; receipts remain in their single review registry.

## Remaining limits and acceptance scope

The locally testable pipeline and audit regressions are implemented. Full universal
semantic certification is not possible from YAML, hashes or deterministic checks.
The host author still researches, decomposes topics, diagnoses open-ended gaps,
authors explanatory bridges and judges pedagogical correctness. Explicit records
bind those judgments to actual artifacts; they do not replace them.

General mathematical proofs and source entailment remain scoped review beyond the
supported polynomial/numerical checks. Empirical data and experimental execution
must come from actual sources/runners. External figure, image-generation and
Mermaid rasterization adapters are not bundled. Native MOC Mermaid is emitted but
not browser-tested. Scientific SVG error bars require a different capable backend.
Large representation matrices require a scientific library. Live Obsidian display,
independent expert/learner assessment and model/GPU experiments were not performed.
These limitations remain visible in manifests and gates; no full-model, universal
proof, independent review or live-UI success is claimed.
