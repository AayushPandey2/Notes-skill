# Six-Stage Verification Gate & Bounded Acceptance

Execute **Stages 1–5 completely before saving** using strictly **manual, script-free inspection**, resolve an explicit bounded **Acceptance Decision**, and run **Stage 6 after saving**. Never use word count, heading count, or image count as proof of educational quality, and never claim automated YAML parsing, code execution, script validation, or live Obsidian rendering checks. Permission, authorization, and safety boundaries ([security-education.md](../safety/security-education.md), [physical-lab-safety.md](../safety/physical-lab-safety.md)) apply continuously throughout the workflow, not only at review time.

## Pre-Publication Stages (Stages 1–5 — Before Saving)

### Stage 1 — Subject, Theory, Evidence & Editorial Correctness (Before Saving)
- Verify [teaching_core.md](../../../core/teaching_core.md), [theory_quality_contract.md](../../../core/theory_quality_contract.md) (including the **Educational & Mathematical Depth Preservation Contract**), [math_gates.md](../../../core/math_gates.md) (continuous mathematical reasoning and complete derivations), [claim-verification.md](../sourcing/claim-verification.md), [educational-editor.md](educational-editor.md), and [adversarial-theory-review.md](adversarial-theory-review.md): concrete grounding before abstractions, **two-dimension prerequisite policy** (`importance` × `learner status`), **objective-to-passage & derivation-completeness verification** (inspecting actual derivation steps inside formula callouts rather than merely checking formula presence, verifying mathematical dependency order and scalar-to-matrix shape justifications), claim-level validity/evidence checks and source-error distinction, explanatory and mathematical failure modes, paragraph contribution test, target `0–5` depth, and dependency-aware repair of Critical/Major/Moderate defects.

### Stage 2 — Artifact Selection & Source Compliance (Before Saving)
- Verify emitted files against the **resolved `artifact_plan`** ([adaptive-engine.md](../authoring/adaptive-engine.md), `artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml)), active `docs/blueprints/formats/` + presets, and explicit user overrides—confirming no unsupported companion labs/cheatsheets were emitted under `M3`, `M4`, `M6`, `M7`, `/scribe-ytnotes`, standalone `M5`, single-file requests, or restrictive `strict` sources.
- Confirm active [source-fidelity.md](../sourcing/source-fidelity.md) permissions (`strict`, etc.) and video transcript-only limits ([video-notes.md](../../blueprints/formats/video-notes.md)) were respected, unconfirmed claims carry `[UNVERIFIED]`, and unverified gaps are disclosed honestly.

### Stage 3 — Disciplinary Completeness & Misconception Boundaries (Before Saving)
- Verify [subject-registry.yaml](../../dispatch/subject-registry.yaml) obligations for the selected primary subject (and any selectively merged secondary support): disciplinary mechanisms, domain-appropriate examples/evidence, and verified misconceptions from [subject-theory-profiles.md](../../blueprints/components/subject-theory-profiles.md)—confirming unrelated subject rules (e.g., ML datasets or 4-language Rust stacks) did not leak into unrelated disciplines.

### Stage 4 — Lab Correctness, Experiment Integrity & Safety Compliance (Before Saving)
- Confirm **zero scripts or temporary builder projects** were created or executed on the host, and confirm [security-education.md](../safety/security-education.md) and [physical-lab-safety.md](../safety/physical-lab-safety.md) guardrails were enforced throughout.
- When a lab or implementation is present, verify [experimental-lab.md](../authoring/experimental-lab.md) and the selected investigation profile (`docs/blueprints/investigations/`): shared-foundation + track-specific **A–G** walkthroughs, static correctness (syntax, types, bounds, operators, equations), and honest 3-attribute integrity (*Origin*, *Method*, *Verification* reflecting what actually occurred) with `Source and static review only; not compiled or executed here.` (never claiming unexecuted code ran or fabricating observations).

### Stage 5 — Presentation, Mathematics, Visuals, Metadata, Links & Bounded Acceptance (Before Saving)
- Verify [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md) (read with folds closed for hypotheses, milestones and conclusions, then open folds to verify derivations, prerequisites, source permission, local derivation ownership, notation, equation spacing and callout boundaries), [representations.md](../authoring/representations.md) (visual source hierarchy, inspected external/native figures, adaptive sizing, ordinary Markdown attribution, diagram-to-model correspondence, zero Mermaid/ASCII, **asset dependency check** ensuring no accepted note references a missing required figure/asset), [properties-policy.md](../../properties/properties-policy.md) (line-1 YAML matching active profile, unique IDs), and [revision-and-linking.md](../updating/revision-and-linking.md) (resolved links, acyclic prerequisites, reciprocal links only to files in `artifact_plan`).
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
    theory: <accepted | accepted_with_disclosed_limitations | omitted | blocked>
    experimental_lab: <accepted | accepted_with_disclosed_limitations | omitted | blocked>
    mastery_pack: <accepted | accepted_with_disclosed_limitations | omitted | blocked>
  review:
    theory: <manually_reviewed | independently_reviewed>
    mathematics: <manually_checked | not_applicable>
    code_execution: <not_performed | actually_executed>
    visual_rendering: <unavailable | live_checked>
  unresolved_gaps: []
```

## Post-Publication Stage (Stage 6 — After Saving)

### Stage 6 — Actual Saved-File Integrity (After Saving)
- Reopen actual saved files (when written to a vault) to confirm valid line-1 YAML frontmatter, intact local asset/embed targets, resolved relative wikilinks matching emitted filenames, and untouched unrelated vault notes/YAML.
