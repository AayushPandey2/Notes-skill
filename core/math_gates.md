# Mathematical Presentation & Precision Gates

## Purpose

Ensure every mathematical expression in Scriptorium theory notes is visually structured, progressively introduced, explained by **meaning**, and verified for exact terminology and arithmetic.

## Activation Trigger & Inputs

- **Activate when:** `math_depth >= 1`, knowledge type is `mathematical` or `scientific`, master is `M4`, or any displayed `$$...$$` block appears.
- **Dependencies:** [core/teaching_core.md](teaching_core.md), [adaptive-engine.md](../docs/procedures/authoring/adaptive-engine.md#selection-and-depth).

## Execution Rules — Spacious, Visual & Consistent Math

1. **Progressive Symbols & Native Delimiters:** Introduce symbols just in time as each equation enters (reserving the full Symbol Dictionary for the trailing Notation Reference). Use native `$...$` and separate-line `$$...$$` delimiters consistently with [authoring_rules.md](authoring_rules.md); never copy `\(...\)` or `\[...\]`.
2. **Individual Subsections for Primary Metrics/Formulas:** Never compress multiple core metrics or formulas (such as Euclidean, Manhattan, Minkowski, and Chebyshev distances) into consecutive text-heavy bullets with inline math. Give each metric or core rule its own numbered subsection (`#### 5.1.1 ...`), display equation, geometric/visual intuition, concrete numerical example, and usage condition.
3. **Keep Inline Math Short & Break Down Multi-Operator Equations:** Reserve `$...$` for short symbols (`$g_i$`, `$h_i$`, `$\lambda$`); move long fractions, summations, and substitutions into display `$$...$$` blocks. Do **not** use `\color{...}` or highlighting inside equations; when a complex equation combines multiple logical operations (e.g., $\arg\max$, $\sum$, indicator function), break its components down cleanly in a visible list or table beneath the equation.
4. **Never Compress Multiple Equations or Derivations:**
   - Introduce composite objectives with a high-level equation first, then present each component in its own display block.
   - Never compress differentiation, setting to zero, and rearrangement into one single-line `\implies` chain; use separate labeled steps or multiline `$$ \begin{aligned} ... \end{aligned} $$` blocks with vertical `=` alignment and `\\[6pt]` spacing.
5. **Consistent Equation-Emphasis Policy (No Arbitrary Boxing or Highlighting):**
   - **Primary algorithm formulas** (including *both* uniform and weighted variants, or all peer update rules) → `\boxed{...}` (or `[!important]` callout).
   - **Mathematical definitions** → standard `$$...$$` display equation.
   - **Intermediate calculations** → multiline `aligned` steps.
   - **Final numerical answers** → bold text (never `==highlight==` or `\color{...}`).
6. **Meaning-First Visible Explanations (No Mechanical Formula Folds):**
   - **Do not** attach `> [!note]- 📐 Understand this formula` or `"Read aloud"` transcriptions beneath every `$$...$$` block, and **never hide core derivations** inside collapsed callouts.
   - Explain mathematical **meaning** visibly in crisp prose, using purposeful callouts (`[!info]`, `[!important]`, `[!example]`, `[!warning]`) selectively. Reserve collapsed callouts in theory notes strictly for optional extended proofs, nested checkpoint answers (`> > [!success]- Reveal Answer`), or advanced supplementary details.
7. **Exact Terminology & Complete Worked Examples:**
   - Maintain exact loss and algorithmic terminology (e.g., SSE vs. total half-squared-error loss, weighted vote proportions vs. calibrated probabilities).
   - Carry the **same running dataset** through multi-stage calculations (`1. Compute → 2. Sort/Select → 3. Aggregate → 4. Result`) for *every* core task promised in the learning objectives, visually separating inputs from calculated outputs.

## Failure Handling & Review

Locally repair compressed metric bullet lists, arbitrary `\boxed{}` usage, single-line derivations, heavy inline math, hidden core derivations, or missing worked examples before finalizing via [verification-checklist.md](../docs/procedures/review/verification-checklist.md).
