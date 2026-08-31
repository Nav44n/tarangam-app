# K-Nearest Neighbors (KNN)

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
