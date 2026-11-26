# Adversarial Theory Review & Unified Depth Verification

## Purpose

Separate **planning, writing, criticism, and repair** so review is genuinely diagnostic rather than rubber-stamping an author's own draft. When the host supports an independent reviewer context, use it selectively for substantial or high-risk topics; otherwise perform distinct authoring and review passes and disclose that independence was not available. Never accept an author's self-declaration as proof that requirements were met—inspect the actual paragraphs, equations, examples, and claims against [educational-editor.md](educational-editor.md) and the unified `0–5` scale in [adaptive-engine.md](../authoring/adaptive-engine.md).

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

1. What could a careful learner **incorrectly conclude** after reading this explanation?
2. Which central mechanism has been **described** (terminology/operation) without being **explained** (cause/why)?
3. Which high-priority concept from the [shared concept plan](../authoring/curriculum-discovery.md) fails its required depth or completion condition?
4. Which mathematical transition, claim qualification, or ideal-to-real assumption shift is unjustified?
5. Where does the running example stop supporting the explanation or fail to interpret *why* its result matters?
6. Could the learner apply this theory to an unfamiliar case or reason in reverse from an observed failure?

## 2. Defect Severity Classification & Dependency-Aware Repair

Classify every defect by severity and repair **both the defect and all downstream artifacts that depend on it**:

| Severity | Examples | Required Action |
|---|---|---|
| **Critical** | Fabricated source/observation, unsafe lab/security instruction, fundamentally wrong theorem/formula | **Block acceptance** until fixed and re-reviewed |
| **Major** | Incorrect derivation/sign/operator, missing central mechanism, broken implementation contract | **Repair and re-review** affected sections & bundle |
| **Moderate** | Unexplained prerequisite, weak/non-discriminating example, missing qualification | **Improve** the affected explanation locally |
| **Minor** | Awkward phrasing, spacing, redundant sentence | **Editorial polish** (never override deeper checks) |

- **Dependency-aware repair:** If an equation, sign, or assumption is corrected in Theory (File 1), trace and update every dependent worked example, visual correspondence, Lab implementation/trace (File 2), Cheatsheet formula, and Q&A/Practice solution (File 3).
- **Honest verification limits:** Record this as manual semantic review of the note's content; actual learner mastery is measured only through assessment responses, never self-assessed completeness.
