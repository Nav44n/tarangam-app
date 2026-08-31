# Decision Tree Anatomy & The 20 Questions Game

**Understanding recursive binary partitioning and tree hierarchy.**

<a id="the-intuition"></a>
## 1. The Intuition: The 20 Questions Game

Decision Trees ask a hierarchical sequence of threshold questions to segment data into pure, homogeneous subsets.

### Tree Components:
- **Root Node:** Top-level node containing 100% of the training dataset.
- **Internal Decision Nodes:** Intermediate questions testing a specific feature ($x_j \le \theta$).
- **Leaf (Terminal) Nodes:** Final prediction outcomes containing class labels or regression averages.

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Terminal Nodes
What does a leaf node in a classification Decision Tree represent?
(A) A feature split threshold
(*B) The final predicted class label
(C) The learning rate
(D) The gradient vector
::: explanation
Leaf nodes are terminal nodes that do not split any further; they contain the model's final prediction for all instances falling into that leaf.
:::
