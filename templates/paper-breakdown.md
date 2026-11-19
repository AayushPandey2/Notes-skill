<!-- scaffold:preflight
Decision-Matrix Pre-Flight: [routing index](../shared/note_decision_matrix.md) and [shared decision guide](../shared/notes_decision_matrix.md).
Switches: D01 route (`paper-breakdown`); D02 single-paper scope; D03 reader; D04 research synthesis/verification outcome; D05 primary paper + supplement;
D06–D09 `math_level` (level 2 for core contribution equations); D10 running tensor/token fixture; D11 architecture diagram;
D12–D13 minimal code sanity check / ablation audit; D14 optional module (`history`); D15 final audit.
Strip this block before emission. Load detailed DM branches only when active.
-->

# Primary Research Paper Deconstruction, Derivation & Ablation Audit

- **Header Block**: Metadata per shared contract + `# Paper Breakdown: <Paper Title>` + `> [!abstract] Core Equations & Contribution Summary`.

## 1. What bottleneck was the field stuck on & what did this paper contribute? (Citation, Prior Wall & Breakthrough)

<!-- Gate: DM-01, DM-03, DM-05.
KEEP paper identity, access, proposed contribution, and the evidence it addresses. Remove this gate before publication. -->

- `> [!info] Primary Paper Metadata`: Full Title, Authors, Venue & Year, Direct arXiv/DOI/PDF URL, Official Code Repository URL, and Supplementary Material status.
- **The Pre-Paper Bottleneck (`4–5` sentences)**: Detail the exact theoretical, architectural, or compute bottleneck in prior literature that motivated this work.
- **Core Contribution & Thesis (`3–4` sentences + 3 bullets)**: What the paper actually introduces, its governing invariant, and what it deliberately leaves out of scope.
- **Research Lineage**: Upstream foundational papers it builds upon and downstream works it directly unlocked.

## 2. How does the proposed mechanism work & why do the equations hold? (Architecture, Equations & Derivations)

<!-- Gate: DM-04, DM-05, DM-06, DM-07, DM-09.
ADAPT to the actual mechanism and preserve the paper's assumptions and sequence. Remove this gate before publication. -->

- **Mechanism Walkthrough & Visual Architecture**:
    - Define a concrete **Named Running Example** (e.g., a mini batch of tokens, patches, or graph nodes with explicit shapes).
    - Trace the paper's forward/training/inference pipeline through a **Mermaid `flowchart TD` or `sequenceDiagram`** (double-quoted labels, no LaTeX) + `2–3` sentence summary.
- **Key Equations, Symbol Anatomy & Zero-Skip Derivation (`math_level` `1` or `2`)**:
    - Present the paper's core equations (`$$...$$`) with exact equation numbers matching the paper, paired with a **Complete Symbol Anatomy Table** and 4-row **Input-to-Output Behavior Table**.
    - Use `math_level: 2` for any equation central to understanding the paper's contribution, walking through a **Zero-Skip Step-by-Step Derivation** (`$$...$$` + `*Why this step holds:*`).
    - _Pedagogical Transparency Rule_: Whenever you provide an intermediate derivation or intuitive reformulation that was omitted by the authors or differs from their notation, wrap or label it explicitly as:`> [!note] Explanatory Derivation (Distinct from Authors' Presentation in Section X)`

## 3. Do the experiments and ablations actually prove the claim? (Empirical Evaluation & Ablation Audit)

<!-- Gate: DM-05, DM-17, DM-18.
KEEP evaluation conditions and distinguish experimental evidence from general claims. Remove this gate before publication. -->

- **Primary Benchmark Results**: Summarize main quantitative comparisons against baselines (citing exact Table/Figure numbers, datasets, metrics, and compute budgets).
- **Structured Ablation Audit Table**:`Ablated Component / Hyperparameter | Experimental Setup & Control | Reported Metric & Delta | Causal Finding (What This Proves)`
- _Missing-Evidence Rule_: Explicitly state when a key result, error bar, compute cost, or expected ablation study is absent from the paper and supplementary material (`[ABLATION / RESULT ABSENT IN PAPER]`).

## 4. Can we verify the paper's core mechanism in minimal code? (Executable Sanity Check)

<!-- Gate: DM-14, DM-15, DM-18.
Use an executable check only for a reproducible claim. Otherwise describe a real verification barrier. Remove this gate before publication. -->

- When the paper introduces a concrete mathematical operator, loss function, attention mask, or algorithm, provide a minimal runnable verification snippet (`Python + NumPy / PyTorch`) implementing the core equation on the Named Running Example and asserting tensor shapes / invariants. (If the paper is purely empirical/survey/non-computational, trace a structured thought experiment / manual verification instead).

## 5. Where does this method break & what came next? (Limitations, Legacy & Vault Connections)

<!-- Gate: DM-05, DM-19, DM-20.
KEEP material threats to validity and evidenced follow-up. Remove this gate before publication. -->

- **Stated vs. Unstated Limitations**: Contrast the limitations acknowledged by the authors against practical deployment bottlenecks, scaling walls, or hidden assumptions.
- **What Came Next**: How subsequent papers improved upon or superseded this mechanism (citing verified follow-up work when supported).
- **Primary Sources & Paper Section/Equation Verification Table**.

<!-- optional: history -->
## [OPTIONAL] Which earlier constraint explains this design? (Historical Evolution & Competing Paradigms)

<!-- Gate: DM-05, DM-19.
Include only documented design lineage that explains a material choice. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: A verified historical bottleneck or competing paradigm directly motivates a core architectural or theoretical choice in the paper; D05, D14.
- When to Omit Cleanly: Omit if Section 1's Pre-Paper Bottleneck already covers the lineage or if historical claims lack primary citations. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Contrast documented prior capability and constraint with the paper's mechanism; cite primary passages and separate chronology from causal attribution.
-->

- **Context:** State the historical bottleneck, competing paradigm, and cited prior work.
- **Analysis:** Contrast the prior limitation against this paper's design choice, keeping chronology distinct from causal attribution.
- **Check:** Verify each historical attribution against inspected primary passages (mark gaps `[UNVERIFIED]`).

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`paper-breakdown`):** Ground every claim, equation number, and ablation in the paper/supplement; use `math_level: 2` for core contribution equations; explicitly label added explanatory derivations as distinct from the authors' text; mark absent ablations `[ABLATION / RESULT ABSENT IN PAPER]`.
