# Shared Canonical Teaching Core

Single authoritative pedagogical contract shared across substantive Scriptorium notes (`M1`, `M2`, `M4`, `M5`, `M7`). Keep prose **topic-independent**, **self-contained**, and written like a dedicated instructor preparing a domain textbook for a first-time learner—never chatbot dialogue, never formula dumps, and never mechanical heading checklists.

## 1. Progressive Understanding Principle & Layers (`A`–`H`)

**Core Rule:** Never introduce notation, formalism, or algorithms before the reader has enough context to understand what problem they solve.

1. **Layer A — Orientation:** Establish the problem, why earlier/simpler approaches fail, and what goal the concept achieves.
2. **Layer B — Intuition:** Build a simple concrete mental model or familiar scenario first (disclose explicitly where any analogy stops holding).
3. **Layer C — Foundation Bridge & Components:** Define unfamiliar terms, units, and required prerequisites right before use; never leave the reader guessing basic vocabulary.
4. **Layer D — Mechanism Breakdown:** Walk step by step through what enters, transforms, interacts, and exits.
5. **Layer E — Formalization & Math Deconstruction (`M01`–`M14`):** Translate the mechanism into notation only after motivation is clear (`scriptorium/engines/mathematics.py`, `MATH-01`–`MATH-10`):
   - **M01 Purpose / M02 Pronunciation:** State why the equation exists and how it is read aloud naturally.
   - **M03 Symbol Inventory / M04 Types / M05 Dimensions:** Define every symbol, subscript, superscript, transpose, operator, mathematical object type, and operand shape compatibility (e.g., `(1×3)(3×1) = (1×1)` scalar vs. `(3×1)(3×1)` mismatch).
   - **M06 Operations / M07 Expanded Form:** Expand compact dot products, matrices, and summations into elementary terms and state evaluation order.
   - **M08 Substitution / M09 Arithmetic / M10 Interpretation / M11 Sanity Check:** Plug declared synthetic numbers in, show intermediate arithmetic, interpret the output in real units/meaning, and check bounds, signs, or dimensions.
   - **M12 Misconceptions / M13 Generalization / M14 Advanced Details:** Place trap prevention beside the step where errors happen, then generalize and state deeper assumptions cleanly. *(Adapt detail to expression complexity and learner level; never bloat simple definitions.)*
6. **Layer F — Complete Worked Application (`Step 1`–`Step 12`):** For numerical problems, progress through: Question & Objective -> Method & Assumptions -> Symbols & Formula -> Substituted Inputs -> Intermediate Operations -> Result -> Contextual Interpretation -> Sanity Verification -> Common Mistakes -> Generalization.
7. **Layer G — Analysis, Causal Comparisons & Boundaries:** Explain *why* alternatives differ causally in scenario prose **before** summarizing in comparison tables. Always state applicability assumptions and explicit **Use when / When not to use** limits.
8. **Layer H — Visual Reading Integration & Reinforcement:** Embed local web-acquired figures (`assets/scriptorium/<slug>/`) with `Explain -> Show -> Decode -> Connect` answering: what it represents, where to start reading, what key labels/arrows/curves show, and what conclusion connects to the next concept. End assessments with reasoning-rich solutions and natural forward transitions.

## 2. Internal Semantic Composition Sequence (`A`–`N`)

Use this sequence to plan coherent continuous prose with natural domain headings (never dump stage letters or mechanical titles like `"Starting Intuition"` literally when smoother headings read better):
`A. Concept Orientation -> B. Starting Intuition -> C. Foundation Bridge -> D. Mechanism Breakdown -> E. Formal Representation -> F. Mathematical Deconstruction -> G. Complete Worked Example -> H. Visual Explanation -> I. Deeper Interpretation -> J. Comparisons and Selection -> K. Limitations and Misconceptions -> L. Practical Application -> M. Knowledge Check -> N. Transition`.

## 3. Quality Gate & Executable Verification

Notes must pass both structural integrity (`validate_published_composition`) and **12-dimension teaching-quality verification** (`QualityEngine.evaluate_teaching()`, `scriptorium/engines/quality.py`) plus the 8-question **Beginner Reader Simulation**—never averaging away critical technical, mathematical, prerequisite, or overcompression defects.
