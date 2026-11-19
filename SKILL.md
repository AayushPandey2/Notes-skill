---
name: scriptorium
description: Create, research, organize, and query Obsidian study notes, source summaries, algorithm solutions, and practice sets.
---

# Pre-flight routing

1. Parse command and source using [router.md](router.md).
2. For deep-study generation (`/scribe-deepnotes`), plan per-concept subtemplates, objectives, prerequisites, and independent depth profiles (`0–5`) in [references/adaptive-engine.md](references/adaptive-engine.md) and compose with [templates/deepstudy-master.md](templates/deepstudy-master.md).
3. Load only the selected template, selected registry entries from [references/instructional-registry.json](references/instructional-registry.json), and required shared contracts ([shared/authoring_rules.md](shared/authoring_rules.md), [shared/math_gates.md](shared/math_gates.md)); never load the template directory as a bundle.
4. Plan, research, draft, validate, then publish through the router workflow. Existing-note commands bypass generation.
