# Progressive Problems: Asymptotic Notations (Big-O, Big-$\Omega$, Big-$\Theta$)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic high-school arithmetic and algebra.

---

## Level 1: Linear Polynomials & The Formal Definitions

In this level, we introduce the formal mathematical definitions of asymptotic bounds using the simplest possible functions: straight lines (linear functions of the form $a \cdot n + b$).

---

### Problem 1.1: Prove an Upper Bound (Big-O) for a Linear Function

**Problem Statement:** Using the formal definition of Big-$O$, prove that:

$$f(n) = 3n + 8 = O(n)$$

::: callout-intuition Core Mental Model
Think of Big-$O$ as an adjustable "ceiling" or "speed limit". We want to find a simple multiplier $c$ such that the line $c \cdot n$ stays higher than our actual function $3n + 8$ forever, once $n$ gets past some starting point $n_0$. Since $3n + 8$ grows at a steady linear rate, scaling $n$ by a slightly larger number (like $11$) will easily keep it above $3n + 8$.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Write down the formal mathematical definition</div>
**What are we doing?** We write down the target inequality we must satisfy to prove Big-$O$.  
**Why are we starting here?** A mathematical proof requires a clear target. We cannot claim a statement is true until we know the precise conditions that define truth.  
**How do we do it?** We plug our specific functions $f(n) = 3n + 8$ and $g(n) = n$ into the definition of Big-$O$.  
**Where did this formula/concept come from?** The standard definition of Big-$O$: $f(n) = O(g(n))$ means there exist two positive constants $c > 0$ and $n_0 \ge 1$ such that for all integers $n \ge n_0$:

$$0 \le f(n) \le c \cdot g(n)$$

Plugging in our functions gives:

$$0 \le 3n + 8 \le c \cdot n \quad \text{for all } n \ge n_0$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Replace the loose constant term with a term in $n$</div>
**What changed from Step 1?** We need to simplify $3n + 8$ into a single term of the form $(\text{number}) \cdot n$. Right now, the $+ 8$ has no $n$ attached to it, making it hard to compare directly with $c \cdot n$.  
**Why are we starting here?** If every term in the expression has $n$ attached, we can combine like terms using simple addition.  
**How do we do it?** Notice what happens when $n \ge 1$:
* If $n = 1$, then $8 \cdot n = 8 \cdot 1 = 8$.
* If $n = 2$, then $8 \cdot n = 8 \cdot 2 = 16$, which is strictly greater than $8$.
* Therefore, as long as $n \ge 1$, it is always true that:

$$8 \le 8n$$

Now, replace the standalone $+ 8$ with the larger quantity $+ 8n$:

$$3n + 8 \le 3n + 8n$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Combine like terms algebraically</div>
**What changed from Step 2?** We now have two terms that both contain $n$, so we can add their coefficients.  
**How do we manipulate the equation?** Apply the distributive law: $3n + 8n = (3 + 8)n = 11n$.

$$3n + 8 \le 11n$$

This inequality is guaranteed to be true for all $n \ge 1$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Identify the witnesses $(c, n_0)$ and state the conclusion</div>
**What is the final answer?** We choose $c = 11$ and $n_0 = 1$.  
**Why does this answer make sense?** * Checking $n = 1$: $f(1) = 3(1) + 8 = 11$. Upper bound: $11(1) = 11$. ($11 \le 11$ holds).
* Checking $n = 2$: $f(2) = 3(2) + 8 = 14$. Upper bound: $11(2) = 22$. ($14 \le 22$ holds).
* Checking $n = 10$: $f(10) = 3(10) + 8 = 38$. Upper bound: $11(10) = 110$. ($38 \le 110$ holds).

Because we found specific positive constants $c = 11$ and $n_0 = 1$ where $3n + 8 \le c \cdot n$ holds for every $n \ge n_0$, the proof is complete:

$$3n + 8 = O(n)$$
</div>

</div>

---

### Problem 1.2: Prove a Lower Bound (Big-$\Omega$) for a Linear Function

**Problem Statement:** Using the formal definition of Big-$\Omega$, prove that:

$$f(n) = 3n + 8 = \Omega(n)$$

::: callout-intuition Core Mental Model
Big-$\Omega$ is a "floor" or "safety net". We want to show that our function never drops below a scaled version of $g(n) = n$. Since $3n + 8$ is always strictly larger than $3n$ (because $+8$ is a positive quantity), finding a floor is as simple as ignoring the $+8$.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Write down the formal mathematical definition</div>
**What are we doing?** We write down the exact inequality required for Big-$\Omega$.  
**Why are we starting here?** Big-$\Omega$ flips the inequality direction compared to Big-$O$. We must establish our target before doing algebra.  
**How do we do it?** State the definition: $f(n) = \Omega(g(n))$ means there exist positive constants $c > 0$ and $n_0 \ge 1$ such that:

$$f(n) \ge c \cdot g(n) \quad \text{for all } n \ge n_0$$

Plugging in $f(n) = 3n + 8$ and $g(n) = n$:

$$3n + 8 \ge c \cdot n \quad \text{for all } n \ge n_0$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Drop the positive constant term</div>
**What changed from Step 1?** We observe the standalone $+ 8$.  
**Why are we starting here?** When trying to make an expression *smaller* (to establish a lower floor), removing a positive number makes the expression smaller.  
**How do we do it?** Because $8 > 0$, subtracting $8$ leaves us with a strictly smaller value:

$$3n + 8 > 3n$$

Therefore, for all $n \ge 1$:

$$3n + 8 \ge 3n$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Extract the constants and verify</div>
**What is the final answer?** We choose $c = 3$ and $n_0 = 1$.  
**Why does this answer make sense?** * At $n = 1$: $3(1) + 8 = 11 \ge 3(1) = 3$.
* At $n = 5$: $3(5) + 8 = 23 \ge 3(5) = 15$.

The function $3n + 8$ will always stay above the floor $3n$. Thus, with $c = 3$ and $n_0 = 1$:

$$3n + 8 = \Omega(n)$$
</div>

</div>

---

### Problem 1.3: Prove a Tight Bound (Big-$\Theta$) for a Linear Function

**Problem Statement:** Using the formal definition of Big-$\Theta$, prove that:

$$f(n) = 3n + 8 = \Theta(n)$$

::: callout-intuition Core Mental Model
Big-$\Theta$ is a "sandwich". A function is $\Theta(g(n))$ if it can be trapped between two constant multiples of $g(n)$—a lower floor $c_1 \cdot g(n)$ and an upper ceiling $c_2 \cdot g(n)$. If a function is bounded from above by $n$ (Big-$O$) and bounded from below by $n$ (Big-$\Omega$), it is tightly locked to $n$ (Big-$\Theta$).
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Write down the sandwich inequality definition</div>
**What are we doing?** We write down the formal two-sided inequality for Big-$\Theta$.  
**Why are we starting here?** A tight bound requires simultaneously satisfying both a lower bound and an upper bound.  
**How do we do it?** By definition, $f(n) = \Theta(g(n))$ means there exist positive constants $c_1 > 0$, $c_2 > 0$, and an integer $n_0 \ge 1$ such that:

$$c_1 \cdot g(n) \le f(n) \le c_2 \cdot g(n) \quad \text{for all } n \ge n_0$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Combine the findings from Problems 1.1 and 1.2</div>
**What changed from Step 1?** We already proved the lower bound and upper bound individually. Now we join them into a single compound inequality.  
**How do we manipulate the equation?**
* From Problem 1.2, we established the lower bound:
  $$3n \le 3n + 8 \quad \text{for all } n \ge 1$$
* From Problem 1.1, we established the upper bound:
  $$3n + 8 \le 11n \quad \text{for all } n \ge 1$$
* Combining both into one continuous chain:

$$3n \le 3n + 8 \le 11n \quad \text{for all } n \ge 1$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Declare the witnesses and state conclusion</div>
**What is the final answer?** The constants are $c_1 = 3$, $c_2 = 11$, and $n_0 = 1$.  
**Why does this answer make sense?** The function $f(n) = 3n + 8$ is permanently trapped between the lines $3n$ and $11n$ for every integer $n \ge 1$. Since both the upper and lower envelopes grow at rate $n$, the function itself grows at rate $n$:

$$3n + 8 = \Theta(n)$$
</div>

</div>

---

## Level 2: Quadratic Polynomials with Subtraction & Negative Terms

In this level, we introduce expressions that contain negative signs and higher powers. Subtraction introduces a classic pitfall: dropping a negative term makes an expression *larger*, which helps when finding upper bounds, but can break lower bounds if not handled with care.

---

### Problem 2.1: Upper Bound (Big-O) for a Quadratic with Negative Terms

**Problem Statement:** Prove using the formal definition that:

$$f(n) = 5n^2 - 4n + 12 = O(n^2)$$

::: callout-intuition Core Mental Model
When finding a ceiling (Big-$O$), having a term subtracted (like $-4n$) is actually working in our favor! Subtraction pulls the curve down. If we simply pretend the subtraction is not happening (by dropping $-4n$), the resulting expression is guaranteed to be strictly larger than our original function.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Set up the Big-O inequality target</div>
**What are we doing?** We state the target condition: find $c > 0$ and $n_0 \ge 1$ such that:

$$5n^2 - 4n + 12 \le c \cdot n^2 \quad \text{for all } n \ge n_0$$

**Why are we starting here?** To remind ourselves that all terms must ultimately be bounded by the highest power, which is $n^2$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Eliminate the subtracted term $-4n$</div>
**What changed from Step 1?** We analyze the term $-4n$.  
**How do we do it?** For any integer $n \ge 1$, $4n$ is a positive number. When you subtract a positive number from an expression, you make it smaller. Therefore, omitting the subtraction creates an upper bound:

$$5n^2 - 4n + 12 \le 5n^2 + 12 \quad \text{for all } n \ge 1$$

**Where did this rule come from?** Basic arithmetic: for any $A$ and positive $B$, $A - B \le A$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Convert the constant $+12$ to an $n^2$ term</div>
**What changed from Step 2?** We now have $5n^2 + 12$. We need all terms to look like $n^2$.  
**How do we do it?** Since $n \ge 1$, squaring both sides gives $n^2 \ge 1^2 = 1$.  
Multiply both sides of $1 \le n^2$ by $12$:

$$12 \le 12n^2 \quad \text{for all } n \ge 1$$

Now substitute this into our inequality:

$$5n^2 + 12 \le 5n^2 + 12n^2$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Combine coefficients</div>
**What changed from Step 3?** Both terms now share the identical variable factor $n^2$.  
**How do we manipulate the equation?** Add the coefficients $5$ and $12$:

$$5n^2 + 12n^2 = (5 + 12)n^2 = 17n^2$$

Chaining all inequalities together:

$$5n^2 - 4n + 12 \le 5n^2 + 12 \le 17n^2 \quad \text{for all } n \ge 1$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Select witnesses and conclude</div>
**What is the final answer?** Constants $c = 17$ and $n_0 = 1$.  
**Why does this answer make sense?** Testing $n = 1$: $f(1) = 5(1) - 4(1) + 12 = 13$. The bound is $17(1)^2 = 17$. Since $13 \le 17$, the bound holds. As $n$ grows larger, $17n^2$ grows dramatically faster than $5n^2 - 4n + 12$. Therefore:

$$5n^2 - 4n + 12 = O(n^2)$$
</div>

</div>

---

### Problem 2.2: Lower Bound (Big-$\Omega$) for a Quadratic with Negative Terms

**Problem Statement:** Prove using the formal definition that:

$$f(n) = 5n^2 - 4n + 12 = \Omega(n^2)$$

::: callout-intuition Core Mental Model
Lower bounds with negative terms are dangerous. You cannot simply drop $-4n$, because dropping a negative makes the expression *bigger*, but for a lower bound, we need something *smaller*. Instead, we must ask: "How big does $n$ need to be before the powerful $n^2$ term completely overpowers the dragging $-4n$ term?"
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Set up the Big-$\Omega$ inequality target</div>
**What are we doing?** We need to find $c > 0$ and $n_0 \ge 1$ such that:

$$5n^2 - 4n + 12 \ge c \cdot n^2 \quad \text{for all } n \ge n_0$$

**Why are we starting here?** We want to build a floor below $f(n)$ using a fraction of $n^2$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Drop the positive constant term $+12$</div>
**What changed from Step 1?** We look at the $+12$.  
**Why are we starting here?** To establish a lower bound, dropping a positive number safely makes the expression smaller:

$$5n^2 - 4n + 12 \ge 5n^2 - 4n$$

This leaves us with the harder challenge: how to handle the $-4n$ without violating the $\ge$ direction.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Sacrifice a small portion of $5n^2$ to neutralize $-4n$</div>
**What changed from Step 2?** We need to find when the negative term $4n$ is smaller than a piece of our quadratic term.  
**How do we do it?** Let us break $5n^2$ into two parts: $4n^2 + 1n^2$.  
We ask: when is $1n^2 \ge 4n$?  
Divide both sides by $n$ (which is positive since $n \ge 1$):

$$n \ge 4$$

This means that as long as $n \ge 4$, the term $n^2$ is guaranteed to be greater than or equal to $4n$.  
Equivalently:

$$-4n \ge -n^2 \quad \text{for all } n \ge 4$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Substitute the bound into the expression</div>
**What changed from Step 3?** We replace $-4n$ with the smaller quantity $-n^2$:

$$5n^2 - 4n \ge 5n^2 - n^2 \quad \text{for all } n \ge 4$$

Now perform the subtraction:

$$5n^2 - n^2 = (5 - 1)n^2 = 4n^2$$

Connecting the chain:

$$5n^2 - 4n + 12 \ge 5n^2 - 4n \ge 4n^2 \quad \text{for all } n \ge 4$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Declare the witnesses and state conclusion</div>
**What is the final answer?** Constants $c = 4$ and $n_0 = 4$.  
**Why does this answer make sense?** * At $n = 4$: $f(4) = 5(16) - 4(4) + 12 = 80 - 16 + 12 = 76$. The floor is $4(4^2) = 4(16) = 64$. Since $76 \ge 64$, the floor holds.
* For any $n > 4$, the quadratic growth of $5n^2$ crushes the linear $-4n$ even more severely.

Since $5n^2 - 4n + 12 \ge 4n^2$ for all $n \ge 4$:

$$5n^2 - 4n + 12 = \Omega(n^2)$$
</div>

</div>

---

## Level 3: Logarithmic, Exponential, and Factorial Pitfalls

In this level, we tackle the mathematical rules where intuition often misleads beginners: logarithm exponent properties, exponential bases, and factorial expansions.

---

### Problem 3.1: Logarithm Exponent Rule: Prove $\log_2(n^{100}) = O(\log_2 n)$

**Problem Statement:** A student looks at $\log_2(n^{100})$ and guesses it must grow much faster than $\log_2(n)$ because the power is $100$. Prove that:

$$\log_2(n^{100}) = O(\log_2 n)$$

::: callout-intuition Core Mental Model
Powers inside a logarithm do not create exponential growth. A logarithm measures the number of digits or the number of times you can divide. Raising the inside to a power just repeats that work a constant number of times. By the logarithm power law, $\log(x^k) = k \cdot \log(x)$, the giant exponent $100$ falls down as a simple scalar multiplier!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Recall the fundamental power law of logarithms</div>
**What are we doing?** We simplify the expression inside the logarithm before trying to set up bounds.  
**Why are we starting here?** Never perform asymptotic analysis on an unsimplified algebraic expression if standard logarithm laws apply.  
**Where did this formula come from?** The fundamental property of logarithms:

$$\log_b(A^k) = k \cdot \log_b(A)$$

Applying this rule to $f(n) = \log_2(n^{100})$:

$$\log_2(n^{100}) = 100 \cdot \log_2(n)$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Compare against the Big-O definition</div>
**What changed from Step 1?** We now match the simplified expression directly against the definition: $f(n) \le c \cdot g(n)$.  
**How do we do it?** Here, $f(n) = 100 \log_2 n$ and $g(n) = \log_2 n$.  
We must find $c > 0$ and $n_0 \ge 1$ such that:

$$100 \log_2 n \le c \cdot \log_2 n \quad \text{for all } n \ge n_0$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Choose the constants carefully avoiding $\log_2(1) = 0$</div>
**What changed from Step 2?** Notice what happens at $n = 1$: $\log_2(1) = 0$. While $0 \le 0$ is true, standard computer science definitions typically require $g(n) > 0$ to avoid trivial zero cases.  
**How do we do it?** We pick $n_0 = 2$, where $\log_2(2) = 1 > 0$.  
For the constant $c$, since both sides have $\log_2 n$, we can pick $c = 100$:

$$100 \log_2 n \le 100 \log_2 n \quad \text{for all } n \ge 2$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: State conclusion</div>
**What is the final answer?** Constants $c = 100$ and $n_0 = 2$.  
**Why does this answer make sense?** Even though $n^{100}$ looks enormous, the logarithm compresses it completely. An exponent inside a logarithm is merely a constant factor outside:

$$\log_2(n^{100}) = O(\log_2 n)$$
</div>

</div>

---

### Problem 3.2: The Exponential Addition vs. Multiplication Trap

**Problem Statement:** 1. Prove that $2^{n + 5} = O(2^n)$.
2. Prove that $2^{3n} \ne O(2^n)$.

::: callout-intuition Core Mental Model
Adding to an exponent is just multiplying by a fixed constant ($2^{n+5} = 2^5 \cdot 2^n = 32 \cdot 2^n$). Since 32 is a constant, it fits inside Big-$O$. But multiplying an exponent creates an entirely different class of growth: $2^{3n} = (2^3)^n = 8^n$. A process that multiplies by $8$ every step outpaces one that multiplies by $2$ every step by an infinite margin as $n \to \infty$.
:::

#### Part A: Proving $2^{n + 5} = O(2^n)$

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Apply the exponent addition rule</div>
**What are we doing?** Split the exponent into a constant base and a variable base.  
**Where did this rule come from?** The exponent product rule: $a^{x + y} = a^x \cdot a^y$.

$$2^{n + 5} = 2^n \cdot 2^5$$

Calculate $2^5 = 2 \cdot 2 \cdot 2 \cdot 2 \cdot 2 = 32$:

$$2^{n + 5} = 32 \cdot 2^n$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Match with Big-O target inequality</div>
**What changed from Step 1?** We compare $32 \cdot 2^n$ against $c \cdot 2^n$.  
**How do we do it?** Set $c = 32$:

$$32 \cdot 2^n \le 32 \cdot 2^n \quad \text{for all } n \ge 1$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Conclusion for Part A</div>
**What is the final answer?** Constants $c = 32$ and $n_0 = 1$.  
**Why does this answer make sense?** The function $2^{n+5}$ is simply $2^n$ multiplied by 32. In asymptotic notation, constant multipliers are absorbed by $c$. Therefore:

$$2^{n + 5} = O(2^n)$$
</div>

</div>

#### Part B: Proving $2^{3n} \ne O(2^n)$ by Contradiction

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Assume the opposite (Proof by Contradiction)</div>
**What are we doing?** We assume that $2^{3n} = O(2^n)$ is true, and show that this assumption leads to an impossible contradiction.  
**How do we do it?** If $2^{3n} = O(2^n)$, then by definition there must exist some fixed finite positive numbers $c > 0$ and $n_0 \ge 1$ such that:

$$2^{3n} \le c \cdot 2^n \quad \text{for all } n \ge n_0$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Divide both sides by $2^n$</div>
**What changed from Step 1?** We isolate the constant $c$.  
**Why are we doing this?** If $c$ is a fixed constant, isolating it allows us to test if the other side stays below it.  
**How do we do it?** Because $2^n > 0$ for all $n$, we can divide both sides by $2^n$ without changing the inequality sign:

$$\frac{2^{3n}}{2^n} \le c$$

Using exponent subtraction $\frac{a^x}{a^y} = a^{x - y}$:

$$2^{3n - n} \le c \implies 2^{2n} \le c \implies 4^n \le c \quad \text{for all } n \ge n_0$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Expose the contradiction</div>
**What changed from Step 2?** We examine the statement: $4^n \le c$ for all $n \ge n_0$.  
**Why does this fail?** $c$ is supposed to be a fixed, unchanging number (like $100$, $10^6$, or $10^{12}$). But $4^n$ grows without bound as $n \to \infty$:
* If $n = 1$: $4^1 = 4$
* If $n = 10$: $4^{10} = 1{,}048{,}576$
* If $n = 50$: $4^{50} \approx 1.26 \times 10^{30}$

No single finite number $c$ can be greater than or equal to $4^n$ for all values of $n$. We can always pick an $n$ large enough such that $4^n > c$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: State conclusion for Part B</div>
**What is the final answer?** Since the assumption that $2^{3n} = O(2^n)$ leads to the mathematical impossibility $4^n \le c$, the assumption is false. Therefore:

$$2^{3n} \ne O(2^n)$$
</div>

</div>

---

### Problem 3.3: Factorial Bounds: Prove $\log_2(n!) = \Theta(n \log_2 n)$

**Problem Statement:** Prove that the logarithm of the factorial function satisfies:

$$\log_2(n!) = \Theta(n \log_2 n)$$

::: callout-intuition Core Mental Model
$n!$ is $1 \times 2 \times 3 \times \dots \times n$. Taking the logarithm turns this massive multiplication into an addition of terms: $\log(1) + \log(2) + \dots + \log(n)$. 
* **Upper ceiling:** Every one of those $n$ terms is smaller than or equal to $\log(n)$. So the sum is clearly $\le n \log n$.
* **Lower floor:** At least the second half of those numbers (from $n/2$ up to $n$) are all at least as big as $\log(n/2)$. Adding up those $n/2$ terms already gives a substantial fraction of $n \log n$.
:::

#### Part A: Prove the Upper Bound $\log_2(n!) = O(n \log_2 n)$

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Expand the factorial definition</div>
**What are we doing?** Write out the components of $n!$.  
**Where did this formula come from?** Definition of factorial:

$$n! = 1 \cdot 2 \cdot 3 \cdots n$$

Take $\log_2$ of both sides. Using the logarithm product rule $\log(a \cdot b) = \log a + \log b$:

$$\log_2(n!) = \sum_{i=1}^n \log_2(i) = \log_2(1) + \log_2(2) + \log_2(3) + \dots + \log_2(n)$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Replace every individual term with the maximum term $\log_2(n)$</div>
**What changed from Step 1?** Every index $i$ in the sum satisfies $i \le n$.  
**How do we do it?** Because the logarithm is a strictly increasing function, if $i \le n$, then $\log_2(i) \le \log_2(n)$.  
Replace every term in the sum with $\log_2(n)$:

$$\log_2(1) \le \log_2(n)$$
$$\log_2(2) \le \log_2(n)$$
$$\vdots$$
$$\log_2(n) \le \log_2(n)$$

Adding all $n$ inequalities together:

$$\log_2(n!) \le \underbrace{\log_2(n) + \log_2(n) + \dots + \log_2(n)}_{n \text{ times}} = n \log_2(n)$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Extract Big-O witnesses for Part A</div>
**What is the final answer?** With $c = 1$ and $n_0 = 1$:

$$\log_2(n!) \le 1 \cdot n \log_2(n) \quad \text{for all } n \ge 1$$

Thus:

$$\log_2(n!) = O(n \log_2 n)$$
</div>

</div>

#### Part B: Prove the Lower Bound $\log_2(n!) = \Omega(n \log_2 n)$

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Truncate the first half of the sum</div>
**What are we doing?** We discard the smaller numbers in the sum to create an clean lower bound.  
**Why are we starting here?** The numbers from $1$ to $n/2$ are small and messy to bound. Dropping them makes the remaining sum strictly smaller:

$$\log_2(n!) = \sum_{i=1}^n \log_2(i) \ge \sum_{i=\lceil n/2 \rceil}^n \log_2(i)$$

**Where did this rule come from?** Since $\log_2(i) \ge 0$ for all $i \ge 1$, dropping non-negative terms from a sum makes the total smaller or equal.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Bound each remaining term by the smallest element in the upper half</div>
**What changed from Step 1?** In the range from $n/2$ to $n$, the smallest value is at least $n/2$.  
**How do we do it?** For every $i \ge n/2$, we have $\log_2(i) \ge \log_2(n/2)$.  
How many terms are in this upper half? There are at least $\frac{n}{2}$ terms. Therefore:

$$\sum_{i=\lceil n/2 \rceil}^n \log_2(i) \ge \frac{n}{2} \cdot \log_2\left(\frac{n}{2}\right)$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Simplify using logarithm division rules</div>
**What changed from Step 2?** We need the right-hand side to look like a multiple of $n \log_2 n$.  
**How do we manipulate the equation?** Use the logarithm quotient rule $\log_2(a/b) = \log_2 a - \log_2 b$:

$$\log_2\left(\frac{n}{2}\right) = \log_2(n) - \log_2(2) = \log_2(n) - 1$$

Substitute this back into the lower bound:

$$\log_2(n!) \ge \frac{n}{2} (\log_2(n) - 1) = \frac{1}{2} n \log_2(n) - \frac{n}{2}$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Bound the subtracted term for sufficiently large $n$</div>
**What changed from Step 3?** We have a trailing subtraction $-\frac{n}{2}$. We must absorb it.  
**How do we do it?** When $n \ge 4$, we know that $\log_2(n) \ge \log_2(4) = 2$.  
If $\log_2(n) \ge 2$, then:

$$1 \le \frac{1}{2} \log_2(n)$$

Substitute this inequality to replace the $-1$ with a fraction of the logarithm:

$$\log_2(n) - 1 \ge \log_2(n) - \frac{1}{2}\log_2(n) = \frac{1}{2} \log_2(n) \quad \text{for all } n \ge 4$$

Now plug this into our Step 2 expression:

$$\log_2(n!) \ge \frac{n}{2} \cdot \left(\frac{1}{2} \log_2(n)\right) = \frac{1}{4} n \log_2(n) \quad \text{for all } n \ge 4$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Combine bounds into the Big-$\Theta$ conclusion</div>
**What is the final answer?** * From Part A: $\log_2(n!) \le 1 \cdot n \log_2(n)$ for $n \ge 1$ (Upper bound constant $c_2 = 1$).
* From Part B: $\log_2(n!) \ge \frac{1}{4} \cdot n \log_2(n)$ for $n \ge 4$ (Lower bound constant $c_1 = \frac{1}{4}$).

Combining both into the sandwich inequality for all $n \ge 4$:

$$\frac{1}{4} n \log_2(n) \le \log_2(n!) \le 1 \cdot n \log_2(n)$$

**Why does this answer make sense?** With $c_1 = \frac{1}{4}$, $c_2 = 1$, and $n_0 = 4$, $\log_2(n!)$ is trapped tightly between two scalar multiples of $n \log_2(n)$. Therefore:

$$\log_2(n!) = \Theta(n \log_2 n)$$
</div>

</div>
