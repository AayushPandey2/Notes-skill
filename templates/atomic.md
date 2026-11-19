<!-- scaffold:preflight
Pre-Flight: [router](../router.md) and [authoring rules](../shared/authoring_rules.md).
Route: `atomic` (single-concept scope, <150 words, single direct search, optional `boundary` module).
Strip this block before emission.
-->

# Single-Concept Transcludable Knowledge Building Block

**Strict Quantitative Cap**: Total Markdown body **<150 words** (including the link block). Use canonical titles and paths so larger DeepStudy notes can embed this note via native Obsidian transclusion (`![[Canonical Title]]`). Never trigger recursive atomic generation.
- **Routing & Destination Rules**:
    - Supports `/scribe-atomic-notes <topic name>` (bypasses deep multi-hop research workflows; uses a single, direct web search/fetch to gather core facts quickly) as well as atomic definitions planned inside a multi-note run.
    - Save all atomic notes into the centralized shared `Atomic Notes/` folder located at the **same directory level** (sibling level) as the `<subtopic>/` folders (e.g., `Atomic Notes/<topic_name>.md`).
- **Header Block**: Metadata per shared contract + `# <Canonical Concept Title>`.

## What is this concept and its governing claim?

<!-- Authoring note: KEEP one independently reusable claim. Define its essential terms within the note. Remove this gate before publication. -->

- `2–3` high-precision sentences defining the exact concept or claim, plus its governing relationship or formula (`$$...$$` if `math_level >= 1`).

## What does a tiny concrete example look like?

<!-- Authoring note: ADAPT to the smallest distinct concrete case. Attribute borrowed examples. Remove this gate before publication. -->

- One micro numerical, tensor-shape, or real-world example (`2–3` lines maximum) that makes the definition concrete at a glance.

## Where does the intuition break?

<!-- Authoring note: KEEP the boundary where the claim changes. MERGE a one-line condition into the claim if it suffices. Remove this gate before publication. -->

- `1` crisp sentence naming the primary boundary condition or misconception.

## How does this connect to the vault?

<!-- Authoring note: KEEP verified connections that explain where the concept applies. Remove this gate before publication. -->

- `- **Parent / Broader:** [[Resolved Vault Note or Plan Entry]]`
- `- **Contrasts With:** [[Resolved Vault Note or Plan Entry]]`
- `- **Used In:** [[Resolved Vault Note or Plan Entry]]`_(If an honest target does not exist in the vault or current routing plan, keep the relationship label and write the suggested concept as plain text marked `(pending note)`—never fabricate a dead wiki-link)._

<!-- optional: boundary -->
## [OPTIONAL] Which nearby case falls outside this definition? (Boundary Case)

<!-- Authoring note: Include a nearby contrast only when it exposes a distinct boundary. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: A plausible near miss clarifies membership within the strict `<150`-word body cap.
- When to Omit Cleanly: Omit if already covered in "Where does the intuition break?" or if adding it would breach the `<150`-word cap. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: State one discriminating condition and its consequence in 1–2 crisp lines; link fuller treatment rather than duplicating it.
-->

- **Context:** State the near-miss case and boundary condition.
- **Analysis:** Identify the exact discriminating condition and consequence.
- **Check:** State the quick membership test or linked reference.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`atomic`):** Keep total Markdown body strictly `<150` words for zero-fluff `![[Canonical Title]]` transclusion; focus on one indivisible concept, one micro-example, and verified links or `(pending note)`.
