# Evaluation Fixture (Source): Adam Optimizer Tutorial Excerpt

## How Adam Updates Parameters

Adam (Adaptive Moment Estimation) maintains exponential moving averages of the first moment (gradient mean, $m_t$) and the second raw moment (exponential moving average of squared gradients, $v_t$):

1. $m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t$
2. $v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$
3. Bias-corrected estimates: $\hat{m}_t = \frac{m_t}{1 - \beta_1^t}$ and $\hat{v}_t = \frac{v_t}{1 - \beta_2^t}$
4. Parameter update: $\theta_t = \theta_{t-1} - \alpha \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$

Because each parameter receives a scaled effective step size based on its historical squared-gradient magnitude, Adam often converges quickly during early training on sparse-gradient or deep architectures without extensive learning-rate warmup tuning. In practice, practitioners frequently prefer Adam as the default optimizer because it outperforms SGD across deep learning tasks.
