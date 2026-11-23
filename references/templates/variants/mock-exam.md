# Variant: Mock Exam & Viva Preparation

- **Purpose:** Simulate progressive written exams or oral viva defenses with rubric-backed collapsed answer keys.
- **Parent Master:** [M6 — Practice & Assessment](../masters/assessment.md) (`mock_exam`)
- **Activation Trigger:** `"mock exam"`, `"viva"`, `"practice test"`, or interactive `/scribe-quiz`.
- **Inputs & Dependencies:** Target objectives/notes, difficulty mix, verified claims; [authoring_rules.md](../../../shared/authoring_rules.md), [math_gates.md](../../../shared/math_gates.md).
- **Execution Overrides:**
  1. Structure strictly in escalating progression: Section A (Core Definitions & Defense), Section B (Quantitative Derivation, Calculation, or State Trace), Section C (Boundary Critique & Oral Viva Follow-Ups).
  2. Isolate full worked solutions and grading rubrics inside collapsed callouts (`> [!tip]- Reveal approach and solution`) or a trailing Answer Key.
  3. Keep interaction boundaries honest: `/scribe-quiz` quizzes one question per turn in chat; static Markdown never pretends auto-grading.
- **Review:** Check that quantitative answers show the reasoning and that the note has no extra quiz-state YAML keys.
