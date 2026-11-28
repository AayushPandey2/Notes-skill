# Preset: Formula Sheet (`M3` / `formula_sheet`)

- **Parent Master:** [M3 — Quick Reference](../formats/quick-reference.md) (`<=500` prose words excluding YAML and `$`/`$$` math; `single_artifact`).
- **Activation Trigger:** `"formula sheet"`, `"cheat sheet for ... formulas"` via `/scribe-notes`.

## Execution Overrides
1. **Density-Compatible Presentation ([math_gates.md](../../../core/math_gates.md)):** Keep the parent M3 Core Equations & Bounds callout, Decision Block, and traps. Use native `$...$`/`$$...$$` math, stable notation, a compact formula table, and derivation links instead of repeated folds. For independent formula sheets where application matters, include one compact micro-trace (3–5 lines: condition -> formula -> substitution -> unit-checked result); a formula-sheet request alone does not mean "formulas only." Omit it only when application is irrelevant or the user explicitly requests no examples. For source-grounded sheets, retain in-scope source examples; add derived examples only when [source permissions](../../procedures/sourcing/source-fidelity.md) allow.
2. **Non-Negotiable Precision:** Define symbols on first use. Keep each formula's and usage rule's consequential assumptions attached, including in decision blocks and traps; distinguish a general relation from a simplified special case when the difference matters. Never drop parameter constancy, sign conventions, domains, or process/boundary conditions to save words. Under `strict` mode, extract only source-supported formulas with locators.
