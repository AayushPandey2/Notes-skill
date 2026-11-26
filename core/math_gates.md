# Mathematical Inclusion, Depth & Presentation Policy

## Purpose

Govern **whether, how deeply, and how** mathematics appears across Scriptorium outputs (`M1`–`M7`, video notes, and companion labs/cheatsheets) in one coherent, instruction-only policy. Use one shared standard with focused domain guidance—never append competing rules or assign one mathematical depth to an entire domain.

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

- **Choose the minimum depth that satisfies the objective.** Increase depth when the mechanism cannot be understood without it, the learner must implement the calculation, a transformation would otherwise be unexplained, a proof/derivation is requested, assumptions materially affect the conclusion, or numerical verification exposes a mistake. Keep detail lighter for recognition, orientation, or overviews. **Never** use equation counts or minimum derivation lengths as quality targets.
- **Adapt to the topic, not just its domain:** ML optimization may need losses, gradients, and shapes, whereas an ML workflow overview may need only a diagram and concrete example; a mathematical theorem centers on definitions, assumptions, proof, and counterexamples; physics emphasizes governing laws, units, conditions, and limiting cases; chemistry uses quantitative relations where they explain the process; historical/conceptual topics use math only when it answers the actual question. Never force calculus into arithmetic or gradient descent into non-gradient methods.

## 2. Explanatory Bridge & Collapsed Formula Walkthroughs

Follow **Question → intuition → necessary quantities → mathematical statement → worked reasoning → interpretation → check**:

1. **Before displaying any equation:** Explain the problem it solves, introduce essential terms, establish what the quantities represent, and state what the learner should expect the expression to do. Never open an unfamiliar concept with an unexplained equation, and keep the core explanation understandable before opening any fold.
2. **Immediately beneath every coherent top-level displayed mathematical unit**, include a collapsed explanation (prefixing every interior line, including blank lines, with `>`).
   - **Coherent Mathematical Unit Grouping:** Group sequential algebraic derivation steps inside one `aligned` block with **one** `> [!example]- Understand this formula step by step` fold beneath the unit—never fragment successive elementary lines into separate repeated folds.
   - **Non-recursive exception:** Displayed `$$...$$` equations inside an existing formula fold, lab fold, or `> [!tip]- Answer` / `> [!tip]- Solution` block do **not** spawn nested folds—explain them inline within the enclosing fold.
   - **Compact reference exception:** Compact references (`M3`, `formula-sheet`, `atomic-card`) may use inline or grouped relations with direct units, applicability conditions, and canonical derivation links instead of bulky full folds.
   - Never skip central algebraic transitions with `"rearranging gives"` or `"solving yields"`—keep the central transition visible in prose or `aligned` steps and place full step-by-step algebra inside the fold. A bare top-level displayed formula is never compliant merely because its symbols appear in a trailing notation table:

```markdown
> [!example]- Understand this formula step by step
> ...
```

Cover the applicable items—**purpose, plain-language reading, symbols and indices, types/dimensions/units/domains, operations and order, assumptions, non-obvious transformations, numerical example or appropriate alternative, interpretation, and sanity check/limitations**—adapted to the formula (a proof statement needs no artificial numerical substitution; a dimensionless quantity needs no invented units). For derivations, explain each substantive transition without hiding unrelated formulas inside one block. Never repeat the same symbol dictionary or worked calculation across sections.

## 3. Obsidian Rendering & Equation Readability

- **Native delimiters only:** Use `$...$` for short inline symbols/simple relationships and separate-line `$$` delimiters (with blank lines before and after) for central equations, substantial calculations, matrices, piecewise definitions, and derivations. Never mix delimiter conventions, never use code fences for equations, never leave raw LaTeX commands (`\frac`, `\sum`, `\mathbb`) in prose, keep code identifiers in backticks, and never place raw LaTeX inside Mermaid labels.
- **Readable formatting:** Use `aligned` with vertical `=` alignment and meaningful breaks for long derivations; use `cases` for genuine piecewise definitions; use clear matrix environments; write textual annotations with `\text{...}`; format units consistently; avoid excessive `\boxed{...}`, oversized expressions, `==highlight==`, or `\color{...}`, and avoid packing independent ideas into one display. Inside callouts, prefix every line—including blank lines and `$$` delimiters—with `>`. Avoid complex math inside Markdown tables, and escape literal pipes (`\|`).

## 4. Notation Governance, Code Mapping & Reasoning Distinctions

- **Notation hygiene:** Define symbols at or before first meaningful use and keep meanings stable. Distinguish sample indices from feature indices, scalars/vectors/matrices consistently, and estimates from exact quantities. State residual direction, keep units and objective scaling consistent (e.g., SSE vs. half-SSE vs. MSE; normalized vs. unnormalized penalties), and explain notation shifts between sources or libraries. Introduce advanced notation only when its explanatory value justifies the prerequisite burden.
- **Equation-to-code alignment:** In implementation notes, verify and explain `@` vs. `*` in NumPy, `**` vs. `^`, array shapes and transposes, broadcasting, reduction axes, integer vs. floating-point division, objective normalization, gradient signs/scaling, and regularization conversions (`C`, `alpha`). A visually neat expression representing the wrong operation fails review.
- **Distinguish reasoning types:** Clearly separate definitions (stipulated, not proved like theorems), modeling assumptions (justified, not proved universally), empirical relationships (evidence-backed within a regime), algebraic equivalences (valid transformations), identities, approximations, numerical illustrations, and formal proofs (a numerical example illustrates a theorem but does not prove it; an optimization step does not unconditionally decrease the objective). State conditions cleanly without burying the learner.
- **Formula Intelligence & Construction (Selectively for Governing Equations):** Do not merely define symbols and evaluate numbers—select the relevant responsibilities from these twelve so the learner understands *why* the expression has its structure (e.g., deriving $\sigma(z) = \frac{1}{1+e^{-z}}$ from log-odds $z = \ln\frac{p}{1-p}$):
  1. *Origin* (where it comes from) · 2. *Construction* (why these operations/terms) · 3. *Symbol semantics* · 4. *Operation semantics* · 5. *Geometric interpretation* · 6. *Alternative equivalent forms* · 7. *Sensitivity* (input changes) · 8. *Invariance* · 9. *Limiting/extreme behavior* · 10. *Numerical stability* (e.g., log-sum-exp, forward difference $\frac{f(x+h)-f(x)}{h}$ vs. exact $\frac{d}{dx}(x^2)=2x$ and cancellation) · 11. *Applicability conditions* · 12. *Independent verification*.
  *(Not every equation needs all twelve—apply them selectively to central governing relationships.)*
- **Prevent repetition & overload:** Give each important equation one canonical home (referencing it briefly elsewhere unless a new context requires re-explanation). Keep essential reasoning visible; put extended calculations, refreshers, and optional formal detail in folds without concealing missing explanation. When a note becomes overloaded, narrow scope or split distinct objectives rather than stripping essential steps.
