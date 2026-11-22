# Illustrative outputs for review

These short original samples demonstrate composition, not exhaustive production notes or measured model outputs. They omit vault metadata because they are review excerpts. The regression suite separately exercises full publication.

## Conceptual sample: A definition and a distinction

An algorithm is a specified procedure for obtaining a result from permitted inputs. To recognize one, look for the operations, their order or selection rules, and how the procedure finishes. “Find the answer somehow” leaves the operations unspecified; “inspect each item and stop at the first match or the end” provides a procedure.

The distinction matters because a reader should be able to trace the instructions on a concrete input. For [4, 7, 3], searching for 7 inspects 4, then 7, and stops. Searching for 8 reaches the end without a match. Neither equations nor a programming language are needed to understand this distinction.

Recall: what must the procedure do when no item matches? It must define an outcome for reaching the end. That boundary is part of the procedure, not an implementation detail to guess later.

## Mathematical sample: One descent step

Let the loss be $L(w)=w^2$, where $w$ is a real scalar. Its derivative $L'(w)=2w$ describes local change: positive slope means a sufficiently small move left reduces the loss. Gradient descent subtracts a multiple of that slope, using a positive step size $\eta$.

Substituting the derivative into the update gives $w_{next}=w-\eta(2w)=(1-2\eta)w$. The second equality factors out $w$; it shows directly how the step size changes the next position. With $w=3$ and $\eta=0.1$, the derivative is 6, the step is 0.6 and the new position is 2.4. The loss falls from 9 to 5.76.

For nonzero $w$, the loss decreases exactly when $(1-2\eta)^2<1$, or $0<\eta<1$. At $\eta=1$ the sign flips and the loss stays the same. This result follows for this quadratic; it is not a universal learning-rate interval for arbitrary loss functions.

Transfer check: at $\eta=0.5$, the next position is zero from any starting value. This follows from the factor $1-2\eta$, without repeating the entire calculation.

## Source-led sample: Ordered lookup

The [fixture's definition](source-fixture.md#definition) requires an ascending sequence. Its [worked example](source-fixture.md#example) starts from [2, 5, 9, 14, 20] and seeks 14. Because the middle value is 9 and all values before it are no greater than 9, the target can only remain to its right. The remaining candidates are [14, 20].

The [figure](source-fixture.md#figure) separates discarded positions from surviving candidates. Its divider represents a decision boundary between candidate groups, not an array value. This interpretation is an educational clarification of the diagram.

The [source exercise](source-fixture.md#exercise) asks about seeking 5 instead. Educational solution: compare 5 with 9; 5 is smaller, so [2, 5] remain. The [qualification](source-fixture.md#qualification) is essential: sortedness licenses the discard. The example does not establish which duplicate occurrence a complete implementation would return.

## Beginner and advanced treatments of the same result

For a beginner learning why a square cannot be negative, begin with multiplication signs: positive times positive is positive, negative times negative is positive, and zero times zero is zero. The case $(-3)^2=9$ distinguishes squaring a negative input from negating a square. Ask the learner to explain why $-3^2$ needs attention to notation.

For an advanced reader of ordered fields, state the target precisely: for every real $x$, $x^2\geq0$. If $x\geq0$, multiplication preserves nonnegativity. If $x<0$, then $-x>0$ and $x^2=(-x)^2>0$. Equality holds exactly at zero. The proof relies on order compatibility with multiplication; an unordered field does not supply the same inequality statement. This treatment needs explicit assumptions and proof, without beginner repetition or code.
