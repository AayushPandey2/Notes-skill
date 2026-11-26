# Conditional teaching moves

Load this page when a selected master needs a teaching move beyond its own instructions. These are choices for an author, not software components or checks to execute.

| Need in the request | Use when | What to add and review |
|---|---|---|
| Real-world map & naming fix | Concept has real uses or misleading name | Open with tiny concrete example table, applications table, and name clarification. |
| Motivation & baseline limitations | Learner asks "why not use X?" | Show concrete numbers where simpler baseline is limited + contrast visual (qualified, not exaggerated). |
| Progressive symbols & local foundation | Formulas rely on unfamiliar math/tools | Introduce symbols as needed (with clash note), teach prerequisite tools locally, and place full Symbol Dictionary at the end. |
| Scalar-to-vector-to-matrix construction *(required when vectorizing central formulas)* | Formulas use vectors, matrices, or multi-parameter sums | Derive **1-parameter scalar $\to$ indexed sum $\to$ compact matrix/vector form**, explicitly explaining array shapes, why transposes appear, component alignment, and how matrix multiplication performs summation. |
| Spacious math & formula walkthroughs | A displayed equation serves the objective | Follow [math_gates.md](../../../core/math_gates.md) (bridge before formula, `aligned`/`cases`, grouped coherent folds, compact-reference & non-recursive exceptions). |
| Multi-iteration hand trace | Concept involves iterative updates/steps | Trace consecutive meaningful states on one tiny shared fixture, explaining the progress criterion, whether progress is guaranteed, and failure/stopping conditions. |
| Limits, myths & "NOT required" | Readers confuse adjacent assumptions | Contrast with counterexamples, state what is **NOT** assumed/required, and give `Mistake \| Fix` table. |
| Visual reasoning | Spatial, curve, or flow structure matters | Place at inflection points via [visual guidance](../../procedures/authoring/representations.md). |
| Retrieval & practice cues | Artifact is standalone (no File 3 companion) | Include compact retrieval/practice cues in-note; when File 3 is emitted under `artifact_policy`, keep full formula sheets and Q&A packs in File 3. |

Select only moves needed by the current objective. Review the actual note with [the manual checklist](../../procedures/review/verification-checklist.md).
