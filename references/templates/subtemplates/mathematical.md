# Subtemplate: Mathematical

- **Purpose:** Teach theorems, derivations, quantitative relations, and numerical problem solving by bridging intuition and visual meaning into rigorous symbols, transformations, and checks.
- **Activation conditions:** Displayed equations, formal derivations, proofs, quantitative modeling, or worked numerical problems (`mathematical`).
- **Expected inputs:** Governing equations, symbol dictionary (with types, dimensions, units), prerequisites, assumptions/domain restrictions, non-obvious transformation steps, and a stable numerical fixture.

> **Authoring-agent image instruction:** Before drafting, identify the visual learning needs of each substantive concept. Acquire suitable images where they materially improve understanding. Inspect the saved images, then compose the explanation around their actual visible content. Do not treat image placement as an optional finishing step.

- **Teaching progression:** Bridge via **Question → intuition → visual meaning → symbols → formula → calculation → interpretation → check** ([teaching_core.md](../../../shared/teaching_core.md) & [math_gates.md](../../../shared/math_gates.md)) using question-driven headings; never drop an equation before motivating what problem it solves.
- **Necessary prerequisite bridges:** Define every symbol, index, operator, quantifier, and unit/shape before first use; provide read-aloud phrasing for unfamiliar notation.
- **Visual opportunities:** Follow [representations.md](../../workflows/notes-creation/representations.md) using the six-phase visual narrative. Image opportunities: geometric constructions, function/contour plots, probability distributions, and coordinate transformations (use inspected local raster plots rather than Mermaid for accurate curves or geometry).
- **Formalism appropriate to the knowledge type:** Use native Obsidian `$...$` / `$$...$$` delimiters, pair every displayed equation with `> [!note]- 📐 Understand this formula`, state all assumptions/domain restrictions explicitly, justify non-obvious transformations, and distinguish numerical evidence from universal proof.
- **Worked-example requirements:** Work one small numerical fixture completely with explicit intermediate arithmetic, carefully interpret what the result measures vs. what it does not establish, test a boundary/degenerate case (or counterexample when relevant), and add a transfer check.
- **Evidence requirements:** Distinguish source derivations from added explanatory bridges; verify arithmetic independently and label unchecked calculations as manual review.
- **Practice and mastery checks:** Include derivation-step, boundary-case, calculation-interpretation, and diagram-reading checks with separately positioned collapsed answers.
- **Failure handling:** Locally repair naked equations, undefined symbols, dimension mismatches, raw LaTeX outside delimiters, nested formula callouts, or uninterpreted numbers via [verification-checklist.md](../../workflows/validation/verification-checklist.md).
