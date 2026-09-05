# Progressive Problems: Travelling Salesman Problem via Reduced Cost Matrix Branch and Bound

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic arithmetic.

---

## Level 1: 4-City Asymmetric TSP State-Space Tree

### Problem 1.1: Complete Least-Cost Branch and Bound Trace for a 4-City TSP

Given the 4-city cost matrix $A$:

$$A = \begin{bmatrix}
\infty & 10 & 15 & 20 \\
5 & \infty & 9 & 10 \\
6 & 13 & \infty & 12 \\
8 & 8 & 9 & \infty
\end{bmatrix}$$

Using the **Reduced Cost Matrix Least-Cost Branch and Bound (LC-BB)** method:
1. Compute the root node lower bound $\hat{c}(1)$ and reduced matrix $M_1$.
2. Branch to all valid children at Level 1 (Cities 2, 3, 4).
3. Expand the most promising node, update upper bound $U$, prune unviable paths, and state the optimal tour and minimum cost.

::: callout-intuition Core Mental Model
Think of the cost matrix as a table of flight prices.
* Every city must have a departure flight (one ticket from each row).
* Every city must have an arrival flight (one ticket into each column).
* The absolute cheapest ticket in each row and column sets a rock-bottom baseline price (the lower bound).
* Whenever you commit to flying from city $i$ to city $j$, you lock in that price and eliminate city $i$ departures and city $j$ arrivals forever.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Root Node Matrix Reduction (Node 1)</summary>

* **Row Reductions:**
  * Row 1: $\min(\infty, 10, 15, 20) = \mathbf{10}$. Subtract $10 \implies [\infty, 0, 5, 10]$.
  * Row 2: $\min(5, \infty, 9, 10) = \mathbf{5}$. Subtract $5 \implies [0, \infty, 4, 5]$.
  * Row 3: $\min(6, 13, \infty, 12) = \mathbf{6}$. Subtract $6 \implies [0, 7, \infty, 6]$.
  * Row 4: $\min(8, 8, 9, \infty) = \mathbf{8}$. Subtract $8 \implies [0, 0, 1, \infty]$.
  * Row Reduction Sum: $R_{\text{sum}} = 10 + 5 + 6 + 8 = \mathbf{29}$.

Row-reduced matrix $A'$:
$$A' = \begin{bmatrix}
\infty & 0 & 5 & 10 \\
0 & \infty & 4 & 5 \\
0 & 7 & \infty & 6 \\
0 & 0 & 1 & \infty
\end{bmatrix}$$

* **Column Reductions:**
  * Col 1 min: $0$ (contains 0).
  * Col 2 min: $0$ (contains 0).
  * Col 3: $\min(5, 4, \infty, 1) = \mathbf{1}$. Subtract $1 \implies [4, 3, \infty, 0]^T$.
  * Col 4: $\min(10, 5, 6, \infty) = \mathbf{5}$. Subtract $5 \implies [5, 0, 1, \infty]^T$.
  * Column Reduction Sum: $C_{\text{sum}} = 0 + 0 + 1 + 5 = \mathbf{6}$.

* **Base Lower Bound of Root Node 1:**
  $$\mathbf{\hat{c}(1) = R_{\text{sum}} + C_{\text{sum}} = 29 + 6 = 35}$$

Fully Reduced Matrix $M_1$:
$$M_1 = \begin{bmatrix}
\infty & 0 & 4 & 5 \\
0 & \infty & 3 & 0 \\
0 & 7 & \infty & 1 \\
0 & 0 & 0 & \infty
\end{bmatrix}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Level 1 Branching from City 1</summary>

We evaluate 3 outgoing edges from City 1: $(1, 2), (1, 3), (1, 4)$.

---

#### 1. Branch $(1, 2) \implies$ Child Node 2 (Path $1 \to 2$)
* Lookup cost in parent matrix: $M_1[1, 2] = \mathbf{0}$.
* Zero Row 1, Column 2, and set $M[2, 1] = \infty$:
  $$\begin{bmatrix}
  \infty & \infty & \infty & \infty \\
  \infty & \infty & 3 & 0 \\
  0 & \infty & \infty & 1 \\
  0 & \infty & 0 & \infty
  \end{bmatrix}$$
* Reductions:
  * Rows 2, 3, 4 all contain at least one 0.
  * Active columns (1, 3, 4) all contain at least one 0.
  * Additional reduction $r = \mathbf{0}$.
* Bound:
  $$\mathbf{\hat{c}(2) = \hat{c}(1) + M_1[1, 2] + r = 35 + 0 + 0 = 35}$$

---

#### 2. Branch $(1, 3) \implies$ Child Node 3 (Path $1 \to 3$)
* Lookup cost: $M_1[1, 3] = \mathbf{4}$.
* Zero Row 1, Column 3, and set $M[3, 1] = \infty$:
  $$\begin{bmatrix}
  \infty & \infty & \infty & \infty \\
  0 & \infty & \infty & 0 \\
  \infty & 7 & \infty & 1 \\
  0 & 0 & \infty & \infty
  \end{bmatrix}$$
* Reductions:
  * Row 3 min: $\min(\infty, 7, \infty, 1) = \mathbf{1}$. Subtract 1.
  * Col 1 min = 0, Col 2 min = 0, Col 4 min = 0.
  * Additional reduction $r = \mathbf{1}$.
* Bound:
  $$\mathbf{\hat{c}(3) = 35 + 4 + 1 = 40}$$

---

#### 3. Branch $(1, 4) \implies$ Child Node 4 (Path $1 \to 4$)
* Lookup cost: $M_1[1, 4] = \mathbf{5}$.
* Zero Row 1, Column 4, and set $M[4, 1] = \infty$:
  $$\begin{bmatrix}
  \infty & \infty & \infty & \infty \\
  0 & \infty & 3 & \infty \\
  0 & 7 & \infty & \infty \\
  \infty & 0 & 0 & \infty
  \end{bmatrix}$$
* Reductions: All rows and columns have a 0 $\implies r = 0$.
* Bound:
  $$\mathbf{\hat{c}(4) = 35 + 5 + 0 = 40}$$

---

#### Priority Queue after Level 1:
$$\text{Live Nodes} = \Big\{ \mathbf{\text{Node 2: } \hat{c}=35}, \; \text{Node 3: } \hat{c}=40, \; \text{Node 4: } \hat{c}=40 \Big\}$$
**Next E-Node:** **Node 2 ($\hat{c} = 35$, Path: $1 \to 2$)**.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Level 2 Branching from Node 2 (Path 1 -> 2)</summary>

From Node 2, unvisited cities are $\{3, 4\}$.

---

#### Branch $(2, 3) \implies$ Node 5 (Path $1 \to 2 \to 3$)
* Cost in $M_2$: $M_2[2, 3] = \mathbf{3}$.
* Zero Row 2, Column 3, and set $M[3, 1] = \infty$:
  $$\begin{bmatrix}
  \infty & \infty & \infty & \infty \\
  \infty & \infty & \infty & \infty \\
  \infty & \infty & \infty & 1 \\
  0 & \infty & \infty & \infty
  \end{bmatrix}$$
* Reductions: Row 3 min $= 1$. Additional reduction $r = \mathbf{1}$.
* Bound:
  $$\mathbf{\hat{c}(5) = 35 + 3 + 1 = 39}$$

---

#### Branch $(2, 4) \implies$ Node 6 (Path $1 \to 2 \to 4$)
* Cost in $M_2$: $M_2[2, 4] = \mathbf{0}$.
* Zero Row 2, Column 4, and set $M[4, 1] = \infty$:
  $$\begin{bmatrix}
  \infty & \infty & \infty & \infty \\
  \infty & \infty & \infty & \infty \\
  0 & \infty & \infty & \infty \\
  \infty & \infty & 0 & \infty
  \end{bmatrix}$$
* Reductions: All rows and cols have 0 $\implies r = 0$.
* Bound:
  $$\mathbf{\hat{c}(6) = 35 + 0 + 0 = 35}$$

Reduced Matrix $M_6$:
$$M_6 = \begin{bmatrix}
\infty & \infty & \infty & \infty \\
\infty & \infty & \infty & \infty \\
0 & \infty & \infty & \infty \\
\infty & \infty & 0 & \infty
\end{bmatrix}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Path Completion from Node 6 (Path 1 -> 2 -> 4)</summary>

The only remaining unvisited city is **City 3**.
The path must proceed:
$$1 \to 2 \to 4 \to 3 \to 1$$

* From matrix $M_6$:
  * Cost of edge $(4, 3) = M_6[4, 3] = 0$.
  * Cost of return edge $(3, 1) = M_6[3, 1] = 0$.

* **Complete Tour Cost:**
  $$\mathbf{\text{Cost}(1 \to 2 \to 4 \to 3 \to 1) = 35}$$

#### Update Global Upper Bound:
$$\mathbf{U \leftarrow 35}$$

#### Pruning All Live Nodes:
* Node 5 ($\hat{c} = 39 \ge 35$): **PRUNED!**
* Node 3 ($\hat{c} = 40 \ge 35$): **PRUNED!**
* Node 4 ($\hat{c} = 40 \ge 35$): **PRUNED!**
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Verification and Final Tour</summary>

Original cost verification from matrix $A$:
$$\text{Cost} = A[1, 2] + A[2, 4] + A[4, 3] + A[3, 1] = 10 + 10 + 9 + 6 = \mathbf{35}$$

* **Optimal Tour:** $\mathbf{1 \to 2 \to 4 \to 3 \to 1}$
* **Minimum Tour Cost:** $\mathbf{35}$
</details>

</div>
