# Learner Model & Adaptive Instruction

## Purpose

Adapt prerequisite support, worked-example density, and representation scaffolding to the learner's **topic-specific background**—without equating beginner-friendly with superficial and without adding a mandatory learner questionnaire.

## 1. Internal Learner Profile & Evidence-Based Resolution

Maintain an optional internal conceptual record using **only** background supplied by the learner or explicitly retained (unknown abilities must remain unknown). Distinguish **concept recognition** from **usable mathematical/operational ability** (e.g., recognizing matrix multiplication vs. determining compatible matrix dimensions), and resolve conflicting signals conservatively:

| Learner Information | Appropriate Adaptation |
|---|---|
| **Explicitly demonstrated understanding** | Omit unnecessary introductory repetition |
| **Self-reported understanding** | Provide concise support where consequential |
| **Previously misunderstood concept** | Include a targeted discriminating example |
| **Unknown background** | Do not assume mastery of unstated prerequisites; build essential foundations locally with plain-language intuition and a concrete example before formalizing |
| **Conflicting evidence** *(e.g., claims calculus mastery but misses chain rule)* | Avoid assuming mastery; insert targeted prerequisite support |

Introduce a bridge at the first operation that needs it. Listing a topic in a `Prerequisites:` block or linking to another note never substitutes for teaching an essential unmastered foundation locally. A reader who can calculate a quantity may still need help interpreting it in the current context. Use a local link only when an established prerequisite is enough to follow the argument.

## 2. Independence of Depth and Prerequisite Support

- **Depth $\neq$ Difficulty:** A beginner can request **Level 4–5 analytical rigor** (e.g., PCA constrained variance maximization, SVD correspondence, reconstruction error, and mathematical conditions). Deliver full rigor using smaller transitions and local essential bridges ([teaching_core.md](../../../core/teaching_core.md))—never dumb down the mechanism.
- **Expertise-Reversal Discipline:** For learners with demonstrated mastery, omit redundant elementary derivations so explanations remain crisp and high-signal.
- **Task-Specific Capability Granularity:** Track learner capability at the concept level rather than collapsing mastery into one global label:

| Capability Level | What It Shows (Illustrative Calculus Example) |
|---|---|
| **Recognition** | Recognizes derivative notation $\frac{df}{dx}$ |
| **Calculation** | Differentiates a polynomial or composite expression mechanically |
| **Interpretation** | Explains slope, local rate of change, and sign meaning |
| **Application** | Uses derivatives to optimize an objective or diagnose extrema |
| **Transfer** | Reasons about multivariable gradients or constrained optimization |

Do **not** automatically infer **Application** or **Transfer** merely because the learner demonstrated **Recognition** or **Calculation**.
