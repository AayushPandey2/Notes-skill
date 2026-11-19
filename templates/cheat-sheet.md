<!-- scaffold:preflight
Pre-Flight: [router](../router.md) and [authoring rules](../shared/authoring_rules.md).
Route: `cheat-sheet` (revision scope, ≤350 words, ≤20 words per bullet, optional `selection` module).
Strip this block before emission.
-->

# High-Density Pre-Exam & Interview Rapid-Recall Sheet

**Strict Quantitative Caps**: Total Markdown body **≤350 words**; every ordinary bullet **≤20 words**. Measure directly before saving. Target 1 printed page / 1–2 screenfuls.
- **Routing & Destination Rules**:
    - Save all cheatsheets (whether generated via `/scribe-distill <topic>` or routed to `cheat-sheet`) inside the centralized shared `Cheatsheets/` folder located at the **same directory level** (sibling level) as the `<subtopic>/` folders—never inside individual `<subtopic>/` folders.
    - Enforce clear topic/subtopic identifiers in the filename so cheatsheets from different topics/subtopics never collide (`Cheatsheets/<topic-slug>-CHEAT-SHEET.md` for topic-wide distill, or `Cheatsheets/<topic-slug>-<subtopic-slug>-CHEAT-SHEET.md` when scoped to a subtopic).
- **Header Block**: YAML frontmatter + `# <nn>. <Subtopic Title> — Cheat Sheet`.

## 1. What are the core equations and invariants at a glance? (Formulas & Complexity)

<!-- Authoring note: ADAPT to scan-friendly facts and necessary notation. Retain conditions for every bound. Remove this gate before publication. -->

- `> [!abstract] Core Equations & Bounds`: At positive math levels, use compact display formulas (`$$...$$`), tight 1-line symbol definitions, and asymptotic time/space complexity table. At level 0, use prose invariants and omit this callout.

## 2. Which tool or variant do I pick under pressure? (Condition-to-Tool Decision Block)

<!-- Authoring note: KEEP compact cues for choices the reader is likely to face. State when the cue applies. Remove this gate before publication. -->

- Ultra-compact Markdown table: `If You See / Need... | Pick... | Why (1-Line Invariant) | Fatal Caveat`.

## 3. What are the highest-yield rules of thumb? (Scan-Friendly Key Facts)

<!-- Authoring note: KEEP only previously explained, high-yield facts and remove duplicates. Remove this gate before publication. -->

- Grouped high-signal bullets strictly **≤20 words per bullet** retaining the exact conditions, thresholds, and distinctions needed for rapid recall.

## 4. What traps catch people in exams and interviews? (One-Line Gotchas & Links)

<!-- Authoring note: KEEP consequential traps with short prevention cues and usable source or note links. Remove this gate before publication. -->

- `> [!caution] One-Line Exam & Interview Traps`: `4–6` razor-sharp `_Trap_ -> _True Rule_` bullets (≤20 words each).
- **Open Confusion**: `**Confusion** :: <1-line edge question>` + **Connection**: `[[Sibling Vault Links]]` + `dataviewjs` **Mark Revisited** button.

<!-- optional: selection -->
## [OPTIONAL] Which condition changes my choice? (Selection Cue)

<!-- Authoring note: Include only if the cue distinguishes two otherwise plausible choices. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: A single sharp conditional flip prevents likely exam/interview misuse and fits within the `≤350`-word cap.
- When to Omit Cleanly: Omit if Section 2 already covers the decision or if adding it breaches the `≤350`-word / `≤20`-word bullet cap. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: State the trigger, resulting choice, and decisive limitation in compact bullets (`≤20` words each); link the full comparison if available.
-->

- **Context:** State the decision trigger and constraint.
- **Analysis:** Name the resulting choice and decisive limitation (`≤20` words).
- **Check:** State the sanity check or linked full comparison.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`cheat-sheet`):** Enforce the `≤350`-word total body cap and `≤20`-word bullet cap ruthlessly; eliminate historical narrative and multi-paragraph prose in favor of exact formulas, decision thresholds, complexity bounds, and exam/interview traps.
