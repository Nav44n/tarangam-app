# MLE for Continuous Variables: 1D Gaussian Distribution

**Deriving why the sample mean and variance are the mathematically optimal parameters of a normal distribution.**

<a id="the-intuition"></a>
## 1. The Intuition: Fitting the Bell Curve

Suppose you measure the heights of 1,000 students. You assume heights follow a normal distribution $\mathcal{N}(\mu, \sigma^2)$. How do you prove mathematically that the best bell curve center is simply the arithmetic average?

---

<a id="the-math"></a>
## 2. Mathematical Proof

For $m$ independent samples $x_1, \dots, x_m$:

$$ P(x_i \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x_i - \mu)^2}{2\sigma^2} \right) $$

### Step 1: Log-Likelihood Formulation
$$ \ell(\mu, \sigma^2) = -\frac{m}{2}\ln(2\pi) - \frac{m}{2}\ln(\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^m (x_i - \mu)^2 $$

### Step 2: Deriving Optimal Mean $\hat{\mu}_{\text{MLE}}$
Take partial derivative with respect to $\mu$ and set to 0:
$$ \frac{\partial \ell}{\partial \mu} = \frac{1}{\sigma^2}\sum_{i=1}^m (x_i - \mu) = 0 \implies \sum_{i=1}^m x_i - m\mu = 0 \implies \hat{\mu}_{\text{MLE}} = \frac{1}{m}\sum_{i=1}^m x_i $$

### Step 3: Deriving Optimal Variance $\hat{\sigma}^2_{\text{MLE}}$
Take partial derivative with respect to $\sigma^2$ and set to 0:
$$ \frac{\partial \ell}{\partial \sigma^2} = -\frac{m}{2\sigma^2} + \frac{1}{2(\sigma^2)^2}\sum_{i=1}^m (x_i - \mu)^2 = 0 \implies \hat{\sigma}^2_{\text{MLE}} = \frac{1}{m}\sum_{i=1}^m (x_i - \mu)^2 $$

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Analytical Result
What is the Maximum Likelihood Estimator for the mean $\mu$ of a 1D Gaussian distribution?
(*A) The sample mean $\frac{1}{m}\sum x_i$
(B) The sample median
(C) The maximum value in the dataset
(D) $\frac{1}{m-1}\sum (x_i - \bar{x})^2$
::: explanation
Setting the derivative of the Gaussian log-likelihood with respect to $\mu$ to zero directly yields the arithmetic average $\frac{1}{m}\sum x_i$.
:::
