# Explicit Legacy Deep Note Contract

Generate the 7-section skeleton deterministically with:
```bash
python3 "<skill_dir>/scripts/scaffold_note.py" "<vault_path>" --output "<rel_path>" --template legacy-deep --number "<nn>" --title "<Title>" --base-domain "<Domain>" --master-topic "<Master>" --topic "<Topic>"
```
*(Or follow a custom vault template if one was selected in `pre_gen_gate.md`.)*

**Global Authoring Rules:**
- Keep the exact 7 sections in order (`S1`–`S7`). Adapt non-math topics to evidence/logic while keeping all headings.
- Define every symbol in Section 2 before later equations; reuse **one** named running example across Sections 3–5.
- Cite primary claims inline and list exact locations in Section 7; label missing evidence `[UNVERIFIED]`.
- Link existing vault notes via `[[Exact Filename|Title]]`; keep uncreated future topics as plain text.
- Keep raw LaTeX out of YAML frontmatter; escape literal pipes in Markdown tables (`\|`).

---

## Header & `> [!abstract] Key Equations`
- YAML keys: `id`, `title`, `aliases` (include `<Subtopic Title>`, acronym, alternative name), `base_domain`, `master_topic`, `topic`, optional `depends_on` / `next_topic`, `tags` (kebab-case).
- Title: `# <nn>. <Subtopic Title>`.
- `> [!abstract] Key Equations`: 1–3 core display equations (`$$...$$`).

## `## 1. Executive Synthesis & Architectural Significance`
- **Core Problem & Computational Purpose:** 3–4 symbol-free sentences (problem, inputs/outputs, simpler-approach limit and where it still works) + bullets for **Learning outcome**, **Scope**, **Practical recognition**.
- **Governing Mechanism & Unbreakable Invariant:** 2–3 sentences (central mechanism + invariant & domain; reserve proof for S4) + **Validity boundary**, **Success criterion**.
- **Position in the Broader Architecture:** **Taxonomic Lineage**, **Systemic Role** (prerequisites, downstream consumers, real interface), **Conceptual Mental Model** (1 sentence).

## `## 2. Building Blocks & Deep Historical Context`
- `> [!note] Zero-Baseline Prerequisites`: Introduce terms in dependency order (meaning, type/domain/units, tiny example), **Readiness check**, and **Prerequisite connections** (`[[Exact Filename|Title]]`).
- **Historical & Engineering Motivation:** **The Pre-Invention Bottleneck** (4–5 sentences), **The Breakthrough & Core Insight** (4–5 sentences with verified attribution/dates), **Theoretical Impact & Modern Legacy** (3–4 sentences).

## `## 3. Deep Theory Stack: Intuition to Formal Mathematics`
- **Daily-Life Analogy:** Everyday situation + concrete object mapping + `> [!warning] Where the Analogy Breaks Down` (2–3 sentences).
- **Step-by-Step Mechanism & Visuals:** Preconditions (`A1, A2, ...`), **Running example**, 4-step **Causal Pipeline** (`Signal Ingestion` $\to$ `Internal Aggregation` $\to$ `Gate/Threshold` $\to$ `Final Output`), **Mermaid `flowchart TD`** (double-quoted labels, Unicode, no `$...$` inside nodes) + 2–3 sentence text summary, and **Contrastive "Is vs. Is Not" Table** (`Core Mechanism`, `Parameter / Learning Nature`, `Governing Invariant`, `Primary Failure Mode`, `Appropriate Use`).
- **Mathematical Intuition:** 1–2 paragraphs linking operations to geometry/scale/dependence and sensitivity.
- **Formal Equation & Complete Symbol Anatomy:** Domain/assumptions, display equation (`$$...$$`), symbol table (every symbol/operator/index with shape/domain/units and directional sensitivity), **Input-to-Output Behavior Table** (smallest case, running example, changed input, boundary/degenerate case), **Boundary Limits** ($\to 0$, $\to 1/-1$, degenerate/tie, $\to \pm\infty$), and one overgeneralization counterexample.

## `## 4. Step-by-Step Mathematical Proof & Derivation (Zero Skips)`
- State target result, domain, and strategy; number every nontrivial step with `$$...$$` and `*Why this step holds:*` (assumptions, domain/division guards, equivalence vs. implication). Close with sanity check, consequence, and what remains unproven.

## `## 5. Executable Verification (<Primary / Ecosystem Language List>)`
- **Domain-to-Language Routing (1–3 implementations, never pad with trivial variations):**
  - **ML / Deep Learning:** 1. `Python + NumPy` (from-scratch S4 math) · 2. `Python + scikit-learn` (classical API) · 3. `Python + PyTorch` (tensor/autodiff, when applicable)
  - **DSA:** 1. `C++20` (zero-overhead systems/competitive) · 2. `Python 3` (clean reference) · 3. *(Optional)* `Rust` or `Java`
  - **Systems / OS / Concurrency:** 1. `C17` or `Rust` (low-level memory/syscall) · 2. `Python 3` (high-level harness/simulation)
  - **Databases / Data Engineering:** 1. `SQL` (PostgreSQL / DuckDB) · 2. `Python (pandas / polars)`
  - **Web / Distributed Systems / APIs:** 1. `TypeScript / Node.js` or `Go` · 2. `Python 3`
  - **Pure Math / Formal Logic / Non-Code:** 1. `Python + SymPy / NumPy` *(or reproducible proof/counterexample check if code is inapplicable)*
- **Shared Test Contract (Sections 3–4 Parity):** Include `- **Selected Verification Stack:**` and `- **Shared Test Contract:**` (running-example input $\to$ output, boundary/degenerate case, invalid-input guard). Every `### Implementation <k> — <Language & Paradigm>` must share identical variable names, test inputs, and expected assertions so outputs cross-verify.
- State runtime/compiler/package versions, execution status (`not executed` unless actually run), expected vs. observed output, precision/numerical stability, time/space complexity (defining input-size variables), and what tests do not prove.

## `## 6. Deep Conceptual & Analytical Q&A Mastery Set`
- Write 5–6 (up to 7) transfer questions progressing from intuition $\to$ quantitative trace $\to$ parameter synthesis $\to$ boundary stress-test $\to$ cross-architecture trade-off.
- Use `> [!example]- Reveal Detailed Answer & Step-by-Step Breakdown` with every answer line prefixed by `> `. Never use `<details>`/`<summary>` or "I Do/We Do/You Do/Drill A/B".

## `## 7. Common Traps, Primary Sources & Bridge`
- `> [!caution] Common Misconceptions & Anti-Patterns`: 3+ `_Avoid_ -> True Invariant` entries with refuting example and diagnostic check.
- **Primary Sources & Deep Links:** Table (`Source | Direct External Deep Link | Vault Deep Link | Exact Claim / Equation Verified`) with page/theorem/section and inspection status.
- **Bridge to Next Topic:** 2–3 sentences linking to the next concept (plain text if uncreated).
