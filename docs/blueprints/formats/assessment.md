# M6 — Practice, Active Recall & Diagnostic Assessment

*Master ID: `M6` (`assessment`, variants: `flashcards.md`, `mock-exam.md`). Artifact policy: `single_artifact` per [master-registry.yaml](../../dispatch/master-registry.yaml).*

- **Destination & Mode Contract:** Save inside `<Configured Target>/<Topic>/` when part of a topic bundle, or `Practice Sets/<Subtopic> - Practice.md` / `Practice Sets/<Topic> - Collection Assessment.md` only when explicitly requested as a standalone assessment ([properties-policy.md](../../properties/properties-policy.md)). Reuse verified equations and conditions from sibling notes. Static Markdown uses collapsed callouts (`self-test`) or visible keys (`practice with answers`); interactive `/scribe-quiz` asks **one question per turn** in chat without claiming static Markdown auto-grades.
- **Header Block:** Line-1 Standard Obsidian Properties YAML + `# <Topic or Subtopic> — Active Recall & Synthesis Practice Set` (no long theory summary).

## 1. Cognitive Skill Sampling & Dynamic Question Numbering

Sample across the ten mastery dimensions in [mastery-design.md](../../procedures/authoring/mastery-design.md) (*Recognition, Recall, Explanation, Execution, Prediction, Diagnosis, Discrimination, Construction, Critique, Transfer*) and integrate [revision-strategy.md](../../procedures/learning/revision-strategy.md) for spaced/interleaved practice sets rather than writing ten progressively longer definition prompts.

Scale question count dynamically (`10–14` narrow sets; `15–20` full sets) and **compute tier headings dynamically** to match actual counts (never hardcode mismatched `Q1–Q5 / Q6–Q12 / Q13–Q18` ranges):
- `## Tier 1 — Foundational Recall & Recognition (Q1–Q<n1>)`
- `## Tier 2 — Application, Calculation & Mechanism Tracing (Q<n1+1>–Q<n2>)`
- `## Tier 3 — Boundary Stress-Tests, Diagnosis & Transfer (Q<n2+1>–Q<N>)`

## 2. Answer Expectations & Misconception Diagnostics

| Question Type | Required Answer Quality |
|---|---|
| **Definition** | Precise statement + exact boundary conditions |
| **Calculation** | Governing method + intermediate steps + units + final result |
| **Explanation** | Causal or logical mechanism (not bare symptom listing) |
| **Diagnosis** | Identified failure mechanism + discriminating evidence |
| **Proof** | Explicit hypotheses + justified logical transitions |
| **Design** | Requirements satisfied + trade-offs + justified choice |

- **Misconception-Sensitive MCQs:** Map each wrong option to a specific plausible misconception ([subject-theory-profiles.md](../components/subject-theory-profiles.md)).
- **Interactive `/scribe-quiz` sessions:** Follow [skills/scribe-quiz/SKILL.md](../../../skills/scribe-quiz/SKILL.md) exclusively for live one-question-at-a-time oral/interactive quizzing, read-only vault discipline, and adaptive diagnostic grading rather than generating a static `M6` file.
- **Self-test reveal:** Put the solution in a collapsed answer callout. Add a separate hint when it helps the learner progress without revealing the method. Keep the callouts separate and quote each interior line with `>`. Follow the selected preset for flashcards and mock exams.

````markdown
### Q<k>. <Specific Prompt>

> [!hint]- Need a nudge?
> <Governing principle or setup constraint without spoiling the result.>

> [!success]- Approach and Solution
> **Core intuition:** <One-sentence causal explanation.>
>
> 1. **Setup & Assumptions:** <Hypotheses, units, shapes, or boundaries.>
> 2. **Step-by-Step Working:** <Explicit calculation, trace, or argument.>
>
> **Final answer:** <Verified conclusion with qualifiers.>
>
> **Common trap:** <Typical misstep -> why it fails.>
````

*Contract: [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), [verification-checklist.md](../../procedures/review/verification-checklist.md).*
