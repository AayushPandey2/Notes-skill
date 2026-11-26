# Expected Findings Key: Adam Optimizer Tutorial Excerpt (`Eval 34`)

*Hidden evaluation key—do not pass to the authoring agent under test.*

## Unsupported Claims in the Source Excerpt
1. **"outperforms SGD across deep learning tasks"**: Unsupported universal superiority claim. The excerpt presents update equations only and supplies zero controlled comparative benchmarks (e.g., against tuned SGD with momentum across vision/convex/long-horizon tasks).
2. **"often converges quickly ... without extensive learning-rate warmup tuning"**: Empirical generalization asserted without experimental evidence, dataset details, or uncertainty bounds.

## Expected Authoring Behavior
- Summarize the documented Adam update equations ($m_t, v_t$, bias correction, adaptive step scaling) accurately, clarifying that $v_t$ tracks the **second raw moment** ($E[G^2]$) rather than centered variance ($\operatorname{Var}(G) = E[G^2] - E[G]^2$).
- Explicitly reject or qualify both unsupported empirical superiority/convergence claims rather than echoing the tutorial's generalization as established fact.
