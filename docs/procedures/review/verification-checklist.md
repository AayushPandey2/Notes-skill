# Six-Stage Verification Gate & Bounded Acceptance

Before saving, apply the applicable checks in stages 1–5 in a single proportionate manual review and resolve an acceptance decision. Apply stage 6 to actual writes. For compact artifacts, check correctness, scope, source fidelity, presentation and links without opening unrelated review or lab policies. Report only the checks performed. Follow safety and authorization throughout.

## Pre-Publication Stages (Stages 1–5 — Before Saving)

### Stage 1 — Subject, Theory, Evidence & Editorial Correctness (Before Saving)
- Check actual passages against their intended objectives and support. For substantive theory, use [the theory contract](../../../core/theory_quality_contract.md); apply [claim verification](../sourcing/claim-verification.md), [editorial review](educational-editor.md) and [adversarial review](adversarial-theory-review.md) when applicable. Assess mathematical soundness here and inspect mathematical presentation in stage 5.

### Stage 2 — Artifact Selection & Source Compliance (Before Saving)
- Verify emitted files against the **resolved `artifact_plan`** ([adaptive-engine.md](../authoring/adaptive-engine.md), `artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml)), active `docs/blueprints/formats/` + presets, and explicit user overrides—confirming no unsupported companion labs/cheatsheets were emitted under `M3`, `M4`, `M6`, `M7`, `/scribe-ytnotes`, standalone `M5`, single-file requests, or restrictive `strict` sources.
- Confirm active [source-fidelity.md](../sourcing/source-fidelity.md) permissions (`strict`, etc.) and video transcript-only limits ([video-notes.md](../../blueprints/formats/video-notes.md)) were respected, unconfirmed claims carry `[UNVERIFIED]`, and unverified gaps are disclosed honestly.

### Stage 3 — Disciplinary Completeness & Misconception Boundaries (Before Saving)
- Verify [subject-registry.yaml](../../dispatch/subject-registry.yaml) obligations for the selected primary subject (and any selectively merged secondary support): disciplinary mechanisms, domain-appropriate examples/evidence, and verified misconceptions from [subject-theory-profiles.md](../../blueprints/components/subject-theory-profiles.md)—confirming unrelated subject rules (e.g., ML datasets or 4-language Rust stacks) did not leak into unrelated disciplines.

### Stage 4 — Lab Correctness, Experiment Integrity & Safety Compliance (Before Saving)
- Confirm the [root non-execution rule](../../../SKILL.md#scriptorium) and any active [security](../safety/security-education.md) or [physical-lab](../safety/physical-lab-safety.md) boundaries. For a lab or implementation, inspect the actual trace and snippets using the applicable [lab integrity rules](../authoring/experimental-lab.md) and selected practical guidance.

### Stage 5 — Presentation, Mathematics, Visuals, Metadata, Links & Bounded Acceptance (Before Saving)
- Check the draft against the applicable [authoring rules](../../../core/authoring_rules.md), [properties policy](../../properties/properties-policy.md) and [link policy](../updating/revision-and-linking.md). For substantive mathematics, read with folds closed and open, then apply the [math policy](../../../core/math_gates.md), including its table rules. If an artifact needs figures, apply the [visual policy](../authoring/representations.md) and confirm each required asset is inspected and ready to publish.
**Independent acceptance checks.** For each applicable dimension, cite concrete evidence and resolve defects before judging the whole artifact. Mark a dimension inapplicable when it is outside the resolved scope.

| Dimension | Observable evidence |
|---|---|
| Concepts | Definitions, prerequisites and boundaries are introduced before use |
| Mechanism | A trace or causal explanation shows what changes and why |
| Mathematics | Valid derivations, assumptions, identified symbols and verified examples |
| Visuals | Essential relationships are legible in an inspected figure or sufficient permitted fallback, with material gaps disclosed |
| Readability | Focused prose and a coherent visible reading path support the intended audience |
| Practical reasoning | Worked comparisons show behavior, decisions, or failure diagnosis at the requested depth |
| Independent learning | Application, explanation or transfer checks match the objective when practice is permitted |

A strength on one dimension cannot cancel a material failure on another. Verify the required policy dependencies in [the runtime pipeline](../../../core/runtime_pipeline.md) before claiming full compliance. Apply the bounded acceptance outcomes below to unresolved defects.

- **Bounded Acceptance Decision:** Resolve acceptance cleanly instead of looping indefinitely when sources or tools remain unavailable:

| Outcome | Required Action |
|---|---|
| `accepted` | Publish accepted artifacts to approved destination and proceed to Stage 6 |
| `accepted_with_disclosed_limitations` | Publish only supported material and explicitly disclose unresolved limitations/gaps |
| `repair_required` | Repair affected content and downstream bundle dependencies, then re-review |
| `blocked` | Do **not** save or represent the artifact as completed; explain what is blocking completion |
| *No new evidence / host capability available* | **Stop repeated repair attempts** and finalize either `accepted_with_disclosed_limitations` or `blocked` |

- **Minimal Internal Quality Manifest:** Maintain this status record internally during normal generation (never create an extra vault file per note; expose a concise summary only if the user requests an audit or detailed verification report):

```yaml
quality_manifest:
  requested_scope: <topic and active format/preset>
  target_depth: <0-5>
  artifact_status:
    - artifact: <role and intended path from the resolved plan>
      status: <accepted | accepted_with_disclosed_limitations | repair_required | omitted | blocked>
  review:
    theory: <not_applicable | not_reviewed | manually_reviewed | independently_reviewed>
    mathematics: <manually_checked | not_applicable>
    code_execution: not_performed
    external_execution_evidence: <none | user_supplied | published>
    image_inspection: <not_applicable | unavailable | host_inspected_image>
  unresolved_gaps: []
```

## Post-Publication Stage (Stage 6 — After Saving)

### Stage 6 — Actual Saved-File Integrity (After Saving)
- Reopen actual saved files and check the applicable metadata profile or preservation rule, local asset targets, wikilinks and unrelated content. On a partial write, reconcile links in the saved artifacts under the [link policy](../updating/revision-and-linking.md) and report which files exist.
