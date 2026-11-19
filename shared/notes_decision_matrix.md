# Study-note decision matrices

Use this guide for every built-in note template. The [routing index](note_decision_matrix.md) selects the route, and its template describes the section gates. The detailed decisions here apply across routes. Use KEEP when a section serves its role as written, ADAPT when its form or depth needs to change, MERGE when useful content belongs beside another explanation or a verified link, and OMIT when it adds no value. Remove any empty headings left by an omission.

Resolve conflicts in order. Follow the explicit request and verified output contract, preserve source fidelity and visible access limits, respect the route and its source sequence, choose detail that serves the outcome, then eliminate duplication. Keep the decision record in planning state.

The following mapping retains the established DM anchors. Some decisions use more than one existing matrix.

| Requested decision | Established matrices |
|---|---|
| DM-01 Scope; DM-02 Reader; DM-03 Outcomes | DM-01, DM-02, DM-03 respectively |
| DM-04 Source access; DM-05 Provenance | DM-05 for both |
| DM-06 Explanation structure | DM-04, DM-10 |
| DM-07 Math inclusion; DM-08 Math depth and calculus; DM-09 Notation | DM-06; DM-07 and DM-08; DM-09 respectively |
| DM-10 Examples; DM-11 Analogies and visuals | DM-11; DM-12 and DM-13 respectively |
| DM-12 Code inclusion; DM-13 Tool; DM-14 Implementations; DM-15 Verification | DM-14; DM-15; DM-16 and DM-17; DM-18 respectively |
| DM-16 Reference selection; DM-17 Caveats | DM-19 for both, supported by DM-05 for evidence |
| DM-18 Recall; DM-19 Links and footer; DM-20 Cohesion | DM-20 for all three |

## Decision record

Complete this compact record in planning state or a draft-side file, not by publishing unanswered prompts. Record conclusions and concise reasons, not private chain-of-thought. “None, because…” is valid; unresolved information stays explicitly unresolved. Store only the parts useful to the reader in the finished note.

| Field | Record before drafting |
|---|---|
| Topic and target reader | Bounded subject; beginner, familiar/intermediate, advanced/reference, or mixed; relevant existing knowledge. |
| Learning outcome | Observable task(s): explain, calculate, derive, implement, choose/design, verify, debug; what successful performance looks like. |
| Scope | Atomic mechanism, family/comparison, survey, or map of content; what is deferred and why. |
| Track | Conceptual, mathematical, algorithmic, systems, applied, or hybrid; name the essential tracks when hybrid. |
| Prerequisites | Explain locally vs. briefly refresh vs. link; confirm linked notes exist and identify the knowledge needed from each. |
| Source access and order | Full, partial, metadata only, or synthesis. Record consulted passages, access gaps, and source or study sequence. |
| Research need | No external verification, authoritative-source check, current documentation check, or deeper source comparison; list claims and sources to inspect. |
| Math | Domain, requested and effective level, inclusion role or none; structural/logical, operational, derivational, or proof-level; any local depth exception and its purpose. |
| Derivatives/calculus | None, update intuition, scalar derivative, chain-rule derivation, implementation/debugging, or theorem-specific calculus; reason and needed conditions. |
| Example and visual | Case that exposes the mechanism; important intermediate states; visual choice or none, with reason. |
| Code | Purpose or none; language/tool; none, illustrative, from-scratch, standard library/framework, or production-oriented depth; selected layers and why each earns space. |
| Verification | What will be checked, against what reference, with which material environment details; record actual execution status after checking. |
| Alternatives and failures | Choices, invalid assumptions, misconceptions, or operational failures consequential enough to include. |
| Module disposition | Selected, adapted/shortened/merged, omitted, or deferred modules, each with a brief reason and canonical home for overlapping content. |
| Unresolved matters | Missing source/access, unconfirmed behavior, uncertain assumptions, or genuine research questions; impact on the note. |

Keep these axes independent. “Systems” does not mean “little math”; “algorithmic” does not mean “runnable code”; “conceptual” does not preclude quantitative evidence. If the outcome changes, revisit the affected decisions rather than merely adding sections. Automated enforcement lives in `scripts/decision_matrix.py` (`resolve` before writing, `audit` / `validate_note.py` after writing).

## DM-01

**Title:** Topic scope and note architecture. **Purpose:** Choose a coherent unit of learning. **Decision question:** Is the reader learning one mechanism, choosing among relatives, surveying a field, or navigating a learning path?

**Inputs:** User request, source scope, independent outcomes, existing topic map.
**Default:** KEEP one bounded unit before proposing extra notes.
**Precedence:** Source order and verified command scope govern splits.

| Branch / condition | Output / choice | Leave out or link |
|---|---|---|
| One bounded mechanism or claim with one usable outcome | Atomic-mechanism note; explain it at the required depth, even if lengthy. “Atomic” here is a scope, not the separate short `atomic.md` template. | Independent prerequisite lessons and unrelated variants. |
| Related methods must be distinguished or selected | Family/comparison note with shared axes, common model, and conditional selection rules. | Full implementation or derivation of every member; link child notes. |
| Reader needs representative coverage and synthesis of a field | Survey organized by questions/taxonomy, with evidence-backed coverage boundaries and representative cases. | Pretending shallow coverage establishes mastery of each mechanism. |
| Source sequence carries the reasoning | KEEP a source walkthrough with verified locators and claims in sequence. | Imposing a textbook sequence on a source-led note. |
| Reader needs navigation, dependencies, or study sequence | Map of content with scope, prerequisites, linked note roles, and meaningful ordering. | Repeating child-note explanations. |
| One note contains independently reusable outcomes or conflicting reader baselines | Split those units and keep an overview only if it connects them. | Splitting merely to meet a length quota. |

**Example of change:** “Choose an optimizer” becomes a family comparison with links to update derivations; “trace one SGD update” stays one mechanism note.

## DM-02

**Title:** Reader baseline and prerequisites. **Purpose:** Supply enough foundation without reteaching a subject. **Decision question:** What must this reader know at the point of use?

**Inputs:** Audience description, existing notes, expected task.
**Default:** ADAPT with a short local definition of essential concepts.
**Precedence:** DM-03 determines which prerequisites matter.

| Branch / condition | Output / choice | Leave out or link |
|---|---|---|
| Beginner lacks a concept used in the central explanation | Explain its minimal meaning and a small case before using it; introduce relevant symbols/units/shapes at use. | A whole prerequisite chapter if a usable existing note covers it. |
| Familiar/intermediate reader needs a reminder | Brief refresh of the exact fact, convention, or relation being used. | Full foundational derivation. |
| Advanced/reference reader already knows the foundation | State nonstandard conventions, assumptions, interfaces, and exceptional conditions. | Beginner analogy and generic glossary. |
| Mixed readers need different depths | Accessible core plus linked or optional deeper treatment with clear prerequisites. | Interleaving repeated beginner and advanced explanations. |
| Missing prerequisite is large or independently useful | Link its verified existing note and specify the needed section/skill; if unavailable, explain the essential minimum or explicitly mark the dependency as unresolved. | A fabricated wikilink or unsupported claim that the reader is ready. |

**Example of change:** A NumPy broadcast-debugging note refreshes axis alignment and shows one mismatched shape; it does not repeat an entire linear-algebra course.

## DM-03

**Title:** Learning outcome. **Purpose:** Make content selection accountable to a reader capability. **Decision question:** What should the reader be able to do afterward, and what would demonstrate it?

**Inputs:** Requested task, available evidence, learner baseline.
**Default:** KEEP a bounded explanation and one observable check.
**Precedence:** DM-02 and DM-05 decide feasibility.

| Branch / outcome | Output / choice | Leave out unless separately justified |
|---|---|---|
| Explain | Definition, mechanism, distinction, and a causal or conceptual self-check. | Full code and proof. |
| Calculate | Operational relation, symbol/domain treatment, worked substitution and interpretation. | Derivation not needed to apply it correctly. |
| Derive | Target result, assumptions, named-rule steps, and transfer to a modified case. | Framework tours. |
| Implement | Contract, algorithm/interface, chosen code depth, and observable verification. | Unrelated provenance/history. |
| Choose/design | Constraints, matched alternatives, resource/quality trade-offs, and a conditional decision rule. | A universal “best” method or benchmark without context. |
| Verify | Claim and evidence standard, independent check, assumptions, limitations; proof only for a mathematical guarantee. | Treating a passed example as a general guarantee. |
| Debug | Trigger, observable symptom, isolating trace/check, cause, correction, and regression check where useful. | An exhaustive error catalog. |
| Several outcomes are essential | Name them separately and select only the union of necessary modules; split if each needs an independent lesson. | Assuming “deep” means all outcomes. |

**Example of change:** Identifying neural-network parts selects definitions and a forward diagram; deriving parameter updates selects calculus and a tiny computation graph instead.

## DM-04

**Title:** Knowledge track. **Purpose:** Choose the explanatory structure without deciding math or code depth. **Decision question:** What kind of object or relationship carries the explanation?

**Inputs:** Mechanism, causal evidence, algorithm steps, comparisons, proof goal.
**Default:** KEEP a direct explanation and one discriminating example.
**Precedence:** DM-03 selects the primary structure, then DM-06 and DM-14 select math and code independently.

| Branch / track | Output / choice | Leave out or link |
|---|---|---|
| Conceptual | Meaning, distinctions, causal argument, representative cases, evidence when needed. | Invented equations or invariants. |
| Mathematical | Definitions, conditions, relations, examples; derivation/proof only at the selected depth. | Unrequested implementation. |
| Algorithmic | Input/output contract, state, recurrence or steps, termination/correctness conditions, resource model when useful. | Runnable code if pseudocode/trace fulfills the goal. |
| Systems | Components, interfaces, lifecycle, data/control flow, concurrency/failure behavior where material. | Forced four-stage pipelines. |
| Applied | Task constraints, workflow, evaluation, decision points, and operational caveats. | General theory that changes no action. |
| Hybrid | Combine the named essential structures and explicitly connect them at their interfaces. | Duplicating an entire conceptual lesson and entire coding lesson. |

**Example of change:** A queueing-based service design note combines systems structure with operational or derivational math and a simulation if it tests a design decision.

## DM-05

**Title:** Research and source strategy. **Purpose:** Match verification effort to claims and uncertainty. **Decision question:** Which claims require external support, currentness, or comparison?

**Inputs:** Assigned sources, accessible excerpts, timestamps, source claims, dates.
**Default:** ADAPT to the material actually accessible and mark the gap.
**Precedence:** Preserve source sequence and claim-level provenance before adding support.

| Branch / research need | Output / choice | Leave out or label |
|---|---|---|
| Complete assigned source | KEEP its sequence and attach exact page, heading, or timestamp locators at claims and examples. | Rearranging it or mixing in unmarked additions. |
| Partial assigned source | ADAPT to the passages or segments actually available. State known coverage and gaps. | Inferring what a missing segment says or fabricating locators. |
| Metadata only | KEEP bibliographic identification and a specific access limitation. Request material when faithful treatment depends on it. | Attributing substantive claims or detailed learning outcomes. |
| Several consulted references | ADAPT around an identified anchor or name the synthesis order. Label independent findings, interpretations, and added illustrations. | Presenting the synthesis as one source's sequence. |
| No assigned source | ADAPT to a declared study outline and identify only inspected references. | Implying the outline came from a source. |
| No external verification needed | Use supplied inspected material, an explicitly stated model, or self-contained reasoning for stable claims; distinguish a constructed example from evidence about the world. | New historical, empirical, disputed, or mutable claims masquerading as established facts. |
| Authoritative-source check | Inspect an original paper, authoritative textbook, official standard, or relevant primary source; record the precise passage/result and conditions. | A snippet or abstract as support when the full claim is elsewhere. |
| Current documentation check | Inspect official docs for the actual library/runtime/standard version; record version or access date as relevant. | Guessing behavior from another version or from remembered tutorials. |
| Deeper source comparison | Compare primary sources when results conflict, a survey synthesizes evidence, or a consequential design conclusion depends on context; record differing definitions, methods, populations, or assumptions. | Counting sources as agreement without comparing what they establish. |
| Historical attribution or empirical measurement occurs in any branch | Verify the attribution from primary/reputable scholarly evidence; for measurements preserve task, dataset/population, baseline, metric, uncertainty, and setup. | Unsourced origin stories, performance numbers, or causal conclusions. |
| Source is inaccessible or weak | State the specific access/support gap; narrow or omit the claim, or label it `[UNVERIFIED]`. | Fabricated quotations, inspected-status claims, page numbers, or transcript contents. |

The overall research label summarizes the highest needed effort, but verification stays claim-specific. Cite beside the supported claim. Separate source findings, one's own measurements, and synthesis/inference. A source list is not evidence that its contents were inspected.

**Example of change:** With only two transcript segments, keep their verified locators in sequence and record the gap. A symbolic recurrence under stated assumptions may require no new browsing; a current framework API comparison requires versioned official docs, and a throughput claim requires an actual benchmark setup.

## DM-06

**Title:** Math inclusion gate. **Purpose:** Decide whether notation earns space. **Decision question:** Does math define, quantify, predict, support a decision, or check something the reader needs?

**Inputs:** Learning outcome, required computations, relevant validity conditions.
**Default:** OMIT displays and use prose.
**Precedence:** Apply DM-07 for the allowed depth and DM-09 for definition and placement.

| Branch / role | Output / choice | Leave out |
|---|---|---|
| Defines the object or mechanism | State the minimal defining relation and its meaning; select depth separately with DM-07. | Automatic derivation merely because an equation exists. |
| Quantifies behavior or resource use | Provide the model, inputs, units/shape, assumptions, and interpretable result. | Precision the model or evidence does not support. |
| Determines a design or selection decision | Show the inequality, objective, bound, or threshold and how it changes the choice. | Unused formalism. |
| Helps verify behavior | Show a relevant shape, dimension, normalization, sign, or numerical check. | Calling that check a proof. |
| Formal detail serves only a secondary outcome | MERGE a link to a verified treatment if useful. | Extra equations without work for the reader to do. |
| None of these roles applies | Omit equations; structural/logical reasoning may be sufficient. | Decorative notation or a blank math heading. |

For each equation, ask whether removing it prevents the reader from understanding an essential defining relation, computing a required value, tracing an update, or checking a bound. Keep it only when the answer is yes.

**Example of change:** An architecture-identification note may name layers without calculus; a memory-budget note includes parameter/storage arithmetic even though its track is systems.

## DM-07

**Title:** Independent mathematical depth. **Purpose:** Match mathematics to each concept's objective. **Decision question:** Does this learner need awareness, a formula, application, derivation or proof?

**Inputs:** Learning objectives, source obligations, prerequisites and explicit profile.
**Default:** Lowest sufficient local depth; no subject-wide cap for deep study.
**Precedence:** Explicit goals and source fidelity precede defaults.

New deep plans use per-concept M0?M5 from the [depth table](../references/adaptive-engine.md#selection-and-depth). Do not infer proof from ?exhaustive?, suppress a needed derivation because the title says implementation, or impose display-equation quotas. The legacy CLI `math_level` 0/1/2/3 remains an adapter to M0/M3/M4/M5. Structured concepts can vary within a note. Ordinary code, theory, visual and assessment levels remain independent.

Existing saved contracts retain their former checks on resume; source-study and compact routes retain their existing CLI range and validation. New deep plans store `contract_version: 2` and use semantic review for mathematical sufficiency, without whole-document equation counts or mandatory proof headings. Display each central relation once where it is explained.

**Example of change:** One gradient-descent lesson uses M1 for motivation, M3 for loss calculation and M4 for update derivation; convergence proof is M5 only when requested.

## DM-08

**Title:** Derivative/calculus gate. **Purpose:** Prevent calculus from being forced into architecture or prediction lessons. **Decision question:** Is local change, parameter learning, gradient correctness, or a calculus-based guarantee part of the outcome?

**Inputs:** Forward or backward computation, parameter updates, differentiability.
**Default:** OMIT derivatives.
**Precedence:** Use only derivatives necessary at the effective DM-07 depth.

| Branch / learning goal | Output / choice | Leave out or link |
|---|---|---|
| Identify network parts or trace a forward pass/prediction | No derivatives; compute forward operations and interpret output. | Loss gradients, chain-rule calculations, and an optimizer detour. |
| Explain ordinary gradient-descent training at a high level | Gradient as local sensitivity; update direction, learning-rate role, and distinction between loss and prediction. | Full network derivatives. |
| Calculate a simple parameter update | Small scalar derivative with its independent variable, fixed quantities, evaluation point, and sign interpretation. | Large Jacobians and framework boilerplate. |
| Derive backpropagation | Tiny network/computation graph; local derivatives, chain rule along paths, sum of contributions for shared dependencies, and update interpretation. | A large numerical trace that hides the chain rule. |
| Implement/debug gradients | Explicit shapes/axes and reduction conventions, accumulation, nondifferentiable points, and numerical gradient checks at suitable smooth points with justified tolerances. | Declaring agreement at one point a proof of correctness. |
| Prove a calculus-dependent theorem | Only the differentiability, smoothness, convexity, or other assumptions used by that theorem; show where they enter the argument. | Claiming those assumptions for every neural network or training process. |
| Operation is discrete, nonsmooth, or optimized without derivatives | Explain the relevant convention, subgradient, surrogate, estimator, or derivative-free method only if needed. | Pretending an ordinary derivative exists everywhere. |

A neural-network forward pass/inference does not require derivatives. Ordinary gradient-descent training uses derivatives of the loss to update parameters; backpropagation computes those derivatives by applying the chain rule through the computation graph. A forward pass performed while recording a graph is still a forward computation, not a derivative calculation. [PyTorch autograd documentation](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) supports this forward/backward distinction.

**Example of change:** A prediction trace stops after weighted sums and activations. A training-debugging note adds loss reduction, gradient shapes, and a finite-difference check away from activation kinks.

## DM-09

**Title:** Equation and symbol treatment. **Purpose:** Make central equations understandable and valid without repeated tables. **Decision question:** What must the reader know to interpret and apply this relation here?

**Inputs:** Governing equation, variables, domains, units, shapes and assumptions.
**Default:** ADAPT to inline definitions and one relevant check.
**Precedence:** DM-06 and DM-07 govern equation inclusion and depth.

| Branch / need | Output / choice | Leave out or link |
|---|---|---|
| Central equation defines/predicts something | State the question it answers; show the relation, define unfamiliar symbols/operators, explain assumptions, work a small example or derivation, interpret the result, and check a relevant property. | Equation previews repeated in multiple sections. |
| Few symbols, meanings obvious after definition | Define inline beside first use, including index ranges and conventions when they matter. | Mandatory symbol table. |
| Dense or reused notation | One compact symbol table near the first central use; distinguish scalars, vectors, matrices, axes, shapes, units, domains, and fixed vs. variable quantities as applicable. | Directional sensitivity columns that do not teach anything. |
| Validity depends on a condition | State it beside the relation: e.g., nonzero denominator, positive logarithm argument, invertibility, independence, or an approximation regime. | A generic condition checklist with irrelevant cases. |
| Misuse is revealed by a specific check | Check dimensions/units for physical relations, compatible shapes for arrays, normalization/support for probabilities, or a meaningful sign/boundary. | Universal zero, ±1, ties, and infinity tables. |
| Routine expression only applies established notation | Explain the operation at the required reader level and reference the central definition. | Repeating the entire equation protocol. |

Apply [rendering rules](authoring_rules.md#rendering). Use one canonical display of a relation; later substitutions or derived relations are new work, not a second summary of the same equation.

**Example of change:** A probability normalization formula states its support and nonzero normalizer; a matrix multiplication states compatible dimensions. Neither receives an irrelevant “tie” test.

## DM-10

**Title:** Derivation granularity. **Purpose:** Show enough reasoning to reproduce important transitions. **Decision question:** Which step would this reader otherwise have to guess?

**Inputs:** Target result, baseline, known identities and meaningful transitions.
**Default:** MERGE a short justification at the first non-obvious step.
**Precedence:** DM-07 gates derivation and proof.

| Branch / transition | Output / choice | Leave out or link |
|---|---|---|
| Routine arithmetic/rearrangement within the baseline | Compress; expand a representative step if needed. | A “why” paragraph for every arithmetic operation. |
| Chain rule, identity, inequality, expectation rule, induction, or invariant argument | Name the rule, identify its operands/hypotheses, and show the significant intermediate relation. | An unexplained jump with a rule name pasted after it. |
| Division, cancellation, logarithm, inverse, square root, interchange of limits/sums/derivatives | State the actual domain/nonzero/regularity condition needed for this step. | Generic “assume valid” language. |
| Approximation or one-way implication replaces equality/equivalence | Mark it correctly and explain lost direction or approximation conditions. | Reversible arrows for irreversible reasoning. |
| Proof is outside the outcome | State the usable result and relevant conditions; link a proof when available. | Proof-shaped filler. |

**Example of change:** A backpropagation derivation expands the chain rule and shared-path sum, while compressing arithmetic substitution after the learner knows the rule.

## DM-11

**Title:** Example and trace design. **Purpose:** Expose mechanism with minimal bookkeeping. **Decision question:** What small case makes the important decision or transformation visible?

**Inputs:** Source examples, intended task, fixture inputs and edge conditions.
**Default:** KEEP one small labeled illustration if it closes a comprehension gap.
**Precedence:** DM-05 governs attribution, and DM-18 governs verification.

| Branch / mechanism | Output / choice | Leave out |
|---|---|---|
| Numerical transformation | Small distinct, often asymmetric values; trace the intermediate quantities that explain the output. | Large random datasets and repeated arithmetic. |
| Tensor/index/broadcast behavior | Small unequal dimensions or distinct entries that expose axis alignment; show shapes and selected entries. | Equal dimensions that accidentally hide a transpose/broadcast error. |
| Search, recurrence, protocol, lifecycle | Minimal state/event sequence that exercises the relevant branch, termination, or recovery; show state changes. | Every possible path. |
| Conceptual distinction or empirical argument | Representative case plus a near miss/counterexample if it reveals the boundary; separate constructed illustration from observed evidence. | Treating an anecdote as a measured general result. |
| Shared mechanism across math and code | Define the case once and keep names, values, assumptions, and outputs consistent. | Reintroducing full input tables at each layer. |
| Survey or family has incompatible mechanisms | Use distinct named cases or linked examples with explicit roles. | Forcing one “running example” to fit everything. |

Mark a borrowed example with a verified locator. Label an original teaching example as an added illustration. MERGE an integrated problem into the sequential explanation when it would interrupt the source order elsewhere. OMIT an example if it repeats a trace.

**Example of change:** A tensor note uses a small rectangular input to expose axes instead of a square matrix whose mistaken transpose is hard to notice.

## DM-12

**Title:** Analogy decision. **Purpose:** Improve intuition without importing false properties. **Decision question:** Does a familiar relation predict the specific unfamiliar behavior better than a direct case?

**Inputs:** Proposed analogy and its point of failure.
**Default:** OMIT analogy and explain directly.
**Precedence:** DM-11 tests whether an example already works.

| Branch / condition | Output / choice | Leave out |
|---|---|---|
| A useful relation transfers cleanly | Short analogy, explicit mapping, and adjacent limit: what the reader must not infer. | Unmapped metaphor and decorative story. |
| Some parts map, but a central property differs | Restrict the analogy to the useful part and demonstrate the mismatch; use a direct model for the rest. | Letting intuition overrule the definition. |
| Topic is concrete or metaphor creates more misconceptions | Omit analogy; use a real example, definition, or diagram. | A compulsory analogy heading. |
| Confusion is between nearby formal concepts | Prefer contrasting cases on shared dimensions. | Unrelated everyday imagery. |

**Example of change:** A memory-ownership note uses an ownership/lifetime trace if a borrowing metaphor would falsely imply shared mutable access.

## DM-13

**Title:** Visual selection. **Purpose:** Match a visual to the relationship it clarifies. **Decision question:** Which relation is costly to reconstruct from prose alone?

**Inputs:** Spatial geometry, data or control flow, comparative structure.
**Default:** OMIT a visual if prose is sufficient.
**Precedence:** Use a verified or generated figure for spatial geometry under the rendering rules.

| Branch / relation | Output / choice | Leave out |
|---|---|---|
| Data/control flow or branching | Flowchart; use sequence diagram when actor-to-actor message order is the point. | Fake pipeline stages. |
| Discrete states and legal transitions | State diagram or transition table, with triggers/guards. | Treating simultaneous components as successive states. |
| Matrix/tensor axes, broadcasting, indexing, memory layout | Grid with axes, dimensions, representative entries, or offsets. | Decorative boxes with missing axis meaning. |
| Recursion or alternative search paths | Search/call tree with expansion order or pruning reason. | Huge unreadable trees. |
| Temporal order changes the explanation | Timeline with sourced dates or a task-relative event order. | Mandatory history. |
| Alternatives differ on shared decision criteria | Comparison table with consistent axes. | A table repeating the paragraph verbatim. |
| Spatial/geometry relation, physics schematic, function plot, or ML decision boundary is central | Real `.png`/`.svg` diagram saved under `assets/<topic>/` and embedded with `![[...]]` (extracted open-license source figure or clean Matplotlib/SVG plot; never raw ASCII `text` art or a `mermaid flowchart TD` box chain). | Unreadable ASCII art or `mermaid flowchart` substituting for geometry. |
| Prose or a small trace already makes the relation clear | No diagram. | A visual required by component count. |

Apply [rendering rules](authoring_rules.md#rendering); explain the inference beside the visual. Select the visual only for its teaching purpose.

**Example of change:** A retry protocol gets a state diagram, and broadcast rules get a tensor grid. A wavefront refraction explanation uses an embedded figure with the interface, normal, rays, and their angles. A simple definition can use prose alone.

## DM-14

**Title:** Code inclusion gate. **Purpose:** Select code depth before choosing a language. **Decision question:** What would this code teach, demonstrate, or verify that the rest of the note does not?

**Inputs:** Need to teach internals, use an API, or verify a claim.
**Default:** OMIT runnable code.
**Precedence:** DM-03 selects the goal; non-computing subjects need an explicit simulation request.

> **Hard Non-Computing Subject Rule:** For non-computing subjects (Physics, Chemistry, Biology, Humanities, Pure Mathematics), **default to `None` (no code block)**. Never write Python/NumPy wrappers around closed-form formulas (like Snell's law, kinematics, or equilibrium equations). Include code **only** when the user explicitly requests a simulation/script or when the topic itself is computational modeling. Enforced programmatically by `scripts/decision_matrix.py`.

| Subject family | Code & section policy | Forbidden patterns |
|---|---|---|
| `non-computing` (Physics, Chemistry, Biology, Pure Math, History, Economics, Literature) | Hard-lock `code_depth = "none"`, `language = "none"`, `verification_stack = []`; omit code sections completely. | Python/NumPy wrappers around closed-form laws; CS jargon headings (*"Computational Purpose"*, *"Broader Architecture"*, *"Cross-Architecture Trade-Off"*, *"Executable Verification"*); legacy `<!-- SECTION: S* -->` markers. |
| `computational-science` (explicit numerical simulation/FDTD/Monte Carlo requested) | Allow code only when user explicitly asks for a simulation/script or numerical solver is the learning outcome. | Unrequested runtime claims or toy algebraic assert wrappers. |
| `computing` (CS, DSA, ML engineering, systems, databases, APIs) | Follow `DM-14`–`DM-17` to pick exact language and depth. | Defaulting to Python/NumPy when pseudocode or conceptual prose suffices. |

| Branch / code depth | Output / choice | Leave out or link |
|---|---|---|
| None: code adds no new understanding/evidence | Omit implementation. | A code block added because the topic sounds technical. |
| Illustrative: control flow or one operation is the lesson | Pseudocode or a clearly labeled focused fragment with its contract/expected behavior. | Claiming a fragment is self-contained runnable software. |
| From-scratch: internal construction is the outcome | Transparent implementation exposing relevant operations, with small checks and intentional limitations. | Hidden framework machinery that bypasses the mechanism. |
| Standard library/framework: practical use is the outcome | Minimal idiomatic workflow, inputs/outputs, important configuration, evaluation/checks. | Reimplementing internals the reader does not need. |
| Production-oriented: actual operation/design is the outcome | One realistic implementation path addressing the task's error handling, resource, security, concurrency, observability, or deployment constraints as applicable. | Calling toy code production-ready or adding every conceivable operational concern. |
| Code exists only to check a calculation/model | Small verification script with expected vs. observed results and scope. | Treating numerical agreement as proof. |

**Example of change:** An algorithm explanation uses pseudocode only; a framework-training workflow uses one standard model; a latency-debugging task adds only the profiling code needed to expose the bottleneck.

## DM-15

**Title:** Language/tool selection. **Purpose:** Choose the tool whose behavior matters to the outcome. **Decision question:** Which interface or abstraction must the reader understand or use?

**Inputs:** Domain, user-selected tools, required semantic behavior.
**Default:** KEEP one suitable tool when code is necessary.
**Precedence:** Explicit selections take precedence over the domain defaults.

| Branch / tool | Output / choice | Leave out or caveat |
|---|---|---|
| Language-independent algorithm | Pseudocode with explicit indexing, state, stopping, and relevant tie/ordering conventions. | Pretending it was executed. |
| General logic or lightweight experiment | Python if familiar to the reader and suitable for the task. | Adding numerical libraries without a purpose. |
| Equations-to-arrays, axes, broadcasting, explicit numerical operations | NumPy with relevant shapes and explicit forward/gradient calculations. | Assuming automatic differentiation; NumPy itself does not provide autograd. |
| Standard estimator, preprocessing, evaluation, pipeline | scikit-learn workflow with split and metric appropriate to the task. | Presenting `fit` as an explanation of backpropagation. |
| Tensor computation, autograd, custom model, explicit training loop | PyTorch when these operations or its ecosystem are the target. | Assuming framework use replaces the mathematical explanation. |
| TensorFlow/Keras model construction or training workflow | Use the relevant TensorFlow/Keras API and identify the actual package/backend/version when behavior depends on it. | Treating all Keras configurations as interchangeable with TensorFlow. |
| Ownership, layout, types, concurrency, performance, or a course/task requirement | C, C++, Rust, or Java according to the behavior being taught. | Attributing the same memory model to all four languages. |
| Relational queries or query plans | SQL in the named dialect/engine. | A Python replacement that hides database semantics. |
| Process composition, environment, or deployment commands | Shell for the specified OS/shell, with concrete effects and expected behavior. | Invented portability. |
| Dedicated implementation or explicit ecosystem comparison | Use the saved stack and the fixture shared across its implementations. | Adding unrelated ecosystems or duplicating earlier derivations. |

`numpy.gradient` estimates derivatives of sampled values using finite differences; it is not automatic differentiation through an arbitrary model. [NumPy reference](https://numpy.org/doc/stable/reference/generated/numpy.gradient.html).

For a dedicated implementation note choose one primary tool for the learning objective. Specialty hints provide a fallback (NumPy for transparent numerical updates, Python for algorithm logic, C for layout, SQL for queries, TypeScript for typed web interfaces); explicitly selected tools win. Use scikit-learn for estimator workflows and a tensor framework for tensor/autodiff outcomes. Additional implementations require explicit comparison goals or distinct justified roles. Never automatically generate all specialty frameworks.

**Example of change:** An ownership lesson selects Rust; a database isolation lesson selects SQL; neither receives an obligatory Python implementation.

## DM-16

**Title:** ML implementation ladder. **Purpose:** Select distinct teaching layers without requiring a sequence of frameworks. **Decision question:** Which abstraction levels must this ML lesson expose?

**Inputs:** Intended ML abstraction, selected framework, available fixture.
**Default:** KEEP one implementation or hand trace.
**Precedence:** DM-15 sets the tool and DM-17 justifies additional implementation depth.

| Branch / layer | Output / choice: what it teaches | Leave out unless separately needed |
|---|---|---|
| Hand calculation/pseudocode | Operations without language overhead; small weighted sum, activation, prediction, or update. | Derivatives for a forward-only goal. |
| NumPy | Equations become arrays: axes, shapes, broadcasting, explicit forward pass and manual gradients when selected by DM-08. | Automatic differentiation claims. |
| scikit-learn | Estimator workflow: preprocessing, fitting, prediction, evaluation, and leakage-aware splitting. | A claim that calling `fit` teaches backpropagation, even when the estimator trains using it. |
| PyTorch | Tensor operations, autograd, custom models, explicit loss/backward/update loop when that is the outcome. | A second full manual derivation already taught elsewhere. |
| TensorFlow/Keras | Its model-building, configuration, training, and evaluation workflow; custom gradient/loop detail only if required. | A parallel PyTorch example without a comparison goal. |

Select zero, one, or several layers according to distinct outcomes; the ladder is not a mandatory curriculum. Official capability references: [scikit-learn MLP](https://scikit-learn.org/stable/modules/neural_networks_supervised.html), [PyTorch autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), and [TensorFlow/Keras training and evaluation](https://www.tensorflow.org/guide/keras/training_with_built_in_methods). These sources establish tool behavior; the layer choices are editorial guidance.

**Example of change:** Explaining a prediction uses hand calculation alone. Teaching array-level backpropagation uses hand calculation plus NumPy. Learning a Keras workflow uses Keras without compulsory NumPy, scikit-learn, or PyTorch versions.

## DM-17

**Title:** Number and depth of implementations. **Purpose:** Justify each implementation and make comparisons meaningful. **Decision question:** Does another implementation reveal a different abstraction or answer an explicit comparison question?

**Inputs:** Proposed stack, common fixture and distinct teaching roles.
**Default:** OMIT additional implementations without a separate teaching role.
**Precedence:** Reproduce each required stack under DM-18.

| Branch / condition | Output / choice | Leave out or link |
|---|---|---|
| One task and one relevant abstraction | One implementation at DM-14's chosen depth. | Automatic “first-principles plus idiomatic” duplication. |
| Distinct internal-mechanism and practical-workflow outcomes | Matched layers with a short statement of what each exposes and hides. | Repeating shared setup and explanation. |
| Language/framework comparison is an explicit outcome | Match task, data, inputs, outputs, split, objective, metric, preprocessing, and material training/measurement conditions. State unavoidable differences. | Rankings caused by different datasets, budgets, defaults, or hardware. |
| Exact computational parity is claimed | Align parameters, operations, precision, conventions, and tolerances; compare the same test contract. | Assuming the same random seed gives identical parameters across libraries. |
| Second implementation adds only syntax | Omit or link an external example. | Counting languages as depth. |

Toy/from-scratch examples must state their limitations. Comparable evaluation does not imply bitwise equality or production readiness.

For a required multi-stack note, state the common inputs and parameters in a **Shared fixture** field or plain `Shared fixture:` line. Reuse the fixture from an earlier trace when it exists. Provide a runnable block for each planned stack and a table with columns Framework (or Language), Exposes, Hides, and Pitfall. Use the exact stack ID in the first column. Keep default differences visible.

**Example of change:** A PyTorch/Keras comparison uses the same task, split, architecture, loss, and metric, and reports differences in initialization or execution instead of presenting unrelated demos as evidence.

## DM-18

**Title:** Verification and reproducibility. **Purpose:** Match checks to claims and report exactly what was done. **Decision question:** What observable evidence would detect a consequential mistake here?

**Inputs:** Reference outputs, fixture, runtime, bounds, determinism and tolerance.
**Default:** Describe what could be checked and record the actual static or execution status.
**Precedence:** Proof and source evidence retain their separate standards.

| Branch / claim | Output / choice | Leave out or qualify |
|---|---|---|
| Hand calculation or pseudocode | Independently check the small expected result or trace and relevant invariant/termination condition. | Runtime/dependency lists for non-executable content. |
| Runnable example/from-scratch code | Imports/setup and actual inputs; expected result; assertions or manual checks that can expose the main error; relevant invalid/boundary cases only. | Tests that merely restate the implementation or universal edge-case quotas. |
| Numerical result | State dtype/precision/tolerance when material; check relevant units, shapes, stability, or reference value. | Exact-equality claims for approximate results without justification. |
| Manual/custom gradient | Use an independent derivative or finite-difference comparison at differentiable points; choose perturbation/tolerance mindful of roundoff, scale, and truncation error. | Numerical checks as proof or checks at kinks without explaining the convention. |
| Stochastic training/experiment | Record data/preprocessing, train/validation/test roles, split, metric, seeds, material versions/device/settings, and uncertainty when comparing performance. | Fitting preprocessing on held-out data; treating a seed as universal reproducibility. |
| Systems/production behavior | Check the relevant observable contract under the specified concurrency, resource, failure, or recovery conditions. | General robustness claims from a tiny unit test. |
| Not executed or only partly checked | Label `Status: static verification (not executed)` (or specify which components ran with verbatim stdout/stderr); omit execution claims completely when `language: "none"`. | Invented logs, runtime versions (`NumPy 2.5.5`), passing assertions, or `"executed via"` / `"Observed Execution Output"` when no code ran. |

When executed, record the actual command/environment details needed for reproduction, observed result, and limits of the check. A documentation check verifies a documented claim, not execution of the sample. Keep verification adjacent to the example/code or in one dedicated module.

For required stacks, each example must exercise the intended behavior. New deep contracts have no code line quota; legacy contracts retain their earlier minimum. Run the example via the planner's `verify-runtimes` command before publishing. For each stack, report under `### Verification — <stack-id>` with `Status: executed`, the observed `Version:` when reported, and one `text` fence with verbatim stdout. If the report says a package or tool is missing, use the exact static status and omit observed output and version. The publish gate reruns examples from trusted drafts and checks this evidence. Equivalent numeric examples print `PARITY: [<values>]` as one line of finite JSON numbers in the same input order. A workflow-only comparison may use `Parity: workflow-only — <specific reason>`.

**Example of change:** A manual gradient lesson adds a small smooth-point finite-difference check and reports tolerance; an inference-only lesson tests output shapes and values without a gradient check.

## DM-19

**Title:** Alternatives, failure modes, and boundaries. **Purpose:** Include only consequential decisions and errors. **Decision question:** What plausible choice, misuse, or failure would materially change the result?

**Inputs:** Introduced rules, selection cues, real failure modes and evidence gaps.
**Default:** OMIT secondary references and unsupported caveats.
**Precedence:** DM-05 governs corrections and attribution.

| Branch / need | Output / choice | Leave out or link |
|---|---|---|
| A real method/design choice exists | Compare common task and constraints: assumptions, cost, quality, data needs, interfaces, or operational burden as relevant; end with conditional selection. | Unqualified best-method claims. |
| Nearby concepts are confused | Contrast their defining behavior using the smallest discriminating example. | Arbitrary comparison rows. |
| Mathematical result is invalid outside an assumption | State the boundary near the result; add a counterexample if it clarifies the failure. | Repeating it in a second edge-case catalog. |
| Plausible implementation/system failure is consequential | Trigger, symptom/consequence, cause, diagnostic, and mitigation; link or reference its check. | A required bug count or speculative exhaustive list. |
| Evidence supports less than the reader might infer | Identify confounding, sample/task limits, approximation, or untested regimes; narrow conclusions. | Using a caveat to preserve an otherwise unsupported general claim. |
| No distinct decision/error remains | Omit the section or integrate a brief warning at the point of use. | Invented alternatives or gotchas. |

KEEP a reference matrix when several already-explained rules benefit from lookup. Use rule, meaning, conditions, and notes or units. ADAPT to a decision guide when competing methods need recognition cues. MERGE into the explanation when one condition is enough. For uncertainty, distinguish a sourced correction, an observed boundary, an access gap, and a genuine open question. Name what would settle an open question.

**Example of change:** An ML workflow retains leakage and train/inference mismatch if they affect the lesson; a memory-lifetime note retains use-after-free. Neither inherits the other's bug list.

## DM-20

**Title:** Recall, connections, and final anti-filler audit. **Purpose:** Confirm that the finished note teaches its chosen outcome without residue. **Decision question:** What helps retrieval or transfer, and what can be removed without losing understanding?

**Inputs:** Outcomes, explained concepts, candidate links and final draft.
**Default:** KEEP a short teachable check and applicable footer elements.
**Precedence:** Source fidelity and route constraints take precedence over enrichment.

| Branch / finding | Output / choice | Remove or repair |
|---|---|---|
| Retrieval would benefit the learner | Select distinct checks for the taught objectives, with answers or checks when useful. Deep notes have no fixed question quota; legacy routes retain their limits. | Trivia, repeated checks or unrelated cognitive tiers. |
| A takeaway is a useful retrieval cue | Brief cue pointing to the mechanism or decision. | Another full summary of the opening. |
| A prerequisite, extension, comparison, or application is a real next step | Link an existing note with the relationship explained; use plain text for a future note not yet created. | Broken/ambiguous wikilinks and compulsory next-note promises. |
| A real uncertainty remains | State the specific question, known limits, and what evidence would resolve it. | Fabricated confusion or empty open-question fields. |
| Same equation, table, trace, code, or boundary explanation occurs twice | Choose its most useful home, merge or link, update local anchors after omission. | Redundant previews, repeated behavior/edge-case tables, pasted code copies. |
| Unsupported history/measurement/current behavior or inferred execution appears | Verify, narrow, label unverified, or remove; require specific document URLs in citations (never bare root domains like `https://gallica.bnf.fr/` or `https://archive.org/`); keep source and execution status honest. | Fabricated citation details, bare homepage links, API claims, runtime versions when `code_depth == "none"`, and invented test results. |
| Unused section, authoring gate, matrix, empty row, template token, or padding remains | Remove it and check the result still meets the outcome; shorten/merge where clearer. | Arbitrary word/sentence quotas, rigid stage counts, bug/implementation quotas, filler phrasing. |
| Formatting or navigation is uncertain | Check Markdown table columns/escaped pipes, fences, callout quoting, math delimiters, and actual link targets; inspect rendering when available. | Claiming rendered QA when only source syntax was inspected. |

Tie recall to the taught outcomes. Progress from a factual cue through causal explanation to application or diagnosis, with a short answer or non-spoiling hint. Choose links whose link text or surrounding prose explains the progression. Follow the [footer contract](footer_widgets.md) for applicable widgets and retain an open confusion only if it names a real unresolved issue.

**Example of change:** A conceptual note ends after a precise distinction and a useful transfer question, with no math/code headings. A coding note keeps runnable verification without a forced proof or invented “open confusion.”
