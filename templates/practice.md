# Three-Tier Active Recall, Tracing & Synthesis Practice Test

- **Routing & Destination Rules**:
    - Support manual `/scribe-practice <topic-or-note>` (saved under `<Topic Folder>/Practice Set/<Subtopic> - Practice.md`, reusing an existing resolved topic folder).
    - Support automatic topic-wide generation when a run creates a new topic folder (saved under `<Topic Folder>/Practice Set/<Topic> - Practice Test.md`).
    - Reuse retrieved evidence, equations, and running-example invariants from sibling notes. A `practice` route must **never** trigger another `practice` route.
- **Header Block**: YAML frontmatter (`type: practice`) + `# <Topic or Subtopic> — Active Recall & Synthesis Practice Set`.

## 1. What notes, prerequisites & equations does this practice set test? (Scope & Readiness)

- List wiki-links to the target sibling vault notes (`[[01 - ...]]`, `[[02 - ...]]`) and any prerequisite notes needed before attempting the test.

## 2. Tier 1 — Do I know the core definitions, invariants & sanity checks? (Q1–Q4: Foundational Recall)


## 3. Tier 2 — Can I trace code, compute outputs & debug failures? (Q5–Q10: Quantitative Application, Code Tracing & Math)


## 4. Tier 3 — Can I handle pathological edge cases & cross-topic synthesis? (Q11–Q15: Boundary Stress-Tests & System Design)

_(Question Count Rule: Target `12–15` questions total, distributed as `Q1–Q4` Tier 1, `Q5–Q10` Tier 2, `Q11–Q15` Tier 3. For a narrow single subtopic where 15 questions would be repetitive, use `10–11` high-signal questions distributed as `Q1–Q3` Tier 1, `Q4–Q7` Tier 2, `Q8–Q11` Tier 3)._

- **Mandatory Dual-Callout Question Architecture**:
- Every single question (`### Q<k>. <Question Prompt>`) **must** use two separate, independently collapsed native Obsidian callouts (`> [!hint]- Need a nudge?` and `> [!tip]- Reveal approach and solution`) so expanding the hint never reveals the answer.
- Inside both callouts, prefix every line—including blank separator lines between paragraphs and before numbered/bulleted lists—with `>` so Obsidian never breaks the callout box:

````markdown
### Q1. What spatial shape does a 2D convolution return for input `(B=4, C_in=3, H=32, W=32)` with `16` kernels of size `3x3`, `stride=2`, `padding=1`, and `dilation=2`?
> [!hint]- Need a nudge?
> Compute the dilated effective kernel extent $K_{\text{eff}} = d(K - 1) + 1$ along height and width before applying floor division.
> [!tip]- Reveal approach and solution
> **Core intuition:** Dilation inserts $(d - 1)$ zeros between adjacent kernel weights, expanding the receptive field span without adding learnable parameters.
>
> 1. Calculate effective kernel height and width: $K_{\text{eff}} = 2(3 - 1) + 1 = 5$.
> 2. Evaluate output height: $H_{\text{out}} = \lfloor (32 + 2(1) - 5) / 2 \rfloor + 1 = \lfloor 29 / 2 \rfloor + 1 = 15$.
> 3. Evaluate output width identically: $W_{\text{out}} = 15$.
> 4. Combine batch size $B=4$ and output channels $C_{\text{out}}=16$.
>
> **Final answer:** `(4, 16, 15, 15)`
>
> **Common trap:** Multiplying $d \times K = 6$ instead of $d(K - 1) + 1 = 5$, or forgetting the $+1$ offset after floor division.
````
## 5. Where did my mental model crack? (Diagnostic Error Log & Open Confusion)

- Diagnostic review checklist mapping each tier back to specific sections of the sibling study notes + `**Confusion** :: <Specific question or concept that tripped me up for Weekly Review>`.

Follow [shared authoring rules](../shared/authoring_rules.md) and the [footer contract](../shared/footer_widgets.md). Apply the math gate only at the planned level. Scaffold comments are editing slots and must be removed before publication.

> [!important] AGENT AUTHORING DIRECTIVE — `practice` Strictly enforce the two independently collapsed callouts (`[!hint]-` and `[!tip]-`) and preserve blank `>` lines before lists and between paragraphs inside every callout so Obsidian renders them without broken boxes. Ban trivial true/false or rote copy-paste questions: design every question in Tiers 2 and 3 to test real quantitative calculation, tensor/pointer code tracing, silent bug diagnosis, or boundary-case breakdown derived directly from the sibling study notes.
