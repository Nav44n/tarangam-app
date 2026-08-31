# K-Nearest Neighbors: Instance-Based Lazy Learning

**Why KNN has zero training phase and how neighborhood proximity guides non-parametric classification.**

<a id="the-intuition"></a>
## 1. The Intuition: Neighborhood Voting

To classify a new query point $q$:
1. Locate the $K$ closest training samples in feature space.
2. Take a majority vote among those $K$ neighbors.

::: callout-intuition What makes KNN "Lazy"?
- **Eager Learners (Linear Regression, Decision Trees):** Spend time during training learning weights $\theta$ so inference is fast ($O(1)$).
- **Lazy Learners (KNN):** Spend $O(1)$ time during training (just stores data in memory) and perform all heavy distance computations at query time ($O(m \cdot d)$).
:::

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Computational Profile
What is the training time complexity of standard KNN?
(*A) $O(1)$
(B) $O(m \cdot d)$
(C) $O(m^2)$
(D) $O(d^3)$
::: explanation
KNN is a non-parametric instance-based learner; training consists merely of loading dataset vectors into memory.
:::
