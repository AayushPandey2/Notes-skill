# Deep Learning Implementation Lab Blueprint

Use this lean, implementation-focused blueprint for Deep Learning companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs beneath every implementation, zero local execution, and static correctness review.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, separate training-dynamics experiments, 11-step workflows, quizzes/challenges, or repetitive summaries. **Do not** force 4-language Rust tracks onto Deep Learning unless the user explicitly requests Rust.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Implementation Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Task & Tensor Contract
Briefly define one coherent task across the tracks: tensor shapes (`(B, d_in) -> (B, d_out)`), `dtype`, forward computation, activation, loss scaling (e.g., logits-based cross-entropy vs manual sigmoid+BCE), parameter initialization, actual optimizer (`SGD+momentum`, `Adam`, `AdamW`), and equivalence boundaries.

## Implementation Tracks

Include the smallest meaningful tracks—typically **From-Scratch NumPy / Tensor** (explicit forward pass, manual chain-rule backprop, update) and **Framework (PyTorch / JAX)** (verified against official docs: module, loss, `zero_grad()`, `.backward()`, `optimizer.step()`, `.train()` vs `.eval()`).

For each track:
- `### [Implementation name]` + short rationale.
- Setup/dependencies block + proportionate collapsed explanation.
- Complete code block.
- Immediately beneath it, `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` covering **A–G** (inputs & tensor shapes, forward/backprop math & loss scaling, line-by-line execution order, a tiny batch forward/backward numerical dry run, output interpretation, failure cases like `NaN`/missing `zero_grad()`, and core-logic reconstruction).

## Verification Status

End with **`Source and static review only; not compiled or executed here.`**
