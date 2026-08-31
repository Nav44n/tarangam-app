# Naïve Bayes Classification

**Fast, probabilistic classification based on Bayes' Theorem and feature independence assumptions.**

<a id="the-intuition"></a>
## 1. The Intuition: The "Naïve" Doctor

Imagine a doctor diagnosing whether a patient has the **Flu ($C_1$)** or a **Common Cold ($C_2$)** based on 3 symptoms: **Fever ($x_1$)**, **Cough ($x_2$)**, and **Fatigue ($x_3$)**.

::: callout-intuition Why is it called "Naïve"?
To compute the true joint probability $P(x_1, x_2, x_3 \mid C)$, you would need data on every possible combination of symptoms occurring together. 
- **The Naïve Assumption:** The algorithm assumes that every feature is **conditionally independent** of every other feature given the disease.
- It assumes: having a high fever has zero correlation with feeling fatigued. 
- In the real world, this assumption is completely false! Yet in practice, Naïve Bayes works remarkably well for spam filtering, sentiment analysis, and medical diagnosis.
:::

---

<a id="the-math"></a>
## 2. Mathematical Derivation

From Bayes' Theorem:

$$ P(C_k \mid x) = \frac{P(x \mid C_k) P(C_k)}{P(x)} $$

For a feature vector $x = (x_1, x_2, \dots, x_d)$, applying the Conditional Independence assumption:

$$ P(x \mid C_k) = P(x_1, x_2, \dots, x_d \mid C_k) = \prod_{j=1}^d P(x_j \mid C_k) $$

### The Naïve Bayes Classification Rule:
Since the evidence denominator $P(x) = \sum_k P(x|C_k)P(C_k)$ is identical for all candidate classes, we drop it:

$$ \hat{y} = \arg\max_{k \in \{1, \dots, K\}} P(C_k) \prod_{j=1}^d P(x_j \mid C_k) $$

Taking logs for numerical stability:

$$ \hat{y} = \arg\max_{k} \left[ \ln P(C_k) + \sum_{j=1}^d \ln P(x_j \mid C_k) \right] $$

---

<a id="worked-example"></a>
## 3. The Zero-Probability Trap & Laplace Smoothing

::: callout-pitfall The Zero-Frequency Disaster
Suppose the word *"Crypto"* never appeared in any training email labeled `Not Spam`. 
Then $P(\text{"Crypto"} \mid \text{Not Spam}) = 0$. 
Because we multiply all feature probabilities together:
$$ P(\text{Email} \mid \text{Not Spam}) = P(\text{word}_1) \times \dots \times 0 \times \dots = 0 $$
A single unseen word completely zeroes out the entire probability, wiping out all other evidence!
:::

### The Fix: Laplace ($+1$) Smoothing:
We add a pseudo-count of $\alpha = 1$ to the numerator, and adjust the denominator by the total vocabulary size $|V|$:

$$ \hat{P}(x_j \mid C_k) = \frac{\text{Count}(x_j, C_k) + 1}{\sum_{w \in V} \text{Count}(w, C_k) + |V|} $$

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Assumption Breakdown
What is the core independence assumption made by the Naïve Bayes classifier?
(A) Target classes are uniformly distributed
(*B) All features $x_i$ and $x_j$ are conditionally independent given the class label $y$
(C) Feature values must follow a standard normal distribution
(D) The covariance matrix of features is dense and non-diagonal
::: explanation
Naïve Bayes explicitly assumes that the presence or absence of a particular feature is completely unrelated to the presence or absence of any other feature, conditional on the class variable ($P(x_1, x_2|y) = P(x_1|y)P(x_2|y)$).
:::

::: quiz Q2: Smoothing Mechanics
Why is Laplace smoothing applied during Naïve Bayes text classification?
(A) To normalize text vector lengths
(*B) To prevent unseen words in test data from multiplying the total class probability down to zero
(C) To speed up matrix multiplication
(D) To reduce the number of features
::: explanation
Laplace ($+1$) additive smoothing ensures that every possible word has a tiny non-zero probability baseline, preventing a single unseen vocabulary token from destroying valid classification predictions.
:::
