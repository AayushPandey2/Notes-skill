<!-- scaffold:preflight
Decision-Matrix Pre-Flight: [note_decision_matrix.md](../shared/note_decision_matrix.md) & [notes_decision_matrix.md](../shared/notes_decision_matrix.md).
Switches: D01 route (`deepstudy-master`); D02 scope (`DM-01`); D03 reader (`DM-02`); D04 track/outcome (`DM-03`); D05 sources (`DM-05`);
D06–D09 `math_level` 0–3 & calculus (`DM-06`–`DM-09`); D10 running fixture & actual topology (`DM-11`); D11 visual (`DM-13`);
D12–D13 verification stack & checks (`DM-14`–`DM-18`); D14 optional modules (`memory`, `history`, `operations` via `DM-19`); D15 audit (`DM-20`).
Strip this block before emission. Load detailed DM branches only when active.
-->

# Adaptive Deep Study Master

This is the canonical deep-study template. The companion [notes_decision_matrix.md](../shared/notes_decision_matrix.md) is the single authority for section selection and depth. Follow the [authoring rules](../shared/authoring_rules.md), [math gate](../shared/math_gates.md), and applicable [footer widgets](../shared/footer_widgets.md). Use the [routing index](../shared/note_decision_matrix.md) to select relevant branches and complete its [decision record](../shared/notes_decision_matrix.md#decision-record) before drafting each note. The former coding/general names are compatibility links to this pair.

This is an authoring specification, not text to paste wholesale into a finished note. The stable core is a single concise opening (**Core Model, Scope & Historical Context**, without repeating the thesis across separate intro/motivation blocks), followed by precise explanation to meet the outcome. Use **domain-natural headings** matching the topic's track (never CS/architecture buzzwords like *"Computational Purpose"*, *"Position in the Broader Architecture"*, *"Deep Theory Stack"*, or *"Cross-Architecture Trade-Off"* on non-software subjects). Strip all `<!-- SECTION: S* -->` markers, authoring gates, and unused headings before publication. Renumber retained inquiry headings after omission and repair local links.

Routing dimensions are independent. A systems note may need proof-level mathematics; an algorithm note may stop at pseudocode; a conceptual note may need quantitative evidence. Prefer depth at the point of difficulty over adding modules. These two canonical files supersede legacy deep-study section quotas, math gates, implementation defaults, and mandatory footer widgets. Other template families keep their own contracts.

## 1. What am I studying and for whom? (Metadata and Routing)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-01](../shared/notes_decision_matrix.md#dm-01), [DM-02](../shared/notes_decision_matrix.md#dm-02), [DM-03](../shared/notes_decision_matrix.md#dm-03), [DM-04](../shared/notes_decision_matrix.md#dm-04), [DM-05](../shared/notes_decision_matrix.md#dm-05), [DM-07](../shared/notes_decision_matrix.md#dm-07), [DM-14](../shared/notes_decision_matrix.md#dm-14).
> - **Include when:** Always make the routing decision; publish metadata only for identity, discovery, or an actual vault workflow.
> - **Adapt when:** Keep the seven planning axes in the decision record. In this repository, retain the existing five YAML keys: `id`, `aliases`, `topic`, `tags`, `nexttopics`; put the actual topic in the H1.
> - **Omit or link when:** Keep the authoring record outside the finished note unless the reader needs a decision rationale. Outside this repository, use the vault's schema; omit unsupported metadata fields.
> - **Quality check:** Are reader, outcome, scope, track, research need, math depth, and code depth chosen separately? Are retained IDs stable and tags meaningful?
> - **Duplication check:** Store routing reasons once in the record; reader-facing boundaries belong in Scope below.

Preserve an existing note's identity and useful metadata. Record actual values, not alternatives separated by pipes or template tokens. Do not add a blanket “verified” status when only part of the note was checked.

## 2. What is the central idea? (Core Model)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-03](../shared/notes_decision_matrix.md#dm-03), [DM-04](../shared/notes_decision_matrix.md#dm-04), [DM-20](../shared/notes_decision_matrix.md#dm-20).
> - **Include when:** The reader needs orientation before the details: what the object is, its essential relationship, and what it enables.
> - **Adapt when:** Use a causal model for mechanisms, a central proposition for mathematics, or the organizing question for surveys and maps.
> - **Omit or link when:** Merge with Intuition and precise definition if a separate summary would merely repeat it.
> - **Quality check:** Does this make a useful prediction or distinction without overstating a guarantee?
> - **Duplication check:** Keep equations at their explanatory home; do not add a second equation preview or closing paraphrase.

Give the reader a short organizing model in plain language. Do not invent an invariant for a topic whose useful structure is a taxonomy, argument, or observation.

## 3. What must I know and be able to do? (Scope and Outcomes)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-01](../shared/notes_decision_matrix.md#dm-01), [DM-02](../shared/notes_decision_matrix.md#dm-02), [DM-03](../shared/notes_decision_matrix.md#dm-03).
> - **Include when:** Ambiguity about the topic, reader baseline, or intended capability would change the explanation.
> - **Adapt when:** Explain essential missing foundations locally for beginners; refresh or link for familiar readers; state conventions for reference readers. Maps emphasize dependency order.
> - **Omit or link when:** Fold a simple outcome into the opening; move substantial prerequisite lessons to existing notes and state the exact skill needed from each.
> - **Quality check:** Can the reader perform the stated task using this note and its available prerequisites? Is the excluded scope explicit where confusion is likely?
> - **Duplication check:** Define each term at first meaningful use; this section names prerequisites without recreating a glossary.

State the bounded question, an observable outcome, and only the dependencies actually used. Distinguish explain, calculate, derive, implement, choose/design, verify, and debug. Do not silently promote an inference lesson into a training lesson.

## 4. What problem makes this useful? (Motivation)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-03](../shared/notes_decision_matrix.md#dm-03), [DM-05](../shared/notes_decision_matrix.md#dm-05), [DM-19](../shared/notes_decision_matrix.md#dm-19).
> - **Include when:** A concrete need, bottleneck, or question explains why the mechanism or distinction exists.
> - **Adapt when:** Use a mathematical question, engineering constraint, conceptual confusion, or task baseline; include history only if chronology changes understanding and is sourced.
> - **Omit or link when:** The opening already establishes the problem; link a separate historical account if provenance is outside the outcome.
> - **Quality check:** Is the limitation of a simpler approach real under stated conditions? Are historical or empirical claims supported?
> - **Duplication check:** Introduce the problem here; detailed alternative selection belongs in Alternatives and selection.

Explain the need without inventing an origin story or claiming the technique is universally necessary.

## 5. What does it mean precisely? (Intuition and Definition)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-02](../shared/notes_decision_matrix.md#dm-02), [DM-04](../shared/notes_decision_matrix.md#dm-04), [DM-12](../shared/notes_decision_matrix.md#dm-12).
> - **Include when:** The central term, object, relation, or contract must be established before reasoning about it.
> - **Adapt when:** Start with an accessible case for beginners or the exact definition for advanced readers; give a positive case and a near miss if membership is easily confused.
> - **Omit or link when:** Merge with Core model or Formal model if the definition already lives there; link an established definition with a short local reminder.
> - **Quality check:** Is intuition consistent with the exact definition, including the conditions that distinguish nearby concepts?
> - **Duplication check:** Give the authoritative definition once; later sections apply it rather than restating it.

### Analogy

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-12](../shared/notes_decision_matrix.md#dm-12), [DM-20](../shared/notes_decision_matrix.md#dm-20).
> - **Include when:** A familiar relationship makes a specific unfamiliar operation easier to predict.
> - **Adapt when:** Map only corresponding parts and immediately identify the inference that stops being valid.
> - **Omit or link when:** A direct example is clearer, or the analogy needs more repair than explanation; omit this subsection entirely.
> - **Quality check:** What exact relationship transfers, and what false prediction could this analogy cause?
> - **Duplication check:** Do not retell the whole worked example in metaphor; use a short paragraph if no separate heading is needed.

## 6. How does it work? (Mechanism)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-03](../shared/notes_decision_matrix.md#dm-03), [DM-04](../shared/notes_decision_matrix.md#dm-04), [DM-09](../shared/notes_decision_matrix.md#dm-09), [DM-11](../shared/notes_decision_matrix.md#dm-11), [DM-13](../shared/notes_decision_matrix.md#dm-13).
> - **Include when:** Understanding requires following relationships, operations, state changes, or a causal argument.
> - **Adapt when:** Use the topic's natural structure: stages, recurrence, state machine, components, proof dependencies, workflow, memory lifecycle, or data flow. A survey explains shared structure; a map links the mechanisms.
> - **Omit or link when:** A definition suffices or a worked trace already explains the complete mechanism; merge rather than create a second walkthrough.
> - **Quality check:** Can the reader explain why each consequential transition occurs and what assumptions make it valid? Are inputs, outputs, stopping conditions, and side effects stated where applicable?
> - **Duplication check:** Keep general rules here and concrete arithmetic in the example, unless teaching them together is clearer; then omit the separate example section.

Use meaningful invariants only where they apply. Discuss resource cost when it affects feasibility or selection, defining the input-size variables and cost model. No universal number of stages or compulsory complexity analysis.

### Visual explanation

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-11](../shared/notes_decision_matrix.md#dm-11), [DM-13](../shared/notes_decision_matrix.md#dm-13).
> - **Include when:** Spatial arrangement, branching, state, timing, or aligned differences are harder to understand from prose alone.
> - **Adapt when:** Select a flowchart, state diagram, tensor grid, search tree, timeline, or comparison table according to the relationship being taught.
> - **Omit or link when:** A visual adds no information; place it beside its actual explanatory home instead of maintaining this separate subsection.
> - **Quality check:** Are labels, direction, axes, units, and state meanings sufficient to read it? Does nearby text explain the relevant inference?
> - **Duplication check:** A visual may clarify a relationship; it should not duplicate an exhaustive trace or a second comparison table.

## 7. What does the formal model explain? (Mathematics)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-06](../shared/notes_decision_matrix.md#dm-06), [DM-07](../shared/notes_decision_matrix.md#dm-07), [DM-08](../shared/notes_decision_matrix.md#dm-08), [DM-09](../shared/notes_decision_matrix.md#dm-09).
> - **Include when:** Math defines the object or mechanism, predicts or quantifies behavior, supports a choice, or checks a result the reader needs.
> - **Adapt when:** Use structural/logical constraints, operational formulas, derivational development, or proof-level statements at the effective level in the saved contract. Use the domain ceiling and subtopic gate in DM-07.
> - **Omit or link when:** Equations add no explanatory or decision value; integrate a single useful relation into the mechanism or example, or link background theory.
> - **Quality check:** What question does each central equation answer? Are symbols, shapes, units, assumptions, domains, interpretation, and relevant checks supplied as needed?
> - **Duplication check:** Define and display each central relation once. Reference that equation from derivations, examples, and code instead of repeating a preview/table.

Apply DM-09's equation treatment. A forward pass or prediction trace needs no derivative calculation. Add calculus only after DM-08 selects a learning or verification purpose. Do not substitute a fixed set of zero, unit, tie, or infinite cases for domain-specific checks.

## 8. Why does the result follow? (Derivation or Proof)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-03](../shared/notes_decision_matrix.md#dm-03), [DM-07](../shared/notes_decision_matrix.md#dm-07), [DM-08](../shared/notes_decision_matrix.md#dm-08), [DM-10](../shared/notes_decision_matrix.md#dm-10).
> - **Include when:** Deriving a result or establishing a guarantee is itself an outcome, or the derivation resolves a central misconception needed for that outcome.
> - **Adapt when:** Show named-rule steps at M2, or a quantified theorem, complete proof and counterexample at M3. Calibrate calculus using DM-08.
> - **Omit or link when:** The reader only needs to apply the result; state its validity conditions and link its proof. An aligned chain with explicit justifications can live beside its governing equation.
> - **Quality check:** Are the target, assumptions, strategy, non-obvious steps, and conclusion justified? Is an approximation or one-way implication labeled? Is a numerical check clearly distinguished from proof?
> - **Duplication check:** Reference existing definitions and example inputs; do not rederive the same result in the implementation section.

## 9. How does a concrete case unfold? (Worked Trace)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-02](../shared/notes_decision_matrix.md#dm-02), [DM-09](../shared/notes_decision_matrix.md#dm-09), [DM-11](../shared/notes_decision_matrix.md#dm-11), [DM-18](../shared/notes_decision_matrix.md#dm-18).
> - **Include when:** A concrete case exposes a decision, intermediate state, calculation, or failure that a definition leaves obscure.
> - **Adapt when:** Trace values for numerical work, states for algorithms/systems, or evidence and distinctions for conceptual topics. Use independent examples when one fixture would distort a survey.
> - **Omit or link when:** The mechanism already contains the example or the example only substitutes obvious values; link a larger lab when it exceeds this note's outcome.
> - **Quality check:** Is the case small yet capable of exposing the intended behavior? Are setup, consequential intermediate results, final interpretation, and a relevant check present?
> - **Duplication check:** Establish shared inputs once and reuse them by reference in code/tests; add a second case only to teach a different behavior.

## 10. How do I implement or verify it? (Implementation)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-14](../shared/notes_decision_matrix.md#dm-14), [DM-15](../shared/notes_decision_matrix.md#dm-15), [DM-16](../shared/notes_decision_matrix.md#dm-16), [DM-17](../shared/notes_decision_matrix.md#dm-17), [DM-18](../shared/notes_decision_matrix.md#dm-18).
> - **Include when:** Code teaches operations, demonstrates a required interface/workflow, verifies a claim, or supports implementation/debugging as an outcome.
> - **Adapt when:** Select none, illustrative, from-scratch, standard library/framework, or production-oriented depth. Select the language and ML layers by what each teaches; pseudocode can be sufficient.
> - **Omit or link when:** Code repeats the explanation without new insight or a complete application belongs in a lab/repository. Do not force runnable code into an algorithmic or conceptual lesson.
> - **Quality check:** Is the purpose explicit? Does the fragment or runnable program fulfill it with understandable inputs/outputs and honest limits? Does every extra implementation have a distinct reason?
> - **Duplication check:** Keep one code home per teaching purpose. Refer to the equation, trace, and shared comparison contract rather than copying them.

State the selected tool and reason. Annotate shape, ownership, precision, or lifetime transitions only where they explain behavior or prevent a relevant error. Label toy/from-scratch examples as such; production-oriented treatment needs the actual task's operational constraints. For a dedicated implementation note, use the planned stack and apply the earlier trace's fixture. At M0 refer to the update or governing relation in the earlier note. Use a matched trade-off table when the stack has multiple entries.

### Verification and reproducibility

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-05](../shared/notes_decision_matrix.md#dm-05), [DM-17](../shared/notes_decision_matrix.md#dm-17), [DM-18](../shared/notes_decision_matrix.md#dm-18).
> - **Include when:** The reader must trust or reproduce a computation, implementation, empirical result, or diagnostic.
> - **Adapt when:** Use expected hand results, assertions, numerical checks, matched evaluation, or operational checks according to the claim. This subsection may move beside mathematics or evidence even if Implementation is omitted.
> - **Omit or link when:** There is no executable or empirical claim to verify (`language: "none"` omits code and all execution claims); for a required stack, use the exact status, version and output from the runtime report as described in DM-18.
> - **Quality check:** Are observed outputs verbatim stdout/stderr distinct from expected outputs? Are execution status, material versions, seeds, tolerances, boundary choices, and limitations accurate rather than inferred?
> - **Duplication check:** Put each assertion or check here or beside the relevant example/code, never in both places. Failure-mode entries point to the check.

## 11. Which alternative fits my constraints? (Selection)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-01](../shared/notes_decision_matrix.md#dm-01), [DM-03](../shared/notes_decision_matrix.md#dm-03), [DM-05](../shared/notes_decision_matrix.md#dm-05), [DM-19](../shared/notes_decision_matrix.md#dm-19).
> - **Include when:** The reader faces a real choice among methods, abstractions, configurations, or explanations.
> - **Adapt when:** Compare shared decision axes and constraints; a family note may make this its main structure. Source empirical rankings and current recommendations.
> - **Omit or link when:** There is no decision to make or an existing comparison answers it; retain only the relevant choice and link.
> - **Quality check:** Do the alternatives solve the same task under comparable conditions? Can the reader use the resulting conditional selection rule?
> - **Duplication check:** Keep the comparison here; the motivation needs only the motivating baseline, and failures need only additional diagnostics.

## 12. Where does it fail or stop applying? (Limits)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-05](../shared/notes_decision_matrix.md#dm-05), [DM-09](../shared/notes_decision_matrix.md#dm-09), [DM-18](../shared/notes_decision_matrix.md#dm-18), [DM-19](../shared/notes_decision_matrix.md#dm-19).
> - **Include when:** A plausible misconception, invalid assumption, operational failure, or evidence limitation materially changes the result or a decision.
> - **Adapt when:** Explain trigger, consequence, and a diagnostic/correction for code/systems; use a counterexample or scope restriction for mathematical/conceptual claims.
> - **Omit or link when:** The validity condition or failure is already explained next to its formula, transition, or test; link specialist troubleshooting beyond the scope.
> - **Quality check:** Is each retained case consequential and supported? Can the reader detect or avoid it, or understand the unresolved limitation?
> - **Duplication check:** Do not repeat equation boundaries, comparison trade-offs, and test cases in another catch-all table.

## 13. What supports these claims? (Evidence)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-05](../shared/notes_decision_matrix.md#dm-05), [DM-18](../shared/notes_decision_matrix.md#dm-18), [DM-20](../shared/notes_decision_matrix.md#dm-20).
> - **Include when:** External claims, source synthesis, empirical results, historical attribution, or version-dependent behavior need traceability.
> - **Adapt when:** Cite beside claims; add a source-to-claim list or table only when it helps inspect several sources. Record relevant section/page, version/date, scope, and access status.
> - **Omit or link when:** No external claim needs sourcing, or inline citations already supply complete support; omit a redundant bibliography, not necessary attribution.
> - **Quality check:** Was the supporting passage actually inspected? Does it support the exact claim? Are source observations, own measurements, inference, and unverified statements distinguished?
> - **Duplication check:** Keep full source details in one place and use precise nearby links; do not reproduce a research dossier or inaccessible-source filler rows.

## 14. Can I use and connect this knowledge? (Recall)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-03](../shared/notes_decision_matrix.md#dm-03), [DM-20](../shared/notes_decision_matrix.md#dm-20).
> - **Include when:** Retrieval, transfer, a genuine unresolved question, or a next-note relationship helps the reader use the note.
> - **Adapt when:** Choose questions matching the outcome; an advanced reference may need only an index link. Use the subsections below independently.
> - **Omit or link when:** There is no added retrieval or navigation value; link an existing practice set instead of duplicating it.
> - **Quality check:** Does the ending help the reader do something beyond rereading the opening?
> - **Duplication check:** Keep takeaway cues brief and point to explanations already present.

### Recall and transfer

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-03](../shared/notes_decision_matrix.md#dm-03), [DM-20](../shared/notes_decision_matrix.md#dm-20).
> - **Include when:** A question can test the intended explanation, calculation, derivation, implementation, choice, verification, or diagnosis.
> - **Adapt when:** Cap to **2–3 high-signal, non-overlapping questions** (core mechanism, quantitative trace, and optional boundary/adversarial edge case). Change one meaningful condition or ask for a justified decision; supply an answer/check where self-study needs it. Optional hidden answers use `> [!example]- Answer`, with every answer line quoted.
> - **Omit or link when:** Questions merely repeat definitions or are already in a useful practice set.
> - **Quality check:** Is the answer supported by the note, and does the question test understanding rather than an arbitrary detail?
> - **Duplication check:** Reference the main explanation; do not copy its whole derivation into an answer.

### Takeaways, open questions, and next-note connections

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-01](../shared/notes_decision_matrix.md#dm-01), [DM-05](../shared/notes_decision_matrix.md#dm-05), [DM-20](../shared/notes_decision_matrix.md#dm-20).
> - **Include when:** A retrieval cue, unresolved uncertainty, or specific dependency/extension deserves explicit follow-up.
> - **Adapt when:** Include only the useful items; distinguish a real open question from material merely deferred by scope.
> - **Omit or link when:** There is no unresolved issue or meaningful next step; do not fabricate confusion or force a review widget.
> - **Quality check:** Does each connection explain why to follow it, and does its target exist? Is any unknown clearly labeled?
> - **Duplication check:** Reuse the existing core model and prerequisite links; do not add a second summary or link list without a new purpose.


<!-- optional: memory -->
## [OPTIONAL] How do layout and allocation change performance? (Hardware, Memory Layout & Systems Performance Profile)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-18](../shared/notes_decision_matrix.md#dm-18), [DM-19](../shared/notes_decision_matrix.md#dm-19).
> - **Include when:** Low-level systems, C++/Rust, or ML kernel topics where memory layout, strides, alignment, cache locality, ownership, or device transfers materially drive performance; D04, D10–D14.
> - **Adapt when:** Use only constraints relevant to the selected track and outcome.
> - **Omit or link when:** Already explained elsewhere or outside scope; delete the heading and renumber retained sections.
> - **Quality check:** Does this change a decision or expose a consequential failure?
> - **Duplication check:** Link the existing explanation rather than repeating math, code or measurements.

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Low-level systems, C++/Rust, or ML kernel topics where memory layout, strides, ownership, cache behavior, or device transfers drive performance; D04, D10–D14.
- When to Omit Cleanly: Delete this heading and block completely if hardware/memory layout does not change understanding or decisions; never emit N/A; renumber retained headings sequentially.
- What to Write: Trace one concrete allocation/view or cache/memory path, name lifetime/aliasing constraints, compare layout choices, and specify a profiler or diagnostic check without inventing timings.
-->

- **Context:** State the hardware/runtime constraint, data layout, and assumptions activating this profile.
- **Analysis:** Trace one concrete allocation, view, or memory path; name lifetime/aliasing constraints and compare relevant layout choices.
- **Check:** State the profiler/diagnostic check and evidence limit (observed vs. unmeasured performance).

<!-- optional: history -->
## [OPTIONAL] Which earlier constraint explains this design? (Historical Evolution & Competing Paradigms)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-05](../shared/notes_decision_matrix.md#dm-05), [DM-19](../shared/notes_decision_matrix.md#dm-19).
> - **Include when:** Verified historical design constraints or competing paradigms illuminate why the modern architecture evolved this way; D05, D14.
> - **Adapt when:** Use only constraints relevant to the selected track and outcome.
> - **Omit or link when:** Already explained in Motivation or unsupported by primary sources; delete the heading and renumber retained sections.
> - **Quality check:** Does this change a decision or expose a consequential failure?
> - **Duplication check:** Link the existing explanation rather than repeating math, code or measurements.

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Verified historical design constraints or competing paradigms illuminate modern architectural choices; D05, D14.
- When to Omit Cleanly: Delete this heading and block completely if Motivation already covers provenance or primary historical citations are absent; never emit N/A; renumber retained headings sequentially.
- What to Write: Contrast documented prior capability and constraint with the modern mechanism; cite primary passages and separate chronology from causal attribution.
-->

- **Context:** State the prior paradigm, documented constraint, and verified primary source.
- **Analysis:** Contrast the prior limitation against the modern design, keeping chronology distinct from causal attribution.
- **Check:** State primary-source verification status (mark uninspected attributions `[UNVERIFIED]`).

<!-- optional: operations -->
## [OPTIONAL] How would I operate and diagnose it? (Production Deployment, Debugging & Observability Playbook)

> [!note] Authoring gate — remove after applying
> - **Decision-matrix IDs:** [DM-18](../shared/notes_decision_matrix.md#dm-18), [DM-19](../shared/notes_decision_matrix.md#dm-19).
> - **Include when:** An applied engineering or systems outcome includes real deployment, monitoring, or incident diagnosis; D04, D12–D14.
> - **Adapt when:** Use only constraints relevant to the selected track and outcome.
> - **Omit or link when:** Already explained elsewhere or outside scope; delete the heading and renumber retained sections.
> - **Quality check:** Does this change a decision or expose a consequential failure?
> - **Duplication check:** Link the existing explanation rather than repeating math, code or measurements.

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: An applied engineering or systems outcome requires real deployment criteria, observability signals, or incident diagnosis; D04, D12–D14.
- When to Omit Cleanly: Delete this heading and block completely for purely theoretical or non-operational notes; never emit N/A; renumber retained headings sequentially.
- What to Write: Specify the operational contract, primary failure signals, isolating diagnostic check, recovery action, and verification limits.
-->

- **Context:** State the deployment environment, operational contract, and failure surface.
- **Analysis:** Map failure signals to isolating checks, root causes, and concrete recovery actions.
- **Check:** State what the diagnostic verifies and which production regimes remain untested.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`deepstudy-master`):** Complete the [decision record](../shared/notes_decision_matrix.md#decision-record) before drafting, decompose `/scribe-deepnotes` topics into a syllabus + `3–6` dependency-ordered subtopic notes unless single-note locked, use strict 5-key YAML (`id`, `aliases`, `topic`, `tags`, `nexttopics` — no extra tag required), emit only selected domain-natural modules (embedded `.png`/`.svg` figures in `assets/<topic>/` for spatial/physics/ML plots; complete implementations and live verification for the saved stack when required; `2–3` Q&A cap; specific non-homepage source URLs or `[UNVERIFIED]`), strip all authoring gates and `<!-- SECTION: S* -->` markers, and renumber retained headings sequentially.
