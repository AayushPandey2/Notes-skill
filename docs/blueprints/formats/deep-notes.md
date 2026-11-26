# M1 — Comprehensive Theory Notes

- **Master ID:** `M1` (`deep_notes`)
- **Primary intent:** `comprehensive_learning` — deliver a complete, self-contained explanation from motivation and essential foundations through mechanisms, concrete reasoning, formal depth, limitations, and transfer.
- **Activation signals:** `"teach me from scratch"`, `"explain deeply"`, `"comprehensive notes"`, `"from fundamentals to advanced"`, or bare `/scribe-notes <topic>` without an explicit alternate format.
- **Non-activation:** Do not select `M1` when the user primarily requests a compact cheat sheet (`M3`), solved problem set (`M4`), implementation guide (`M5`), quiz/flashcards (`M6`), or standalone comparison/revision pack (`M7`).
- **Load as needed:** [teaching rules](../../../core/teaching_core.md), [theory quality contract](../../../core/theory_quality_contract.md), [math guidance](../../../core/math_gates.md), [visual rules](../../procedures/authoring/representations.md), [adaptive planning](../../procedures/authoring/adaptive-engine.md), [source fidelity](../../procedures/sourcing/source-fidelity.md), [authoring rules](../../../core/authoring_rules.md), and the primary subject blueprint in [subject-registry.yaml](../../dispatch/subject-registry.yaml).
- **Output profile:** Comprehensive collections use the five-key YAML profile in [properties policy](../../properties/properties-policy.md); single or existing notes use Standard Obsidian Properties without overwriting user-managed fields.

## 1. Opening Roadmap (Purpose, Learning Path & TOC)

Open cleanly with line-1 YAML, H1 title, a concise purpose and learning path (without repeating YAML `difficulty` as a visible body dump), and a compact **clickable Obsidian Table of Contents** (`- [[#1. Heading|Short Label]]`). Apply the two-dimension prerequisite policy in [teaching_core.md](../../../core/teaching_core.md): never use a link to replace an essential unmastered local foundation.

## 2. Progressive Explanation Flow (Discipline-Independent)

Load the matching knowledge-type subtemplate (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, or `historical`) and primary subject profile (`docs/blueprints/subjects/`). Let headings and structure emerge naturally from the subject rather than forcing identical headings or ML templates onto unrelated fields:

1. **One Conceptual Burden at a Time (Opening):** Introduce the central question, problem, or phenomenon in ordinary language before terminology or formalism (never stuffing advanced claims into an opening callout).
2. **Definitions & Local Prerequisites:** Teach essential building blocks locally; for key definitions, establish the need, state a concise definition, translate to ordinary language, provide a concrete example beside it, and state the nearest boundary—separating definition, consequence, assumption, and optional advanced property.
3. **Domain-Appropriate Mechanism & Example Portfolio:** Carry one consistent **running example, case, system, or evidence anchor** through the explanation, selectively adding *minimal, discriminating, boundary, counterexample,* or *transfer* examples where each clarifies a distinct point.
4. **Limitations of Simpler Baselines & Conceptual Surprise:** Show concretely why a naive or idealized baseline fails before introducing the richer mechanism or model.
5. **Continuous mathematical reasoning:** Use [math_gates.md](../../../core/math_gates.md) to order reasoning units by dependency. Let visible prose and milestone equations develop the argument, then complete each central derivation locally in the visible argument or in a descriptive formula fold below the principal result. Apply the canonical-reference rules in the math policy to prerequisites and reused results. Explain what the result lets the reader do next.
6. **Consequential Transitions, Result Interpretation & Micro-Checks:** Trace consequential state, logical, physical, or causal transitions step by step, interpret what the resulting outcome establishes (and does not establish), and optionally include a brief local reconstruction check or assumption-change analysis where helpful.
7. **Assumptions, Evidence, Validity Boundaries & Checkpoints:** Distinguish epistemic claim types ([theory_quality_contract.md](../../../core/theory_quality_contract.md)), qualify strong claims, state *"What It Does NOT Assume/Establish"* boundaries, and place visible `> [!question] Concept Checkpoint` blocks (with nested `> > [!success]- Reveal Answer`) where active checking adds value.

## 3. Closing & Companion Handoff

End cleanly with a concise **Mental Model** (when it aids reconstruction rather than repeating headings), a trailing **Notation Reference** *only when quantitative/symbolic notation warrants one*, and reciprocal links to `<note stem> - Experimental Lab.md` and `<note stem> - Cheatsheet & Interview Q&A.md` **only when those companions are included in the resolved `artifact_plan`** (per [adaptive-engine.md](../../procedures/authoring/adaptive-engine.md) and `artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml)).

Do **not** duplicate companion formula sheets, tiered interview/viva Q&A, or worked problem packs inside the main note when File 3 is generated. Review against [verification-checklist.md](../../procedures/review/verification-checklist.md) before saving; for multi-chapter `M1` collections, follow [composition-contract.md](../../procedures/authoring/composition-contract.md).

Plan complete learning units around questions the reader needs to answer. Give core mechanisms room for a concrete setup, step-by-step change, and interpretation. Use that visible teaching path to organize prose, examples, equations and figures before adding supporting callouts or assessments. If resource limits require partitioning, finish coherent sections and disclose outstanding scope.
