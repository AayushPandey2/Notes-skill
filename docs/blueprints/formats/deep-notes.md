# M1 — Comprehensive Theory Notes

- **Master ID:** `M1` (`deep_notes` / compatibility route `deepstudy-master`)
- **Primary intent:** `comprehensive_learning` — deliver a complete, self-contained explanation from motivation and essential foundations through mechanisms, concrete reasoning, formal depth, limitations, and transfer.
- **Activation signals:** `"teach me from scratch"`, `"explain deeply"`, `"comprehensive notes"`, `"from fundamentals to advanced"`, or bare `/scribe-notes <topic>` without an explicit alternate format.
- **Non-activation:** Do not select `M1` when the user primarily requests a compact cheat sheet (`M3`), solved problem set (`M4`), implementation guide (`M5`), quiz/flashcards (`M6`), or standalone comparison/revision pack (`M7`).
- **Load as needed:** [teaching rules](../../../core/teaching_core.md), [theory quality contract](../../../core/theory_quality_contract.md), [math guidance](../../../core/math_gates.md), [visual rules](../../procedures/authoring/representations.md), [adaptive planning](../../procedures/authoring/adaptive-engine.md), [source fidelity](../../procedures/sourcing/source-fidelity.md), [authoring rules](../../../core/authoring_rules.md), and the primary subject blueprint in [subject-registry.yaml](../../dispatch/subject-registry.yaml).
- **Output profile:** Comprehensive collections use the five-key YAML profile in [properties policy](../../properties/properties-policy.md); single or existing notes use Standard Obsidian Properties without overwriting user-managed fields.

## 1. Opening Roadmap (Purpose, Learning Path & TOC)

Open cleanly with line-1 YAML, H1 title, a concise purpose and learning path (without repeating YAML `difficulty` as a visible body dump), and a compact **clickable Obsidian Table of Contents** (`- [[#1. Heading|Short Label]]`). Apply the 3-tier prerequisite rule in [teaching_core.md](../../../core/teaching_core.md): never use a link to replace an essential local foundation.

## 2. Progressive Explanation Flow (Discipline-Independent)

Load the matching knowledge-type subtemplate (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, or `historical`) and primary subject profile (`docs/blueprints/subjects/`). Let headings and structure emerge naturally from the subject rather than forcing identical headings or ML templates onto unrelated fields:

1. **One Conceptual Burden at a Time (Opening):** Introduce the central question, problem, or phenomenon in ordinary language before terminology or formalism (never stuffing advanced claims into an opening callout).
2. **Definitions & Local Prerequisites:** Teach essential building blocks locally; for key definitions, establish the need, state a concise definition, translate to ordinary language, provide a concrete example beside it, and state the nearest boundary—separating definition, consequence, assumption, and optional advanced property.
3. **Domain-Appropriate Mechanism & Example Portfolio:** Carry one consistent **running example, case, system, or evidence anchor** through the explanation, selectively adding *minimal, discriminating, boundary, counterexample,* or *transfer* examples where each clarifies a distinct point.
4. **Limitations of Simpler Baselines & Conceptual Surprise:** Show concretely why a naive or idealized baseline fails before introducing the richer mechanism or model.
5. **Objective-Driven Formalism & Explicit Transitions:** When quantitative or formal, follow [math_gates.md](../../../core/math_gates.md) to choose each concept's minimum math profile, build the explanatory bridge before equations, never skip central steps, and attach `> [!example]- Understand this formula step by step` beneath coherent top-level displayed blocks.
6. **Consequential Transitions, Result Interpretation & Micro-Checks:** Trace consequential state, logical, physical, or causal transitions step by step, interpret what the resulting outcome establishes (and does not establish), and optionally include a brief local reconstruction check or assumption-change analysis where helpful.
7. **Assumptions, Evidence, Validity Boundaries & Checkpoints:** Distinguish epistemic claim types ([theory_quality_contract.md](../../../core/theory_quality_contract.md)), qualify strong claims, state *"What It Does NOT Assume/Establish"* boundaries, and place visible `> [!question] Concept Checkpoint` blocks (with nested `> > [!success]- Reveal Answer`) where active checking adds value.

## 3. Closing & Companion Handoff

End cleanly with a concise **Mental Model** (when it aids reconstruction rather than repeating headings), a trailing **Notation Reference** *only when quantitative/symbolic notation warrants one*, and reciprocal links to `<note stem> - Experimental Lab.md` and `<note stem> - Cheatsheet & Interview Q&A.md` **only when those companions are generated** under `artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml).

Do **not** duplicate companion formula sheets, tiered interview/viva Q&A, or worked problem packs inside the main note when File 3 is generated. Review against [verification-checklist.md](../../procedures/review/verification-checklist.md) before saving; for multi-chapter `M1` collections, follow [composition-contract.md](../../procedures/authoring/composition-contract.md).
