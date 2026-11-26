# Knowledge Consistency & Shared Collection Ledger

## Purpose

Maintain strict symbol, convention, fixture, and concept-ownership consistency across **3-file topic bundles** (Theory, Lab, Mastery) and **multi-chapter collections** without creating extra generated files.

## Internal Collection & Bundle Ledger

Track these four fields internally inside the [shared concept plan](adaptive-engine.md) during multi-file or multi-chapter authoring (never publish the raw ledger as YAML or clutter):

1. **Notation & conventions:** Fixed symbol meanings (e.g., $m$ samples, $n$ features, $X$ matrix, $\mathbf{y}$ target, $\mathbf{w}, b$ parameters; or passive sign convention in circuits).
2. **Canonical definitions & objective scaling:** Single authoritative home for each definition/objective (e.g., if Theory defines MSE with $\frac{1}{m}$, Lab must not silently switch to half-MSE $\frac{1}{2m}$ without explicitly stating the factor conversion).
3. **Shared fixtures:** Reuse named running fixtures across Theory, Lab, and File 3 where continuity helps, declaring any intentional stress/evaluation fixture separately.
4. **Concept ownership & chapter boundaries:** Record which chapter owns each concept's full explanation so later chapters link back (`[[03 - Gradient Descent]]`) instead of re-deriving or drifting.

## Cross-Artifact Consistency Check

Before finalizing a bundle or collection, verify that Theory, Lab, and Mastery share identical definitions, symbol meanings, objective/hyperparameter scaling, and applicability conditions—or explicitly explain any deliberate convention shift (such as a library's `C = 1 / alpha`).
