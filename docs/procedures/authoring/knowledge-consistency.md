# Knowledge Consistency & Shared Collection Ledger

## Purpose

Maintain strict symbol, convention, shared worked-example, and concept-ownership consistency across every artifact included in the resolved **`artifact_plan`** ([adaptive-engine.md](adaptive-engine.md)—covering single-note updates, multi-file topic bundles, and multi-chapter collections) without creating extra generated files.

## Collection-Level Ledger (Not Per-Concept)

Maintain this ledger once at the **collection/bundle level** inside the [hierarchical plan](adaptive-engine.md)—never repeat it per concept and never publish the raw ledger as YAML clutter:

1. **Notation & conventions (with explicit scopes):** Distinguish five notation scopes rather than forcing one brittle global rule across unrelated fields:
   - *Collection-wide conventions* (shared across chapters in one bundle/topic, e.g., $m$ samples, $n$ features, or passive sign convention in circuits)
   - *Chapter-level conventions* (intentional shifts between modules, e.g., $n$ as sample size in statistics vs. vector-space dimension in linear algebra)
   - *Local mathematical symbols* (dummy indices or temporary proof variables)
   - *Source-specific conventions* (`M2` faithfully preserving a lecture's symbols)
   - *Library-specific parameter names* (API names mapped explicitly back to canonical equations)
   Whenever a convention changes across scope boundaries, bridge the transition explicitly so no symbol is ambiguous inside its reasoning context.
2. **Canonical definitions & objective scaling:** Single authoritative home for each definition/objective (e.g., if Theory defines MSE with $\frac{1}{m}$, Lab must not silently switch to half-MSE $\frac{1}{2m}$).
3. **Shared worked examples:** Reuse named running examples across active `artifact_plan` roles (`theory`, `experimental_lab`, `mastery_pack`, or multi-chapter chapters) where continuity helps, declaring any stress or edge-case example separately.
4. **Concept ownership & chapter boundaries:** Record which chapter owns each concept's full explanation so later chapters link back (`[[03 - Gradient Descent]]`) instead of re-deriving or drifting.

## Objective-Level Equivalence & Cross-Artifact Check

Never assume generic parameter conversion shortcuts (such as `C = 1 / alpha`) hold universally. Parameter translations depend on the **exact objective normalization, penalty definition, intercept treatment, and solver**—establish objective-level equivalence explicitly before translating hyperparameters (for instance, comparing $J_1(\mathbf{w}) = \frac{1}{2m}\|X\mathbf{w}-\mathbf{y}\|^2 + \frac{\lambda}{2}\|\mathbf{w}\|^2$ against $J_2(\mathbf{w}) = \frac{1}{2}\|X\mathbf{w}-\mathbf{y}\|^2 + \frac{\alpha}{2}\|\mathbf{w}\|^2$ gives equivalent minimizers at $\alpha = m\lambda$, not $\alpha = \lambda$).

## Artifact-Interface Contracts (Resolved `artifact_plan` Roles)

Align coverage cleanly across whichever roles are included in the resolved `artifact_plan` (supporting single notes, partial bundles, strict-source suppression, video notes, standalone assessments, and multi-chapter collections without assuming fixed three-file bundles):
- **`theory` (or `video_note`/`synthesis`):** Explains and establishes mechanisms, definitions, assumptions, and conceptual transitions.
- **`experimental_lab`:** Realizes, computes, traces, and investigates the same mechanism under stated inputs and parameters.
- **`mastery_pack` (or `assessment`):** Tests recognition, diagnosis, edge cases, and transfer aligned to the taught objectives without disconnected trivia or verbatim derivations.
Verify before acceptance that included practical/mastery artifacts align cleanly with `theory` in notation, objective scaling, and validity conditions.

## Claim Propagation & Defect Tracking

Whenever a canonical claim, assumption, counterexample, or defect is established or repaired (for example, clarifying that raising a classification threshold does *not* monotonically guarantee higher precision), trace and update **every dependent occurrence** across Theory explanatory prose, Lab traces and explanations, Cheatsheet summary rows, Interview Q&A answers, and related Quiz/Revision prompts—preserving productive retrieval repetition without propagating conflicting claims.
