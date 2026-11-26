# Mathematics Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Mathematical Contract
Applies to proofs, symbolic constructions, linear algebra, calculus, discrete math, and numerical analysis. State definitions, hypotheses, quantifiers, and domain restrictions once. **Do not** force numerical examples onto abstract proof topics or force programming tracks onto non-computational mathematics.

## Practical Realizations
1. **Analytical / Symbolic Construction:** Exact symbolic derivation, logical proof, or formal construction.
2. **Concrete Example (Numerical or Logical):** Worked exact-arithmetic example *or* concrete non-numerical logical/structural construction matching the topic.
3. **Alternative Representation:** Geometric, graphical, or second independent mathematical method showing why the result holds.
4. **Verification, Counterexamples & Boundaries:** Independent substitution/invariant checks, hypothesis-relaxation tests, and explicit counterexamples (plus a minimal verification snippet *only* when computation is part of the objective).

## Specialized Walkthrough & Verification
Verify every transition and degenerate/boundary case (`0` divisors, defective matrices, dropped hypotheses). State **author-derived / analytical / independently_checked**; if code appears end with **`Source and static review only; not compiled or executed here.`** otherwise **`Analytical and manual review only (no code executed).`**
