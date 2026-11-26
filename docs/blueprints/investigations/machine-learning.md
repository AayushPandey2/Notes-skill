# Machine Learning Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Track Policy
Applies to Machine Learning algorithms and pipelines. Provide the **4 comparable Python/Rust tracks** below as the default for applicable learning algorithms; honor explicit user language requests (e.g., Python-only) or narrow-topic overrides cleanly without forcing irrelevant tracks.

## Shared Fixture & Cross-Track Contract
- Distinguish the shared **model** from each track's actual **solver** and **objective convention** (SSE, MSE, half-MSE, normalized vs. unnormalized penalties, intercept treatment, hyperparameter scaling like `C` vs. `alpha`).
- Use a **hand-trace fixture** (tiny values for manual arithmetic in Track 1) and, where appropriate, an **evaluation/stress fixture** (collinear, imbalanced, or non-orthogonal observations) exposing limits hidden by orthogonal toy data.
- Include a **Cross-Track Equivalence Table** (predictions, parameter conventions, regularization scaling, intercept handling, convergence criteria, precision, tolerances—never demanding bit-for-bit equality across different solvers).

## Practical Realizations
1. **Python + NumPy (First Principles):** Distinguish a **miniature 1-step hand trace** (exposing centering, norms, gradients/residuals, shapes, and broadcasting step by step) from a **complete algorithm implementation** (`fit`, stopping tolerances/iteration limits, loss history, `predict_proba`/`predict`, and evaluation fixtures)—providing both where an applicable algorithm calls for an iterative or full pipeline realization.
2. **Python Libraries (`scikit-learn`, etc.):** Explain internal fitting, actual solver, objective-parameter conversions, learned state, and prediction behavior—never reduce to `.fit()`.
3. **Rust from Scratch:** Clear Rust covering types, mutability, borrowing, slices, numeric casts, error handling, and sequential vs. simultaneous updates.
4. **Rust (`linfa` / `smartcore`):** Verify crate versions, feature flags, dataset matrices, fit/predict methods, and error handling against official `docs.rs` (only when `source_policy` permits external docs; mark unverified otherwise). Never omit solely due to missing local Cargo; if genuinely unsupported, state the exact gap without inventing APIs.

## Specialized Walkthrough & Static Verification
- **Actual optimizer honesty:** Match the real solver (coordinate descent, proximal GD, SGD/L-BFGS, closed-form, tree/KNN construction)—never force GD onto non-gradient methods.
- **ML static review:** Verify `*` vs. `@`, `**` vs. `^`, integer vs. float division, reduction axes, transpose/broadcasting, gradient signs/scaling, and algorithm-specific checks (*unconstrained OLS* residual orthogonality, finite-precision sigmoid saturation vs. $(0,1)$, KNN distance ties, tree split criteria, K-means centroids, PCA orthogonality/reconstruction, numerical gradient check). End with **`Source and static review only; not compiled or executed here.`**
