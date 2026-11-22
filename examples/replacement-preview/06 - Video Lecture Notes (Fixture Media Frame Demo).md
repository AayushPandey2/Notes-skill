---
topic: Video Notes Preview
tags:
- topic/video-notes-preview
- subject/supervised-learning-replacement-preview
- domain/machine-learning
- master-topic/supervised-learning-replacement-preview
- concept/video-notes-preview
- type/deep-notes
- ml
- supervised-learning
- replacement-preview
master_topic: Supervised Learning (Replacement Preview)
domain: machine-learning
note_type: deep-notes
---

# Gradient Step Derivation (Labeled Fixture Media Demo)

> [!info] Source & Access Context
> **Access Mode:** `transcript_plus_frames` | **Source:** https://www.youtube.com/watch?v=fixtureDemo1

## Concept Segment 1 ([00:10](https://www.youtube.com/watch?v=fixtureDemo1&t=10s))

**Presenter explanation ([00:10](https://www.youtube.com/watch?v=fixtureDemo1&t=10s)):** First set up the residual error r equals y minus w x plus b as an intermediate expression.

**What to look for (intermediate derivation step before chain-rule differentiation):** Inspect the visual state captured at timestamp `15s`.

![[assets/scriptorium/supervised-learning-preview/frame-00015s-81dc2a0bbe.png]]

*Visible details:* y_hat = w*x + b; r = y - (w*x + b).

## Concept Segment 2 ([00:40](https://www.youtube.com/watch?v=fixtureDemo1&t=40s))

**Presenter explanation ([00:40](https://www.youtube.com/watch?v=fixtureDemo1&t=40s)):** Next differentiate using the chain rule so dL over dw pulls down factor negative 2 x_i.

> [!note] Fixture Media & Unverified Live Video Status
> Host tool availability observed: `ffmpeg=False`, `yt-dlp=False`.
> The embedded PNG frames above come from **labeled local fixture media** verifying timeline alignment and intermediate-state retention—live YouTube extraction remains unverified on this host.

### Formal Equation & Worked Numerical Verification (Independently Verified Fold)

Trace how each residual scales the weight update in one single-feature gradient step shown at 00:45.

$$
\frac{dL}{dw} = -\frac{2}{n} \sum_{i=1}^{n} x^{(i)} \big(y^{(i)} - (w x^{(i)} + b)\big)
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Trace how each residual scales the weight update in one single-feature gradient step shown at 00:45.
>
> **How to read it aloud:** d L over d w equals negative two over n times the sum over i of x^(i) times residual y^(i) minus predicted w x^(i) plus b.
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $\frac{dL}{dw}$ | weight gradient of MSE loss | scalar | 1x1 | weight gradient of MSE loss |
> | $x^{(i)}$ | i-th sample input feature | scalar | 1x1 | i-th sample input feature |
> | $y^{(i)}$ | i-th sample true target | scalar | 1x1 | i-th sample true target |
>
> **Worked numerical example:**
> - **Declared inputs:** `x1 = 2.0`, `y1 = 5.0`, `w = 1.0`, `b = 1.0`, `n = 1.0`
> - **pred:** `w * x1 + b` = `3.0`
> - **grad:** `-(2 / n) * x1 * (y1 - yh)` = `-8.0` — negative gradient tells optimizer to increase slope w
> - **Interpretation:** Gradient -8.0 underpredicts y=5 at w=1; subtracting negative gradient increases w.
> - **Sanity check:** Zero residual yields zero gradient cleanly.
>
> **Common misunderstandings to avoid:**
> - Forgetting the outer minus sign from differentiating (y - y_hat)^2 with respect to y_hat reverses gradient descent into gradient ascent.

Suppose a single observation has given input $x=2.0$, true target $y=5.0$, weight $w=1.0$, and bias $b=1.0$ ($n=1$):
1. First evaluate prediction $w x + b = 1.0(2.0) + 1.0 = 3.0$, giving residual $5.0 - 3.0 = 2.0$.
2. Next multiply $-(2/1)(2.0)(2.0) = -8.0$, telling gradient descent to increase $w$.
3. Sanity check: zero residual returns $0$ gradient cleanly, avoiding the mistake of flipping the minus sign.
