# Mathematical Inclusion, Derivation & Presentation Policy

## Purpose

Govern **whether, how deeply, and how** mathematics appears across Scriptorium outputs (`M1`–`M7`, video notes, and companion labs/cheatsheets) in one coherent, instruction-only policy. Use one shared standard with focused domain guidance—never append competing rules or force irrelevant equations onto non-quantitative topics.

## 1. Objective-Driven Inclusion & Concept-Level Profiles

Before drafting each concept, decide whether mathematics serves the learning objective: what the learner must understand or accomplish, whether a mathematical representation reveals something essential, whether math is required to calculate, derive, implement, compare, or verify, and what prerequisite bridge makes it accessible.

- **Use math when it improves precision or enables the intended reasoning.** Never add equations merely because a subject is technical, and never omit necessary math merely because the audience is a beginner (supply the missing bridge instead of replacing the mechanism with an analogy).
- **Select depth per concept** using these internal planning profiles (planning decisions, **not** mandatory visible labels; different sections of one note may use different profiles):

| Profile | Appropriate treatment |
|---|---|
| **Conceptual** | No equations unless essential; teach through language, examples, and visuals. |
| **Quantitative intuition** | Small calculations, proportions, counts, units, or numerical comparisons. |
| **Working formulation** | Main equations, defined notation, interpretation, and a complete worked example. |
| **Derivation and mechanism** | Justified transformations, intermediate steps, assumptions, and implementation mapping where relevant. |
| **Formal reasoning** | Precise definitions, proofs, conditions, counterexamples, and generalization when required. |

- **Choose the right rigor without truncating derivations:** Keep detail lighter *only* for genuine recognition, orientation, or `M3` compact overviews. For **comprehensive theory (`M1` and substantive quantitative `M2`/`M5`/`M7`)**, invoke the **Mandatory Derivation Contract** below whenever a consequential relationship is derivable. **Never** use arbitrary equation counts or derivation length limits to shorten explanations.
- **Adapt to the topic across all mathematical & technical disciplines:** Apply complete derivations whenever quantitative structure matters—**Linear algebra** (eigenvalues, projections, least squares, factorizations), **Calculus** (derivative identities, integration, Taylor expansions), **Probability & Statistics** (Bayes' rule, expectation/variance identities, estimators, test statistics), **ML / Deep Learning** (objectives, gradients, backpropagation, attention, convergence), **Physics & Electrical** (governing laws, differential equations, transfer functions, time constants), **Algorithms & Computer Architecture** (complexity recurrences, loop invariants, CPI/AMAT, cache decoding), **Numerical Computing & Information Theory** (Taylor updates, error bounds, entropy/mutual-information/coding bounds), and **Chemistry** (equilibrium/kinetic relations). Never force calculus onto qualitative humanities or pure API syntax notes.

## 2. Mandatory Derivation Contract & Mathematical Classification

Every **distinct, consequential, derivable mathematical relationship** introduced in comprehensive theory (including central inline formulas, not only separate-line `$$` blocks) **must receive a complete derivation** from established definitions, assumptions, axioms, governing laws, or previously derived results:
- Explain each consequential transformation: **operation performed**, **permitting mathematical rule**, **why the operation helps**, and **how it advances the result**.
- **Never** substitute symbol definitions, numerical plug-ins, verbal paraphrases, or restatements of the final equation for an actual derivation.
- **Never** fabricate a "proof" or derivation for something that is fundamentally a definition, axiom, modeling convention, or empirical law—classify each formula accurately first:

| Formula Category | Required Explanation |
|---|---|
| **Derived relationship** | Complete derivation from definitions, laws, assumptions, or prior results |
| **Mathematical identity** | Complete algebraic or analytic proof/derivation before downstream use |
| **Mathematical definition** | Motivation, construction, ordinary meaning, and nearest discriminating boundary |
| **Modeling assumption** | Justification, alternatives, and consequences |
| **Theorem** | Exact hypotheses, appropriate proof, and scope limits |
| **Empirical formula** | Evidence origin and empirical validity regime |
| **Approximation** | Derivation and stated error/validity regime |
| **Algorithm update** | Mathematical/optimization justification and structural anatomy |
| **Evaluation metric** | Construction from underlying error/count quantities |
| **Previously derived formula** | Explicit link/reference back to its canonical derivation |
| **Intermediate algebraic expression** | Explained inline within the parent derivation |

## 3. Three Mathematical Reading Layers & Collapsed Formula Architecture

Preserve both clean reading flow and complete mathematical rigor across three coordinated reading layers:
- **Layer 1 — Main theory (always visible):** Connected prose, conceptual motivation, necessary notation, essential equations, key assumptions, interpretation, and transitions into the next concept. Notes must remain coherent with all callouts collapsed.
- **Layer 2 — Collapsible mathematical depth (`> [!example]- Understand this formula step by step`):** Complete step-by-step derivations, transformation rationales, structural anatomy, concrete calculations, alternative forms, and boundary verification.
- **Layer 3 — Advanced extensions:** Optional alternative proofs, deeper generalizations, and specialist implications.

Follow **Question → intuition → necessary quantities → mathematical statement → complete step-by-step derivation (inside fold) → interpretation → next-concept transition**:

1. **Before displaying any equation:** Explain the problem it solves, introduce essential terms locally, establish what the quantities represent, and state what the learner should expect the expression to establish. Never open an unfamiliar concept with an unexplained equation.
2. **Immediately beneath every coherent top-level displayed mathematical unit**, place `> [!example]- Understand this formula step by step` (prefixing every interior line, including blank lines, with `>`), fulfilling these **7 intellectual responsibilities** proportionally (not rigid forced subheadings):
   1. *Mathematical origin* (starting principles, definitions, assumptions)
   2. *Symbol interpretation* (meaning, dimensions, indices, units, domains)
   3. *Complete derivation* (all consequential intermediate transformations)
   4. *Explanation of each step* (operation, permitting rule, and why it is useful)
   5. *Formula construction* (why each term, sign, factor, and operation appears—e.g., in gradient descent $w_{t+1} = w_t - \eta\frac{\partial J}{\partial w_t}$, explain why $w_t$ anchors the step, why $\frac{\partial J}{\partial w_t}$ captures local sensitivity, why subtracting reverses ascent, why $\eta$ controls step magnitude, why iteration repeats, and when reduction actually holds)
   6. *Worked calculation* (concrete values or appropriate discrete check where helpful)
   7. *Interpretation, boundaries & independent verification* (geometric meaning, invariance, limiting values, finite-precision numerical stability, conditions, and sanity check)
   - **Coherent Grouping Exception:** Group sequential derivation steps inside one `aligned` block with **one** fold beneath the unit rather than fragmenting elementary lines.
   - **Non-recursive Exception:** Displayed `$$...$$` blocks inside an existing formula fold, lab fold, or `> [!tip]- Answer`/`Solution` explain steps inline rather than nesting another fold.
   - **Compact Reference Exception:** `M3` cheat sheets, `formula-sheet`, and `atomic-card` may use inline/grouped relations with units, conditions, and canonical derivation links instead of full folds.

## 4. Mathematical Dependency Ordering & Scalar-to-Matrix Progression

- **Mathematical dependency ordering:** Plan derivations so no equation relies on an unproven identity or unexplained construct (for example, establish log-odds $\to$ sigmoid $\to$ sigmoid derivative $\sigma'(z) = \sigma(z)(1-\sigma(z))$ **before** differentiating BCE likelihood). Explain what each newly derived result enables in the next stage of the theory.
- **Required scalar-to-vector-to-matrix pathway:** Whenever a central relationship is vectorized (e.g., gradients, projections, convolutions, covariances), show the progression: **1-parameter scalar form $\to$ indexed multi-parameter summation $\to$ compact matrix/vector form** ($\nabla_{\mathbf{w}} J = \frac{1}{m}X^\top(\hat{\mathbf{p}}-\mathbf{y})$), explicitly justifying array dimensions, why any transpose appears, which component corresponds to each parameter, and how matrix multiplication executes the summation.

## 5. Obsidian Rendering, Notation Hygiene & Code Alignment

- **Native delimiters only:** Use `$...$` inline and separate-line `$$` blocks (with blank lines around display math). Never mix delimiters, use code fences for equations, leave raw LaTeX in prose, place raw LaTeX inside Mermaid labels, or use `==highlight==` / `\color{...}`. Use `aligned`, `cases`, and `\text{...}` cleanly, quote every callout line including blank lines (`>`), escape literal pipes (`\|`) in tables, and reserve `\boxed{...}` strictly for final governing results or key numerical answers.
- **Notation hygiene & code alignment:** Define symbols at first use, distinguish sample vs. feature indices, scalars vs. vectors/matrices, and estimates vs. true quantities. State residual conventions, align objective normalization/penalty scaling explicitly (`C` vs. `alpha`), and verify NumPy/framework operators (`@` vs. `*`, `**` vs. `^`, reduction axes, integer vs. float division, broadcasting, gradient sign, finite-precision cancellation/overflow guards).
- **Single canonical home:** Give each major derivation one canonical home; link or briefly reference prior results elsewhere unless context shifts require bridging.
