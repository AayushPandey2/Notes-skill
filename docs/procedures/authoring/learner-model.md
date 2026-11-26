# Learner Model & Adaptive Instruction

## Purpose

Adapt prerequisite support, worked-example density, and representation scaffolding to the learner's **topic-specific background**—without ever equating beginner-friendly with superficial. A learner may be intermediate in programming, foundational in linear algebra, and a beginner in probability; one global difficulty tag cannot capture this.

## 1. Internal Learner Profile (Never Fabricated)

Maintain an optional internal conceptual record using **only** background explicitly supplied by the learner or retained by user choice—unknown abilities must remain unknown (never invent quiz histories or publish internal profile YAML):
- `objective` (e.g., `technical_mastery`, `exam_prep`, `implementation`, `quick_lookup`)
- `prior_knowledge` (per-prerequisite or per-subdomain: `beginner`, `foundational`, `intermediate`, `advanced`, or `unknown`)
- `known_concepts` vs. `uncertain_prerequisites`
- `guidance_level` (`high`, `moderate`, `low`), `mathematical_rigor`, `practical_depth`

## 2. Independence of Depth and Prerequisite Support

- **Depth $\neq$ Difficulty:** A beginner can request **Level 4–5 analytical rigor**. Deliver the same intellectual depth by supplying smaller conceptual transitions, local essential prerequisite bridges ([teaching_core.md](../../../core/teaching_core.md)), and complete worked steps—never dumb down the mechanism.
- **Expertise-Reversal Discipline:** For learners with demonstrated or stated mastery (`advanced` / `known_concepts`), omit redundant elementary derivations and over-scaffolded arithmetic so explanations stay crisp and high-signal.
