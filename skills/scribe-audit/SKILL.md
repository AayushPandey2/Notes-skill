---
name: scribe-audit
description: Inspect existing Obsidian vault notes read-only across factual, pedagogical, presentation, Scriptorium-conformance, bundle-consistency, and currency profiles, proposing actionable targeted repairs without rewriting the vault. Use for /scribe-audit or explicit quality-review requests on existing notes.
---

# `/scribe-audit`

## Purpose & Activation

Run a **read-only quality audit** over existing Obsidian vault learning notes and propose actionable, confidence-tagged repairs without rewriting the vault by default. Activate on `/scribe-audit`, `"audit my notes"`, or `"review my existing note quality"`.

## Inputs, Source-Research Mode & Inspection Discipline

- **Inputs:** An explicitly supplied draft, or a target note, bundle, folder path, or topic scope within the configured vault from [pre-gen-gate.md](../../docs/procedures/authoring/pre-gen-gate.md).
- **Source-research mode:** Inspect the vault or supplied draft and any supplied references. Browse outside this material only when the user explicitly requests or authorizes an external check.
- **Content & visual inspection:** Read matching vault notes, linked bundle companions, and referenced local image assets via visual inspection before judging diagram correspondence or readability; never create scripts, edit vault files by default, or execute note code on the host.

## Six Audit Profiles (Respect Original Note Purpose)

Select the applicable audit profile(s) so an imported lecture note, compact reference, or manually formatted note is judged against its **intended purpose** rather than penalized for lacking Scriptorium-specific YAML or headings (default comprehensive audits evaluate relevant profiles while separating stylistic conformance from universal quality defects):

| Audit Profile | Evaluation Standard |
|---|---|
| **Factual** | Technical, mathematical, derivation, and evidence accuracy; causal mechanisms; parameter bounds, equality/tie-policy conditions, cost-component separation (reference vs. read/copy vs. index vs. query), empirical tendency vs. monotonic guarantee distinction, and claim validity |
| **Pedagogical** | Prerequisite closure, beginner accessibility throughout (detecting analogy-to-formalism cliffs), concrete-to-abstract progression (detecting generalized-first math inversion and operator dumping), concept-before-terminology, collapsed-state coherence, independent-application readiness, non-compressed later sections, and discriminating examples |
| **Presentation** | Textbook tone (flagging dramatic phrasing, AI signatures, and compressed shorthand), purposeful callouts and titles (detecting both overload and underutilization), focus/clarity of tables, math formatting, and multi-visual teaching/inspection clarity |
| **Scriptorium conformance** | Compliance with Scriptorium YAML, clickable TOC, formula folds, and `artifact_plan` rules *(apply only when auditing native Scriptorium notes or explicitly requested)* |
| **Bundle** | Cross-artifact consistency in notation, objective scaling, claims, and learning objectives |
| **Currency** | Version-sensitive library, API, framework, or standard claims flagged for verification |

For substantive mathematics, use [math_gates.md](../../core/math_gates.md) and [adversarial-theory-review.md](../../docs/procedures/review/adversarial-theory-review.md). Inspect the argument with folds closed, then check the actual derivation steps and conditions. When a strict source omits needed reasoning, identify the gap and distinguish repairs supported by the supplied text from additions that need permission.

## Output Structure & Actionable Findings

1. Resolve overall outcome: `accepted` · `accepted_with_disclosed_limitations` · `repair_required` · **`blocked`** (when target notes/vault access or required assets are inaccessible or insufficient to audit reliably), paired with a concise `quality_manifest` status block ([verification-checklist.md](../../docs/procedures/review/verification-checklist.md)).
2. Report concrete findings ordered by severity (**Critical**, **Major**, **Moderate**, **Minor**), explicitly separating **`confirmed`** defects, **`suspected`** issues, and **`unverifiable`** claims—using this structured finding contract (rendered cleanly in prose or structured bullets):

```yaml
finding:
  location: "<Note Title#Heading>"
  severity: "<critical | major | moderate | minor>"
  confidence: "<confirmed | suspected | unverifiable>"
  defect: "<exact technical, pedagogical, or consistency issue>"
  correction: "<specific targeted fix>"
  verification: "<how to verify the fix holds>"
  affected_artifacts: ["<theory | experimental_lab | mastery_pack>"]
```

3. Remain read-only until the learner explicitly approves targeted fixes or invokes `/scribe-notes`.

## Failure Handling

- If a required vault path is unconfigured or target inputs are missing or unreadable, return `blocked` (or report missing coverage) cleanly without fabricating findings.
- Do not claim unperformed code execution, uninspected image verification, unauthorized external lookups, or live Obsidian UI rendering checks.
