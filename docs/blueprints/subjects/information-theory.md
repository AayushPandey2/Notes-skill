# Subject Theory Blueprint: Information Theory

## Purpose

Teach Information Theory through **uncertainty quantification, source coding limits, divergence/mutual information, and noisy-channel bounds**.

## Core Theory Obligations

1. **Entropy & Surprise:** Motivate surprisal $-\log_2 p(x)$, Shannon entropy $H(X)$ (expected code-length lower bound), joint/conditional entropy, and chain rules.
2. **Divergence & Mutual Information:** Contrast KL divergence $D_{\mathrm{KL}}(P \| Q)$ (asymmetry, cross-entropy link $H(P, Q) = H(P) + D_{\mathrm{KL}}(P \| Q)$) with symmetric mutual information $I(X; Y)$ and the data-processing inequality.
3. **Coding & Channel Limits:** Asymptotic equipartition property (AEP), lossless compression bounds (Huffman/arithmetic vs. $H(X)$), and channel capacity $C = \max_{p(x)} I(X;Y)$ assumptions.
