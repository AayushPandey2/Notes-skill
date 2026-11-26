# Information Theory Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Probabilistic Fixture
Applies to entropy, cross-entropy, KL divergence, mutual information, source coding, and noisy-channel capacity. Define discrete alphabet(s), probability distributions, or DMC transition matrix $P(Y \mid X)$ once, selecting realizations matching the topic:

| Topic | Targeted Investigation Focus |
|---|---|
| **Entropy** | Deterministic vs. uniform extremes (e.g., binary entropy $H(0.5) = 1.0000\text{ bit}$ maximum vs. $H(0)=H(1)=0$) |
| **Cross-entropy** | True vs. assumed coding distributions $H(P, Q) = H(P) + D_{\mathrm{KL}}(P \| Q)$ |
| **KL divergence** | Asymmetry ($D_{\mathrm{KL}}(P \| Q) \neq D_{\mathrm{KL}}(Q \| P)$) and support-mismatch singularity |
| **Mutual information** | Independent ($I=0$) vs. functionally coupled variables |
| **Source coding** | Prefix-free tree/code construction, Kraft's inequality, and $H(X) \le L < H(X)+1$ |
| **Channel capacity** | Transition matrix optimization under explicit input/channel constraints |

## Practical Realizations
1. **Manual Entropy & Divergence Calculation:** Hand-compute $H(X)$, $H(P, Q)$, $D_{\mathrm{KL}}(P \| Q)$, and $I(X;Y)$ on small discrete distributions using base-2 logs (bits). Enforce **zero-probability rules accurately**: `0 log 0 = 0` holds for Shannon entropy, whereas **KL divergence requires support inclusion** ($P(x) > 0$ with $Q(x) = 0 \implies D_{\mathrm{KL}}(P \| Q) = +\infty$).
2. **Coding Construction:** Build a concrete **prefix-free** code (e.g., Huffman), verify Kraft's inequality, decode a sample bitstream, and compare average code length $L$ against $H(X)$.
3. **Noisy-Channel Analysis:** Compute joint/marginal distributions across a concrete channel (e.g., BSC or erasure channel) and maximize $I(X;Y)$ under stated DMC assumptions.
4. **Bounds, Limiting Cases & Assumptions:** Verify $0 \le H(X) \le \log_2 |\mathcal{X}|$, non-negativity of $D_{\mathrm{KL}}$ and $I(X;Y)$, deterministic/independent extremes, and where prefix or memoryless assumptions fail.

## Specialized Walkthrough & Verification
Check probability normalization ($\sum p_i = 1$) and entropy/KL support rules explicitly; end with **`Analytical and manual calculation review only (no code executed).`** (or **`Source and static review only; not compiled or executed here.`** if simulation code appears).
