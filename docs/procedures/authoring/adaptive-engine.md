# Instructional Planning & Unified Depth Scale

Load this for substantive theory planning. [master-registry.yaml](../../dispatch/master-registry.yaml) and [subject-registry.yaml](../../dispatch/subject-registry.yaml) resolve format, artifact selection, and primary/secondary subjects; [instructional-registry.json](instructional-registry.json) maps knowledge types to subtemplates. Read only selected entries.

## 1. Shared Internal Concept Record & Planning Input

Maintain **one shared internal concept record** enriched across planning policies rather than rebuilding separate planning tables across files (keep this internal—never publish planning scaffolding or create JSON builders):
- `concept_id`, `role` (`prerequisite`, `core`, `extension`, `advanced`), `dependencies`
- `knowledge_type` (`conceptual`, `mathematical`, `programming`, `algorithmic`, `architectural`, `scientific`, `historical`, `comparative`, `procedural`, `research`) & `primary_subject` (+ selective secondary support)
- `learning_objective` & `source_policy` (`independent`, `strict`, `source_first`, `expanded`, `comparative`)
- `depth` (unified `0–5` theory depth + separate `math_profile` from [math_gates.md](../../../core/math_gates.md) + `code`/`visual` needs)
- `evidence_locators`, `teaching_methods`, and `completion_condition`

For comprehensive independent notes or unfamiliar disciplines, populate records via [curriculum-discovery.md](curriculum-discovery.md) (staying inside supplied material under `strict` mode) and [subject-theory-profiles.md](../../blueprints/components/subject-theory-profiles.md). Apply the 3-tier prerequisite rule in [teaching_core.md](../../../core/teaching_core.md).

### Audience & Scope Presets
- **Beginner:** Stronger local prerequisite bridges, one conceptual burden at a time, concrete examples beside definitions.
- **Advanced:** Higher causal/formal depth, boundary conditions, and technical qualifications without skipping necessary definitions.
- **Comprehensive:** Full mechanism depth, worked examples, evidence, and transfer, emitting companions per `artifact_policy`.
- **Compact (`M3`, `quick-summary`, `atomic-card`):** Narrow scope and high retrieval density while preserving governing conditions.

## 2. Unified Theory Depth Scale (0–5) & Mathematical Profile

Keep the **5 mathematical profiles** in [math_gates.md](../../../core/math_gates.md) separate (`Conceptual`, `Quantitative intuition`, `Working formulation`, `Derivation and mechanism`, `Formal reasoning`). Use **one unified 0–5 theory depth scale** across planning, curriculum coverage, and adversarial review:

| Level | Observable Content Requirement |
|---|---|
| **0** | Outside scope (explicitly excluded) |
| **1** | Recognition (named and situated only) |
| **2** | Precise explanation (definition, ordinary-language meaning, concrete example, boundary) |
| **3** | Mechanism or reasoning (how and why it works step by step) |
| **4** | Analytical justification (assumptions, conditions, ideal-to-real limits, failure diagnosis) |
| **5** | Independent application & transfer (forward/reverse reasoning, unseen cases, cross-topic transfer) |

*(Note: Actual learner mastery is measured separately via assessment responses—never claim a learner understands a subject merely because the authored note reached Level 4–5.)*

## 3. Selective Module Depth & Tool Selection

Use [module-catalog.md](../../blueprints/components/module-catalog.md) only for teaching moves serving the objective. Adapt each selected module proportionally (**Awareness 1–2 / Mechanism 3 / Analytical & Transfer 4–5**):
- **Proof & Formal Justification:** Activated by topic and objective across any appropriate master—**including `M4` worked proof construction and `M5` algorithm correctness proofs** (never force proofs onto non-proof topics, and never forbid proofs in `M4`).
- **Computational Tools:** Select executable code only when coding serves the objective, honoring explicit user language/stack choices and statically verifying code per [experimental-lab.md](experimental-lab.md).

## 4. Coherent Composition & Targeted Repair

Assign every definition, equation, example, and assumption one canonical home. Partition very large collections cleanly at natural topic boundaries without sacrificing required completeness. Gather verified claims via [research-engine.md](../sourcing/research-engine.md) within [source-fidelity.md](../sourcing/source-fidelity.md), enrich dependency ordering and misconception placement via [pedagogical-intelligence.md](pedagogical-intelligence.md), and apply targeted local repairs on review rather than regenerating unrelated sections.
