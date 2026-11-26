# Preset: Formula Sheet (`M3` / `formula_sheet`)

- **Parent Master:** [M3 — Quick Reference](../formats/quick-reference.md) (`<=500`-word formula-reference budget; `single_artifact`).
- **Activation Trigger:** `"formula sheet"`, `"cheat sheet for ... formulas"` via `/scribe-notes`.

## Execution Overrides
1. **Density-Compatible Presentation ([math_gates.md](../../../core/math_gates.md)):** Use native `$...$`/`$$...$$` delimiters, notation stability, and compact inline/table formatting: `Relationship | Symbols & Units | Applicability Conditions | Recognition Cue | Canonical Derivation Link`—linking to canonical derivations rather than emitting repetitive full formula folds inside the sheet.
2. **Non-Negotiable Precision:** Never strip smoothness, convexity, independence, sign conventions, or domain assumptions to save words; under `strict` mode, extract only formulas from the supplied source with locators.
