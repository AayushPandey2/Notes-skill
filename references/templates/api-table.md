# API-Table

**Purpose:** fast, accurate reference for a library, module, class, command family, or a small but parameter-dense API surface.

Use these headings in order:



## What is this for?

## How to think about it

## Common operations

## Recipes

## Gotchas / Performance

## Related notes / Sources

### Authoring contract

- **What is this for?** Identify package/tool, version or dialect, namespace, supported scope, and the tasks it solves. State what is deliberately outside this reference.
- **How to think about it:** Briefly explain the governing model before listing calls: axes/strides/views, iterator ownership, transaction state, command staging, or another relevant abstraction. Define shared notation and setup once. Include a level-1 formula only when needed, such as an output-shape rule; link longer theory.
- **Common operations:** Group by actual workflow, such as creation, selection, transformation, aggregation, linear algebra, or cleanup. Use **Function/signature | What it does | Key parameters | Returns / Mutates? | Quick example | Cost / Memory**. Split excessively wide tables into a main operation table and a contract/cost table keyed by the same operation instead of deleting useful content.
- State exact parameter semantics and defaults that matter, accepted types/shapes, return types/shapes, mutation, copy/view/alias behavior, and relevant errors. Distinguish a documented guarantee from an implementation detail. Verify version-sensitive behavior against official docs.
- Complexity and allocation claims need conditions. Mark a cost as unknown, implementation-dependent, or not applicable rather than inventing a universal bound.
- **Recipes:** Include 3–5 realistic runnable task recipes with shared setup, small input, expected output, and execution status. Use concise one-liners when readable; use several lines when validation or safe handling requires them.
- Include at least one meaningful edge case for a recipe, such as a zero-norm row, missing value, empty result, duplicate key, or transaction failure.
- **Gotchas / Performance:** Address silent incorrectness, axis/index confusion, dtype or overflow, views versus copies, hidden allocations, mutation, and expensive patterns as applicable. Explain the corrected usage.
- **Related notes / Sources:** Link mechanism notes and official deep API anchors. Keep source attribution close enough to resolve disputed behavior.
- Do not turn the API catalog into dozens of nearly identical deep notes or hide essential contracts behind vague “see documentation” links.
