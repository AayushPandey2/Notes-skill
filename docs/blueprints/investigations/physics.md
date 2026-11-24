# Physics experimental lab

Use for physical models, measurements, and uncertainty. Keep this hierarchy and the opening rules in [the lab contract](../../procedures/authoring/experimental-lab.md). For theoretical work use a thought experiment, supplied or published data, or verified external simulation where appropriate. Never invent measurements. Each section needs an observable deliverable and fitting visual; retain genuinely inapplicable headings with a specific reason.

The section prompts below define purpose and content. Use this companion check for a concrete example, evidence, visual opportunity, and common mistake. A theoretical investigation retains the measurement headings and states its thought-experiment or sourced-data basis.

| Section | Example and evidence/deliverable | Visual opportunity | Avoid; genuine limit |
|---|---|---|---|
| 01 | Predict circuit response to a changed voltage | System overview | Avoid a goal with no measurable quantity; always |
| 02 | Meter range, circuit boundary, and unit table | Verified apparatus schematic | Avoid unlabeled polarity; apparatus absent in a thought experiment |
| 03 | Ohm's law with assumptions and units | Relation graph | Avoid idealizing non-ohmic devices silently; always |
| 04 | Derive predicted current for two voltages | Prediction curve | Avoid deriving after observing; always |
| 05 | Set up circuit or specify published dataset | Setup photograph/schematic | Avoid unsafe or irreproducible procedure; physical steps absent for published-data work |
| 06 | Record voltage/current with resolution and source | Measurement table | Avoid invented readings; actual observations absent until measured |
| 07 | Compute resistance and uncertainty | Plot with error bars if data exist | Avoid false precision; uncertainty requires known measurement basis |
| 08 | Change voltage while holding resistance/setup fixed | Verified trend plot | Avoid confounded variables; a theoretical study can vary model parameters |
| 09 | Estimate power in a rated component | Real system diagram | Avoid exceeding rating without precautions; always |
| 10 | Compare model prediction with data and uncertainty | Prediction-versus-data plot | Avoid equating visual closeness with agreement; no empirical comparison without data |
| 11 | Diagnose contact resistance or meter offset | Error-source diagram | Avoid generic troubleshooting; always |
| 12 | Identify heating as a model limit | Alternative-model curves | Avoid extrapolating beyond measured range; always |
| 13 | Design a measurement and explain uncertainty | Annotated setup | Avoid tasks requiring unavailable apparatus without a paper option; always |
| 14 | Explain sign, units, and discrepancy | Small calculation table | Avoid formula recall alone; always |
| 15 | State model, evidence status, and scope | Usually no new image | Avoid presenting illustration as measurement; always |

## LAB SECTION 01 — INTRODUCTION AND PHYSICAL OBJECTIVES
### System and question
State what is investigated, level, prior concepts, predicted relationship, and success criterion. Show the physical situation, not an unrelated stock image.
## LAB SECTION 02 — SYSTEM, APPARATUS, AND MEASURABLE QUANTITIES
### Boundary and measurement plan
Define system boundary, coordinates, sign convention, variables and units; list apparatus, calibration and resolution when relevant. Use an inspected setup photograph or schematic and label where each quantity is measured.
## LAB SECTION 03 — PHYSICAL MODEL AND MATHEMATICAL FOUNDATIONS
### Laws and assumptions
State governing laws, approximations, units, and expected scale. Explain formulas in folds and use dimensional checks; avoid treating an ideal model as exact reality.
## INVESTIGATION TRACK A — MODEL AND PREDICTION
Predict before seeing observations.
## LAB SECTION 04 — DERIVATION AND EXPECTED PHYSICAL BEHAVIOR
### Derive a testable relation
Derive the dependence, limiting cases, and a numerical prediction with units. A verified reference graph may illustrate shape but is not a lab result.
## EXPERIMENTAL TRACK
Specify independent, dependent, and controlled variables.
## LAB SECTION 05 — EXPERIMENTAL DESIGN AND PROCEDURE
### Repeatable method
Give apparatus setup, calibration, steps, range, repetitions, and relevant practical precautions. For unavailable or unsafe apparatus, use sourced data or a thought experiment and explain the choice.
## LAB SECTION 06 — OBSERVATIONS AND MEASUREMENT RECORD
### Raw evidence
Provide a table with units, resolution, source/status, and space for observations. Separate actual, supplied, published, and illustrative values; do not fill missing measurements.
## LAB SECTION 07 — DATA ANALYSIS AND UNCERTAINTY
### Derived quantities
Show calculations, uncertainty propagation suited to the measurement, significant figures, and plot interpretation if actual data exists. Avoid false precision.
## CONTROLLED INVESTIGATION
Keep other conditions comparable.
## LAB SECTION 08 — PARAMETER VARIATIONS AND MODEL TESTS
### Test sensitivity
Vary one parameter, record predicted and actual or sourced behavior, and analyze deviations. Use an appropriate figure only with a clear evidence label.
## APPLICATION TRACK
Transfer the model to a real system.
## LAB SECTION 09 — REAL-WORLD APPLICATION OR SYSTEM STUDY
### Part A — Complete Real-World Physical System Study (10–12 Steps)
Replace thin single-number estimates with a complete end-to-end physical system analysis using realistic published/supplied data or a clearly labeled thought-experiment model (never fabricate measurements). For **every** step, provide prose purpose, equations or analysis code (`Status: static review (not executed)` if unexecuted), collapsed walkthrough (`> [!example]- Step-by-step: ...` / `> [!note]- 📐 Understand this formula`), interpretation, and transition:
1. **System Setup & Physical Constants:** Define physical constants with SI units, coordinate axes, and sign conventions.
2. **Load or Specify Physical Dataset / System Parameters:** Document sample/trial count, measured quantities, and `Variable | Symbol | SI Unit | Instrument Resolution` table.
3. **Inspect Data Quality & Sanity Bounds:** Check units, physical bounds (positivity, conservation limits), missing readings, and outliers (`Check | Purpose` table).
4. **Partition Calibration vs. Held-Out Test Regimes:** Separate runs used to calibrate apparatus/model constants from independent held-out operating points.
5. **Build the Physical Modeling Pipeline:** Chain `raw reading -> baseline/zero-offset correction -> governing physical law -> uncertainty propagation`, preventing calibration leakage across held-out runs.
6. **Trace Internal Physical Mechanism:** Walk step by step through energy/momentum/charge conservation, force balance, or field response behind the calculation.
7. **Compare Ideal vs. Corrected vs. Measured Outputs:** Contrast ideal textbook prediction, calibrated/damped model prediction, and observed data in a `Model/Source | Example Output (with units)` table.
8. **Evaluate Agreement Metrics by Error Type:** Separate **systematic bias / residual drift** from **random statistical uncertainty** ($\sigma$, standard error, $\chi^2_{\text{red}}$) on the **same** test points.
9. **Plot Residuals & Parity (Predicted vs. Measured):** Show how to inspect non-random residual curvature (signaling unmodeled physics such as friction, heating, or non-ohmic behavior).
10. **Extract Fitted Physical Constants & Uncertainties:** Report fitted parameters (`slope`, `intercept`, physical constants) with SI units and propagated uncertainty (`Attribute/Quantity | Meaning` table).
11. **Error-Budget Breakdown & Causation Caveat:** Rank dominant uncertainty sources and note that statistical fit alone does not prove microscopic mechanism without controlled variation.

### Part B — Physical Regimes, Approximations & Experimental Controls
- **Universal Constants vs. Controllable Apparatus Parameters Table:** Contrast physical constants ($g, c, k_B, \epsilon_0$) against experimental controls (voltage, load, temperature, sampling rate, geometry).
- **Validity Regime Table:** Map dimensionless numbers or scale limits (e.g., small-angle $\theta \ll 1\text{ rad}$, laminar vs. turbulent, linear vs. plastic regime) to model breakdown points.
- **Model & Solver Compatibility Matrix:** Compare closed-form ideal laws, perturbative/linearized approximations, and numerical ODE/PDE integration across accuracy and assumptions.
- **Instrument & Systematic Controls:** Explain resolution floor, detector saturation, contact/tare offset, and environmental drift controls.
- **Multi-Condition Cross-Regime Validation:** Define a controlled parameter sweep across independent conditions, stating trial counts and keeping expected trends strictly distinct from observed data.
## FINAL VALIDATION AND LEARNING
Judge the model against evidence.
## LAB SECTION 10 — MODEL–MEASUREMENT COMPARISON
### Agreement
Compare values with uncertainty, conservation and dimensional checks; state what agreement supports and what it cannot establish.
## LAB SECTION 11 — SYSTEMATIC ERRORS AND TROUBLESHOOTING
### Diagnose bias
Connect a plausible instrument, setup, or model bias to its direction and a concrete check.
## LAB SECTION 12 — APPROXIMATIONS, LIMITS, AND ALTERNATIVE MODELS
### Valid range
State when assumptions fail and what model would be needed next, without pretending the alternative was tested.
## LAB SECTION 13 — PRACTICAL CHALLENGES
### Predictions and checks
Ask learners to predict a variation, design a measurement, and interpret uncertainty.
## LAB SECTION 14 — FINAL LEARNING CHECKPOINT
### Explain evidence
Ask for units, sign convention, one prediction, and a reason for discrepancy; include answer guidance.
## LAB SECTION 15 — FINAL SUMMARY
### Physical conclusion
Summarize model, evidence status, uncertainty, and limits.
