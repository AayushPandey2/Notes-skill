# Subject Theory Blueprint: Machine Learning

## Purpose

Upgrade Scriptorium's Machine Learning notes from algorithm-centric explanations to **complete machine learning education**—covering problem formulation, data-generating processes, objective construction, generalization, evaluation design, numerical stability, failure diagnosis, and interpretability alongside first-principles internal mechanics. These are **internal teaching responsibilities** selected by topic relevance, never ten compulsory headings.

## 1. Twelve Core ML Theory Dimensions

- **P0 (Essential for substantive ML notes):** Problem formulation (why the task takes this ML paradigm) · Data-generating process (observations, labels, noise) · Mathematical foundations (probability, geometry, calculus, linear algebra) · Learning objectives (statistical criterion vs. optimization objective) · Generalization (inductive bias, sampling, estimation error) · Evaluation (metric choice, experimental design, decision thresholds).
- **P1/P2 (Activate when relevant):** Numerical computation (stability, conditioning, precision) · Model selection (validation, selection bias) · Failure diagnosis (symptom-to-mechanism reasoning) · Interpretability (association vs. attribution vs. causation) · Deployment behavior (distribution shift, drift, uncertainty) · Research foundations (original motivation and evidence).

## 2. Generalized ML Lifecycle & Model–Objective–Solver Separation

Adapt the opening flow to the paradigm (supervised, unsupervised, reinforcement, probabilistic, sequential) rather than assuming binary classification everywhere. Always separate these seven components explicitly—never equate an estimation criterion (e.g., ordinary least squares) with one numerical solver:

| Component | Meaning | Linear Regression Example |
|---|---|---|
| **Model** | Mathematical form of predictions | $\hat y = wx + b$ |
| **Parameters** | Quantities learned from data | $w, b$ |
| **Objective** | Criterion defining the desired solution | Sum of squared errors (SSE) |
| **Regularization** | Additional preference or constraint | $L_2$ penalty $\lambda \|w\|_2^2$ |
| **Solver** | Numerical procedure finding a solution | QR, SVD, normal equations, or gradient descent |
| **Evaluation metric** | Measure of predictive performance | MAE, MSE, RMSE, or $R^2$ |
| **Decision procedure** | How predictions drive an action | Task-dependent decision rule |

## 3. Mathematical Objective-Construction & Multi-Perspective Teaching

For every governing objective, explain: (1) what behavior it rewards or penalizes (e.g., why squared loss magnifies large residuals while absolute loss grows linearly), (2) why the formula captures that behavior, (3) justifying assumptions, (4) convexity/differentiability/nonsmoothness, (5) how reductions/penalty conventions alter optimization, and (6) whether optimizing the surrogate loss necessarily improves the target metric.

Connect **relevant complementary perspectives** explicitly (do not treat them as disconnected facts—e.g., in PCA, connect maximum projected variance with minimum squared reconstruction error):

| Algorithm | Complementary Perspectives Worth Connecting |
|---|---|
| **Linear / Ridge / Lasso** | Algebra, projection geometry, optimization, statistical estimation |
| **Logistic regression** | Linear scores, log-odds/probability, likelihood, decision boundaries |
| **KNN** | Distance geometry, local density/estimation, computational complexity |
| **Decision trees** | Axis-aligned partition geometry, impurity reduction, recursive greedy construction |
| **Random forest** | Bootstrap sampling, variance reduction, correlated-tree aggregation |
| **Gradient boosting** | Additive modeling, functional optimization, residual/pseudo-gradient fitting |
| **SVM** | Geometric margins, constrained optimization/duality, kernel similarity |
| **PCA** | Projected variance, orthogonal projection, eigendecomposition, SVD, reconstruction |
| **K-means** | Voronoi distance geometry, distortion objective, alternating minimization |
| **Naive Bayes** | Conditional probability, Bayes' rule, conditional independence assumptions |
| **Neural networks** | Function composition, tensor shapes, computational graphs, chain-rule optimization |

## 4. Data-Generating Process, Leakage & Generalization Theory

Before fitting any model, distinguish the **dataset** from the **data-generating process**: *Population vs. Sample, Features vs. Target, Signal vs. Noise, Sampling bias, Label noise, Joint distribution, and Data leakage* (trace actual information flow—what is known at training time vs. genuinely available at prediction time).

Teach **why generalization is possible**: hypothesis space & capacity, inductive bias, empirical vs. expected risk, approximation vs. estimation error, sample complexity, capacity control, validation/selection bias, and out-of-distribution shift. Introduce the squared-error bias–variance decomposition $\mathbb{E}[(Y - \hat f(x))^2] = \operatorname{Bias}^2 + \operatorname{Variance} + \sigma^2$ **only** after establishing repeated-sampling assumptions—never claim it holds identically for all classification losses.

## 5. Evaluation Design, Numerical Computation & Algorithm Variants

- **Three evaluation problems:** Distinguish **Measurement** (metric choice), **Experimental design** (leak-free splits/CV), and **Decision-making** (threshold trade-offs—show how changing a threshold alters TP/FP/TN/FN, precision, recall, and accuracy without changing the fitted model or predicted probabilities). Connect regression metrics to residual tails and error costs.
- **Numerical stability overlay:** Explain floating-point rounding, overflow/underflow, catastrophic cancellation, ill-conditioned design matrices, **QR/SVD vs. inverting normal equations**, **log-sum-exp / logits-based cross-entropy** vs. naive $\sigma(z)$, convergence tolerances, and `float32` vs. `float64`.
- **Variant lineage:** Frame related models as design-space responses to limitations (e.g., OLS $\to$ Ridge $L_2$ magnitude control $\to$ Lasso $L_1$ sparsity $\to$ Elastic Net $\to$ Robust regression against heavy-tailed residuals).

## 6. Algorithm-Family Overlays, Failure Diagnosis & Interpretability

Apply paradigm-appropriate rules—never force supervised train/test or target-label logic onto clustering or RL:
- *Regression* (conditional targets, residuals, diagnostics) · *Classification* (scores, calibration, decision costs) · *Clustering* (similarity, initialization instability, validation) · *Dimensionality reduction* (projection, reconstruction) · *Anomaly detection* (rarity, contamination, thresholds) · *Recommender systems* (implicit feedback, ranking, cold start) · *Time-series* (temporal dependence, chronological splits) · *RL* (states, actions, rewards, policies, exploration) · *Semi-/Self-supervised* (consistency, pretext tasks) · *Probabilistic* (priors, likelihood, posterior) · *Online* (streaming updates, nonstationarity) · *Ensembles* (diversity, error dependence) · *Generative* (learned distributions, sampling, latent variables).

**Failure diagnosis (symptom $\to$ competing hypotheses $\to$ discriminating check):**
- High train / low val $\to$ overfitting, leakage, or split shift $\to$ inspect splits & learning curves.
- Low train & low val $\to$ underfitting, weak features, or non-convergence $\to$ inspect optimization trace & capacity.
- Unstable coefficients $\to$ collinearity or small $n$ $\to$ check condition number & feature correlations.
- `NaN` loss $\to$ overflow, invalid log/div, or excessive step size $\to$ inspect logits & gradient norms.
- Overconfident probabilities $\to$ miscalibration or shift $\to$ check reliability diagram on held-out data.
- High validation variance $\to$ small sample or unstable fitter $\to$ repeated stratified/grouped CV.
- Post-deployment drop $\to$ covariate/label shift or stale features $\to$ compare train vs. serving distributions.

**Interpretability:** Distinguish global vs. local, intrinsic vs. post-hoc, correlation/feature attribution (SHAP, permutation importance, partial dependence) vs. real-world causal intervention, and prediction vs. epistemic uncertainty.
