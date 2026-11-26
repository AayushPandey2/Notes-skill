# Mathematical Inclusion, Derivation & Presentation Policy

## Purpose

Govern **whether, how deeply, and how** mathematics appears across Scriptorium outputs (`M1`–`M7`, video notes, and companion labs/cheatsheets) in one coherent, instruction-only policy. Use one shared standard with focused domain guidance—never append competing rules or force irrelevant equations onto non-quantitative topics.

## 1. Objective-Driven Inclusion & Concept-Level Profiles

Before drafting each concept, decide whether mathematics serves the learning objective: what the learner must understand or accomplish, whether a mathematical representation reveals something essential, whether math is required to calculate, derive, implement, compare, or verify, and what prerequisite bridge makes it accessible.

- **Use math when it improves precision or enables the intended reasoning.** Never add equations merely because a subject is technical, and never omit necessary math merely because the audience is a beginner (supply the missing bridge instead of replacing the mechanism with an analogy).
- **Select depth per concept** using these internal planning profiles (planning decisions, **not** mandatory visible labels; different sections of one note may use different profiles):

| Profile | Appropriate treatment |
|---|---|
| **Conceptual** | No equations unless essential; teach through language, examples, and visuals. |
| **Quantitative intuition** | Small calculations, proportions, counts, units, or numerical comparisons. |
| **Working formulation** | Main equations, defined notation, interpretation, and a complete worked example. |
| **Derivation and mechanism** | Justified transformations, intermediate steps, assumptions, and implementation mapping where relevant. |
| **Formal reasoning** | Precise definitions, proofs, conditions, counterexamples, and generalization when required. |

- **Apply proportional rigor.** In comprehensive quantitative theory (including substantive M1, M2, M5, M7 and video notes), provide complete derivations under the locality rules below. In M4, show every consequential step in the solution itself. Apply the same rigor to worked M6 answers and companion labs where the exercise or implementation depends on it. Compact M3 references may give conditions, units and a canonical link.
- **Honor source permissions first.** Follow [source-fidelity.md](../docs/procedures/sourcing/source-fidelity.md). Reconstruct source-supported steps within the allowed scope. If a derivation needs unprovided premises, identities or instruction and additions are prohibited, disclose the gap. Permission to verify a claim does not authorize adding a derivation or browsing under strict policy.

## 2. Continuous Mathematical Reasoning & Complete Formula Derivations

### Visible Reasoning Units

A reasoning unit uses prose and connected equations to establish one mathematical result. Start with the problem, relevant quantities, available relationships and governing assumptions. Display the intermediate relationships the reader needs to follow the argument. Explain what each establishes and why the next operation follows. Finish with the result, its interpretation and the dependency it supplies to the next concept.

Read the main theory with all formula folds closed. The question, hypotheses, essential notation, turning points and conclusions should still be clear. Use a natural structure for the material: hypotheses and proof for a theorem, model and criterion for an estimator, or governing relationship and state trace for an algorithm. Introduce local definitions and conventions where they do explanatory work.

For an unfamiliar abstraction, work an ordinary case with meaningful quantities before introducing indices or a generalized family. Show which calculation becomes a term or operation in the general expression. Refer back to the visible example after formalizing it and interpret at least one outcome or boundary when it advances the objective. Lead with definitions or hypotheses directly when the audience or task warrants formal treatment.

### Required Coverage and Derivation Ownership

Every distinct consequential derivable relationship in comprehensive theory needs a complete derivation, subject to the source permissions above. Derive the topic's central results locally, in visible prose or a formula fold. For a result already derived in the chapter, point back to its section. If an essential prerequisite is unfamiliar, explain locally the part required for the next step. A brief anchor or accessible canonical link can support an established prerequisite or an optional extension. Verify that any cited derivation is accessible and uses compatible assumptions and notation. Disclose source-prohibited derivations as gaps.

### Complete Expandable Derivations

When a reasoning unit needs a local expandable derivation, attach one concise descriptive Obsidian callout after its principal result (prefer `> [!example]- Derivation: <Focus>` or `> [!example]- Proof: <Focus>` rather than repeating monotonous titles, keeping compatibility with existing `Understand this formula step by step` folds). Never duplicate algebraic steps already written in full in the visible prose immediately above—keep visible text focused on motivation, turning points, and consequences, and place full step-by-step algebra inside the fold:

`> [!example]- Derivation: <Concise focus>` *(or `> [!example]- Proof: <Concise focus>`)*

Use one fold for connected steps serving the same objective. Give a genuinely distinct local result its own derivation. Use the ownership rules above for canonical references. A derivation that is already in a worked solution, answer or lab fold stays there. If the derivation is itself the requested visible artifact, keep its consequential steps visible rather than duplicating it in another fold.

Cover the objective, starting principles, assumptions, applicable identities, notation (including domains, dimensions and units), intermediate transformations, formula structure, interpretation and verification. Explain which rule permits each consequential operation and why the new form helps. Use a numerical application, limiting case, counterexample or other independent check where it adds insight. These responsibilities guide the explanation without prescribing fixed subheadings. Numerical substitution, paraphrase and unexplained shortcuts cannot stand in for derivation.

### Classify the Relationship Before Explaining It

| Relationship | Treatment |
|---|---|
| Derived formula or identity | Justified steps from established results |
| Definition, axiom or convention | Meaning, motivation and applicability |
| Modeling assumption or empirical law | Rationale or evidence, alternatives and validity conditions |
| Theorem | Hypotheses, valid proof and implications |
| Approximation | Starting relation, simplifying assumptions and error or validity regime |
| Algorithm update | Mathematical justification, role of each term and a trace where helpful |
| Evaluation metric | Construction from error, count, ranking or probability quantities |
| Intermediate or reused formula | Explain locally in its parent unit or reference its canonical derivation |

## 3. Mathematical Dependencies & Depth

Establish unfamiliar identities before their first dependent use. Give familiar prerequisites a short anchor where that suffices for the learner. When component-to-matrix reasoning clarifies a vectorization, derive a representative component, show the indexed sum and then assemble the matrix form. For a naturally matrix-defined object, start at matrix level and unpack the relevant rows, columns or operator actions. Justify shapes, transposes and reductions wherever they matter.

Choose a derivation strategy that exposes the relevant structure: an indexed expansion for shapes, a geometric argument for invariance, or a Taylor model for a local update. After a consequential result, interpret a useful implication such as a stationarity condition, changed assumption, or limiting case. When it serves the objective, translate between a formula and its geometry, computation, or numerical realization. A short inverse problem can check whether the reader can reconstruct an input or assumption from an outcome.

Retain consequential assumptions, algebra, examples and limitations. Give longer arguments room or split broad topics into coherent chapters. Keep advanced alternative proofs and generalizations optional unless they are part of the requested scope.

## 4. Obsidian Rendering, Notation Hygiene & Code Alignment

- **Native delimiters only:** Use `$...$` inline and separate-line `$$` blocks (with blank lines around display math). Never mix delimiters, use code fences for equations, leave raw LaTeX in prose, place raw LaTeX inside Mermaid labels, or use `==highlight==` / `\color{...}`. Use inline math for short symbols and relations. Display longer transformations and separate independent stages with explanatory prose. Use `aligned`, `cases`, and `\text{...}` cleanly, leave an unquoted blank line before returning from a callout to visible prose, quote every callout line including blank lines (`>`), escape literal pipes (`\|`) in tables, and reserve `\boxed{...}` strictly for final governing results or key numerical answers.
- **Notation hygiene & code alignment:** Define symbols at first use, distinguish sample vs. feature indices, scalars vs. vectors/matrices, and estimates vs. true quantities. State residual conventions, align objective normalization/penalty scaling explicitly (`C` vs. `alpha`), and verify NumPy/framework operators (`@` vs. `*`, `**` vs. `^`, reduction axes, integer vs. float division, broadcasting, gradient sign, finite-precision cancellation/overflow guards).
- **Single canonical home:** Give each major derivation one canonical home; link or briefly reference prior results elsewhere unless context shifts require bridging.
