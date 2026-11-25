# Shared Canonical Teaching Core

## Purpose

Establish one domain-independent theory-authoring architecture across substantive Scriptorium outputs (`M1`, `M2`, `M4`, `M5`, `M7`, and video notes) so every note delivers a **complete, zero-prerequisite, visually scannable learning experience**. Compact `M3` cheat sheets and question-only `M6` assessments follow their own density contracts while preserving symbol accuracy and assumptions.

## Self-Containment & Progressive Tiering

A reader starting with only basic foundational background must understand the note's entire argument without jumping to outside resources:
- **Essential foundations first:** Teach every prerequisite concept, mathematical tool, or base model (e.g., decision trees before gradient boosting; distance metrics before KNN) locally with small concrete examples *before* advanced formulas rely on them.
- **Tiered complexity (Fundamentals → Practical Understanding → Advanced Mechanisms):** Separate core intuition and basic prediction from practical tuning/leakage/evaluation, and clearly mark advanced mechanisms (e.g., spatial trees, high-dimensional geometry, systems optimization) as deeper material so beginners are not overwhelmed.
- **Useful but secondary / outside scope:** Provide a brief local bridge or explicit boundary with an optional wikilink—never substituting a link for an essential local explanation.

## Visual Identity, Spacing & Navigation

Break visual monotony so definitions, formulas, worked examples, warnings, and checkpoints each have a distinct visual identity:
- **Separated opening metadata & clickable TOC:** Place blank lines between `Difficulty`, `Prerequisites`, and `Learning objectives` blocks so renderers never merge them into one paragraph. Follow with a compact **clickable Obsidian Table of Contents** (`- [[#1. Heading|Short Label]]`).
- **One concept per block:** Keep paragraphs to 1–3 concise sentences (avoiding long 200+ character source lines that pack multiple properties, equations, and leakage warnings together). Separate multi-part definitions (e.g., instance-based vs. non-parametric vs. lazy learning, or standardization vs. effect vs. leakage) into distinct labeled blocks, and place blank lines between complex list items.
- **Consistent multi-level numbered `H1–H4` headings:** Use short, subject-first headings (`Prerequisites`, `<Topic> by Example`, `Mathematics of <Topic>`, `Worked Classification Example`, `Assumptions and Limitations`, `Algorithm Summary`) numbered consistently down to `H3`/`H4` (`## 5. Mathematics of ...` → `### 5.1 ...` → `#### 5.1.1 ...`). Never use bold text as pseudo-headings.
- **Purposeful callouts & clean emphasis (no highlighting):** Do **not** use `==highlight==`, semantic highlight spans, or colored formula segments anywhere in notes. Use purposeful callouts (`[!info]` definitions, `[!important]` core formulas/conditions, `[!example]` numerical calculations, `[!warning]` data leakage/mistakes) and selective bolding rather than highlighting. Reserve `---` horizontal rules for major thematic transitions (foundations → math → practical/advanced → revision), not every section boundary.
- **Visible Concept Checkpoints:** Keep checkpoint questions **always visible** inside `> [!question] Concept Checkpoint`, hiding only the answer inside a nested collapsed `> > [!success]- Reveal Answer` block—never collapse the outer question.

## Tone & Precision

Write calm, direct, technically precise reference prose:
- **No scripted filler or formal bloat:** Ban `"We now..."`, `"Let us..."`, `"Notice how..."`, `"Inspect Figure..."`, `"local tools"`, `"single-prototype summary"`, and `"dwarfs the entire range"`. State the takeaway directly.
- **No unedited self-corrections or unsupported absolutes:** Never leave `"Wait—check the sign carefully!"` or an incorrect table alongside a correction; teach pitfalls via a `[!warning]` or `Common mistake` callout beside the correct table. Qualify conditional claims accurately (distinguishing example defaults from library defaults, tie-breaking rules, data-dependent tree complexity, uncalibrated vote proportions, and leakage validity vs. direction).

## Conceptual Flow & Worked-Example Completeness

Follow **See it → Understand it → Derive it → Calculate it → Apply it**:
1. **Introduction & Core Characteristics:** Explain what the method does, where it applies, and its core properties in separate short blocks.
2. **Prerequisites & Base Concepts:** Teach essential building blocks locally.
3. **Early Visual Worked Example & Consistent Running Dataset:** Introduce one tiny concrete dataset early, **visualize it**, and trace a complete multi-stage example (`1. Compute → 2. Sort/Select → 3. Aggregate → 4. Result`) *before* heavy formalism, then carry that **exact same dataset** through derivations, visuals, and evaluation.
4. **Progressive Symbol Introduction & Full Objective Coverage:** Introduce symbols just in time (reserving the full **Notation Reference** for the end). Fulfill **every** declared learning objective with complete numerical calculations (e.g., if objectives cover both classification and regression, include complete worked calculations for both).
5. **Evaluation, Assumptions & Companion Handoff:** Cover scaling/leakage, assumptions, tiered concepts, inline **Concept Checkpoints**, **Algorithm Summary**, trailing **Notation Reference**, and reciprocal links to `<note stem> - Experimental Lab.md` and `<note stem> - Cheatsheet & Interview Q&A.md`.
