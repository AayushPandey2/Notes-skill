# Single-Concept Transcludable Knowledge Building Block

**Strict Quantitative Cap**: Total Markdown body **<150 words** (including the link block). Use canonical titles and paths so larger DeepStudy notes can embed this note via native Obsidian transclusion (`![[Canonical Title]]`). Never trigger recursive atomic generation.
- **Header Block**: YAML frontmatter (`type: atomic`) + `# <Canonical Concept Title>`.

## What is this concept and its governing claim?

- `2–3` high-precision sentences defining the exact concept or claim, plus its governing relationship or formula (`$$...$$` if `math_level >= 1`).

## What does a tiny concrete example look like?

- One micro numerical, tensor-shape, or real-world example (`2–3` lines maximum) that makes the definition concrete at a glance.

## Where does the intuition break?

- `1` crisp sentence naming the primary boundary condition or misconception.

## How does this connect to the vault?

- `- **Parent / Broader:** [[Resolved Vault Note or Plan Entry]]`
- `- **Contrasts With:** [[Resolved Vault Note or Plan Entry]]`
- `- **Used In:** [[Resolved Vault Note or Plan Entry]]`_(If an honest target does not exist in the vault or current routing plan, keep the relationship label and write the suggested concept as plain text marked `(pending note)`—never fabricate a dead wiki-link)._

Follow [shared authoring rules](../shared/authoring_rules.md) and the [footer contract](../shared/footer_widgets.md). Apply the math gate only at the planned level. Scaffold comments are editing slots and must be removed before publication.

> [!important] AGENT AUTHORING DIRECTIVE — `atomic` Keep the entire Markdown body strictly under 150 words so this file functions as a clean, zero-fluff transclusion block (`![[...]]`) inside larger notes. Focus on one indivisible definition, one governing equation/invariant, one micro-example, and verified knowledge-graph links.
