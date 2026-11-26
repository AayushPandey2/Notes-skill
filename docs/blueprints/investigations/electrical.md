# Electrical & Electronics Engineering Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md), and enforces [physical-lab-safety.md](../../procedures/safety/physical-lab-safety.md).

## Applicability & Shared Circuit Contract
Applies to circuits, analog/digital electronics, signals, control, embedded systems, and machines/power. Define node/branch labels, passive sign convention, reference ground, nominal values, tolerances, and SI units once in the shared contract. **Safety:** Evaluate **voltage, current limits, component power ratings ($P = I^2R$), stored energy ($\frac{1}{2}CV^2$, $\frac{1}{2}LI^2$), and supervision**—substitute analytical/simulated models for mains or high-energy systems.

## Practical Realizations
1. **Analytical Calculation:** Apply governing laws (KCL, lumped-circuit KVL, nodal/mesh, phasors, Laplace, Boolean logic) under stated idealizations.
2. **Circuit / Logic Simulation:** SPICE netlist, digital timing/logic simulator, or numerical response script.
3. **Safe Physical Realization:** Low-voltage/low-current educational build, power-rating check, and instrument placement (ammeter in series, voltmeter in parallel).
4. **Tolerances & Fault Diagnosis:** Compare nominal vs. tolerance-shifted behavior and diagnose open/short faults, saturation, or loading effects.

## Specialized Walkthrough & Verification
Reference the shared circuit model across tracks. Distinguish analytical predictions and dimensional checks from supplied or published bench readings, using the shared lab evidence rules.
