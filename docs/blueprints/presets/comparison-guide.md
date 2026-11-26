# Preset: Domain-Adaptive Comparison Guide (`M7` / `comparison_guide`)

- **Parent Master:** [M7 — Synthesis & Revision](../formats/synthesis-revision.md) (`single_artifact`).
- **Activation Trigger:** `"compare X vs Y"`, `"trade-offs between A and B"`, `"when to use X vs Y"`.

## Execution Overrides
1. **Domain-Adaptive Comparison Dimensions:** Select criteria from the objects being compared—never force time/memory complexity onto historical, philosophical, or biological comparisons:
   - *Algorithms:* Correctness, complexity, constraints, resource use.
   - *Scientific models:* Predictive scope, assumptions, evidence, limitations.
   - *Historical interpretations:* Primary evidence, causal reasoning, context.
   - *Philosophical positions:* Premises, logical implications, objections.
   - *Engineering designs:* Cost, reliability, safety, performance.
   - *Statistical methods:* Assumptions, estimands, uncertainty, robustness.
2. **Matched Assumptions & Conditional Verdicts:** Compare under strictly matched assumptions/workloads; lead with `"Choose X When..."` or explicitly conclude **"No universal winner"** when options dominate in distinct regimes or remain context-dependent.
3. **Causal Divergence & Crossover:** Explain *why* mechanisms diverge before tables ([math_gates.md](../../../core/math_gates.md), [representations.md](../../procedures/authoring/representations.md)) and trace one shared case showing where preferences flip. Never fabricate unmeasured benchmarks (`[UNVERIFIED]`).
