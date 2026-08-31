# Maximum A Posteriori (MAP): Bayesian Parameter Estimation

**Overcoming the small-data overfitting flaw of MLE by incorporating prior knowledge.**

<a id="the-intuition"></a>
## 1. The Intuition: Why MLE Fails on 3 Coin Flips

If you flip a normal coin 3 times and get 3 Heads, pure MLE asserts $\hat{p} = 1.00$. This is absurd because you have a lifetime of prior experience knowing coins are fair.

::: callout-intuition Bayes' Theorem Framework
$$ P(\theta \mid D) = \frac{P(D \mid \theta) P(\theta)}{P(D)} $$
- **Posterior:** $P(\theta \mid D)$ (Our belief about $\theta$ after seeing data $D$).
- **Likelihood:** $P(D \mid \theta)$ (The MLE objective).
- **Prior:** $P(\theta)$ (Our background knowledge before seeing data).
:::

---

<a id="the-math"></a>
## 2. The MAP Objective

$$ \hat{\theta}_{\text{MAP}} = \arg\max_\theta P(\theta \mid D) = \arg\max_\theta \left[ \ln P(D \mid \theta) + \ln P(\theta) \right] $$

::: callout-formula Asymptotic Convergence
As dataset size $N \to \infty$, the likelihood $\ln P(D|\theta)$ grows linearly with $N$ and completely overwhelms the fixed prior $\ln P(\theta)$. Thus:
$$ \lim_{N \to \infty} \hat{\theta}_{\text{MAP}} = \hat{\theta}_{\text{MLE}} $$
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Large Data Limit
What happens to the MAP parameter estimate as the number of observed training samples approaches infinity ($N \to \infty$)?
(A) The prior completely overrides the data
(*B) The MAP estimate converges exactly to the MLE estimate
(C) The model severely overfits
(D) The parameter estimate goes to zero
::: explanation
With infinite data, empirical observations overwhelm any prior belief, making Bayesian MAP converge to Frequentist MLE.
:::
