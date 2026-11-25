# M1 — Deep Learning Notes

- **Master ID:** `M1` (`deep_notes` / compatibility route `deepstudy-master`)
- **Primary intent:** `comprehensive_learning` — deliver a complete, zero-prerequisite, self-contained explanation from first intuition through formal derivations, multi-step numerical traces, evaluation, common pitfalls, and independent practice.
- **Activation signals:** `"teach me from scratch"`, `"explain deeply"`, `"comprehensive notes"`, `"from fundamentals to advanced"`, or bare `/scribe-notes <topic>` without an explicit alternate product format.
- **Non-activation:** Do not select `M1` when the user primarily requests a compact `<350`-word cheat sheet (`M3`), pure solved problem set (`M4`), pure algorithm build guide (`M5`), pure quiz/flashcards (`M6`), or standalone comparison/revision pack (`M7`).
- **Load as needed:** [teaching rules](../../../core/teaching_core.md), [math guidance](../../../core/math_gates.md), [visual rules](../../procedures/authoring/representations.md), [adaptive planning](../../procedures/authoring/adaptive-engine.md), [research](../../procedures/sourcing/research-engine.md), [source fidelity](../../procedures/sourcing/source-fidelity.md), and [authoring rules](../../../core/authoring_rules.md).
- **Output profile:** Comprehensive collections use the five-key YAML profile in [properties policy](../../properties/properties-policy.md); single or existing notes use Obsidian properties without overwriting user-managed fields.

## 1. Opening Roadmap (Purpose, Learning Path & TOC)

Open cleanly with line-1 YAML, H1 title, a concise purpose and learning path (without repeating YAML `difficulty` as a visible body dump), and a compact **clickable Obsidian Table of Contents** (`- [[#1. Heading|Short Label]]`). Apply the 3-tier prerequisite rule in [teaching_core.md](../../../core/teaching_core.md): never use a link to replace an essential local foundation.

## 2. Progressive Explanation Flow

Load and follow the matching knowledge-type subtemplate (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, or `historical`). Use fewer, **question-driven** `H1–H4` headings developed through explanation, example, and interpretation (never 1-sentence micro-sections, bold pseudo-headings, or identical headings forced across domains), **short single-idea paragraphs (1–3 sentences)**, blank lines between complex list items, sparing non-collapsed `[!info]` definition callouts, right-aligned numerical tables (placed *after* explaining compared ideas), and controlled bolding—with **no `==highlight==`, semantic highlight spans, or `\color{...}` in formulas**. Reserve `---` horizontal rules for major thematic transitions only. Realize [teaching_core.md](../../../core/teaching_core.md) progressively:

1. **One Conceptual Burden at a Time (Opening):** Introduce the outcome to estimate, known examples, combined score, probability, and separate threshold rule progressively before introducing advanced terms (never stuffing advanced claims into an opening callout to shorten a paragraph).
2. **Definitions & Prerequisites:** Teach essential building blocks locally; for key definitions, establish the need, state a concise definition, translate to ordinary language, demonstrate beside it, and establish the nearest boundary—separating definition, consequence, assumption, and optional advanced property.
3. **Motivated Representations & Early Running Example:** Visualize and trace one tiny concrete dataset early, and explain *what* each new representation expresses, *why* transform, *what* changes numerically, and *what* stays invariant before showing comparison tables.
4. **Limitations of Simpler Baselines:** Show where a simpler baseline is limited on concrete numbers (calm, qualified language) alongside an inspected contrast visual.
5. **Objective-Driven Mathematics & Explicit Transitions:** Follow [math_gates.md](../../../core/math_gates.md) to choose each concept's minimum math profile, build the explanatory bridge before every equation, build multi-step objectives (such as MLE → log-loss) as a sequence of questions with a small numerical example, never skip central transitions with `"rearranging gives"`, and place `> [!example]- Understand this formula step by step` directly beneath every displayed `$$...$$` block.
6. **Mechanism-Interpreted Traces & Consolidated Scope:** Carry the running dataset through numerical updates explaining *why* initial predictions start as they do, what residual signs mean, why features multiply residuals, why averaging happens, why subtracting a negative gradient increases a weight, and why total loss can drop while individual points worsen. Consolidate core mechanics before extensions (labeling brief orientations honestly), and teach metrics from actual vs. predicted counts (TP/FP/TN/FN first) before any summary table.
7. **Qualified Best Practices & Visible Checkpoints:** Flag and qualify strong claims (calibration, optimum existence, outlier robustness, solver defaults, regularization scaling), state *"What It Does NOT Require"* boundaries, and place visible `> [!question] Concept Checkpoint` blocks (with nested collapsed `> > [!success]- Reveal Answer`) after major sections.

## 3. Closing Mental Model, Notation Reference & Companion Handoff

End deep notes cleanly with a crisp **5–7 step Final Numbered Mental Model**, the trailing **Notation Reference** (complete Symbol Dictionary), and reciprocal links to `<note stem> - Experimental Lab.md` ([experimental-lab.md](../../procedures/authoring/experimental-lab.md)) and `<note stem> - Cheatsheet & Interview Q&A.md` ([cheatsheet-interview.md](../../procedures/authoring/cheatsheet-interview.md)).

Do **not** duplicate the full Formula Cheat Sheet, Tiered Interview Q&A, or Worked Practice Problems inside the main note; those now live in `<note stem> - Cheatsheet & Interview Q&A.md` with tap-to-reveal collapsible answers (`> [!tip]- Answer` and `> [!tip]- Solution`).

Review claims, citations, formula folds, local visual embeds, and readability against [verification-checklist.md](../../procedures/review/verification-checklist.md) before saving; repair the smallest affected span rather than regenerating whole chapters. For multi-chapter `M1` collections, follow [composition-contract.md](../../procedures/authoring/composition-contract.md).
