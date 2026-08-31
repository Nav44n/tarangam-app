# Decision Trees & Information Gain

**Hierarchical decision systems that recursively partition data using Information Theory.**

<a id="the-intuition"></a>
## 1. The Intuition: The 20 Questions Game

Imagine playing the game *"20 Questions"* to guess a mystery animal.

::: callout-intuition What makes a good question?
- A bad question: *"Is its name Bob?"* (Only eliminates 1 option).
- A great question: *"Does it live on land or in water?"* (Instantly cuts the possibilities in half!).
- **Decision Trees** operate on the exact same logic. At every step, the algorithm searches across all features to find the single question that **maximizes purity** (reduces uncertainty the most).
:::

---

<a id="the-math"></a>
## 2. Mathematical Metrics: Entropy & Information Gain

### 1. Shannon Entropy ($H(S)$):
Entropy measures the degree of disorder, uncertainty, or impurity in a set of examples $S$:

$$ H(S) = -\sum_{i=1}^C p_i \log_2(p_i) $$

Where $p_i$ is the proportion of examples belonging to class $i$.
- If a node is **100% Pure** (all samples are Spam): $H(S) = - (1 \cdot \log_2(1)) = 0$.
- If a node is **50/50 Balanced** (maximum confusion): $H(S) = - (0.5\log_2(0.5) + 0.5\log_2(0.5)) = 1.0\text{ bit}$.

### 2. Information Gain ($IG(S, A)$):
Information Gain measures the expected reduction in entropy achieved by splitting dataset $S$ on feature $A$:

$$ IG(S, A) = H(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v) $$

### 3. Gini Impurity (Used by CART):
$$ \text{Gini}(S) = 1 - \sum_{i=1}^C p_i^2 $$

---

<a id="worked-example"></a>
## 3. Overfitting & Pruning Techniques

A Decision Tree left unrestricted will grow until every single leaf contains exactly 1 sample ($H(S)=0$), perfectly memorizing all training noise $\implies$ catastrophic overfitting.

::: step [Strategy 1: Pre-Pruning (Early Stopping)] Stopping Criteria
Halt tree growth before completion if:
- Maximum tree depth is reached (`max_depth = 4`).
- Minimum samples required to split a node is not met (`min_samples_split = 10`).
- Information Gain falls below a minimum threshold ($\Delta IG < \epsilon$).
:::

::: step [Strategy 2: Post-Pruning (Cost-Complexity Pruning)] Pruning Back
Grow the tree to full depth, then prune subtrees upward if removing them does not significantly worsen validation accuracy, balancing tree size against error:
$$ \mathcal{L}_\alpha(T) = \text{Error}(T) + \alpha |T| $$
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Metric Interpretation
If a decision tree node contains 20 examples, and all 20 belong to Class 'Approved' (0 belong to 'Rejected'), what is the Shannon Entropy of this node?
(*A) 0.00 bits
(B) 0.50 bits
(C) 1.00 bits
(D) Undefined
::: explanation
Because the subset is completely pure (zero uncertainty), $p_1 = 1.0$. The entropy is $H(S) = - (1.0 \cdot \log_2(1.0)) = 0.00$. Zero entropy corresponds to absolute certainty.
:::

::: quiz Q2: Splitting Objective
During the construction of a classification tree using the ID3 algorithm, which feature is selected at each split?
(A) The feature with the highest variance
(*B) The feature that yields the maximum Information Gain (highest reduction in entropy)
(C) The feature with the smallest number of unique categories
(D) The feature with the lowest correlation to the target
::: explanation
ID3 uses a greedy heuristic that evaluates all available candidate features and selects the one that maximizes Information Gain ($IG = H(S) - H(S|A)$), creating child subsets that are as pure as possible.
:::
