# Logistic Regression & Sigmoid Activation

**The quintessential probabilistic classification algorithm: mapping linear predictions to bounded probabilities.**

<a id="the-intuition"></a>
## 1. The Intuition: Why Linear Regression Fails for Classification

Suppose you want to predict whether a medical tumor is **Malignant ($y=1$)** or **Benign ($y=0$)** based on tumor radius ($x$).

::: callout-intuition The Flaws of Linear Regression for Categories
If you fit a straight line $h_\theta(x) = \theta_0 + \theta_1 x$:
1. **Unbounded Outputs:** For very large tumors, linear regression predicts $\hat{y} = 2.45$. What does a "245% probability of cancer" mean? Probabilities must strictly be bounded within $[0, 1]$.
2. **Sensitivity to Outliers:** A single extreme benign outlier far to the right pivots the regression line, shifting your decision threshold and causing dangerous misdiagnoses.
:::

**The Fix:** Wrap the linear score $z = \theta^T x$ inside a non-linear **S-shaped Sigmoid function** $\sigma(z)$ that squashes any input into a valid probability $(0, 1)$.

---

<a id="the-math"></a>
## 2. Mathematical Formulation

### The Logistic Sigmoid Function:
$$ \sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{1 + e^z} $$

Where $z = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d = \theta^T x$.

### The Probabilistic Hypothesis:
$$ h_\theta(x) = P(y=1 \mid x; \theta) = \sigma(\theta^T x) = \frac{1}{1 + e^{-\theta^T x}} $$

$$ P(y=0 \mid x; \theta) = 1 - h_\theta(x) $$

### Odds and Log-Odds (The Logit Function):
The **Odds** of an event is the ratio of probability of occurrence to non-occurrence:

$$ \text{Odds} = \frac{P(y=1|x)}{1 - P(y=1|x)} = \frac{\sigma(z)}{1 - \sigma(z)} = e^z $$

Taking the natural logarithm yields the **Log-Odds (Logit)**:

$$ \ln\left( \frac{P(y=1|x)}{1 - P(y=1|x)} \right) = \ln(e^z) = z = \theta^T x $$

*Insight:* Logistic Regression is fundamentally a **linear model for the log-odds of the positive class!*

---

<a id="worked-example"></a>
## 3. Cost Function & The Non-Convexity Trap

::: callout-pitfall Why MSE is Forbidden in Logistic Regression
If you plug the non-linear sigmoid $\sigma(\theta^Tx)$ into the Mean Squared Error cost function $\frac{1}{2m}\sum (\sigma(\theta^Tx) - y)^2$, the resulting cost surface is **wavy and non-convex** with dozens of local minima. Gradient descent will get stuck in poor local minima!
:::

### The Convex Cross-Entropy Loss (Log Loss):
$$ J(\theta) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln(h_\theta(x^{(i)})) + (1 - y^{(i)}) \ln(1 - h_\theta(x^{(i)})) \right] $$

- When $y = 1$: Cost is $-\ln(h_\theta(x))$. If $h_\theta(x) \to 1$, $\text{Cost} \to 0$. If $h_\theta(x) \to 0$, $\text{Cost} \to \infty$ (infinite penalty for confident wrong guesses!).
- When $y = 0$: Cost is $-\ln(1 - h_\theta(x))$. If $h_\theta(x) \to 0$, $\text{Cost} \to 0$. If $h_\theta(x) \to 1$, $\text{Cost} \to \infty$.

---

<a id="simulation"></a>
## 4. Visualizing the Sigmoid Activation

::: manim assets/videos/m2_logistic_sigmoid.mp4 Sigmoid Decision Boundary
Watch how inputs from $-\infty$ to $+\infty$ are smoothly squashed into the probability interval $(0, 1)$ with threshold at $z=0$.
:::

---

<a id="self-check"></a>
## 5. Active Recall Checkpoint

::: quiz Q1: Decision Boundary
If a fitted binary logistic regression model produces a linear score $z = \theta^T x = 0$, what is the predicted probability of the positive class $\hat{y}$?
(A) 0.00
(*B) 0.50
(C) 1.00
(D) Undefined
::: explanation
$\sigma(0) = \frac{1}{1 + e^{-0}} = \frac{1}{1 + 1} = \frac{1}{2} = 0.50$. In standard binary classification, $z=0$ defines the exact geometric hyperplane of the Decision Boundary.
:::

::: quiz Q2: Optimization Geometry
Why is Binary Cross-Entropy used instead of Mean Squared Error when optimizing Logistic Regression?
(A) MSE produces gradients that explode infinitely
(*B) Sigmoid combined with MSE creates a non-convex error surface with local minima, whereas Cross-Entropy is strictly convex
(C) Cross-Entropy does not require computing derivatives
(D) Cross-Entropy only works on continuous real numbers
::: explanation
The non-linearity of the sigmoid creates wavy valleys when squared. Cross-entropy loss cancels the exponential behavior in the gradient, producing a guaranteed convex bowl where gradient descent always converges to the global minimum.
:::
