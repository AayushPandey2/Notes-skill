# Statistics & Probability Implementation Lab Blueprint

Use this lean, realization-focused blueprint for Statistics & Probability companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs, experiment integrity, and static review.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Statistical Investigation Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Statistical Model & Data Fixture
Define the target population parameter vs. sample estimator, distributional assumptions, sample size, and one small shared dataset.

## Four Statistical Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Manual Calculation:** Compute probabilities, estimators, test statistics, or confidence intervals by hand on the small fixture.
2. **Track 2 — Formal Reasoning:** Derive or justify the governing estimator/test statistic and its sampling-distribution assumptions.
3. **Track 3 — Simulation or Data Analysis:** Provide a learner-executable Python or R simulation demonstrating repeated sampling or model behavior (mark output **Expected** unless observed data is supplied).
4. **Track 4 — Statistical Verification:** Test assumption sensitivity (normality, independence, outliers), uncertainty bounds, and **statistical vs. practical significance**.

Directly beneath each realization, include `> [!example]- Understand this realization: statistics, steps, and numerical dry run` (or `...implementation...` for simulation code) covering **A–G**: **A** parameter vs. estimator & data fixture; **B** probabilistic/sampling mechanism; **C** step-by-step calculation/code order; **D** full numerical dry run; **E** interval/test interpretation; **F** $p$-value misinterpretation, independence violation, small-sample failures; **G** core-reasoning reconstruction.

## Verification Status

If simulation code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Hand-calculated and analytical review only (no code executed).`**
