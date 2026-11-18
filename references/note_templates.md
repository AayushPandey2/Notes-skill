# Selected note contracts

Resolve the request before research using [routing.md](routing.md) and the vault's
[pre-generation gate](pre_gen_gate.md). [routes.json](routes.json) is the single
built-in registry: identifier, template path, ordered headings and evidence profile.
Load only the chosen template and [authoring module](modules/authoring.md), plus
[math](modules/math.md) for levels 1/2 and [verification](modules/verification.md)
when implementation or reproducible checks matter. `note_contracts.resources_for`
returns this resource list without reading every template body.

## Metadata and drafts

Preserve `id`, `title`, `aliases`, `base_domain`, `master_topic`, `topic`, `tags`,
`depends_on` and `next_topic` conventions, including existing numbering. Add
canonical/acronym aliases. Reuse exact discovered tags. Keep existing `type`, `area`,
`created`, `mastery` and `revisited_date` fields when the vault uses them.
The built-in scaffolder emits `note_type` (registry identifier), `math_level`,
and a draft marker; these select static validation without changing user metadata.
Alternatively a per-file manifest `notes` mapping selects routes without those keys.
Never save a draft as a complete lesson: populate all sections and remove the marker.
Custom templates are materialized by the agent; never execute Templater code unattended.

`scaffold_note.py` retains all identity, output, syllabus and overwrite arguments.
Its default is `deepstudy-general`, math level 0. Pass `--template <registry-id>` and
`--math-level 0|1|2` after routing. `--template legacy-deep` explicitly selects the
[old contract](legacy_deep_template.md); the legacy Python renderer remains available.
Existing unmarked seven-section notes and explicitly selected old Cheat-Sheet/Comparison
contracts keep their validators. Do not migrate user-authored notes automatically.

## Deep-study content mapping

Both deep routes have eleven exact headings in registry order. Old synthesis and
context map to the question and Overview; mechanism to How it works and Intuition;
formal theory/proof to Details; executable checks to Experiment; transfer Q&A to
What I learned; traps to Limitations; sources and bridge to Connection. Preserve
`**Confusion** ::` in Open Confusion and the Atomize workflow. At math level 0 omit
math modules, while retaining interfaces, invariants, traces and substantive code.
The optional Key equations callout belongs after definitions in Details.
Use 1-3 purposeful stacks from routing.md, sharing one test contract. General notes
may be mathematical; Coding notes may be math-free. Non-code subjects need evidence
or worked reasoning rather than compulsory implementations.

## Deterministic compact-word measurement

`note_contracts.rendered_word_count` excludes YAML, HTML comments, fence markers,
reference definitions, URLs and Markdown punctuation. It retains headings, table
cells, link labels, callout titles, code contents and math tokens. Split on whitespace
after removing syntax; count tokens containing a Unicode word character. Inline
code with spaces counts each word. Wiki links count their label, or target when
unlabelled. This is a reproducible approximation, not a rendered page-size guarantee.
Atomic: fewer than 150 words. Cheat-Sheet: at most 350, ordinary bullets at most 20.
An explicit expanded-sheet request is recorded in the per-file manifest.

## Mixed manifest extension (backward compatible)

Keep the existing `operation_id`, `outputs`, template provenance/hash and
`pre_generation_tags`. Add `notes: {"topic/01-note.md": {"template":
"deepstudy-coding", "math_level": 0}}` for mixed output. Per-file
`template_type: custom` wins over built-in route selection; the existing top-level
custom template hash check remains mandatory. Route/depth fields belong in the
manifest when the vault schema should remain unchanged.
