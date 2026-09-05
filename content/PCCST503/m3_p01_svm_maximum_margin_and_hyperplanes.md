# Module 3: Worked Problems — Support Vector Machines & Hyperplanes
## Progressive Problem Workbook: Canonical Planes, Margin Calculations, Slack Variables, and Kernel Transformations

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Topic:** Module 3 (SVM Calculations, Margins, and Kernel Matrices)  
> **Format:** Step-by-step numerical solutions with full algebraic derivations and no skipped steps.

---

# Problem 1: Canonical Hyperplane & Margin Calculation (Standard 2D)

### Problem Statement
A binary classification dataset has the following three training points in 2D space:
- **Class +1:** $\mathbf{x}_1 = [3, 3]^T$, $\mathbf{x}_2 = [4, 3]^T$
- **Class -1:** $\mathbf{x}_3 = [1, 1]^T$

1. Identify the support vectors.
2. Find the optimal weight vector $\mathbf{w} = [w_1, w_2]^T$ and bias $b$ for the canonical separating hyperplane.
3. Calculate the geometric margin width $M$.
4. Classify an unseen test query point $\mathbf{x}_{\text{test}} = [2, 1]^T$.

---

### Step-by-Step Solution

#### Step 1: Geometric Inspection & Candidate Support Vectors
Plotting the points:
- The negative point is $\mathbf{x}_3 = (1, 1)$.
- The closest positive point to $(1, 1)$ is $\mathbf{x}_1 = (3, 3)$.
- The point $\mathbf{x}_2 = (4, 3)$ lies further to the right ($x_1 = 4 > 3$), so the boundary is dictated by the vector connecting $(1, 1)$ and $(3, 3)$.
- Candidate support vectors: $\mathbf{x}_1 = [3, 3]^T$ (on positive margin) and $\mathbf{x}_3 = [1, 1]^T$ (on negative margin).

#### Step 2: Formulating the Canonical Equations
By definition of canonical support hyperplanes:
$$\mathbf{w}^T \mathbf{x}_+ + b = +1 \implies w_1(3) + w_2(3) + b = +1 \quad \text{--- (Equation 1)}$$
$$\mathbf{w}^T \mathbf{x}_- + b = -1 \implies w_1(1) + w_2(1) + b = -1 \quad \text{--- (Equation 2)}$$

Subtract Equation (2) from Equation (1):
$$[3w_1 + 3w_2 + b] - [w_1 + w_2 + b] = 1 - (-1)$$
$$2w_1 + 2w_2 = 2 \implies w_1 + w_2 = 1$$

Since the vector connecting $(1, 1)$ to $(3, 3)$ is $\Delta \mathbf{x} = [2, 2]^T$, the normal vector $\mathbf{w}$ is parallel to $[1, 1]^T$, meaning $w_1 = w_2$.
$$w_1 + w_1 = 1 \implies 2w_1 = 1 \implies w_1 = 0.5, \quad w_2 = 0.5$$

#### Step 3: Solving for Bias $b$
Substitute $w_1 = 0.5, w_2 = 0.5$ into Equation (2):
$$0.5(1) + 0.5(1) + b = -1 \implies 1.0 + b = -1 \implies b = -2.0$$

The optimal separating hyperplane is:
$$0.5 x_1 + 0.5 x_2 - 2 = 0 \quad \iff \quad x_1 + x_2 - 4 = 0$$

#### Step 4: Verification on Remaining Points
Check $\mathbf{x}_2 = [4, 3]^T$ with $y_2 = +1$:
$$y_2 (\mathbf{w}^T \mathbf{x}_2 + b) = (+1)(0.5(4) + 0.5(3) - 2) = (+1)(2 + 1.5 - 2) = 1.5 \ge 1 \quad \checkmark$$
Since $1.5 > 1$, $\mathbf{x}_2$ is safely outside the margin and not an active support vector.

#### Step 5: Calculate the Geometric Margin Width
$$\|\mathbf{w}\| = \sqrt{w_1^2 + w_2^2} = \sqrt{(0.5)^2 + (0.5)^2} = \sqrt{0.25 + 0.25} = \sqrt{0.5} = \frac{1}{\sqrt{2}} \approx 0.7071$$
$$\text{Margin Width } M = \frac{2}{\|\mathbf{w}\|} = \frac{2}{1/\sqrt{2}} = 2\sqrt{2} \approx \mathbf{2.8284}$$

#### Step 6: Classify Query Point $\mathbf{x}_{\text{test}} = [2, 1]^T$
Evaluate decision function:
$$f(\mathbf{x}_{\text{test}}) = \mathbf{w}^T \mathbf{x}_{\text{test}} + b = 0.5(2) + 0.5(1) - 2 = 1.0 + 0.5 - 2 = -0.5$$
$$\text{Predicted Class } \hat{y} = \text{sign}(-0.5) = \mathbf{-1}$$

---

# Problem 2: Soft-Margin SVM & Slack Variable Evaluation

### Problem Statement
An SVM model has learned the hyperplane $w_1 x_1 + w_2 x_2 + b = 0$ with parameters:
$$\mathbf{w} = [1.0, 1.0]^T, \quad b = -3.0$$
The canonical positive margin is $\mathbf{w}^T \mathbf{x} + b = +1$ and the negative margin is $\mathbf{w}^T \mathbf{x} + b = -1$.

For each of the following training instances, determine whether it satisfies the margin or calculate its exact slack variable $\xi_i$:
1. Point $A$: $\mathbf{x}_A = [4, 2]^T$ with true label $y_A = +1$.
2. Point $B$: $\mathbf{x}_B = [2, 2]^T$ with true label $y_B = +1$.
3. Point $C$: $\mathbf{x}_C = [1.5, 1.0]^T$ with true label $y_C = +1$.
4. Point $D$: $\mathbf{x}_D = [0, 1]^T$ with true label $y_D = -1$.

---

### Step-by-Step Solution

::: callout-formula Slack Variable Formula
Recall the soft-margin constraint: $y_i(\mathbf{w}^T \mathbf{x}_i + b) \ge 1 - \xi_i$ with $\xi_i \ge 0$.
$$\xi_i = \max\left(0, \; 1 - y_i(\mathbf{w}^T \mathbf{x}_i + b)\right)$$
:::

#### Instance A: $\mathbf{x}_A = [4, 2]^T, y_A = +1$
- Functional value: $\mathbf{w}^T \mathbf{x}_A + b = 1(4) + 1(2) - 3 = 6 - 3 = +3$.
- $y_A (\mathbf{w}^T \mathbf{x}_A + b) = (+1)(3) = 3$.
- Slack: $\xi_A = \max(0, 1 - 3) = \max(0, -2) = \mathbf{0}$.
- *Interpretation:* Correctly classified, lies safely outside the positive margin.

#### Instance B: $\mathbf{x}_B = [2, 2]^T, y_B = +1$
- Functional value: $\mathbf{w}^T \mathbf{x}_B + b = 1(2) + 1(2) - 3 = 4 - 3 = +1$.
- $y_B (\mathbf{w}^T \mathbf{x}_B + b) = (+1)(1) = 1$.
- Slack: $\xi_B = \max(0, 1 - 1) = \mathbf{0}$.
- *Interpretation:* Lies exactly on the positive canonical margin boundary. This is an active support vector.

#### Instance C: $\mathbf{x}_C = [1.5, 1.0]^T, y_C = +1$
- Functional value: $\mathbf{w}^T \mathbf{x}_C + b = 1(1.5) + 1(1.0) - 3 = 2.5 - 3 = -0.5$.
- $y_C (\mathbf{w}^T \mathbf{x}_C + b) = (+1)(-0.5) = -0.5$.
- Slack: $\xi_C = \max(0, 1 - (-0.5)) = \max(0, 1.5) = \mathbf{1.5}$.
- *Interpretation:* Because $\xi_C > 1$, this point crosses over the decision boundary ($f(x) < 0$) and is **misclassified**!

#### Instance D: $\mathbf{x}_D = [0, 1]^T, y_D = -1$
- Functional value: $\mathbf{w}^T \mathbf{x}_D + b = 1(0) + 1(1) - 3 = -2$.
- $y_D (\mathbf{w}^T \mathbf{x}_D + b) = (-1)(-2) = +2$.
- Slack: $\xi_D = \max(0, 1 - 2) = \max(0, -1) = \mathbf{0}$.
- *Interpretation:* Correctly classified, lies beyond the negative margin.

---

# Problem 3: Polynomial Kernel Gram Matrix Evaluation

### Problem Statement
Consider three 2D instances:
$$\mathbf{x}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad \mathbf{x}_2 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}, \quad \mathbf{x}_3 = \begin{bmatrix} 0 \\ 2 \end{bmatrix}$$
Using the quadratic polynomial kernel $K(\mathbf{x}, \mathbf{z}) = (\mathbf{x}^T \mathbf{z} + 1)^2$, compute the full $3 \times 3$ **Gram Matrix** (Kernel Matrix) $K$.

---

### Step-by-Step Solution

#### Step 1: Pairwise Dot Products ($\mathbf{x}_i^T \mathbf{x}_j$)
- $\mathbf{x}_1^T \mathbf{x}_1 = (1)(1) + (0)(0) = 1$
- $\mathbf{x}_1^T \mathbf{x}_2 = (1)(1) + (0)(1) = 1$
- $\mathbf{x}_1^T \mathbf{x}_3 = (1)(0) + (0)(2) = 0$
- $\mathbf{x}_2^T \mathbf{x}_2 = (1)(1) + (1)(1) = 2$
- $\mathbf{x}_2^T \mathbf{x}_3 = (1)(0) + (1)(2) = 2$
- $\mathbf{x}_3^T \mathbf{x}_3 = (0)(0) + (2)(2) = 4$

#### Step 2: Applying the Kernel Formula $K_{ij} = (\mathbf{x}_i^T \mathbf{x}_j + 1)^2$
- $K_{11} = (1 + 1)^2 = 2^2 = \mathbf{4}$
- $K_{12} = (1 + 1)^2 = 2^2 = \mathbf{4}$
- $K_{13} = (0 + 1)^2 = 1^2 = \mathbf{1}$
- $K_{21} = K_{12} = \mathbf{4}$ (by symmetry)
- $K_{22} = (2 + 1)^2 = 3^2 = \mathbf{9}$
- $K_{23} = (2 + 1)^2 = 3^2 = \mathbf{9}$
- $K_{31} = K_{13} = \mathbf{1}$
- $K_{32} = K_{23} = \mathbf{9}$
- $K_{33} = (4 + 1)^2 = 5^2 = \mathbf{25}$

#### Step 3: The Complete Gram Matrix:
$$K = \begin{bmatrix} 4 & 4 & 1 \\ 4 & 9 & 9 \\ 1 & 9 & 25 \end{bmatrix}$$
*Notice that $K$ is symmetric ($K = K^T$) and all diagonal elements are strictly positive, satisfying Mercer's prerequisite.*

---

# Problem 4: Radial Basis Function (RBF / Gaussian) Kernel Calculation

### Problem Statement
Given two points in 2D space:
$$\mathbf{x}_1 = [2, 3]^T, \quad \mathbf{x}_2 = [5, 7]^T$$
1. Calculate the squared Euclidean distance $\|\mathbf{x}_1 - \mathbf{x}_2\|^2$.
2. Compute the RBF kernel value $K(\mathbf{x}_1, \mathbf{x}_2) = \exp(-\gamma \|\mathbf{x}_1 - \mathbf{x}_2\|^2)$ for $\gamma = 0.05$.
3. What is the value of $K(\mathbf{x}_1, \mathbf{x}_1)$?

---

### Step-by-Step Solution
1. **Squared Euclidean Distance:**
   $$\|\mathbf{x}_1 - \mathbf{x}_2\|^2 = (2 - 5)^2 + (3 - 7)^2 = (-3)^2 + (-4)^2 = 9 + 16 = \mathbf{25}$$
2. **RBF Kernel Evaluation:**
   $$K(\mathbf{x}_1, \mathbf{x}_2) = \exp(-0.05 \times 25) = \exp(-1.25) = \frac{1}{e^{1.25}} \approx \frac{1}{3.4903} \approx \mathbf{0.2865}$$
3. **Self-Similarity $K(\mathbf{x}_1, \mathbf{x}_1)$:**
   $$\|\mathbf{x}_1 - \mathbf{x}_1\|^2 = 0 \implies K(\mathbf{x}_1, \mathbf{x}_1) = \exp(0) = \mathbf{1.0}$$
   *(The RBF kernel value is always exactly 1.0 between a point and itself, and decays towards 0 as distance increases).*
