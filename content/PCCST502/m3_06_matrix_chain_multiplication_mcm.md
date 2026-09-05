# Module 3.6: Matrix Chain Multiplication (MCM) — Optimization via Dynamic Programming
**Course Code: PCCST502 | Design and Analysis of Algorithms | KTU 2024 Scheme**

---

### Table of Contents
1. [Foundational Problem Mechanics](#foundational-mechanics)
   - [Matrix Multiplication Dimensions & Computational Cost](#multiplication-cost)
   - [The Associative Property & Parenthesization Combinatorics](#parenthesization-combinatorics)
   - [The Catalan Number Explosion: Derivation & Stirling's Approximation](#catalan-derivation)
2. [Dynamic Programming Formulation](#dp-formulation)
   - [Characterizing Optimal Substructure (The Split-Index $k$)](#optimal-substructure)
   - [The Bellman Recurrence Relation for $m[i, j]$](#bellman-recurrence)
   - [The Split Matrix $s[i, j]$ (Tracking Optimal Parentheses)](#split-matrix)
3. [Algorithm Design & Subproblem Dependency Geometry](#algorithm-design)
   - [Why Standard Row-Major Traversal Fails (The Diagonal Traversal Requirement)](#diagonal-traversal)
   - [Complete Pseudocode: `MatrixChainOrder` and `PrintOptimalParens`](#pseudocode)
   - [Rigorous Asymptotic Complexity Analysis ($\Theta(n^3)$ Time, $\Theta(n^2)$ Space)](#complexity-analysis)
4. [Step-by-Step 5W1H Stepped Execution Trace](#execution-trace)
   - [Reference 4-Matrix Sequence Specification](#reference-sequence)
   - [Stepped Diagonal Fill ($l = 2, 3, 4$) using 5W1H Methodology](#stepped-fill)
   - [Final Cost Matrix $M$ and Split Matrix $S$](#final-matrices)
   - [Optimal Parenthesization Reconstruction Walkthrough](#reconstruction-walkthrough)
5. [KTU Exam High-Yield Summary](#exam-summary)
   - [Frequently Asked 3-Mark Questions & Model Answers](#three-mark-questions)
   - [High-Frequency Student Pitfalls & Marking Traps](#marking-traps)

---

<a id="foundational-mechanics"></a>
## 1. Foundational Problem Mechanics

<a id="multiplication-cost"></a>
### Matrix Multiplication Dimensions & Computational Cost

Let $A$ be a matrix of dimensions $p \times q$ and let $B$ be a matrix of dimensions $q \times r$. 
The matrix product $C = A \times B$ is well-defined if and only if the number of columns in $A$ matches the number of rows in $B$ (compatibility condition). The resulting product matrix $C$ has dimensions $p \times r$.

```
                     STANDARD MATRIX MULTIPLICATION COMPATIBILITY
                     
            Matrix A                     Matrix B                 Product Matrix C
         [ p x q ]         x          [ q x r ]         =         [ p x r ]
         
       p rows, q cols               q rows, r cols              p rows, r cols
       +------------+               +------------+              +------------+
       |            |               |            |              |            |
     p |            |             q |            |            p |            |
       |            |               |            |              |            |
       +------------+               +------------+              +------------+
             q                            r                           r
             
       Compatibility Constraint: Inner dimension q must match identically!
       Total Scalar Multiplications = p * q * r
```

#### The Scalar Multiplication Cost Function:
Under the standard textbook matrix multiplication algorithm, computing each of the $p \times r$ entries in $C$ requires $q$ scalar multiplications and $q - 1$ scalar additions:
$$C_{ij} = \sum_{k=1}^q A_{ik} B_{kj}$$

Because scalar additions run in proportional time and scalar multiplications are computationally dominant, we measure computational cost strictly by the **total number of scalar multiplications**:
$$\text{Cost}(A \times B) = p \cdot q \cdot r$$

---

<a id="parenthesization-combinatorics"></a>
### The Associative Property & Parenthesization Combinatorics

Matrix multiplication is **associative**. For any compatible sequence of matrices $A, B, C$:
$$(A \times B) \times C = A \times (B \times C)$$

However, matrix multiplication is **not commutative** ($A \times B \ne B \times A$). 
While the final product matrix is identical regardless of how parentheses are placed, the **computational cost (number of scalar multiplications) varies dramatically**.

#### Concrete Demonstration of Cost Sensitivity:
Consider three matrices $\langle A_1, A_2, A_3 \rangle$ with dimensions:
* $A_1$: $10 \times 100$
* $A_2$: $100 \times 5$
* $A_3$: $5 \times 50$

We compare the two valid parenthesizations:

```
                    PARENTHESIZATION COST DISCREPANCY
                    
      Parenthesization 1: ((A_1 x A_2) x A_3)        Parenthesization 2: (A_1 x (A_2 x A_3))
      
      Step 1: Compute (A_1 x A_2)                   Step 1: Compute (A_2 x A_3)
        Dims: (10 x 100) x (100 x 5)                  Dims: (100 x 5) x (5 x 50)
        Cost: 10 * 100 * 5 = 5,000                    Cost: 100 * 5 * 50 = 25,000
        Result Dims: 10 x 5                           Result Dims: 100 x 50
        
      Step 2: Multiply by A_3                       Step 2: Multiply A_1 by result
        Dims: (10 x 5) x (5 x 50)                     Dims: (10 x 100) x (100 x 50)
        Cost: 10 * 5 * 50 = 2,500                     Cost: 10 * 100 * 50 = 50,000
        
      TOTAL COST: 5,000 + 2,500 = 7,500             TOTAL COST: 25,000 + 50,000 = 75,000
```

Parenthesization 1 is **10 times faster** than Parenthesization 2 ($7,500$ vs $75,000$ operations). For longer chains of matrices, the difference between optimal and poor parenthesizations can span many orders of magnitude.

#### The Matrix Chain Multiplication (MCM) Problem:
Given a sequence (chain) of $n$ matrices $\langle A_1, A_2, \dots, A_n \rangle$, where matrix $A_i$ has dimensions $p_{i-1} \times p_i$ for $i \in \{1, \dots, n\}$, determine a parenthesization that minimizes the total number of scalar multiplications required to compute the product $A_1 A_2 \dots A_n$.

*(Note: The MCM problem does not perform the multiplications; it determines the optimal ordering in which to perform them).*

---

<a id="catalan-derivation"></a>
### The Catalan Number Explosion: Derivation & Stirling's Approximation

Why not simply enumerate all possible parenthesizations and pick the best one?

Let $P(n)$ denote the number of alternative parenthesizations of a sequence of $n$ matrices.
* When $n = 1$, there is only one matrix: $P(1) = 1$.
* When $n \ge 2$, a full parenthesization splits the chain between the $k$-th and $(k+1)$-th matrices for some $k \in \{1, 2, \dots, n-1\}$:
  $$(A_1 A_2 \dots A_k) \times (A_{k+1} A_{k+2} \dots A_n)$$
Because the two sub-chains can be parenthesized independently, the total number of ways to parenthesize the split is $P(k) \cdot P(n-k)$.

Summing over all possible split positions $k$:
$$P(n) = \begin{cases} 
1 & \text{if } n = 1, \\
\sum_{k=1}^{n-1} P(k) \cdot P(n-k) & \text{if } n \ge 2.
\end{cases}$$

This recurrence defines the **Catalan Numbers**:
$$P(n) = C_{n-1} = \frac{1}{n} \binom{2n - 2}{n - 1}$$

#### Growth Rate via Stirling's Approximation:
Applying Stirling's approximation ($n! \approx \sqrt{2\pi n} \left(\frac{n}{e}\right)^n$):
$$C_{n-1} \approx \frac{4^{n-1}}{\sqrt{\pi} (n-1)^{3/2}} = \mathbf{\Omega\left(\frac{4^n}{n^{3/2}}\right)}$$

<div class="table-wrap">

| Chain Length ($n$) | Number of Matrices | Alternative Parenthesizations ($P(n)$) |
| :---: | :---: | :---: |
| $n = 1$ | $1$ | $1$ |
| $n = 2$ | $2$ | $1$ |
| $n = 3$ | $3$ | $2$ |
| $n = 4$ | $4$ | $5$ |
| $n = 5$ | $5$ | $14$ |
| $n = 10$ | $10$ | $4,862$ |
| $n = 15$ | $15$ | $2,674,440$ |
| $n = 20$ | $20$ | $1,767,263,190$ |

</div>

Because $P(n)$ grows as $\Omega(4^n / n^{3/2})$, exhaustive brute-force search is computationally infeasible for large $n$. We turn to **Dynamic Programming**.

---

<a id="dp-formulation"></a>
## 2. Dynamic Programming Formulation

<a id="optimal-substructure"></a>
### Characterizing Optimal Substructure (The Split-Index $k$)

To apply Dynamic Programming, we first verify the **Optimal Substructure** property:

Let $A_{i..j}$ denote the product matrix resulting from multiplying the sub-chain $A_i A_{i+1} \dots A_j$ for $1 \le i \le j \le n$. 
Any parenthesization of $A_{i..j}$ must split the product at some index $k$ such that $i \le k < j$:
$$A_{i..j} = (A_i A_{i+1} \dots A_k) \times (A_{k+1} A_{k+2} \dots A_j) = A_{i..k} \times A_{k+1..j}$$

```
                     MCM OPTIMAL SUBSTRUCTURE SPLIT
                     
       Sub-chain A_{i..j} :   A_i   A_{i+1} ... A_k   A_{k+1} ... A_{j-1}   A_j
                              \_______________/   \___________________/
                                  Subproblem 1         Subproblem 2
                                    A_{i..k}            A_{k+1..j}
                                        \                   /
                                         v                 v
       Final Merge Multiplications:      p_{i-1}  *  p_k  *  p_j
```

#### The Subproblem Cost Breakdown:
The total cost of computing $A_{i..j}$ split at position $k$ equals:
1. The cost of computing the prefix product $A_{i..k}$, plus
2. The cost of computing the postfix product $A_{k+1..j}$, plus
3. The cost of multiplying the two resulting matrices together.

From our dimension convention, sub-chain $A_{i..k}$ produces a matrix of dimensions $p_{i-1} \times p_k$, and sub-chain $A_{k+1..j}$ produces a matrix of dimensions $p_k \times p_j$. 
Multiplying these two matrices requires:
$$\text{Merge Cost} = p_{i-1} \cdot p_k \cdot p_j$$

#### Cut-and-Paste Proof of Optimal Substructure:
Suppose that the optimal parenthesization of $A_{i..j}$ splits at index $k$. 
Then, the parenthesization of the prefix sub-chain $A_{i..k}$ must be an **optimal parenthesization** of $A_{i..k}$. 
If an alternative parenthesization of $A_{i..k}$ existed with strictly lower scalar multiplications, substituting it into the global split would strictly decrease the total cost of computing $A_{i..j}$, contradicting the assumed optimality of the original solution. 
The same logic applies to the postfix sub-chain $A_{k+1..j}$.

Thus, the problem exhibits **Optimal Substructure**.

---

<a id="bellman-recurrence"></a>
### The Bellman Recurrence Relation for $m[i, j]$

Define the state value $m[i, j]$ as:
> The minimum number of scalar multiplications needed to compute the matrix product $A_{i..j} = A_i A_{i+1} \dots A_j$, where $1 \le i \le j \le n$.

For the full problem, our goal is to compute $m[1, n]$.

#### 1. Base Cases ($i = j$):
When $i = j$, the sub-chain contains only a single matrix $A_i$. No multiplications are required:
$$m[i, i] = 0 \quad \forall i \in \{1, 2, \dots, n\}$$

#### 2. Recursive Step ($i < j$):
When $i < j$, we minimize the sum of the subproblem costs plus the merge cost over all possible split positions $k \in \{i, i+1, \dots, j-1\}$:

$$\mathbf{m[i, j] = \begin{cases} 
0 & \text{if } i = j, \\
\min_{i \le k < j} \Big\{ m[i, k] + m[k+1, j] + p_{i-1} \cdot p_k \cdot p_j \Big\} & \text{if } i < j.
\end{cases}}$$

---

<a id="split-matrix"></a>
### The Split Matrix $s[i, j]$ (Tracking Optimal Parentheses)

To reconstruct the optimal parenthesization, we maintain an auxiliary table $s[i, j]$ that records the optimal split point $k$:

$$\mathbf{s[i, j] = \arg\min_{i \le k < j} \Big\{ m[i, k] + m[k+1, j] + p_{i-1} \cdot p_k \cdot p_j \Big\}}$$

The entry $s[i, j]$ stores the exact index $k$ such that splitting the product into $A_{i..k}$ and $A_{k+1..j}$ achieves the minimal cost $m[i, j]$. 
The table $s[i, j]$ is defined for $1 \le i < j \le n$.

---

<a id="algorithm-design"></a>
## 3. Algorithm Design & Subproblem Dependency Geometry

<a id="diagonal-traversal"></a>
### Why Standard Row-Major Traversal Fails (The Diagonal Traversal Requirement)

To compute $m[i, j]$, the recurrence queries:
* $m[i, k]$ (a subproblem in the same row $i$, but a column $k < j$)
* $m[k+1, j]$ (a subproblem in the same column $j$, but a row $k+1 > i$)

```
                     SUBPROBLEM DEPENDENCY TOPOLOGY
                                  Column k   Column j
                       +-------------+----------+
                Row i  |             | m[i, k]  | m[i, j] <--- Target Cell
                       +-------------+----------+
                       |             |          |
                       +-------------+----------+
              Row k+1  |             |          | m[k+1, j]
                       +-------------+----------+
                       
       Computing m[i, j] requires cells to its LEFT (m[i, k])
       and cells BELOW it (m[k+1, j]).
       A standard row-major traversal (i from 1 to n, j from 1 to n)
       FAILS because m[k+1, j] will not yet be computed!
```

#### The Topological Solution: Chain Length ($l$) Iteration
Notice that computing $m[i, j]$ requires solutions for subproblems of lengths $k - i + 1$ and $j - (k + 1) + 1 = j - k$. 
Both of these lengths are **strictly less than the length of $A_{i..j}$** ($l = j - i + 1$).

Therefore, the correct evaluation order is by **increasing chain length $l$**:
1. Base cases: chain length $l = 1$ (the main diagonal $m[i, i] = 0$).
2. Next: chain length $l = 2$ (sub-chains of 2 matrices: $A_1 A_2, A_2 A_3, \dots$).
3. Next: chain length $l = 3$ (sub-chains of 3 matrices).
4. Continue until $l = n$ (the target $m[1, n]$).

In the 2D table, this corresponds to **filling the matrix along its diagonals**, moving from the main diagonal outward to the top-right corner.

```
                     DIAGONAL TRAVERSAL PATTERN (n = 4)
                       j=1       j=2       j=3       j=4
                     +---------+---------+---------+---------+
              i = 1  |  l = 1  |  l = 2  |  l = 3  |  l = 4  | <--- m[1, 4] Target!
                     +---------+---------+---------+---------+
              i = 2  |    X    |  l = 1  |  l = 2  |  l = 3  |
                     +---------+---------+---------+---------+
              i = 3  |    X    |    X    |  l = 1  |  l = 2  |
                     +---------+---------+---------+---------+
              i = 4  |    X    |    X    |    X    |  l = 1  |
                     +---------+---------+---------+---------+
                     
       * Diagonal 0 (l = 1): m[1,1], m[2,2], m[3,3], m[4,4] (All 0s)
       * Diagonal 1 (l = 2): m[1,2], m[2,3], m[3,4]
       * Diagonal 2 (l = 3): m[1,3], m[2,4]
       * Diagonal 3 (l = 4): m[1,4] (Final Answer)
```

---

<a id="pseudocode"></a>
### Complete Pseudocode: `MatrixChainOrder` and `PrintOptimalParens`

```text
Algorithm MatrixChainOrder(p, n)
// Input: Dimension sequence p = <p_0, p_1, ..., p_n> where matrix A_i has dimensions p_{i-1} x p_i
// Output: Minimum scalar multiplications table m[1..n, 1..n] and split table s[1..n-1, 2..n]
begin
    Allocate m[1..n, 1..n];
    Allocate s[1..n-1, 2..n];
    
    // Step 1: Initialize main diagonal base cases (l = 1) - O(n)
    for i ← 1 to n do
        m[i, i] ← 0;
        
    // Step 2: Loop over chain lengths l from 2 to n
    for l ← 2 to n do
    begin
        for i ← 1 to (n - l + 1) do
        begin
            j ← i + l - 1;           // Set right boundary of current sub-chain
            m[i, j] ← +∞;            // Initialize minimum to infinity
            
            // Try all possible split positions k between i and j - 1
            for k ← i to (j - 1) do
            begin
                // Recurrence calculation
                cost ← m[i, k] + m[k + 1, j] + (p[i - 1] * p[k] * p[j]);
                
                if cost < m[i, j] then
                begin
                    m[i, j] ← cost;
                    s[i, j] ← k;     // Record optimal split position
                end;
            end;
        end;
    end;
    
    return (m, s);
end;

Algorithm PrintOptimalParens(s, i, j)
// Input: Split table s, current sub-chain boundaries i and j
// Output: Formatted string representation of optimal parenthesization
begin
    if i = j then
        print("A" + i);
    else
    begin
        print("(");
        PrintOptimalParens(s, i, s[i, j]);        // Recurse on left prefix
        PrintOptimalParens(s, s[i, j] + 1, j);    // Recurse on right postfix
        print(")");
    end;
end;
```

---

<a id="complexity-analysis"></a>
### Rigorous Asymptotic Complexity Analysis ($\Theta(n^3)$ Time, $\Theta(n^2)$ Space)

#### 1. Time Complexity Derivation:
The algorithm consists of three nested loops:
* The outer loop tracks chain length $l$, iterating from $2$ to $n$ ($n - 1$ times).
* The middle loop tracks start index $i$, running from $1$ to $n - l + 1$.
* The inner loop tracks split index $k$, running from $i$ to $j - 1 = i + l - 2$, executing exactly $l - 1$ times.

The total number of iterations across all three loops is:
$$T(n) = \sum_{l=2}^n \sum_{i=1}^{n-l+1} \sum_{k=i}^{i+l-2} 1 = \sum_{l=2}^n (n - l + 1)(l - 1)$$

Let $z = l - 1$. As $l$ ranges from $2$ to $n$, $z$ ranges from $1$ to $n - 1$:
$$T(n) = \sum_{z=1}^{n-1} (n - z) z = \sum_{z=1}^{n-1} (n z - z^2) = n \sum_{z=1}^{n-1} z - \sum_{z=1}^{n-1} z^2$$

Using the standard summation identities $\sum_{z=1}^{m} z = \frac{m(m+1)}{2}$ and $\sum_{z=1}^m z^2 = \frac{m(m+1)(2m+1)}{6}$ with $m = n - 1$:
$$T(n) = n \left[ \frac{(n-1)n}{2} \right] - \left[ \frac{(n-1)n(2n-1)}{6} \right]$$
$$T(n) = \frac{n^2(n-1)}{2} - \frac{n(n-1)(2n-1)}{6} = \frac{n(n-1)}{6} \Big[ 3n - (2n - 1) \Big] = \frac{n(n-1)(n+1)}{6}$$
$$T(n) = \frac{n(n^2 - 1)}{6} = \frac{n^3 - n}{6} = \mathbf{\Theta(n^3)}$$

Each inner iteration performs a constant number of operations (lookups, additions, and multiplications). Thus, the runtime is **$\mathbf{\Theta(n^3)}$**.

#### 2. Space Complexity Derivation:
* The cost table $m$ requires storage for $\frac{n(n+1)}{2}$ cells (upper triangular matrix), which is $\Theta(n^2)$.
* The split table $s$ requires storage for $\frac{(n-1)n}{2}$ cells, which is $\Theta(n^2)$.
* Total Auxiliary Space Complexity: $\mathbf{\Theta(n^2)}$.

---

<a id="execution-trace"></a>
## 4. Step-by-Step 5W1H Stepped Execution Trace

We trace the algorithm on a sequence of 4 matrices ($n = 4$).

<a id="reference-sequence"></a>
### Reference 4-Matrix Sequence Specification:
* Matrices: $\langle A_1, A_2, A_3, A_4 \rangle$
* Dimensions:
  * $A_1$: $10 \times 20$ ($p_0 = 10, p_1 = 20$)
  * $A_2$: $20 \times 5$ ($p_1 = 20, p_2 = 5$)
  * $A_3$: $5 \times 15$ ($p_2 = 5, p_3 = 15$)
  * $A_4$: $15 \times 30$ ($p_3 = 15, p_4 = 30$)
* Dimension vector:
  $$\mathbf{p = \langle 10, \; 20, \; 5, \; 15, \; 30 \rangle} \quad (p_0 \dots p_4)$$

---

<a id="stepped-fill"></a>
### Stepped Diagonal Fill ($l = 2, 3, 4$) using 5W1H Methodology

#### Phase 1: Base Case Initialization (Diagonal $l = 1$)
For all $i \in \{1, 2, 3, 4\}$:
$$m[1, 1] = 0, \quad m[2, 2] = 0, \quad m[3, 3] = 0, \quad m[4, 4] = 0$$

---

#### Phase 2: Chain Length $l = 2$ (Sub-chains of 2 Matrices)

##### Cell $m[1, 2]$: Computing Product $A_1 A_2$
* **What are we doing?** Evaluating optimal cost for sub-chain $A_1 A_2$.
* **Why are we starting here?** Length $l = 2$ spans indices $i = 1$ to $j = 2$.
* **How do we execute the step mechanically?**
  Only one possible split point: $k = 1$.
  $$m[1, 2] = m[1, 1] + m[2, 2] + (p_0 \cdot p_1 \cdot p_2) = 0 + 0 + (10 \cdot 20 \cdot 5) = \mathbf{1,000}$$
  Record split: $s[1, 2] = 1$.

##### Cell $m[2, 3]$: Computing Product $A_2 A_3$
* Indices: $i = 2, j = 3$, only split: $k = 2$.
  $$m[2, 3] = m[2, 2] + m[3, 3] + (p_1 \cdot p_2 \cdot p_3) = 0 + 0 + (20 \cdot 5 \cdot 15) = \mathbf{1,500}$$
  Record split: $s[2, 3] = 2$.

##### Cell $m[3, 4]$: Computing Product $A_3 A_4$
* Indices: $i = 3, j = 4$, only split: $k = 3$.
  $$m[3, 4] = m[3, 3] + m[4, 4] + (p_2 \cdot p_3 \cdot p_4) = 0 + 0 + (5 \cdot 15 \cdot 30) = \mathbf{2,250}$$
  Record split: $s[3, 4] = 3$.

---

#### Phase 3: Chain Length $l = 3$ (Sub-chains of 3 Matrices)

##### Cell $m[1, 3]$: Computing Product $A_1 A_2 A_3$
* **What are we doing?** Finding the optimal parenthesization for $A_1 A_2 A_3$ ($i = 1, j = 3$).
* **Where did this formula originate?** Testing all split points $k \in \{1, 2\}$ using recurrence $m[1, k] + m[k+1, 3] + p_0 p_k p_3$.
* **How do we execute the step mechanically?**
  * **Test $k = 1$** (Split as $(A_1) \times (A_2 A_3)$):
    $$\text{Cost} = m[1, 1] + m[2, 3] + (p_0 \cdot p_1 \cdot p_3) = 0 + 1,500 + (10 \cdot 20 \cdot 15) = 1,500 + 3,000 = \mathbf{4,500}$$
  * **Test $k = 2$** (Split as $(A_1 A_2) \times (A_3)$):
    $$\text{Cost} = m[1, 2] + m[3, 3] + (p_0 \cdot p_2 \cdot p_3) = 1,000 + 0 + (10 \cdot 5 \cdot 15) = 1,000 + 750 = \mathbf{1,750}$$
  * **Minimum Selection:** $\min(4,500, \; 1,750) = \mathbf{1,750}$ at $k = 2$.
  $$\mathbf{m[1, 3] = 1,750, \quad s[1, 3] = 2}$$
* **What changed from previous step?** The optimal parenthesization for $A_1 A_2 A_3$ is determined to be $((A_1 A_2) A_3)$ with cost $1,750$.

---

##### Cell $m[2, 4]$: Computing Product $A_2 A_3 A_4$
* Indices: $i = 2, j = 4$, with split points $k \in \{2, 3\}$.
  * **Test $k = 2$** (Split as $(A_2) \times (A_3 A_4)$):
    $$\text{Cost} = m[2, 2] + m[3, 4] + (p_1 \cdot p_2 \cdot p_4) = 0 + 2,250 + (20 \cdot 5 \cdot 30) = 2,250 + 3,000 = \mathbf{5,250}$$
  * **Test $k = 3$** (Split as $(A_2 A_3) \times (A_4)$):
    $$\text{Cost} = m[2, 3] + m[4, 4] + (p_1 \cdot p_3 \cdot p_4) = 1,500 + 0 + (20 \cdot 15 \cdot 30) = 1,500 + 9,000 = \mathbf{10,500}$$
  * **Minimum Selection:** $\min(5,250, \; 10,500) = \mathbf{5,250}$ at $k = 2$.
  $$\mathbf{m[2, 4] = 5,250, \quad s[2, 4] = 2}$$

---

#### Phase 4: Chain Length $l = 4$ (Full Chain $A_1 A_2 A_3 A_4$)

##### Cell $m[1, 4]$: Computing Global Optimum
* **What are we doing?** Finding the globally optimal cost and parenthesization for all 4 matrices ($i = 1, j = 4$).
* **How do we execute the step mechanically?** Test all split points $k \in \{1, 2, 3\}$:
  * **Test $k = 1$** (Split as $(A_1) \times (A_2 A_3 A_4)$):
    $$\text{Cost} = m[1, 1] + m[2, 4] + (p_0 \cdot p_1 \cdot p_4) = 0 + 5,250 + (10 \cdot 20 \cdot 30) = 5,250 + 6,000 = \mathbf{11,250}$$
  * **Test $k = 2$** (Split as $(A_1 A_2) \times (A_3 A_4)$):
    $$\text{Cost} = m[1, 2] + m[3, 4] + (p_0 \cdot p_2 \cdot p_4) = 1,000 + 2,250 + (10 \cdot 5 \cdot 30) = 3,250 + 1,500 = \mathbf{4,750}$$
  * **Test $k = 3$** (Split as $(A_1 A_2 A_3) \times (A_4)$):
    $$\text{Cost} = m[1, 3] + m[4, 4] + (p_0 \cdot p_3 \cdot p_4) = 1,750 + 0 + (10 \cdot 15 \cdot 30) = 1,750 + 4,500 = \mathbf{6,250}$$
  * **Minimum Selection:** $\min(11,250, \; 4,750, \; 6,250) = \mathbf{4,750}$ at $k = 2$.
  $$\mathbf{m[1, 4] = 4,750, \quad s[1, 4] = 2}$$

---

<a id="final-matrices"></a>
### Final Cost Matrix $M$ and Split Matrix $S$

#### Matrix $M$ ($m[i, j]$ Costs):

<div class="table-wrap">

| $i$ \ $j$ | $j = 1$ | $j = 2$ | $j = 3$ | $j = 4$ |
| :---: | :---: | :---: | :---: | :---: |
| **$i = 1$** | $0$ | $1,000$ | $1,750$ | **$4,750^*$** |
| **$i = 2$** | - | $0$ | $1,500$ | $5,250$ |
| **$i = 3$** | - | - | $0$ | $2,250$ |
| **$i = 4$** | - | - | - | $0$ |

</div>

*\* The globally optimal minimum number of scalar multiplications is $m[1, 4] = \mathbf{4,750}$.*

#### Matrix $S$ ($s[i, j]$ Split Positions):

<div class="table-wrap">

| $i$ \ $j$ | $j = 2$ | $j = 3$ | $j = 4$ |
| :---: | :---: | :---: | :---: |
| **$i = 1$** | $1$ | $2$ | **$2$** |
| **$i = 2$** | - | $2$ | $2$ |
| **$i = 3$** | - | - | $3$ |

</div>

---

<a id="reconstruction-walkthrough"></a>
### Optimal Parenthesization Reconstruction Walkthrough

We reconstruct the optimal grouping by invoking `PrintOptimalParens(s, 1, 4)`:

```
                   RECURSIVE RECONSTRUCTION CALL TREE
                   
                     PrintOptimalParens(s, 1, 4)
                     [ Look up s[1, 4] = 2: Split as (1..2) x (3..4) ]
                                   /           \
                                  /             \
        PrintOptimalParens(s, 1, 2)             PrintOptimalParens(s, 3, 4)
        [ s[1, 2] = 1: Split (1) x (2) ]        [ s[3, 4] = 3: Split (3) x (4) ]
                 /         \                             /         \
                /           \                           /           \
         Print(1)          Print(2)              Print(3)          Print(4)
         [Base A1]         [Base A2]             [Base A3]         [Base A4]
```

1. **At $(1, 4)$:** Look up $s[1, 4] = 2$.
   The optimal top-level split separates the chain between $A_2$ and $A_3$:
   $$(A_1 A_2) \times (A_3 A_4)$$
2. **At Left Subproblem $(1, 2)$:** Look up $s[1, 2] = 1$.
   Split between $A_1$ and $A_2$:
   $$(A_1 \times A_2)$$
3. **At Right Subproblem $(3, 4)$:** Look up $s[3, 4] = 3$.
   Split between $A_3$ and $A_4$:
   $$(A_3 \times A_4)$$

#### Final Optimal Parenthesization:
$$\mathbf{((A_1 A_2) \times (A_3 A_4))}$$
*Total Scalar Multiplications:* **$4,750$**.

---

<a id="exam-summary"></a>
## 5. KTU Exam High-Yield Summary

<a id="three-mark-questions"></a>
### Frequently Asked 3-Mark Questions & Model Answers

#### Q1: State the Matrix Chain Multiplication problem and define its objective.
**Model Answer:**
Given a sequence of $n$ matrices $\langle A_1, A_2, \dots, A_n \rangle$ where matrix $A_i$ has dimensions $p_{i-1} \times p_i$, the Matrix Chain Multiplication problem seeks to determine the fully parenthesized product grouping that minimizes the total number of scalar multiplications required to evaluate $A_1 A_2 \dots A_n$.

---

#### Q2: Write the recurrence relation for the Matrix Chain Multiplication problem.
**Model Answer:**
Let $m[i, j]$ be the minimum number of scalar multiplications to compute $A_i \dots A_j$.
$$m[i, j] = \begin{cases} 
0 & \text{if } i = j, \\
\min_{i \le k < j} \Big\{ m[i, k] + m[k+1, j] + p_{i-1} \cdot p_k \cdot p_j \Big\} & \text{if } i < j.
\end{cases}$$

---

#### Q3: Why does a standard row-major traversal fail when filling the MCM dynamic programming table?
**Model Answer:**
Computing $m[i, j]$ requires $m[i, k]$ (cells to its left in the same row) and $m[k+1, j]$ (cells below it in the same column, where row index $k+1 > i$). In standard row-major order ($i$ from $1$ to $n$), cell $m[k+1, j]$ has not yet been computed when evaluating row $i$. The table must be filled in order of increasing chain length $l = j - i + 1$ (diagonal-by-diagonal).

---

#### Q4: Show that the number of possible parenthesizations of $n$ matrices grows exponentially.
**Model Answer:**
The number of alternative parenthesizations $P(n)$ satisfies the recurrence:
$$P(n) = \sum_{k=1}^{n-1} P(k) P(n-k) \quad \text{for } n \ge 2, \quad P(1) = 1$$
This yields the Catalan numbers:
$$P(n) = C_{n-1} = \frac{1}{n} \binom{2n-2}{n-1} = \Omega\left(\frac{4^n}{n^{3/2}}\right)$$
Because $P(n)$ is bounded below by an exponential in $4$, brute-force enumeration is computationally intractable.

---

<a id="marking-traps"></a>
### High-Frequency Student Pitfalls & Marking Traps

::: callout-exam Exam Traps & Avoidance Strategies
1. **The Dimension Array Indexing Off-By-One:**
   * *The Error:* Using $p_i \cdot p_k \cdot p_j$ instead of $p_{i-1} \cdot p_k \cdot p_j$.
   * *The Fix:* Remember that a sequence of $n$ matrices requires an array of **$n+1$ dimensions** ($p_0, p_1, \dots, p_n$). Matrix $A_i$ has rows $p_{i-1}$ and columns $p_i$. The merge cost is always:
     $$\mathbf{p_{i-1} \cdot p_k \cdot p_j}$$

2. **The Split Range Bound ($k < j$):**
   * *The Error:* Letting split index $k$ run up to $j$ ($i \le k \le j$), causing $m[k+1, j] = m[j+1, j]$ to index out of bounds.
   * *The Fix:* A chain cannot be split after its final element. The split index $k$ strictly satisfies:
     $$i \le k < j \quad (\text{or } k \in \{i, \dots, j-1\})$$

3. **Loop Ordering in Pseudocode:**
   * *The Error:* Writing `for i = 1 to n` as the outer loop.
   * *The Fix:* The outer loop must iterate over chain length: `for l = 2 to n`. The inner loops then derive $i$ and $j = i + l - 1$.

4. **Incomplete Answer Structure in 10-Mark Questions:**
   * *The Error:* Filling the $M$ matrix correctly but omitting the $S$ (split) matrix or the parenthesization string.
   * *The Fix:* Full marks require four deliverables: the recurrence relation, the completed $M$ table, the completed $S$ table, and the final parenthesization string obtained via backtracking (e.g., $((A_1 A_2)(A_3 A_4))$).
:::
