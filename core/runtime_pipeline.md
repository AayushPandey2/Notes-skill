# Direct-Authoring Workflow, Layer Activation & Graceful Degradation

The [root authoring rule and precedence](../SKILL.md#scriptorium) govern every route. Enforce safety and authorization throughout.

## 1. Ten-Stage Educational Authoring Lifecycle

This unified lifecycle governs **creation**, **revision** (reconciling existing notes non-destructively), **video ingestion** (`/scribe-ytnotes` transcript-first mode via [video-notes.md](../docs/blueprints/formats/video-notes.md)), and **fallback delivery** (downloadable `.md` / chat Markdown when vault writes are unavailable):

1. **Resolve the learning request:** Determine subject, intended learning objective, learner level, requested scope, output format (defaulting bare comprehensive requests to `M1`), source restrictions (`source_permissions`), requested artifacts, available host capabilities, and publication authorization—never ask *"which type of notes do you want?"* and never silently narrow a comprehensive request into a summary.
2. **Discover the conceptual territory:** Load the matching policies from the activation matrix below (never reading unrelated directories) and identify the subject's foundational concepts, motivating problems, definitions, mechanisms, math, assumptions, variants, applications, misconceptions, failures, practical details, comparisons, and extensions ([curriculum-discovery.md](../docs/procedures/authoring/curriculum-discovery.md)) as a coverage plan, not a mandatory heading list.
3. **Construct the dependency order:** Determine which concepts and prerequisites must precede others and order the learning material by intellectual dependencies rather than alphabetical or research-paper order (preserving source sequence where required by source mode).
4. **Design the educational presentation:** For each central learning unit ([adaptive-engine.md](../docs/procedures/authoring/adaptive-engine.md), [concept-reasoning.md](../docs/procedures/authoring/concept-reasoning.md)), decide what the learner should understand, which explanation strategy fits, what terminology and math reasoning are needed, whether visuals add essential understanding, which examples reveal the mechanism ([example-engineering.md](../docs/blueprints/components/example-engineering.md)), what stays visible vs. progressive disclosure, and which checkpoints confirm understanding—without forcing identical unit structures.
5. **Acquire and validate learning resources:** When authorized and relevant ([source-fidelity.md](../docs/procedures/sourcing/source-fidelity.md), [claim-verification.md](../docs/procedures/sourcing/claim-verification.md), [representations.md](../docs/procedures/authoring/representations.md)), consult authoritative sources, acquire and inspect needed visuals, inspect supplied figures, establish mathematical references, verify current/versioned technical claims, and resolve uncertain terminology without fabricating assets or using prohibited scripts.
6. **Write the educational narrative:** Author Markdown directly in a natural teaching progression—teaching concepts and simpler baselines before assuming familiarity with terminology or advanced upgrades, connecting mathematics to mechanisms, and weaving meaningful examples and adjacent visuals into connected prose under [teaching_core.md](teaching_core.md) and [theory_quality_contract.md](theory_quality_contract.md).
7. **Develop mastery:** Integrate appropriate recall, explanation, calculation, prediction, method selection, reverse reasoning, failure diagnosis, and transfer opportunities adapted to the active format and artifact plan.
8. **Perform educational review:** Review the completed draft and assets from consolidated learner, subject-specialist, mathematical, visual-learning, textbook-editor, practical, and source perspectives under [verification-checklist.md](../docs/procedures/review/verification-checklist.md) and [adversarial-theory-review.md](../docs/procedures/review/adversarial-theory-review.md)—identifying real omissions or errors and never accepting a draft merely because expected sections exist.
9. **Repair and recheck:** Correct confirmed defects and reinspect affected downstream explanations, calculations, visuals, companion artifacts, and dependencies without rewriting stable sections unnecessarily.
10. **Final delivery:** Verify requested scope, metadata, mathematical formatting, navigation, source fidelity, image references, artifact consistency, and publication authorization; create topic directories inside the approved vault ([pre-gen-gate.md](../docs/procedures/authoring/pre-gen-gate.md)) only for accepted/disclosed-limitation deliveries; publish approved assets alongside accepted notes (never deleting preexisting user assets); and inspect actual saved files under Stage 6 post-save verification without claiming publication unless it occurred.

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
