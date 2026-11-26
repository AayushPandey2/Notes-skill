# Template and module guide

Use [router.md](../../router.md) and [routing-policy.md](../dispatch/routing-policy.md) to route across **four independent dimensions**:
1. **Master format** (`M1`–`M7`, `video_notes`) under [blueprints/formats/](../blueprints/formats/), with artifact cardinality governed by `artifact_policy` in [master-registry.yaml](../dispatch/master-registry.yaml).
2. **Preset overrides** under [blueprints/presets/](../blueprints/presets/) (e.g., `formula-sheet.md`, `lecture-order.md`, `paper-breakdown.md`).
3. **Subject specialization** via [subject-registry.yaml](../dispatch/subject-registry.yaml) (`blueprints/subjects/` + `procedures/safety/` when applicable).
4. **Knowledge-type teaching style** (`conceptual`, `mathematical`, `computational`, `scientific`, `historical`, `empirical`) under [blueprints/domains/](../blueprints/domains/) and **investigation lab profile** under `blueprints/investigations/`.

The [module catalog](../blueprints/components/module-catalog.md) lists optional teaching moves and [subject theory profiles](../blueprints/components/subject-theory-profiles.md) provides topic-family checklists and verified misconceptions. Load only selected entries, never full directories.

[master-registry.yaml](../dispatch/master-registry.yaml), [subject-registry.yaml](../dispatch/subject-registry.yaml), and [instructional-registry.json](../procedures/authoring/instructional-registry.json) are declarative routing aids. They do not execute, validate, install aliases, or establish that an output was checked. [Manual verification](../procedures/review/verification-checklist.md) applies to actual output.
