# Deep Learning Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Contract
Applies to neural networks, computational graphs, autograd, and deep architectures. Define I/O tensor shapes (`(B, d_in) -> (B, d_out)`), `dtype`, activation, loss scaling (e.g., logits-based cross-entropy), initialization, and optimizer once in the shared contract, defaulting to **Python** unless another stack is requested and **never including Rust unless explicitly requested**.

## Practical Realizations
1. **Manual Tensor Implementation:** Explicit NumPy forward pass, activation, loss scaling, manual chain-rule backprop, and parameter update on a tiny batch.
2. **Automatic Differentiation:** Minimal computational graph / tape / functional grad pass illustrating reverse-mode gradient accumulation and parameter/state complexity.
3. **Framework Implementation (Explicitly Select PyTorch OR JAX):** Use verified APIs for the chosen framework—never mix PyTorch stateful calls (`zero_grad()`, `.backward()`, `optimizer.step()`, `.train()`, `.eval()`) into JAX functional transforms (`jax.grad`, `value_and_grad`, explicit pytree parameters/optimizer state, stateless training flags).
4. **Testing, Training Diagnostics & Independent Exercises:** Gradient checks, debugging steps for initialization/normalization/clipping/`NaN`/overflow or shape/mode bugs, and 1–2 **Independent Exercises** (`> [!hint]-` / `> [!success]-`).

## Specialized Walkthrough & Verification
Trace tensor shapes, intermediate forward/backprop states, edge cases, and failure modes, closing code labs with **`Source and static review only; not compiled or executed here.`** (never claiming execution/benchmarking without external evidence).
