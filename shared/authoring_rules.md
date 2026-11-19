# Shared authoring rules

## Metadata

Generated notes have strictly these 5 ordered YAML keys: `id`, `aliases`, `topic`, `tags`, `nexttopics`. IDs/topic are nonempty strings; the others are lists. Aliases include the title; tags stay clean and topic-relevant (do not require or inject a `deepstudy-master` tag); `nexttopics` contains resolved forward wikilinks. Reject legacy/extra keys (`title`, `base_domain`, `master_topic`, `track`, `math_level`, `status`, `prerequisites`, etc.). Keep routing flags, language and review logs in planning state or body fields, never extra YAML keys. Preserve existing IDs when editing.

## Rendering

Use native `$...$` and separate-line `$$` math delimiters. Never place code inside math. Quote every line of a callout, including blank lines and answers: an unquoted blank ends the block. Good: `> [!note] Assumption` followed by `> $x > 0$`; bad: an unquoted equation intended to remain inside that callout.

Escape literal pipes in Markdown tables, even inside code or wikilink aliases: `[[Target\|Label]]`. Quote Mermaid node labels and use Unicode symbols: good `A["x ? y"]`, bad `A["$x$"]`. For spatial geometry, physics schematics, function plots, and ML decision boundaries, embed real `.png` or `.svg` figures saved under `assets/<topic>/` (`![[assets/<topic>/<figure>.png]]`)—either extracted from verified open-license primary sources (e.g., OpenStax / Wikimedia Commons) or rendered cleanly with Matplotlib/SVG—instead of ASCII `text` art blocks; reserve `mermaid flowchart` / `sequenceDiagram` for causal pipelines, state machines, and protocol exchanges. Check rendering separately when available; syntax checks do not establish visual correctness.

Use `**Confusion** :: question` on its own line for Dataview. Do not emit empty or invented confusion. Strip scaffold comments, legacy `<!-- SECTION: S* -->` markers, authoring gates, optional markers, unused headings and placeholder rows before publication. If numbered sections are omitted, renumber retained sections consecutively and repair anchor links.

## Evidence

Read the full supporting passage before citing it. Cite near claims; record version/page/section when material. Never cite bare root domains/homepages (`https://gallica.bnf.fr/`, `https://arxiv.org/`, `https://archive.org/`, `https://openstax.org/`) in Primary Sources tables—omit the generic URL and mark `[UNVERIFIED]` if no specific deep link is verified. Distinguish source findings, inference, expected results and observed execution. When `language: "none"` (or no fenced code block exists), forbid execution claims (`executed via`, `Observed Execution Output`, `all assertions passed`); when code is not executed in a live shell, label `Status: static verification (not executed)` and never invent version strings.

## Cohesion

Explain the causal connection between ideas; use precise student-to-future-self prose and domain-natural headings (ban CS/architecture buzzwords like `"Computational Purpose"`, `"Position in the Broader Architecture"`, `"Taxonomic Lineage"`, `"Deep Theory Stack"`, `"Cross-Architecture Trade-Off"`, and `"Parameter Synthesis & Reverse-Engineering"` on non-software notes). Merge short opening material when it avoids repetition; give substantial missing prerequisites enough space before use. Deep-note mastery checks follow the objectives without a question quota; other routes retain their existing limits. Define notation at first use and keep asymmetric example values.

## Links and placement

Standardize sequential filenames and body wikilinks on `01 - <Title>.md` (never mix `02-hyphenated-slug` style with `01 - Title` naming). Existing notes must match exact on-disk filenames; planned future notes mentioned via forward wikilink (`[[02 - ...]]`) must be listed in YAML `nexttopics`, otherwise keep future mentions as plain text until created. Practice, atomic notes and cheatsheets live in sibling `Practice Sets/`, `Atomic Notes/`, and `Cheatsheets/` directories; compare outputs live in `comparison/`.

## Contracts

Math: [math_gates.md](math_gates.md). Routing and module selection: [note_decision_matrix.md](note_decision_matrix.md). Reflection implementation: [footer_widgets.md](footer_widgets.md). Machine checks implement schema, syntax and links; authors remain responsible for source fidelity and reasoning.
