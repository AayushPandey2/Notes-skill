# Machine Learning Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Language Policy (Python Default; Explicit-Only Rust)
Applies to ML algorithms and pipelines under the strict language rule in [experimental-lab.md](../../procedures/authoring/experimental-lab.md) (§1.2): **default strictly to Python**, add **Rust only on explicit user request** (never for *implementation, optimization, performance, production,* or *advanced* wording), and honor explicit C++/multi-language requests without unrequested languages.

## Shared Fixture & Cross-Track Contract
- Explain dataset structure, target semantics, train/validation split design, feature preprocessing, and leakage guards before code, distinguishing the shared **model** from each track's actual **solver**, **loss/objective convention** (SSE, MSE, half-MSE, normalized vs. unnormalized penalties, `C` vs. `alpha`), and evaluation metrics.
- Use a **hand-trace worked example** (tiny values for manual arithmetic in Track 1) and an **evaluation/stress dataset** (collinear, imbalanced, unscaled, or non-orthogonal observations) exposing limits hidden by orthogonal toy data.
- Explain *why* each experiment and code block behaves as it does—what changes, what remains constant, expected results, numerical stability, and practical trade-offs—rather than dumping long uncommented code listings. Whenever multiple libraries or explicitly requested languages appear, include a compact **Equivalence Table** comparing parameter/scaling conventions and tolerances.

## Practical Realizations (Default Python Progression + Controlled Experiments)
1. **Python + NumPy (First Principles):** Distinguish a **miniature 1-step hand trace** (exposing centering, norms, gradients/residuals, shapes, and broadcasting step by step) from a **complete algorithm implementation** (`fit`, stopping tolerances/iteration limits, loss history, `predict_proba`/`predict`, and validation check).
2. **Python Libraries (`scikit-learn`, etc.) & Baseline Comparison:** Compare against a simpler baseline on identical splits; explain internal fitting, actual solver, objective-parameter conversions, learned state, evaluation metrics, and inference behavior—never reduce to `.fit()`.
3. **Controlled Parameter & Ablation Experiments:** Vary one hyperparameter, scaling choice, regularization strength, or distance/splitting assumption at a time while holding the data/split fixed; state expected directional behavior and conclusion.
4. **Failure Diagnosis, Numerical Stability & Independent Experimentation:** Diagnose ill-conditioning, scaling distortion, overflow/cancellation, or data leakage; conclude with 1–2 **Independent Experimentation** prompts (`> [!hint]-` / `> [!success]-`).
5. **Conditional Explicit-Request Rust Track *(ONLY when explicitly requested by the user)*:** By default, skip Rust completely. Only when the user explicitly requests Rust, load [overlays/ml-rust-overlay.md](overlays/ml-rust-overlay.md) (`Rust from Scratch` and/or `linfa` / `smartcore` verification + multi-language equivalence).

## Specialized Walkthrough & Static Verification
- **Actual optimizer & non-execution honesty:** Match the real solver (coordinate descent, proximal GD, SGD/L-BFGS, closed-form, tree/KNN construction)—never force GD onto non-gradient methods. All code remains non-executed instructional text (`Source and static review only; not compiled or executed here.`).
- **ML static review:** Apply shared math and lab checks: unconstrained OLS residual orthogonality, sigmoid saturation in floating point, KNN distance/voting ties, tree split/pruning equality, K-means centroids, PCA orthogonality/reconstruction, or finite-difference gradient checks.
