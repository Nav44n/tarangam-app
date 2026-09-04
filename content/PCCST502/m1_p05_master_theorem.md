# Progressive Problems: The Master Theorem for Divide-and-Conquer Recurrences

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic high-school arithmetic and logarithms.

---

## The Master Theorem Blueprint: The Ultimate Tug-of-War

The Master Theorem is a shortcut cookbook for solving divide-and-conquer recurrences of the standard form:

$$T(n) = a \cdot T\left(\frac{n}{b}\right) + f(n)$$

Where:
* $a \ge 1$: The number of subproblems spawned at each step (branching factor).
* $b > 1$: The factor by which the input size is divided (shrink factor).
* $f(n)$: The cost of splitting the problem and merging the subproblem solutions (root / non-recursive work).

### The Battle Between Two Functions
Every divide-and-conquer algorithm is a tug-of-war between two opposing forces:
1. **The Leaf Force (Subproblem Explosion):**
   The total work done exclusively by the base-case leaves at the bottom of the tree is:
   $$\text{Leaf Work} = \Theta\left(n^{\log_b a}\right)$$
   We call the exponent $p = \log_b a$ the **Critical Exponent**.
2. **The Root Force (Divide/Combine Work):**
   The non-recursive work done at the top is:
   $$\text{Root Work} = f(n)$$

The Master Theorem simply compares these two quantities:
* **Case 1 (Leaves Win):** If $n^{\log_b a}$ is polynomially larger than $f(n)$ by a factor of $n^\epsilon$ ($\epsilon > 0$), then $T(n) = \Theta\left(n^{\log_b a}\right)$.
* **Case 2 (A Tie / Balanced Work):** If $n^{\log_b a}$ and $f(n)$ grow at the exact same rate, the work is evenly distributed across all levels. Then $T(n) = \Theta\left(n^{\log_b a} \log_2 n\right)$.
* **Case 3 (Root Wins):** If $f(n)$ is polynomially larger than $n^{\log_b a}$ by a factor of $n^\epsilon$ ($\epsilon > 0$), and satisfies a regularity condition, then $T(n) = \Theta(f(n))$.

---

## Level 1: Case 1 (The Leaves Dominate)

In this level, the number of subproblems grows so fast that the leaves do overwhelmingly more work than the root.

---

### Problem 1.1: Classic Case 1: $T(n) = 4T(n/2) + n$

**Problem Statement:** Find the asymptotic bound for the recurrence:

$$T(n) = 4T(n/2) + n$$

::: callout-intuition Core Mental Model
Imagine a bacterial colony where each parent cell splits into 4 child cells, but the resources per cell only shrink by half. The population explodes exponentially downwards. By the time you reach the bottom generation, there are so many leaves that the work done at the leaves completely drowns out the tiny work $n$ done at the top.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Extract the parameters $a$, $b$, and $f(n)$</div>
**What are we doing?** We match our given recurrence against the template $T(n) = a T(n/b) + f(n)$.  
**Why are we starting here?** We cannot calculate any exponents until we correctly identify the components.  
**How do we do it?** * $a = 4$ (there are $4$ subproblems).
* $b = 2$ (the input size $n$ is divided by $2$).
* $f(n) = n$ (the outside additive work).
* Check validity: $a \ge 1$ ($4 \ge 1$) and $b > 1$ ($2 > 1$). The standard form is satisfied.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Calculate the Critical Exponent and the Leaf Work $n^{\log_b a}$</div>
**What are we doing?** We evaluate the expression $n^{\log_b a}$ step by step.  
**Why are we doing this?** This quantity represents the total computational weight of the base-case leaves.  
**How do we do it?** Substitute $a = 4$ and $b = 2$:

$$\log_b a = \log_2 4$$

**Where did this logarithm value come from?** The question asks: "2 raised to what power equals 4?"  
Since $2^2 = 4$, we have:

$$\log_2 4 = 2$$

Now, put this exponent on $n$:

$$n^{\log_b a} = n^2$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Compare $f(n)$ with $n^{\log_b a}$</div>
**What changed from Step 2?** We now compare our two competing forces:
* Root Work: $f(n) = n = n^1$
* Leaf Work: $n^{\log_b a} = n^2$

**How do we compare them?** We check if $n^{\log_b a}$ is **polynomially larger** than $f(n)$.  
This means we must find a positive number $\epsilon > 0$ such that:

$$f(n) = O\left(n^{\log_b a - \epsilon}\right)$$

Substitute our values:

$$n^1 \le n^{2 - \epsilon}$$

Set the exponents equal to find $\epsilon$:

$$1 = 2 - \epsilon \implies \epsilon = 2 - 1 = 1$$

Since $\epsilon = 1 > 0$, $f(n)$ is indeed polynomially smaller than $n^2$ by a factor of $n^1$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Apply Case 1 and State Conclusion</div>
**What is the final answer?** $T(n) = \Theta(n^2)$.  
**Why does this answer make sense?** The leaves do $\Theta(n^2)$ work while the root only does $\Theta(n)$ work. Because the leaves dominate, the total complexity is dictated entirely by the leaves:

$$T(n) = \Theta\left(n^{\log_b a}\right) = \Theta(n^2)$$
</div>

</div>

---

### Problem 1.2: Deceptive Constant Trap: $T(n) = 8T(n/2) + 1000n^2$

**Problem Statement:** Find the asymptotic complexity of:

$$T(n) = 8T(n/2) + 1000n^2$$

::: callout-intuition Core Mental Model
A beginner looks at $1000n^2$ and thinks: "A thousand is huge! The root must dominate!" But in asymptotic analysis, constant coefficients are completely powerless against higher polynomial powers as $n \to \infty$. A tiny leaf power of $n^3$ will eventually crush $1000n^2$ into absolute insignificance.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Extract parameters</div>
**What are we doing?** Identify the values from the recurrence.  
**How do we do it?** * $a = 8$
* $b = 2$
* $f(n) = 1000n^2$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Calculate the Leaf Work $n^{\log_b a}$</div>
**What changed from Step 1?** Calculate the critical exponent:

$$\log_b a = \log_2 8$$

Since $2^3 = 8$, we have $\log_2 8 = 3$.  
Therefore:

$$n^{\log_b a} = n^3$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Compare $f(n) = 1000n^2$ against $n^3$</div>
**What are we doing?** We check for a polynomial gap between $1000n^2$ and $n^3$.  
**How do we do it?** In Big-$O$ notation, constant coefficients like $1000$ are dropped: $f(n) = 1000n^2 = O(n^2)$.  
We test:

$$f(n) = O\left(n^{3 - \epsilon}\right)$$

Setting $2 = 3 - \epsilon$ gives:

$$\epsilon = 1 > 0$$

Because $\epsilon = 1$ is strictly positive, $f(n)$ is polynomially smaller than the leaf work $n^3$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: State Conclusion</div>
**What is the final answer?** $T(n) = \Theta(n^3)$.  
**Why does this answer make sense?** No matter how large the constant $1000$ is, when $n = 10{,}000$, $n^3 = 10^{12}$ while $1000n^2 = 10^{11}$. The leaves overtake the root and win decisively.
</div>

</div>

---

## Level 2: Case 2 (The Balanced Tie)

In this level, the work done at the root is asymptotically equal to the work done at the leaves. The work is distributed evenly across all horizontal levels of the recursion tree.

---

### Problem 2.1: Classic Case 2 (Merge Sort): $T(n) = 2T(n/2) + n$

**Problem Statement:** Solve the recurrence:

$$T(n) = 2T(n/2) + n$$

::: callout-intuition Core Mental Model
Think of a multi-story building where every single floor has exactly the same number of offices. If each floor does $n$ work, you simply calculate: (work per floor) $\times$ (number of floors). The number of floors in a binary tree is $\log_2 n$. Multiplying them gives $n \log_2 n$.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Extract parameters</div>
**What are we doing?** We identify $a$, $b$, and $f(n)$.  
**How do we do it?** * $a = 2$
* $b = 2$
* $f(n) = n$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Calculate the Leaf Work $n^{\log_b a}$</div>
**What changed from Step 1?** Compute the critical exponent:

$$\log_b a = \log_2 2 = 1$$

Therefore:

$$n^{\log_b a} = n^1 = n$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Compare $f(n)$ and $n^{\log_b a}$</div>
**What are we doing?** We compare Root Work $f(n) = n$ with Leaf Work $n^{\log_b a} = n$.  
**How do we do it?** Notice that both sides are identical:

$$f(n) = \Theta\left(n^{\log_b a}\right) \implies n = \Theta(n)$$

There is no polynomial gap. Neither side dominates. This is an exact tie.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Apply Case 2 Formula and Conclude</div>
**What is the final answer?** $T(n) = \Theta(n \log_2 n)$.  
**Why does this answer make sense?** Under Case 2 of the Master Theorem:

$$T(n) = \Theta\left(n^{\log_b a} \log_2 n\right)$$

Since $n^{\log_b a} = n$, we multiply by the tree depth factor $\log_2 n$:

$$T(n) = \Theta(n \log_2 n)$$
</div>

</div>

---

### Problem 2.2: Extended Case 2 with Polylogarithmic Factors: $T(n) = 2T(n/2) + n \log_2 n$

**Problem Statement:** Find the tight bound for:

$$T(n) = 2T(n/2) + n \log_2 n$$

::: callout-intuition Core Mental Model
Here, the root does slightly more than $n$ because of the extra $\log_2 n$ factor. But a logarithm is not a polynomial power ($n^{0.001}$ eventually beats any $\log n$). Because the difference is merely logarithmic rather than polynomial, it still falls under the balanced "tie" family, but each level of the tree accumulates an additional log factor.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Extract parameters and calculate critical exponent</div>
**What are we doing?** * $a = 2$, $b = 2 \implies \log_b a = \log_2 2 = 1$.
* Leaf Work: $n^{\log_b a} = n^1 = n$.
* Root Work: $f(n) = n \log_2 n$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Recognize the Extended Case 2 Template</div>
**What changed from Step 1?** We test if $f(n)$ matches the generalized Case 2 form:

$$f(n) = \Theta\left(n^{\log_b a} \cdot \log^k n\right) \quad \text{for some } k \ge 0$$

**How do we check this?** Here, $n^{\log_b a} = n$, so:

$$f(n) = n \cdot \log_2^1 n$$

This matches the template with $k = 1$!
</div>

<div class="step-card">
<div class="step-badge">Final Step: Apply the Extended Case 2 Formula</div>
**What is the final answer?** $T(n) = \Theta(n \log_2^2 n)$.  
**Where did this formula come from?** When $f(n) = \Theta(n^{\log_b a} \log^k n)$, the solution is:

$$T(n) = \Theta\left(n^{\log_b a} \cdot \log^{k + 1} n\right)$$

Plugging in $n^{\log_b a} = n$ and $k = 1$:

$$T(n) = \Theta\left(n \log^{1 + 1} n\right) = \Theta(n \log^2 n)$$
</div>

</div>

---

## Level 3: Case 3 (The Root Dominates & The Regularity Condition)

In this level, the work done at the root is polynomially larger than the leaf work. However, there is a mandatory second hurdle: we must verify the **Regularity Condition** to prove that subproblems shrink smoothly without surging at deeper levels.

---

### Problem 3.1: Root-Dominated Recurrence with Regularity Check: $T(n) = 3T(n/4) + n^2$

**Problem Statement:** Solve using the Master Theorem:

$$T(n) = 3T(n/4) + n^2$$

::: callout-intuition Core Mental Model
Imagine a pyramid where the top stone accounts for 90% of the entire pyramid's weight, and every lower layer is drastically lighter. The root work $n^2$ shrinks by a factor of 16 when $n$ is divided by 4, completely overwhelming the fact that there are 3 children. The root wins effortlessly.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Extract parameters and compute leaf exponent</div>
**What are we doing?** We extract $a = 3$, $b = 4$, and $f(n) = n^2$.  
**How do we calculate the exponent?** $$\log_b a = \log_4 3$$

Since $4^0 = 1$ and $4^1 = 4$, $\log_4 3$ must be a decimal between $0$ and $1$.  
Using the base-change formula:

$$\log_4 3 = \frac{\ln 3}{\ln 4} \approx \frac{1.0986}{1.3863} \approx 0.7925$$

So the leaf work is:

$$n^{\log_b a} = n^{0.7925}$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Check for a Polynomial Gap (Case 3 condition)</div>
**What changed from Step 1?** We compare $f(n) = n^2$ against $n^{0.7925}$.  
**How do we do it?** We must find $\epsilon > 0$ such that:

$$f(n) = \Omega\left(n^{\log_b a + \epsilon}\right)$$

Substitute:

$$n^2 \ge n^{0.7925 + \epsilon}$$

Solve for $\epsilon$:

$$2 = 0.7925 + \epsilon \implies \epsilon = 2 - 0.7925 = 1.2075 > 0$$

Because $\epsilon \approx 1.21 > 0$, $f(n)$ is polynomially larger than the leaf work.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Verify the Regularity Condition</div>
**What are we doing?** We must prove that the children's combined non-recursive work is strictly smaller than the parent's work.  
**Why are we doing this?** If an unusual function $f(n)$ oscillates or surges unpredictably at smaller sizes, Case 3 can give a false answer. The Regularity Condition guarantees stability.  
**Where did this formula come from?** The definition of the Regularity Condition requires finding a constant $c < 1$ such that for all sufficiently large $n$:

$$a \cdot f\left(\frac{n}{b}\right) \le c \cdot f(n)$$

Substitute our specific values ($a = 3$, $b = 4$, and $f(n) = n^2$):

$$3 \cdot f\left(\frac{n}{4}\right) \le c \cdot n^2$$

Since $f(k) = k^2$, evaluate $f(n/4)$:

$$f\left(\frac{n}{4}\right) = \left(\frac{n}{4}\right)^2 = \frac{n^2}{16}$$

Substitute this back into the left-hand side:

$$3 \cdot \left(\frac{n^2}{16}\right) = \frac{3}{16} n^2$$

Now compare against $c \cdot n^2$:

$$\frac{3}{16} n^2 \le c \cdot n^2$$

Divide both sides by $n^2$:

$$\frac{3}{16} \le c$$

Can we choose a constant $c < 1$?  
Yes! We can choose $c = \frac{3}{16} = 0.1875 < 1$.  
The Regularity Condition is satisfied!
</div>

<div class="step-card">
<div class="step-badge">Final Step: State Conclusion</div>
**What is the final answer?** $T(n) = \Theta(n^2)$.  
**Why does this answer make sense?** The root does $\Theta(n^2)$ work, the lower levels shrink geometrically by a factor of $\frac{3}{16}$, and the regularity test confirms total stability. Thus, the root dominates:

$$T(n) = \Theta(f(n)) = \Theta(n^2)$$
</div>

</div>

---

## Level 4: The Traps (When the Master Theorem CANNOT Be Applied)

Not all divide-and-conquer recurrences can be solved with the Master Theorem. In this level, we identify the exact reasons why the Master Theorem fails and how to recognize these traps on exams.

---

### Problem 4.1: The Non-Polynomial Gap Trap: $T(n) = 2T(n/2) + \frac{n}{\log_2 n}$

**Problem Statement:** Explain why the Master Theorem cannot solve:

$$T(n) = 2T(n/2) + \frac{n}{\log_2 n}$$

::: callout-intuition Core Mental Model
Imagine two runners finishing a race just one millimeter apart. One runner is technically ahead, but the gap is so microscopic that neither runner can be declared the definitive dominant winner. The Master Theorem requires a decisive "polynomial gap" ($n^\epsilon$). A logarithmic difference is not a polynomial gap; it falls into the crack between Case 1 and Case 2.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Extract parameters and compute leaf exponent</div>
**What are we doing?** * $a = 2$, $b = 2$.
* Critical exponent: $\log_b a = \log_2 2 = 1$.
* Leaf Work: $n^{\log_b a} = n^1 = n$.
* Root Work: $f(n) = \frac{n}{\log_2 n} = n \cdot (\log_2 n)^{-1}$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Test Case 1 (Is there a polynomial gap?)</div>
**What changed from Step 1?** Notice that $f(n) = \frac{n}{\log_2 n}$ is smaller than $n^{\log_b a} = n$.  
So a beginner might guess **Case 1**. Let us test the mathematical requirement for Case 1:

$$f(n) = O\left(n^{\log_b a - \epsilon}\right) \iff \frac{n}{\log_2 n} \le c \cdot n^{1 - \epsilon} \quad \text{for some } \epsilon > 0$$

Divide both sides by $n$:

$$\frac{1}{\log_2 n} \le c \cdot \frac{n^{1 - \epsilon}}{n} = c \cdot n^{-\epsilon} = \frac{c}{n^\epsilon}$$

Invert both sides:

$$\log_2 n \ge \frac{n^\epsilon}{c}$$

**Where does this fail?** For ANY positive constant $\epsilon > 0$ (even $\epsilon = 0.0001$), any polynomial power $n^\epsilon$ grows strictly faster than $\log_2 n$ as $n \to \infty$.  
Therefore, $\log_2 n$ can NEVER be greater than or equal to a positive power of $n$ for large $n$.  
There is **NO valid $\epsilon > 0$**! The gap between $n$ and $\frac{n}{\log n}$ is purely logarithmic, not polynomial.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Test Case 2 (Is it a tie?)</div>
**What changed from Step 2?** Can it be Case 2?  
Case 2 requires $f(n) = \Theta(n^{\log_b a} \log^k n)$ with $k \ge 0$.  
Here, our power of log is negative: $k = -1$ (since $\frac{1}{\log n} = \log^{-1} n$).  
The standard Master Theorem explicitly requires $k \ge 0$. It does not apply to $k = -1$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: State Why the Master Theorem Fails and How to Solve It</div>
**What is the final answer?** The Master Theorem **cannot be applied** because $f(n)$ falls into the non-polynomial gap between Case 1 and Case 2.  
**How should it actually be solved?** It must be solved using a **Recursion Tree**:
* Tree height: $h = \log_2 n$.
* Cost at level $i$: $\frac{n}{\log_2(n / 2^i)} = \frac{n}{\log_2 n - i}$.
* Summing this series yields $T(n) = \Theta(n \log \log n)$.
</div>

</div>

---

### Problem 4.2: Summary Checklist: When Does the Master Theorem Fail?

**Problem Statement:** What are the 4 fundamental conditions where the Master Theorem is completely invalid?

::: callout-intuition Core Mental Model
The Master Theorem is like an automatic transmission in a car. It only works on standard paved roads. If the road has uneven ruts (non-constant coefficients), changes slopes randomly (non-dividing steps), or oscillates wildly (trigonometric terms), the automatic transmission stalls, and you must switch to manual transmission (Recursion Tree or Substitution).
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Trap 1: The Branching Factor $a$ is Not Constant</div>
**Example:** $T(n) = 2^n T(n/2) + n$.  
**Why it fails:** The parameter $a$ must be a fixed, constant positive number. Here, $a(n) = 2^n$ is a function of $n$, not a constant.
</div>

<div class="step-card">
<div class="step-badge">Trap 2: The Shrink Factor $b$ is Subtractive, Not Divisive</div>
**Example:** $T(n) = 2T(n - 1) + 1$.  
**Why it fails:** The Master Theorem requires dividing the input size by a constant ($n/b$). Here, the size shrinks by subtraction ($n - 1$). This recurrence is an exponential linear recurrence ($O(2^n)$), not divide-and-conquer.
</div>

<div class="step-card">
<div class="step-badge">Trap 3: The Gap is Not Polynomial</div>
**Example:** $T(n) = 2T(n/2) + n \log \log n$.  
**Why it fails:** $n \log \log n$ is strictly larger than $n$, but NOT by a factor of $n^\epsilon$ for any $\epsilon > 0$. It falls into the crack between Case 2 and Case 3.
</div>

<div class="step-card">
<div class="step-badge">Trap 4: Failure of the Regularity Condition in Case 3</div>
**Example:** $T(n) = T(n/2) + n(2 - \cos n)$.  
**Why it fails:** Here $a = 1$, $b = 2$, and $n^{\log_2 1} = n^0 = 1$. The function $f(n) = n(2 - \cos n) = \Omega(n^1)$, so it looks like Case 3. However, because $\cos n$ oscillates infinitely between $-1$ and $+1$, the inequality $a f(n/b) \le c f(n)$ cannot hold for any fixed constant $c < 1$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Diagnostic Flowchart for Any Recurrence</div>
**What is the final rule of thumb?**
1. Check: Is it $T(n) = aT(n/b) + f(n)$ with constant $a \ge 1, b > 1$? If no $\to$ Use Recursion Tree or Substitution.
2. Compute $p = \log_b a$.
3. Compare $n^p$ with $f(n)$:
   * $n^p \gg f(n)$ by $n^\epsilon \implies$ **Case 1:** $\Theta(n^p)$.
   * $n^p \approx f(n)$ (equal up to $\log^k n$) $\implies$ **Case 2:** $\Theta(n^p \log^{k+1} n)$.
   * $f(n) \gg n^p$ by $n^\epsilon$ AND $a f(n/b) \le c f(n) \implies$ **Case 3:** $\Theta(f(n))$.
   * Gap is non-polynomial or regularity fails $\to$ Master Theorem fails; use Recursion Tree!
</div>

</div>
