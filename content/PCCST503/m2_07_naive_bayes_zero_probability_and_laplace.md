# The Zero-Frequency Problem & Laplace Smoothing

**How $+1$ additive smoothing rescues Bayesian classifiers from multiplying by zero.**

<a id="the-intuition"></a>
## 1. The Zero-Probability Trap

If an unseen word (e.g. *"Cryptocurrency"*) appears in test data and was never seen in training Spam emails:
$$ P(\text{"Cryptocurrency"} \mid \text{Spam}) = 0 \implies \prod P(x_j \mid \text{Spam}) = 0 $$
A single zero wipes out all other positive evidence!

---

<a id="the-math"></a>
## 2. Laplace ($+1$) Additive Smoothing Formula

$$ \hat{P}(x_j \mid C_k) = \frac{\text{Count}(x_j, C_k) + 1}{\sum_{w \in V} \text{Count}(w, C_k) + |V|} $$

Where $|V|$ is the total unique vocabulary size.

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Smoothing Impact
What does Laplace smoothing add to the denominator of the probability estimate?
(A) $+1$
(*B) $+|V|$ (the total size of the vocabulary)
(C) $+N^2$
(D) The variance
::: explanation
Because a pseudo-count of $+1$ is added to every one of the $|V|$ vocabulary words in the numerator, the denominator must increase by $+|V|$ so total probabilities sum to 1.
:::
