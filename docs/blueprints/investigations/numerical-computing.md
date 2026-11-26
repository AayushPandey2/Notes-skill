# Numerical Computing Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Numerical Fixture
Applies to root-finding, numerical linear algebra, interpolation, quadrature, and ODE discretization. Define exact problem, precision (`float32` vs. `float64`), initial iterate/step size $h$, and stopping tolerances once.

## Practical Realizations
1. **Exact / Reference Solution:** Establish analytical solution or high-precision reference value where available.
2. **Manual Approximation Trace:** Hand-trace 2–3 complete iterations (e.g., Newton–Raphson $x_{k+1} = x_k - f(x_k)/f'(x_k)$) showing intermediate values and rounding effects.
3. **Numerical Implementation:** Implement the algorithm with explicit stopping criteria (residual tolerance, step change, max iterations) and stability guards (e.g., zero-derivative or pivoting checks).
4. **Error, Conditioning & Stability Study:** Vary starting points, step sizes, or condition numbers $\kappa$; demonstrate catastrophic cancellation, divergence/multiple-root slowdown, and explain **why a small residual $\|A\hat{\mathbf{x}}-\mathbf{b}\|$ does not guarantee a small solution error $\|\hat{\mathbf{x}}-\mathbf{x}^*\|$ in ill-conditioned problems**.

## Specialized Walkthrough & Verification
Label computed tables **author-derived / manual_arithmetic or analytical / statically_reviewed**; end with **`Source and static review only; not compiled or executed here.`** (or **`Analytical and manual numerical review only (no code executed).`**).
