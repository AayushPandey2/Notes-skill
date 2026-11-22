# Scriptorium System Architecture Overview

This document is the authoritative architectural reference connecting Scriptorium's universal `/scribe-notes` command, interactive configuration, routing, Knowledge Collection Plan (`KCP`), seven canonical masters (`M1`–`M7`), variants, subtemplates, reusable modules, six consolidated Python engines, and Obsidian vault lifecycle.

## 1. End-to-End Logical Architecture

Comprehensive M1 collections also use [KCP v2 integrity](../contracts/composition-integrity.md).
The runtime implementation coordinates 12 canonical logical responsibilities
(**A0 Director, A1 Map, A2 Tutor, A3 Planner, A4 Researcher, A5 Writer, A6
Visuals, A7 Assets, A8 Quiz, A9 Checker, A10 Vault, A11 Speed**) and 16
explicit triggers (`T01`–`T16` in `scriptorium/triggers.py`) across the package
and `scriptorium/engines/composition/`: planning/publication, shared
obligations, web-image discovery/inspection, and scoped semantic checks.

The stages below represent **logical responsibilities** coordinated in Python and on-demand reference loading—not separate LLM calls for every box:

```text
/scribe-notes <topic, source, or request>
     |
     v
REQUEST ANALYSIS & SCOPE CLASSIFICATION (S0-S5)        [E1 Orchestration]
     |
     v
INTERACTIVE CONFIGURATION GATE (Zero Pre-Gen Quiz)     [E1 Orchestration]
     |
     v
ROUTING & WORKFLOW SELECTION (M1-M7 + Variants)        [E1 Orchestration]
     |
     v
KNOWLEDGE COLLECTION PLAN (KCP: F02-F08)               [E1 + E3 + E4]
  - Existing-Note Reuse (F03)
  - Prerequisite Gap Analysis G1-G5 (F04)
  - Scope & Size Negotiation (F05)
  - Collection-Level Adaptive Depth Allocation (F02)
  - Adaptive Note Granularity Split/Merge/Retain (F07)
  - Cross-Note Learning Path Generation (F08)
     |
     v
MASTER -> VARIANT -> SUBTEMPLATE -> CONDITIONAL MODULES [E1 + E4 + Registry]
     |
     v
PEDAGOGICAL & EXPLANATION INTELLIGENCE                 [E2 + E4]
  - ARRIE Research & Source Fidelity (E2)
  - Contract v3 + P01-P11 + EIS-01..EIS-06 (E4)
  - Terminology & Notation Governance (F09)
  - Progressive Disclosure (F11) & Competencies (F12)
  - Cross-Note Synthesis M7 (F10) & Assessments M6 (F13)
     |
     v
VALIDATION & TARGETED REPAIR                           [E5 Quality]
  - Representation, Claim, EIS-07 Friction & Collection-Wide Validation
     |
     v
CHECKPOINTED OBSIDIAN VAULT OUTPUT (F06)               [E6 Vault]
  - Mandatory Line-1 Obsidian Properties, Parent MOCs, Manifests, Safe Writes
     |
     v
COLLECTION LIFECYCLE & REFINEMENT (F14-F15)            [E3 + E5 + E6]
  - Versioning, Semantic Change-Impact Analysis, Explicit Reader Feedback Repair
```

> **Explicit Exclusion (Feature 1):** Scriptorium intentionally does **not** implement pre-generation Interactive Knowledge Diagnosis quizzes (`INTERACTIVE_KNOWLEDGE_DIAGNOSIS_ENABLED = False`). Prior knowledge is gathered strictly via the non-intrusive interactive configuration gate.

## 2. Single-Owner Decision Authority

| Decision Domain | Single Authoritative Owner | Canonical Spec / Implementation |
|---|---|---|
| Public note-creation command & interactive configuration | Engine E1 (`OrchestrationEngine`) | [skills/scribe-notes/SKILL.md](../../skills/scribe-notes/SKILL.md), [orchestration.py](../../scriptorium/engines/orchestration.py), [_interactive.py](../../scriptorium/engines/_interactive.py) |
| Master (`M1`–`M7`), variant, subtemplate & module registry | Engine E1 (`OrchestrationEngine`) | [master-registry.yaml](../routing/master-registry.yaml), [routing-policy.md](../routing/routing-policy.md) |
| Research, source verification & resource curation (ARRIE) | Engine E2 (`ResearchEngine`) | [research.py](../../scriptorium/engines/research.py), [research-policy-registry.json](../workflows/research/research-policy-registry.json) |
| Concept identity, coverage, claim traceability, reuse (F03), gaps (F04), notation (F09), change impact (F14) | Engine E3 (`KnowledgeEngine`) | [knowledge.py](../../scriptorium/engines/knowledge.py), [_collection_intelligence.py](../../scriptorium/engines/_collection_intelligence.py) |
| Contract v3, P01–P11, EIS-01..06, depth allocation (F02), granularity (F07), paths (F08), synthesis (F10), disclosure (F11), outcomes (F12), assessments (F13) | Engine E4 (`PedagogyEngine`) | [pedagogy.py](../../scriptorium/engines/pedagogy.py), [instructional-registry.json](../workflows/notes-creation/instructional-registry.json) |
| Representation checks, EIS-07 friction review, collection-wide validation, competency checks (F12), reader feedback repair (F15), golden evals, repo audit | Engine E5 (`QualityEngine`) | [quality.py](../../scriptorium/engines/quality.py), [verification-checklist.md](../workflows/validation/verification-checklist.md) |
| Obsidian Properties, tag taxonomy, Parent MOCs, checkpointed batch commits (F06), incremental updates, safe atomic writes | Engine E6 (`VaultEngine`) | [vault.py](../../scriptorium/engines/vault.py), [properties-policy.md](../metadata/properties-policy.md) |

## 3. Public Command & CLI Footprint

- **Active Public Skills (`skills/` — 4 total):**
  1. `/scribe-notes` — Sole canonical public note-creation command (universal routing across `M1`–`M7`, single notes, and hierarchical collections).
  2. `/scribe-doubt` — Read-only vault Q&A.
  3. `/scribe-quiz` — Interactive active-recall quiz over existing notes.
  4. `/scribe-setfolder` — Default target notes folder configuration.
- **Public CLI Scripts (`scripts/` — 8 thin entry points):**
  `scribe.py` (including `notes`, `optimize`, `route`, `explain`, `evaluate`, `audit`), `plan_notes.py`, `scaffold_note.py`, `validate_note.py`, `vault_index.py`, `vault_graph.py`, `patch_links.py`, `verify_vault_notes.py`.

## 4. Token Efficiency & Zero-Quality-Loss Runtime (`_token_optimizer.py`)

Scriptorium minimizes avoidable LLM token overhead without shortening notes, dropping derivations, or weakening any of the 14 mandatory validation checks:

- **Selective Context Loading & Canonical Prompt Compilation:** Loads only the selected master, variant, knowledge-type subtemplates, module dependency closure, and conditional policies (`scripts/scribe.py optimize --compile "<request>"`), stripping scaffold comments and duplicate boilerplate while organizing stable rules into a provider-cacheable prefix.
- **Single-Pass Source Segmentation (`SourceSegmentStore`) & Multi-Level Cache (`L1`–`L10`):** Parses sources once, retrieves targeted passages plus adjacent context while tracking a complete Source Coverage Ledger, and caches content-addressed results with strict user isolation, TTL freshness, and credential scrubbing.
- **Partitioned Collection Context & Minimal Span Repair:** Sends Global/Group/Note slices per child note rather than full collection prose, runs deterministic validations locally at 0 LLM tokens with an `L9` audit trail, and extracts minimal defective spans for targeted repairs.

See [template-module-catalog.md](template-module-catalog.md) for the complete Master, Variant, Subtemplate, and Module inventory and usage matrix.

## Comprehensive composition profile

The [composition contract](../workflows/notes-creation/composition-contract.md) defines full-topic M1 collections: one MOC, 5–10 comprehensive chapters in the vault-native `<Topic>/` layout (`resolve_collection_layout`, `create_category_folders=false` default), shared `S01–S18` capabilities in the existing instructional registry, independent depth dimensions, web-image-first BVIA/LAVIA visuals (`assets/scriptorium/<collection-slug>/`), and authored publication with exactly five YAML keys. Its profile-specific rules take precedence over legacy collection metadata and file layout above. Existing single-note and `M2–M7` contracts remain supported.
