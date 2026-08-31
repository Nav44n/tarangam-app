# Gini Impurity & CART Binary Trees

**The computational alternative to Entropy used in standard production Decision Trees.**

<a id="the-math"></a>
## 1. Gini Impurity Definition

$$ \text{Gini}(S) = 1 - \sum_{i=1}^C p_i^2 $$

- **Pure Node:** $\text{Gini} = 1 - (1^2) = 0.00$.
- **50/50 Balanced Node:** $\text{Gini} = 1 - (0.5^2 + 0.5^2) = 1 - 0.50 = 0.50$.

::: callout-formula Gini vs Entropy
Gini Impurity avoids expensive $\log_2$ calculations, making it computationally faster to compute while yielding virtually identical split choices to Entropy.
:::

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Computational Difference
Why does Scikit-Learn's CART algorithm use Gini Impurity by default instead of Entropy?
(A) Entropy is mathematically inaccurate
(*B) Gini Impurity does not require logarithmic computations, making training faster
(C) Gini Impurity guarantees zero overfitting
(D) Gini works on continuous features whereas Entropy does not
::: explanation
Computing logarithms ($\log_2$) is computationally more expensive on CPUs than simple squaring and subtraction.
:::
