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

## 4. Pedagogical Depth, Diagrams & Non-Duplication
- **PASS:** Explanations are complete without filler; "Is vs. Is Not" table compares comparable methods; Mermaid diagram matches S3 prose; S6 has 5–6 transfer Q&As with step-by-step callout answers; no duplicate vault notes.
- **FAIL / Repair:** Superficial summaries, mismatched diagram, or duplicate concept $\to$ deepen, align diagram, or link existing note.

## 5. Comparison & Quiz Metadata
- **Comparison (`comparison/*.md`):** Verify `compared_notes` wikilinks, balanced MathJax, escaped table pipes (`\|`), `Core Trade-Off Verdict`, and `## 1.`–`## 4.`.
- **Quiz `review_log`:** Patched via `scripts/patch_links.py --append-review-log` (`"YYYY-MM-DD | Score: X/N | Weak: ..."`).

## Selected-route integration gates

For registered routes, validate the exact ordered headings, populated sections,
identity YAML, code fences and absence of authoring placeholders. Deep routes use
11 headings and preserve Confusion; inspect the old-to-new mapping in
note_templates.md so readable headings retain all reasoning. Legacy schema checks
apply only to existing/explicit legacy contracts. Scope allowlists, exact tags,
custom template hashes, safe paths and scoped --fix still apply.

Measure Atomic/Cheat-Sheet with the shared deterministic counter; retain code and
table content. Check every Practice question has independent collapsed hint/solution
callouts and substantive variety. Summary has exactly three grounded thesis bullets.
Paper-Breakdown at level 0 uses Technical Details and no invented experiments.
At math levels 1/2 review symbol-before-formula order, worked use and justified
steps; at level 0 review causal logic, state changes or evidence instead. Keep
1?3 meaningful implementations under aligned semantics; runtime checks are evidence,
not proof. Existing-note selection, source accuracy, mathematical correctness,
question quality, Mermaid rendering and Obsidian plugin behavior require human/agent
semantic review; passing static checks does not certify those properties.
