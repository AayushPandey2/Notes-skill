# Information Theory Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Probabilistic Fixture
Applies to entropy, source coding, KL divergence, mutual information, and noisy-channel capacity. Define the discrete alphabet, probability distribution(s), or DMC transition matrix $P(Y \mid X)$ once.

## Practical Realizations
1. **Manual Entropy & Information Calculation:** Hand-compute $H(X)$, $H(Y \mid X)$, $D_{\mathrm{KL}}(P \| Q)$, and $I(X;Y)$ on a small discrete distribution using base-2 logs (bits).
2. **Coding Construction:** Build a concrete **prefix-free** code (e.g., Huffman), verify Kraft's inequality, decode a sample bitstream, and compare average code length $L$ against $H(X)$.
3. **Noisy-Channel Analysis:** Compute joint/marginal distributions across a concrete channel (e.g., BSC or erasure channel) and maximize $I(X;Y)$ under stated DMC assumptions.
4. **Bounds, Limiting Cases & Assumptions:** Verify $0 \le H(X) \le \log_2 |\mathcal{X}|$, non-negativity of $D_{\mathrm{KL}}$ and $I(X;Y)$, deterministic/independent extremes, and where prefix/memoryless assumptions fail.

## Specialized Walkthrough & Verification
Check probability normalization ($\sum p_i = 1$) and `0 log 0 = 0` conventions; end with **`Analytical and manual calculation review only (no code executed).`** (or **`Source and static review only; not compiled or executed here.`** if simulation code is included).
