<!-- scaffold:preflight
Purpose: Generate pure active-recall problem sets, flashcards, or exam simulations grounded in vault evidence without duplicating theory summaries.
Master ID: M6 (assessment / compatibility route: practice).
Activation Trigger: /scribe-notes practice/assessment requests, /scribe-quiz (interactive single-question vault mode), "quiz me", "make flashcards", "mock exam", "viva questions".
Non-activation: Never run as an unsolicited pre-generation diagnostic quiz; an M6 route never triggers another M6 route.
Inputs: Verified sibling notes or source equations/definitions, target scope (narrow vs collection), interaction mode (self-test collapsed vs quiz interactive).
Dependencies: router.md, core/authoring_rules.md, core/math_gates.md; variants flashcards.md, mock-exam.md.
Decision Rules: 15–20 tiered questions for full sets (10–14 narrow); keep hints and solutions in separate collapsed callouts separated by an unquoted blank line.
Failure Handling: Reject answer-only quantitative keys without worked steps or trivial copy-paste recall; mark static Markdown limits honestly.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md) (`M6` assessment rules).
-->

# M6 — Practice, Active Recall & Diagnostic Assessment

- **Destination & Mode Contract:** Save inside `<Configured Target>/<Topic>/` when part of a topic bundle, or to `Practice Sets/<Subtopic> - Practice.md` / `Practice Sets/<Topic> - Collection Assessment.md` only when explicitly requested as a standalone assessment ([properties-policy.md](../../properties/properties-policy.md)). Exempt from 3-file companion generation unless explicitly requested. Reuse verified equations and conditions from sibling notes. Static Markdown uses collapsed callouts (`self-test`) or visible keys (`practice with answers`); interactive `/scribe-quiz` asks one question per turn in chat without claiming Markdown auto-grades.
- **Header Block:** Line-1 Obsidian Properties + `# <Topic or Subtopic> — Active Recall & Synthesis Practice Set` (no long theory summary or symbol preview).

## Tier 1 — Foundational Recall (Q1–Q5)

Consecutive prompts testing essential definitions, recognition cues, and applicability distinctions (`10–14` total for narrow sets; `15–20` full sets).

## Tier 2 — Quantitative Application, Code Tracing & Math (Q6–Q12)

Adapt strictly to the subject and objectives (quantitative calculation, state tracing, or causal mechanism analysis).

## Tier 3 — Boundary Stress-Tests & Cross-Topic Synthesis (Q13–Q18)

Novel transfer scenarios, edge conditions, and misconception-targeting distractors.

- **Mandatory Dual-Callout Format (Self-Test Mode):** Quote every line inside each callout (including interior blank lines with `>`) and keep an unquoted blank line between hint and solution so expanding a hint never reveals the answer:

````markdown
### Q<k>. <Specific Recall, Quantitative, or Transfer Question>

> [!hint]- Need a nudge?
> <State the governing principle, setup constraint, or first structural step without spoiling the result.>

> [!tip]- Reveal approach and solution
> **Core intuition:** <One-sentence causal explanation of why the mechanism behaves this way.>
>
> 1. **Setup & Assumptions:** <Confirm hypotheses, units, shapes, or boundary conditions.>
> 2. **Step-by-Step Working:** <Explicit intermediate substitution, computation, or causal derivation.>
>
> **Final answer:** <Verified result with units/scope qualifiers.>
>
> **Common trap:** <Typical misstep -> why it fails.>
````

<!-- optional: diagnosis -->
## [OPTIONAL] What would distinguish these failure causes? (Diagnostic Transfer)

<!-- Activate only when sibling notes expose competing plausible failure causes; omit cleanly otherwise. -->

- **Context:** Ambiguous symptom and competing hypotheses.
- **Analysis:** Discriminating observation or check separating true cause, linked back to canonical note sections.
- **Check:** Expected vs. refuting signal and remaining blind spots.

- **Output & Verification Contract:** See [authoring_rules.md](../../../core/authoring_rules.md) and [math_gates.md](../../../core/math_gates.md). Strip scaffolding comments and verify step-by-step derivations inside all quantitative solutions.
