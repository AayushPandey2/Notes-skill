# Machine Learning experimental lab reference

Use this compact 7-section hierarchy for classical ML investigations. This overrides earlier multi-track 14/15-section layouts and is an authoring reference, not text to copy verbatim. The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs opening prose, dataset/unit consistency, collapsed walkthroughs, technical accuracy, and execution honesty.

Keep the title, YAML frontmatter, and parent-note navigation link. **Do not** include a visible opening inventory (`Level`, `Estimated prerequisites`, `Implementation languages`, `Libraries and tools`, `Practical objective`, `Experiment objective`).

# EXPERIMENTAL LAB [NUMBER]: [TOPIC NAME]

> [!abstract] Parent Note
> Core theory lives in [[<Parent Note>]].

Open with a short, connected introduction explaining what the learner will investigate, why it matters, and an inspected local web architecture figure (or structured stage table; never Mermaid or ASCII) showing how data splitting, modeling, experiments, and end-to-end verification connect.

## LAB SECTION 01 — INTRODUCTION
Explain the concrete problem, why training error alone is misleading, what the learner will build and investigate, and any essential prerequisite reminders needed before Section 02.

## LAB SECTION 02 — PROBLEM AND INPUT DESIGN
Organize into three coherent subsections:
### 2.1 What problem will we investigate?
Start in ordinary language: explain the concrete situation, what is known, what must be predicted or compared, why training performance alone is insufficient, and what the learner will investigate before introducing formal names.
### 2.2 What does one example look like?
Choose one consistent primary dataset (keep synthetic vs. real-unit rules strictly aligned throughout the entire lab). Explain what each row and column represents, the target, units, shapes (`p` features vs `k` polynomial degree), and one concrete input/output pair. Introduce a small table in prose, distinguish observed labels from model predictions, and explain *why* a single new sample needs a 2D feature matrix.
### 2.3 How will we judge the result fairly?
Explain train, validation, and test responsibilities, assumptions, baseline, metric, what evidence supports improvement, and what the experiment cannot guarantee (never promise a specific degree always wins). Embed and decode a local raster visual here via [representations.md](../../procedures/authoring/representations.md) rather than only pointing to the parent chapter.

## LAB SECTION 03 — THEORETICAL AND MATHEMATICAL BRIDGE
Organize into three connected subsections without repeating the same worked calculation or scattering pronunciation/symbol/dimension headings:
### 3.1 From a prediction mistake to an average training error
Walk step by step from one prediction → difference from truth → squaring → averaging → empirical risk minimization. Introduce one canonical `$$...$$` formula with an immediately following `> [!note]- 📐 Understand this formula` fold containing pronunciation, symbols, dimensions, assumptions, and interpretation.
### 3.2 Follow one example from predictions to MSE
Establish one canonical worked calculation showing true values, predictions, residuals, squares, sum, average, and accurate unit interpretation. Connect later sections back to this example.
### 3.3 Translate the reasoning into computation
Explain how predictions, subtraction, squaring, and averaging map to vectorized code, array shapes, and accidental broadcasting risks (use a compact mapping table only if helpful). Do not inject unbridged advanced formalism (such as empirical distributions or Dirac deltas) into a beginner bridge.

## LAB SECTION 04 — FOUR IMPLEMENTATIONS OF THE SAME LEARNING TASK
Implement the **same underlying learning task** across all four tracks using comparable inputs, outputs, objective, intercept convention, and evaluation rules (never compare a hand-written mean with a polynomial regression model as if they solve the same task). Choose the smallest common task teachable cleanly across all four tracks and explain differences from Section 06's experiment.

Beneath each track heading (`4.1`–`4.4`), include: what this version reveals, dependencies/setup, complete educational code in a Markdown fence, an immediately following collapsed `> [!example]- Understand this implementation line by line` walkthrough (covering meaningful lines/groups in execution order: purpose, syntax, types/structures, inputs, internal operation, shapes, math link, output/state, mistakes, next step), and brief interpretation/comparison.

### 4.1 Python and NumPy (from scratch)
Explain array shapes, axis choices, vectorization, and broadcasting inside the collapsed walkthrough.
### 4.2 Scikit-learn (standard library)
Explain estimator state, `.fit()`, transformation, `.predict()`, and pipeline behavior inside the collapsed walkthrough.
### 4.3 Rust (standard library only)
Explain ownership, borrowing, references, slices, iterators, explicit `as f64` conversions, and `Result` error handling inside the collapsed walkthrough.
### 4.4 Rust (using suitable verified libraries)
For educational code inside Markdown, **do not** inspect the local environment, install dependencies, create project files, compile, or execute—missing local Cargo, dependencies, or compiler access is never a reason to omit this track. Use official, version-specific crate documentation (`docs.rs` / `crates.io`) and examples to establish compatible dependency declarations, imports, dataset construction, types, fitting, prediction, and error handling without inventing APIs or mixing incompatible versions. Provide complete `Cargo.toml` and Rust source blocks followed by a detailed collapsed line-by-line explanation, label it once **"Documentation-checked example; not compiled or executed here."**, and describe expected behavior without fabricating execution results. Report a limitation only if the crate documentation itself is inaccessible.

## LAB SECTION 05 — CONTROLLED EXPERIMENTS
Design a small number of substantive investigations (e.g., polynomial complexity, baseline vs learned model, sample size with fair evaluation design, and out-of-domain extrapolation on separate diagnostic inputs without mutating the held-out test set). For each experiment, cover in connected prose: question, why it matters, hypothesis/reasoning, changed variable, controls, exact procedure, relevant code in Markdown, collapsed code/procedure walkthrough, what to record, how to interpret different possible outcomes, and limitations.

Never promise that Degree 4 always wins, Degree 15 always hits zero train error, more samples always shrink the gap, or one run must be U-shaped; distinguish theoretical nested-class properties from finite-precision solver behavior. Label unexecuted designs honestly; never title anticipated patterns "experimental findings."

## LAB SECTION 06 — REALISTIC END-TO-END WORKFLOW
Replace toy arrays with a complete, realistic end-to-end project on a built-in benchmark or domain-appropriate multi-feature dataset (for classification, e.g., Scikit-learn's `load_breast_cancer()` with 569 samples and 30 numerical features), followed by full hyperparameter and cross-validation mastery.

Organize Section 06 into two cohesive parts—**Part A: Complete Real-World Project (12 Steps)** and **Part B: Hyperparameters, Optimizers & Cross-Validation Tuning**—keeping every variable consistent and labeling unexecuted code `Status: static review (not executed)`.

### Part A — Complete Real-World Project (12 Steps)
For **every** applicable step, provide: (1) prose explaining purpose and design choice, (2) executable Markdown code block, (3) collapsed `> [!example]- Step-by-step: ...` walkthrough, (4) expected output/table interpretation without fabricating unrun metrics, and (5) transition to the next step:
1. **Import Libraries:** Group imports cleanly (`numpy`, `pandas`, `matplotlib.pyplot`, dataset loader, `train_test_split`, `GridSearchCV`, `StandardScaler`, estimator, `Pipeline`, and metrics/display classes).
2. **Load Dataset & Align Target Polarity:** Load features into a labeled `DataFrame` and target into a `Series`; document sample count, feature count, and original `Label | Meaning` table. When domain recall targets the `0` label (e.g., `0 = Malignant, 1 = Benign`), explicitly flip (`y = 1 - y`) and show the updated `Label | Meaning` table.
3. **Explore & Validate Dataset Integrity:** Inspect `head()`, `shape`, `info()`, `describe()`, `isnull().sum()`, and `value_counts()`, paired with a `Function | Purpose` reference table.
4. **Split Dataset (Stratified Partition):** Perform `train_test_split(..., test_size=0.2, random_state=42, stratify=y)`, state exact partition sample counts (e.g., `569 -> 455 (~80%) train + 114 (~20%) test`), include a `Parameter | Meaning` table, and note that `42` is an arbitrary reproducibility seed.
5. **Build Leakage-Free Preprocessing & Model `Pipeline`:** Chain `StandardScaler` ($x' = \frac{x - \mu}{s}$) and the estimator inside `Pipeline([...])`, explaining why scaling statistics must be learned on training data alone.
6. **Train the Model (`.fit()` Internals):** Call `model.fit(X_train, y_train)` and walk through the internal execution sequence (compute train means/stds → standardize train features → initialize parameters → compute forward predictions → compute regularized loss → run optimizer steps → stop on tolerance or `max_iter`).
7. **Predictions vs. Probabilities vs. Raw Scores:** Compare `predict()`, `predict_proba()`, `predict_proba()[:, 1]`, and `decision_function()` in a `Method | Example output` table, and remind learners to inspect `classes_` when labels are not `{0, 1}`.
8. **Evaluate Metrics by Required Input Type:** Compute `accuracy_score`, `precision_score`, `recall_score`, `f1_score`, `roc_auc_score`, `log_loss`, `confusion_matrix`, and `classification_report` on the **same** test partition against a baseline, paired with a `Metric | Input` table separating hard-label metrics from probability/score metrics.
9. **Plot Confusion Matrix:** Show `ConfusionMatrixDisplay.from_predictions(...)` with domain `display_labels` and explain how to read TP/FP/FN/TN trade-offs.
10. **Plot ROC Curve:** Show `RocCurveDisplay.from_predictions(y_test, y_prob)` and explain threshold-independent ranking vs. calibration.
11. **Extract Learned Parameters:** Inspect `named_steps["classifier"]` attributes (`coef_`, `intercept_`, `classes_`, `n_iter_`) in an `Attribute | Meaning` table, noting that pipeline coefficients measure log-odds/score change per **standardized** feature unit.
12. **Visualize Coefficients & Causal Caveat:** Plot sorted horizontal bar coefficients (`pd.Series(..., index=X.columns).sort_values().plot(kind="barh")`), explain positive vs. negative effects holding other model features constant, and explicitly warn that learned associations are **not** causal relationships.

### Part B — Hyperparameters, Optimizers & Cross-Validation Tuning
Replace shallow single-loop tuning with a complete hyperparameter and `GridSearchCV` breakdown:
- **Parameters vs. Hyperparameters Table:** Contrast learned weights/bias (updated by optimizer from data) against configured hyperparameters (`C`, `penalty`, `solver`, `max_iter`, `tol`, `class_weight`, `fit_intercept`, `l1_ratio`).
- **Inverse Regularization Strength ($C$):** Present $C = \frac{1}{\lambda}$ (with compatible-normalization caveat) and a concrete `C | Regularization` table (`0.001` very strong → `1` moderate → `100` very weak), showing relative penalty $1/C$.
- **Penalties & Mixing (`l1_ratio`):** Table of `L1` ($\sum_j |w_j|$), `L2` ($\sum_j w_j^2$), `Elastic Net` ($r\|\mathbf{w}\|_1 + \frac{1-r}{2}\|\mathbf{w}\|_2^2$ with `l1_ratio` table $0 \to 1$), and `None` (noting Scikit-learn version differences).
- **Solvers, Compatibility & Second-Order Intuition:** Table of solver characteristics (`lbfgs`, `liblinear`, `newton-cg`, `newton-cholesky`, `sag`, `saga`), a `Solver | L1 | L2 | Elastic Net` compatibility matrix, and a concise **Newton's Method & L-BFGS** bridge ($w_{\text{new}} = w_{\text{old}} - \frac{J'(w)}{J''(w)}$ verified on $J(w) = w^2$ at $w=4$, plus $\boldsymbol{\theta}_{\text{new}} = \boldsymbol{\theta}_{\text{old}} - H^{-1}\nabla J$ and L-BFGS inverse-Hessian approximation).
- **Stopping & Class-Handling Controls:** Explain `max_iter` (cap, not guaranteed count + convergence-warning troubleshooting), `tol`, `class_weight` (`"balanced"` vs. `{0: 1, 1: 5}`), and `fit_intercept` (origin-forced boundary when `False`).
- **Hyperparameter Tuning with `GridSearchCV`:** Provide complete `Pipeline` + `param_grid` + `GridSearchCV(..., cv=5, scoring=..., n_jobs=-1)` code with a collapsed walkthrough, a 5-fold rotation table (`Round 1–5`), the CV average formula $S_{\text{CV}} = \frac{1}{K}\sum_{k=1}^{K} S_k$ with a concrete fold-average calculation, a `GridSearchCV` parameter/attribute table (`estimator`, `param_grid`, `cv`, `scoring`, `n_jobs`, `best_params_`, `best_estimator_`, `best_score_`), and exact total-fit counting (`combinations × folds + 1 refit`). Validate single-sample inference shapes explicitly (never `np.atleast_2d` blindly).

## LAB SECTION 07 — VERIFICATION, DEBUGGING, COMPARISON, AND INDEPENDENT PRACTICE
Keep distinct final subheadings where helpful for navigation:
### 7.1 Verification and Honest Status
State property checked, concrete inputs, independently expected results, tolerance, what each check establishes/does not establish, and `Status: static review (not executed)` if unexecuted. Qualify small-test-set uncertainty honestly.
### 7.2 Common Mistakes and Debugging
Cover programming, mathematical, and experimental errors (e.g., fitting scalers before splitting, MSE vs RMSE unit confusion, tuning on test data, treating a train–val gap as proof of noise memorization) with concrete fixes.
### 7.3 Implementation Comparison
Compare the four tracks from Section 04 and the integrated pipeline on mathematical visibility, abstraction, error surface, and best use.
### 7.4 Challenges, Checkpoint, and Summary
Provide progressive challenges (beginner, intermediate, advanced, debugging), a reasoning checkpoint with collapsed `> [!tip]- Answer` guidance, and a concise summary linking back to the parent note and next topic.
