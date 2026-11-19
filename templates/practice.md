<!-- scaffold:preflight
Decision-Matrix Pre-Flight: [note_decision_matrix.md](../shared/note_decision_matrix.md).
Switches: D01 route (`practice`, never triggers nested practice); D02 sibling topic/subtopic scope; D03 reader; D04 active-recall & transfer outcome;
D05 sibling vault notes; D06–D09 inherited sibling `math_level`; D10 sibling running-example invariants; D11 dual-callout architecture;
D12–D13 code/math tracing & edge diagnosis; D14 optional module (`diagnosis`); D15 final audit.
Strip this block before emission. Load detailed DM branches only when active.
-->

# Three-Tier Active Recall, Tracing & Synthesis Practice Set

- **Routing & Destination Rules**:
    - Support manual `/scribe-practice <topic-or-note>` (saved in the centralized `Practice Sets/` folder located at the same sibling directory level as the `<subtopic>/` folders, e.g., `Practice Sets/<Subtopic> - Practice.md`, reusing an existing resolved topic folder).
    - Support automatic topic-wide generation when a run creates a new topic folder (saved in the centralized `Practice Sets/` folder located at the same sibling directory level as the `<subtopic>/` folders, e.g., `Practice Sets/<Topic> - Practice Test.md`).
    - Reuse retrieved evidence, equations, and running-example invariants from sibling notes. A `practice` route must **never** trigger another `practice` route.
- **Header Block**: Metadata per shared contract + `# <Topic or Subtopic> — Active Recall & Synthesis Practice Set`. Do **not** include study-note theory summaries, symbol tables, or equation previews in Section 1—deliver pure tiered questions (`15–20` questions total; `10–14` for narrow single-subtopic sets).

## Tier 1 — Foundational Recall (Q1–Q5)


## Tier 2 — Quantitative Application, Code Tracing & Math (Q6–Q12)


## Tier 3 — Boundary Stress-Tests & Cross-Topic Synthesis (Q13–Q18)

_(Question Count Rule: Target `15–20` questions total, distributed consecutively across Tiers 1–3, e.g., `Q1–Q5` Tier 1, `Q6–Q12` Tier 2, `Q13–Q18` Tier 3. For a narrow single subtopic where 15+ questions would be repetitive, use `10–14` high-signal questions distributed across Tiers 1–3)._

- **Mandatory Dual-Callout Question Architecture**:
- Every single question (`### Q<k>. <Question Prompt>`) **must** use two separate, independently collapsed native Obsidian callouts (`> [!hint]- Need a nudge?` and `> [!tip]- Reveal approach and solution`) separated by an unquoted blank line so expanding the hint never reveals the answer.
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

<!-- optional: diagnosis -->
## [OPTIONAL] What would distinguish these failure causes? (Diagnostic Transfer)

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Sibling notes expose competing plausible failure causes (e.g., numerical instability vs. bug vs. assumption violation) that require differential diagnosis; D04, D13–D14.
- When to Omit Cleanly: Omit for straightforward recall sets with no overlapping failure modes. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Present symptoms and distinguishing observations, explain why a single check separates causes, and link remediation back to the sibling notes.
-->

- **Context:** State the ambiguous failure symptom and competing candidate causes from the sibling notes.
- **Analysis:** Specify the discriminating observation or test that isolates the true cause and link remediation to the source section.
- **Check:** State the expected vs. refuting signal and any remaining diagnostic blind spot.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
- **Template Contract (`practice`):** Emit pure tiered questions (`15–20` questions total across `Tier 1`, `Tier 2`, `Tier 3`, or `10–14` for narrow sets) without Section 1 theory summaries; enforce two independently collapsed callouts (`> [!hint]- Need a nudge?` and `> [!tip]- Reveal approach and solution`) separated by an unquoted blank line with `>` prefixing every interior blank line; ban trivial true/false or rote copy-paste prompts.
