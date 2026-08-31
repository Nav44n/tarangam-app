# Information Gain & The ID3 Algorithm

**Greedy recursive tree construction by maximizing entropy reduction.**

<a id="the-math"></a>
## 1. Information Gain Formula

$$ IG(S, A) = H(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v) $$

The ID3 algorithm evaluates all available features at each step and splits on feature $A^* = \arg\max_A IG(S, A)$.

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Splitting Rule
Which feature is chosen for splitting at a node during ID3 tree construction?
(A) The feature with the highest variance
(*B) The feature that maximizes Information Gain
(C) The feature with the lowest entropy
(D) The feature with the smallest number of distinct categories
::: explanation
ID3 uses a greedy heuristic that selects the feature achieving the greatest reduction in entropy (highest Information Gain).
:::
