# Primary Research Paper Deconstruction, Derivation & Ablation Audit

- **Header Block**: YAML frontmatter (`type: paper-breakdown`) + `# Paper Breakdown: <Paper Title>` + `> [!abstract] Core Equations & Contribution Summary`.

## 1. What bottleneck was the field stuck on & what did this paper contribute? (Citation, Prior Wall & Breakthrough)

- `> [!info] Primary Paper Metadata`: Full Title, Authors, Venue & Year, Direct arXiv/DOI/PDF URL, Official Code Repository URL, and Supplementary Material status.
- **The Pre-Paper Bottleneck (`4–5` sentences)**: Detail the exact theoretical, architectural, or compute bottleneck in prior literature that motivated this work.
- **Core Contribution & Thesis (`3–4` sentences + 3 bullets)**: What the paper actually introduces, its governing invariant, and what it deliberately leaves out of scope.
- **Research Lineage**: Upstream foundational papers it builds upon and downstream works it directly unlocked.

## 2. How does the proposed mechanism work & why do the equations hold? (Architecture, Equations & Derivations)

- **Mechanism Walkthrough & Visual Architecture**:
    - Define a concrete **Named Running Example** (e.g., a mini batch of tokens, patches, or graph nodes with explicit shapes).
    - Trace the paper's forward/training/inference pipeline through a **Mermaid `flowchart TD` or `sequenceDiagram`** (double-quoted labels, no LaTeX) + `2–3` sentence summary.
- **Key Equations, Symbol Anatomy & Zero-Skip Derivation (`math_level` `1` or `2`)**:
    - Present the paper's core equations (`$$...$$`) with exact equation numbers matching the paper, paired with a **Complete Symbol Anatomy Table** and 4-row **Input-to-Output Behavior Table**.
    - Use `math_level: 2` for any equation central to understanding the paper's contribution, walking through a **Zero-Skip Step-by-Step Derivation** (`$$...$$` + `*Why this step holds:*`).
    - _Pedagogical Transparency Rule_: Whenever you provide an intermediate derivation or intuitive reformulation that was omitted by the authors or differs from their notation, wrap or label it explicitly as:`> [!note] Explanatory Derivation (Distinct from Authors' Presentation in Section X)`

## 3. Do the experiments and ablations actually prove the claim? (Empirical Evaluation & Ablation Audit)

- **Primary Benchmark Results**: Summarize main quantitative comparisons against baselines (citing exact Table/Figure numbers, datasets, metrics, and compute budgets).
- **Structured Ablation Audit Table**:`Ablated Component / Hyperparameter | Experimental Setup & Control | Reported Metric & Delta | Causal Finding (What This Proves)`
- _Missing-Evidence Rule_: Explicitly state when a key result, error bar, compute cost, or expected ablation study is absent from the paper and supplementary material (`[ABLATION / RESULT ABSENT IN PAPER]`).

## 4. Can we verify the paper's core mechanism in minimal code? (Executable Sanity Check)

- When the paper introduces a concrete mathematical operator, loss function, attention mask, or algorithm, provide a minimal runnable verification snippet (`Python + NumPy / PyTorch`) implementing the core equation on the Named Running Example and asserting tensor shapes / invariants. (If the paper is purely empirical/survey/non-computational, trace a structured thought experiment / manual verification instead).

## 5. Where does this method break & what came next? (Limitations, Legacy & Vault Connections)

- **Stated vs. Unstated Limitations**: Contrast the limitations acknowledged by the authors against practical deployment bottlenecks, scaling walls, or hidden assumptions.
- **What Came Next**: How subsequent papers improved upon or superseded this mechanism (citing verified follow-up work when supported).
- **Primary Sources & Paper Section/Equation Verification Table**.
- Append `shared/footer_widgets.md` (**What I learned**, **Open Confusion** `**Confusion** :: ...`, **Atomize**, **Connection**, and the `dataviewjs` **Mark Revisited** button).

Follow [shared authoring rules](../shared/authoring_rules.md) and the [footer contract](../shared/footer_widgets.md). Apply the math gate only at the planned level. Scaffold comments are editing slots and must be removed before publication.

> [!important] AGENT AUTHORING DIRECTIVE — `paper-breakdown` Ground every claim, equation number, and ablation metric directly in the primary paper and its supplementary material. Always use `math_level: 2` for equations essential to the paper's core contribution, explicitly label any explanatory derivation you construct that is distinct from the authors' own presentation, and transparently report when an ablation or metric was absent from the paper rather than inferring or fabricating results. Execute the mandatory **Humanization & Cohesion Pass** so the breakdown reads like a sharp researcher explaining the paper's true insight and limits to their future self, with logical transitions and zero AI clichés.
