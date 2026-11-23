---
name: scribe-notes
description: Create or revise Obsidian learning notes from a topic, PDF, article, video, source material, or existing notes. Use for comprehensive notes, study guides, worked solutions, implementation explanations, quick references, assessments, and comparisons.
---

# `/scribe-notes`

Input: the learner's request and sources; an explicit vault path if given. Default to a single note for a narrow request and a planned collection for a broad topic. Use [router.md](../../router.md) to select the master, and [the destination gate](../../references/workflows/notes-creation/pre-gen-gate.md) before any write. A video request uses Command V in the [command playbooks](../../references/workflows/notes-creation/command-playbooks.md) when transcript or media access is available.

Follow [the direct-authoring workflow](../../shared/runtime_pipeline.md) and the [root authoring rule](../../SKILL.md#scriptorium). Load only the selected master and relevant variant, knowledge-type subtemplate, and policies via [the reference index](../../references/README.md). Source-only means no outside browsing; distinguish any labeled expansion the user permits. Teach prerequisites before first use, explain equations and worked examples at the requested depth, and cite actual source locations.

Output: final Obsidian Markdown, a companion lab for each newly generated content note under [the lab contract](../../references/workflows/notes-creation/experimental-lab.md), and needed, inspected local raster assets at the authorized destination. Review image needs and completed embeds separately for each note and lab; when multiple genuine needs exist, a single image or Mermaid diagram does not finish that file. Complete [visual acquisition and saved-embed checks](../../references/workflows/notes-creation/representations.md). For ML labs, check documented Rust crate support and include the library implementation when available, even if local Cargo execution is unavailable. Review actual files with [verification-checklist.md](../../references/workflows/validation/verification-checklist.md); preserve unrelated notes, custom properties, and assets. If source access, download, image inspection, execution, or Obsidian rendering is unavailable, report the specific limit and do not claim it was verified.
