---
name: scriptorium
description: Create, research, organize, and query Obsidian study notes, lecture summaries, mathematical derivations with collapsible step-by-step explanations, YouTube video & lecture notes (/scribe-ytnote), worked solutions, implementation guides, practice quizzes (/scribe-quiz), cheat sheets, and read-only vault Q&A (/scribe-doubt). Use whenever the user asks to generate, expand, summarize, or verify learning notes from topics, PDFs, URLs, or videos, or run /scribe-* commands in Obsidian.
---

# Scriptorium

Scriptorium is an instruction-and-reference-only Obsidian learning skill. It turns topics, PDFs, articles, and videos into beginner-clear, self-contained Obsidian notes using progressive disclosure so only the rules and templates needed for the active task enter context.

**Direct-authoring rule:** During note creation, author content directly. Never create, execute, or modify scripts or project source code (`.py`, `.js`, `.mjs`, `.ps1`, `.sh`, `.bat`, inline interpreter builders, or temporary helpers) to assemble, render, validate, download, or publish notes.

## Entry Commands

- `/scribe-notes` ([skills/scribe-notes](skills/scribe-notes/SKILL.md)): Universal note-creation gateway covering all seven masters (`M1`–`M7`), variants, interactive scope calibration, topic collections, and video/lecture notes (`/scribe-ytnote`, `/scribe-ytnotes`, `/scribe-ytlecture`).
- `/scribe-doubt` ([skills/scribe-doubt](skills/scribe-doubt/SKILL.md)): Read-only Q&A strictly grounded in existing vault notes with `[[Note Title]]` citations.
- `/scribe-quiz` ([skills/scribe-quiz](skills/scribe-quiz/SKILL.md)): One-question-at-a-time interactive recall over existing vault notes.
- `/scribe-setfolder` ([skills/scribe-setfolder](skills/scribe-setfolder/SKILL.md)): Persist the default target Obsidian notes folder in `~/.scriptorium-config.json`.

## Script-Free Workflow

1. **Resolve Scope & Destination:** Resolve vault destination (explicit path → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json`), master (`M1`–`M7`), variant, depth, source policy, and layout before writing prose—never run a pre-generation diagnostic quiz. See [router.md](router.md) and [routing-policy.md](references/routing/routing-policy.md).
2. **Load Only Required Context:** Consult [references/README.md](references/README.md) and read only the active master, variant, knowledge-type subtemplate, and policy needed for the request rather than bulk-loading `references/`.
3. **Research & Acquire Assets First:** Research primary claims with native search/read tools. For visual needs, find openly licensed raster images (`png`/`jpg`/`webp`), download them via native tools into `<Vault>/assets/scriptorium/<collection-slug>/`, and inspect each downloaded image via `read_file` before describing it ([representations.md](references/workflows/notes-creation/representations.md)). Programmatic SVG generation is retired; report unavailable visuals honestly.
4. **Author Beginner-First Markdown Directly:** Follow [shared/teaching_core.md](shared/teaching_core.md) and [shared/authoring_rules.md](shared/authoring_rules.md). Pair every displayed `$$...$$` equation with an immediately following `> [!note]- 📐 Understand this formula` callout ([shared/math_gates.md](shared/math_gates.md)), include complete `Step 1`–`12` worked examples, and write `Explain -> Show -> Decode -> Connect` around inspected visuals.
5. **Write, Review & Repair:** Write Markdown directly to `<Vault>/<Topic>/` (preserving existing notes, IDs, and custom YAML), review every file against [verification-checklist.md](references/workflows/validation/verification-checklist.md), and repair only defective spans. Disclose clearly when an automated check (such as code execution or Obsidian UI rendering) is unavailable.
