# Evaluation Fixture (Golden): RC Step Response (`evaluations/fixtures/electrical/`)

*Evaluation-only reference excerpt—never copy as a mandatory template.*

## Shared Circuit Contract & Passive Sign Convention
Consider a series RC circuit driven by an ideal 5 V DC step at $t = 0$ (initial capacitor voltage $v_C(0^-) = 0\text{ V}$), with $R = 1\text{ k}\Omega$ and $C = 10\,\mu\text{F}$ (low-voltage benchtop educational regime; stored energy at steady state $\frac{1}{2}CV_s^2 = 0.125\text{ mJ}$). Using the passive sign convention ($i(t)$ enters the positive terminal of $R$ and $C$), lumped-circuit KVL gives:
$$
V_s = i(t)R + v_C(t) = RC\frac{dv_C(t)}{dt} + v_C(t), \qquad t \ge 0
$$
Solving with $v_C(0^+) = 0\text{ V}$ yields $v_C(t) = V_s(1 - e^{-t/\tau})$ with time constant $\tau = RC = 10\text{ ms}$. At $t = \tau$, $v_C(\tau) = 5(1 - e^{-1}) \approx 3.16\text{ V}$ (analytical prediction; no hardware executed).
