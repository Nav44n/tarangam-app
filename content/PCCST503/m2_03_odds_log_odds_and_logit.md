# Odds, Log-Odds, and the Logit Function

**Proving that Logistic Regression is fundamentally a linear model for the log-odds of the positive class.**

<a id="the-math"></a>
## 1. Mathematical Derivation of Log-Odds

Let $p = P(y=1 \mid x) = \sigma(z)$.

### The Odds Ratio:
$$ \text{Odds} = \frac{p}{1 - p} = \frac{\frac{1}{1 + e^{-z}}}{1 - \frac{1}{1 + e^{-z}}} = \frac{\frac{1}{1 + e^{-z}}}{\frac{e^{-z}}{1 + e^{-z}}} = \frac{1}{e^{-z}} = e^z $$

### The Log-Odds (Logit):
Taking the natural logarithm yields:

$$ \text{logit}(p) = \ln\left( \frac{p}{1 - p} \right) = \ln(e^z) = z = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d $$

::: callout-formula Core Insight
While the relationship between features $x$ and probability $p$ is non-linear (S-shaped), the relationship between features $x$ and **Log-Odds** is strictly linear!
:::

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Logit Interpretation
If an event has probability $p = 0.80$, what is the Odds Ratio of that event occurring?
(A) 0.80
(*B) 4.0 (4 to 1)
(C) 0.20
(D) 1.25
::: explanation
$\text{Odds} = \frac{p}{1-p} = \frac{0.80}{1 - 0.80} = \frac{0.80}{0.20} = 4.0$.
:::
