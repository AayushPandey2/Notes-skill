# Subtemplate: Mathematical

- **Purpose:** Teach theorems, derivations, quantitative relations, and numerical problem solving by building intuition before formalism and verifying every symbol, dimension, and step.
- **Activation conditions:** Displayed equations, formal derivations, proofs, quantitative modeling, or worked numerical problems (`mathematical`).
- **Required inputs:** Governing equations, symbol definitions with types/dimensions/units, prerequisites, assumptions/domain restrictions, derivation steps, and concrete numerical fixtures.

> **Authoring-agent image instruction:** Before drafting, identify the visual learning needs of each substantive concept. Acquire suitable images where they materially improve understanding. Inspect the saved images, then compose the explanation around their actual visible content. Do not treat image placement as an optional finishing step.

## Teaching Sequence

1. **Orient & motivate:** Explain what relationship the equation captures and what breaks without it before showing symbols.
2. **Prepare symbols & dimensions:** Define variables, constants, operators, indices, and units/shapes before first use.
3. **Display formula + collapsed walkthrough:** Pair every displayed `$$...$$` equation with an immediately following `> [!note]- 📐 Understand this formula` callout per [math_gates.md](../../../shared/math_gates.md).
4. **Derive & prove:** Justify non-obvious steps and state where assumptions enter; never treat a numerical example as a universal proof.
5. **Worked numerical check:** Substitute concrete inputs, show intermediate arithmetic inline, and run magnitude/unit/boundary sanity checks.

## Obligations

- **Evidence expectations:** Distinguish source derivations from added explanatory bridges; label unexecuted numerical checks as manual review.
- **Visual requirements:** Follow [representations.md](../../workflows/notes-creation/representations.md) using **Orient → Show → Explain → Work through → Connect**. Image opportunities: geometry diagrams, function behavior/surface plots, probability distributions, and coordinate transformations (use downloaded raster plots/figures rather than Mermaid for accurate curves or geometry).
- **Mathematical explanation requirements:** Enforce [math_gates.md](../../../shared/math_gates.md) (`M01`–`M14`); keep arithmetic inside folds inline, never nest `$$` inside callouts, and never leave raw LaTeX commands (such as `\frac`) outside `$...$` or `$$...$$`.
- **Practical-example requirements:** Solve at least one small concrete fixture end to end and test one boundary or degenerate case.
- **Failure handling:** Locally repair naked equations, undefined symbols, dimension mismatches, raw LaTeX outside delimiters, or skipped algebraic steps.
- **Completion checks:** Verify against [verification-checklist.md](../../workflows/validation/verification-checklist.md) — 100% formula-fold parity, valid delimiters, and verified arithmetic.
