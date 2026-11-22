# Shared Authoring Rules

## Purpose

Canonical specification for note frontmatter profiles, Obsidian Markdown/math/Mermaid rendering, source evidence hygiene, prose cohesion, and vault path/link integrity across every Scriptorium output.

## Activation Trigger

Always active across `/scribe-notes` and any vault write (`VaultEngine`, `scripts/validate_note.py`, `scripts/verify_vault_notes.py`).

## Metadata

Every note begins on line 1 with valid YAML (`---` ... `---`) matching its profile:
- **Comprehensive `M1` KCP v2 collections** ([composition-contract.md](../references/workflows/notes-creation/composition-contract.md)): strictly the 5 ordered keys `id`, `aliases`, `topic`, `tags`, `nexttopics` (nonempty strings for `id`/`topic`, lists for the rest; aliases include title; `domain/`/`subject/`/`topic/` tags; resolved forward wikilinks in `nexttopics`; zero extra keys).
- **Single notes, `M2`–`M7`, and legacy nested collections** ([properties-policy.md](../references/metadata/properties-policy.md)): canonical Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, plus managed optional keys via `VaultEngine`).

Never inject a `deepstudy-master` tag or internal review/routing logs into YAML; preserve existing IDs and custom user properties on updates.

## Rendering

- **Math & Callouts:** Use native `$...$` and separate-line `$$` delimiters without code inside math. Quote every line of a callout, including internal blank lines (`>`), because an unquoted blank ends the block.
- **Tables & Mermaid:** Escape literal pipes inside Markdown tables (`[[Target\|Label]]` and inside inline math). Quote Mermaid node labels and use Unicode symbols (`A["x → y"]`, never `A["$x$"]`).
- **Web-Image-First Visuals:** For schematics, architecture figures, geometry, and plots, follow [representations.md](../references/workflows/notes-creation/representations.md): acquire verified openly licensed raster images (`png`/`jpg`/`webp`), inspect pixels/labels, store locally under `assets/scriptorium/<collection-slug>/` (`![[assets/scriptorium/<collection-slug>/<figure>.png]]`), and teach via `Explain -> Show -> Decode -> Connect`. Programmatic SVG diagram synthesis is retired; report unavailable external visuals honestly instead of fabricating SVGs or ASCII boxes. Reserve Mermaid `flowchart` / `sequenceDiagram` for causal workflows and state transitions.
- **Publish Hygiene:** Use `**Confusion** :: question` on its own line for Dataview only when genuine. Strip all scaffold comments, `<!-- SECTION: S* -->` markers, authoring notes, unused optional sections, and placeholder rows; renumber remaining headings and repair internal anchors.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed runtime execution. When no runnable fenced code exists (`language: "none"`), forbid execution claims (`Observed Execution Output`, `all assertions passed`); label unexecuted code `Status: static verification (not executed)`. For runtime checks via `scripts/plan_notes.py verify-runtimes`, record runtime version and verbatim `stdout` under `### Verification — <stack>`, and include `Shared fixture:` + `Framework | Exposes | Hides | Pitfall` for multi-stack comparisons.

## Cohesion

- Write clear, beginner-respectful instructor prose per [teaching_core.md](teaching_core.md) with domain-natural headings (ban generic CS labels like `"Computational Purpose"`, `"Position in the Broader Architecture"`, `"Taxonomic Lineage"`, `"Deep Theory Stack"`, `"Cross-Architecture Trade-Off"`, `"Parameter Synthesis & Reverse-Engineering"` on non-software subjects).
- Give definitions and governing formulas one canonical home; state analogy breakdown boundaries; merge thin opening prose; align prose/math/visuals/code dimensions cleanly.
- Standardize sequential filenames and body wikilinks on `01 - <Title>.md` (never mix hyphen-slug and numbered styles). Place new collections directly under the configured vault target (`resolve_collection_layout`, `create_category_folders=false` default). Future planned notes linked in prose must appear in YAML `nexttopics`; otherwise keep future mentions as plain text.

## Validation

Machine verification (`scripts/validate_note.py`, `scripts/verify_vault_notes.py`) enforces schema, delimiters, callout quoting, fold parity, and links; authors/reviewers remain responsible for mathematical correctness and source fidelity.
