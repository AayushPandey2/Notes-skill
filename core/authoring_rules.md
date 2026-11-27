# Shared Authoring Rules

## Purpose

Canonical specification for note frontmatter profiles, Obsidian Markdown/math rendering, source evidence hygiene, prose cohesion, and vault path/link integrity across every Scriptorium output.

## Activation Trigger

Apply to newly authored notes and revised passages. Follow the [direct-authoring pipeline](runtime_pipeline.md) and the [root authoring rule](../SKILL.md#scriptorium). Keep non-executed examples in Markdown when they serve the lesson.

## Metadata

Use the [properties policy](../docs/properties/properties-policy.md) for frontmatter, naming and update preservation. Use the [tag taxonomy](../docs/properties/tag-taxonomy.md) for new managed tags.

## Rendering

- **Adaptive Opening, Hierarchy & Three-Layer Disclosure:** Open substantive notes with plain-language intuition and a concrete scenario *before* formal definitions, followed by concise **separated** orientation (`**Difficulty:**`, `**Prerequisites:**` only alongside local teaching, never repeating YAML `difficulty`), observable `## Learning objectives`, and a clickable **Table of Contents** (`- [[#1. Heading|Label]]`; short single notes, narrow problem sets, and compact `M3`/`atomic-card`/`M6` omit TOC/objectives when unhelpful). Structure notes via **Three-Layer Progressive Disclosure** ([math_gates.md](math_gates.md)) using pure Obsidian syntax without Dataview, Templater, custom JS/CSS, or color-only cues:
  - *Layer 1 (Visible main path):* motivation, essential prerequisites, core definitions, mechanisms, figures, governing equations/milestones, central worked examples, interpretations, assumptions, and limits—self-contained with collapsed blocks closed.
  - *Layer 2 (Collapsed `-` depth):* extended derivations, formal proofs, optional prerequisite refreshers, alternate intuition, extra examples, code walkthroughs, and failure analyses.
  - *Layer 3 (Active learning):* visible `[!question]` checkpoints, practice problems, collapsed `[!hint]-` hints and `[!success]-` answers/solutions, and transfer tasks.
  Adapt presentation by role (**Theory**: reading continuity; **Lab**: reproducibility, traces, failure diagnosis; **Mastery**: rapid retrieval/practice), using student-friendly `H1–H4` headings (no `5.2.1` nesting, bold pseudo-headings, or `01 - ` prefixes on standalone notes), `---` only at major breaks, and `\boxed{...}` strictly for final formulas/numeric results.
- **Unified Native Obsidian Callouts & Visual Typography:** Use native Obsidian syntax (`+` expanded, `-` collapsed, quoting every interior line including blank lines with `>`, preserving valid user callouts on revision):

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

  - **Callout Balance & Titles:** Keep connected prose dominant (do not box every paragraph or nest multi-level theory folds; nest `[!hint]-`/`[!success]-` cleanly inside `[!question]`). Give every callout a specific purpose-driven title (never generic *"Important information"*, *"Deep dive"*, *"Additional knowledge"*, or repetitive *"Understand this formula step by step"*). Never emit placeholder image paths without an inspected asset.
  - **Semantic Typography, Tables & Lists:** Bold terms only at first definition; italicize lightly; avoid decorative emojis; define key symbols locally on first use; format math variables/terms in LaTeX (`$x_i$`, `$\mathrm{TP}$`), reserving backticks for code identifiers, CLI commands, parameters, paths, and literal values. Use tables (`3–5` focused columns, right-aligned numbers, `\|` for literal pipes per [math_gates.md](math_gates.md)) strictly for tabular data (never formula-stuffed prose replacements), and use lists for parallel/sequential items with causal explanations rather than bare bullet dumps.
- **Active-Learning Placement:** Without imposing fixed quotas or boxing every heading, place `> [!question]` checkpoints (with collapsed `> [!hint]-` / `> [!success]-` answers) across early, middle, and late substantive units after teaching the prerequisites needed to predict, diagnose, or transfer—avoiding trivial definition restatements.
- **Math, Visuals & Proximity:** Follow [math_gates.md](math_gates.md) (no `==highlight==`, `\color{...}`, raw HTML spans, or equation code fences) and web-only [representations.md](../docs/procedures/authoring/representations.md) (never generate images/plots/SVG/Mermaid/ASCII; distribute verified local web images across relevant sections when permitted), keeping lead-in, image, caption/attribution, and interpretation uninterrupted.
- **Cognitive Whitespace & Opening Grounding:** Ground substantive openings in a concrete scenario or motivating problem (never `"Imagine that"` clichés); break back-to-back abstractions with concrete examples, visuals, interpretations, checkpoints, or natural teaching pauses (never `"Pause here"` boilerplate); keep single blank lines around blocks without HTML spacing hacks; strip scaffold comments and placeholder rows. Maintain one coherent teaching move per paragraph without 1-sentence fragmentation or repeated definitions.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed execution. Never fabricate execution outputs or runtime parity.
- For comprehensive independent notes (`M1` and non-strict notes drawing on canonical references), include a concise **References** section citing primary authoritative sources (foundational papers, version-qualified official documentation, or standard textbooks) alongside verified deep links where available.

## Cohesion

- Keep internal planning/evaluation machinery invisible (**anti-template leakage**) and write calm, textbook prose per [teaching_core.md](teaching_core.md):
  - **Precision over drama:** Never dramatize trade-offs as *"fatal flaw"*, *"catastrophic failure"*, or *"revolutionary breakthrough"*; state precise conditions (*sensitive to noise, unstable under..., requires...*).
  - **No AI clichés or filler:** Omit generic hooks, repetitive rhetorical questions, scripted filler (*"We now..."*, *"Let us..."*, *"In simple words"*, `"Inspect Figure..."`), mechanical recaps, compulsory analogies, or *"Imagine that"* openers.
  - **Textbook headings & anti-jargon:** Ban robotic process headings (*"Computational Purpose"*, *"Taxonomic Lineage"*, *"Parameter Synthesis"*, *"Operational Mechanism Reconstruction"*, *"Epistemic Boundaries"*, *"Source-Preserving Educational Reconstruction"*, *"Comparative Realization Analysis"*) and internal jargon (*"fixture"*, *"canonical example"*, *"artifact"*, *"acceptance criteria"*, *"verification gate"*, *"epistemic boundary"*, *"mechanism reconstruction"*, *"conceptual inflection point"*, *"representation correspondence"*, *"operational phase"*, *"intellectual dependency"*, *"original audit"*) unless genuinely part of the subject taught.
- Follow filename, staging, and link conventions in [properties-policy.md](../docs/properties/properties-policy.md) and [revision-and-linking.md](../docs/procedures/updating/revision-and-linking.md), emitting `[[Wikilinks]]` only to verified existing/published notes (plain text or `nexttopics` for unbuilt targets).

## Validation

Review every output manually against [verification-checklist.md](../docs/procedures/review/verification-checklist.md) for YAML validity, delimiters, callout quoting, reasoning-unit coverage, local image embeds, and internal wikilinks. Label this honestly as manual review rather than an automated test.
