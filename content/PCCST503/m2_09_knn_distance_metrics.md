# Distance Metrics: Euclidean, Manhattan, and Minkowski

**The geometric distance metrics governing multi-dimensional similarity.**

<a id="the-math"></a>
## 1. Distance Metric Formulations

### 1. Euclidean Distance ($L_2$ Norm):
$$ d_E(p, q) = \sqrt{\sum_{j=1}^d (p_j - q_j)^2} $$

### 2. Manhattan Distance ($L_1$ Norm / City Block):
$$ d_M(p, q) = \sum_{j=1}^d |p_j - q_j| $$

### 3. Minkowski Distance ($L_p$ Metric):
$$ d_p(p, q) = \left( \sum_{j=1}^d |p_j - q_j|^p \right)^{1/p} $$

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Metric Equivalence
When $p = 1$ in the Minkowski distance formula, which distance metric does it simplify to?
(A) Euclidean Distance ($L_2$)
(*B) Manhattan Distance ($L_1$)
(C) Chebyshev Distance ($L_\infty$)
(D) Mahalanobis Distance
::: explanation
$d_1(p, q) = (\sum |p_j - q_j|^1)^1 = \sum |p_j - q_j|$, which is the exact definition of Manhattan ($L_1$) distance.
:::
