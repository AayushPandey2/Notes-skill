# Scriptorium 5 implementation and release report

## 1. Executive summary

Extended the existing working architecture rather than replacing it with parallel
engines. Comprehensive composition now allocates 5–10 substantive chapters plus
a MOC, generates nested semantic tags, executes a twelve-family representation
registry through shared backends, validates remote PNG acquisition, and enforces
stricter assessment and claim integrity. Public commands and the canonical KCP
transport remain compatible. Remaining host and pedagogical limits are explicit.

## 2. Repository discovery findings

The initial branch was `NewApproach`, clean at
`6afa73164626cea525de423cd992199d4e9c2017`. Its existing `origin` uses the
`AayushPandey2/scriptorium` URL; the requested `Notes-skill` URL returned the same
branch and default-branch hashes. Both remote histories were inspected before edits.
The baseline suite passed **413 tests in 109.30 seconds**.

Existing functionality included six engine facades, seven master products, twelve
variants, six subtemplates, seventeen modules, four public commands, ARRIE research,
artifact-bound review, scoped mathematical checks, native folded assessment,
checkpointed publication, selective context and dependency-aware repair. Defects
included fixed five-chapter allocation, generic-only comprehensive tags, unavailable
external media, ignored assessment owners, unchecked contradictory/nonfinite claims,
and ordinary Markdown images bypassing asset checks. The
[inventory](scriptorium-5-inventory.json) records actual files and dependencies;
absence of a static caller was not treated as deletion evidence.

## 3. Subagent execution report

| Actual workstream | Inspected and changed scope | Verification and findings |
|---|---|---|
| `audit_architecture` | Audited models, six-engine/KCP integration, metadata, composition, instructions and tests; added `composition/planning.py`, planner tests, then scope routing in `_interactive.py` and its tests | 29 planner tests; later 139 routing/planning/lifecycle regressions. Independent CLI inventories produced 8 circuit and 6 history chapters. Found comprehensive requests defaulting to single notes, notation collisions and misleading legacy coverage status. |
| `audit_render_media` | Audited existing visual/research/publication paths; added `composition/renderers.py`, `media.py`, extended `visuals.py`, rendering/media tests and cross-domain demonstrations | 111 focused tests at handoff; actual SVG, Mermaid, table, HTML and PNG fixture checks. Nine demonstration artifacts passed offline regeneration. Found hidden arrowheads and malformed-node failure handling; both repaired. |
| `audit_quality` | Audited contracts, checks, explanation, optimizer and tests; changed `composition/contracts.py`, `checks.py`, added assessment/integrity regressions | 22 new regressions. Independent review passed 90 tests across other workstreams and published chronology/HTML/offline PNG in a temporary vault. Found invalid classification types, generic-only acceptance and malformed explicit objectives; lead repaired each. |

The lead owned shared contracts, metadata, CLI integration, asset scanning, code
version invalidation, documentation, acceptance execution, cleanup and Git release.
Workstreams had disjoint implementation ownership and read-only discovery first.
No agent self-certified the whole system. Subagent tests are intermediate evidence;
the final integrated suite is recorded separately.

## 4. Final architecture

[The ownership contract](scriptorium-5-contract.md) maps A0–A10 responsibilities
onto the six established facades. `KnowledgeCollectionPlan.composition` remains
the canonical version-2 plan: concepts, classified prerequisites, objectives,
depth, capability contributions, notation, evidence obligations, chapters,
representations, assessments and validation state share stable identities.

Data flows from request/session to concept inventory and allocation, then prepared
authored bodies, explicit evidence/reviews, scoped verification, and E6 safe writes.
Failures persist without being converted into completion. Existing `_composition`
and `_composition_visuals` modules remain live compatibility aliases.

## 5. Knowledge and metadata improvements

The shared vault generator now emits `topic/`, `subject/`, `domain/` in addition
to compatible existing tags. Comprehensive chapters derive topic tags from their
owned concepts and classification from the collection hierarchy. Explicit
`classification.subject` and `.domain` handle unknown topics. Generic-only
classification can be planned but cannot pass comprehensive publication.

```yaml
tags:
  - topic/expectation-damages
  - subject/contract-law
  - domain/law
```

The exact five-key comprehensive YAML remains `id`, `aliases`, `topic`, `tags`,
`nexttopics`. Other profiles preserve their established Properties and user metadata.
Synonyms normalize and deduplicate. KCP notation now uses exact-symbol hashes, so
case-distinct and non-ASCII symbols survive instead of overwriting one another.
Taxonomy validation checks structure and coverage; semantic classification still
needs author review.

## 6. Pedagogical improvements

Existing EIS and capability stages were retained. The conceptual-depth review
deliverable previously requested only mechanism, prerequisite bridge and limits.
It now explicitly asks for motivation, intuition, definitions, mechanism, an
appropriate worked example with intermediate reasoning, interpretation, assumptions,
relationships and a likely misconception. The authoring contract explains how to
use the relevant explanatory spine without mechanically printing thirteen headings.

For an actual worked example, the authored gradient-descent collection explains
the first-order term, derives the update, traces numerical states, executes code,
and separates observed behavior from convergence conditions. This material already
existed and was preserved; it is not presented as newly invented pedagogy.
The new workload allocation avoids compressing every topic into five files.
Legacy scaffold metadata now says `generated` and `verified: false`; file-write
completion is explicitly distinguished from educational completion.

## 7. Adaptive chapter planning

When `chapters` is absent, the planner orders the prerequisite DAG, reuses canonical
depth allocation, estimates instructional workload, and balances coherent contiguous
groups with dynamic programming. Explicit 5–10 chapter plans remain supported.
No concepts are invented; fewer than five substantive concepts require a narrower
profile or better inventory. Rationale records split/merged groups, estimates,
overloads and scope review. Units are transparent heuristics, not learning-time data.

Actual plans in [the cross-domain examples](../../examples/scriptorium-5/README.md):

| Topic | Concepts | Chapters | Scope review |
|---|---:|---:|---|
| Multivariable differential calculus | 13 | 8 | No cap warning |
| Transformer attention mechanics | 17 | 10 | Required: estimated workload exceeds the cap |
| DC resistive circuit analysis | 12 | 7 | No cap warning |
| Binary search with half-open intervals | 9 | 5 | No cap warning |
| French Revolution political transitions | 7 | 5 | No cap warning |

Publication regressions exercise 5, 6, 8 and 10 chapters with MOC/navigation,
unique ownership, strict evidence and idempotent writes. Counts 4 and 11 fail.
The narrow reminder routes to M3 and invokes no renderers or research.

## 8. Research and mathematical verification

ARRIE remains the retrieval and scientific-integrity owner. Existing exact source
locations, versions, snapshots/hashes, classifications, strict-source restrictions,
assumptions, exact polynomial checks and numerical counterexamples remain intact.
Unresolved contradictions at the claim or source now block verification.
NaN/infinite measured values and invalid uncertainty/run counts are rejected.
Strict plans prevent unsupplied remote-media acquisition before network access.

The demonstration executes scalar updates and checks boundary conditions; it does
not claim training, model inference or universal numerical proof. Its pinned
[Python isfinite source](https://docs.python.org/3.14/library/math.html#math.isfinite)
was reopened during this release and its runtime boundaries checked. Source
entailment and unrestricted mathematical proof still require identified review.

## 9. UMRIA implementation

`FAMILIES`, `KINDS` and `BACKENDS` in the renderer registry declare twelve logical
families, accepted semantic inputs, outputs, dependencies, verification, explicit
fallbacks and failure behavior. Reusable backends execute scientific plots, SVG
interfaces/masks, graphs, equal-scale coordinates, typed tables, native Mermaid,
constrained state-viewer HTML and verified PNG resources. Opportunity review,
semantic planning, execution, verification, registration and exact embedding all
use the same composition records. Hybrid parts have independent obligations.
See the [representation contract](../workflows/notes-creation/representations.md).

## 10. Visual artifacts

The new examples contain **nine actual persisted artifacts** and five galleries,
with specification/code hashes, exact embeds and offline regeneration receipts.
Binary-search states were executed and asserted: midpoints 3, 5, 4 locate index 4.
The existing gradient-descent collection was republished and read-only validated;
its displayed Python block executed, repeat publication wrote no files, and a
deliberately failed review prevented false completion.

Cross-domain galleries and plans are prepared demonstrations with open educational
obligations. They are not five fully authored textbooks. Native Mermaid is source
for the host renderer; HTML is a standalone frame viewer. Graphs show supplied
topology, and historical arrows show sequence without claiming causal proof.

## 11. Remote media

Remote image acquisition validates HTTPS, every redirect, exclusively public DNS,
pinned IP sockets with original-host TLS, MIME, byte/time/pixel limits and complete
supported PNG scanline reconstruction. Local snapshots and receipts preserve source,
rights, alternative text, relevance and acquisition time. Policies support remote
embedding, local preference and offline-only assets with explicit fallback.

Publication checks ordinary Markdown images as well as wiki embeds and hashes all
renderer artifacts/media receipts. Read-only verification performs no network
request. Tests use mocked transport and real encoded fixtures; no live remote-media
fetch, license verification or image-search session is claimed.

## 12. Assessment improvements

Questions now reject duplicate IDs, unknown chapters and unknown or cross-owner
objective references at planning time. Algorithmic, historical, causal and
experimental-design types are supported. Milestone questions require real,
unambiguous headings. Comprehensive finals retain 4–5 questions, at least three
types and objective coverage. Hints and answers remain independently folded:

```markdown
**Question:** Why must an update use the old state?

> [!hint]- Show hint
> Compare simultaneous and sequential coordinate changes.

> [!answer]- Show detailed answer
> A simultaneous update evaluates every component at the same old state.
> Updating a coordinate before evaluating the next changes the specified method.
```

Live Obsidian interaction remains untested; disclosure syntax is verified.

## 13. Repository restructuring

The existing separation already had concrete value, so it was extended in place:

```text
SKILL.md / skills/                  existing command entrypoints
scriptorium/models.py             shared identities/parsing/hashes
scriptorium/engines/               existing E1–E6 facades
  composition/
    __init__.py                   integrated planning/publication/context
    contracts.py / checks.py      obligations and scoped verification
    planning.py                   adaptive chapter allocation
    renderers.py / visuals.py     registry and artifact execution
    media.py                      acquisition/decoding/offline receipts
scripts/                          eight compatible CLI entrypoints
references/                       canonical policies and architecture records
tests/                            existing plus five new regression modules
examples/adaptive-composition/    authored end-to-end collection
examples/scriptorium-5/           domain plans, artifacts and measurements
```

## 14. Deleted and merged files

No useful runtime module was proven dead; none was removed merely to meet a cleanup
quota. Repeated comprehensive-profile paragraphs in metadata/template references
were consolidated into canonical contract links. The selector's duplicated local
kind map now delegates to the shared registry. Previous five-chapter constraints
were replaced across command help and active authoring instructions.

One tracked generated SVG with superseded renderer-version identity was removed
from the authored example and replaced by the currently referenced artifact.
An intermediate untracked render was also discarded. Compatibility aliases stay
at their old paths. Existing user vaults are never implicitly migrated or deleted.

## 15. Testing results

The integrated suite contains **564 tests**; final command results are preserved
in [release validation](scriptorium-5-validation.json). The 13-case golden evaluation,
repository connectivity/authority/registry audit and both skill validators were
also executed. Focused tests cover SSRF/redirect/DNS pinning, MIME and PNG corruption,
response/time/pixel limits, tampering, offline publication, malformed input,
classification, symbol identity, source restrictions and failed critical obligations.

One intermediate full-suite run observed the demonstration README before its JSON
targets had been written. The completed-artifact repository suite subsequently
passed all 11 tests. Another sandboxed run could not access pytest's temporary
directory; the required escalated retry passed. The final full rerun includes
regressions for nested/escaped Markdown captions and reference-style images, and
preserves both H1-only and ordinary repeated-title/section placement.

## 16. Performance measurements

The cross-domain runner measured approximately 0.18 seconds for its recorded local run,
10 renderer calls (execute plus offline checking), nine cache hits, and 9,046
artifact bytes, with zero network calls. These are actual local measurements,
not a speedup claim. The authored demo measured cold validation around 0.207
seconds and warm validation around 0.741 seconds: all 82 checks reused cache, but
disk/cache overhead was slower for this small workload. No acceleration is claimed.

Selective context loads representation guidance only for active visual concepts.
Code-version keys now include all composition modules and shared metadata logic,
normalizing text newlines across platforms. Actual provider tokens, model calls
for authoring, retrieval savings and comparative learning quality were not measured.

## 17. Compatibility results

Seven masters, four public commands, eight CLI scripts, legacy collection layout,
metadata preservation and existing import aliases remain exercised. Existing
five-chapter plans still work. Deliberately stricter behavior rejects generic-only
comprehensive tags, dangling assessment objectives, contradictory claims and
unsupported remote images. Such plans need correction rather than a silent bypass.
Legacy `complete` remains file-generation completion; generated state and
`verified: false` make its scope explicit.

## 18. Remaining limitations

- Complete independently reviewed collections were not authored in all five domains;
  those new examples verify planning and actual representations. The existing
  quadratic collection is the authored end-to-end acceptance case.
- External decoding currently supports noninterlaced 8-bit grayscale/RGB/alpha PNG.
  Other image formats and image generation need adapters. Media discovery remains
  the agent/ARRIE's job, and rights/relevance require editorial verification.
- No live Obsidian/browser/mobile/theme checks or live remote-image acquisition were
  performed. Mermaid source and HTML artifact generation do not establish host display.
- Circuit diagrams are topology, not a circuit-symbol CAD system; the HTML viewer
  steps through supplied states, not a physical equation solver.
- Workload and taxonomy inference are fallible and require scope/classification
  review. General fallback cannot pass comprehensive publication unchanged.
- Deterministic checks do not independently authenticate a reviewer's identity,
  prove arbitrary mathematics, establish source entailment or certify teaching quality.
- Legacy narrow generation still creates scaffolds requiring authored content and
  semantic review. Its status now records that distinction explicitly.

## 19. Git deployment

Target: [Notes-skill / NewApproach](https://github.com/AayushPandey2/Notes-skill/tree/NewApproach).
Runtime and regression commit: `40f17360ebbe4f17710876784e1066e206ada601`.
Release uses ordinary non-force commits/push with final remote SHA comparison.
The runtime commit, final documentation commit and confirmed remote SHA are
reported in the final delivery message; this report is included with the release.
The initial clean tree and inspected remote history are recorded above. The
release validation artifact contains the final pre-push checks. No user vault,
installed skill directory or unrelated branch is part of this release.
