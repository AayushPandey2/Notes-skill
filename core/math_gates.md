# Mathematical Presentation & Precision Gates

## Purpose

Ensure every mathematical expression in Scriptorium theory notes is genuinely accessible to beginners—spaciously formatted, progressively introduced, explained by **meaning** rather than mechanical symbol transcription, and verified for exact terminology and arithmetic.

## Activation Trigger & Inputs

- **Activate when:** `math_depth >= 1`, knowledge type is `mathematical` or `scientific`, master is `M4`, or any displayed `$$...$$` block appears.
- **Dependencies:** [core/teaching_core.md](teaching_core.md), [adaptive-engine.md](../docs/procedures/authoring/adaptive-engine.md#selection-and-depth).

## Execution Rules — Spacious & Meaning-First Math

1. **Progressive Symbols & Native Delimiters:** Introduce symbols just in time as each equation enters (reserving the full Symbol Dictionary for the trailing revision section). Use native `$...$` and separate-line `$$...$$` delimiters consistently with [authoring_rules.md](authoring_rules.md); never copy `\(...\)` or `\[...\]`.
2. **Keep Inline Math Short:** Reserve `$...$` for short symbols (`$g_i$`, `$h_i$`, `$\lambda$`). Move long fractions, summations, substitutions, and multi-step calculations into separate display `$$...$$` blocks so prose remains readable.
3. **Never Compress Multiple Equations or Derivations:**
   - Introduce composite objectives with a high-level conceptual equation first (e.g., $\mathcal{L} = \text{Training Loss} + \text{Regularization}$), then present each component in its own numbered display block with plain-language explanation.
   - Never compress differentiation, setting to zero, and algebraic rearrangement into one single-line `\implies` chain. Present derivations as separate labeled steps or a multiline `$$ \begin{aligned} ... \end{aligned} $$` block with vertical `=` alignment and `\\[6pt]` row spacing.
4. **Distinguish Core Formulas Visually:** Highlight the central formulas a learner must remember (using `\boxed{...}` and dedicated interpretation prose) so they stand out cleanly from intermediate substitutions and auxiliary definitions.
5. **Meaning-First Visible Explanations (No Mechanical Formula Folds):**
   - **Do not** attach `> [!note]- 📐 Understand this formula` or mechanical `"Read aloud"` transcriptions beneath every `$$...$$` block.
   - **Never hide core derivations** (such as optimal weights, gradients, or key identities) inside collapsed callouts. Explain mathematical **meaning** visibly in crisp prose (what the numerator, denominator, sign, and regularization parameter control), using purposeful visible callouts (`Definition`, `Intuition`, `Worked example`, `Common mistake`) only where they clarify.
   - Reserve collapsed callouts in theory notes strictly for optional extended proofs, hidden checkpoint answers (`> [!tip]- Answer`), or advanced supplementary details.
6. **Exact Terminology, Assumptions & Consistent Worked Examples:**
   - Maintain exact mathematical terminology (e.g., distinguish **sum of squared errors** $\sum(y_i - \hat{y}_i)^2$ from **total half-squared-error loss** $\frac{1}{2}\sum(y_i - \hat{y}_i)^2$).
   - Qualify closed-form solutions accurately (e.g., exact for the stated quadratic approximation under convexity assumptions, not necessarily for the original nonquadratic objective).
   - Trace iterative algorithms step by step on the **same running dataset** introduced early in the note, visually separating given inputs from calculated outputs.

## Failure Handling & Review

Locally repair compressed single-line derivations, heavy inline math, hidden core derivations, mechanical `"Read aloud"` filler, wrong loss terminology, or unedited error transcripts before finalizing via [verification-checklist.md](../docs/procedures/review/verification-checklist.md).
