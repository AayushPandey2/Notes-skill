# Scriptorium Research Protocol (Waves 0–4)

Governs Phase 1 synthesis before writing any `.md` note.

## §0. Wave Routing
- **`/scribe-notes`:** Wave 0 $\to$ 1 $\to$ 2 $\to$ 3 $\to$ 4 (full subtopic tree).
- **`/scribe-expand`:** Wave 0 (gap audit) $\to$ Waves 1–4 for missing/expansion nodes only.
- **`/scribe-distill`:** Wave 0 + `--extract` from vault notes only (skip Waves 2–3 unless `[UNVERIFIED]` gaps exist).

## §1. Source Discipline (Non-Negotiable)
- **Chase to origin:** Cite primary sources (foundational papers, textbooks, RFCs, official docs, source repos) for definitions, proofs, and equations—never secondary blogs/listicles/AI summaries.
- **Practitioner wisdom:** Use post-mortems, maintainer talks, benchmarks, and vetted issues for traps, numerical instability, and failure modes.
- **Gaps & conflicts:** Tag conflicting definitions, paywalled details, or uncertain attributions `[UNVERIFIED]` inline and log in the dossier—never fabricate citations.

## §2. Four-Wave Pipeline

### Wave 0 — Vault Reconnaissance (Zero-Token Index)
1. Run `vault_index.py "<vault_path>" --discover --topic "<topic>"` (or `--fields file,title,aliases,depends_on,next_topic,status`) instead of reading full notes.
2. **Branch:**
   - `/scribe-notes`: exclude verified subtopics; link as prerequisites.
   - `/scribe-expand`: fill missing core subtopics first; if core is complete, propose 3–5 high-leverage expansions (proofs, edge-case pathology, optimizations, generalizations).
   - `/scribe-distill`: extract equations, symbols, and traps via `--extract` without web search unless a core formula is missing.

### Wave 1 — Exhaustive Five-Layer DAG Scoping & Notation Lock
Evaluate all five layers within the requested scope; do not invent a proof, variant,
history or independent note when it does not apply. Complete broad coverage while
keeping cohesive mechanisms together. The selected route governs each note's form.
1. **Five-Layer Curriculum Completeness Mandate:** Before writing any note, decompose `<topic>` into a **complete, end-to-end acyclic DAG** (`topic-01` ... `topic-NN`, sized to requested scope: typically 8-15 for a standard topic or 12-20+ for a broad pillar domain; a narrow cohesive mechanism may need one note) covering all 5 mastery strata:
   - **Layer 1 — Foundations & Axioms:** Historical bottleneck, core mathematical/logical primitives, representations, baseline models.
   - **Layer 2 — Core Mechanisms & Algorithms:** Forward/inference mechanics, decision boundaries, learning/update rules, exact algorithms.
   - **Layer 3 — Formal Theory & Proofs:** Convergence theorems, existence/uniqueness proofs, complexity bounds, optimality conditions.
   - **Layer 4 — Variants, Generalizations & Extensions:** Multi-class, non-linear, regularized, kernelized, dual, or architectural extensions.
   - **Layer 5 — Pathology, Failure Regimes & Practitioner Edge Cases:** Divergence/non-separability cases, numerical instability, sensitivity traps, engineering trade-offs.
2. **Pre-Execution Coverage Audit & Syllabus Lock (Before Leaving Wave 1):**
   - Lock the complete numbered manifest (`01` through `NN`) with exact filenames, `depends_on`, and `next_topic` edges.
   - Self-check: *"If a learner masters ONLY these `NN` subtopics, would any foundational theorem, standard algorithm, major variant, or classic failure mode still be missing?"* If **yes**, add those missing nodes **immediately in Wave 1**—never defer them to future `/scribe-expand` runs.
   - **Write `00-MOC-<topic-slug>.md` FIRST (`references/syllabus_template.md` / `scaffold_note.py --syllabus`):** Set `scope_locked: true`, populate `allowed_subtopics` (the exact allowlist) and `excluded_adjacent_topics` (at least 3–5 tempting tangents/prerequisites that must NOT become files), and draw the detailed 5-layer Mermaid learning-flow graph.
   - **Tangential Concept Rule:** Never create a note outside `allowed_subtopics`. If a tangent arises during Phase 2, link it if it exists in the vault or give a 2-sentence inline recap as plain text.
   - **`/scribe-expand` Parity:** Apply this same Five-Layer Coverage Audit against `vault_index.py` output; update `allowed_subtopics` in `00-MOC-<topic-slug>.md` *first* for all missing nodes across Layers 1–5, then generate every missing subtopic in that single run.
3. **Route and notation lock:** Resolve each note via routing.md before expensive retrieval. Lock notation only for mathematical modules; use consistent terms and interfaces for level 0. Keep one cohesive mechanism together and select API-Table for parameter-dense lookup.

### Wave 2 — Primary Knowledge Retrieval
For each subtopic, retrieve from primary sources only:
1. Formal problem, I/O, and invariant type (*definition*, *theorem*, *assumption*, or *heuristic*).
2. Verified historical lineage (discovery vs. formalization vs. popularization, author/year/venue).
3. Math gate: level 0 uses logic/evidence; level 1 adds symbols/formula/worked use; level 2 adds a justified derivation with domain guards, equivalence versus implication and shape/unit checks.
4. Complexity contract (time/auxiliary space with input-size variable defined) and the selected domain/language reference logic where implementation matters.

### Wave 3 — Practitioner Wisdom & Stress-Testing
1. **Contrastive lookalike:** Closest confused concept + exact differences in mechanism, parameters, invariant, and failure mode.
2. **Applicable boundary regimes only:** Zero/null ($\to 0$/empty), unit/normalized ($\to \pm 1$), degenerate/tie (boundary equality, rank deficiency, zero denominator), asymptotic ($\to \pm\infty$).
3. **Sharp edges:** Overflow/underflow, violated assumptions, hyperparameter sensitivities for Limitations and transfer Q&A.

### Wave 4 — Pre-Writing Subtopic Dossier
Lock per subtopic before drafting:
- [ ] Identity, filenames, `aliases`, `depends_on`, `next_topic`, verified primary URLs.
- [ ] For math levels 1/2: balanced LaTeX and full symbol coverage; omit ornamental math at level 0.
- [ ] **One** named running example reused consistently across mechanism, Details and verification.
- [ ] Deep routes: 5-7 standalone transfer Q&As (mechanism, trace, synthesis, boundary, trade-off) using *new* inputs.
- [ ] Explicit `[UNVERIFIED]` / gap log.
