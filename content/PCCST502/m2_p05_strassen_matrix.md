# Progressive Problems: Strassen's Matrix Multiplication

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Level 1: Standard $2 \times 2$ Matrix Multiplication Baseline

### Problem 1.1: The Row-by-Column Dot Product and the 8-Multiplication Barrier

Suppose we have two small $2 \times 2$ matrices, labeled $A$ and $B$:
$$A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix}, \quad B = \begin{pmatrix} b_{11} & b_{12} \\ b_{21} & b_{22} \end{pmatrix}$$
We want to compute their matrix product:
$$C = A \times B = \begin{pmatrix} c_{11} & c_{12} \\ c_{21} & c_{22} \end{pmatrix}$$

We will:
1. Trace the row-by-column formula for all four output entries: $c_{11}, c_{12}, c_{21}, c_{22}$.
2. Explicitly count every single scalar multiplication and scalar addition performed.
3. Formulate the divide-and-conquer recurrence relation $T(n) = 8T(n/2) + O(n^2)$ when this approach is applied to block matrices of size $n \times n$.
4. Solve the recurrence to show why the standard divide-and-conquer strategy remains trapped at cubic time, $O(n^3)$.

::: callout-intuition Core Mental Model
Think of matrix multiplication as a "Row meets Column" handshake:
- To find the entry in **Row $r$** and **Column $c$** of the answer matrix $C$, take **Row $r$** from matrix $A$ and lay it across **Column $c$** of matrix $B$.
- You pair up corresponding numbers, multiply each pair together, and then add those products up.
- Because a $2 \times 2$ matrix has $4$ total spots to fill, and each spot requires pairing up $2$ numbers, you end up doing $4 \times 2 = 8$ separate multiplications!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Compute Entry c11 (Top-Left)</div>

**What are we doing?** We calculate the value that goes into the first row and first column of the output matrix $C$.

**Why are we starting here?** The standard way to evaluate a matrix is row-by-row, starting from the top-left cell $(1, 1)$.

**How do we do it?** 1. Pick **Row 1** of Matrix $A$: $[a_{11}, a_{12}]$.
2. Pick **Column 1** of Matrix $B$: $\begin{pmatrix} b_{11} \\ b_{21} \end{pmatrix}$.
3. Pair the first elements and multiply: $a_{11} \times b_{11}$.
4. Pair the second elements and multiply: $a_{12} \times b_{21}$.
5. Add the two products together:
   $$c_{11} = (a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21})$$

**Where did this formula come from?** The universal mathematical definition of matrix multiplication:
$$c_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}$$
For $i=1, j=1$, and $n=2$, the sum expands to $a_{11}b_{11} + a_{12}b_{21}$.

**Operation Count for this entry:**
- Multiplications: $2$ (specifically: $a_{11} \cdot b_{11}$ and $a_{12} \cdot b_{21}$)
- Additions: $1$ (the $+$ between them)
</div>

<div class="step-card">
<div class="step-badge">Step 2: Compute Entry c12 (Top-Right)</div>

**What changed from Step 1?** We stay on Row 1 of matrix $A$, but shift our focus to **Column 2** of matrix $B$.

**What are we doing?** Calculate $c_{12}$.

**How do we do it?** 1. Pick **Row 1** of Matrix $A$: $[a_{11}, a_{12}]$.
2. Pick **Column 2** of Matrix $B$: $\begin{pmatrix} b_{12} \\ b_{22} \end{pmatrix}$.
3. Multiply corresponding pairs:
   - First pair: $a_{11} \times b_{12}$
   - Second pair: $a_{12} \times b_{22}$
4. Add them:
   $$c_{12} = (a_{11} \cdot b_{12}) + (a_{12} \cdot b_{22})$$

**Operation Count for this entry:**
- Multiplications: $2$
- Additions: $1$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Compute Entry c21 (Bottom-Left)</div>

**What changed from Step 2?** We move down to **Row 2** of matrix $A$, and look at **Column 1** of matrix $B$.

**What are we doing?** Calculate $c_{21}$.

**How do we do it?** 1. Pick **Row 2** of Matrix $A$: $[a_{21}, a_{22}]$.
2. Pick **Column 1** of Matrix $B$: $\begin{pmatrix} b_{11} \\ b_{21} \end{pmatrix}$.
3. Multiply corresponding pairs:
   - First pair: $a_{21} \times b_{11}$
   - Second pair: $a_{22} \times b_{21}$
4. Add them:
   $$c_{21} = (a_{21} \cdot b_{11}) + (a_{22} \cdot b_{21})$$

**Operation Count for this entry:**
- Multiplications: $2$
- Additions: $1$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Compute Entry c22 (Bottom-Right)</div>

**What changed from Step 3?** We stay on **Row 2** of matrix $A$, and move to **Column 2** of matrix $B$.

**What are we doing?** Calculate $c_{22}$, the final entry of matrix $C$.

**How do we do it?** 1. Pick **Row 2** of Matrix $A$: $[a_{21}, a_{22}]$.
2. Pick **Column 2** of Matrix $B$: $\begin{pmatrix} b_{12} \\ b_{22} \end{pmatrix}$.
3. Multiply corresponding pairs:
   - First pair: $a_{21} \times b_{12}$
   - Second pair: $a_{22} \times b_{22}$
4. Add them:
   $$c_{22} = (a_{21} \cdot b_{12}) + (a_{22} \cdot b_{22})$$

**Operation Count for this entry:**
- Multiplications: $2$
- Additions: $1$
</div>

<div class="step-card">
<div class="step-badge">Step 5: Tally All Operations & Set Up Recurrence</div>

**What are we doing?** We count all the arithmetic operations we just performed across all $4$ cells and analyze how this scales up to larger matrices.

**How do we do it?** Let's sum the operations from Steps 1 through 4:
- Total Multiplications:
  $$2 + 2 + 2 + 2 = \mathbf{8} \text{ scalar multiplications}$$
- Total Additions:
  $$1 + 1 + 1 + 1 = \mathbf{4} \text{ scalar additions}$$

**How does this apply to large $n \times n$ matrices?**
Suppose $A$ and $B$ are large $n \times n$ matrices. We can divide both matrices into $4$ sub-blocks of size $\frac{n}{2} \times \frac{n}{2}$:
$$A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}, \quad B = \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}$$
To compute the $4$ sub-blocks of $C$, the naive block algorithm performs:
- $8$ recursive matrix multiplications of sub-blocks of size $\frac{n}{2} \times \frac{n}{2}$
- $4$ matrix additions of size $\frac{n}{2} \times \frac{n}{2}$ (which takes $O(n^2)$ time)

This yields the classic recurrence relation:
$$T(n) = 8T\left(\frac{n}{2}\right) + O(n^2)$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Solving the Recurrence via Master Theorem</div>

**What is the runtime of the standard divide-and-conquer approach?**
We apply the Master Theorem to $T(n) = aT(n/b) + O(n^d)$:
- Number of subproblems: $a = 8$
- Subproblem size reduction factor: $b = 2$
- Work outside recursion (matrix additions): $f(n) = O(n^2) \implies d = 2$

Now we compare the critical exponent $\log_b(a)$ with $d$:
$$\log_b(a) = \log_2(8) = 3$$
Since $\log_2(8) = 3 > d = 2$, we fall into **Case 1 of the Master Theorem**:
$$T(n) = \Theta\left(n^{\log_b a}\right) = \Theta\left(n^{\log_2 8}\right) = \mathbf{\Theta(n^3)}$$

**Why does this matter?**
Even though we divided the problem using divide-and-conquer, the runtime did not improve at all! It is still $O(n^3)$, identical to three nested `for` loops.  
The **bottleneck** is the number of recursive multiplications ($a = 8$). If we could somehow compute the product using fewer than $8$ multiplications, the exponent $\log_2(a)$ would drop below $3$!
</div>

</div>

---

## Level 2: Strassen's 7-Multiplication Method

### Problem 2.1: Dropping from 8 to 7 Multiplications via Clever Cancellations

In 1969, Volker Strassen discovered that you don't need $8$ multiplications to multiply two $2 \times 2$ matrices. You only need **$7$**!  
He introduced $7$ intermediate helper products, labeled $M_1, M_2, M_3, M_4, M_5, M_6, M_7$ (often also written as $P_1$ through $P_7$).

We will:
1. List all $7$ of Strassen's multiplication formulas clearly.
2. Focus on the bottom-right output quadrant:
   $$c_{22} = M_1 - M_2 + M_3 + M_6$$
3. Expand every single term algebraically from scratch—step-by-step with zero skipped algebra—and watch unwanted cross-terms cancel out until only the exact standard formula $a_{21}b_{12} + a_{22}b_{22}$ remains.
4. Solve Strassen's new recurrence relation $T(n) = 7T(n/2) + O(n^2)$ to prove the time complexity drops to $O(n^{\log_2 7}) \approx O(n^{2.807})$.

::: callout-intuition Core Mental Model
Imagine you want to buy a combo meal that costs exactly:
$$\text{Burger} + \text{Fries}$$
- In the standard method, you buy the Burger directly, then buy the Fries directly (two separate purchases).
- Strassen's idea is like using coupons and bundled deals:
  - You buy Bundle A: (Burger + Drink)
  - You buy Bundle B: (Fries - Drink)
  - When you add Bundle A and Bundle B together, the $+ \text{Drink}$ and $- \text{Drink}$ cancel each other out! You are left with exactly $\text{Burger} + \text{Fries}$.
- You had to do a couple of additions and subtractions to set up the bundles, but in computer science, **adding matrices is cheap ($O(n^2)$), while multiplying matrices is expensive ($O(n^3)$)**. Trading $1$ expensive multiplication for a few extra additions is a huge win!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: The 7 Magic Products (M1 through M7)</div>

**What are we doing?** We state the $7$ specific multiplication formulas designed by Strassen.

**Why are we doing this?** These $7$ products replace the $8$ standard multiplications. Each $M_k$ is formed by multiplying a linear combination of elements from $A$ with a linear combination of elements from $B$.

**The 7 Formulas:**
1. $$M_1 = (a_{11} + a_{22})(b_{11} + b_{22})$$
2. $$M_2 = (a_{21} + a_{22})b_{11}$$
3. $$M_3 = a_{11}(b_{12} - b_{22})$$
4. $$M_4 = a_{22}(b_{21} - b_{11})$$
5. $$M_5 = (a_{11} + a_{12})b_{22}$$
6. $$M_6 = (a_{21} - a_{11})(b_{11} + b_{12})$$
7. $$M_7 = (a_{12} - a_{22})(b_{21} + b_{22})$$

**Notice:** Every single equation has exactly **one** multiplication symbol between two terms. That means computing $M_1$ through $M_7$ requires only **$7$ multiplications** in total!

Once these $7$ values are computed, the final output entries are assembled purely using addition and subtraction:
- $c_{11} = M_1 + M_4 - M_5 + M_7$
- $c_{12} = M_3 + M_5$
- $c_{21} = M_2 + M_4$
- $c_{22} = M_1 - M_2 + M_3 + M_6$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Choose c22 and Expand M1, M2, M3, M6 Individually</div>

**What changed from Step 1?** We will now prove that Strassen's formula for $c_{22}$ actually works. We select the target equation:
$$c_{22} = M_1 - M_2 + M_3 + M_6$$
From Level 1, our goal is to prove this simplifies to the true mathematical definition of $c_{22}$:
$$c_{22}^{\text{target}} = a_{21}b_{12} + a_{22}b_{22}$$

**What are we doing?** Expand the $4$ relevant products ($M_1, M_2, M_3, M_6$) using basic FOIL / distributive multiplication: $(x+y)(w+z) = xw + xz + yw + yz$.

**How do we do it?** 1. **Expand $M_1$:**
   $$M_1 = (a_{11} + a_{22})(b_{11} + b_{22})$$
   $$M_1 = a_{11}b_{11} + a_{11}b_{22} + a_{22}b_{11} + a_{22}b_{22}$$

2. **Expand $M_2$:**
   $$M_2 = (a_{21} + a_{22})b_{11}$$
   $$M_2 = a_{21}b_{11} + a_{22}b_{11}$$

3. **Expand $M_3$:**
   $$M_3 = a_{11}(b_{12} - b_{22})$$
   $$M_3 = a_{11}b_{12} - a_{11}b_{22}$$

4. **Expand $M_6$:**
   $$M_6 = (a_{21} - a_{11})(b_{11} + b_{12})$$
   $$M_6 = a_{21}b_{11} + a_{21}b_{12} - a_{11}b_{11} - a_{11}b_{12}$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Substitute the Expansions into (M1 - M2 + M3 + M6)</div>

**What changed from Step 2?** We now assemble all $4$ expanded pieces into one single, comprehensive algebraic expression.

**What are we doing?** Write down:
$$c_{22} = \underbrace{(M_1)}_{\text{Part 1}} - \underbrace{(M_2)}_{\text{Part 2}} + \underbrace{(M_3)}_{\text{Part 3}} + \underbrace{(M_6)}_{\text{Part 4}}$$

**How do we do it?** Substitute each bracketed expansion carefully, distributing the negative sign to all terms inside $M_2$:

$$\begin{aligned}
c_{22} = &\phantom{-} [a_{11}b_{11} + a_{11}b_{22} + a_{22}b_{11} + a_{22}b_{22}] && \text{(this is } M_1\text{)} \\
&- [a_{21}b_{11} + a_{22}b_{11}] && \text{(this is } -M_2\text{)} \\
&+ [a_{11}b_{12} - a_{11}b_{22}] && \text{(this is } +M_3\text{)} \\
&+ [a_{21}b_{11} + a_{21}b_{12} - a_{11}b_{11} - a_{11}b_{12}] && \text{(this is } +M_6\text{)}
\end{aligned}$$

Distribute the minus sign across $M_2$:
$$\begin{aligned}
c_{22} = &\phantom{+} a_{11}b_{11} + a_{11}b_{22} + a_{22}b_{11} + a_{22}b_{22} \\
&- a_{21}b_{11} - a_{22}b_{11} \\
&+ a_{11}b_{12} - a_{11}b_{22} \\
&+ a_{21}b_{11} + a_{21}b_{12} - a_{11}b_{11} - a_{11}b_{12}
\end{aligned}$$
There are $12$ individual terms in this expression.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Cancel Every Unwanted Term Step-by-Step</div>

**What changed from Step 3?** We have $12$ terms laid out in front of us. We will now hunt down and pair up opposite terms $(+X \text{ and } -X)$ so they cancel to zero.

**What are we doing?** Inspecting terms one pair at a time:

1. Look at $a_{11}b_{11}$:
   - We have $+a_{11}b_{11}$ (from line 1)
   - We have $-a_{11}b_{11}$ (from line 4)
   - $a_{11}b_{11} - a_{11}b_{11} = \mathbf{0}$ $\implies$ **Cancelled!**

2. Look at $a_{11}b_{22}$:
   - We have $+a_{11}b_{22}$ (from line 1)
   - We have $-a_{11}b_{22}$ (from line 3)
   - $a_{11}b_{22} - a_{11}b_{22} = \mathbf{0}$ $\implies$ **Cancelled!**

3. Look at $a_{22}b_{11}$:
   - We have $+a_{22}b_{11}$ (from line 1)
   - We have $-a_{22}b_{11}$ (from line 2)
   - $a_{22}b_{11} - a_{22}b_{11} = \mathbf{0}$ $\implies$ **Cancelled!**

4. Look at $a_{21}b_{11}$:
   - We have $-a_{21}b_{11}$ (from line 2)
   - We have $+a_{21}b_{11}$ (from line 4)
   - $-a_{21}b_{11} + a_{21}b_{11} = \mathbf{0}$ $\implies$ **Cancelled!**

5. Look at $a_{11}b_{12}$:
   - We have $+a_{11}b_{12}$ (from line 3)
   - We have $-a_{11}b_{12}$ (from line 4)
   - $a_{11}b_{12} - a_{11}b_{12} = \mathbf{0}$ $\implies$ **Cancelled!**

**What terms are still standing?**
Let us gather the survivors that had no negative partners to cancel them:
- From line 1: $+a_{22}b_{22}$
- From line 4: $+a_{21}b_{12}$

Putting them together:
$$c_{22} = a_{21}b_{12} + a_{22}b_{22}$$
This matches the exact standard formula for $c_{22}$ from Level 1! The identity is algebraically verified.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Formulate Strassen's Recurrence Relation</div>

**What are we doing?** We write down the recursive equation for Strassen's algorithm when dividing an $n \times n$ matrix into $\frac{n}{2} \times \frac{n}{2}$ sub-matrices.

**How do we do it?** 1. **Recursive Multiplications:**
   Instead of $8$ recursive calls, we compute $M_1, M_2, \dots, M_7$.
   That is exactly **$7$ recursive calls** on sub-matrices of size $\frac{n}{2} \times \frac{n}{2}$:
   $$\text{Multiplication cost} = 7T\left(\frac{n}{2}\right)$$

2. **Matrix Additions and Subtractions:**
   To prepare the inputs for $M_1 \dots M_7$, and to assemble the final quadrants $c_{11}, c_{12}, c_{21}, c_{22}$, we perform $18$ matrix additions/subtractions on blocks of size $\frac{n}{2} \times \frac{n}{2}$.
   Adding two $\frac{n}{2} \times \frac{n}{2}$ matrices requires adding $\left(\frac{n}{2}\right)^2 = \frac{n^2}{4}$ numbers, which is proportional to $n^2$:
   $$\text{Addition/Subtraction cost} = 18 \times \left(\frac{n}{2}\right)^2 = \frac{18}{4}n^2 = O(n^2)$$

Combining both parts gives the complete recurrence relation:
$$T(n) = 7T\left(\frac{n}{2}\right) + O(n^2)$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Solve Strassen's Recurrence via Master Theorem</div>

**What is the final time complexity of Strassen's Algorithm?**
We apply the Master Theorem to:
$$T(n) = aT\left(\frac{n}{b}\right) + O(n^d)$$
where:
- $a = 7$ (number of subproblems)
- $b = 2$ (subproblem size reduction factor)
- $d = 2$ (work to add matrices, $O(n^2)$)

**Calculate the critical exponent:**
$$\log_b(a) = \log_2(7)$$
Let us evaluate $\log_2(7)$ using basic arithmetic:
- We know $2^2 = 4 \implies \log_2(4) = 2$
- We know $2^3 = 8 \implies \log_2(8) = 3$
- Since $7$ is between $4$ and $8$, $\log_2(7)$ is strictly between $2$ and $3$:
  $$\log_2(7) \approx 2.80735...$$

**Compare $\log_b(a)$ with $d$:**
$$\log_2(7) \approx 2.807 > d = 2$$
Because $\log_b(a) > d$, **Case 1 of the Master Theorem** applies:
$$T(n) = \Theta\left(n^{\log_b a}\right) = \Theta\left(n^{\log_2 7}\right) \approx \mathbf{O(n^{2.807})}$$

**Why is this a monumental breakthrough?**
- Standard matrix multiplication: $O(n^3) = O(n^{3.000})$
- Strassen's algorithm: $O(n^{\log_2 7}) \approx O(n^{2.807})$

For a matrix of dimension $n = 1024 = 2^{10}$:
- $n^3 = (2^{10})^3 = 2^{30} \approx 1,073,741,824$ operations
- $n^{2.807} \approx (2^{10})^{2.807} = 2^{28.07} \approx 280,000,000$ operations

Strassen's algorithm does nearly **$4$ times fewer operations** on a $1024 \times 1024$ matrix than the traditional method, mathematically breaking the cubic barrier for the first time in history!
</div>

</div>
