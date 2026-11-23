# Note routing

Use this page only for `/scribe-notes`. An explicit command or requested artifact takes priority over inferred intent. Keep the user's source restrictions even when a template would usually call for more research. Ignore negated artifact words when choosing a route (for example, “don't make a cheat sheet”). [Routing details](references/routing/routing-policy.md) and the [declarative registry](references/routing/master-registry.yaml) apply when a request is ambiguous or asks for multiple products.

| Request | Master | Load |
|---|---|---|
| Comprehensive explanation from first principles | M1 | [Deep notes](references/templates/masters/deep-notes.md) |
| Supplied lecture, source, or syllabus in its order | M2 | [Study notes](references/templates/masters/study-notes.md) |
| Cheat sheet, formula, syntax, command, or atomic card | M3 | [Quick reference](references/templates/masters/quick-reference.md) and selected variant |
| Solve given problems step by step | M4 | [Worked solutions](references/templates/masters/worked-solutions.md) |
| Explain an implementation or algorithm | M5 | [Implementation guide](references/templates/masters/implementation-guide.md) |
| Practice questions, flashcards, or mock exam | M6 | [Assessment](references/templates/masters/assessment.md) |
| Comparison, paper analysis, summary, or revision | M7 | [Synthesis and revision](references/templates/masters/synthesis-revision.md) |

Video-note requests, including `/scribe-ytnote`, use M2 by default and Command V in the [command playbooks](references/workflows/notes-creation/command-playbooks.md). The video names in the registry are intent aliases, not installed public skill folders. If a request asks for two distinct artifacts, author each with its selected master; share verified facts and notation without forcing one template on both.

For any write, resolve the destination with the [pre-generation gate](references/workflows/notes-creation/pre-gen-gate.md). For broad collections, plan a map and prerequisite-ordered chapters; let the subject determine the chapter count. Use one naming convention: `00 - Map of Contents.md`, then `01 - <Title>.md`, and so on. Preserve existing vault layouts when revising them. Load [shared teaching rules](shared/teaching_core.md), [authoring rules](shared/authoring_rules.md), [math guidance](shared/math_gates.md) when quantitative material appears, and the dominant knowledge-type subtemplate (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, or `historical`) via the [index](references/README.md).
