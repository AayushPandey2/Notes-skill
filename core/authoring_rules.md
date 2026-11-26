# Shared Authoring Rules

## Purpose

Canonical specification for note frontmatter profiles, Obsidian Markdown/math rendering, source evidence hygiene, prose cohesion, and vault path/link integrity across every Scriptorium output.

## Activation Trigger

Apply to newly authored notes and revised passages. Follow the [direct-authoring pipeline](runtime_pipeline.md) and the [root authoring rule](../SKILL.md#scriptorium). Keep non-executed examples in Markdown when they serve the lesson.

## Metadata

Use the [properties policy](../docs/properties/properties-policy.md) for frontmatter, naming and update preservation. Use the [tag taxonomy](../docs/properties/tag-taxonomy.md) for new managed tags.

## Rendering

- **Adaptive Opening, Hierarchy & Accessibility:** Start substantive notes cleanly with plain-language intuition and a concrete everyday problem/scenario *before* formal definitions, dense technical terminology, or oversized navigation blocks, followed by concise **separated** orientation (`**Difficulty:**`, `**Prerequisites:**` only as meaningful orientation alongside local foundational teaching—never repeating YAML `difficulty` verbatim and never substituting for teaching unmastered prerequisites), focused observable `## Learning objectives`, and a clickable **Table of Contents** (`- [[#1. Heading|Label]]`). (*Precedence:* short single-concept notes, short 1–3 problem sets lacking cross-problem complexity, and compact masters `M3`, `atomic-card`, `M6` may omit objectives/TOC when they add no navigational benefit.) Organize comprehensive notes cleanly across **Three-Layer Progressive Disclosure** ([math_gates.md](math_gates.md)) without hiding essential reasoning or creating dependencies on Dataview, Templater, custom JavaScript, or custom CSS:
  - *Layer 1 — Main learning path (always visible):* motivation, essential prerequisites, core definitions, mechanisms, diagrams, governing equations and consequential intermediate milestones, essential mathematical reasoning, central worked examples, interpretation, governing assumptions, and consequential limitations—the main learning path must never depend on opening every optional block.
  - *Layer 2 — Expandable depth (collapsed `-` callouts):* extended derivations (`> [!example]- Derivation: <Focus>`), formal proofs (`> [!example]- Proof: <Focus>`), optional prerequisite refreshers (`> [!note]- Prerequisite: <Focus>`), alternative intuition (`> [!tip]-`), additional examples, advanced connections, line-by-line code walkthroughs, and detailed failure analyses (`> [!failure]-`).
  - *Layer 3 — Active learning:* visible thinking checkpoints (`> [!question]`), practice questions, concealed hints (`> [!hint]-`), concealed answers/solutions (`> [!success]-`), and independent transfer exercises.
  Shape presentation by artifact role within existing formats: **Theory** prioritizes reading continuity and progressive reasoning; **Lab** prioritizes reproducibility, concrete traces, inputs/outputs, and failure diagnosis; **Mastery** prioritizes rapid retrieval, clear problem prompts, and collapsed solutions. Use clear, student-friendly `H1–H4` headings without deep `5.2.1` nesting (never bold pseudo-headings; choose the clearest form—question or noun phrase—without forcing every heading into one pattern, and avoid collection prefixes like `01 - ` on standalone notes), reserve `---` horizontal rules only for major independent transitions, avoid relying on color alone, ensure navigation works without optional Obsidian plugins, and reserve `\boxed{...}` strictly for final governing formulas or key numeric results.
- **Unified Native Obsidian Callout Vocabulary & Visual Typography:** Standardize callouts across every format, preset, and procedure using native Obsidian syntax (`+` starts expanded, `-` starts collapsed, quoting every interior line including blank lines with `>`, without custom CSS or forcing callouts where ordinary prose works better; **preserve valid existing user callouts during revision**):

  | Callout | Intended purpose | Default state |
  |---|---|---|
  | `[!info]` | Important definitions (also attribution/metadata when relevant) | Visible |
  | `[!important]` | Fundamental insights and governing invariants | Visible |
  | `[!warning]` | Critical misconceptions, assumptions, and limitations | Visible |
  | `[!example]+` | Central worked examples | Expanded |
  | `[!example]-` | Additional worked examples or walkthroughs | Collapsed |
  | `[!example]- Derivation: ...` | Extended step-by-step derivations | Collapsed |
  | `[!example]- Proof: ...` | Supporting formal proofs | Collapsed |
  | `[!note]- Prerequisite: ...` | Optional prerequisite refreshers | Collapsed |
  | `[!note]- Advanced connection: ...` | Advanced supporting theory | Collapsed |
  | `[!tip]-` | Additional intuition or useful techniques | Collapsed |
  | `[!question]` | Active-learning checkpoints | Visible |
  | `[!hint]-` | Optional assistance inside checkpoints/exercises | Collapsed |
  | `[!success]-` | Answers and solutions (standalone or `> > [!success]-`) | Collapsed |
  | `[!failure]-` | Detailed failure analysis | Collapsed |
  | `[!abstract]-` | Optional revision material | Collapsed |

  **Prevent both callout underutilization and callout overload:** Do not place every definition or paragraph in colored boxes (connected prose stays dominant), yet do not dump lengthy extended proofs, supporting prerequisite refreshers, or extra walkthroughs all into the visible narrative merely because callouts are optional. Nest callouts primarily for active-learning checkpoints (`[!question]` with `[!hint]-` / `[!success]-`)—never stack deeply nested theory boxes or cram unrelated topics into one fold. Give every callout a **specific title communicating its educational purpose** (prefer `Derivation: Euclidean distance`, `Prerequisite: Reading summation notation`, `Why scaling changes neighbor selection`, `Failure case: Conflicting duplicate examples`); **never use generic titles** such as *"Important information"*, *"Deep dive"*, *"Additional knowledge"*, *"Understanding everything"*, *"More explanation"*, or monotonous repeated *"Understand this formula step by step"*. Never emit literal placeholder asset paths (e.g., `assets/verified-tree-split.png`) without an inspected corresponding asset. Give formatting semantic meaning: **bold** new terms only at first meaningful definition (never whole paragraphs); *italicize* sparingly for light emphasis and captions; avoid decorative emojis and unnecessary markers in academic notes; introduce every important symbol locally at first use rather than relying only on a trailing notation reference; write variables and mathematical abbreviations in LaTeX (`$x_i$`, `$\mathrm{TP}$`—never inline code for `TP`/`FP` or ordinary categorical prose labels); reserve inline backticks strictly for code identifiers, CLI commands, parameter names, file paths, and literal program values; use **tables strictly for genuinely tabular data** (3–5 focused columns, right-aligned numeric columns, escaping literal pipes as `\|` while using [math_gates.md](math_gates.md) delimiters—never replacing prose theory with wide formula-stuffed cells); and use **lists strictly for genuinely parallel or sequential items**, supported by causal explanations rather than turning central theory into unexplained bullet summaries.
- **Math, Visuals & Whitespace Hygiene:** Follow [math_gates.md](math_gates.md) (no `==highlight==`, `\color{...}`, raw HTML spans, or code fences for equations) and [representations.md](../docs/procedures/authoring/representations.md) (no Mermaid/ASCII). Author notes as balanced, thoughtfully authored educational chapters (prose, headings, math, visuals, examples, callouts, active-learning checks) tailored to the subject rather than one uniform template. Create **cognitive whitespace**—avoid introducing several unfamiliar abstractions back-to-back without letting the learner ground each one via a concrete example, visual, interpretation, prediction check, refresher, or paragraph break—and apply natural *visual, reflective, predictive, computational, consolidation, and transition* learning pauses (never write `"Pause here"` after every heading). Keep blank lines around display equations, images, tables, and callouts without repeated empty lines or HTML spacing hacks, and keep each image's intro, caption, and interpretation visually connected (never breaking them with an unrelated heading). Strip scaffold comments, placeholder rows, and `<!-- SECTION -->` markers, renumbering headings cleanly.

Keep one coherent teaching purpose per paragraph (definition, mechanism, justification, example, interpretation, assumption, or limitation) without arbitrary sentence-count quotas, separating walls of text while avoiding 1-sentence fragmentation, excessive parentheses, dense jargon chains, or repeated definitions.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed execution. Never fabricate execution outputs or runtime parity.
- For comprehensive independent notes (`M1` and non-strict notes drawing on canonical references), include a concise **References** section citing primary authoritative sources (foundational papers, version-qualified official documentation, or standard textbooks) alongside verified deep links where available.

## Cohesion

- Keep internal planning frameworks, maturity levels, teaching moves, evaluation gates, visual inventories, coverage audits, and analytical operations completely invisible (**anti-template leakage**): the learner must see a polished university textbook, never the authoring architecture used to produce it. Write clear, calm, approachable professor-and-textbook prose per [teaching_core.md](teaching_core.md), avoiding research-paper shorthand, API docs tone, or chatbot patterns:
  - **Ban unnecessarily dramatic language:** never dramatize ordinary properties or trade-offs as *"fatal flaw"*, *"catastrophic failure"*, or *"revolutionary breakthrough"*; use calm, precise terms (*important limitation, sensitive to noise, computationally expensive, unreliable under these conditions, requires additional assumptions, may yield unstable predictions*).
  - **Eliminate AI writing signatures:** omit generic motivational hooks, repetitive rhetorical questions, artificial filler (*"We now..."*, *"Let us understand..."*), repeated *"Imagine that"* openings, repeated *"In simple words"* labels, mechanical section-ending recaps, compulsory analogies, and generic key-takeaway boxes (without banning ordinary natural transitions where they clarify conceptual flow).
  - **Textbook headings & anti-jargon leakage:** use natural descriptive textbook headings without parenthetical meta-labels; ban robotic internal-process headings (`"Computational Purpose"`, `"Taxonomic Lineage"`, `"Parameter Synthesis"`, `"Operational Mechanism Reconstruction"`, `"Epistemic Boundaries"`, `"Source-Preserving Educational Reconstruction"`, `"Comparative Realization Analysis"`) and internal engineering jargon (`"fixture"`, `"canonical example"`, `"artifact"`, `"acceptance criteria"`, `"verification gate"`, `"epistemic boundary"`, `"mechanism reconstruction"`, `"conceptual inflection point"`, `"representation correspondence"`, `"operational phase"`, `"intellectual dependency"`, `"original audit"`) from student-facing prose unless genuinely part of the topic being taught.
- Follow filename, path-staging, and four-case link conventions in [properties-policy.md](../docs/properties/properties-policy.md) and [revision-and-linking.md](../docs/procedures/updating/revision-and-linking.md) (`01 - <Title>.md` for multi-branch collections; natural `<Topic>.md` for single bundles; create directories only when publishing accepted notes). Distinguish verified existing notes and published companions (`[[Wikilinks]]`) from unbuilt future topics in standalone outputs (plain text or `nexttopics`, reserving unresolved placeholder links only for explicit user requests).

## Validation

Review every output manually against [verification-checklist.md](../docs/procedures/review/verification-checklist.md) for YAML validity, delimiters, callout quoting, reasoning-unit coverage, local image embeds, and internal wikilinks. Label this honestly as manual review rather than an automated test.
