# Subtemplate: Scientific

- **ID:** `scientific` | **Registry alignment:** `scientific` (physics, chemistry, biology, engineering).
- **Entry & Scope:** Selected internally through `/scribe-notes` for standalone notes or hierarchical collection children; respects resolved interactive preferences, source policy, and F02 depth allocation.
- **Compatible Masters:** `M1`, `M2`, `M3` (`formula_sheet`), `M4`, `M6`, `M7`.
- **Modules:**
  - **Required (depth-gated):** `definitions`, `representation_alignment` (`P03` dimensional/unit checks), `limitations` (approximation regimes), `F09` scoped notation & unit governance.
  - **Optional:** `mathematics`, `experiment`, `worked_examples` (`P04`), `visual_reasoning` (`P05` geometric schematics), `F11` progressive disclosure.
  - **Excluded:** Forced software code unless computational simulation is an explicit user objective.
- **Core Adaptations:**
  - Ground laws in physical intuition, dimensional/unit consistency, coordinate conventions, and explicit approximation regimes (e.g., steady current, ideal gas, small-angle limit).
  - Use clean `.png`/`.svg` geometric schematics (`assets/<topic>/`) rather than Mermaid box chains for spatial geometry (`P05`).
  - Distinguish experimental measurements and error bounds from idealized theoretical models; preserve exact source scope under `strict` mode.
- **Validation:** `QualityEngine.check_representations()` (units/consistency), `F09` unit consistency, `KnowledgeEngine.verify_claim_links()`.
