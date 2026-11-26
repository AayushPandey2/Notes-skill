# Preset: Syntax & API Reference (`M3` / `syntax_reference`)

- **Parent Master:** [M3 — Quick Reference](../formats/quick-reference.md) (`<=600`-word API-reference budget; `single_artifact`).
- **Activation Trigger:** `"syntax reference"`, `"api table"`, or library workflow reference via `/scribe-notes`.

## Execution Overrides
1. **Separate Signature Lookup from Extended Cookbook Recipes:** Keep Section 1–2 concise for rapid lookup and place multi-call recipes in Section 3 on one shared example.
2. **Language-Relevant Semantics Only:** Explain only semantics applicable to the actual language/library (e.g., mutation, ownership/borrowing, async behavior, return types, error conditions, and version constraints)—never force array-view/memory-stride assumptions onto APIs where they do not apply.
3. **Workflow-Organized Lookup:** Group calls by task (`Initialization`, `Transform`, `Query`, `Error / Cleanup`) using `Signature | Key Parameters & Defaults | Return & Side Effects / Errors | Version / Complexity Notes` (escaping literal `|`). Label unexecuted recipes `Source and static review only; not compiled or executed here.`
