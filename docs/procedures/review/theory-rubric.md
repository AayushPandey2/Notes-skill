# Canonical Theory Quality Rubric (`M1` & Comprehensive Theory)

*Single canonical authority for the 10-dimension `M1` theory quality rubric, accessible to both Stage 5 runtime self-review ([verification-checklist.md](verification-checklist.md)) and independent benchmark evaluation ([benchmark-protocol.md](../../../evaluations/benchmark-protocol.md) and [rubrics/theory.md](../../../evaluations/rubrics/theory.md)). Apply criteria proportionally to the intended artifact (`M1`/`M2` theory vs. strict-source note) rather than penalizing material intentionally omitted by `artifact_plan` or `source_policy`.*

## 1. Evidence & Scoring Scale

Every criterion requires **citing concrete output passages**. Author self-attestation (e.g., *"I verified this checklist"*) never counts as passing evidence.

- **Rating scale (`0–5` per applicable dimension):** `0` *missing or fundamentally wrong* · `1` *seriously deficient* · `2` *partially adequate* · `3` *competent* · `4` *strong* · `5` *exceptional*.
- **Proportional normalization:** Exclude genuinely inapplicable dimensions (such as mathematical derivations in pure history) and normalize remaining weights proportionally—never declare visual teaching inapplicable on a visually rich topic without documented retrieval-failure justification.
- **Passing threshold (`M1`):** Weighted score **`>= 85/100`** and **`>= 4/5` in applicable essential dimensions**, with **zero unresolved Critical defects**. Classify applicability before grading using objective scope (never by weight alone):
  - *Universally essential (`>= 4/5`):* `Beginner Accessibility`, `Self-Contained Knowledge`, `Theory Completeness`, `Factual Accuracy`, `Conceptual Reasoning`.
  - *Objective-dependent essential (`>= 4/5` when applicable; mark inapplicable when outside topic/source bounds):* `Mathematical Teaching` (consequential math/derivations), `Examples & Independent Application` (worked traces or independent problem solving), `Visual Teaching` (visually rich & asset-permitted).
  - *Supporting (contribute to the `>= 85/100` aggregate and remain subject to Critical Defect Overrides, without a separate numeric floor):* `Writing Tone & Continuity`, `Formatting & Reading Experience`.

## 2. Author Self-Review vs. Independent Evaluation

- **Author Self-Review (Stage 5 runtime check):** Check generated passages against every applicable dimension below before saving and honestly disclose when no independent reviewer context evaluated the work.
- **Independent Benchmark Evaluation (`evaluations/`):** Use anonymized candidate outputs in a separate reviewer context without author self-attestation, grading strictly from observed passages ([benchmark-protocol.md](../../../evaluations/benchmark-protocol.md)).

## 3. Ten Weighted Dimensions & Mandatory Integrity Overrides

| Dimension (M1 Weight) | Pass Standard (Cite Supporting Passage) | Critical Defect / Override Trigger |
|---|---|---|
| **Beginner Accessibility (`15%`)** | Opens with plain-language intuition, concrete scenario, and simpler baseline before dense formalism; paces complexity without confounding simpler words with accessibility | Opens with jargon-heavy reference summary assuming unintroduced prerequisites or invokes untaught tools/methods (e.g., analogy-to-formalism cliff or unexplained composite operators) |
| **Self-Contained Knowledge (`10%`)** | Teaches essential terminology, symbols, central mechanisms, core math ops, assumptions, derivations, and limits locally within declared scope without external-note dependence | Relies on external links or bare `Prerequisites:` lists to supply essential unmastered knowledge |
| **Theory Completeness (`15%`)** | Core concepts reach target depth (`Level 3–5`); comprehensive `M1` covers foundations/baselines, mechanism, key task types/variants, practical config, limitations, comparisons, and primary references | `M1` note degenerates into a narrow formula summary omitting central pillars, leaves core mechanisms at `Level 1–2`, or compresses late sections |
| **Factual Accuracy (`10%`)** | Definitions, theorems, equations, library behaviors, version caveats, and misconceptions match authoritative subject truth | Any Critical factual error, wrong sign/operator, library-variant conflation, or unqualified overclaim (including empirical tendencies stated as monotonic guarantees) |
| **Mathematical Teaching (`15%`)** | Motivates formulas before introducing them, climbs the abstraction ladder cleanly, explains equation anatomy/operations, keeps milestones/assumptions visible with folds closed, completes derivations | Formula dumping, skipped derivation/algebraic jumps, dimension/normalization/bound/tie-policy error, stipulated definition treated as theorem, or fold-only essential reasoning |
| **Conceptual Reasoning (`10%`)** | Establishes need, causal mechanism (*how* and *why*), conceptual discrimination, state carryover, and interpretation independently of bare equations | Technically correct definition or topic mention substitutes for causal explanation or confuses commonly conflated terms |
| **Visual Teaching (`8%`)** | Distributes multiple specialized, verified existing web-sourced (or supplied) images across relevant sections when permitted with attribution and adjacent before/image/caption/after narrative, or documents search refinement + honest prose/table fallback without ever generating images | Any AI/native-generated image, programmatic plot, custom SVG, redrawn art, Mermaid/ASCII, 0–1 token visual on a visually rich topic without disclosed retrieval failure, disconnected gallery, or fabricated/placeholder embed |
| **Examples & Independent Application (`7%`)** | Progressive/continuous worked traces (multi-round + unseen inference where iterative, fading scaffolding where warranted) and prediction/diagnosis/transfer checks | Single-round incomplete trace, trivial numeric substitution, or exercises requiring untaught knowledge |
| **Writing Tone & Continuity (`5%`)** | University-textbook prose with natural pauses, chapter continuity, and clear causal transitions | Compressed research-paper shorthand, multi-step dense sentences, robotic meta-headings, internal-template leakage, or disconnected sections |
| **Formatting & Reading Experience (`5%`)** | Native Obsidian H1–H4 headings, semantic callouts (`[!info]`..`[!abstract]-`), 3 progressive disclosure layers, spacing, and compact tables cleanly applied | Broken callouts/tables, oversized collapsed blocks, wide formula-stuffed cells, fragmented prose, or hidden essential reasoning |
| **Mandatory Integrity Conditions *(Non-overrideable)*** | Honors active `source_policy` permissions, safety boundaries, non-execution rules, domain neutrality (no leaked ML boilerplate in non-ML topics), and epistemic distinctions | Critical correctness, safety, source-integrity, authorization, or essential-prerequisite defects; fabricated assets/citations; or script generation — **fails acceptance regardless of numerical score** |
