# Progressive Problems: All-Pairs Shortest Paths (Floyd-Warshall & Transitive Closure)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic algebra.

---

## Level 1: Floyd-Warshall 4-Vertex Complete Matrix Transformation Trace

### Problem 1.1: Tracing $D^{(0)}$ to $D^{(4)}$

Compute all-pairs shortest path distances for the directed graph with 4 vertices $\{1, 2, 3, 4\}$ and adjacency matrix:

$$D^{(0)} = \begin{bmatrix}
0 & 3 & \infty & 7 \\
8 & 0 & 2 & \infty \\
5 & \infty & 0 & 1 \\
2 & \infty & \infty & 0
\end{bmatrix}$$

Show the complete state of matrices $D^{(1)}, D^{(2)}, D^{(3)}, D^{(4)}$.

::: callout-intuition Core Mental Model
In the Floyd-Warshall algorithm, we incrementally unlock new intermediate transit airports:
* Phase 0: Only non-stop direct flights are allowed.
* Phase 1: You are allowed to layover at Airport 1. Can anybody reach their destination faster by transferring through 1?
* Phase 2: You can layover at Airport 1 and/or Airport 2.
* ...
* Phase 4: All airports are available as layovers. Every possible shortcut has been found.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: The Floyd-Warshall Recurrence</div>

For step $k \in \{1, 2, 3, 4\}$:
$$D^{(k)}[i, j] = \min\Big(D^{(k-1)}[i, j], \; D^{(k-1)}[i, k] + D^{(k-1)}[k, j]\Big)$$

* **Row $k$ and Column $k$ never change** during iteration $k$ (since $D[k, k] = 0$).
* The diagonal $D[i, i]$ remains $0$ (assuming no negative cycles).
</div>

<div class="step-card">
<div class="step-badge">Step 2: Compute D^(1) (Intermediate Vertex 1)</div>

* **Pivot:** Row 1 (`[0, 3, ∞, 7]`) and Column 1 (`[0, 8, 5, 2]^T`).
* Let's test non-pivot cells:
  * $D^{(1)}[2, 3] = \min(2, D^{(0)}[2, 1] + D^{(0)}[1, 3]) = \min(2, 8 + \infty) = 2$.
  * $D^{(1)}[2, 4] = \min(\infty, D^{(0)}[2, 1] + D^{(0)}[1, 4]) = \min(\infty, 8 + 7 = 15) \implies \mathbf{15}$.
  * $D^{(1)}[3, 2] = \min(\infty, D^{(0)}[3, 1] + D^{(0)}[1, 2]) = \min(\infty, 5 + 3 = 8) \implies \mathbf{8}$.
  * $D^{(1)}[3, 4] = \min(1, 5 + 7) = 1$.
  * $D^{(1)}[4, 2] = \min(\infty, D^{(0)}[4, 1] + D^{(0)}[1, 2]) = \min(\infty, 2 + 3 = 5) \implies \mathbf{5}$.
  * $D^{(1)}[4, 3] = \min(\infty, 2 + \infty) = \infty$.

$$D^{(1)} = \begin{bmatrix}
0 & 3 & \infty & 7 \\
8 & 0 & 2 & \mathbf{15} \\
5 & \mathbf{8} & 0 & 1 \\
2 & \mathbf{5} & \infty & 0
\end{bmatrix}$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Compute D^(2) (Intermediate Vertex 2)</div>

* **Pivot:** Row 2 (`[8, 0, 2, 15]`) and Column 2 (`[3, 0, 8, 5]^T`).
* Test cells:
  * $D^{(2)}[1, 3] = \min(\infty, D^{(1)}[1, 2] + D^{(1)}[2, 3]) = \min(\infty, 3 + 2 = 5) \implies \mathbf{5}$.
  * $D^{(2)}[1, 4] = \min(7, 3 + 15) = 7$.
  * $D^{(2)}[3, 1] = \min(5, 8 + 8) = 5$.
  * $D^{(2)}[3, 4] = \min(1, 8 + 15) = 1$.
  * $D^{(2)}[4, 1] = \min(2, 5 + 8) = 2$.
  * $D^{(2)}[4, 3] = \min(\infty, D^{(1)}[4, 2] + D^{(1)}[2, 3]) = \min(\infty, 5 + 2 = 7) \implies \mathbf{7}$.

$$D^{(2)} = \begin{bmatrix}
0 & 3 & \mathbf{5} & 7 \\
8 & 0 & 2 & 15 \\
5 & 8 & 0 & 1 \\
2 & 5 & \mathbf{7} & 0
\end{bmatrix}$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Compute D^(3) (Intermediate Vertex 3)</div>

* **Pivot:** Row 3 (`[5, 8, 0, 1]`) and Column 3 (`[5, 2, 0, 7]^T`).
* Test cells:
  * $D^{(3)}[1, 2] = \min(3, 5 + 8) = 3$.
  * $D^{(3)}[1, 4] = \min(7, D^{(2)}[1, 3] + D^{(2)}[3, 4]) = \min(7, 5 + 1 = 6) \implies \mathbf{6}$.
  * $D^{(3)}[2, 1] = \min(8, D^{(2)}[2, 3] + D^{(2)}[3, 1]) = \min(8, 2 + 5 = 7) \implies \mathbf{7}$.
  * $D^{(3)}[2, 4] = \min(15, D^{(2)}[2, 3] + D^{(2)}[3, 4]) = \min(15, 2 + 1 = 3) \implies \mathbf{3}$.
  * $D^{(3)}[4, 1] = \min(2, 7 + 5) = 2$.
  * $D^{(3)}[4, 2] = \min(5, 7 + 8) = 5$.

$$D^{(3)} = \begin{bmatrix}
0 & 3 & 5 & \mathbf{6} \\
\mathbf{7} & 0 & 2 & \mathbf{3} \\
5 & 8 & 0 & 1 \\
2 & 5 & 7 & 0
\end{bmatrix}$$
</div>

<div class="step-card">
<div class="step-badge">Step 5: Compute D^(4) (Intermediate Vertex 4)</div>

* **Pivot:** Row 4 (`[2, 5, 7, 0]`) and Column 4 (`[6, 3, 1, 0]^T`).
* Test cells:
  * $D^{(4)}[1, 2] = \min(3, 6 + 5) = 3$.
  * $D^{(4)}[1, 3] = \min(5, 6 + 7) = 5$.
  * $D^{(4)}[2, 1] = \min(7, D^{(3)}[2, 4] + D^{(3)}[4, 1]) = \min(7, 3 + 2 = 5) \implies \mathbf{5}$.
  * $D^{(4)}[3, 1] = \min(5, D^{(3)}[3, 4] + D^{(3)}[4, 1]) = \min(5, 1 + 2 = 3) \implies \mathbf{3}$.
  * $D^{(4)}[3, 2] = \min(8, D^{(3)}[3, 4] + D^{(3)}[4, 2]) = \min(8, 1 + 5 = 6) \implies \mathbf{6}$.

$$D^{(4)} = \begin{bmatrix}
0 & 3 & 5 & 6 \\
\mathbf{5} & 0 & 2 & 3 \\
\mathbf{3} & \mathbf{6} & 0 & 1 \\
2 & 5 & 7 & 0
\end{bmatrix}$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Final APSP Matrix & Verification</div>

The final all-pairs shortest path matrix is:
$$D = \begin{bmatrix}
0 & 3 & 5 & 6 \\
5 & 0 & 2 & 3 \\
3 & 6 & 0 & 1 \\
2 & 5 & 7 & 0
\end{bmatrix}$$

Notice:
* Diagonal entries remain 0 $\implies$ No negative cycle.
* Every pair of vertices now possesses a finite shortest path distance.
</div>

</div>
