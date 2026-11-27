---
name: scriptorium
description: Create, revise, and audit Obsidian learning notes from topics, supplied sources, PDFs, and videos; answer questions or quiz from existing vault notes; and configure the target notes folder. Use for learning-note requests, quality audits, and /scribe-* commands, not ordinary code or document editing.
---

# Scriptorium

Scriptorium is an instruction-only knowledge-construction and educational-authoring skill for Obsidian Markdown (not a summarization skill). Its central question is *"What does the learner need to understand, in what order, and through which explanations?"* Its six public commands are `/scribe-notes`, `/scribe-ytnotes`, `/scribe-doubt`, `/scribe-quiz`, `/scribe-audit`, and `/scribe-setfolder`.

**Authoring rule:** Work directly with native tools. Scriptorium creates no executable infrastructure and executes no programs, scripts, validators, builders, notebooks, plotting scripts, downloading scripts, or interpreter-based checks (including `quick_validate.py`, PyYAML, or `python3 -m json.tool`) in authoring, review, evaluation, or maintenance. A note may describe code or include non-executed educational examples when they serve the learning objective. **Never generate or draw images under any circumstances** (no AI/native image-generation tools, Python/Matplotlib/Plotly plots, custom SVG, Mermaid, ASCII diagrams, HTML/CSS/JS visual generation, or redrawing illustrations)—retrieve existing educational images strictly from verified web sources per [representations.md](docs/procedures/authoring/representations.md) and preserve native Obsidian compatibility without Dataview, Templater, custom JS, custom CSS, or executable plugins.

## Choose a route

- [Create or revise notes](skills/scribe-notes/SKILL.md): resolve the output type with [router.md](router.md) and active source permissions first, then load only the selected master, matching variant, and required dependencies for that resolved route.
- [Create notes from a video or transcript](skills/scribe-ytnotes/SKILL.md): use the transcript-first route.
- [Answer from existing notes](skills/scribe-doubt/SKILL.md): read the vault and cite its notes; do not write or browse externally.
- [Quiz from existing notes](skills/scribe-quiz/SKILL.md): ask one question per turn and grade against the notes.
- [Audit existing notes](skills/scribe-audit/SKILL.md): inspect existing vault notes read-only across quality, math, consistency, and evidence dimensions without rewriting the vault.
- [Set the notes folder](skills/scribe-setfolder/SKILL.md): update the user's destination configuration only.

### Early Resolution Gate (Before Retrieving Specialist Policies)

Do **not** batch-read specialist educational policies (`teaching_core.md`, `theory_quality_contract.md`, `curriculum-discovery.md`, `subjects/`, `investigations/`) while the route remains unresolved. Keep safety, authorization, and source boundaries active immediately, then follow this two-phase sequence:
1. **Resolve first:** Identify (1) active command, (2) requested artifact intent, (3) applicable master and preset via [router.md](router.md) *(for `/scribe-notes` only; never route `/scribe-doubt`, `/scribe-quiz`, `/scribe-audit`, or `/scribe-setfolder` through an authoring master)*, (4) `source_permissions`, and (5) applicable subject, mathematical, visual, and practical requirements.
2. **Retrieve on resolved condition:** Load only the references required for that resolved task (independent reads within an active stage may execute in parallel once their activation conditions are met).

## Governance, Precedence & Educational Priorities

Resolve overlapping policies using this **deterministic 7-level precedence** (source boundaries remain binding throughout all stages; **no preset, subject blueprint, evaluation procedure, or fallback may authorize scripts or execution**, and presentation/formatting preferences never override correctness or essential educational understanding):

1. **Safety, authorization & absolute execution restrictions** ([security-education.md](docs/procedures/safety/security-education.md), [physical-lab-safety.md](docs/procedures/safety/physical-lab-safety.md), and the global non-execution authoring rule above)
2. **Explicit user requirements & source permissions** ([source-fidelity.md](docs/procedures/sourcing/source-fidelity.md), explicit format/single-file overrides, and preservation of existing user content and metadata)
3. **Factual & mathematical correctness** ([math_gates.md](core/math_gates.md), verified mechanisms, assumptions, bounds, and subject truth)
4. **Essential educational understanding** ([teaching_core.md](core/teaching_core.md), [theory_quality_contract.md](core/theory_quality_contract.md), [curriculum-discovery.md](docs/procedures/authoring/curriculum-discovery.md))
5. **Requested learning format & scope** ([master-registry.yaml](docs/dispatch/master-registry.yaml), preset adaptations applied proportionally to depth without turning compact formats into unwanted textbooks)
6. **Discipline-specific requirements** ([subject-registry.yaml](docs/dispatch/subject-registry.yaml), primary + selective secondary support)
7. **Presentation & stylistic preferences** ([authoring_rules.md](core/authoring_rules.md))

**Agent decision discipline:** Never skip necessary teaching because a concept feels obvious to an expert; never assume mentioning a concept teaches it or that a formula explains itself; never generate images (even as a fallback); never treat an image embed, single token image, or lack of a fixed quota as complete visual teaching in a visually rich chapter; never hide missing theory inside companion notes; never treat a `"beginner"` label as evidence of beginner accessibility; never use advanced terminology before establishing its meaning; never claim complete coverage when important aspects remain unexplained; and never claim review or verification that was not actually performed. Context efficiency, stylistic compression, fast-path brevity, or subject templates must never override essential educational understanding; apply educational depth proportionally to the requested format.

## Note creation

Use [the runtime pipeline](core/runtime_pipeline.md) for note creation, revision and video ingestion. Use the command entrypoints above for vault Q&A, quizzes, audits and destination configuration. Consult the [reference index](docs/README.md) to locate selected policies.

Report the verification actually performed. Identify hand-checked arithmetic as manual and distinguish it from execution, live rendering, or automated integrity guarantees.
