# M1 — Deep Learning Notes

- **Master ID:** `M1` (`deep_notes` / compatibility route `deepstudy-master`)
- **Primary intent:** `comprehensive_learning` — deliver a complete, zero-prerequisite, self-contained explanation from first intuition through formal derivations, multi-step numerical traces, evaluation, common pitfalls, and independent practice.
- **Activation signals:** `"teach me from scratch"`, `"explain deeply"`, `"comprehensive notes"`, `"from fundamentals to advanced"`, or bare `/scribe-notes <topic>` without an explicit alternate product format.
- **Non-activation:** Do not select `M1` when the user primarily requests a compact `<350`-word cheat sheet (`M3`), pure solved problem set (`M4`), pure algorithm build guide (`M5`), pure quiz/flashcards (`M6`), or standalone comparison/revision pack (`M7`).
- **Load as needed:** [teaching rules](../../../core/teaching_core.md), [math guidance](../../../core/math_gates.md), [visual rules](../../procedures/authoring/representations.md), [adaptive planning](../../procedures/authoring/adaptive-engine.md), [research](../../procedures/sourcing/research-engine.md), [source fidelity](../../procedures/sourcing/source-fidelity.md), and [authoring rules](../../../core/authoring_rules.md).
- **Output profile:** Comprehensive collections use the five-key YAML profile in [properties policy](../../properties/properties-policy.md); single or existing notes use Obsidian properties without overwriting user-managed fields.

## 1. Opening Roadmap (Goal, Prerequisites & TOC)

Open cleanly with line-1 YAML, H1 title, a concise 3-line framing (`Level`, `Prerequisites` — noting all essential concepts are explained locally — and `Goal`), and a compact numbered **Table of Contents** written as plain numbered section titles with **zero links** (never use `[[#...]]` or `[...](#...)` links inside the Table of Contents). Apply the 3-tier prerequisite rule in [teaching_core.md](../../../core/teaching_core.md): never use a link to replace an essential local foundation.

## 2. Progressive Self-Contained Flow (Micro-Cadence & 12 Layers)

Load and follow the matching knowledge-type subtemplate (`conceptual`, `mathematical`, `computational`, `scientific`, `empirical`, or `historical`) and write in **short, crisp single-idea paragraphs (1–3 sentences)** separated by tables, calculations, and strategic visuals. Realize the applicable [12 teaching layers](../../../core/teaching_core.md#twelve-generalized-teaching-layers) in natural domain order without forcing irrelevant code or math onto non-quantitative topics:

1. **Orientation, Real-World Map & Naming Clarification:** Start with a tiny concrete input-to-output table showing what the idea produces, add a real-world applications table, and clarify any misleading name (e.g., why its name reflects its math vs. its use).
2. **Terminology, Concrete Dataset Table & Upfront Symbol Dictionary:** Show a tiny concrete multi-column fixture *before* defining terms; map each column to its role; include a complete **Symbol Dictionary** (`Symbol | Meaning`) plus explicit **notation-clash notes** wherever textbooks disagree.
3. **Why Simpler Alternatives Fail:** Test the simpler baseline on concrete numbers that produce impossible or broken results, place a **failure-contrast visual** beside the math, and summarize in a comparison table.
4. **Local Zero-Prerequisite Foundations:** Teach every needed mathematical or conceptual building block from scratch—with tiny reference value tables, governing identities, and boundary curves—before using them.
5. **Progressive Model Construction:** Show the end-to-end stage pipeline using an inspected downloaded web diagram (never Mermaid or ASCII), then progress from **1-variable scalar case → multi-variable summation (with explicit contribution table) → compact vector/matrix or general form**, verifying matrix/data shapes visibly.
6. **Component-by-Component Equation & Visual Dissection:** Break core formulas into parts (`Part | Purpose`), test **negative, zero, positive, and extreme limiting inputs** alongside paired curve/derivative visuals ([representations.md](../../procedures/authoring/representations.md)), pair every `$$...$$` with `> [!note]- 📐 Understand this formula`, and state **"what this does NOT imply"** caveats cleanly.
7. **First-Principles Origin, Multi-Iteration Trace & Evaluation:** Derive *why* the rule or objective follows from first principles (noting numerical stability fixes where computational), trace a tiny fixture through **Iteration 1 → Update → Iteration 2** by hand, and define evaluation metrics and calibration around **one shared numerical fixture** (explaining when metrics like accuracy mislead).
8. **Constraints, Assumptions ("What It Does NOT Require") & Variants:** Cover regularization/constraints with concrete penalty numbers, explicit assumptions alongside a **"What this method does NOT assume or require"** section, data preprocessing/leakage hygiene, variants, a `Mistake | Correct approach` table, and a multi-method comparison table.

## 3. Closing Mental Model & Companion Handoff

End deep notes cleanly with a crisp **5–7 step Final Numbered Mental Model** recapping the entire mechanism end to end, plus reciprocal links to the topic's two required companion files—`<note stem> - Experimental Lab.md` ([experimental-lab.md](../../procedures/authoring/experimental-lab.md)) and `<note stem> - Cheatsheet & Interview Q&A.md` ([cheatsheet-interview.md](../../procedures/authoring/cheatsheet-interview.md)).

Do **not** duplicate the full Formula Cheat Sheet, Tiered Interview Q&A, or Worked Practice Problems inside the main note; those now live in `<note stem> - Cheatsheet & Interview Q&A.md` with tap-to-reveal collapsible answers (`> [!tip]- Answer` and `> [!tip]- Solution`).

Review claims, citations, formula folds, local visual embeds, and readability against [verification-checklist.md](../../procedures/review/verification-checklist.md) before saving; repair the smallest affected span rather than regenerating whole chapters. For multi-chapter `M1` collections, follow [composition-contract.md](../../procedures/authoring/composition-contract.md).
