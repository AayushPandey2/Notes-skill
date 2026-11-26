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
**Ten Independent Educational Acceptance Gates (Gates A–J):** Check each applicable gate against concrete passages before approving the artifact; mark a gate inapplicable only when genuinely outside the resolved format or strict-source scope:

| Acceptance Gate | Observable Evidence Required |
|---|---|
| **Gate A — Scope completeness** | Central learning objectives developed proportionally (`M1` covers foundations/baselines, core mechanism, task types/variants, practical usage, limitations, comparisons, and primary sources rather than collapsing into a summary) |
| **Gate B — Beginner accessibility** | Plain-language intuition opens before dense jargon; simpler baselines precede upgrades; mathematical progression and technical terms are introduced cleanly |
| **Gate C — Self-contained understanding** | Essential prerequisites, terminology, symbols, and governing assumptions are taught locally within declared scope without forcing external note lookups (or disclosed honestly under strict sources) |
| **Gate D — Theory quality** | Causal mechanisms and why-level reasoning explain how inputs transform, what changes under altered conditions, and what multi-step iterative rounds carry over |
| **Gate E — Mathematical quality** | Equations are accurate, mathematical tools/approximations are motivated and taught before use, governing models match worked examples, consequential derivation steps stay visible with folds closed, and results are interpreted |
| **Gate F — Visual quality** | Meaningful visual opportunities (structural, geometric, sequential, functional) attempted via permitted capabilities, placed adjacent with captions/decoding, or fallback/limitations honestly disclosed |
| **Gate G — Example quality** | Worked traces and contrasting/boundary/failure examples demonstrate mechanisms accurately with complete arithmetic and unseen-input inference |
| **Gate H — Writing & presentation** | Calm university-textbook prose (no compressed research-paper shorthand or banned meta-headings), clean YAML, Obsidian callouts, compact tables, and navigable whitespace |
| **Gate I — Independent understanding** | Checkpoints and problem/diagnosis/transfer framing equip the learner to reason and apply concepts on unfamiliar cases when permitted |
| **Gate J — Integrity** | Active safety rules, non-execution rule, `source_policy` boundaries, accurate attribution, valid metadata, and verified internal wikilinks/embeds all pass |

**Acceptance threshold, Critical Defect Override & Final Learner-Experience Test:** Comprehensive `M1` notes require an overall manual rubric score $\ge 85/100$, $\ge 4/5$ in applicable essential dimensions, and **zero unresolved Critical defects**. **Never accept an educationally incomplete note merely because its YAML, LaTeX delimiters, callouts, and isolated equations look structurally clean.** Reject any draft regardless of aggregate score if it contains an unresolved Critical defect: serious factual misinformation, consequential mathematical errors (including invalid bounds, wrong equality/tie-policy logic, or empirical tendencies stated as monotonic guarantees), missing essential prerequisites, **severe beginner accessibility failures** (such as an analogy-to-formalism cliff or unexplained composite operators), **major omissions in the declared curriculum** (or compressed late sections), fabricated visual assets or sources, source-integrity violations, **essential reasoning hidden in collapsed folds or delegated to companion notes**, or serious safety/authorization violations. Ask the final learner-experience test before finalizing: *"Could a motivated beginner with the declared starting knowledge read this chapter independently, understand why the subject works, follow its mathematics, interpret its figures, and solve representative unfamiliar problems?"* Whenever a verified defect appears: identify exact cause, repair both the note and all dependent passages/companions, re-evaluate affected dimensions, and disclose remaining limitations honestly. Apply the bounded acceptance outcomes below to unresolved defects.

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
