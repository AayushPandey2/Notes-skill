<!-- scaffold:preflight
Master ID: M3 (quick_reference / compatibility route: cheat-sheet).
Primary intent: rapid_reference — high-density, fast-retrieval sheet (≤350 words, ≤20 words/bullet for default cheat sheet).
Activation signals: "cheat sheet", "quick reference", "formula sheet", "syntax sheet", "command reference", "atomic note" via `/scribe-notes`.
Non-activation: Do not select M3 when the user asks for deep explanation or explicitly negates a cheat sheet.
Variants: formula-sheet.md, syntax-reference.md, command-reference.md, atomic-card.md.
Pre-Flight: [router](../../../router.md) and [authoring rules](../../../shared/authoring_rules.md).
Strip this block before emission.
-->

# M3 — Quick Reference & Rapid-Recall Cheat Sheet

**Strict Quantitative Caps (default cheat sheet)**: Total Markdown body **≤350 words**; every ordinary bullet **≤20 words**. Measure directly before saving. Target 1 printed page / 1–2 screenfuls. Compression must **never** strip essential domain conditions, symbol definitions, or version caveats.
- **Routing & Destination Rules**:
    - Save cheatsheets inside the centralized sibling `Cheatsheets/` folder (`Cheatsheets/<topic-slug>-CHEAT-SHEET.md` or `Cheatsheets/<topic-slug>-<subtopic-slug>-CHEAT-SHEET.md`).
- **Header Block**: 5-key YAML frontmatter + `# <nn>. <Subtopic Title> — Cheat Sheet`.

## 1. What are the core equations and invariants at a glance? (Formulas & Complexity)

<!--
ADAPT to scan-friendly facts and necessary notation. Retain conditions for every bound or formula. Remove before publication.
-->

- `> [!abstract] Core Equations & Bounds`: At positive math levels, use compact display formulas (`$$...$$`), tight 1-line symbol definitions, applicability conditions, and asymptotic complexity table. At level 0, use prose invariants and omit this callout.

## 2. Which tool or variant do I pick under pressure? (Condition-to-Tool Decision Block)

<!--
KEEP compact cues for choices the reader is likely to face. State when the cue applies. Remove before publication.
-->

- Ultra-compact Markdown table: `If You See / Need... | Pick... | Why (1-Line Invariant) | Fatal Caveat`.

## 3. What are the highest-yield rules of thumb? (Scan-Friendly Key Facts)

<!--
KEEP only previously explained, high-yield facts and remove duplicates. Remove before publication.
-->

- Grouped high-signal bullets strictly **≤20 words per bullet** retaining exact conditions, thresholds, syntax arguments, and distinctions needed for rapid recall.

## 4. What traps catch people in exams and interviews? (One-Line Gotchas & Links)

<!--
KEEP consequential traps with short prevention cues and usable source or note links. Remove before publication.
-->

- `> [!caution] One-Line Exam & Interview Traps`: `4–6` razor-sharp `_Trap_ -> _True Rule_` bullets (≤20 words each).
- **Open Confusion**: `**Confusion** :: <1-line edge question>` + **Connection**: `[[Sibling Vault Links]]` + `dataviewjs` **Mark Revisited** button.

<!-- optional: selection -->
## [OPTIONAL] Which condition changes my choice? (Selection Cue)

<!--
Include only if the cue distinguishes two otherwise plausible choices. Remove before publication.
-->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: A single sharp conditional flip prevents likely exam/interview misuse and fits within the `≤350`-word cap.
- When to Omit Cleanly: Omit if Section 2 already covers the decision or if adding it breaches the `≤350`-word / `≤20`-word bullet cap. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: State the trigger, resulting choice, and decisive limitation in compact bullets (`≤20` words each); link the full comparison if available.
-->

- **Context:** State the decision trigger and constraint.
- **Analysis:** Name the resulting choice and decisive limitation (`≤20` words).
- **Check:** State the sanity check or linked full comparison.

See [authoring rules](../../../shared/authoring_rules.md), [math gates](../../../shared/math_gates.md), and [footer contract](../../../shared/footer_widgets.md).
- **Template Contract (`M3` / `cheat-sheet`):** Enforce the `≤350`-word body cap and `≤20`-word bullet cap; eliminate long motivation prose; preserve every formula's symbols and validity conditions.
