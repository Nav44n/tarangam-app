# Naïve Bayes Fundamentals: Bayes' Theorem in Classification

**The foundational Bayesian probability architecture for predictive inference.**

<a id="the-math"></a>
## 1. Bayes' Theorem in Machine Learning

$$ P(C_k \mid x) = \frac{P(x \mid C_k) P(C_k)}{P(x)} $$

Where:
- $P(C_k \mid x)$ is the **Posterior Probability** of class $C_k$ given feature vector $x$.
- $P(x \mid C_k)$ is the **Class-Conditional Likelihood**.
- $P(C_k)$ is the **Class Prior Probability**.
- $P(x) = \sum_k P(x \mid C_k) P(C_k)$ is the **Evidence (Marginal Likelihood)**.

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Evidence Role
Why can the denominator $P(x)$ be dropped when selecting the winning class $\hat{y} = \arg\max_k P(C_k|x)$?
(A) It always equals 1.0
(*B) It is identical across all candidate classes $C_k$ and does not change the ranking
(C) It is non-differentiable
(D) It is an imaginary number
::: explanation
Because $P(x)$ is a constant scaling factor across all classes for a given input $x$, the class that maximizes the numerator also maximizes the posterior.
:::
