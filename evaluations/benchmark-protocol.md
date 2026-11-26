# Scriptorium Comparative Benchmark & Learning-Effectiveness Protocol

*Evaluation-only specification—never load during normal note authoring.*

## 1. Controlled Comparative Benchmark

Compare candidate approaches (e.g., plain prompt vs. prior Scriptorium commit vs. current Scriptorium) under strictly matched conditions:
- Identical **topic**, **source material**, **learner knowledge profile**, **model**, **available tools**, and **resource limits**.
- **Blind grading:** Evaluate anonymized generated notes against [theory.md](rubrics/theory.md), [practical.md](rubrics/practical.md), [presentation.md](rubrics/presentation.md), and blind flawed fixtures (`*.flawed.md` without exposing `*.expected-findings.md`). Every passed criterion must cite exact passages.

## 2. Weighted Scoring Rubric (100 Points; Critical Failure Overrides Score)

Redistribute inapplicable criteria (e.g., practical code for pure humanities) proportionally when scoring non-technical topics:

| Criterion | Weight |
|---|---|
| Factual and mathematical accuracy | 25% |
| Conceptual and causal depth | 20% |
| Prerequisite accessibility | 10% |
| Worked-example quality | 10% |
| Source and evidence integrity | 10% |
| Practical correctness | 10% |
| Readability and visual design | 7% |
| Transfer and assessment quality | 5% |
| Relevance and conciseness | 3% |

**Override rule:** Any **Critical** defect (fabricated source/observation, unsafe instruction, or fundamentally wrong theorem/formula) fails acceptance regardless of numerical score.

## 3. Measuring Actual Learning Effectiveness

Spec compliance alone does not prove learning effectiveness. Where learner testing is conducted, measure: **immediate recall**, **mechanism explanation ("why")**, **application accuracy**, **delayed recall**, **transfer to unfamiliar cases**, **study time**, and **misconception reduction**.
