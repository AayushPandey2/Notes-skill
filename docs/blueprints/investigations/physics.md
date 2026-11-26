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
Report predictions as **author-derived / analytical or simulation / statically_reviewed** (never fabricated **observed** apparatus measurements). If code appears end with **`Source and static review only; not compiled or executed here.`** otherwise **`Analytical, dimensional, and manual arithmetic review only (no physical apparatus or code executed).`**
