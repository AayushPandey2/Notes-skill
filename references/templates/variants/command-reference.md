# Variant: Command Reference

- **Purpose:** Deliver a compact, workflow-grouped CLI command and flag lookup sheet preserving shell/OS safety caveats.
- **Parent Master:** [M3 — Quick Reference & Cheat Sheet](../masters/quick-reference.md) (`command_reference`)
- **Activation Trigger:** `"command reference"`, `"cli reference"`, `"flags summary"` via `/scribe-notes`.
- **Inputs & Dependencies:** Official CLI documentation, OS shell context (PowerShell vs. Bash), tested versions; [authoring_rules.md](../../../shared/authoring_rules.md).
- **Execution Overrides:**
  1. Group commands strictly by operational workflow (`Inspect`, `Create`, `Debug`, `Recover`) rather than alphabetical order.
  2. Emit dense tables: `Command & Key Flags | Effect | Concrete Example | Safety / Destructive Caveat`.
  3. Declare OS/shell assumptions and exact verified versions; never invent unverified flags.
- **Failure Handling & Validation:** Label destructive operations visibly; review syntax against [verification-checklist.md](../../workflows/validation/verification-checklist.md) (`<=350`-word default M3 target where applicable).
