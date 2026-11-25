# Electrical & Electronics Engineering Lab Blueprint

Use this lean, engineering-focused blueprint for Electrical & Electronics companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) and [physical lab safety policy](../../procedures/safety/physical-lab-safety.md) govern structure, collapsed **A–G** walkthroughs, safe low-voltage boundaries, and honest status.

**Safety boundary:** Keep physical realizations strictly within safe low-voltage educational conditions (e.g., 5 V DC benchtop circuits). Mains electricity, high-energy power systems, and hazardous hardware require professional supervision and must be modeled analytically or simulated instead.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Electrical Engineering Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Circuit / System & Sign Convention Contract
Define node/branch labels, passive sign convention, reference ground, nominal component values & tolerances, supply conditions, and target quantities with SI units.

## Four Electrical Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Analytical Calculation:** Apply governing circuit/system laws (KCL, KVL, Ohm's law, nodal/mesh, phasors, Laplace/transfer functions, or Boolean logic).
2. **Track 2 — Circuit / Logic Simulation:** Construct a SPICE netlist, digital logic simulation, or numerical transfer-response script (marking predicted curves **Expected** unless supplied).
3. **Track 3 — Safe Physical Realization:** Document a low-voltage breadboard/educational build, instrument placement (ammeter in series, voltmeter in parallel), and power-dissipation limits.
4. **Track 4 — Measurement, Tolerances & Fault Diagnosis:** Compare nominal vs. tolerance-shifted outputs and diagnose open-circuit, short-circuit, saturation, or loading faults.

### Topic-Family Method Selection
Adapt methods to the topic: *DC circuits* (KCL/KVL, nodal/mesh) · *AC circuits* (phasors, impedance, Bode) · *RC/RL/RLC* (transients, time constants, damping/resonance) · *Electronics* (biasing, Q-point, gain) · *Digital* (truth tables, timing, FSMs) · *Control* (step response, stability) · *Signals* (filtering, sampling) · *Power* (analytical & safe simulation only).

Directly beneath each realization, include `> [!example]- Understand this realization: circuit, analysis, and numerical dry run` covering **A–G**: **A** topology, values, tolerances, sign conventions; **B** governing electrical laws; **C** step-by-step equation/simulation order; **D** complete numerical dry run (currents, node voltages, power dissipation); **E** signal/circuit interpretation; **F** open/short faults, wrong instrument placement, rated-power exceedance; **G** core-analysis reconstruction.

## Verification Status

Label calculations **Analytical** / **Expected** (never **Observed** bench measurements unless supplied). If netlist/code is included, end with **`Source and static review only; not compiled or executed here.`**; otherwise **`Analytical, dimensional, and manual circuit review only (no hardware or simulator executed).`**
