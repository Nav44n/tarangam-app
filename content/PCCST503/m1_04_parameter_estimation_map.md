# Parameter Estimation: Maximum A Posteriori (MAP)

**How to inject prior common sense into parameter estimation so small datasets don't mislead your model.**

<a id="the-intuition"></a>
## 1. The Intuition: When MLE Fails Spectacularly

Imagine a friend hands you a brand-new, standard coin. You flip it **3 times**, and it lands on **Heads all 3 times**.

::: callout-intuition Why Common Sense Matters
- **Pure MLE says:** $\hat{p}_{\text{MLE}} = \frac{3}{3} = 1.00$ (*"This coin is physically incapable of landing on Tails!"*).
- **Your Brain says:** *"No, I have flipped thousands of normal coins in my life. The probability is almost certainly around $0.50$, and 3 heads was just a lucky streak."*
- **Maximum A Posteriori (MAP)** is Bayesian parameter estimation. It combines your **Prior Belief ($P(\theta)$)** with the **Observed Likelihood ($P(D|\theta)$)** to find the balanced posterior truth.
:::

---

<a id="the-math"></a>
## 2. Bayes' Theorem Formulation

From Bayes' Theorem:

$$ P(\theta | D) = \frac{P(D | \theta) P(\theta)}{P(D)} $$

Where:
- $P(\theta | D)$ is the **Posterior Probability** (the probability of parameter $\theta$ given the observed data).
- $P(D | \theta)$ is the **Likelihood** (how probable the data is under parameter $\theta$).
- $P(\theta)$ is the **Prior** (our belief about $\theta$ before seeing the experiment).
- $P(D) = \int P(D|\theta)P(\theta)d\theta$ is the **Evidence** (a constant scaling factor independent of $\theta$).

### The MAP Optimization Objective:
Since the denominator $P(D)$ does not depend on $\theta$, the MAP estimate solves:

$$ \hat{\theta}_{\text{MAP}} = \arg\max_\theta P(\theta | D) = \arg\max_\theta \left[ \ln P(D | \theta) + \ln P(\theta) \right] $$

::: callout-formula MLE vs MAP Head-to-Head
| Feature | Maximum Likelihood (MLE) | Maximum A Posteriori (MAP) |
| :--- | :--- | :--- |
| **Philosophical School** | Frequentist | Bayesian |
| **Formula** | $\arg\max_\theta \ln P(D\|\theta)$ | $\arg\max_\theta [\ln P(D\|\theta) + \ln P(\theta)]$ |
| **Small Data Performance** | Prone to extreme overfitting | Robust (anchored by prior) |
| **Infinite Data Limit ($N \to \infty$)** | Converges to true parameter | Converges to MLE (Data overwhelms the prior!) |
| **Regularization Link** | Unregularized model | Equivalent to L2 (Ridge) / L1 (Lasso) regularization |
:::

---

<a id="worked-example"></a>
## 3. Deriving MAP for a Coin Toss (Beta Prior)

Let the prior on $p$ be modeled by a **Beta distribution** $\text{Beta}(\alpha, \beta)$, which acts as pseudo-counts ($\alpha-1$ prior heads, $\beta-1$ prior tails):

$$ P(p) \propto p^{\alpha - 1} (1-p)^{\beta - 1} $$

::: step [Step 1: Joint Likelihood & Prior] Setup
$$ P(D | p) P(p) = \left[ p^k (1-p)^{n-k} \right] \cdot \left[ p^{\alpha - 1} (1-p)^{\beta - 1} \right] = p^{k + \alpha - 1} (1-p)^{n - k + \beta - 1} $$
:::

::: step [Step 2: Log-Posterior] Log Transformation
$$ \ln P(p | D) = (k + \alpha - 1) \ln(p) + (n - k + \beta - 1) \ln(1-p) + \text{const} $$
:::

::: step [Step 3: Differentiation & Solution] Finding Peak
Taking derivative with respect to $p$ and setting to zero yields:
$$ \hat{p}_{\text{MAP}} = \frac{k + \alpha - 1}{n + \alpha + \beta - 2} $$
:::

::: callout-exam Example with Numbers
If our prior is $\text{Beta}(5, 5)$ (representing a strong prior belief of a fair coin) and we observe $k=3$ heads in $n=3$ tosses:
$$ \hat{p}_{\text{MAP}} = \frac{3 + 5 - 1}{3 + 5 + 5 - 2} = \frac{7}{11} \approx 0.636 $$
Notice how MAP wisely pulled the extreme $1.0$ estimate back toward the sensible $0.50$ baseline!
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Asymptotic Behavior
What happens to the MAP estimate $\hat{\theta}_{\text{MAP}}$ as the sample size $N \to \infty$ (approaches infinity)?
(A) The prior completely dominates the data
(*B) The MAP estimate converges exactly to the MLE estimate
(C) The variance of the parameter estimate increases
(D) The posterior probability collapses to zero
::: explanation
As the volume of observed empirical data grows infinitely large ($N \to \infty$), the likelihood term $\ln P(D|\theta)$ grows linearly with $N$ and completely overwhelms the fixed prior $\ln P(\theta)$, making MAP identical to MLE.
:::

::: quiz Q2: Regularization Equivalence
In linear regression, placing a zero-mean Gaussian (Normal) prior on the weight vector $w \sim \mathcal{N}(0, \sigma^2)$ is mathematically equivalent to which technique?
(A) L1 Regularization (Lasso)
(*B) L2 Regularization (Ridge Regression / Weight Decay)
(C) Dropout
(D) Early Stopping
::: explanation
A Gaussian prior adds $-\frac{\lambda}{2}\|w\|_2^2$ to the log-likelihood objective, which is the exact penalty term used in Ridge Regression ($L_2$). A Laplace prior conversely yields L1 (Lasso) regularization.
:::
