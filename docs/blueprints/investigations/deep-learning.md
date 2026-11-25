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

## Four Deep Learning Tracks (Apply Track-Applicability Gate)

For comprehensive DL topics, cover all 4 tracks below; for narrower concepts, select the meaningful subset. **Do not** force 4-language Rust tracks onto Deep Learning unless the user explicitly requests Rust.

1. **Track 1 — Manual Tensor Implementation (First Principles):** Explicit NumPy forward pass, activation, loss scaling, manual chain-rule backpropagation, and parameter update on a tiny batch.
2. **Track 2 — Automatic Differentiation:** Minimal computational graph / tape / autograd pass showing how forward dependencies drive reverse-mode gradient accumulation.
3. **Track 3 — Framework Implementation (PyTorch / JAX):** Official-doc-verified module, numerically stable loss (e.g., logits-based cross-entropy), `zero_grad()`, `.backward()`, `optimizer.step()`, and `.train()` vs `.eval()` state management.
4. **Track 4 — Training Diagnostics & Stability:** Controlled investigation of initialization, learning rate, normalization, gradient clipping, vanishing/exploding gradients, or shape/training-state failure modes.

For each track:
- `### [Implementation name]` + short rationale.
- Setup/dependencies block + proportionate collapsed explanation.
- Complete code block.
- Immediately beneath it, `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` covering **A–G**: **A** batch dimensions, tensor dtypes, parameter shapes; **B** forward functions, loss scaling, chain-rule dependencies; **C** execution and gradient order; **D** one complete tiny batch forward/backward numerical dry run; **E** predictions, losses, gradients, updated parameters; **F** shape mismatches, `NaN`/overflow, missing `zero_grad()`, eval-mode mistakes; **G** reconstruction of the full training iteration.

## Verification Status

State experiment status honestly (**Expected** / **Hand-calculated**, never **Executed**) and end with **`Source and static review only; not compiled or executed here.`**
