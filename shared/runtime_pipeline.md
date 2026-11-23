# Direct-authoring pipeline

During note creation, author content directly. Never create, execute, or modify scripts or project source code to assemble, render, validate, download, or publish notes.

This prohibition covers:
- Separate `.py`, `.js`, `.mjs`, `.cjs`, `.ts`, `.ps1`, `.sh`, `.bat`, or equivalent executable files.
- Inline interpreter commands, heredoc programs, generated functions, or temporary builders used as a substitute for separate files.
- Executable code hidden inside Markdown, JSON, configuration, or files with renamed extensions.
- Runtime patches or newly generated helpers used to bypass an unavailable capability.

## Workflow

1. Resolve the requested note type (`M1`–`M7`), scope, sources, and authorized Obsidian destination.
2. Read only the relevant master, subtemplate, and policies from `shared/` and `references/`.
3. Research claims and acquire/inspect required raster assets (`png`/`jpg`/`webp`) using native tools.
4. Author final Markdown directly and write notes/assets into the authorized destination (preserving unrelated notes).
5. Review actual Markdown, YAML, wikilinks, local embeds, and formula folds against [verification-checklist.md](../references/workflows/validation/verification-checklist.md).

Educational code examples may appear inside a note's Markdown fences when the lesson requires them; they remain lesson content, never the mechanism used to generate notes. If a capability (such as code execution, hash verification, or Obsidian UI rendering) cannot be established with available native tools, report that limitation honestly rather than claiming automated verification.
