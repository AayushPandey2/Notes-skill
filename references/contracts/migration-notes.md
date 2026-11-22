# Adaptive deep-notes migration

## Second-stage consolidation (Contract v3)

The adaptive instructional engine (`references/workflows/notes-creation/adaptive-engine.md`, `references/workflows/notes-creation/instructional-registry.json`, `references/templates/masters/deep-notes.md`, and `scriptorium/engines/pedagogy.py`) is the single source of truth for all new deep-note planning, subtemplate composition, selective module activation, per-concept depth assignment (`0–5`), implementation selection, visualization selection, and validation (`contract_version: 3`).

### Separation of responsibilities

1. **Command routing (`router.md`, `plan_notes.inspect_request`):** Determines which user-requested workflow or explicit output product runs (`/scribe-deepnotes` -> `deepstudy-master`, `/scribe-notes` -> `studynotes`, `/scribe-compare` -> `comparison`, `/scribe-practice` -> `practice`, `/scribe-distill` -> `cheat-sheet`, `/scribe-atomic-notes` -> `atomic`, `/scribe-dsa` -> `dsa`, standalone paper URL -> `paper-breakdown`, standalone article/video URL -> `summary`).
2. **Instructional planning (`references/workflows/notes-creation/adaptive-engine.md`, `scriptorium/engines/pedagogy.py`):** Exclusively controls how a deep-study topic is taught: per-concept knowledge-type subtemplates, deduplicated subtemplate composition (`compose_concept_sequence`, `compose_document_outline`), selective module activation (`required`, `supporting`, `optional`, `excluded`), independent `0–5` depth dimensions (`math`, `code`, `visual`, `theory`, `practice`, `assessment`), prerequisite dependency graphs (`build_concept_dependency_graph`), concept-specific coding and visual selection, and source-element coverage receipts.
3. **Legacy compatibility (`scriptorium/engines/_instructional.py`):** Isolates conversion of historical outlines and saved v1/v2 plans (`from_legacy`, `adapt_legacy_contract`) so old artifacts remain readable without allowing obsolete heuristics to influence new deep-note generation.

### Retired legacy decision-matrix artifacts

- Removed the legacy decision-matrix specs (`shared/note_decision_matrix.md`, `shared/notes_decision_matrix.md`, and the retired top-level `notes_decision_matrix.md`) from the active repository after migrating all unique mathematical, coding, visual, and evidence rules into `references/workflows/notes-creation/adaptive-engine.md`, `shared/math_gates.md`, and `shared/authoring_rules.md`.
- Removed `select_route(purpose, impl_weight, density)` from the `/scribe-deepnotes` and `instructional_plan` planning path so deep-study subtopics are never silently switched into `api-table`, `atomic`, `cheat-sheet`, or `comparison` by legacy `impl_weight` or `density` fields.
- Removed silent `from_legacy()` fallback when a malformed `instructional_plan` is supplied; malformed plans raise actionable `ValueError` validation errors immediately.
- Removed domain-keyword math ceilings, automatic multi-framework keyword stacks, regex visual overrides, and `<!-- decision-contract: ... -->` / `shared/notes_decision_matrix.md` scaffold comments from new deep-note scaffolds.

## Third-stage reorganization: Multi-Master Architecture (M1–M7) & Reference Consolidation

- **Seven Canonical Master Output Templates (`M1–M7`):** Replaced the flat retired top-level templates directory with organized specs under `references/templates/masters/` (`deep-notes.md`, `study-notes.md`, `quick-reference.md`, `worked-solutions.md`, `implementation-guide.md`, `assessment.md`, `synthesis-revision.md`), 12 variants under `references/templates/variants/`, 6 domain-independent knowledge-type subtemplates under `references/templates/subtemplates/`, and `references/templates/modules/module-catalog.md`.
- **Legacy top-level templates retirement mapping (old basename -> canonical path):**
  - `deepstudy-master.md` -> `references/templates/masters/deep-notes.md` (`M1`)
  - `studynotes.md` -> `references/templates/masters/study-notes.md` (`M2`)
  - `cheat-sheet.md` -> `references/templates/masters/quick-reference.md` (`M3`)
  - `api-table.md` -> `references/templates/variants/syntax-reference.md` (`M3` variant)
  - `atomic.md` -> `references/templates/variants/atomic-card.md` (`M3` variant)
  - `dsa.md` -> `references/templates/masters/implementation-guide.md` (`M5`)
  - `practice.md` -> `references/templates/masters/assessment.md` (`M6`)
  - `comparison.md` -> `references/templates/variants/comparison-guide.md` (`M7` variant)
  - `paper-breakdown.md` -> `references/templates/variants/paper-breakdown.md` (`M7` variant)
  - `summary.md` -> `references/templates/variants/quick-summary.md` (`M7` variant)
- **Intelligent Routing Engine (`scriptorium/engines/orchestration.py` (`scripts/scribe.py route`), `references/routing/master-registry.yaml`, `references/routing/routing-policy.md`):** Unifies explicit `/scribe-*` command priority, negation-aware explicit artifact detection, dominant-intent classification, multi-artifact shared-context routing, and source-policy preservation while preserving all existing `/scribe-*` commands and Contract v3 / ARRIE / P01–P11 engines.
- **Workflow folder reorganization:** Moved flat `references/*.md` files into `references/workflows/{research,notes-creation,revision,validation}/`, `references/routing/`, `references/templates/`, and `references/contracts/`.

## Fourth-stage upgrade: Six Cohesive Engines, 20 Advanced Mechanisms & Automatic Obsidian Properties

- **Python Script Consolidation (`scripts/` 18 → 8 CLI entry points):** Consolidated 11 overlapping/non-CLI scripts into six cohesive engines under `scriptorium/engines/` (`orchestration.py`, `research.py`, `knowledge.py`, `pedagogy.py`, `quality.py`, `vault.py`) plus shared `scriptorium/models.py` and `scriptorium/layout.py`, exposed through unified `scripts/scribe.py` and 7 retained vault/planning CLIs (`plan_notes.py`, `scaffold_note.py`, `validate_note.py`, `vault_index.py`, `vault_graph.py`, `patch_links.py`, `verify_vault_notes.py`).
- **Mandatory Obsidian Properties (`references/metadata/`):** Every newly generated note begins on line 1 with valid YAML frontmatter containing `topic`, `tags` (hierarchical `domain/`, `master-topic/`, `subdomain/`, `concept/`, `type/`), `master_topic`, `domain`, and `note_type`, plus optional managed fields; existing custom properties and user-managed tags are preserved idempotently during incremental updates.
- **20 Advanced Knowledge Intelligence Mechanisms:** Integrated across E1–E6 (intent normalization, constraint precedence, template capability matrix, instruction authority linting, concept identity registry, coverage ledger, explanation gap detector, information density controller, example optimizer, representation consistency checker, claim traceability, uncertainty ledger, adaptive clarification policy, multi-artifact consistency, knowledge compression, incremental notes update, semantic change impact graph, failure-aware targeted repair, 13-case golden evaluation harness, and secret-scrubbed decision tracing).

## Fifth-stage upgrade: Universal `/scribe-notes`, Interactive Intelligence & Hierarchical Knowledge Generation

- **Public Command Consolidation (`12` → `4` active public skills):** Unified all 8 redundant note-creation public skill wrappers (`/scribe-deepnotes`, `/scribe-distill`, `/scribe-atomic-notes`, `/scribe-compare`, `/scribe-dsa`, `/scribe-practice`, `/scribe-ingest`, `/scribe-expand`) into the single universal `/scribe-notes` command while preserving the 3 non-note commands (`/scribe-doubt`, `/scribe-quiz`, `/scribe-setfolder`). All 7 internal master templates (`M1`–`M7`), 12 variants, 6 subtemplates, ARRIE, Contract v3, P01–P11, EIS-01..EIS-07, and Obsidian Properties remain intact and dynamically selectable through `/scribe-notes`.
- **Mandatory Interactive Configuration Gate:** `/scribe-notes` analyzes requests (`OrchestrationEngine.start_notes_session`), infers provisional template, depth, scope (`S0`–`S5`), and organization (`single_note` vs. `hierarchical_collection`), asks only unanswered adaptive plain-text questions, and supports natural follow-ups without repeating `/scribe-notes` (`respond_to_session`).
- **Hierarchical Knowledge Generation & Collection-Wide Validation:** Broad topics (`S3`–`S5`) decompose into structured Parent Maps of Content (`note_type: index`) and adaptive child notes with separated Topic Hierarchy (`parent_id`/`child_ids`), Prerequisite (`prerequisite_ids`), and Related (`related_ids`) graphs, collection manifests under `.scriptorium/collections/`, non-destructive existing-note reconciliation, and collection-wide validation (`QualityEngine.validate_collection`).
## KCP composition integrity v2

Comprehensive M1 publication now requires the [integrity contract](composition-integrity.md).
Rebuild a v1 composition from its authored specification, prepare actual assets and
assessments, then review the prepared chapter bodies. Nonempty review strings and
renderer selections no longer qualify as verification. Programmatic SVG diagram
generation is retired in favor of web-image-first local acquisition, and the superseded
private `_composition*.py` shims have been removed in favor of `scriptorium/engines/composition/`.
Other masters, source-only modes and legacy layouts retain their established
contracts. This migration does not rewrite or delete existing user notes.
