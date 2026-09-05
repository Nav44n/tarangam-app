# Module 4: Unsupervised Learning, Clustering & Dimensionality Reduction (PCA)
## Comprehensive Theory: K-Means, Hierarchical Linkages, Dendrograms, and Principal Component Analysis

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Module Alignment:** Module 4 (Unsupervised Pattern Discovery & Linear Subspace Projections)  
> **Target Audience:** Absolute beginners with no prior knowledge of clustering or linear algebra eigenvalues.

---

# Table of Contents
1. [The Unsupervised Learning Paradigm](#1-the-unsupervised-learning-paradigm)
2. [Distance & Similarity Metrics: The Measuring Tapes of ML](#2-distance--similarity-metrics-the-measuring-tapes-of-ml)
3. [Partitional Clustering: The $K$-Means Algorithm](#3-partitional-clustering-the-k-means-algorithm)
4. [Determining Optimal Clusters: The Elbow Method & Silhouette Score](#4-determining-optimal-clusters-the-elbow-method--silhouette-score)
5. [Hierarchical Clustering: Agglomerative & Linkage Criteria](#5-hierarchical-clustering-agglomerative--linkage-criteria)
6. [Dimensionality Reduction & The Curse of Dimensionality](#6-dimensionality-reduction--the-curse-of-dimensionality)
7. [Principal Component Analysis (PCA): Mathematical Derivation](#7-principal-component-analysis-pca-mathematical-derivation)
8. [Explained Variance, Scree Plots & Multidimensional Scaling (MDS)](#8-explained-variance-scree-plots--multidimensional-scaling-mds)
9. [Interactive Knowledge Check Quizzes](#9-interactive-knowledge-check-quizzes)
10. [KTU University Exam Review: Part A & Part B](#10-ktu-university-exam-review-part-a--part-b)

---

# 1. The Unsupervised Learning Paradigm

::: callout-intuition Finding Constellations in the Night Sky
In **Supervised Learning**, a teacher gives you photographs labeled "Dog" or "Cat", and your goal is to learn the mapping from pixels to labels.
In **Unsupervised Learning**, there are **NO LABELS** and **NO TEACHER**. You are given an unorganized collection of points $\{ \mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_m \}$ and asked:
- *"Do these points naturally group into families?"* (**Clustering**)
- *"Can we summarize these 1,000 measurements using just 2 essential axes without losing key information?"* (**Dimensionality Reduction**)
It is like looking up at the stars and discovering constellations based purely on geometric proximity!
:::

---

# 2. Distance & Similarity Metrics: The Measuring Tapes of ML

Before an algorithm can group items, it must mathematically quantify what "similar" or "close" means.

### A. Euclidean Distance ($L_2$ Norm)
The standard straight-line "ruler" distance between points $\mathbf{x}$ and $\mathbf{z}$ in $d$-dimensional space:
$$d_{\text{Euclidean}}(\mathbf{x}, \mathbf{z}) = \|\mathbf{x} - \mathbf{z}\|_2 = \sqrt{\sum_{i=1}^d (x_i - z_i)^2}$$

### B. Manhattan Distance ($L_1$ Norm / City Block)
The distance traveling strictly along grid axes (like a taxi driving around Manhattan city blocks):
$$d_{\text{Manhattan}}(\mathbf{x}, \mathbf{z}) = \|\mathbf{x} - \mathbf{z}\|_1 = \sum_{i=1}^d |x_i - z_i|$$

### C. Cosine Similarity
Measures the angle $\theta$ between two feature vectors, ignoring their magnitudes:
$$\text{Cosine Similarity} = \cos(\theta) = \frac{\mathbf{x} \cdot \mathbf{z}}{\|\mathbf{x}\| \|\mathbf{z}\|} = \frac{\sum x_i z_i}{\sqrt{\sum x_i^2} \sqrt{\sum z_i^2}}$$
- $\cos(0^\circ) = +1$ (identical direction).
- $\cos(90^\circ) = 0$ (completely orthogonal/independent).
- Ideal for **text documents and recommendation systems** where document length varies widely.

### D. Jaccard Coefficient
Measures overlap between two sets $A$ and $B$:
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

---

# 3. Partitional Clustering: The $K$-Means Algorithm

$K$-Means partitions an unlabeled dataset into $K$ distinct, non-overlapping clusters $C = \{C_1, C_2, \dots, C_K\}$.

### The Objective Function: Within-Cluster Sum of Squares (WCSS / Inertia)
$$J = \sum_{k=1}^K \sum_{\mathbf{x} \in C_k} \|\mathbf{x} - \boldsymbol{\mu}_k\|^2$$
where $\boldsymbol{\mu}_k = \frac{1}{|C_k|} \sum_{\mathbf{x} \in C_k} \mathbf{x}$ is the **centroid** (center of mass) of cluster $k$.
The goal is to find centroids $\boldsymbol{\mu}_k$ and cluster assignments that **minimize $J$**.

### The Two-Step Expectation-Maximization (EM) Algorithm:
1. **Initialization:** Select $K$ initial centroids $\boldsymbol{\mu}_1, \dots, \boldsymbol{\mu}_K$ (randomly or via $K$-Means++).
2. **Assignment Step (E-Step):** Assign each data point $\mathbf{x}_i$ to the nearest centroid:
   $$c^{(i)} = \arg\min_k \|\mathbf{x}_i - \boldsymbol{\mu}_k\|^2$$
3. **Update Step (M-Step):** Recompute the centroid of each cluster by taking the arithmetic average of all points assigned to it:
   $$\boldsymbol{\mu}_k = \frac{1}{|C_k|} \sum_{\mathbf{x}_i \in C_k} \mathbf{x}_i$$
4. **Convergence Check:** Repeat Steps 2 and 3 until centroids no longer move (or change is below a threshold $\epsilon$).

::: callout-pitfall Convergence to Local Minima
$K$-Means is guaranteed to terminate because WCSS decreases monotonically at every step. However, it is **NOT guaranteed to find the global optimum**. The final solution depends heavily on the initial centroid positions. Solution: run $K$-Means multiple times with different random starts, or use **$K$-Means++ initialization** (which spreads out initial centroids proportionally to squared distance).
:::

---

# 4. Determining Optimal Clusters: The Elbow Method & Silhouette Score

How does a data scientist choose the integer $K$ when there are no labels?

### A. The Elbow Method
1. Run $K$-Means for values of $K$ from $1$ to $10$.
2. Plot the WCSS (Inertia) against $K$.
3. As $K$ increases, WCSS always decreases (at $K = N$, WCSS $= 0$).
4. The **optimal $K$** is the "elbow" point—where adding another cluster yields diminishing returns in variance reduction.

```
  WCSS ^
       |  \
       |   \
       |    \
       |     * <-- "Elbow Point" (Optimal K = 3)
       |      \ _ _ _ _ _
       +-----------------------> K
          1   2   3   4   5
```

### B. Silhouette Analysis
For point $i$, let $a(i)$ be the mean distance to all other points in its own cluster, and $b(i)$ be the mean distance to points in the nearest neighboring cluster.
The **Silhouette Coefficient** $s(i)$ is:
$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}, \quad \text{Range: } [-1, +1]$$
- $s(i) \approx +1$: Point is well-clustered (far from neighbors, close to center).
- $s(i) \approx 0$: Point lies on the border between two clusters.
- $s(i) < 0$: Point was probably assigned to the wrong cluster.

---

# 5. Hierarchical Clustering: Agglomerative & Linkage Criteria

Hierarchical clustering constructs a tree of nested clusters called a **Dendrogram**.
- **Agglomerative (Bottom-Up):** Starts with every point in its own individual cluster and iteratively merges the closest pair of clusters until only one remains.
- **Divisive (Top-Down):** Starts with all points in one giant cluster and recursively splits them.

### Linkage Criteria: How to Measure Distance Between Two Clusters $A$ and $B$:
1. **Single Linkage (Minimum Distance):**
   $$D(A, B) = \min_{\mathbf{x} \in A, \mathbf{z} \in B} \|\mathbf{x} - \mathbf{z}\|$$
   *Flaw:* Suffers from the **chaining effect** (creates elongated, straggly clusters connected by single noisy points).
2. **Complete Linkage (Maximum Distance):**
   $$D(A, B) = \max_{\mathbf{x} \in A, \mathbf{z} \in B} \|\mathbf{x} - \mathbf{z}\|$$
   *Advantage:* Produces compact, tight, spherical clusters. Avoids chaining.
3. **Average Linkage:**
   $$D(A, B) = \frac{1}{|A| |B|} \sum_{\mathbf{x} \in A} \sum_{\mathbf{z} \in B} \|\mathbf{x} - \mathbf{z}\|$$
4. **Ward's Method:**
   Merges the two clusters that cause the minimum increase in total within-cluster variance.

```
       Dendrogram Representation
       Height ^
              |         +---------+
              |         |         |
              |    +----+----+    |
              |    |         |    |
              |  +-+-+     +-+-+  |
              |  A   B     C   D  E
              +---------------------> Data Instances
```

---

# 6. Dimensionality Reduction & The Curse of Dimensionality

When data has hundreds or thousands of features ($d \gg 100$):
1. **Volume Explosion:** High-dimensional space is mostly empty. Points become equidistant from each other, breaking distance metrics ($d_{\max} \approx d_{\min}$).
2. **Overfitting:** Models require exponentially more training data to generalize.
3. **Computational Inefficiency:** Storage and processing time explode.

**Dimensionality Reduction** projects data into a lower-dimensional subspace ($k \ll d$) while preserving maximal statistical information.

---

# 7. Principal Component Analysis (PCA): Mathematical Derivation

**Principal Component Analysis (PCA)** is an unsupervised linear technique invented by Karl Pearson (1901) that finds orthogonal axes of **maximum variance**.

### Step-by-Step Mathematical Derivation:

#### Step 1: Mean Centering the Data
Let the data matrix be $X \in \mathbb{R}^{m \times d}$ (where each row is a sample $\mathbf{x}_i$).
Compute the mean vector $\boldsymbol{\mu} = \frac{1}{m} \sum_{i=1}^m \mathbf{x}_i$, and subtract it from all rows:
$$X_{\text{centered}} = X - \mathbf{1} \boldsymbol{\mu}^T$$

#### Step 2: Compute the Sample Covariance Matrix $\Sigma$
$$\Sigma = \frac{1}{m} X_{\text{centered}}^T X_{\text{centered}} \in \mathbb{R}^{d \times d}$$
- Diagonal entry $\Sigma_{ii} = \text{Var}(x_i)$: Variance of feature $i$.
- Off-diagonal entry $\Sigma_{ij} = \text{Cov}(x_i, x_j)$: Covariance between features $i$ and $j$.

#### Step 3: Maximizing the Projected Variance
Let $\mathbf{v}$ be a unit vector ($\|\mathbf{v}\|^2 = \mathbf{v}^T \mathbf{v} = 1$) along which we project the centered data.
The projected coordinates are $y_i = \mathbf{x}_i^T \mathbf{v}$.
The sample variance of the projected data is:
$$\text{Var}(y) = \frac{1}{m} \sum_{i=1}^m (\mathbf{x}_i^T \mathbf{v})^2 = \mathbf{v}^T \left( \frac{1}{m} X^T X \right) \mathbf{v} = \mathbf{v}^T \Sigma \mathbf{v}$$

To maximize this variance subject to $\mathbf{v}^T \mathbf{v} = 1$, we formulate the Lagrangian:
$$\mathcal{L}(\mathbf{v}, \lambda) = \mathbf{v}^T \Sigma \mathbf{v} - \lambda (\mathbf{v}^T \mathbf{v} - 1)$$

Take the partial derivative with respect to $\mathbf{v}$ and set to zero:
$$\frac{\partial \mathcal{L}}{\partial \mathbf{v}} = 2 \Sigma \mathbf{v} - 2 \lambda \mathbf{v} = 0 \implies \mathbf{\Sigma} \mathbf{v} = \lambda \mathbf{v}$$

::: callout-formula The Fundamental Eigenvalue Equation
$$\Sigma \mathbf{v} = \lambda \mathbf{v}$$
- The optimal projection directions $\mathbf{v}$ are the **Eigenvectors** of the covariance matrix $\Sigma$.
- The variance captured along each direction is exactly equal to its corresponding **Eigenvalue** $\lambda$!
:::

#### Step 4: Sorting and Subspace Projection
1. Solve the characteristic polynomial $\det(\Sigma - \lambda I) = 0$ to find eigenvalues $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_d \ge 0$.
2. Find the normalized eigenvectors $\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k$ corresponding to the top $k$ largest eigenvalues.
3. Form the projection matrix $V_k = [\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k] \in \mathbb{R}^{d \times k}$.
4. Project the original data into $k$ dimensions:
   $$Y = X_{\text{centered}} V_k \in \mathbb{R}^{m \times k}$$

---

# 8. Explained Variance, Scree Plots & Multidimensional Scaling (MDS)

### Explained Variance Ratio:
The proportion of total dataset variance captured by the $i$-th principal component is:
$$\text{Explained Variance Ratio}_i = \frac{\lambda_i}{\sum_{j=1}^d \lambda_j}$$

A **Scree Plot** graphs eigenvalues $\lambda_i$ against component numbers. Look for the "elbow" to pick the optimal number of components $k$ (typically choosing enough components to retain $90\% - 95\%$ of total variance).

### Multidimensional Scaling (MDS):
While PCA projects features by maximizing variance, **MDS** seeks a low-dimensional representation $Y$ that preserves all pairwise dissimilarities/distances between instances:
$$\min_Y \sum_{i < j} (d_{ij}^{(X)} - d_{ij}^{(Y)})^2$$

---

# 9. Interactive Knowledge Check Quizzes

::: quiz K-Means Clustering
Why does running K-Means with different random initializations often produce different final clusters?
(A) The distance formula changes on every run
(*B) The objective function (WCSS) is non-convex and gradient updates converge to local minima
(C) Centroid updates use stochastic sampling
(D) Outliers are randomly deleted
::: explanation
Because WCSS is non-convex with many local minima, standard $K$-Means converges to whatever local basin of attraction the initial centroids land in.
:::

::: quiz Principal Component Analysis
In PCA, what does the largest eigenvalue of the sample covariance matrix represent?
(A) The smallest reconstruction error
(B) The number of training samples
(*C) The maximum variance captured by the first principal component
(D) The determinant of the feature matrix
::: explanation
When we solve $\max_{\mathbf{v}} \mathbf{v}^T \Sigma \mathbf{v}$ subject to $\|\mathbf{v}\|=1$, the maximum variance achieved is $\lambda_{\max}$, and the direction of that variance is the corresponding eigenvector $\mathbf{v}_1$.
:::

---

# 10. KTU University Exam Review: Part A & Part B

### Part A: Rapid 3-Mark Questions
1. **Explain the chaining effect in Agglomerative Clustering.**  
   *Answer:* The chaining effect occurs in Single Linkage clustering because distance is measured between the two closest points. Unwanted bridges of noise can chain two distinct clusters together into a long straggly group.
2. **State the mathematical objective of the K-Means algorithm.**  
   *Answer:* $K$-Means minimizes the Within-Cluster Sum of Squares (Inertia): $J = \sum_{k=1}^K \sum_{\mathbf{x} \in C_k} \|\mathbf{x} - \boldsymbol{\mu}_k\|^2$.
3. **What is the geometric meaning of an eigenvector in PCA?**  
   *Answer:* An eigenvector of the covariance matrix represents an orthogonal principal axis along which the data exhibits maximum variance.

### Part B: 9-Mark Master Derivation Outline
1. **Derive the Principal Component Analysis (PCA) formulation using the Lagrangian method.**
   - Define data matrix $X$ and sample covariance matrix $\Sigma = \frac{1}{m} X^T X$.
   - Express projected variance as $\mathbf{v}^T \Sigma \mathbf{v}$ along unit vector $\mathbf{v}$ ($\mathbf{v}^T \mathbf{v} = 1$).
   - Formulate the Lagrangian $\mathcal{L}(\mathbf{v}, \lambda) = \mathbf{v}^T \Sigma \mathbf{v} - \lambda(\mathbf{v}^T \mathbf{v} - 1)$.
   - Differentiate with respect to $\mathbf{v}$ to arrive at the characteristic equation $\Sigma \mathbf{v} = \lambda \mathbf{v}$.
   - Explain how top $k$ eigenvectors construct the projection matrix $V_k$.
