---
name: scribe-notes
description: Universal adaptive Obsidian note-creation command. Use when asked to create, expand, or organize study notes, comprehensive first-principles guides, lecture/PDF/YouTube video notes (/scribe-ytnote), worked solutions, implementation tutorials, comparison guides, cheat sheets, or atomic cards in Obsidian.
---

# `/scribe-notes`

`/scribe-notes` is Scriptorium's single public entrypoint for creating or updating learning notes (including `/scribe-ytnote`—combining `/scribe-ytnotes` and `/scribe-ytlecture`—via `scripts/scribe.py ytnote`). Interactive calibration runs first so template, depth, and folder layout match user intent without wasted generation passes.

## Execution Flow

1. **Interactive Configuration Gate (`scripts/scribe.py notes start` / `respond`):**
   - Pass user request and vault path to infer master (`M1`–`M7`), variant, depth, scope tier (`S0`–`S5`), and `single_note` vs. `hierarchical_collection`. Ask only unanswered configuration questions (never a knowledge quiz) and accept plain follow-up replies or `"use your recommendations"`.
   - For broad collections (`S3`–`S5`), preview the Parent Map of Content + child notes + dependency path before writing, keeping hierarchy, prerequisite, and related graphs separate.
2. **Research, Pedagogical Core & Visuals:**
   - Load [shared/teaching_core.md](../../shared/teaching_core.md), [shared/authoring_rules.md](../../shared/authoring_rules.md), and the active master/subtemplate via selective context compilation—avoid loading unrelated masters.
   - Put intuition before formal definitions, embed an atomic `> [!example]- Understand this formula step by step` fold directly beneath every displayed `$$...$$`, and acquire verified raster web/video visuals under `assets/scriptorium/<collection-slug>/` via LAVIA/BVIA ([representations.md](../../references/workflows/notes-creation/representations.md)) with zero programmatic SVG synthesis.
3. **Comprehensive M1 Collections vs. Single / `M2`–`M7` Notes:**
   - **Comprehensive M1 (KCP v2):** Follow [composition-contract.md](../../references/workflows/notes-creation/composition-contract.md) and [composition-integrity.md](../../references/contracts/composition-integrity.md). Publish one MOC + 5–10 chapters directly under `<Vault>/<Topic>/` with exact five-key YAML (`id`, `aliases`, `topic`, `tags`, `nexttopics`), using `scripts/scribe.py notes compose --spec` through `--prepare`, artifact-bound review receipts, `--publish`, `--repair`, and `--validate`.
   - **Single notes & `M2`–`M7`:** Run `scripts/scribe.py notes generate --vault "<vault>" --session-id "<id>" --validate`, applying Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`), safe incremental reconciliation, and semantic/structural validation.

## On-Demand References

- Routing & full architecture: [SKILL.md](../../SKILL.md), [router.md](../../router.md), [routing-policy.md](../../references/routing/routing-policy.md)
- Pre-gen gate & playbooks: [pre-gen-gate.md](../../references/workflows/notes-creation/pre-gen-gate.md), [command-playbooks.md](../../references/workflows/notes-creation/command-playbooks.md)
- Metadata & taxonomy: [properties-policy.md](../../references/metadata/properties-policy.md), [tag-taxonomy.md](../../references/metadata/tag-taxonomy.md)
