# Scriptorium Comparative Benchmark, Ablation & Learning-Effectiveness Protocol

*Evaluation-only manual specification. All evaluations use fresh outputs and evaluator-supplied inputs outside this repository. Keep test scripts and generated outputs out of this workflow and repository.*

For scenarios referring to a supplied note, PDF, image, access restriction, or publication failure, establish that setup explicitly before scoring. An empty `files` list means the repository has no fixture for the case. Use `evaluator_supplied_input` where present. If the setup is unavailable, record the affected case as blocked and omit its score.

## 1. Controlled Comparative Benchmark & Blind Anonymization

Compare candidate approaches (e.g., plain prompt vs. prior Scriptorium version vs. current Scriptorium) manually under strictly matched conditions:
- Identical **topic**, **freshly supplied source material**, **learner knowledge profile**, **model**, **available tools**, and **resource limits**.
- **Blind & anonymized manual grading:** Distinguish explicitly among **self-review**, **independent review**, and **real learner evaluation**: strip commit names and identifying metadata when presenting anonymized fresh candidate outputs (e.g., `candidate-A`, `candidate-B`) to independent reviewers alongside [theory.md](rubrics/theory.md), [practical.md](rubrics/practical.md), and [presentation.md](rubrics/presentation.md). Keep evaluator answer keys separate from candidate prompts; never claim measured educational improvements without actual comparative evidence, and never claim student mastery solely from an AI quality score.
- **Evidence & variance discipline:** Cite **exact passages** for both satisfied requirements and missing/contradicting claims; evaluate repeated fresh generations to measure variance; inspect tool-use logs when judging `source_policy` compliance without executing educational code or custom test scripts.

## 2. Artifact-Aware Scoring Profiles (100 Points) & Calibrated Anchors

Resolve applicable criteria from the intended artifact (`Theory`, `Lab`, `Compact Reference / Atomic Card`, `Strict-Source Note`) **before** scoring—never penalize a compact reference card or `strict`-source note for omitting sections intentionally excluded by `artifact_plan` or `source_policy`. Redistribute inapplicable criteria proportionally. **Override rule:** Any **Critical** correctness, safety, or source-boundary failure fails acceptance regardless of numerical score.

| Artifact Profile | Accuracy | Mechanism / Depth | Prerequisites | Examples / Trace | Evidence / Fidelity | Presentation & Conciseness |
|---|---|---|---|---|---|---|
| **Experimental Lab / `M5`** | 25% | 15% | 8% | 32% (lab correctness & A–G) | 10% | 10% |
| **Compact Reference (`M3`)** | 35% | 15% | 10% | 20% | 10% | 10% |
| **Strict-Source Note (`strict`)** | 30% | 20% | 10% | 10% (source-bound) | 20% (fidelity & gaps) | 10% |

| Dedicated Artifact / Workflow Profile | Primary Scoring Dimensions (100% Proportional) |
|---|---|
| **`M4` Worked Solutions** | Method selection & hypotheses (25%), complete logical/algebraic steps (40%), boundary checks & verification (25%), clarity (10%) |
| **`M6` Assessment** | Question & answer accuracy (35%), objective coverage (25%), discrimination & transfer breadth (25%), tap-to-reveal formatting (15%) |
| **Video Notes (`/scribe-ytnotes`)** | Transcript coverage & timestamps (30%), factual/math reconstruction fidelity (35%), honest access/visual limits (20%), presentation (15%) |
| **`M7` Synthesis & Revision** | Meaningful cross-note relationships (35%), contradiction/convention reconciliation (30%), non-redundancy (20%), presentation (15%) |
| **Interactive Quiz (`/scribe-quiz`)** | One-question pacing (20%), accurate grading & `note_conflict` handling (30%), uncertainty-aware misconception diagnosis & retest (35%), vault read-only hygiene (15%) |
| **Quality Audit (`/scribe-audit`)** | Finding precision & defect recall (40%), severity/confidence calibration (25%), actionable local repairs (25%), purpose-respecting & read-only restraint (10%) |
| **Multi-File Bundle (Aggregate)** | Individual artifact weighted average (75%) + cross-artifact consistency across symbols, objective scaling, claims, and learning objectives (25%) |

| Criterion | Low (0–3) | Medium (4–7) | High (8–10) |
|---|---|---|---|
| **Factual and mathematical accuracy** | Wrong equation, operator, or theorem | Core math holds; minor qualification gaps | Exact hypotheses, units, and checks |
| **Conceptual and causal depth** | Surface definitions only | Mechanism explained; weak limits | Causal depth + transfer + boundaries |
| **Prerequisite accessibility** | Unexplained notation/jumps | Some bridges; uneven pacing | Zero-gap pacing matched to learner |
| **Worked-example quality** | Trivial or inconsistent arithmetic | Correct trace; weak discrimination | Discriminating, verified, faded progression |
| **Source and evidence integrity** | Fabricated or unverified claims | Sources cited; uneven precision | Exact locators, sufficiency & caveats |
| **Practical / Lab correctness** | Unusable or mismatched lab | Static code sound; weak failure analysis | Sound APIs, full A–G, honest 3-attr status |
| **Readability, transfer & conciseness** | Bloated walls of text or broken links | Clean Markdown; minor clutter | Cohesive prose, diagnostic transfer, accessible |

## 3. Experimental Benchmark Matrix, Ablation & Learning Effectiveness

Choose the comparisons that answer the requested evaluation question. Use matched conditions and independent blind review where available. Include unseen cross-domain topics and failure scenarios when they bear on the question.

| Experiment | Purpose |
|---|---|
| **1. Plain prompt vs. Scriptorium** | Establish overall instructional gain over vanilla prompting |
| **2. Previous commit vs. current commit** | Detect regressions in accuracy, coherence, or length |
| **3. Single-layer ablation** | Remove one layer (e.g., Concept Reasoning, Learner Adaptation, Example Engineering, Educational Editor) to estimate marginal value vs. context cost |
| **4. Overlapping layer-group ablation** | Remove layer pairs/clusters to detect duplicated functionality |
| **5. Narrow vs. broad topics** | Measure scaling discipline from atomic cards to full bundles |
| **6. Repeated generations** | Measure output stability and variance across runs |
| **7. Cross-model portability** | Measure instruction reliability across different supported models |

Record exact generated artifacts, model configuration, available tools, input/source conditions, and observed limitations alongside scores.

### Comprehensive Theory Scorecard (100 Points)
Use the single canonical 10-dimension `M1` rubric, exact weights, `0–5` rating scale, `>= 85/100` & `>= 4/5` thresholds, proportional normalization rules, and non-overrideable Critical Defect Overrides defined in [theory-rubric.md](../docs/procedures/review/theory-rubric.md) (evaluated via [theory.md](rubrics/theory.md)). Distinguish clearly between runtime author self-review and independent benchmark grading; a quality-control score is never a measured guarantee of student learning.
- **Learning effectiveness:** Where learner testing is conducted, measure **immediate recall**, **mechanism explanation ("why")**, **application accuracy**, **delayed recall**, **transfer**, **study time**, and **misconception reduction**.

## 4. Resource Accounting *(Evaluations & Requested Performance Reports Only)*

Activate only during evaluations or when the user explicitly requests performance/cost accounting (never add overhead during normal note generation). When provider metadata is available, record model, input/output tokens, cached input, reasoning tokens if exposed, calls/retries/validation calls, elapsed time, accepted output size, and cost using an identified price schedule. Avoid double counting reasoning tokens if included in output totals. Without metadata, report only explicitly labeled estimates or measured character/byte sizes.
