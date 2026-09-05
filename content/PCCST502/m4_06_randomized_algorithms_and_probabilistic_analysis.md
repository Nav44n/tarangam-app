# Module 4.6: Randomized Algorithms — Probabilistic Foundations, Las Vegas vs. Monte Carlo, and QuickSort Analysis

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search & Computational Complexity  
**Document Classification:** Publication-Grade Theoretical Lecture Note & Mathematical Foundation  

---

## 1. Executive Overview: The Power of Randomness in Computation

In deterministic algorithm design, an algorithm is viewed as a mathematical function mapping an input $x$ to a deterministic output $y = A(x)$. For every execution on input $x$, the internal control flow, the sequence of machine instructions, and the runtime are identical. A deterministic algorithm cannot protect itself against an **adversary**: an external entity who analyzes the algorithm's source code and intentionally crafts a pathological worst-case input designed to trigger exponential or quadratic behavior (e.g., feeding an already-sorted array to a deterministic QuickSort that picks the first element as pivot).

A **Randomized Algorithm** fundamentally changes this dynamic by introducing **independent random bits** as an auxiliary computational resource alongside time and space.

```text
               Deterministic Computation:
               Input x ─────────────────────────> [ Algorithm A ] ──────> Output y (Fixed)

               Randomized Computation:
               Input x ───────────+
                                  |
                                  v
               Random Bits r ───> [ Algorithm A ] ──────> Output y (Probabilistic)
               (Coin Flips)
```

By allowing the algorithm to consult an unbiased source of entropy (a random coin flipper) during execution:
1. **Adversary Neutralization:** No static input instance can reliably trigger worst-case behavior, because the algorithm's execution path depends on coin flips made at runtime.
2. **Algorithmic Simplicity:** Randomized algorithms are often dramatically simpler, easier to implement, and have smaller constant factors than their deterministic counterparts (e.g., Randomized QuickSort vs. Median-of-Medians QuickSelect).
3. **Breaking Symmetry:** In distributed computing and cryptography, randomness is essential for resolving deadlocks and selecting leaders.

::: callout-intuition
**Mental Model: Changing Who Controls the Coin**  
- **Average-Case Analysis:** Assumes the *input* comes from a probability distribution (e.g., all permutations are equally likely). If the real world violates this assumption, the algorithm can degrade to worst-case performance.
- **Randomized Analysis:** Assumes *nothing* about the input (it can be chosen by a malicious adversary). The probability distribution is introduced *internally by the algorithm's own coin flips*. The performance guarantees hold for **every single input instance**.
:::

---

## 2. Las Vegas vs. Monte Carlo Paradigms

Randomized algorithms are divided into two fundamental architectural classes based on whether the randomness affects the **running time** or the **solution correctness**.

```text
+======================================================================================================+
|                                  RANDOMIZED ALGORITHM TAXONOMY                                       |
+=========================+========================================+===================================+
| Dimension               | Las Vegas Algorithms                   | Monte Carlo Algorithms            |
+=========================+========================================+===================================+
| Correctness Guarantee   | **Deterministic & Absolute (100%):**   | **Probabilistic:**                |
|                         | Always outputs the correct answer.     | May output an incorrect answer or |
|                         | Never produces an erroneous result.    | fail with bounded probability ε.  |
+-------------------------+----------------------------------------+-----------------------------------+
| Running Time Profile    | **Random Variable:**                   | **Deterministic or Strict:**      |
|                         | Runtime varies between executions.     | Runtime is strictly bounded       |
|                         | Guarantees *expected* polynomial time. | (e.g., always O(n log n)).        |
+-------------------------+----------------------------------------+-----------------------------------+
| Canonical Example       | Randomized QuickSort,                  | Miller-Rabin Primality Test,      |
|                         | Randomized QuickSelect                 | Karger's Min-Cut Algorithm        |
+-------------------------+----------------------------------------+-----------------------------------+
| Mathematical Objective  | Bound the Expected Time E[T(n)].       | Minimize the Error Probability ε  |
|                         | Prove small variance Var(T(n)).        | using independent repetitions.    |
+=========================+========================================+===================================+
```

---

### 2.1 Las Vegas Algorithms: Guaranteed Correctness, Variable Time

#### Definition 2.1 (Las Vegas Algorithm)
An algorithm $A$ is a **Las Vegas algorithm** for a computational problem if, for every input instance $x$:
1. $A(x)$ always returns the mathematically correct solution:
   $$\Pr[A(x) = \text{Correct Solution}] = 1.0$$
2. The running time $T(x)$ is a random variable over the space of internal coin flips $\Omega$. The performance is characterized by its **expected running time**:
   $$\mathbb{E}[T(x)] = \sum_{t=1}^{\infty} t \cdot \Pr[T(x) = t]$$

*Example:* In **Randomized QuickSort**, the output is always correctly sorted. The algorithm never produces a mis-sorted array. However, the number of comparisons depends on which pivots are chosen at runtime.

---

### 2.2 Monte Carlo Algorithms: Guaranteed Time, Probabilistic Correctness

#### Definition 2.2 (Monte Carlo Algorithm)
An algorithm $A$ is a **Monte Carlo algorithm** with error probability $\epsilon \in [0, 1)$ if:
1. The running time is deterministic and strictly bounded by $p(|x|)$ for all execution paths.
2. For every input instance $x$, the probability of returning an incorrect answer is bounded:
   $$\Pr[A(x) \ne \text{Correct Solution}] \le \epsilon$$

---

### 2.3 Error Reduction via Independent Amplification

For Monte Carlo algorithms, an error probability $\epsilon < 1/2$ can be driven arbitrarily close to zero by running independent repetitions.

#### One-Sided Error Amplification:
Consider a Monte Carlo algorithm for a decision problem with **one-sided error** (e.g., the Miller-Rabin primality test):
- If the true answer is **COMPOSITE**, the algorithm answers "COMPOSITE" with probability $\ge 1/2$, and answers "PRIME" with probability $\le 1/2$.
- If the true answer is **PRIME**, the algorithm answers "PRIME" with probability $1.0$ (never falsely reports composite).

```text
               Instance x is COMPOSITE:
               
               Trial 1:  Error (reports PRIME) with Pr ≤ 1/2
               Trial 2:  Error (reports PRIME) with Pr ≤ 1/2
               ...
               Trial k:  Error (reports PRIME) with Pr ≤ 1/2
               
               Joint Probability of k consecutive false reports:
                            Pr[All k err] ≤ (1/2)^k
```

If we run the algorithm $k$ independent times and answer "COMPOSITE" if *any* run finds a witness:
$$\Pr[\text{Failure after } k \text{ trials}] \le \left( \frac{1}{2} \right)^k$$
For $k = 100$:
$$\Pr[\text{Failure}] \le 2^{-100} \approx 7.88 \times 10^{-31}$$
This error probability is smaller than the likelihood of a cosmic ray flipping a bit in the CPU memory during computation!

#### Two-Sided Error Amplification (Chernoff Bound):
If an algorithm has two-sided error with probability $p = 1/2 + \delta$ (where $\delta > 0$) of being correct:
- Run the algorithm $k$ independent times.
- Return the **majority vote** of the $k$ outcomes.
- By the **Chernoff-Hoeffding Bound**, the probability that the majority vote is incorrect decays exponentially:
  $$\Pr[\text{Majority Vote Fails}] \le e^{-2 k \delta^2}$$
- Setting $k = \mathcal{O}\left(\frac{1}{\delta^2} \ln \frac{1}{\epsilon}\right)$ reduces the error probability below any target $\epsilon > 0$.

---

## 3. Mathematical Foundations of Probabilistic Analysis

Analyzing randomized algorithms requires three foundational tools from probability theory: **Sample Spaces**, **Random Variables**, and **Linearity of Expectation**.

### 3.1 Probability Space and Random Variables
- **Sample Space ($\Omega$):** The set of all possible outcomes of the algorithm's coin flips.
- **Random Variable ($X$):** A real-valued function defined on the sample space:
  $$X: \Omega \to \mathbb{R}$$
- **Expected Value ($\mathbb{E}[X]$):** The weighted average of all values $X$ can take:
  $$\mathbb{E}[X] = \sum_{x \in \text{Range}(X)} x \cdot \Pr[X = x]$$

---

### 3.2 Indicator Random Variables

The **Indicator Random Variable** bridges events and expectations, converting probabilistic questions into algebraic summations.

#### Definition 3.1 (Indicator Random Variable)
Let $A$ be an event in sample space $\Omega$. The indicator random variable $I\{A\}$ (or $X_A$) is defined as:
$$I\{A\} = \begin{cases} 1, & \text{if event } A \text{ occurs} \\ 0, & \text{if event } A \text{ does not occur} \end{cases}$$

#### Lemma 3.1 (Fundamental Expectation of Indicators)
*The expected value of an indicator random variable is equal to the probability of its corresponding event:*
$$\mathbb{E}[I\{A\}] = \Pr[A]$$

**Proof:**
$$\mathbb{E}[I\{A\}] = 1 \cdot \Pr[I\{A\} = 1] + 0 \cdot \Pr[I\{A\} = 0] = \Pr[A] \quad \blacksquare$$

---

### 3.3 Linearity of Expectation

**Linearity of Expectation** is one of the most powerful tools in algorithm analysis. Crucially, it holds **regardless of whether the random variables are independent**.

#### Theorem 3.2 (Linearity of Expectation)
*Let $X_1, X_2, \dots, X_m$ be arbitrary random variables defined on the same probability space, and let $c_1, c_2, \dots, c_m \in \mathbb{R}$ be scalar constants. Then:*
$$\mathbb{E}\left[ \sum_{i=1}^m c_i X_i \right] = \sum_{i=1}^m c_i \mathbb{E}[X_i]$$

**Proof (for discrete variables):**
$$\mathbb{E}\left[ \sum_{i=1}^m X_i \right] = \sum_{\omega \in \Omega} \left( \sum_{i=1}^m X_i(\omega) \right) \Pr[\omega] = \sum_{i=1}^m \left( \sum_{\omega \in \Omega} X_i(\omega) \Pr[\omega] \right) = \sum_{i=1}^m \mathbb{E}[X_i] \quad \blacksquare$$

---

## 4. Rigorous Analysis of Randomized QuickSort

We now apply these probabilistic tools to perform an exact, formal analysis of **Randomized QuickSort**.

### 4.1 The Algorithmic Vulnerability of Deterministic QuickSort
Standard deterministic QuickSort selects a fixed element (such as the first element $A[p]$ or the last element $A[r]$) as the partition pivot.

```text
Deterministic Worst-Case: Input is already sorted: [1, 2, 3, 4, 5]
Pivot = 1 ---> Partitions into [] and [2, 3, 4, 5] (Sizes 0 and n-1)
Recurrence: T(n) = T(n - 1) + O(n) = O(n^2) comparisons!
```

To eliminate this vulnerability, **Randomized QuickSort** chooses its pivot **uniformly at random** from the current subarray.

```text
Algorithm RandomizedPartition(A, p, r)
begin
    // Select an index uniformly at random from {p, p+1, ..., r}
    i := RandomInteger(p, r);
    
    // Swap A[i] with A[r] to use standard partition logic
    Swap(A[i], A[r]);
    
    return LomutoPartition(A, p, r);
end;

Algorithm RandomizedQuickSort(A, p, r)
begin
    if p < r then
        q := RandomizedPartition(A, p, r);
        RandomizedQuickSort(A, p, q - 1);
        RandomizedQuickSort(A, q + 1, r);
    end if;
end;
```

---

### 4.2 Formal Definition of the Comparison Counting Model
Let $A = (a_1, a_2, \dots, a_n)$ be an array of $n$ distinct elements.  
The total running time of QuickSort is dominated by the number of element-to-element comparisons executed during the partition steps. All other operations (swapping, recursion management) are proportional to the comparison count.

Let $X$ denote the total number of comparisons performed across the entire recursive execution of Randomized QuickSort on array $A$. We will prove:
$$\mathbb{E}[X] = 2n \ln n + \mathcal{O}(n) = \Theta(n \log n)$$

---

### 4.3 Setup: Order Statistics Notation
To analyze comparisons without tracking recursive calls, we rename the elements of array $A$ by their **true sorted order**.

Let:
$$z_1 < z_2 < z_3 < \dots < z_n$$
denote the elements of $A$ sorted in strictly increasing order, where $z_i$ is the $i$-th smallest element of $A$.
- Let $Z_{ij} = \{z_i, z_{i+1}, \dots, z_j\}$ denote the set of elements from $z_i$ up to $z_j$ inclusive (where $1 \le i < j \le n$).
- The total number of elements in subset $Z_{ij}$ is:
  $$|Z_{ij}| = j - i + 1$$

---

### 4.4 Decomposition via Indicator Random Variables

We define an indicator random variable for every pair of indices $(i, j)$ with $1 \le i < j \le n$:
$$X_{ij} = I\{z_i \text{ is compared with } z_j \text{ at some point during execution}\}$$

#### Critical Observation 1: At Most One Comparison
In QuickSort, elements are only compared against the **active pivot**. Once a pivot is selected, it is placed into its final sorted position and never participates in any future partition steps. Therefore:
> *Any two distinct elements $z_i$ and $z_j$ are compared **at most once** during the entire execution of the algorithm.*

Thus, $X_{ij} \in \{0, 1\}$. The total number of comparisons across the entire algorithm is:
$$X = \sum_{i=1}^{n-1} \sum_{j=i+1}^n X_{ij}$$

Applying **Linearity of Expectation** (Theorem 3.2):
$$\mathbb{E}[X] = \mathbb{E}\left[ \sum_{i=1}^{n-1} \sum_{j=i+1}^n X_{ij} \right] = \sum_{i=1}^{n-1} \sum_{j=i+1}^n \mathbb{E}[X_{ij}]$$

Applying **Lemma 3.1** ($\mathbb{E}[X_{ij}] = \Pr[X_{ij} = 1]$):
$$\mathbb{E}[X] = \sum_{i=1}^{n-1} \sum_{j=i+1}^n \Pr[z_i \text{ is compared with } z_j]$$

The entire analysis now reduces to computing this single probability: $\Pr[z_i \text{ is compared with } z_j]$.

---

### 4.5 Deriving the Pairwise Comparison Probability $\Pr[X_{ij} = 1]$

Consider the set of elements between $z_i$ and $z_j$ in the sorted order:
$$Z_{ij} = \{z_i, z_{i+1}, z_{i+2}, \dots, z_{j-1}, z_j\}$$

What happens as the algorithm executes?
- Initially, all elements of $Z_{ij}$ reside together in the same subarray.
- As recursive partitioning proceeds, elements outside $Z_{ij}$ are chosen as pivots. These splits either keep all elements of $Z_{ij}$ together in the same subproblem, or move elements entirely outside $Z_{ij}$.
- Eventually, a recursive call arrives where an element **from the set $Z_{ij}$ is selected as a pivot for the first time**.

Let $z_k \in Z_{ij}$ be the **very first element from $Z_{ij}$** chosen as a pivot.

```text
Elements of Z_ij:
[ z_i,   z_{i+1},   z_{i+2},   ...,   z_k,   ...,   z_{j-1},   z_j ]
  |                                    |                        |
  +--- Case 1: First pivot is z_i      |                        |
       (Compared with all in Z_ij)     +--- Case 3: First pivot |
       ===> z_i compared with z_j!          is z_k (i < k < j)  |
                                            (Splits Z_ij apart) |
                                            ===> NEVER compared!|
                                                                |
  +-------------------------------------------------------------+
  |
  +--- Case 2: First pivot is z_j
       (Compared with all in Z_ij)
       ===> z_i compared with z_j!
```

There are three mutually exclusive cases:

1. **Case 1: The first pivot selected from $Z_{ij}$ is $z_i$.**  
   Because $z_i$ is the pivot, it is compared against every other element in its current subarray. Since $z_j$ is in the same subarray, **$z_i$ and $z_j$ are compared**.
2. **Case 2: The first pivot selected from $Z_{ij}$ is $z_j$.**  
   Symmetrically, $z_j$ is the pivot, so it is compared against every element in its subarray, including $z_i$. **$z_i$ and $z_j$ are compared**.
3. **Case 3: The first pivot selected from $Z_{ij}$ is an intermediate element $z_k$ (where $i < k < j$).**  
   Element $z_k$ is compared against the elements in its subarray. Then, the partition step divides the subarray:
   - Elements smaller than $z_k$ (which includes $z_i$) go to the left subarray.
   - Elements larger than $z_k$ (which includes $z_j$) go to the right subarray.
   - $z_i$ and $z_j$ are now separated into two completely disjoint recursive subtrees.
   - They will **never** appear in the same subproblem again, meaning **$z_i$ and $z_j$ are never compared**.

#### The Key Deduction:
> *$z_i$ and $z_j$ are compared **if and only if** the first element chosen as a pivot from $Z_{ij}$ is either $z_i$ or $z_j$.*

Because the pivot at each step is selected **uniformly at random**, every element currently in the subarray has an equal probability of being chosen.  
Until some element from $Z_{ij}$ is picked as pivot, no element from $Z_{ij}$ has been chosen. Therefore, conditioned on the event that *some* element from $Z_{ij}$ is selected as the first pivot, **each of the $|Z_{ij}|$ elements is equally likely to be that first pivot**.

The number of elements in $Z_{ij}$ is:
$$|Z_{ij}| = j - i + 1$$

The favorable outcomes are selecting $z_i$ or selecting $z_j$ (2 outcomes).  
Therefore, the probability is:

$$\Pr[z_i \text{ is compared with } z_j] = \frac{2}{|Z_{ij}|} = \frac{2}{j - i + 1}$$

---

### 4.6 Summing the Harmonic Series to Bound $\mathbb{E}[X]$

Now, substitute this exact probability back into our expectation formula:

$$\mathbb{E}[X] = \sum_{i=1}^{n-1} \sum_{j=i+1}^n \frac{2}{j - i + 1}$$

To evaluate this double summation, introduce a change of variable:
- Let $k = j - i$.
- For a fixed $i$, as $j$ runs from $i + 1$ to $n$, the difference $k$ runs from $1$ to $n - i$.
- The denominator becomes $(j - i + 1) = k + 1$.

$$\mathbb{E}[X] = \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{2}{k + 1}$$

We can upper-bound this sum by extending the inner summation range from $n - i$ up to $n$:

$$\mathbb{E}[X] < \sum_{i=1}^{n-1} \sum_{k=1}^n \frac{2}{k + 1} = \sum_{i=1}^{n-1} \left( 2 \sum_{k=1}^n \frac{1}{k + 1} \right)$$

Shift the summation index by setting $m = k + 1$:

$$\sum_{k=1}^n \frac{1}{k + 1} = \sum_{m=2}^{n+1} \frac{1}{m} = \left( \sum_{m=1}^n \frac{1}{m} \right) - 1 + \frac{1}{n+1} = H_n - 1 + \frac{1}{n+1}$$

where $H_n = \sum_{m=1}^n \frac{1}{m}$ is the $n$-th **Harmonic Number**.

```text
Harmonic Number Integral Bound:
  ln(n) < H_n <= ln(n) + 1
```

Substituting $H_n \le \ln n + 1$:

$$\sum_{k=1}^n \frac{1}{k + 1} \le \ln n$$

Now evaluate the outer summation:

$$\mathbb{E}[X] < \sum_{i=1}^{n-1} 2 \ln n = 2 \ln n \sum_{i=1}^{n-1} 1 = 2(n - 1) \ln n$$

Using the natural logarithm to base-2 identity ($\ln n = \frac{\log_2 n}{\log_2 e} \approx 0.693 \log_2 n$):

$$\mathbb{E}[X] < 2n \ln n = (2 \ln 2) n \log_2 n \approx 1.386 \, n \log_2 n$$

#### Final Conclusion:
$$\mathbb{E}[X] = \mathcal{O}(n \log n)$$

On average, Randomized QuickSort performs only **$38.6\%$ more comparisons** than the theoretical lower bound for comparison sorting ($n \log_2 n$). And this bound holds for **every possible input array of size $n$**. $\blacksquare$

---

## 5. Concrete Numerical Trace of the Expectation Proof

To see the math in action, let us compute the exact expected comparison count for an array of size $n = 4$.

Sorted elements: $z_1 < z_2 < z_3 < z_4$.  
Total pairs: $\binom{4}{2} = \frac{4 \times 3}{2} = 6$ pairs.

```text
+==============+==============+=================+====================================+
| Pair (i, j)  | Gap k = j - i| Subarray Size   | Comparison Probability             |
|              |              | |Z_ij| = j-i+1  | Pr[X_ij = 1] = 2 / (j - i + 1)     |
+==============+==============+=================+====================================+
| (1, 2)       | 1            | 2 (z1, z2)      | 2 / 2 = 1.000                      |
+--------------+--------------+-----------------+------------------------------------+
| (2, 3)       | 1            | 2 (z2, z3)      | 2 / 2 = 1.000                      |
+--------------+--------------+-----------------+------------------------------------+
| (3, 4)       | 1            | 2 (z3, z4)      | 2 / 2 = 1.000                      |
+--------------+--------------+-----------------+------------------------------------+
| (1, 3)       | 2            | 3 (z1, z2, z3)  | 2 / 3 ≈ 0.667                      |
+--------------+--------------+-----------------+------------------------------------+
| (2, 4)       | 2            | 3 (z2, z3, z4)  | 2 / 3 ≈ 0.667                      |
+--------------+--------------+-----------------+------------------------------------+
| (1, 4)       | 3            | 4 (z1..z4)      | 2 / 4 = 0.500                      |
+==============+==============+=================+====================================+
```

Summing the probabilities across all 6 pairs:
$$\mathbb{E}[X] = 1.0 + 1.0 + 1.0 + \frac{2}{3} + \frac{2}{3} + \frac{1}{2} = 3.0 + \frac{4}{3} + 0.5 = 3.0 + 1.333 + 0.5 = 4.833 \text{ comparisons}$$

- **Adjacent elements** ($(1, 2), (2, 3), (3, 4)$): $j - i + 1 = 2$, so comparison probability is $2/2 = 1.0$. **Adjacent elements are always compared**, regardless of which pivots are chosen.
- **Extremes** ($(1, 4)$): Comparison probability is $2/4 = 0.5$. The minimum and maximum elements have only a $50\%$ chance of being directly compared, because picking either $z_2$ or $z_3$ as the first pivot separates them forever.

---

## 6. High-Probability Bounds: Tail Inequalities

While $\mathbb{E}[X] = \mathcal{O}(n \log n)$ characterizes average behavior, we can also prove that the probability of Randomized QuickSort deviating significantly from its expected runtime is exponentially small.

### 6.1 Markov's Inequality
For any non-negative random variable $Y \ge 0$ and any constant $a > 0$:
$$\Pr[Y \ge a] \le \frac{\mathbb{E}[Y]}{a}$$
- Setting $a = 10 \cdot \mathbb{E}[X]$:
  $$\Pr[X \ge 10 \cdot \mathbb{E}[X]] \le \frac{1}{10} = 10\%$$
- While useful, Markov's inequality provides relatively weak bounds because it uses only the expectation.

### 6.2 Chebyshev's Inequality
Incorporating the **variance** $\text{Var}(Y) = \mathbb{E}[(Y - \mathbb{E}[Y])^2]$:
$$\Pr[|Y - \mathbb{E}[Y]| \ge k \sigma] \le \frac{1}{k^2}$$
For QuickSort, $\text{Var}(X) = \mathcal{O}(n^2)$, which proves that the standard deviation is $\sigma = \mathcal{O}(n)$, much smaller than the expectation $\mathbb{E}[X] = \Theta(n \log n)$.

### 6.3 Chernoff Bounds (High Probability Guarantee)
By modeling the partition process as a sequence of independent Bernoulli trials:
$$\Pr[X > c \cdot n \ln n] \le \frac{1}{n^d} \quad (\text{for constants } c, d)$$
This proves that Randomized QuickSort runs in $\mathcal{O}(n \log n)$ **with high probability** (w.h.p.), meaning the probability of encountering the worst-case $\mathcal{O}(n^2)$ on an array of size $n = 10^6$ is less than $10^{-100}$.

---

## 7. Las Vegas vs. Monte Carlo: Architectural Trade-Offs

```text
+======================================================================================================+
|                              PARADIGM COMPARISON: LAS VEGAS VS. MONTE CARLO                          |
+======================+=======================================+=======================================+
| Dimension            | Las Vegas Paradigm                    | Monte Carlo Paradigm                  |
+======================+=======================================+=======================================+
| Primary Objective    | Protect runtime against malicious     | Solve computationally hard problems   |
|                      | inputs; maintain exact correctness.   | faster by tolerating bounded error.   |
+----------------------+---------------------------------------+---------------------------------------+
| Output Reliability   | Always correct (error prob = 0).      | Bounded error probability ε > 0.      |
+----------------------+---------------------------------------+---------------------------------------+
| Stopping Criterion   | Terminates when the verified correct  | Terminates after a fixed number of    |
|                      | solution is produced.                 | computational cycles.                 |
+----------------------+---------------------------------------+---------------------------------------+
| Conversion Mechanism | Can be converted to Monte Carlo by    | Can be converted to Las Vegas if a    |
|                      | terminating after a fixed time limit  | fast deterministic verifier exists    |
|                      | (returns failure if incomplete).      | (run until output verifies).          |
+----------------------+---------------------------------------+---------------------------------------+
| Representative       | 1. Randomized QuickSort               | 1. Miller-Rabin Primality Testing     |
| Algorithms           | 2. Randomized QuickSelect (linear time| 2. Karger's Min-Cut Algorithm         |
|                      |    expected median finder)            | 3. Monte Carlo Tree Search (MCTS)     |
|                      | 3. Randomized Treaps / Skip Lists     | 4. Random Walk Testing                |
+======================+=======================================+=======================================+
```

---

## 8. KTU Examination High-Yield Preparation

This section provides model answers formatted for direct scoring under the KTU 2024 scheme for course code **PCCST502 / CST306**.

---

### Question 1 (3 Marks): Differentiate between Las Vegas and Monte Carlo randomized algorithms with an example for each.

#### Model Answer:
| Attribute | Las Vegas Algorithm | Monte Carlo Algorithm |
| :--- | :--- | :--- |
| **Correctness** | Always produces the correct answer ($\Pr[\text{Success}] = 1.0$). | May produce an incorrect answer with bounded error probability ($\Pr[\text{Error}] \le \epsilon$). |
| **Running Time** | Random variable; expected running time is polynomial. | Fixed / strictly bounded running time. |
| **Example** | **Randomized QuickSort** (always sorts correctly; expected time is $\mathcal{O}(n \log n)$). | **Miller-Rabin Primality Test** (runs in polynomial time; may falsely declare composite as prime with probability $\le 4^{-k}$). |

---

### Question 2 (3 Marks): Define Indicator Random Variable. State and prove the fundamental lemma relating it to probability.

#### Model Answer:
- **Definition:** Given sample space $\Omega$ and event $A$, the indicator random variable $I\{A\}$ is defined as:
  $$I\{A\} = \begin{cases} 1, & \text{if event } A \text{ occurs} \\ 0, & \text{if event } A \text{ does not occur} \end{cases}$$
- **Lemma:** $\mathbb{E}[I\{A\}] = \Pr[A]$
- **Proof:** By definition of expected value:
  $$\mathbb{E}[I\{A\}] = 1 \cdot \Pr[I\{A\} = 1] + 0 \cdot \Pr[I\{A\} = 0] = \Pr[A] + 0 = \Pr[A] \quad \blacksquare$$

---

### Question 3 (10 Marks): Prove that the expected running time of Randomized QuickSort on any input array of size $n$ is $\mathcal{O}(n \log n)$.

#### Model Answer Structure:
1. **Model Formulation:**
   - Let $z_1 < z_2 < \dots < z_n$ be the elements of $A$ in sorted order.
   - Let $X_{ij} = I\{z_i \text{ is compared with } z_j\}$ for $1 \le i < j \le n$.
   - Note that any pair is compared at most once. Total comparisons: $X = \sum_{i=1}^{n-1} \sum_{j=i+1}^n X_{ij}$. *(2 Marks)*
2. **Linearity of Expectation:**
   $$\mathbb{E}[X] = \sum_{i=1}^{n-1} \sum_{j=i+1}^n \mathbb{E}[X_{ij}] = \sum_{i=1}^{n-1} \sum_{j=i+1}^n \Pr[z_i \text{ is compared with } z_j] \quad (2\text{ Marks})$$
3. **Probability Derivation:**
   - Consider $Z_{ij} = \{z_i, z_{i+1}, \dots, z_j\}$ of size $j - i + 1$.
   - $z_i$ and $z_j$ are compared if and only if the first pivot chosen from $Z_{ij}$ is either $z_i$ or $z_j$.
   - If an intermediate pivot $z_k$ ($i < k < j$) is chosen first, $z_i$ and $z_j$ are separated into different partitions and never compared.
   - Since pivots are chosen uniformly at random, each of the $j - i + 1$ elements is equally likely to be the first pivot.
   - Therefore: $\Pr[X_{ij} = 1] = \frac{2}{j - i + 1}$. *(3 Marks)*
4. **Summation Evaluation:**
   $$\mathbb{E}[X] = \sum_{i=1}^{n-1} \sum_{j=i+1}^n \frac{2}{j - i + 1} = \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{2}{k+1} < 2 \sum_{i=1}^{n-1} H_n < 2n \ln n = \mathcal{O}(n \log n) \quad (3\text{ Marks})$$

---

### Question 4 (5 Marks): Explain how the error probability of a Monte Carlo algorithm can be reduced using independent repetitions.

#### Model Answer:
1. **One-Sided Error Amplification:**
   - Suppose a Monte Carlo algorithm has a one-sided error probability of at most $1/2$ (e.g., if the true answer is YES, it reports YES with probability $\ge 1/2$; if NO, it always reports NO).
   - Run the algorithm $k$ independent times on the same input.
   - Return YES if **at least one** run returns YES; return NO only if all $k$ runs return NO.
2. **Error Probability Bound:**
   - The algorithm only errs if all $k$ runs independently fail to detect the YES answer.
   - Because the runs use independent random coin flips:
     $$\Pr[\text{Error after } k \text{ runs}] \le \left( \frac{1}{2} \right)^k$$
3. **Exponential Suppression:**
   - For $k = 10$, $\Pr[\text{Error}] \le 1/1024 < 0.001$.
   - For $k = 30$, $\Pr[\text{Error}] \le 2^{-30} \approx 10^{-9}$.
   - This drives the error probability exponentially close to zero with only a linear increase in running time ($k \cdot T(n)$). $\blacksquare$
