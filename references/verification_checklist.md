# Scriptorium Semantic Verification Checklist

Mechanical formatting checks (YAML syntax, mandatory keys, duplicate IDs, raw LaTeX in YAML, inline math spacing, delimiter balance, table pipe safety, placeholder tokens, wikilink/anchor resolution, Section 6 Q&A count, `> [!example]-` callouts, banned `<details>`/scaffolding labels, quoted headings, and Mermaid `$` checks) are enforced automatically by:

```bash
python3 "<skill_dir>/scripts/verify_vault_notes.py" "<vault_path>" --fix
```

Exit code `0` from `verify_vault_notes.py` is **necessary but not sufficient**. Use the semantic rubric below to audit what Python cannot verify.

---

## 1. Research & Source Integrity

- **PASS:** Every historical attribution, theorem, bound, and empirical claim matches a Tier 1–3 primary source; uncertain claims are omitted or marked `[UNVERIFIED]`; external URLs are real and non-placeholder.
- **FAIL:** Unverified claims presented as settled fact, misattributed priority, or fabricated/unverified citations.
- **Repair:** Verify against primary source or narrow/label claim as `[UNVERIFIED]`.

## 2. Mathematical & Derivation Validity

- **PASS:** Every symbol in `> [!abstract] Key Equations`, Section 3, Section 4, and Section 5 is defined consistently with domain, tensor shape/type, units, and sign convention; every Section 4 step is valid with zero skipped nontrivial transitions and explicit domain/division guards.
- **FAIL:** Shifting symbol meaning across sections, invalid algebraic/logical jumps, or missing validity conditions.
- **Repair:** Harmonize symbols across all sections and expand/correct invalid derivation steps.

## 3. Running-Example & Code Fidelity

- **PASS:** One named running example uses identical parameters/values across Sections 3, 4, and 5; Section 5 Python code faithfully implements the derived equation, handles boundary cases, and passes isolated execution without altering expected results to hide bugs.
- **FAIL:** Contradictory example values across sections, or Python code that diverges from Section 3–4 math.
- **Repair:** Align example values and fix Section 5 code/assertions to match the verified derivation.

## 4. Pedagogical Depth, Diagrams & Non-Duplication

- **PASS:** Conceptual explanations are complete without filler; Contrastive "Is vs. Is Not" table compares comparable tasks/assumptions; Mermaid diagram accurately depicts the mechanism; all 5–6 Section 6 questions test conceptual transfer with complete step-by-step callout answers; note does not duplicate an existing vault note.
- **FAIL:** Superficial summaries, mismatched diagram logic, repetitive Q&As, or concept duplication.
- **Repair:** Deepen incomplete explanations, align diagram nodes/edges with Section 3 prose, or merge/cross-reference duplicate concepts.
