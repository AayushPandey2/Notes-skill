# Adaptive deep-notes migration

## Second-stage consolidation (Contract v3)

The adaptive instructional engine (`references/adaptive-engine.md`, `references/instructional-registry.json`, `templates/deepstudy-master.md`, and `scripts/instructional_plan.py`) is the single source of truth for all new deep-note planning, subtemplate composition, selective module activation, per-concept depth assignment (`0–5`), implementation selection, visualization selection, and validation (`contract_version: 3`).

### Separation of responsibilities

1. **Command routing (`router.md`, `plan_notes.inspect_request`):** Determines which user-requested workflow or explicit output product runs (`/scribe-deepnotes` -> `deepstudy-master`, `/scribe-notes` -> `studynotes`, `/scribe-compare` -> `comparison`, `/scribe-practice` -> `practice`, `/scribe-distill` -> `cheat-sheet`, `/scribe-atomic-notes` -> `atomic`, `/scribe-dsa` -> `dsa`, standalone paper URL -> `paper-breakdown`, standalone article/video URL -> `summary`).
2. **Instructional planning (`references/adaptive-engine.md`, `scripts/instructional_plan.py`):** Exclusively controls how a deep-study topic is taught: per-concept knowledge-type subtemplates, deduplicated subtemplate composition (`compose_concept_sequence`, `compose_document_outline`), selective module activation (`required`, `supporting`, `optional`, `excluded`), independent `0–5` depth dimensions (`math`, `code`, `visual`, `theory`, `practice`, `assessment`), prerequisite dependency graphs (`build_concept_dependency_graph`), concept-specific coding and visual selection, and source-element coverage receipts.
3. **Legacy compatibility (`scripts/legacy_contract_adapter.py`):** Isolates conversion of historical outlines and saved v1/v2 plans (`from_legacy`, `adapt_legacy_contract`) so old artifacts remain readable without allowing obsolete heuristics to influence new deep-note generation.

### Retired legacy decision-matrix artifacts

- Removed `shared/note_decision_matrix.md`, `shared/notes_decision_matrix.md`, and `templates/notes_decision_matrix.md` from the active repository after migrating all unique mathematical, coding, visual, and evidence rules into `references/adaptive-engine.md`, `shared/math_gates.md`, and `shared/authoring_rules.md`.
- Removed `select_route(purpose, impl_weight, density)` from the `/scribe-deepnotes` and `instructional_plan` planning path so deep-study subtopics are never silently switched into `api-table`, `atomic`, `cheat-sheet`, or `comparison` by legacy `impl_weight` or `density` fields.
- Removed silent `from_legacy()` fallback when a malformed `instructional_plan` is supplied; malformed plans raise actionable `ValueError` validation errors immediately.
- Removed domain-keyword math ceilings, automatic multi-framework keyword stacks, regex visual overrides, and `<!-- decision-contract: ... -->` / `shared/notes_decision_matrix.md` scaffold comments from new deep-note scaffolds.
