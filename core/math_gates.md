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
- **Model-to-example equation consistency:** Every term used in worked numerical examples (such as an initial prediction/intercept $F_0$, learning rate $\eta$, regularization penalties, or link transformations) must appear explicitly in the governing model equation—or any absorption convention must be declared upfront so the general theory and numerical traces match without contradiction.
- **Keep essential reasoning visible:** Read the main theory with all formula folds closed. The question, hypotheses, essential notation, turning points, objective setup, and conclusions must all remain clear in visible prose and milestone displays—never hide the only explanation of a core mechanism inside a collapsed fold, and use aligned multi-line equations rather than single-line compressed chains or wide formula-stuffed tables. When the derivation itself is the principal learning objective (or inside `M4` worked solutions), keep the consequential derivation directly visible.

Use a natural structure for the material: hypotheses and proof for a theorem, model and criterion for an estimator, or governing relationship and state trace for an algorithm. Introduce local definitions and conventions where they do explanatory work, rather than deferring every symbol definition to an end-of-note table.

For an unfamiliar abstraction, work an ordinary case with meaningful quantities before introducing indices or a generalized family. Show which calculation becomes a term or operation in the general expression. Refer back to the visible example after formalizing it and interpret at least one outcome or boundary when it advances the objective. Lead with definitions or hypotheses directly when the audience or task warrants formal treatment.

### Required Coverage and Derivation Ownership

Every distinct consequential derivable relationship in comprehensive theory needs a complete derivation, subject to the source permissions above. Derive the topic's central results locally, in visible prose or a formula fold. For a result already derived in the chapter, point back to its section. If an essential prerequisite is unfamiliar, explain locally the part required for the next step. A brief anchor or accessible canonical link can support an established prerequisite or an optional extension. Verify that any cited derivation is accessible and uses compatible assumptions and notation. Disclose source-prohibited derivations as gaps.

### Complete Expandable Derivations *(Separated by Purpose)*

When a reasoning unit needs a local expandable derivation, attach one concise descriptive Obsidian callout after its principal result with a **clear mathematical-objective title** (`> [!example]- Derivation: <Focus>` or `> [!example]- Proof: <Focus>`—never combine unrelated proofs into one oversized fold, and **never emit vague repeated titles** such as *"Understand this formula step by step"*). Never duplicate algebraic steps already written in full in the visible prose immediately above—keep visible text focused on motivation, turning points, and consequences, and place full step-by-step algebra inside the fold:

`> [!example]- Derivation: <Concise focus>` *(or `> [!example]- Proof: <Concise focus>`)*

Use one fold for connected steps serving the same objective. Give a genuinely distinct local result its own derivation. Use the ownership rules above for canonical references. A derivation that is already in a worked solution, answer or lab fold stays there. If the derivation is itself the requested visible artifact, keep its consequential steps visible rather than duplicating it in another fold.

Cover the objective, starting principles, assumptions, applicable identities, notation (including domains, dimensions and units), intermediate transformations, formula structure, interpretation and verification. Explain which rule permits each consequential operation and why the new form helps. Use a numerical application, limiting case, counterexample or other independent check where it adds insight. These responsibilities guide the explanation without prescribing fixed subheadings. Numerical substitution, paraphrase and unexplained shortcuts cannot stand in for derivation.

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

Establish unfamiliar identities before their first dependent use. Give familiar prerequisites a short anchor where that suffices for the learner. When complex formalism creates a barrier, climb the **mathematical abstraction ladder** proportionally to the learner's preparation (without repeating elementary math unnecessarily): *concrete intuition $\to$ simple numerical operations $\to$ scalar mathematical representation $\to$ vector or matrix form (where applicable) $\to$ general formal notation $\to$ interpretation and application*—always establishing the operation before its general symbol. When component-to-matrix reasoning clarifies a vectorization, derive a representative component, show the indexed sum and then assemble the matrix form. For a naturally matrix-defined object, start at matrix level and unpack the relevant rows, columns or operator actions. Justify shapes, transposes and reductions wherever they matter.

Distinguish scalar quantities from general multidimensional ones (for example, a scalar second derivative for single-output objectives versus a Hessian matrix in general multidimensional optimization). Distinguish exact optima of an *approximated* surrogate objective from optima of the true underlying objective, and state exact validity conditions (such as smoothness, convexity, additivity across observations, positive curvature, or omitted penalty terms like $L_1 = 0$) instead of making overbroad claims about arbitrary functions.

Choose a derivation strategy that exposes the relevant structure: an indexed expansion for shapes, a geometric argument for invariance, or a Taylor model for a local update. After a consequential result, interpret a useful implication such as a stationarity condition, changed assumption, or limiting case. Where parameter behavior matters, provide static mathematical exploration—showing how changing a quantity affects outcomes via static curves, comparison tables, numerical examples, limiting cases, and prediction exercises without introducing executable interactive components, custom scripts, or plugin dependencies. When it serves the objective, translate between a formula and its geometry, computation, or numerical realization. A short inverse problem can check whether the reader can reconstruct an input or assumption from an outcome.

Retain consequential assumptions, algebra, examples and limitations. Give longer arguments room or split broad topics into coherent chapters. Keep advanced alternative proofs and generalizations optional unless they are part of the requested scope.

## 4. Obsidian Rendering, Notation Hygiene & Code Alignment

- **Native delimiters, display placement & table math:** Use `$...$` inline and separate-line `$$...$$` display blocks with surrounding blank lines. In body prose, place `$$` delimiters flush left (never use 4-space indentation that turns equations into code blocks, and never wrap ordinary LaTeX in code fences); inside Obsidian callouts, preserve `>` prefixes on display and blank lines; inside lists, indent consistently with the enclosing list item so list containment stays intact. Keep longer transformations in display equations rather than narrow table cells, use `aligned`, `cases`, and `\text{...}` cleanly, leave an unquoted blank line after exiting a callout, quote every callout interior line (`>`), and reserve `\boxed{...}` for final governing results or key numerical answers. Inside **Markdown tables**, avoid raw vertical pipes splitting cells and use unambiguous LaTeX commands instead of `\|` for math delimiters: `\lvert x \rvert` (or `\left\lvert \dots \right\rvert`) for absolute value/cardinality, `\lVert \mathbf{x} \rVert_2` for norms, `P(A \mid B)` for conditional probability, `\{x \mid x > 0\}` for set-builder notation, and `\det(A)` (or display `vmatrix` outside tables) for determinants.
- **Notation hygiene, set-vs.-index consistency, bounds verification & code alignment:** Define symbols at first use and maintain consistent notation across prose, equations, examples, and companion artifacts without creating a separate notation registry—never use the same symbol for incompatible objects (strictly separate a *dataset*, a *set of example pairs*, a *set of indices*, a *feature vector*, a *target*, a *prediction*, a *distance function*, a *dimensionality variable*, and a *parameter*). Manually verify arithmetic, algebra, derivations, signs, dimensions, units, domains, parameter bounds (e.g., upper and lower bounds on discrete counts/sizes), zero-denominator cases, index consistency, quantifier conditions, and **exact equality/inequality & tie-policy assumptions behind bounds or pruning rules** (stating whether strict `>` vs. non-strict `>=` depends on retaining ties, whether a bound is universal or conditional, and separating verified mathematical invariants/monotonicity from empirical tendencies). Verify NumPy/framework operators (`@` vs. `*`, `**` vs. `^`, reduction axes, integer vs. float division, broadcasting, gradient sign, finite-precision cancellation/overflow guards).
- **Single canonical home:** Give each major derivation one canonical home; link or briefly reference prior results elsewhere unless context shifts require bridging.
