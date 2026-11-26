# Information Theory Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Probabilistic Fixture
Applies to entropy, cross-entropy, KL divergence, mutual information, source coding, and noisy-channel capacity. Define discrete alphabet(s), probability distributions, or DMC transition matrix $P(Y \mid X)$ once, selecting realizations matching the topic:

| Topic | Targeted Investigation Focus |
|---|---|
| **Entropy** | Deterministic vs. uniform extremes (e.g., binary entropy $H(0.5) = 1.0000\text{ bit}$ maximum vs. $H(0)=H(1)=0$) |
| **Cross-entropy** | True vs. assumed coding distributions $H(P, Q) = H(P) + D_{\mathrm{KL}}(P \Vert Q)$ |
| **KL divergence** | $D_{\mathrm{KL}}(P \Vert Q)$ and $D_{\mathrm{KL}}(Q \Vert P)$ can differ; both are zero for identical distributions. Check support mismatch. |
| **Mutual information** | Independent ($I=0$) vs. functionally coupled variables |
| **Source coding** | Prefix-free tree/code construction, Kraft's inequality, universal lower bound $H(X) \le L$, and existence of optimal binary prefix codes (e.g., Huffman) achieving $L < H(X) + 1$ |
| **Channel capacity** | Transition matrix optimization under explicit input/channel constraints |

## Practical Realizations
1. **Manual Entropy & Divergence Calculation:** Compute $H(X)$, $H(P, Q)$, $D_{\mathrm{KL}}(P \Vert Q)$, and $I(X;Y)$ on small discrete distributions using base-2 logs. Use the limiting convention $0\log 0=0$ in entropy. On a finite alphabet, $D_{\mathrm{KL}}(P \Vert Q)$ is finite exactly when $Q(x)>0$ for every $x$ with $P(x)>0$. It is infinite if any $x$ has $P(x)>0$ and $Q(x)=0$.
2. **Coding Construction:** Build a concrete **prefix-free** code (e.g., Huffman), verify Kraft's inequality, decode a sample bitstream, establish the universal lower bound $H(X) \le L$ separately from optimal-code existence achieving $L < H(X) + 1$ (explaining that arbitrary valid prefix codes can exceed $H(X) + 1$), and check efficiency.
3. **Noisy-Channel Analysis:** Compute joint/marginal distributions across a concrete channel (e.g., BSC or erasure channel) and maximize $I(X;Y)$ under stated DMC assumptions.
4. **Bounds, Limiting Cases & Assumptions:** Verify $0 \le H(X) \le \log_2 |\mathcal{X}|$, non-negativity of $D_{\mathrm{KL}}$ and $I(X;Y)$, deterministic/independent extremes, and where prefix or memoryless assumptions fail.

## Specialized Walkthrough & Verification
Check probability normalization ($\sum p_i = 1$) and entropy/KL support rules explicitly. Use the shared lab contract for evidence and verification disclosures.
