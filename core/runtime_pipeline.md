# Direct-Authoring Workflow, Layer Activation & Graceful Degradation

The [authoring rule in the root skill](../SKILL.md#scriptorium) governs every note-creation route. Educational code in a note is lesson content, never a note builder. Respect active safety and authorization boundaries continuously throughout every step—never treat them solely as end-of-pipeline checks.

## 1. Execution Sequence

1. **Resolve request:** Infer intent, output format (defaulting bare topics to `M1`), permitted sources (`source_permissions`), user constraints, learner profile, single-bundle vs. multi-branch layout, and authorized destination directly—never ask *"which type of notes do you want?"* or send a reverification prompt.
2. **Select applicable policies:** Load only the selected master (`docs/blueprints/formats/`), preset (`docs/blueprints/presets/`), primary subject (+ selective secondary support), knowledge type, and active functional layers from the **Layer Activation Matrix** below.
3. **Construct learning plan:** Build the internal three-level plan in [adaptive-engine.md](../docs/procedures/authoring/adaptive-engine.md): concept objectives, dependencies, target `0–5` depth, scope/resource estimate, and the resolved `artifact_plan` manifest dictating which artifacts and visuals are included or omitted.
4. **Research and refine:** Discover needed concepts and verify consequential claims within active `source_permissions` ([source-fidelity.md](../docs/procedures/sourcing/source-fidelity.md), [claim-verification.md](../docs/procedures/sourcing/claim-verification.md)), updating the internal plan as evidence emerges.
5. **Engineer examples:** Apply the validity gate in [example-engineering.md](../docs/blueprints/components/example-engineering.md), align shared fixtures, check calculations, select needed visual representations, and align assessments with concept objectives.
6. **Author coherent artifacts:** Draft Markdown directly, emitting only the artifacts marked `included: true` in the resolved `artifact_plan` (per `artifact_policy` in [master-registry.yaml](../docs/dispatch/master-registry.yaml) and `source_permissions`).
7. **Review and repair (before saving):** Run **Stages 1–5** of [verification-checklist.md](../docs/procedures/review/verification-checklist.md) and [adversarial-theory-review.md](../docs/procedures/review/adversarial-theory-review.md) on the **complete drafts before saving**. Resolve an explicit acceptance decision (`accepted`, `accepted_with_disclosed_limitations`, `repair_required`, or `blocked`), executing bounded dependency-aware repairs and stopping repeated loops when no new evidence or host capability is available.
8. **Publish and inspect (after saving):** Verify the resolved destination stays inside the approved vault ([pre-gen-gate.md](../docs/procedures/authoring/pre-gen-gate.md)), save accepted files (or use downloadable/chat fallback when vault write is unavailable), and run **Stage 6** post-save integrity inspection on actual saved files.

## 2. Layer Activation Matrix

Activate functional layers as **execution defaults** proportional to the artifact—these control how much reasoning and verification work the author performs, never adding mandatory boilerplate headings:

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
