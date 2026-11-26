---
name: scribe-notes
description: Create or revise Obsidian learning notes from a topic, PDF, article, video, source material, or existing notes. Use for comprehensive notes, study guides, worked solutions, implementation explanations, quick references, assessments, and comparisons.
---

# `/scribe-notes`

Input: the learner's request and sources; an explicit vault path if given. Never ask *"which type of notes do you want?"* or pause for pre-write reverification—infer intent, format, and structure directly from the user's message.

Resolve artifact selection using `artifact_policy` in [master-registry.yaml](../../docs/dispatch/master-registry.yaml) before determining filenames. Honor explicit artifact inclusion and exclusion requests, and do not independently infer additional companion files outside the resolved artifact plan. Resolve destination via [pre-gen-gate.md](../../docs/procedures/authoring/pre-gen-gate.md), route across the four dimensions in [router.md](../../router.md) and [subject-registry.yaml](../../docs/dispatch/subject-registry.yaml), follow [runtime_pipeline.md](../../core/runtime_pipeline.md) (no scripts/builders), apply [representations.md](../../docs/procedures/authoring/representations.md) where relevant and permitted, and verify saved files against [verification-checklist.md](../../docs/procedures/review/verification-checklist.md). Report any unavailable source, visual, execution, or rendering check honestly.
