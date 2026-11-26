# Note routing

Use this page only for `/scribe-notes`. Infer the master, depth, and file structure automatically from the user's message after the command—never send a reverification prompt or ask *"which type of notes do you want?"*. When the user supplies only a topic name after `/scribe-notes`, default automatically to **`M1` Deep Notes** from scratch covering the topic completely. An explicit command or requested artifact takes priority over inferred intent. Keep the user's source restrictions even when a template would usually call for more research. Ignore negated artifact words when choosing a route (for example, “don't make a cheat sheet”). [Routing details](docs/dispatch/routing-policy.md) and the [declarative registry](docs/dispatch/master-registry.yaml) apply when a request names multiple products.

| Request | Master | Load |
|---|---|---|
| Comprehensive explanation from first principles | M1 | [Deep notes](docs/blueprints/formats/deep-notes.md) |
| Supplied lecture, source, or syllabus in its order | M2 | [Study notes](docs/blueprints/formats/study-notes.md) |
| Cheat sheet, formula, syntax, command, or atomic card | M3 | [Quick reference](docs/blueprints/formats/quick-reference.md) and selected variant |
| Solve given problems step by step | M4 | [Worked solutions](docs/blueprints/formats/worked-solutions.md) |
| Explain an implementation or algorithm | M5 | [Implementation guide](docs/blueprints/formats/implementation-guide.md) |
| Practice questions, flashcards, or mock exam | M6 | [Assessment](docs/blueprints/formats/assessment.md) |
| Comparison, paper analysis, summary, or revision | M7 | [Synthesis and revision](docs/blueprints/formats/synthesis-revision.md) |

Video-note requests (`/scribe-ytnotes`) follow [Video notes](docs/blueprints/formats/video-notes.md) and Command V in the [command playbooks](docs/procedures/authoring/command-playbooks.md) (or `M7` / [quick-summary.md](docs/blueprints/presets/quick-summary.md) if only a brief summary is requested). `/scribe-ytnotes` explicitly overrides one-file-per-subtopic collection splitting, automatic companion-lab generation, mandatory multi-language implementation tracks, and automatic full-playlist processing. If a request asks for two distinct artifacts, author each with its selected master; share verified facts and notation without forcing one template on both.

For any write, resolve the complete `artifact_plan` manifest ([adaptive-engine.md](docs/procedures/authoring/adaptive-engine.md)) first according to the selected master and `artifact_policy` in [master-registry.yaml](docs/dispatch/master-registry.yaml), explicit user instructions, source permissions ([source-fidelity.md](docs/procedures/sourcing/source-fidelity.md)), and existing vault layout ([pre-gen-gate.md](docs/procedures/authoring/pre-gen-gate.md)) with zero confirmation/reverification prompts. Create only the artifacts included in that resolved manifest.

Separate **four independent routing dimensions** via [routing-policy.md](docs/dispatch/routing-policy.md): (1) **Master format** (`M1`–`M7` / `video_notes`), (2) **Knowledge type** (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, `historical`), (3) **Subject specialization** ([subject-registry.yaml](docs/dispatch/subject-registry.yaml) $\to$ one primary subject + selective secondary support), and (4) **Lab profile** (`docs/blueprints/investigations/` plus `docs/procedures/safety/` when required). Load [shared teaching rules](core/teaching_core.md), [theory quality contract](core/theory_quality_contract.md), [authoring rules](core/authoring_rules.md), and [math guidance](core/math_gates.md) conditionally.
