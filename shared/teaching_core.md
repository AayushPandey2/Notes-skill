# Shared Canonical Teaching Core

## Purpose

Establish one domain-independent educational architecture shared across substantive Scriptorium outputs (`M1`, `M2`, `M4`, `M5`, `M7`, including source and `/scribe-ytnotes` video notes) so first-time learners understand *why* an idea exists before encountering formal symbols, code, or visuals.

## Activation Trigger & Scope

- **Activate on:** Every generated note routed to `M1`, `M2`, `M4`, `M5`, or `M7` (`T03`, `TEACH-01`–`TEACH-10`). Compact `M3` cheat sheets and question-only `M6` assessments follow their own density/self-test contracts while preserving symbol/condition accuracy.
- **Dependencies:** [shared/math_gates.md](math_gates.md) (`M01`–`M14`, `Step 1`–`12`, formula folds), [shared/authoring_rules.md](authoring_rules.md) (YAML, rendering, evidence, cohesion), [representations.md](../references/workflows/notes-creation/representations.md) (`BVIA`/`LAVIA`).

## Execution Sequence — Progressive Understanding Layers (`A`–`H`)

Write continuous, domain-natural prose advancing one conceptual move per paragraph—never dump bare `$$...$$` formulas, repeat H1 chapter titles as H2 headings, dump figures after code, or expose internal step labels as section headings:

1. **Layer A — Orientation:** State the concrete problem, why naive/earlier methods break, and what capability the concept delivers.
2. **Layer B — Intuition:** Build an accessible mental model from familiar experience before introducing formalism; state where any analogy stops holding (`CF-08`).
3. **Layer C — Foundation Bridge & Components:** Define unfamiliar terms, units, and required prerequisites immediately before first use rather than deferring to vague pointers.
4. **Layer D — Mechanism Breakdown:** Walk chronologically/causally through inputs, transformations, interactions, and outputs.
5. **Layer E — Formalism & Folded Walkthrough (`shared/math_gates.md`):** Introduce notation only after intuition is ready; pair every displayed `$$...$$` equation with an immediately following `> [!example]- Understand this formula step by step` callout (`M01`–`M14`).
6. **Layer F — Complete Worked Application (`Step 1`–`12`):** Execute worked numerical/structural examples following [shared/math_gates.md](math_gates.md#worked-application-protocol-step-112).
7. **Layer G — Causal Comparisons & Boundaries:** Explain *why* alternatives differ causally in scenario prose **before** summary comparison tables; state applicability assumptions and explicit **Use when / When not to use** limits.
8. **Layer H — Visual & Video-Frame Integration:** Embed inspected local raster assets (`png`/`jpg`/`webp`; SVG synthesis retired) at the exact point of need using `Explain -> Show -> Decode -> Connect`.

## Output Semantic Spine (`A`–`N`)

Plan continuous sections along: `Orientation -> Intuition -> Foundation Bridge -> Mechanism -> Formalism + Fold -> Worked Example -> Visual Walkthrough -> Deeper Interpretation -> Causal Comparison -> Limitations & Misconceptions -> Application -> Knowledge Check -> Transition`.

## Failure Handling & Validation

- **Failure Handling:** Reject unprepared equation drops, undefined symbols, ungrounded analogies, or sparse summary-bullet overcompression compressing multiple distinct concepts; repair the smallest defective span rather than rewriting passing sections.
- **Validation:** Pass `QualityEngine.evaluate_teaching()` (12 teaching dimensions + Beginner Reader Simulation), `validate_formula_folds`, and `QualityEngine.review_explanatory_clarity()` (`CF-01`–`CF-12`).
