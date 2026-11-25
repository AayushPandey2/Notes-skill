<!-- scaffold:preflight
Purpose: Deliver high-density, rapid-retrieval reference sheets strictly within word/bullet budgets without dropping governing validity conditions.
Master ID: M3 (quick_reference / compatibility route: cheat-sheet).
Activation Trigger: Explicit request for "cheat sheet", "quick reference", "formula sheet", "syntax sheet", "command reference", or "atomic note".
Non-activation: Never select M3 when the learner asks for deep explanation or explicitly negates a cheat sheet.
Inputs: Verified sibling notes or concise authoritative definitions, formulas with units/conditions, and common exam/operational traps.
Dependencies: router.md, core/authoring_rules.md, core/math_gates.md; variants formula-sheet.md, syntax-reference.md, command-reference.md, atomic-card.md.
Decision Rules: Default body <=350 words and bullets <=20 words; omit equations cleanly under the Conceptual math profile (core/math_gates.md); exempt from 3-file companion bundle generation unless explicitly requested.
Failure Handling: Never sacrifice essential domain restrictions or symbol definitions just to compress lines.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md) (`M3` quick-reference rules).
-->

# M3 — Quick Reference & Rapid-Recall Cheat Sheet

- **Hard Caps (Default Cheat Sheet):** Total Markdown body **<=350 words**; ordinary bullets **<=20 words** each; preserve every symbol definition, domain restriction, and version caveat.
- **Placement & Header:** Save inside `<Configured Target>/<Topic>/` when part of a topic bundle, or `Cheatsheets/<topic-slug>-CHEAT-SHEET.md` only when explicitly requested as a standalone cross-topic sheet ([properties-policy.md](../../properties/properties-policy.md)), with line-1 Standard Obsidian Properties YAML + `# <nn>. <Subtopic Title> — Cheat Sheet`. Omit TOC and do not generate companion labs/cheatsheets.

## 1. What are the core equations and invariants at a glance? (Formulas & Complexity)

At positive math depth, emit `> [!abstract] Core Equations & Bounds` with compact `$$...$$` relations, inline symbol meanings, domain assumptions, and complexity table. At level `0`, state concise prose invariants and omit the equation block.

## 2. Which tool or variant do I pick under pressure? (Condition-to-Tool Decision Block)

Compact table: `If You See / Need... | Pick... | Why (1-Line Invariant) | Fatal Caveat`.

## 3. What are the highest-yield rules of thumb? (Scan-Friendly Key Facts)

High-signal rules strictly **<=20 words per bullet** retaining thresholds, syntax arguments, and conditions.

## 4. What traps catch people in exams and interviews? (One-Line Gotchas & Links)

- `> [!caution] One-Line Exam & Interview Traps`: `4–6` `_Trap_ -> _True Rule_` bullets (`<=20` words each).
- **Open Confusion:** `**Confusion** :: <1-line edge question>` + `[[Sibling Links]]` + reflection footer ([footer_widgets.md](../../../core/footer_widgets.md)).

<!-- optional: selection -->
## [OPTIONAL] Which condition changes my choice? (Selection Cue)

<!-- Include only if needed to disambiguate a plausible flip within the <=350-word cap; delete completely otherwise. -->

- **Context / Analysis / Check:** Decision trigger, resulting choice (`<=20` words), and cross-reference link.

- **Contract Summary:** Verify word/bullet caps, equation assumptions, and link resolution ([authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md)).
