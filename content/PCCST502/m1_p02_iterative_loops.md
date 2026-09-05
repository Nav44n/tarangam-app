# Progressive Problems: Iterative Loop Complexity

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior programming analysis background beyond basic arithmetic and algebra.

---

## Level 1: Single Independent Loops (Linear Counting & Step Sizes)

In this level, we examine loops that run one after another along a single line of execution. We focus on how loop indices change, how many times the loop body executes, and how step sizes alter the operation count.

---

### Problem 1.1: Single Loop Incrementing by 1 (Inclusive Boundaries)

**Problem Statement:** Analyze the time complexity $T(n)$ and find the Big-$\Theta$ bound for the following code snippet:

```c
int count = 0;
for (int i = 1; i <= n; i++) {
    count++;
}
```

::: callout-intuition Core Mental Model
Imagine you are walking along a row of fence posts numbered $1, 2, 3, \dots, n$. At every single fence post, you place a sticker on it (`count++`). If there are 10 posts, you place 10 stickers. If the number of posts doubles to 20, you place 20 stickers. The total work is strictly proportional to the total number of posts.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Identify the sequence of values taken by the loop variable</summary>
**What are we doing?** We list the exact numerical values that the loop counter $i$ takes during execution.  
**Why are we starting here?** A loop runs once for every unique value its counter assumes before failing the loop test. Listing these values reveals the pattern.  
**How do we do it?** * The loop initializes at $i = 1$.
* After every pass, $i{+}{+}$ adds $1$ to $i$.
* The loop continues as long as $i \le n$.
* The sequence of values is:

$$i \in \{1, 2, 3, 4, \dots, n\}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Calculate the exact number of iterations using the Fencepost Formula</summary>
**What changed from Step 1?** We convert the list of numbers into an exact count.  
**Why are we starting here?** Beginners often make "off-by-one" errors (forgetting whether to add or subtract 1). We must use a rigorous counting rule.  
**How do we do it?** When counting consecutive integers from a starting integer $\text{start}$ to an ending integer $\text{end}$ inclusive, the formula is:

$$\text{Count} = \text{end} - \text{start} + 1$$

**Where did this formula/concept come from?** Consider counting numbers from $1$ to $3$: $3 - 1 = 2$, but the numbers are $\{1, 2, 3\}$ (which is $3$ numbers). You must add $1$ because the starting element is included.  
Plugging in $\text{start} = 1$ and $\text{end} = n$:

$$\text{Iterations} = n - 1 + 1 = n$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Formulate the total execution cost equation $T(n)$</summary>
**What changed from Step 2?** We account for all machine operations executed inside and outside the loop.  
**How do we manipulate the equation?** * The initialization `int count = 0;` and `int i = 1;` execute once: $c_1$ constant operations.
* The comparison $i \le n$ executes $n$ times where it evaluates to true, plus $1$ final time where it evaluates to false ($n + 1$ times).
* The increment $i{+}{+}$ executes $n$ times.
* The loop body `count++;` executes $n$ times: $c_2 \cdot n$ operations.  
Summing these constants gives:

$$T(n) = c_2 \cdot n + c_1$$

Where $c_1$ and $c_2$ are fixed constants independent of $n$.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Express the growth rate in Big-$\Theta$ notation</summary>
**What is the final answer?** $T(n) = \Theta(n)$ (Linear Time).  
**Why does this answer make sense?** As $n$ approaches infinity, the constant addition $c_1$ becomes negligible, and the multiplier $c_2$ does not change the fact that doubling $n$ strictly doubles the operations:

$$c_2 \cdot n \le T(n) \le (c_1 + c_2) \cdot n \implies T(n) = \Theta(n)$$
</details>

</div>

---

### Problem 1.2: Single Loop with a Constant Step Size $k > 1$

**Problem Statement:** Analyze the time complexity of the following loop where the counter advances by $3$ on each step:

```c
for (int i = 0; i < n; i += 3) {
    // Basic constant time operation O(1)
    do_something();
}
```

::: callout-intuition Core Mental Model
Imagine climbing a flight of $n$ stairs, but you take $3$ steps at a time. If there are $30$ stairs, you only take $10$ strides. Increasing your step size divides the total number of actions by that step size.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Write down the explicit values of $i$ for each iteration</summary>
**What are we doing?** We trace the index $i$ as a function of the iteration number $m$ (where $m = 0, 1, 2, \dots$).  
**Why are we starting here?** Because $i$ does not increase by $1$, we must determine how quickly $i$ approaches the termination threshold $n$.  
**How do we do it?** * Iteration $0$ (start): $i_0 = 0 = 3 \times 0$
* Iteration $1$: $i_1 = 0 + 3 = 3 = 3 \times 1$
* Iteration $2$: $i_2 = 3 + 3 = 6 = 3 \times 2$
* Iteration $m$: $i_m = 3 \times m$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Solve for the stopping condition</summary>
**What changed from Step 1?** We connect the formula for $i_m$ to the loop condition $i < n$.  
**How do we do it?** The loop continues as long as $i_m < n$. The loop terminates at the very first iteration $m$ where:

$$i_m \ge n$$

Substitute our formula $i_m = 3m$:

$$3m \ge n$$

Divide both sides by $3$:

$$m \ge \frac{n}{3}$$

Because the iteration count must be an integer, the total number of iterations executed is:

$$\text{Iterations} = \left\lceil \frac{n}{3} \right\rceil$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Determine the Asymptotic Complexity</summary>
**What is the final answer?** $\Theta(n)$.  
**Why does this answer make sense?** Even though the loop takes only one-third as many iterations as Problem 1.1, $\frac{1}{3}$ is a constant multiplier:

$$\left\lceil \frac{n}{3} \right\rceil \approx \frac{1}{3} n$$

In asymptotic analysis, constant coefficients are absorbed by the definition of Big-$\Theta$:

$$\frac{1}{3}n = \Theta(n)$$
</details>

</div>

---

### Problem 1.3: Decrementing Single Loop

**Problem Statement:** Analyze the runtime of a loop that counts downwards:

```c
for (int i = n; i > 0; i--) {
    do_something();
}
```

::: callout-intuition Core Mental Model
Counting down from $10$ to $1$ during a rocket launch requires the exact same number of spoken words as counting up from $1$ to $10$. Reversing the direction of a loop does not alter the total count of steps taken.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Identify the sequence of index values</summary>
**What are we doing?** We list the descending values of $i$.  
**How do we do it?** * Start value: $i = n$.
* Decrement: $i$ decreases by $1$ after each iteration.
* Stop boundary: the loop requires $i > 0$, so the smallest value executed is $i = 1$.
* The sequence is:

$$i \in \{n, n - 1, n - 2, \dots, 2, 1\}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Count the elements in the sequence</summary>
**What changed from Step 1?** We count how many numbers are in the set $\{n, n-1, \dots, 1\}$.  
**How do we do it?** Use the inclusive boundary rule: $\text{Count} = \text{max} - \text{min} + 1$.

$$\text{Iterations} = n - 1 + 1 = n$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Asymptotic Complexity</summary>
**What is the final answer?** $\Theta(n)$.  
**Why does this answer make sense?** The loop executes exactly $n$ times. Running backwards from $n$ down to $1$ takes identical time to running forwards from $1$ up to $n$.
</details>

</div>

---

## Level 2: Nested Loops (Independent and Dependent Progressions)

In this level, we place one loop inside another. We analyze two major categories: independent loops (where the inner loop does not care about the outer loop's counter) and dependent loops (where the inner loop's boundaries change on every single cycle of the outer loop).

---

### Problem 2.1: Independent Nested Loops (Rectangular Iterations)

**Problem Statement:** Find the exact number of inner operations and the asymptotic complexity for:

```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        do_something(); // Cost: 1 unit of time
    }
}
```

::: callout-intuition Core Mental Model
Think of an egg carton with $n$ rows and $m$ columns. To inspect every slot, you walk through all $n$ rows, and on each row, you check all $m$ slots. The total number of slots checked is simply the area of the rectangle: $\text{rows} \times \text{columns} = n \times m$.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Express the total work as a nested summation</summary>
**What are we doing?** We convert nested programming loops into formal mathematical summation notation ($\sum$).  
**Why are we starting here?** Summations provide an unambiguous mathematical language that handles any nested loop structure without hand-waving.  
**How do we do it?** * The outer loop index $i$ goes from $1$ to $n$. This forms the outer sum: $\sum_{i=1}^n$.
* The inner loop index $j$ goes from $1$ to $m$. This forms the inner sum: $\sum_{j=1}^m$.
* The inner body does $1$ unit of work.

$$\text{Total Steps} = \sum_{i=1}^n \left( \sum_{j=1}^m 1 \right)$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Solve the inner summation</summary>
**What changed from Step 1?** We isolate and compute the inner sum $\sum_{j=1}^m 1$.  
**How do we manipulate the equation?** Adding the number $1$ to itself $m$ times equals $m$:

$$\sum_{j=1}^m 1 = \underbrace{1 + 1 + 1 + \dots + 1}_{m \text{ times}} = m$$

Now, substitute $m$ back into the outer sum:

$$\text{Total Steps} = \sum_{i=1}^n m$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Solve the outer summation</summary>
**What changed from Step 2?** We now evaluate $\sum_{i=1}^n m$.  
**How do we do it?** Notice that $m$ does not contain the outer variable $i$. From the perspective of $i$, $m$ is a constant.  
Adding $m$ to itself $n$ times gives:

$$\sum_{i=1}^n m = \underbrace{m + m + m + \dots + m}_{n \text{ times}} = n \cdot m$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State complexity</summary>
**What is the final answer?** $\Theta(n \cdot m)$. If $m = n$, the complexity is $\Theta(n^2)$.  
**Why does this answer make sense?** The outer loop repeats $n$ times. On each repetition, the inner loop executes completely from start to finish ($m$ times). Total iterations $= n \times m$.
</details>

</div>

---

### Problem 2.2: Dependent Triangular Nested Loop ($j$ from $1$ to $i$)

**Problem Statement:** Calculate the exact number of operations and find the Big-$\Theta$ bound for:

```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= i; j++) {
        do_something();
    }
}
```

::: callout-intuition Core Mental Model
Imagine setting up bowling pins. In row 1, you place 1 pin. In row 2, you place 2 pins. In row 3, you place 3 pins. In row $n$, you place $n$ pins. The shape formed is a triangle. Finding the total work means calculating the total number of bowling pins in that triangle: $1 + 2 + 3 + \dots + n$.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Trace iterations row by row to discover the pattern</summary>
**What are we doing?** We make a concrete execution trace table for the first few values of $i$.  
**Why are we starting here?** When the inner loop depends on the outer loop ($j \le i$), the work per row is not constant. We must see what changes at each step.  
**How do we do it?** * When $i = 1$: $j$ runs from $1$ to $1 \implies 1$ iteration.
* When $i = 2$: $j$ runs from $1$ to $2 \implies 2$ iterations.
* When $i = 3$: $j$ runs from $1$ to $3 \implies 3$ iterations.
* $\dots$
* When $i = n$: $j$ runs from $1$ to $n \implies n$ iterations.

The total iterations is the sum:

$$S = 1 + 2 + 3 + 4 + \dots + n$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Set up the mathematical summation</summary>
**What changed from Step 1?** We write the summation symbolically:

$$S = \sum_{i=1}^n \left( \sum_{j=1}^i 1 \right) = \sum_{i=1}^n i$$

**Where did this formula come from?** The inner sum $\sum_{j=1}^i 1$ evaluates to $i$ because $1$ is added $i$ times.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Derive Gauss's Formula step-by-step with zero leaps</summary>
**What are we doing?** We evaluate the sum $1 + 2 + 3 + \dots + n$ from first principles.  
**How do we do it?** Write the sum forwards:

$$S = 1 + 2 + 3 + \dots + (n - 1) + n$$

Now write the exact same sum backwards directly beneath it:

$$S = n + (n - 1) + (n - 2) + \dots + 2 + 1$$

Add the two equations together vertically, column by column:
* Column 1: $1 + n = n + 1$
* Column 2: $2 + (n - 1) = n + 1$
* Column 3: $3 + (n - 2) = n + 1$
* $\dots$
* Column $n$: $n + 1 = n + 1$

Notice that every single pair adds up to exactly $(n + 1)$!  
Because there are $n$ pairs in total:

$$S + S = 2S = n \times (n + 1)$$

Divide both sides by $2$ to solve for $S$:

$$S = \frac{n(n + 1)}{2}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Expand the polynomial algebraically</summary>
**What changed from Step 3?** We expand the formula to identify the leading term:

$$S = \frac{n^2 + n}{2} = \frac{1}{2}n^2 + \frac{1}{2}n$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Bound with Big-$\Theta$</summary>
**What is the final answer?** $\Theta(n^2)$.  
**Why does this answer make sense?** The leading term of the polynomial is $\frac{1}{2}n^2$. By the polynomial rule of asymptotic growth, lower-order terms (like $\frac{1}{2}n$) and constant coefficients (like $\frac{1}{2}$) are dominated by $n^2$ as $n \to \infty$.  
Therefore, a triangular loop runs in half the operations of a square loop, but both belong to the exact same quadratic complexity class $\Theta(n^2)$.
</details>

</div>

---

### Problem 2.3: Dependent Shrinking Nested Loop ($j$ from $i$ to $n$)

**Problem Statement:** Find the time complexity of a loop where the inner counter starts at the outer counter:

```c
for (int i = 1; i <= n; i++) {
    for (int j = i; j <= n; j++) {
        do_something();
    }
}
```

::: callout-intuition Core Mental Model
Imagine having a to-do list of $n$ tasks. On day 1, you review tasks from item 1 to $n$ ($n$ tasks). On day 2, you cross off item 1 and review tasks from item 2 to $n$ ($n - 1$ tasks). On the final day, you only review item $n$ ($1$ task). The work shrinks every day.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Count inner iterations for a fixed value of $i$</summary>
**What are we doing?** We determine how many times the inner loop runs for any given value of $i$.  
**How do we do it?** The inner loop counter $j$ goes from $\text{start} = i$ to $\text{end} = n$ inclusive.  
Using the fencepost rule:

$$\text{Inner Iterations} = \text{end} - \text{start} + 1 = n - i + 1$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Trace the values as $i$ increments</summary>
**What changed from Step 1?** We see the specific numbers generated:
* For $i = 1$: $n - 1 + 1 = n$
* For $i = 2$: $n - 2 + 1 = n - 1$
* For $i = 3$: $n - 3 + 1 = n - 2$
* $\dots$
* For $i = n$: $n - n + 1 = 1$

The total work is:

$$S = n + (n - 1) + (n - 2) + \dots + 2 + 1$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Recognize the reversed sum</summary>
**What changed from Step 2?** Notice that the sum $n + (n - 1) + \dots + 1$ is identical to $1 + 2 + \dots + n$.  
**How do we manipulate the equation?** Addition is commutative ($a + b = b + a$). Reversing the order gives Gauss's sum:

$$S = \sum_{k=1}^n k = \frac{n(n + 1)}{2} = \frac{1}{2}n^2 + \frac{1}{2}n$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Conclude Complexity</summary>
**What is the final answer?** $\Theta(n^2)$.  
**Why does this answer make sense?** Whether a triangular nested loop grows from $1$ up to $n$ (Problem 2.2) or shrinks from $n$ down to $1$ (Problem 2.3), the total number of operations is identical: $\frac{n(n+1)}{2}$.
</details>

</div>

---

## Level 3: Non-Linear Loops (Logarithmic Steps, Powers, and Square Roots)

In this level, the loop counter does not increase by a constant addition. Instead, it multiplies, divides, or relies on non-linear stopping conditions.

---

### Problem 3.1: Logarithmic Multiplicative Loop ($i = i \times 2$)

**Problem Statement:** Find the exact number of iterations and the asymptotic complexity for:

```c
for (int i = 1; i < n; i = i * 2) {
    do_something();
}
```

::: callout-intuition Core Mental Model
Imagine folding a sheet of paper in half over and over. With each fold, the thickness doubles: 1 layer, 2 layers, 4 layers, 8, 16, 32... Because the quantity doubles every step, it shoots up with extreme speed. To reach a height of $n$, you need very few folds—only $\log_2(n)$ folds.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Track the value of $i$ across iterations</summary>
**What are we doing?** We express the value of $i$ at iteration number $k$ (starting at $k = 0$).  
**Why are we starting here?** Multiplicative patterns generate powers. We must find the mathematical relation between iteration number $k$ and the value of $i$.  
**How do we do it?**
* At iteration $k = 0$: $i_0 = 1 = 2^0$
* At iteration $k = 1$: $i_1 = 1 \times 2 = 2 = 2^1$
* At iteration $k = 2$: $i_2 = 2 \times 2 = 4 = 2^2$
* At iteration $k = 3$: $i_3 = 4 \times 2 = 8 = 2^3$
* At iteration $k$: $i_k = 2^k$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Determine when the loop stops</summary>
**What changed from Step 1?** We relate the formula $i_k = 2^k$ to the loop condition $i < n$.  
**How do we do it?** The loop keeps running while $i < n$. It stops at the very first iteration $k$ where:

$$i_k \ge n$$

Substitute $i_k = 2^k$:

$$2^k \ge n$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Solve for $k$ using logarithms</summary>
**What changed from Step 2?** We need to isolate $k$, which is currently trapped in the exponent of $2^k$.  
**How do we do it?** Take the base-2 logarithm ($\log_2$) of both sides of the equation $2^k = n$:

$$\log_2(2^k) = \log_2(n)$$

**Where did this rule come from?** The definition of a logarithm: $\log_b(b^x) = x$.  
Applying this rule to the left-hand side:

$$k = \log_2(n)$$

Since iterations occur at integer boundaries, the total number of iterations is:

$$k = \lceil \log_2(n) \rceil$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Asymptotic Complexity</summary>
**What is the final answer?** $\Theta(\log n)$.  
**Why does this answer make sense?** Let us test real numbers:
* If $n = 8$: $i$ takes values $\{1, 2, 4\}$, which is $3 = \log_2(8)$ iterations.
* If $n = 1024$: $i$ takes values $\{1, 2, 4, 8, \dots, 512\}$, which is only $10 = \log_2(1024)$ iterations!
* If $n = 1{,}000{,}000$: the loop finishes in approximately $20$ iterations.

Because doubling the problem size only adds $1$ single extra step to the loop, its growth rate is purely logarithmic: $\Theta(\log n)$.
</details>

</div>

---

### Problem 3.2: Division Loop (Halving down to 1)

**Problem Statement:** Analyze the runtime of a loop that repeatedly divides its counter by 2:

```c
for (int i = n; i >= 1; i = i / 2) {
    do_something();
}
```

::: callout-intuition Core Mental Model
Imagine cutting a rope of length $n$ in half, then cutting the remainder in half, until the piece left is smaller than 1 unit. This is the exact reverse of the folding problem: halving down to 1 takes the exact same number of steps as doubling up from 1 to $n$.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Track the value of $i$ across iterations</summary>
**What are we doing?** We express the value of $i$ at iteration $k$ (with $k = 0$ as the first iteration).  
**How do we do it?**
* Iteration $k = 0$: $i_0 = n = \frac{n}{2^0}$
* Iteration $k = 1$: $i_1 = \frac{n}{2} = \frac{n}{2^1}$
* Iteration $k = 2$: $i_2 = \frac{n/2}{2} = \frac{n}{4} = \frac{n}{2^2}$
* Iteration $k$: $i_k = \frac{n}{2^k}$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Solve the termination condition</summary>
**What changed from Step 1?** The loop condition is $i \ge 1$. The loop terminates as soon as $i < 1$.  
**How do we do it?** Set $i_k < 1$:

$$\frac{n}{2^k} < 1$$

Multiply both sides by $2^k$:

$$n < 2^k \iff 2^k > n$$

Take $\log_2$ of both sides:

$$k > \log_2(n) \implies k = \lfloor \log_2(n) \rfloor + 1$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Asymptotic Complexity</summary>
**What is the final answer?** $\Theta(\log n)$.  
**Why does this answer make sense?** Repeated division by a constant factor $b > 1$ reduces the number to $1$ in $\log_b(n)$ steps. Thus, repeated halving takes $\Theta(\log n)$ time.
</details>

</div>

---

### Problem 3.3: Square Root Loop Condition ($i \times i \le n$)

**Problem Statement:** Analyze the time complexity of the following primality-style check loop:

```c
for (int i = 1; i * i <= n; i++) {
    do_something();
}
```

::: callout-intuition Core Mental Model
Imagine building square tiles of size $i \times i$ on the floor. At $i = 1$, the tile area is $1$. At $i = 2$, the area is $4$. At $i = 10$, the area is $100$. If your budget of floor space is $n$, you can only increase $i$ until the square tile's area $i^2$ exceeds the total space $n$. How many tiles can you build? Exactly $\sqrt{n}$ tiles.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Analyze the loop condition algebraically</summary>
**What are we doing?** We rewrite the loop condition $i \cdot i \le n$ to isolate the loop variable $i$.  
**Why are we starting here?** The loop increases $i$ by $1$ each time ($i{+}{+}$). Therefore, if we know the maximum numerical value $i$ can reach, that maximum directly tells us the number of iterations!  
**How do we do it?**
The loop condition is:

$$i^2 \le n$$

Take the principal (positive) square root $\sqrt{\phantom{x}}$ on both sides:

$$\sqrt{i^2} \le \sqrt{n}$$

Since $i \ge 1$ is always positive, $\sqrt{i^2} = i$:

$$i \le \sqrt{n}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Count the iterations from start to stop</summary>
**What changed from Step 1?** We now have the loop written in standard form: $i$ starts at $1$, increments by $1$, and stops when $i > \sqrt{n}$.  
**How do we do it?**
The values taken by $i$ are:

$$i \in \{1, 2, 3, \dots, \lfloor \sqrt{n} \rfloor\}$$

Using our counting formula $\text{end} - \text{start} + 1$:

$$\text{Iterations} = \lfloor \sqrt{n} \rfloor - 1 + 1 = \lfloor \sqrt{n} \rfloor$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Asymptotic Complexity</summary>
**What is the final answer?** $\Theta(\sqrt{n})$.  
**Why does this answer make sense?** * If $n = 100$: the loop stops when $i^2 > 100$, which happens when $i = 11$. The loop runs for $i \in \{1, 2, \dots, 10\}$, exactly $10 = \sqrt{100}$ iterations.
* If $n = 10{,}000$: the loop runs $100 = \sqrt{10{,}000}$ iterations.

Because the number of steps is directly bounded by $\sqrt{n}$, the complexity is $\Theta(\sqrt{n})$.
</details>

</div>

---

### Problem 3.4: Mixed Linear-Logarithmic Nested Loop ($n \log n$)

**Problem Statement:** Analyze the time complexity of the following nested loop combination:

```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j < n; j = j * 2) {
        do_something();
    }
}
```

::: callout-intuition Core Mental Model
Imagine an instructor teaching a school of $n$ students. The instructor visits each student one by one ($n$ outer visits). During each visit, the instructor plays a game that halves the board until a winner is chosen ($\log_2 n$ inner rounds). The total rounds played across all students is the number of visits multiplied by the rounds per visit: $n \times \log_2 n$.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Analyze the independence of the inner loop</summary>
**What are we doing?** We check whether the inner loop's start, stop, or step conditions depend on the outer variable $i$.  
**Why are we starting here?** If the inner loop is independent of $i$, its work is identical on every single iteration of the outer loop.  
**How do we do it?**
* The inner loop initializes at $j = 1$.
* The inner loop terminates when $j \ge n$.
* The inner loop advances by $j = j \times 2$.
* Notice that $i$ does not appear anywhere in the inner loop header.
* Therefore, the inner loop is completely independent of $i$.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Calculate the work per single outer iteration</summary>
**What changed from Step 1?** We compute the cost of one pass of the inner loop using the result from Problem 3.1.  
**How do we do it?** From Problem 3.1, a loop starting at $1$, doubling each time, and stopping at $n$ executes:

$$\text{Inner Iterations} = \lceil \log_2 n \rceil$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Multiply by the number of outer iterations</summary>
**What changed from Step 2?** We sum the inner work across all iterations of the outer loop.  
**How do we do it?**
The outer loop runs for $i = 1$ to $n$, which is $n$ iterations.  
Using summation notation:

$$\text{Total Work} = \sum_{i=1}^n \left( \sum_{k=0}^{\lceil \log_2 n \rceil - 1} 1 \right) = \sum_{i=1}^n \lceil \log_2 n \rceil$$

Since $\lceil \log_2 n \rceil$ does not depend on $i$, we factor it out:

$$\text{Total Work} = \lceil \log_2 n \rceil \times \left( \sum_{i=1}^n 1 \right) = n \cdot \lceil \log_2 n \rceil$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: State Asymptotic Complexity</summary>
**What is the final answer?** $\Theta(n \log n)$.  
**Why does this answer make sense?** The outer loop contributes a linear factor $n$. The inner loop contributes a logarithmic factor $\log n$. Multiplying independent components yields $\Theta(n \log n)$.
</details>

</div>
