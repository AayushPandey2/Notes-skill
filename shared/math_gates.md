# Math levels

- **0 — No formal math.** Use prose invariants, state transitions, constraints and manual traces. Omit the equation preview, display equations, mathematical anatomy and derivation sections completely.
- **1 — Operational formula.** Under the H1 provide an `[!abstract] Key Equations` preview with 1–3 core display equations and short symbol introductions. In the applicable mechanism/theory section, state the domain and assumptions and show the governing display equation. Include the tables below. For a practice set use the scoped formulas from its notes and place tables/derivation in the scope section without revealing exercise solutions.
- **2 — Derivation and limits.** Include level 1. Before the equation write 1–2 paragraphs of mathematical intuition about geometry, scale, dependence, and sensitivity. Analyze zero, normalized ±1, a degenerate or tie case, and ±∞ after stating the valid domain. Explain when a listed regime is outside that domain. Give a concrete counterexample to overgeneralization.

## Complete Symbol Anatomy

| Symbol / Operator | Meaning | Shape / Dimensions | Domain / Units | Directional Sensitivity |
|---|---|---|---|---|

Define each symbol, index and operator before use. Quantify how a change affects the output or why direction alone is insufficient.

## Input-to-Output Behavior

| Case | Concrete Inputs | Intermediate Computation | Final Output | Interpretation |
|---|---|---|---|---|

Include four rows in order: smallest non-trivial case, named running example, perturbed input showing sensitivity, and boundary/degenerate case.

## Zero-skip proof or derivation (level 2)

State the target, domain and proof strategy. Number every nontrivial algebraic/calculus step, render it in display math, and immediately follow it with `*Why this step holds:*`. Name the assumption, domain/division guards, and whether the move is an equivalence or implication. Finish with a dimensional sanity check, engineering consequence, and the scope of what remains unproven.
