# Chemistry experimental lab

Use for chemical species, reactions, conditions, and analytical evidence. Keep this hierarchy and the opening rules in [the lab contract](../../procedures/authoring/experimental-lab.md). Link macroscopic observation, particle explanation, and symbolic equation. Wet-lab work is optional; use supplied or published evidence, paper analysis, or verified simulation when appropriate. Never invent observations or unsafe procedures. Give every section evidence and a relevant visual when useful; retain an inapplicable heading with a specific reason.

The section prompts below define purpose and content. Use this companion check for an example, evidence, visual opportunity, and common error. A paper or published-data investigation retains the evidence headings and states the actual source of observations.

| Section | Example and evidence/deliverable | Visual opportunity | Avoid; genuine limit |
|---|---|---|---|
| 01 | Predict acid–base neutralization indicator change | Verified process picture | Avoid claiming an observed result up front; always |
| 02 | Species, concentrations, phases, and conditions | Verified molecular/apparatus figure | Avoid ambiguous labels; apparatus absent for paper analysis |
| 03 | Balanced reaction and mole ratio | Particle-to-symbol diagram | Avoid unbalanced charge/atoms; always |
| 04 | Predict color or pH from species change | Verified structure or reaction scheme | Avoid using an unrelated molecule image; always |
| 05 | Control volume/concentration or analyze sourced titration | Apparatus schematic | Avoid unsafe procedure; physical steps absent for sourced-data mode |
| 06 | Record pH, color, source, and status | Observation table or verified spectrum | Avoid inventing observations; actual readings absent until supplied/measured |
| 07 | Compute moles and concentration with units | Calculation table | Avoid spurious significant figures; always |
| 08 | Change one concentration or temperature | Verified relationship graph | Avoid confounding conditions; source data may support only a limited comparison |
| 09 | Identify an unknown from multiple indicators | Analytical workflow | Avoid claiming identity from one clue; always |
| 10 | Check balance, replicate evidence, uncertainty | Evidence comparison table | Avoid calling one run reproducible; replicates need data |
| 11 | Diagnose contamination or calibration bias | Failure pathway | Avoid generic safety filler; always |
| 12 | Compare indicators or analytic methods | Method matrix | Avoid ignoring detection limits; a second method may be unavailable |
| 13 | Calculation and evidence-interpretation tasks | Figure to label if useful | Avoid requiring a wet lab without authorization; always |
| 14 | Link observation, particles, and equation | Three-level diagram | Avoid symbol-only recall; always |
| 15 | State mechanism, evidence, and limits | Usually no new image | Avoid converting expected color into observation; always |

## LAB SECTION 01 — INTRODUCTION AND CHEMICAL OBJECTIVES
### Question and scale
State the chemical question, learning outcome, relevant system, and success criterion. Show a verified structure or process figure if it clarifies the task.
## LAB SECTION 02 — CHEMICAL SYSTEM, MATERIALS, AND CONDITIONS
### Species and context
Define substances, phases, concentrations, quantities, temperature/pressure, and relevant handling or disposal constraints. Do not infer an actual setup from a stock photograph.
## LAB SECTION 03 — CHEMICAL PRINCIPLES AND QUANTITATIVE FOUNDATIONS
### Model and units
Explain bonding, equilibrium, kinetics, or stoichiometry as relevant; define symbols and assumptions, balance equations, and use significant figures.
## INVESTIGATION TRACK A — PARTICLE-LEVEL AND SYMBOLIC REASONING
Connect microscopic mechanism to expected macroscopic evidence.
## LAB SECTION 04 — STRUCTURES, EQUATIONS, AND PREDICTIONS
### Verify the representation
Show a verified molecular or process figure, balanced equation, conserved atoms/charge, and predicted observable change. Check figure labels and avoid using a misleading structure.
## EXPERIMENTAL OR EVIDENCE TRACK
Choose a safe and suitable investigation mode.
## LAB SECTION 05 — INVESTIGATION DESIGN AND PROCEDURE
### Controlled plan
State independent, dependent, and controlled conditions, sampling, measurement method, and relevant handling/disposal. For paper or published-data work, explain extraction and source limits.
## LAB SECTION 06 — OBSERVATIONS AND CHEMICAL EVIDENCE
### Evidence record
Provide a table for color, phase, temperature, spectrum, pH, or other relevant indicators, with source/status. Distinguish expected, supplied, published, and observed data.
## LAB SECTION 07 — CALCULATIONS AND DATA INTERPRETATION
### Quantitative bridge
Calculate quantities with units, limiting reagent or concentration where relevant, uncertainty and significant figures; connect numbers to species and observations.
## CONTROLLED INVESTIGATION
Change one condition while preserving comparability.
## LAB SECTION 08 — EFFECTS OF CONDITIONS AND COMPETING EXPLANATIONS
### Test alternatives
Predict how concentration, temperature, solvent, or pH changes evidence as relevant; explain competing mechanisms and what distinguishes them.
## APPLICATION TRACK
Use the chemistry in a meaningful analytical or practical setting.
## LAB SECTION 09 — ANALYTICAL OR PRACTICAL APPLICATION
### Part A — Complete Real-World Chemical / Analytical Study (10–12 Steps)
Replace single-indicator guesses with a complete end-to-end analytical or reaction-system workflow grounded in balanced stoichiometry and sourced/published evidence (never invent wet-lab readings). For **every** step, provide prose purpose, balanced equations or analysis code (`Status: static review (not executed)` if unexecuted), collapsed walkthrough, interpretation, and transition:
1. **Reagents, Constants & Balanced Equations:** State chemical species, phases, molar masses, equilibrium/rate constants, and balanced equations with conserved atoms and charge.
2. **Load Analytical Dataset or Reaction Conditions:** Document replicate/standard counts, concentrations, temperature/pressure, and `Variable | Phase/Unit | Role` table.
3. **Inspect Sample & Condition Integrity:** Check blank controls, replicate consistency, pH/temperature stability, and detection limits (`Check | Purpose` table).
4. **Partition Calibration Standards vs. Unknown/Validation Samples:** Separate known standards used for calibration curves from unknown or held-out verification samples.
5. **Build the Analytical Pipeline:** Chain `raw instrument signal -> blank/baseline subtraction -> calibration model (e.g., Beer-Lambert / Henderson-Hasselbalch) -> concentration & yield calculation`, preventing standard-to-unknown leakage.
6. **Trace Internal Particle & Stoichiometric Mechanics:** Walk step by step through limiting reagent, proton transfer, equilibrium shift (Le Chatelier), or rate-law step.
7. **Compare Qualitative, Calculated & Measured Outputs:** Contrast qualitative indicator shifts, idealized stoichiometric yields, and calibrated analytical concentrations in a `Method/Level | Example Output` table.
8. **Evaluate Analytical Metrics by Category:** Separate **accuracy/trueness** (% recovery, relative error vs. reference standard) from **precision/sensitivity** (RSD, LOD, LOQ, $R^2$ of linear calibration range).
9. **Plot Calibration Curve & Residuals:** Explain how to read linear dynamic range, upper saturation (Beer-Lambert deviation), and systematic residual drift.
10. **Extract Fitted Thermodynamic/Kinetic Parameters:** Report fitted $K_a, k, E_a, \Delta H^\circ$ or molar absorptivity $\varepsilon$ with exact units and uncertainty (`Parameter | Meaning` table).
11. **Error-Contribution Breakdown & Mechanistic Caveat:** Rank dominant analytical errors (pipetting, CO$_2$ absorption, side reactions) and note that kinetic fit alone does not uniquely prove elementary mechanism without intermediate evidence.

### Part B — Reaction Conditions, Analytical Methods & Optimization
- **Intrinsic Properties vs. Controllable Reaction/Instrument Parameters Table:** Contrast fixed molecular constants ($pK_a$, $\Delta G^\circ$) against tunable lab/process conditions (`pH`, `temperature`, `concentration`, `solvent`, `catalyst_loading`, `wavelength`).
- **Condition-Sensitivity Table:** Concrete table showing how varying `pH`, temperature, or ionic strength shifts equilibrium position, selectivity, or side-reaction risk.
- **Analytical Method Compatibility Matrix:** Compare titrimetry, UV-Vis spectrophotometry, potentiometry/pH-metry, and chromatography across selectivity, detection limit, matrix interference, and sample destructiveness.
- **Limit, Purity & Safety Controls:** Explain LOD/LOQ bounds, buffer capacity limits, quenching/neutralization, and safe handling boundaries.
- **Systematic Condition Sweep & Replicate Design:** Define a controlled factorial or one-factor-at-a-time matrix across replicates (`conditions × replicates`), keeping predicted shifts clearly separated from observed measurements.
## FINAL VALIDATION AND LEARNING
Check the claim against chemistry and evidence.
## LAB SECTION 10 — VERIFICATION, UNCERTAINTY, AND REPRODUCIBILITY
### Independent support
Check atom/charge balance, units, controls, replicates or independent analytical evidence, and uncertainty.
## LAB SECTION 11 — COMMON ERRORS AND TROUBLESHOOTING
### Diagnose mismatch
Show one plausible contamination, concentration, calibration, or equation error and a concrete corrective check.
## LAB SECTION 12 — METHOD COMPARISON AND LIMITATIONS
### Choose an approach
Compare methods by selectivity, sensitivity, safety, resources, and assumptions.
## LAB SECTION 13 — PRACTICAL CHALLENGES
### Exercises
Offer a prediction, a balanced-equation or calculation task, and an evidence interpretation with checks.
## LAB SECTION 14 — FINAL LEARNING CHECKPOINT
### Three-level explanation
Ask learners to link observation, particles, and symbols and identify one competing explanation; include answer guidance.
## LAB SECTION 15 — FINAL SUMMARY
### Chemical conclusion
Summarize mechanism, evidence status, uncertainty, and conditions.
