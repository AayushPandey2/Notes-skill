# M1 — Deep Learning Notes

- **Master ID:** `M1` (`deep_notes` / compatibility route `deepstudy-master`)
- **Primary intent:** `comprehensive_learning` — deliver a complete, zero-prerequisite, self-contained explanation from first intuition through formal derivations, multi-step numerical traces, evaluation, common pitfalls, and independent practice.
- **Activation signals:** `"teach me from scratch"`, `"explain deeply"`, `"comprehensive notes"`, `"from fundamentals to advanced"`, or bare `/scribe-notes <topic>` without an explicit alternate product format.
- **Non-activation:** Do not select `M1` when the user primarily requests a compact `<350`-word cheat sheet (`M3`), pure solved problem set (`M4`), pure algorithm build guide (`M5`), pure quiz/flashcards (`M6`), or standalone comparison/revision pack (`M7`).
- **Load as needed:** [teaching rules](../../../core/teaching_core.md), [math guidance](../../../core/math_gates.md), [visual rules](../../procedures/authoring/representations.md), [adaptive planning](../../procedures/authoring/adaptive-engine.md), [research](../../procedures/sourcing/research-engine.md), [source fidelity](../../procedures/sourcing/source-fidelity.md), and [authoring rules](../../../core/authoring_rules.md).
- **Output profile:** Comprehensive collections use the five-key YAML profile in [properties policy](../../properties/properties-policy.md); single or existing notes use Obsidian properties without overwriting user-managed fields.

## 1. Opening Roadmap (Difficulty, Prerequisites, Objectives & TOC)

Open cleanly with line-1 YAML, H1 title, and three **blank-line-separated** metadata blocks (`Difficulty`, `Prerequisites` — noting essential concepts are taught locally — and `Learning objectives`), followed by a compact numbered **Table of Contents** written as plain numbered section titles with **zero links** (never use `[[#...]]` or `[...](#...)` links inside the Table of Contents). Apply the 3-tier prerequisite rule in [teaching_core.md](../../../core/teaching_core.md): never use a link to replace an essential local foundation.

## 2. Progressive Self-Contained Flow (See It → Understand It → Derive It → Calculate It → Apply It)

Load and follow the matching knowledge-type subtemplate (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, or `historical`). Use short, navigable `H1–H4` headings (never bold text as pseudo-headings), **short single-idea paragraphs (1–3 sentences)**, blank lines between complex list items, right-aligned numerical tables, and controlled bolding. Realize the applicable [teaching layers](../../../core/teaching_core.md#conceptual-flow--progressive-teaching-layers) in natural domain order:

1. **Introduction & Intuition:** Explain what the concept does in plain language, where it applies, and clarify any misleading name without dumping advanced jargon upfront.
2. **Prerequisite Concepts & Base Models:** Teach every essential building block locally (e.g., base models, loss functions, derivatives, or structural rules) before combining them.
3. **Example Dataset & Early Intuitive Walkthrough:** Introduce one tiny concrete dataset early and trace an intuitive example on it *before* full derivations, introducing symbols **progressively** as they enter (reserving the full **Notation Reference** for the end of the note).
4. **Limitations of Simpler Baselines:** Show where a simpler baseline breaks on concrete numbers (using calm, qualified language—never dramatic absolutes) alongside a contrast visual.
5. **Model Construction & Spacious Mathematics:** Progress from **1-variable scalar case → multi-term sum → compact vector/matrix form**. Break composite equations into separate numbered display blocks, use multiline `aligned` derivations rather than single-line `\implies` chains, highlight core formulas with `\boxed{...}`, and explain mathematical **meaning visibly** in prose rather than attaching `> [!note]- 📐 Understand this formula` folds or `"Read aloud"` transcriptions.
6. **Complete Step-by-Step Training & Algorithmic Coverage:** Walk the **exact same running dataset** through multi-step calculations with inputs clearly distinguished from outputs; when teaching selection algorithms (e.g., splits), compare candidate choices in a table; when covering both regression and classification, develop classification mechanics (logits, sigmoid, probabilities, gradients) explicitly.
7. **Evaluation, Regularization & Qualified Best Practices:** Define metrics around the shared fixture, explain regularization and hyperparameters with concrete numbers, state assumptions and *"What It Does NOT Require"* boundaries, show `Mistake | Correct approach` tables, and place short 2–4 question **Concept Checkpoints** after major sections.

## 3. Closing Mental Model, Notation Reference & Companion Handoff

End deep notes cleanly with a crisp **5–7 step Final Numbered Mental Model**, the trailing **Notation Reference** (complete Symbol Dictionary), and reciprocal links to `<note stem> - Experimental Lab.md` ([experimental-lab.md](../../procedures/authoring/experimental-lab.md)) and `<note stem> - Cheatsheet & Interview Q&A.md` ([cheatsheet-interview.md](../../procedures/authoring/cheatsheet-interview.md)).

Do **not** duplicate the full Formula Cheat Sheet, Tiered Interview Q&A, or Worked Practice Problems inside the main note; those now live in `<note stem> - Cheatsheet & Interview Q&A.md` with tap-to-reveal collapsible answers (`> [!tip]- Answer` and `> [!tip]- Solution`).

Review claims, citations, formula folds, local visual embeds, and readability against [verification-checklist.md](../../procedures/review/verification-checklist.md) before saving; repair the smallest affected span rather than regenerating whole chapters. For multi-chapter `M1` collections, follow [composition-contract.md](../../procedures/authoring/composition-contract.md).
