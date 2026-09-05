# Module 3.7: Backtracking Foundations — State-Space Trees, N-Queens, and Sum of Subsets
**Course Code: PCCST502 | Design and Analysis of Algorithms | KTU 2024 Scheme**

---

### Table of Contents
1. [Theoretical Foundations of Backtracking](#backtracking-foundations)
   - [Backtracking vs. Exhaustive Brute Force: The Systematic Search Paradigm](#systematic-search)
   - [Formal State-Space Tree Terminology](#state-space-terminology)
   - [Explicit Constraints vs. Implicit Constraints](#constraints-taxonomy)
   - [Bounding Functions and the Pruning Mechanism](#bounding-pruning)
   - [General Backtracking Control Abstractions (Recursive and Iterative)](#control-abstractions)
2. [The Classical $N$-Queens Problem](#n-queens-problem)
   - [Problem Specification & 1D Vector Formulation](#n-queens-specification)
   - [Derivation of the Diagonal Collision Invariant](#diagonal-invariant)
   - [The Safety Verification Primitive (`Place(k, i)`)](#place-primitive)
   - [Complete Recursive Pseudocode for $N$-Queens](#n-queens-pseudocode)
   - [Complete 5W1H Stepped Execution Trace for the 4-Queens Problem](#four-queens-trace)
   - [Full Pruned State-Space Tree Diagram for $N = 4$](#four-queens-tree)
3. [The Sum of Subsets Problem](#sum-of-subsets)
   - [Problem Definition & Mathematical Formulation](#subsets-formulation)
   - [Formulation A: Variable-Tuple Size (Permutation / Combinatorial View)](#formulation-a)
   - [Formulation B: Fixed-Tuple Size (Binary Inclusion Vector $x_i \in \{0, 1\}$)](#formulation-b)
   - [Bounding Functions & Pruning Conditions](#subsets-bounding)
   - [Complete Pseudocode (`SumOfSubsets`)](#subsets-pseudocode)
   - [Complete 5W1H Stepped Execution Trace on a Reference Instance](#subsets-trace)
   - [Full Pruned State-Space Binary Decision Tree Diagram](#subsets-tree)
4. [Comparative Analysis: Algorithmic Paradigms](#comparative-analysis)
   - [Dynamic Programming vs. Backtracking vs. Branch and Bound](#comparison-matrix)
5. [KTU Exam High-Yield Summary](#exam-summary)
   - [Frequently Asked 3-Mark Questions & Model Answers](#three-mark-questions)
   - [High-Frequency Student Pitfalls & Marking Scheme Traps](#marking-traps)

---

<a id="backtracking-foundations"></a>
## 1. Theoretical Foundations of Backtracking

<a id="systematic-search"></a>
### Backtracking vs. Exhaustive Brute Force: The Systematic Search Paradigm

Many combinatorial optimization and decision problems (such as graph coloring, knapsack, and constraint satisfaction) are **NP-hard** or require searching through a solution space of exponential size ($2^n$ or $n!$). 

A naive **exhaustive brute-force search** enumerates every potential candidate solution in the entire combinatorial domain, evaluates each against the problem constraints, and discards invalid candidates. 
For instance, placing $n$ queens on an $n \times n$ chessboard generates:
$$\binom{n^2}{n} \quad \text{configurations (e.g., for } n = 8, \ \binom{64}{8} = 4,426,165,368 \text{ states)}$$

```
                   EXHAUSTIVE BRUTE FORCE vs. BACKTRACKING
                   
      EXHAUSTIVE SEARCH (Blind Generation):
      Root ---> Candidate 1 (Full Depth) ---> Evaluate ---> Reject
           ---> Candidate 2 (Full Depth) ---> Evaluate ---> Reject
           ---> Candidate 3 (Full Depth) ---> Evaluate ---> ACCEPT!
           (Generates all leaves before testing feasibility!)
           
      BACKTRACKING (Depth-First Pruning):
      Root ---> Choice 1 ---> Partial State ---> [Pruned! Bounding Test Fails]
           |                                       |
           |                                       v
           |                                (Backtrack to Root immediately!)
           +---> Choice 2 ---> Partial State ---> Solution Found!
           (Prunes entire exponential subtrees at shallow depths!)
```

**Backtracking** is a systematic search methodology that explores the solution space using a **Depth-First Search (DFS)** traversal. 
Instead of generating full candidate solutions before testing validity, backtracking builds candidate solutions **incrementally, component by component**:
$$X = \langle x_1, x_2, \dots, x_k \rangle \quad \text{for } k \le n$$

At each step, a **bounding function** evaluates whether the partial vector $\langle x_1, \dots, x_k \rangle$ has any possibility of being extended into a complete, valid solution:
* **If viable:** Search proceeds deeper by choosing an assignment for $x_{k+1}$.
* **If non-viable:** The algorithm **prunes** the entire subtree rooted at that partial state, halts further exploration down that branch, and **backtracks** to the parent node at level $k-1$ to try the next alternative choice.

---

<a id="state-space-terminology"></a>
### Formal State-Space Tree Terminology

The conceptual framework of backtracking relies on the **State-Space Tree**:

```
                       STATE-SPACE TREE TOPOLOGY
                                ( 1 ) [Root Node]
                               /     \
                       [Branch]       [Branch]
                             /         \
                           ( 2 )       ( 3 ) [Dead Node / Pruned]
                          /     \         X
                        ( 4 )   ( 5 )
                          |       |
                        [Leaf]  [Answer Node]
```

1. **State Space:** The set of all possible configurations or tuples $\langle x_1, \dots, x_k \rangle$ that could potentially be explored during search.
2. **State-Space Tree:** An organization of the state space as a rooted tree, where the root represents the initial unassigned state, each internal node at depth $k$ represents a partial solution $\langle x_1, \dots, x_k \rangle$, and each branch represents a decision for the next component $x_{k+1}$.
3. **Problem State:** Any node within the state-space tree representing a partial or complete candidate tuple.
4. **Solution State:** A problem state $X = \langle x_1, \dots, x_k \rangle$ that satisfies all explicit constraints of the problem, whether or not it satisfies the implicit constraints.
5. **Answer Node (Goal Node):** A solution state that satisfies **all** constraints (both explicit and implicit), representing a valid solution to the problem instance.
6. **Live Node:** A node that has been generated, whose feasibility has not yet been ruled out, but whose children have not all been generated.
7. **E-Node (Expanding Node):** The unique live node whose children are currently being generated. In backtracking, there is exactly one active E-node at any moment.
8. **Dead Node:** A generated node that either cannot be expanded further (all children generated) or has been **killed (pruned)** by the bounding function because it cannot lead to an answer node.

---

<a id="constraints-taxonomy"></a>
### Explicit Constraints vs. Implicit Constraints

Backtracking classifies constraints into two categories:

#### 1. Explicit Constraints:
Rules that restrict each individual variable $x_i$ to take values strictly from a given domain set $S_i$, independent of the values assigned to other variables.
$$\forall i, \quad x_i \in S_i$$
* *Examples:*
  * In the 0/1 Knapsack problem: $x_i \in \{0, 1\}$.
  * In the $N$-Queens problem: $x_i \in \{1, 2, \dots, n\}$ (queen in row $i$ must be in a valid column).
  * In Graph Coloring: $x_i \in \{1, 2, \dots, m\}$ ($m$ allowed colors).

#### 2. Implicit Constraints:
Rules that define the mathematical relationships or constraints that must hold **between different variables** in the tuple $\langle x_1, \dots, x_k \rangle$.
* *Examples:*
  * In the 0/1 Knapsack problem: $\sum_{i=1}^n w_i x_i \le W$.
  * In the $N$-Queens problem: No two queens may share the same column or diagonal:
    $$x_i \ne x_j \quad \text{and} \quad |x_i - x_j| \ne |i - j| \quad \forall i \ne j$$
  * In the Sum of Subsets problem: $\sum_{i=1}^k w_i x_i = M$.

---

<a id="bounding-pruning"></a>
### Bounding Functions and the Pruning Mechanism

A **bounding function** $B_k(x_1, x_2, \dots, x_k)$ is a predicate that evaluates a partial solution tuple. 

$$B_k(x_1, \dots, x_k) = \begin{cases} 
\text{True} & \text{if the partial vector could lead to a valid solution,} \\
\text{False} & \text{if the partial vector CANNOT possibly lead to an answer node.}
\end{cases}$$

#### The Pruning Criterion:
If $B_k(x_1, \dots, x_k) = \text{False}$, the algorithm immediately **kills** the current E-node. 
No child nodes are generated, pruning the entire combinatorial subtree rooted at that node ($|S_{k+1}| \times |S_{k+2}| \times \dots \times |S_n|$ potential leaves are skipped in a single step).

```
                    THE PRUNING POWER OF BOUNDING
                    
                                Level k: ( x_1, ..., x_k )
                                            |
                              Bounding Function Evaluates:
                              B_k(x_1, ..., x_k) == FALSE
                                            |
                                            v
                                  [ KILL NODE / PRUNE ]
                                     /     |     \
                                  ( X )  ( X )  ( X )
                                  /   \  /   \  /   \
                                 *     **     **     *
                                 
           All descendant paths are eliminated without exploration!
```

---

<a id="control-abstractions"></a>
### General Backtracking Control Abstractions (Recursive and Iterative)

#### 1. Recursive Control Abstraction:
```text
Algorithm Backtrack(k)
// Input: Current recursion depth / variable index k
// Global Vector: x[1..n] storing candidate variable assignments
begin
    // Generate all candidate values for variable x[k] from its explicit domain
    for each element c ∈ Domain(k) do
    begin
        x[k] ← c;
        
        // Bounding Function Test: Test partial vector x[1..k]
        if BoundingTest(x, k) = true then
        begin
            // Test if full candidate vector is formed
            if IsCompleteSolution(x, k) then
                OutputSolution(x, k);
            
            // If not yet complete, recurse deeper into state-space tree
            if k < n then
                Backtrack(k + 1);
        end;
        // Implicit Backtracking Step: Next loop iteration overwrites x[k]
    end;
end;
```

#### 2. Iterative Control Abstraction:
```text
Algorithm IterativeBacktrack(n)
// Non-recursive state exploration using an explicit depth pointer
begin
    k ← 1;
    InitializeDomain(x, k);
    
    while k > 0 do
    begin
        if HasNextCandidate(x, k) then
        begin
            x[k] ← GetNextCandidate(x, k);
            
            if BoundingTest(x, k) = true then
            begin
                if IsCompleteSolution(x, k) then
                    OutputSolution(x, k);
                
                if k < n then
                begin
                    k ← k + 1;               // Move down to next level
                    InitializeDomain(x, k);
                end;
            end;
        end
        else
        begin
            k ← k - 1;                       // Backtrack up to parent node
        end;
    end;
end;
```

---

<a id="n-queens-problem"></a>
## 2. The Classical $N$-Queens Problem

<a id="n-queens-specification"></a>
### Problem Specification & 1D Vector Formulation

The **$N$-Queens Problem** requires placing $n$ non-attacking queens on an $n \times n$ chessboard such that no two queens attack each other. 
Under standard chess rules, a queen attacks any piece located along the same **row**, **column**, or **diagonal**.

```
                   1D VECTOR REPRESENTATION OF CHESSBOARD
                   
         Col 1   Col 2   Col 3   Col 4
       +-------+-------+-------+-------+
 Row 1 |   .   |   Q   |   .   |   .   |   Row 1: Queen at Col 2  (x[1] = 2)
       +-------+-------+-------+-------+
 Row 2 |   .   |   .   |   .   |   Q   |   Row 2: Queen at Col 4  (x[2] = 4)
       +-------+-------+-------+-------+
 Row 3 |   Q   |   .   |   .   |   .   |   Row 3: Queen at Col 1  (x[3] = 1)
       +-------+-------+-------+-------+
 Row 4 |   .   |   .   |   Q   |   .   |   Row 4: Queen at Col 3  (x[4] = 3)
       +-------+-------+-------+-------+
       
       Board state encoded as compact 1D vector: X = < 2, 4, 1, 3 >
```

#### Compact 1D Vector Encoding:
Rather than maintaining an $n \times n$ 2D matrix, we observe that since no two queens can share the same row, **every row $i \in \{1, \dots, n\}$ must contain exactly one queen**.

We represent the board as a 1D vector of length $n$:
$$X = \langle x_1, x_2, \dots, x_n \rangle$$
where $x_i$ denotes the **column index** where the queen in row $i$ is placed.
* **Row placement:** Handled implicitly by array index $i$.
* **Column placement:** Handled by the value $x_i \in \{1, 2, \dots, n\}$.

---

<a id="diagonal-invariant"></a>
### Derivation of the Diagonal Collision Invariant

Two queens at positions $(i, x_i)$ and $(j, x_j)$ conflict if and only if they share a column or a diagonal.

#### 1. Column Collision:
Two queens lie in the same column if:
$$x_i = x_j$$

#### 2. Diagonal Collision:
Consider a chessboard viewed as a Cartesian grid:
* **Major Diagonal (Top-Left to Bottom-Right):**
  Moving down and right increments both row and column indices equally:
  $$j - i = x_j - x_i \implies x_j - x_i = j - i$$
* **Minor Diagonal (Top-Right to Bottom-Left):**
  Moving down and left increments row while decrementing column:
  $$j - i = -(x_j - x_i) \implies x_j - x_i = -(j - i)$$

```
                      DIAGONAL COLLISION GEOMETRY
                      
       Major Diagonal (Slope = +1):           Minor Diagonal (Slope = -1):
            (i, x_i)                                      (i, x_i)
                \                                          /
                 \                                        /
                  v                                      v
               (j, x_j)                              (j, x_j)
         j - i = x_j - x_i                      j - i = -(x_j - x_i)
```

Combining both cases using the absolute value:
$$|x_j - x_i| = |j - i| \quad \text{or} \quad \mathbf{|x_i - x_j| = |i - j|}$$

#### Theorem 1 (The $N$-Queens Collision Invariant):
Two queens positioned at $(i, x_i)$ and $(j, x_j)$ attack each other along a diagonal if and only if:
$$|x_i - x_j| = |i - j|$$

---

<a id="place-primitive"></a>
### The Safety Verification Primitive (`Place(k, i)`)

The bounding function `Place(k, i)` determines whether placing a queen in row $k$ at column $i$ conflicts with any of the $k-1$ queens already placed in rows $1 \dots k-1$:

```text
Algorithm Place(k, i)
// Input: Row index k of new queen, Candidate column i
// Global Vector: x[1..k-1] containing previously placed queens
// Output: Boolean True if safe, False if in conflict
begin
    for j ← 1 to (k - 1) do
    begin
        // Check 1: Same column conflict (x[j] = i)
        // Check 2: Diagonal conflict (|x[j] - i| = |j - k|)
        if (x[j] = i) or (abs(x[j] - i) = abs(j - k)) then
            return false;
    end;
    return true;
end;
```

---

<a id="n-queens-pseudocode"></a>
### Complete Recursive Pseudocode for $N$-Queens

```text
Algorithm NQueens(k, n)
// Input: Current row index k, Total board dimension n
// Global Vector: x[1..n] initialized to empty
begin
    // Try placing queen k in every column from 1 to n
    for col ← 1 to n do
    begin
        if Place(k, col) = true then
        begin
            x[k] ← col;              // Place queen k at column 'col'
            
            if k = n then            // All n queens safely placed!
                PrintSolution(x, n);
            else
                NQueens(k + 1, n);   // Recurse to place queen in next row
                
            // Backtracking: Handled implicitly as next iteration tests col + 1
        end;
    end;
end;
```

---

<a id="four-queens-trace"></a>
### Complete 5W1H Stepped Execution Trace for the 4-Queens Problem

We trace the algorithm on a $4 \times 4$ board ($n = 4$) to find its first solution.

#### Initial State:
* $n = 4$, $x = [\text{NIL}, \text{NIL}, \text{NIL}, \text{NIL}]$. 
* Call `NQueens(1, 4)`.

---

#### 5W1H Stepped Iteration Walkthrough:

##### Step 1: Placing Queen in Row 1 ($k = 1$)
* **What are we doing?** Trying column positions for Queen 1.
* **Why are we starting here?** Row 1 is the initial root level.
* **How do we execute the step mechanically?**
  * Try $col = 1$: `Place(1, 1)` checks 0 previous queens $\implies$ **Safe**.
  * Set $x[1] = 1$. Recurse to `NQueens(2, 4)`.
* **What changed?** Queen 1 placed at $(1, 1)$. Active vector: $\langle 1 \rangle$.

---

##### Step 2: Placing Queen in Row 2 ($k = 2$)
* Current board: $x[1] = 1$.
* Try $col = 1$: `x[1] == 1` $\implies$ **Column Conflict**. Pruned.
* Try $col = 2$: $|x[1] - 2| = |1 - 2| = 1$; $|1 - 2| = 1$ $\implies$ **Diagonal Conflict**. Pruned.
* Try $col = 3$:
  * Column check: $x[1] \ne 3$ ($1 \ne 3$). Safe.
  * Diagonal check: $|x[1] - 3| = |1 - 3| = 2 \ne |1 - 2| = 1$. Safe.
  * Set $x[2] = 3$. Recurse to `NQueens(3, 4)`.
* **What changed?** Queen 2 placed at $(2, 3)$. Active vector: $\langle 1, 3 \rangle$.

---

##### Step 3: Placing Queen in Row 3 ($k = 3$) — All Choices Pruned!
* Current board: $x = \langle 1, 3 \rangle$.
* Try $col = 1$: `x[1] == 1` $\implies$ **Column Conflict**. Pruned.
* Try $col = 2$: Diagonal with Queen 2: $|x[2] - 2| = |3 - 2| = 1 == |2 - 3| = 1 \implies$ **Diagonal Conflict**. Pruned.
* Try $col = 3$: `x[2] == 3` $\implies$ **Column Conflict**. Pruned.
* Try $col = 4$: Diagonal with Queen 2: $|x[2] - 4| = |3 - 4| = 1 == |2 - 3| = 1 \implies$ **Diagonal Conflict**. Pruned.
* **Dead Node:** No columns available in row 3!
* **What changed?** **Backtrack to Level 2!** Resume loop for Queen 2 at $col = 4$.

---

##### Step 4: Backtracked to Row 2 ($k = 2$)
* Reset $x[2]$; test $col = 4$:
  * Column: $4 \ne 1$.
  * Diagonal: $|1 - 4| = 3 \ne |1 - 2| = 1$. Safe.
* Set $x[2] = 4$. Recurse to `NQueens(3, 4)`.
* **What changed?** Queen 2 moved to $(2, 4)$. Active vector: $\langle 1, 4 \rangle$.

---

##### Step 5: Placing Queen in Row 3 ($k = 3$)
* Current board: $x = \langle 1, 4 \rangle$.
* Try $col = 1$: `x[1] == 1` $\implies$ Column Conflict.
* Try $col = 2$:
  * Check against Queen 1: $2 \ne 1$; $|1 - 2| = 1 \ne |1 - 3| = 2$. Safe.
  * Check against Queen 2: $2 \ne 4$; $|4 - 2| = 2 \ne |2 - 3| = 1$. Safe.
  * Set $x[3] = 2$. Recurse to `NQueens(4, 4)`.
* **What changed?** Queen 3 placed at $(3, 2)$. Active vector: $\langle 1, 4, 2 \rangle$.

---

##### Step 6: Placing Queen in Row 4 ($k = 4$) — All Choices Pruned!
* Current board: $x = \langle 1, 4, 2 \rangle$.
* Try $col = 1$: `x[1] == 1` $\implies$ Column Conflict.
* Try $col = 2$: `x[3] == 2` $\implies$ Column Conflict.
* Try $col = 3$: Diagonal with Queen 3: $|2 - 3| = 1 == |3 - 4| = 1 \implies$ Diagonal Conflict.
* Try $col = 4$: `x[2] == 4` $\implies$ Column Conflict.
* **Dead Node:** All columns exhausted in row 4.
* **Backtrack to Level 3:** Row 3 has no further columns ($col = 3, 4$ also conflict with $x=\langle 1, 4 \rangle$).
* **Backtrack to Level 2:** Row 2 has no further columns ($col = 4$ was the last).
* **Backtrack to Level 1:** Queen 1 at $col = 1$ has failed. Advance Queen 1 to $col = 2$!

---

##### Step 7: Restarting Row 1 at Column 2 ($x[1] = 2$)
* Set $x[1] = 2$. Recurse to `NQueens(2, 4)`.
* In Row 2 ($k = 2$):
  * $col = 1, 2, 3$ fail conflicts.
  * $col = 4$: Safe ($x[1]=2, x[2]=4$). Recurse to `NQueens(3, 4)`.
* In Row 3 ($k = 3$):
  * $col = 1$: Safe!
    * Check Queen 1: $1 \ne 2$; $|2 - 1| = 1 \ne |1 - 3| = 2$.
    * Check Queen 2: $1 \ne 4$; $|4 - 1| = 3 \ne |2 - 3| = 1$.
  * Set $x[3] = 1$. Recurse to `NQueens(4, 4)`.
* In Row 4 ($k = 4$):
  * Try $col = 1$: `x[3] == 1` $\implies$ Column Conflict.
  * Try $col = 2$: `x[1] == 2` $\implies$ Column Conflict.
  * Try $col = 3$:
    * Check Queen 1: $3 \ne 2$; $|2 - 3| = 1 \ne |1 - 4| = 3$. Safe.
    * Check Queen 2: $3 \ne 4$; $|4 - 3| = 1 \ne |2 - 4| = 2$. Safe.
    * Check Queen 3: $3 \ne 1$; $|1 - 3| = 2 \ne |3 - 4| = 1$. Safe.
    * **All checks pass! Queen 4 placed at $(4, 3)$!**
* Since $k = n = 4$, **SOLUTION ATTAINED!**

#### First Valid Solution:
$$\mathbf{X = \langle 2, \; 4, \; 1, \; 3 \rangle}$$

---

<a id="four-queens-tree"></a>
### Full Pruned State-Space Tree Diagram for $N = 4$

```
                   STATE-SPACE TREE FOR 4-QUEENS (Solution 1)
                   
                                      ( Root )
                                    /    |    \
                        [x1 = 1]   /     |     \   [x1 = 2]
                                  /      |      \
                                (1)      |      (2)
                               /   \     |       |
                       [x2=3] /     \    |       | [x2=4]
                             /     [x2=4]|       |
                           (1,3)    (1,4)|     (2,4)
                            /         |  |       |
                     [All col]        |  |       | [x3=1]
                      PRUNED!       (1,4,2)      |
                                      |        (2,4,1)
                                   [All col]     |
                                    PRUNED!      | [x4=3]
                                                 |
                                            (2, 4, 1, 3)
                                            [ANSWER NODE!]
```

---

<a id="sum-of-subsets"></a>
## 3. The Sum of Subsets Problem

<a id="subsets-formulation"></a>
### Problem Definition & Mathematical Formulation

Given a set of $n$ positive integers (weights):
$$W = \{w_1, w_2, \dots, w_n\}$$
and a positive target integer $M$, find all subsets of $W$ whose elements sum to exactly $M$.

Without loss of generality, we assume the weights are sorted in **strictly non-decreasing order**:
$$w_1 \le w_2 \le \dots \le w_n$$

---

<a id="formulation-a"></a>
### Formulation A: Variable-Tuple Size (Permutation / Combinatorial View)
In this formulation, the solution is represented as a variable-length tuple:
$$X = \langle x_1, x_2, \dots, x_k \rangle \quad \text{where } 1 \le k \le n$$
Each $x_i \in \{1, \dots, n\}$ is the index of an included element, with $x_1 < x_2 < \dots < x_k$ to prevent duplicate permutations.

---

<a id="formulation-b"></a>
### Formulation B: Fixed-Tuple Size (Binary Inclusion Vector $x_i \in \{0, 1\}$)
In this formulation (standard in algorithm design), every candidate solution is represented as a fixed-length boolean vector:
$$X = \langle x_1, x_2, \dots, x_n \rangle \quad \text{where } x_i \in \{0, 1\}$$
* $x_i = 1$: Element $w_i$ is included in the subset.
* $x_i = 0$: Element $w_i$ is excluded from the subset.

The problem constraints are:
$$\sum_{i=1}^n w_i x_i = M \quad \text{subject to} \quad x_i \in \{0, 1\}$$

The state-space tree is a **Binary Tree** of depth $n$, containing $2^{n+1} - 1$ total nodes and $2^n$ leaves.

---

<a id="subsets-bounding"></a>
### Bounding Functions & Pruning Conditions

Let the search be at depth $k$, where decisions have been made for variables $x_1 \dots x_k$. 
Define:
* **$s$ (Current Weight Sum):** The sum of weights chosen so far:
  $$s = \sum_{i=1}^k w_i x_i$$
* **$r$ (Remaining Available Weight):** The sum of all remaining weights that could potentially be added:
  $$r = \sum_{i=k+1}^n w_i$$

A partial state $\langle x_1, \dots, x_k \rangle$ is pruned if either of the following bounding conditions is violated:

```
                      PRUNING CONDITIONS FOR SUM OF SUBSETS
                      
  PRUNING RULE 1 (Weight Exceeded):
      s + w_{k+1} > M
      Adding the next element exceeds target M.
      Since weights are sorted (w_{k+1} <= w_{k+2} <= ...), no future element
      can fit either! Prune the branch.
      
  PRUNING RULE 2 (Insufficient Weight Remaining):
      s + r < M
      Even if we include ALL remaining elements, the sum cannot reach M!
      The branch can never achieve the target. Prune the branch.
```

#### The Composite Bounding Predicate:
Generate left child ($x_{k+1} = 1$) if and only if:
$$\mathbf{s + w_{k+1} \le M \quad \text{and} \quad s + r \ge M}$$

Generate right child ($x_{k+1} = 0$) if and only if:
$$\mathbf{s + (r - w_{k+1}) \ge M}$$

---

<a id="subsets-pseudocode"></a>
### Complete Pseudocode (`SumOfSubsets`)

```text
Algorithm SumOfSubsets(s, k, r, M, w, x, n)
// Input: 
//   s : Accumulated sum of selected items so far
//   k : Index of the current decision item (w[k])
//   r : Total weight of remaining unconsidered items
//   M : Target sum
//   w : Sorted array of positive weights w[1..n]
//   x : Solution vector x[1..n] where x[i] ∈ {0, 1}
begin
    // Generate Left Child: Include item w[k] (x[k] = 1)
    x[k] ← 1;
    
    // Check if target sum is achieved
    if s + w[k] = M then
    begin
        PrintSubset(x, k);           // Output solution vector up to index k
    end
    // Bounding condition to explore deeper down the left branch
    else if k < n and s + w[k] + w[k + 1] ≤ M then
    begin
        SumOfSubsets(s + w[k], k + 1, r - w[k], M, w, x, n);
    end;
    
    // Generate Right Child: Exclude item w[k] (x[k] = 0)
    // Bounding condition: remaining items must be sufficient to reach M
    if s + r - w[k] ≥ M and (k < n and s + w[k + 1] ≤ M) then
    begin
        x[k] ← 0;
        SumOfSubsets(s, k + 1, r - w[k], M, w, x, n);
    end;
end;
```

---

<a id="subsets-trace"></a>
### Complete 5W1H Stepped Execution Trace on a Reference Instance

#### Problem Instance:
* Weights: $W = \{w_1 = 3, \; w_2 = 5, \; w_3 = 6, \; w_4 = 7\}$
* Number of items: $n = 4$
* Target Sum: $M = 11$
* Total sum of all weights: $r_0 = 3 + 5 + 6 + 7 = 21$.

---

#### 5W1H Execution Trace:

##### Initial Call:
`SumOfSubsets(s = 0, k = 1, r = 21)`

---

##### Step 1: Evaluating Item 1 ($w_1 = 3$)
* **What are we doing?** Generating left child ($x_1 = 1$, include $w_1 = 3$).
* **Why this step?** Left branch corresponds to including the current candidate.
* **How do we execute the step mechanically?**
  * New sum: $s + w_1 = 0 + 3 = 3$.
  * Check match: $3 \ne 11$.
  * Left bound check: $s + w_1 + w_2 = 3 + 5 = 8 \le 11$. Safe!
  * New remaining: $r' = r - w_1 = 21 - 3 = 18$.
  * Call `SumOfSubsets(s = 3, k = 2, r = 18)`.
* **What changed?** Item 1 included. $x = [1, \dots]$.

---

##### Step 2: Evaluating Item 2 ($w_2 = 5$) under $x_1 = 1$
* **Left Child ($x_2 = 1$):**
  * New sum: $s + w_2 = 3 + 5 = 8 \ne 11$.
  * Left bound check: $s + w_2 + w_3 = 8 + 6 = 14 > 11$ (Next element exceeds $M$!).
  * Cannot recurse left.
* **Right Child ($x_2 = 0$, Exclude $w_2$):**
  * Check bound: $s + r - w_2 = 3 + 18 - 5 = 16 \ge 11$. Safe!
  * Next element check: $s + w_3 = 3 + 6 = 9 \le 11$. Safe!
  * Set $x_2 = 0$; $r' = 18 - 5 = 13$.
  * Call `SumOfSubsets(s = 3, k = 3, r = 13)`.
* **What changed?** Item 2 excluded. $x = [1, 0, \dots]$.

---

##### Step 3: Evaluating Item 3 ($w_3 = 6$) under $x_1 = 1, x_2 = 0$
* **Left Child ($x_3 = 1$):**
  * New sum: $s + w_3 = 3 + 6 = 9 \ne 11$.
  * Left bound check: $s + w_3 + w_4 = 9 + 7 = 16 > 11$ (Exceeds $M$!).
  * Cannot recurse left.
* **Right Child ($x_3 = 0$, Exclude $w_3$):**
  * Check bound: $s + r - w_3 = 3 + 13 - 6 = 10 < 11$ ($s + r < M$!).
  * **PRUNED BY BOUND 2!** Remaining weight ($10$) cannot reach target $11$.
* **What changed?** Branch dead. Backtrack to root.

---

##### Step 4: Backtracked to Root: Evaluating Exclude Item 1 ($x_1 = 0$)
* Check right bound: $s + r - w_1 = 0 + 21 - 3 = 18 \ge 11$. Safe!
* Set $x_1 = 0$; $r' = 21 - 3 = 18$.
* Call `SumOfSubsets(s = 0, k = 2, r = 18)`.

---

##### Step 5: Evaluating Item 2 ($w_2 = 5$) under $x_1 = 0$
* **Left Child ($x_2 = 1$):**
  * New sum: $s + w_2 = 0 + 5 = 5 \ne 11$.
  * Left bound: $s + w_2 + w_3 = 5 + 6 = 11 \le 11$. Safe!
  * Set $x_2 = 1$; $r' = 18 - 5 = 13$.
  * Call `SumOfSubsets(s = 5, k = 3, r = 13)`.
    * **Inside Call ($k = 3$, $w_3 = 6$):**
      * Try $x_3 = 1$: New sum $= s + w_3 = 5 + 6 = \mathbf{11 == M}$!
      * **TARGET SUM ACHIEVED!**
      * **SOLUTION 1 FOUND:** $x_1 = 0, \; x_2 = 1, \; x_3 = 1 \implies \mathbf{\{5, 6\}}$.
    * Try $x_3 = 0$: $s + r - w_3 = 5 + 13 - 6 = 12 \ge 11$.
      * Next check: $s + w_4 = 5 + 7 = 12 > 11$ (Exceeds $M$). Pruned!

---

##### Step 6: Evaluating Exclude Item 2 ($x_2 = 0$) under $x_1 = 0$
* Set $x_2 = 0$; $r' = 18 - 5 = 13$.
* Call `SumOfSubsets(s = 0, k = 3, r = 13)`.
* **Inside Call ($k = 3$, $w_3 = 6$):**
  * Try $x_3 = 1$: $s + w_3 = 6$.
    * Next check: $s + w_3 + w_4 = 6 + 7 = 13 > 11$ (Exceeds $M$). Cannot recurse left.
  * Try $x_3 = 0$: $s + r - w_3 = 0 + 13 - 6 = 7 < 11$ ($s + r < M$).
  * **PRUNED BY BOUND 2!**

#### All Valid Subsets Summing to $M = 11$:
$$\mathbf{\{w_2, w_3\} = \{5, 6\}} \quad \text{with vector } X = \langle 0, 1, 1, 0 \rangle$$

---

<a id="subsets-tree"></a>
### Full Pruned State-Space Binary Decision Tree Diagram

```
                     BINARY STATE-SPACE TREE FOR SUM OF SUBSETS
                     W = {3, 5, 6, 7}, Target M = 11, Total r = 21
                     
                                       ( s=0, r=21 )
                                     /               \
                       [x1=1: +3]   /                 \   [x1=0: +0]
                                   /                   \
                            ( s=3, r=18 )             ( s=0, r=18 )
                            /           \             /           \
                 [x2=1: +5]/             \[x2=0]     /             \[x2=0]
                          /               \         /               \
                   ( s=8, r=13 )     ( s=3, r=13 ) ( s=5, r=13 )  ( s=0, r=13 )
                      /     \             /     \       |               |
                   [+6>M]  [s+r<M]     [+7>M] [s+r<M]   | [x3=1: +6] [s+r<M]
                   PRUNED! PRUNED!     PRUNED! PRUNED!  v            PRUNED!
                                                   ( s=11 )
                                                 [ANSWER NODE!]
                                                 Subset: {5, 6}
```

---

<a id="comparative-analysis"></a>
## 4. Comparative Analysis: Algorithmic Paradigms

<div class="table-wrap">

| Dimension | Dynamic Programming | Backtracking | Branch and Bound |
| :--- | :--- | :--- | :--- |
| **Search Strategy** | Tabular / DAG Topological Order | **Depth-First Search (DFS)** with LIFO stack | **Breadth-First Search (BFS)** or **Best-First Search** via Priority Queue |
| **Pruning Mechanism** | None (solves all overlapping subproblems) | **Bounding functions** kill infeasible subtrees | **Cost bounds** ($\hat{c}(x)$ / lower bounds) prune unpromising subtrees |
| **Primary Problem Class** | Multistage Optimization | Constraint Satisfaction / Decision ($N$-Queens, Sudoku) | Combinatorial Optimization (TSP, 0/1 Knapsack) |
| **State-Space Traversal** | Dense evaluation of matrix/array states | Deep descent along a single path; retreats on failure | Expands all live nodes across frontier simultaneously |
| **Memory Footprint** | $O(n \cdot W)$ or $O(n^2)$ table storage | **$O(n)$** (Minimal; only stores current path stack) | High; queue stores all live frontier nodes ($O(2^n)$ in worst case) |

</div>

---

<a id="exam-summary"></a>
## 5. KTU Exam High-Yield Summary

<a id="three-mark-questions"></a>
### Frequently Asked 3-Mark Questions & Model Answers

#### Q1: Differentiate between explicit and implicit constraints in backtracking.
**Model Answer:**
* **Explicit Constraints:** Rules that restrict each variable to a specific domain independent of other variables (e.g., $x_i \in \{0, 1\}$ or $x_i \in \{1 \dots n\}$).
* **Implicit Constraints:** Mathematical relations that must hold between different variables in the solution tuple (e.g., no two queens on the same diagonal $|x_i - x_j| \ne |i - j|$, or subset sum $\sum w_i x_i = M$).

---

#### Q2: Derive the condition used to detect diagonal collisions in the $N$-Queens problem.
**Model Answer:**
Let two queens be placed at $(i, x_i)$ and $(j, x_j)$. 
Along a major diagonal, the slope is $+1 \implies j - i = x_j - x_i$. 
Along a minor diagonal, the slope is $-1 \implies j - i = -(x_j - x_i)$. 
Combining both via absolute values yields the diagonal collision condition:
$$|x_i - x_j| = |i - j|$$

---

#### Q3: Define a bounding function and explain its role in state-space tree pruning.
**Model Answer:**
A bounding function is a predicate $B(x_1 \dots x_k)$ evaluated on partial solutions. If the function determines that the partial vector cannot possibly be extended to a valid or optimal solution, it returns false. The algorithm then **prunes** the entire subtree rooted at that node, avoiding exponential exploration of invalid branches.

---

#### Q4: State the two pruning conditions used in the Sum of Subsets problem.
**Model Answer:**
For current sum $s$, candidate weight $w_{k+1}$, and remaining weight $r$:
1. **Weight Exceeded:** $s + w_{k+1} > M$ (Prunes branch because weights are sorted non-decreasingly).
2. **Insufficient Remaining Weight:** $s + r < M$ (Prunes branch because even taking all remaining items cannot reach target $M$).

---

<a id="marking-traps"></a>
### High-Frequency Student Pitfalls & Marking Scheme Traps

::: callout-exam Exam Traps & Avoidance Strategies
1. **The 2D Matrix Representation Trap in $N$-Queens:**
   * *The Error:* Representing the board as an $n \times n$ matrix $B[i][j]$ and writing 8-directional scan loops.
   * *The Fix:* Use the standard **1D array representation** $x[1..n]$ where $x[i]$ represents the column of the queen in row $i$. This implicitly enforces the "one queen per row" constraint and simplifies collision checking to an $O(k)$ loop.

2. **Omitting the Sorted Weights Prerequisite in Sum of Subsets:**
   * *The Error:* Applying the condition $s + w_{k+1} > M$ to prune remaining candidates without first stating that the input weights must be sorted.
   * *The Fix:* State explicitly: *"Assuming weights are sorted in non-decreasing order ($w_1 \le w_2 \le \dots \le w_n$), if $s + w_{k+1} > M$, then for all $j > k+1$, $s + w_j > M$, so all remaining candidates can be safely pruned."*

3. **Incomplete Tree Diagrams:**
   * *The Error:* Drawing only the successful path in the state-space tree.
   * *The Fix:* KTU marking schemes require showing **pruned dead nodes** with an "X" or "Pruned" label along with the violated bounding condition (e.g., *Crossed / Killed by $B_k$*).

4. **Missing Backtrack Restoration in Non-Recursive Code:**
   * *The Error:* Forgetting to reset variable values or sum variables when backtracking up the tree.
   * *The Fix:* When stepping back from depth $k$ to $k-1$, restore state variables: $s \leftarrow s - w_k$ and $r \leftarrow r + w_k$.
:::
