# M1 — Deep Learning Notes

- **Master ID:** `M1` (`deep_notes` / compatibility route `deepstudy-master`)
- **Primary intent:** `comprehensive_learning` — build complete first-principles understanding from the learner's baseline to requested mastery.
- **Activation signals:** "teach me from scratch", "explain deeply", "comprehensive notes", "from fundamentals to advanced", or bare `/scribe-notes <topic>` without an explicit alternate product format.
- **Non-activation:** Do not select M1 when the user primarily requests a compact cheat sheet (`M3`), solved problem set (`M4`), implementation/build guide (`M5`), quiz/flashcards (`M6`), or standalone comparison/revision pack (`M7`).
- **Engines & Shared Contracts:** [adaptive-engine.md](../../workflows/notes-creation/adaptive-engine.md), [instructional-registry.json](../../workflows/notes-creation/instructional-registry.json), [pedagogical-intelligence.md](../../workflows/notes-creation/pedagogical-intelligence.md), [research-engine.md](../../workflows/research/research-engine.md), [source-fidelity.md](../../workflows/research/source-fidelity.md), [authoring_rules.md](../../../shared/authoring_rules.md), [math_gates.md](../../../shared/math_gates.md).
- **Modern Integration:** Supports universal `/scribe-notes` interactive configuration, `EIS-01..EIS-07` explanatory clarity, F02 collection-level depth allocation, F11 progressive disclosure, F12 learning-outcome coverage, and mandatory line-1 Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, `parent_topic`, `collection_id`).

## Orientation

Give the bounded topic, central question, observable objectives, and learning roadmap. Prepare only prerequisites the learner needs (`assume`, `remind`, `bridge`, `teach`, or `defer`) using `P01` cognitive dependency mapping. Preserve five-key YAML identity (`id`, `aliases`, `topic`, `tags`, `nexttopics`); keep planning records outside the finished note.

## Core learning sequence

Order concepts topologically by essential prerequisites (preserving source sequence with local bridges under `strict`/`expanded` policies). Establish definitions and notation before use. Choose dominant and merged knowledge-type subtemplates (`subtemplates/`), progress smoothly through active `L1–L8` explanation layers, and teach active modules at independent `0–5` depths. Exclude inactive modules completely—mathematics, code, proofs, diagrams, chronology, and experiments are conditional.

Compose one coherent explanation with domain-natural headings. Give every definition and governing equation one canonical home; align prose, math, visuals, tensor shapes, worked examples, and code (`P03`). Place misconception corrections at the point of need (`P06`) and put consequential assumptions beside the claims they constrain.

## Integration and assessment

Connect concepts through synthesis or cross-topic vault bridges (`P08`) without repeating prior chapters. Verify stated objectives through recall, calculation, derivation, diagnosis, or source interpretation without arbitrary question quotas.

## Revision and further learning

Provide Layer B structured concept review and concise retrieval cues (`P11`) preserving all applicability conditions, plus separately curated further-learning resources ([resource-recommendations.md](../../workflows/research/resource-recommendations.md)) when helpful. Use [footer_widgets.md](../../../shared/footer_widgets.md) only for active vault workflows.

## Quality & validation gate

Validate Contract v3 (`validate_note.py --contract --evidence --pedagogical-plan`), ARRIE source coverage/citations, `PED-xxx` pedagogical quality, and runtime execution (`plan_notes.py verify-runtimes`) before publication. Repair the smallest affected region rather than regenerating the entire note.

**Positive examples:** *"Explain backpropagation from scratch with derivation, graph, example, and Python code."* / *"Teach me PCA from geometric intuition through eigenvalues."*  
**Negative examples:** *"Pandas cheat sheet"* -> `M3`; *"Solve these 10 integrals step by step"* -> `M4`; *"Compare Adam vs SGD"* -> `M7`.
