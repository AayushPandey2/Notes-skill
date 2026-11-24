# Mathematical Reasoning & Formula-Fold Gates

## Purpose

Ensure every mathematical expression is built from scratch—motivated, read aloud, dissected piece by piece, verified across negative/zero/positive/boundary inputs, and connected smoothly from **Question → intuition → visual meaning → scalar case → general summation/vector form → calculation → interpretation → sanity check**.

## Activation Trigger & Inputs

- **Activate when:** `math_depth >= 1`, knowledge type is `mathematical` or `scientific`, master is `M4`, or any displayed `$$...$$` block appears anywhere.
- **Inputs:** Concept objective, depth (`M0`–`M5` for deep notes; `math_level` `0`–`2` for source/compact routes), governing equations, upfront symbol dictionary, local foundation rules, and the stable running fixture.
- **Dependencies:** [core/teaching_core.md](teaching_core.md), [adaptive-engine.md](../docs/procedures/authoring/adaptive-engine.md#selection-and-depth).

## Execution Rules — Complete Mathematical Teaching Standard

1. **Pre-Equation Foundations & Clash Checks:** Never assume familiarity with constants ($e$, $\pi$), logs, summations ($\sum$), products ($\prod$), or derivatives ($\frac{d}{dx}$, $\partial$). Explain required math tools locally with small value tables first. Include an upfront **Symbol Dictionary** (`Symbol | Meaning`) and flag any standard textbook notation clashes (e.g., $\hat{y}$ vs $p$, $n$ vs $m$).
2. **Simple → Multi → Compact Progression:** Always introduce a 1-variable concrete scalar formula before multi-variable summations and vector/matrix transpose notation ($\mathbf{w}^\top \mathbf{x} + b$), showing matrix shape compatibility (`(n×m)(m×1) = (n×1)`) visually.
3. **Native Obsidian Delimiters:** Use `$...$` and separate-line `$$...$$` consistently with [authoring_rules.md](authoring_rules.md) (never copy `\(...\)` or `\[...\]` from external samples, and never leave raw LaTeX commands outside math delimiters).
4. **Visible Part-by-Part Intuition + Multi-Case Checks + Collapsed Support:**
   - Beneath key governing formulas, keep essential part-by-part intuition (`Part | Purpose` table), multi-case numerical tests (**negative / zero / positive / extreme limits**), and critical *"does NOT imply"* caveats (e.g., odds ratio vs. probability) visible in crisp micro-paragraphs so the reader learns without hunting inside folds.
   - Pair every displayed `$$...$$` equation with an immediately following `> [!note]- 📐 Understand this formula` callout (quoting every line including blank separator lines with `>`) covering read-aloud phrasing, symbol/type/unit breakdown, assumptions (distinguishing **approximation**, **identity**, **assumption**, **empirical observation**, and **theorem**), full step-by-step transformations/derivation without skipping steps, numerical stability notes (e.g., overflow clipping or log-sum-exp where computational), and sanity checks.
5. **Multi-Iteration Hand Trace & One Canonical Fixture:** For iterative algorithms, trace **Iteration 1** and **Iteration 2** across a single canonical 3–4 point fixture (with intermediate columns) so the learner verifies convergence direction numerically. Never repeat identical dummy arithmetic unnecessarily; carry the same fixture across loss, gradient, and metric sections.

## Failure Handling & Review

Locally repair unprepared equations, stacked equations without prose, skipped algebraic cancellations, missing symbol clashes, or uninterpreted numbers before verifying against [verification-checklist.md](../docs/procedures/review/verification-checklist.md).
