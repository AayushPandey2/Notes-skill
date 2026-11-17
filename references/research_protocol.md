# `scriptorium` — Wave-Based Deep Research Protocol (`references/research_protocol.md`)

<!-- EXECUTION CONTRACT:
- Governs Phase 1 (Research & Dossier Synthesis) before any `.md` note is written to the Obsidian vault.
- Designed for maximum signal-to-token efficiency: inspect existing vault metadata via `vault_index.py` first, execute research in four deterministic waves, and lock a verified per-subtopic dossier before drafting.
-->

---

## §0. Command Entry & Wave Routing

| Command | Vault Discovery | Research Waves Executed | Output Target |
| :--- | :--- | :--- | :--- |
| **`/scribe-notes <topic>`** | `vault_index.py` (check duplicates) | **Wave 0 $\to$ Wave 1 $\to$ Wave 2 $\to$ Wave 3 $\to$ Wave 4** | Full multi-subtopic `.md` tree (`topic-01` ... `topic-nn`) |
| **`/scribe-expand <topic>`** | `vault_index.py --topic "<topic>"` | **Wave 0** (gap audit) $\to$ **Waves 1–4** (missing/advanced nodes only) | Missing core subtopics OR advanced expansion subtopics |
| **`/scribe-distill <topic>`** | `vault_index.py --topic "<topic>"` | **Wave 0** + existing vault notes only *(skip Waves 2–3 unless vault has `[UNVERIFIED]` gaps)* | Single `<topic-name>-CHEAT-SHEET.md` |

---

## §1. Retrieval & Source Discipline (Non-Negotiable)

- **Chase to origin:** Never cite a secondary blog, Medium post, or wrapper tutorial when the original paper, RFC, specification, textbook, or source repository is reachable.
- **Knowledge (Primary Sources — Required for Definitions, Proofs & Equations):**
  - Peer-reviewed foundational papers, canonical textbooks, RFCs/standards, official language/framework documentation, source repositories, and official release notes.
- **Wisdom (Practitioner Sources — Required for Traps, Limits & Trade-offs):**
  - Engineering post-mortems, creator/maintainer talks, canonical benchmark analyses, and vetted issue threads exposing real-world sharp edges, numerical instability, or failure modes.
- **Strict Exclusions:**
  - Never rely on or cite SEO listicles, AI-generated summaries, undated/unversioned tutorials, or unverified claims.
- **Explicit Gap & Conflict Logging:**
  - Conflicting definitions across papers, paywalled details, missing benchmarks, or unverified historical attributions must be tagged `[UNVERIFIED]` inline and logged explicitly in the dossier's **Gaps & Unverified Claims** block—never paper over them or fabricate citations.

---

## §2. The Four-Wave Research Pipeline

### Wave 0 — Vault Reconnaissance & Scope Locking (Zero-Token Index)
1. **Run Indexer First:** Execute `python3 <skill_dir>/scripts/vault_index.py "<vault_path>"` (filtered by `--topic` when applicable) instead of reading full vault notes.
2. **Map Existing Topology:** Record existing `id`, `title`, `aliases`, `depends_on`, `next_topic`, and `status` across the domain.
3. **Branch by Command Intent:**
   - **`/scribe-notes`:** Exclude already-verified subtopics from recreation; link to them as prerequisites.
   - **`/scribe-expand`:**
     - *Branch A (Core Gaps Exist):* Target every missing foundational or core subtopic needed for complete coverage.
     - *Branch B (Core Complete):* Propose 3–5 high-leverage expansion subtopics (e.g., convergence proofs, edge-case pathology, hardware/complexity optimizations, or modern generalizations).
   - **`/scribe-distill`:** Extract equations, symbols, and traps directly from existing vault notes; do not run external web retrieval unless a core formula is missing.

---

### Wave 1 — Architectural Scoping & First-Principles DAG Decomposition
1. **Atomic Subtopic Tree:** Decompose `<topic>` into a Directed Acyclic Graph (DAG) of atomic subtopics (`topic-01`, `topic-02`, ..., `topic-nn`) ordered strictly from:
   $$\text{Foundational Axioms/Objects} \longrightarrow \text{Core Mechanism} \longrightarrow \text{Formal Proofs/Algorithms} \longrightarrow \text{Variants, Limits \& Failure Regimes}$$
2. **Graph Edge Pre-Assignment:** Assign exact target filenames, clean `aliases`, `depends_on`, and `next_topic` edges for every node *before* writing begins so cross-links resolve 100% on the first pass.
3. **Global Notation Lock:** Establish one canonical symbol table for the entire `<topic>` series (e.g., $\mathbf{x} \in \mathbb{R}^d$, $\mathbf{w} \in \mathbb{R}^d$, $b = -\theta$, $\hat{y} \in \{0, 1\}$) so notation never drifts between `topic-01` and `topic-06`.

---

### Wave 2 — Primary Knowledge Retrieval ("Chase to Origin")
For each subtopic in the DAG, retrieve from **Primary Sources** only:
1. **Formal Problem & Governing Invariant:** Exact problem statement, inputs/outputs, mathematical formulation, and whether the core statement is a *definition*, *theorem*, *modeling assumption*, or *empirical heuristic*.
2. **Verified Historical Lineage:** Original formulation, independent rediscoveries, formalization vs. popularization, and exact publication year/author/venue (marking uncertain attribution `[UNVERIFIED]`).
3. **Zero-Skip Mathematical Derivation:** Every algebraic, logical, or probabilistic transition from starting axioms to the governing equation, tracking domain restrictions, equivalence ($\iff$) vs. implication ($\implies$), and dimensional/shape compatibility.
4. **Algorithmic & Complexity Contract:** Exact time and auxiliary space complexity (with input-size variables explicitly defined) plus deterministic reference logic for Section 5's Python/NumPy verification script.

---

### Wave 3 — Practitioner Wisdom, Edge Cases & Adversarial Stress-Testing
Query **Practitioner & Benchmark Sources** to stress-test every subtopic beyond textbook idealizations:
1. **Contrastive Lookalike ("Is vs. Is Not"):** Identify the single closest concept learners confuse with this subtopic and isolate exact differences in mechanism, parameter nature, invariant, and failure mode.
2. **Four Boundary Regimes:** Determine exact behavior under:
   - *Zero / Null Regime* ($\to 0$ or empty input)
   - *Unit / Normalized Regime* ($\to \pm 1$)
   - *Degenerate / Tie Regime* (equality on boundary, rank deficiency, zero denominator)
   - *Asymptotic Regime* ($\to \pm\infty$ or large scale)
3. **Real-World Sharp Edges & Traps:** Collect practitioner failure modes (e.g., numerical overflow/underflow, non-convergence under violated assumptions, hidden hyperparameter sensitivities) to populate Section 7's `> [!caution]` callout and Section 6's adversarial questions.

---

### Wave 4 — Cross-Verification & Pre-Writing Subtopic Dossier
Before invoking `note_templates.md` to write a subtopic `.md` file, assemble and validate a compact internal dossier containing:
- [ ] **Identity & Graph Edges:** `id`, exact filename, `aliases`, `depends_on`, `next_topic`, and verified primary source URLs/citations.
- [ ] **Locked Equations & Symbol Table:** Every equation checked for balanced syntax, valid LaTeX, and 1-to-1 symbol coverage.
- [ ] **One Named Running Example:** A single concrete numerical/structural example with verified inputs, intermediate values, and outputs to reuse consistently across **Sections 3, 4, and 5**.
- [ ] **5–6 Distinct Transfer Q&As:** Five to six standalone analytical scenarios (mechanism, quantitative trace, parameter synthesis, boundary stress-test, cross-architecture trade-off) that test *new* transfer inputs rather than repeating the running example.
- [ ] **Gaps & Unverified Claims Log:** Explicit list of any conflicting claims, paywalled details, or missing empirical bounds discovered during Waves 2–3.
