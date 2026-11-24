# Note routing

Use this page only for `/scribe-notes`. An explicit command or requested artifact takes priority over inferred intent. Keep the user's source restrictions even when a template would usually call for more research. Ignore negated artifact words when choosing a route (for example, “don't make a cheat sheet”). [Routing details](docs/dispatch/routing-policy.md) and the [declarative registry](docs/dispatch/master-registry.yaml) apply when a request is ambiguous or asks for multiple products.

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

For any write, resolve the destination with the [pre-generation gate](docs/procedures/authoring/pre-gen-gate.md). For broad collections, plan a map and prerequisite-ordered chapters; let the subject determine the chapter count. Use one naming convention: `00 - Map of Contents.md`, then `01 - <Title>.md`, and so on. Preserve existing vault layouts when revising them. Load [shared teaching rules](core/teaching_core.md), [authoring rules](core/authoring_rules.md), [math guidance](core/math_gates.md) when quantitative material appears, and the dominant knowledge-type subtemplate (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, or `historical`) via the [index](docs/README.md).
