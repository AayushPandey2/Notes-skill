# Subject Theory Blueprint: Machine Learning

## Purpose

Deliver complete Machine Learning education—covering problem formulation, data-generating processes, objective construction, generalization, evaluation design, numerical stability, failure diagnosis, and interpretability alongside first-principles internal mechanics. Activate responsibilities selectively via the Topic-Family Applicability table below; never treat the full ML lifecycle as mandatory for a single formula or narrow concept.

## 1. Topic-Family Applicability (Prevent Scope Inflation)

| ML Topic Family | Required Theoretical Responsibilities |
|---|---|
| **Individual formula / metric** | Meaning, construction/derivation, assumptions, interpretation, boundary/failure case |
| **Learning algorithm** | Simpler baseline foundation, model/mechanism, learning criterion, task types (regression, binary/multiclass classification with full link/derivative chains), training vs. inference, key algorithmic variants & sparse/categorical data handling, grouped hyperparameters (purpose, mechanism, versioned defaults, interactions, tuning), assumptions, training/validation workflow, interpretability, and comparisons with nearest alternatives |
| **Optimization** | Objective landscape (convex/nonconvex/nonsmooth), geometry, updates, convergence, numerical stability |
| **Evaluation** | Measurement, sampling unit, split design, uncertainty, threshold/decision costs |
| **Preprocessing** | Transformation semantics, fit-on-train scope, leakage prevention, invertibility |
| **Statistical learning** | Data-generating process, risk, capacity, inductive bias, estimation vs. approximation |
| **Deployment** | Serving contract, distribution shift types, monitoring, failure & recovery |
| **Reinforcement learning** | Sequential decisions, states, actions, rewards, returns, policies, exploration |

## 2. Learning Mechanisms & Conditional Model–Objective–Solver Separation

Select the actual learning mechanism rather than assuming gradient descent everywhere:
- *Closed-form / direct estimation* (e.g., unconstrained OLS) · *Iterative gradient-based* (e.g., logistic regression, neural nets) · *Coordinate / proximal optimization* (e.g., Lasso) · *Greedy structure construction* (decision trees) · *Instance-based prediction* (KNN—retains training points, no learned weight vector) · *Alternating optimization* (K-means) · *Probabilistic inference* (Bayes, EM, posteriors) · *Sequential decision learning* (RL).

Where applicable (making inapplicable components optional for nonparametric/instance-based methods), separate **Model** ($\hat y = wx+b$) · **Parameters** ($w,b$) · **Objective** (SSE) · **Regularization** ($\lambda \|w\|_2^2$) · **Solver** (QR, SVD, GD, coordinate descent) · **Evaluation metric** (MAE, MSE, $R^2$) · **Decision procedure** (threshold/action rule). Never equate an estimation criterion (e.g., OLS) with one numerical solver.

## 3. Mathematical Rigor, Objective Construction & Multi-Perspective Teaching

- **Objective construction:** Explain (1) what behavior the objective rewards/penalizes (e.g., squared vs. absolute loss), (2) why the formula captures it, (3) justifying assumptions (distinguishing likelihood assumptions from convenient surrogates), (4) optimization landscape (convexity, local minima, saddle points, nonsmoothness), (5) how reductions/scaling alter regularization parameters (`C`, `alpha`), and (6) whether minimizing the surrogate improves the target metric.
- **ML-specific mathematical obligations:** Verify **shape propagation**, check **parameter identifiability**, separate **numerical solver convergence** from **statistical generalization**, qualify OLS residual orthogonality $X^\top(\mathbf{y} - X\hat{\mathbf{w}})=0$ strictly to **unconstrained** least squares (not arbitrary regularized/constrained solutions), and distinguish exact mathematical sigmoid outputs $(0,1)$ from **finite-precision saturation** (`0.0`/`1.0`).
- **ML technical accuracy & library-variant guardrails:**
  - Verify algorithm variants and defaults against official versioned documentation rather than conflating distinct methods or presenting library defaults as timeless facts (for example, distinguish `exact` split search, Hessian-weighted `approx` sketching, and pre-training global weighted `hist` binning; do not generalize one `grow_policy` or pruning updater as universal behavior).
  - Distinguish explicit numeric zeros in dense inputs from absent entries / missing values in sparse matrices, and teach default routing semantics accurately.
  - State explicit validity conditions for custom objectives (smoothness, additivity across observations, convexity/usable positive curvature, and behavior when Hessians are clipped or non-smooth, such as Huber vs. pseudo-Huber).
  - Avoid false monotonic or universal claims about hyperparameters (for example, lower `learning_rate` does not automatically improve generalization without capacity/round control, and larger $L_2$ `reg_lambda` shrinks individual leaf magnitudes for fixed sums rather than monotonically reducing every split-gain difference).
  - Describe tree-ensemble predictions accurately as additive combinations of learned leaf scores (not averages of training leaf targets), and distinguish extrapolation outside training feature domains from target-range bounds.
- **ML worked-trace specifics:** Keep training-phase updates distinct from prediction-phase inference, and make explicit what residual signs mean, *why* features multiply residuals, *why* subtracting a negative gradient increases a weight, *why* total loss can drop while individual points worsen, finite-sample vs. asymptotic OOB behavior (e.g., $(5/6)^6 \approx 33.5\%$ vs. $36.8\%$), and paper conventions vs. library defaults (`scikit-learn` probability averaging vs. hard voting, `max_features`).

Connect **relevant complementary perspectives** explicitly (e.g., in PCA, connect maximum projected variance with minimum squared reconstruction error; qualify projection vs. penalized optimization across OLS, Ridge, and Lasso):
- *Linear/Ridge/Lasso:* Algebra, projection geometry (where applicable), optimization, estimation · *Logistic:* Log-odds, probability, likelihood, decision boundaries · *KNN:* Distance geometry, local estimation, inference cost · *Trees:* Partition geometry, impurity, greedy splits · *Random forest:* Bootstrap sampling, variance reduction, correlated aggregation · *Boosting:* Functional optimization, residual/gradient fitting · *SVM:* Geometric margins, constrained duality, kernels · *PCA:* Variance, projection, eigendecomposition/SVD, reconstruction · *K-means:* Voronoi geometry, distortion, alternating updates · *Naive Bayes:* Bayes' rule, conditional independence · *Neural nets:* Composition, tensor shapes, computational graphs.

## 4. Data-Generating Process, Generalization & Distribution Shift

Before modeling, select the paradigm-appropriate data representation (do not force supervised targets onto clustering or RL): **Population vs. Sample, Features vs. Target, Signal vs. Noise, Sampling bias, Label noise, Joint distribution, IID vs. grouped/temporal dependence, and Data leakage** (trace training-time vs. prediction-time information flow).

Teach **generalization**: hypothesis space & representable capacity (beyond parameter count alone), inductive bias, empirical vs. expected risk, approximation vs. estimation error, sample complexity, and validation matched to the sampling unit (stratified, grouped, or chronological—never interchangeable). Introduce $\mathbb{E}[(Y-\hat f(x))^2] = \operatorname{Bias}^2 + \operatorname{Variance} + \sigma^2$ **only** under repeated-sampling squared-error assumptions. When covering deployment/generalization, distinguish **Covariate shift** ($P(X)$ changes, $P(Y\mid X)$ stable), **Label shift** ($P(Y)$ changes, $P(X\mid Y)$ stable), **Concept shift** ($P(Y\mid X)$ changes), **Data-quality change**, and **Training-serving skew**.

## 5. Evaluation, Numerical Stability, Variants & Diagnosis

- **Three evaluation problems:** **Measurement** (metric choice; teach TP/FP/TN/FN counts before summary tables; distinguish **discrimination** from **calibration**), **Experimental design** (leak-free splits matched to dependence), and **Decision-making** (threshold sweeps altering TP/FP/TN/FN without changing the fitted model).
- **Numerical stability (activate when relevant):** Floating-point rounding, overflow/underflow, cancellation, ill-conditioning, **QR/SVD vs. inverting normal equations**, **log-sum-exp / logits-based cross-entropy**, convergence tolerances, and `float32` vs. `float64`.
- **Related modeling alternatives:** Frame OLS, Ridge ($L_2$), Lasso ($L_1$), Elastic Net ($L_1+L_2$), and Robust regression as **alternative objective designs** addressing distinct limitations (not one mandatory linear progression).
- **Failure diagnosis (require discriminating evidence before concluding a cause):**
  - High train / low val $\to$ overfitting, leakage, or split shift $\to$ inspect splits & learning curves.
  - Low train & val $\to$ underfitting, weak features, or non-convergence $\to$ inspect optimization trace & capacity.
  - Unstable coefficients $\to$ collinearity or small $n$ $\to$ check condition number & feature correlations.
  - `NaN` loss $\to$ overflow, invalid log/div, or step size $\to$ inspect logits & gradient norms.
  - Overconfident probabilities $\to$ miscalibration or shift $\to$ reliability diagram on held-out data.
  - High validation variance $\to$ small sample or unstable fitter $\to$ appropriate repeated/grouped/time CV.
  - Post-deployment drop $\to$ covariate/label/concept shift or skew $\to$ compare train vs. serving distributions.
- **Interpretability & Uncertainty:** Separate global vs. local, intrinsic vs. post-hoc, correlation/attribution (SHAP, permutation importance, PDP) vs. causal intervention, and predictive vs. **aleatoric** vs. **epistemic** uncertainty.

Distinguish the data-generating probability, model probability, observed label, and thresholded prediction, carrying this distinction consistently through examples, code, and assessment.

For nearest-neighbor topics, introduce the query and feature units before the distance function. Trace a ranking and aggregation before general notation. Hold the data fixed across changes to metric, scaling, weights or neighborhood size. Distinguish distance ties at selection from label ties at voting. For complete KNN coverage, trace a weighted-vote reversal, the regression output range, density dependence of a fixed neighbor count, and an exact pruning decision. Compare approximate retrieval with exact search and separate both from model validation.
