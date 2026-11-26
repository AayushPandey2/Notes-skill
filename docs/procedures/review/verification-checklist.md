# Six-Stage Verification Gate

Execute **Stages 1–5 on the complete draft before saving**, resolve an explicit **Acceptance Decision**, and run **Stage 6 after saving**. Never use word count, heading count, or image count as proof of educational quality, and never represent manual review as automated verification.

**Acceptance Decisions:** `accepted` · `accepted_with_disclosed_limitations` · `repair_required` · `blocked` (never save or publish a critically flawed note as completed).

## Stage 1 — Universal Correctness, Evidence & Editorial Quality
- Verify [teaching_core.md](../../../core/teaching_core.md), [theory_quality_contract.md](../../../core/theory_quality_contract.md), [claim-verification.md](../sourcing/claim-verification.md), [educational-editor.md](educational-editor.md), and [adversarial-theory-review.md](adversarial-theory-review.md): concrete grounding before abstractions, 4-category prerequisite discipline, claim-level evidence & contradiction checks, paragraph contribution test, target `0–5` depth, and dependency-aware repair of any Critical/Major/Moderate defects.

## Stage 2 — Selected Master & Artifact Cardinality
- Verify the active format (`docs/blueprints/formats/` + any preset in `docs/blueprints/presets/`) and confirm emitted files match `artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml) and explicit user overrides (no unrequested companion labs/cheatsheets for `M3`, `M4`, `M6`, `M7`, `/scribe-ytnotes`, standalone `M5`, or single-file requests).

## Stage 3 — Primary Subject & Misconception Boundaries
- Verify [subject-registry.yaml](../../dispatch/subject-registry.yaml) obligations for the selected primary subject (and any selectively merged secondary support): disciplinary mechanisms, domain-appropriate examples/evidence, and verified misconceptions from [subject-theory-profiles.md](../../blueprints/components/subject-theory-profiles.md)—confirming unrelated subject rules (e.g., ML datasets or 4-language Rust stacks) did not leak into unrelated disciplines.

## Stage 4 — Companion Lab & Three-Attribute Experiment Integrity
- When a lab or implementation is present, verify [experimental-lab.md](../authoring/experimental-lab.md) and the selected investigation profile (`docs/blueprints/investigations/`): shared-foundation + track-specific **A–G** walkthroughs, static correctness (syntax, types, bounds, operators, equations), and honest 3-attribute integrity (*Origin*, *Method*, *Verification*) with `Source and static review only; not compiled or executed here.` (never claiming unexecuted code ran or fabricating observations).

## Stage 5 — Presentation, Mathematics, Visuals & Link Hygiene
- Verify [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md) (native delimiters, grouped `aligned` folds, non-recursive/compact-reference exceptions, notation consistency), [representations.md](../authoring/representations.md) (visual hierarchy, inspected local embeds, adaptive sizing, ordinary Markdown attribution, diagram-to-model correspondence, zero Mermaid/ASCII), [properties-policy.md](../../properties/properties-policy.md) (line-1 YAML matching active profile, unique IDs), and [revision-and-linking.md](../updating/revision-and-linking.md) (resolved links, acyclic prerequisites, reciprocal links only to existing files).

## Stage 6 — Pre-Publication Correctness vs. Post-Publication Delivery Integrity
- **Pre-publication correctness (before saving):** Confirm zero scripts/projects were created or executed on the host, active [source-fidelity.md](../sourcing/source-fidelity.md) permissions (`strict`, etc.) and video transcript-only limits ([video-notes.md](../../blueprints/formats/video-notes.md)) were respected, safety policies ([security-education.md](../safety/security-education.md), [physical-lab-safety.md](../safety/physical-lab-safety.md)) were enforced, and any unverified gaps are disclosed honestly.
- **Post-publication integrity (after saving):** Reopen the saved files to confirm line-1 YAML validity, intact embed targets/assets, resolved relative links, and that unrelated vault notes/YAML remained untouched.
