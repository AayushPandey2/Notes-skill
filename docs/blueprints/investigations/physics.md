# Physics Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md), and enforces [physical-lab-safety.md](../../procedures/safety/physical-lab-safety.md).

## Applicability & Shared Physical Model
Applies to mechanics, thermodynamics, electromagnetism, waves/optics, and quantum mechanics. Define the system boundary, reference frame, coordinate axes, sign conventions, idealizations, and SI units **once** in the shared contract—subsequent tracks reference this model rather than repeating identical derivations. Never invent wet-lab/apparatus readings or force ML/4-language programming tracks.

## Practical Realizations
1. **Analytical Model:** Derive governing physical relationships under stated idealizations.
2. **Safe Physical Investigation:** Safe educational apparatus, effective measurements, and resolution methods (or published/simulated setup for high-energy/hazardous regimes).
3. **Numerical Prediction & Parameter Sweep:** Vary physical parameters under the shared model to examine behavior and limiting cases.
4. **Uncertainty & Idealization Breakdown:** Propagate measurement uncertainty, verify SI unit cancellation, and analyze where idealizations fail (air drag, finite amplitude, real-gas forces).

## Specialized Walkthrough & Verification
Report author-derived predictions using `analytical` or `manual_arithmetic` method and the verification status actually performed (attributing any `simulation` or `measurement` outputs only to `user-supplied` or `published` sources, and never fabricating **observed** apparatus measurements). For non-code labs, end with **`Analytical, dimensional, and manual arithmetic review only (no physical apparatus or code executed).`**
