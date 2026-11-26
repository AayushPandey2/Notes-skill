# Shared Authoring Rules

## Purpose

Canonical specification for note frontmatter profiles, Obsidian Markdown/math rendering, source evidence hygiene, prose cohesion, and vault path/link integrity across every Scriptorium output.

## Activation Trigger

Apply to newly authored notes and revised passages. Follow the [direct-authoring pipeline](runtime_pipeline.md) and the [root authoring rule](../SKILL.md#scriptorium). Keep non-executed examples in Markdown when they serve the lesson.

## Metadata

Use the [properties policy](../docs/properties/properties-policy.md) for frontmatter, naming and update preservation. Use the [tag taxonomy](../docs/properties/tag-taxonomy.md) for new managed tags.

## Rendering

- **Adaptive Opening, Hierarchy & Accessibility:** Start substantive notes cleanly with a short, concrete problem before formal definitions, followed by concise **separated** orientation (`**Difficulty:**`, `**Prerequisites:**` only as meaningful orientation or local bridge—never verbatim repetition of YAML `difficulty` or `prerequisites`), focused observable `## Learning objectives`, and a clickable **Table of Contents** (`- [[#1. Heading|Label]]`) without stuffing metadata into a large box. (*Precedence:* short single-concept notes, short 1–3 problem sets lacking cross-problem complexity, and compact masters `M3`, `atomic-card`, `M6` may omit objectives/TOC when they add no navigational benefit.) Align **Three-Level Progressive Disclosure** with the three mathematical reading layers ([math_gates.md](math_gates.md)):
  - *Main reading path (Layer 1 — always visible):* essential intuition, definitions, governing mechanisms, governing equations and consequential intermediate milestones, critical assumptions, key results, transitions into the next concept, and failure conditions (notes must remain educationally complete with all callouts collapsed).
  - *Expandable detail (Layer 2 — collapsed `> [!example]- Derivation: <Focus>` / `Proof: <Focus>` or `> [!example]- Understand this implementation: <Focus>` / Lab folds):* complete derivations, intermediate transformation rationales, mathematical identities, concrete calculations, alternative forms, and line-by-line code walkthroughs.
  - *Linked reference (Layer 3 — advanced extensions):* deep prerequisites, optional alternative proofs, generalized formulations, and related topics.
Shape presentation by artifact role within existing formats: **Theory** prioritizes reading continuity and progressive reasoning; **Lab** prioritizes reproducibility, concrete traces, inputs/outputs, and failure diagnosis; **Mastery** prioritizes rapid retrieval, clear problem prompts, and collapsed solutions. Use concise, student-friendly `H1–H4` headings without deep `5.2.1` nesting (never bold pseudo-headings), reserve `---` rules for major transitions, avoid relying on color alone, ensure navigation works without optional Obsidian plugins, and reserve `\boxed{...}` strictly for final governing formulas or key numeric results.
- **Unified Callout Vocabulary & Visual Typography:** Standardize callouts across every format, preset, and procedure using this single Obsidian vocabulary without forcing extra boxes where ordinary prose works better (**always preserve valid existing user callouts when updating existing notes**):
  - *Visible callouts:* `[!info]` (metadata, context, attribution, isolated **Definitions**), `[!important]` (**Key insights**, governing rules, core equations/invariants), `[!warning]` (**Common misconceptions**, exam/interview traps, caveats, safety bounds), `[!example]` (inline worked example), `[!question]` (**Test your understanding** prompts or exercises).
  - *Collapsed callouts (`-` suffix, quoting every interior line including blank lines with `>`):* `[!example]-` (**Derivations / Proofs** per [math_gates.md](math_gates.md) and **Implementation walkthroughs**), `[!hint]-` (progressive hints), `[!success]-` (answer reveals, worked solutions, marking rubrics, flashcard backs—including nested `> > [!success]- Reveal Answer` under `[!question]`).
  Give formatting semantic meaning: **bold** new terms only at first meaningful definition; *italicize* sparingly for light emphasis; write variables and mathematical abbreviations in LaTeX (`$x_i$`, `$\mathrm{TP}$`—never inline code for `TP`/`FP` or ordinary categorical prose labels); reserve inline backticks strictly for code identifiers, CLI commands, parameter names, file paths, and literal program values; and target **3–5 focused columns** for ordinary study tables (right-align numeric columns, escape literal text pipes as `\|` while following [math_gates.md](math_gates.md) for mathematical delimiters inside tables, and never pack paragraphs, long derivations, or multi-row matrices into table cells).
- **Math, Visuals & Publish Hygiene:** Follow [math_gates.md](math_gates.md) (no `==highlight==`, `\color{...}`, raw HTML spans, or code fences for equations) and [representations.md](../docs/procedures/authoring/representations.md) (no Mermaid/ASCII). Strip scaffold comments, placeholder rows, and `<!-- SECTION -->` markers, renumbering headings cleanly.

Keep one primary teaching move per paragraph rather than enforcing arbitrary sentence-count quotas: start a new paragraph whenever switching from definition to mechanism, comparing alternatives, or interpreting a result, and let a coherent mathematical or causal derivation run longer where logical flow requires it. Place blank lines around figures, displays, tables, and callouts.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed execution. Never fabricate execution outputs or runtime parity.

## Cohesion

- Write clear, engaging professor-and-textbook reference prose per [teaching_core.md](teaching_core.md): allow natural connective transitions while banning empty conversational filler (`"We now..."`, `"Let us..."`, `"Notice how..."`). Ban both robotic CS meta-headings (`"Computational Purpose"`, `"Taxonomic Lineage"`, `"Parameter Synthesis"`) and **internal engineering jargon** (`"fixture"`, `"canonical example"`, `"artifact"`, `"acceptance criteria"`, `"verification gate"`, `"epistemic boundary"`, `"mechanism reconstruction"`, `"conceptual inflection point"`, `"representation correspondence"`, `"operational phase"`, `"intellectual dependency"`, `"original audit"`) from student-facing prose unless genuinely part of the topic being taught.
- Follow filename, path-staging, and four-case link conventions in [properties-policy.md](../docs/properties/properties-policy.md) and [revision-and-linking.md](../docs/procedures/updating/revision-and-linking.md) (`01 - <Title>.md` for multi-branch collections; natural `<Topic>.md` for single bundles; create directories only when publishing accepted notes). Distinguish verified existing notes and published companions (`[[Wikilinks]]`) from unbuilt future topics in standalone outputs (plain text or `nexttopics`, reserving unresolved placeholder links only for explicit user requests).

## Validation

Review every output manually against [verification-checklist.md](../docs/procedures/review/verification-checklist.md) for YAML validity, delimiters, callout quoting, reasoning-unit coverage, local image embeds, and internal wikilinks. Label this honestly as manual review rather than an automated test.
