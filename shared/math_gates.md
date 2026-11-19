# Math gates

Use [per-concept mathematical depth](../references/adaptive-engine.md#selection-and-depth) (`M0–M5`) for deep-study notes, and route-level `math_level` (`0–2`) for source-study and compact routes. Rendering follows [authoring rules](authoring_rules.md#rendering).

Good: state the formula's question, define symbols/shape/units and assumptions at first use, show a useful calculation or justified transformation, interpret, then check a meaningful condition (dimensions/units for physical laws, compatible shapes for arrays, normalization/support for probabilities, or sign/boundary behavior). Bad: repeat the same equation in an abstract, body and footer, or force irrelevant zero/tie/infinity tables outside its domain.

Good: use unequal dimensions (e.g., asymmetric non-square matrices/tensors) and distinct numerical values to reveal axis, transpose, or broadcast errors. Bad: a symmetric fixture that accidentally passes after transposition. Good: name the chain rule, identity, or invariant at a non-obvious transition; bad: expand every trivial addition while skipping the nonzero or domain condition required for division, logarithm, or limit interchange.

Keep forward prediction and backward derivative calculations distinct: a neural-network forward pass or inference trace computes weighted sums and activations without derivatives; calculus and chain-rule derivations enter only when local sensitivity, parameter updates, backpropagation, or gradient debugging are part of the concept's objective.

Deep notes use [per-concept depth](../references/adaptive-engine.md#selection-and-depth) (`M0–M5`), without domain ceilings or display-equation quotas. Saved legacy contracts and source-study retain their existing checks. Keep simple assignments or comparisons inline and give each central display equation one canonical home. The compact templates retain their existing layout checks within the planned level. Label out-of-domain cases as invalid. In source study, label independently added derivations and preserve the original sequence.
