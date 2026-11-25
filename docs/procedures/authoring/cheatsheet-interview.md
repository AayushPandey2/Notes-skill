# Companion Cheatsheet & Interview Q&A Pack (File 3)

For each newly generated **substantive non-video learning note** (`M1`, `M2`, `M5`—unless the user requests a single file), generate a **3-file topic bundle** (replacing the older 2-file note + lab model):
1. **File 1 — Learning Notes:** `<note stem>.md` (theory, intuition, foundations, visuals, derivations, and final mental model).
2. **File 2 — Experimental Lab:** `<note stem> - Experimental Lab.md` ([experimental-lab.md](experimental-lab.md)).
3. **File 3 — Cheatsheet & Interview Q&A:** `<note stem> - Cheatsheet & Interview Q&A.md` (this specification).

**Explicit exemptions (no companions unless explicitly requested):** `M3` quick-reference and all compact presets (`atomic-card`, `formula-sheet`, `syntax-reference`, `command-reference`, `quick-summary`), standalone `M6` assessments (`flashcards`, `mock-exam`), standalone `M4`/`M7` outputs, `/scribe-ytnotes` video notes, playlist indexes, MOCs, labs, cheatsheet packs, and internal workflow documents. Link File 1, File 2, and File 3 reciprocally, share the active YAML metadata profile ([properties-policy.md](../../properties/properties-policy.md)), and preserve identical notation, symbols, and source limits across all three files.

## Required Structure of File 3

Open with line-1 YAML frontmatter matching the active profile, the H1 title (`# <Topic> — Cheat Sheet, Interview Q&A & Practice`), and a concise reciprocal navigation callout linking back to `[[<Parent Note>]]` and `[[<Parent Note> - Experimental Lab]]`. Do **not** duplicate long prose derivations from File 1; keep File 3 dense, scannable, and self-testing.

### Section 1 — Complete Formula / Rule Cheat Sheet
Organize core equations and rules into clean, domain-grouped subsections (for quantitative/ML topics: **Prediction Formulas**, **Probability / Core Relations**, **Loss & Optimization Formulas**, **Regularization / Constraint Formulas**, and **Evaluation Formulas**):
- Present table-friendly rules in two-column `Concept | Formula` or `Metric | Formula` tables (using `$...$` inline math inside table cells and escaping any literal pipes).
- Present multi-line objectives, gradients, and updates in separate-line `$$...$$` blocks followed by `> [!example]- Understand this formula step by step` (consistent with [math_gates.md](../../../core/math_gates.md)).
- Define special indicators (such as $\mathbb{1}[\cdot]$), domain restrictions, and numerical stability expressions explicitly.

### Section 2 — Tiered Interview Questions & Answers (Tap-to-Reveal)
Provide **30 high-yield interview questions** (or domain-scaled equivalent: `10 Beginner`, `10 Intermediate`, `10 Advanced`) organized under three clear subheadings:
- `### Beginner-Level Questions (Q1–Q10)`
- `### Intermediate-Level Questions (Q11–Q20)`
- `### Advanced-Level Questions (Q21–Q30)`

**Mandatory Collapsible Answer Rule:** Every single answer **must** be hidden inside an Obsidian collapsed callout (`> [!tip]- Answer`) so the learner sees only the question until they tap to reveal it. Quote **every** line inside the callout (including blank separator lines and `$$...$$` math blocks with `>`) and place an unquoted blank line before the next question so expanding one answer never reveals another:

````markdown
**Q<k>. <Clear, specific interview question>**

> [!tip]- Answer
> <Direct, technically precise answer with intuition, formulas, or edge-case reasoning.>
````

### Section 3 — Practice Problems with Worked Solutions (Tap-to-Reveal)
Provide **5+ multi-step applied practice problems** (covering prediction/inference, loss calculation, boundary/threshold calculation, probability/odds or core mechanism transforms, and a multi-step update/verification problem):
- State the **Given** values and exact task visibly under each problem heading (`### Problem <k>: <Title>`).
- Place the complete step-by-step derivation, boxed final answer (`\boxed{...}`), and explicit verification check inside a collapsed `> [!tip]- Solution` callout so the learner can attempt the problem before tapping to reveal the solution.

## Failure Handling & Review

Reject visible uncollapsed interview answers, missing collapsible `> [!tip]-` prefixes (notice the trailing `-` for collapsed-by-default in Obsidian), unquoted blank lines breaking callouts, incompatible `\(...\)` / `\[...\]` delimiters, or notation drift against File 1 and File 2 ([verification-checklist.md](../review/verification-checklist.md)).
