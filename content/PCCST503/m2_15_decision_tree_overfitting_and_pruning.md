# Decision Tree Overfitting & Pruning Strategies

**Controlling tree growth to prevent complete training set memorization.**

<a id="the-intuition"></a>
## 1. The Overfitting Problem in Trees

An unconstrained Decision Tree will split until every leaf contains exactly 1 sample ($H=0$). It achieves 100% training accuracy but generalizes terribly on test data.

---

<a id="worked-example"></a>
## 2. Pruning Techniques

::: step [Pre-Pruning (Early Stopping)]
Stop tree expansion early if:
- `max_depth` is reached (e.g. 4 layers).
- `min_samples_split` is below threshold (e.g. $< 10$).
- $\Delta IG < \epsilon$.
:::

::: step [Post-Pruning (Cost-Complexity)]
Grow tree to full size, then prune subtrees upward minimizing:
$$ \mathcal{L}_\alpha(T) = \text{Error}(T) + \alpha |T| $$
Where $|T|$ is the number of terminal leaves and $\alpha$ is the complexity penalty.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Regularization Parameter
In cost-complexity pruning ($\mathcal{L}_\alpha = \text{Error} + \alpha |T|$), what happens as $\alpha \to \infty$?
(A) The tree grows infinitely deep
(*B) The tree collapses to a single root node
(C) The training error becomes zero
(D) The tree becomes a neural network
::: explanation
As $\alpha$ becomes huge, the penalty for having leaves ($|T|$) dominates error, forcing the algorithm to prune all branches down to the root.
:::
