---
name: scribe-notes
description: Create and publish Obsidian learning notes from researched teaching records, sources, PDFs, or videos. Use when generating study notes, comprehensive collections, worked solutions, implementations, comparisons, revision or assessments.
---

# `/scribe-notes`

Follow [the direct-authoring workflow](../../shared/runtime_pipeline.md). During note creation, author content directly—never create, execute, or modify scripts or project source code to assemble, render, validate, download, or publish notes. Keep educational code inside Markdown fences only when the objective requires code.

## Execution Flow

1. **Interactive Configuration & Scope Gate:** Resolve vault path (explicit → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json`), master (`M1`–`M7`), variant, depth, source policy, and `single_note` vs. `hierarchical_collection`. Ask only unanswered configuration questions (never a knowledge quiz). For broad topics, preview `00 - Map of Contents.md` + prerequisite-ordered chapters before writing.
2. **Load Only Required Context:** Read [teaching rules](../../shared/teaching_core.md), [authoring rules](../../shared/authoring_rules.md), [math gates](../../shared/math_gates.md), and only the active master/subtemplate from `references/`. Research primary claims with native tools; strict source policy forbids unsupplied outside claims or media.
3. **Visual Discovery, Download & Inspection First:** For visual needs, search open educational images, verify file-specific permissive licenses, download real raster bytes (`png`/`jpg`/`webp`) into `<Vault>/assets/scriptorium/<collection-slug>/`, and inspect each downloaded image via `read_file` before writing prose. Report unavailable visuals honestly; never synthesize SVGs.
4. **Author Beginner-First Notes Directly:** Write natural prose covering orientation, intuition, prerequisite bridges, mechanism, formalization, worked examples (`Step 1`–`12`), `Explain -> Show -> Decode -> Connect` visual walkthroughs, causal comparisons before tables, limitations, and folded hint/answer assessments. Place `> [!note]- 📐 Understand this formula` immediately beneath every displayed `$$...$$`.
5. **Review & Publish Safely:** Write Markdown files directly under `<Vault>/<Topic>/` (5-key YAML for comprehensive `M1` collections per [composition-contract.md](../../references/workflows/notes-creation/composition-contract.md), or Obsidian Properties per [properties-policy.md](../../references/metadata/properties-policy.md)). Review YAML, wikilinks, local image embeds, and formula folds against [verification-checklist.md](../../references/workflows/validation/verification-checklist.md), preserving unrelated user notes.
