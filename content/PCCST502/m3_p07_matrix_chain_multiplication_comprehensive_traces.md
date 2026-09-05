# Progressive Problems: Matrix Chain Multiplication (MCM Traces & Splits)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic algebra.

---

## Level 1: Standard 4-Matrix Chain Evaluation

### Problem 1.1: Tracing M and S Tables for p = <5, 10, 3, 12, 5>

Given a chain of 4 matrices $\langle A_1, A_2, A_3, A_4 \rangle$ with dimensions:
* $A_1$: $5 \times 10$ ($p_0 = 5, p_1 = 10$)
* $A_2$: $10 \times 3$ ($p_1 = 10, p_2 = 3$)
* $A_3$: $3 \times 12$ ($p_2 = 3, p_3 = 12$)
* $A_4$: $12 \times 5$ ($p_3 = 12, p_4 = 5$)
Dimension array: $p = \langle 5, 10, 3, 12, 5 \rangle$.

1. Compute the cost matrix $M[1..4, 1..4]$.
2. Compute the split matrix $S[1..3, 2..4]$.
3. Reconstruct the optimal parenthesization.

::: callout-intuition Core Mental Model
Imagine you are packing boxes into crates.
Whether you pack Box 1 and 2 together first, or Box 2 and 3 together first, changes the packing cost.
We solve this by checking small pairs of boxes first (chains of length 2), then trios (chains of length 3), and finally the entire set of four boxes (chain of length 4).
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: The MCM Recurrence Relation</summary>

$$m[i, j] = \begin{cases}
0 & \text{if } i = j, \\
\min_{i \le k < j} \Big\{ m[i, k] + m[k+1, j] + p_{i-1} p_k p_j \Big\} & \text{if } i < j.
\end{cases}$$

Base cases ($l = 1$):
$$m[1, 1] = 0, \quad m[2, 2] = 0, \quad m[3, 3] = 0, \quad m[4, 4] = 0$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Diagonal l = 2 (Chains of Length 2)</summary>

* **Cell $m[1, 2]$ ($A_1 A_2$):** $i = 1, j = 2, k = 1$.
  $$m[1, 2] = m[1, 1] + m[2, 2] + (p_0 \cdot p_1 \cdot p_2) = 0 + 0 + (5 \cdot 10 \cdot 3) = \mathbf{150}$$
  $s[1, 2] = 1$.
* **Cell $m[2, 3]$ ($A_2 A_3$):** $i = 2, j = 3, k = 2$.
  $$m[2, 3] = m[2, 2] + m[3, 3] + (p_1 \cdot p_2 \cdot p_3) = 0 + 0 + (10 \cdot 3 \cdot 12) = \mathbf{360}$$
  $s[2, 3] = 2$.
* **Cell $m[3, 4]$ ($A_3 A_4$):** $i = 3, j = 4, k = 3$.
  $$m[3, 4] = m[3, 3] + m[4, 4] + (p_2 \cdot p_3 \cdot p_4) = 0 + 0 + (3 \cdot 12 \cdot 5) = \mathbf{180}$$
  $s[3, 4] = 3$.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Diagonal l = 3 (Chains of Length 3)</summary>

* **Cell $m[1, 3]$ ($A_1 A_2 A_3$):** $i = 1, j = 3$, test $k \in \{1, 2\}$:
  * For $k = 1$: $m[1, 1] + m[2, 3] + (p_0 \cdot p_1 \cdot p_3) = 0 + 360 + (5 \cdot 10 \cdot 12) = 360 + 600 = 960$.
  * For $k = 2$: $m[1, 2] + m[3, 3] + (p_0 \cdot p_2 \cdot p_3) = 150 + 0 + (5 \cdot 3 \cdot 12) = 150 + 180 = 330$.
  * Minimum: $\min(960, 330) = \mathbf{330}$ at $k = 2$.
  $$\mathbf{m[1, 3] = 330, \quad s[1, 3] = 2}$$

* **Cell $m[2, 4]$ ($A_2 A_3 A_4$):** $i = 2, j = 4$, test $k \in \{2, 3\}$:
  * For $k = 2$: $m[2, 2] + m[3, 4] + (p_1 \cdot p_2 \cdot p_4) = 0 + 180 + (10 \cdot 3 \cdot 5) = 180 + 150 = 330$.
  * For $k = 3$: $m[2, 3] + m[4, 4] + (p_1 \cdot p_3 \cdot p_4) = 360 + 0 + (10 \cdot 12 \cdot 5) = 360 + 600 = 960$.
  * Minimum: $\min(330, 960) = \mathbf{330}$ at $k = 2$.
  $$\mathbf{m[2, 4] = 330, \quad s[2, 4] = 2}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Diagonal l = 4 (Full Chain m[1, 4])</summary>

$i = 1, j = 4$, test $k \in \{1, 2, 3\}$:
* For $k = 1$:
  $$m[1, 1] + m[2, 4] + (p_0 \cdot p_1 \cdot p_4) = 0 + 330 + (5 \cdot 10 \cdot 5) = 330 + 250 = \mathbf{580}$$
* For $k = 2$:
  $$m[1, 2] + m[3, 4] + (p_0 \cdot p_2 \cdot p_4) = 150 + 180 + (5 \cdot 3 \cdot 5) = 330 + 75 = \mathbf{405}$$
* For $k = 3$:
  $$m[1, 3] + m[4, 4] + (p_0 \cdot p_3 \cdot p_4) = 330 + 0 + (5 \cdot 12 \cdot 5) = 330 + 300 = \mathbf{630}$$
* Minimum: $\min(580, 405, 630) = \mathbf{405}$ at $k = 2$.
$$\mathbf{m[1, 4] = 405, \quad s[1, 4] = 2}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Final Matrices M and S</summary>

**Matrix M:**

| $i$ \ $j$ | $1$ | $2$ | $3$ | $4$ |
| :---: | :---: | :---: | :---: | :---: |
| **$1$** | $0$ | $150$ | $330$ | **$405$** |
| **$2$** | - | $0$ | $360$ | $330$ |
| **$3$** | - | - | $0$ | $180$ |
| **$4$** | - | - | - | $0$ |

**Matrix S:**

| $i$ \ $j$ | $2$ | $3$ | $4$ |
| :---: | :---: | :---: | :---: |
| **$1$** | $1$ | $2$ | **$2$** |
| **$2$** | - | $2$ | $2$ |
| **$3$** | - | - | $3$ |

</details>

<details class="step-card">
<summary class="step-badge">Final Step: Reconstruct Optimal Parenthesization</summary>

* Start at $s[1, 4] = 2 \implies (A_1 A_2) \times (A_3 A_4)$.
* Left prefix $(1, 2)$: $s[1, 2] = 1 \implies (A_1 \times A_2)$.
* Right postfix $(3, 4)$: $s[3, 4] = 3 \implies (A_3 \times A_4)$.
* **Optimal Parenthesization:** $\mathbf{((A_1 A_2)(A_3 A_4))}$.
* **Total Minimum Multiplications:** $\mathbf{405}$.
</details>

</div>
