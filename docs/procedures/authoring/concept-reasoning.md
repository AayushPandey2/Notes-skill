# Concept Reasoning Intelligence

## Purpose

Select the **explanatory strategy** per concept inside the [shared internal concept record](adaptive-engine.md) rather than forcing every section of a note through one fixed sequence. Different concepts inside the same subject require distinct reasoning structures and completion criteria.

## Thirteen Concept Reasoning Types & Completion Criteria

Assign one primary reasoning type (or sequence across sub-concepts) inside the internal concept record:

| Reasoning Type | Explanatory Sequence | Completion Requirement |
|---|---|---|
| **Definition** | Need $\to$ precise meaning $\to$ ordinary translation $\to$ example & non-example | When a genuine confusing distinction exists, separate it from its closest misleading alternative |
| **Mechanism** | Initial state $\to$ operation $\to$ causal intermediate changes $\to$ outcome | Justify consequential state transitions |
| **Transformation** | Input representation $\to$ operation $\to$ preserved vs. changed properties | Distinguish explicitly what information is preserved, changed, or lost |
| **Mathematical relationship** | Motivation $\to$ quantities $\to$ structural construction $\to$ interpretation & limits | Explain *why* the mathematical structure captures the relationship |
| **Theorem** | Exact hypotheses $\to$ assertion $\to$ proof/justification $\to$ consequences | Establish hypotheses, logical validity, and scope |
| **Algorithm** | Problem & representation $\to$ **appropriate correctness principle** ([algorithms.md](../../blueprints/subjects/algorithms.md)) $\to$ operations $\to$ complexity | Verify correctness and progress, termination, or liveness as appropriate under preconditions |
| **Statistical inference** | Observations $\to$ probabilistic model $\to$ estimand/statistic $\to$ uncertainty | Separate estimand, estimator, assumptions, and uncertainty |
| **Architecture** | Purpose $\to$ components & contracts $\to$ interactions $\to$ isolation/failure boundaries | Trace interactions and responsibilities across boundaries |
| **Scientific process** | Entities & conditions $\to$ interactions $\to$ governing laws $\to$ evidence | Distinguish theoretical mechanism from observational evidence |
| **Historical explanation** | Prior context $\to$ chronology $\to$ causal mechanisms $\to$ evidence | Evaluate competing causal interpretations when materially contested |
| **Design decision** | Requirements $\to$ candidate alternatives $\to$ constraints & trade-offs $\to$ choice | Compare trade-offs under stated constraints without inventing a single artificial winner |
| **Diagnostic reasoning** | Symptom $\to$ competing causes $\to$ discriminating check $\to$ **proposed / analytically justified remediation** | Distinguish confirmed causes from plausible hypotheses |
| **Procedure** | Preconditions $\to$ ordered actions with reasons $\to$ expected outcome $\to$ check | Establish how successful completion can be verified |

For a multistage process, trace inputs, operations, retained or changing state, and outputs before describing variants. Explain the governing choice between stages and where the process can fail. For a trade-off, hold the fixture constant when practical so the changed choice is visible. For a statistical tendency, use a counterexample or boundary case to show what the explanation can predict.

## Concept & Equation Transitions

Connect concepts and equations through the question, operation or dependency that motivates the next step. Use those questions to plan, then write natural transitions in the note.
- **Concept transitions:** Avoid presenting individually strong sections as disconnected islands (e.g., *linear score $\to$ odds $\to$ log-odds $\to$ sigmoid $\to$ sigmoid derivative $\to$ Bernoulli likelihood $\to$ BCE $\to$ gradient $\to$ convexity $\to$ optimization $\to$ regularization $\to$ threshold*).
- **Equation-level transitions:** Replace vague leaps (*"Differentiating gives"*, *"Rearranging gives"*, *"Substituting gives"*, *"After simplification"*, *"Therefore, the objective is"*, *"The final matrix equation is"*) by naming: (1) the exact differentiation variable/rule or algebraic operation, (2) the source identity being substituted, (3) which factors cancel and why, (4) why the resulting expression measures the intended target, and (5) how scalar indices pack into vector/matrix dimensions and transposes. (Match granularity to learner mastery without omitting any step a derivation critically depends on.)
