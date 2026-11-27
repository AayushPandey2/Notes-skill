---
name: scribe-notes
description: Create or revise Obsidian learning notes from a topic, PDF, article, video, source material, or existing notes. Use for comprehensive notes, study guides, worked solutions, implementation explanations, quick references, assessments, and comparisons.
---

# `/scribe-notes`

Input: the learner's request and sources, plus an explicit vault path if given. Use the [root skill](../../SKILL.md) for shared restrictions and the Early Resolution Gate: first read [note routing](../../router.md), the matching format/preset, and [the authoring pipeline](../../core/runtime_pipeline.md) to resolve route and `source_permissions`; retrieve specialist policies (`teaching_core.md`, `theory_quality_contract.md`, `subjects/`, `investigations/`) **only after** the format and scope require them.
