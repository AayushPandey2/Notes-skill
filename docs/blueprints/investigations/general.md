# General experimental lab

Use when a named domain would impose irrelevant machinery. Keep this hierarchy and the opening rules in [the lab contract](../../procedures/authoring/experimental-lab.md). Support conceptual, observational, procedural, computational, and design work. Each section needs a concrete learner action, evidence or deliverable, and suitable visual opportunity; retain an inapplicable heading with a specific reason. Do not insert ML metrics, Rust, chemical apparatus, or physical measurements without genuine need.

The section prompts below define purpose and content. Use this companion check for an example, evidence, visual opportunity, and common mistake. Keep a heading with a specific reason if a tool or observation cannot be used for the selected topic.

| Section | Example and evidence/deliverable | Visual opportunity | Avoid; genuine limit |
|---|---|---|---|
| 01 | Compare two note-search methods and define outcomes | Workflow overview | Avoid vague “understand” goals; always |
| 02 | Specify query, corpus, and success criteria | Input/output map | Avoid undefined quality claims; always |
| 03 | Define relevance and ranking terms | Concept diagram | Avoid jargon before examples; always |
| 04 | Walk a search manually through matching and ranking | State sequence | Avoid hidden decisions; always |
| 05 | Apply an established search feature to same query | Tool screenshot if verified | Avoid claiming tool use without access; tool-specific action may be unavailable |
| 06 | Change query wording while holding corpus fixed | Variation table | Avoid changing multiple conditions; always |
| 07 | Record retrieved items and relevance judgments | Evidence table | Avoid invented observations; actual tool output absent until accessed |
| 08 | Complete a bounded retrieval task | End-to-end flow | Avoid an uncheckable deliverable; always |
| 09 | Compare output against stated criteria | Quality matrix | Avoid using personal preference as universal proof; always |
| 10 | Diagnose a missed relevant result | Failure trace | Avoid generic troubleshooting; always |
| 11 | Compare manual and tool methods on same corpus | Method table | Avoid unfair input changes; a second method may be unavailable |
| 12 | State corpus/language transfer limits | Boundary diagram if helpful | Avoid overstating generality; always |
| 13 | Try a harder query and explain expected evidence | Annotated example | Avoid tasks with no answer check; always |
| 14 | Justify one method and diagnose a failure | Decision table | Avoid terminology recall alone; always |
| 15 | State result, evidence status, and next task | Usually no new image | Avoid treating planned work as completed; always |

## LAB SECTION 01 — INTRODUCTION AND LEARNING OBJECTIVES
### Why investigate
State the practical question, level, prerequisites, outcomes, and a motivating instance.
## LAB SECTION 02 — PROBLEM, CONTEXT, AND SUCCESS CRITERIA
### Boundaries
Define inputs, setting, stakeholders or constraints, expected deliverable, and how success will be judged; avoid vague goals.
## LAB SECTION 03 — FOUNDATIONS, TERMS, AND ASSUMPTIONS
### Shared language
Define essential terms and assumptions before the procedure; show a small example or concept map.
## INVESTIGATION TRACK A — CORE MECHANISM
Reveal the idea's causal steps.
## LAB SECTION 04 — FIRST-PRINCIPLES CONSTRUCTION OR WALKTHROUGH
### Trace one instance
Build or reason through a small complete case, showing intermediate states and why each step follows. Use an inspected local web figure or structured step table as appropriate (never Mermaid or ASCII).
## INVESTIGATION TRACK B — ESTABLISHED METHOD OR TOOL
Explain what the standard approach adds.
## LAB SECTION 05 — STANDARD PRACTICE AND GUIDED APPLICATION
### Repeatable method
Apply a credible established method to the same case, explaining inputs, outputs, choices, and limits without inventing tool use.
## EXPERIMENTAL INVESTIGATION
State a question and one controlled variation.
## LAB SECTION 06 — CONTROLLED VARIATIONS
### Compare fairly
Hold context stable, vary one relevant condition, and state hypothesis, procedure, and what would count as evidence.
## LAB SECTION 07 — OBSERVATIONS AND EVIDENCE
### Record and interpret
Table actual, supplied, published, or expected observations with clear labels. Distinguish evidence from interpretation and avoid fictional results.
## APPLICATION TRACK
Combine the stages in a realistic bounded task.
## LAB SECTION 08 — END-TO-END PRACTICAL TASK
### Part A — Complete Real-World Practical Workflow (10–12 Steps)
Replace a brief summary with a realistic end-to-end applied workflow on a concrete domain corpus, case set, or operational task. For **every** step, provide prose purpose, structured procedure or executable Markdown block (`Status: static review (not executed)` if unexecuted), collapsed `> [!example]- Step-by-step: ...` walkthrough, expected output/interpretation, and transition:
1. **Setup, Criteria & Scope Alignment:** State tools, constraints, stakeholders, and exact success-polarity definition (`Outcome | Meaning` table).
2. **Load & Frame the Realistic Case Set:** Document item/case count, attributes, and contextual metadata.
3. **Inspect & Audit Input Quality:** Check completeness, ambiguity, duplicates, conflicting definitions, and edge cases (`Audit Check | Purpose` table).
4. **Partition Development Cases vs. Held-Out Evaluation Cases:** Separate reference cases used to refine rules/heuristics from unseen cases reserved for final testing.
5. **Build the End-to-End Execution Pipeline:** Chain `ingest -> normalize/filter -> apply core method -> validate output -> format deliverable`, keeping criteria isolated from test-case peeking.
6. **Trace Internal Decision Mechanics:** Walk step by step through how inputs are weighted, ranked, filtered, or resolved under constraints.
7. **Compare Intermediate Scores vs. Final Decisions:** Contrast raw observations, intermediate scores/rankings, and final thresholded decisions in a `Stage | Example Output` table.
8. **Evaluate Outcomes by Criterion Type:** Separate **process reliability** (consistency, reproducibility, constraint compliance) from **outcome effectiveness** (precision, recall, error cost, user impact) on the **same** held-out cases against a baseline.
9. **Diagnostic Error & Trade-Off Analysis:** Map false positives vs. false negatives or failure modes across cases (using a structured matrix or inspected local web visual; never Mermaid/ASCII).
10. **Extract Key Decision Drivers & Thresholds:** Inspect which rules, criteria, or weights governed the final outputs (`Driver | Meaning` table).
11. **Visualize Impact & Correlation-vs-Causation Caveat:** Rank dominant drivers and explicitly note that observational pattern alignment does not prove causal effect without controlled intervention.

### Part B — Constraints, Method Variants & Systematic Validation
- **Fixed Constraints vs. Tunable Process Parameters Table:** Contrast non-negotiable domain constraints against configurable settings (thresholds, strictness, weights, batch size, review depth).
- **Threshold & Strictness Sensitivity Table:** Concrete table showing how tightening or relaxing criteria trades coverage against precision/effort.
- **Method & Strategy Compatibility Matrix:** Compare manual, rule-based, heuristic, and structured-framework approaches across transparency, scalability, edge-case handling, and failure cost.
- **Quality & Failure Guards:** Explain stopping criteria, escalation triggers, tie-breaking rules, and fallback handling when evidence is incomplete.
- **Multi-Case Cross-Validation Protocol:** Define a repeatable $K$-split or A/B case evaluation (`variants × splits`), reporting exact case counts and keeping planned trials distinct from verified outcomes.
## FINAL VALIDATION AND LEARNING
Judge quality and transfer.
## LAB SECTION 09 — VERIFICATION AND QUALITY CHECKS
### Independent check
Check the output against success criteria, a countercase, and source or tool limits.
## LAB SECTION 10 — ERRORS, FAILURE MODES, AND TROUBLESHOOTING
### Diagnose a real failure
Connect symptoms to causes and a corrective test rather than giving generic advice.
## LAB SECTION 11 — ALTERNATIVES AND TRADE-OFFS
### Choose deliberately
Compare two suitable methods on quality, effort, constraints, and evidence.
## LAB SECTION 12 — LIMITATIONS AND TRANSFER
### Bound the conclusion
State where the method stops working and how to adapt it to a nearby case.
## LAB SECTION 13 — PRACTICAL CHALLENGES
### Extend the task
Give progressively harder exercises with deliverables and checks.
## LAB SECTION 14 — FINAL LEARNING CHECKPOINT
### Explain a choice
Ask learners to justify a method, interpret evidence, and diagnose one failure; include answer guidance.
## LAB SECTION 15 — FINAL SUMMARY
### Takeaway
Summarize mechanism, evidence, limits, and next application.
