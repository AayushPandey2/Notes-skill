# Scriptorium Comparative Benchmark, Ablation & Learning-Effectiveness Protocol

*Evaluation-only specification—never load during normal note authoring.*

## 1. Controlled Comparative Benchmark & Blind Anonymization

Compare candidate approaches (e.g., plain prompt vs. prior Scriptorium commit vs. current Scriptorium) under strictly matched conditions:
- Identical **topic**, **source material**, **learner knowledge profile**, **model**, **available tools**, and **resource limits**.
- **Blind & anonymized grading:** Strip commit names, file-status tags (`-golden` / `-flawed`), and identifying headings, presenting anonymized IDs (e.g., `candidate-A`, `candidate-B`) to reviewers alongside [theory.md](rubrics/theory.md), [practical.md](rubrics/practical.md), and [presentation.md](rubrics/presentation.md). Keep `*-flawed.md` fixtures separate from their `*-flawed.expected-findings.md` keys.
- **Evidence & variance discipline:** Record **missing requirements and contradicting passages** in addition to passed passages; evaluate repeated generations to measure variance; include relevant tool-use and source-access logs when judging `source_policy` compliance.

## 2. Weighted Scoring Rubric (100 Points) & Calibrated Anchors

Redistribute inapplicable criteria proportionally when scoring non-technical topics. **Override rule:** Any **Critical** defect fails acceptance regardless of numerical score.

| Criterion | Weight | Low (0–3) | Medium (4–7) | High (8–10) |
|---|---|---|---|---|
| Factual and mathematical accuracy | 25% | Wrong equation, operator, or theorem | Core math holds; minor qualification gaps | Exact hypotheses, units, and checks |
| Conceptual and causal depth | 20% | Surface definitions only | Mechanism explained; weak limits | Causal depth + transfer + boundaries |
| Prerequisite accessibility | 10% | Unexplained notation/jumps | Some bridges; uneven pacing | Zero-gap pacing matched to learner |
| Worked-example quality | 10% | Trivial or inconsistent arithmetic | Correct trace; weak discrimination | Discriminating, verified, faded progression |
| Source and evidence integrity | 10% | Fabricated or unverified claims | Sources cited; uneven precision | Exact locators, sufficiency & caveats |
| Practical correctness | 10% | Unusable or mismatched lab | Static code sound; weak failure analysis | Sound APIs, full A–G, honest 3-attr status |
| Readability and visual design | 7% | Walls of text or broken embeds | Clean Markdown; minor clutter | Cohesive prose, adaptive visuals, accessible |
| Transfer and assessment quality | 5% | Rote recall only | Mix of recall and application | Diagnostic, misconception-aware, transfer |
| Relevance and conciseness | 3% | Bloated boilerplate or off-topic | Mostly focused; minor redundancy | Every paragraph earns its place |

## 3. Layer Ablation & Learning Effectiveness

- **Layer ablation testing:** Compare full-skill generation against ablated variants (omitting one layer such as Concept Reasoning, Learner Modeling, Example Engineering, Consistency Ledger, or Educational Editor) to verify every retained layer measurably improves output quality over its context cost.
- **Learning effectiveness:** Where learner testing is conducted, measure **immediate recall**, **mechanism explanation ("why")**, **application accuracy**, **delayed recall**, **transfer**, **study time**, and **misconception reduction**.
