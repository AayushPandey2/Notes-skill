# Two-sample averaging filter

Let $x[n]$ be a sampled signal with the previous sample available. Define the smoothed output by $y[n]=(x[n]+x[n-1])/2$.

**Proof of the definition.** The output is the mean of the two samples because smoothing was defined as taking their mean. This proves that the definition must hold.

For the input $x[n]=(-1)^n$, the filter output is

$$
y[n]=0 .
$$

> [!example]- Understand this formula step by step — Alternating input
>
> The input switches between $+1$ and $-1$. How the previous sample relates to the current one is left implicit.

The output for a constant input $x[n]=c$ is $y[n]=c$.

> [!info]- What the comparison reveals
>
> The alternating component disappears, while the constant component passes through unchanged. The distinction is the point of comparing the two inputs.
