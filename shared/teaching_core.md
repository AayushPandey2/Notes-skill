# Shared Canonical Teaching Core

Single authoritative pedagogical contract shared across substantive Scriptorium notes (`M1`, `M2`, `M4`, `M5`, `M7`) including topic notes, source notes, and video notes (`/scribe-ytnotes`, `/scribe-ytlecture`). Keep prose **topic-independent**, **self-contained**, and written like a dedicated instructor preparing a domain textbook for a first-time learner—never formula dumps, duplicated H1/H2 chapter headers, post-code diagram dumps, or mechanical heading checklists.

## 1. Progressive Understanding Principle & Layers (`A`–`H`)

**Core Rule:** Never introduce notation, formalism, or algorithms before the reader has enough context to understand what problem they solve. Develop one conceptual move per paragraph, explain prose reasoning before compact summary tables, and distinguish derivation, prediction, inference, optimization, and code execution.

1. **Layer A — Orientation:** Establish the concrete problem, why earlier/simpler approaches fail, and what goal the concept achieves.
2. **Layer B — Intuition:** Build a simple concrete mental model or familiar scenario first (disclose explicitly where any analogy stops holding).
3. **Layer C — Foundation Bridge & Components:** Define unfamiliar terms, units, and required prerequisites right before use; provide inline refreshers or exact links rather than `"See linear algebra"`.
4. **Layer D — Mechanism Breakdown:** Walk step by step through what enters, transforms, interacts, and exits.
5. **Layer E — Mandatory Atomic Formula + Folded Walkthrough Contract (`M01`–`M14`):** Render every displayed `$$...$$` equation together with its immediately following Obsidian-native collapsed explanation (`render_formula_component`, `validate_formula_folds`, `scriptorium/engines/mathematics.py`):
   - **Placement:** Every displayed formula across main prose, worked examples, assessments, appendices, display tables, and video/source notes MUST own a `> [!example]- Understand this formula step by step` callout immediately below it while keeping preceding prose readable with folds closed.
   - **Content (`10` adaptive elements):** Answer (1) Purpose, (2) Plain-language reading aloud, (3) All symbols/indices/operators, (4) Object types/shapes/units, (5) Operations, (6) Evaluation order, (7) Non-obvious derivation reasoning & assumptions, (8) Meaningful concrete numerical example + interpretation (no generic `"substitute the values"` / `"this computes the result"` filler), (9) Conditions/edge cases, (10) Misconceptions.
   - **Anti-Recursive Nesting:** Keep supporting arithmetic inside a formula fold inline (`$...$`); if a derivation step needs its own display block, emit a sibling formula+fold component rather than nesting callouts recursively or bundling unrelated formulas into one `$$...$$` block.
6. **Layer F — Complete Worked Application (`Step 1`–`Step 12`):** Progress cleanly through: Question & Objective → Method & Assumptions → Formula + Fold → Substituted Inputs → Intermediate Operations → Result → Interpretation → Sanity Check → Common Mistakes → Generalization (retaining folded assessments separately from inline formula folds).
7. **Layer G — Analysis, Causal Comparisons & Boundaries:** Explain *why* alternatives differ causally in scenario prose **before** summarizing in comparison tables. Always state applicability assumptions and explicit **Use when / When not to use** limits.
8. **Layer H — Raster Visual & Video-Frame Reading Integration:** Use verified local downloaded raster images (`png`/`jpg`/`webp` — SVGs rejected on new acquisitions) and verified local video frames placed where the reader first needs the visual (never dumped after code). Wrap each visual with `Explain -> Show -> Decode -> Connect`.

## 2. Internal Semantic Composition Sequence (`A`–`N`)

Use this sequence to plan coherent continuous prose with single clean H1 chapter titles (never repeat H1 as H2):
`A. Concept Orientation -> B. Starting Intuition -> C. Foundation Bridge -> D. Mechanism Breakdown -> E. Formal Representation + Fold -> F. Complete Worked Example -> G. Visual / Frame Walkthrough -> H. Deeper Interpretation -> I. Comparisons and Selection -> J. Limitations and Misconceptions -> K. Practical Application -> L. Knowledge Check -> M. Transition`.

## 3. Quality Gate & Executable Verification

Notes must pass both structural integrity (`validate_formula_folds`, `validate_published_composition`) and **12-dimension teaching-quality verification** (`QualityEngine.evaluate_teaching()`, `scriptorium/engines/quality.py`) plus the 8-question **Beginner Reader Simulation**—never averaging away missing formula folds, duplicate headings, misplaced figures, prerequisite gaps, or overcompression.
