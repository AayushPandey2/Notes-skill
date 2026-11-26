# Machine Learning Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Language Policy (Python Default; Explicit-Only Rust)
Applies to Machine Learning algorithms and pipelines. **Default strictly to Python** unless the user explicitly specifies another language. **NEVER include Rust by default** (including parallel Python/Rust tracks, optional/collapsed blocks, Cargo/crate setups, or "for completeness")—and never treat requests for *implementation, optimization, performance, production readiness,* or *advanced experiments* as permission to add Rust. Include Rust (`Rust from Scratch` and/or `linfa` / `smartcore`) **only when the user explicitly requests Rust**; honor explicit single- or multi-language requests (e.g., C++) faithfully without adding unrequested languages.

## Shared Fixture & Cross-Track Contract
- Explain dataset structure, target semantics, train/validation split design, feature preprocessing, and leakage guards before code, distinguishing the shared **model** from each track's actual **solver**, **loss/objective convention** (SSE, MSE, half-MSE, normalized vs. unnormalized penalties, `C` vs. `alpha`), and evaluation metrics.
- Use a **hand-trace worked example** (tiny values for manual arithmetic in Track 1) and an **evaluation/stress dataset** (collinear, imbalanced, unscaled, or non-orthogonal observations) exposing limits hidden by orthogonal toy data.
- Explain *why* each experiment and code block behaves as it does—what changes, what remains constant, expected results, numerical stability, and practical trade-offs—rather than dumping long uncommented code listings. Whenever multiple libraries or explicitly requested languages appear, include a compact **Equivalence Table** comparing parameter/scaling conventions and tolerances.

## Practical Realizations (Default Python Progression + Controlled Experiments)
1. **Python + NumPy (First Principles):** Distinguish a **miniature 1-step hand trace** (exposing centering, norms, gradients/residuals, shapes, and broadcasting step by step) from a **complete algorithm implementation** (`fit`, stopping tolerances/iteration limits, loss history, `predict_proba`/`predict`, and validation check).
2. **Python Libraries (`scikit-learn`, etc.) & Baseline Comparison:** Compare against a simpler baseline on identical splits; explain internal fitting, actual solver, objective-parameter conversions, learned state, evaluation metrics, and inference behavior—never reduce to `.fit()`.
3. **Controlled Parameter & Ablation Experiments:** Vary one hyperparameter, scaling choice, regularization strength, or distance/splitting assumption at a time while holding the data/split fixed; state expected directional behavior and conclusion.
4. **Failure Diagnosis, Numerical Stability & Independent Experimentation:** Diagnose ill-conditioning, scaling distortion, overflow/cancellation, or data leakage; conclude with 1–2 **Independent Experimentation** prompts (`> [!hint]-` / `> [!success]-`).
5. **Conditional Explicit-Request Rust Track *(ONLY when explicitly requested by the user)*:** If Rust is explicitly requested, provide **Rust from Scratch** (types, ownership/borrowing, slices, numeric casts, error handling, sequential vs. simultaneous updates) and/or **Rust (`linfa` / `smartcore`)** (checking crate versions, feature flags, dataset matrices, fit/predict methods, and error handling against official `docs.rs` when permitted, or marking unverified cleanly without inventing APIs).

## Specialized Walkthrough & Static Verification
- **Actual optimizer & non-execution honesty:** Match the real solver (coordinate descent, proximal GD, SGD/L-BFGS, closed-form, tree/KNN construction)—never force GD onto non-gradient methods. All code remains non-executed instructional text (`Source and static review only; not compiled or executed here.`).
- **ML static review:** Apply shared math and lab checks: unconstrained OLS residual orthogonality, sigmoid saturation in floating point, KNN distance/voting ties, tree split/pruning equality, K-means centroids, PCA orthogonality/reconstruction, or finite-difference gradient checks.
