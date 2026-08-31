# Why Linear Regression Fails for Classification

**The structural failure modes of applying continuous regression lines to discrete categorical tasks.**

<a id="the-intuition"></a>
## 1. The Intuition: Tumor Malignancy

Suppose you want to predict whether a medical biopsy is **Malignant ($y=1$)** or **Benign ($y=0$)** based on tumor size ($x$).

::: callout-intuition Why Straight Lines Fail on Categories
If you fit a standard linear model $h_\theta(x) = \theta_0 + \theta_1 x$:
1. **Unbounded Output Values:** For large tumors, linear regression predicts $\hat{y} = 2.85$. A probability must strictly be bounded in $[0, 1]$.
2. **Extreme Outlier Sensitivity:** Adding a single benign tumor with huge radius far to the right pivots the line, drastically altering your classification decision threshold ($h(x) \ge 0.5$) and causing fatal false negatives!
:::

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Linear Model Flaws
Why is linear regression mathematically inappropriate for predicting binary probabilities?
(A) It requires gradient descent
(*B) It can output negative values and values strictly greater than 1.0
(C) It cannot handle continuous features
(D) It only works on 1-dimensional datasets
::: explanation
Probabilities are strictly bounded in the range $[0, 1]$. A linear function $\theta^T x$ has an unbounded range $(-\infty, +\infty)$.
:::
