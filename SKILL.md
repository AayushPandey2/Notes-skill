---
name: scriptorium
description: Create, revise, and audit Obsidian learning notes from topics, supplied sources, PDFs, and videos; answer questions or quiz from existing vault notes; and configure the target notes folder. Use for learning-note requests, quality audits, and /scribe-* commands, not ordinary code or document editing.
---

# Scriptorium

Scriptorium is an instruction-only skill for authoring Obsidian Markdown. Its six public commands are `/scribe-notes`, `/scribe-ytnotes`, `/scribe-doubt`, `/scribe-quiz`, `/scribe-audit`, and `/scribe-setfolder`.

**Authoring rule:** Work directly with native tools. Scriptorium creates no executable infrastructure and executes no educational code, scripts, builders, or custom validators in authoring, review, evaluation, or maintenance. A note may describe code or include non-executed examples when they serve the learning objective.

## Choose a route

- [Create or revise notes](skills/scribe-notes/SKILL.md): choose the output type with [router.md](router.md), then load only its master, needed variant, relevant knowledge-type subtemplate, and applicable policies from [docs/README.md](docs/README.md).
- [Create notes from a video or transcript](skills/scribe-ytnotes/SKILL.md): use the transcript-first route.
- [Answer from existing notes](skills/scribe-doubt/SKILL.md): read the vault and cite its notes; do not write or browse externally.
- [Quiz from existing notes](skills/scribe-quiz/SKILL.md): ask one question per turn and grade against the notes.
- [Audit existing notes](skills/scribe-audit/SKILL.md): inspect existing vault notes read-only across quality, math, consistency, and evidence dimensions without rewriting the vault.
- [Set the notes folder](skills/scribe-setfolder/SKILL.md): update the user's destination configuration only.

## Governance & Deterministic Precedence

Resolve overlapping policies using this **deterministic 7-level precedence** (source boundaries remain binding throughout all stages; **no preset, subject blueprint, evaluation procedure, or fallback may authorize scripts or execution**, and presentation/metadata preferences never override correctness):

1. **Host safety, permission & authorization restrictions** ([security-education.md](docs/procedures/safety/security-education.md), [physical-lab-safety.md](docs/procedures/safety/physical-lab-safety.md))
2. **Global instruction-only & non-execution restrictions** (see the authoring rule above)
3. **Explicit user requirements & source restrictions** ([source-fidelity.md](docs/procedures/sourcing/source-fidelity.md), explicit format/single-file overrides, and preservation of existing user content and metadata)
4. **Factual, conceptual & mathematical correctness** ([math_gates.md](core/math_gates.md), verified mechanisms and subject truth)
5. **Requested output format & applicable preset** ([master-registry.yaml](docs/dispatch/master-registry.yaml), preset overrides over parent master defaults)
6. **Relevant subject-specific guidance** ([subject-registry.yaml](docs/dispatch/subject-registry.yaml), primary + selective secondary support)
7. **Presentation & optional teaching preferences** ([authoring_rules.md](core/authoring_rules.md), [teaching_core.md](core/teaching_core.md), [theory_quality_contract.md](core/theory_quality_contract.md))

## Note creation

Use [the runtime pipeline](core/runtime_pipeline.md) for note creation, revision and video ingestion. Use the command entrypoints above for vault Q&A, quizzes, audits and destination configuration. Consult the [reference index](docs/README.md) to locate selected policies.

Report the verification actually performed. Identify hand-checked arithmetic as manual and distinguish it from execution, live rendering, or automated integrity guarantees.
