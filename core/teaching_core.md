# Shared Canonical Teaching Core

## Purpose

Establish one domain-independent theory-authoring architecture across substantive Scriptorium outputs (`M1`, `M2`, `M4`, `M5`, `M7`, and video notes) so every note delivers a **complete, zero-prerequisite, self-contained learning experience**. Compact `M3` cheat sheets and question-only `M6` assessments follow their own density contracts while preserving symbol accuracy and assumptions.

## Self-Containment & Prerequisite Rule

A reader starting with only basic foundational background must understand the note's entire argument without jumping to outside resources:
- **Essential foundations first:** Teach every prerequisite concept, mathematical tool, or base model (e.g., decision trees before gradient boosting; derivatives before optimization) locally with small concrete examples *before* advanced formulas or variants rely on them.
- **Useful but secondary:** Provide a brief local bridge and an optional wikilink.
- **Outside the learning objective:** State the boundary explicitly and link for further study.
A link must never replace an essential local explanation.

## Tone, Spacing & Visual Hierarchy

Write in one consistent voice—calm, technically precise, explanatory, and approachable:
- **Separated opening metadata:** Place blank lines between `Difficulty`, `Prerequisites`, and `Learning objectives` blocks so Markdown renderers never merge them into a single paragraph, followed by a plain-text numbered Table of Contents (zero links).
- **One idea per paragraph (1–3 sentences):** Break dense prose into small conceptual blocks separated by whitespace, tables, formulas, and visuals. Never introduce five or six advanced mechanisms inside one introductory paragraph.
- **Breathing room in lists:** Never turn bullet points into miniature chapters; place blank lines between complex list items or promote substantial explanations into subsections.
- **Short, navigable `H1–H4` headings:** Use clear 2–5 word headings (`Example Dataset`, `Mathematical Foundations`, `Objective Function`, `Mathematical Derivation`, `Step-by-Step Training`, `Evaluation and Best Practices`) rather than academic paper titles. Maintain a consistent `H1–H4` hierarchy across all sections and never use bold text (`**Step 1A**`) as pseudo-headings.
- **Controlled bolding & natural prose:** Bold only key new terms or decisive takeaways, never every technical phrase. Ban commanding phrasing (`"Inspect Figure 4 carefully"`, `"Look at Figure 1"`), dramatic/exaggerated claims (`"Why Do Simpler Alternatives Fail?"` -> `"Limitations of ..."`), unsupported absolutes (`necessarily`, `always`, `dramatically lowers`, `prevents overfitting`, `dominant`), patronizing shortcuts (`"obviously"`, `"trivially"`, `"simply"`), and unedited self-correction transcripts (`"Wait—check the sign carefully!"`). Never retain a wrong table alongside a correction; teach pitfalls via a deliberate `Common mistake` callout beside the correct table.

## Conceptual Flow & Progressive Teaching Layers

Follow the natural learning progression **See it → Understand it → Derive it → Calculate it → Apply it** across the topic's sections:
1. **Introduction & Intuition:** Explain what the concept does in plain language, where it is used, and clarify any misleading name without premature jargon.
2. **Prerequisite Concepts & Base Models:** Build essential foundations locally (e.g., trees, loss functions, gradients, derivatives, regularization) before combining them.
3. **Early Intuitive Example & Consistent Running Dataset:** Introduce one tiny concrete dataset early and trace an intuitive example on it *before* full derivations, then carry that **exact same dataset** consistently through derivations, visuals, step-by-step calculations, and evaluation.
4. **Progressive Symbol Introduction (Notation Dictionary at the End):** Introduce symbols just in time as each concept enters (e.g., targets/predictions → base learner → gradients → curvature → regularization), flagging notation clashes inline. Place the complete **Notation / Symbol Dictionary** at the **end** of the note as a revision reference rather than dumping 15–20 symbols upfront.
5. **Progression from Simple to General:** Move from a concrete 1-variable or single-step case → multi-term sum → compact vector/matrix form, explaining *why* compactness is introduced.
6. **Complete Algorithmic & Domain Coverage:** When teaching selection algorithms (e.g., tree splits), compare candidate options in a table to show *why* the winning choice is selected; when claiming both regression and classification coverage, develop classification mechanics (logits, sigmoid, probabilities, gradients) explicitly rather than leaving them as regression-only examples.
7. **Inline Concept Checkpoints & Section Takeaways:** Place short 2–4 question **Concept Checkpoints** (with optional collapsed `> [!tip]- Answer` folds) and brief takeaways after major sections so learners can test understanding without reading 5,000+ words to revise.
8. **Closing Mental Model & Companion Handoff:** Close comprehensive notes with a concise numbered **Mental Model**, the trailing **Notation Reference**, and reciprocal links to `<note stem> - Experimental Lab.md` and `<note stem> - Cheatsheet & Interview Q&A.md` (which owns the full grouped Formula Cheat Sheet, tiered Q&A, and worked problem sets).
