# Progressive Problems: 0/1 Knapsack (Dynamic Programming Tabular Traces)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic algebra.

---

## Level 1: Standard 4-Item 0/1 Knapsack Problem

### Problem 1.1: Complete DP Matrix Construction and Backtracking Trace

A thief has a knapsack with maximum weight capacity $W = 5$. There are $n = 4$ items with the following weights and values:
* Item 1: Weight $w_1 = 2$, Value $v_1 = 12$
* Item 2: Weight $w_2 = 1$, Value $v_2 = 10$
* Item 3: Weight $w_3 = 3$, Value $v_3 = 20$
* Item 4: Weight $w_4 = 2$, Value $v_4 = 15$

Find:
1. The maximum total value achievable within capacity $W = 5$.
2. The exact subset of items chosen using the dynamic programming table backtracking method.

::: callout-intuition Core Mental Model
Unlike the spice-bazaar fractional problem where we could scoop half a bag of cinnamon, here items are indivisible electronics (laptops, cameras). You either take the whole item ($x_i = 1$) or leave it behind ($x_i = 0$).
For every item $i$ and every possible knapsack size $w \in \{0, 1, \dots, W\}$, we ask one question:
*"If I have room for this item, is my total profit higher if I skip it (inherit value from row above) OR if I take it (add its value to the best solution for the remaining weight)?"*
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Understand the Recurrence Relation</summary>

**Where did the formula come from?** The 0/1 Knapsack Bellman optimality equation:

$$V[i, w] = \begin{cases} 
0 & \text{if } i = 0 \text{ or } w = 0, \\
V[i-1, w] & \text{if } w_i > w \text{ (Item does not fit)}, \\
\max\Big(V[i-1, w], \; V[i-1, w - w_i] + v_i\Big) & \text{if } w_i \le w \text{ (Item fits)}.
\end{cases}$$

* $V[i, w]$: Maximum profit achievable using a subset of the first $i$ items with weight capacity $w$.
* Dimensions of table: $(n+1) \times (W+1) = 5 \times 6 = 30$ cells.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Base Cases (Row 0 and Column 0)</summary>

**What are we doing?** Fill Row 0 ($i = 0$, zero items available) and Column 0 ($w = 0$, zero capacity).
* For all $w \in \{0, \dots, 5\}$: $V[0, w] = 0$.
* For all $i \in \{0, \dots, 4\}$: $V[i, 0] = 0$.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Fill Row 1 (Item 1: w1 = 2, v1 = 12)</summary>

* For $w = 0$: $V[1, 0] = 0$.
* For $w = 1$: $w_1 (2) > 1 \implies$ Doesn't fit: $V[1, 1] = V[0, 1] = 0$.
* For $w = 2$: Fits! $\max(V[0, 2], V[0, 2 - 2] + 12) = \max(0, 0 + 12) = \mathbf{12}$.
* For $w = 3$: Fits! $\max(V[0, 3], V[0, 3 - 2] + 12) = \max(0, 0 + 12) = \mathbf{12}$.
* For $w = 4$: Fits! $\max(0, 12) = \mathbf{12}$.
* For $w = 5$: Fits! $\max(0, 12) = \mathbf{12}$.

Row 1 entries: `[0, 0, 12, 12, 12, 12]`.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Fill Row 2 (Item 2: w2 = 1, v2 = 10)</summary>

* For $w = 1$: Fits! $\max(V[1, 1], V[1, 1-1] + 10) = \max(0, 0 + 10) = \mathbf{10}$.
* For $w = 2$: Fits! $\max(V[1, 2], V[1, 2-1] + 10) = \max(12, 0 + 10) = \mathbf{12}$ (Better to keep Item 1!).
* For $w = 3$: Fits! $\max(V[1, 3], V[1, 3-1] + 10) = \max(12, 12 + 10) = \mathbf{22}$ (Take both Item 1 and Item 2!).
* For $w = 4$: Fits! $\max(V[1, 4], V[1, 4-1] + 10) = \max(12, 12 + 10) = \mathbf{22}$.
* For $w = 5$: Fits! $\max(V[1, 5], V[1, 5-1] + 10) = \max(12, 12 + 10) = \mathbf{22}$.

Row 2 entries: `[0, 10, 12, 22, 22, 22]`.
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Fill Row 3 (Item 3: w3 = 3, v3 = 20)</summary>

* For $w = 1$: $w_3 (3) > 1 \implies V[3, 1] = V[2, 1] = \mathbf{10}$.
* For $w = 2$: $w_3 (3) > 2 \implies V[3, 2] = V[2, 2] = \mathbf{12}$.
* For $w = 3$: Fits! $\max(V[2, 3], V[2, 3-3] + 20) = \max(22, 0 + 20) = \mathbf{22}$.
* For $w = 4$: Fits! $\max(V[2, 4], V[2, 4-3] + 20) = \max(22, V[2, 1] + 20) = \max(22, 10 + 20) = \mathbf{30}$ (Item 2 + Item 3!).
* For $w = 5$: Fits! $\max(V[2, 5], V[2, 5-3] + 20) = \max(22, V[2, 2] + 20) = \max(22, 12 + 20) = \mathbf{32}$ (Item 1 + Item 3!).

Row 3 entries: `[0, 10, 12, 22, 30, 32]`.
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Fill Row 4 (Item 4: w4 = 2, v4 = 15)</summary>

* For $w = 1$: $w_4 (2) > 1 \implies V[4, 1] = V[3, 1] = \mathbf{10}$.
* For $w = 2$: Fits! $\max(V[3, 2], V[3, 2-2] + 15) = \max(12, 15) = \mathbf{15}$.
* For $w = 3$: Fits! $\max(V[3, 3], V[3, 3-2] + 15) = \max(22, 10 + 15) = \mathbf{25}$.
* For $w = 4$: Fits! $\max(V[3, 4], V[3, 4-2] + 15) = \max(30, 12 + 15) = \mathbf{30}$.
* For $w = 5$: Fits! $\max(V[3, 5], V[3, 5-2] + 15) = \max(32, V[3, 3] + 15) = \max(32, 22 + 15) = \mathbf{37}^*$.

Row 4 entries: `[0, 10, 15, 25, 30, 37]`.
</details>

<details class="step-card">
<summary class="step-badge">Step 7: The Complete DP Table</summary>

| $i$ \ $w$ | $w = 0$ | $w = 1$ | $w = 2$ | $w = 3$ | $w = 4$ | $w = 5$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$i = 0$** | 0 | 0 | 0 | 0 | 0 | 0 |
| **$i = 1$** ($w=2, v=12$) | 0 | 0 | 12 | 12 | 12 | 12 |
| **$i = 2$** ($w=1, v=10$) | 0 | 10 | 12 | 22 | 22 | 22 |
| **$i = 3$** ($w=3, v=20$) | 0 | 10 | 12 | 22 | 30 | 32 |
| **$i = 4$** ($w=2, v=15$) | 0 | 10 | 15 | 25 | 30 | **37** |

Maximum achievable profit is $V[4, 5] = \mathbf{37}$.
</details>

<details class="step-card">
<summary class="step-badge">Step 8: Backtracking to Reconstruct Selected Items</summary>

1. Start at cell $(4, 5)$: Value $= 37$.
   * Look at cell directly above $(3, 5)$: Value $= 32$.
   * Since $V[4, 5] \ne V[3, 5]$ ($37 \ne 32$), **Item 4 WAS INCLUDED!**
   * Deduct weight of Item 4 ($w_4 = 2$): New capacity $w = 5 - 2 = 3$.
   * Move to cell $(3, 3)$.
2. At cell $(3, 3)$: Value $= 22$.
   * Look at cell directly above $(2, 3)$: Value $= 22$.
   * Since $V[3, 3] == V[2, 3]$ ($22 == 22$), **Item 3 WAS NOT INCLUDED!**
   * Capacity remains $w = 3$. Move to cell $(2, 3)$.
3. At cell $(2, 3)$: Value $= 22$.
   * Look at cell directly above $(1, 3)$: Value $= 12$.
   * Since $V[2, 3] \ne V[1, 3]$ ($22 \ne 12$), **Item 2 WAS INCLUDED!**
   * Deduct weight of Item 2 ($w_2 = 1$): New capacity $w = 3 - 1 = 2$.
   * Move to cell $(1, 2)$.
4. At cell $(1, 2)$: Value $= 12$.
   * Look at cell directly above $(0, 2)$: Value $= 0$.
   * Since $V[1, 2] \ne V[0, 2]$ ($12 \ne 0$), **Item 1 WAS INCLUDED!**
   * Deduct weight of Item 1 ($w_1 = 2$): New capacity $w = 2 - 2 = 0$.
   * Capacity is 0; trace finishes.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Summary of Optimal Items</summary>

* **Optimal Item Subset:** $\{\text{Item 1}, \text{Item 2}, \text{Item 4}\}$
* **Total Weight:** $w_1 + w_2 + w_4 = 2 + 1 + 2 = \mathbf{5} \le 5$.
* **Total Value:** $v_1 + v_2 + v_4 = 12 + 10 + 15 = \mathbf{37}$.
</details>

</div>
