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

## 2. Cognitive Completeness (4 Levels)

Substantive core concepts must reach **Explanatory** or **Analytical** depth—never stop at terminology or surface operation when a mechanism is central to the topic:

| Level | Standard | Example (Recursion) |
|---|---|---|
| **1. Terminology** | Names and defines the concept | A function that calls itself. |
| **2. Operational** | Describes step-by-step surface behavior | Factorial calls itself with `n - 1` until `n == 0`. |
| **3. Explanatory** | Explains *why* the mechanism works | Each call solves a smaller instance; pending frames combine returned sub-results back up. |
| **4. Analytical** | States correctness conditions, invariants, resource costs, and failure modes | Requires a valid base case, progress toward termination, and call-stack space unless tail-call eliminated. |

## 3. Multi-Perspective Explanation

When a core concept cannot be fully understood from one angle, combine complementary perspectives and **connect them explicitly** (disconnected parallel explanations do not create integrated understanding):

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

## 6. Knowledge-Boundary & Claim-Classification Policy

Treat different epistemic statuses accurately in natural prose (without mechanically attaching a bracketed tag to every sentence):

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
