<!-- scaffold:preflight
Decision-Matrix Pre-Flight: [note_decision_matrix.md](../shared/note_decision_matrix.md).
Switches: D01 route (`studynotes`); D02–D04 scope/reader/outcome; D05 fast direct fetch or supplied source;
D06–D09 `math_level` (default 0; raise only if inherently mathematical/physical/quantitative); D10 source-order examples;
D11 optional visual walkthrough; D12–D13 checks; D14 optional modules (`procedures`, `reference`, `caveats`, `formal`, `visual`); D15 final audit.
Strip this block before emission. Load detailed DM branches only when active.
-->

---
id: "<nn>-<topic-slug>"
aliases: []
topic: "<Topic or source title>"
tags: [study-notes]
nexttopics: []
---

# <Topic / Source Title>

> [!important] Source-Sequence Rule
> Follow the source's order of ideas. Keep definitions, examples, derivations, evidence, and caveats beside the subtopic they explain. Do not reorganize the material into a textbook order unless the source itself follows that order or a clearly labeled explanatory bridge is needed.

> [!important] Source-Fidelity Rule
> Keep source claims distinct from added teaching explanations. Do not invent missing facts, quotations, examples, dates, or conclusions. Mark unsupported details as [UNVERIFIED] and ambiguous or incomplete material as [NEEDS CLARIFICATION]. If the source is unavailable or incomplete, state what was actually accessible.

> [!important] Teaching Sequence
> For each concept, move from plain-language intuition → precise term and symbol definitions → step-by-step reasoning → a suitable example → a quick self-check. Adapt or omit a step when it does not fit the concept; never add filler to satisfy the sequence.

See [math gates](../shared/math_gates.md); select depth from source and outcome.

## 1. What is this note about, where does the material come from, and what should I learn? (Overview, Source Context & Learning Goals)

> [!info] Source & Scope Context
> - **Subject / Domain**: <Field or area>
> - **Module / Section**: <Chapter, section, or topic group, if applicable>
> - **Primary Source(s)**: <Title, author/organization, publication date or version when known, and link or precise location>
> - **Source Access**: <Full text / transcript / documentation available / partial text / metadata only>
> - **Scope Boundaries**: <What this note covers and what it leaves for linked notes>

- **Sequential Topic Outline**:
  1. <First topic in the source's order>
  2. <Next topic>
  3. <Continue only as needed>
- **By the end of this note, I should be able to**:
  - <Concrete action or explanation target>
  - <Concrete calculation, distinction, or application target>
  - <Concrete evaluation, implementation, or reasoning target>
- **Source-to-Note Distinction**: <State which parts below summarize the source and which parts add explanation, examples, or independent verification.>

### Section Check

- **Decision matrix**: D02–D15 select scope, reader level, learning outcomes, and source traceability.
- **Include when**: Every note needs a topic, its source/access status, scope, and useful learning outcomes.
- **Adapt when**: For a self-study topic without one primary source, name the materials or evidence used and label the note as a synthesis.
- **Omit or shorten when**: A metadata item is unknown or irrelevant; do not invent it or retain empty placeholders.
- **Quality check**: Can a reader identify what material the note is based on, what it covers, and what they should be able to do after reading it?

## 2. How does the source develop each idea, and how can I understand it step by step? (Core Concepts & Sequential Breakdown)

Create one numbered subsection for each meaningful subtopic, in the exact order it appears in the source. Repeat the structure below where it helps. Delete fields that do not fit a subtopic.

### 2.1 <First Subtopic in Source Order>

- **Core Point / Source Statement**: <What the source states, defines, establishes, or demonstrates. Keep claims faithful and cite the source location when useful.>
- **In Simple Words**: <Explain the idea in clear, beginner-friendly language without changing the source's meaning.>
- **Why This Matters**: <Explain purpose, intuition, consequence, or connection to the previous subtopic.>
- **Key Terms & Symbols**:
  - **<Term or symbol>**: <Meaning, domain, shape, or units before first substantive use.>
  - **<Term or symbol>**: <Meaning and relevant distinction.>
- **Step-by-Step Explanation**:
  1. <First reasoning step. Explain why it follows when that is not obvious.>
  2. <Next step. Keep assumptions and intermediate changes visible.>
  3. <Result, interpretation, or transition to the next idea.>
- **Illustrative Example** *(include when it clarifies the idea)*:
  - **Setup / Given**: <Input, situation, values, or conditions>
  - **Step-by-Step Working**:
    1. <Action and reason>
    2. <Next action and reason>
  - **Result / Interpretation**: <Meaning of the result; include units or output shape when relevant>
- **Quick Check**: <One focused question that tests the subtopic's central idea. Add a short hint only when useful.>
- **Source Location / Evidence** *(when traceability matters)*: <Page, heading, timestamp, equation, or documentation section>

### 2.2 <Next Subtopic in Source Order>

- **Core Point / Source Statement**: <Source-faithful claim or definition>
- **In Simple Words**: <Plain-language explanation>
- **Why This Matters**: <Purpose or causal bridge>
- **Key Terms & Symbols**: <Define new items before using them>
- **Step-by-Step Explanation**:
  1. <Reasoning step>
  2. <Reasoning step>
  3. <Result or connection>
- **Illustrative Example** *(optional)*:
  - **Setup / Given**: <Small, informative case>
  - **Step-by-Step Working**: <Show meaningful intermediate steps>
  - **Result / Interpretation**: <Explain the outcome>
- **Quick Check**: <Focused self-test>
- **Source Location / Evidence** *(optional)*: <Reference location>

### Section Check

- **Decision matrix**: D02–D15 select source order, teaching sequence, terminology, example choice, and source attribution.
- **Include when**: This is the main body of a source-faithful study note.
- **Adapt when**: A subtopic is conceptual, procedural, mathematical, historical, or implementation-focused. Use only the fields that clarify it; examples and calculations are optional when they do not fit.
- **Omit or link when**: A prerequisite needs a full separate lesson, a repeated explanation already exists, or a source detail is outside this note's scope.
- **Quality check**: Is source order preserved? Are claims locatable? Are new terms defined before use? Does the explanation show why steps follow? Does each example teach?
- **Duplication check**: Keep the full explanation here. Section 3 is for a larger method or integrated problem, not a second copy of every subsection example.

<!-- optional: procedures -->
## [OPTIONAL] How do the procedures, reasoning chains, or worked problems fit together? (Procedures, Reasoning Chains & Worked Problems)

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Source teaches a multi-step procedure, reasoning chain, or integrative worked problem spanning multiple subtopics beyond Section 2's local examples; D04, D06–D10, D14.
- When to Omit Cleanly: Delete this heading and block completely if Section 2 already covers every trace; never emit N/A; renumber subsequent sections sequentially.
- What to Write: Begin with Context (source procedure/problem trigger), develop Analysis (step-by-step method, worked problem, and safe/unsafe heuristic conditions), and end with Check (sanity check and validity scope).
-->

- **Context:** Identify the integrated source procedure, derivation, or worked problem activating this section.
- **Analysis:** Apply the method, worked-problem, and heuristic specifications below without repeating Section 2's local examples.
- **Check:** State the sanity check (units, shape, sign, or boundary behavior) and exact applicability boundary.


Use this section for a method, derivation, proof, multi-step procedure, or integrative worked problem that deserves a complete trace beyond the local examples in Section 2. If the source contains no such material, omit this section from the finished note.

### Method / Procedure / Derivation *(choose the label that fits)*

1. **Starting Point**: <Given information, definition, equation, input, or assumption>
2. **Step**: <Operation or reasoning and why it is valid>
3. **Step**: <Continue without skipping a consequential logical, algebraic, or computational transition>
4. **Result & Applicability**: <Conclusion and the conditions under which it holds>

### Worked Problem *(when the material supports one)*

- **Given**: <Known values, facts, or conditions>
- **Find**: <Requested result>
- **Plan**: <Choose a concept, formula, or procedure and explain why it applies>
- **Solution**:
  1. <Step and justification>
  2. <Step and justification>
  3. <Final result>
- **Sanity Check**: <Check units, shape, sign, boundary behavior, assumptions, or plausibility—choose only checks relevant to this problem>

### Key Insight, Heuristic, or Shortcut *(optional)*

- **Pattern**: <Useful recognition cue or efficient method>
- **Safe when**: <Exact conditions that justify it>
- **Unsafe when**: <Condition or counterexample where it fails>

### Section Check

- **Decision matrix**: D02–D15 select topic type, math depth, derivation depth, example choice, and code/procedure purpose.
- **Include when**: The source teaches a reusable process, derivation, proof, or problem-solving method, or when separate concepts need one integrated example.
- **Adapt when**: A non-mathematical procedure is better represented as states, decisions, or actions than equations.
- **Omit or link when**: Section 2 already contains the complete trace and no larger process needs synthesis.
- **Quality check**: Is each consequential step shown and justified? Are assumptions visible? Does the result state when it applies?
- **Duplication check**: Do not repeat each local example from Section 2; use one integrative problem or link to the detailed derivation.

<!-- optional: reference -->
## [OPTIONAL] Which rules, definitions, or formulas should I use, and when do they apply? (Rules, Definitions & Reference Matrix)

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Source introduces multiple reusable rules, definitions, commands, or formulas whose selection conditions benefit from compact side-by-side lookup; D06–D09, D14.
- When to Omit Cleanly: Delete this heading and block completely if the topic has only one obvious rule or the table would merely duplicate Section 2; never emit N/A; renumber subsequent sections sequentially.
- What to Write: Populate the compact lookup matrix below with only items used in this note, plus explicit selection cues for distinguishing when each rule applies.
-->

- **Context:** Identify the reusable rule/formula family introduced by the source.
- **Analysis:** Fill the reference matrix and selection cues below with exact conditions and caveats.
- **Check:** Confirm every row appears in this note and specifies a concrete misuse boundary.


Record only items introduced or needed in this note. If the subject has no useful compact reference set, omit the table rather than filling it with generic material.

| Rule / Definition / Formula | Meaning of Each Term or Symbol | Conditions for Use | Notes / Units / Caveats |
|---|---|---|---|
| <Item> | <Definitions, domain, units, or shape> | <Assumptions and recognition cues> | <Relevant limitation or source location> |

- **How to Choose the Right Rule or Approach**: <Give explicit cues for distinguishing which method applies. Include a short decision path only when there is a real choice.>

### Section Check

- **Decision matrix**: D02–D15 select math necessity, symbol/units, formula validity, and method selection.
- **Include when**: Reusable rules, definitions, equations, commands, or selection cues benefit from quick lookup.
- **Adapt when**: Keep only relevant columns; omit units for qualitative definitions, include shapes for tensor formulas, and preconditions for procedures.
- **Omit or link when**: The table would duplicate explanations or contain only one obvious item; keep that explanation in its canonical section.
- **Quality check**: Does every entry appear in or support this note? Are conditions and caveats specific enough to prevent misuse?
- **Duplication check**: This is a compact reference, not a replacement for Sections 2 or 3.

<!-- optional: caveats -->
## [OPTIONAL] What questions, ambiguities, and caveats should I resolve? (Deep Questions, Confusions & Caveats)

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Source presents genuine edge cases, ambiguities, contested claims, subtle assumptions, or unresolved confusions worth tracking; D05, D13–D14.
- When to Omit Cleanly: Delete this heading and block completely if no meaningful caveat or open question remains; never fabricate confusion or emit N/A; renumber subsequent sections sequentially.
- What to Write: Separate source uncertainty from added verification and personal confusion (`**Confusion** ::`), documenting concrete corrections and `[UNVERIFIED]` / `[NEEDS CLARIFICATION]` gaps.
-->

- **Context:** Identify the source ambiguity, edge case, or assumption conflict activating this section.
- **Analysis:** Document the critical question, resolution or correction, and exact validity boundary.
- **Check:** Distinguish source claims from independent verification and flag unresolved items clearly.


- **Critical Question / Edge Case**: <A non-trivial question raised by the material>
  - **Resolution / Explanation**: <Clear reasoning, evidence, or derivation. If unresolved, say exactly what remains unknown.>
**Confusion** :: <Exact unresolved step, assumption, term, or ambiguity and what would resolve it>
- **Corrections & Caveats**:
  - **Potential misunderstanding**: <Claim or inference that may be mistaken>
  - **Correction / boundary**: <Accurate version and the condition or evidence that matters>
- **Unverified detail** *(only when present)*: <[UNVERIFIED] or [NEEDS CLARIFICATION] item, why it cannot yet be confirmed, and where to verify it>

### Section Check

- **Decision matrix**: D02–D15 select source confidence, edge-case relevance, misconception risk, and follow-up.
- **Include when**: Material presents genuine ambiguity, disagreement, edge cases, assumptions, common errors, or unresolved questions.
- **Adapt when**: Distinguish source uncertainty from your own confusion and from independent correction.
- **Omit or link when**: No meaningful question or caveat remains; do not invent one.
- **Quality check**: Is each resolution supported or labeled as added verification? Is each open confusion specific enough to follow up?
- **Duplication check**: Keep general caveats here; leave the core mechanism in Section 2 and brief retrieval cues in Section 6.

## 6. What should I remember, test myself on, and study next? (Key Takeaways & Active Recall)

- **Key Takeaways**:
  - <Core principle>
  - <Main mechanism, method, or relationship>
  - <Practical significance, boundary, or use condition>
- **Common Mistakes to Avoid**:
  - **Mistake**: <What can go wrong> — **Why it fails**: <Reason> — **Prevention**: <Specific check or correction>
- **Q&A Mastery Check** *(2–3 non-overlapping questions with collapsible answers)*:

1. **Recall:** <State or identify the central idea.>
> [!example]- Answer
> <Concise verification answer; quote every line inside this callout with `>`.>

2. **Causal Explanation:** <Explain why a mechanism, step, or condition matters.>
> [!example]- Answer
> <Concise reasoning cue; quote every line inside this callout with `>`.>

3. **Application:** <Apply, distinguish, calculate, or diagnose a suitable new case.>
> [!example]- Answer
> <Application check or solution; quote every line inside this callout with `>`.>

- **Next Topic Connection**: <Explain how this note prepares the reader for an item in nexttopics. Omit if no next topic is known.>

### Section Check

- **Decision matrix**: D02–D15 select recall type, question difficulty, answer visibility, and learning-sequence links.
- **Include when**: The note is intended for later study or retrieval.
- **Adapt when**: Match questions to the material: conceptual prompts for concepts, numerical/application prompts for quantitative topics, and diagnosis prompts for procedures.
- **Omit or shorten when**: A recap only repeats earlier text; retain only retrieval cues that test useful understanding.
- **Quality check**: Do questions test recall, causal understanding, and transfer without unstated prerequisites? Are answers concise enough to support self-checking?
- **Duplication check**: Takeaways are retrieval cues, not a second full summary.

<!-- optional: formal -->
## [OPTIONAL] Why does this result follow? (Formal Proof & Convergence / Complexity Derivation)

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: The topic is inherently mathematical, physical, or quantitative engineering and the source or outcome requires a derivation at `math_level == 2`; D06–D09, D14.
- When to Omit Cleanly: Omit whenever `math_level < 2` or plain-language intuition suffices. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: State claim, domain assumptions, and source location; justify every non-obvious step (`*Why this step holds:*`); label any added reasoning as supplemental; distinguish numerical checks from proof.
-->

- **Context:** State the theorem/result, domain assumptions, and source location requiring `math_level == 2` derivation.
- **Analysis:** Walk through each non-obvious derivation step with explicit assumptions and label supplemental steps distinctly from the source.
- **Check:** Confirm dimensional/limit sanity and distinguish numerical verification from formal proof.

<!-- optional: visual -->
## [OPTIONAL] How do components, states, or layouts interact visually? (Visual Diagram / ASCII State-Transition Walkthrough)

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Multi-component architecture, control flow, memory layout, or state transitions are significantly clearer spatially than in prose alone; D10–D11, D14.
- When to Omit Cleanly: Omit when prose or existing examples already make structure obvious. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Render one focused Mermaid diagram (`flowchart TD` / `sequenceDiagram`, double-quoted labels, Unicode symbols) or compact ASCII layout followed by a 2–3 sentence transition walkthrough.
-->

- **Context:** Name the spatial or state relationship that prose alone obscures.
- **Analysis:** Present the Mermaid diagram or ASCII state-transition walkthrough and trace the key transition in 2–3 sentences.
- **Check:** Confirm every node/state matches Section 2 terminology and no raw LaTeX delimiters appear inside Mermaid nodes.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`studynotes`):** Preserve the source's logical sequence, keep source claims distinct from added explanations, default `math_level: 0` unless inherently quantitative, end every subtopic note with a `2–3` question Q&A Mastery Check using collapsed `> [!example]- Answer` callouts, mark gaps `[UNVERIFIED]` / `[NEEDS CLARIFICATION]`, and strip all `### Section Check` gates and unused optional blocks before emission.
