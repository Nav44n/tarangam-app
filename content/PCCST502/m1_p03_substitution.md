# Progressive Problems: The Substitution Method for Recurrences

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior experience with formal mathematical induction beyond basic algebra.

---

## What is the Substitution Method? (The 3-Step Recipe)

The Substitution Method solves recurrences in three clear phases:
1. **Guess** the form of the solution (using recursion trees, pattern spotting, or inspection).
2. **Verify by Mathematical Induction** (assume the guess is true for all smaller inputs, substitute that assumption into the recurrence, and prove it holds for $n$).
3. **Solve for the Constants** ($c > 0$ and $n_0 \ge 1$) to prove the bound works mathematically.

---

## Level 1: Linear Recurrences (Subtract-by-Constant)

In this level, we apply the substitution method to subtract-and-conquer recurrences of the form $T(n) = T(n - 1) + (\text{work})$. We start with simple linear and quadratic guesses.

---

### Problem 1.1: Linear Recurrence with Constant Work: $T(n) = T(n - 1) + 1$

**Problem Statement:** Given the recurrence relation:

$$T(n) = \begin{cases} 1 & \text{if } n = 1 \\ T(n - 1) + 1 & \text{if } n > 1 \end{cases}$$

Use the Substitution Method to prove that $T(n) = O(n)$.

::: callout-intuition Core Mental Model
Imagine adding one coin to a piggy bank every day. On Day 1, you have 1 coin. On Day 2, you have $1 + 1 = 2$ coins. On Day $n$, you have $n$ coins. The total work grows directly in proportion to $n$. We guess an upper bound of the form $c \cdot n$ and use induction like falling dominoes: if our ceiling holds for day $n-1$, does adding $1$ coin keep it under the ceiling for day $n$?
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: State the Guess and the Inductive Hypothesis</summary>
**What are we doing?** We declare our educated guess for Big-$O$ and frame the inductive hypothesis.  
**Why are we starting here?** Induction cannot begin without an explicit hypothesis to test.  
**How do we do it?** * We guess that $T(n) = O(n)$.
* By definition of Big-$O$, this requires showing that $T(n) \le c \cdot n$ for some fixed constant $c > 0$ and for all $n \ge n_0$.
* **Inductive Hypothesis:** We assume that our guess holds true for all smaller problem sizes. Specifically, for the subproblem of size $n - 1$:

$$T(n - 1) \le c(n - 1)$$

**Where did this formula come from?** We took our target claim $T(k) \le c \cdot k$ and replaced the input variable $k$ with the smaller argument $(n - 1)$.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: The Inductive Step (Substitute into the Recurrence)</summary>
**What changed from Step 1?** We now analyze $T(n)$ by plugging the inductive hypothesis directly into the recurrence equation.  
**Why are we doing this?** The recurrence tells us how $T(n)$ is built from $T(n - 1)$. If we replace $T(n - 1)$ with its assumed upper bound, we can see what happens to $T(n)$.  
**How do we do it?**
Write the original recurrence:

$$T(n) = T(n - 1) + 1$$

Substitute $T(n - 1) \le c(n - 1)$:

$$T(n) \le c(n - 1) + 1$$

Expand the parentheses using the distributive property:

$$T(n) \le c \cdot n - c + 1$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Enforce the Target Inequality and Solve for $c$</summary>
**What changed from Step 2?** We have $c \cdot n - c + 1$, but our ultimate goal is to prove $T(n) \le c \cdot n$.  
**How do we manipulate the equation?** We demand that our current expression is less than or equal to our goal:

$$c \cdot n - c + 1 \le c \cdot n$$

Subtract $c \cdot n$ from both sides:

$$-c + 1 \le 0$$

Add $c$ to both sides:

$$1 \le c \iff c \ge 1$$

This tells us: as long as we choose any constant $c \ge 1$, the inductive step is mathematically guaranteed to work!
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Establish the Base Case</summary>
**What changed from Step 3?** We must check the smallest value of $n$ to ensure the chain of induction has a solid starting ground.  
**Why are we doing this?** A ladder is useless if the bottom rung is broken. The base case proves the first domino falls.  
**How do we do it?** * From the recurrence definition, the base value is given as: $T(1) = 1$.
* Our target formula says: $T(1) \le c \cdot 1 = c$.
* Does $1 \le c$ hold? Yes, because from Step 3 we already decided that $c \ge 1$.
* If we choose $c = 1$, then $T(1) = 1 \le 1 \cdot (1) = 1$, which is completely valid.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State the Complete Formal Conclusion</summary>
**What is the final answer?** $T(n) \le 1 \cdot n$ for all $n \ge 1$. Thus, $T(n) = O(n)$.  
**Why does this answer make sense?** * Base case holds: $T(1) \le 1(1)$.
* Inductive step holds for all $n > 1$ with $c = 1$.
* By the principle of mathematical induction, $T(n) \le n$ for every positive integer $n$.
</details>

</div>

---

### Problem 1.2: Linear Recurrence with Linear Work: $T(n) = T(n - 1) + n$

**Problem Statement:** Given the recurrence relation:

$$T(n) = \begin{cases} 1 & \text{if } n = 1 \\ T(n - 1) + n & \text{if } n > 1 \end{cases}$$

Use the Substitution Method to prove that $T(n) = O(n^2)$.

::: callout-intuition Core Mental Model
In this recurrence, each step costs as much as the current size $n$. At step 1 you do 1 work, at step 2 you do 2 work, at step $n$ you do $n$ work. Total work is $1 + 2 + \dots + n = \frac{n(n+1)}{2} \approx \frac{1}{2}n^2$. Since the leading term has power 2, guessing a quadratic bound $c \cdot n^2$ matches the physics of the growth.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Formulate the Guess and Inductive Hypothesis</summary>
**What are we doing?** We set up the inductive claim for $T(n) = O(n^2)$.  
**How do we do it?** * We guess that $T(n) \le c \cdot n^2$ for some positive constant $c$.
* **Inductive Hypothesis:** Assume the bound holds for the smaller problem size $n - 1$:

$$T(n - 1) \le c(n - 1)^2$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Substitute Hypothesis into the Recurrence</summary>
**What changed from Step 1?** We replace $T(n - 1)$ inside the recurrence $T(n) = T(n - 1) + n$.  
**How do we do it?** $$T(n) \le c(n - 1)^2 + n$$

Expand $(n - 1)^2 = n^2 - 2n + 1$ using the binomial formula:

$$T(n) \le c(n^2 - 2n + 1) + n$$

Distribute $c$:

$$T(n) \le c \cdot n^2 - 2c \cdot n + c + n$$

Group terms containing $n$:

$$T(n) \le c \cdot n^2 - (2c - 1)n + c$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Enforce the Target Inequality $T(n) \le c \cdot n^2$</summary>
**What changed from Step 2?** We want the entire right-hand side to be $\le c \cdot n^2$.  
**How do we manipulate the equation?** Set up the requirement:

$$c \cdot n^2 - (2c - 1)n + c \le c \cdot n^2$$

Subtract $c \cdot n^2$ from both sides:

$$-(2c - 1)n + c \le 0$$

Move $(2c - 1)n$ to the right-hand side:

$$c \le (2c - 1)n$$

Divide both sides by $n$ (valid because $n \ge 1$):

$$\frac{c}{n} \le 2c - 1$$

What is the worst-case (largest) value of $\frac{c}{n}$ for integers $n \ge 1$? It occurs when $n = 1$, where $\frac{c}{1} = c$.  
So if we satisfy this for $n = 1$:

$$c \le 2c - 1 \implies 1 \le c \iff c \ge 1$$

Thus, any choice of $c \ge 1$ makes $-(2c - 1)n + c \le 0$ true for all $n \ge 1$.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Verify the Base Case</summary>
**What changed from Step 3?** Check $n = 1$.  
**How do we do it?** * From definition: $T(1) = 1$.
* Target inequality: $T(1) \le c \cdot (1)^2 = c$.
* If we select $c = 1$:

$$T(1) = 1 \le 1(1)^2 = 1 \quad \text{(Holds)}$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Conclusion</summary>
**What is the final answer?** With $c = 1$ and $n_0 = 1$, $T(n) \le 1 \cdot n^2$ for all $n \ge 1$. Therefore, $T(n) = O(n^2)$.  
**Why does this answer make sense?** The arithmetic series sums to $\frac{n^2 + n}{2}$. For $n \ge 1$, $\frac{n^2 + n}{2} \le \frac{n^2 + n^2}{2} = n^2$. Our induction rigorously matches this exact arithmetic truth.
</details>

</div>

---

## Level 2: Divide-and-Conquer Recurrences (Halving Input)

In this level, we move to recurrences where the input size is divided by 2. This is the hallmark of algorithms like Merge Sort and Binary Search.

---

### Problem 2.1: Merge Sort Recurrence: $T(n) = 2T(n/2) + n$

**Problem Statement:** Given the recurrence relation:

$$T(n) = \begin{cases} 1 & \text{if } n = 1 \\ 2T(n/2) + n & \text{if } n > 1 \text{ (assume } n \text{ is a power of 2)} \end{cases}$$

Use the Substitution Method to prove that $T(n) = O(n \log_2 n)$.

::: callout-intuition Core Mental Model
Merge Sort splits an array into two halves ($2T(n/2)$) and does linear merging work ($+ n$). At each level of the recursion tree, the total work across all subproblems is always $n$. Since the tree has $\log_2 n$ levels, multiplying the work per level by the depth gives $n \log_2 n$.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: State the Guess and the Inductive Hypothesis</summary>
**What are we doing?** Formulate the mathematical hypothesis for $O(n \log_2 n)$.  
**How do we do it?** * We guess that $T(n) \le c \cdot n \log_2 n$ for some constant $c > 0$.
* **Inductive Hypothesis:** Assume this inequality holds for all positive integers strictly smaller than $n$. Specifically, for the subproblem of size $n/2$:

$$T(n/2) \le c \left(\frac{n}{2}\right) \log_2\left(\frac{n}{2}\right)$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Substitute into the Recurrence and Apply Log Rules</summary>
**What changed from Step 1?** We plug our hypothesis into $T(n) = 2T(n/2) + n$.  
**How do we do it?** $$T(n) \le 2 \left[ c \left(\frac{n}{2}\right) \log_2\left(\frac{n}{2}\right) \right] + n$$

Cancel the $2$ and the $\frac{1}{2}$:

$$T(n) \le c \cdot n \cdot \log_2\left(\frac{n}{2}\right) + n$$

**Where did this log rule come from?** Use the logarithm quotient rule: $\log_2(A / B) = \log_2(A) - \log_2(B)$.  
Here: $\log_2(n/2) = \log_2(n) - \log_2(2) = \log_2(n) - 1$.  
Substitute this back:

$$T(n) \le c \cdot n \cdot [\log_2(n) - 1] + n$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Expand and Re-group to match target</summary>
**What changed from Step 2?** Expand the bracketed multiplication.  
**How do we manipulate the equation?** $$T(n) \le c \cdot n \log_2(n) - c \cdot n + n$$

Group the final two linear terms together:

$$T(n) \le c \cdot n \log_2(n) - (c - 1)n$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Solve for $c$ to satisfy the Big-O bound</summary>
**What changed from Step 3?** We need our expression to stay bounded by our target: $c \cdot n \log_2(n)$.  
**How do we do it?** We require:

$$c \cdot n \log_2(n) - (c - 1)n \le c \cdot n \log_2(n)$$

Subtract $c \cdot n \log_2(n)$ from both sides:

$$-(c - 1)n \le 0$$

Divide both sides by $n$ (since $n > 0$):

$$-(c - 1) \le 0 \implies c - 1 \ge 0 \iff c \ge 1$$

As long as $c \ge 1$, the negative term $-(c - 1)n$ is $\le 0$, which guarantees the inequality holds!
</details>

<details class="step-card">
<summary class="step-badge">Step 5: The Base Case Hurdle and How to Resolve It</summary>
**What are we doing?** We test the base case $n = 1$.  
**What goes wrong?** Let us plug $n = 1$ into our target formula:

$$T(1) \le c \cdot 1 \cdot \log_2(1) = c \cdot 1 \cdot 0 = 0$$

But the recurrence explicitly specifies $T(1) = 1$!  
Since $1 \le 0$ is completely **false**, the base case fails at $n = 1$.  
**How do we resolve this?** Recall the formal definition of Big-$O$: the inequality only needs to hold for all $n \ge n_0$. We do **not** have to start at $n_0 = 1$! We can pick a larger base case, such as $n_0 = 2$.  
* Compute $T(2)$ using the recurrence:

$$T(2) = 2T(2/2) + 2 = 2T(1) + 2 = 2(1) + 2 = 4$$

* Check target bound at $n = 2$:

$$T(2) \le c \cdot 2 \cdot \log_2(2) = c \cdot 2 \cdot 1 = 2c$$

We require $T(2) \le 2c$:

$$4 \le 2c \iff c \ge 2$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Conclusion</summary>
**What is the final answer?** Choosing $c = 2$ and $n_0 = 2$ satisfies both the base case ($T(2) = 4 \le 2(2) = 4$) and the inductive step ($c \ge 1$).  
Therefore:

$$T(n) = O(n \log_2 n)$$
</details>

</div>

---

### Problem 2.2: Binary Search Recurrence: $T(n) = T(n/2) + 1$

**Problem Statement:** Given the recurrence relation:

$$T(n) = \begin{cases} 1 & \text{if } n = 1 \\ T(n/2) + 1 & \text{if } n > 1 \end{cases}$$

Use the Substitution Method to prove that $T(n) = O(\log_2 n)$.

::: callout-intuition Core Mental Model
In Binary Search, each comparison discards half the remaining elements and costs 1 comparison. The number of times you can cut an array in half until 1 item remains is $\log_2 n$.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: State the Inductive Hypothesis</summary>
**What are we doing?** We guess $T(n) \le c \log_2 n$.  
**How do we do it?** * **Inductive Hypothesis:** Assume for the smaller size $n/2$:

$$T(n/2) \le c \log_2(n/2)$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Substitute and Simplify</summary>
**What changed from Step 1?** Plug into $T(n) = T(n/2) + 1$.  
**How do we do it?** $$T(n) \le c \log_2(n/2) + 1$$

Apply logarithm division rule $\log_2(n/2) = \log_2 n - \log_2 2 = \log_2 n - 1$:

$$T(n) \le c(\log_2 n - 1) + 1 = c \log_2 n - c + 1$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Solve for $c$</summary>
**What changed from Step 2?** Match against target ceiling $c \log_2 n$.  
**How do we do it?** We require:

$$c \log_2 n - c + 1 \le c \log_2 n \implies -c + 1 \le 0 \iff c \ge 1$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Verify Base Case at $n_0 = 2$</summary>
**What are we doing?** Since $\log_2(1) = 0$, we test base case at $n = 2$:
* From recurrence: $T(2) = T(1) + 1 = 1 + 1 = 2$.
* From bound: $T(2) \le c \log_2(2) = c(1) = c$.
* Setting $2 \le c \implies c \ge 2$.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Conclusion</summary>
**What is the final answer?** Choosing $c = 2$ and $n_0 = 2$ guarantees $T(n) \le 2 \log_2 n$ for all $n \ge 2$.  
Therefore, $T(n) = O(\log n)$.
</details>

</div>

---

## Level 3: Advanced Traps & The "Lower-Order Subtraction Trick"

In this level, we tackle the most notorious trap in algorithmic induction: **when a naive guess is asymptotically correct, but the inductive proof fails because the algebra leaves behind an unwanted constant.** We demonstrate how subtracting a lower-order term fixes the proof completely.

---

### Problem 3.1: The Failing Induction Trap on $T(n) = 2T(n/2) + 1$

**Problem Statement:** Consider the recurrence:

$$T(n) = 2T(n/2) + 1 \quad \text{with } T(1) = 1$$

A student guesses that $T(n) = O(n)$ because the Master Theorem gives $n^{\log_2 2} = n^1$.  
1. Show why the naive hypothesis $T(n) \le c \cdot n$ fails.
2. Fix the proof by strengthening the hypothesis using the subtraction trick: $T(n) \le c \cdot n - d$.

::: callout-intuition Core Mental Model
Imagine jumping across a chasm with a heavy backpack. You miss the ledge by just 2 inches. You do not need a rocket booster; you just need to drop 5 pounds of luggage. When your induction is left with an extra $+1$ that ruins the inequality $\le c \cdot n$, your guess is "too loose". By subtracting a constant ($c \cdot n - d$), the algebra produces a negative balance that absorbs the rogue $+1$.
:::

#### Part A: Demonstrating the Failure of the Naive Guess

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Attempt the Naive Inductive Hypothesis</summary>
**What are we doing?** We try to prove $T(n) \le c \cdot n$ directly.  
**Hypothesis:** Assume $T(n/2) \le c(n/2)$.  
**Substitute into recurrence:**

$$T(n) = 2T(n/2) + 1 \le 2\left(c \frac{n}{2}\right) + 1$$

Simplify:

$$T(n) \le c \cdot n + 1$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Witness the Fatal Algebraic Failure</summary>
**What changed from Step 1?** We attempt to enforce our target inequality: $T(n) \le c \cdot n$.  
**Where does it break?** We need:

$$c \cdot n + 1 \le c \cdot n$$

Subtract $c \cdot n$ from both sides:

$$1 \le 0 \quad \text{\textbf{(FALSE FOR ALL CHOICES OF }} c \text{\textbf{!)}}$$

**Why did this happen?** No matter how large a value of $c$ you pick ($c = 100$, $c = 1{,}000{,}000$), $c \cdot n + 1$ will ALWAYS be strictly greater than $c \cdot n$. The $+1$ never goes away! The naive induction fails completely.
</details>

</div>

#### Part B: Fixing the Proof with the Subtraction Trick

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Strengthen the Inductive Hypothesis by Subtracting a Constant $d$</summary>
**What are we doing?** We revise our guess to include a subtracted lower-order constant $d > 0$:

$$T(n) \le c \cdot n - d$$

**Why are we subtracting instead of adding?** If we prove $T(n) \le c \cdot n - d$, then because $d > 0$, it is automatically true that $T(n) \le c \cdot n$ (since $c \cdot n - d < c \cdot n$). Subtracting a constant makes our hypothesis *stronger* (tighter), which gives us more algebraic ammunition on the smaller side!  
**Inductive Hypothesis:** Assume for the smaller subproblem:

$$T(n/2) \le c\left(\frac{n}{2}\right) - d$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Substitute the Strengthened Hypothesis into Recurrence</summary>
**What changed from Step 1?** We plug the new hypothesis into $T(n) = 2T(n/2) + 1$.  
**How do we do it?** $$T(n) \le 2\left(c \frac{n}{2} - d\right) + 1$$

Distribute the $2$ to both terms inside the parentheses:

$$T(n) \le 2 \cdot c \frac{n}{2} - 2d + 1$$

Simplify:

$$T(n) \le c \cdot n - 2d + 1$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Force the expression into the target shape $(c \cdot n - d)$</summary>
**What changed from Step 2?** Our target is not $c \cdot n$; our target is $c \cdot n - d$.  
**How do we manipulate the equation?** Rewrite $-2d$ as $-d - d$:

$$T(n) \le c \cdot n - d - d + 1 = (c \cdot n - d) - (d - 1)$$

To guarantee that $T(n) \le c \cdot n - d$, we require the extra trailing piece to be $\le 0$:

$$-(d - 1) \le 0 \implies d - 1 \ge 0 \iff d \ge 1$$

Look at what happened! By choosing $d = 1$, the rogue $+1$ is completely neutralized by $-2d + 1 = -2(1) + 1 = -1 = -d$!  
The algebraic contradiction has vanished!
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Check the Base Case and Solve for $c$</summary>
**What changed from Step 3?** We test our chosen $d = 1$ on the base case $n = 1$.  
**How do we do it?** * Given base value: $T(1) = 1$.
* Target formula with $d = 1$:

$$T(1) \le c(1) - d = c(1) - 1 = c - 1$$

Enforce the inequality:

$$1 \le c - 1 \implies c \ge 2$$

So we choose $c = 2$ and $d = 1$.  
Let us test: $T(1) = 1 \le 2(1) - 1 = 1$. It holds with exact equality!
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State the Complete Validated Bound</summary>
**What is the final answer?** With constants $c = 2$ and $d = 1$:

$$T(n) \le 2n - 1 \quad \text{for all } n \ge 1$$

Since $2n - 1 \le 2n$, it follows that:

$$T(n) \le 2n \implies T(n) = O(n)$$

**Why does this answer make sense?** Unrolling $T(n) = 2T(n/2) + 1$ explicitly yields $T(n) = 2n - 1$ exactly. The naive hypothesis failed because it attempted to prove $2n - 1 \le c \cdot n$ without acknowledging the $-1$ offset. Subtracting $d$ restored algebraic symmetry to the induction.
</details>

</div>

---

### Problem 3.2: Uneven Divide-and-Conquer Recurrence: $T(n) = T(n/3) + T(2n/3) + n$

**Problem Statement:** Prove that the unbalanced divide-and-conquer recurrence:

$$T(n) = T(n/3) + T(2n/3) + n \quad \text{with } T(1) = 1$$

satisfies $T(n) = O(n \log_2 n)$.

::: callout-intuition Core Mental Model
Even though the subproblems are unequal (one gets $1/3$ of the data, the other gets $2/3$), the total work done at each recursion level is still $\frac{1}{3}n + \frac{2}{3}n = 1n$. Because the sum of the fractions equals 1, the total work per level remains exactly $n$. The deepest branch reaches depth $\log_{3/2} n$, which differs from $\log_2 n$ only by a constant multiplier.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Formulate the Inductive Hypothesis</summary>
**What are we doing?** We state the hypothesis for two unequal branches simultaneously.  
**Hypothesis:** Assume for all values $k < n$ that $T(k) \le c \cdot k \log_2 k$.  
Specifically, we assume this holds for $k = n/3$ and $k = 2n/3$:

$$T(n/3) \le c\left(\frac{n}{3}\right)\log_2\left(\frac{n}{3}\right)$$
$$T(2n/3) \le c\left(\frac{2n}{3}\right)\log_2\left(\frac{2n}{3}\right)$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Substitute into Recurrence and Expand Logarithms</summary>
**What changed from Step 1?** Plug both assumptions into $T(n) = T(n/3) + T(2n/3) + n$:

$$T(n) \le c\left(\frac{n}{3}\right)\log_2\left(\frac{n}{3}\right) + c\left(\frac{2n}{3}\right)\log_2\left(\frac{2n}{3}\right) + n$$

Apply the quotient rule $\log_2(A/B) = \log_2 A - \log_2 B$:
* $\log_2(n/3) = \log_2 n - \log_2 3$
* $\log_2(2n/3) = \log_2(2n) - \log_2 3 = \log_2 n + \log_2 2 - \log_2 3 = \log_2 n + 1 - \log_2 3$

Substitute these expansions back:

$$T(n) \le c\frac{n}{3}[\log_2 n - \log_2 3] + c\frac{2n}{3}[\log_2 n + 1 - \log_2 3] + n$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Collect Like Terms Algebraically</summary>
**What changed from Step 2?** Group all terms containing $\log_2 n$ together, and all linear $n$ terms together.  
**How do we manipulate the equation?**
First, distribute the fractions:

$$T(n) \le \left(c\frac{n}{3}\log_2 n + c\frac{2n}{3}\log_2 n\right) - c\frac{n}{3}\log_2 3 - c\frac{2n}{3}\log_2 3 + c\frac{2n}{3}(1) + n$$

Combine the $\log_2 n$ terms:

$$c\frac{n}{3}\log_2 n + c\frac{2n}{3}\log_2 n = c\left(\frac{1}{3} + \frac{2}{3}\right)n \log_2 n = c \cdot n \log_2 n$$

Combine the $\log_2 3$ terms:

$$- c\frac{n}{3}\log_2 3 - c\frac{2n}{3}\log_2 3 = -c\left(\frac{1}{3} + \frac{2}{3}\right)n \log_2 3 = -c \cdot n \log_2 3$$

Putting it all together:

$$T(n) \le c \cdot n \log_2 n - c \cdot n \log_2 3 + \frac{2}{3}c \cdot n + n$$

Factor out $n$:

$$T(n) \le c \cdot n \log_2 n - n \left[ c\left(\log_2 3 - \frac{2}{3}\right) - 1 \right]$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Solve for $c$ to Guarantee the Bound</summary>
**What changed from Step 3?** We require the subtracted quantity inside the bracket to be $\ge 0$ so that $T(n) \le c \cdot n \log_2 n$.  
**How do we calculate it?**
We need:

$$c\left(\log_2 3 - \frac{2}{3}\right) - 1 \ge 0 \iff c\left(\log_2 3 - \frac{2}{3}\right) \ge 1$$

Calculate the numerical value of $\log_2 3 - \frac{2}{3}$:
* Since $2^{1.585} \approx 3$, we have $\log_2 3 \approx 1.585$.
* $\frac{2}{3} \approx 0.667$.
* Difference: $\log_2 3 - \frac{2}{3} \approx 1.585 - 0.667 = 0.918 > 0$.

Because this difference is strictly positive ($0.918$), we can safely divide:

$$c \ge \frac{1}{\log_2 3 - 2/3} \approx \frac{1}{0.918} \approx 1.09$$

Choosing any constant $c \ge 2$ easily satisfies this condition!
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Conclusion</summary>
**What is the final answer?** By choosing $c \ge 2$ and handling the base cases for small values of $n \ge 3$, the inductive step holds:

$$T(n) \le c \cdot n \log_2 n \implies T(n) = O(n \log n)$$

**Why does this answer make sense?** Even with asymmetric splits, the total work per level of recursion sums to $n$. As long as the sum of the argument coefficients ($\frac{1}{3} + \frac{2}{3} = 1$) equals 1, the total work per tier is conserved, producing a clean $\Theta(n \log n)$ bound.
</details>

</div>
