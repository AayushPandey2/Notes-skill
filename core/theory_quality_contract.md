# Universal Theory Quality Contract

## Purpose

Establish discipline-independent intellectual quality standards across substantive Scriptorium theory notes (`M1`, `M2`, `M4`, `M5`, `M7`, and video notes) so every subject—not only Machine Learning—achieves deep causal, structural, and analytical clarity. Apply these principles selectively where they serve the learning objective; never turn them into compulsory boilerplate headings.

## 1. Progressive Abstraction Ladder

Introduce concrete operations before formal abstractions so notation compresses something the learner already understands:

1. **Concrete observation:** Start with a particular object, system, or situation.
2. **Small worked example:** Demonstrate the behavior on tiny, inspectable values or states.
3. **General relationship:** Name the recurring pattern observed in the example.
4. **Formal representation:** Express the pattern with precise notation, equations, or rules.
5. **Abstract generalization:** Extend the representation beyond the opening example.
6. **Application and limitations:** Use the abstraction and examine where its assumptions break.

## 2. Cognitive Completeness & Concept Maturity (Mapped to Unified 0–5 Scale)

Evaluate substantive concepts across seven maturity facets mapped onto the unified `0–5` scale in [adaptive-engine.md](../docs/procedures/authoring/adaptive-engine.md)—matching target maturity to the learning objective without creating a competing numeric scale: **Recognition**, **Intuition**, **Mechanism**, **Formal understanding**, **Application**, **Prediction**, and **Critical understanding**. **Never consider a central concept complete merely because it has been defined** (`Level 1–2`); substantive core concepts must reach **Mechanism/Reasoning (Level 3)**, **Analytical Justification (Level 4)**, or **Independent Transfer (Level 5)**:

| Unified Depth | Standard | Example (Recursion) |
|---|---|---|
| **1–2. Recognition / Explanation** | Names, defines, and describes surface steps | A function calling itself (`n - 1` until `n == 0`). |
| **3. Mechanism** | Explains *why* the mechanism works causally | Each call solves a smaller instance; pending frames combine returned sub-results back up. |
| **4. Analytical** | States correctness conditions, invariants, resource costs, and failure modes | Requires a valid base case, progress toward termination, and call-stack space unless tail-call eliminated. |
| **5. Transfer** | Enables independent application to unfamiliar cases and reverse diagnosis | Identifies infinite-recursion bugs or converts tree recursion to iterative/tail-recursive form. |

## 3. Multi-Perspective & Alternative Explanation Selection

When a concept admits multiple valid approaches (for example, explaining **eigenvectors** via *geometric invariant directions*, *algebraic $Av = \lambda v$*, *computational characteristic equations/eigensolvers*, *structural invariant subspaces*, or *applied PCA/stability*), choose the **primary perspective** that best establishes the central intuition for the learner's goal and depth. Add a secondary perspective only when it contributes genuine non-redundant insight and connect them explicitly—disconnected parallel perspectives increase cognitive load without deepening understanding.

| Discipline | Complementary Perspectives |
|---|---|
| **ML** | Geometric, probabilistic, optimization, computational |
| **Calculus** | Algebraic, graphical, numerical, limiting behavior |
| **Programming** | Syntax, semantics, memory, execution |
| **Physics** | Mathematical, physical, experimental |
| **Chemistry** | Macroscopic, molecular, symbolic, energetic |
| **Biology** | Structural, functional, molecular, evolutionary |
| **Economics** | Graphical, mathematical, behavioral, empirical |
| **History** | Political, economic, social, institutional |
| **Philosophy** | Logical, conceptual, historical, critical |

## 4. Forward and Reverse Reasoning

Teach both directions wherever mastery requires diagnosis, design, or inference:

- **Forward reasoning:** Given inputs, laws, or initial conditions, predict the output or behavior.
- **Reverse reasoning:** Given an observed output, failure, or measurement, infer plausible inputs, mechanisms, or violated conditions.
- **Underdetermination discipline:** Reverse reasoning often admits multiple explanations; distinguish unique conclusions from plausible hypotheses and state what additional evidence discriminates between them.

## 5. Ideal-to-Real Model Progression

Whenever idealization is central to a subject (e.g., frictionless motion → drag; ideal gas → intermolecular forces; ideal diode → forward drop/leakage; reliable channel → loss/congestion; constant-time ops → memory hierarchy; perfect competition → market power/asymmetry; simple Mendelian → polygenic/environmental; IID data → distribution shift), make the transition explicit:

1. State the idealized model and its simplifying assumptions.
2. Explain which assumptions are relaxed in the refined model.
3. Explain why the refined model matches reality better and what new complexity or failure mode it introduces.

## 6. Knowledge-Boundary, Claim-Classification & Scientific Precision Policy

Treat different epistemic statuses accurately in natural prose (without mechanically attaching a bracketed tag to every sentence), preserving technical precision even while simplifying: explain the boundaries of important analogies, refine introductory simplifications before formal reasoning relies on them, distinguish mathematical guarantees from typical empirical behavior, and qualify version-dependent implementation details:

| Claim Type | Required Treatment |
|---|---|
| **Definition** | State precise meaning and scope convention |
| **Axiom** | Establish as an accepted starting assumption |
| **Theorem** | State hypotheses/conditions and provide appropriate justification |
| **Empirical law** | Explain observed regularity and validity regime |
| **Scientific model** | State assumptions and predictive scope |
| **Approximation** | State what is simplified and the error regime |
| **Hypothesis** | Distinguish proposed explanation from established consensus |
| **Interpretation** | Identify supporting evidence and competing accounts |
| **Convention** | Note that alternative conventions exist |
| **Best practice** | Explain context and governing trade-offs |
| **Implementation detail** | Identify the relevant language, library, platform, or version |
| **Open problem** | Separate what is established from what remains unresolved |

## 7. Question-Specific Explanation Patterns

Match the reasoning structure to the heading's question so a *"why"* question is never answered with a bare definition or a *"how"* question with a list of benefits:

| Question Pattern | Required Reasoning |
|---|---|
| **What is X?** | Definition, ordinary-language meaning, concrete example, nearest boundary |
| **Why does X exist?** | Problem solved, need, limitations of simpler alternatives |
| **How does X work?** | Ordered mechanism and causal state transitions |
| **Why does X work?** | Underlying principles, invariants, or logical justification |
| **What happens if X changes?** | Sensitivity analysis and changed assumptions |
| **When does X fail?** | Violated preconditions, failure mechanism, observable consequences |
| **When should X be used?** | Decision criteria, trade-offs, and alternatives |
| **How is X derived?** | Starting assumptions and justified transformations |
| **How do we know X?** | Evidence, measurement, experiment, or proof |
| **How does X differ from Y?** | Common basis of comparison and discriminating conditions |
| **Can X be generalized?** | Broader formulation and which properties survive or break |

## 8. Nested Mechanisms, Conceptual Transfer & Application Mapping

- **Nested mechanisms:** When a mechanism contains sub-mechanisms (e.g., Transformer → attention → scaled dot product; organism → cell → pathway), establish the **parent purpose**, explain the **internal behavior**, and **return to its role** inside the larger system.
- **Conceptual transfer:** Where helpful, connect topics through shared underlying principles (*feedback, equilibrium, conservation, hierarchy, information, optimization, uncertainty, state transitions, generalization, stability*). Always state both the shared structure and **where the analogy breaks**.
- **Concept-to-application mapping:** Never list bare industry names (`"used in navigation and social networks"`). For every substantive application, map the abstract construct onto concrete objects, relations/operations, and domain limitations (e.g., for graphs: what vertices represent, what edges represent, which query is solved, and what breaks the model).

## 9. Rigorous Theory Note Closing

End substantive theory notes with a concise **Mental Model** (enabling the learner to reconstruct the central mechanism, not merely repeat headings) and trailing **Notation Reference** (when quantitative). Selectively add only the closing elements that add distinct value:

- *Concept relationships* (how major ideas interlock)
- *Conditions of applicability* (where the theory holds vs. breaks)
- *Important distinctions* (resolving easily confused pairs)
- *Unifying principle* (deeper idea tying the note together)
- *Recognition cues* (when to reach for this method)
- *Knowledge boundary* (what the note deliberately does not establish)
- *Next intellectual dependency* (what to study next, aligned with `nexttopics`)

## 10. Anti-Patterns (What Scriptorium Must Never Become)

- Never turn these standards into dozens of compulsory headings or inflate word count as a proxy for depth.
- Never force ML datasets, equations, or code onto unrelated subjects.
- Never produce disconnected blocks of definitions, formulas, and examples, or repeat the same prerequisite across unrelated sections.
- Never treat an unverified self-assessment as proof of educational quality.

## 11. Educational Depth Preservation Contract

Theory must be the central strength of comprehensive notes rather than a brief introduction before formulas or implementation. Distinguish clearly between **Description** (*what happens*), **Mechanism** (*how it happens*), **Justification** (*why it happens*), **Prediction** (*what changes under altered conditions*), **Interpretation** (*what the outcome means*), and **Limitation** (*when the explanation becomes unsuitable*).

Preserve full intellectual depth wherever a substantive explanation requires space, ensuring a comprehensive `M1` note reads as a complete, self-contained learning chapter—never a condensed technical reference for someone who already knows the field:

1. Never sacrifice conceptual depth or beginner accessibility for conciseness, context-saving goals, visually compact layout, or a rush to formulas.
2. Remove genuine redundancy and empty filler, never necessary reasoning, foundational bridges, or explanatory depth.
3. Never skip consequential mathematical derivation steps or prerequisite mathematical tools.
4. Explain *why* every major mechanism works, not merely *how*.
5. Allow multiple examples when they reveal different properties, regimes, or tasks.
6. Do not impose a maximum word or line count on `M1` theory, and never impose an arbitrary minimum word-count target either—optimize for genuine learner understanding without inflating text via generic statements or repeated definitions.
7. Split exceptionally broad topics into coherent chapters rather than compressing their explanations into a narrow formula summary.
8. Keep beginner-friendly explanations detailed, even when they require significantly more space, without repeating full prerequisite courses unnecessarily.
9. Treat resource limitations as reasons to disclose incomplete coverage, not silently reduce depth.
10. Ensure editorial review never removes unique educational information.

Follow the [math policy](math_gates.md) for the steps, assumptions, and visible reasoning needed in a complete derivation.

## Complete Learning Units & Algorithmic Planning Guide

A topic mention establishes coverage at recognition depth. For comprehensive `M1` topics, cover the subject's major intellectual pillars proportionally—foundations and simpler baselines, core mechanism and necessary mathematical tools, major task types or variants, practical configuration and workflows, limitations and failure modes, comparisons with nearest alternatives, and authoritative primary references—rather than over-concentrating on one sub-formula while silently omitting the rest of the topic. For each core concept, develop its identity and purpose, the mechanism and why it works, and a consequence or limit at the intended depth, alongside necessary mathematics and application. At target depth 3 or higher, give the reader enough prior knowledge to reconstruct what happens and why. For a consequential comparison, explain each mechanism first, then change one relevant condition and explain the outcome. Move supporting tangents to an extension. When a chapter is broad, divide it at conceptual boundaries and keep each delivered unit complete.

When teaching **algorithmic topics** (never forced onto non-algorithmic disciplines), plan appropriate coverage across the algorithm lifecycle: problem definition & inputs/outputs (and why simpler approaches fall short), conceptual mechanism independent of syntax, key components/states, mathematical objective & updates, step-by-step trace exposing state changes, repeated/iterative carryover across multiple rounds, unseen-input output/inference, complexity with stated assumptions, parameters via actual effect on mechanism, failure conditions, balanced comparisons without simplistic winners, and non-executed implementation relationships.
