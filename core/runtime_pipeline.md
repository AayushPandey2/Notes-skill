# Direct-Authoring Workflow, Layer Activation & Graceful Degradation

The [authoring rule in the root skill](../SKILL.md#scriptorium) governs every note-creation route. Educational code in a note is lesson content, never a note builder.

## 1. Execution Sequence

1. Infer the user's request, format (defaulting bare topics to `M1`), permitted sources, learner profile, single-bundle vs. multi-branch layout, and authorized destination directly—never ask *"which type of notes do you want?"* or send a reverification prompt.
2. Load only the selected master, preset, primary subject, knowledge type, and conditionally active layers from the **Layer Activation Matrix** below.
3. Research and verify claims within active `source_permissions` ([source-fidelity.md](../docs/procedures/sourcing/source-fidelity.md), [claim-verification.md](../docs/procedures/sourcing/claim-verification.md)).
4. Draft the intended Markdown directly, emitting only the artifact(s) dictated by `artifact_policy` in [master-registry.yaml](../docs/dispatch/master-registry.yaml) and `source_permissions`.
5. **Pre-save review:** Run Stages 1–5 of [verification-checklist.md](../docs/procedures/review/verification-checklist.md) and [adversarial-theory-review.md](../docs/procedures/review/adversarial-theory-review.md) on the **complete draft before saving**, executing dependency-aware repairs until acceptance passes.
6. **Save & post-save check:** Verify the resolved destination stays inside the approved vault ([pre-gen-gate.md](../docs/procedures/authoring/pre-gen-gate.md)), save approved files, and run Stage 6 post-save inspection on the saved files (confirming embeds, links, and untouched unrelated notes).

## 2. Layer Activation Matrix

Activate intelligence layers proportionally to the artifact—never force heavy collection layers onto atomic notes:

| Functional Layer | Atomic (`M3`) | Comprehensive (`M1`) | Source Notes (`M2`) | Labs | Revision (`M7`/`M6`) |
|---|---|---|---|---|---|
| **Concept reasoning** | Light | Full | Full | Relevant | Relevant |
| **Learner model** | Optional | Full | Relevant | Relevant | Full |
| **Curriculum discovery** | Off | Full | Source-bound | Limited | Off |
| **Claim verification** | Selective | Full | Full | Relevant | Selective |
| **Example engineering** | Light | Full | Permission-bound | Full | Relevant |
| **Consistency ledger** | Off | If bundled | If bundled | If bundled | If multi-note |
| **Educational editing** | Light | Full | Full | Full | Relevant |
| **Mastery design** | Off | If applicable | Permission-bound | Transfer only | Full |
| **Retention** | Off | Optional | Optional | Off | Full |

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
