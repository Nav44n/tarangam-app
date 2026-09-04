# Progressive Problems: The Recursion Tree & Iteration Method

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic high-school arithmetic and algebra.

---

## The Recursion Tree Blueprint (The 5 Fundamental Questions)

To solve any recurrence using a recursion tree, we always answer these five questions in order:
1. **Node Cost:** How much non-recursive work is done at a single node of size $k$?
2. **Branching Factor:** How many children does each node spawn?
3. **Cost per Level:** What is the sum of costs of all nodes sitting on level $i$?
4. **Tree Height:** How many levels exist before the subproblem size shrinks down to $1$?
5. **Total Summation:** What do we get when we add the costs of all levels plus the base-case leaf nodes?

---

## Level 1: Perfectly Balanced Recursion Trees

In this level, every recursive branch divides by the same factor. Every path from the root to a leaf has the exact same length, making the tree completely symmetrical.

---

### Problem 1.1: Balanced Tree with Equal Cost per Level: $T(n) = 2T(n/2) + n$

**Problem Statement:** Use the Recursion Tree Method to solve the recurrence:

$$T(n) = 2T(n/2) + n \quad \text{with } T(1) = 1 \text{ (assume } n \text{ is a power of 2)}$$

::: callout-intuition Core Mental Model
Imagine a company CEO who has a budget of $n$ tasks. The CEO keeps $n$ tasks to organize at the top level, but delegates two equal packages of size $n/2$ to two managers ($2T(n/2)$). Each manager keeps their own portion of work ($n/2$) and delegates to two junior leads ($n/4$ each). At every corporate tier, when you add up all the work done by everyone on that horizontal floor, it always sums to exactly $n$. The total company effort is simply (work per floor) $\times$ (number of floors).
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Decompose the root node (Level 0)</div>
**What are we doing?** We draw the top of the tree (Level $i = 0$).  
**Why are we starting here?** Every recursion begins with the original problem of size $n$.  
**How do we do it?** The recurrence says $T(n) = 2T(n/2) + n$.  
* The local work done at this root node is the non-recursive term: $+ n$.
* The subproblems spawned are two calls of size $n/2$:

```
Level 0:                 [ n ]                  ---> Cost: n
                        /     \
                T(n/2)           T(n/2)
```

At Level 0:
* Number of nodes: $2^0 = 1$
* Size of each node's problem: $\frac{n}{2^0} = n$
* Total work at Level 0: $1 \times n = n$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Expand to Level 1 and Level 2</div>
**What changed from Step 1?** We expand the children nodes by applying the recurrence formula to size $n/2$.  
**How do we do it?** * For each $T(n/2)$ node, the non-recursive work is $\frac{n}{2}$, and it spawns two subproblems of size $\frac{n/2}{2} = \frac{n}{4}$:

```
Level 0:                 [ n ]                  ---> Cost: n
                        /     \
Level 1:           [ n/2 ]   [ n/2 ]            ---> Cost: n/2 + n/2 = n
                   /    \     /    \
Level 2:       [n/4]  [n/4] [n/4]  [n/4]        ---> Cost: 4 * (n/4) = n
```

Let us calculate the total work on each level explicitly:
* **Level 1:** There are $2^1 = 2$ nodes. Each node does work $\frac{n}{2}$.  
  $$\text{Level 1 Cost} = 2 \times \left(\frac{n}{2}\right) = n$$
* **Level 2:** There are $2^2 = 4$ nodes. Each node does work $\frac{n}{4}$.  
  $$\text{Level 2 Cost} = 4 \times \left(\frac{n}{4}\right) = n$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Express the general formula for Level $i$</div>
**What changed from Step 2?** We generalize the pattern to any arbitrary depth $i$ (where $i = 0, 1, 2, \dots$).  
**How do we manipulate the equation?** * Number of nodes at level $i$: doubles at each tier $\implies 2^i$.
* Size of subproblem at level $i$: halves at each tier $\implies \frac{n}{2^i}$.
* Cost of one node at level $i$: equal to its subproblem size $\implies \frac{n}{2^i}$.  
Multiply (number of nodes) $\times$ (cost per node):

$$\text{Cost of Level } i = 2^i \times \left(\frac{n}{2^i}\right) = n$$

**Where did this result come from?** The $2^i$ in the numerator cancels the $2^i$ in the denominator! The cost per level is a constant $n$, completely independent of the level index $i$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Determine the height of the tree $h$</div>
**What are we doing?** We find how many levels exist before the subproblem size shrinks to the base case size $1$.  
**Why are we doing this?** We need to know how many levels of cost $n$ to add together.  
**How do we do it?** At the leaf level (call it level $h$), the subproblem size has shrunk down to $1$:

$$\frac{n}{2^h} = 1$$

Multiply both sides by $2^h$:

$$n = 2^h$$

Take the base-2 logarithm ($\log_2$) of both sides:

$$\log_2(n) = \log_2(2^h) \implies h = \log_2(n)$$

Thus, the tree levels are indexed from $i = 0$ to $i = \log_2(n)$.  
The total number of levels is:

$$\text{Total Levels} = \text{height} + 1 = \log_2(n) + 1$$
</div>

<div class="step-card">
<div class="step-badge">Step 5: Calculate the leaf-level base-case work</div>
**What changed from Step 4?** We count how much work is done exclusively by the base-case leaves at level $h = \log_2 n$.  
**How do we do it?** * Number of leaves: $2^h = 2^{\log_2 n} = n$.
* Cost per leaf: $T(1) = 1$.  
$$\text{Cost of all leaves} = n \times T(1) = n \times 1 = n$$
</div>

<div class="step-card">
<div class="step-badge">Step 6: Sum the costs of all levels</div>
**What changed from Step 5?** We sum the cost from level $i = 0$ all the way down to level $i = \log_2 n$.  
**How do we do it?** Total work $T(n)$ is the sum across all levels:

$$T(n) = \sum_{i=0}^{\log_2 n} (\text{Cost of Level } i)$$

Since every level costs exactly $n$:

$$T(n) = \sum_{i=0}^{\log_2 n} n = n \times \left( \sum_{i=0}^{\log_2 n} 1 \right)$$

How many terms are in the sum from $i = 0$ to $\log_2 n$?  
Using the counting formula $\text{end} - \text{start} + 1$:

$$\text{Count} = \log_2 n - 0 + 1 = \log_2 n + 1$$

Therefore:

$$T(n) = n \cdot (\log_2 n + 1) = n \log_2 n + n$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: State the Asymptotic Complexity</div>
**What is the final answer?** $T(n) = \Theta(n \log n)$.  
**Why does this answer make sense?** The tree has $\log_2 n + 1$ horizontal floors. Every floor performs exactly $n$ operations. Multiplying (levels) $\times$ (work per level) yields $(n) \times (\log_2 n + 1) = \Theta(n \log n)$.
</div>

</div>

---

### Problem 1.2: Root-Dominated Balanced Tree: $T(n) = 3T(n/4) + cn^2$

**Problem Statement:** Use the Recursion Tree Method to solve the recurrence:

$$T(n) = 3T(n/4) + cn^2 \quad \text{with } T(1) = d$$

::: callout-intuition Core Mental Model
Imagine a funnel where almost all water stays at the very top rim, with only a tiny trickle reaching the lower pipes. Here, the local work is quadratic ($n^2$). When the problem size quarters to $n/4$, the work shrinks by a factor of $4^2 = 16$! Even though there are 3 children, the work per child drops by 16, meaning the total work at each deeper level shrinks geometrically. The root node does the lion's share of all work.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Analyze Node Counts and Subproblem Sizes per Level</div>
**What are we doing?** We identify how the tree branches and how the subproblem sizes shrink.  
**How do we do it?** * **Branching factor:** Each node splits into $3$ children. At level $i$, there are $3^i$ nodes.
* **Subproblem size:** Divided by $4$ at each step. At level $i$, each node has size $\frac{n}{4^i}$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Calculate the work done at Level $i$</div>
**What changed from Step 1?** We calculate the cost of a single node and multiply by the number of nodes at level $i$.  
**How do we do it?** * Cost function: $f(k) = c \cdot k^2$.
* Cost of one node at level $i$:

$$f\left(\frac{n}{4^i}\right) = c \cdot \left(\frac{n}{4^i}\right)^2 = c \cdot \frac{n^2}{(4^i)^2} = c \cdot \frac{n^2}{16^i}$$

* Total cost of Level $i$ (multiply by $3^i$ nodes):

$$\text{Level } i \text{ Cost} = 3^i \times \left( c \cdot \frac{n^2}{16^i} \right) = c \cdot n^2 \cdot \left(\frac{3}{16}\right)^i$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Determine the tree height and leaf-level cost</div>
**What are we doing?** Find the leaf level $h$ and total leaf work.  
**How do we do it?** The leaves are reached when the size shrinks to $1$:

$$\frac{n}{4^h} = 1 \implies 4^h = n \implies h = \log_4(n)$$

* **Total number of leaves:**

$$\text{Leaves} = 3^h = 3^{\log_4 n} = n^{\log_4 3}$$

**Where did this exponent swap come from?** The logarithm power identity: $a^{\log_b c} = c^{\log_b a}$.  
Since $\log_4 3 \approx 0.793$:

$$\text{Cost of all leaves} = n^{\log_4 3} \times T(1) = d \cdot n^{\log_4 3} = \Theta(n^{0.793})$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Sum all internal levels using the Geometric Series Formula</div>
**What changed from Step 3?** We sum the costs of all levels from $i = 0$ to $h - 1$:

$$\text{Internal Cost} = \sum_{i=0}^{\log_4(n) - 1} c n^2 \left(\frac{3}{16}\right)^i = c n^2 \sum_{i=0}^{\log_4(n) - 1} \left(\frac{3}{16}\right)^i$$

**Where did the series formula come from?** For any ratio $r < 1$, an infinite geometric series satisfies:

$$\sum_{i=0}^{\infty} r^i = \frac{1}{1 - r}$$

Because our finite sum is strictly smaller than the infinite sum:

$$\sum_{i=0}^{\log_4(n) - 1} \left(\frac{3}{16}\right)^i < \sum_{i=0}^{\infty} \left(\frac{3}{16}\right)^i = \frac{1}{1 - \frac{3}{16}} = \frac{1}{\frac{13}{16}} = \frac{16}{13}$$

Therefore:

$$\text{Internal Cost} < cn^2 \left(\frac{16}{13}\right) = \frac{16}{13} c n^2$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Combine Internal Work and Leaf Work</div>
**What is the final answer?** $T(n) = \Theta(n^2)$.  
**Why does this answer make sense?** * Total work $= \text{Internal Work} + \text{Leaf Work}$.
* Internal work $= \Theta(n^2)$.
* Leaf work $= \Theta(n^{\log_4 3}) \approx \Theta(n^{0.793})$.
* Since $n^2$ grows dramatically faster than $n^{0.793}$, the top-level root work completely dominates the entire tree:

$$T(n) = \Theta(n^2)$$
</div>

</div>

---

## Level 2: Asymmetric / Unbalanced Recursion Trees

In this level, subproblems divide unevenly. Different branches terminate at completely different depths, producing a lopsided tree with a ragged bottom.

---

### Problem 2.1: The Asymmetric Tree: $T(n) = T(n/3) + T(2n/3) + n$

**Problem Statement:** Use the Recursion Tree Method to find the asymptotic bound of:

$$T(n) = T(n/3) + T(2n/3) + n \quad \text{with } T(1) = 1$$

::: callout-intuition Core Mental Model
Imagine an uneven tree where the left branches shrink very quickly (dividing by 3) and hit the ground first, while the right branches shrink very slowly (dividing by 1.5, or keeping 2/3 of their weight) and plunge much deeper into the earth. The tree is not a neat rectangle; it has a jagged bottom. However, on every full level near the top, the total weight sums to $n$.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Draw the first three levels of the uneven tree</div>
**What are we doing?** We draw the tree and compute the sum of costs row by row.  
**How do we do it?** * Level 0: The root does work $n$. It spawns two children of sizes $n/3$ and $2n/3$.
* Level 1: Left child does work $n/3$. Right child does work $2n/3$.  
  $$\text{Level 1 Sum} = \frac{n}{3} + \frac{2n}{3} = \left(\frac{1}{3} + \frac{2}{3}\right)n = 1n$$
* Level 2: 
  * $n/3$ splits into $\frac{n/3}{3} = \frac{n}{9}$ and $\frac{2(n/3)}{3} = \frac{2n}{9}$.
  * $2n/3$ splits into $\frac{2n/3}{3} = \frac{2n}{9}$ and $\frac{2(2n/3)}{3} = \frac{4n}{9}$.
  * Add all four nodes at Level 2:
  $$\text{Level 2 Sum} = \frac{n}{9} + \frac{2n}{9} + \frac{2n}{9} + \frac{4n}{9} = \frac{1 + 2 + 2 + 4}{9} n = \frac{9}{9} n = 1n$$

```
Level 0:                    [  n  ]                     ---> Cost = n
                           /       \
Level 1:           [ n/3 ]           [ 2n/3 ]           ---> Cost = n
                   /     \           /      \
Level 2:       [n/9]    [2n/9]   [2n/9]    [4n/9]       ---> Cost = n
               /   \     /   \   /    \    /    \
              ...  ...  ...  ... ...  ... ...   ...
```
</div>

<div class="step-card">
<div class="step-badge">Step 2: Calculate the Shortest Branch Depth ($h_{\min}$)</div>
**What are we doing?** We follow the most aggressive division path (always taking the $n/3$ branch) to find when the very first leaf appears.  
**Why are we starting here?** Once the first leaf is reached, deeper levels will no longer be full, meaning the cost per level will begin to drop below $n$.  
**How do we do it?** Along the extreme left path, the subproblem size after $k$ steps is $\frac{n}{3^k}$.  
Set this size to $1$:

$$\frac{n}{3^{h_{\min}}} = 1 \implies 3^{h_{\min}} = n \implies h_{\min} = \log_3(n)$$

Thus, all levels from $i = 0$ down to $i = \log_3(n)$ are **completely full**, and every single one of those levels costs exactly $n$!
</div>

<div class="step-card">
<div class="step-badge">Step 3: Calculate the Longest Branch Depth ($h_{\max}$)</div>
**What changed from Step 2?** We follow the slowest division path (always taking the $2n/3$ branch) to find the absolute maximum depth of the tree.  
**How do we do it?** Along the extreme right path, the size after $k$ steps is $n \cdot \left(\frac{2}{3}\right)^k = \frac{n}{(3/2)^k}$.  
Set this size to $1$:

$$\frac{n}{(3/2)^{h_{\max}}} = 1 \implies \left(\frac{3}{2}\right)^{h_{\max}} = n \implies h_{\max} = \log_{3/2}(n)$$

Thus, the tree terminates completely at depth $\log_{3/2}(n)$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Establish the Lower Bound ($\Omega$)</div>
**What are we doing?** We sum only the guaranteed full levels to establish a lower bound.  
**How do we do it?** Every level from $i = 0$ to $i = \log_3(n)$ is 100% complete and costs exactly $n$:

$$T(n) \ge \sum_{i=0}^{\log_3(n)} n = n \cdot (\log_3(n) + 1)$$

Using the base-change formula for logarithms $\log_3(n) = \frac{\log_2 n}{\log_2 3}$:

$$T(n) \ge \frac{1}{\log_2 3} n \log_2 n \implies T(n) = \Omega(n \log n)$$
</div>

<div class="step-card">
<div class="step-badge">Step 5: Establish the Upper Bound ($O$)</div>
**What changed from Step 4?** Beyond level $\log_3(n)$, leaves start terminating, so levels cost *strictly less* than $n$.  
**How do we do it?** If we pretend every level all the way to the maximum depth $h_{\max}$ were completely full and cost $n$, we obtain an upper bound:

$$T(n) \le \sum_{i=0}^{\log_{3/2}(n)} n = n \cdot (\log_{3/2}(n) + 1)$$

Using the base-change formula $\log_{3/2}(n) = \frac{\log_2 n}{\log_2(1.5)}$:

$$T(n) \le \frac{1}{\log_2(1.5)} n \log_2 n \implies T(n) = O(n \log n)$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Combine into Big-$\Theta$ Conclusion</div>
**What is the final answer?** $T(n) = \Theta(n \log n)$.  
**Why does this answer make sense?** * Lower bound floor: $\Omega(n \log_3 n) = \Omega(n \log n)$.
* Upper bound ceiling: $O(n \log_{3/2} n) = O(n \log n)$.
* Since the floor and ceiling differ only by a constant ratio $\left(\frac{\log_2 3}{\log_2(1.5)}\right)$, the function is tightly bounded:

$$T(n) = \Theta(n \log n)$$
</div>

</div>

---

## Level 3: The Iteration (Unrolling) Method

The Iteration Method (or "unrolling") is the algebraic equivalent of drawing a recursion tree. Instead of drawing boxes and branches, we substitute the recurrence equation back into itself repeatedly until a general formula emerges.

---

### Problem 3.1: Unrolling a Linear Recurrence: $T(n) = T(n - 1) + 2n$

**Problem Statement:** Solve the recurrence $T(n) = T(n - 1) + 2n$ with base case $T(0) = 0$ using the Iteration / Unrolling Method.

::: callout-intuition Core Mental Model
Think of unwrapping nested Russian nesting dolls. You open the outermost doll $T(n)$ and find a smaller doll $T(n-1)$ plus a label "$+ 2n$". You unwrap $T(n-1)$ and find a smaller doll $T(n-2)$ plus "$+ 2(n-1)$". You continue peeling layers until you hit the solid wooden core $T(0)$.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Perform the first three unrollings</div>
**What are we doing?** We repeatedly substitute the definition of $T(\dots)$ into itself.  
**Why are we starting here?** Seeing 3 consecutive substitutions reveals the evolving mathematical pattern.  
**How do we do it?** * Base formula: $T(n) = T(n - 1) + 2n$
* **1st Unrolling:** Replace $T(n - 1)$ with $[T(n - 2) + 2(n - 1)]$:  
  $$T(n) = [T(n - 2) + 2(n - 1)] + 2n$$
  $$T(n) = T(n - 2) + 2(n - 1) + 2n$$
* **2nd Unrolling:** Replace $T(n - 2)$ with $[T(n - 3) + 2(n - 2)]$:  
  $$T(n) = [T(n - 3) + 2(n - 2)] + 2(n - 1) + 2n$$
  $$T(n) = T(n - 3) + 2(n - 2) + 2(n - 1) + 2n$$
* **3rd Unrolling:** Replace $T(n - 3)$ with $[T(n - 4) + 2(n - 3)]$:  
  $$T(n) = T(n - 4) + 2(n - 3) + 2(n - 2) + 2(n - 1) + 2n$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Express the pattern at iteration $k$</div>
**What changed from Step 1?** We replace the specific step numbers ($1, 2, 3$) with an arbitrary variable $k$.  
**How do we manipulate the equation?** Look at the indices after $k$ substitutions:
* The subproblem is size $n - k$.
* The sum contains terms starting from $2(n - (k - 1))$ up to $2n$.

$$T(n) = T(n - k) + \sum_{j=0}^{k - 1} 2(n - j)$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Solve for the base case iteration $k$</div>
**What are we doing?** We find the exact value of $k$ that reaches the base case $T(0)$.  
**How do we do it?** We set the subproblem argument equal to the base case input:

$$n - k = 0 \implies k = n$$

Substitute $k = n$ into our general formula from Step 2:

$$T(n) = T(0) + \sum_{j=0}^{n - 1} 2(n - j)$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Evaluate the summation algebraically</div>
**What changed from Step 3?** We plug in $T(0) = 0$ and evaluate the arithmetic series.  
**How do we do it?** Write out the terms of the sum $\sum_{j=0}^{n - 1} 2(n - j)$:
* For $j = 0$: $2n$
* For $j = 1$: $2(n - 1)$
* $\dots$
* For $j = n - 1$: $2(1)$

$$T(n) = 0 + [2n + 2(n - 1) + 2(n - 2) + \dots + 2(1)]$$

Factor out the constant $2$:

$$T(n) = 2 \cdot [1 + 2 + 3 + \dots + n]$$

Substitute Gauss's sum formula $\frac{n(n + 1)}{2}$:

$$T(n) = 2 \cdot \left[ \frac{n(n + 1)}{2} \right] = n(n + 1) = n^2 + n$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: State Asymptotic Complexity</div>
**What is the final answer?** $T(n) = n^2 + n = \Theta(n^2)$.  
**Why does this answer make sense?** The unrolling process expands into an arithmetic sequence with $n$ terms where the average term has magnitude $n$. Multiplying (number of terms) $\times$ (average value) produces $n \times n = n^2$.
</div>

</div>

---

### Problem 3.2: Unrolling a Divide-and-Conquer Recurrence: $T(n) = 2T(n/2) + c$

**Problem Statement:** Solve $T(n) = 2T(n/2) + c$ with $T(1) = d$ using the Iteration Method.

::: callout-intuition Core Mental Model
Here, each step doubles the number of subproblems but adds only a fixed flat cost $c$. Unrolling this shows how repeated doubling builds a power of 2 that multiplies the base-case leaf work.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Perform repeated substitutions</div>
**What are we doing?** We substitute $T(n/2)$ into the recurrence equation.  
**How do we do it?** * Base equation: $T(n) = 2T(n/2) + c$
* **1st Unrolling:** Replace $T(n/2)$ with $[2T(n/4) + c]$:  
  $$T(n) = 2[2T(n/4) + c] + c = 4T(n/4) + 2c + c = 2^2 T(n/2^2) + c(2^1 + 2^0)$$
* **2nd Unrolling:** Replace $T(n/4)$ with $[2T(n/8) + c]$:  
  $$T(n) = 4[2T(n/8) + c] + 2c + c = 8T(n/8) + 4c + 2c + c = 2^3 T(n/2^3) + c(2^2 + 2^1 + 2^0)$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Express the state at step $k$</div>
**What changed from Step 1?** Generalize the powers of 2 for step $k$:

$$T(n) = 2^k T\left(\frac{n}{2^k}\right) + c \sum_{j=0}^{k - 1} 2^j$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Reach the base case size $1$</div>
**What are we doing?** Set $\frac{n}{2^k} = 1 \implies 2^k = n \implies k = \log_2 n$.  
Substitute $2^k = n$ and $k = \log_2 n$:

$$T(n) = n \cdot T(1) + c \sum_{j=0}^{\log_2(n) - 1} 2^j$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Solve the finite geometric series</div>
**What changed from Step 3?** We evaluate the sum $\sum_{j=0}^{\log_2(n) - 1} 2^j$.  
**Where did this formula come from?** The standard finite sum of powers of 2:

$$\sum_{j=0}^{m - 1} 2^j = 2^m - 1$$

With $m = \log_2 n$:

$$\sum_{j=0}^{\log_2(n) - 1} 2^j = 2^{\log_2 n} - 1 = n - 1$$

Substitute this back into our equation:

$$T(n) = n \cdot d + c(n - 1) = (d + c)n - c$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: State Asymptotic Complexity</div>
**What is the final answer?** $T(n) = \Theta(n)$.  
**Why does this answer make sense?** The total cost is a linear combination $(d + c)n - c$, which has leading term $n$. Thus:

$$T(n) = \Theta(n)$$
</div>

</div>
