---
name: scriptorium
description: Create, research, organize, and query Obsidian study notes, source summaries, worked solutions, implementation guides, practice assessments, and revision packs.
---

# Scriptorium 6.0 — Pre-flight routing

## Logical Architecture (12 Roles)

Scriptorium coordinates 12 logical responsibilities over its six Python engines (`E1`–`E6`) and `composition/` package without spawning redundant LLM calls:

| Role | Backing Owner | Responsibility |
|---|---|---|
| **Director** | `E1` (`orchestration.py`) | Request intake, negation/precedence routing (`M1`–`M7` + variants), interactive configuration gate (no pre-gen quiz) |
| **Map** | `E3` (`knowledge.py`) | Concept identity, prerequisite DAG, existing-note reuse (`F03`), gap analysis (`F04`), notation governance (`F09`), impact (`F14`) |
| **Tutor** | `E4` (`pedagogy.py`) | Adaptive instructional engine (`P01`–`P11`), `EIS-01`–`EIS-07` clarity, independent `0–5` depths, progressive disclosure (`F11`) |
| **Planner** | `E1` + `E4` (`composition/`) | Scope tiers (`S0`–`S5`), KCP v2 adaptive 5–10 chapter allocation (`build_composition`), learning paths (`F08`) |
| **Researcher** | `E2` (`research.py`) | ARRIE modes (`R-S0`–`R-R`), per-concept evidence (`R0`–`R5`), provenance, contradiction escalation, separate further-learning curation |
| **Writer** | Agent + `E4`/`E6` | Continuous domain-natural prose from compiled selective context (`--context`), shared notation, and profile-governed frontmatter |
| **Visuals** | `E4` (`renderers.py`, `visuals.py`, `bvia.py`) | `R1`–`R12` adapters, BVIA cognitive accessibility ranking (Levels 0–6), mandatory `Explain -> Show -> Decode -> Connect` walkthroughs |
| **Assets** | `E4` (`lavia.py`, `media.py`) | LAVIA web-image-first routing (Reuse → Discover → Download/Validate → Documented SVG Fallback), `assets/scriptorium/<collection-slug>/`, `manifest.json` |
| **Quiz** | `E4` + `E6` (`/scribe-quiz`) | Objective-bound folded assessments (`M6` / chapter-end & milestone checks) and interactive vault recall |
| **Checker** | `E5` (`quality.py`, `contracts.py`) | KCP v2 executable obligations, artifact-bound reviews, `EIS-07` friction, runtime checks, dependency-aware targeted repair |
| **Vault** | `E6` (`vault.py`) | Vault-native `<Topic>/` placement (`resolve_collection_layout`, `/scribe-setfolder`, `create_category_folders=false`), atomic writes, checkpoints |
| **Speed** | `E1` (`_token_optimizer.py`) | Selective prompt compilation (`optimize --compile`, `--context`), single-pass source segmentation, `L1`–`L10` cache, minimal-span repair |

## Execution Triggers (`Tier 0`–`Tier 4`, `T01`–`T16`)

- **Tier 0 — Entry & Safety:** `T01` Entry & Intent Intake · `T02` Interactive Configuration Gate · `T03` Source Policy & Untrusted-Content Lock.
- **Tier 1 — Planning & Discovery:** `T04` Vault Discovery & `<Topic>/` Layout Resolution · `T05` KCP Concept & Chapter Allocation · `T06` ARRIE Research & Evidence Planning.
- **Tier 2 — Authoring & Visuals:** `T07` Selective Context Compilation · `T08` Prose & Pedagogical Composition · `T09` Web-Image-First BVIA/LAVIA Visual Preparation · `T10` Folded Assessment Binding.
- **Tier 3 — Verification & Publication:** `T11` Deterministic, Visual & Runtime Checks · `T12` Artifact-Bound Semantic Review · `T13` Checkpointed Atomic Publication.
- **Tier 4 — Lifecycle & Query:** `T14` Post-Publish Validation · `T15` Targeted Dependency-Aware Repair · `T16` Read-Only Vault Query & Recall (`/scribe-doubt`, `/scribe-quiz`).

See [router.md](router.md) for full trigger-to-command dispatch.

## Core Routing Steps

1. **Universal Entry (`/scribe-notes`):** All note creation enters through `/scribe-notes` (`/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder` remain separate). Start with `scripts/scribe.py notes start "<request>"` to calibrate template (`M1`–`M7`), depth, scope (`S0`–`S5`), and organization (`single_note` vs. `hierarchical_collection`). Never run a pre-generation diagnostic quiz.
2. **Architecture & Registry:** Consult [references/architecture/system-overview.md](references/architecture/system-overview.md) and [references/architecture/template-module-catalog.md](references/architecture/template-module-catalog.md) for component ownership and master-subtemplate-module matrices. Parse intent and source policy with [router.md](router.md), [references/routing/routing-policy.md](references/routing/routing-policy.md), and [references/routing/master-registry.yaml](references/routing/master-registry.yaml) (`scripts/scribe.py route` + `scripts/plan_notes.py inspect`).
3. **Master & Subtemplate Selection:** Route every authoring request to one of the **Seven Canonical Masters (`M1–M7`)** under [references/templates/masters/](references/templates/masters/README.md) with optional variant ([references/templates/variants/](references/templates/variants/README.md)) and knowledge-type subtemplates ([references/templates/subtemplates/](references/templates/subtemplates/README.md)).
4. **Selective Loading:** Load only the selected master/variant, active entries from [references/workflows/notes-creation/instructional-registry.json](references/workflows/notes-creation/instructional-registry.json) and [references/workflows/research/research-policy-registry.json](references/workflows/research/research-policy-registry.json), metadata policies ([references/metadata/properties-policy.md](references/metadata/properties-policy.md), [references/metadata/tag-taxonomy.md](references/metadata/tag-taxonomy.md)), and shared contracts ([shared/authoring_rules.md](shared/authoring_rules.md), [shared/math_gates.md](shared/math_gates.md)); never load the entire template directory.
5. **Adaptive Deep Learning (`M1`):** Plan per-concept capabilities/depths (`0–5`) in [references/workflows/notes-creation/adaptive-engine.md](references/workflows/notes-creation/adaptive-engine.md), ARRIE evidence in [references/workflows/research/research-engine.md](references/workflows/research/research-engine.md), active `P01`–`P11` / `EIS-01`–`EIS-07` mechanisms in [references/workflows/notes-creation/pedagogical-intelligence.md](references/workflows/notes-creation/pedagogical-intelligence.md) (`scripts/scribe.py explain`), and compose with [references/templates/masters/deep-notes.md](references/templates/masters/deep-notes.md).
6. **Frontmatter, Visuals & Publication:** Every note starts on line 1 with profile-governed YAML: exact 5-key YAML (`id`, `aliases`, `topic`, `tags`, `nexttopics`) for comprehensive M1 KCP v2 collections, or standard Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, plus optional `parent_topic`/`collection_id`) via `scripts/scribe.py properties` / `scripts/scaffold_note.py` for single notes, `M2`–`M7`, and legacy nested collections. Follow web-image-first BVIA/LAVIA visual routing ([representations.md](references/workflows/notes-creation/representations.md)) storing verified local assets under `assets/scriptorium/<collection-slug>/`. Validate (`scripts/scribe.py notes validate`) before publication. Existing-note utilities (`/scribe-doubt`, `/scribe-quiz`) bypass generation.

## Comprehensive topic collections

For full-topic M1 output, follow the [composition contract](references/workflows/notes-creation/composition-contract.md) and [KCP integrity contract](references/contracts/composition-integrity.md) after scope calibration:
- **Layout:** Vault-native `<Topic>/` folder (`resolve_collection_layout`, honoring `/scribe-setfolder`, `create_category_folders=false` default) with one numbered MOC and 5–10 substantive authored chapters (omit `chapters` in the spec for prerequisite-aware adaptive allocation; inspect `chapter_rationale` before authoring).
- **Metadata & Tags:** Exact five-key YAML (`id`, `aliases`, `topic`, `tags`, `nexttopics`) with hierarchical `domain/`, `subject/`, `topic/` tags; supply `classification.subject` / `classification.domain` when inference is insufficient.
- **Visuals, Preparation & Integrity:** Inspect [the renderer registry](scriptorium/engines/composition/renderers.py) and [representations.md](references/workflows/notes-creation/representations.md) only for active visual capabilities; enforce web-image-first LAVIA acquisition, BVIA `Explain -> Show -> Decode -> Connect` prose, and local embeds under `assets/scriptorium/<collection-slug>/`. Run `scripts/scribe.py notes compose` (`--prepare`, then artifact-bound review receipts + exact source evidence, then `--publish`, and `--validate` / `--repair` as needed). Critical open obligations block completion. Other masters and narrow single notes retain their established contracts.
