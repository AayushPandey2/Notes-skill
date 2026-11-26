# Preset: Command Reference (`M3` / `command_reference`)

- **Parent Master:** [M3 — Quick Reference](../formats/quick-reference.md) (`<=600`-word operational budget; `single_artifact`).
- **Activation Trigger:** `"command reference"`, `"cli reference"`, `"flags summary"` via `/scribe-notes`.

## Execution Overrides
1. **OS, Shell & Version Scope:** Declare exact OS, shell (Bash vs. PowerShell), permissions required, and verified tool versions (never invent unverified flags).
2. **Workflow Grouping & Safety Classification:** Group commands by workflow (`Inspect`, `Configure / Create`, `Debug`, `Recover`) and clearly tag **read-only**, **state-changing**, and **destructive** operations.
3. **Structured Lookup Fields:** Present `Command & Key Syntax | Preconditions / Permissions | Effect & Side Effects | Verification Check | Recovery / Reversal`.
