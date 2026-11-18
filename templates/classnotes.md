# Class Notes: <Course / Lecture Title>

- **Header Block**: YAML frontmatter (`type: classnotes`; optional `course`, `unit`, `lecture`, `instructor`, `date`, `tags: [classnotes]`) + `# Class Notes: <Course / Lecture Title>`.
- **Ordering Rule**: Follow the teacher's or lesson's sequence exactly. Keep examples, definitions, derivations, questions, and board work beside the topic where they occurred. Do not reorganize the lesson by textbook order.
- **Teaching Style**: Explain each idea clearly and intuitively: start simply, define every new term or symbol, build intuition, show the reasoning step by step, then give an example and a quick check for understanding. Keep the source's meaning and flag unclear or missing information instead of guessing.
- **Mathematical Notation Guardrail**: Default to `math_level: 0`—do **not** include formal mathematical formulas, LaTeX equations, or heavy derivations by default. Explain concepts using plain language, intuitive analogies, and structured text. Only include mathematical notation (`math_level >= 1`) when it is strictly essential to the subject matter itself (e.g., an inherently Mathematics, Physics, or quantitative engineering topic where omitting equations would make the explanation incomplete).

## 1. What class is this, and what are we learning today? (Class Context & Learning Goals)

- `> [!info] Class Details`:
    - **Course / Subject**: <Course name>
    - **Unit / Chapter**: <Unit or chapter>
    - **Lecture / Date**: <Lecture number and date>
    - **Teacher**: <Teacher name>
    - **Materials**: <Slides, textbook pages, board notes, or other materials>
- **Topic sequence from class**: <List the topics in the order the teacher introduced them.>
- **By the end of this class, I should be able to**:
    - <Learning goal 1>
    - <Learning goal 2>
    - <Learning goal 3>

## 2. What did the teacher explain first, and how does the idea work? (Ordered Lesson Notes)

- Create one subsection for each topic, in the exact order it appeared in class:

### 2.1 <First topic as introduced by the teacher>

- **Teacher's point**: <What the teacher said, demonstrated, or wrote.>
- **In simple words**: <Explain the idea in clear, beginner-friendly language.>
- **Why this matters**: <State the purpose, intuition, or connection to the previous topic.>
- **Key terms and symbols**:
    - `<term or symbol>`: <Meaning, including units where relevant.>
- **Step-by-step explanation**:
    1. <First reasoning step>
    2. <Next reasoning step>
    3. <Conclusion or result>
- **Example from class**:
    - **Question / setup**: <Write the given information or problem.>
    - **Working**: <Show each step and explain why it is valid.>
    - **Answer**: <State the result with units or interpretation.>
- **Quick check**: <One short question that tests the main idea.>

### 2.2 <Next topic as introduced by the teacher>

- Repeat the same pattern for every topic. Add or remove the example and calculation fields when they do not fit the subject, while keeping the teacher's order.

## 3. How did the class connect the ideas or solve problems? (Derivations, Procedures & Worked Examples)

- **Method / derivation / procedure**: <Use when demonstrating a procedure, reasoning chain, or (only when essential for math/physics/quantitative topics) a derivation.>
    1. **Starting point**: <Given situation, definition, data, or assumption.>
    2. **Step**: <Show the operation and explain why it is used.>
    3. **Step**: <Continue without skipping logic or code changes.>
    4. **Result**: <State what was derived or established and when it applies.>
- **Worked problem**:
    - **Given**: <List known values or conditions.>
    - **Find**: <State what is being asked.>
    - **Plan**: <Choose the relevant concept or approach and explain why.>
    - **Solution**: <Show steps one at a time.>
    - **Check**: <Check sanity, boundary cases, or whether the answer makes sense.>
- **Teacher's shortcut or observation**: <Record useful insight and explain when it is safe to use.>

## 4. Which rules, key concepts, or definitions should I remember? (Reference & Meaning)

- Record only items introduced or needed in this lesson (include formulas only when strictly required by a mathematical/physical/quantitative topic):

| Rule / Definition / Formula | What each term or symbol means | Conditions for use | Notes / Units |
|---|---|---|---|
| <Item> | <Meaning> | <When it applies> | <Notes or caution> |

- **How to choose the right rule or approach**: <Explain how to recognize when each item applies.>

## 5. What questions, confusions, or corrections came up? (Class Discussion & Open Points)

- **Student question**: <Question>
    - **Teacher's answer**: <Answer, keeping important reasoning.>
- **Open confusion**: `**Confusion** :: <What is still unclear and what exact step needs clarification?>`
- **Correction or caveat**: <Record a corrected statement, assumption, exception, or point to verify.>

## 6. What should I be able to recall after class? (Takeaways & Self-Check)

- **Key takeaways**:
    - <Main idea in one sentence.>
    - <Important relationship, method, or result.>
    - <When or why to use it.>
- **Common mistakes to avoid**:
    - <Mistake> — <Why it is wrong and how to avoid it.>
- **Self-check questions**:
    1. <Recall question>
    2. <Explain-the-reason question>
    3. <Apply-the-method question>
- **Answers / hints**: <Add concise answers or leave blank for active recall.>
- **Next class connection**: <What this lesson prepares me to learn next.>

Follow [shared authoring rules](../shared/authoring_rules.md) and the [footer contract](../shared/footer_widgets.md). Apply the math gate only when strictly essential to a mathematical, physical, or quantitative engineering topic (default `math_level: 0`). Scaffold comments are editing slots and must be removed before publication.

Follow the lesson order throughout. Preserve important wording, examples, and notation from class or the fetched source, but explain them in your own clear words. Define every new term and symbol before relying on it. For reasoning, procedures, code, or calculations, show each step and explain why it follows. Keep source statements separate from added explanation; mark uncertain details as `[CHECK WITH TEACHER]` or `[UNVERIFIED]` instead of filling gaps by guesswork. End with the key takeaways and self-check questions.

> [!important] AGENT AUTHORING DIRECTIVE — `classnotes` Keep the notes faithful to the lesson sequence and content. Teach each topic from the basic idea to the reasoning, then to a worked example and a brief understanding check. Explain unfamiliar words, connect each new topic to what came before with readable transitions, and apply the mandatory **Humanization & Cohesion Pass** (conversational yet rigorous tone to your future self, zero AI clichés, synthesized mental models rather than pasted raw text). Minimize mathematical notation by default (`math_level: 0`, plain language and intuitive analogies); include LaTeX equations only when the topic itself is inherently mathematical, physical, or quantitative engineering where omitting them would make the explanation incomplete. Do not invent lecture details, examples, teacher statements, or answers; label gaps clearly for follow-up.
