# Decision Trees

**A hierarchical model that uses a tree-like graph of decisions and their possible consequences.**

Decision Trees are non-parametric supervised learning methods used for classification and regression. The goal is to create a model that predicts the value of a target variable by learning simple decision rules inferred from the data features.

## Tree Anatomy

- **Root Node**: The top node that represents the entire dataset.
- **Splitting**: The process of dividing a node into two or more sub-nodes.
- **Decision Node**: A node that splits into further sub-nodes.
- **Leaf/Terminal Node**: Nodes that do not split; they represent the final predicted class or value.

## Splitting Criteria

The algorithm chooses the best feature to split the data at each node. For classification, it uses metrics like **Gini Impurity** or **Entropy** (Information Gain).

**Entropy**:
$$ H(S) = - \sum_{i=1}^{c} p_i \log_2(p_i) $$

**Information Gain**:
$$ IG(S, A) = H(S) - \sum_{v \in Values(A)} rac{|S_v|}{|S|} H(S_v) $$

The algorithm maximizes Information Gain, meaning it looks for the split that most effectively separates the classes, resulting in child nodes that are as pure as possible.

## Self Check

::: toggle Q1: What happens if a Decision Tree is grown to its maximum depth without stopping criteria?
**Answer:** It will severely overfit the training data.

*Explanation:* Without constraints like maximum depth, minimum samples per leaf, or pruning, the tree will perfectly memorize the training set (each leaf having only 1 sample), resulting in terrible generalization on unseen data.
:::
