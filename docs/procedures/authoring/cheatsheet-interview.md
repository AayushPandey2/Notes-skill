# Companion Cheatsheet & Interview / Viva Pack (File 3)

Emit this sibling file (`<note stem> - Cheatsheet & Interview Q&A.md`) only when `mastery_pack` is included in the resolved `artifact_plan` ([adaptive-engine.md](adaptive-engine.md)), governed by `artifact_policy` and `source_constraints` in [master-registry.yaml](../../dispatch/master-registry.yaml) (default for `M1`/`M2` unless `explicit_single_file`, an existing layout, or restrictive `strict` source constraints forbidding unsupported outside additions override it; exempting `M3`, `M4`, `M6`, `M7`, `/scribe-ytnotes`, MOCs, and standalone `M5`). Link generated companions reciprocally, match the active YAML profile ([properties-policy.md](../../properties/properties-policy.md)), and preserve identical notation and source limits across the bundle.

## Required Structure of File 3 (Subject-Adaptive)

Open with line-1 YAML frontmatter matching the active profile, a discipline-appropriate H1 (`# <Topic> — Cheat Sheet, Interview Q&A & Practice` for technical/engineering topics, or `# <Topic> — Reference Sheet, Viva & Critical Thinking Pack` for humanities/natural sciences), and a concise navigation callout linking `[[<Parent Note>]]` and `[[<Parent Note> - Experimental Lab]]` (only linking existing/generated files). Do **not** duplicate long prose derivations from File 1; keep File 3 dense, scannable, and self-testing.

### Section 1 — Subject-Adaptive Reference & Formula / Rule Sheet
| Subject | Reference Sheet Focus | Applied Problems Focus |
|---|---|---|
| **ML / DL / GenAI** | Objectives, architectures, gradients/updates, evaluation & stability | Model calculations, metric trade-offs & failure diagnosis |
| **DSA / Programming** | Invariants, complexity, APIs, memory/state rules | Tracing, correctness proofs & debugging |
| **Full-Stack / Systems** | Protocols, APIs, request lifecycle, schemas, design rules | System design, request tracing & debugging |
| **Cybersecurity** | Security properties, trust boundaries, defensive controls | Root-cause analysis & defensive verification |
| **Electrical** | Circuit laws, component models, transfer & timing rules | Circuit calculations, transient/AC analysis & fault diagnosis |
| **Mathematics / Stats** | Definitions, theorems, identities, conditions & cues | Proofs, calculations & assumption checks |
| **Physics / Chemistry** | Governing laws, units, reaction/equilibrium conditions | Physical modeling, stoichiometry & validity checks |
| **Biology** | Structures, pathways, regulation & experimental models | Mechanism tracing, data interpretation & disruption analysis |
| **History / Humanities** | Chronology, key actors/concepts, arguments & interpretations | Primary-source evaluation, argument critique & comparison |

- Present table-friendly rules in two-column `Concept | Formula / Rule` tables (using `$...$` inline math, escaping literal pipes, stating units/conditions).
- Display multi-line reasoning in separate-line `$$...$$` blocks. Link to canonical derivations in compact references and show needed transformations directly inside worked answers ([math_gates.md](../../../core/math_gates.md)).

### Section 2 — Tiered Interview / Viva Questions & Answers (Tap-to-Reveal)
Default to **30 high-yield questions** for comprehensive topics (scaling count naturally to actual topic scope), sampling across the ten mastery dimensions in [mastery-design.md](mastery-design.md) (`Recognition`, `Explanation`, `Prediction`, `Diagnosis`, `Discrimination`, `Critique`, `Transfer`, etc.), and **compute tier headings dynamically** to match the actual question count:
- `### Beginner-Level Questions (Q1–Q<n1>)`
- `### Intermediate-Level Questions (Q<n1+1>–Q<n2>)`
- `### Advanced-Level Questions (Q<n2+1>–Q<N>)`

**Mandatory Collapsible Answer Rule:** Quote **every** interior line inside `> [!success]- Answer` (including blank lines and `$$...$$` blocks with `>`) and leave an unquoted blank line before the next question:

````markdown
**Q<k>. <Clear, specific interview or viva question>**

> [!success]- Answer
> <Direct, technically precise answer with intuition, equations, or edge-case reasoning.>
````

### Section 3 — Applied Practice Problems with Worked Solutions (Tap-to-Reveal)
Provide **4–6 domain-appropriate applied problems** when source permissions permit (under `strict` source mode, include only problems supported by the supplied material rather than inventing outside exercises—matching the Applied Problems Focus table above; never force ML loss/threshold templates onto unrelated disciplines):
- State **Given / Context** and exact task visibly under `### Problem <k>: <Title>`.
- Place the complete step-by-step reasoning, final result (boxed when numeric), and independent verification check inside `> [!success]- Solution`.

*Review against [verification-checklist.md](../review/verification-checklist.md) for collapsed `> [!success]-` prefixes, quoted interior lines, compatible delimiters, and notation alignment.*
