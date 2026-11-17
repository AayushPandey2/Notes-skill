# Scriptorium Research Protocol (Phase 1 SOP)

Executes in Phase 1 of `/scribe-notes` and `/scribe-expand` **before** writing any final `.md` note. Outputs an internal vault inventory, an acyclic subtopic DAG, and a complete per-subtopic research dossier.

---

## Step 1 — Vault Discovery & Zero-Duplication

1. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>"` (or `--topic "<topic>"` for `/scribe-expand`) to inspect existing filenames, `id`, `title`, `aliases`, `topic`, `master_topic`, `depends_on`, `next_topic`, and `##` headings.
2. Inspect full note bodies **only** when headings/metadata leave concept coverage ambiguous.
3. Classify concepts into **Covered** (reuse/reference; never duplicate under synonyms), **Partial** (extend only in `/scribe-expand`), **Uncovered** (new DAG nodes), and **Out of Scope**.

**Gate:** Explicit scope map exists before Step 2.

---

## Step 2 — First-Principles DAG Decomposition

Decompose uncovered concepts into atomic learning units ordered logically where applicable:
1. Terminology & definitions → 2. Assumptions & prerequisites → 3. Core mechanisms → 4. Governing equations → 5. Step-by-step derivations → 6. Algorithms & code → 7. Advanced variants → 8. Limitations & failure modes → 9. Applications & connections.

Assign sequential planning IDs (`topic-01`, `topic-02`, ...) with `{subtopic_id, title, objective, depends_on, next_topic}`.
- Verify zero cycles, zero missing prerequisites, and zero duplicate subtopics.
- Keep uncreated future topics as plain text until their `.md` target exists or is created in the same batch.

**Gate:** Acyclic DAG with defined prerequisites and learning objectives before Step 3.

---

## Step 3 — Primary-Source Research & Citation Integrity

Source hierarchy:
- **Tier 1:** Peer-reviewed foundational papers, original publications, canonical textbooks, published proofs/specifications.
- **Tier 2:** Official API/language documentation, formal standards/RFCs, institutional publications.
- **Tier 3:** University lecture notes, reputable course materials, recognized specialist texts.
- *(Generic blogs, SEO articles, and AI summaries are discovery-only; verify all substantive claims against Tier 1–3.)*

Record internally for every cited source: `{source_title, author, publication, publication_date, source_type, url, claims_supported}`.

**Zero-Fabrication Rule:** Never invent or approximate URLs, DOIs, authors, dates, theorem/page numbers, benchmarks, or claims. Mark unverifiable details `[UNVERIFIED]`; omit unsupported claims unless essential, in which case disclose uncertainty explicitly. Distinguish facts, deductions, interpretations, and assumptions.

For every governing equation, verify original form, applicability conditions, symbol definitions/domains, dimensional consistency, sign conventions, boundary conditions, and algebraic equivalence.

**Gate:** Every claim and equation is source-traceable or labeled as assumption/derivation/`[UNVERIFIED]`.

---

## Step 4 — Pre-Writing 7-Part Research Dossier

Complete A–G internally for each subtopic (or justify non-applicability explicitly):
- **A. Conceptual Foundation:** Definition, intuition, purpose, prerequisites, assumptions, interpretation, and relation to prior topics.
- **B. Governing Equations:** Canonical form, symbol definitions/domains/shapes/units, sign conventions, assumptions, special cases, boundary conditions.
- **C. One Named Running Example:** One concrete, explicitly named example with exact values reused consistently across Sections 3, 4, and 5; explain any modification mathematically.
- **D. Complete Derivation:** Starting assumptions, governing equations, every nontrivial algebraic/logical step, substitutions, theorems/identities, division/domain conditions, and final verification.
- **E. Edge Cases & Failure Modes:** Boundary/degenerate inputs, undefined regimes, violated assumptions, implementation traps.
- **F. Is vs. Is Not Comparison:** At least one lookalike concept compared on similarities, exact differences, assumptions, math form, and confusion hazards.
- **G. Analytical Q&A Scenarios:** 5–6 distinct transfer scenarios (unfamiliar inputs, changed assumptions, reverse reasoning, boundary stress tests, error diagnosis, cross-concept comparison) with full solutions—do not reuse the running example as the central question in every scenario.

---

## Step 5 — Pre-Draft Consistency Review

Confirm before drafting: zero vault duplication, source-verified definitions/equations, consistent symbol definitions, complete running example, valid zero-skip derivation, accurate edge cases & Is vs. Is Not table, 5–6 distinct solved Q&As, acyclic DAG dependencies, and exact fit to `references/note_templates.md`.
