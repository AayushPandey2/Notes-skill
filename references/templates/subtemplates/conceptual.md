# Conceptual composition

Activate for conceptual mastery, definitions, comparisons, or method-selection objectives (TEACH-01, TEACH-02, TEACH-04, TEACH-08).

Inputs are the concept identity, learning objectives, prerequisites, audience, source policy, authored theory, examples, boundary conditions, and relevant source evidence. Bridge unfamiliar prerequisites before relying on them. Explain an analogy's limits before advancing to formal reasoning.

The runtime composition owner is `scriptorium/engines/composition/writing.py`: `plan_depth` establishes obligations; `teach` places prerequisite material before formalism; `write` composes the selected content; `validate` records generated and pending obligations on the actual artifact. All stages share the Composition record.

Use natural paragraphs, meaningful transitions, concrete examples and counterexamples. Explain causal differences before a comparison table. Do not fill a missing lesson with a topic-name substitution or invent mathematical content for a nonmathematical concept.

The output is Markdown plus execution and obligation evidence in the blueprint's `composition_result`. Set `require_complete` for a request that must reject missing structural teaching obligations. That check is not an educational accuracy certificate. Review the actual source-grounded reasoning and run `QualityEngine.evaluate_teaching` and `QualityEngine.review_explanatory_clarity` before claiming educational acceptance.

When evidence or content is missing, repair the specific pending obligation. Preserve strict source restrictions; retrieve additional sources only when that policy permits them. See [teaching_core.md](../../../shared/teaching_core.md).
