# Instructional Planning, Scope Budgeting & Unified Depth Scale

Load this for substantive theory planning. [master-registry.yaml](../../dispatch/master-registry.yaml) and [subject-registry.yaml](../../dispatch/subject-registry.yaml) resolve format, artifact selection, and primary/secondary subjects; [instructional-registry.json](instructional-registry.json) maps knowledge types to subtemplates. Read only selected entries.

## 1. Three-Level Internal Planning Hierarchy

Maintain **one compact internal plan** structured at three levels rather than repeating collection metadata inside every concept or creating JSON builders (never publish internal planning records):
- **Request level:** `artifact_policy`, extensible list-based resolved `artifact_plan`, `learning_objectives`, `source_permissions`, `learner_profile` ([learner-model.md](learner-model.md)). Maintain `artifact_plan` directly inside the request plan as the single artifact manifest consumed by authoring, linking, destination, and verification rules—supporting single notes, multi-chapter collections, MOCs, playlist sets, standalone labs/sheets, create-vs.-update operations, and asset permissions without fixed 3-file assumptions:

```yaml
artifact_plan:
  artifacts:
    - id: <artifact-id>
      role: <theory | experimental_lab | mastery_pack | moc | video_note | reference | assessment | synthesis>
      master: <M1..M7 | video_notes>
      action: <create | update>
      filename: <intended filename>
      required: <true | false>
      dependencies: []
  omitted_artifacts: []
  permissions:
    external_visuals: <true | false>
```

- **Collection level** *(only when bundled or multi-chapter)*: `notation`, `canonical_definitions`, `shared_fixtures`, `concept_ownership` ([knowledge-consistency.md](knowledge-consistency.md)).
- **Concept level:** `concept_id`, **`learning_objective`** (required anchor for reasoning, examples, coverage, mastery, and verification), `role` (`prerequisite`, `core`, `extension`, `advanced`), `dependencies`, `knowledge_type`, `primary_subject` (+ selective secondary support), `concept_reasoning` ([concept-reasoning.md](concept-reasoning.md)), `depth` (unified `0–5` + separate `math_profile`), `example_roles` ([example-engineering.md](../../blueprints/components/example-engineering.md)), `evidence_locators`, and `completion_condition`.

For comprehensive independent notes or unfamiliar disciplines, populate records via [curriculum-discovery.md](curriculum-discovery.md) (within active `source_permissions`) and [subject-theory-profiles.md](../../blueprints/components/subject-theory-profiles.md). Apply the **two-dimension prerequisite policy** (`importance` × `learner status`) in [teaching_core.md](../../../core/teaching_core.md).

### Scope & Resource-Budget Planning
Before drafting, estimate total intellectual burden from: **core concept count, target depth, source complexity, artifact count, mathematical derivation load, practical implementation load, and distinct visual needs**.
- For focused requests, finish the complete learning unit at full target depth.
- For broad collections, partition cleanly at natural conceptual boundaries and verify completed chapters—if resource or context limits prevent finishing the entire curriculum, **disclose exactly what remains incomplete** rather than silently thinning later chapters or claiming full coverage.

### Audience & Scope Presets
- **Beginner:** Stronger local prerequisite bridges, one conceptual burden at a time, concrete examples beside definitions.
- **Advanced:** Higher causal/formal depth, boundary conditions, and technical qualifications without skipping necessary definitions.
- **Comprehensive:** Full mechanism depth, worked examples, evidence, and transfer, emitting companions per `artifact_policy` and `source_permissions`.
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

*(Actual learner mastery is measured separately via assessment responses—never claim a learner understands a subject merely because the authored note reached Level 4–5.)*

## 3. Selective Module Depth & Tool Selection

Use [module-catalog.md](../../blueprints/components/module-catalog.md) only for teaching moves serving the objective. Adapt each selected module proportionally (**Awareness 1–2 / Mechanism 3 / Analytical & Transfer 4–5**):
- **Proof & Formal Justification:** Activated by topic and objective across any appropriate master—**including `M4` worked proof construction and `M5` algorithm correctness proofs**.
- **Computational Tools:** Select executable code only when coding serves the objective, honoring explicit user language/stack choices and statically verifying code per [experimental-lab.md](experimental-lab.md).

## 4. Coherent Composition & Targeted Repair

Assign every definition, equation, example, and assumption one canonical home. Gather verified claims via [research-engine.md](../sourcing/research-engine.md) and [claim-verification.md](../sourcing/claim-verification.md) within [source-fidelity.md](../sourcing/source-fidelity.md), enrich dependency ordering and misconception placement via [pedagogical-intelligence.md](pedagogical-intelligence.md), and apply dependency-aware local repairs on review rather than regenerating unrelated sections.
