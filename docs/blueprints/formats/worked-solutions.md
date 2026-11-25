<!-- scaffold:preflight
Master ID: M4 (worked_solutions / route: worked-solutions).
Primary intent: worked_problem_solving — problem-centered step-by-step solutions with method selection, intermediate calculations, and verification.
Activation signals: "solve these problems", "worked solutions", "show every step/calculation", "solved examples", "explain how to solve".
Non-activation: "Teach me concept X with examples" -> M1 or M2; "Quiz me without answers" -> M6; "Implement a codebase" -> M5.
Contracts: [teaching core](../../../core/teaching_core.md), [router](../../../router.md), [authoring rules](../../../core/authoring_rules.md), [math gates](../../../core/math_gates.md), [pedagogical-intelligence](../../procedures/authoring/pedagogical-intelligence.md).
Strip this block before emission.
-->

# M4 — Worked Problems & Step-by-Step Solutions

- **Header Block**: Standard Obsidian Properties YAML (`topic`, `tags`, `master_topic`, `domain`, `note_type: worked-solutions`) per [properties-policy.md](../../properties/properties-policy.md) + `# <nn>. <Topic> — Worked Problems & Solutions`.
- **Six Worked-Solution Modes:** Select the reasoning mode matching the discipline rather than forcing one fixed algebraic template:
  - *Calculation* (math, physics, chemistry) · *Proof construction* (math, theoretical CS) · *Algorithm tracing* (DSA, programming, systems) · *Diagnosis* (debugging, networking, electronics) · *Design* (engineering, software architecture) · *Evidence interpretation* (statistics, research, history).
- **Core Rule**: Organize around problems and explicitly justified step-by-step reasoning ([math_gates.md](../../../core/math_gates.md) when quantitative), never long textbook prose or bare final answers. Every consequential step must be justified and verified independently.

## 1. Problem Set Scope, Governing Tools & Method Selection Map

- State the problem family, shared definitions/notation, and exact assumptions/theorems invoked across the set.
- Compact **Recognition-to-Method Table**: `Problem Pattern | Governing Method / Theorem | Key Precondition | Common Trap`.

## 2. Step-by-Step Worked Solutions (with Optional Faded Progression)

For each problem (`### Problem <k>: <Short Title>`), include the needed logical elements:
1. **Problem Statement, Given & Objective**: Exact statement, known values/units/constraints, and target quantity.
2. **Method Selection & Preconditions**: Why this rule/theorem/strategy applies and confirmation of its hypotheses (e.g., distinguishing stationary points from extrema, or checking input invariants).
3. **Intermediate Steps & Reasoning**: Numbered transitions with explicit justification at every non-obvious step (zero skipped algebra, hidden domain divisions, or unexplained state jumps).
4. **Final Answer**: Clearly stated result with units, dimensions, or domain qualifiers.
5. **Independent Verification**: Substitution, dimensional check, boundary test, invariant proof, or counter-check confirming the result solves the stated problem.
6. **Deepening Extensions** *(include when pedagogically valuable)*: **Alternative method** (showing a revealing second approach), **Incorrect solution analysis** (explaining why a plausible wrong method fails), and **Transfer variation** (modifying one condition and explaining how the solution changes).

- **Faded Worked Examples (for multi-problem practice sets):** Gradually reduce scaffolding across the set so learners transition to independent solving: *Problem 1 (full worked steps)* → *Problem 2 (method supplied, learner predicts intermediate steps with collapsed reveal)* → *Problem 3 (governing principle + hint only, collapsed solution)* → *Problem 4+ (independent problem with concealed `> [!tip]- Solution`)*.

## 3. Synthesis of Solution Patterns & Pitfalls

- Concise summary of how to recognize which method applies on unseen variations, linking back to full conceptual notes (`M1`/`M2`) where available.
- **Verification Integrity**: Recalculate every numerical step carefully; under `strict` source mode, distinguish source problems from added practice variations.

See [authoring rules](../../../core/authoring_rules.md), [math gates](../../../core/math_gates.md), and [footer contract](../../../core/footer_widgets.md).
- **Template Contract (`M4` / `worked-solutions`):** Lead with problem-solving structure, show every consequential intermediate step, verify every final answer independently, and preserve all theorem hypotheses.
