# Physics Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md), and enforces [physical-lab-safety.md](../../procedures/safety/physical-lab-safety.md).

## Applicability & Shared Physical Model
Applies to mechanics, thermodynamics, electromagnetism, waves/optics, and quantum mechanics. Define the system boundary, reference frame, coordinate axes, sign conventions, idealizations, apparatus descriptions (with verified web-sourced setup diagrams per [representations.md](../../procedures/authoring/representations.md) when helpful, never generated), and SI units **once** in the shared contract—subsequent tracks reference this model rather than repeating identical derivations. Never invent wet-lab/apparatus readings or force ML/programming tracks.

## Practical Realizations
1. **Analytical Model:** Derive governing physical relationships and predicted behavior under stated idealizations.
2. **Safe Physical Investigation & Apparatus Procedure:** Safe educational apparatus, web-sourced setup figure, step-by-step measurement & calibration procedure, structured observation table columns (SI units + significant figures), and viva preparation cues (or published/simulated setup for hazardous regimes).
3. **Numerical Prediction & Parameter Sweep:** Vary one physical parameter while holding others fixed to predict behavior and limiting cases.
4. **Uncertainty, Error Sources & Idealization Breakdown:** Distinguish systematic vs. random error, propagate measurement uncertainty (checking SI unit cancellation), compare predictions against theoretical expectations, and analyze idealization limits (drag, finite amplitude, real-gas forces).

## Specialized Walkthrough & Verification
Report author-derived predictions using `analytical` or `manual_arithmetic` method and the verification status actually performed (attributing any `simulation` or `measurement` outputs only to `user-supplied` or `published` sources, and never fabricating **observed** apparatus measurements). For non-code labs, end with **`Analytical, dimensional, and manual arithmetic review only (no physical apparatus or code executed).`**
