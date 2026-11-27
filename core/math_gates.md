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

- **Apply proportional rigor.** In comprehensive quantitative theory (including substantive M1, M2, M5, M7 and video notes), provide complete derivations under the locality rules below. In M4, show every consequential step in the solution itself. Apply the same rigor to worked M6 answers and companion labs where the exercise or implementation depends on it. Compact M3 references may give conditions, units and a canonical link.
- **Honor source permissions first.** Follow [source-fidelity.md](../docs/procedures/sourcing/source-fidelity.md). Reconstruct source-supported steps within the allowed scope. If a derivation needs unprovided premises, identities or instruction and additions are prohibited, disclose the gap. Permission to verify a claim does not authorize adding a derivation or browsing under strict policy.

## 2. Continuous Mathematical Reasoning & Complete Formula Derivations

### Concrete-to-Abstract Ladder, Formula Origin & Visible Reasoning Units

Never dump a consequential formula before establishing the problem it solves, what quantity is calculated, why it is needed, which quantities participate, what operations are involved, and what the result represents (compact `M3` references may assume prior understanding when appropriate). When teaching unfamiliar mathematical machinery, climb the **concrete-to-abstract mathematical ladder** where applicable:
1. Ordinary-language intuition
2. Concrete numerical example
3. Visual or geometric interpretation
4. Simple mathematical expression
5. Generalized notation
6. Advanced mathematical representation
7. Formal derivation or proof

*Never begin with the most generalized expression merely because it algebraically subsumes special cases* (for distance geometry, develop ordinary distance between two numbers/points and Pythagorean Euclidean distance before Manhattan/alternatives, multi-dimensional vectors, generalized Minkowski $L_p$ notation, or metric-equivalence proofs). Explicitly teach each **individual operator before combining composite expressions** (for instance, before writing a composite rule like $\arg\max_{c}\sum_{i}\mathbb{I}(y_i=c)$, establish ordinary counting, then the indicator test, then summation, then argmax selection—applying the same decomposition to nested matrix products, probabilistic objectives, or chained constraints). Prioritize **deriving foundational formulas before proving advanced extensions**—never leave basic formulas asserted while proving secondary asymptotics or norm limits. Distinguish formula origins honestly (**definition, derived identity, theorem, axiom, empirical law, physical law, approximation, optimization result, convention**) and never fabricate a derivation for a definition or empirical relation.

A reasoning unit uses prose and connected equations to establish one mathematical result with deliberate **mathematical pacing**: introduce what is calculated, display the equation, compute/interpret intermediate quantities visibly rather than chaining five transformations into one dense line or table row, explain why each transformation helps, and interpret what the final expression means and unlocks next.

- **Teach the mathematical tool before applying it:** Before invoking an approximation, optimization technique, or calculus identity (e.g., Taylor expansion, Newton's method, composite chain rule, Lagrange multipliers) on a multi-sample or multidimensional objective, introduce it first on a simple one-variable or single-sample case, explain the intuitive meaning of each term (such as slope vs. curvature or why a $\frac{1}{2}$ factor appears), and explicitly map the simple symbols onto the target problem.
- **Explain equation anatomy & mathematical behavior near introduction:** Explain every consequential symbol, index, summation limit, denominator, sign, power, root, logarithm, normalization term, dimension, unit, and constraint *locally where first used* rather than deferring to a trailing notation table. Explain **mathematical behavior** rather than leaving static equations inert: what makes the output increase/decrease, what happens at zero-parameter or boundary values, when assumptions change, whether a trend is **monotonic vs. a general tendency**, whether values are bounded, and what transformations leave the result invariant.
- **Model-to-example equation consistency (Operational Procedure):** Follow these six steps whenever connecting a governing mathematical formulation to a worked numerical trace across any quantitative discipline (machine learning, physics, statistics, engineering):
  1. Identify the governing model or physical equation in general form.
  2. Identify every parameter, initial state, constant, sign, and convention used in the worked example.
  3. Match each parameter and operation explicitly back to the governing equation.
  4. If a parameter (e.g., an intercept, baseline $F_0$, step/learning rate $\eta$, damping constant, or unit conversion) is absorbed into a term or uses an alternative sign convention, declare that equivalence explicitly upfront before computing.
  5. Execute the numerical trace strictly under that same formulation.
  6. Inspect the governing equation, boxed formula, explanatory prose, summary tables, and worked example side by side before finalizing to confirm zero contradiction, dropped prefactors (e.g., $\frac{1}{2}$), sign/ratio mismatches, or hidden parameters.
  - *Completion condition:* The worked example can be reconstructed directly from the governing model without introducing unexplained parameters or conventions.

<example type="contrastive" topic="model-to-example-consistency">
- **Insufficient:** States an additive update $\hat{y}_i = \sum_{k=1}^{K} f_k(x_i)$, then runs a numerical trace starting from baseline $\hat{y}^{(0)} = F_0$ and scaling trees by $\eta$ without showing $F_0$ or $\eta$ in the governing equation (or in physics/statistics, writes $E = mc^2$ or $\mathcal{L}(\theta)$ while evaluating with an unintroduced shift or penalty weight).
- **Preferred:** Writes the governing equation matching the trace—such as $\hat{y}_i^{(t)} = F_0 + \sum_{k=1}^{t} \eta\, f_k(x_i)$ with $\hat{y}_i^{(0)} = F_0$—or explicitly states an absorption convention (e.g., absorbed intercept $F_0 = f_0$, step scale $\eta = 1$) before the worked example begins.
*(Transferable principle: align governing symbols with numerical steps cleanly across every quantitative subject without forcing boosting notation onto unrelated topics.)*
</example>
- **Keep essential reasoning visible:** Read the main theory with all formula folds closed. The question, hypotheses, essential notation, turning points, objective setup, and conclusions must all remain clear in visible prose and milestone displays—never hide the only explanation of a core mechanism inside a collapsed fold, and use aligned multi-line equations rather than single-line compressed chains or wide formula-stuffed tables. When the derivation itself is the principal learning objective (or inside `M4` worked solutions), keep the consequential derivation directly visible.

Use a natural structure for the material (hypotheses and proof for a theorem, model and criterion for an estimator, governing relationship and state trace for an algorithm), mapping concrete calculations onto general terms and referring back to interpret outcomes or boundaries (or leading directly with formal definitions when warranted).

### Required Coverage and Derivation Ownership

Every distinct consequential derivable relationship in comprehensive theory needs a complete derivation, subject to the source permissions above. Derive the topic's central results locally, in visible prose or a formula fold. For a result already derived in the chapter, point back to its section. If an essential prerequisite is unfamiliar, explain locally the part required for the next step. A brief anchor or accessible canonical link can support an established prerequisite or an optional extension. Verify that any cited derivation is accessible and uses compatible assumptions and notation. Disclose source-prohibited derivations as gaps.

### Complete Expandable Derivations *(Separated by Purpose)*

When a reasoning unit needs a local expandable derivation, attach one concise callout after its principal result with a specific title (`> [!example]- Derivation: <Concise focus>` or `> [!example]- Proof: <Concise focus>`—never combine unrelated proofs or emit generic titles like *"Understand this formula step by step"*). Keep visible prose focused on motivation, turning points, and consequences, placing full step-by-step algebra inside the fold without duplicating visible steps. Give distinct local results separate folds, keep derivations already inside worked solutions or visible requests in place, and cover objective, premises, assumptions, applicable identities, notation/units, permitted intermediate steps with rationale, interpretation, and an independent check (limiting case, numerical test, or counterexample—never mere substitution or paraphrase).

### Mathematical Understanding Test *(Apply to Key Formulas & Objectives)*

Before marking a mathematical unit complete, verify that a thoughtful learner can answer every applicable question from the text (plus its closed/open derivation):
- **Why each transform or operator?** (e.g., *why a logarithm, negative sign, square, norm, or inner product is used instead of a simpler alternative*)
- **Why this term structure?** (e.g., *why terms sum, average, normalize, or cancel in this exact form*)
- **Why is each intermediate step valid?** (*what theorem, algebraic identity, linearity/independence condition, or domain restriction permits the transition*)
- **What assumptions, sensitivity, and limits govern it?** (*where the formula holds, how outputs respond when inputs or parameters shift, and what breaks at boundaries or edge cases*)

### Classify the Relationship Before Explaining It

| Relationship | Treatment |
|---|---|
| Derived formula or identity | Justified steps from established results |
| Definition, axiom or convention | Meaning, motivation and applicability |
| Modeling assumption or empirical law | Rationale or evidence, alternatives and validity conditions |
| Theorem | Hypotheses, valid proof and implications |
| Approximation | Starting relation, simplifying assumptions and error or validity regime |
| Algorithm update | Mathematical justification, role of each term and a trace where helpful |
| Evaluation metric | Construction from error, count, ranking or probability quantities |
| Intermediate or reused formula | Explain locally in its parent unit or reference its canonical derivation |

## 3. Mathematical Dependencies & Depth

Establish unfamiliar identities before their first dependent use, giving familiar prerequisites a short anchor where sufficient. Climb the abstraction ladder proportionally to the learner's preparation without repeating elementary math unnecessarily. When component-to-matrix reasoning clarifies a vectorization, derive a representative component, show the indexed sum, and assemble the matrix form; for a naturally matrix-defined object, start at matrix level and unpack relevant rows, columns, or operator actions. Justify shapes, transposes, and reductions wherever they matter.

Distinguish scalar quantities from general multidimensional ones (for example, a scalar second derivative for single-output objectives versus a Hessian matrix in general multidimensional optimization). Distinguish exact optima of an *approximated* surrogate objective from optima of the true underlying objective, and state exact validity conditions (such as smoothness, convexity, additivity across observations, positive curvature, or omitted penalty terms like $L_1 = 0$) instead of making overbroad claims about arbitrary functions.

Choose a derivation strategy that exposes the relevant structure: an indexed expansion for shapes, a geometric argument for invariance, or a Taylor model for a local update. After a consequential result, interpret a useful implication such as a stationarity condition, changed assumption, or limiting case. Where parameter behavior matters, provide static mathematical exploration—showing how changing a quantity affects outcomes via static curves, comparison tables, numerical examples, limiting cases, and prediction exercises without introducing executable interactive components, custom scripts, or plugin dependencies. When it serves the objective, translate between a formula and its geometry, computation, or numerical realization. A short inverse problem can check whether the reader can reconstruct an input or assumption from an outcome.

Retain consequential assumptions, algebra, examples and limitations. Give longer arguments room or split broad topics into coherent chapters. Keep advanced alternative proofs and generalizations optional unless they are part of the requested scope.

## 4. Obsidian Rendering, Notation Hygiene & Code Alignment

### Native Delimiters, Callouts & Table Math
- **Native delimiters & display placement:** Use `$...$` inline and separate-line `$$...$$` display blocks with surrounding blank lines. In body prose, place `$$` delimiters flush left (never use 4-space indentation that turns equations into code blocks, and never wrap ordinary LaTeX in code fences). Keep longer transformations in aligned display equations (`aligned`, `cases`, `\text{...}`) rather than narrow table cells or single-line compressed chains, and reserve `\boxed{...}` for final governing results or key numerical answers.
- **Callout & list math:** Inside Obsidian callouts, quote every interior line—including display-math lines and interior blank lines—with `>`, and leave an unquoted blank line after exiting the callout. Inside lists, indent equations consistently with the enclosing list item so list containment stays intact.
- **Table delimiters:** Inside Markdown tables, avoid raw vertical pipes splitting cells by using unambiguous LaTeX commands instead of `\|`: `\lvert x \rvert` (or `\left\lvert \dots \right\rvert`) for absolute value/cardinality, `\lVert \mathbf{x} \rVert_2` for norms, `P(A \mid B)` for conditional probability, `\{x \mid x > 0\}` for set-builder notation, and `\det(A)` (or display `vmatrix` outside tables) for determinants.

### Notation Hygiene, Bounds Verification & Code Alignment
- **Local symbol introduction & set-vs.-index hygiene:** Define symbols at first use and maintain consistent notation across prose, equations, examples, and companion artifacts without creating a separate notation registry. Never use the same symbol for incompatible objects (strictly separate a *dataset*, a *set of example pairs*, a *set of indices*, a *feature vector*, a *target*, a *prediction*, a *distance function*, a *dimensionality variable*, and a *parameter*). If a long chapter legitimately reuses a letter across distinct domains (e.g., Hessian sum $H_j$ vs. feature histogram), disambiguate explicitly (e.g., $\mathrm{Hist}_{\text{right}}$ or an explicit scope qualifier) wherever nearby equations could conflict.
- **Arithmetic, bounds & tie-policy verification:** Manually verify arithmetic, algebra, derivations, signs, dimensions, units, domains, derived table columns/ratios (e.g., $k_{\text{cat}}/K_M$, gains, probabilities), parameter bounds (upper and lower bounds on discrete counts/sizes), zero-denominator cases, index consistency, quantifier conditions, and exact equality/inequality & tie-policy assumptions behind bounds or pruning rules (explicitly stating whether strict `>` vs. non-strict `>=` depends on retaining ties, whether a bound is universal or conditional, and separating verified mathematical invariants/monotonicity from empirical tendencies). For consequential numerical results and derived table entries, perform an independent static cross-check proportional to quantitative scope—such as re-substitution, order-of-magnitude/exponent check, dimensional check, or limiting-case check—rather than trusting copied values.
- **Framework operator alignment:** Verify NumPy/framework operators (`@` vs. `*`, `**` vs. `^`, reduction axes, integer vs. float division, broadcasting, gradient sign, finite-precision cancellation/overflow guards).
- **Single canonical home:** Give each major derivation one canonical home; link or briefly reference prior results elsewhere unless context shifts require bridging.
