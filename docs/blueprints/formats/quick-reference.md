# M3 — Quick Reference & Rapid-Recall Cheat Sheet

*Master ID: `M3` (`quick_reference`, variants: `formula-sheet.md`, `syntax-reference.md`, `command-reference.md`, `atomic-card.md`). Artifact policy: `single_artifact` per [master-registry.yaml](../../dispatch/master-registry.yaml).*

- **Five Reference Profiles & Preset-Specific Budgets:** Count the complete authored body (including collapsed text) toward the selected profile budget—prioritizing retrieval accuracy and explicit validity conditions over mechanical truncation (if correctness genuinely requires exceeding the target, disclose why concisely):
  - **Atomic reference (`atomic-card`, `<150` words):** Recall one precise concept, micro-example, and boundary.
  - **Formula reference (`formula-sheet`, `<=500` words):** `Relationship | Symbols & Units | Applicability Conditions | Recognition Cue | Canonical Derivation Link`. Use inline/grouped relations with direct conditions and canonical derivation links instead of bulky repeated formula folds ([math_gates.md](../../../core/math_gates.md)).
  - **Operational / Command reference (`command-reference`, `<=600` words):** Distinguish **read-only**, **state-changing**, and **destructive** operations; include `Command & Syntax | Preconditions/Permissions | Effect & Side Effects | Verification Check | Recovery | Version Notes`.
  - **API / Syntax reference (`syntax-reference`, `<=600` words):** Document signature, relevant semantics (mutation/ownership/async only where applicable), return types, error conditions, and version constraints.
  - **Decision / General Cheat Sheet (default `M3`, `<=350` words, bullets `<=20` words):** Rapid condition-to-tool decision lookup and high-yield traps.
- **Placement & Header:** Save inside `<Configured Target>/<Topic>/` when part of a topic bundle, or `Cheatsheets/<topic-slug>-CHEAT-SHEET.md` only when explicitly requested as a standalone cross-topic sheet ([properties-policy.md](../../properties/properties-policy.md)), with line-1 Standard Obsidian Properties YAML + `# <nn>. <Subtopic Title> — Cheat Sheet`. Omit TOC and do not generate companion labs/cheatsheets.

## 1. Core Equations, Rules & Invariants at a Glance
At positive math depth, emit `> [!abstract] Core Equations & Bounds` with concise `$...$` or grouped `$$...$$` relations, symbol meanings, units, domain assumptions, and canonical derivation links. Under the `Conceptual` math profile, state concise prose invariants.

## 2. Condition-to-Tool Decision Block
Compact table: `If You See / Need... | Pick... | Why (1-Line Invariant) | Fatal Caveat`.

## 3. High-Yield Rules of Thumb & Exam/Operational Traps
- Concise scan-friendly rules retaining thresholds, syntax, and conditions.
- `> [!caution] One-Line Exam & Interview Traps`: `4–6` `_Trap_ -> _True Rule_` bullets + optional `**Confusion** :: <1-line edge question>` + `[[Sibling Links]]` + [footer_widgets.md](../../../core/footer_widgets.md).

*Contract: [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), [verification-checklist.md](../../procedures/review/verification-checklist.md).*
