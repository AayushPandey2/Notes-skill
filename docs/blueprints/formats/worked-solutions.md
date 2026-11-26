# M4 — Worked Problems & Step-by-Step Solutions

*Master ID: `M4` (`worked_solutions`). Artifact policy: `single_artifact` per [master-registry.yaml](../../dispatch/master-registry.yaml).*

- **Header Block:** Standard Obsidian Properties YAML (`topic`, `tags`, `master_topic`, `domain`, `note_type: worked-solutions`) per [properties-policy.md](../../properties/properties-policy.md) + `# <Topic> — Worked Problems & Solutions` (prepend `<nn>. ` only inside a numbered multi-branch collection).
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

## 1. Problem Set Scope, Governing Tools & Method Selection Map *(Opening Proportionality)*
- Match opening weight to the actual complexity of the problem set (not problem count alone): for short 1–3 problem sets on one cohesive method, omit TOC/objectives and start cleanly after a compact 2–3 sentence tool/notation recap directly before Problem 1. Retain broader orientation and a **Recognition-to-Method Table** (`Problem Pattern | Governing Method / Theorem | Key Precondition | Common Trap`) whenever a set spans multiple methods, shared notation/hypotheses, substantial proofs, or genuine prerequisite gaps. Keep primary solution reasoning visible (collapsing hints, alternative methods, or faded-practice follow-ups only where appropriate).

## 2. Step-by-Step Worked Solutions (with Optional Faded Progression)
For each problem (`### Problem <k>: <Short Title>`), include the needed elements:
1. **Problem Statement, Given & Objective:** Exact statement, known values/constraints, and target.
2. **Method Selection & Preconditions:** Why this rule/theorem/strategy applies and confirmation of hypotheses (e.g., distinguishing stationary points from extrema).
3. **Intermediate Steps & Reasoning:** Show and justify every consequential step in the solution, keeping it within the existing answer fold when the format uses one. Use numbered transitions where they help the reader follow the method ([math_gates.md](../../../core/math_gates.md) when quantitative).
4. **Final Result:** Clearly stated conclusion (boxed numerical answer with units *when numeric*; valid conclusion/proof/design otherwise).
5. **Check the Result:** Apply the mode-appropriate check from the table above. Use a different line of reasoning where it can catch an error, such as substitution into the original equation or testing an invariant.
6. **Deepening Extensions** *(when pedagogically valuable)*: **Alternative method**, **Incorrect solution analysis**, and **Transfer variation**.

- **Faded Worked Examples (for multi-problem sets):** Gradually reduce scaffolding: *Problem 1 (full worked steps)* $\to$ *Problem 2 (method supplied, learner predicts intermediate steps with collapsed reveal)* $\to$ *Problem 3 (governing principle + hint only, collapsed solution)* $\to$ *Problem 4+ (independent problem with concealed `> [!success]- Solution`)*.

## 3. Synthesis of Solution Patterns & Pitfalls
Summarize how to recognize which method applies and link back to existing conceptual notes. Use variations only when the active source permissions allow them.

*Contract: [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), [footer_widgets.md](../../../core/footer_widgets.md), [verification-checklist.md](../../procedures/review/verification-checklist.md).*
