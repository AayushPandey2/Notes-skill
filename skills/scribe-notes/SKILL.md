---
name: scribe-notes
description: Create and publish Obsidian learning notes from researched teaching records, sources, PDFs, or videos. Use when generating study notes, comprehensive collections, worked solutions, implementations, comparisons, revision or assessments.
---

# /scribe-notes

Use `python scripts/scribe.py notes start "<request>" --vault "<vault>"`, then `notes respond` for unresolved configuration and plan approval. Preserve M1–M7 output products, variants, source policy, prerequisite order and the user's chosen layout. Video aliases enter through `scripts/scribe.py ytnote`.

Before authoring, load [teaching rules](../../shared/teaching_core.md), [authoring rules](../../shared/authoring_rules.md), and only the active master and subtemplates via `scripts/scribe.py optimize --compile "<request>"`. Research actual claims; strict source policy forbids unsupplied outside claims and media.

Prepare concept-owned teaching records using [the teaching input contract](../../references/contracts/teaching-input.md). For comprehensive collections, every child needs researched theory, foundations, meaningful examples and limitations. Supply mathematical records for substantive equations; the runtime emits immediate collapsible twelve-stage explanations and verifies declared arithmetic. Select the [mathematical subtemplate](../../references/templates/subtemplates/mathematical.md) only when needed.

Express required visuals as `visual_requirements` or `visual_specs` on the owning concept. Follow [the media contract](../../references/workflows/notes-creation/representations.md): research and compare candidates, verify each file's reuse rights, acquire real local raster bytes, inspect them, and supply hash-bound semantic findings before grounded writing. Missing required images block the chapter and its parent index. Metadata/pixel inspection alone does not establish image meaning. Custom SVG generation has no active backend.

Run `python scripts/scribe.py notes generate --vault "<vault>" --session-id "<id>" --teaching "<teaching.json>" --validate`. Ordinary and checkpoint modes execute `composition/publication.py`, which calls `composition/writing.py` and the mathematical/visual owners. Comprehensive runs require teaching records and reject pending teaching obligations; there is no generic prose fallback. Keep execution and validation evidence with the generated artifacts.

For importing an already-authored five-key collection, retain `notes compose --spec` with preparation, artifact-bound reviews, publication, repair and validation under [the comprehensive contract](../../references/workflows/notes-creation/composition-contract.md). This is an authored-artifact import, not a second prose generator. Both publication surfaces use the same Publisher owner and safe-write boundary.

Validate actual Markdown, local hashes, links and assessments. Inspect educational reasoning separately from structural checks. Verify Reading View and Live Preview when Obsidian access is available; otherwise report UI acceptance as incomplete. Never modify existing notes or assets during tests.

Use [metadata policy](../../references/metadata/properties-policy.md) for Properties profiles. Preserve the five-key profile for explicit comprehensive imports. The other public skills remain read-only doubt answering, interactive quizzes and folder configuration.
