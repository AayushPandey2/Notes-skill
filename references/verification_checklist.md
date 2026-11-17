# Scriptorium Semantic Verification Checklist

Mechanical formatting checks are enforced automatically by `verify_vault_notes.py --fix` and `vault_graph.py --check-cycles`. Exit code `0` is **necessary but not sufficient**—audit only what Python cannot verify:

## 1. Research & Source Integrity
- **PASS:** Claims, attributions, theorems, and bounds match Tier 1–3 primary sources; uncertain claims are `[UNVERIFIED]`; URLs are real.
- **FAIL / Repair:** Unverified claims stated as fact or fabricated citations $\to$ verify or label `[UNVERIFIED]`.

## 2. Mathematical & Derivation Validity
- **PASS:** Symbols in `Key Equations`, S3, S4, and S5 share identical domain, shape/type, units, and sign conventions; S4 skips no nontrivial steps and includes domain/division guards.
- **FAIL / Repair:** Shifting symbol meaning or invalid algebraic jumps $\to$ harmonize symbols and expand missing steps.

## 3. Running-Example & Code Fidelity
- **PASS:** One named running example uses identical values across S3–S5; S5 Python code matches S3–S4 math, handles boundary cases, and passes isolated execution without relaxed assertions.
- **FAIL / Repair:** Contradictory example values or code diverging from math $\to$ align example and fix S5 code.

## 4. Pedagogical Depth, Diagrams & Non-Duplication
- **PASS:** Explanations are complete without filler; "Is vs. Is Not" table compares comparable methods; Mermaid diagram matches S3 prose; S6 has 5–6 transfer Q&As with step-by-step callout answers; no duplicate vault notes.
- **FAIL / Repair:** Superficial summaries, mismatched diagram, or duplicate concept $\to$ deepen, align diagram, or link existing note.

## 5. Comparison & Quiz Metadata
- **Comparison (`comparison/*.md`):** Verify `compared_notes` wikilinks, balanced MathJax, escaped table pipes (`\|`), `Core Trade-Off Verdict`, and `## 1.`–`## 4.`.
- **Quiz `review_log`:** Patched via `scripts/patch_links.py --append-review-log` (`"YYYY-MM-DD | Score: X/N | Weak: ..."`).
