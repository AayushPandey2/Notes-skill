# Subtemplate: Mathematical

- **ID:** `mathematical` | **Registry alignment:** `mathematical` (`M0–M5` depth via [adaptive-engine.md](../../workflows/notes-creation/adaptive-engine.md) and [math_gates.md](../../../shared/math_gates.md)).
- **Entry & Scope:** Selected internally through `/scribe-notes` for standalone notes or hierarchical collection children (never requires a separate slash command; consumes resolved interactive preferences and F02 depth allocation).
- **Compatible Masters:** `M1`, `M2`, `M3` (`formula_sheet`), `M4`, `M5`, `M6`, `M7`.
- **Modules:**
  - **Required (depth-gated):** `definitions`, `mathematics`, `representation_alignment` (`P03`), `EIS-03` derivation motivation (for `M1`/`M4`), `F09` notation governance.
  - **Optional:** `derivation` (`M4`), `proof` (`M5`), `worked_examples` (`P04`), `visual_reasoning` (`P05`), `F11` progressive disclosure, `F12` calculation/derivation outcomes.
  - **Excluded:** Unmotivated code blocks when `C0`, decorative non-mathematical analogies without breakdown disclosure.
- **Core Adaptations:**
  - Define symbols, domains, units, and shapes at first use; give each governing equation one canonical home and preserve source-specific notation (`E(W)` vs. `J(\theta)`) under `strict` mode.
  - Pair formal statements with geometric/intuitive interpretation and verified numerical traces (`EIS-05`, `P03`).
  - Justify every non-obvious transformation at `M4` (naming the rule and domain guard); supply quantified theorem hypotheses, proof, and counterexample at `M5`.
  - Never substitute intuition or a numerical check for a requested proof, and never strip validity conditions in condensed `M3`/`M7` outputs.
- **Validation:** `QualityEngine.check_representations()`, `PedagogyEngine.verify_trace()`, `shared/math_gates.md`, `F09` `CollectionTerminologyRegistry.validate_consistency()`.
