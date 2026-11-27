# Subject Theory Profiles & Misconception Catalog

## Activation & Non-Activation

- **When to load:** Load selectively **only** when:
  1. The active subject is `general` or lacks a dedicated blueprint under `docs/blueprints/subjects/*.md` (e.g., Humanities, Social Sciences, or Engineering topics outside `electrical.md`),
  2. An unfamiliar or cross-disciplinary topic needs the Cross-Discipline Pedagogical Equivalence Table or a secondary topic-family checklist not covered by the loaded `subjects/<p>.md` blueprint(s), or
  3. An `M6` assessment ([assessment.md](../formats/assessment.md)) constructs misconception-sensitive MCQ distractors.
- **When NOT to load:** Skip whenever loaded primary/secondary blueprints under `docs/blueprints/subjects/*.md` (such as [machine-learning.md](../subjects/machine-learning.md), [biology.md](../subjects/biology.md), or [chemistry.md](../subjects/chemistry.md)) already govern the active curriculum and misconceptions, or during compact `M3` formula/reference routes.

## Purpose

Extend ML-level pedagogical specificity across Computer Science, Mathematics, Natural Sciences, Engineering, Social Sciences, and Humanities without forcing unrelated obligations or duplicating primary subject blueprints. Load only the matching discipline and topic family.

## 1. Cross-Discipline Pedagogical Equivalence

Apply equivalent rigor to each discipline's central mechanisms (pedagogical counterparts, not claims of mathematical equivalence):

| ML Pedagogical Move | Algorithms Equivalent | Physics Equivalent | Biology Equivalent |
|---|---|---|---|
| Dataset walkthrough | Concrete input trace | Physical system setup | Biological system / organism context |
| Model architecture | Data representation & invariants | Physical model & idealizations | Structural organization |
| Loss function explanation | Problem objective & correctness | Governing physical relationship | Functional / fitness outcome |
| Gradient update trace | State transition trace | Change in physical quantities | Molecular or cellular transition |
| Convergence analysis | Termination & correctness proof | Equilibrium / steady-state analysis | Regulation / homeostasis dynamics |
| Hyperparameter sensitivity | Algorithm configuration | Parameter / boundary dependence | Environmental / regulatory influence |
| Generalization | Validity across input classes | Model validity regime | Generalizability across contexts |
| Regularization trade-offs | Time/space resource trade-offs | Approximation trade-offs | Physiological / evolutionary trade-offs |
| Model failure analysis | Invalid preconditions / edge cases | Breakdown of idealization | Disruption of biological function |

## 2. Selectable Topic-Family Theory Completeness Catalogue

Use the matching topic family as a **selectable checklist** during [curriculum discovery](../../procedures/authoring/curriculum-discovery.md)—include only what fits the note's scope, but do not silently omit core pillars of the requested topic:

### Computer Science
- **Programming fundamentals:** Types, evaluation order, control flow, scope, binding, state.
- **Memory management:** Allocation, lifetime, aliases, ownership, invalid access.
- **Object-oriented programming:** State, behavior, abstraction, dispatch, composition vs. inheritance.
- **Functional programming:** Pure functions, composition, immutability, closures, evaluation strategy.
- **Data structures:** Representation, operations, invariants, complexity & memory trade-offs.
- **Algorithms:** Correctness, termination, complexity, invariants, alternative approaches.
- **Operating systems:** Abstractions, isolation, address translation, resource management, concurrency.
- **Computer architecture:** Instruction semantics, datapaths, control, pipelining, memory hierarchy.
- **Databases:** Data models, integrity constraints, query semantics, transactions/ACID, storage/indexing.
- **Networking:** Protocol semantics, encapsulation, state machines, latency/bandwidth, partial failure.
- **Compilers:** Lexing, parsing, semantic analysis, IR, optimization, code generation.
- **Distributed systems:** Coordination, partial failure, time/ordering, consistency, replication.
- **Cybersecurity:** Threat models, trust boundaries, security properties, defensive mechanisms.
- **Software engineering:** Requirements, abstraction boundaries, coupling/cohesion, testing, maintenance.
- **Computer graphics:** Coordinate systems, transformations, projection, rasterization/rendering.

### Mathematics
- **Arithmetic & Algebra:** Number representations, operations, equivalence transformations, solution conditions.
- **Calculus:** Limits, continuity, rates of change, accumulation, approximation & error.
- **Linear algebra:** Vector spaces, linear transformations, basis, rank, eigenvalues/invariance.
- **Probability & Statistics:** Sample spaces, events, distributions, dependence, sampling, estimation, uncertainty, inference.
- **Discrete mathematics:** Logic, quantifiers, proof techniques, induction, discrete structures.
- **Differential equations:** Governing relationships, initial/boundary conditions, qualitative & analytical solution behavior.
- **Real & Complex analysis:** Rigorous definitions, convergence, counterexamples, analyticity, contour reasoning.
- **Abstract algebra:** Algebraic structures, axioms, operations, structure-preserving maps.
- **Numerical analysis & Optimization:** Approximation, conditioning, stability, error bounds, objectives, feasible regions, optimality conditions, convergence.

### Natural Sciences
- **Mechanics:** Reference frames, forces, motion, energy, momentum, conservation laws.
- **Thermodynamics:** Systems, state variables, processes, energy conservation, entropy, irreversibility.
- **Electromagnetism:** Charges, fields, potentials, interactions, governing laws.
- **Waves & Optics:** Oscillation, superposition, propagation, interference, diffraction.
- **Quantum mechanics:** States, observables, measurement, probabilistic predictions, uncertainty.
- **Chemistry & Biology:** Owned canonically by [chemistry.md](../subjects/chemistry.md) and [biology.md](../subjects/biology.md) (atomic/molecular structure, thermodynamics vs. kinetics, catalysis, regulation, evolution, cellular pathways); consult those blueprints directly when active rather than duplicating their checklists here.

### Engineering
- **Circuit theory & Electronics:** Voltage, current, circuit laws, power, equivalent circuits, semiconductor behavior, switching, amplification.
- **Signals, Control & Communications:** Signal representations, transforms, system properties, feedback, stability, response, modulation, channels, noise, information transfer.
- **Materials, Solid & Fluid Mechanics, Heat Transfer:** Structure-property-failure links, loads/stress/strain/constitutive models, flow/pressure/conservation/regimes, conduction/convection/radiation/thermal resistance.
- **Robotics:** Kinematics, dynamics, sensing, estimation, control, uncertainty.

### Humanities & Social Sciences
- **Microeconomics & Macroeconomics:** Choice, incentives, constraints, market structure, equilibrium, aggregate quantities, institutions, dynamics, policy.
- **Psychology & Sociology:** Constructs, mechanisms, measurements, evidence, social structures, institutions, theoretical perspectives.
- **Political science:** Power, institutions, governance, political behavior.
- **History:** Chronology, primary vs. secondary sources, context, causation, competing interpretations.
- **Philosophy:** Problems, concepts, arguments, validity vs. soundness, objections, alternatives.
- **Literature, Linguistics & Geography:** Language/structure/context/interpretation; phonology/morphology/syntax/semantics/pragmatics; spatial relationships, scale, human-environment interaction.

## 3. Discipline-Specific Misconception Library

Place relevant clarifications inline beside the concept where confusion arises using the canonical 5-step internal misconception diagnosis and placement workflow in [pedagogical-intelligence.md](../../procedures/authoring/pedagogical-intelligence.md).

### Computer Science
- **Pointer vs. pointed-to value:** Memory address vs. dereferenced object.
- **Concurrency vs. parallelism:** Overlapping logical progress vs. simultaneous physical execution.
- **Process vs. thread:** Isolated resource ownership vs. shared-address execution context.
- **Stack vs. heap:** Language storage-duration/lifetime semantics vs. implementation-dependent memory placement (noting compilers may optimize or escape-allocate objects).
- **Time complexity vs. wall-clock runtime:** Asymptotic growth rate vs. constant factors and hardware effects.
- **Authentication vs. authorization:** Verifying identity vs. granting permissions.
- **TLB miss vs. page fault:** A TLB miss means only that the translation is not cached in the TLB—the subsequent page-table lookup may resolve to a valid resident page with no fault; a page fault occurs when lookup fails (non-resident/unmapped page, **permission violation**, or architecture-specific fault).
- **Bandwidth vs. latency:** Transfer capacity per unit time vs. end-to-end delay.
- **Database isolation vs. atomicity:** Visibility of concurrent transactions vs. all-or-nothing commit/rollback.

### Mathematics & Statistics
- **Function vs. equation:** Input-to-output mapping vs. equality statement (which may express a definition, identity, relationship, or constraint to solve).
- **Continuity vs. differentiability:** Unbroken behavior vs. well-defined local linear slope.
- **Necessary vs. sufficient:** Direction of logical implication: if $A \Rightarrow B$, then $A$ is **sufficient** for $B$, and $B$ is **necessary** for $A$.
- **Local vs. global optimum:** Best within a neighborhood vs. best across the entire feasible domain.
- **Independent vs. mutually exclusive:** $P(A \cap B) = P(A)P(B)$ vs. disjoint events ($P(A \cap B) = 0$).
- **Correlation vs. causation:** Statistical association vs. causal interventional effect.
- **Probability density vs. probability:** Density value $f(x)$ (can exceed 1) vs. integrated area over an interval.
- **$p$-value vs. $P(H_0 \mid \text{data})$:** Probability, assuming $H_0$ is true, of observing a **test statistic** at least as extreme as the observed value under the null distribution—not the probability that $H_0$ is true.
- **Numerical evidence vs. proof:** Examples check plausibility; they do not establish universal truth.

### Natural Sciences
- **Heat vs. temperature:** Energy transfer driven by temperature difference vs. thermodynamic state variable.
- **Mass vs. weight:** Inertial/gravitational matter property vs. gravitational force.
- **Velocity vs. acceleration:** Rate of position change (with direction) vs. rate of velocity change.
- **Energy vs. power:** Total work/energy quantity vs. rate of energy transfer per unit time.
- **Chemistry & Biology misconceptions:** Canonical misconceptions (equilibrium vs. stopped reaction, kinetics rate vs. $\Delta G$, gene vs. allele, cellular respiration vs. mechanical breathing, population evolution vs. individual adaptation) are owned by [chemistry.md](../subjects/chemistry.md) and [biology.md](../subjects/biology.md).

### Humanities & Social Sciences
- **Demand vs. quantity demanded:** Entire price-quantity relationship (curve) vs. quantity at one price.
- **Nominal vs. real value:** Current monetary units vs. inflation-adjusted purchasing power.
- **Economic growth vs. development:** Output expansion (GDP) vs. broader structural and welfare outcomes.
- **Chronology vs. causality:** Temporal precedence (*post hoc*) vs. demonstrated causal mechanism.
- **Primary vs. secondary evidence:** Contemporary/direct artifact of the subject vs. later scholarly analysis.
- **Valid vs. sound argument:** Logically valid form vs. valid form with true premises.
- **Descriptive vs. normative claim:** What *is* observed vs. what *ought* to be valued or done.
