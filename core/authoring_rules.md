# Shared Authoring Rules

## Purpose

Canonical specification for note frontmatter profiles, Obsidian Markdown/math/Mermaid rendering, source evidence hygiene, prose cohesion, and vault path/link integrity across every Scriptorium output.

## Activation Trigger

Always active across `/scribe-notes` and any vault write. Follow [the direct-authoring pipeline](runtime_pipeline.md): author Markdown directly; never generate or run scripts to assemble, render, validate, download, or publish notes.

## Metadata

Every note begins on line 1 with valid YAML (`---` ... `---`) matching its profile:
- **Comprehensive `M1` collections** ([composition-contract.md](../docs/procedures/authoring/composition-contract.md)): strictly the 5 ordered keys `id`, `aliases`, `topic`, `tags`, `nexttopics` (nonempty strings for `id`/`topic`, lists for the rest; aliases include title; `domain/`/`subject/`/`topic/` tags; resolved forward wikilinks in `nexttopics`; zero extra keys).
- **Single notes, `M2`–`M7`, and legacy nested collections** ([properties-policy.md](../docs/properties/properties-policy.md)): canonical Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, plus managed optional keys).

Never inject a `deepstudy-master` tag or internal review/routing logs into YAML; preserve existing IDs and custom user properties on updates.

## Rendering

- **Math & Callouts:** Use native `$...$` and separate-line `$$` delimiters without code inside math. Quote every line of a callout, including internal blank lines (`>`), because an unquoted blank ends the block.
- **Tables & Mermaid:** Escape literal pipes inside Markdown tables (`[[Target\|Label]]` and inside inline math). Quote Mermaid node labels and use Unicode symbols (`A["x → y"]`, never `A["$x$"]`).
- **Visuals:** Follow [representations.md](../docs/procedures/authoring/representations.md): preserve native Mermaid for suitable relationships, and count an external raster image only after source check, local download and inspection, embed, and saved-note target check.
- **Publish Hygiene:** Use `**Confusion** :: question` on its own line for Dataview only when genuine. Strip all scaffold comments, `<!-- SECTION: S* -->` markers, authoring notes, unused optional sections, and placeholder rows; renumber remaining headings and repair internal anchors.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed execution. When code in a Markdown fence has not been executed, label it `Status: static review (not executed)`—never fabricate execution outputs or runtime parity.

## Cohesion

- Write clear, beginner-respectful instructor prose per [teaching_core.md](teaching_core.md) with domain-natural headings (ban generic CS labels like `"Computational Purpose"`, `"Position in the Broader Architecture"`, `"Taxonomic Lineage"`, `"Deep Theory Stack"`, `"Cross-Architecture Trade-Off"`, `"Parameter Synthesis & Reverse-Engineering"` on non-software subjects).
- Give definitions and governing formulas one canonical home; state analogy breakdown boundaries; merge thin opening prose; align prose/math/visuals/code dimensions cleanly.
- Standardize sequential filenames and body wikilinks on `01 - <Title>.md` (never mix hyphen-slug and numbered styles). Place new collections directly under the configured vault target (`create_category_folders=false` default). Future planned notes linked in prose must appear in YAML `nexttopics`; otherwise keep future mentions as plain text.

## Validation

Review every output manually against [verification-checklist.md](../docs/procedures/review/verification-checklist.md) for YAML validity, delimiters, callout quoting, formula-fold parity, local image embeds, and internal wikilinks. Label this honestly as manual review rather than an automated test.
