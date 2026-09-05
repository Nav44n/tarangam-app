# Module 4 - Problem Worklab 6: Randomized Algorithms — Randomized Quicksort & Karger's Min-Cut

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search, Computational Complexity & Randomized Algorithms  
**Document Classification:** Publication-Grade Problem Worklab & Rigorous Probabilistic Trace  

---

## 1. Executive Summary & Foundational Randomization Theory

When deterministic algorithms face adversarial worst-case inputs, their performance can degrade drastically—for example, deterministic Quicksort degenerates to $\Theta(n^2)$ time on sorted arrays, and deterministic minimum cut algorithms on dense graphs require complex network-flow machinery.

**Randomized Algorithms** overcome these limitations by allowing the computing machine access to an unbiased stream of random bits. By making random choices during execution, the algorithm ensures that **no fixed input instance can consistently force worst-case behavior**.

```text
========================================================================================================
                                 THE DUAL RANDOMIZED TAXONOMY PIPELINE
========================================================================================================

          [ Problem Instance x ] ────+
                                     |
                                     v
                        +──────────────────────────+
                        |   Randomized Algorithm   | <──── [ Random Seed / Bits ]
                        +──────────────────────────+
                                     |
                    +----------------+----------------+
                    |                                 |
                    v                                 v
        [ Las Vegas Paradigm ]              [ Monte Carlo Paradigm ]
        - Correctness: 100% Guaranteed      - Correctness: Probabilistic (1 - δ)
        - Runtime: Random Variable          - Runtime: Deterministic / Fixed Bound
        - Metric: Expected Time E[T(n)]     - Metric: Error Bound Amplification
        - Example: Randomized Quicksort     - Example: Karger's Min-Cut
```

### 1.1 Mathematical Formulation of the Two Paradigms

#### Definition 1.1 (Las Vegas Algorithm)
An algorithm $\mathcal{A}$ is a **Las Vegas algorithm** for problem $\Pi$ if for every input instance $x$:
1. $\mathcal{A}(x)$ always outputs the mathematically correct, optimal solution upon termination:
   $$\Pr(\mathcal{A}(x) = \Pi(x)) = 1.0$$
2. The running time $T(x)$ is a random variable. The algorithm is bounded by its **expected time complexity**:
   $$\mathbb{E}[T(n)] \le p(n) \quad \text{for some polynomial } p$$

#### Definition 1.2 (Monte Carlo Algorithm)
An algorithm $\mathcal{B}$ is a **Monte Carlo algorithm** with error probability $\delta \in (0, 1)$ if for every input instance $x$:
1. The running time $T(x)$ is strictly bounded deterministically by a polynomial $q(|x|)$.
2. The output is correct with high probability:
   $$\Pr(\mathcal{B}(x) = \Pi(x)) \ge 1 - \delta$$

::: callout-intuition
**Mental Model: The Locksmith vs. The Metal Detector**  
- **Las Vegas (Randomized Quicksort):** Like a master locksmith who tries random keys from a ring without repetition. He is **100% guaranteed** to unlock the door eventually; the only unknown is how many minutes it will take.
- **Monte Carlo (Karger's Min-Cut):** Like scanning an open field with a metal detector within a strict 15-minute time limit. The search will always finish on time, but there is a small probability that a deeply buried coin was overlooked. To achieve near-certainty, you scan the field multiple times independently (**probability amplification**).
:::

---

## 2. Level 1: Randomized Quicksort Partitioning & Expected Comparisons

### Problem 1.1 Specification
Let $A$ be an array of $n = 8$ distinct integers indexed from $1$ to $8$:
$$A = [28, 14, 35, 42, 7, 19, 50, 21]$$

Our objective is to:
1. Trace the complete execution of **Randomized Quicksort** using randomized pivot selection and Lomuto partitioning.
2. Contrast this behavior against deterministic Quicksort on an already sorted array to demonstrate how deterministic partitioning degrades to $\Theta(n^2)$.
3. Provide a rigorous, zero-logical-leap mathematical proof using indicator random variables showing that the expected number of comparisons is:
   $$\mathbb{E}[X] = 2n \ln n + \mathcal{O}(n) = \Theta(n \log n)$$

---

### Step-Card 1.1: Root Call — Randomized Partitioning of $A[1..8]$

#### 1. What are we doing?
Executing `RandomizedPartition(A, p = 1, r = 8)` on the full array:
$$A = [28, 14, 35, 42, 7, 19, 50, 21]$$

#### 2. Why are we starting here?
The algorithm sorts the entire range $[p..r]$. Before partitioning, it selects an index $k \in [p..r]$ uniformly at random and swaps $A[k]$ with $A[r]$.

#### 3. How do we execute the step mechanically?

##### Phase 1: Random Pivot Selection & Normalization
- Domain of indices: $\{1, 2, 3, 4, 5, 6, 7, 8\}$.
- Let the uniform random number generator yield:
  $$k = \text{Random}(1, 8) = 8$$
  *(Value $A[8] = 21$ is selected as the pivot).*
- Swap $A[k]$ with $A[r]$: Since $k = r = 8$, no element moves. Pivot value:
  $$\text{pivot} = x = A[8] = 21$$

##### Phase 2: Lomuto Partitioning Trace
We initialize pointer $i = p - 1 = 1 - 1 = 0$.  
Pointer $j$ scans from $p = 1$ to $r - 1 = 7$.

```text
Initial State:
  i = 0
  j = 1
  A = [ 28,  14,  35,  42,   7,  19,  50  |  21 (PIVOT) ]
```

| Scan Index ($j$) | Inspected Element $A[j]$ | Comparison with Pivot ($A[j] \le 21$) | Boolean Result | Action Taken | Array State After Step | Updated $i$ |
| :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **$j = 1$** | $A[1] = 28$ | $28 \le 21$ | **FALSE** | None. Advance $j$. | $[28, 14, 35, 42, 7, 19, 50 \mid 21]$ | $i = 0$ |
| **$j = 2$** | $A[2] = 14$ | $14 \le 21$ | **TRUE** | Increment $i \to 1$. Swap $A[i]=A[1]$ and $A[j]=A[2]$. | $[\mathbf{14}, \mathbf{28}, 35, 42, 7, 19, 50 \mid 21]$ | $i = 1$ |
| **$j = 3$** | $A[3] = 35$ | $35 \le 21$ | **FALSE** | None. Advance $j$. | $[14, 28, 35, 42, 7, 19, 50 \mid 21]$ | $i = 1$ |
| **$j = 4$** | $A[4] = 42$ | $42 \le 21$ | **FALSE** | None. Advance $j$. | $[14, 28, 35, 42, 7, 19, 50 \mid 21]$ | $i = 1$ |
| **$j = 5$** | $A[5] = 7$ | $7 \le 21$ | **TRUE** | Increment $i \to 2$. Swap $A[i]=A[2]$ and $A[j]=A[5]$. | $[14, \mathbf{7}, 35, 42, \mathbf{28}, 19, 50 \mid 21]$ | $i = 2$ |
| **$j = 6$** | $A[6] = 19$ | $19 \le 21$ | **TRUE** | Increment $i \to 3$. Swap $A[i]=A[3]$ and $A[j]=A[6]$. | $[14, 7, \mathbf{19}, 42, 28, \mathbf{35}, 50 \mid 21]$ | $i = 3$ |
| **$j = 7$** | $A[7] = 50$ | $50 \le 21$ | **FALSE** | None. Advance $j$. | $[14, 7, 19, 42, 28, 35, 50 \mid 21]$ | $i = 3$ |

##### Phase 3: Final Pivot Placement
- Increment $i \to i + 1 = 3 + 1 = 4$.
- Swap $A[i] = A[4]$ (which is $42$) with pivot $A[r] = A[8]$ (which is $21$).
- Resulting array:
  $$A = [14, 7, 19, \mathbf{21}, 28, 35, 50, 42]$$
- Returned partition split index:
  $$q = 4$$

#### 4. Where did this formula / invariant originate?
From Lomuto's loop invariant:
$$\forall k \in [p..i], \; A[k] \le \text{pivot} \quad \text{and} \quad \forall k \in [i+1..j-1], \; A[k] > \text{pivot}$$

#### 5. What changed from the previous step?
- Pivot element $21$ is placed in its final, sorted position at index $q = 4$.
- Array is partitioned into two subproblems:
  * **Left Subarray ($A[1..3]$):** $[14, 7, 19]$ (size $n_L = 3$).
  * **Right Subarray ($A[5..8]$):** $[28, 35, 50, 42]$ (size $n_R = 4$).
- Total comparisons expended in this call: $r - p = 8 - 1 = \mathbf{7}$.

---

### Step-Card 1.2: Left Branch Recursion — Partitioning $A[1..3]$

#### 1. What are we doing?
Executing `RandomizedPartition(A, p = 1, r = 3)` on subarray:
$$A[1..3] = [14, 7, 19]$$

#### 2. How do we execute the step mechanically?

##### Phase 1: Random Pivot Selection
- Uniform random choice: $k = \text{Random}(1, 3) = 2$.
- Selected element: $A[2] = 7$.
- Swap $A[k] = A[2]$ with $A[r] = A[3]$:
  $$A[1..3] \text{ becomes } [14, 19, \mathbf{7}]$$
- Pivot value: $\text{pivot} = 7$.

##### Phase 2: Lomuto Partitioning
- Initialize $i = p - 1 = 0$.
- Scan $j = 1$: $A[1] = 14 \le 7$ is **FALSE**.
- Scan $j = 2$: $A[2] = 19 \le 7$ is **FALSE**.
- Scan finishes. Increment $i \to 0 + 1 = 1$.
- Swap $A[i] = A[1]$ with $A[r] = A[3]$:
  $$A[1..3] \text{ becomes } [\mathbf{7}, 19, 14]$$
- Partition index returned:
  $$q_1 = 1$$

##### Phase 3: Recursive Subproblems Generated
- Left side: $A[1..0]$ (length $0 \le 0 \implies$ Base case, returns immediately).
- Right side: $A[2..3] = [19, 14]$.
  * In `RandomizedPartition(A, 2, 3)`:
    - Random choice: $k = \text{Random}(2, 3) = 3 \implies \text{pivot} = 14$.
    - Scan $j = 2$: $A[2] = 19 \le 14$ is **FALSE**.
    - Swap $A[2]$ with $A[3] \implies [14, 19]$.
    - Pivot $14$ fixed at index $2$.
  * Left side: $A[2..1]$ (Base case).
  * Right side: $A[3..3] = [19]$ (Base case, size 1).
- Left half is fully sorted:
  $$A[1..3] = [7, 14, 19]$$
- Total comparisons in left branch: $2 + 1 = \mathbf{3}$.

---

### Step-Card 1.3: Right Branch Recursion — Partitioning $A[5..8]$

#### 1. What are we doing?
Executing `RandomizedPartition(A, p = 5, r = 8)` on subarray:
$$A[5..8] = [28, 35, 50, 42]$$

#### 2. How do we execute the step mechanically?

##### Phase 1: Random Pivot Selection
- Uniform random choice: $k = \text{Random}(5, 8) = 6$.
- Selected element: $A[6] = 35$.
- Swap $A[6]$ with $A[8]$:
  $$A[5..8] \text{ becomes } [28, 42, 50, \mathbf{35}]$$
- Pivot value: $\text{pivot} = 35$.

##### Phase 2: Lomuto Partitioning
- Initialize $i = p - 1 = 4$.
- Scan $j = 5$: $A[5] = 28 \le 35$ is **TRUE**. Increment $i \to 5$. Swap $A[5]$ with $A[5]$ (no change).
- Scan $j = 6$: $A[6] = 42 \le 35$ is **FALSE**.
- Scan $j = 7$: $A[7] = 50 \le 35$ is **FALSE**.
- Scan finishes. Increment $i \to 5 + 1 = 6$.
- Swap $A[i] = A[6]$ ($42$) with $A[r] = A[8]$ ($35$):
  $$A[5..8] \text{ becomes } [28, \mathbf{35}, 50, 42]$$
- Partition index returned:
  $$q_2 = 6$$

##### Phase 3: Recursive Subproblems Generated
- Left side: $A[5..5] = [28]$ (Base case, size 1).
- Right side: $A[7..8] = [50, 42]$.
  * In `RandomizedPartition(A, 7, 8)`:
    - Random choice: $k = \text{Random}(7, 8) = 8 \implies \text{pivot} = 42$.
    - Scan $j = 7$: $A[7] = 50 \le 42$ is **FALSE**.
    - Swap $A[7]$ with $A[8] \implies [42, 50]$.
    - Pivot $42$ fixed at index $7$.
  * Left side: $A[7..6]$ (Base case).
  * Right side: $A[8..8] = [50]$ (Base case, size 1).
- Right half is fully sorted:
  $$A[5..8] = [28, 35, 42, 50]$$
- Total comparisons in right branch: $3 + 1 = \mathbf{4}$.

#### Final Sorted Array:
$$A_{\text{sorted}} = [7, 14, 19, 21, 28, 35, 42, 50]$$
Total comparisons across entire execution:
$$X_{\text{actual}} = 7 + 3 + 4 = \mathbf{14 \text{ comparisons}}$$

---

### Step-Card 1.4: Adversarial Contrast — Deterministic Quicksort on Sorted Inputs

::: callout-warning
**The Deterministic Quicksort Pathological Trap**  
If an implementation deterministically selects either the first ($A[p]$) or last ($A[r]$) element as the pivot, an adversary can supply an **already sorted** or **reverse-sorted** array to trigger the worst-case behavior:
$$\mathcal{T}(n) = \Theta(n^2)$$
:::

#### Execution Trace on Pre-Sorted Array:
Consider $A = [7, 14, 19, 21, 28, 35, 42, 50]$ ($n = 8$) under deterministic last-element pivot selection:

```text
========================================================================================================
                         DETERMINISTIC QUICKSORT DEGENERATION ON SORTED ARRAY
========================================================================================================

Level 0:  [ 7, 14, 19, 21, 28, 35, 42 | 50 (PIVOT) ]  ---> 7 comparisons. Split: [7..42] (size 7) and []
Level 1:  [ 7, 14, 19, 21, 28, 35 | 42 (PIVOT) ]      ---> 6 comparisons. Split: [7..35] (size 6) and []
Level 2:  [ 7, 14, 19, 21, 28 | 35 (PIVOT) ]          ---> 5 comparisons. Split: [7..28] (size 5) and []
Level 3:  [ 7, 14, 19, 21 | 28 (PIVOT) ]              ---> 4 comparisons. Split: [7..21] (size 4) and []
Level 4:  [ 7, 14, 19 | 21 (PIVOT) ]                  ---> 3 comparisons. Split: [7..19] (size 3) and []
Level 5:  [ 7, 14 | 19 (PIVOT) ]                      ---> 2 comparisons. Split: [7..14] (size 2) and []
Level 6:  [ 7 | 14 (PIVOT) ]                          ---> 1 comparison.  Split: [7]     (size 1) and []

Total Comparisons = 7 + 6 + 5 + 4 + 3 + 2 + 1 = 28 comparisons!
Recursion Depth   = n = 8 (Linear call stack exhaustion / Risk of Stack Overflow)
========================================================================================================
```

#### Analytical Breakdown of Degeneration:
1. **Recurrence Relation:**
   $$T(n) = T(n - 1) + T(0) + \Theta(n) = T(n - 1) + \Theta(n)$$
2. **Expansion:**
   $$T(n) = \sum_{k=1}^{n-1} k = \frac{(n-1)n}{2} = \frac{n^2 - n}{2} = \Theta(n^2)$$
3. **Why Randomized Quicksort Prevents This:**  
   Because the pivot is selected uniformly at random from the active subarray:
   $$\Pr(\text{Pivot produces worst-case split } (0, n-1)) = \frac{2}{n}$$
   The probability of hitting this worst-case split across all $n$ recursive levels is:
   $$\Pr(\text{Adversarial Quadratic Path}) = \prod_{i=2}^n \frac{2}{i} = \frac{2^{n-1}}{n!} \ll 10^{-15} \quad (\text{for } n \ge 20)$$
   No adversary can supply a fixed input sequence that forces this behavior because the choice of pivot is decoupled from the data ordering.

---

### Step-Card 1.5: Mathematical Proof of Expected Runtime $\mathbb{E}[T(n)] = \Theta(n \log n)$

We prove that the expected number of comparisons made by Randomized Quicksort is $\Theta(n \log n)$ using indicator random variables, with zero skipped steps.

#### Step 1: Formal Variable Setup
1. Let the input elements be $A = \{a_1, a_2, \dots, a_n\}$.
2. Let $Z = \langle z_1, z_2, \dots, z_n \rangle$ denote the set of array elements arranged in their **true, final sorted order**:
   $$z_1 < z_2 < z_3 < \dots < z_{n-1} < z_n$$
3. Let $Z_{ij} = \{z_i, z_{i+1}, \dots, z_j\}$ denote the contiguous sequence of elements between $z_i$ and $z_j$ inclusive, for any $1 \le i < j \le n$.
4. The number of elements in the set $Z_{ij}$ is:
   $$|Z_{ij}| = j - i + 1$$

---

#### Step 2: Formulating Indicator Random Variables
1. Observe that two elements $z_i$ and $z_j$ are compared **at most once** during the entire execution:
   - Elements are only compared to the pivot.
   - Once a pivot is processed, it is placed in its final position and never compared again.
2. Define the indicator random variable $X_{ij}$:
   $$X_{ij} = \mathbb{I}\{z_i \text{ is compared to } z_j\} = \begin{cases} 1, & \text{if } z_i \text{ is compared to } z_j \\ 0, & \text{otherwise} \end{cases}$$
3. The total number of comparisons $X$ across the entire algorithm is:
   $$X = \sum_{i=1}^{n-1} \sum_{j=i+1}^n X_{ij}$$

---

#### Step 3: Determining the Comparison Probability $\Pr(X_{ij} = 1)$
1. Before any element in $Z_{ij}$ is chosen as a pivot, all elements of $Z_{ij}$ belong to the same recursive subproblem.
2. Consider the first time a pivot is chosen from the subset $Z_{ij}$:
   - **Case A:** The chosen pivot is an internal element $z_k$ where $i < k < j$.  
     Then $z_i < z_k$ falls into the left partition, and $z_j > z_k$ falls into the right partition.  
     They are separated into disjoint subarrays and will **never** be compared.
   - **Case B:** The chosen pivot is **either $z_i$ or $z_j$**.  
     That pivot is compared to every other element in the current subproblem, including the other endpoint.  
     Thus, $z_i$ and $z_j$ are compared.
3. Therefore:
   $$\Pr(X_{ij} = 1) = \Pr(\text{The first pivot chosen from } Z_{ij} \text{ is either } z_i \text{ or } z_j)$$
4. Because pivots are chosen uniformly at random, every element in $Z_{ij}$ has an equal probability of being chosen first:
   $$\Pr(\text{Specific element is first pivot}) = \frac{1}{|Z_{ij}|} = \frac{1}{j - i + 1}$$
5. Since the events of selecting $z_i$ and selecting $z_j$ are mutually exclusive:
   $$\Pr(X_{ij} = 1) = \frac{1}{j - i + 1} + \frac{1}{j - i + 1} = \frac{2}{j - i + 1}$$

---

#### Step 4: Linearity of Expectation Derivation
By Linearity of Expectation:
$$\mathbb{E}[X] = \mathbb{E}\left[ \sum_{i=1}^{n-1} \sum_{j=i+1}^n X_{ij} \right] = \sum_{i=1}^{n-1} \sum_{j=i+1}^n \mathbb{E}[X_{ij}]$$

Since $\mathbb{E}[X_{ij}] = 1 \cdot \Pr(X_{ij} = 1) + 0 \cdot \Pr(X_{ij} = 0) = \Pr(X_{ij} = 1)$:
$$\mathbb{E}[X] = \sum_{i=1}^{n-1} \sum_{j=i+1}^n \frac{2}{j - i + 1}$$

We evaluate this double summation algebraically:
1. Introduce a substitution for the inner sum. Let:
   $$k = j - i$$
   Since $j$ ranges from $i + 1$ to $n$:
   - When $j = i + 1$, $k = (i + 1) - i = 1$.
   - When $j = n$, $k = n - i$.
2. The denominator becomes:
   $$j - i + 1 = k + 1$$
3. Substitute $k$ into the summation:
   $$\mathbb{E}[X] = \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{2}{k + 1}$$
4. Factor out the constant factor of 2:
   $$\mathbb{E}[X] = 2 \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{1}{k + 1}$$
5. For all $i \ge 1$, the upper limit satisfies $n - i < n$:
   $$\sum_{k=1}^{n-i} \frac{1}{k + 1} < \sum_{k=1}^{n-1} \frac{1}{k + 1} = \sum_{m=2}^n \frac{1}{m} = \left(\sum_{m=1}^n \frac{1}{m}\right) - 1 = H_n - 1$$
   where $H_n = \sum_{m=1}^n \frac{1}{m}$ is the $n$-th **Harmonic Number**.
6. Replace the inner sum with the upper bound $H_n$:
   $$\mathbb{E}[X] \le 2 \sum_{i=1}^{n-1} H_n = 2 H_n \sum_{i=1}^{n-1} 1 = 2(n - 1)H_n < 2n H_n$$
7. Using the integral upper bound for the Harmonic series:
   $$H_n = \sum_{m=1}^n \frac{1}{m} \le 1 + \int_1^n \frac{1}{x} \, dx = 1 + \ln n$$
8. Substitute this into the inequality:
   $$\mathbb{E}[X] < 2n (\ln n + 1) = 2n \ln n + 2n$$
9. Using the logarithmic base conversion $\ln n = \frac{\log_2 n}{\log_2 e} = (\ln 2)(\log_2 n) \approx 0.693 \log_2 n$:
   $$\mathbb{E}[X] < 2n (0.693 \log_2 n) + 2n \approx 1.386 \, n \log_2 n + \mathcal{O}(n)$$
10. Therefore, the expected total running time satisfies:
    $$\mathbb{E}[T(n)] = \Theta(n + \mathbb{E}[X]) = \mathbf{\Theta(n \log n)}$$
This holds for **any** input array configuration. $\blacksquare$

---

## 3. Level 2: Karger's Randomized Min-Cut Contraction

### Problem 2.1 Specification
Let $G = (V, E)$ be a connected, undirected multigraph with:
- **Vertex Set ($|V| = n = 4$):** $V = \{A, B, C, D\}$
- **Edge Set ($|E| = m = 5$):**
  $$e_1 = (A, B), \quad e_2 = (A, C), \quad e_3 = (B, C), \quad e_4 = (B, D), \quad e_5 = (C, D)$$

```text
========================================================================================================
                                     INPUT MULTIGRAPH TOPOLOGY G = (V, E)
========================================================================================================

             (A)-----------------(B)
              |  \             /  |
              |    \         /    |
              |      \     /      |
          e_2 |        \ /        | e_4
              |        / \        |
              |      /     \      |
              |    /   e_3   \    |
              |  /             \  |
             (C)-----------------(D)
                       e_5

   Edge Inventory (m = 5):
   e_1 = (A, B)
   e_2 = (A, C)
   e_3 = (B, C)
   e_4 = (B, D)
   e_5 = (C, D)
   
   Vertex Degrees:
   deg(A) = 2,  deg(B) = 3,  deg(C) = 3,  deg(D) = 2
   Degree Sum = 2 + 3 + 3 + 2 = 10 = 2m (Verified by Handshaking Lemma)
========================================================================================================
```

Our objective is to:
1. Trace **Karger's Contraction Algorithm** step-by-step through a successful run that uncovers the true global minimum cut.
2. Trace an alternative run that demonstrates an algorithm failure.
3. Derive the exact mathematical success probability $P(\text{success}) \ge \frac{2}{n(n-1)} = \frac{1}{\binom{n}{2}}$.
4. Prove that repeating the algorithm $T = \binom{n}{2} \ln n$ times reduces the failure probability to less than $\frac{1}{n}$.

---

### Step-Card 2.1: Execution Trace A — Successful Contraction to Global Min-Cut

#### 1. What are we doing?
Tracing Karger's contraction on multigraph $G$ until exactly 2 super-nodes remain.

#### 2. Why are we starting here?
The algorithm iteratively contracts a uniformly selected random edge until the vertex count drops from $n = 4$ down to $2$.

#### 3. How do we execute the step mechanically?

---

#### Contraction Iteration 1 ($n = 4 \to n = 3$):
- **Current Edge Pool:** $\{e_1, e_2, e_3, e_4, e_5\}$, with $|E| = 5$.
- **Random Selection:** Let the uniform selector pick edge:
  $$e^*_1 = e_3 = (B, C)$$
- **Contraction Mechanics:**
  1. Merge vertex $B$ and vertex $C$ into a single composite super-node:
     $$BC = \{B, C\}$$
  2. Edge $e_3 = (B, C)$ now connects $BC$ to itself, forming a **self-loop**.  
     **Remove $e_3$**.
  3. Re-map all remaining incident edges to super-node $BC$:
     - Edge $e_1 = (A, B) \implies (A, BC)$
     - Edge $e_2 = (A, C) \implies (A, BC)$
     - Edge $e_4 = (B, D) \implies (BC, D)$
     - Edge $e_5 = (C, D) \implies (BC, D)$
- **Multigraph State after Iteration 1:**
  - Vertices: $V' = \{A, BC, D\}$ ($|V'| = 3$).
  - Multi-edges:
    * Two parallel edges between $A$ and $BC$: $e_1, e_2$.
    * Two parallel edges between $BC$ and $D$: $e_4, e_5$.
  - Total remaining edges: $4$.

```text
========================================================================================================
                              INTERMEDIATE GRAPH AFTER CONTRACTION 1 (EDGE B-C)
========================================================================================================

                 e_1                         e_4
           (A)========= [ BC ] =========(D)
                 e_2                         e_5
                 
   Remaining Vertices: { A, BC, D }  (|V'| = 3)
   Remaining Edges:    4 edges (Parallel pairs: {e_1, e_2} and {e_4, e_5})
========================================================================================================
```

---

#### Contraction Iteration 2 ($n = 3 \to n = 2$):
- **Current Edge Pool:** $\{e_1, e_2, e_4, e_5\}$, with $|E| = 4$.
- **Random Selection:** Let the uniform selector pick edge:
  $$e^*_2 = e_1 = (A, BC)$$
- **Contraction Mechanics:**
  1. Merge vertex $A$ and super-node $BC$ into a larger super-node:
     $$ABC = \{A, B, C\}$$
  2. Edge $e_1$ was the contracted edge $\implies$ **Remove**.
  3. Edge $e_2$ originally connected $A$ and $C$. Since both $A, C \in ABC$, edge $e_2$ is now a **self-loop** $\implies$ **Remove**.
  4. Retain edges connecting $ABC$ to external vertices:
     - Edge $e_4 = (BC, D) \implies (ABC, D)$
     - Edge $e_5 = (C, D) \implies (ABC, D)$
- **Multigraph State after Iteration 2:**
  - Vertices: $V'' = \{ABC, D\}$ ($|V''| = 2$).
  - Multi-edges: $\{e_4, e_5\}$ connecting $ABC$ and $D$.
  - Total remaining edges: $2$.

```text
========================================================================================================
                              FINAL GRAPH AFTER CONTRACTION 2 (TERMINATION)
========================================================================================================

                                  e_4
                      [ ABC ] ============= (D)
                                  e_5

   Remaining Super-Nodes: S_1 = {A, B, C},  S_2 = {D}
   Crossing Cut Edges:    { e_4, e_5 }  (Cardinality = 2)
========================================================================================================
```

---

#### Termination and Cut Extraction:
1. Exactly $2$ super-nodes remain:
   $$(S, V \setminus S) = (\{A, B, C\}, \{D\})$$
2. Count the crossing edges:
   $$\text{Cut Edges} = \{e_4, e_5\} = \{(B, D), (C, D)\}$$
3. Computed Min-Cut Value:
   $$\text{Cut Size} = \mathbf{2}$$

---

### Step-Card 2.2: Comprehensive Audit of All Feasible Cuts in Graph $G$

To verify whether the cut size of $2$ is the true global minimum, we enumerate all $2^{n-1} - 1 = 2^{4-1} - 1 = 7$ non-trivial cuts:

| Cut Index ($k$) | Subset Partition $(S, V \setminus S)$ | Crossing Edges | Cut Cardinality | Classification |
| :---: | :---: | :---: | :---: | :--- |
| **Cut 1** | $\{A\} \;\mid\; \{B, C, D\}$ | $(A, B), (A, C)$ | **2** | **GLOBAL MINIMUM CUT** |
| **Cut 2** | $\{B\} \;\mid\; \{A, C, D\}$ | $(A, B), (B, C), (B, D)$ | $3$ | Sub-optimal Cut |
| **Cut 3** | $\{C\} \;\mid\; \{A, B, D\}$ | $(A, C), (B, C), (C, D)$ | $3$ | Sub-optimal Cut |
| **Cut 4** | $\{D\} \;\mid\; \{A, B, C\}$ | $(B, D), (C, D)$ | **2** | **GLOBAL MINIMUM CUT (Found in Trace A)** |
| **Cut 5** | $\{A, B\} \;\mid\; \{C, D\}$ | $(A, C), (B, C), (B, D)$ | $3$ | Sub-optimal Cut |
| **Cut 6** | $\{A, C\} \;\mid\; \{B, D\}$ | $(A, B), (B, C), (C, D)$ | $3$ | Sub-optimal Cut |
| **Cut 7** | $\{A, D\} \;\mid\; \{B, C\}$ | $(A, B), (A, C), (B, D), (C, D)$ | $4$ | Maximum Cut |

#### Ground Truth:
The global minimum cut capacity of graph $G$ is:
$$k = \mathbf{2}$$
There are two distinct minimum cut partitions: Cut 1 ($\{A\} \mid \{B, C, D\}$) and Cut 4 ($\{D\} \mid \{A, B, C\}$).  
Trace A successfully found Cut 4.

---

### Step-Card 2.3: Execution Trace B — Algorithmic Failure Mode

#### 1. What are we doing?
Demonstrating how a poor random choice contracts a min-cut edge, causing Karger's algorithm to return a sub-optimal cut.

#### 2. How do we execute the step mechanically?

##### Iteration 1: Selection of Edge $e_4 = (B, D)$
- Random choice: The algorithm picks edge $e_4 = (B, D) \in E$.
- Contract $B$ and $D$ into super-node $BD = \{B, D\}$.
- Edge $e_4$ becomes a self-loop and is removed.
- Remaining edges:
  * $e_1 = (A, B) \implies (A, BD)$
  * $e_2 = (A, C) \implies (A, C)$
  * $e_3 = (B, C) \implies (BD, C)$
  * $e_5 = (C, D) \implies (C, BD)$
- Active edges: $\{e_1, e_2, e_3, e_5\}$.

##### Iteration 2: Selection of Edge $e_2 = (A, C)$
- Random choice: The algorithm picks edge $e_2 = (A, C)$.
- Contract $A$ and $C$ into super-node $AC = \{A, C\}$.
- Edge $e_2$ becomes a self-loop and is removed.
- Remaining edges connecting $AC$ and $BD$:
  * $e_1$: connects $A \in AC$ to $B \in BD \implies (AC, BD)$
  * $e_3$: connects $C \in AC$ to $B \in BD \implies (AC, BD)$
  * $e_5$: connects $C \in AC$ to $D \in BD \implies (AC, BD)$
- Terminate: Exactly 2 super-nodes remain: $AC = \{A, C\}$ and $BD = \{B, D\}$.

##### Output of Trace B:
- Cut Partition:
  $$(S, V \setminus S) = (\{A, C\}, \{B, D\})$$
- Crossing Edges: $\{e_1, e_3, e_5\}$
- Returned Cut Size:
  $$\text{Cut Size} = \mathbf{3} > k(2) \quad \implies \quad \text{\textbf{ALGORITHM FAILED (Returned Sub-optimal Cut)}}$$

#### Root Cause:
Edge $e_4 = (B, D)$ was a crossing edge of the target minimum cut $\{A, B, C\} \mid \{D\}$. By selecting and contracting $e_4$ in Iteration 1, the algorithm destroyed that minimum cut.

---

### Step-Card 2.4: Formal Mathematical Proof of Success Probability Bound

#### Theorem 2.1 (Karger's Contraction Invariant)
*Let $G = (V, E)$ be an undirected multigraph with $|V| = n$ vertices. A single run of Karger's Contraction Algorithm discovers a specific minimum cut $C^*$ with probability at least:*
$$\Pr(\text{Success}) \ge \frac{2}{n(n-1)} = \frac{1}{\binom{n}{2}}$$

#### Complete Proof with Zero Logical Leaps:

##### Step 1: Degree Formulation of Cut Lower Bound
1. Let $C^*$ be a specific minimum cut of $G$, and let $k = |C^*|$ be the size of this cut.
2. The removal of $C^*$ disconnects $G$ into two components $(S, V \setminus S)$.
3. Because $C^*$ is the *minimum* cut, the degree of every single vertex $v \in V$ must be at least $k$:
   $$\deg(v) \ge k \quad \forall \; v \in V$$
   *(If some vertex $u$ had $\deg(u) < k$, the singleton cut $(\{u\}, V \setminus \{u\})$ would have size $\deg(u) < k$, contradicting the assumption that $k$ is minimal).*
4. By the Handshaking Lemma, the sum of all vertex degrees equals twice the number of edges $|E| = m$:
   $$\sum_{v \in V} \deg(v) = 2m$$
5. Substituting the inequality $\deg(v) \ge k$:
   $$2m = \sum_{v \in V} \deg(v) \ge \sum_{v \in V} k = n \cdot k$$
6. Dividing by 2 yields a lower bound on the total number of edges in $G$:
   $$m \ge \frac{n \cdot k}{2}$$

---

##### Step 2: Probability of Preserving $C^*$ in Iteration 1
1. Cut $C^*$ survives the first contraction if and only if the edge chosen for contraction does **not** belong to $C^*$.
2. The algorithm selects an edge uniformly at random from the $m$ available edges.
3. The number of edges belonging to $C^*$ is exactly $k$.
4. Let $\mathcal{E}_1$ denote the event that the edge contracted in Step 1 is not in $C^*$:
   $$\Pr(\neg \mathcal{E}_1) = \frac{|C^*|}{m} = \frac{k}{m}$$
5. Substituting the bound $m \ge \frac{nk}{2}$:
   $$\Pr(\neg \mathcal{E}_1) \le \frac{k}{\frac{nk}{2}} = \frac{2}{n}$$
6. Therefore, the probability that $C^*$ survives the first iteration is:
   $$\Pr(\mathcal{E}_1) = 1 - \Pr(\neg \mathcal{E}_1) \ge 1 - \frac{2}{n} = \frac{n - 2}{n}$$

---

##### Step 3: Conditional Chain Rule Across all $n - 2$ Contractions
1. Let $r$ denote the number of remaining super-nodes. Initially $r = n$.
2. In each contraction step, two super-nodes are merged, reducing the vertex count by 1:
   $$r \in \{n, n-1, n-2, \dots, 3\}$$
3. When $r$ super-nodes remain, no super-node can have a degree less than $k$ (otherwise that super-node would define a cut smaller than $k$).
4. Therefore, the number of edges remaining at step $i$ (when $n - i + 1$ vertices remain) satisfies:
   $$m_i \ge \frac{(n - i + 1) \cdot k}{2}$$
5. Let $\mathcal{E}_i$ be the event that the $i$-th contracted edge does not belong to $C^*$.
6. The conditional probability that $C^*$ survives the $i$-th contraction, given that it survived all previous steps, is:
   $$\Pr(\mathcal{E}_i \mid \mathcal{E}_1 \cap \dots \cap \mathcal{E}_{i-1}) \ge 1 - \frac{k}{m_i} \ge 1 - \frac{k}{\frac{(n - i + 1)k}{2}} = 1 - \frac{2}{n - i + 1} = \frac{n - i - 1}{n - i + 1}$$

---

##### Step 4: Telescoping the Probability Product
Cut $C^*$ survives to the end if and only if it survives all $n - 2$ contractions:
$$\Pr(\text{Success}) = \Pr(\mathcal{E}_1 \cap \mathcal{E}_2 \cap \dots \cap \mathcal{E}_{n-2})$$

Applying the conditional probability chain rule:
$$\Pr(\text{Success}) = \Pr(\mathcal{E}_1) \cdot \Pr(\mathcal{E}_2 \mid \mathcal{E}_1) \cdot \Pr(\mathcal{E}_3 \mid \mathcal{E}_1 \cap \mathcal{E}_2) \cdots \Pr(\mathcal{E}_{n-2} \mid \bigcap_{j=1}^{n-3} \mathcal{E}_j)$$

Substituting each term:
- For $i = 1$ ($r = n$): $\Pr(\mathcal{E}_1) \ge \frac{n - 2}{n}$
- For $i = 2$ ($r = n - 1$): $\Pr(\mathcal{E}_2 \mid \mathcal{E}_1) \ge \frac{n - 3}{n - 1}$
- For $i = 3$ ($r = n - 2$): $\Pr(\mathcal{E}_3 \mid \mathcal{E}_1 \cap \mathcal{E}_2) \ge \frac{n - 4}{n - 2}$
- $\dots$
- For $i = n - 3$ ($r = 4$): Term is $\frac{4 - 2}{4} = \frac{2}{4}$
- For $i = n - 2$ ($r = 3$): Term is $\frac{3 - 2}{3} = \frac{1}{3}$

Writing out the full product:
$$\Pr(\text{Success}) \ge \left( \frac{n - 2}{n} \right) \left( \frac{n - 3}{n - 1} \right) \left( \frac{n - 4}{n - 2} \right) \left( \frac{n - 5}{n - 3} \right) \cdots \left( \frac{2}{4} \right) \left( \frac{1}{3} \right)$$

Observe the **telescoping cancellation**:
- The numerator $(n - 2)$ cancels with the denominator of the 3rd term $(n - 2)$.
- The numerator $(n - 3)$ cancels with the denominator of the 4th term $(n - 3)$.
- Every term cancels except:
  * The numerators of the final two terms: $2$ and $1$.
  * The denominators of the initial two terms: $n$ and $n - 1$.

Carrying out the cancellation:
$$\Pr(\text{Success}) \ge \frac{2 \times 1}{n \times (n - 1)} = \frac{2}{n(n - 1)} = \frac{1}{\binom{n}{2}}$$

For our $n = 4$ problem:
$$\Pr(\text{Success}) \ge \frac{2}{4(3)} = \frac{2}{12} = \mathbf{\frac{1}{6} \approx 16.67\%} \quad \blacksquare$$

---

### Step-Card 2.5: Error Probability Amplification

A success probability of $p \ge \frac{2}{n^2}$ is small for large $n$. However, because Karger's algorithm runs in polynomial time, we can run it multiple times independently and record the minimum cut found across all runs.

#### 1. Mathematical Formulation of Independent Repetitions
Let the algorithm be executed $T$ times independently on graph $G$.  
Let $C_{\min}$ be the smallest cut discovered across all $T$ iterations:
$$C_{\min} = \min_{1 \le t \le T} \text{Cut}_t$$

The overall procedure fails if and only if **every single run fails** to discover the true minimum cut $C^*$:
$$\Pr(\text{Failure after } T \text{ runs}) = \prod_{t=1}^T \Pr(\text{Run } t \text{ fails})$$

Since runs are independent:
$$\Pr(\text{Failure}) \le (1 - p)^T \quad \text{where } p \ge \frac{2}{n(n-1)} > \frac{2}{n^2}$$

---

#### 2. Derivation of the Number of Iterations $T$
Using the standard exponential inequality:
$$1 - x \le e^{-x} \quad \forall \; x \in \mathbb{R}$$
Substituting $x = p$:
$$\Pr(\text{Failure}) \le \left( 1 - \frac{2}{n^2} \right)^T \le \left( e^{-2/n^2} \right)^T = e^{-\frac{2T}{n^2}}$$

##### Goal: Reduce Failure Probability to at most $\delta = \frac{1}{n}$
We set the failure bound:
$$e^{-\frac{2T}{n^2}} \le \frac{1}{n}$$
Taking the natural logarithm ($\ln$) on both sides:
$$\ln\left( e^{-\frac{2T}{n^2}} \right) \le \ln\left( \frac{1}{n} \right)$$
$$-\frac{2T}{n^2} \le -\ln n$$
Multiply by $-1$ (which reverses the inequality):
$$\frac{2T}{n^2} \ge \ln n \iff T \ge \frac{n^2}{2} \ln n = \binom{n}{2} \ln n$$

##### Goal: Reduce Failure Probability to at most $\delta = \frac{1}{n^k}$
$$e^{-\frac{2T}{n^2}} \le n^{-k} \implies -\frac{2T}{n^2} \le -k \ln n \iff T \ge \frac{k}{2} n^2 \ln n$$

---

#### 3. Numerical Demonstration for $n = 4$:
- Single-run failure probability:
  $$1 - p \le 1 - \frac{1}{6} = \frac{5}{6} \approx 83.33\%$$
- Number of runs for target $\delta \le \frac{1}{4} = 0.25$:
  $$T \ge \binom{4}{2} \ln(4) = 6 \times 1.386 \approx 8.31 \implies \text{Choose } T = 9 \text{ runs}$$
- Actual failure probability after 9 runs:
  $$\Pr(\text{Failure}) \le \left( \frac{5}{6} \right)^9 = \frac{1,953,125}{10,077,696} \approx \mathbf{0.1938} \le 0.25$$
- Overall success probability:
  $$\Pr(\text{Success}) \ge 1 - 0.1938 = \mathbf{80.62\%}$$

---

## 4. Algorithmic Pseudocode

### 4.1 Randomized Quicksort Specification

```text
Algorithm RandomizedPartition(A, p, r)
// Input: Array A, subsegment indices p and r
// Output: Split index q such that A[p..q-1] <= A[q] <= A[q+1..r]
begin
    // Step 1: Select pivot uniformly at random
    k := Random(p, r);
    
    // Step 2: Swap chosen pivot to rightmost position
    swap(A[k], A[r]);
    pivot := A[r];
    
    // Step 3: Standard Lomuto Partitioning
    i := p - 1;
    for j := p to r - 1 do
        if (A[j] <= pivot) then
            i := i + 1;
            swap(A[i], A[j]);
        end if;
    end for;
    
    // Step 4: Place pivot in final sorted location
    swap(A[i + 1], A[r]);
    return i + 1;
end;

Algorithm RandomizedQuickSort(A, p, r)
begin
    if (p < r) then
        q := RandomizedPartition(A, p, r);
        RandomizedQuickSort(A, p, q - 1);
        RandomizedQuickSort(A, q + 1, r);
    end if;
end;
```

---

### 4.2 Karger's Min-Cut Specification

```text
Algorithm KargerMinCut(G = (V, E))
// Input: Connected multigraph G with n vertices and m edges
// Output: A cut (S, V \ S) and its capacity
begin
    Initialize SuperNodes := { {v} for each v in V };
    CurrentVertices := |V|;
    
    while (CurrentVertices > 2) do
        // Step 1: Uniformly select a random edge e = (u, v) from E
        select e = (u, v) uniformly at random from E;
        
        // Step 2: Identify super-nodes containing endpoints u and v
        SuperU := FindSet(u);
        SuperV := FindSet(v);
        
        if (SuperU ≠ SuperV) then
            // Contract super-nodes SuperU and SuperV into a single super-node
            Union(SuperU, SuperV);
            CurrentVertices := CurrentVertices - 1;
            
            // Remove self-loops (edges whose endpoints now lie in the same super-node)
            for each edge (x, y) in E do
                if (FindSet(x) = FindSet(y)) then
                    E := E \ {(x, y)};
                end if;
            end for;
        end if;
    end while;
    
    // Step 3: Return the remaining crossing edges between the 2 super-nodes
    return |E|;
end;

Algorithm AmplifiedKarger(G, n)
begin
    best_cut := infinity;
    T := (n * (n - 1) / 2) * ceil(ln(n));
    
    for t := 1 to T do
        cut_candidate := KargerMinCut(G_copy);
        if (cut_candidate < best_cut) then
            best_cut := cut_candidate;
        end if;
    end for;
    
    return best_cut;
end;
```

---

## 5. Master Comparative Verification Matrix

```text
+======================================================================================================================+
|                                    MASTER RANDOMIZED ALGORITHMS MATRIX                                               |
+==================+======================+====================+======================+================================+
| Algorithm        | Problem Domain       | Paradigm Class     | Key Random Variable  | Theoretical Performance Bound  |
+==================+======================+====================+======================+================================+
| Randomized       | Sorting Array of     | Las Vegas          | Execution Time /     | E[T(n)] = 2n ln n + O(n)       |
| Quicksort        | Cardinality n        | (Zero Error)       | Comparisons X        | = Θ(n log n) (All Inputs)      |
+------------------+----------------------+--------------------+----------------------+--------------------------------+
| Deterministic    | Sorting Array of     | Deterministic      | None                 | Best: O(n log n)               |
| Quicksort        | Cardinality n        | (Can be exploitable|                      | Worst: Θ(n^2) on sorted inputs |
+------------------+----------------------+--------------------+----------------------+--------------------------------+
| Karger's Min-Cut | Global Min-Cut in    | Monte Carlo        | Solution Correctness | Single Run: P(succ) ≥ 2/(n^2)  |
| (Single Run)     | Undirected Multigraph| (Bounded Error)    | (Cut Preservation)   | Runtime: O(n^2) using Disjoint |
+------------------+----------------------+--------------------+----------------------+--------------------------------+
| Karger's Min-Cut | Global Min-Cut in    | Monte Carlo        | Number of Successes  | P(Error) ≤ 1/n                 |
| (Amplified)      | Undirected Multigraph| (Amplified)        | across T runs        | Runs: T = O(n^2 ln n)          |
+==================+======================+====================+======================+================================+
```

---

## 6. KTU Examination Scoring Blueprint (10-Mark Rubric)

When a question on Randomized Quicksort and Karger's Min-Cut appears in KTU exams under course code **PCCST502 / CST306**, marks are allocated strictly according to the following evaluation criteria:

| Evaluation Phase | Expected Answer Components | Allocated Marks |
| :--- | :--- | :---: |
| **Phase 1: Randomized Quicksort Trace & Lomuto Walkthrough** | Correct step-by-step trace of `RandomizedPartition` on array $A=[28, 14, 35, 42, 7, 19, 50, 21]$, showing random pivot selection, pointer updates ($i, j$), swaps, and returned partition index $q=4$. | **2 Marks** |
| **Phase 2: Adversarial Degeneration Analysis** | Explanation of how deterministic Quicksort degrades to $\Theta(n^2)$ and recursion depth $n$ on already sorted inputs, and how uniform pivot selection avoids this trap. | **2 Marks** |
| **Phase 3: Formal Indicator Proof of Expected Comparisons** | Full algebraic derivation using indicator random variables $X_{ij}$, proof that $\Pr(X_{ij} = 1) = \frac{2}{j - i + 1}$, change-of-variable summation, Harmonic bounds, and concluding $\mathbb{E}[X] \le 2n \ln n = \Theta(n \log n)$. | **3 Marks** |
| **Phase 4: Karger Contraction Execution Trace** | Step-by-step contraction trace on the 4-vertex multigraph, showing edge selections, super-node merging, removal of self-loops, and final crossing cut count. | **2 Marks** |
| **Phase 5: Success Probability & Error Amplification** | Derivation of single-run success probability $\Pr(\text{Success}) \ge \frac{2}{n(n-1)}$ via telescoping product, and mathematical proof showing $T = \binom{n}{2} \ln n$ repetitions reduce failure probability to $< 1/n$. | **1 Mark** |
| **Total Marks** | | **10 Marks** |
