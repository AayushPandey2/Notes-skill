# Companion Experimental Lab Contract

Emit this sibling file (`<note stem> - Experimental Lab.md`) only when dictated by `artifact_policy` and `source_constraints` in [master-registry.yaml](../../dispatch/master-registry.yaml) (default for `M1`/`M2` unless `explicit_single_file`, an existing layout, or `strict` source constraints forbidding unsupported outside labs override it; exempting `M3`, `M4`, `M6`, `M7`, `/scribe-ytnotes`, MOCs, and avoiding duplicating an `M5` implementation guide). Link generated companions reciprocally, follow the active YAML profile in [properties-policy.md](../../properties/properties-policy.md), and keep definitions, symbols, and source limits consistent with the parent note.

## 1. Shared Structure & Lean Discipline-Independent Contract

**Do not** include standalone chapters for bloated metadata inventories, repeated theory chapters, historical background, generic project workflows, quizzes, roadmaps, or repetitive final summaries. Retain **only**:

1. **Header & Navigation:** Line-1 YAML frontmatter matching the parent note's profile, `# <Topic> — <Domain> Lab`, and a concise navigation callout linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]` (only linking existing/generated companions).
2. **Shared Problem & Reproducibility Contract:** State once (without repeating across tracks):
   - *Learning objective* (what the practical realization establishes)
   - *Fixture / system & inputs* (reusable miniature data, apparatus/circuit, schema, or primary evidence + initial conditions)
   - *Preconditions & governing mechanism* (validity assumptions, law, invariant, or procedure)
   - *Observable outcome & verification method* (expected result and how it is checked)
   - *Compact reproducibility block (when code/simulation/config appears):* environment/version/dialect, dependencies, block placement, expected behavior, learner execution instructions, and unverified environment limitations.
3. **Practical Realizations (Four Universal Coverage Obligations):** Load the matching investigation profile under `docs/blueprints/investigations/`. Use the four universal perspectives—**First principles**, **Standard method**, **Controlled investigation**, and **Verification & failure analysis**—as **coverage obligations** (domain tracks may appear in any order and combine perspectives; merge tracks if two realizations would merely repeat the same operations; use the meaningful subset for narrow topics).
4. **Setup & Complete Artifacts:** Place dependencies/manifests beside the track that needs them and place any code/configs inside Markdown fences (never create scripts, projects, or execute code on the host).

## 2. Shared Foundation + Track-Specific A–G Walkthroughs

Keep essential interpretation visible in prose and place extended trace/derivation detail inside `> [!example]- Understand this realization: <focus> and dry run` (or `...implementation: ...` for code), quoting **every** interior line—including blank lines—with `>`.

- **Avoid cross-track repetition:** Explain the shared fixture, initial conditions, governing model, and notation **once** in the Shared Contract or Track 1. Subsequent tracks reference that shared foundation and focus on *what the new method changes*, *the new trace*, and *method-specific failures*.
- **A–G Responsibilities:** **A** Setup & inputs · **B** Governing mechanism · **C** Execution / step-by-step operations · **D** Complete concrete trace · **E** Interpretation & limits · **F** Failure analysis (**Problematic approach $\to$ failure mechanism $\to$ correction $\to$ explanation**) · **G** Plain-language reconstruction.

## 3. Three-Attribute Experiment Integrity & Static Review Gate

Never present predicted outputs, synthetic calculations, or fictional apparatus readings as observed or executed evidence. Track and render three independent attributes naturally in prose (e.g., *"These values are hand-calculated predictions for an illustrative fixture; the implementation has not been executed."*):

| Attribute | Values |
|---|---|
| **Origin** | `user-supplied`, `published`, `synthetic`, `author-derived` |
| **Method** | `analytical`, `manual_arithmetic`, `simulation`, `measurement`, `execution` |
| **Verification** | `independently_checked`, `statically_reviewed`, `unverified`, `actually_executed` |

Verification status must record **what actually occurred** during authoring/review rather than being preset automatically by an investigation blueprint (only mark `independently_checked` when an independent check actually happened). Never execute code, compile projects, or probe local runtimes. Statically verify syntax, imports, bounds, edge cases, official versioned APIs (when permitted by `source_policy`), and equations ([math_gates.md](../../../core/math_gates.md)). End labs containing code or simulation netlists with **`Source and static review only; not compiled or executed here.`** (or the matching analytical/manual review statement for non-code labs).
