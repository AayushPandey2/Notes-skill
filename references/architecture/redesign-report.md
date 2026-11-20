# Adaptive composition implementation report

This report describes implemented work, not completion of every acceptance
criterion in `D:\MasterPrompt.txt`. The core comprehensive composition path is
implemented and exercised. Full research-level collections for all requested
subjects and live model efficiency comparisons remain outstanding.

## A. Repository audit

The repository already had six engine facades, Contract v3, KCP, ten instructional
strategies, EIS-01–07, ARRIE, source policies, coverage and terminology registries,
atomic writes, selective prompt compilation and layered caches. These were reused.
The baseline passed **355 tests in 104.61 seconds**. Initial sandbox runs failed at
pytest's existing Windows temporary directory; the approved run passed.

The main gaps were nested concept/file allocation, generic fallback prose being
treated as finished output, incompatible frontmatter instructions, collapsed
algorithmic depth, untyped tables and missing deterministic figure artifacts.
See [audit](redesign-audit.md) and [file inventory](redesign-inventory.json).
The inventory lists purpose, dependencies, textual callers, size and disposition;
textual caller matches are an aid, not proof of dynamic runtime reachability.

## B. Actual architecture

Existing E1–E6 facades remain the public architecture. E4 delegates comprehensive
planning, independent depth and shared stage ownership to `_composition.py`, and
precise SVG generation to `_composition_visuals.py`. The existing instructional
registry owns capability declarations and common contract defaults. KCP has an
additive `composition` field. E2 exposes evidence sufficiency; E5 exposes chapter
and published-collection checks; E6 exposes publication and migration inventory.
The existing `scripts/scribe.py notes` CLI adds `compose`; no new public command
or script was introduced.

## C. Subtemplate system

These logical capabilities extend existing strategies; six physical knowledge-type
subtemplate documents remain supported. Every capability also inherits the shared
input, enrichment, compatibility, conflict, depth, output and repair contract.

| Capability | Responsibility | Dependencies |
|---|---|---|
| S01 | Definitions, motivation, intuition, prerequisites | none |
| S02 | Variables, assumptions, derivations, boundaries | S01 |
| S03 | State, invariants, traces, complexity | S01 |
| S04 | Complete code, environment, tests | S03 |
| S05 | Components, interfaces, data flow, shapes | S01 |
| S06 | Original methodology and paper contributions | S01 |
| S07 | Hypotheses, metrics, uncertainty | S01 |
| S08 | Fair criteria and comparable evidence | S01 |
| S09 | Worked calculations and interpretation | S01 |
| S10 | Causes, boundaries, diagnostics, recovery | S01 |
| S11 | Chronology, attribution, causal transitions | S01 |
| S12 | Educational visuals with precise labels | S01 |
| S13 | Typed, comparable, source-aware tables | S01 |
| S14 | Connections and qualified synthesis | S01 |
| S15 | Objective-aligned questions and answers | S01 |
| S16 | Data types, distributions, representations | S01 |
| S17 | Objectives, convergence, resource bounds | S03 |
| S18 | Requirements and operational decisions | S08 |

## D. Composition engine

The shared plan validates identities, single chapter ownership, prerequisite order
and chapter limits. Dependency resolution supplies selected capabilities in stable
order. Shared explanation stages have one primary owner, supporting contributors
and deduplicated technical obligations. For example, S04 activates S03 then S01;
adding S02 and S12 contributes mathematics and visuals to the same progression.
The author writes a continuous chapter from that plan. No concatenated template
blocks or automatic topic-name-to-textbook claims are made.

## E. Adaptive depth

Seven independent ordinal dimensions coexist with the legacy six-dimensional
contract. A `trace` objective requires algorithmic depth 3 without forcing code.
A `derive` objective requires mathematical depth 3. Conflicting evidence raises
research effort to at least 4 without raising implementation depth. A strict
source policy still prohibits external retrieval. Decisions record reasons.
Changing the specification changes its identity and requires dependent checks.

## F. Research architecture

Each selected capability produces concept-specific evidence obligations. Existing
ARRIE remains responsible for actual retrieval, normalization, citation auditing,
freshness and source evaluation. The composition adapter requires a verified
record, source, location, compatible provenance and no open contradiction. Paper
analysis requires primary evidence; API obligations need version/check information.
Pending obligations block publication; contradictions request escalation. The
adapter does not itself verify that a URL supports a statement. Evidence records
must come from actual research or explicitly identified reproducible derivations.

## G. Table Intelligence

Twelve types are implemented: definition, variable, comparison, execution,
complexity, experimental, architecture, failure, decision, evidence, prerequisite
and formula. Rendering requires populated columns, a learning objective and prose
interpretation. Comparisons reject different conditions, metrics or units. Vague,
nonfinite and unsuitable multiline values are rejected. Numerical/source truth
still requires calculation and evidence review. The gradient-descent trace and
failure table demonstrate prose integration; tests exercise incomparable metrics.

## H. Visual Intelligence

Renderer selection supports external figures, scientific curves, Mermaid, SVG,
conceptual image generation and hybrid plans. Standard-library scientific SVG and
architecture SVG renderers execute locally; XML checks reject malformed or active
content. The MOC emits native Mermaid. Three generated SVGs show quadratic
trajectories, attention interfaces and a synthetic quantization mapping.
External/image-generation/hybrid rendering requires available host adapters;
these were not executed. A full Mermaid parser/browser renderer was unavailable.

## I. Real multi-file output

The [example](../../examples/adaptive-composition/README.md) publishes:

```text
examples/adaptive-composition/vault/6 - Full Notes/Gradient Descent/
  00 - Map of Contents.md
  01 - Why Local Descent Works.md
  02 - Deriving the Update and Its Limits.md
  03 - Tracing the Algorithm.md
  04 - Implementing and Testing Descent.md
  05 - Curvature and Failure Analysis.md
```

All six notes use exactly the five requested Properties. The graph contains
concept dependencies. Assets and internal manifests are outside the topic folder.
The collection deliberately covers quadratic gradient descent, not all optimization.
Its published Python block ran, scalar closed forms were checked, boundary behavior
was tested, and the actual CLI publication and validation commands succeeded.
Identical reruns wrote no chapter files.

## J. Precision improvements

The legacy writer could reinforce an unknown M5 topic with a generic identity
function and invariant reminder. The comprehensive path requires authored chapters
and blocks missing evidence/reviews instead of treating that scaffold as completion.
The new example explains why the negative derivative is locally useful, derives
the exact multiplier, proves its stability interval, distinguishes state from loss
oscillation and states the SPD assumptions behind the eigenvalue extension.
This is a concrete content example, not a measured pedagogical superiority claim.

## K. Optimization results

[Measurements](../../examples/adaptive-composition/measurements.json) record actual
local runner timing, six output files, three figures and one executed published
Python block. The narrow capability bundle serializes to 1,115 bytes versus 20,337
bytes for all resolved capability contracts. These are JSON byte counts, not model
tokens or measured savings against the old architecture. The existing 12-workload
[optimizer benchmark](../../examples/adaptive-composition/optimizer-benchmark.json)
passed compilation checks and retained 14 verification obligations. Its token
figures use the existing estimator and synthetic eager-loading baseline; they are
not actual model usage or an attributable improvement from this redesign.

## L. Quality verification

The new suite exercises ownership and graph rejection, dependency cycles,
independent depth, policy restrictions, sufficiency/contradictions, six-file output,
exact YAML, KCP integration, preflight failures, protected targeted changes,
non-destructive migration inventory, typed comparisons, finite scientific data,
SVG XML, CLI planning, truncation, specification invalidation, dirty output folders
and resumable simulated disk failure. Repository syntax/link, authority and
registry audits pass. Both changed skills passed the skill-creator validator.
Final regression results are recorded in `validation-results.json` alongside this
report: **381 passed in 100.79 seconds**, including 26 new behavioral tests.
Deterministic checks do not replace factual or instructional review. A single
baseline/final timing pair is not evidence of a performance improvement.

## M. File changes

New: two private composition helpers, the comprehensive behavior test suite,
canonical composition contract, audit/inventory/report artifacts, and reproducible
example inputs, authored notes, assets and measurements. Modified: KCP; pedagogy,
research, quality and vault facades; the existing CLI; instructional registry;
root and note skill guidance; architecture, metadata, master and subtemplate docs.
No files were moved, merged away, deprecated or deleted. No installed global skill
or real user vault was modified. The workspace Git changes remain uncommitted.

## N. Compatibility

All seven masters, twelve variants, six knowledge-type documents, seventeen module
declarations and four public slash commands remain registered. Existing legacy
APIs remain available. New M1 hierarchical CLI generation directs authors to the
composition path; `--legacy-layout` explicitly retains nested output. Five-key
metadata is profile-specific, so legacy validators and unrelated vault metadata
are not weakened. Migration currently inventories and preserves originals.

## O. Outstanding work and acceptance status

The full master-prompt acceptance criteria are **not all met**. In particular:

- Transformer, quantization, OS and shared-research scenarios demonstrate selection
  and limited numerical/visual checks, not complete research-level chapter sets.
- No model backend, autonomous source retriever or live token/retrieval telemetry
  is bundled. The author/host agent supplies content and audited research records.
- Full proof checking, tensor validation, source-entailment verification, rendered
  Mermaid checks and measured pedagogical regression are not implemented here.
- Migration inventories text/hashes/links/backlinks; automatic lossless consolidation
  and backlink rewriting are not implemented. No originals are deleted.
- Composition-specific caching uses an invalidation identity and unchanged-file
  reuse; it does not replace or newly integrate every existing layered cache.
- The legacy interactive preview still reflects the concept inventory before the
  agent supplies its subject-specific chapter specification. It is not a complete
  automated comprehensive-plan UI.

These limits are explicit so a passing structural test suite is not mistaken for
completion of the requested research and teaching system.
