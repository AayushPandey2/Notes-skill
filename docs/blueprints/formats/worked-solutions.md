# M4 — Worked Problems & Step-by-Step Solutions

*Master ID: `M4` (`worked_solutions`). Artifact policy: `single_artifact` per [master-registry.yaml](../../dispatch/master-registry.yaml).*

- **Header Block:** Standard Obsidian Properties YAML (`topic`, `tags`, `master_topic`, `domain`, `note_type: worked-solutions`) per [properties-policy.md](../../properties/properties-policy.md) + `# <nn>. <Topic> — Worked Problems & Solutions`.
- **Six Worked-Solution Modes:** Select the reasoning mode matching the discipline rather than forcing numeric calculations or boxed answers onto every problem:

| Mode | Applicable Problems | Required Verification Standard |
|---|---|---|
| **Calculation** | Math, physics, chemistry | Arithmetic, substitution, units/dimensions |
| **Proof construction** | Math, theoretical CS | Logical validity, exact hypotheses, edge cases |
| **Algorithm tracing** | DSA, programming, systems | Correctness invariants, input/edge-case coverage |
| **Diagnosis** | Debugging, networking, electronics | Discriminating evidence separating candidate causes |
| **Design** | Engineering, software architecture | Satisfaction of stated requirements & trade-offs |
| **Evidence interpretation** | Statistics, research, history | Supporting evidence & plausible alternative readings |

- **Valid vs. Unique Distinction:** For design, diagnosis, and historical/empirical interpretation, explicitly distinguish a *defensible valid solution* from a *unique solution* rather than pretending only one answer exists.

## 1. Problem Set Scope, Governing Tools & Method Selection Map
- State the problem family, shared definitions/notation, and exact assumptions/theorems invoked across the set.
- Compact **Recognition-to-Method Table**: `Problem Pattern | Governing Method / Theorem | Key Precondition | Common Trap`.

## 2. Step-by-Step Worked Solutions (with Optional Faded Progression)
For each problem (`### Problem <k>: <Short Title>`), include the needed elements:
1. **Problem Statement, Given & Objective:** Exact statement, known values/constraints, and target.
2. **Method Selection & Preconditions:** Why this rule/theorem/strategy applies and confirmation of hypotheses (e.g., distinguishing stationary points from extrema).
3. **Intermediate Steps & Reasoning:** Numbered transitions with explicit justification at every non-obvious step ([math_gates.md](../../../core/math_gates.md) when quantitative).
4. **Final Result:** Clearly stated conclusion (boxed numerical answer with units *when numeric*; valid conclusion/proof/design otherwise).
5. **Independent Verification:** Run the mode-appropriate verification from the table above.
6. **Deepening Extensions** *(when pedagogically valuable)*: **Alternative method**, **Incorrect solution analysis**, and **Transfer variation**.

- **Faded Worked Examples (for multi-problem sets):** Gradually reduce scaffolding: *Problem 1 (full worked steps)* $\to$ *Problem 2 (method supplied, learner predicts intermediate steps with collapsed reveal)* $\to$ *Problem 3 (governing principle + hint only, collapsed solution)* $\to$ *Problem 4+ (independent problem with concealed `> [!tip]- Solution`)*.

## 3. Synthesis of Solution Patterns & Pitfalls
Summarize how to recognize which method applies on unseen variations and link back to conceptual notes (`M1`/`M2`). Under `strict` source mode, distinguish source problems from added variations.

*Contract: [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), [footer_widgets.md](../../../core/footer_widgets.md), [verification-checklist.md](../../procedures/review/verification-checklist.md).*
