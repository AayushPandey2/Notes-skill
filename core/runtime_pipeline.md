# Direct-Authoring Workflow, Layer Activation & Graceful Degradation

The [authoring rule in the root skill](../SKILL.md#scriptorium) governs every note-creation route. During normal note authoring, never create or execute custom scripts, builders, or note code (trusted standalone verification scripts under `evaluations/` are strictly development-only tooling). Respect active safety and authorization boundaries continuously throughout every step—never treat them solely as end-of-pipeline checks.

## 1. Execution Sequence

This sequence governs **creation**, **revision** (reconciling existing notes non-destructively), **video ingestion** (`/scribe-ytnotes` transcript-first mode via [video-notes.md](../docs/blueprints/formats/video-notes.md)), and **fallback delivery** (downloadable `.md` / chat Markdown when vault writes are unavailable):

1. **Resolve request:** Infer mode (`create`, `update`, `video_ingest`, or `fallback`), output format (defaulting bare topics to `M1`), permitted sources (`source_permissions`), user constraints, learner profile, layout, and authorized destination directly—never ask *"which type of notes do you want?"* or send a reverification prompt.
2. **Select applicable policies & scale activation:** Confirm the required instruction dependencies below. Load only the selected master (`docs/blueprints/formats/`), preset (`docs/blueprints/presets/`), primary subject (+ selective secondary support), knowledge type, and active functional layers from the **Layer Activation Matrix** below, adjusted for **`Master × preset × topic breadth × requested depth × evidence risk`**.
3. **Construct learning plan *(conditioned on resolved layer activation)*:** Build the internal three-level plan in [adaptive-engine.md](../docs/procedures/authoring/adaptive-engine.md): concept objectives (only as heavy as active `Concept reasoning` / `Curriculum discovery` require), dependencies, target `0–5` depth, scope/resource estimate, and the extensible `artifact_plan` manifest (`artifacts[]`, `omitted_artifacts`, `permissions.external_visuals`).
4. **Research and refine *(conditioned on `Claim verification` & `source_permissions`)*:** Discover needed concepts and verify consequential claims ([source-fidelity.md](../docs/procedures/sourcing/source-fidelity.md), [claim-verification.md](../docs/procedures/sourcing/claim-verification.md)), updating the internal plan as evidence emerges.
5. **Engineer examples & stage visual checks:** Apply the validity gate in [example-engineering.md](../docs/blueprints/components/example-engineering.md), align shared fixtures, check calculations, and check planned representations and inspect needed external/native visual assets (external acquisition requires the corresponding permission) outside the final vault directory first where host tools permit—resolving intended filenames and links without prematurely creating unused vault folders.
6. **Author coherent artifacts:** Draft and review one complete representative core unit against its objective and mechanism before carrying its structure into later units. Then author Markdown directly, emitting only entries in `artifact_plan.artifacts` while strictly upholding the **Educational Depth Preservation Contract** ([theory_quality_contract.md](theory_quality_contract.md)).
7. **Review and repair (before saving):** Run **Stages 1–5** of [verification-checklist.md](../docs/procedures/review/verification-checklist.md) and [adversarial-theory-review.md](../docs/procedures/review/adversarial-theory-review.md) on the **complete drafts and required asset dependencies before saving**. Resolve an explicit acceptance decision (`accepted`, `accepted_with_disclosed_limitations`, `repair_required`, or `blocked`), executing bounded dependency-aware repairs and stopping repeated loops when no new evidence or host capability is available.
8. **Publish and inspect (after saving):** Verify the resolved destination stays inside the approved vault ([pre-gen-gate.md](../docs/procedures/authoring/pre-gen-gate.md)), create topic directories only for accepted/disclosed-limitation deliveries, publish approved assets alongside accepted notes (tracking actually created files, reporting any partial publication failure honestly, and **never** deleting preexisting user assets during cleanup), and run **Stage 6** post-save integrity inspection on actual saved files.

### Required instruction dependencies

Before drafting, confirm readable copies of the routing and artifact registries, resolved format, governing source policy, teaching rules, and verification procedure. For substantive theory also load [theory quality](theory_quality_contract.md), [teaching core](teaching_core.md), [concept reasoning](../docs/procedures/authoring/concept-reasoning.md), and [the educational editor](../docs/procedures/review/educational-editor.md). Load [math gates](math_gates.md) when mathematics serves an objective, and [representation guidance](../docs/procedures/authoring/representations.md) when an objective depends on a representation. Read selected subject or companion policies when their roles are present.

Recover a missing reference from its canonical package location if possible. If a governing policy remains unreadable, name it and identify the affected artifact or claim. Publish a reduced artifact only when authorization, source constraints, and integrity checks can still be established. Otherwise block the dependent artifact. Optional host tools use the capability fallbacks below.

## 2. Layer Activation Matrix (Objective-Adaptive Starting Configuration)

Treat this matrix as the **default starting configuration**, then adjust proportionally by **`Master × preset × topic breadth × requested depth × evidence risk`** (for example, tighten full claim verification on a brief `M7` `quick_summary` or full learner adaptation on a single-integral `M4` calculation, while expanding `Concept reasoning` on a dense `M3` API reference or `Consistency` on a multi-chapter `M6` mock exam). Never add mandatory boilerplate headings:

| Functional Layer | `M1` | `M2` | `M3` | `M4` | `M5` | `M6` | `M7` | `Video` |
|---|---|---|---|---|---|---|---|---|
| **Concept reasoning** | Full | Full | Light | Full | Full | Relevant | Relevant | Full |
| **Learner adaptation** | Full | Relevant | Light | Full | Relevant | Full | Full | Relevant |
| **Curriculum discovery** | Full | Source-bound | Off | Limited | Limited | Objective-bound | Selective | Source-bound |
| **Claim verification** | Full | Full | Selective | Full | Full | Answers | Full | Full |
| **Example engineering** | Full | Permitted | Light | Full | Full | Full | Relevant | Permitted |
| **Consistency** | Bundled | Bundled | Relevant | Relevant | Relevant | Relevant | Multi-note | Relevant |
| **Educational editor** | Full | Full | Light | Full | Full | Full | Full | Full |
| **Mastery design** | Optional | Permitted | Off | Transfer | Transfer | Full | Relevant | Optional |
| **Retention** | Optional | Optional | Off | Optional | Off | Optional | Full | Optional |

*(Interactive `/scribe-quiz` sessions activate `Mastery design` and `Retention` read-only over existing vault notes via [skills/scribe-quiz/SKILL.md](../skills/scribe-quiz/SKILL.md).)*

### Activation Level Legend
- **`Full`:** Apply all relevant responsibilities at the planned target depth.
- **`Relevant`:** Apply only the parts that directly support the artifact's active objectives or failure modes.
- **`Light`:** Inspect the central concept, governing conditions, and nearest discriminating boundary.
- **`Selective`:** Activate only for uncertain, consequential, or boundary-sensitive material.
- **`Source-bound` / `Permitted`:** Activate strictly within permitted sources and `source_permissions` (never import unsupported external additions).
- **`Limited` / `Objective-bound`:** Discover or scope only what is required to solve, implement, or assess the requested target.
- **`Bundled` / `Multi-note`:** Activate cross-file symbol, fixture, and ownership alignment whenever generating 2+ artifacts or reading multiple vault notes.
- **`Transfer` / `Answers`:** Target proof/implementation transfer or answer-key correctness rather than full theory prose.
- **`Optional`:** Activate when helpful to the user's goal and permitted by sources.
- **`Off`:** Do not load unless explicitly requested.

## 3. Capability Negotiation & Graceful Degradation

When a host environment lacks an optional capability, degrade transparently without fabricating success or abandoning supported work:

| Missing Capability | Required Fallback |
|---|---|
| **Web research** | Use permitted supplied or established knowledge; mark unconfirmed claims `[UNVERIFIED]` |
| **PDF visual inspection** | Mark inaccessible diagrams/equations explicitly; never guess hidden figures |
| **Transcript access** | Avoid reconstructing unseen video lectures; record `access_state` honestly |
| **Image acquisition** | Use reliable Markdown tables, state traces, or attributed reference links (never Mermaid/ASCII) |
| **Code execution** | Preserve `Source and static review only; not compiled or executed here.` |
| **Vault write access** | Deliver copyable Markdown blocks or supported downloadable `.md` attachments |
| **Independent reviewer** | Run separated authoring and review passes; disclose lack of independent reviewer context |
| **Obsidian rendering** | Verify Markdown/YAML/LaTeX syntax statically without claiming live UI rendering |
