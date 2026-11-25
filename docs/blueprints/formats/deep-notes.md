# M1 — Deep Learning Notes

- **Master ID:** `M1` (`deep_notes` / compatibility route `deepstudy-master`)
- **Primary intent:** `comprehensive_learning` — deliver a complete, zero-prerequisite, self-contained explanation from first intuition through formal derivations, multi-step numerical traces, evaluation, common pitfalls, and independent practice.
- **Activation signals:** `"teach me from scratch"`, `"explain deeply"`, `"comprehensive notes"`, `"from fundamentals to advanced"`, or bare `/scribe-notes <topic>` without an explicit alternate product format.
- **Non-activation:** Do not select `M1` when the user primarily requests a compact `<350`-word cheat sheet (`M3`), pure solved problem set (`M4`), pure algorithm build guide (`M5`), pure quiz/flashcards (`M6`), or standalone comparison/revision pack (`M7`).
- **Load as needed:** [teaching rules](../../../core/teaching_core.md), [math guidance](../../../core/math_gates.md), [visual rules](../../procedures/authoring/representations.md), [adaptive planning](../../procedures/authoring/adaptive-engine.md), [research](../../procedures/sourcing/research-engine.md), [source fidelity](../../procedures/sourcing/source-fidelity.md), and [authoring rules](../../../core/authoring_rules.md).
- **Output profile:** Comprehensive collections use the five-key YAML profile in [properties policy](../../properties/properties-policy.md); single or existing notes use Obsidian properties without overwriting user-managed fields.

## 1. Opening Roadmap (Difficulty, Prerequisites, Objectives & TOC)

Open cleanly with line-1 YAML, H1 title, and three **blank-line-separated** metadata blocks (`Difficulty`, `Prerequisites` — noting essential concepts are taught locally — and `Learning objectives`), followed by a compact **clickable Obsidian Table of Contents** (`- [[#1. Heading|Short Label]]`). Apply the 3-tier prerequisite rule in [teaching_core.md](../../../core/teaching_core.md): never use a link to replace an essential local foundation.

## 2. Progressive Self-Contained Flow (See It → Understand It → Derive It → Calculate It → Apply It)

Load and follow the matching knowledge-type subtemplate (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, or `historical`). Use short, subject-first, multi-level numbered `H1–H4` headings (`## 5.` → `### 5.1` → `#### 5.1.1`), **short single-idea paragraphs (1–3 sentences)**, blank lines between complex list items, purposeful callouts (`[!info]`, `[!important]`, `[!example]`, `[!warning]`), right-aligned numerical tables with semantic outcome labels and marked selected rows, and controlled bolding—with **no `==highlight==`, semantic highlight spans, or `\color{...}` in formulas**. Reserve `---` horizontal rules for major thematic transitions only. Realize the [teaching core](../../../core/teaching_core.md#conceptual-flow--worked-example-completeness) in natural domain order:

1. **Introduction & Core Characteristics:** Explain what the concept does, where it applies, and separate its defining characteristics into distinct short blocks without dumping advanced jargon upfront.
2. **Prerequisites & Base Models:** Teach every essential building block locally before combining them, and cleanly separate **Fundamentals → Practical Understanding → Advanced Mechanisms**.
3. **Visual Running Dataset & Early Multi-Stage Example:** Introduce one tiny concrete dataset early, **visualize it**, and trace a complete multi-stage example (`1. Compute → 2. Sort/Select → 3. Aggregate → 4. Result`) *before* heavy formalism, introducing symbols **progressively** as they enter (reserving the full **Notation Reference** for the end).
4. **Limitations of Simpler Baselines:** Show where a simpler baseline is limited on concrete numbers (calm, qualified language) alongside a contrast visual.
5. **Spacious Mathematics & Individual Metric Subsections:** Give each core metric/formula its own numbered subsection, display equation, numerical example, and usage condition. Split composite objectives into separate blocks, use multiline `aligned` derivations, break down multi-operator equations cleanly in prose/tables without `\color{...}`, apply `\boxed{...}` consistently across all primary algorithm formulas, and explain mathematical **meaning visibly** without `> [!note]- 📐 Understand this formula` folds or `"Read aloud"` filler.
6. **Complete Algorithmic & Objective Coverage:** Carry the **exact same running dataset** through complete multi-stage calculations fulfilling **every** declared learning objective (e.g., both classification and regression when both are promised), compare candidate choices when teaching selection algorithms, and develop classification mechanics explicitly.
7. **Evaluation, Assumptions & Visible Checkpoints:** Define metrics around the shared fixture, highlight leakage/mistake warnings in `[!warning]` callouts, state *"What It Does NOT Require"* boundaries, and place visible `> [!question] Concept Checkpoint` blocks (with nested collapsed `> > [!success]- Reveal Answer`) after major sections.

## 3. Closing Mental Model, Notation Reference & Companion Handoff

End deep notes cleanly with a crisp **5–7 step Final Numbered Mental Model**, the trailing **Notation Reference** (complete Symbol Dictionary), and reciprocal links to `<note stem> - Experimental Lab.md` ([experimental-lab.md](../../procedures/authoring/experimental-lab.md)) and `<note stem> - Cheatsheet & Interview Q&A.md` ([cheatsheet-interview.md](../../procedures/authoring/cheatsheet-interview.md)).

Do **not** duplicate the full Formula Cheat Sheet, Tiered Interview Q&A, or Worked Practice Problems inside the main note; those now live in `<note stem> - Cheatsheet & Interview Q&A.md` with tap-to-reveal collapsible answers (`> [!tip]- Answer` and `> [!tip]- Solution`).

Review claims, citations, formula folds, local visual embeds, and readability against [verification-checklist.md](../../procedures/review/verification-checklist.md) before saving; repair the smallest affected span rather than regenerating whole chapters. For multi-chapter `M1` collections, follow [composition-contract.md](../../procedures/authoring/composition-contract.md).
