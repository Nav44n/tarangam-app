# Progressive Problems: Fractional Knapsack & Greedy Strategy

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic algebra.

---

## Level 1: Standard Fractional Knapsack (Distinct Value-to-Weight Ratios)

### Problem 1.1: Optimal Resource Allocation with Clear Value Density

A hiker has a knapsack with maximum carrying capacity $W = 50\text{ kg}$. Three items are available with the following weights and values:
* Item 1: Weight $w_1 = 10\text{ kg}$, Value $v_1 = \$60$
* Item 2: Weight $w_2 = 20\text{ kg}$, Value $v_2 = \$100$
* Item 3: Weight $w_3 = 30\text{ kg}$, Value $v_3 = \$120$

Compute the fraction $x_i \in [0, 1]$ of each item to take to maximize total monetary profit without exceeding the $50\text{ kg}$ weight limit.

::: callout-intuition Core Mental Model
Imagine you are at a bulk spice bazaar with a bag that holds at most $50\text{ kg}$.
* Saffron costs $\$6$ per kg.
* Cinnamon costs $\$5$ per kg.
* Pepper costs $\$4$ per kg.
To walk away with the most valuable bag, you must prioritize the most expensive spice per kilogram first. Once you pack all available Saffron, you pack Cinnamon. When the bag runs low on space, you scoop whatever partial kilogram amount of Pepper fits before the bag is full.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Calculate Value-to-Weight Densities</div>

**What are we doing?** We calculate the value density $r_i = \frac{v_i}{w_i}$ for each item.

**Why are we starting here?** The greedy choice property states that prioritizing items with higher value per unit of weight yields the optimal solution for the fractional knapsack problem.

**How do we do it?** Divide value by weight for each item:
* Item 1: $r_1 = \frac{60}{10} = 6.0\text{ \$/kg}$
* Item 2: $r_2 = \frac{100}{20} = 5.0\text{ \$/kg}$
* Item 3: $r_3 = \frac{120}{30} = 4.0\text{ \$/kg}$

**Where did this formula come from?** The continuous optimization formulation:
$$\max \sum_{i=1}^n \left(\frac{v_i}{w_i}\right) (w_i x_i) \quad \text{subject to} \quad \sum_{i=1}^n (w_i x_i) \le W$$

**Summary Table:**

| Item ($i$) | Weight ($w_i$) | Value ($v_i$) | Density ($r_i = v_i / w_i$) |
| :---: | :---: | :---: | :---: |
| 1 | $10\text{ kg}$ | $\$60$ | **$6.0$** |
| 2 | $20\text{ kg}$ | $\$100$ | **$5.0$** |
| 3 | $30\text{ kg}$ | $\$120$ | **$4.0$** |

</div>

<div class="step-card">
<div class="step-badge">Step 2: Sort Items in Non-Increasing Order of Density</div>

**What changed from Step 1?** We establish the processing order based on density values:
$$r_1 (6.0) > r_2 (5.0) > r_3 (4.0)$$
The sorted sequence is $\langle \text{Item 1}, \text{Item 2}, \text{Item 3} \rangle$.
Initial available capacity: $W_{\text{rem}} = 50\text{ kg}$. Total profit: $P = \$0$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Evaluate Item 1 (Highest Density)</div>

**What are we doing?** Check if Item 1 fits completely into the remaining capacity.

**How do we do it?**
* Weight needed: $w_1 = 10\text{ kg}$.
* Capacity available: $W_{\text{rem}} = 50\text{ kg}$.
* Since $w_1 \le W_{\text{rem}}$ ($10 \le 50$), take the entire item:
  $$x_1 = 1.0$$
* Deduct weight: $W_{\text{rem}} \leftarrow 50 - 10 = 40\text{ kg}$.
* Add profit: $P \leftarrow 0 + (1.0 \times 60) = \$60$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Evaluate Item 2</div>

**What are we doing?** Check if Item 2 fits into the remaining $40\text{ kg}$.

**How do we do it?**
* Weight needed: $w_2 = 20\text{ kg}$.
* Capacity available: $W_{\text{rem}} = 40\text{ kg}$.
* Since $w_2 \le W_{\text{rem}}$ ($20 \le 40$), take the entire item:
  $$x_2 = 1.0$$
* Deduct weight: $W_{\text{rem}} \leftarrow 40 - 20 = 20\text{ kg}$.
* Add profit: $P \leftarrow 60 + (1.0 \times 100) = \$160$.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Evaluate Item 3 (Fractional Inclusion)</div>

**What are we doing?** Check if Item 3 fits into the remaining $20\text{ kg}$.

**How do we do it?**
* Weight needed: $w_3 = 30\text{ kg}$.
* Capacity available: $W_{\text{rem}} = 20\text{ kg}$.
* Since $w_3 > W_{\text{rem}}$ ($30 > 20$), the knapsack cannot accommodate the whole item.
* Take a fractional amount equal to the remaining capacity:
  $$x_3 = \frac{W_{\text{rem}}}{w_3} = \frac{20}{30} = \frac{2}{3} \approx 0.667$$
* Deduct weight: $W_{\text{rem}} \leftarrow 20 - \left(\frac{2}{3} \times 30\right) = 20 - 20 = 0\text{ kg}$.
* Add profit: $P \leftarrow 160 + \left(\frac{2}{3} \times 120\right) = 160 + 80 = \$240$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Conclusion & Results</div>

**What is the final answer?**
* Fraction vector: $\mathbf{X = \langle x_1 = 1.0, \; x_2 = 1.0, \; x_3 = 0.667 \rangle}$
* Weight consumed: $10(1) + 20(1) + 30(2/3) = 10 + 20 + 20 = 50\text{ kg}$.
* **Maximum Profit:** $\mathbf{\$240}$.

**Why does this answer make sense?**
Any alternative selection that takes less of Item 1 or Item 2 to make room for more of Item 3 would replace higher-density value ($\$6/\text{kg}$ or $\$5/\text{kg}$) with lower-density value ($\$4/\text{kg}$), reducing total profit.
</div>

</div>

---

## Level 2: Ties in Value Density & Multiple Fractions

### Problem 2.1: Handling Identical Ratios

A knapsack has capacity $W = 16\text{ kg}$. Four items are presented:
* Item 1: $w_1 = 6\text{ kg}, v_1 = \$36$
* Item 2: $w_2 = 10\text{ kg}, v_2 = \$60$
* Item 3: $w_3 = 4\text{ kg}, v_3 = \$16$
* Item 4: $w_4 = 5\text{ kg}, v_4 = \$15$

Compute the optimal selection vector $X$.

::: callout-intuition Core Mental Model
When two items have the exact same price-per-kilogram ratio, you can take either one first without affecting the final profit. The rate of return per unit weight is identical.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Compute Densities and Identify Ties</div>

* $r_1 = \frac{36}{6} = 6.0\text{ \$/kg}$
* $r_2 = \frac{60}{10} = 6.0\text{ \$/kg}$
* $r_3 = \frac{16}{4} = 4.0\text{ \$/kg}$
* $r_4 = \frac{15}{5} = 3.0\text{ \$/kg}$

Notice that $r_1 = r_2 = 6.0\text{ \$/kg}$. A tie occurs between Item 1 and Item 2.
Sorted order (tie broken arbitrarily): $\langle \text{Item 1}, \text{Item 2}, \text{Item 3}, \text{Item 4} \rangle$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Pack Items Greedily</div>

* **Item 1:** $w_1 = 6 \le 16 \implies x_1 = 1.0$.
  $W_{\text{rem}} = 16 - 6 = 10\text{ kg}$. Profit $= \$36$.
* **Item 2:** $w_2 = 10 \le 10 \implies x_2 = 1.0$.
  $W_{\text{rem}} = 10 - 10 = 0\text{ kg}$. Profit $= 36 + 60 = \$96$.
* Capacity is completely exhausted ($W_{\text{rem}} = 0$).
* **Item 3 & Item 4:** Cannot be taken ($x_3 = 0, x_4 = 0$).
</div>

<div class="step-card">
<div class="step-badge">Final Step: Solution Summary</div>

* **Selection Vector:** $\mathbf{X = \langle 1.0, \; 1.0, \; 0, \; 0 \rangle}$
* **Total Weight:** $6 + 10 = 16\text{ kg}$.
* **Total Maximum Profit:** $\mathbf{\$96}$.
</div>

</div>
