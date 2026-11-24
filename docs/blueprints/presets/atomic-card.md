<!-- scaffold:preflight
Purpose: Create an atomic, transcludable single-concept knowledge card (<150 words total) ready for native Obsidian '![[Canonical Title]]' embedding.
Parent Master: M3 (../formats/quick-reference.md) | Route: atomic (variant: atomic_card).
Activation Trigger: "/scribe-notes atomic note on <concept>" or single-concept card item inside a collection plan.
Non-activation: Never trigger recursive atomic card generation; defer multi-concept guides to M1/M2.
Inputs: Single canonical concept title, single direct fact lookup/verification, existing vault link targets.
Dependencies: router.md, core/authoring_rules.md, core/math_gates.md.
Decision Rules: Strictly <150 words body (including links); one indivisible claim + one micro-example + one boundary; bounded direct fetch only.
Failure Handling: Represent planned non-existent vault links cleanly as plain text marked '(pending note)' rather than fabricating dead wikilinks.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md).
-->

# Single-Concept Transcludable Knowledge Building Block

- **Placement & Header:** Save to `Atomic Notes/<Canonical Concept Title>.md` with line-1 YAML + `# <Canonical Concept Title>` (strictly **<150 words** total Markdown body).

## What is this concept and its governing claim?

`2–3` high-precision sentences defining the exact concept plus its governing relation (`$$...$$` only if `math_level >= 1`).

## What does a tiny concrete example look like?

One micro numerical, structural, or real-world example (`2–3` lines max) clarifying the definition immediately.

## Where does the intuition break?

One crisp sentence stating the primary boundary condition, limitation, or misconception.

## How does this connect to the vault?

- **Parent / Broader:** `[[Resolved Vault Note or Plan Entry]]`
- **Contrasts With:** `[[Resolved Vault Note or Plan Entry]]`
- **Used In:** `[[Resolved Vault Note or Plan Entry]]` (mark unbuilt targets `(pending note)` in plain text).

<!-- optional: boundary -->
## [OPTIONAL] Which nearby case falls outside this definition? (Boundary Case)

<!-- Include only if distinct from Section 3 and total body remains strictly <150 words; delete completely otherwise. -->

- **Context / Analysis / Check:** Near-miss contrast, exact discriminating condition, and membership check.

- **Contract Summary:** Verify `<150`-word cap, single indivisible claim, valid links, and [authoring_rules.md](../../../core/authoring_rules.md) / [math_gates.md](../../../core/math_gates.md) / [footer_widgets.md](../../../core/footer_widgets.md).
