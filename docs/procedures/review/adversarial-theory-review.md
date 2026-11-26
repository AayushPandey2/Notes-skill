# Adversarial Theory Review & Unified Depth Verification

## Purpose

Separate **planning, writing, criticism, and repair** so review is genuinely diagnostic rather than rubber-stamping an author's own draft. When the host supports an independent reviewer context, use it selectively for substantial or high-risk topics; otherwise perform distinct authoring and review passes and disclose that independence was not available. Never accept an author's self-declaration as proof that requirements were met—inspect the actual paragraphs, equations, examples, and claims against [educational-editor.md](educational-editor.md) and the unified `0–5` scale in [adaptive-engine.md](../authoring/adaptive-engine.md).

## 1. Seven Consolidated Review Perspectives

Apply these seven diagnostic perspectives in a single consolidated manual review pass (no separate redundant full-document review passes or subagents required):

| Perspective | What It Hunts For |
|---|---|
| **1. Sequential beginner review** | Read strictly from start to finish as a first-time learner; find the **earliest** unexplained term, analogy-to-formalism cliff, missing essential prerequisite, operator dump, unsupported formula, confusing transition, incomplete example, or exercise requiring untaught knowledge—repairing the earliest defect before reviewing dependent sections |
| **2. Professor perspective** | Missing curriculum pillars, superficial mechanism descriptions lacking causal *why*, misleading analogies/simplifications, omitted variants/limitations, compressed later sections |
| **3. Mathematical perspective** | Generalized-first abstraction inversion, skipped foundational derivations, operator dumping, invalid algebra, missing parameter bounds/equality/tie-policy conditions, set-vs.-index notation drift, empirical-to-monotonic overclaims, hidden fold-only milestones |
| **4. Visual-learning perspective** | Prohibited generated visuals (AI/native tools, plotting scripts, custom SVG, redrawn art), visually rich sections limited to 0–1 token images or clustered in the intro/gallery, uninspected assets or search-thumbnail/webpage URLs, missing before/image/caption/after narrative, missing attribution/license checks |
| **5. Textbook-editor & collapsed-state perspective** | Compressed research-paper shorthand, unnecessary dramatic language (`"fatal flaw"`), AI writing signatures (`"In simple words"`, repeated `"Imagine that"`), generic callout titles, collapsed-state coherence failures (read with every optional callout closed first, then expanded), callout underutilization/overload, meta/robotic headings, broken reading rhythm |
| **6. Practical-learning & independent-learning perspective** | Theory disconnected from implementation, conflated cost components (data reference vs. read/copy vs. index vs. query), omitted edge cases, weak fading/transfer readiness to solve unfamiliar cases (evaluating preparation without claiming empirical mastery) |
| **7. Source-review perspective** | Unsupported certainty, conflated epistemic statuses, library/version/variant conflation, missing primary references, inaccurate attribution, or source-policy breaches |

### Mandatory Diagnostic Questions

1. What could a careful learner **incorrectly conclude** after reading this explanation?
2. Which central mechanism has been **described** (terminology/operation) without being **explained** (cause/why)?
3. Which high-priority concept from the [shared concept plan](../authoring/curriculum-discovery.md) fails its required depth or completion condition?
4. Which mathematical transition, claim qualification, or ideal-to-real assumption shift is unjustified?
5. Where does the running example stop supporting the explanation or fail to interpret *why* its result matters?
6. Could the learner apply this theory to an unfamiliar case or reason in reverse from an observed failure?

### Explanatory Failure Modes & Conceptual Why-Depth (Internal Diagnostic Only)

Search drafts for these explanatory failure modes without emitting a visible checklist:

| Failure Mode | What It Looks Like |
|---|---|
| **Circular explanation** | Explains a term using the term itself |
| **Mechanism omission** | States what happens without explaining the causal transition |
| **Algebraic teleportation** | Skips the exact transformation the learner needs to follow |
| **Analogy substitution** | Leaves an analogy standing in place of the actual mechanism |
| **Representation mismatch** | Diagram, equation, and prose describe inconsistent systems |
| **Example illusion** | One lucky example hides an invalid generalization |
| **Assumption invisibility** | Presents a conditional theorem/rule as universally true |
| **Definition overload** | Introduces too many mutually dependent terms at once |
| **False completeness** | Name-drops advanced jargon without teaching its mechanism |
| **Procedure memorization** | Gives steps without why they hold (`Level 1–2` instead of justification) |
| **Context-free formalism** | Drops equations without establishing what question they answer |
| **Unsupported certainty** | States plausible hypotheses or conditional results as settled fact |
| **Jargon-first / analogy-to-formalism cliff** | Opens with an everyday analogy or dense technical summary and immediately drops formal sets, vectors, or jargon before building the idea |
| **Generalized-first math inversion** | Starts with the most general parametric family (e.g., general $L_p$ norms) before concrete cases and foundational Pythagorean/Euclidean derivations |
| **Operator dumping** | Combines indicator functions, summations, and $\arg\max$ (or nested matrix/probabilistic ops) before teaching each operation singly |
| **Premature mathematical tool use** | Applies Taylor expansion, Newton's method, etc. on complex objectives before teaching the tool on a simple case |
| **Compressed research-paper tone & later-section thinning** | Packs three or four conceptual/algebraic steps into one sentence, uses dramatic labels (`"fatal flaw"`), or delivers rich early sections followed by compressed late topics |
| **Empirical-to-monotonic / cost conflation** | Turns a qualitative tendency into a strict monotonic guarantee or equates retaining a dataset reference with reading/copying/scanning the whole dataset |
| **Single-step iterative trace** | Stops an iterative/sequential algorithm after one round without showing updated state carryover or unseen inference |
| **Prohibited image generation or single-image token compliance** | Uses AI/native-generated images, plotting scripts, custom SVG, or redrawn diagrams, or stops at one token image / gallery dump on a visually rich chapter without running web-search refinement and fallback disclosure |
| **Unverified search thumbnail / missing vault image** | Confuses an image-search result link or webpage URL with a downloaded, inspected educational image |
| **Callout underutilization or hidden reasoning** | Leaves long optional proofs/refreshers all inline or hides essential mechanisms, assumptions, or prerequisites inside collapsed folds/companion files |
| **Library/variant conflation** | Presents method-specific or version-specific behavior (e.g., `approx` vs `hist`, pruning updaters) as universal algorithm law |

**Conceptual "Why-Depth" Check:** Within the existing unified `0–5` scale, ensure core mechanisms rise past bare **operation** (*"subtracts $\eta\nabla J$"*) through **immediate reason** (*"steepest local descent direction"*), **mathematical/causal justification** (*first-order expansion $J(w+\Delta w) \approx J(w) + \nabla J(w)^\top \Delta w$*), and **validity boundary** (*holds locally for small steps at nonstationary points, not arbitrary step sizes or global optimality*).

### Mathematical Derivation Defects (Internal Review Criteria)

Read the draft twice, first with formula folds closed to check the visible argument, then with them open to inspect each consequential step. A missing core derivation in comprehensive theory is a `Major` defect even when the formula is correct. If the source policy forbids filling the gap, identify the missing source material and repair the visibility or attribution within the authorized scope.

| Mathematical Defect | Required Repair |
|---|---|
| **Fold-only reasoning** | Restore assumptions, milestones and conclusions to the visible argument |
| **Fragmented reasoning** | Group connected equations under one objective and give their operations explanatory transitions |
| **Definition treated as theorem** | Identify the stipulation and motivate its meaning |
| **Missing derivation** | Construct the formula completely from established principles/identities |
| **Missing algebraic transitions** | Restore the missing transformations in the visible derivation or its existing solution/formula fold, as appropriate |
| **Unexplained cancellation** | Explain explicitly which factors cancel and why |
| **Missing assumption** | State conditions/hypotheses required for the transformation to hold |
| **Circular proof** | Replace with valid independent starting principles |
| **Sign inconsistency** | Correct the derivation and propagate across examples/labs/cheatsheets |
| **Incorrect normalization** | Align sum, mean, and regularization penalty scaling explicitly |
| **Unexplained mathematical identity** | Establish the identity cleanly before invoking it downstream |
| **Undefined symbol** | Define the symbol locally before first use |
| **Invalid dimension** | Clarify array shapes, component correspondence, and transposes |
| **False mathematical necessity** | Distinguish a modeling choice/link convention from a unique theorem |
| **Approximation presented as equality** | Restore `≈` and state the error/approximation regime |
| **Numerical example presented as proof** | Supply the general derivation alongside illustrative checks |
| **Unexplained final expression** | Interpret what each term, sign, and boundary in the result means |

A compressed topic list leaves a mechanism-level objective incomplete. Treat missing core conceptual or causal reasoning as a substantive defect even when the equations are correct. Locate the missing transition, causal explanation or worked contrast and repair the gap locally. Use prediction, diagnosis or transfer checks for objectives beyond recall.

## 2. Defect Severity Classification & Dependency-Aware Repair

Classify every defect by severity and repair **both the defect and all downstream artifacts that depend on it**:

| Severity | Examples | Required Action |
|---|---|---|
| **Critical** | Fabricated source/observation, unsafe lab/security instruction, fundamentally wrong theorem/formula | **Block acceptance** until fixed and re-reviewed |
| **Major** | Incorrect derivation/sign/operator, missing central mechanism, missing essential prerequisites or core mathematical tool bridges, silent omission of major `M1` curriculum pillars, silent omission of required permitted visuals, broken implementation contract | **Repair and re-review** affected sections & bundle |
| **Moderate** | Unexplained prerequisite, weak/non-discriminating example, missing qualification | **Improve** the affected explanation locally |
| **Minor** | Awkward phrasing, spacing, redundant sentence | **Editorial polish** (never override deeper checks) |

- **Dependency-aware repair:** If an equation, sign, or assumption is corrected in Theory (File 1), trace and update every dependent worked example, visual correspondence, Lab implementation/trace (File 2), Cheatsheet formula, and Q&A/Practice solution (File 3).
- **Honest verification limits:** Record this as manual semantic review of the note's content; actual learner mastery is measured only through assessment responses, never self-assessed completeness.
