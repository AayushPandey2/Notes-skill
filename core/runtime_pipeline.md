# Direct-Authoring Workflow, Layer Activation & Graceful Degradation

The [root authoring rule and precedence](../SKILL.md#scriptorium) govern every route. Enforce safety and authorization throughout.

## 1. Execution Sequence

This sequence governs **creation**, **revision** (reconciling existing notes non-destructively), **video ingestion** (`/scribe-ytnotes` transcript-first mode via [video-notes.md](../docs/blueprints/formats/video-notes.md)), and **fallback delivery** (downloadable `.md` / chat Markdown when vault writes are unavailable):

1. **Resolve request:** Infer mode (`create`, `update`, `video_ingest`, or `fallback`), output format (defaulting bare topics to `M1`), permitted sources (`source_permissions`), user constraints, learner profile, layout, and authorized destination directly—never ask *"which type of notes do you want?"* or send a reverification prompt.
2. **Select applicable policies & scale activation:** Confirm the required instruction dependencies below. Load only the selected master (`docs/blueprints/formats/`), preset (`docs/blueprints/presets/`), primary subject (+ selective secondary support), knowledge type, and active functional layers from the **Layer Activation Matrix** below, adjusted for **`Master × preset × topic breadth × requested depth × evidence risk`**.
3. **Plan the artifacts:** Resolve the included artifacts, omissions, dependencies, and permissions before drafting. For a compact artifact, record its objective, boundaries and essential checks. For a substantive chapter or collection, use the three-level [adaptive plan](../docs/procedures/authoring/adaptive-engine.md).
4. **Research and refine *(conditioned on `Claim verification` & `source_permissions`)*:** Discover needed concepts and verify consequential claims ([source-fidelity.md](../docs/procedures/sourcing/source-fidelity.md), [claim-verification.md](../docs/procedures/sourcing/claim-verification.md)), updating the internal plan as evidence emerges.
5. **Check examples and visuals:** Apply the [example validity gate](../docs/blueprints/components/example-engineering.md) when the artifact includes examples. Inspect needed visuals before publishing and follow the source permissions for external acquisition.
6. **Author coherent artifacts:** For a substantial chapter or collection, review a representative core unit against its objective before extending the draft. Author Markdown directly for the resolved artifacts, preserving substantive depth under [the theory contract](theory_quality_contract.md).
7. **Review and repair (before saving):** Apply the applicable checks to complete drafts and assets under [the verification policy](../docs/procedures/review/verification-checklist.md), which owns review depth, repair and acceptance. Use adversarial review when a substantive theory argument or material uncertainty warrants it.
8. **Publish and inspect (after saving):** Verify the resolved destination stays inside the approved vault ([pre-gen-gate.md](../docs/procedures/authoring/pre-gen-gate.md)), create topic directories only for accepted/disclosed-limitation deliveries, publish approved assets alongside accepted notes (tracking actually created files, reporting any partial publication failure honestly, and **never** deleting preexisting user assets during cleanup), and run **Stage 6** post-save integrity inspection on actual saved files.

### Required instruction dependencies

Before drafting, confirm the resolved format, [artifact registry](../docs/dispatch/master-registry.yaml), [source policy](../docs/procedures/sourcing/source-fidelity.md), [authoring rules](authoring_rules.md), and [verification policy](../docs/procedures/review/verification-checklist.md) are accessible. Read the applicable rules from those owners. For substantive theory, also load [theory quality](theory_quality_contract.md) and [teaching core](teaching_core.md); select concept reasoning, editorial and specialist guidance by the activation matrix. A cross-reference does not by itself activate another policy.

Recover a missing reference from its canonical package location if possible. If a governing policy remains unreadable, name it and identify the affected artifact or claim. Publish a reduced artifact only when authorization, source constraints, and integrity checks can still be established. Otherwise block the dependent artifact. Optional host tools use the capability fallbacks below.

#### Minimal-Load & Conditional Fast Paths *(Soft Targets — Never Sacrifice Correctness or `M1` Completeness)*
Fast-path reference trimming applies **only** to compact formats (`M3`, atomic cards, narrow single-formula lookups) and must **never** bypass `M1` curriculum discovery, beginner prerequisite bridges, mathematical tool explanations, active visual acquisition attempts, or full educational verification. Separate **already-available root instructions**, **newly opened reference files**, **source documents**, **existing vault notes**, and **optional supporting references** rather than conflating them:
- **Compact `M3` (`quick_reference` and its presets):** Read the selected compact format and preset with the applicable source, authoring, metadata and verification rules. Open subject or domain guidance when a consequential convention, assumption, misconception or safety boundary requires it. Keep accuracy, source and table/unit checks active; skip the chapter plan, lab and extended theory review unless separately requested or necessary for a consequential claim.
- **Mathematics (`math_gates.md`):** Activate by **learning objective** (when equations, derivations, proofs, numerical calculations, units, or statistical reasoning are consequential)—not domain label alone.
- **Visuals (`representations.md`):** Skip when visuals are disabled *and* no supplied source figure requires interpretation (never skip reading/explaining user-supplied figures merely because external image acquisition is disabled).
- **Labs (`experimental-lab.md`, `investigations/`):** Load only when a practical lab or implementation guide is actually in the resolved `artifact_plan` (respecting single-file overrides and `strict` source bounds).
- **Proportional review:** Scale review scope by complexity, mathematical depth, source sensitivity, artifact count, practical risk, and revision scope while keeping essential factual, link, and source-integrity checks active on every fast path.

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
- **`Bundled` / `Multi-note`:** Activate cross-file symbol, worked-example, and ownership alignment whenever generating 2+ artifacts or reading multiple vault notes.
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
| **Vault write access** | Deliver copyable Markdown blocks or supported downloadable `.md` attachments |
| **Independent reviewer** | Run separated authoring and review passes; disclose lack of independent reviewer context |
| **Obsidian rendering** | Verify Markdown/YAML/LaTeX syntax statically without claiming live UI rendering |
