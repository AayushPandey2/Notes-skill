# Single-Concept Transcludable Knowledge Building Block

**Strict Quantitative Cap**: Total Markdown body **<150 words** (including the link block). Use canonical titles and paths so larger DeepStudy notes can embed this note via native Obsidian transclusion (`![[Canonical Title]]`). Never trigger recursive atomic generation.
- **Routing & Destination Rules**:
    - Supports `/scribe-atomic-notes <topic name>` (bypasses deep multi-hop research workflows; uses a single, direct web search/fetch to gather core facts quickly) as well as atomic definitions planned inside a multi-note run.
    - Save all atomic notes into the centralized shared `Atomic Notes/` folder located at the **same directory level** (sibling level) as the `<subtopic>/` folders (e.g., `Atomic Notes/<topic_name>.md`).
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

> [!important] AGENT AUTHORING DIRECTIVE — `atomic` Keep the entire Markdown body strictly under 150 words so this file functions as a clean, zero-fluff transclusion block (`![[...]]`) inside larger notes. Focus on one indivisible definition, one governing equation/invariant, one micro-example, and verified knowledge-graph links. Apply the mandatory **Humanization & Cohesion Pass** before finalizing: write in a conversational yet rigorous tone to your future self, connect the definition to the micro-example and boundary condition with natural transitions, ban AI clichés ("In conclusion," "It is important to note," "Delving into," "Crucial aspect," "Let's explore"), and synthesize retrieved facts into an intuitive mental model rather than pasting raw definitions.
