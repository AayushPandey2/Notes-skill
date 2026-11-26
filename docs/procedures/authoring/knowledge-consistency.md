# Knowledge Consistency & Shared Collection Ledger

## Purpose

Maintain strict symbol, convention, fixture, and concept-ownership consistency across **3-file topic bundles** (Theory, Lab, Mastery) and **multi-chapter collections** without creating extra generated files.

## Collection-Level Ledger (Not Per-Concept)

Maintain this ledger once at the **collection/bundle level** inside the [hierarchical plan](adaptive-engine.md)—never repeat it per concept and never publish the raw ledger as YAML clutter:

1. **Notation & conventions:** Fixed symbol meanings (e.g., $m$ samples, $n$ features, $X$ matrix, $\mathbf{y}$ target, $\mathbf{w}, b$ parameters; or passive sign convention in circuits).
2. **Canonical definitions & objective scaling:** Single authoritative home for each definition/objective (e.g., if Theory defines MSE with $\frac{1}{m}$, Lab must not silently switch to half-MSE $\frac{1}{2m}$).
3. **Shared fixtures:** Reuse named running fixtures across Theory, Lab, and File 3 where continuity helps, declaring any intentional stress/evaluation fixture separately.
4. **Concept ownership & chapter boundaries:** Record which chapter owns each concept's full explanation so later chapters link back (`[[03 - Gradient Descent]]`) instead of re-deriving or drifting.

## Objective-Level Equivalence & Cross-Artifact Check

Never assume generic parameter conversion shortcuts (such as `C = 1 / alpha`) hold universally. Parameter translations depend on the **exact objective normalization, penalty definition, intercept treatment, and solver**—establish objective-level equivalence explicitly before translating hyperparameters (for instance, comparing $J_1(\mathbf{w}) = \frac{1}{2m}\|X\mathbf{w}-\mathbf{y}\|^2 + \frac{\lambda}{2}\|\mathbf{w}\|^2$ against $J_2(\mathbf{w}) = \frac{1}{2}\|X\mathbf{w}-\mathbf{y}\|^2 + \frac{\alpha}{2}\|\mathbf{w}\|^2$ gives equivalent minimizers at $\alpha = m\lambda$, not $\alpha = \lambda$). Before finalizing a bundle or collection, verify that Theory, Lab, and Mastery match across definitions, symbols, objective scaling, and applicability conditions.
