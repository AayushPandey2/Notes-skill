# Scriptorium 5 integration contract

The canonical plan remains `KnowledgeCollectionPlan.composition` (version 2),
built by `composition.build_composition`. The six existing engine facades and
four public commands remain the compatibility boundary. Logical A0–A10 duties
map to these owners; they are not eleven competing engines.

| Responsibility | Canonical owner | Inputs → outputs | Failure / verification |
|---|---|---|---|
| A0 orchestration | E1 orchestration | request → session, selected profile | unresolved configuration remains pending |
| A1 metadata | E3 knowledge / E6 vault | concept identity, classification → normalized nested tags | duplicate/cyclic identities and invalid tags rejected |
| A2/A3 pedagogy, allocation | E4 composition / planning | concepts, prerequisites, burden → 5–10 chapter owners | insufficient inventory or impossible scope rejected |
| A4 integrity | E2 ARRIE / composition checks | source policy, exact claims → evidence records | gaps/contradictions block consequential claims |
| A5 composition | E4 composition | shared plan, authored bodies → prepared drafts | missing deliverables remain open |
| A6 representations | E4 composition renderers/visuals/media | semantic specification → artifact, receipt, embed | unsupported backends explicitly blocked |
| A7 assessment | E4 composition contracts | objective IDs → independent hints and solutions | dangling IDs, gaps and duplicate questions rejected |
| A8 verification | E5 quality / composition contracts | exact prepared artifacts → scoped outcomes | generated never implies verified |
| A9 publication | E6 vault / composition | successful outcomes, reviewed digests → files, manifest | unsafe paths and unreviewed overwrite rejected |
| A10 optimization | E1 token optimizer | selected capabilities, dependency hashes → context/cache | relevant dependency changes invalidate results |

## Migration and ownership

- Lead owns `composition/__init__.py`, vault metadata, public CLI/docs and integration.
- Planning workstream owns `composition/planning.py` and its new tests only.
- Rendering workstream owns `composition/renderers.py`, `composition/media.py`,
  `composition/visuals.py` and its new tests only.
- Quality workstream owns `composition/contracts.py`, `composition/checks.py`
  and its new tests only.
- Existing `_composition` and `_composition_visuals` import aliases are live
  compatibility shims; keep them. Do not create duplicate KCP or research engines.

## Shared interfaces

`plan_chapters(concepts, *, known_prerequisites=())` returns
`{"chapters": [...], "rationale": {...}}`. Chapters have stable `id`, `title`,
`concepts`, `sections` and estimated workload.
Explicit chapter plans remain supported and must have 5–10 unique owners. The
planner uses only supplied concepts/objectives/depth and rejects fewer than five
substantive concepts instead of inventing padding. Lead integrates its result.

Renderer selection delegates to one registry. Existing visual result fields
remain available; `embed` carries the exact learner-facing markup, `path` a local
artifact when applicable, and remote provenance stays in internal results.
Read-only validation must never fetch remote media or create execution records.
An existing verified local snapshot supports offline checking; live availability
is established only at acquisition time, never implied by a cached receipt.

Comprehensive YAML retains exactly `id`, `aliases`, `topic`, `tags`, `nexttopics`.
Required semantic tag roots are `topic/`, `subject/`, `domain/`; existing useful
tags may coexist. Explicit classification handles unknown subjects without
pretending a generic classifier knows their parent.

## Status

Integrated: adaptive allocation, semantic metadata, twelve-family shared renderer
registry, safe remote PNG acquisition, assessment ownership and claim checks.
Independent reviews found and repaired scope routing, symbol-identity collisions,
malformed record handling and generic-only metadata acceptance. The release
report records executable acceptance evidence and remaining host limitations.
