# Shared Canonical Teaching Core

## Purpose

Establish one domain-independent theory-authoring architecture across substantive Scriptorium outputs (`M1`, `M2`, `M4`, `M5`, `M7`, and video notes) so every note delivers a **complete, zero-prerequisite, self-contained learning experience** matching patient one-on-one mentoring. Compact `M3` cheat sheets and question-only `M6` assessments follow their own density contracts while preserving symbol accuracy and assumptions.

## Self-Containment & Prerequisite Rule

A reader starting with only basic foundational background must understand the note's entire argument without jumping to outside resources to decode terms, symbols, images, or derivations:
- **Essential foundations now:** include a dedicated local foundations section or inline bridge explaining every mathematical, scientific, or conceptual tool from scratch—with small concrete value tables and real-world intuition—*before* formulas rely on them.
- **Useful but secondary:** provide a brief local bridge and an optional wikilink.
- **Outside the learning objective:** state the boundary explicitly and link for further study.
A link must never replace an essential local explanation.

## Tone, Micro-Cadence & Readability

Write as a **patient, technically accurate one-on-one mentor**:
- **Short, crisp paragraphs (1–3 sentences):** Break dense theory into clean, single-idea paragraphs separated by whitespace, tables, and visual anchors. Never bury beginners under walls of prose or use `"obviously"`, `"trivially"`, `"simply"`, `"as you know"`, hype, or classroom framing.
- **Concrete example/table before abstract definition:** Open unfamiliar concepts with a tiny labeled table or everyday scenario (`inputs → intermediate → outcome`) first, then name and unpack the formal term beside it.
- **Question-driven navigation:** Start comprehensive guides with Goal/Prerequisites + a clean Table of Contents, and use numbered, question-driven headings (`## 3. Why can't we use <Simpler Method> here?`).
- **Connective tissue:** Link every transition using `Claim → reason → example → consequence`, `Before → operation → change → explanation → after`, or `Intuition → precise term → mechanism → application`. Never drop an equation, term, or visual without first stating what question it answers.

## Twelve Generalized Teaching Layers

Realize the applicable layers cleanly in the topic's natural sequence (adapting to the domain without forcing math/code onto unrelated subjects):
1. **Layer 1 — Context, Real-World Map & Naming Clarification:** Open with what the concept does, a tiny concrete table showing how outputs behave, a real-world applications table (`Case | Negative/Class 0 | Positive/Class 1` or domain equivalent), and clarify misleading terminology (e.g., why something is named after its math vs. its task).
2. **Layer 2 — Running Dataset/Case & Upfront Symbol Dictionary:** Show a tiny concrete multi-column example first, name inputs/targets beside it, provide a **complete upfront Symbol Dictionary** (`Symbol | Meaning`), and add a **notation-clash callout** wherever textbooks use the same symbol for different quantities.
3. **Layer 3 — Why Simpler Alternatives Fail:** Test the simpler baseline on concrete numbers that expose exact impossible or broken outputs, illustrate the contrast visually, and summarize in a comparison table (`Property | Simpler Baseline | Target Concept`).
4. **Layer 4 — Local Mathematical & Conceptual Foundations:** Teach every prerequisite tool needed later (constants, inverse functions, summations, derivatives/rates, units, or structural rules) using plain intuition, small reference value tables, plots, and governing identities before using them.
5. **Layer 5 — Progressive Model Construction (Simple → Multi-Component → Compact Form):** Present the end-to-end stage diagram first, then build systematically from **1-variable scalar case → multi-variable summation (with a step-by-step calculation table) → compact vector/matrix or general form**, explaining *why* transpose or compactness is introduced.
6. **Layer 6 — Component-by-Component Equation & Visual Dissection:** Break governing functions into individual sub-parts (`Part | Purpose`), inspect behavior across concrete **negative, zero, positive, and limiting cases** alongside paired curves/derivatives, and map every stage to the running example via [representations.md](../docs/procedures/authoring/representations.md).
7. **Layer 7 — First-Principles Origin & Mechanism Trace:** Derive *why* the rule or objective exists from first principles (or physical/causal mechanism), contrast it causally against naive objectives, note numerical/practical stability fixes, and trace `Starting state → operation → reason → intermediate change → outcome`.
8. **Layer 8 — Multi-Step Quantitative Hand Trace:** Initialize a tiny 3–4 row fixture and walk through **Iteration 1 → Parameter/State Update → Iteration 2** by hand (tables of intermediate terms included) so the learner sees quantities actually improve step by step.
9. **Layer 9 — Evaluation, Diagnostics & Calibration:** Define every relevant metric or test around **one shared numerical fixture**, explain *when* aggregate scores mislead (e.g., imbalance), and decode diagnostic curves/matrices visually.
10. **Layer 10 — Regularization, Assumptions & What Is NOT Required:** State constraints, failure regimes, and hyperparameters with concrete numerical penalties and solver/trade-off tables—plus an explicit **"What this method does NOT require"** section preventing common student myths.
11. **Layer 11 — Preprocessing, Variants & Common Mistakes:** Explain input preparation, leakage boundaries, major variants/extensions, real advantages/disadvantages, a `Mistake | Correct approach` table, and a multi-method selection comparison table.
12. **Layer 12 — Mental Model & Companion Cheatsheet/Interview Handoff:** Close comprehensive notes with a final numbered **N-Step Mental Model** summary and reciprocal links to the topic's companion lab and companion **Cheatsheet & Interview Q&A** file (which owns the grouped Formula/Rule Cheat Sheet, tiered **Beginner → Intermediate → Advanced** Q&A with tap-to-reveal `> [!tip]- Answer` folds, and **Worked Practice Problems** with `> [!tip]- Solution` folds). Keep collapsed callouts for long optional derivations in the main note while keeping the teaching argument clear in visible prose.
