# Practice

**Purpose:** active recall, application, debugging, edge-case reasoning, and transfer across the studied material.



## What this tests

## Recall / Sanity Checks

## Apply / Trace / Debug

## Edge Cases / Connections

## Review next

### Authoring contract

- Support `/scribe-practice <topic-or-note>`. Resolve an existing note/topic when supplied, and base questions on actual or successfully generated material. Identify prerequisites and covered objectives.
- Automatically create **one topic-wide set** when a normal generation run creates a new topic folder, unless the user opts out. Save it as `<Topic Folder>/Practice Set/<Topic> - Practice Test.md`.
- Save a manual subtopic set as `<Topic Folder>/Practice Set/<Subtopic> - Practice.md`. Reuse the resolved topic folder and existing collision policy. A Practice route must never spawn another Practice route.
- Prefer **12–15 questions**. Use **10–11** for a narrow scope when additional questions would repeat the same skill. Do not pad with paraphrases.
- Start with Q1–Q4 for recall and sanity checks. Use the middle questions for multi-step application, code/math tracing, and debugging. Reserve the last questions for boundaries, counterexamples, combining ideas, and transfer. For 15 questions, Q5–Q10 and Q11–Q15 form the latter tiers.
- Provide all data, assumptions, units, and constraints needed for a well-posed answer. Do not ask students to guess an unspecified API version or runtime behavior.
- Each question has two **independently collapsed** native Obsidian callouts: one actionable hint and a separate complete solution. Opening a hint must keep the solution hidden.
- The solution includes **Core intuition**, justified steps, **Final answer**, and **Common trap**. Include expected output, proof, complexity, or verification when the question requires it.
- Use the math gate per question. For code questions, use the topic's chosen language unless a deliberate comparison is part of the objective.
- **Review next:** Map missed question groups to concepts or existing notes. Do not invent the user's score or claim the practice was completed.

Use this structural pattern, replacing example text with a real question:

```markdown
### Q1. What shape does the operation return?

> [!hint]- Need a nudge?
> Track the spatial dimensions independently.

> [!tip]- Reveal approach and solution
> **Core intuition:** Count valid placements along each axis.
>
> 1. Evaluate the height under the stated assumptions.
> 2. Evaluate the width under the same assumptions.
>
> **Final answer:** Give the computed shape and its dimension order.
>
> **Common trap:** Mixing the batch/channel layout with the spatial axes.
```

The illustrative pattern above is not a complete generated question: actual questions must specify numerical input and all relevant parameters when asking for a numerical shape.
