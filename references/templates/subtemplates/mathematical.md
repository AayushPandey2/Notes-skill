# Mathematical composition

Activate for a displayed equation, a mathematical objective, or a worked numerical problem (MATH-01 through MATH-10).

Before composition, supply the equation, its purpose, symbol meanings and types, prerequisite explanations, operation order, assumptions, and any numerical inputs. Supply dimensions for matrix operations. Use the twelve stages defined in [math_gates.md](../../../shared/math_gates.md); adapt stage depth to the actual formula rather than inventing irrelevant examples.

Bind every displayed `$$...$$` formula directly to an immediately following `> [!note]- 📐 Understand this formula` callout ([math_gates.md](../../../shared/math_gates.md)), covering applicable stages (`1`–`12`) and explicit intermediate arithmetic for worked examples.

For a proof, state the claim, assumptions, and why each step follows; a numerical example cannot prove a universal result. For a calculation, show actual intermediate values, units, and a magnitude or boundary check. Mark any computation that was not independently executed as a manual review.

Keep intermediate arithmetic inside folds inline. Distinct displayed derivation steps need separate sibling formula-and-fold components. Never nest display math inside a formula explanation.

Review the composed Markdown against [verification-checklist.md](../../workflows/validation/verification-checklist.md); missing, generic, or nested formula folds, dimension mismatches, or unverified arithmetic must be repaired locally before finishing. Do not replace a failure with a generic explanation.
