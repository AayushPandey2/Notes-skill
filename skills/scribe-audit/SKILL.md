---
name: scribe-audit
description: Inspect existing Obsidian vault notes read-only for factual, mathematical, prerequisite, pedagogical, consistency, and presentation defects, proposing targeted corrections without rewriting the vault. Use for /scribe-audit or explicit quality-review requests on existing notes.
---

# `/scribe-audit`

## Purpose & Activation

Run a **read-only quality audit** over existing Obsidian vault learning notes and propose targeted, non-destructive repairs without rewriting the vault by default. Activate on `/scribe-audit`, `"audit my notes"`, or `"review my existing note quality"`.

## Inputs & Scope

- **Inputs:** Target note, bundle, folder path, or topic scope, plus the configured vault root from [pre-gen-gate.md](../../docs/procedures/authoring/pre-gen-gate.md).
- **Discovery:** Read only matching vault files (notes, linked bundle companions, and referenced local image metadata); do **not** modify vault files unless the user explicitly asks to apply specific repairs afterward, and never create scripts or execute note code on the host.

## 9-Dimension Audit Inspection

Follow [Command J](../../docs/procedures/authoring/command-playbooks.md#command-j--read-only-vault-quality-audit-scribe-audit), applying [adversarial-theory-review.md](../../docs/procedures/review/adversarial-theory-review.md), [educational-editor.md](../../docs/procedures/review/educational-editor.md), [verification-checklist.md](../../docs/procedures/review/verification-checklist.md), and [claim-verification.md](../../docs/procedures/sourcing/claim-verification.md) proportionally to the artifact type:

| Dimension | What to Inspect |
|---|---|
| **1. Theory** | Central mechanism depth (`0–5`), conceptual transitions, causal why-depth, and explanatory failure modes |
| **2. Mathematics** | Hypothesis validity, algebraic transitions, notation consistency, and grouped non-recursive formula folds |
| **3. Prerequisites** | Two-dimension prerequisite alignment (no unexplained essential symbols or concepts) |
| **4. Practical work** | API/operator soundness, edge cases, A–G walkthroughs, and honest 3-attribute experiment integrity |
| **5. Evidence** | Citation locators, source sufficiency, freshness, and qualified uncertain/conditional claims |
| **6. Presentation** | Line-1 YAML profile, clickable TOC, concise scannable tables, visual correspondence, zero Mermaid/highlighting |
| **7. Consistency** | Symbol/objective-scaling/fixture parity across Theory, Lab, and Mastery bundles |
| **8. Currency** | Version-sensitive API, library, or standard assumptions flagged clearly |
| **9. Mastery** | Assessment alignment with taught learning objectives and misconception diagnostics |

## Output Format

1. Summarize overall readiness (`accepted` · `accepted_with_disclosed_limitations` · `repair_required`) with a compact `quality_manifest` status block ([verification-checklist.md](../../docs/procedures/review/verification-checklist.md)).
2. List verified findings ordered by severity (**Critical**, **Major**, **Moderate**, **Minor**), citing exact `[[Note Title#Heading]]` locators and concrete defect descriptions.
3. Propose **targeted local fixes** (plus dependency-aware downstream checks) that the user can approve selectively or apply via `/scribe-notes`.

## Failure Handling

- If the vault path is unconfigured or target notes are missing, ask for the vault/note path cleanly without fabricating findings.
- Do not fabricate compiler execution results, live Obsidian UI rendering checks, or uninspected source verifications.
