# Scriptorium Semantic Verification Checklist

Mechanical formatting checks are enforced automatically by `verify_vault_notes.py --fix` and `vault_graph.py --check-cycles`. Exit code `0` is **necessary but not sufficient**—audit only what Python cannot verify:

## 1. Research & Source Integrity
- **PASS:** Claims, attributions, theorems, and bounds match Tier 1–3 primary sources; uncertain claims are `[UNVERIFIED]`; URLs are real.
- **FAIL / Repair:** Unverified claims stated as fact or fabricated citations $\to$ verify or label `[UNVERIFIED]`.

## 2. Mathematical & Derivation Validity
- **PASS:** Symbols in `Key Equations`, S3, S4, and S5 share identical domain, shape/type, units, and sign conventions; S4 skips no nontrivial steps and includes domain/division guards.
- **FAIL / Repair:** Shifting symbol meaning or invalid algebraic jumps $\to$ harmonize symbols and expand missing steps.

## 3. Running-Example & Multi-Implementation Code Fidelity
- **PASS:** One named running example uses identical values across S3–S5; all 1–3 Section 5 implementations match the topic's native domain stack, share identical test inputs/boundary cases/invalid-input guards, cross-verify identical expected outputs, and pass isolated execution without relaxed assertions.
- **FAIL / Repair:** Contradictory example values, trivial padding, or implementations diverging from S3–S4 math $\to$ align shared test contract and fix diverging code.

## 4. Pedagogical Depth, Humanization, Diagrams & Non-Duplication
- **PASS:** Passed the mandatory **Humanization & Cohesion Pass** (conversational yet rigorous student/engineer-to-future-self tone; logical narrative transitions explaining *why* one concept leads to the next; zero robotic AI clichés such as *"In conclusion," "It is important to note," "Delving into," "Crucial aspect," "Let's explore"*; synthesized mental models, analogies, and concrete examples rather than copy-pasted raw definitions); "Is vs. Is Not" table compares comparable methods; Mermaid diagram matches S3 prose; S6 has 5–6 transfer Q&As with step-by-step callout answers; no duplicate vault notes.
- **FAIL / Repair:** Robotic/stiff AI phrasing, banned filler clichés, abrupt isolated bullet dumps without narrative transitions, raw pasted definitions, superficial summaries, mismatched diagram, or duplicate concept $\to$ rewrite through the Humanization & Cohesion Pass, deepen, align diagram, or link existing note.

## 5. Comparison, Classnotes, Practice, Atomic & Quiz Metadata
- **Classnotes (`/scribe-classnotes`):** Verify multi-subtopic structure matches `/scribe-notes` layout, core notes use `templates/classnotes.md` (never `deepstudy-coding` or `deepstudy-general`), and `math_level` is `0` (no LaTeX/heavy derivations) unless the subject itself is inherently Mathematics, Physics, or quantitative engineering.
- **Comparison (`comparison/*.md`):** Verify `compared_notes` wikilinks, balanced MathJax, escaped table pipes (`\|`), `Core Trade-Off Verdict`, and `## 1.`–`## 5.` (`templates/comparison.md`).
- **Centralized Practice Sets (`Practice Sets/*.md`), Atomic Notes (`Atomic Notes/*.md`) & Cheatsheets (`Cheatsheets/*.md`):** Saved in their centralized sibling folders at the same directory level as `<subtopic>/` folders rather than nested inside individual `<subtopic>/` folders, with clear topic/subtopic identifiers in cheatsheet filenames to avoid collisions.
- **Quiz `review_log`:** Patched via `scripts/patch_links.py --append-review-log` (`"YYYY-MM-DD | Score: X/N | Weak: ..."`).
