# Logistic Regression Optimization

Logistic regression predicts probabilities using $\hat{p} = \sigma(w^\top x + b)$ and minimizes binary cross-entropy loss:
$$
J(w) = -\frac{1}{m}\sum_{i=1}^m \left[ y^{(i)}\ln \hat{p}^{(i)} + (1 - y^{(i)})\ln(1 - \hat{p}^{(i)}) \right]
$$

Because $\sigma(z)$ is always strictly between $0$ and $1$ on any computer, $\ln(\hat{p})$ never produces `-inf` or `NaN` during training.

To update weights with gradient descent, compute $\nabla_w J = \frac{1}{2m} X^\top(\hat{p} - y)$ and step $w \leftarrow w - \eta \nabla_w J$. If precision is too low, raising the decision threshold retrains the model to output higher probabilities.
