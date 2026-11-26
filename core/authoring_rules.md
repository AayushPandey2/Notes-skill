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

- **Spacing, Hierarchy & Accessibility:** Open substantive notes with separated metadata (`Difficulty`, `Prerequisites`, `Learning objectives`) and a **clickable Obsidian Table of Contents** (`- [[#1. Heading|Label]]`), without repeating YAML `difficulty` as a visible body dump. (*Precedence:* compact masters `M3`, `atomic-card`, and `M6` omit TOC.) Shape presentation by artifact role within existing formats: **Theory** prioritizes reading continuity and progressive reasoning; **Lab** prioritizes reproducibility, concrete traces, inputs/outputs, and failure diagnosis; **Mastery** prioritizes rapid retrieval, clear problem prompts, and collapsed solutions. Prefer short single-idea paragraphs (allowing longer coherent derivations), use meaningful question-driven or concise descriptive `H1–H4` headings without deep `5.2.1` nesting (never bold pseudo-headings), reserve `---` rules for major transitions, keep essential explanations understandable with all callouts collapsed, keep math/code lines readable on smaller screens, avoid relying on color alone, ensure navigation works without optional Obsidian plugins, and apply bolding selectively (reserve `\boxed{...}` for central numeric results).
- **Math & Callouts (No Highlighting):** Follow [math_gates.md](math_gates.md) as the single owner for math delimiters, `aligned`/`cases` formatting, non-recursive `> [!example]- Understand this formula step by step` folds beneath top-level `$$...$$` blocks, and operator parity. Do **not** use `==highlight==`, semantic highlight spans, `\color{...}`, code fences for equations, or raw LaTeX inside prose. Quote every line of a callout, including internal blank lines (`>`) and `$$` delimiters. Use purposeful visible callouts (`[!info]`, `[!important]`, `[!example]`, `[!warning]`, and visible `[!question]` checkpoints with nested `> > [!success]- Reveal Answer`). For companion labs, follow [experimental-lab.md](../docs/procedures/authoring/experimental-lab.md) (including A–G walkthroughs).
- **Definitions, Callouts & Tables:** Bold only the term being defined (never entire explanatory paragraphs), use short non-collapsed `[!info]` definition callouts sparingly (notes must read as connected explanation, not a stack of boxes), keep concrete examples beside definitions, separate definition/consequence/assumption/advanced property, and place comparison tables *after* explaining the compared ideas and working one candidate by hand. Escape literal pipes inside Markdown tables (`[[Target\|Label]]` and inside inline math). Keep each table focused on **one question** (never cramming 7 unrelated columns into one wide table), keep cells concise, **right-align numerical columns** (`|---:|`), use human-readable semantic outcome labels (`0 — Fail`, `1 — Pass`) instead of bare `0`/`1`, mark selected/winning rows clearly (without `==highlight==`), and distinguish inputs from calculated outputs.
- **Visuals:** Follow [representations.md](../docs/procedures/authoring/representations.md) as the single owner for visual relevance, source-only precedence (`strict` mode disables external web images), local raster acquisition/inspection, controlled display width (`![[...|650]]`), ordinary Markdown source/attribution lines (zero raw HTML), the Six-Phase Visual Narrative, and the Zero-Mermaid/ASCII rule.
- **Publish Hygiene:** Use `**Confusion** :: question` on its own line for Dataview only when genuine. Strip all scaffold comments, `<!-- SECTION: S* -->` markers, authoring notes, unused optional sections, and placeholder rows; renumber remaining headings and repair any body internal anchors.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed execution. Never execute educational code or inspect local runtimes; label unexecuted code `Source and static review only; not compiled or executed here.`—never fabricate execution outputs or runtime parity.

## Cohesion

- Write clear, calm, direct reference prose per [teaching_core.md](teaching_core.md) with question-driven subject headings (ban generic CS labels like `"Computational Purpose"`, `"Position in the Broader Architecture"`, `"Taxonomic Lineage"`, `"Deep Theory Stack"`, `"Cross-Architecture Trade-Off"`, `"Parameter Synthesis & Reverse-Engineering"`, artificial labels like `"Canonical fixture"`, `"Read aloud"`, `"Sanity check"`, `"Shape check"`, and scripted filler like `"We now..."`, `"Let us..."`, `"Notice how..."`). Flag and qualify strong claims (guaranteed calibration, optimum uniqueness/existence, outlier robustness, solver defaults, regularization conventions, universal preprocessing), and never leave unedited self-correction transcripts (`"Wait—check the sign carefully!"`) or incorrect tables in finished notes.
- Give definitions and governing formulas one canonical home; state analogy breakdown boundaries; merge thin opening prose; align prose/math/visuals/code dimensions cleanly.
- Standardize sequential filenames and body wikilinks on `01 - <Title>.md` (never mix hyphen-slug and numbered styles). Always create a dedicated topic folder `<Configured Target>/<Topic>/` first (where `<Configured Target>` is the resolved vault/notes folder) and place everything created for that topic (main note, companion lab, cheatsheet/Q&A pack, subtopic bundles/MOC, and `assets/`) inside that `<Topic>/` folder—never save topic notes loose under the vault root or configured notes folder. Future planned notes linked in prose must appear in YAML `nexttopics`; otherwise keep future mentions as plain text.

## Validation

Review every output manually against [verification-checklist.md](../docs/procedures/review/verification-checklist.md) for YAML validity, delimiters, callout quoting, formula-fold parity, local image embeds, and internal wikilinks. Label this honestly as manual review rather than an automated test.
