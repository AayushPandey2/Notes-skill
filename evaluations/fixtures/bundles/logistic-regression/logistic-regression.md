---
id: eval-golden-logistic-regression
aliases:
  - Logistic Regression
topic: Logistic Regression
tags:
  - domain/ml
  - subject/machine-learning
  - topic/logistic-regression
nexttopics: []
---

# Logistic Regression

Logistic regression models binary event probabilities by linearly parameterizing conditional log-odds and fitting the parameters by minimizing binary cross-entropy. An optional penalty controls coefficient growth.

**Difficulty:** Intermediate (requires linear combinations, logarithm/exponential inverses, and single-variable calculus; multivariable chain-rule and Hessian steps are derived inline)

**Prerequisites:** Linear equations ($\mathbf{w}^\top\mathbf{x} + b$), inverse identities ($e^{\ln u} = u$), product/quotient/chain derivative rules, and positive semidefinite quadratic forms ($\mathbf{v}^\top A \mathbf{v} \ge 0$)

## Learning objectives
1. Derive the Bernoulli variance and explain why an unconstrained least-squares fit can leave the probability interval.
2. Derive the logistic sigmoid and odds-ratio weight interpretation from a linear log-odds assumption, connect scores to hyperplane decision geometry, and derive $\sigma'(z) = \sigma(z)(1 - \sigma(z))$ before likelihood differentiation.
3. Construct Binary Cross-Entropy (BCE) step by step from conditional Bernoulli likelihood and prove why BCE is globally convex while sigmoid squared error loses convexity in saturation tails.
4. Derive BCE scalar, indexed, and vectorized matrix gradients ($\nabla_{\mathbf{w}} J = \frac{1}{m}X^\top(\mathbf{p}-\mathbf{y})$) from first principles, trace one gradient update by hand, and explain both Gradient Descent anatomy and Newton–Raphson / IRLS curvature scaling.
5. Formulate $L_2$ regularization for linear separation, derive signed-logit numerical stability, and separate fitted probabilities from non-monotonic classification thresholding ($\tau$).

**Table of Contents**
- [[#1. Problem Formulation & Why Ordinary Least Squares Fails|1. Problem Formulation & OLS Failure]]
- [[#2. Probability, Odds, Log-Odds & Sigmoid Derivation|2. Log-Odds to Sigmoid Derivation]]
- [[#3. Odds-Ratio Interpretation & Sigmoid Derivative|3. Odds Ratios & Sigmoid Derivative]]
- [[#4. Bernoulli Likelihood to Binary Cross-Entropy Derivation|4. Bernoulli MLE to BCE Derivation]]
- [[#5. Chain-Rule & Scalar-to-Matrix Gradient Derivation|5. Chain-Rule & Matrix Gradients]]
- [[#6. Convexity, Hessian Geometry & Parameter Optimization|6. Convexity & Newton Optimization]]
- [[#7. L2 Regularization, Separation & Numerical Stability|7. L2 Regularization & Numerical Stability]]
- [[#8. Decision Thresholds, Evaluation & Model Limitations|8. Thresholds, Evaluation & Limitations]]
- [[#9. Mental Model, Notation Reference & Bundle Links|9. Mental Model & Bundle Links]]

---

## 1. Problem Formulation & Why Ordinary Least Squares Fails

A learner deciding whether an email is spam can ask two questions: how likely is it to be spam, and should it be filtered? A model can estimate a probability first. A threshold turns that estimate into a decision. The observed label $y_i$ records what actually happened for example $i$, with $1$ for spam and $0$ otherwise. Its features $\mathbf x_i$ might include a link count and whether the sender is known.

Write $p_i^\ast=P(Y_i=1\mid\mathbf x_i)$ for the underlying conditional probability. The bar means we are comparing outcomes for a fixed feature vector. Even with identical recorded features, two emails can have different labels. Write $\hat p_i$ for the probability assigned by the model and $\hat y_i$ for the thresholded prediction. The modeled probability may differ from $p_i^\ast$.

A binary random variable with this success probability is Bernoulli. Its mean is the probability-weighted average of the two outcomes, $0\cdot(1-p_i^\ast)+1\cdot p_i^\ast=p_i^\ast$. Since $0^2=0$ and $1^2=1$, its second moment is also $p_i^\ast$. Subtracting the square of the mean gives

$$
\operatorname{Var}(Y_i\mid\mathbf{x}_i)=p_i^\ast(1-p_i^\ast).
$$

> [!example]- Understand this formula step by step — Bernoulli variance
>
> Conditional variance is the expected squared deviation from the conditional mean. Suppress the condition $\mathbf{x}_i$ and write the true mean as $p$. Weight the squared deviations at $1$ and $0$ by their probabilities.
>
> $$
> \begin{aligned}
> \operatorname{Var}(Y\mid\mathbf x)
> &=p(1-p)^2+(1-p)p^2\\
> &=p(1-p)[(1-p)+p]=p(1-p).
> \end{aligned}
> $$
>
> The variance is $0.25$ at $p=0.5$ and zero at either deterministic endpoint.

A first attempt fits the affine prediction $wx+b$ by ordinary least squares (OLS). The derivative of the mean half-squared residual with respect to $b$ is the mean residual. Making it zero forces the line through $(\bar x,\bar y)$. Centering there reduces the slope calculation to the inner product of centered inputs and outputs divided by the squared norm of centered inputs.

$$
w_{\mathrm{OLS}}=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}
                        {\sum_i(x_i-\bar x)^2},
\qquad b_{\mathrm{OLS}}=\bar y-w_{\mathrm{OLS}}\bar x .
$$

> [!example]- Understand this formula step by step — Centered least squares
>
> For $m>0$, minimize $Q(w,b)=\frac1{2m}\sum_i(wx_i+b-y_i)^2$. Differentiating with respect to $b$ cancels the $1/2$ and multiplies each residual by its derivative $1$.
>
> $$
> 0=\frac{\partial Q}{\partial b}=w\bar x+b-\bar y
> \quad\Longrightarrow\quad b=\bar y-w\bar x .
> $$
>
> This minimizes $Q$ for fixed $w$, since the second derivative in $b$ is $1$. Substitute this intercept to obtain residual $w(x_i-\bar x)-(y_i-\bar y)$. Differentiating in $w$ multiplies each residual by $x_i-\bar x$. Set the derivative to zero and multiply by $m$:
>
> $$
> 0=w\sum_i(x_i-\bar x)^2-\sum_i(x_i-\bar x)(y_i-\bar y).
> $$
>
> The sum of centered squares is positive when the inputs vary. It gives positive curvature in $w$ after eliminating $b$ and can be divided out. For constant inputs, only the fitted constant is identifiable.
>
> For $x=(-2,-1,1,2)$ and $y=(0,0,1,1)$, the means are $0$ and $0.5$. The numerator is $1+0.5+0.5+1=3$ and the denominator is $4+1+1+4=10$. The fit has slope $0.3$ and intercept $0.5$.

The fit returns $-0.10$ at $x=-2$ and $1.10$ at $x=2$. An affine prediction with nonzero slope crosses the probability bounds on an unbounded input domain. Least squares is a fitting criterion. A Gaussian model with constant error variance adds a separate assumption, while the binary variance just derived depends on $p_i^\ast$.

An affine score still gives us a concise way to combine features. Each $w_jx_j$ is the contribution of feature $j$ in score units, and the intercept $b$ sets the score at the zero feature vector.

$$
z=b+\sum_{j=1}^n w_jx_j=b+\mathbf w^\top\mathbf x .
$$

A one-unit increase in $x_j$ adds $w_j$ to the score with the other predictors held fixed. To turn this unconstrained score into a probability, we need a scale that can represent every real number.

---

## 2. Probability, Odds, Log-Odds & Sigmoid Derivation

For $0<p<1$, the odds $p/(1-p)$ compare positive outcomes to negative outcomes. At $p=0.8$ the odds are $4$. Taking their natural logarithm gives a real number, with log-odds zero at $p=0.5$. This defines the **logit link**, which maps probability to score. In the model equations in this section, $p$ denotes the modeled probability at one feature vector. The sigmoid will map in the opposite direction. Choosing the logit is a modeling assumption. Probit and complementary log-log are alternative links.

Logistic regression models these conditional log-odds as a linear function of predictors:

$$
z = \mathbf{w}^\top \mathbf{x} + b = \ln\left(\frac{p}{1 - p}\right)
$$

Exponentiating removes the logarithm. Clearing the denominator then puts every term involving $p$ on one side.

$$
e^z=\frac{p}{1-p}
\quad\Longrightarrow\quad
e^z=p(1+e^z).
$$

Dividing by $1+e^z$ isolates $p$. Dividing numerator and denominator by $e^z$ gives the **logistic sigmoid**, the inverse link.

$$
\boxed{p = \sigma(z) = \frac{1}{1 + e^{-z}}}
$$

> [!example]- Understand this formula step by step — Log-odds to sigmoid
>
> 1. **Mathematical origin:** Start from the modeling assumption $z = \ln\left(\frac{p}{1 - p}\right)$ with $0 < p < 1$ so both $p$ and $1 - p$ are strictly positive.
> 2. **Symbol interpretation:** $z \in \mathbb{R}$ is the unconstrained linear score ($\mathbf{w}^\top\mathbf{x} + b$), $p \in (0, 1)$ is $P(Y=1 \mid \mathbf{x})$, and $1-p$ is $P(Y=0 \mid \mathbf{x})$.
> 3. **Remove the logarithm:** Exponentiate both sides (valid because $\exp$ and $\ln$ are inverse functions on $(0, +\infty)$):
>
> $$
> e^z = e^{\ln\left(\frac{p}{1 - p}\right)} = \frac{p}{1 - p}
> $$
>
> 4. **Clear the denominator:** Multiply both sides by $1 - p > 0$ and distribute $e^z$:
>
> $$
> e^z(1 - p) = p \implies e^z - p e^z = p
> $$
>
> 5. **Collect and isolate $p$:** Add $p e^z$ to both sides, factor out $p$, and divide by $1 + e^z > 0$:
>
> $$
> e^z = p(1 + e^z) \implies p = \frac{e^z}{1 + e^z}
> $$
>
> 6. **Normalize to standard reciprocal form:** Divide numerator and denominator by $e^z > 0$ so $z$ appears once with negative sign:
>
> $$
> p = \frac{e^z / e^z}{(1 + e^z)/e^z} = \frac{1}{e^{-z} + 1} = \frac{1}{1 + e^{-z}}
> $$
>
> 7. **Worked check & boundaries:** At $z = 3.0$, $\operatorname{odds} = e^{3.0} \approx 20.0855$ and $p = \frac{20.0855}{21.0855} = \frac{1}{1 + e^{-3}} \approx 0.9526$. Since $e^{-z} > 0$ for all finite $z \in \mathbb{R}$, denominator $1 + e^{-z} > 1$, guaranteeing $\sigma(z) \in (0, 1)$ strictly ($\lim_{z\to+\infty}\sigma(z)=1$, $\lim_{z\to-\infty}\sigma(z)=0$, $\sigma(0)=0.5$).

---

## 3. Odds-Ratio Interpretation & Sigmoid Derivative

### How a feature changes the odds
Exponentiating $z = \ln\left(\frac{p}{1-p}\right)$ yields $\operatorname{odds}(\mathbf{x}) = \exp(\mathbf{w}^\top\mathbf{x} + b)$. Consequently, a unit step in predictor $x_j$ scales modeled odds multiplicatively by $e^{w_j}$:

$$
\boxed{\frac{\operatorname{odds}(\dots, x_j + 1, \dots)}{\operatorname{odds}(\dots, x_j, \dots)} = e^{w_j}}
$$

> [!example]- Understand this formula step by step — Odds multiplier
>
> 1. **Starting identity:** Let $\mathbf{x}'$ agree with $\mathbf{x}$ on every coordinate except $x_j' = x_j + 1$. Then $z' = \mathbf{w}^\top \mathbf{x}' + b = (\mathbf{w}^\top \mathbf{x} + b) + w_j = z + w_j$.
> 2. **Exponentiate and factor:** Using $e^{a+b} = e^a e^b$:
>
> $$
> \frac{\operatorname{odds}(\mathbf{x}')}{\operatorname{odds}(\mathbf{x})} = \frac{e^{z + w_j}}{e^z} = \frac{e^z e^{w_j}}{e^z} = e^{w_j}
> $$
>
> 3. **Interpretation & limitation:** A $+1$ change in $x_j$ multiplies odds by $e^{w_j}$ holding other covariates fixed (for example, $w_j = \ln 2 \approx 0.6931$ doubles odds). Note this holds only under the linear log-odds specification and depends directly on $x_j$'s measurement units.

The odds multiplier is constant for a fixed feature increment. The change in probability depends on where the original score lies on the sigmoid.

### Sigmoid Derivative (Derived Before Likelihood Optimization)
Fitting the model requires knowing how changes in score affect probability. Treat $\sigma(z)=(1+e^{-z})^{-1}$ as a composition. The chain rule contributes two minus signs, one from the reciprocal and one from the exponent.

$$
\sigma'(z)=\frac{e^{-z}}{(1+e^{-z})^2}.
$$

Factoring the denominator lets us express the derivative using the original probability and its complement.

$$
\boxed{\sigma'(z) = \sigma(z)\bigl(1 - \sigma(z)\bigr)}
$$

> [!example]- Understand this formula step by step — Sigmoid derivative and symmetry
>
> 1. **Mathematical origin:** Rewrite $\sigma(z) = (1 + e^{-z})^{-1}$ as a composition $u^{-1}$ with inner function $u(z) = 1 + e^{-z}$.
> 2. **Chain rule differentiation:** Differentiating wrt $z$ applies the power rule $\frac{d}{du}(u^{-1}) = -u^{-2}$ multiplied by $\frac{du}{dz} = -e^{-z}$:
>
> $$
> \sigma'(z) = -(1 + e^{-z})^{-2}(-e^{-z}) = \frac{e^{-z}}{(1 + e^{-z})^2}
> $$
>
> 3. **Factor to express cleanly in $\sigma(z)$:** Split one factor $\frac{1}{1+e^{-z}} = \sigma(z)$ and algebraically rewrite the remaining factor $\frac{e^{-z}}{1 + e^{-z}} = \frac{(1 + e^{-z}) - 1}{1 + e^{-z}} = 1 - \frac{1}{1 + e^{-z}} = 1 - \sigma(z)$:
>
> $$
> \sigma'(z) = \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} = \sigma(z)\bigl(1 - \sigma(z)\bigr)
> $$
>
> 4. **Symmetry identity:** Checking $\sigma(-z) = \frac{1}{1+e^z} = \frac{e^{-z}}{e^{-z}+1} = 1 - \sigma(z)$ confirms $\sigma'(-z) = \sigma'(z)$ (even sensitivity around $z=0$).
>
> Complete the square to bound the derivative at $p=\sigma(z)$.
>
> $$
> p(1-p)=\frac14-\left(p-\frac12\right)^2.
> $$
>
> The square vanishes only at $p=0.5$, giving $\sigma'(0)=0.25$. At $z=3$, the derivative is approximately $0.9526(0.0474)=0.0452$. It approaches zero in either tail.

A shift in score has its greatest local effect near $p=0.5$. Its derivative has the same form as the conditional variance, a factor that will cancel when we differentiate the loss.

---

## 4. Bernoulli Likelihood to Binary Cross-Entropy Derivation

At each input the model assigns probability $\hat p_i=\sigma(\mathbf w^\top\mathbf x_i+b)$ to label $1$ and $1-\hat p_i$ to label $0$. The binary label $y_i$ selects the corresponding factor.

$$
P_{\mathbf w,b}(Y_i=y_i\mid\mathbf x_i)=\hat p_i^{y_i}(1-\hat p_i)^{1-y_i}.
$$

Under conditional independence given the design, the joint likelihood $L$ multiplies these masses. The logarithm preserves their ordering and turns the product into a sum.

$$
\begin{aligned}
L(\mathbf w,b)&=\prod_{i=1}^m \hat p_i^{y_i}(1-\hat p_i)^{1-y_i},\\
\ln L(\mathbf w,b)&=\sum_{i=1}^m
  [y_i\ln \hat p_i+(1-y_i)\ln(1-\hat p_i)].
\end{aligned}
$$

Negation turns maximization into minimization. Dividing by $m>0$ gives mean **binary cross-entropy** (BCE).

$$
\boxed{J(\mathbf w,b)=-\frac1m\sum_{i=1}^m
  [y_i\ln \hat p_i+(1-y_i)\ln(1-\hat p_i)]}
$$

> [!example]- Understand this formula step by step — Bernoulli likelihood to cross-entropy
>
> For label $1$, the mass is $\hat p_i^1(1-\hat p_i)^0=\hat p_i$. For label $0$, it is $\hat p_i^0(1-\hat p_i)^1=1-\hat p_i$. Conditional independence permits multiplying the selected positive factors. Use the log of a product, then the log of a power.
>
> $$
> \begin{aligned}
> \ln L
> &=\sum_i\ln[\hat p_i^{y_i}(1-\hat p_i)^{1-y_i}]\\
> &=\sum_i[\ln(\hat p_i^{y_i})+\ln((1-\hat p_i)^{1-y_i})]\\
> &=\sum_i[y_i\ln \hat p_i+(1-y_i)\ln(1-\hat p_i)].
> \end{aligned}
> $$
>
> For two parameter choices, $L_A>L_B$ implies $\ln L_A>\ln L_B$ and $-\ln L_A/m<-\ln L_B/m$. The ordering equivalence holds even when no finite optimum exists. Adding logs also avoids forming a tiny product in floating point.
>
> With $y_i=1$, predicting $\hat p_i=0.90$ costs about $0.1054$, while $\hat p_i=0.01$ costs about $4.6052$. Larger loss means the model assigned less probability to the observed outcome.

### Expressing BCE directly in the score

Substitute $p=e^z/(1+e^z)$, so $1-p=1/(1+e^z)$. Taking logs gives the same term $-\ln(1+e^z)$ in both log probabilities. Their weights inside BCE add to one, leaving a single logarithm.

$$
\boxed{\ell(z,y)=\ln(1+e^z)-yz}
$$

> [!example]- Understand this formula step by step — Cross-entropy in logit form
>
> Apply the log of a quotient to positive arguments and use $\ln(e^z)=z$.
>
> $$
> \begin{aligned}
> \ln p&=z-\ln(1+e^z),\\
> \ln(1-p)&=-\ln(1+e^z).
> \end{aligned}
> $$
>
> Substitute the two logs into the loss and combine coefficients of the common term.
>
> $$
> \begin{aligned}
> \ell(z,y)
> &=-y[z-\ln(1+e^z)]+(1-y)\ln(1+e^z)\\
> &=-yz+[y+(1-y)]\ln(1+e^z)\\
> &=\ln(1+e^z)-yz .
> \end{aligned}
> $$
>
> At $z=0$, either label costs $\ln 2$, matching $-\ln 0.5$.

This form exposes curvature in the score. To update the model we also need to carry the score derivative back through each feature.

---

## 5. Chain-Rule & Scalar-to-Matrix Gradient Derivation

### Partial Derivatives via Exact Factor Cancellation
A partial derivative asks what changes when one parameter moves while all others are held fixed. The gradient collects these derivatives into one vector. The derivative of one example's BCE with respect to its probability has denominator $\hat p_i(1-\hat p_i)$. Moving back through the sigmoid multiplies by exactly that factor. For a finite score, $0<\hat p_i<1$ and the factors cancel.

$$
\frac{\partial\ell_i}{\partial z_i}
=\frac{\hat p_i-y_i}{\hat p_i(1-\hat p_i)}\hat p_i(1-\hat p_i)=\hat p_i-y_i .
$$

A weight shifts each score in proportion to the corresponding feature value. The intercept shifts every score by the same amount. The chain rule gives the two derivatives of the mean loss.

$$
\boxed{
\begin{aligned}
\frac{\partial J}{\partial w_j}&=\frac1m\sum_i(\hat p_i-y_i)x_{ij},\\
\frac{\partial J}{\partial b}&=\frac1m\sum_i(\hat p_i-y_i).
\end{aligned}}
$$

> [!example]- Understand this formula step by step — Weight and intercept gradients
>
> Differentiate $-\ln \hat p_i$ and $-\ln(1-\hat p_i)$ with respect to $\hat p_i$ using the chain rule. Use a common denominator to combine the terms.
>
> $$
> \begin{aligned}
> \frac{\partial\ell_i}{\partial \hat p_i}
> &=-\frac{y_i}{\hat p_i}+\frac{1-y_i}{1-\hat p_i}\\
> &=\frac{-y_i(1-\hat p_i)+\hat p_i(1-y_i)}{\hat p_i(1-\hat p_i)}\\
> &=\frac{\hat p_i-y_i}{\hat p_i(1-\hat p_i)} .
> \end{aligned}
> $$
>
> Multiply by $\partial \hat p_i/\partial z_i=\hat p_i(1-\hat p_i)$ from the sigmoid derivative. Then use $\partial z_i/\partial w_j=x_{ij}$ and $\partial z_i/\partial b=1$:
>
> $$
> \begin{aligned}
> \frac{\partial\ell_i}{\partial w_j}
> &=\frac{\partial\ell_i}{\partial z_i}\frac{\partial z_i}{\partial w_j}
>   =(\hat p_i-y_i)x_{ij},\\
> \frac{\partial\ell_i}{\partial b}
> &=\frac{\partial\ell_i}{\partial z_i}\frac{\partial z_i}{\partial b}
>   =\hat p_i-y_i .
> \end{aligned}
> $$
>
> Averaging follows from linearity. For $y_i=1$ and $\hat p_i=0.01$, the score derivative is $-0.99$, so the confidently wrong example still produces a large score gradient. The extra sigmoid factor cancels at the output loss. Gradient magnitude elsewhere still depends on features and, in a neural network, the derivatives of earlier layers.

### Scalar-to-Vector-to-Matrix Gradient Construction
Stack the $m$ feature vectors as the rows of $X\in\mathbb R^{m\times n}$. Each weight derivative is the dot product of one feature column and the residual vector $\hat{\mathbf p}-\mathbf y$. Rows of $X^\top$ are precisely those feature columns, so one matrix product computes all $n$ derivatives.

$$
\boxed{\nabla_{\mathbf{w}} J = \frac{1}{m}X^\top(\hat{\mathbf p} - \mathbf{y})}
$$

> [!example]- Understand this formula step by step — Indexed gradients to matrix form
>
> 1. **Stage 1 (1 parameter, scalar):** $\frac{\partial J}{\partial w} = \frac{1}{m}\sum_{i=1}^m (\hat p_i - y_i)x_i$.
> 2. **Stage 2 ($n$ parameters, indexed sums):** For feature column $j \in \{1, \dots, n\}$, weight $w_j$ accumulates residual-weighted entries down column $j$: $\left[\nabla_{\mathbf{w}} J\right]_j = \frac{1}{m}\sum_{i=1}^m x_{ij}(\hat p_i - y_i)$.
> Row $j$ of $X^\top$ contains the $m$ measurements for feature $j$. Its dot product with the $m$ residuals produces one gradient component. Hence the product has $n$ entries.
>
> For three observations, use
>
> $$
> X=\begin{bmatrix}1&2\\2&1\\3&0\end{bmatrix},
> \qquad \mathbf r=\begin{bmatrix}0.2\\-0.4\\0.1\end{bmatrix}.
> $$
>
> The first row of $X^\top$ gives $1(0.2)+2(-0.4)+3(0.1)=-0.3$. The second gives $2(0.2)+1(-0.4)+0(0.1)=0$. Averaging produces gradient $(-0.1,0)^\top$. At this iterate the second feature has zero net contribution even though individual rows contribute.

At a finite unregularized stationary point, $X^\top\mathbf r=\mathbf 0$ and $\mathbf 1^\top\mathbf r=0$. The first equation balances the residuals against each feature column. The intercept condition balances their total. Individual predictions can still differ from their observed labels. With a weight penalty, feature residual sums offset the penalty gradient, while the intercept balance is unchanged.

### Why gradient descent subtracts the gradient

Write $\boldsymbol\theta=(\mathbf w^\top,b)^\top$ and let $g_t=\nabla_{\boldsymbol\theta}J(\boldsymbol\theta_t)$. The first-order change for a proposed step is $g_t^\top\Delta$. Aligning the step opposite the gradient makes this change negative when $g_t\ne0$.

$$
\boxed{\boldsymbol\theta_{t+1}=\boldsymbol\theta_t-\eta g_t,\qquad \eta>0}
$$

> [!example]- Understand this formula step by step — Gradient descent from local slope
>
> For a fixed Euclidean step length, Cauchy–Schwarz bounds the first-order change below by $-\|g_t\|_2\|\Delta\|_2$, attained by an antiparallel step. Choose its length as $\eta\|g_t\|_2$ so the step shrinks with the gradient. First-order Taylor expansion gives
>
> $$
> J(\boldsymbol\theta_t-\eta g_t)-J(\boldsymbol\theta_t)
> =-\eta\|g_t\|_2^2+o(\eta).
> $$
>
> At a fixed nonstationary iterate the negative linear term dominates for sufficiently small positive $\eta$. Large steps can raise the loss. If $g_t=0$, this update leaves the iterate unchanged.

### Hand Trace on Shared 4-Point Fixture ($w_0 = 0, b_0 = 0, \eta = 1.0$)
The four-point dataset from the least-squares example has $x=(-2,-1,1,2)$ and $y=(0,0,1,1)$. At the zero iterate every logit is zero and every probability is $0.50$.

**Prediction pass:**

| Sample $i$ | Feature $x_i$ | True Label $y_i$ | Logit $z_i$ | Predicted $\hat p_i$ |
|---:|---:|---|---:|---:|
| 1 | $-2$ | `0 — Negative` | $0.00$ | $0.50$ |
| 2 | $-1$ | `0 — Negative` | $0.00$ | $0.50$ |
| 3 | $+1$ | `1 — Positive` | $0.00$ | $0.50$ |
| 4 | $+2$ | `1 — Positive` | $0.00$ | $0.50$ |

**Learning update pass ($J(0,0) = -\ln(0.5) \approx 0.6931$):**

| Sample $i$ | Feature $x_i$ | Residual $\hat p_i - y_i$ | Gradient Term $(\hat p_i - y_i)x_i$ |
|---:|---:|---:|---:|
| 1 | $-2$ | $+0.50$ | $-1.00$ |
| 2 | $-1$ | $+0.50$ | $-0.50$ |
| 3 | $+1$ | $-0.50$ | $-0.50$ |
| 4 | $+2$ | $-0.50$ | $-1.00$ |

- Mean gradients: $\frac{\partial J}{\partial w} = \frac{-3.00}{4} = -0.75$ and $\frac{\partial J}{\partial b} = 0.00$.
- Step 1 update ($\eta = 1.0$): $w_1 = 0 - 1.0(-0.75) = 0.75$, $b_1 = 0.00$, shifting probabilities to $\hat{\mathbf p} \approx [0.1824, 0.3208, 0.6792, 0.8176]$ and lowering BCE to $J(0.75, 0) \approx 0.2941$.

---

## 6. Convexity, Hessian Geometry & Parameter Optimization

The score gradient is nonlinear in the parameters, so solving the stationarity equations generally requires iteration. Curvature tells us whether the objective is convex and helps explain how a second-order step differs from gradient descent.

### Global Convexity of Binary Cross-Entropy
The Hessian collects the rates at which gradient components change when parameters move. An outer product of a column and its transpose records every pairwise component product. To read curvature along a direction, multiply the Hessian on both sides by that direction. The logit loss gives the first derivative $\hat p_i-y_i$. Differentiate again in $z_i$ to get $d_i=\hat p_i(1-\hat p_i)$, which is positive at every finite score. Let $\tilde{\mathbf x}_i=(\mathbf x_i^\top,1)^\top$ and stack these rows in $\tilde X=[X,\mathbf 1]$. Each score is affine in $\boldsymbol\theta$, so the chain rule turns its scalar curvature into a weighted outer product.

$$
\nabla^2_{\boldsymbol\theta}\ell_i=d_i\tilde{\mathbf x}_i\tilde{\mathbf x}_i^\top.
$$

The mean of these outer products is a positive semidefinite Hessian, because its quadratic form in any direction is a sum of squares with nonnegative weights.

$$
\boxed{H=\nabla_{\boldsymbol\theta}^2J=\frac1m\tilde X^\top D\tilde X\succeq 0,
\qquad D=\operatorname{diag}(d_1,\ldots,d_m)}
$$

> [!example]- Understand this formula step by step — Hessian and convexity
>
> 1. **Scalar first and second logit derivatives:** Differentiating $\ell(z, y) = \ln(1 + e^z) - yz$ wrt $z$ gives $\frac{\partial \ell}{\partial z} = \frac{e^z}{1+e^z} - y = \sigma(z) - y$. Differentiating a second time uses Section 3's identity:
>
> $$
> \frac{\partial^2 \ell}{\partial z^2} = \sigma'(z) = \sigma(z)\bigl(1 - \sigma(z)\bigr) \ge 0
> $$
>
> 2. **Chain rule to augmented parameters:** Since $z_i = \tilde{\mathbf{x}}_i^\top \boldsymbol{\theta}$, $\nabla_{\boldsymbol{\theta}} \ell_i = (\hat p_i - y_i)\tilde{\mathbf{x}}_i$, and differentiating once more gives rank-1 Hessian $\nabla_{\boldsymbol{\theta}}^2 \ell_i = \hat p_i(1 - \hat p_i)\tilde{\mathbf{x}}_i\tilde{\mathbf{x}}_i^\top$.
> 3. **Matrix assembly & positive semidefiniteness:** Summing $\frac{1}{m}\sum_{i=1}^m d_i \tilde{\mathbf{x}}_i\tilde{\mathbf{x}}_i^\top = \frac{1}{m}\tilde{X}^\top D \tilde{X}$ with $d_i = \hat p_i(1 - \hat p_i) \ge 0$. For every vector $\mathbf{v} \in \mathbb{R}^{n+1}$, quadratic form $\mathbf{v}^\top \nabla^2 J\,\mathbf{v} = \frac{1}{m}\sum_{i=1}^m d_i (\tilde{\mathbf{x}}_i^\top \mathbf{v})^2 \ge 0$. Therefore $J$ is **globally convex** (strictly convex whenever $\tilde{X}$ has full column rank and $\hat p_i \in (0, 1)$).

The Hessian is positive definite at every finite iterate when $\tilde X$ has full column rank. A deficient design has a null direction that leaves all scores unchanged.

### Why squared error after the sigmoid has different curvature

With label $1$, the half-squared probability error gives a score derivative $-p(1-p)^2$. A second derivative can change sign because the remaining factor $3p-1$ crosses zero.

$$
\frac{\partial^2 \ell_{\mathrm{sq}}}{\partial z^2}=p(1-p)^2(3p-1).
$$

> [!example]- Understand this formula step by step — Negative curvature of sigmoid squared error
>
> For $y=1$ take $\ell_{\mathrm{sq}}=\frac12(p-1)^2$. Its derivative in $p$ is $p-1$. Multiplying by $\sigma'(z)=p(1-p)$ gives $-p(1-p)^2$.
>
> $$
> \frac{d}{dp}\big[-p(1-p)^2\big]
> =-(1-p)^2+2p(1-p)=(1-p)(3p-1).
> $$
>
> Apply $dp/dz=p(1-p)$ again to obtain the score curvature. For $p=0.1$, the squared-error curvature is $-0.0567$ and the BCE curvature is $0.09$. Negative curvature whenever $p<1/3$ rules out global convexity in general. The shape of an aggregate squared-error loss still depends on the dataset.

### Newton's method and local curvature

Gradient descent uses one learning rate in every direction. Newton's method approximates the objective near the current augmented parameter vector $\boldsymbol\theta_t$ using the gradient $g_t$ and Hessian $H_t$ at that point. The step $\Delta$ enters a quadratic model:

$$
q_t(\Delta)=J(\boldsymbol\theta_t)+g_t^\top\Delta+
              \tfrac12\Delta^\top H_t\Delta .
$$

The linear part contributes $g_t$ to the step derivative, and the symmetric quadratic part contributes $H_t\Delta$. If $H_t$ is positive definite, setting their sum to zero yields the unique minimizer of the local model.

$$
\boxed{H_t\Delta_t=-g_t,\qquad
       \boldsymbol\theta_{t+1}=\boldsymbol\theta_t+\Delta_t}
$$

> [!example]- Understand this formula step by step — Newton's linear system
>
> The second-order Taylor polynomial gives $q_t$ for a twice differentiable objective. In component $j$, differentiating the quadratic produces
>
> $$
> \frac12\sum_k (H_t)_{jk}\Delta_k
> +\frac12\sum_k (H_t)_{kj}\Delta_k=(H_t\Delta)_j.
> $$
>
> Hessian symmetry combines the two terms. The stationarity condition is $g_t+H_t\Delta=0$. Positive definiteness makes this stationary point a minimum of $q_t$. In an eigenvector direction of curvature $h>0$, the component is $-g/h$. A direction with curvature $h=4$ and gradient component $g=-2$ therefore gets a step of $0.5$.
>
> An invertible $H_t$ gives the algebraic expression $\Delta=-H_t^{-1}g_t$. In code, solve the linear system. A deficient design can make $H_t$ singular, and a nearly separated fit can leave very small curvature even with full rank.

The undamped method converges quadratically from sufficiently close to a finite minimizer with nonsingular Hessian and locally Lipschitz Hessian. Away from that neighborhood, damping or a line search can control the step. Convexity alone gives neither a finite minimizer nor a guarantee of fast convergence.

### Why the same Newton step is weighted least squares

Write $\mathbf z_t=\tilde X\boldsymbol\theta_t$ and $\hat{\mathbf p}_t=\sigma(\mathbf z_t)$ elementwise. The diagonal weight $d_i=\hat p_i(1-\hat p_i)$ records the local curvature of each example. To encode the score residual in a least-squares target, add its curvature-scaled correction to the current score.

$$
\mathbf u_t=\mathbf z_t+D_t^{-1}(\mathbf y-\hat{\mathbf p}_t).
$$

The normal equations for a weighted fit to $\mathbf u_t$ yield the same system for the Newton increment. Recompute both the weights and the working response after each step. This is **iteratively reweighted least squares** (IRLS).

$$
\boxed{\boldsymbol\theta_{t+1}=\arg\min_{\boldsymbol\beta}
 \frac1{2m}(\tilde X\boldsymbol\beta-\mathbf u_t)^\top
 D_t(\tilde X\boldsymbol\beta-\mathbf u_t)}
$$

> [!example]- Understand this formula step by step — Newton to IRLS
>
> At finite logits $D_t$ is positive diagonal in exact arithmetic. From the gradient and Hessian already derived, multiplying the Newton system by $m$ gives
>
> $$
> \tilde X^\top D_t\tilde X\Delta_t=\tilde X^\top(\mathbf y-\hat{\mathbf p}_t).
> $$
>
> Substitute $\Delta_t=\boldsymbol\theta_{t+1}-\boldsymbol\theta_t$ and move the current iterate term to the right. Factor out $\tilde X^\top D_t$:
>
> $$
> \begin{aligned}
> \tilde X^\top D_t\tilde X\boldsymbol\theta_{t+1}
> &=\tilde X^\top[D_t\mathbf z_t+\mathbf y-\hat{\mathbf p}_t]\\
> &=\tilde X^\top D_t\mathbf u_t .
> \end{aligned}
> $$
>
> Differentiating the weighted squared residual in the boxed objective gives $\tilde X^\top D_t(\tilde X\boldsymbol\beta-\mathbf u_t)/m$. Setting this derivative to zero reproduces the system. A full-column-rank $\tilde X$ makes this weighted fit unique.
>
> On the four-point fixture at zero weights, each weight is $1/4$ and $\mathbf u_0=(-2,-2,2,2)^\top$. Centered weighted least squares has slope $12/10=1.2$ and intercept $0$. The Newton system gives the same slope step from gradient $-0.75$ and slope curvature $0.625$. Near numerical saturation, prefer the Newton right-hand side directly to dividing by small $d_i$.

From the same zero iterate, the hand trace used unit-step gradient descent and reached $w=0.75$. Newton and IRLS reached $w=1.2$ because the slope curvature was $0.625$. With $\lambda=0.05$, the initial gradient is unchanged and Newton divides by $0.625+0.05$, reaching $w=10/9$. The three updates have the same zero intercept on this symmetric dataset. The larger Newton step reflects local curvature on this fixture. Outside the local regime, compare loss before accepting a full step. The four-point example can keep improving with larger separating scores, which raises a separate question about whether a finite optimum exists.

---

## 7. L2 Regularization, Separation & Numerical Stability

### L2 Regularization & Conditions for a Unique Finite Optimum
For **complete separation**, some augmented parameter vector $\boldsymbol\theta_0=(\mathbf w_0^\top,b_0)^\top$ gives a positive signed margin $(2y_i-1)z_i$ for every sample. Multiplying the entire vector, including the intercept, by $a>0$ multiplies every margin by $a$. As $a$ grows, the probability of each observed label tends to one and every BCE term goes to zero. At finite scores every such term is still positive, so the unregularized loss has no finite minimizer in this case.

Penalize the squared norm of the weights to make continued growth costly. Differentiating the penalty adds a term proportional to each weight, with an unchanged intercept derivative.

$$
\boxed{
\begin{aligned}
J_\lambda(\mathbf w,b)&=J(\mathbf w,b)+\frac{\lambda}{2}\|\mathbf w\|_2^2,\\
\nabla_{\mathbf w}J_\lambda&=\frac1mX^\top(\hat{\mathbf p}-\mathbf y)+\lambda\mathbf w .
\end{aligned}}
$$

> [!example]- Understand this formula step by step — Separation and the L2 penalty
>
> Expand the norm into $\sum_k w_k^2$. Terms with $k\ne j$ are constant in $w_j$. Differentiating $w_j^2$ contributes $2w_j$, which cancels the $1/2$. The penalty contains no $b$, so the intercept derivative remains the mean probability residual.
>
> For finite inputs, $\lambda>0$ and both classes present, bounded objective forces $\mathbf w$ to stay bounded. If $b$ escapes to $+\infty$, a negative label has loss going to infinity. If $b$ escapes to $-\infty$, a positive label has loss going to infinity. Thus sublevel sets are bounded and closed, giving a finite minimizer. With only one class, the unpenalized intercept can escape.
>
> For a direction $(\mathbf v,c)$, the penalty adds $\lambda\|\mathbf v\|^2$ to the BCE Hessian quadratic form. This is positive if $\mathbf v\ne0$. If only $c\ne0$, the BCE form itself is positive because the intercept column is all ones and each $d_i>0$. The full Hessian is positive definite at finite parameters, giving strict convexity and a unique minimizer. Curvature in the intercept can approach zero far from the optimum.

Setting the unpenalized intercept derivative to zero at a finite optimum gives

$$
\frac1m\sum_i \hat p_i=\frac1m\sum_i y_i .
$$

The average fitted training probability equals the observed positive fraction for this unweighted fit. This equality alone says nothing about calibration across subgroups or prevalence in a shifted population.

To match a library with summed loss, compare objectives before comparing parameters. For the unweighted L-BFGS setup in the [[logistic-regression-lab|Logistic Regression - Experimental Lab]], write the equivalent summed objective as $C\sum_i\ell_i+\|\mathbf w\|^2/2$. Divide by $mC$ to recover mean loss with a penalty coefficient of $1/(2mC)$.

$$
\boxed{C=\frac1{m\lambda}}
$$

> [!example]- Understand this formula step by step — Mean-to-sum penalty conversion
>
> Scaling by a positive constant preserves minimizers. For $C>0$ and $m>0$,
>
> $$
> \frac{C\sum_i\ell_i+\frac12\|\mathbf w\|^2}{mC}
> =\frac1m\sum_i\ell_i+\frac{1}{2mC}\|\mathbf w\|^2 .
> $$
>
> Matching the coefficient $\lambda/2$ gives $\lambda=1/(mC)$ and the boxed conversion for $\lambda>0$. With $m=4$ and $\lambda=0.05$, use $C=5$. The conversion assumes identical intercept treatment, unweighted observations and these objective conventions.

### Overflow-Safe Sigmoid & Subtraction-Free Logit BCE
For large negative scores, evaluating $e^{-z}$ directly can overflow. For $z<0$, multiply numerator and denominator by $e^z$, which is bounded by one. Let $t=e^{-|z|}$, so either branch uses the same bounded exponent.

$$
\sigma(z)=
\begin{cases}
1/(1+t),&z\ge 0,\\
t/(1+t),&z<0.
\end{cases}
$$

> [!example]- Understand this formula step by step — Overflow-safe sigmoid
>
> At $z\ge0$, $t=e^{-z}$ and the original denominator is already bounded by two. At $z<0$, $t=e^z$ and multiplying by $t/t$ gives
>
> $$
> \frac{1}{1+e^{-z}}=\frac{e^z}{e^z+e^z e^{-z}}=\frac{t}{1+t}.
> $$
>
> At $z=0$ both forms give $1/2$. At $z=-1000$ the bounded exponential can underflow to zero in floating point without an overflowing intermediate. Finite precision can round the probability to an endpoint even though the exact sigmoid remains in $(0,1)$.

Computing BCE as $\ln(1+e^z)-yz$ can lose the difference between two nearly equal terms. At $z=50$ and $y=1$, the true loss is about $1.93\times10^{-22}$. Select the logit sign using the label before taking the logarithm, using $\sigma(-z)=1-\sigma(z)$ for the negative class.

$$
\boxed{\ell(z, y) = \ln\Bigl(1 + e^{(1 - 2y)z}\Bigr), \qquad y \in \{0, 1\}}
$$

> [!example]- Understand this formula step by step — Stable BCE from signed logits
>
> 1. **Case $y = 1$:** Multiplier $(1 - 2y) = -1$, giving $-\ln \sigma(z) = \ln(1 + e^{-z})$. At $z = 50$, `logaddexp(0, -50)` preserves $e^{-50} \approx 1.93 \times 10^{-22}$ without subtracting nearly equal terms.
> 2. **Case $y = 0$:** Multiplier $(1 - 2y) = +1$, giving $-\ln(1 - \sigma(z)) = -\ln\sigma(-z) = \ln(1 + e^{+z})$.
> 3. **Applicability limit:** Exact for hard binary labels $y \in \{0, 1\}$; soft fractional targets $y \in (0, 1)$ require convex weighting $(1-y)\ln(1+e^z) + y\ln(1+e^{-z})$.

### Preserving small gradients in floating point

Even when softplus preserves the loss, subtracting $1$ from a rounded probability can erase the gradient. Put $s=1-2y$. Applying the chain rule to $\ln(1+e^{sz})$ gives

$$
\frac{\partial\ell}{\partial z}
=\frac{s e^{sz}}{1+e^{sz}}
=s\,\sigma(sz).
$$

> [!example]- Understand this formula step by step — Stable signed-logit gradient
>
> The outer derivative of $\ln(1+u)$ is $1/(1+u)$. The inner derivative of $u=e^{sz}$ is $s e^{sz}$, since the binary target holds $s$ fixed. Combining the derivatives gives the displayed relation. For $y=0$ it is $\sigma(z)$. For $y=1$ it is $-\sigma(-z)$, equal in exact arithmetic to $\sigma(z)-1$ by sigmoid symmetry.
>
> For $z=50$ and $y=1$, the direct subtraction rounds to zero in float64. The signed expression retains a derivative near $-1.93\times10^{-22}$. Extremely small values can still underflow.

---

## 8. Decision Thresholds, Evaluation & Model Limitations

### From probabilities to a decision boundary

For a fixed fit, predict class $1$ whenever $p\ge\tau$. If $0<\tau<1$, applying the increasing logit to both sides preserves the inequality. The boundary is the score at equality.

$$
\begin{aligned}
p\ge\tau &\iff \mathbf w^\top\mathbf x+b\ge\ln\frac{\tau}{1-\tau},\\
\mathbf w^\top\mathbf x&=\ln\frac{\tau}{1-\tau}-b
\qquad\text{on the boundary}.
\end{aligned}
$$

> [!example]- Understand this formula step by step — Threshold geometry
>
> The logit is increasing as the composition of increasing functions $p/(1-p)$ and $\ln$. Applying it to $p=\sigma(z)$ gives $z$, and subtracting $b$ isolates the feature dot product at equality. For $\mathbf w\ne0$, changes $\Delta\mathbf x$ satisfying $\mathbf w^\top\Delta\mathbf x=0$ leave the dot product unchanged. These directions form an $(n-1)$-dimensional subspace, so the boundary is an affine hyperplane normal to $\mathbf w$.
>
> With $\tau=0.5$, the logit threshold is $0$. For $w=0.75$ and $b=0$, this places the boundary at $x=0$. If $\mathbf w=0$, the model predicts a constant probability and the decision is constant. For finite scores the endpoint thresholds $0$ and $1$ also yield constant decisions.

> [!question] What score produces a probability of 0.8?
> Keep the fitted model fixed and reconstruct the logit before thinking about any decision threshold.
> > [!success]- Reveal Answer
> > The odds are $0.8/(1-0.8)=4$, so the score is $\ln 4\approx1.386$.

Increasing $\tau$ keeps the fitted weights and probabilities fixed and removes some predicted positives. True positives and false positives can both fall. Precision is their ratio after conditioning on predicted positives, so its direction depends on which cases leave the set.

| Case $i$ | Predicted Probability $\hat p_i$ | Actual Class $y_i$ | Decision ($\tau = 0.50$) | Decision ($\tau = 0.70$) |
|---:|---:|---|---|---|
| 1 | $0.95$ | `1 — Positive` | `TP` | `TP` |
| 2 | $0.85$ | `0 — Negative` | `FP` | `FP` |
| 3 | $0.65$ | `1 — Positive` | `TP` | `FN` |
| 4 | $0.55$ | `1 — Positive` | `TP` | `FN` |
| 5 | $0.40$ | `0 — Negative` | `TN` | `TN` |
| 6 | $0.20$ | `0 — Negative` | `TN` | `TN` |

- At $\tau = 0.50$: `TP = 3, FP = 1` $\implies$ **Precision = $75.0\%$ (`3/4`)**, **Recall = $100.0\%$ (`3/3`)**.
- At $\tau = 0.70$: dropping true positives at $0.65$ and $0.55$ while keeping false positive $0.85$ gives `TP = 1, FP = 1` $\implies$ **Precision drops to $50.0\%$ (`1/2`)** alongside **Recall = $33.3\%$ (`1/3`)**.

For thresholded decisions, **precision** is the share of predicted positives that are truly positive, and **recall** is the share of actual positives recovered. Their denominators are $\mathrm{TP}+\mathrm{FP}$ and $\mathrm{TP}+\mathrm{FN}$ respectively, and a zero denominator leaves the corresponding ratio undefined without a stated convention. When both ratios are defined and positive, their harmonic mean is $F_1$. Substituting the two denominators into the reciprocal form of the harmonic mean gives the count formula:

$$
F_1=\frac{2}{1/\mathrm{precision}+1/\mathrm{recall}}
   =\frac{2\,\mathrm{TP}}{2\,\mathrm{TP}+\mathrm{FP}+\mathrm{FN}}.
$$

> [!example]- Understand this formula step by step — F1 from confusion counts
>
> When $\mathrm{TP}>0$, the reciprocal of precision is $(\mathrm{TP}+\mathrm{FP})/\mathrm{TP}$ and the reciprocal of recall is $(\mathrm{TP}+\mathrm{FN})/\mathrm{TP}$. Adding and taking twice the reciprocal gives the count form. At the lower threshold in the table, it yields $6/7$. At the higher threshold it yields $2/5$.
>
> The count form extends to zero true positives when at least one false positive or false negative exists. If all three counts are zero, declare the reporting convention explicitly.

ROC-AUC characterizes ranking across thresholds. BCE is a probabilistic scoring rule, and a reliability curve directly compares predicted probability with observed frequency.

The model assumes linear log-odds in the supplied features. For example, XOR requires an interaction or another suitable feature representation for linear separation. Resampling can change the fitted intercept and probability interpretation if the training and deployment prevalences differ.

### Extending to mutually exclusive classes

For $K$ classes with finite scores $z_k$, choose a log-linear odds model: each class's odds relative to reference class $K$ are $e^{z_k-z_K}$. Every class therefore has probability proportional to $e^{z_k}$. Joint normalization gives a single probability distribution:

$$
\boxed{P(Y=k\mid\mathbf x)=\frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}}}
$$

> [!example]- Understand this formula step by step — Normalizing multiclass odds
>
> Let $p_k$ be class $k$'s probability. The modeling assumption $p_k/p_K=e^{z_k-z_K}$ implies $p_k=(p_K e^{-z_K})e^{z_k}$. The factor in parentheses is shared by every class. Sum over $k$ and use $\sum_k p_k=1$ to solve for that factor:
>
> $$
> 1=(p_K e^{-z_K})\sum_j e^{z_j}
> \quad\Longrightarrow\quad p_K e^{-z_K}=\frac1{\sum_j e^{z_j}}.
> $$
>
> With two classes, dividing numerator and denominator by $e^{z_1}$ gives $p_1=1/(1+e^{-(z_1-z_2)})=\sigma(z_1-z_2)$. Adding any common score offset cancels from numerator and denominator. Subtract the largest score before exponentiating for stable evaluation.

Softmax models mutually exclusive classes jointly. One-vs-rest instead fits a separate binary model for each class, and its probabilities need not sum to one.

---

## 9. Mental Model, Notation Reference & Bundle Links

**Mental Model:** Construct conditional log-odds linearity $\to$ invert to $\sigma(z)$ $\to$ derive $\sigma'(z) = p(1-p)$ $\to$ build Bernoulli MLE negative log-likelihood (BCE) $\to$ combine chain-rule cancellation with $X^\top(\hat{\mathbf p}-\mathbf{y})$ $\to$ establish Hessian convexity + Newton/GD + $L_2$ separation control $\to$ stabilize numerically with signed logits before choosing threshold $\tau$ for asymmetric decision costs.

**Trailing Notation Reference:** $m$ samples · $n$ features · $X \in \mathbb{R}^{m\times n}, \tilde{X} = [X,\mathbf{1}]$ · $\mathbf{w}, b, \boldsymbol{\theta}$ parameters · $z$ logit · $\sigma(z)$ sigmoid · $p_i^\ast$ underlying probability · $\hat p_i$ modeled probability · $\hat y_i$ thresholded prediction · $y_i \in \{0,1\}$ targets · $\eta$ step size · $\lambda, C$ $L_2$ regularization parameters · $\tau$ threshold.

- **Companions in this bundle:** [[logistic-regression-lab|Logistic Regression - Experimental Lab]] · [[logistic-regression-mastery|Logistic Regression - Cheatsheet & Interview Q&A]]
