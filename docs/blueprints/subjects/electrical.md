# Subject Theory Blueprint: Electrical & Electronics Engineering

## Purpose

Give Electrical and Electronics Engineering notes rigorous physical, mathematical, and circuit-level teaching structure aligned with [physical-lab-safety.md](../../procedures/safety/physical-lab-safety.md).

## 1. Core Engineering Progression & Method Selection

Develop topics naturally along:
**Physical phenomenon $\to$ component model & sign convention $\to$ circuit/system configuration $\to$ analysis-method selection $\to$ governing equations $\to$ analytical/transient/frequency solution $\to$ signal behavior $\to$ non-ideal effects & tolerances $\to$ engineering application & limits.**

Always establish **reference directions** and the **passive sign convention** before writing element equations ($v = iR$, $p = vi$, $i = C\frac{dv}{dt}$, $v = L\frac{di}{dt}$). Qualify **Kirchhoff's Voltage Law (KVL)** explicitly under **lumped-circuit assumptions** (negligible time-varying magnetic flux linkage outside lumped inductors; distinguish loop KVL from induced electromotive force $\oint \mathbf{E}\cdot d\mathbf{l} = -\frac{d\Phi_B}{dt}$). Teach *why* a circuit reduction (series/parallel, Thévenin/Norton) or analysis method (nodal vs. mesh vs. superposition vs. phasors/Laplace) fits the topology.

## 2. Subdomain Theory Obligations

- **Circuit theory:** Nodes, branches, loops, KCL, lumped-circuit KVL, Thévenin/Norton equivalents, nodal/mesh analysis, superposition (linearity limits), maximum power transfer.
- **Analog electronics:** Biasing & DC operating point (Q-point), small-signal linearization, gain, input/output impedance & loading, frequency response & saturation clipping.
- **Digital electronics:** Number systems, Boolean algebra & minimization, combinational vs. sequential logic, flip-flops, setup/hold timing, hazards/glitches, finite-state machines.
- **Semiconductor devices:** Charge carriers, $p$-$n$ junctions, depletion region, diode/BJT/MOSFET operating regions (cutoff, triode/linear, saturation), ideal vs. non-ideal $I$–$V$ behavior.
- **Signals & systems:** Continuous vs. discrete time, LTI properties (linearity, time-invariance, causality, BIBO stability), convolution, Fourier/Laplace/z-transforms, sampling & aliasing.
- **Control systems:** Open- vs. closed-loop feedback, transfer functions, poles/zeros, transient vs. steady-state response, stability margins & trade-offs.
- **Embedded systems:** Memory-mapped registers, GPIO, timers/PWM, ADC/DAC, interrupts vs. polling, `volatile`/concurrency hazards, peripheral buses (SPI/I2C/UART).
- **Electrical machines & Power systems:** Electromagnetic induction, Faraday/Lorentz laws, torque/speed curves, efficiency/losses, three-phase phasors, generation/transmission, protection & safety boundaries.
