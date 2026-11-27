# Preset: Formula Sheet (`M3` / `formula_sheet`)

- **Parent Master:** [M3 — Quick Reference](../formats/quick-reference.md) (`<=500` prose words excluding YAML frontmatter and `$` / `$$` LaTeX math; `single_artifact`).
- **Activation Trigger:** `"formula sheet"`, `"cheat sheet for ... formulas"` via `/scribe-notes`.

## Execution Overrides
1. **Density-Compatible Presentation ([math_gates.md](../../../core/math_gates.md)):** Use native `$...$`/`$$...$$` delimiters, notation stability, and compact inline/table formatting: `Relationship | Symbols & Units | Applicability Conditions | Recognition Cue | Canonical Derivation Link`—linking to canonical derivations rather than emitting repetitive full formula folds inside the sheet. For independent non-strict formula sheets where formula application matters, include one compact worked or symbolic micro-trace (3–5 lines: condition -> selected formula -> substitution/step -> unit-checked result); omit on explicitly formula-only requests or strict sources that forbid outside examples.
2. **Non-Negotiable Precision:** Define every symbol appearing in the sheet (including auxiliary or critical variables) on first use, and never omit smoothness, convexity, independence, sign conventions, domain assumptions, or essential process/boundary conditions (e.g., adiabatic/insulated boundary on $Q=0$) to save words; under `strict` mode, extract only formulas from the supplied source with locators.
