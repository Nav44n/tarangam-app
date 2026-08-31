# Maximum Likelihood Estimation (MLE): Bernoulli Derivation

**How a computer finds the single model parameter that makes observed data the most statistically probable.**

<a id="the-intuition"></a>
## 1. The Intuition: The Biased Coin Detective

Suppose you flip a coin $n = 10$ times, observing $k = 7$ Heads and $3$ Tails. What is the most mathematically probable value for the true probability of heads $p$?

::: callout-intuition The MLE Principle
MLE asks: *"Among all possible values of $p \in [0, 1]$, which specific $p$ maximizes the mathematical likelihood of getting our exact observed dataset?"*
:::

---

<a id="the-math"></a>
## 2. Step-by-Step Calculus Derivation

### Step 1: Likelihood Function $L(p)$
Assuming independent and identically distributed (i.i.d.) tosses:
$$ L(p) = \prod_{i=1}^n P(x_i \mid p) = p^k (1-p)^{n-k} $$

### Step 2: The Log-Likelihood Trick $\ell(p)$
$$ \ell(p) = \ln L(p) = k \ln(p) + (n-k) \ln(1-p) $$

### Step 3: First Derivative with respect to $p$
$$ \frac{d}{dp}\ell(p) = \frac{k}{p} - \frac{n-k}{1-p} $$

### Step 4: First-Order Condition $\frac{d\ell}{dp} = 0$
$$ \frac{k}{p} = \frac{n-k}{1-p} \implies k(1-p) = p(n-k) \implies k - kp = np - kp \implies \hat{p}_{\text{MLE}} = \frac{k}{n} $$

::: callout-formula Summary
For any Bernoulli trial, the Maximum Likelihood Estimator is simply the sample proportion $\frac{k}{n}$ (e.g. $\frac{7}{10} = 0.70$).
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Log Transformation
Why do machine learning algorithms optimize $\ln L(\theta)$ instead of $L(\theta)$?
(A) The logarithm alters the location of the optimal parameter
(*B) It converts numerically unstable products into stable sums while preserving the exact maximum
(C) It eliminates the need to compute derivatives
(D) It turns non-convex functions into concave functions
::: explanation
Because $\ln(x)$ is strictly monotonically increasing, $\arg\max L(\theta) = \arg\max \ln L(\theta)$. It prevents underflow errors from multiplying tiny probabilities.
:::
