# Subject Theory Blueprint: Numerical Computing

## Purpose

Teach Numerical Computing through **floating-point representation, conditioning vs. stability, truncation vs. rounding error, and iterative convergence**.

## Core Theory Obligations

1. **IEEE-754 & Error Sources:** Machine epsilon ($\epsilon_{\text{mach}}$), overflow/underflow, catastrophic cancellation, and separating **truncation/discretization error** from **rounding error**.
2. **Conditioning vs. Stability:** Distinguish **problem conditioning** (sensitivity $\kappa$ of the mathematical problem to input perturbations) from **algorithm stability** (whether the numerical method amplifies rounding errors—e.g., QR/SVD vs. normal equations).
3. **Convergence & Stopping Criteria:** Order of convergence (linear, superlinear, quadratic), step-size vs. residual tolerances, and stiffness in ODEs/solvers.
4. **Beginner Progression, Visuals & Practice:** Motivate numerical pitfalls with a tiny finite-precision arithmetic failure before formal $\epsilon_{\text{mach}}$ or condition-number definitions (closing Taylor-series and norm prerequisites inline), pair convergence/stability regimes with verified web-sourced plots per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII), and contrast one naive vs. numerically stable calculation before an independent error-analysis exercise.
