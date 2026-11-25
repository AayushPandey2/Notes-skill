# Companion Cheatsheet & Interview Q&A Pack (File 3)

For each newly generated **substantive non-video learning note** (`M1`, `M2`, `M5`—unless the user requests a single file), generate a **3-file topic bundle** (replacing the older 2-file note + lab model):
1. **File 1 — Learning Notes:** `<note stem>.md` (theory, intuition, foundations, visuals, derivations, and final mental model).
2. **File 2 — Experimental Lab:** `<note stem> - Experimental Lab.md` ([experimental-lab.md](experimental-lab.md)).
3. **File 3 — Cheatsheet & Interview Q&A:** `<note stem> - Cheatsheet & Interview Q&A.md` (this specification).

**Explicit exemptions (no companions unless explicitly requested):** `M3` quick-reference and all compact presets (`atomic-card`, `formula-sheet`, `syntax-reference`, `command-reference`, `quick-summary`), standalone `M6` assessments (`flashcards`, `mock-exam`), standalone `M4`/`M7` outputs, `/scribe-ytnotes` video notes, playlist indexes, MOCs, labs, cheatsheet packs, and internal workflow documents. Link File 1, File 2, and File 3 reciprocally, share the active YAML metadata profile ([properties-policy.md](../../properties/properties-policy.md)), and preserve identical notation, symbols, and source limits across all three files.

## Required Structure of File 3 (Subject-Adaptive)

Open with line-1 YAML frontmatter matching the active profile, an H1 title adapted to the discipline (`# <Topic> — Cheat Sheet, Interview Q&A & Practice` for technical/engineering topics, or `# <Topic> — Reference Sheet, Viva & Critical Thinking Pack` for humanities/natural sciences where software-interview framing is unnatural), and a concise reciprocal navigation callout linking back to `[[<Parent Note>]]` and `[[<Parent Note> - Experimental Lab]]`. Do **not** duplicate long prose derivations from File 1; keep File 3 dense, scannable, and self-testing.

### Section 1 — Subject-Adaptive Reference & Formula / Rule Cheat Sheet
Adapt subsections and applied problems to the actual discipline rather than forcing ML loss/gradient categories onto unrelated subjects:

| Subject | Reference Sheet Focus | Applied Problems Focus |
|---|---|---|
| **ML / DL** | Objectives, prediction, gradients, regularization, evaluation | Model calculations, metric trade-offs & failure diagnosis |
| **DSA / Programming** | Invariants, complexity, APIs, memory/state rules | Tracing, correctness proofs & debugging |
| **Full-Stack / Systems** | Protocols, APIs, request lifecycle, schemas, design rules | System design, request tracing & debugging |
| **Cybersecurity** | Security properties, trust boundaries, defensive controls | Vulnerability root-cause analysis & defensive verification |
| **Electrical** | Circuit laws, component models, transfer & timing rules | Circuit calculations, transient/AC analysis & fault diagnosis |
| **Mathematics / Stats** | Definitions, theorems, identities, conditions & cues | Proofs, calculations & assumption checks |
| **Physics / Chemistry** | Governing laws, units, reaction/equilibrium conditions | Physical modeling, stoichiometry & validity checks |
| **Biology** | Structures, pathways, regulation & experimental models | Mechanism tracing, data interpretation & disruption analysis |
| **History / Humanities** | Chronology, key actors/concepts, arguments & interpretations | Primary-source evaluation, argument critique & comparison |

- Present table-friendly rules in two-column `Concept | Formula / Rule` tables (using `$...$` inline math inside table cells, escaping literal pipes, and stating units/conditions).
- Present multi-line objectives, laws, or derivations in separate-line `$$...$$` blocks followed by `> [!example]- Understand this formula step by step` ([math_gates.md](../../../core/math_gates.md), non-recursive inside folds).

### Section 2 — Tiered Interview / Viva Questions & Answers (Tap-to-Reveal)
Provide **30 high-yield questions** by default for comprehensive topics (`10 Beginner`, `10 Intermediate`, `10 Advanced`)—scaling narrower or broader when actual topic coverage warrants—organized under three clear subheadings:
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
