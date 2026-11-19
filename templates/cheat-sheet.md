<!-- scaffold:preflight
Decision-Matrix Pre-Flight: [routing index](../shared/note_decision_matrix.md) and [shared decision guide](../shared/notes_decision_matrix.md).
Switches: D01 route (`cheat-sheet`); D02 revision scope; D03 reader; D04 rapid-recall outcome; D05 vault-notes extraction;
D06–D09 `math_level` (compact bounds); D10 high-yield cues; D11 compact table; D12–D13 omit runnable code; D14 optional module (`selection`); D15 audit (≤350 words).
Strip this block before emission. Load detailed DM branches only when active.
-->

# High-Density Pre-Exam & Interview Rapid-Recall Sheet

**Strict Quantitative Caps**: Total Markdown body **≤350 words**; every ordinary bullet **≤20 words**. Measure directly before saving. Target 1 printed page / 1–2 screenfuls.
- **Routing & Destination Rules**:
    - Save all cheatsheets (whether generated via `/scribe-distill <topic>` or routed to `cheat-sheet`) inside the centralized shared `Cheatsheets/` folder located at the **same directory level** (sibling level) as the `<subtopic>/` folders—never inside individual `<subtopic>/` folders.
    - Enforce clear topic/subtopic identifiers in the filename so cheatsheets from different topics/subtopics never collide (`Cheatsheets/<topic-slug>-CHEAT-SHEET.md` for topic-wide distill, or `Cheatsheets/<topic-slug>-<subtopic-slug>-CHEAT-SHEET.md` when scoped to a subtopic).
- **Header Block**: YAML frontmatter + `# <nn>. <Subtopic Title> — Cheat Sheet`.

## 1. What are the core equations and invariants at a glance? (Formulas & Complexity)

<!-- Gate: DM-06, DM-07, DM-09, DM-19.
ADAPT to scan-friendly facts and necessary notation. Retain conditions for every bound. Remove this gate before publication. -->

- `> [!abstract] Core Equations & Bounds`: At positive math levels, use compact display formulas (`$$...$$`), tight 1-line symbol definitions, and asymptotic time/space complexity table. At level 0, use prose invariants and omit this callout.

## 2. Which tool or variant do I pick under pressure? (Condition-to-Tool Decision Block)

<!-- Gate: DM-03, DM-19.
KEEP compact cues for choices the reader is likely to face. State when the cue applies. Remove this gate before publication. -->

- Ultra-compact Markdown table: `If You See / Need... | Pick... | Why (1-Line Invariant) | Fatal Caveat`.

## 3. What are the highest-yield rules of thumb? (Scan-Friendly Key Facts)

<!-- Gate: DM-02, DM-19, DM-20.
KEEP only previously explained, high-yield facts and remove duplicates. Remove this gate before publication. -->

- Grouped high-signal bullets strictly **≤20 words per bullet** retaining the exact conditions, thresholds, and distinctions needed for rapid recall.

## 4. What traps catch people in exams and interviews? (One-Line Gotchas & Links)

<!-- Gate: DM-05, DM-19, DM-20.
KEEP consequential traps with short prevention cues and usable source or note links. Remove this gate before publication. -->

- `> [!caution] One-Line Exam & Interview Traps`: `4–6` razor-sharp `_Trap_ -> _True Rule_` bullets (≤20 words each).
- **Open Confusion**: `**Confusion** :: <1-line edge question>` + **Connection**: `[[Sibling Vault Links]]` + `dataviewjs` **Mark Revisited** button.

<!-- optional: selection -->
## [OPTIONAL] Which condition changes my choice? (Selection Cue)

<!-- Gate: DM-11, DM-19.
Include only if the cue distinguishes two otherwise plausible choices. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: A single sharp conditional flip prevents likely exam/interview misuse and fits within the `≤350`-word cap; D04, D14.
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
