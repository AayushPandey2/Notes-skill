# Conditional mathematics (levels 1 and 2 only)

For every mathematical module that is included:

1. State the problem, input and output domains, assumptions, and intended result before manipulating equations.
2. Define every symbol, index, operator, parameter, and relevant unit before its first mathematical use. Give shape/dimensions for vectors and tensors. A local symbol key can be extended as new notation appears; never force the reader to infer notation from a later table.
3. Give a complete symbol-anatomy table before the main formula: **Symbol | Meaning | Type/domain/shape | Units/range | Effect when changed**. Then present the formula in `$$...$$`. Mark sensitivity as context-dependent when it is not monotonic.
4. Connect the operations to geometry, scale, dependence, or another useful interpretation. Do not impose a geometric story when none is justified.
5. Include a small input-to-output table covering the smallest valid case, the running example, one changed input, and a boundary/degenerate case where applicable.
6. Analyze relevant domain boundaries. Discuss zero, one, negative values, ties, singular inputs, or infinite limits only where they belong to the mathematical domain. Do not calculate a meaningless limit just to fill a checklist.
7. For level 2, state the target and proof strategy. Number every nontrivial step and explain **Why this step holds**, including assumptions, division guards, and equivalence versus implication. Do not hide a nontrivial leap behind “clearly” or “after simplification.”
8. End with a sanity check, what follows from the result, a counterexample to a tempting overgeneralization, and what remains unproven.

Mathematical proof, experimental evidence, and numerical agreement are different kinds of support. Label them accurately.
