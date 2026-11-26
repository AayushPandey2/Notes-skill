# Mathematics Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Mathematical Contract
Applies to proofs, symbolic constructions, linear algebra, calculus, discrete math, and numerical analysis. State definitions, hypotheses, quantifiers, and domain restrictions once. **Do not** force numerical examples onto abstract proof topics or force programming tracks onto non-computational mathematics.

## Practical Realizations
1. **Analytical / Symbolic Construction:** Exact symbolic derivation, logical proof, or formal construction.
2. **Concrete Example (Numerical or Logical):** Worked exact-arithmetic example *or* concrete non-numerical logical/structural construction matching the topic.
3. **Alternative Representation:** Geometric, graphical, or second independent mathematical method showing why the result holds.
4. **Verification, Counterexamples, Boundaries & Independent Practice:** Independent substitution/invariant checks, hypothesis-relaxation tests, explicit counterexamples (plus a minimal verification snippet *only* when computation serves the objective), and 1–2 **Independent Exploration Prompts** (`> [!hint]-` / `> [!success]-`).

## Specialized Walkthrough & Verification
Verify every consequential transition and boundary case (zero divisors, defective matrices, dropped hypotheses), distinguish author-derived analytical results from actually performed checks, and end non-code labs with **`Analytical and manual proof review only (no code executed).`** (or **`Source and static review only; not compiled or executed here.`** if code appears).
