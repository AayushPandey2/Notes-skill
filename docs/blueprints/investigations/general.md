# General Implementation Lab Blueprint

Use this lean, realization-focused blueprint when a named STEM or coding domain would impose irrelevant machinery (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed step-by-step walkthroughs, and honest verification.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, separate variation chapters, 10-step practical-workflow chapters, quizzes/challenges, or repetitive summaries. **Do not** insert Python, Rust, ML metrics, gradient descent, chemical apparatus, or physical measurements without genuine need.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Practical Realization Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Task, Inputs & Success Criteria
Briefly define the practical deliverable, given inputs/constraints, one small shared case, and concrete observable success criteria.

## Discipline-Appropriate Four-Track Realizations (Evidence-Oriented Profiles)

Select the matching discipline profile below rather than manufacturing fake experiments (using all 4 tracks for comprehensive topics, or the meaningful subset for narrower concepts):

| Domain | Track 1 | Track 2 | Track 3 | Track 4 |
|---|---|---|---|---|
| **History** | Primary-source analysis | Chronology reconstruction | Competing interpretations | Evidence & uncertainty limits |
| **Philosophy** | Argument reconstruction | Logical validity & soundness check | Objections & responses | Counterexamples & scope bounds |
| **Literature** | Close reading | Structural / formal analysis | Alternative interpretation | Textual evidence audit |
| **Linguistics** | Language data sample | Pattern & distribution analysis | Rule / grammar construction | Exceptions & variation |
| **Economics** | Analytical model | Concrete numerical example | Comparative statics (assumption shift) | Empirical validity & limits |
| **Psychology** | Construct operationalization | Study-design analysis | Data / effect interpretation | Confounds, bias & limitations |
| **Sociology** | Bounded case study | Theoretical interpretation | Comparative evidence | Alternative structural accounts |
| **Geography** | Spatial data fixture | Physical / human process analysis | Map / scale interpretation | Scale, boundary & uncertainty check |
| **General** | First-principles construction | Standard decision / method | Controlled assumption variation | Verification & failure analysis |

Directly beneath each realization, include `> [!example]- Understand this realization: method, steps, and worked dry run` (or `...implementation...` if code is genuinely required) covering **A–G**: **A** inputs & criteria; **B** governing principle; **C** step-by-step execution/argument order; **D** complete worked dry run (e.g., argument analysis, primary-source trace, or comparative-statics table); **E** interpretation; **F** failure cases & violated assumptions; **G** core-logic reconstruction.

## Verification Status

If code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Manual logical and criteria-based review only (no code executed).`**
