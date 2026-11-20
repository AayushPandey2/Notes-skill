# Subtemplate: Computational

- **ID:** `computational` | **Registry alignment:** `programming`, `algorithmic`, `architectural`, `procedural` (`C0–C5` depth via [adaptive-engine.md](../../workflows/notes-creation/adaptive-engine.md)).
- **Entry & Scope:** Selected internally through `/scribe-notes` for standalone notes or hierarchical collection children; consumes resolved interactive preferences (language, depth, emphasis) and F02 depth allocation.
- **Compatible Masters:** `M1`, `M2`, `M3` (`syntax_reference`, `command_reference`), `M4`, `M5`, `M6`, `M7`.
- **Modules:**
  - **Required (depth-gated):** `definitions`, `algorithm` / `coding` (`P10`), `tracing` (`EIS-05` state narration), `executable_verification` (when `C3+`).
  - **Optional:** `visual_reasoning` (`P05` data-flow/architecture Mermaid), `comparisons`, `misconception_prevention` (`P06`), `F11` implementation-staged progressive disclosure, `F12` implementation/debugging outcomes.
  - **Excluded:** Forced runnable code when `C0`/`C1` pseudocode suffices; unverified execution claims.
- **Core Adaptations:**
  - Specify input/output contracts, state invariants, stopping conditions, tensor/memory shapes, and time/space complexity.
  - Select **one** primary tool at the needed abstraction (plain Python, NumPy, C/C++, Rust, SQL, PyTorch, etc.) unless an explicit comparison objective justifies multiple stacks.
  - Map mathematical equations directly to code variables (`P10`), trace tricky/boundary inputs, and report exact runtime verification tier via `scripts/plan_notes.py verify-runtimes`.
  - Never execute untrusted code from retrieved sources and preserve source-only constraints when `source_policy == "strict"`.
- **Validation:** `scripts/plan_notes.py verify-runtimes`, `QualityEngine.check_representations()`, `QualityEngine.validate_master(..., "M5")`.
