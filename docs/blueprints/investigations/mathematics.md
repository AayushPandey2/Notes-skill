# Mathematics experimental lab

Use for proof, derivation, construction, and counterexample. Keep this hierarchy and the opening rules in [the lab contract](../../procedures/authoring/experimental-lab.md). Define notation before use, explain pronunciation and restrictions, and distinguish numerical evidence from proof. Each section should have a purpose, worked object, checkable deliverable, and appropriate visual; retain a heading with a specific reason when genuinely inapplicable. Code is optional.

The section prompts below define purpose and content. Use this companion check for an example, evidence, visual opportunity, and error to prevent. Retain a heading and explain a specific limitation when its usual representation is genuinely unavailable.

| Section | Example and evidence/deliverable | Visual opportunity | Avoid; genuine limit |
|---|---|---|---|
| 01 | State a matrix identity and proof goal | Small motivating diagram | Avoid a claim without scope; always |
| 02 | Define matrices and compatible dimensions | Shape table | Avoid using symbols before definition; always |
| 03 | Geometric meaning of an algebraic relation | Inspected geometry figure | Avoid treating picture as proof; some abstract topics need a symbolic table instead |
| 04 | Prove identity line by line with justified steps | Dependency flow if proof branches | Avoid hidden cancellation assumptions; always |
| 05 | Compute a 2×2 example and boundary case | Exact-value table | Avoid using examples as proof; always |
| 06 | Algebraic and geometric methods under same assumptions | Labeled comparison figure | Avoid calling equivalent rewrites distinct methods; geometry may lack a faithful representation |
| 07 | Vary a hypothesis and find a counterexample | Graph or counterexample table | Avoid declaring a numerical pattern universal; always |
| 08 | Apply the result to a small transformation | Diagram of application | Avoid forced coding; a pure theorem may use a paper construction |
| 09 | Substitute result and test a limiting case | Verification table | Avoid saying checks replace proof; always |
| 10 | Show invalid division by zero and correction | Annotated failed step | Avoid generic “be careful”; always |
| 11 | Compare direct proof and induction where suitable | Method table | Avoid ignoring domain restrictions; alternative proof may be unavailable |
| 12 | Generalize from scalars to matrices with new conditions | Relation map | Avoid unsupported generalization; a specific narrow result can state why it stops |
| 13 | Proof and counterexample exercises with checks | Figure to annotate if useful | Avoid answerless tasks; always |
| 14 | Explain the decisive proof step and a boundary | Short trace table | Avoid memorization-only questions; always |
| 15 | Proven statement, method, exact scope | Usually no new image | Avoid claiming numerical evidence as proof; always |

## LAB SECTION 01 — INTRODUCTION AND MATHEMATICAL OBJECTIVES
### Claim and outcome
State the question, intended theorem or construction, level, prerequisites, and what a successful explanation establishes. Show a simple motivating case; avoid presenting the conclusion as self-evident.
## LAB SECTION 02 — PROBLEM, DEFINITIONS, AND ASSUMPTIONS
### Domain and notation
Define objects, symbols, quantifiers, allowed values, and assumptions with a small example and nonexample. Make domain restrictions explicit before division, inversion, or limits.
## LAB SECTION 03 — INTUITIVE AND VISUAL FOUNDATIONS
### Representation
Explain the core relation in words, then a suitable geometry figure, function graph, or table. Decode labels and limitations; do not treat a diagram as proof.
## INVESTIGATION TRACK A — FIRST-PRINCIPLES REASONING
Identify the key definition or invariant used in the argument.
## LAB SECTION 04 — DERIVATION, PROOF, OR CONSTRUCTION
### Complete argument
Give a complete topic-suited derivation or proof, justify non-obvious steps, and state where assumptions enter. Fold displayed formulas and check the end statement against the original claim.
## LAB SECTION 05 — FULLY WORKED EXAMPLES
### Small and boundary cases
Work a normal case and a boundary or degenerate case step by step. Show exact values before approximations; avoid skipping arithmetic that carries the idea.
## INVESTIGATION TRACK B — ALTERNATIVE REPRESENTATIONS AND METHODS
Choose genuinely distinct methods rather than cosmetic rewrites.
## LAB SECTION 06 — SYMBOLIC, GEOMETRIC, AND NUMERICAL PERSPECTIVES
### Compare representations
Translate one object across relevant representations, show conditions under which each works, and compare exact versus approximate results. Use plots or tables only when they clarify.
## EXPERIMENTAL INVESTIGATION
Frame a conjecture that examples can test but cannot alone prove.
## LAB SECTION 07 — CONJECTURES, VARIATIONS, AND COUNTEREXAMPLES
### Probe the claim
Vary an assumption, record examples, seek a counterexample to an overbroad claim, then prove or narrow the result. Label numerical pattern as evidence, not proof.
## APPLICATION TRACK
Connect the mathematical object to a genuine use without forcing code.
## LAB SECTION 08 — APPLIED MATHEMATICAL INVESTIGATION
### Part A — Complete Applied Mathematical Case Study (10–12 Steps)
Replace isolated single-equation checks with a realistic multi-step mathematical modeling or theorem-application workflow (paper construction and/or numerical verification where helpful). For **every** step, provide prose purpose, formal expression or code (`Status: static review (not executed)` if unexecuted), collapsed `> [!example]- Step-by-step: ...` or `> [!note]- 📐 Understand this formula` walkthrough, expected interpretation, and transition:
1. **Setup & Conventions:** State domain, ambient space ($\mathbb{R}^n$, $\mathbb{C}^n$, metric space), and notation conventions.
2. **Formulate the Concrete System / Problem:** Define the governing object (matrix, operator, differential system, or optimization objective) with exact dimensions and `Symbol | Domain | Meaning` table.
3. **Structural & Domain Inspection:** Check domain restrictions, continuity/smoothness, symmetry, rank/determinant, or boundary conditions (`Check | Purpose` table).
4. **Partition Hypotheses vs. Target Consequences:** Separate given axioms/boundary constraints from quantities to be solved or bounded.
5. **Construct the Solution Pipeline:** Chain transformations (`normalize/canonicalize -> invariant reduction -> solve -> verify`), explaining why each transformation preserves equivalence.
6. **Execute Internal Derivation / Solver Mechanics:** Walk step by step through the core algebraic, spectral, or iterative mechanism without skipping cancellations.
7. **Compare Representation Forms:** Contrast exact symbolic form, numerical approximation, and geometric meaning in a `Representation | Example Output` table.
8. **Verify Residuals & Error Metrics by Type:** Separate **exact algebraic identities** (zero residual, conservation laws) from **numerical accuracy bounds** (condition number, truncation/rounding error).
9. **Diagnostic Plot / Phase & Error Geometry:** Interpret geometric trajectory, level-set, or convergence curves (using an inspected local web figure or exact table; never Mermaid/ASCII).
10. **Extract Governing Invariants:** Inspect eigenvalues, singular values, fixed points, Lipschitz constants, or critical thresholds (`Invariant | Meaning` table).
11. **Sensitivity Breakdown & Proof-vs-Evidence Caveat:** Show how outputs respond to parameter perturbations and explicitly distinguish **numerical evidence** from **formal proof**.

### Part B — Hypotheses, Regime Parameters & Robustness Analysis
- **Fixed Axioms vs. Tunable Model Parameters Table:** Contrast unchangeable domain axioms against controllable parameters (step size, regularization/damping, tolerance, truncation order).
- **Sensitivity & Conditioning Table:** Show concrete regime behavior across parameter scales (well-conditioned vs. ill-conditioned / singular limits).
- **Solution Method Compatibility Matrix:** Compare direct algebraic, inductive, spectral, and iterative methods (e.g., Newton's method $w_{\text{new}} = w_{\text{old}} - \frac{J'(w)}{J''(w)}$ vs. fixed-point iteration) across linearity, convexity, smoothness, and uniqueness requirements.
- **Degeneracy & Boundary Controls:** Explain strictness tolerances, zero-pivot/singularity guards, and what happens when boundary hypotheses fail.
- **Systematic Regime Sweep:** Design a multi-case verification across regular, boundary, and near-singular parameters, counting test regimes cleanly and distinguishing verified identities from unexecuted sweeps.
## FINAL VALIDATION AND LEARNING
Check reasoning independently.
## LAB SECTION 09 — VERIFICATION AND CONSISTENCY CHECKS
### Independent checks
Substitute results, inspect units/domains, test special cases, and compare an alternative derivation. Explain why each check supports but does not replace proof.
## LAB SECTION 10 — COMMON ERRORS AND FAILED REASONING
### Counterdiagnosis
Show a tempting invalid step, its exact failure, a counterexample, and a corrected argument.
## LAB SECTION 11 — METHOD COMPARISON AND LIMITATIONS
### Conditions
Compare proof or computation methods by assumptions, clarity, generality, and numerical reliability.
## LAB SECTION 12 — CONNECTIONS AND GENERALIZATIONS
### Transfer
Relate the result to a nearby theorem or broader structure, stating which assumptions change.
## LAB SECTION 13 — PRACTICAL AND PROOF CHALLENGES
### Exercises
Offer a worked-start challenge, a proof task, and a counterexample task with checkable outcomes.
## LAB SECTION 14 — FINAL LEARNING CHECKPOINT
### Explain the hinge
Ask learners to state the crucial step, a restriction, and why examples alone are insufficient; include answer guidance.
## LAB SECTION 15 — FINAL SUMMARY
### Claim and scope
Restate the proven result, method, limits, and useful connection concisely.
