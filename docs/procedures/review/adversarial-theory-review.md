# Adversarial Theory Review & Concept-Level Benchmark

## Purpose

Make manual review of substantive theory notes (`M1`, `M2`, `M4`, `M5`, `M7`, and video notes) genuinely diagnostic rather than a rubber-stamp pass. Inspect **actual paragraphs, derivations, examples, and claims** through focused adversarial lenses and anchor depth judgments on observable concept mastery.

## 1. Six Adversarial Review Lenses

Apply these as focused review perspectives in a single manual pass (no separate subagents required):

| Lens | What It Hunts For |
|---|---|
| **1. Subject expert** | Factual errors, missing core mechanisms, outdated conventions, misleading simplifications |
| **2. Beginner learner** | Unexplained terminology, hidden prerequisites, abrupt leaps from concrete to abstract |
| **3. Mathematical reviewer** | Unjustified algebraic transitions, missing hypotheses/conditions, unit/dimension/notation drift, wrong operators |
| **4. Skeptical reader** | Unsupported claims, conflated epistemic statuses (hypothesis stated as law, correlation as causation), overgeneralizations |
| **5. Practical problem solver** | Explanations that describe a concept without enabling the learner to apply, compute, trace, or diagnose an unseen case |
| **6. Educational editor** | Redundant repetition, broken conceptual continuity, weak transitions, tables/visuals disconnected from prose |

### Mandatory Diagnostic Questions

Inspect the drafted note and answer honestly before saving:

1. What could a careful learner **incorrectly conclude** after reading this explanation?
2. Which central mechanism has been **described** (terminology/operation) without being **explained** (cause/why)?
3. Which high-priority concept from the internal [coverage matrix](../authoring/curriculum-discovery.md) is absent or fails its completion condition?
4. Which mathematical transition, claim qualification, or ideal-to-real assumption shift is unjustified?
5. Where does the running example stop supporting the explanation or fail to interpret *why* its result matters?
6. Could the learner apply this theory to a different example or reason in reverse from an observed failure?

## 2. Concept-Level Understanding Benchmark (0–7)

Use these levels as **review anchors** for the existing theory-depth scale in [adaptive-engine.md](../authoring/adaptive-engine.md) (not a competing routing system):

| Level | Observable Quality Achieved in the Note |
|---|---|
| **0** | Concept omitted |
| **1** | Concept merely mentioned |
| **2** | Definition supplied |
| **3** | Definition + intuitive explanation |
| **4** | Mechanism or causal reasoning explained |
| **5** | Mechanism + formalism + worked example |
| **6** | Assumptions, exceptions, and limitations explained |
| **7** | Learner can independently reason about unfamiliar cases (forward & reverse transfer) |

### Repair Rule

- **Critical errors override scores:** A factual error, wrong equation/operator, violated source restriction, or fabricated claim fails review regardless of how well other sections read.
- **Targeted local repair:** When a high-priority concept falls below its required benchmark level (e.g., a core mechanism sitting at Level 2 instead of Level 5–6), repair that specific conceptual gap directly—never pad introductions or add generic summary prose.
- **Honest status:** Record this as a manual semantic review; never represent it as automated verification or executed testing.
