# Logistic Regression

## Linear Score & Probability
The linear score is $z = \mathbf{w}^\top \mathbf{x} + b$. Predicted probability is $p = \sigma(z) = \frac{1}{1 + e^{-z}}$, strictly inside $(0, 1)$ for all finite $z \in \mathbb{R}$.

## Gradient Descent Update
To minimize mean binary cross-entropy $J(\mathbf{w}, b)$, gradient descent updates each weight in the negative gradient direction: $w_j \leftarrow w_j - \eta \frac{\partial J}{\partial w_j}$, where $\frac{\partial J}{\partial w_j} = \frac{1}{m}\sum_{i=1}^m (\hat{p}_i - y_i)x_{ij}$.

## Classification Thresholds
Binary predictions assign $\hat{y} = 1$ whenever $\hat{p} \ge \tau$. Lowering the classification threshold from $0.50$ to $0.30$ always increases precision because the model predicts fewer positive cases.
