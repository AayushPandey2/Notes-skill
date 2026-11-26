# Subject Theory Blueprint: Information Theory

## Purpose

Teach Information Theory through **uncertainty quantification, source coding limits, divergence/mutual information, and noisy-channel bounds**—always stating the exact coding and channel assumptions behind every bound.

## Core Theory Obligations

1. **Entropy & Source Coding Bounds:** Motivate surprisal $-\log_2 p(x)$, Shannon entropy $H(X)$, joint/conditional entropy, and chain rules; state explicitly that expected code-length lower bounds ($L \ge H(X)$) apply to **uniquely decodable / prefix-free codes** under stated source assumptions.
2. **Divergence & Mutual Information:** Contrast KL divergence $D_{\mathrm{KL}}(P \| Q)$ (asymmetry, cross-entropy link $H(P, Q) = H(P) + D_{\mathrm{KL}}(P \| Q)$) with symmetric mutual information $I(X; Y)$ and the data-processing inequality.
3. **Channel Capacity & Assumptions:** Qualify $C = \max_{p(x)} I(X;Y)$ explicitly under the **discrete memoryless channel (DMC)** setting without extra constraints, alongside AEP and lossless compression algorithms (Huffman, arithmetic).
4. **Beginner Progression, Visuals & Practice:** Motivate entropy, divergence, and coding limits on concrete small-alphabet distributions (e.g., biased coin or 4-symbol code) while closing probability/logarithm/Jensen prerequisites inline, pair binary entropy curves, Huffman trees, and channel diagrams with verified web-sourced figures per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII), and complete one small numerical calculation before an independent exercise.
