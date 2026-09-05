# Module 4: Worked Problems — Clustering & PCA Traces
## Progressive Problem Workbook: K-Means Iterations, Agglomerative Dendrogram Matrices, and End-to-End PCA Numerical Calculations

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Topic:** Module 4 (Clustering Mechanics & Principal Component Analysis)  
> **Format:** Step-by-step arithmetic and numerical solutions with zero skipped steps.

---

# Problem 1: Step-by-Step $K$-Means Clustering Trace (2D Space)

### Problem Statement (Classic KTU Core Exam Problem)
Given four 2D data instances:
$$A_1 = (2, 10), \quad A_2 = (2, 5), \quad A_3 = (8, 4), \quad A_4 = (5, 8)$$
Perform $K$-Means clustering with $K = 2$.
- Initial Centroid for Cluster 1 ($C_1$): $\boldsymbol{\mu}_1 = A_1 = (2, 10)$
- Initial Centroid for Cluster 2 ($C_2$): $\boldsymbol{\mu}_2 = A_4 = (5, 8)$
- Use squared Euclidean distance: $d^2(\mathbf{x}, \boldsymbol{\mu}) = (x_1 - \mu_1)^2 + (x_2 - \mu_2)^2$.

Execute:
1. Iteration 1: Compute distances, assign each point to the nearest centroid, and recalculate new centroids.
2. Iteration 2: Recompute distances and check for convergence.

---

### Step-by-Step Solution

#### Iteration 1:
Initial centroids: $\boldsymbol{\mu}_1 = (2, 10)$, $\boldsymbol{\mu}_2 = (5, 8)$.

**Distance Calculations:**
1. **For $A_1(2, 10)$:**
   - $d^2(A_1, \boldsymbol{\mu}_1) = (2 - 2)^2 + (10 - 10)^2 = 0$
   - $d^2(A_1, \boldsymbol{\mu}_2) = (2 - 5)^2 + (10 - 8)^2 = (-3)^2 + (2)^2 = 9 + 4 = 13$
   - Nearest centroid: $\boldsymbol{\mu}_1 \implies \mathbf{A_1 \in C_1}$
2. **For $A_2(2, 5)$:**
   - $d^2(A_2, \boldsymbol{\mu}_1) = (2 - 2)^2 + (5 - 10)^2 = 0 + (-5)^2 = 25$
   - $d^2(A_2, \boldsymbol{\mu}_2) = (2 - 5)^2 + (5 - 8)^2 = (-3)^2 + (-3)^2 = 9 + 9 = 18$
   - $18 < 25 \implies$ Nearest centroid: $\boldsymbol{\mu}_2 \implies \mathbf{A_2 \in C_2}$
3. **For $A_3(8, 4)$:**
   - $d^2(A_3, \boldsymbol{\mu}_1) = (8 - 2)^2 + (4 - 10)^2 = 6^2 + (-6)^2 = 36 + 36 = 72$
   - $d^2(A_3, \boldsymbol{\mu}_2) = (8 - 5)^2 + (4 - 8)^2 = 3^2 + (-4)^2 = 9 + 16 = 25$
   - $25 < 72 \implies$ Nearest centroid: $\boldsymbol{\mu}_2 \implies \mathbf{A_3 \in C_2}$
4. **For $A_4(5, 8)$:**
   - $d^2(A_4, \boldsymbol{\mu}_1) = (5 - 2)^2 + (8 - 10)^2 = 3^2 + (-2)^2 = 9 + 4 = 13$
   - $d^2(A_4, \boldsymbol{\mu}_2) = (5 - 5)^2 + (8 - 8)^2 = 0$
   - Nearest centroid: $\boldsymbol{\mu}_2 \implies \mathbf{A_4 \in C_2}$

**Cluster Formations for Iteration 1:**
- $C_1 = \{ A_1 \}$
- $C_2 = \{ A_2, A_3, A_4 \}$

**Update Centroids (Centroid Recalculation):**
- $\boldsymbol{\mu}_1^{\text{new}} = A_1 = \mathbf{(2, 10)}$
- $\boldsymbol{\mu}_2^{\text{new}} = \left(\frac{2 + 8 + 5}{3}, \; \frac{5 + 4 + 8}{3}\right) = \left(\frac{15}{3}, \; \frac{17}{3}\right) = \mathbf{(5.0, 5.67)}$

---

#### Iteration 2:
Centroids: $\boldsymbol{\mu}_1 = (2, 10)$, $\boldsymbol{\mu}_2 = (5.0, 5.67)$.

**Recompute Distances:**
1. **For $A_1(2, 10)$:**
   - $d^2(A_1, \boldsymbol{\mu}_1) = 0$
   - $d^2(A_1, \boldsymbol{\mu}_2) = (2 - 5)^2 + (10 - 5.67)^2 = 9 + (4.33)^2 = 9 + 18.75 = 27.75$
   - Nearest centroid: $\boldsymbol{\mu}_1 \implies \mathbf{A_1 \in C_1}$
2. **For $A_2(2, 5)$:**
   - $d^2(A_2, \boldsymbol{\mu}_1) = 25$
   - $d^2(A_2, \boldsymbol{\mu}_2) = (2 - 5)^2 + (5 - 5.67)^2 = 9 + (-0.67)^2 = 9 + 0.45 = 9.45$
   - Nearest centroid: $\boldsymbol{\mu}_2 \implies \mathbf{A_2 \in C_2}$
3. **For $A_3(8, 4)$:**
   - $d^2(A_3, \boldsymbol{\mu}_1) = 72$
   - $d^2(A_3, \boldsymbol{\mu}_2) = (8 - 5)^2 + (4 - 5.67)^2 = 9 + (-1.67)^2 = 9 + 2.79 = 11.79$
   - Nearest centroid: $\boldsymbol{\mu}_2 \implies \mathbf{A_3 \in C_2}$
4. **For $A_4(5, 8)$:**
   - $d^2(A_4, \boldsymbol{\mu}_1) = (5 - 2)^2 + (8 - 10)^2 = 9 + 4 = 13$
   - $d^2(A_4, \boldsymbol{\mu}_2) = (5 - 5)^2 + (8 - 5.67)^2 = 0 + (2.33)^2 = 5.43$
   - Nearest centroid: $\boldsymbol{\mu}_2 \implies \mathbf{A_4 \in C_2}$

**Cluster Formations for Iteration 2:**
- $C_1 = \{ A_1 \}$
- $C_2 = \{ A_2, A_3, A_4 \}$

**Convergence Check:**
The cluster assignments in Iteration 2 are **identical** to Iteration 1!
Centroids will not move. **Algorithm has converged.**
Final Clusters:
- **Cluster 1:** $\{ (2, 10) \}$ with centroid $(2, 10)$
- **Cluster 2:** $\{ (2, 5), (8, 4), (5, 8) \}$ with centroid $(5.0, 5.67)$

---

# Problem 2: Agglomerative Hierarchical Clustering with Single & Complete Linkage

### Problem Statement
Consider 4 points $P_1, P_2, P_3, P_4$ with the following symmetric pairwise Euclidean distance matrix:

| | $P_1$ | $P_2$ | $P_3$ | $P_4$ |
| :---: | :---: | :---: | :---: | :---: |
| **$P_1$** | 0 | 2 | 6 | 10 |
| **$P_2$** | 2 | 0 | 5 | 9 |
| **$P_3$** | 6 | 5 | 0 | 4 |
| **$P_4$** | 10 | 9 | 4 | 0 |

Construct the step-by-step cluster merges using:
1. **Single Linkage** (Minimum Distance).
2. **Complete Linkage** (Maximum Distance).

---

### Step-by-Step Solution

#### Part 1: Single Linkage

- **Step 1:** Find the minimum off-diagonal distance in the matrix.
  The minimum value is $D(P_1, P_2) = 2$.
  Merge $P_1$ and $P_2$ to form cluster **$(P_1, P_2)$** at height $\mathbf{h = 2}$.

- **Step 2:** Update distance matrix using Single Linkage ($D((A, B), C) = \min(D(A, C), D(B, C))$):
  - $D((P_1, P_2), P_3) = \min(D(P_1, P_3), D(P_2, P_3)) = \min(6, 5) = 5$
  - $D((P_1, P_2), P_4) = \min(D(P_1, P_4), D(P_2, P_4)) = \min(10, 9) = 9$
  - $D(P_3, P_4) = 4$

  Reduced Matrix:
  
  | | $(P_1, P_2)$ | $P_3$ | $P_4$ |
  | :---: | :---: | :---: | :---: |
  | **$(P_1, P_2)$** | 0 | 5 | 9 |
  | **$P_3$** | 5 | 0 | **4** |
  | **$P_4$** | 9 | **4** | 0 |

- **Step 3:** The smallest entry is $D(P_3, P_4) = 4$.
  Merge $P_3$ and $P_4$ to form cluster **$(P_3, P_4)$** at height $\mathbf{h = 4}$.

- **Step 4:** Final merge distance:
  $D((P_1, P_2), (P_3, P_4)) = \min(D((P_1, P_2), P_3), D((P_1, P_2), P_4)) = \min(5, 9) = 5$.
  Merge all into **$((P_1, P_2), (P_3, P_4))$** at height $\mathbf{h = 5}$.

```
  Single Linkage Dendrogram:
  Height ^
       5 |          +---------------+
         |          |               |
       4 |          |           +---+---+
         |          |           |       |
       2 |      +---+---+       |       |
         |      |       |       |       |
       0 +------+-------+-------+-------+-->
               P1      P2      P3      P4
```

---

#### Part 2: Complete Linkage

- **Step 1:** Smallest entry is still $D(P_1, P_2) = 2$.
  Merge $P_1$ and $P_2$ into **$(P_1, P_2)$** at height $\mathbf{h = 2}$.

- **Step 2:** Update using Complete Linkage ($D((A, B), C) = \max(D(A, C), D(B, C))$):
  - $D((P_1, P_2), P_3) = \max(6, 5) = 6$
  - $D((P_1, P_2), P_4) = \max(10, 9) = 10$
  - $D(P_3, P_4) = 4$

  Reduced Matrix:
  
  | | $(P_1, P_2)$ | $P_3$ | $P_4$ |
  | :---: | :---: | :---: | :---: |
  | **$(P_1, P_2)$** | 0 | 6 | 10 |
  | **$P_3$** | 6 | 0 | **4** |
  | **$P_4$** | 10 | **4** | 0 |

- **Step 3:** Smallest entry is $D(P_3, P_4) = 4$.
  Merge $P_3$ and $P_4$ into **$(P_3, P_4)$** at height $\mathbf{h = 4}$.

- **Step 4:** Final merge distance:
  $D((P_1, P_2), (P_3, P_4)) = \max(D(P_1, P_3), D(P_1, P_4), D(P_2, P_3), D(P_2, P_4)) = \max(6, 10, 5, 9) = \mathbf{10}$.
  Merge all into **$((P_1, P_2), (P_3, P_4))$** at height $\mathbf{h = 10}$.

---

# Problem 3: Complete Numerical PCA Calculation from Scratch (2D to 1D)

### Problem Statement (Core 9-Mark KTU Exam Problem)
Given a dataset of 4 instances with 2 features:
$$X = \begin{bmatrix} 2 & 4 \\ 3 & 6 \\ 4 & 8 \\ 5 & 10 \end{bmatrix}$$
1. Center the data by subtracting feature means.
2. Compute the sample covariance matrix $\Sigma$.
3. Find the eigenvalues $\lambda_1, \lambda_2$ by solving the characteristic equation $|\Sigma - \lambda I| = 0$.
4. Determine the eigenvector $\mathbf{v}_1$ corresponding to the largest eigenvalue.
5. Compute the explained variance ratio of the first principal component.
6. Project the centered data points onto the first principal component.

---

### Step-by-Step Solution

#### Step 1: Mean Centering
- Mean of Feature 1: $\mu_1 = \frac{2 + 3 + 4 + 5}{4} = \frac{14}{4} = 3.5$
- Mean of Feature 2: $\mu_2 = \frac{4 + 6 + 8 + 10}{4} = \frac{28}{4} = 7.0$

Subtract means from each row:
$$X_{\text{centered}} = \begin{bmatrix} 2 - 3.5 & 4 - 7.0 \\ 3 - 3.5 & 6 - 7.0 \\ 4 - 3.5 & 8 - 7.0 \\ 5 - 3.5 & 10 - 7.0 \end{bmatrix} = \begin{bmatrix} -1.5 & -3.0 \\ -0.5 & -1.0 \\ +0.5 & +1.0 \\ +1.5 & +3.0 \end{bmatrix}$$

#### Step 2: Compute Sample Covariance Matrix $\Sigma$
Using $m = 4$ samples ($\Sigma = \frac{1}{m} X^T X$):
- $\text{Var}(x_1) = \frac{(-1.5)^2 + (-0.5)^2 + (0.5)^2 + (1.5)^2}{4} = \frac{2.25 + 0.25 + 0.25 + 2.25}{4} = \frac{5.0}{4} = 1.25$
- $\text{Var}(x_2) = \frac{(-3)^2 + (-1)^2 + (1)^2 + (3)^2}{4} = \frac{9 + 1 + 1 + 9}{4} = \frac{20}{4} = 5.0$
- $\text{Cov}(x_1, x_2) = \frac{(-1.5)(-3) + (-0.5)(-1) + (0.5)(1) + (1.5)(3)}{4} = \frac{4.5 + 0.5 + 0.5 + 4.5}{4} = \frac{10.0}{4} = 2.5$

$$\Sigma = \begin{bmatrix} 1.25 & 2.5 \\ 2.5 & 5.0 \end{bmatrix}$$

#### Step 3: Solve the Characteristic Equation $\det(\Sigma - \lambda I) = 0$
$$\det \begin{bmatrix} 1.25 - \lambda & 2.5 \\ 2.5 & 5.0 - \lambda \end{bmatrix} = 0$$
$$(1.25 - \lambda)(5.0 - \lambda) - (2.5)^2 = 0$$
$$\lambda^2 - 6.25\lambda + 6.25 - 6.25 = 0$$
$$\lambda^2 - 6.25\lambda = 0 \implies \lambda(\lambda - 6.25) = 0$$

The eigenvalues are:
$$\boldsymbol{\lambda_1 = 6.25}, \quad \boldsymbol{\lambda_2 = 0.0}$$

#### Step 4: Find the Principal Eigenvector $\mathbf{v}_1$ for $\lambda_1 = 6.25$
Solve $(\Sigma - \lambda_1 I) \mathbf{v}_1 = \mathbf{0}$:
$$\begin{bmatrix} 1.25 - 6.25 & 2.5 \\ 2.5 & 5.0 - 6.25 \end{bmatrix} \begin{bmatrix} v_1 \\ v_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
$$\begin{bmatrix} -5.0 & 2.5 \\ 2.5 & -1.25 \end{bmatrix} \begin{bmatrix} v_1 \\ v_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
$$-5.0 v_1 + 2.5 v_2 = 0 \implies 2.5 v_2 = 5.0 v_1 \implies v_2 = 2 v_1$$

Choose $v_1 = 1 \implies v_2 = 2$.
Normalize to unit length:
$$\|\mathbf{v}\| = \sqrt{1^2 + 2^2} = \sqrt{1 + 4} = \sqrt{5}$$
$$\mathbf{v}_1 = \begin{bmatrix} \frac{1}{\sqrt{5}} \\ \frac{2}{\sqrt{5}} \end{bmatrix} \approx \begin{bmatrix} 0.4472 \\ 0.8944 \end{bmatrix}$$

#### Step 5: Explained Variance Ratio
$$\text{Total Variance} = \lambda_1 + \lambda_2 = 6.25 + 0.0 = 6.25$$
$$\text{Explained Variance Ratio}_1 = \frac{\lambda_1}{\lambda_1 + \lambda_2} = \frac{6.25}{6.25} = \mathbf{1.0 \quad (100\%)}$$
*(Because $x_2$ is perfectly collinear with $x_1$ ($x_2 = 2x_1$), the single first principal component captures 100% of all data variance with zero loss of information!)*

#### Step 6: Project Centered Points onto $\mathbf{v}_1$
$$y_i = \mathbf{x}_i^T \mathbf{v}_1 = x_{i1}(0.4472) + x_{i2}(0.8944)$$
- Point 1: $(-1.5 \times 0.4472) + (-3.0 \times 0.8944) = -0.6708 - 2.6832 = \mathbf{-3.354}$
- Point 2: $(-0.5 \times 0.4472) + (-1.0 \times 0.8944) = -0.2236 - 0.8944 = \mathbf{-1.118}$
- Point 3: $(+0.5 \times 0.4472) + (+1.0 \times 0.8944) = +0.2236 + 0.8944 = \mathbf{+1.118}$
- Point 4: $(+1.5 \times 0.4472) + (+3.0 \times 0.8944) = +0.6708 + 2.6832 = \mathbf{+3.354}$
