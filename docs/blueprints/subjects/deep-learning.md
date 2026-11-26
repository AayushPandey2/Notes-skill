# Subject Theory Blueprint: Deep Learning

## Purpose

Guide Deep Learning theory notes from scalar operations to modern tensor architectures, keeping computational graphs, initialization, stability, framework semantics, and hardware/precision constraints crystal clear. Activate obligations conditionally—never force every DL technique into one introductory note.

## 1. Core Theory Obligations

1. **Progressive Tensor & Graph Construction:** Build *scalar neuron $\to$ vector layer $\to$ matrix batch* before general tensor contractions, verifying layouts, `(batch, ..., dim)` shapes, broadcasting, and reduction axes.
2. **Computational Graphs, Autograd & Gradient Checking:** Trace forward activation caching and reverse-mode chain-rule gradient accumulation; separate analytical derivatives from finite-difference checks.
3. **Architecture & Inductive Bias:** Explain *why* each structural mechanism exists—convolutions (locality/equivariance), recurrence/gating (sequential state), residual connections (gradient highways), normalization (BatchNorm/LayerNorm statistics & train-vs.-eval state behavior), and attention (query-key-value similarity & quadratic scaling).
4. **Optimization, Initialization, Precision & Stability:** Motivate Xavier/He variance-preserving initialization, momentum/`Adam`/`AdamW` (decoupled weight decay), learning-rate schedules, gradient accumulation, gradient clipping, mixed precision (`fp16`/`bf16` vs. `fp32` master weights/loss scaling), and logits-based losses.
5. **Generalization & Failure Modes:** Address capacity/regularization, dead ReLUs, vanishing/exploding gradients, and training-vs.-inference mode mismatches.
6. **Beginner Progression, Visuals & Practice:** Close prerequisite calculus/linear-algebra tools (chain rule, matrix shapes) inline before backpropagation equations, trace one tiny hand-verifiable forward-and-backward numerical pass before scaling to layers (followed by an independent check), and retrieve verified web-sourced architecture/curve diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII).

## 2. Framework Semantics Separation (PyTorch vs. JAX)

Teach the universal principle first, then select **verified framework-specific semantics**—never force PyTorch stateful APIs onto JAX or vice versa:

| Concept | PyTorch | JAX-Style Functional |
|---|---|---|
| **Differentiation** | Autograd tape + `.backward()` | Pure functional transforms (`jax.grad`, `value_and_grad`) |
| **Parameters** | Module-owned stateful tensors (`nn.Module`) | Explicit parameter pytrees passed as arguments |
| **Optimizer State** | Stateful `Optimizer` object | Explicit functional optimizer state (`optax`) |
| **Gradient Clearing** | Explicit `zero_grad()` (accumulates by default) | Fresh gradients returned per `grad` call |
| **Updates** | Mutating `optimizer.step()` | Pure functional parameter/state update |
| **Train vs. Eval Mode** | Module mode toggle (`.train()` / `.eval()`) | Explicit stateless/carried state arguments (`training=True/False`) |
