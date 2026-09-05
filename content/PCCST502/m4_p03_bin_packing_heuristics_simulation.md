# Progressive Problems: Bin Packing Heuristics Simulation (NF, FF, BF, FFD, BFD)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic decimals and addition.

---

## Level 1: Online Packing Traces (Next Fit vs. First Fit vs. Best Fit)

### Problem 1.1: Tracing 10 Normalized Items on Unit Bins

Given a set of 10 items to be packed into bins of capacity $C = 1.0$:
$$S = \langle 0.4, \; 0.8, \; 0.2, \; 0.2, \; 0.7, \; 0.1, \; 0.5, \; 0.6, \; 0.1, \; 0.4 \rangle$$

1. Calculate the theoretical lower bound on the optimal number of bins ($\text{OPT}$).
2. Trace the step-by-step execution of **Next Fit (NF)**.
3. Trace the step-by-step execution of **First Fit (FF)**.
4. Trace the step-by-step execution of **Best Fit (BF)**.

::: callout-intuition Core Mental Model
Imagine you are packing grocery bags where each bag can carry up to 1.0 kg:
* **Next Fit:** You only keep one bag open on the counter. The moment an item doesn't fit into the current bag, you tie it up, push it into the cart, and never look at it again.
* **First Fit:** You keep all previous bags lined up on the counter. When an item arrives, you walk down the line from left to right and drop it into the first bag that has enough space.
* **Best Fit:** You scan all open bags and drop the item into whichever bag leaves the smallest remaining sliver of empty space.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Total Weight and Trivial Lower Bound</div>

Sum of all 10 item weights:
$$\sum_{i=1}^{10} s_i = 0.4 + 0.8 + 0.2 + 0.2 + 0.7 + 0.1 + 0.5 + 0.6 + 0.1 + 0.4 = \mathbf{4.0}$$

Since bin capacity $C = 1.0$:
$$\mathbf{\text{OPT} \ge \left\lceil \frac{\sum s_i}{C} \right\rceil = \left\lceil \frac{4.0}{1.0} \right\rceil = 4 \text{ bins}}$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Next Fit (NF) Execution Trace</div>

* Maintain only 1 active bin. If item exceeds remaining space, close current bin and open a new one.
1. Item 1 (0.4): Open Bin 1. [B1: 0.4, space: 0.6]
2. Item 2 (0.8): $0.4 + 0.8 = 1.2 > 1.0$. Close Bin 1. Open Bin 2. [B2: 0.8, space: 0.2]
3. Item 3 (0.2): Fits in B2 ($0.8 + 0.2 = 1.0$). [B2: 1.0, space: 0.0]
4. Item 4 (0.2): $1.0 + 0.2 > 1.0$. Close Bin 2. Open Bin 3. [B3: 0.2, space: 0.8]
5. Item 5 (0.7): Fits in B3 ($0.2 + 0.7 = 0.9$). [B3: 0.9, space: 0.1]
6. Item 6 (0.1): Fits in B3 ($0.9 + 0.1 = 1.0$). [B3: 1.0, space: 0.0]
7. Item 7 (0.5): $1.0 + 0.5 > 1.0$. Close Bin 3. Open Bin 4. [B4: 0.5, space: 0.5]
8. Item 8 (0.6): $0.5 + 0.6 = 1.1 > 1.0$. Close Bin 4. Open Bin 5. [B5: 0.6, space: 0.4]
9. Item 9 (0.1): Fits in B5 ($0.6 + 0.1 = 0.7$). [B5: 0.7, space: 0.3]
10. Item 10 (0.4): $0.7 + 0.4 = 1.1 > 1.0$. Close Bin 5. Open Bin 6. [B6: 0.4, space: 0.6]

**Next Fit Total Bins Used:** **6 Bins.**
* $B_1: \{0.4\}$
* $B_2: \{0.8, 0.2\}$
* $B_3: \{0.2, 0.7, 0.1\}$
* $B_4: \{0.5\}$
* $B_5: \{0.6, 0.1\}$
* $B_6: \{0.4\}$
</div>

<div class="step-card">
<div class="step-badge">Step 3: First Fit (FF) Execution Trace</div>

* Scan previously opened bins in order $1, 2, \dots$ and place item in first bin with sufficient room.
1. Item 1 (0.4): Put in B1. [B1 fill: 0.4, space: 0.6]
2. Item 2 (0.8): B1 has room 0.6. Open B2. [B1: 0.4 (0.6), B2: 0.8 (0.2)]
3. Item 3 (0.2): Scan B1: room $0.6 \ge 0.2$. Put in **B1**! [B1: 0.6 (0.4), B2: 0.8 (0.2)]
4. Item 4 (0.2): Scan B1: room $0.4 \ge 0.2$. Put in **B1**! [B1: 0.8 (0.2), B2: 0.8 (0.2)]
5. Item 5 (0.7): Scan B1 (0.2), B2 (0.2). Open B3. [B1: 0.8, B2: 0.8, B3: 0.7 (0.3)]
6. Item 6 (0.1): Scan B1: room $0.2 \ge 0.1$. Put in **B1**! [B1: 0.9 (0.1), B2: 0.8, B3: 0.7]
7. Item 7 (0.5): Scan B1 (0.1), B2 (0.2), B3 (0.3). Open B4. [B1: 0.9, B2: 0.8, B3: 0.7, B4: 0.5 (0.5)]
8. Item 8 (0.6): Scan B1 (0.1), B2 (0.2), B3 (0.3), B4 (0.5). Open B5. [B1: 0.9, B2: 0.8, B3: 0.7, B4: 0.5, B5: 0.6 (0.4)]
9. Item 9 (0.1): Scan B1: room $0.1 \ge 0.1$. Put in **B1**! [B1: 1.0 (0.0), B2: 0.8, B3: 0.7, B4: 0.5, B5: 0.6]
10. Item 10 (0.4): Scan B1 (0.0), B2 (0.2), B3 (0.3). Scan B4: room $0.5 \ge 0.4$. Put in **B4**! [B4: 0.9 (0.1)]

**First Fit Total Bins Used:** **5 Bins.**
* $B_1: \{0.4, 0.2, 0.2, 0.1, 0.1\}$ (Total: 1.0)
* $B_2: \{0.8\}$ (Total: 0.8)
* $B_3: \{0.7\}$ (Total: 0.7)
* $B_4: \{0.5, 0.4\}$ (Total: 0.9)
* $B_5: \{0.6\}$ (Total: 0.6)
</div>

<div class="step-card">
<div class="step-badge">Step 4: Best Fit (BF) Execution Trace</div>

* Place each item in the open bin that minimizes remaining space ($C - \text{fill} - s_i \ge 0$).
1. Item 1 (0.4): Put in B1. [B1 space: 0.6]
2. Item 2 (0.8): Open B2. [B1 space: 0.6, B2 space: 0.2]
3. Item 3 (0.2): Can fit in B1 (space 0.6, leaves 0.4) or B2 (space 0.2, leaves 0.0).
   * **Tightest fit is B2!** Put in **B2**. [B1 space: 0.6, B2: 1.0, space: 0.0]
4. Item 4 (0.2): Fits in B1 (space 0.6, leaves 0.4). Put in **B1**. [B1: 0.6, space: 0.4]
5. Item 5 (0.7): Open B3. [B1 space: 0.4, B2 space: 0.0, B3: 0.7, space: 0.3]
6. Item 6 (0.1): Fits in B1 (space 0.4, leaves 0.3) or B3 (space 0.3, leaves 0.2).
   * **Tightest fit is B3!** Put in **B3**. [B3: 0.8, space: 0.2]
7. Item 7 (0.5): No open bin has space $\ge 0.5$. Open B4. [B4: 0.5, space: 0.5]
8. Item 8 (0.6): Open B5. [B5: 0.6, space: 0.4]
9. Item 9 (0.1): Fits in B1 (leaves 0.3), B3 (leaves 0.1), B4 (leaves 0.4), B5 (leaves 0.3).
   * **Tightest fit is B3!** Put in **B3**. [B3: 0.9, space: 0.1]
10. Item 10 (0.4): Fits in B1 (leaves 0.0) or B4 (leaves 0.1) or B5 (leaves 0.0).
   * **Tightest fit is B1 (or B5)!** Put in **B1**. [B1: 1.0, space: 0.0]

**Best Fit Total Bins Used:** **5 Bins.**
* $B_1: \{0.4, 0.2, 0.4\}$ (Total: 1.0)
* $B_2: \{0.8, 0.2\}$ (Total: 1.0)
* $B_3: \{0.7, 0.1, 0.1\}$ (Total: 0.9)
* $B_4: \{0.5\}$ (Total: 0.5)
* $B_5: \{0.6\}$ (Total: 0.6)
</div>

</div>

---

## Level 2: Offline Packing Traces (First Fit Decreasing)

### Problem 2.1: First Fit Decreasing Trace on Problem 1.1's Items

Using the same item sequence:
$$S = \langle 0.4, 0.8, 0.2, 0.2, 0.7, 0.1, 0.5, 0.6, 0.1, 0.4 \rangle$$
Execute **First Fit Decreasing (FFD)** and show whether it achieves the optimal packing of 4 bins.

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Sort Items in Non-Increasing Order</div>

Sorting the 10 elements in descending order:
$$\mathbf{S_{\text{sorted}} = \langle 0.8, \; 0.7, \; 0.6, \; 0.5, \; 0.4, \; 0.4, \; 0.2, \; 0.2, \; 0.1, \; 0.1 \rangle}$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Trace First Fit on Sorted Elements</div>

1. Item 1 (0.8): Put in B1. [B1: 0.8, space: 0.2]
2. Item 2 (0.7): Doesn't fit in B1. Open B2. [B2: 0.7, space: 0.3]
3. Item 3 (0.6): Doesn't fit in B1 or B2. Open B3. [B3: 0.6, space: 0.4]
4. Item 4 (0.5): Doesn't fit in B1, B2, B3. Open B4. [B4: 0.5, space: 0.5]
5. Item 5 (0.4): 
   * Scan B1 (0.2), B2 (0.3).
   * Fits in **B3**! ($0.6 + 0.4 = 1.0$). [B3: 1.0, space: 0.0]
6. Item 6 (0.4):
   * Scan B1 (0.2), B2 (0.3), B3 (0.0).
   * Fits in **B4**! ($0.5 + 0.4 = 0.9$). [B4: 0.9, space: 0.1]
7. Item 7 (0.2):
   * Fits in **B1**! ($0.8 + 0.2 = 1.0$). [B1: 1.0, space: 0.0]
8. Item 8 (0.2):
   * Scan B1 (0.0).
   * Fits in **B2**! ($0.7 + 0.2 = 0.9$). [B2: 0.9, space: 0.1]
9. Item 9 (0.1):
   * Scan B1 (0.0).
   * Fits in **B2**! ($0.9 + 0.1 = 1.0$). [B2: 1.0, space: 0.0]
10. Item 10 (0.1):
   * Scan B1 (0.0), B2 (0.0), B3 (0.0).
   * Fits in **B4**! ($0.9 + 0.1 = 1.0$). [B4: 1.0, space: 0.0]
</div>

<div class="step-card">
<div class="step-badge">Final Step: FFD Results and Comparison</div>

**FFD Total Bins Used:** **4 Bins (OPTIMAL!).**
* $B_1: \{0.8, 0.2\}$ (Sum = 1.0)
* $B_2: \{0.7, 0.2, 0.1\}$ (Sum = 1.0)
* $B_3: \{0.6, 0.4\}$ (Sum = 1.0)
* $B_4: \{0.5, 0.4, 0.1\}$ (Sum = 1.0)

Every bin achieved **100% capacity utilization ($1.0 / 1.0$)**.
FFD matched the theoretical lower bound $\text{OPT} = 4$.
</div>

</div>
