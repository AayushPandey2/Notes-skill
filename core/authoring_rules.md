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

- **Spacing, Hierarchy & Navigation:** Separate opening metadata (`Difficulty`, `Prerequisites`, `Learning objectives`) with blank lines so renderers do not merge them into one paragraph, and provide a **clickable Obsidian Table of Contents** (`- [[#1. Heading|Label]]`). Keep paragraphs to 1–3 concise sentences (one concept per block; avoid long 200+ character source lines), insert blank lines between complex list items, maintain consistent multi-level numbered `H1–H4` headings (`## 5.` → `### 5.1` → `#### 5.1.1`) with short subject-first titles (never bold pseudo-headings), reserve `---` horizontal rules for major thematic transitions only, and apply bolding selectively.
- **Math & Callouts (No Highlighting):** Use native `$...$` (short symbols only) and separate-line `$$` delimiters, multiline `aligned` derivations, and consistent `\boxed{...}` emphasis ([math_gates.md](math_gates.md)). Do **not** use `==highlight==`, semantic highlight spans, or `\color{...}` anywhere in notes or formulas. Quote every line of a callout, including internal blank lines (`>`). In theory notes, keep core derivations and essential explanations visible using purposeful callouts (`[!info]`, `[!important]`, `[!example]`, `[!warning]`, and **visible** `[!question]` checkpoints with nested collapsed `> > [!success]- Reveal Answer`). In companion implementation labs ([experimental-lab.md](../docs/procedures/authoring/experimental-lab.md)), place detailed **A–G** walkthroughs inside `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` directly beneath every implementation's code block (and proportionate collapsed explanations beneath supporting setup blocks).
- **Tables:** Escape literal pipes inside Markdown tables (`[[Target\|Label]]` and inside inline math). Keep tables compact (avoid 5–6 column wide tables with formula headers; state constants above the table), keep cells concise, **right-align numerical columns** (`|---:|`), use human-readable semantic outcome labels (`0 — Fail`, `1 — Pass`) instead of bare `0`/`1`, mark selected/winning rows clearly (e.g., a `Selected` column or bold text—never `==highlight==`), and distinguish inputs from calculated outputs.
- **Visuals:** Follow [representations.md](../docs/procedures/authoring/representations.md): include **at least 4–5 relevant downloaded & inspected local web raster images** per generated content note (especially visualizing the **running dataset** and core geometric/trade-off concepts), control display width (`![[...|650]]`), separate image, 1-sentence caption, and `<span class="figure-source">` attribution with blank lines, and teach directly around each figure without commanding phrasing. **Never use Mermaid (`mermaid` blocks) or ASCII art/diagrams for graphs, charts, or flows.**
- **Publish Hygiene:** Use `**Confusion** :: question` on its own line for Dataview only when genuine. Strip all scaffold comments, `<!-- SECTION: S* -->` markers, authoring notes, unused optional sections, and placeholder rows; renumber remaining headings and repair any body internal anchors.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed execution. Never execute educational code or inspect local runtimes; label unexecuted code `Source and static review only; not compiled or executed here.`—never fabricate execution outputs or runtime parity.

## Cohesion

- Write clear, calm, direct reference prose per [teaching_core.md](teaching_core.md) with short subject-first headings (ban generic CS labels like `"Computational Purpose"`, `"Position in the Broader Architecture"`, `"Taxonomic Lineage"`, `"Deep Theory Stack"`, `"Cross-Architecture Trade-Off"`, `"Parameter Synthesis & Reverse-Engineering"`, artificial labels like `"Canonical fixture"`, `"Read aloud"`, `"Sanity check"`, `"Shape check"`, and scripted filler like `"We now..."`, `"Let us..."`, `"Notice how..."`). Qualify conditional statements rather than writing unsupported absolutes (e.g., library defaults vs. examples, tie-breaking rules, data-dependent complexity, uncalibrated vote proportions, leakage validity vs. direction), and never leave unedited self-correction transcripts (`"Wait—check the sign carefully!"`) or incorrect tables in finished notes.
- Give definitions and governing formulas one canonical home; state analogy breakdown boundaries; merge thin opening prose; align prose/math/visuals/code dimensions cleanly.
- Standardize sequential filenames and body wikilinks on `01 - <Title>.md` (never mix hyphen-slug and numbered styles). Always create a dedicated topic folder `<Configured Target>/<Topic>/` first (where `<Configured Target>` is the resolved vault/notes folder) and place everything created for that topic (main note, companion lab, cheatsheet/Q&A pack, subtopic bundles/MOC, and `assets/`) inside that `<Topic>/` folder—never save topic notes loose under the vault root or configured notes folder. Future planned notes linked in prose must appear in YAML `nexttopics`; otherwise keep future mentions as plain text.

## Validation

Review every output manually against [verification-checklist.md](../docs/procedures/review/verification-checklist.md) for YAML validity, delimiters, callout quoting, formula-fold parity, local image embeds, and internal wikilinks. Label this honestly as manual review rather than an automated test.
