# Subject Theory Profiles & Misconception Catalog

## Purpose

Extend ML-level pedagogical specificity across Computer Science, Mathematics, Natural Sciences, Engineering, Social Sciences, and Humanities in one lean reference. Load only the discipline and topic family relevant to the current request—never force unrelated obligations into a note.

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
- **Chemistry (Atomic, Bonding, Kinetics, Organic, Physical):** Electronic structure, periodicity, bonding & geometry, rate laws vs. thermodynamics, activation barriers, reaction mechanisms, stereochemistry, equilibrium, molecular models.
- **Biology (Cell, Molecular, Genetics, Evolution, Ecology):** Structures, transport, metabolism, regulation, information flow/expression, inheritance/linkage/gene-environment interaction, selection/drift/mutation/gene flow, population dynamics & energy/matter flow.

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

Place relevant clarifications inline right beside the concept where confusion arises (per [pedagogical-intelligence.md](../../procedures/authoring/pedagogical-intelligence.md)). Expand through authoritative teaching sources when needed; never fabricate statistics about how often learners make a mistake.

### Computer Science
- **Pointer vs. pointed-to value:** Memory address vs. dereferenced object.
- **Concurrency vs. parallelism:** Overlapping logical progress vs. simultaneous physical execution.
- **Process vs. thread:** Isolated resource ownership vs. shared-address execution context.
- **Stack vs. heap:** Scoped automatic lifetime vs. dynamic allocation (noting language differences).
- **Time complexity vs. wall-clock runtime:** Asymptotic growth rate vs. constant factors and hardware effects.
- **Authentication vs. authorization:** Verifying identity vs. granting permissions.
- **TLB miss vs. page fault:** Translation-cache miss (page still in RAM) vs. unmapped/non-resident page fault.
- **Bandwidth vs. latency:** Transfer capacity per unit time vs. end-to-end delay.
- **Database isolation vs. atomicity:** Visibility of concurrent transactions vs. all-or-nothing commit/rollback.

### Mathematics & Statistics
- **Function vs. equation:** Input-to-output mapping vs. equality constraint to solve.
- **Continuity vs. differentiability:** Unbroken behavior vs. well-defined local linear slope.
- **Necessary vs. sufficient:** Direction of logical implication ($A \Rightarrow B$ vs. $B \Rightarrow A$).
- **Local vs. global optimum:** Best within a neighborhood vs. best across the entire feasible domain.
- **Independent vs. mutually exclusive:** $P(A \cap B) = P(A)P(B)$ vs. disjoint events ($P(A \cap B) = 0$).
- **Correlation vs. causation:** Statistical association vs. causal interventional effect.
- **Probability density vs. probability:** Density value $f(x)$ (can exceed 1) vs. integrated area over an interval.
- **$p$-value vs. $P(H_0 \mid \text{data})$:** Conditional probability of data as extreme under $H_0$, not the probability that $H_0$ is true.
- **Numerical evidence vs. proof:** Examples check plausibility; they do not establish universal truth.

### Natural Sciences
- **Heat vs. temperature:** Energy transfer driven by temperature difference vs. thermodynamic state variable.
- **Mass vs. weight:** Inertial/gravitational matter property vs. gravitational force.
- **Velocity vs. acceleration:** Rate of position change (with direction) vs. rate of velocity change.
- **Energy vs. power:** Total work/energy quantity vs. rate of energy transfer per unit time.
- **Chemical equilibrium vs. stopped reaction:** Dynamic balance of equal forward/reverse rates vs. zero reaction.
- **Reaction rate vs. thermodynamic favorability:** Kinetics (barrier height) vs. thermodynamics ($\Delta G$).
- **Gene vs. allele:** Functional locus/sequence unit vs. specific variant at that locus.
- **Respiration vs. breathing:** Cellular ATP-generating biochemistry vs. mechanical gas ventilation.
- **Evolution vs. individual adaptation:** Population allele-frequency change across generations vs. individual physiological response.

### Humanities & Social Sciences
- **Demand vs. quantity demanded:** Entire price-quantity relationship (curve) vs. quantity at one price.
- **Nominal vs. real value:** Current monetary units vs. inflation-adjusted purchasing power.
- **Economic growth vs. development:** Output expansion (GDP) vs. broader structural and welfare outcomes.
- **Chronology vs. causality:** Temporal precedence (*post hoc*) vs. demonstrated causal mechanism.
- **Primary vs. secondary evidence:** Contemporary/direct artifact of the subject vs. later scholarly analysis.
- **Valid vs. sound argument:** Logically valid form vs. valid form with true premises.
- **Descriptive vs. normative claim:** What *is* observed vs. what *ought* to be valued or done.
