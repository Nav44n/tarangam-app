import os

CONTENT_DIR = os.path.join("content", "PCCST503")

naive_bayes = """# Naive Bayes

**A probabilistic classifier based on applying Bayes' theorem with strong (naive) independence assumptions.**

Naive Bayes methods are a set of supervised learning algorithms based on applying Bayes' theorem with the "naive" assumption of conditional independence between every pair of features given the value of the class variable.

## Bayes' Theorem

Bayes' theorem provides a way of calculating posterior probability $P(c|x)$ from $P(c)$, $P(x)$ and $P(x|c)$:

$$ P(c|x) = \frac{P(x|c)P(c)}{P(x)} $$

Where:
- $P(c|x)$ is the posterior probability of class $c$ given predictor $x$.
- $P(c)$ is the prior probability of class.
- $P(x|c)$ is the likelihood which is the probability of predictor given class.
- $P(x)$ is the prior probability of predictor.

## The "Naive" Assumption

The algorithm is called "naive" because it assumes that all features are independent of each other. Mathematically, for a feature vector $X = (x_1, x_2, \dots, x_n)$:

$$ P(X|c) = \prod_{i=1}^{n} P(x_i|c) $$

Despite this oversimplified assumption, Naive Bayes classifiers perform extremely well in many real-world situations, such as document classification and spam filtering.

## Self Check

::: toggle Q1: Why is the Naive Bayes algorithm called "naive"?
**Answer:** Because it assumes all features are independent.

*Explanation:* It assumes that the presence of a particular feature in a class is unrelated to the presence of any other feature, which is rarely true in the real world (e.g., in text, "machine" and "learning" often appear together).
:::
"""

knn = """# K-Nearest Neighbors (KNN)

**A non-parametric, lazy learning algorithm used for both classification and regression.**

K-Nearest Neighbors (KNN) is one of the simplest machine learning algorithms. It makes predictions without any underlying model assumptions. Instead, it relies on distance metrics to find the most similar data points in the training set.

## Distance Metrics

To find the "nearest" neighbors, we must calculate the distance between points. The most common metric is **Euclidean Distance**:

$$ d(p, q) = \sqrt{\sum_{i=1}^{n} (q_i - p_i)^2} $$

Other popular metrics include Manhattan distance (L1 norm) and Minkowski distance.

## How it Works (Classification)

1. Choose the number of neighbors, $K$.
2. Calculate the distance between the query instance and all training samples.
3. Sort the distances and determine the nearest $K$ neighbors.
4. Gather the categories of the nearest neighbors.
5. Use a simple majority vote to assign the class label to the query instance.

## The Role of K

Choosing $K$ is critical:
- A very **small K** (e.g., K=1) leads to low bias but high variance (highly sensitive to noise/outliers, leading to overfitting).
- A very **large K** leads to high bias but low variance (decision boundaries become too smooth, leading to underfitting).

## Self Check

::: toggle Q1: Is KNN a parametric or non-parametric algorithm?
**Answer:** Non-parametric.

*Explanation:* KNN does not make any assumptions about the underlying data distribution and does not learn a parameterized function during training. It simply memorizes the training dataset (lazy learning).
:::
"""

decision_trees = """# Decision Trees

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
$$ IG(S, A) = H(S) - \sum_{v \in Values(A)} \frac{|S_v|}{|S|} H(S_v) $$

The algorithm maximizes Information Gain, meaning it looks for the split that most effectively separates the classes, resulting in child nodes that are as pure as possible.

## Self Check

::: toggle Q1: What happens if a Decision Tree is grown to its maximum depth without stopping criteria?
**Answer:** It will severely overfit the training data.

*Explanation:* Without constraints like maximum depth, minimum samples per leaf, or pruning, the tree will perfectly memorize the training set (each leaf having only 1 sample), resulting in terrible generalization on unseen data.
:::
"""

with open(os.path.join(CONTENT_DIR, "m2_02_naive_bayes.md"), "w", encoding="utf-8") as f:
    f.write(naive_bayes)
with open(os.path.join(CONTENT_DIR, "m2_03_knn.md"), "w", encoding="utf-8") as f:
    f.write(knn)
with open(os.path.join(CONTENT_DIR, "m2_04_decision_trees.md"), "w", encoding="utf-8") as f:
    f.write(decision_trees)

print("Module 2 content populated.")
