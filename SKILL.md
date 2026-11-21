---
name: scriptorium
description: Create, research, organize, and query Obsidian study notes, source summaries, worked solutions, implementation guides, practice assessments, and revision packs.
---

# Pre-flight routing

## Rust local visual services (5.1 migration)

For local images, use the Rust `scribe assets` services and the typed visual plan,
receipt, audit, and create-only publication interfaces documented in
[docs/rust-runtime.md](docs/rust-runtime.md). Build with `cargo build --release --locked`.
Research retrieval and deterministic rendering also run in Rust. All published
image embeds must resolve to verified local files; remote URLs belong in provenance.
License permission and scientific relevance require evidence-backed review.
The legacy educational commands below remain available while the
[migration ledger](docs/rust-migration-ledger.md) records their outstanding parity work.
Do not describe the full Python-to-Rust migration as complete.

1. **Universal Note-Creation Entry Point (`/scribe-notes`):** All note-creation requests enter through `/scribe-notes` (the sole public note-creation command; non-note utilities `/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder` remain separate). Start with the interactive configuration gate (`scripts/scribe.py notes start "<request>"`) to infer provisional template, depth, scope (`S0`–`S5`), and organization (`single_note` vs. `hierarchical_collection`) before generating final notes. Never run a pre-generation diagnostic quiz.
2. **System Architecture & Catalog:** Consult [references/architecture/system-overview.md](references/architecture/system-overview.md) and [references/architecture/template-module-catalog.md](references/architecture/template-module-catalog.md) for component ownership, master-subtemplate-module activation matrices, and Knowledge Collection Plan (`KCP`, `F02`–`F15`) lifecycle integration.
3. Parse command, artifact intent, and source policy using [router.md](router.md), [references/routing/routing-policy.md](references/routing/routing-policy.md), and [references/routing/master-registry.yaml](references/routing/master-registry.yaml) (`scriptorium/engines/orchestration.py` via `scripts/scribe.py route` + `scripts/plan_notes.py inspect`).
4. Route every authoring request to one of the **Seven Canonical Master Output Templates (`M1–M7`)** under [references/templates/masters/](references/templates/masters/README.md) (with optional variant under [references/templates/variants/](references/templates/variants/README.md) and domain-independent knowledge-type subtemplates under [references/templates/subtemplates/](references/templates/subtemplates/README.md)).
5. For deep learning notes (`M1` via `/scribe-notes`), plan per-concept subtemplates, objectives, prerequisites, and independent depth profiles (`0–5`) in [references/workflows/notes-creation/adaptive-engine.md](references/workflows/notes-creation/adaptive-engine.md), plan concept-specific evidence requirements via [references/workflows/research/research-engine.md](references/workflows/research/research-engine.md) (ARRIE), apply active learning-experience mechanisms from [references/workflows/notes-creation/pedagogical-intelligence.md](references/workflows/notes-creation/pedagogical-intelligence.md) and Explanation Intelligence (`EIS-01..EIS-07` via `scripts/scribe.py explain`), and compose with [references/templates/masters/deep-notes.md](references/templates/masters/deep-notes.md).
6. Load only the selected master/variant template, selected registry entries from [references/workflows/notes-creation/instructional-registry.json](references/workflows/notes-creation/instructional-registry.json) and [references/workflows/research/research-policy-registry.json](references/workflows/research/research-policy-registry.json), metadata policies ([references/metadata/properties-policy.md](references/metadata/properties-policy.md), [references/metadata/tag-taxonomy.md](references/metadata/tag-taxonomy.md)), and required shared contracts ([shared/authoring_rules.md](shared/authoring_rules.md), [shared/math_gates.md](shared/math_gates.md)); never load the entire template directory as a bundle.
7. Every generated Markdown note MUST begin on line 1 with valid Obsidian YAML Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, plus `parent_topic` / `collection_id` for hierarchical collections) generated via `VaultEngine` / `scripts/scribe.py properties` or `scripts/scaffold_note.py`. Plan, verify evidence into a structured registry, draft, validate Properties, citations, pedagogical quality, collection integrity (`scripts/scribe.py notes validate`), and contracts, then publish through the router workflow. Existing-note commands (`/scribe-doubt`, `/scribe-quiz`) bypass generation.

## Comprehensive topic collections

Omit `chapters` from the composition specification for adaptive allocation from
the prerequisite DAG; inspect `chapter_rationale` before authoring. Use nested
`topic/`, `subject/`, and `domain/` tags from the owned concepts and shared taxonomy.
Supply `classification.subject` and `classification.domain` when inference is
insufficient. [The renderer registry](scriptorium/engines/composition/renderers.py)
declares available backends; load only relevant rendering guidance.

For full-topic M1 output, use the [composition contract](references/workflows/notes-creation/composition-contract.md) after scope calibration. It takes precedence over the legacy hierarchy/Properties instructions above for this profile: one numbered MOC and 5–10 substantive authored chapters, exact five-key YAML, shared capability/depth/evidence plan, and publication through `scripts/scribe.py notes compose`. Other masters and narrow single notes retain their established contracts.

Apply the [KCP integrity contract](references/contracts/composition-integrity.md) to this path. Prepare the actual figures, tables and independently folded assessments before reviewing chapter bodies. Submit artifact-bound review receipts and exact source evidence; critical open obligations block completion. Use the existing selective compiler and dependency-aware repair plan for active concepts.
