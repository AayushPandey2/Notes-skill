# Preset: Formula Sheet (`M3` / `formula_sheet`)

- **Parent Master:** [M3 — Quick Reference](../formats/quick-reference.md) (`<=500` prose words excluding YAML and `$`/`$$` math; `single_artifact`).
- **Activation Trigger:** `"formula sheet"`, `"cheat sheet for ... formulas"` via `/scribe-notes`.

## Execution Overrides
1. **Density-Compatible Presentation ([math_gates.md](../../../core/math_gates.md)):** Use native `$...$`/`$$...$$` delimiters, notation stability, and compact inline/table formatting: `Relationship | Symbols & Units | Applicability Conditions | Recognition Cue | Canonical Derivation Link`—linking to canonical derivations rather than repeating full folds. For non-strict independent sheets where formula application matters, add one compact micro-trace (3–5 lines: condition -> formula -> substitution -> unit-checked result); omit on formula-only requests or `strict` sources.
2. **Non-Negotiable Precision:** Define every symbol (including critical/auxiliary variables) on first use, and never strip smoothness, convexity, independence, sign conventions, domains, or essential process/boundary conditions (e.g., adiabatic/insulated boundary on $Q=0$) to save words; under `strict` mode, extract only source-supported formulas with locators.
