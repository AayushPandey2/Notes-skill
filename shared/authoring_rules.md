# Shared authoring rules

## Metadata

Every generated note begins on line 1 with valid YAML frontmatter (`---` ... `---`) matching its output profile:
- **Comprehensive M1 KCP v2 collections** ([composition-contract.md](../references/workflows/notes-creation/composition-contract.md)): strictly the 5 ordered YAML keys `id`, `aliases`, `topic`, `tags`, `nexttopics` (nonempty strings for `id`/`topic`, lists for the rest; aliases include the title; hierarchical `domain/`, `subject/`, `topic/` tags; resolved forward wikilinks in `nexttopics`; zero extra keys — planning state and manifests live under `.scriptorium/collections/`).
- **Single notes, `M2`–`M7` outputs, and legacy nested collections** ([properties-policy.md](../references/metadata/properties-policy.md)): standard Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, plus optional managed fields such as `id`, `aliases`, `nexttopics`, `parent_topic`, `collection_id`, `prerequisites`, `related`, `source_mode`, `status`, `created`, `updated` via `VaultEngine`).

Do not inject a `deepstudy-master` tag or dump internal routing/review logs into YAML frontmatter. Preserve existing IDs and custom user properties when editing.

## Rendering

Use native `$...$` and separate-line `$$` math delimiters. Never place code inside math. Quote every line of a callout, including blank lines and answers: an unquoted blank ends the block. Good: `> [!note] Assumption` followed by `> $x > 0$`; bad: an unquoted equation intended to remain inside that callout.

Escape literal pipes in Markdown tables, even inside code or wikilink aliases: `[[Target\|Label]]`. Quote Mermaid node labels and use Unicode symbols: good `A["x → y"]`, bad `A["$x$"]`. For spatial geometry, physics schematics, architecture diagrams, function plots, and ML decision boundaries, follow the web-image-first BVIA/LAVIA workflow ([representations.md](../references/workflows/notes-creation/representations.md)): reuse or acquire verified openly licensed figures first, persist them under `assets/scriptorium/<collection-slug>/` (`![[assets/scriptorium/<collection-slug>/<figure>.png]]`), and fall back to deterministic SVG/plots only with a documented fallback gate or equation/data justification—paired with an `Explain -> Show -> Decode -> Connect` walkthrough instead of ASCII `text` art blocks; reserve `mermaid flowchart` / `sequenceDiagram` for causal pipelines, state machines, and protocol exchanges. Check rendering separately when available; syntax checks do not establish visual correctness.

Use `**Confusion** :: question` on its own line for Dataview. Do not emit empty or invented confusion. Strip scaffold comments, legacy `<!-- SECTION: S* -->` markers, authoring gates, optional markers, unused headings and placeholder rows before publication. If numbered sections are omitted, renumber retained sections consecutively and repair anchor links.

## Evidence

Read the full supporting passage before citing it. Cite near claims; record version/page/section when material. Never cite bare root domains/homepages (`https://gallica.bnf.fr/`, `https://arxiv.org/`, `https://archive.org/`, `https://openstax.org/`) in Primary Sources tables—omit the generic URL and mark `[UNVERIFIED]` if no specific deep link is verified. Distinguish source findings, inference, expected results and observed execution. When `language: "none"` (or no fenced code block exists), forbid execution claims (`executed via`, `Observed Execution Output`, `all assertions passed`); when code is not executed in a live shell, label `Status: static verification (not executed)` and never invent version strings. When an implementation is executed via `plan_notes.py verify-runtimes`, record its exact status, runtime version, and verbatim `stdout` under `### Verification — <stack>`. For multi-stack comparisons, document the common inputs and parameters in a `Shared fixture:` field and include a `Framework | Exposes | Hides | Pitfall` comparison table.

## Cohesion

Explain the causal connection between ideas; use precise student-to-future-self prose and domain-natural headings (ban CS/architecture buzzwords like `"Computational Purpose"`, `"Position in the Broader Architecture"`, `"Taxonomic Lineage"`, `"Deep Theory Stack"`, `"Cross-Architecture Trade-Off"`, and `"Parameter Synthesis & Reverse-Engineering"` on non-software notes). Merge short opening material when it avoids repetition; give substantial missing prerequisites enough space before use. When using an analogy, state its explicit mapping and the adjacent boundary where the analogy breaks so intuition never imports false properties. Deep-note mastery checks follow the objectives without a question quota; other routes retain their existing limits. Define notation at first use and keep asymmetric, non-square example values that expose axis, broadcast, or order bugs.

## Links and placement

Standardize sequential filenames and body wikilinks on `01 - <Title>.md` (never mix `02-hyphenated-slug` style with `01 - Title` naming). Existing notes must match exact on-disk filenames; planned future notes mentioned via forward wikilink (`[[02 - ...]]`) must be listed in YAML `nexttopics`, otherwise keep future mentions as plain text until created. Practice, atomic notes and cheatsheets live in sibling `Practice Sets/`, `Atomic Notes/`, and `Cheatsheets/` directories; compare outputs live in `comparison/`.

## Contracts

Math: [math_gates.md](math_gates.md). Deep-study planning and module composition: [adaptive-engine.md](../references/workflows/notes-creation/adaptive-engine.md). Command routing: [router.md](../router.md). Reflection implementation: [footer_widgets.md](footer_widgets.md). Machine checks implement schema, syntax and links; authors remain responsible for source fidelity and reasoning.
