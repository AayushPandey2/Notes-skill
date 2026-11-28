# Electrical & Electronics Engineering Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md), and enforces [physical-lab-safety.md](../../procedures/safety/physical-lab-safety.md).

## Applicability & Shared Circuit Contract
Applies to circuits, analog/digital electronics, signals, control, embedded systems, and machines/power. Define node/branch labels, passive sign convention, reference ground, nominal values, tolerances, and SI units once in the shared contract. **Safety:** Evaluate **voltage, current limits, component power ratings ($P = I^2R$), stored energy ($\frac{1}{2}CV^2$, $\frac{1}{2}LI^2$), and supervision**—substitute analytical/simulated models for mains or high-energy systems.

## Practical Realizations
1. **Analytical Calculation:** Apply governing laws (KCL, lumped-circuit KVL, nodal/mesh, phasors, Laplace, Boolean logic) under stated idealizations.
2. **Circuit / Logic Simulation:** SPICE netlist, digital timing/logic simulator, or numerical response script.
3. **Safe Physical Realization & Measurement Procedure:** Low-voltage/low-current educational build, power-rating check, verified web-sourced circuit/instrument setup figure per [representations.md](../../procedures/authoring/representations.md) (never generated), ammeter-in-series / voltmeter-in-parallel calibration & probing steps, structured observation table (SI units + significant figures), and viva checks (`> [!hint]-` / `> [!success]-`).
4. **Uncertainty, Tolerances & Fault Diagnosis:** Compare theoretical vs. tolerance-shifted predictions, distinguish systematic (e.g., meter loading) vs. random measurement errors with uncertainty propagation, and diagnose open/short/saturation faults.

## Specialized Walkthrough & Verification
Reference the shared circuit model across tracks, keep illustrative calculations strictly separate from supplied bench readings, and align closing disclosures with [experimental-lab.md](../../procedures/authoring/experimental-lab.md): use **`Analytical, dimensional, and manual circuit review only (no physical apparatus or simulator executed).`** for pure analytical labs without code or netlists, and **`Source and static review only; not compiled or executed here.`** whenever SPICE netlists or simulation scripts appear.
