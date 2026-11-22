<!-- scaffold:preflight
Master ID: M6 (assessment / compatibility route: practice).
Primary intent: knowledge_assessment — active recall, progressive problem sets, flashcards, mock exams, viva preparation, and diagnostic self-testing.
Activation signals: /scribe-notes practice/assessment requests, /scribe-quiz (existing-note interactive quiz), "quiz me", "test my understanding", "make flashcards", "mock exam", "viva questions", "practice exercises".
Variants: flashcards.md, mock-exam.md.
Pre-Flight: [router](../../../router.md) and [authoring rules](../../../shared/authoring_rules.md).
Strip this block before emission.
-->

# M6 — Practice, Active Recall & Diagnostic Assessment

- **Routing & Destination Rules**:
    - Invoked internally through `/scribe-notes` (including F13 collection-wide assessment blueprints) or interactively over existing notes via `/scribe-quiz`. Manual practice sets save to `Practice Sets/<Subtopic> - Practice.md`; collection-wide sets save to `Practice Sets/<Topic> - Collection Assessment.md` or `Practice Sets/<Topic> - Practice Test.md`.
    - Reuse retrieved evidence, equations, and invariants from sibling notes. An `M6` (`practice`) route must **never** trigger another `practice` route, and must **never** run as a compulsory pre-generation diagnostic quiz.
    - Support interaction modes honestly: static Markdown uses collapsed callouts (`self-test`) or visible answers (`practice with answers`); interactive `/scribe-quiz` runs one question per turn in chat without pretending static Markdown is interactive.
- **Header Block**: 5-key YAML frontmatter + `# <Topic or Subtopic> — Active Recall & Synthesis Practice Set`. Do **not** include study-note theory summaries, symbol tables, or equation previews—deliver pure tiered questions (`15–20` questions total; `10–14` for narrow single-subtopic sets).

## Tier 1 — Foundational Recall (Q1–Q5)

<!--
KEEP recall tasks about essential definitions, recognition cues, and conceptual distinctions. Supply distinct hints and answers. Remove before publication.
-->

## Tier 2 — Quantitative Application, Code Tracing & Math (Q6–Q12)

<!--
ADAPT to the actual subject. Use quantitative or code tracing only where the source and learning objectives support it. Remove before publication.
-->

## Tier 3 — Boundary Stress-Tests & Cross-Topic Synthesis (Q13–Q18)

<!--
KEEP novel transfer cases, misconception-based distractors, and justified boundary decisions. Remove before publication.
-->

_(Question Count Rule: Target `15–20` questions total distributed consecutively across Tiers 1–3; use `10–14` for narrow single-subtopic sets.)_

- **Mandatory Dual-Callout Question Architecture (Self-Test Mode)**:
- Every question (`### Q<k>. <Question Prompt>`) uses two separate, independently collapsed native Obsidian callouts (`> [!hint]- Need a nudge?` and `> [!tip]- Reveal approach and solution`) separated by an unquoted blank line so expanding the hint never reveals the answer.
- Inside both callouts, prefix every line—including interior blank separator lines—with `>`:

````markdown
### Q1. What spatial shape does a 2D convolution return for input `(B=4, C_in=3, H=32, W=32)` with `16` kernels of size `3x3`, `stride=2`, `padding=1`, and `dilation=2`?

> [!hint]- Need a nudge?
> Compute the dilated effective kernel extent $K_{\text{eff}} = d(K - 1) + 1$ along height and width before applying floor division.

> [!tip]- Reveal approach and solution
> **Core intuition:** Dilation inserts $(d - 1)$ zeros between adjacent kernel weights, expanding the receptive field span without adding learnable parameters.
>
> 1. Calculate effective kernel height and width: $K_{\text{eff}} = 2(3 - 1) + 1 = 5$.
> 2. Evaluate output height: $H_{\text{out}} = \lfloor (32 + 2(1) - 5) / 2 \rfloor + 1 = 15$.
> 3. Evaluate output width identically: $W_{\text{out}} = 15$.
>
> **Final answer:** `(4, 16, 15, 15)`
>
> **Common trap:** Multiplying $d \times K = 6$ instead of $d(K - 1) + 1 = 5$, or forgetting the $+1$ offset.
````

<!-- optional: diagnosis -->
## [OPTIONAL] What would distinguish these failure causes? (Diagnostic Transfer)

<!--
Include diagnosis only when several plausible causes can be distinguished by evidence. Remove before publication.
-->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Sibling notes expose competing plausible failure causes (e.g., numerical instability vs. bug vs. assumption violation) that require differential diagnosis.
- When to Omit Cleanly: Omit for straightforward recall sets with no overlapping failure modes. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Present symptoms and distinguishing observations, explain why a single check separates causes, and link remediation back to the sibling notes.
-->

- **Context:** State the ambiguous failure symptom and competing candidate causes from the sibling notes.
- **Analysis:** Specify the discriminating observation or test that isolates the true cause and link remediation to the source section.
- **Check:** State the expected vs. refuting signal and any remaining diagnostic blind spot.

See [authoring rules](../../../shared/authoring_rules.md) and [math gates](../../../shared/math_gates.md).
- **Template Contract (`M6` / `practice`):** Emit pure tiered questions without theory summaries; enforce two independently collapsed callouts separated by an unquoted blank line with `>` on interior blank lines; ban trivial true/false or rote copy-paste prompts.
