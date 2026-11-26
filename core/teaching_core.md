# Shared Canonical Teaching Core

## Purpose

Establish one domain-independent theory-authoring architecture across substantive Scriptorium outputs (`M1`, `M2`, `M4`, `M5`, `M7`, and video notes) so explanations develop understanding **gradually** rather than compressing dense technical material into a polished outline. Pair this flow with [theory_quality_contract.md](theory_quality_contract.md) for progressive abstraction, multi-perspective explanations, forward/reverse reasoning, ideal-to-real model progression, claim classification, and question-specific reasoning patterns. Compact `M3` cheat sheets and question-only `M6` assessments follow their own density contracts while preserving symbol accuracy and assumptions.

## Diagnosing Teaching Gaps & Prerequisite Policy

Before drafting each major concept, diagnose the gap: identify (1) what the reader currently understands, (2) what the next paragraph assumes, and (3) the missing explanation connecting them. Add the missing reasoning—never another generic introduction or more jargon.

Apply the **two-dimension prerequisite policy** across all substantive notes (separating prerequisite importance from the learner's demonstrated knowledge status so an essential concept already mastered is not redundantly retaught):

| Prerequisite Importance | Treatment When Learner Status Is Unknown / Uncertain | Treatment When Learner Status Is Self-Reported | Treatment When Learner Status Is Demonstrated |
|---|---|---|---|
| **Essential** | Explain locally before first dependent use (a link never substitutes) | Provide concise bridge and quick verification cue where consequential | Concise 1-line anchor or omit repetitive derivation |
| **Supporting** | Concise bridge or optional collapsed refresher | Brief bridge if needed for the immediate step | Brief reference only |
| **Contextual** | Link or mention briefly only when useful | Link briefly if helpful; do not interrupt core flow | Omit or link only if requested |

Learner knowledge status levels ([learner-model.md](../docs/procedures/authoring/learner-model.md)): `Demonstrated` · `Self-reported` · `Uncertain` · `Not established`.

- **One conceptual burden at a time:** Start with a concrete problem or phenomenon before introducing terminology. Never stuff advanced claims or dense "Core Characteristics" boxes into the opening (move dense characteristics summaries to revision material).
- **Clean metadata & hierarchy:** Do not repeat YAML metadata fields (`difficulty`) as visible body dumps; open with a concise purpose, learning path, and clickable TOC. Avoid deep technical-manual heading nesting (`5 → 5.2 → 5.2.1`) and avoid parallel formula or method catalogues before completing one concrete worked example.
- **Definition teaching structure:** Selectively fulfill five responsibilities in natural prose (not five compulsory headings): establish the need → state a short, accurate definition → translate it into ordinary language → demonstrate with one concrete example beside it → establish the nearest boundary. Bold only the term being defined; use short non-collapsed definition callouts sparingly so the note reads as connected explanation, not a stack of boxes. Separate definition, consequence, assumption, and optional advanced property rather than combining them into one sentence.
- **One hand-worked operation before comparison tables:** Always trace one candidate calculation or concrete case by hand first before presenting a comparison table; keep every table focused on **one question** (never cramming unrelated columns into one wide table).

## Visual Identity, Headings & Reading Path

- **Separated opening metadata & clickable TOC:** Follow [authoring_rules.md](authoring_rules.md) for separated `Difficulty`, `Prerequisites`, and `Learning objectives` blocks and clickable Obsidian TOCs (`- [[#1. Heading|Short Label]]`).
- **Meaningful headings & adaptive paragraphing:** Use question-driven headings or concise descriptive headings matched to the subject (developed through explanation, example, and interpretation—never 1-sentence micro-sections or bold pseudo-headings). Prefer short single-idea paragraphs (1–3 sentences) while allowing slightly longer coherent derivations when splitting would break a logical chain.
- **No decorative highlighting & purposeful callouts:** Follow [authoring_rules.md](authoring_rules.md) and [math_gates.md](math_gates.md) (no `==highlight==`, semantic spans, or `\color{...}`). Keep the central argument visible in prose and milestone equations, with the assumptions and prerequisite relationships established before dependent displays, and reserve collapsed blocks for detailed formula breakdowns, extended derivations, prerequisite refreshers, additional calculations, and checkpoint answers (`> [!question]` visible with nested `> > [!success]- Reveal Answer`).

## Tone, Precision & Accuracy Discipline

Write calm, direct reference prose free of scripted filler (`"We now..."`, `"Let us..."`, `"Notice how..."`, `"Inspect Figure..."`) and unedited self-correction transcripts (`"Wait—check the sign carefully!"`). Flag and qualify strong claims, clearly separating helpful simplifications from unconditional truths.

## Progressive Explanation & Consolidated Scope

1. **Motivate every representation & step-by-step objective:** For any transformation or composite rule, explain what it expresses, why transform, what changes, and what stays invariant before summarizing in a table; build multi-step formalisms through guiding questions on a tiny concrete example before general notation.
2. **Separate phases & declare toy simplifications:** Explicitly separate distinct operational phases (e.g., construction/fitting vs. inference/evaluation; compile time vs. runtime; equilibrium vs. kinetics) and declare miniature-example simplifications honestly.
3. **Separate theoretical results, implementation defaults & empirical observations:** Distinguish idealized or asymptotic theory from finite/real-world behavior, foundational definitions from library/tool defaults, and conditional trade-offs from blanket `"always"` claims. In worked traces, explain *why* each starting value, sign, and state transition occurs.
4. **Decision-framed parameters & aligned checkpoints:** Teach tunable parameters or design knobs by what they control, directional effects, governing trade-offs, and evaluation criteria. Consolidate core mechanics before extensions, and align visible `> [!question] Concept Checkpoint` blocks with the stated learning objectives.
5. **Adaptive Closing & Companion Handoff:** End with a concise **Mental Model** when it adds reconstruction value (beyond repeating headings), a trailing **Notation Reference** when quantitative notation warrants one (essential symbols defined locally first), rationale-rich next-topic recommendations (explaining *why* the next topic matters), and reciprocal links to any companions emitted under `artifact_policy` in [master-registry.yaml](../docs/dispatch/master-registry.yaml).
