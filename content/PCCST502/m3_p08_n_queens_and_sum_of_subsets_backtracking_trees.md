# Progressive Problems: Backtracking (N-Queens & Sum of Subsets State-Space Trees)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic algebra.

---

## Level 1: 4-Queens Problem Complete State-Space Pruned Tree

### Problem 1.1: Complete State-Space Search for N = 4

Trace the complete backtracking execution for the 4-Queens problem on a $4 \times 4$ chessboard.
Enumerate all generated nodes, explicitly state why dead nodes are pruned, and produce all valid solutions.

::: callout-intuition Core Mental Model
Imagine you are placing 4 guards on a $4 \times 4$ grid, one in each row.
* As soon as you place a guard that stares directly at another guard down a column or diagonal, you don't waste time trying to place the next guard.
* You immediately remove the guard you just placed and slide her to the next column.
* If all columns in that row are blocked, you step back to the previous row and adjust that guard instead.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: The Diagonal and Column Conflict Rules</div>

For a board representation $X = \langle x_1, x_2, \dots, x_k \rangle$ where $x_i$ is the column of the queen in row $i$:
* **Column Conflict:** $x_k = x_j$ for some $j < k$.
* **Diagonal Conflict:** $|x_k - x_j| = |k - j|$ for some $j < k$.
* A placement is safe if and only if both checks pass for all $j \in \{1, \dots, k-1\}$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Subtree Under x1 = 1 (Tracing to Complete Dead-End)</div>

1. Place $x_1 = 1$: Board $\langle 1 \rangle$.
2. Row 2:
   * $x_2 = 1$: Column conflict with $x_1$. Pruned.
   * $x_2 = 2$: $|2 - 1| = |2 - 1| \implies$ Diagonal conflict. Pruned.
   * $x_2 = 3$: Safe! Board $\langle 1, 3 \rangle$.
     * Row 3 under $\langle 1, 3 \rangle$:
       * $x_3 = 1$: Col conflict with $x_1$. Pruned.
       * $x_3 = 2$: $|2 - 3| = |3 - 2| \implies$ Diagonal conflict with $x_2$. Pruned.
       * $x_3 = 3$: Col conflict with $x_2$. Pruned.
       * $x_3 = 4$: $|4 - 3| = |3 - 2| \implies$ Diagonal conflict with $x_2$. Pruned.
       * All columns dead! Backtrack to Row 2.
   * $x_2 = 4$: Safe! Board $\langle 1, 4 \rangle$.
     * Row 3 under $\langle 1, 4 \rangle$:
       * $x_3 = 1$: Col conflict. Pruned.
       * $x_3 = 2$: Safe! Board $\langle 1, 4, 2 \rangle$.
         * Row 4 under $\langle 1, 4, 2 \rangle$:
           * $x_4 = 1$: Col conflict with $x_1$. Pruned.
           * $x_4 = 2$: Col conflict with $x_3$. Pruned.
           * $x_4 = 3$: Diagonal with $x_3$ ($|3 - 2| = |4 - 3|$). Pruned.
           * $x_4 = 4$: Col conflict with $x_2$. Pruned.
           * All columns dead! Backtrack.
       * $x_3 = 3$: Diagonal with $x_2$ ($|3 - 4| = |3 - 2|$). Pruned.
       * $x_3 = 4$: Col conflict. Pruned.
3. Subtree under $x_1 = 1$ is exhausted with **zero valid solutions**. Backtrack to Row 1!
</div>

<div class="step-card">
<div class="step-badge">Step 3: Subtree Under x1 = 2 (Reaching Solution 1)</div>

1. Place $x_1 = 2$: Board $\langle 2 \rangle$.
2. Row 2:
   * $x_2 = 1, 2, 3$ all fail conflict checks.
   * $x_2 = 4$: Safe! Board $\langle 2, 4 \rangle$.
3. Row 3:
   * $x_3 = 1$: Safe! ($1 \ne 2, 4$ and $|1-2|=1 \ne 2, |1-4|=3 \ne 1$).
   * Board: $\langle 2, 4, 1 \rangle$.
4. Row 4:
   * $x_4 = 1$: Col conflict.
   * $x_4 = 2$: Col conflict.
   * $x_4 = 3$: Check against:
     * $x_1=2$: $|3-2|=1 \ne 3$. Safe!
     * $x_2=4$: $|3-4|=1 \ne 2$. Safe!
     * $x_3=1$: $|3-1|=2 \ne 1$. Safe!
   * **ALL CHECKS PASS!**
   * **SOLUTION 1 FOUND:** $\mathbf{X = \langle 2, \; 4, \; 1, \; 3 \rangle}$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Subtree Under x1 = 3 (Reaching Solution 2 via Symmetry)</div>

1. Place $x_1 = 3$: Board $\langle 3 \rangle$.
2. Row 2: $x_2 = 1$ is safe! Board $\langle 3, 1 \rangle$.
3. Row 3: $x_3 = 4$ is safe! Board $\langle 3, 1, 4 \rangle$.
4. Row 4: $x_4 = 2$ is safe!
   * **SOLUTION 2 FOUND:** $\mathbf{X = \langle 3, \; 1, \; 4, \; 2 \rangle}$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Complete 4-Queens Solution Set</div>

The 4-Queens problem has exactly **2 distinct solutions**:
1. Solution 1: $\mathbf{\langle 2, 4, 1, 3 \rangle}$
2. Solution 2: $\mathbf{\langle 3, 1, 4, 2 \rangle}$
</div>

</div>

---

## Level 2: Sum of Subsets Bounding Tree

### Problem 2.1: Pruned Binary Tree for W = {2, 4, 6, 8}, M = 10

Find all subsets of $W = \{2, 4, 6, 8\}$ that sum to $M = 10$.
Show which branches are pruned by:
* Bound 1: Exceeding capacity ($s + w_{k+1} > M$)
* Bound 2: Insufficient remaining weight ($s + r < M$)

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Setup and Initialization</div>

* Weights: $w_1 = 2, w_2 = 4, w_3 = 6, w_4 = 8$ (Sorted).
* Target $M = 10$. Total weight $r = 2 + 4 + 6 + 8 = 20$.
* Binary choice at each level $k$: $x_k = 1$ (include $w_k$) or $x_k = 0$ (exclude $w_k$).
</div>

<div class="step-card">
<div class="step-badge">Step 2: Trace Path 1 (x1 = 1, include 2)</div>

* Current sum $s = 2$, remaining $r = 20 - 2 = 18$.
* **Include $w_2 = 4$ ($x_2 = 1$):**
  * New $s = 2 + 4 = 6$, $r = 18 - 4 = 14$.
  * Can we include $w_3 = 6$? $s + w_3 = 6 + 6 = 12 > 10$. **PRUNED BY BOUND 1!**
  * Can we exclude $w_3$ and include $w_4 = 8$? $s + w_4 = 6 + 8 = 14 > 10$. **PRUNED BY BOUND 1!**
* **Exclude $w_2 = 4$ ($x_2 = 0$):**
  * $s = 2, r = 14$.
  * Can we include $w_3 = 6$? $s + w_3 = 2 + 6 = 8 \le 10$.
  * **Include $w_3 = 6$ ($x_3 = 1$):**
    * New $s = 8$. Remaining $w_4 = 8$.
    * Try $w_4$: $8 + 8 = 16 > 10$. Exclude $w_4$: $s = 8 \ne 10$. (Dead end).
  * **Exclude $w_3 = 6$ ($x_3 = 0$):**
    * $s = 2, r = 8$.
    * Try include $w_4 = 8$ ($x_4 = 1$):
    * New sum: $s + w_4 = 2 + 8 = \mathbf{10 == M}$!
    * **SOLUTION 1 FOUND:** $x = \langle 1, 0, 0, 1 \rangle \implies \mathbf{\{2, 8\}}$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Trace Path 2 (x1 = 0, exclude 2)</div>

* Current sum $s = 0$, remaining $r = 18$.
* **Include $w_2 = 4$ ($x_2 = 1$):**
  * New $s = 4, r = 18 - 4 = 14$.
  * **Include $w_3 = 6$ ($x_3 = 1$):**
    * New sum $s = 4 + 6 = \mathbf{10 == M}$!
    * **SOLUTION 2 FOUND:** $x = \langle 0, 1, 1, 0 \rangle \implies \mathbf{\{4, 6\}}$.
  * **Exclude $w_3 = 6$ ($x_3 = 0$):**
    * $s = 4$. Remaining $w_4 = 8$.
    * $s + w_4 = 4 + 8 = 12 > 10$. Exceeds $M$. Pruned!
* **Exclude $w_2 = 4$ ($x_2 = 0$):**
  * $s = 0, r = 14$.
  * Include $w_3 = 6$: $s = 6, r = 8$. If include $w_4 = 8 \implies 14 > 10$. If exclude $w_4 \implies 6 \ne 10$.
  * Exclude $w_3 = 6$: $s = 0, r = 8$. Even including $w_4 = 8$, sum is $8 < 10$. **PRUNED BY BOUND 2 ($s + r < M$)!**
</div>

<div class="step-card">
<div class="step-badge">Final Step: Complete Sum of Subsets Solutions</div>

The valid subsets summing to $M = 10$ are:
1. $\mathbf{\{2, 8\}}$ with vector $\langle 1, 0, 0, 1 \rangle$
2. $\mathbf{\{4, 6\}}$ with vector $\langle 0, 1, 1, 0 \rangle$
</div>

</div>
