# Companion Implementation Lab Contract

For each newly generated **substantive non-video learning note** (`M1` deep-notes, `M2` study-notes, and `M5` implementation-guides—unless the user explicitly requests a single file), create or update a **3-file topic bundle**: the content note (`<note stem>.md`), its sibling `<note stem> - Experimental Lab.md`, and its sibling `<note stem> - Cheatsheet & Interview Q&A.md` ([cheatsheet-interview.md](cheatsheet-interview.md)). **Explicit exemptions (no companions generated unless explicitly requested):** compact/retrieval masters (`M3` quick-reference and all its presets: `atomic-card`, `formula-sheet`, `syntax-reference`, `command-reference`, `quick-summary`), standalone assessments (`M6`, `flashcards`, `mock-exam`), standalone worked problem sets (`M4`) or standalone syntheses/comparisons (`M7`), `/scribe-ytnotes` video notes, playlist indexes, MOCs, labs, cheatsheet packs, and internal workflow documents; never create companions retroactively across a vault. Link all three files reciprocally, share the active YAML profile (following the profile-specific alignment rules in [properties-policy.md](../../properties/properties-policy.md)), and keep definitions, symbols, datasets, assumptions, and conventions strictly consistent with the parent note.

## Lean Implementation-Focused Structure

Replace long multi-chapter experimental labs with a focused, implementation-first document. **Do not** include standalone sections for:

- Opening metadata inventories (`Level`, `Prerequisites`, `Languages`, `Libraries`, `Objectives`).
- Repeated theory chapters (theory lives in `<note stem>.md`).
- Historical background or general experimental investigations.
- Professional-workflow chapters (e.g., 12-step project walkthroughs or hyperparameter sweeps).
- Quiz and challenge chapters, learning roadmaps, repository-structure recommendations, or repetitive final summaries.

Do not recreate removed chapters under different names. Retain **only**:

1. **Title and parent-note navigation:** Line-1 YAML frontmatter, `# <Topic> — Implementation Lab`, and a concise navigation callout linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.
2. **Brief shared problem and I/O contract:** State the central task, dataset/inputs, target, objective scaling, intercept/regularization conventions, prediction meaning, and comparison criteria shared across the tracks.
3. **Relevant implementation / practical tracks (Universal 4-Perspective Architecture):**
   - **Machine Learning:** Retain the **4 comparable Python/Rust tracks** (Python + NumPy, Python libraries, Rust from scratch, Rust using Linfa or SmartCore) per [machine-learning.md](../../blueprints/investigations/machine-learning.md), unless the user requests specific languages or fewer tracks, integrating controlled investigation and verification inside their walkthroughs. Treat multi-track implementations as statically reviewed educational references—verify API signatures against official docs and numerical alignment via hand-traced dry runs, never claiming compiled or runtime-verified parity.
   - **All other disciplines:** Use the matching blueprint under `docs/blueprints/investigations/` (`deep-learning.md`, `coding.md`, `algorithms.md`, `fullstack.md`, `cybersecurity.md`, `electrical.md`, `operating-systems.md`, `networking.md`, `databases.md`, `devops.md`, `distributed-systems.md`, `generative-ai.md`, `mathematics.md`, `statistics.md`, `physics.md`, `chemistry.md`, `biology.md`, or `general.md`), structured around **Four Universal Practical Perspectives** with a **track-applicability gate** (use all 4 when each adds distinct educational value for comprehensive topics; use the meaningful subset for narrower concepts, and **never** force irrelevant programming tracks, ML splits, or wet-lab claims):
     - **Track 1 — First principles:** Reconstruct the central mechanism manually or from scratch.
     - **Track 2 — Standard method:** Apply the established tool, library, framework, procedure, or formal technique.
     - **Track 3 — Controlled investigation:** Vary inputs, parameters, constraints, or assumptions to examine behavior.
     - **Track 4 — Verification and failure analysis:** Independently check results, edge cases, tolerances, and breakdown regimes.
4. **Setup beside each track:** Show necessary dependencies, versions, or `Cargo.toml` manifests as Markdown learning material directly beside each track, with a proportionate collapsed explanation beneath supporting blocks.
5. **Complete code:** Place complete implementations inside properly formatted Markdown code fences (never create Python files, Rust projects, scripts, downloaders, builders, or validators).
6. **Immediately following collapsed explanations:** Directly beneath every implementation's code block, include:

```markdown
> [!example]- Understand this implementation: mathematics, code, and numerical dry run
> ...
```

7. **Brief, accurate verification status:** Any displayed `$$...$$` equation in a lab follows [math_gates.md](../../../core/math_gates.md) (native delimiters, blank lines, consistent objective scaling, and `> [!example]- Understand this formula step by step` beneath displayed blocks). End every lab containing code with:

**`Source and static review only; not compiled or executed here.`**

Integrate essential examples, comparisons, limitations, and checks directly into the collapsed explanations rather than separate chapters.

## Generalized Collapsed Walkthrough Standard (A–G)

Keep the full realization (code, derivation, physical/circuit model, security analysis, or evidence trace) visible before its walkthrough. Inside `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` (or `> [!example]- Understand this realization: <domain focus> and dry run` for non-code disciplines), quote **every** line—including blank lines—with `>` so Obsidian keeps the entire walkthrough inside one collapsed callout. Supporting blocks (imports, `pip install`, `Cargo.toml`) receive a proportionate collapsed explanation directly beneath them rather than repeating an entire long walkthrough.

Every full walkthrough covers **A through G** adapted naturally to the discipline:

- **A. Setup and inputs:** Define objects, materials, variables, shapes/types/units, assumptions, environment, and success criteria using one consistent shared fixture/system.
- **B. Governing mechanism:** Explain the principle, invariant, law, security property, or mathematical objective (including objective scaling or library parameter conversions where applicable) that determines the outcome.
- **C. Execution:** Trace each meaningful line, logical step, physical/circuit law, or procedural operation in execution order (quoting code expressions when code is present, explaining syntax, entering state, internal operation, and state change).
- **D. Complete trace:** Follow one concrete example through all important intermediate states (`Initialization → forward/update/state transition → output`, hand-calculated arithmetic, logical proof transitions, or evidence chain), explicitly qualifying miniature-fixture simplifications.
- **E. Interpretation:** Explain the returned output, physical/system behavior, or conclusion and what it establishes—and does **not** establish.
- **F. Failure analysis:** Cover invalid inputs, violated assumptions, unstable numerics, wrong operators, fault conditions, or security/logical errors using: **Problematic approach → failure mechanism → correction → explanation.**
- **G. Reconstruction:** Finish with a concise plain-language sequence enabling the learner to reproduce the reasoning independently.

## Experiment Integrity & Static Correctness Gate

Distinguish result status explicitly in every lab—**never** present expected program output, synthetic calculations, fictional apparatus readings, or invented simulation results as observed or executed evidence:

| Result Status | Meaning |
|---|---|
| **Analytical** | Derived mathematically from stated assumptions |
| **Hand-calculated** | Computed manually using stated values |
| **Illustrative** | Constructed miniature example for teaching |
| **Expected** | Predicted behavior from static code/circuit analysis, not observed |
| **Published** | Reported by an identified external source |
| **Observed** | Actually supplied by a performed investigation or user |
| **Executed** | Produced by a verified execution environment |
| **Unverified** | Not independently confirmed |

Never execute code, compile Rust, run Cargo, install dependencies, probe local runtimes, or create executable scripts/projects. Review every displayed realization statically before finalizing:

1. **Operators:** Check every `*` vs `@`, `**` vs `^`, matrix vs element-wise operations, integer vs floating-point division, and logical vs bitwise operators based on types, shapes, and mathematics.
2. **Gradients, Updates & Objective Scaling:** Check signs, averaging factors, transposes, bias updates, penalty gradients, threshold scaling, update ordering, stopping criteria, zero-denominator cases, and library hyperparameter conversions (`C`, `alpha`, `penalty`). Choose optimizers honestly (never force gradient descent onto coordinate-descent, proximal, tree, nearest-neighbor, or quasi-Newton methods).
3. **Implementation Completeness:** Check syntax, indentation, imports, defined variables, consistent naming, input/output shapes, official versioned API consistency, dependencies, bounds, empty inputs, and numerical guards using hand calculations where feasible. Never copy `"Expected output"` from unexecuted references as verified output.
