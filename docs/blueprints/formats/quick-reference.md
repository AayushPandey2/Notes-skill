# M3 — Quick Reference & Rapid-Recall Cheat Sheet

*Master ID: `M3` (`quick_reference`, variants: `formula-sheet.md`, `syntax-reference.md`, `command-reference.md`, `atomic-card.md`). Artifact policy: `single_artifact` per [master-registry.yaml](../../dispatch/master-registry.yaml).*

- **Five Reference Profiles & Preset-Specific Budgets:** Count the complete authored body (including collapsed text) toward the selected profile budget—prioritizing retrieval accuracy and explicit validity conditions over mechanical truncation (if correctness genuinely requires exceeding the target, disclose why concisely):
  - **Atomic reference (`atomic-card`, typically under 150 words):** Recall one precise concept, micro-example, and boundary.
  - **Formula reference (`formula-sheet`, `<=500` words):** `Relationship | Symbols & Units | Applicability Conditions | Recognition Cue | Canonical Derivation Link`. Use inline/grouped relations with direct conditions and canonical derivation links instead of bulky repeated formula folds ([math_gates.md](../../../core/math_gates.md)).
  - **Operational / Command reference (`command-reference`, `<=600` words):** State version/platform scope, distinguish **read-only**, **state-changing**, and **destructive** operations, and follow the 5-column layout in [command-reference.md](../presets/command-reference.md).
  - **API / Syntax reference (`syntax-reference`, `<=600` words):** Document signature, relevant semantics (mutation/ownership/async only where applicable), return types, error conditions, and version constraints.
  - **Decision / General Cheat Sheet (default `M3`, `<=350` words, bullets `<=20` words):** Rapid condition-to-tool decision lookup and high-yield traps.
- **Placement & Header:** Save inside `<Configured Target>/<Topic>/` when part of a topic bundle, or `Cheatsheets/<topic-slug>-CHEAT-SHEET.md` only when explicitly requested as a standalone cross-topic sheet ([properties-policy.md](../../properties/properties-policy.md)), with line-1 Standard Obsidian Properties YAML + `# <Topic> — Cheat Sheet` (prepend `<nn>. ` only when the note belongs to a numbered multi-branch collection; never emit literal `<nn>` placeholders in standalone titles). Omit TOC and do not generate companion labs/cheatsheets.

## 1. Core Equations, Rules & Invariants at a Glance
At positive math depth, emit `> [!important] Core Equations & Bounds` with concise `$...$` or grouped `$$...$$` relations, symbol meanings, units, domain assumptions, and canonical derivation links. Under the `Conceptual` math profile, state concise prose invariants.

## 2. Condition-to-Tool Decision Block
Compact table: `If You See / Need... | Pick... | Why (1-Line Invariant) | Fatal Caveat`.

## 3. High-Yield Rules of Thumb & Exam/Operational Traps
- Concise scan-friendly rules retaining thresholds, syntax, and conditions.
- `> [!warning] One-Line Exam & Interview Traps`: `4–6` `_Trap_ -> _True Rule_` bullets + `[[Sibling Links]]` (when existing). Load [footer_widgets.md](../../../core/footer_widgets.md) **only** when the learner explicitly asks for a reflection/review footer; preserve native Obsidian compatibility without Dataview-specific default guidance (honoring explicitly requested compatible syntax).

## Compact `M3` Dependency Scope
- **Required:** `quick-reference.md`, active preset (if any), [authoring_rules.md](../../../core/authoring_rules.md), [properties-policy.md](../../properties/properties-policy.md), [tag-taxonomy.md](../../properties/tag-taxonomy.md) (for new managed tags), [verification-checklist.md](../../procedures/review/verification-checklist.md) (compact pass), and [math_gates.md](../../../core/math_gates.md) when equations, units, bounds, or applicability conditions are present (preserving full mathematical conditions, units, sign conventions, and table delimiters—not just LaTeX syntax).
- **Conditional:** [source-fidelity.md](../../procedures/sourcing/source-fidelity.md) (whenever a source is supplied, source-restricted, or external research applies—root source boundaries remain active throughout), [subject-registry.yaml](../../dispatch/subject-registry.yaml) -> primary `subjects/<p>.md` (only when a consequential domain convention, sign convention, or safety boundary applies), [revision-and-linking.md](../../procedures/updating/revision-and-linking.md) (only when revising existing notes or linking vault notes), and [footer_widgets.md](../../../core/footer_widgets.md) (only when requested).
- **Skip:** `teaching_core.md`, `theory_quality_contract.md`, `curriculum-discovery.md`, `adaptive-engine.md`, `experimental-lab.md`, `adversarial-theory-review.md`, `educational-editor.md`, `subject-theory-profiles.md`, and `investigations/`.
