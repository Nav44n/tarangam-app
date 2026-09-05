# Module 3.5: All-Pairs Shortest Paths — The Floyd-Warshall Algorithm
**Course Code: PCCST502 | Design and Analysis of Algorithms | KTU 2024 Scheme**

---

### Table of Contents
1. [All-Pairs Shortest Path (APSP) Problem Formulation](#apsp-formulation)
   - [Formal Problem Statement & Matrix Representation](#formal-statement)
   - [Comparison of APSP Strategies: Repeated SSSP vs. Dynamic Programming](#apsp-comparison)
   - [Handling Negative Edge Weights & Negative Cycle Detection](#negative-cycles)
2. [The Floyd-Warshall Algorithm: Theoretical Formulation](#floyd-warshall-theory)
   - [The Intermediate Vertex Concept ($V^{(k)}$ Subsets)](#intermediate-concept)
   - [Derivation of the Triply Nested Dynamic Programming Recurrence](#recurrence-derivation)
   - [Base Cases and Boundary Matrix Configurations ($D^{(0)}$ and $\Pi^{(0)}$)](#base-cases)
   - [The Dual Predecessor Matrix $\Pi^{(k)}$ Mechanics](#predecessor-matrix)
3. [Algorithm Implementation & Mechanics](#algorithm-mechanics)
   - [Complete Pseudocode (Matrix Updates & Predecessor Maintenance)](#pseudocode)
   - [Why the Triple-Loop Order (k Outer, i Middle, j Inner) is Mandatory](#loop-order-proof)
   - [In-Place Space Optimization: From $O(V^3)$ to $O(V^2)$ Space](#space-optimization)
4. [Step-by-Step 5W1H Stepped Execution Trace](#execution-trace)
   - [Reference Directed Weighted Graph Specification](#reference-graph)
   - [Stepped Iteration Matrices: $D^{(0)} \to D^{(1)} \to D^{(2)} \to D^{(3)} \to D^{(4)}$](#matrix-progression)
   - [5W1H Mechanical Execution of $k=2$ and $k=3$ Transitions](#5w1h-trace)
   - [Recursive Shortest Path Reconstruction Procedure](#path-reconstruction)
5. [Transitive Closure of a Directed Graph: Warshall's Algorithm](#warshalls-algorithm)
   - [Reachability Matrix Definition & Boolean Matrix Formulation](#reachability-matrix)
   - [Logical Warshall Recurrence (OR-AND Bitwise Formulation)](#warshall-recurrence)
   - [Comparison: Floyd-Warshall vs. Warshall](#floyd-vs-warshall)
6. [KTU Exam High-Yield Summary](#exam-summary)
   - [Frequently Asked 3-Mark Questions & Model Answers](#three-mark-questions)
   - [High-Frequency Student Pitfalls & Marking Traps](#marking-traps)

---

<a id="apsp-formulation"></a>
## 1. All-Pairs Shortest Path (APSP) Problem Formulation

<a id="formal-statement"></a>
### Formal Problem Statement & Matrix Representation

Let $G = (V, E)$ be a directed graph where $|V| = n$ and $|E| = m$.
Let $w: E \to \mathbb{R}$ be an arbitrary real-valued weight function mapping edges to costs. Unlike Dijkstra's algorithm, edge weights in the All-Pairs Shortest Path problem may be **strictly negative**, provided that the graph contains **no negative-weight cycles**.

```
                        ALL-PAIRS SHORTEST PATH MATRIX MAPPING
         Input Graph G = (V, E)                       Output Distance Matrix D
         
               (1) ---[3]---> (2)                     1    2    3
              /   ^          /                      +----+----+----+
            [8]   [1]      [2]                    1 |  0 |  3 |  5 |
            /       \      v                      +----+----+----+
          (3) <-----[5]--- ( )                    2 |  7 |  0 |  2 |
                                                  +----+----+----+
                                                3 |  8 | 11 |  0 |
                                                  +----+----+----+
         Compute shortest path between            D[i][j] stores delta(i, j)
         EVERY ordered pair (i, j) \in V x V      for all 1 <= i, j <= n.
```

#### The APSP Objective:
Find the shortest-path distance $\delta(i, j)$ and reconstruct a shortest directed path for **every ordered pair** of vertices $(i, j) \in V \times V$.

#### Mathematical Output Representation:
The output of an APSP algorithm is presented as an $n \times n$ matrix $D = (d_{ij})$, where:
$$d_{ij} = \delta(i, j) \quad \forall i, j \in \{1, 2, \dots, n\}$$

To reconstruct the actual paths, an auxiliary $n \times n$ **predecessor matrix** $\Pi = (\pi_{ij})$ is maintained, where $\pi_{ij}$ denotes the predecessor of vertex $j$ on a shortest path from source vertex $i$ to destination vertex $j$:
$$\pi_{ij} = \begin{cases}
\text{NIL} & \text{if } i = j \text{ or there exists no directed path from } i \text{ to } j, \\
\text{predecessor of } j \text{ on path } i \rightsquigarrow j & \text{if } i \ne j \text{ and } j \text{ is reachable from } i.
\end{cases}$$

---

<a id="apsp-comparison"></a>
### Comparison of APSP Strategies: Repeated SSSP vs. Dynamic Programming

The APSP problem can be solved by running Single-Source Shortest Path (SSSP) algorithms repeatedly from every vertex $v \in V$, or by executing a dedicated all-pairs dynamic programming algorithm.

```
                    APSP ARCHITECTURAL DECISION MATRIX
+-----------------------------------------------------------------------------------+
| APPROACH 1: Repeated Dijkstra's (Non-negative weights only: w(e) >= 0)            |
|   * Using Binary Min-Heap:       |V| * O(E log V)    = O(V * E log V)             |
|   * Using Fibonacci Heap:         |V| * O(E + V log V)= O(V * E + V^2 log V)       |
+-----------------------------------------------------------------------------------+
| APPROACH 2: Repeated Bellman-Ford (General weights, detects negative cycles)     |
|   * Time Complexity:              |V| * O(V * E)      = O(V^2 * E)                |
|   * On Dense Graphs (E ≈ V^2):    O(V^4) (Extremely inefficient!)                |
+-----------------------------------------------------------------------------------+
| APPROACH 3: Floyd-Warshall Algorithm (Dynamic Programming)                        |
|   * Time Complexity:              O(V^3) on ALL graph topologies                  |
|   * Structure: Simple triple-nested loop; extremely low constant factor.          |
+-----------------------------------------------------------------------------------+
| APPROACH 4: Johnson's Algorithm (Reweighting via Bellman-Ford + Dijkstra)         |
|   * Time Complexity:              O(V * E + V^2 log V)                            |
|   * Optimal for: Sparse graphs with negative edge weights.                        |
+-----------------------------------------------------------------------------------+
```

<div class="table-wrap">

| Dimension | Repeated Dijkstra | Repeated Bellman-Ford | Floyd-Warshall | Johnson's Algorithm |
| :--- | :--- | :--- | :--- | :--- |
| **Negative Edges Allowed?** | **No** (Fails completely) | **Yes** | **Yes** | **Yes** |
| **Negative Cycle Detection?** | No | Yes | **Yes** (Inspect diagonal) | Yes |
| **Dense Graph ($E \approx V^2$)**| $O(V^3 \log V)$ | $O(V^4)$ | $\mathbf{O(V^3)}$ **(Optimal)** | $O(V^3)$ |
| **Sparse Graph ($E \approx V$)** | $O(V^2 \log V)$ | $O(V^3)$ | $O(V^3)$ | $\mathbf{O(V^2 \log V)}$ **(Optimal)** |
| **Implementation Complexity** | High (Priority Queues) | Low | **Extremely Low** ($\approx 5$ lines) | High (Reweighting + SSSP) |

</div>

---

<a id="negative-cycles"></a>
### Handling Negative Edge Weights & Negative Cycle Detection

A **negative-weight cycle** is a directed cycle whose total edge weight sum is strictly negative:
$$\sum_{e \in C} w(e) < 0$$

If graph $G$ contains a negative-weight cycle reachable on a path from $i$ to $j$, the shortest path distance $\delta(i, j)$ is undefined and evaluates to $-\infty$, because an algorithm could loop through the cycle indefinitely to produce arbitrarily low path weights.

```
                    NEGATIVE CYCLE ANOMALY DETECTOR
                           
                              [ 2 ]
                     ( 1 ) -----------> ( 2 )
                       ^                 |
                        \               / [ -6 ]
                    [ 1 ] \           v
                           +--------- ( 3 )
                           
          Cycle C = <1, 2, 3, 1> with weight sum: 2 + (-6) + 1 = -3 < 0!
          Traversing cycle k times yields cost -3k -> -∞ as k -> ∞.
```

#### Negative Cycle Detection in Floyd-Warshall:
In any graph without negative cycles, the shortest path from any vertex $i$ to itself contains zero edges and has cost $\delta(i, i) = 0$. 

If a negative-weight cycle exists that passes through vertex $i$, the algorithm eventually evaluates a cyclic path from $i$ back to $i$ whose weight is negative, causing:
$$D^{(n)}[i][i] < 0$$

#### Theorem 1 (Negative Cycle Diagnostic Invariant):
A directed graph $G = (V, E, w)$ contains at least one negative-weight cycle reachable by some vertex if and only if, upon termination of the Floyd-Warshall algorithm, the final distance matrix satisfies:
$$\exists i \in \{1, 2, \dots, n\} \quad \text{such that} \quad D^{(n)}[i][i] < 0$$

---

<a id="floyd-warshall-theory"></a>
## 2. The Floyd-Warshall Algorithm: Theoretical Formulation

<a id="intermediate-concept"></a>
### The Intermediate Vertex Concept ($V^{(k)}$ Subsets)

The key insight behind the Floyd-Warshall algorithm is categorizing shortest paths based on their **intermediate vertices**.

#### Definition 1: Intermediate Vertex
For a simple path $p = \langle v_1, v_2, v_3, \dots, v_{m-1}, v_m \rangle$, an **intermediate vertex** is any vertex on the path other than the initial source vertex $v_1$ and the final destination vertex $v_m$. That is, the intermediate vertices are the set:
$$\text{Intermediate}(p) = \{ v_2, v_3, \dots, v_{m-1} \}$$

#### The Nested Vertex Subsets ($V^{(k)}$):
Let the vertices of $G$ be numbered arbitrarily from $1$ to $n$: $V = \{1, 2, \dots, n\}$.
For any integer $k \in \{0, 1, \dots, n\}$, define the subset of vertices:
$$V^{(k)} = \{1, 2, \dots, k\} \subseteq V$$
* When $k = 0$, $V^{(0)} = \emptyset$. A path whose intermediate vertices come from $V^{(0)}$ can have **no intermediate vertices at all**; it must consist of a single direct edge.
* When $k = n$, $V^{(n)} = V = \{1, 2, \dots, n\}$. A path whose intermediate vertices come from $V^{(n)}$ can use **any vertex** in the graph.

```
                    INTERMEDIATE VERTEX SET PROGRESSION
  k = 0:  V^{(0)} = {}                    Direct edges only (no intermediates allowed)
  k = 1:  V^{(1)} = {1}                   Only vertex 1 may serve as an intermediate step
  k = 2:  V^{(2)} = {1, 2}                Vertices {1, 2} may serve as intermediates
  ...
  k = n:  V^{(n)} = {1, 2, ..., n}        All graph vertices are eligible intermediates
```

---

<a id="recurrence-derivation"></a>
### Derivation of the Triply Nested Dynamic Programming Recurrence

Let $d_{ij}^{(k)}$ denote the weight of a shortest path from vertex $i$ to vertex $j$ such that **all intermediate vertices are drawn exclusively from the subset $V^{(k)} = \{1, 2, \dots, k\}$**.

We want to express $d_{ij}^{(k)}$ in terms of subproblem solutions from stage $k-1$ (which use intermediate vertices drawn only from $V^{(k-1)} = \{1, 2, \dots, k-1\}$).

```
                      THE FLOYD-WARSHALL SUBPATH DICHOTOMY
                      
  CASE 1: Vertex k is NOT an intermediate vertex on the optimal path.
          Path uses only intermediates from {1, ..., k-1}:
          ( i ) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~> ( j )
                             Cost = d_{ij}^{(k-1)}
                             
  ---------------------------------------------------------------------
  
  CASE 2: Vertex k IS an intermediate vertex on the optimal path.
          Path decomposes at vertex k into two subpaths:
          ( i ) ~~~~~~~~~~~~~~> ( k ) ~~~~~~~~~~~~~~> ( j )
                 d_{ik}^{(k-1)}         d_{kj}^{(k-1)}
                 
          Total Candidate Cost = d_{ik}^{(k-1)} + d_{kj}^{(k-1)}
```

For any pair of vertices $i, j \in V$, consider a shortest path $p$ from $i$ to $j$ with intermediate vertices in $\{1, \dots, k\}$. Exactly one of two mutually exclusive cases must hold:

#### Case 1: Vertex $k$ is NOT an intermediate vertex on path $p$.
All intermediate vertices of $p$ must come from $\{1, 2, \dots, k-1\}$.
Therefore, the shortest path from $i$ to $j$ with intermediates in $\{1, \dots, k\}$ is simply the shortest path from $i$ to $j$ with intermediates in $\{1, \dots, k-1\}$:
$$d_{ij}^{(k)} = d_{ij}^{(k-1)}$$

#### Case 2: Vertex $k$ IS an intermediate vertex on path $p$.
Because $p$ is a simple path (assuming no negative cycles), vertex $k$ appears as an intermediate vertex **exactly once**. We can decompose $p$ into two subpaths:
$$p = i \overset{p_1}{\rightsquigarrow} k \overset{p_2}{\rightsquigarrow} j$$
* Subpath $p_1$ runs from $i$ to $k$, with all intermediate vertices drawn from $\{1, \dots, k-1\}$. By Theorem 1 of Module 3.3 (Optimal Substructure), $p_1$ must be a shortest path from $i$ to $k$ with intermediates in $\{1, \dots, k-1\}$. Thus, $w(p_1) = d_{ik}^{(k-1)}$.
* Subpath $p_2$ runs from $k$ to $j$, with all intermediate vertices drawn from $\{1, \dots, k-1\}$. By the same substructure property, $w(p_2) = d_{kj}^{(k-1)}$.
* The total path weight is the sum of the two subpath weights:
$$w(p) = w(p_1) + w(p_2) = d_{ik}^{(k-1)} + d_{kj}^{(k-1)}$$

#### The Fundamental Floyd-Warshall Recurrence:
Combining both cases by taking the minimum value yields the core recurrence:

$$\mathbf{d_{ij}^{(k)} = \min \Big( d_{ij}^{(k-1)}, \; d_{ik}^{(k-1)} + d_{kj}^{(k-1)} \Big)}$$

When $k = n$, every vertex in $V$ is an eligible intermediate vertex. Therefore:
$$d_{ij}^{(n)} = \delta(i, j) \quad \forall i, j \in V$$

---

<a id="base-cases"></a>
### Base Cases and Boundary Matrix Configurations ($D^{(0)}$ and $\Pi^{(0)}$)

Before considering any intermediate vertices ($k = 0$), the base matrix $D^{(0)} = (d_{ij}^{(0)})$ is derived directly from the graph's adjacency matrix and weight function $w$:

$$\mathbf{d_{ij}^{(0)} = \begin{cases} 
0 & \text{if } i = j, \\
w(i, j) & \text{if } i \ne j \text{ and } (i, j) \in E, \\
+\infty & \text{if } i \ne j \text{ and } (i, j) \notin E.
\end{cases}}$$

Correspondingly, the base predecessor matrix $\Pi^{(0)} = (\pi_{ij}^{(0)})$ is defined as:

$$\mathbf{\pi_{ij}^{(0)} = \begin{cases} 
\text{NIL} & \text{if } i = j \text{ or } w(i, j) = +\infty, \\
i & \text{if } i \ne j \text{ and } w(i, j) < +\infty.
\end{cases}}$$

---

<a id="predecessor-matrix"></a>
### The Dual Predecessor Matrix $\Pi^{(k)}$ Mechanics

To reconstruct the shortest path between any pair $(i, j)$, we track predecessors using the matrix $\Pi^{(k)} = (\pi_{ij}^{(k)})$. 
Here, $\pi_{ij}^{(k)}$ records the predecessor of vertex $j$ on a shortest path from $i$ to $j$ using intermediate vertices exclusively from $\{1, \dots, k\}$.

#### Predecessor Update Rule:
When updating distance cell $d_{ij}^{(k)}$:
* **If Case 1 holds** ($d_{ij}^{(k-1)} \le d_{ik}^{(k-1)} + d_{kj}^{(k-1)}$):
  The shortest path did not change; it still does not use vertex $k$. The predecessor of $j$ remains unchanged:
  $$\pi_{ij}^{(k)} = \pi_{ij}^{(k-1)}$$
* **If Case 2 holds** ($d_{ij}^{(k-1)} > d_{ik}^{(k-1)} + d_{kj}^{(k-1)}$):
  The optimal path now routes through vertex $k$ to reach $j$. The final segment of this path is the subpath from $k$ to $j$. Therefore, the predecessor of $j$ is the predecessor of $j$ on the path from $k$ to $j$:
  $$\pi_{ij}^{(k)} = \pi_{kj}^{(k-1)}$$

$$\mathbf{\pi_{ij}^{(k)} = \begin{cases} 
\pi_{ij}^{(k-1)} & \text{if } d_{ij}^{(k-1)} \le d_{ik}^{(k-1)} + d_{kj}^{(k-1)}, \\
\pi_{kj}^{(k-1)} & \text{if } d_{ij}^{(k-1)} > d_{ik}^{(k-1)} + d_{kj}^{(k-1)}.
\end{cases}}$$

---

<a id="algorithm-mechanics"></a>
## 3. Algorithm Implementation & Mechanics

<a id="pseudocode"></a>
### Complete Pseudocode (Matrix Updates & Predecessor Maintenance)

```text
Algorithm FloydWarshall(W, n)
// Input: n x n weight matrix W where W[i][j] = w(i, j)
// Output: Distance matrix D and Predecessor matrix Π
begin
    Allocate D[0..n][1..n][1..n];
    Allocate Π[0..n][1..n][1..n];
    
    // Step 1: Base Case Initialization (k = 0) - O(n^2)
    for i ← 1 to n do
    begin
        for j ← 1 to n do
        begin
            if i = j then
            begin
                D[0][i][j] ← 0;
                Π[0][i][j] ← NIL;
            end
            else if W[i][j] ≠ ∞ then
            begin
                D[0][i][j] ← W[i][j];
                Π[0][i][j] ← i;
            end
            else
            begin
                D[0][i][j] ← ∞;
                Π[0][i][j] ← NIL;
            end;
        end;
    end;
    
    // Step 2: Triply-Nested Dynamic Programming Engine - O(n^3)
    // CRITICAL: Variable k MUST iterate in the outermost loop!
    for k ← 1 to n do
    begin
        for i ← 1 to n do
        begin
            for j ← 1 to n do
            begin
                // Guard against addition with infinity
                if D[k - 1][i][k] ≠ ∞ and D[k - 1][k][j] ≠ ∞ and 
                   (D[k - 1][i][k] + D[k - 1][k][j] < D[k - 1][i][j]) then
                begin
                    D[k][i][j] ← D[k - 1][i][k] + D[k - 1][k][j];
                    Π[k][i][j] ← Π[k - 1][k][j];  // Predecessor is inherited from path k -> j
                end
                else
                begin
                    D[k][i][j] ← D[k - 1][i][j];
                    Π[k][i][j] ← Π[k - 1][i][j];
                end;
            end;
        end;
    end;
    
    // Step 3: Negative-Weight Cycle Detection Pass - O(n)
    for i ← 1 to n do
    begin
        if D[n][i][i] < 0 then
            raise Error("Graph contains a negative-weight cycle!");
    end;
    
    return (D[n], Π[n]);
end;
```

---

<a id="loop-order-proof"></a>
### Why the Triple-Loop Order (k Outer, i Middle, j Inner) is Mandatory

A frequent bug among students is placing the intermediate index $k$ in the innermost loop:

```text
// INCORRECT LOOP ORDER (Destroys DP invariant!):
for i ← 1 to n do
    for j ← 1 to n do
        for k ← 1 to n do
            D[i][j] = min(D[i][j], D[i][k] + D[k][j]);
```

#### Why This Fails:
The DP state is parameterized by $k$, representing the set of allowed intermediate vertices $\{1, \dots, k\}$. 

For the recurrence $d_{ij}^{(k)} = \min(d_{ij}^{(k-1)}, d_{ik}^{(k-1)} + d_{kj}^{(k-1)})$ to be mathematically valid, the sub-paths $i \rightsquigarrow k$ and $k \rightsquigarrow j$ must have **already incorporated all optimizations available from vertices $\{1, \dots, k-1\}$**.

* If $k$ is on the outside, iteration $k$ processes the entire matrix using the completed results of iteration $k-1$. 
* If $k$ is on the inside, when evaluating pair $(i, j)$ at $k=3$, the path from $k$ to $j$ ($3 \rightsquigarrow j$) has not yet been computed for other intermediate vertices. The calculation uses incomplete, non-optimal subpath values, causing the algorithm to miss valid shortest paths.

::: callout-pitfall Loop Order Rule
The loop over the intermediate vertex index $k$ **must always be the outermost loop**.
Iterating $i$ and $j$ inside ensures the entire $n \times n$ matrix transition $D^{(k-1)} \to D^{(k)}$ completes fully before any paths are allowed to use vertex $k+1$ as an intermediate.
:::

---

<a id="space-optimization"></a>
### In-Place Space Optimization: From $O(V^3)$ to $O(V^2)$ Space

Storing every intermediate matrix $D^{(0)}, D^{(1)}, \dots, D^{(n)}$ requires $O(n^3)$ memory. We can drop the superscript $k$ and update a single $n \times n$ matrix $D$ **in-place**:

$$D[i][j] \leftarrow \min(D[i][j], \; D[i][k] + D[k][j])$$

#### Mathematical Justification for In-Place Updates:
Does updating a cell in matrix $D$ during iteration $k$ overwrite values needed by other cells in that same iteration?
Consider the cells in row $k$ and column $k$:
1. For an entry in row $k$ ($i = k$):
   $$D[k][j] \leftarrow \min(D[k][j], \; D[k][k] + D[k][j])$$
   Since the graph contains no negative cycles, $D[k][k] = 0$. 
   Therefore:
   $$\min(D[k][j], \; 0 + D[k][j]) = D[k][j]$$
   Entries in row $k$ do not change during iteration $k$.
2. For an entry in column $k$ ($j = k$):
   $$D[i][k] \leftarrow \min(D[i][k], \; D[i][k] + D[k][k]) = \min(D[i][k], \; D[i][k] + 0) = D[i][k]$$
   Entries in column $k$ do not change during iteration $k$.

Because row $k$ and column $k$ remain constant throughout iteration $k$, updating other cells $D[i][j]$ in-place reads the exact same values of $D[i][k]$ and $D[k][j]$ that existed at the start of the iteration. 

Thus, the algorithm can be executed using **a single $n \times n$ matrix**, reducing auxiliary space complexity from $O(n^3)$ to $\mathbf{O(n^2)}$.

---

<a id="execution-trace"></a>
## 4. Step-by-Step 5W1H Stepped Execution Trace

We trace the Floyd-Warshall algorithm on a 4-vertex directed graph containing both positive and negative edge weights.

<a id="reference-graph"></a>
### Reference Directed Weighted Graph Specification:
* Vertices: $V = \{1, 2, 3, 4\}$, with $|V| = 4$.
* Directed Edge Set with Weights:
  $$E = \{ (1, 2, 3), \; (1, 4, 7), \; (2, 1, 8), \; (2, 3, 2), \; (3, 1, 5), \; (3, 4, 1), \; (4, 1, 2) \}$$

```
                          REFERENCE GRAPH TOPOLOGY
                                   [ 3 ]
                           ( 1 ) ----------> ( 2 )
                           ^ | \             / |
                           | |   \ [7]     /   |
                       [8] | |     v     / [2] | [1]
                           | |      ( 4 )      |
                       [5] | |     ^     \     |
                           | v   / [2]     v   v
                           ( 3 ) <---------- +
```

---

<a id="matrix-progression"></a>
### Stepped Iteration Matrices: $D^{(0)} \to D^{(1)} \to D^{(2)} \to D^{(3)} \to D^{(4)}$

#### Base Matrices: $k = 0$ (Direct Edges Only)

$$D^{(0)} = \begin{pmatrix}
0 & 3 & \infty & 7 \\
8 & 0 & 2 & \infty \\
5 & \infty & 0 & 1 \\
2 & \infty & \infty & 0
\end{pmatrix}
\quad \quad
\Pi^{(0)} = \begin{pmatrix}
\text{NIL} & 1 & \text{NIL} & 1 \\
2 & \text{NIL} & 2 & \text{NIL} \\
3 & \text{NIL} & \text{NIL} & 3 \\
4 & \text{NIL} & \text{NIL} & \text{NIL}
\end{pmatrix}$$

---

#### Iteration $k = 1$: Allowing Intermediate Vertex $\{1\}$

We evaluate $D^{(1)}[i][j] = \min(D^{(0)}[i][j], \; D^{(0)}[i][1] + D^{(0)}[1][j])$.
Row 1 and Column 1 remain unchanged.

* Check $(2, 4)$: $D^{(0)}[2][4] = \infty$. 
  Via vertex 1: $D^{(0)}[2][1] + D^{(0)}[1][4] = 8 + 7 = 15 < \infty$.
  Update: $D^{(1)}[2][4] \leftarrow 15, \quad \Pi^{(1)}[2][4] \leftarrow \Pi^{(0)}[1][4] = 1$.
* Check $(3, 2)$: $D^{(0)}[3][2] = \infty$.
  Via vertex 1: $D^{(0)}[3][1] + D^{(0)}[1][2] = 5 + 3 = 8 < \infty$.
  Update: $D^{(1)}[3][2] \leftarrow 8, \quad \Pi^{(1)}[3][2] \leftarrow \Pi^{(0)}[1][2] = 1$.
* Check $(4, 2)$: $D^{(0)}[4][2] = \infty$.
  Via vertex 1: $D^{(0)}[4][1] + D^{(0)}[1][2] = 2 + 3 = 5 < \infty$.
  Update: $D^{(1)}[4][2] \leftarrow 5, \quad \Pi^{(1)}[4][2] \leftarrow \Pi^{(0)}[1][2] = 1$.
* Check $(4, 4)$: $D^{(0)}[4][4] = 0$.
  Via vertex 1: $D^{(0)}[4][1] + D^{(0)}[1][4] = 2 + 7 = 9 > 0$. Unchanged.

$$D^{(1)} = \begin{pmatrix}
0 & 3 & \infty & 7 \\
8 & 0 & 2 & \mathbf{15} \\
5 & \mathbf{8} & 0 & 1 \\
2 & \mathbf{5} & \infty & 0
\end{pmatrix}
\quad \quad
\Pi^{(1)} = \begin{pmatrix}
\text{NIL} & 1 & \text{NIL} & 1 \\
2 & \text{NIL} & 2 & \mathbf{1} \\
3 & \mathbf{1} & \text{NIL} & 3 \\
4 & \mathbf{1} & \text{NIL} & \text{NIL}
\end{pmatrix}$$

---

<a id="5w1h-trace"></a>
### 5W1H Mechanical Execution of $k=2$ and $k=3$ Transitions

#### Iteration $k = 2$: Allowing Intermediate Vertices $\{1, 2\}$
* **What are we doing?** Testing if routing paths through vertex 2 improves any distances:
  $$D^{(2)}[i][j] = \min(D^{(1)}[i][j], \; D^{(1)}[i][2] + D^{(1)}[2][j])$$
* **Why are we starting here?** Row 2 and Column 2 of $D^{(1)}$ provide the pivot distances.
* **Where did this formula originate?** Floyd-Warshall DP recurrence at step $k=2$.
* **How do we execute the step mechanically?**
  * Check $(1, 3)$: $D^{(1)}[1][3] = \infty$.
    Path via 2: $D^{(1)}[1][2] + D^{(1)}[2][3] = 3 + 2 = 5 < \infty$.
    $$\mathbf{D^{(2)}[1][3] \leftarrow 5, \quad \Pi^{(2)}[1][3] \leftarrow \Pi^{(1)}[2][3] = 2}$$
  * Check $(3, 3)$: $D^{(1)}[3][3] = 0$. Path via 2: $D^{(1)}[3][2] + D^{(1)}[2][3] = 8 + 2 = 10 > 0$. Unchanged.
  * Check $(4, 3)$: $D^{(1)}[4][3] = \infty$.
    Path via 2: $D^{(1)}[4][2] + D^{(1)}[2][3] = 5 + 2 = 7 < \infty$.
    $$\mathbf{D^{(2)}[4][3] \leftarrow 7, \quad \Pi^{(2)}[4][3] \leftarrow \Pi^{(1)}[2][3] = 2}$$
* **What changed from previous step?** Vertices 1 and 4 can now reach vertex 3 at lower costs (costs 5 and 7, respectively) by using vertex 2 as an intermediate step.

$$D^{(2)} = \begin{pmatrix}
0 & 3 & \mathbf{5} & 7 \\
8 & 0 & 2 & 15 \\
5 & 8 & 0 & 1 \\
2 & 5 & \mathbf{7} & 0
\end{pmatrix}
\quad \quad
\Pi^{(2)} = \begin{pmatrix}
\text{NIL} & 1 & \mathbf{2} & 1 \\
2 & \text{NIL} & 2 & 1 \\
3 & 1 & \text{NIL} & 3 \\
4 & 1 & \mathbf{2} & \text{NIL}
\end{pmatrix}$$

---

#### Iteration $k = 3$: Allowing Intermediate Vertices $\{1, 2, 3\}$
Pivot Row: $D^{(2)}[3][*] = [5, 8, 0, 1]$; Pivot Column: $D^{(2)}[*][3] = [5, 2, 0, 7]^T$.

* Check $(1, 4)$: $D^{(2)}[1][4] = 7$.
  Via vertex 3: $D^{(2)}[1][3] + D^{(2)}[3][4] = 5 + 1 = 6 < 7$.
  $$\mathbf{D^{(3)}[1][4] \leftarrow 6, \quad \Pi^{(3)}[1][4] \leftarrow \Pi^{(2)}[3][4] = 3}$$
* Check $(2, 1)$: $D^{(2)}[2][1] = 8$.
  Via vertex 3: $D^{(2)}[2][3] + D^{(2)}[3][1] = 2 + 5 = 7 < 8$.
  $$\mathbf{D^{(3)}[2][1] \leftarrow 7, \quad \Pi^{(3)}[2][1] \leftarrow \Pi^{(2)}[3][1] = 3}$$
* Check $(2, 4)$: $D^{(2)}[2][4] = 15$.
  Via vertex 3: $D^{(2)}[2][3] + D^{(2)}[3][4] = 2 + 1 = 3 < 15$.
  $$\mathbf{D^{(3)}[2][4] \leftarrow 3, \quad \Pi^{(3)}[2][4] \leftarrow \Pi^{(2)}[3][4] = 3}$$

$$D^{(3)} = \begin{pmatrix}
0 & 3 & 5 & \mathbf{6} \\
\mathbf{7} & 0 & 2 & \mathbf{3} \\
5 & 8 & 0 & 1 \\
2 & 5 & 7 & 0
\end{pmatrix}
\quad \quad
\Pi^{(3)} = \begin{pmatrix}
\text{NIL} & 1 & 2 & \mathbf{3} \\
\mathbf{3} & \text{NIL} & 2 & \mathbf{3} \\
3 & 1 & \text{NIL} & 3 \\
4 & 1 & 2 & \text{NIL}
\end{pmatrix}$$

---

#### Iteration $k = 4$: Allowing Intermediate Vertices $\{1, 2, 3, 4\}$
Pivot Row: $D^{(3)}[4][*] = [2, 5, 7, 0]$; Pivot Column: $D^{(3)}[*][4] = [6, 3, 1, 0]^T$.

* Check $(2, 1)$: $D^{(3)}[2][1] = 7$.
  Via vertex 4: $D^{(3)}[2][4] + D^{(3)}[4][1] = 3 + 2 = 5 < 7$.
  $$\mathbf{D^{(4)}[2][1] \leftarrow 5, \quad \Pi^{(4)}[2][1] \leftarrow \Pi^{(3)}[4][1] = 4}$$
* Check $(3, 1)$: $D^{(3)}[3][1] = 5$.
  Via vertex 4: $D^{(3)}[3][4] + D^{(3)}[4][1] = 1 + 2 = 3 < 5$.
  $$\mathbf{D^{(4)}[3][1] \leftarrow 3, \quad \Pi^{(4)}[3][1] \leftarrow \Pi^{(3)}[4][1] = 4}$$
* Check $(3, 2)$: $D^{(3)}[3][2] = 8$.
  Via vertex 4: $D^{(3)}[3][4] + D^{(3)}[4][2] = 1 + 5 = 6 < 8$.
  $$\mathbf{D^{(4)}[3][2] \leftarrow 6, \quad \Pi^{(4)}[3][2] \leftarrow \Pi^{(3)}[4][2] = 1}$$

---

#### Final Output Matrices ($D^{(4)}$ and $\Pi^{(4)}$):

$$\mathbf{D^{(4)} = \begin{pmatrix}
0 & 3 & 5 & 6 \\
5 & 0 & 2 & 3 \\
3 & 6 & 0 & 1 \\
2 & 5 & 7 & 0
\end{pmatrix}}
\quad \quad
\mathbf{\Pi^{(4)} = \begin{pmatrix}
\text{NIL} & 1 & 2 & 3 \\
4 & \text{NIL} & 2 & 3 \\
4 & 1 & \text{NIL} & 3 \\
4 & 1 & 2 & \text{NIL}
\end{pmatrix}}$$

*Check for Negative Cycles:* All diagonal entries $D^{(4)}[i][i] = 0 \ge 0$. The graph contains no negative cycles.

---

<a id="path-reconstruction"></a>
### Recursive Shortest Path Reconstruction Procedure

Using the final predecessor matrix $\Pi = \Pi^{(n)}$, the shortest path from $i$ to $j$ can be printed recursively:

```text
Algorithm PrintAllPairsShortestPath(Π, i, j)
// Input: Predecessor matrix Π, source vertex i, destination vertex j
begin
    if i = j then
        print(i);
    else if Π[i][j] = NIL then
        print("No directed path exists from " + i + " to " + j);
    else
    begin
        PrintAllPairsShortestPath(Π, i, Π[i][j]);
        print(" -> " + j);
    end;
end;
```

#### Tracing Path Reconstruction from Vertex 3 to Vertex 2:
1. Goal: reconstruct path $3 \rightsquigarrow 2$. Look up $\pi_{3, 2}$:
   $$\Pi[3][2] = 1 \implies \text{Predecessor of } 2 \text{ is } 1.$$
2. Now find path from $3$ to $1$. Look up $\pi_{3, 1}$:
   $$\Pi[3][1] = 4 \implies \text{Predecessor of } 1 \text{ is } 4.$$
3. Now find path from $3$ to $4$. Look up $\pi_{3, 4}$:
   $$\Pi[3][4] = 3 \implies \text{Predecessor of } 4 \text{ is } 3.$$
4. Now examine path from $3$ to $3$:
   $$i = j \implies \text{Base reached! Print } 3.$$
5. Unwinding the call stack prints the complete trajectory:
   $$\mathbf{3 \to 4 \to 1 \to 2}$$
   *Cost Verification:* $w(3, 4) + w(4, 1) + w(1, 2) = 1 + 2 + 3 = \mathbf{6} == D^{(4)}[3][2]$. Correct.

---

<a id="warshalls-algorithm"></a>
## 5. Transitive Closure of a Directed Graph: Warshall's Algorithm

<a id="reachability-matrix"></a>
### Reachability Matrix Definition & Boolean Matrix Formulation

#### Definition 2: Transitive Closure
Given a directed graph $G = (V, E)$ with $|V| = n$, the **transitive closure** of $G$ is defined as the graph $G^* = (V, E^*)$ where:
$$E^* = \{ (i, j) : \text{there exists a directed path of length } \ge 0 \text{ from } i \text{ to } j \text{ in } G \}$$

The transitive closure is represented by an $n \times n$ boolean **Reachability Matrix** $T = (t_{ij})$, where:
$$t_{ij} = \begin{cases} 
1 & \text{if there exists a directed path from } i \text{ to } j, \\
0 & \text{otherwise.}
\end{cases}$$

---

<a id="warshall-recurrence"></a>
### Logical Warshall Recurrence (OR-AND Bitwise Formulation)

Stephen Warshall (1962) adapted the dynamic programming recurrence of Floyd to operate on **boolean matrices using logical operators**.

Let $t_{ij}^{(k)} = 1$ if there exists a path from $i$ to $j$ with all intermediate vertices drawn from $\{1, 2, \dots, k\}$, and $0$ otherwise.

#### Base Case ($k = 0$):
$$t_{ij}^{(0)} = \begin{cases} 
1 & \text{if } i = j \text{ or } (i, j) \in E, \\
0 & \text{if } i \ne j \text{ and } (i, j) \notin E.
\end{cases}$$

#### The Logical Recurrence Relation:
A path from $i$ to $j$ with intermediate vertices in $\{1, \dots, k\}$ exists if:
1. A path already existed using intermediate vertices from $\{1, \dots, k-1\}$ ($t_{ij}^{(k-1)} = 1$), **OR**
2. A path exists from $i$ to $k$ **AND** a path exists from $k$ to $j$ using intermediates in $\{1, \dots, k-1\}$ ($t_{ik}^{(k-1)} \land t_{kj}^{(k-1)} = 1$).

$$\mathbf{t_{ij}^{(k)} = t_{ij}^{(k-1)} \lor \Big( t_{ik}^{(k-1)} \land t_{kj}^{(k-1)} \Big)}$$

#### Bitwise Pseudocode:
```text
Algorithm WarshallTransitiveClosure(AdjMatrix, n)
// Input: n x n boolean Adjacency Matrix
// Output: n x n boolean Transitive Closure Matrix T
begin
    T ← Copy(AdjMatrix);
    
    // Set reflexive diagonals to 1
    for i ← 1 to n do
        T[i][i] ← 1;
        
    for k ← 1 to n do
    begin
        for i ← 1 to n do
        begin
            for j ← 1 to n do
            begin
                T[i][j] ← T[i][j] OR (T[i][k] AND T[k][j]);
            end;
        end;
    end;
    
    return T;
end;
```

---

<a id="floyd-vs-warshall"></a>
### Comparison: Floyd-Warshall vs. Warshall

<div class="table-wrap">

| Dimension | Floyd-Warshall Algorithm | Warshall's Algorithm |
| :--- | :--- | :--- |
| **Problem Solved** | **All-Pairs Shortest Path (APSP)** | **Transitive Closure (Reachability)** |
| **Edge Weights** | Real-valued numbers ($w(e) \in \mathbb{R}$) | Unweighted / Boolean existence |
| **Data Types** | Arithmetic Floating-point / Integers | **Boolean values** (`0` or `1`, `true`/`false`) |
| **Underlying Operators** | $\min(+)$ semiring: $\min(d_{ij}, d_{ik} + d_{kj})$ | Boolean semiring: $t_{ij} \lor (t_{ik} \land t_{kj})$ |
| **Time Complexity** | $\Theta(V^3)$ arithmetic operations | $\Theta(V^3)$ boolean operations ($O(V^3 / 64)$ with bitsets) |
| **Space Complexity** | $O(V^2)$ storage for numeric distances | $O(V^2)$ storage (can be packed into bit vectors) |

</div>

---

<a id="exam-summary"></a>
## 6. KTU Exam High-Yield Summary

<a id="three-mark-questions"></a>
### Frequently Asked 3-Mark Questions & Model Answers

#### Q1: State the Floyd-Warshall recurrence relation for all-pairs shortest paths.
**Model Answer:**
For a graph with vertices numbered $1 \dots n$, let $d_{ij}^{(k)}$ be the shortest path distance from $i$ to $j$ using intermediate vertices drawn exclusively from $\{1, \dots, k\}$. The recurrence is:
$$d_{ij}^{(k)} = \min \Big( d_{ij}^{(k-1)}, \; d_{ik}^{(k-1)} + d_{kj}^{(k-1)} \Big)$$
with base case $d_{ij}^{(0)} = w(i, j)$ if $(i, j) \in E$, $0$ if $i = j$, and $\infty$ otherwise.

---

#### Q2: How does the Floyd-Warshall algorithm detect the presence of negative-weight cycles?
**Model Answer:**
In a graph with no negative cycles, the shortest path from any vertex $i$ to itself has distance $d_{ii} = 0$. If the graph contains a reachable negative-weight cycle passing through vertex $i$, traversing that cycle reduces the distance below zero. Therefore, if:
$$\exists i \in \{1, \dots, n\} \quad \text{such that} \quad D^{(n)}[i][i] < 0$$
the graph contains at least one negative-weight cycle.

---

#### Q3: Why must the loop over variable $k$ be placed as the outermost loop in Floyd-Warshall?
**Model Answer:**
The dynamic programming formulation relies on subproblems where paths are allowed to use intermediate vertices only from the subset $\{1, \dots, k\}$. Placing $k$ in the outermost loop guarantees that all pairs $(i, j)$ have their shortest paths fully computed using intermediate vertices up to $k-1$ before any path is allowed to use vertex $k$ as an intermediate.

---

#### Q4: Write the logical recurrence relation for Warshall's Transitive Closure algorithm.
**Model Answer:**
Let $t_{ij}^{(k)}$ be a boolean variable indicating whether a directed path exists from vertex $i$ to vertex $j$ using intermediate vertices only from $\{1, \dots, k\}$. The recurrence is:
$$t_{ij}^{(k)} = t_{ij}^{(k-1)} \lor \Big( t_{ik}^{(k-1)} \land t_{kj}^{(k-1)} \Big)$$

---

<a id="marking-traps"></a>
### High-Frequency Student Pitfalls & Marking Traps

::: callout-exam Exam Traps & Avoidance Strategies
1. **The Predecessor Update Misattribution:**
   * *The Error:* When updating matrix cell $d_{ij}^{(k)}$ via vertex $k$, setting $\pi_{ij}^{(k)} \leftarrow k$.
   * *The Fix:* Vertex $k$ is not necessarily the *immediate* predecessor of $j$; it is merely an intermediate vertex on the path. The immediate predecessor of $j$ on the path from $k$ to $j$ is **$\Pi^{(k-1)}[k][j]$**. Always write:
     $$\Pi^{(k)}[i][j] \leftarrow \Pi^{(k-1)}[k][j]$$

2. **Base Matrix Diagonal Misconfiguration:**
   * *The Error:* Initializing diagonal entries $D^{(0)}[i][i]$ with positive edge weights when a self-loop $(i, i)$ exists with weight $w(i, i) > 0$.
   * *The Fix:* In simple shortest path definitions, the path from a vertex to itself with zero edges has cost $0$. Unless the self-loop has negative weight, always initialize the diagonal to **$D^{(0)}[i][i] = 0$**.

3. **Infinity Addition Arithmetic Overflow:**
   * *The Error:* Writing code or traces where $\infty + \text{weight}$ wraps around to a negative number or evaluates to a smaller value.
   * *The Fix:* When performing hand traces or writing code, check explicitly: if either $D[i][k] = \infty$ or $D[k][j] = \infty$, the sum $D[i][k] + D[k][j]$ cannot be used to update $D[i][j]$.

4. **Omitting the Intermediate Matrix Stages:**
   * *The Error:* Jumping directly from $D^{(0)}$ to $D^{(4)}$ in exam answers without writing the intermediate steps.
   * *The Fix:* KTU marking schemes assign marks per matrix step ($D^{(1)}, D^{(2)}$, etc.). Always show each intermediate matrix and highlight at least two cells that updated during that iteration.
:::
