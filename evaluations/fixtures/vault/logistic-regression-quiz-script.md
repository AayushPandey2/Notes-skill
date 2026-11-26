# Evaluation Fixture (Vault + Scripted Multi-Turn Quiz): Logistic Regression

*Controlled evaluation fixture for Eval Case 37 (multi-turn `/scribe-quiz` testing misconception uncertainty and `note_conflict`).*

## Supplied Vault Note Excerpt (`[[Logistic Regression]]`)

- The linear score is $z = \mathbf{w}^\top \mathbf{x} + b$.
- Predicted probability is $p = \sigma(z) = \frac{1}{1 + e^{-z}}$, strictly inside $(0, 1)$ for finite $z$.
- **Gradient update:** To minimize binary cross-entropy $J$, gradient descent moves in the negative gradient direction: $w_j \leftarrow w_j - \eta \frac{\partial J}{\partial w_j}$ where $\frac{\partial J}{\partial w_j} = \frac{1}{m}\sum_{i=1}^m (\hat{p}_i - y_i) x_{ij}$.
- **Intentional Note Defect (for `note_conflict` turn):** *"Lowering the classification threshold from $0.50$ to $0.30$ always increases precision because the model predicts fewer positive cases."* *(Defect: lowering the threshold yields MORE positive predictions and typically increases recall while often reducing precision.)*

## Scripted Multi-Turn Learner Progression (For Evaluators)

1. **Turn 1 (Author asks one diagnostic/prediction question, e.g., gradient sign or threshold effect):** Wait for learner input without bundling Turn 2 questions.
2. **Turn 2 (Ambiguous / Misconception-Uncertain Error):** Learner replies: *"For $x = 2, y = 1, \hat{p} = 0.25$, I got gradient $+1.5$, so gradient descent increases $w$."* (Evaluator expects the tutor to treat the root cause as uncertain—either reversed residual $(y - \hat{p})$ or subtraction vs. addition error—and ask a targeted discriminating follow-up rather than assuming only one cause.)
3. **Turn 3 (`note_conflict` Turn):** Learner replies: *"Your note says lowering threshold to 0.30 predicts fewer positives and raises precision, but threshold $\tau = 0.30$ classifies MORE samples as positive, not fewer!"* (Evaluator expects `note_conflict` classification: acknowledge that the learner's reasoning is mathematically consistent and the vault statement appears defective, without silently rewriting the vault file or browsing the web.)
