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
- **Core Rule**: Organize around **problems and their Step 1–12 solution procedures** ([math_gates.md](../../../core/math_gates.md): Question -> Method & Assumptions -> Symbols & Dimensions -> Formula -> Substitute Inputs -> Intermediate Arithmetic -> Final Answer -> Contextual Interpretation -> Sanity Check -> Common Mistakes -> Generalization), never long textbook chapter prose or bare final numbers. Every intermediate step must be explicitly justified and checked.

## 1. Problem Set Scope, Governing Tools & Method Selection Map

- State the problem family, shared definitions/notation, and exact assumptions/theorems invoked across the set.
- Compact **Recognition-to-Method Table**: `Problem Pattern | Governing Method / Theorem | Key Precondition | Common Trap`.

## 2. Step-by-Step Worked Solutions

For each problem (`### Problem <k>: <Short Title>`), include the needed logical elements:
1. **Problem Statement, Given & Objective**: Exact statement, known values/units/constraints, and target quantity.
2. **Method Selection & Preconditions**: Why this rule/theorem applies and confirmation of its hypotheses.
3. **Intermediate Steps & Calculations**: Numbered transitions with explicit justification at every non-obvious step (zero skipped algebra or hidden domain divisions).
4. **Final Answer**: Clearly highlighted result with units, dimensions, or domain qualifiers.
5. **Verification**: Independent substitution, dimensional check, boundary test, or numerical check confirming the answer solves the stated problem.
6. **Alternative Method or Common Error** *(conditional)*: Include only when an alternative shortcut or frequent trap genuinely prevents mistakes.

## 3. Synthesis of Solution Patterns & Pitfalls

- Concise summary of how to recognize which method applies on unseen variations, linking back to full conceptual notes (`M1`/`M2`) where available.
- **Verification Integrity**: Recalculate every numerical step carefully; under `strict` source mode, distinguish source problems from added practice variations.

See [authoring rules](../../../core/authoring_rules.md), [math gates](../../../core/math_gates.md), and [footer contract](../../../core/footer_widgets.md).
- **Template Contract (`M4` / `worked-solutions`):** Lead with problem-solving structure, show every consequential intermediate step, verify every final answer independently, and preserve all theorem hypotheses.
