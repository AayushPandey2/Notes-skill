# Shared Authoring Rules

## Purpose

Canonical specification for note frontmatter profiles, Obsidian Markdown/math rendering, source evidence hygiene, prose cohesion, and vault path/link integrity across every Scriptorium output.

## Activation Trigger

Always active across `/scribe-notes` and any vault write. Follow [the direct-authoring pipeline](runtime_pipeline.md): author Markdown directly; never generate or execute scripts or educational code during normal note authoring (trusted standalone verification scripts under `evaluations/` are development-only tooling separate from the authoring runtime).

## Metadata

Every note begins on line 1 with valid YAML (`---` ... `---`) matching its profile ([properties-policy.md](../docs/properties/properties-policy.md)):
- **New comprehensive `M1` collections** ([composition-contract.md](../docs/procedures/authoring/composition-contract.md)): strictly the 5 ordered keys `id`, `aliases`, `topic`, `tags`, `nexttopics` (nonempty strings for `id`/`topic`, lists for the rest; aliases include title; `domain/`/`subject/`/`topic/` tags; resolved forward wikilinks in `nexttopics`; zero extra keys).
- **Single notes, `M2`–`M7`, optional extended metadata, and existing note updates** ([properties-policy.md](../docs/properties/properties-policy.md)): canonical Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, plus optional managed keys such as `difficulty` and `prerequisites`). Preserving existing IDs, custom properties, and user layouts always takes precedence over strict 5-key creation rules when updating existing notes.

Never inject a `deepstudy-master` tag, any `type/<note-type>` tag, or internal review/routing logs into YAML.

## Rendering

- **Adaptive Opening, Hierarchy & Accessibility:** Start substantive notes cleanly with a short, concrete problem before formal definitions, followed by concise **separated** metadata (`**Difficulty:**`, `**Prerequisites:**`), focused observable `## Learning objectives`, and a clickable **Table of Contents** (`- [[#1. Heading|Label]]`) without stuffing metadata into a large box or repeating YAML `difficulty` verbatim. (*Precedence:* short single-concept notes and compact masters `M3`, `atomic-card`, `M6` may omit objectives/TOC when they add no navigational benefit.) Align **Three-Level Progressive Disclosure** with the three mathematical reading layers ([math_gates.md](math_gates.md)):
  - *Main reading path (Layer 1 — always visible):* essential intuition, definitions, governing mechanisms, governing equations and consequential intermediate milestones, critical assumptions, key results, transitions into the next concept, and failure conditions (notes must remain educationally complete with all callouts collapsed).
  - *Expandable detail (Layer 2 — `> [!example]- Derivation: <Focus>` / `Proof: <Focus>` or `Understand this formula step by step — <Focus>` / Lab folds):* complete derivations, intermediate transformation rationales, mathematical identities, concrete calculations, alternative forms, and line-by-line code walkthroughs.
  - *Linked reference (Layer 3 — advanced extensions):* deep prerequisites, optional alternative proofs, generalized formulations, and related topics.
Shape presentation by artifact role within existing formats: **Theory** prioritizes reading continuity and progressive reasoning; **Lab** prioritizes reproducibility, concrete traces, inputs/outputs, and failure diagnosis; **Mastery** prioritizes rapid retrieval, clear problem prompts, and collapsed solutions. Use concise, student-friendly `H1–H4` headings without deep `5.2.1` nesting (never bold pseudo-headings), reserve `---` rules for major transitions, avoid relying on color alone, ensure navigation works without optional Obsidian plugins, and reserve `\boxed{...}` strictly for final governing formulas or key numeric results.
- **Semantic Callout Roles & Visual Typography:** Use distinct optional presentation callout roles without forcing five boxes per concept: `[!info]` for key isolated **Definitions**, `[!important]` for **Key insights**, `[!warning]` for **Common misconceptions**, collapsed `[!example]-` for **Derivations / Proofs** (preserving exact `[math_gates.md](math_gates.md)` rules and quoting every interior line including blank lines `>`), and visible `[!question]` with nested `> > [!success]- Reveal Answer` for **Test your understanding** checkpoints. Give formatting semantic meaning: **bold** new terms only at first meaningful definition; *italicize* sparingly for light emphasis; write variables and mathematical abbreviations in LaTeX (`$x_i$`, `$\mathrm{TP}$`—never inline code for `TP`/`FP` or ordinary categorical prose labels); reserve inline backticks strictly for code identifiers, CLI commands, parameter names, file paths, and literal program values; and target **3–5 focused columns** for ordinary study tables (right-align numeric columns, escape `\|`, never pack paragraphs + formulas + citations into one cell).
- **Math, Visuals & Publish Hygiene:** Follow [math_gates.md](math_gates.md) (no `==highlight==`, `\color{...}`, raw HTML spans, or code fences for equations) and [representations.md](../docs/procedures/authoring/representations.md) (no Mermaid/ASCII). Strip scaffold comments, placeholder rows, and `<!-- SECTION -->` markers, renumbering headings cleanly.

Keep one primary teaching move per paragraph rather than enforcing arbitrary sentence-count quotas: start a new paragraph whenever switching from definition to mechanism, comparing alternatives, or interpreting a result, and let a coherent mathematical or causal derivation run longer where logical flow requires it. Place blank lines around figures, displays, tables, and callouts.

## Evidence

- Read the supporting passage before citing; attach locators (`page`, `section`, `timestamp`) near claims. Never cite bare root-domain homepages (`[UNVERIFIED]` if no verified deep link exists).
- Separate observed source statements, author inference, expected behavior, and observed execution. Never fabricate execution outputs or runtime parity.

## Cohesion

- Write clear, engaging professor-and-textbook reference prose per [teaching_core.md](teaching_core.md): allow natural connective transitions while banning empty conversational filler (`"We now..."`, `"Let us..."`, `"Notice how..."`). Ban both robotic CS meta-headings (`"Computational Purpose"`, `"Taxonomic Lineage"`, `"Parameter Synthesis"`) and **internal engineering jargon** (`"fixture"`, `"canonical example"`, `"artifact"`, `"acceptance criteria"`, `"verification gate"`, `"epistemic boundary"`, `"mechanism reconstruction"`, `"conceptual inflection point"`, `"representation correspondence"`, `"operational phase"`, `"intellectual dependency"`, `"original audit"`) from student-facing prose unless genuinely part of the topic being taught.
- Follow filename and path-staging conventions in [properties-policy.md](../docs/properties/properties-policy.md) (`01 - <Title>.md` for multi-branch collections; natural `<Topic>.md` for single bundles; plan paths first and create directories only when publishing accepted notes). Link future planned notes in `nexttopics` when referenced; otherwise keep mentions plain text.

## Validation

Review every output manually against [verification-checklist.md](../docs/procedures/review/verification-checklist.md) for YAML validity, delimiters, callout quoting, reasoning-unit coverage, local image embeds, and internal wikilinks. Label this honestly as manual review rather than an automated test.
