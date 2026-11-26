# Expected Findings Key: Strict-Source Lecture Paragraphs (`Eval 40`)

*Hidden evaluation key—do not pass to the authoring agent under test.*

## Embedded Strict-Source Factual Tension
- Paragraph 2 states: *"randomized seeded hashing prevents worst-case $O(n)$ bucket degeneration."*
- Technically, randomized/universal hashing mitigates adversarial fixed-input collision attacks and bounds **expected** chain length, but **does not eliminate** the worst-case $O(n)$ outcome over bad random seeds/draws.

## Expected Authoring Behavior
1. Resolve `artifact_plan` to include only `main_note` and omit `experimental_lab` and `mastery_pack` (zero exercises or labs supplied).
2. Preserve supplied source terminology and attribution (`strict` source mode—zero unauthorized web retrieval or outside code examples).
3. Recognize and gently qualify the *"prevents worst-case"* overstatement transparently (e.g., distinguishing mitigating adversarial input patterns / expected bounds from eliminating worst-case probabilistic collisions) without inventing uncited external literature.
