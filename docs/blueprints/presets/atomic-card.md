# Preset: Atomic Knowledge Card (`M3` / `atomic_card`)

- **Parent Master:** [M3 — Quick Reference](../formats/quick-reference.md) (`single_artifact`—never trigger companion lab/cheatsheet generation).
- **Activation Trigger:** `"/scribe-notes atomic note on <concept>"` or single-concept card item inside a collection.
- **Placement & Budget:** Save inside `<Configured Target>/<Topic>/` (or `Atomic Notes/<Canonical Concept Title>.md` if explicitly requested as standalone) with Standard Obsidian Properties YAML and the concept title. Aim for fewer than 150 words while preserving essential conditions. Omit the TOC and optional footer.

## Compact Structure (3 Core Parts)
1. **Claim & Definition (`2–3` sentences):** Precise definition + governing relation (`$$...$$` only when needed under [math_gates.md](../../../core/math_gates.md), with compact inline conditions).
2. **Micro-Example (`2–3` lines):** One concrete numerical, structural, or real-world example clarifying the claim.
3. **Boundary & Discriminating Non-Example (`1–2` sentences):** Primary boundary condition, limitation, or near-miss contrast.
4. **Vault Links *(compact bullets)*:** `Parent / Broader`, `Contrasts With`, `Used In` (mark unbuilt targets `(pending note)` in plain text—never fabricate dead wikilinks).
