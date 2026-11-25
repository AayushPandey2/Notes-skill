# Shared Authoring Rules

## Purpose

Canonical specification for note frontmatter profiles, Obsidian Markdown/math rendering, source evidence hygiene, prose cohesion, and vault path/link integrity across every Scriptorium output.

## Activation Trigger

Always active across `/scribe-notes` and any vault write. Follow [the direct-authoring pipeline](runtime_pipeline.md): author Markdown directly; never generate or run scripts to assemble, render, validate, download, or publish notes.

## Metadata

Every note begins on line 1 with valid YAML (`---` ... `---`) matching its profile:
- **Comprehensive `M1` collections** ([composition-contract.md](../docs/procedures/authoring/composition-contract.md)): strictly the 5 ordered keys `id`, `aliases`, `topic`, `tags`, `nexttopics` (nonempty strings for `id`/`topic`, lists for the rest; aliases include title; `domain/`/`subject/`/`topic/` tags; resolved forward wikilinks in `nexttopics`; zero extra keys).
- **Single notes, `M2`–`M7`, and legacy nested collections** ([properties-policy.md](../docs/properties/properties-policy.md)): canonical Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, plus managed optional keys).

Never inject a `deepstudy-master` tag, any `type/<note-type>` tag, or internal review/routing logs into YAML; preserve existing IDs and custom user properties on updates.

## Rendering

- **Spacing, Hierarchy & Bolding:** Separate opening metadata (`Difficulty`, `Prerequisites`, `Learning objectives`) with blank lines so renderers do not merge them into one paragraph. Keep paragraphs to 1–3 sentences (one idea per paragraph), insert blank lines between complex list items, maintain a consistent `H1–H4` heading hierarchy (never use bold text as section headings), use short navigable headings, and apply bolding selectively rather than decorating every technical phrase.
- **Math & Callouts:** Use native `$...$` and separate-line `$$` delimiters without code inside math; keep inline math short and use multiline `aligned` blocks for derivations ([math_gates.md](math_gates.md)). Quote every line of a callout, including internal blank lines (`>`), because an unquoted blank ends the block. In theory notes, keep core derivations and essential explanations visible using purposeful callouts (`Definition`, `Intuition`, `Worked example`, `Common mistake`) rather than repeating `> [!note]- 📐 Understand this formula`. In companion implementation labs ([experimental-lab.md](../docs/procedures/authoring/experimental-lab.md)), place detailed **A–G** walkthroughs inside `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` directly beneath every implementation's code block (and proportionate collapsed explanations beneath supporting setup blocks).
- **Tables:** Escape literal pipes inside Markdown tables (`[[Target\|Label]]` and inside inline math). Keep tables compact (avoid 5–6 column wide tables with formula headers; state constants above the table instead of repeating identical values across rows), keep cells concise (no paragraph-length cells), **right-align numerical columns** (`|---:|`), and visually distinguish inputs from calculated outputs.
- **Visuals:** Follow [representations.md](../docs/procedures/authoring/representations.md): include **at least 4–5 relevant downloaded & inspected local web raster images** per generated content note and teach directly around each figure. **Never use Mermaid (`mermaid` blocks) or ASCII art/diagrams for graphs, charts, or flows.** Count an external raster image only after source check, local download and inspection, embed, and saved-note target check.
- **Publish Hygiene:** Use `**Confusion** :: question` on its own line for Dataview only when genuine. Strip all scaffold comments, `<!-- SECTION: S* -->` markers, authoring notes, unused optional sections, and placeholder rows; renumber remaining headings, keep Table of Contents entries as plain numbered text with zero links, and repair any body internal anchors.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed execution. Never execute educational code or inspect local runtimes; label unexecuted code `Source and static review only; not compiled or executed here.`—never fabricate execution outputs or runtime parity.

## Cohesion

- Write clear, natural instructor prose per [teaching_core.md](teaching_core.md) with short domain-natural headings (ban generic CS labels like `"Computational Purpose"`, `"Position in the Broader Architecture"`, `"Taxonomic Lineage"`, `"Deep Theory Stack"`, `"Cross-Architecture Trade-Off"`, `"Parameter Synthesis & Reverse-Engineering"` on non-software subjects, as well as artificial labels like `"Canonical fixture"`, `"Read aloud"`, `"Sanity check"`, and `"Shape check"`). Qualify conditional statements rather than writing unsupported absolutes (`necessarily`, `always`, `dramatically lowers`, `prevents overfitting`), and never leave unedited self-correction transcripts (`"Wait—check the sign carefully!"`) or incorrect tables in finished notes.
- Give definitions and governing formulas one canonical home; state analogy breakdown boundaries; merge thin opening prose; align prose/math/visuals/code dimensions cleanly.
- Standardize sequential filenames and body wikilinks on `01 - <Title>.md` (never mix hyphen-slug and numbered styles). Place new collections directly under the configured vault target (`create_category_folders=false` default). Future planned notes linked in prose must appear in YAML `nexttopics`; otherwise keep future mentions as plain text.

## Validation

Review every output manually against [verification-checklist.md](../docs/procedures/review/verification-checklist.md) for YAML validity, delimiters, callout quoting, formula-fold parity, local image embeds, and internal wikilinks. Label this honestly as manual review rather than an automated test.
