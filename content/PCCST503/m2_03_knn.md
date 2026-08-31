# K-Nearest Neighbors (KNN)

**A non-parametric, instance-based lazy learner that classifies query points based on neighborhood voting.**

<a id="the-intuition"></a>
## 1. The Intuition: "Show me your friends, and I'll tell you who you are"

Imagine you move to a new neighborhood and want to guess the political affiliation of a house.

::: callout-intuition The Neighborhood Polling Strategy
1. You find the $K$ geographically closest neighbor houses.
2. You take a majority vote among those $K$ neighbors.
3. If $K=5$, and 4 neighbors are Blue while 1 is Red, you classify the target house as **Blue**.
:::

**Why is it called a "Lazy Learner"?**
KNN has zero training phase ($O(1)$ training time). It doesn't learn any mathematical equation or weights! It simply memorizes the entire training dataset into memory and performs all computational heavy-lifting during **test / query time** ($O(m \cdot d)$).

---

<a id="the-math"></a>
## 2. Distance Metrics & Hyperparameters

To determine which neighbors are "nearest", KNN computes distance in $d$-dimensional space:

### 1. Euclidean Distance ($L_2$ Norm):
$$ d(p, q) = \sqrt{\sum_{j=1}^d (p_j - q_j)^2} $$

### 2. Manhattan Distance ($L_1$ Norm):
$$ d(p, q) = \sum_{j=1}^d |p_j - q_j| $$

### 3. Minkowski Distance ($L_p$ Generalized Norm):
$$ d(p, q) = \left( \sum_{j=1}^d |p_j - q_j|^p \right)^{1/p} $$

---

<a id="worked-example"></a>
## 3. The Impact of $K$ & Feature Scaling

::: callout-pitfall The Critical Role of $K$ (Bias vs Variance)
- **When $K = 1$:** The model fits every single noisy training point. Complex, jagged decision boundary $\implies$ **High Variance / Overfitting**.
- **When $K = m$ (Total dataset size):** The model always predicts the majority class in the entire dataset $\implies$ **High Bias / Underfitting**.
- *Rule of Thumb:* Choose an **odd number** for $K$ (e.g., $K=3, 5, 7$) in binary classification to prevent voting ties!
:::

::: callout-exam Why Feature Scaling is Mandatory for KNN!
Suppose feature $x_1$ is Annual Income (\$20,000 to \$200,000) and feature $x_2$ is Age (18 to 70).
The numerical distance in Income $(\Delta x_1 = 50,000)$ is thousands of times larger than $(\Delta x_2 = 20)$, meaning Income will 100% dominate the distance calculation while Age is completely ignored!
**Always apply Min-Max Normalization or Standard Scaling (Z-Score) before running KNN!**
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Computational Complexity
What is the training time complexity of the standard K-Nearest Neighbors algorithm on a dataset of $m$ examples with $d$ features?
(*A) $O(1)$
(B) $O(m \cdot d)$
(C) $O(m^2)$
(D) $O(d^3)$
::: explanation
Because KNN is a non-parametric lazy learner, "training" simply consists of storing the feature vectors in memory, which takes $O(1)$ model parameter fitting time. All distance computations happen at query/inference time.
:::
