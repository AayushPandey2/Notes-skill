# Numerical Computing Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Numerical Fixture
Applies to root-finding, numerical linear algebra, interpolation, quadrature, and ODE discretization. Define exact problem, precision (`float32` vs. `float64`), initial iterate/step size $h$, rounding convention, and stopping tolerances once up front.

## Practical Realizations
1. **Exact / Reference Solution:** Establish analytical solution or high-precision reference value where available so **forward error** ($\|\hat{\mathbf{x}} - \mathbf{x}^*\|$) and **backward error** (smallest problem perturbation $\Delta A, \Delta\mathbf{b}$ explaining $\hat{\mathbf{x}}$) can be interpreted clearly, distinguishing **absolute vs. relative error**.
2. **Manual Approximation Trace & Convergence Contrasts:** Hand-trace complete iterations (e.g., Newton–Raphson $x_{k+1} = x_k - f(x_k)/f'(x_k)$) showing intermediate estimates and errors, and **deliberately contrast normal vs. difficult starting points** (slow convergence, oscillation, near-zero derivative blow-up, or divergence). Separate observed **convergence rate** (step-to-step order) from achieved **final accuracy**.
3. **Numerical Implementation & Stopping Criteria:** Implement the algorithm with explicit stopping criteria and stability guards (zero-derivative/pivoting checks), explaining why small step size $|x_{k+1}-x_k|$, small residual $|f(x_k)|$ or $\|A\hat{\mathbf{x}}-\mathbf{b}\|$, and reliable solution accuracy are distinct criteria.
4. **Conditioning vs. Stability Study:** Separate **conditioning** (sensitivity of the mathematical problem itself, $\kappa$) from **algorithmic stability** (amplification of rounding error in finite precision), demonstrate catastrophic cancellation or multiple-root slowdown, and explain why a small residual does not guarantee small forward error when $\kappa$ is large.

## Specialized Walkthrough & Verification
Label computed tables **author-derived / manual_arithmetic or analytical / statically_reviewed** (recording only checks actually performed); end with **`Source and static review only; not compiled or executed here.`** (or **`Analytical and manual numerical review only (no code executed).`**).
