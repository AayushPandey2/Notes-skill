# Subject Theory Blueprint: Deep Learning

## Purpose

Guide Deep Learning theory notes from scalar operations to modern tensor architectures, keeping computational graphs, initialization, stability, and hardware/precision constraints crystal clear.

## Core Theory Obligations

1. **Progressive Tensor & Graph Construction:** Build *scalar neuron $\to$ vector layer $\to$ matrix batch* before general tensor contractions, verifying every `(batch, ..., dim)` shape and transpose.
2. **Computational Graphs & Backpropagation:** Trace forward activation caching and reverse-mode chain-rule gradient accumulation; distinguish analytical derivatives from finite-difference checks.
3. **Architecture & Inductive Bias:** Explain why each structural mechanism exists—convolutions (translation equivariance/locality), recurrence/gating (sequential state & vanishing gradients), residual connections (gradient highways), normalization (BatchNorm/LayerNorm statistics & train-vs-eval differences), and attention (query-key-value similarity & quadratic scaling).
4. **Optimization, Initialization & Stability:** Motivate weight initialization (Xavier/He variance preservation), momentum/adaptive optimizers (`Adam`/`AdamW` decoupled weight decay), learning-rate schedules, gradient clipping, and numerically stable logits-based losses.
5. **Generalization & Failure Modes:** Address overfitting, double descent/capacity, dropout/augmentation, dead ReLUs, vanishing/exploding gradients, and `.train()` vs. `.eval()` mismatches.
