# Module 3.3: Single-Source Shortest Paths — Dijkstra's Algorithm
**Course Code: PCCST502 | Design and Analysis of Algorithms | KTU 2024 Scheme**

---

### Table of Contents
1. [Single-Source Shortest Path (SSSP) Problem Formulation](#sssp-formulation)
   - [Formal Graph Definitions & Path Weight Metrics](#formal-definitions)
   - [The Shortest Path Distance Function $\delta(u, v)$](#distance-function)
   - [Optimal Substructure of Shortest Paths: Theorem & Cut-and-Paste Proof](#optimal-substructure)
2. [Triangle Inequality & The Relaxation Technique](#triangle-relaxation)
   - [The Triangle Inequality Property: Theorem & Formal Derivation](#triangle-inequality)
   - [Upper-Bound Invariant & Convergence Properties](#upper-bound-property)
   - [The Edge Relaxation Primitive (`Relax(u, v, w)`)](#relaxation-primitive)
3. [Dijkstra's Algorithm: Architecture & Theoretical Foundations](#dijkstras-algorithm)
   - [The Greedy Selection Paradigm & Settled-Set Invariant](#greedy-paradigm)
   - [Complete Pseudocode (Adjacency List & Priority Queue)](#algorithm-pseudocode)
   - [Rigorous Mathematical Proof of Correctness (Loop Invariant Proof)](#correctness-proof)
   - [The Non-Negative Edge Weight Constraint](#non-negative-constraint)
   - [Step-by-Step Counterexample: Catastrophic Failure on Negative Edges](#negative-counterexample)
4. [Step-by-Step 5W1H Stepped Execution Trace](#execution-trace)
   - [Reference Directed Weighted Graph Specification](#reference-graph)
   - [Stepped Iteration Execution Walkthrough](#trace-walkthrough)
   - [Consolidated State Transition Matrix](#state-matrix)
5. [Detailed Asymptotic Complexity Analysis Across Implementations](#complexity-analysis)
   - [Operation Frequency Budget Breakdown](#frequency-budget)
   - [Implementation A: Unordered Array / Linear Search ($O(|V|^2)$)](#impl-array)
   - [Implementation B: Binary Min-Heap ($O((|V| + |E|) \log |V|)$)](#impl-binary-heap)
   - [Implementation C: Fibonacci Heap ($O(|E| + |V| \log |V|)$)](#impl-fib-heap)
   - [Comparative Implementation Trade-Off Matrix](#comparative-matrix)
6. [KTU Exam High-Yield Summary](#exam-summary)
   - [Frequently Asked 3-Mark Questions & Model Answers](#three-mark-questions)
   - [High-Frequency Student Pitfalls & Marking Traps](#marking-traps)

---

<a id="sssp-formulation"></a>
## 1. Single-Source Shortest Path (SSSP) Problem Formulation

<a id="formal-definitions"></a>
### Formal Graph Definitions & Path Weight Metrics

Let $G = (V, E)$ be a directed graph (digraph) where:
* $V$ denotes the finite set of vertices, with cardinality $|V| = n$.
* $E \subseteq V \times V$ denotes the set of directed edges, with cardinality $|E| = m$.
* $w: E \to \mathbb{R}$ is a weight function mapping directed edges to real-valued costs.

```
                    DIRECTED WEIGHTED PATH REPRESENTATION
                     
             e_1=(v_0,v_1)        e_2=(v_1,v_2)             e_k=(v_{k-1},v_k)
       (v_0) ------------> (v_1) ------------> (v_2) ... -------------> (v_k)
               w(e_1)               w(e_2)                    w(e_k)
               
       Path p = <v_0, v_1, v_2, ..., v_k> with total weight w(p) = ∑ w(v_{i-1}, v_i)
```

#### Definition 1: Path Weight
Given a path $p = \langle v_0, v_1, v_2, \dots, v_k \rangle$ from vertex $v_0$ to vertex $v_k$, the weight of the path, denoted $w(p)$, is defined as the sum of the weights of its constituent edges:
$$w(p) = \sum_{i=1}^k w(v_{i-1}, v_i)$$

---

<a id="distance-function"></a>
### The Shortest Path Distance Function $\delta(u, v)$

#### Definition 2: Shortest Path Distance
The **shortest-path distance** $\delta(u, v)$ from vertex $u$ to vertex $v$ is the infimum of the weights of all paths connecting $u$ to $v$:
$$\delta(u, v) = \begin{cases} 
\min \{ w(p) : u \overset{p}{\rightsquigarrow} v \} & \text{if there exists a path from } u \text{ to } v, \\
+\infty & \text{if there is no directed path from } u \text{ to } v.
\end{cases}$$

A path $p^*$ from $u$ to $v$ is qualified as a **shortest path** if and only if:
$$w(p^*) = \delta(u, v)$$

#### The Single-Source Shortest Path (SSSP) Objective:
Given a designated source vertex $s \in V$, the SSSP problem requires determining the shortest path distance $\delta(s, v)$ and constructing an explicit shortest path from $s$ to every vertex $v \in V$.

---

<a id="optimal-substructure"></a>
### Optimal Substructure of Shortest Paths: Theorem & Cut-and-Paste Proof

Shortest path algorithms exploit the fundamental structural property that optimal solutions are composed of optimal sub-solutions.

#### Theorem 1 (Subpaths of Shortest Paths are Shortest Paths):
Let $G = (V, E, w)$ be a weighted directed graph. Let $p = \langle v_0, v_1, \dots, v_k \rangle$ be a shortest path from vertex $v_0$ to vertex $v_k$. For any intermediate indices $i$ and $j$ such that $0 \le i \le j \le k$, let $p_{ij} = \langle v_i, v_{i+1}, \dots, v_j \rangle$ be the subpath of $p$ running from vertex $v_i$ to vertex $v_j$. 
Then, $p_{ij}$ is a shortest path from $v_i$ to $v_j$.

```
                       OPTIMAL SUBSTRUCTURE TOPOLOGY
                       
                 +----------------- Path p -----------------+
                 |                                          |
                (v_0) ~~~~~> (v_i) ===== p_{ij} =====> (v_j) ~~~~~> (v_k)
                  |     p_{0i}                          p_{jk}  |
                  +---------------------------------------------+
                                       ^
               If a strictly shorter subpath p'_{ij} existed,
               replacing p_{ij} with p'_{ij} would make the entire
               path p shorter, contradicting its optimality!
```

#### Mathematical Proof (Proof by Cut-and-Paste / Contradiction):
1. **Decomposition of Path Weight:**
   The path $p$ can be partitioned into three sequential segments:
   $$p = v_0 \overset{p_{0i}}{\rightsquigarrow} v_i \overset{p_{ij}}{\rightsquigarrow} v_j \overset{p_{jk}}{\rightsquigarrow} v_k$$
   By the additive definition of path weights:
   $$w(p) = w(p_{0i}) + w(p_{ij}) + w(p_{jk})$$

2. **Hypothesis for Contradiction:**
   Suppose that $p_{ij}$ is **not** a shortest path from $v_i$ to $v_j$. 
   Then, there must exist an alternative path $p'_{ij}$ connecting $v_i$ to $v_j$ whose total weight is strictly less than that of $p_{ij}$:
   $$w(p'_{ij}) < w(p_{ij})$$

3. **Synthesis of Modified Global Path ($p'$):**
   Construct a modified path $p'$ from $v_0$ to $v_k$ by cutting out subpath $p_{ij}$ from $p$ and pasting in subpath $p'_{ij}$:
   $$p' = v_0 \overset{p_{0i}}{\rightsquigarrow} v_i \overset{p'_{ij}}{\rightsquigarrow} v_j \overset{p_{jk}}{\rightsquigarrow} v_k$$

4. **Weight Evaluation of the Synthesized Path:**
   Compute the total weight of $p'$:
   $$w(p') = w(p_{0i}) + w(p'_{ij}) + w(p_{jk})$$
   Substitute the inequality $w(p'_{ij}) < w(p_{ij})$ into the equation:
   $$w(p') = w(p_{0i}) + w(p'_{ij}) + w(p_{jk}) < w(p_{0i}) + w(p_{ij}) + w(p_{jk}) = w(p)$$
   $$\implies w(p') < w(p)$$

5. **Contradiction:**
   The deduction $w(p') < w(p)$ asserts the existence of a path $p'$ from $v_0$ to $v_k$ with a weight strictly lower than $w(p)$. This directly contradicts the foundational premise that $p$ was a **shortest path** from $v_0$ to $v_k$ ($w(p) = \delta(v_0, v_k)$).
   
   Therefore, the assumption that $w(p'_{ij}) < w(p_{ij})$ must be false. It follows that:
   $$w(p_{ij}) = \delta(v_i, v_j)$$
   The subpath $p_{ij}$ is inherently a shortest path. $\blacksquare$

---

<a id="triangle-relaxation"></a>
## 2. Triangle Inequality & The Relaxation Technique

<a id="triangle-inequality"></a>
### The Triangle Inequality Property: Theorem & Formal Derivation

#### Theorem 2 (The Triangle Inequality):
Let $G = (V, E, w)$ be a directed weighted graph with source vertex $s \in V$. For any directed edge $(u, v) \in E$, the shortest path distance function satisfies:
$$\delta(s, v) \le \delta(s, u) + w(u, v)$$

```
                         THE TRIANGLE INEQUALITY
                                  ( s )
                                 /     \
                \delta(s, u)   /         \   \delta(s, v)
                             v             v
                           ( u ) --------> ( v )
                                  w(u, v)
                                  
     The true shortest path from s to v cannot be longer than the path
     formed by traveling from s to u via the shortest path and then
     taking the direct edge (u, v).
```

#### Mathematical Proof:
1. **Case A (Unreachability):**
   If vertex $u$ is unreachable from $s$, then $\delta(s, u) = +\infty$. 
   The inequality trivially holds as:
   $$\delta(s, v) \le +\infty + w(u, v) = +\infty$$

2. **Case B (Reachability):**
   Assume $u$ is reachable from $s$. Let $p_{su}^*$ be a true shortest path from $s$ to $u$, such that $w(p_{su}^*) = \delta(s, u)$.
   Since edge $(u, v) \in E$, we can concatenate edge $(u, v)$ onto path $p_{su}^*$ to construct a candidate path $p_{sv}$ from $s$ to $v$:
   $$p_{sv} = s \overset{p_{su}^*}{\rightsquigarrow} u \to v$$

3. **Weight Evaluation:**
   The weight of this concatenated candidate path is:
   $$w(p_{sv}) = w(p_{su}^*) + w(u, v) = \delta(s, u) + w(u, v)$$

4. **Application of the Infimum Definition:**
   By Definition 2, $\delta(s, v)$ is the minimum possible weight among *all* valid paths from $s$ to $v$. Therefore, $\delta(s, v)$ must be less than or equal to the weight of the specific candidate path $p_{sv}$:
   $$\delta(s, v) \le w(p_{sv})$$
   Substituting the weight expression yields:
   $$\delta(s, v) \le \delta(s, u) + w(u, v) \quad \blacksquare$$

---

<a id="upper-bound-property"></a>
### Upper-Bound Invariant & Convergence Properties

Throughout shortest-path algorithms, every vertex $v \in V$ maintains an algorithmic state variable:
* **$d[v]$ (Tentative Distance Estimate):** An upper bound on the true shortest-path distance $\delta(s, v)$.
* **$\pi[v]$ (Predecessor / Parent Pointer):** The predecessor of vertex $v$ on the current tentative shortest path from $s$.

#### Invariant 1 (Upper-Bound Property):
For all vertices $v \in V$, the estimate $d[v]$ satisfies:
$$d[v] \ge \delta(s, v) \quad \forall v \in V$$
Furthermore, once $d[v]$ achieves the lower limit $d[v] = \delta(s, v)$, its value never increases or changes.

#### Invariant 2 (Convergence Property):
Let $s \rightsquigarrow u \to v$ be a shortest path in $G$. If $d[u] = \delta(s, u)$ at any point prior to relaxing edge $(u, v)$, then immediately following the relaxation of $(u, v)$, we obtain:
$$d[v] = \delta(s, v)$$

---

<a id="relaxation-primitive"></a>
### The Edge Relaxation Primitive (`Relax(u, v, w)`)

The term **relaxation** denotes the process of testing whether traversing a specific directed edge $(u, v)$ provides a path to vertex $v$ that is cheaper than the currently known tentative estimate $d[v]$. If it does, $d[v]$ and $\pi[v]$ are updated accordingly.

```
                         THE RELAXATION OPERATION
      Before Relax(u, v, w):
           d[u] = 5                  w(u,v) = 2               d[v] = 9
            ( u ) ------------------------------------------> ( v )
            
      Evaluation:
           Tentative Cost via u = d[u] + w(u, v) = 5 + 2 = 7
           Comparison: 7 < 9 (Improvement Found!)
           
      After Relax(u, v, w):
           d[u] = 5                  w(u,v) = 2               d[v] = 7  <-- UPDATED!
            ( u ) ------------------------------------------> ( v )
                                                               \pi[v] = u
```

#### Complete Relaxation Mechanics and Pseudocode:

```text
Algorithm InitializeSingleSource(G = (V, E), s)
// Input: Directed graph G = (V, E) and source vertex s
// Output: Initialized arrays d[1..n] and π[1..n]
begin
    for each vertex v ∈ V do
    begin
        d[v] ← +∞;                   // Set initial distance estimate to infinity
        π[v] ← NIL;                  // Clear parent pointers
    end;
    d[s] ← 0;                        // Distance from source to itself is strictly zero
end;

Algorithm Relax(u, v, w)
// Input: Edge endpoints u and v, and edge weight matrix/function w
// Invariant Preserved: d[v] >= delta(s, v)
begin
    if d[v] > d[u] + w(u, v) then
    begin
        d[v] ← d[u] + w(u, v);      // Pull down the upper bound
        π[v] ← u;                   // Update predecessor pointer
    end;
end;
```

#### Proof that Relaxation Preserves the Upper-Bound Invariant:
* **Base Case:** Prior to any relaxation, `InitializeSingleSource` sets $d[s] = 0 \ge \delta(s, s)$ (since $\delta(s, s) = 0$ in the absence of negative cycles) and $d[v] = +\infty \ge \delta(s, v)$ for all $v \ne s$. The invariant holds initially.
* **Inductive Step:** Suppose $d[x] \ge \delta(s, x)$ for all $x \in V$. The only operation that modifies an estimate is the assignment:
  $$d[v] \leftarrow d[u] + w(u, v)$$
  By the inductive hypothesis, $d[u] \ge \delta(s, u)$. 
  Coupled with the Triangle Inequality ($\delta(s, v) \le \delta(s, u) + w(u, v)$), we obtain:
  $$d[v] = d[u] + w(u, v) \ge \delta(s, u) + w(u, v) \ge \delta(s, v)$$
  Thus, $d[v] \ge \delta(s, v)$ continues to hold. The upper bound is never violated. $\blacksquare$

---

<a id="dijkstras-algorithm"></a>
## 3. Dijkstra's Algorithm: Architecture & Theoretical Foundations

<a id="greedy-paradigm"></a>
### The Greedy Selection Paradigm & Settled-Set Invariant

Dijkstra’s algorithm solves the SSSP problem on a directed graph with **strictly non-negative edge weights**:
$$w(u, v) \ge 0 \quad \forall (u, v) \in E$$

It maintains a dynamic set of settled vertices, denoted $S \subseteq V$, for which the shortest-path distance has already been determined:
$$\forall u \in S, \quad d[u] = \delta(s, u)$$

```
                  DIJKSTRA'S GREEDY SETTLED-SET BOUNDARY
                     
           Settled Vertex Set S            Unvisited Set V \ S (Priority Queue Q)
      +-----------------------------+     +---------------------------------------+
      |                             |     |                                       |
      |   ( s ) ----> ( a )         |     |      ( c )                            |
      |     \        /              |     |     ^                                 |
      |      v      v               |     |    /                                  |
      |        ( b )                |====>|  ( u* ) <--- Min key extracted from Q!|
      |                             |     |   \          d[u*] = delta(s, u*)     |
      |  d[x] = delta(s, x)         |     |    v                                  |
      |  is permanently finalized!  |     |   ( d )          ( e )                |
      +-----------------------------+     +---------------------------------------+
                                           Picks vertex u* with MINIMUM d[u*]!
```

#### The Greedy Choice Strategy:
At each iteration, Dijkstra’s algorithm extracts the vertex $u^* \in V \setminus S$ that has the **minimum tentative distance estimate**:
$$u^* = \arg\min_{v \in V \setminus S} d[v]$$
The algorithm then transfers $u^*$ into $S$ and relaxes all outgoing edges $(u^*, v) \in E$.

---

<a id="algorithm-pseudocode"></a>
### Complete Pseudocode (Adjacency List & Priority Queue)

```text
Algorithm Dijkstra(G = (V, E, w), s)
// Input: Directed graph G represented via adjacency lists, weight function w >= 0, source s
// Output: Arrays d[1..n] containing shortest path distances, and π[1..n] containing the SSSP tree
begin
    InitializeSingleSource(G, s);
    
    S ← ∅;                            // Initialize settled vertex set to empty
    
    // Instantiate Min-Priority Queue containing all vertices keyed on d[v]
    // BuildMinHeap requires O(V) time
    Q ← BuildMinHeap(V, d);
    
    while Q ≠ ∅ do
    begin
        // Extract-Min: Select unvisited vertex u with the smallest tentative distance
        u ← ExtractMin(Q);           // Runs |V| times
        S ← S ∪ {u};                  // Add vertex u to the settled set
        
        // Traverse adjacency list of u to relax all outgoing directed edges
        for each outgoing neighbor v ∈ Adj[u] do
        begin
            // Relaxation Condition check
            if d[v] > d[u] + w(u, v) then
            begin
                d[v] ← d[u] + w(u, v);
                π[v] ← u;
                DecreaseKey(Q, v, d[v]); // Update key position inside Min-Heap: O(log V)
            end;
        end;
    end;
    
    return (d, π);
end;
```

---

<a id="correctness-proof"></a>
### Rigorous Mathematical Proof of Correctness (Loop Invariant Proof)

We prove the correctness of Dijkstra's algorithm by mathematical induction on the size of the settled set $S$.

#### Loop Invariant:
At the start of each iteration of the `while` loop, for every vertex $x \in S$:
$$d[x] = \delta(s, x)$$

#### 1. Initialization (Base Case: $|S| = 0$):
Before the first iteration, $S = \emptyset$. The invariant holds vacuously because there are no vertices in $S$.

#### 2. Maintenance (Inductive Step):
Assume the invariant holds at the beginning of an iteration: $d[x] = \delta(s, x)$ for all $x \in S$. 
We must show that when the algorithm selects $u = \text{ExtractMin}(Q)$ to add to $S$, it is guaranteed that:
$$d[u] = \delta(s, u)$$

```
                  PROOF BY CONTRADICTION GEOMETRIC TOPOLOGY
                        
                 +---------- Set S ----------+     +------- Set V \ S -------+
                 |                           |     |                         |
                 |   ( s ) ~~~~~> ( x ) ------> ( y ) ~~~~~> ( u )           |
                 |                           |  |  |                         |
                 +---------------------------+  |  +-------------------------+
                                                |
                              Edge (x, y) crosses boundary!
                              y is the FIRST vertex on path p outside S.
```

##### Proof by Contradiction:
1. **Hypothesis for Contradiction:**
   Suppose that $d[u] \ne \delta(s, u)$. By Invariant 1 (Upper-Bound Property), $d[u] \ge \delta(s, u)$. Thus, non-equality implies:
   $$d[u] > \delta(s, u)$$

2. **Path Analysis:**
   Because $d[u] > \delta(s, u)$, there must exist a true shortest path $p$ from $s$ to $u$. 
   Since $s \in S$ and $u \in V \setminus S$, the path $p$ begins inside $S$ and ends outside $S$. 
   Therefore, $p$ must cross the boundary from $S$ to $V \setminus S$ at least once.

3. **Identification of Crossing Node ($y$):**
   Let $y$ be the **first vertex** on path $p$ that belongs to $V \setminus S$, and let $x \in S$ be the immediate predecessor of $y$ on path $p$ (note that $x$ could be $s$, in which case the edge is $(s, y)$). 
   Decompose path $p$:
   $$s \overset{p_{sx}}{\rightsquigarrow} x \to y \overset{p_{yu}}{\rightsquigarrow} u$$

4. **Distance Evaluation at $y$:**
   Since $p$ is a shortest path from $s$ to $u$, by Theorem 1 (Optimal Substructure), its subpath from $s$ to $y$ is a shortest path from $s$ to $y$:
   $$\delta(s, y) = w(p_{sy})$$
   Because $x \in S$, by the inductive hypothesis, $d[x] = \delta(s, x)$. 
   When $x$ was added to $S$, the edge $(x, y)$ was relaxed. By Invariant 2 (Convergence Property):
   $$d[y] = \delta(s, y)$$

5. **Inequality Derivation:**
   Because $y$ precedes or equals $u$ on path $p$, and **all edge weights are non-negative ($w(e) \ge 0$)**:
   $$\delta(s, y) \le \delta(s, u)$$
   Combining $d[y] = \delta(s, y)$ with this inequality yields:
   $$d[y] \le \delta(s, u)$$

6. **Greedy Choice Contradiction:**
   Both $u$ and $y$ reside in $V \setminus S$ (they are both members of queue $Q$). 
   The algorithm selected $u = \text{ExtractMin}(Q)$ because $u$ had the minimal tentative distance among all vertices in $Q$:
   $$d[u] \le d[y]$$
   We now assemble the chain of inequalities:
   $$d[u] \le d[y] = \delta(s, y) \le \delta(s, u) \le d[u]$$
   This forces equality across every term:
   $$d[u] = \delta(s, u)$$
   This directly contradicts our initial assumption that $d[u] > \delta(s, u)$.

Therefore, $d[u] = \delta(s, u)$ must hold when $u$ is added to $S$. The invariant is maintained.

#### 3. Termination:
At termination, $Q = \emptyset \implies S = V$. 
By the maintained invariant, $d[v] = \delta(s, v)$ for every vertex $v \in V$. $\blacksquare$

---

<a id="non-negative-constraint"></a>
### The Non-Negative Edge Weight Constraint

Dijkstra’s algorithm relies entirely on the premise that a path can **never become shorter by adding more edges**. 
Mathematically:
$$\forall (u, v) \in E, \quad w(u, v) \ge 0 \implies \delta(s, u) \le \delta(s, u) + w(u, v)$$

If negative edge weights exist ($w(u, v) < 0$), extending a path can reduce its total weight, breaking the greedy choice property.

---

<a id="negative-counterexample"></a>
### Step-by-Step Counterexample: Catastrophic Failure on Negative Edges

We demonstrate how a negative edge causes Dijkstra's algorithm to compute an incorrect shortest path.

#### Graph Counterexample Topology:
* Vertices: $V = \{S, A, B\}$ with source $s = S$.
* Edges:
  $$E = \{ (S, A, 3), \; (S, B, 5), \; (B, A, -4) \}$$

```
                   NEGATIVE WEIGHT COUNTEREXAMPLE TOPOLOGY
                   
                                     [ 3 ]
                             ( S ) ----------> ( A )
                               \                 ^
                                \               /
                            [ 5 ] \           / [ -4 ] (NEGATIVE EDGE!)
                                   v         /
                                     ( B ) -+
                                     
            Shortest path from S to A is NOT the direct edge S -> A (cost 3).
            The true shortest path is S -> B -> A with cost: 5 + (-4) = 1.
```

---

#### 5W1H Execution Trace on Counterexample:

##### Step 1: Initialization
* $d[S] = 0, \quad d[A] = \infty, \quad d[B] = \infty$
* $S_{\text{settled}} = \emptyset, \quad Q = \{ (S, 0), (A, \infty), (B, \infty) \}$

##### Step 2: Processing Source Vertex $S$
* **What are we doing?** Extracting $S$ from $Q$ and relaxing its outgoing edges.
* **Why are we starting here?** $d[S] = 0$ is the minimum value in $Q$.
* **How do we execute the step mechanically?**
  $$\text{ExtractMin}(Q) \implies u = S. \quad S_{\text{settled}} \leftarrow \{S\}$$
  $$\text{Relax}(S, A): d[A] > d[S] + w(S, A) \ ( \infty > 0 + 3 ) \implies d[A] \leftarrow 3, \; \pi[A] \leftarrow S$$
  $$\text{Relax}(S, B): d[B] > d[S] + w(S, B) \ ( \infty > 0 + 5 ) \implies d[B] \leftarrow 5, \; \pi[B] \leftarrow S$$
* **What changed from previous step?** $S$ is settled. $Q$ state: $\{ (A, 3), (B, 5) \}$.

---

##### Step 3: The Fatal Greedy Choice (Processing Vertex $A$)
* **What are we doing?** Extracting the minimum element from $Q = \{ (A, 3), (B, 5) \}$.
* **Why are we starting here?** The greedy heuristic chooses $A$ because $d[A] = 3 < d[B] = 5$.
* **Where did this formula originate?** The invariant assumption that $d[u] = \min_{v \in Q} d[v] \implies d[u] = \delta(s, u)$.
* **How do we execute the step mechanically?**
  $$\text{ExtractMin}(Q) \implies u = A$$
  $$\mathbf{S_{\text{settled}} \leftarrow \{S, A\} \quad \text{(Vertex A is permanently finalized with } d[A] = 3!)}$$
  Vertex $A$ has no outgoing edges. No relaxations occur.
* **What changed from previous step?** $A$ is permanently committed to $S_{\text{settled}}$. $Q$ state: $\{ (B, 5) \}$.

---

##### Step 4: Processing Vertex $B$ and Late Discovery
* **What are we doing?** Extracting the final vertex $B$ from $Q = \{ (B, 5) \}$.
* **Why are we starting here?** $B$ is the sole remaining vertex in $Q$.
* **How do we execute the step mechanically?**
  $$\text{ExtractMin}(Q) \implies u = B. \quad S_{\text{settled}} \leftarrow \{S, A, B\}$$
  $$\text{Relax neighbor } A \text{ via edge } (B, A):$$
  $$\text{Cost via } B = d[B] + w(B, A) = 5 + (-4) = 1$$
  $$\text{Compare: } \mathbf{d[B] + w(B, A) = 1 < d[A] = 3}$$
* **The Failure:** 
  In standard Dijkstra's algorithm, **vertex $A$ is already marked finalized** ($A \in S_{\text{settled}}$). Its distance estimate cannot be legally reduced without breaking the algorithm's execution guarantees.
  * **If $A$ is ignored:** The algorithm outputs $d[A] = 3$, which is **incorrect** (True shortest path is $S \to B \to A$ with weight $1$).
  * **If $A$ is re-inserted into $Q$:** The algorithm degrades into the Bellman-Ford paradigm, and any negative weight cycle causes it to loop infinitely.

::: callout-warning Algorithmic Takeaway: Negative Edges
Dijkstra's algorithm **cannot** be used on graphs containing negative edge weights. 
Even adding a large constant $M$ to all edge weights to make them positive fails because paths with more edges are penalized disproportionately ($k \cdot M$). To handle negative weights safely, use the **Bellman-Ford Algorithm** ($O(V \cdot E)$).
:::

---

<a id="execution-trace"></a>
## 4. Step-by-Step 5W1H Stepped Execution Trace

We trace Dijkstra’s algorithm on a 5-vertex, 9-edge directed graph with non-negative weights, using vertex **$A$** as the source.

<a id="reference-graph"></a>
### Reference Directed Weighted Graph Specification:
* Vertices: $V = \{A, B, C, D, E\}$, with $|V| = 5$.
* Source: $s = A$.
* Directed Edge Set with Weights:
  $$E = \{ (A, B, 10), \; (A, C, 5), \; (B, C, 2), \; (B, D, 1), \; (C, B, 3), \; (C, D, 9), \; (C, E, 2), \; (D, E, 4), \; (E, D, 6) \}$$

```
                          REFERENCE GRAPH TOPOLOGY
                                   [10]
                           (A) -----------> (B)
                            |  \           ^ |
                            |   \ [2]    /   |
                        [5] |    v     / [3] | [1]
                            |    (C) -+      |
                            v   /   \        v
                           (E) <==== (D) <---+
                               [2]      [4]
```

---

<a id="trace-walkthrough"></a>
### Stepped Iteration Execution Walkthrough

#### Initialization (Iteration 0):
* `InitializeSingleSource(G, A)`:
  $$d[A] = 0, \quad d[B] = \infty, \quad d[C] = \infty, \quad d[D] = \infty, \quad d[E] = \infty$$
  $$\pi[A] = \text{NIL}, \quad \pi[B] = \text{NIL}, \quad \pi[C] = \text{NIL}, \quad \pi[D] = \text{NIL}, \quad \pi[E] = \text{NIL}$$
* $S = \emptyset$
* $Q = \{ (A, 0), (B, \infty), (C, \infty), (D, \infty), (E, \infty) \}$

---

#### Iteration 1: Processing Source Vertex $A$
* **What are we doing?** Extracting the minimum-distance vertex from $Q$ and relaxing its outgoing edges.
* **Why are we starting here?** $d[A] = 0$ is the smallest distance estimate in $Q$.
* **Where did this formula originate?** Base initialization of single-source shortest paths: $\delta(s, s) = 0$.
* **How do we execute the step mechanically?**
  $$\text{ExtractMin}(Q) \implies u = A. \quad S \leftarrow \{A\}$$
  $$\text{Examine outgoing edges from } A: \ Adj[A] = \{ (A, B, 10), (A, C, 5) \}$$
  $$\text{Edge } (A, B): d[B] > d[A] + w(A, B) \implies \infty > 0 + 10 \implies d[B] \leftarrow 10, \; \pi[B] \leftarrow A$$
  $$\text{Edge } (A, C): d[C] > d[A] + w(A, C) \implies \infty > 0 + 5 \implies d[C] \leftarrow 5, \; \pi[C] \leftarrow A$$
* **What changed from previous step?** $A$ entered $S$. $d[B]$ updated to $10$; $d[C]$ updated to $5$. 
  Queue: $Q = \{ (C, 5), (B, 10), (D, \infty), (E, \infty) \}$.

---

#### Iteration 2: Processing Vertex $C$
* **What are we doing?** Extracting the vertex with the minimum distance estimate from $Q$.
* **Why are we starting here?** In $Q = \{ (C, 5), (B, 10), (D, \infty), (E, \infty) \}$, vertex $C$ has the minimal key ($d[C] = 5$).
* **Where did this formula originate?** Greedy Choice: $u = \arg\min_{v \in Q} d[v]$.
* **How do we execute the step mechanically?**
  $$\text{ExtractMin}(Q) \implies u = C. \quad S \leftarrow \{A, C\}$$
  $$\text{Examine outgoing edges from } C: \ Adj[C] = \{ (C, B, 3), (C, D, 9), (C, E, 2) \}$$
  $$\text{Edge } (C, B): d[B] > d[C] + w(C, B) \implies 10 > 5 + 3 = 8 \implies \mathbf{d[B] \leftarrow 8, \; \pi[B] \leftarrow C \quad (\text{Decrease-Key!})}$$
  $$\text{Edge } (C, D): d[D] > d[C] + w(C, D) \implies \infty > 5 + 9 = 14 \implies d[D] \leftarrow 14, \; \pi[D] \leftarrow C$$
  $$\text{Edge } (C, E): d[E] > d[C] + w(C, E) \implies \infty > 5 + 2 = 7 \implies d[E] \leftarrow 7, \; \pi[E] \leftarrow C$$
* **What changed from previous step?** $C$ is finalized ($d[C] = \delta(A, C) = 5$). 
  $d[B]$ decreased from $10$ to $8$; $d[D]$ decreased from $\infty$ to $14$; $d[E]$ decreased from $\infty$ to $7$.
  Queue: $Q = \{ (E, 7), (B, 8), (D, 14) \}$.

---

#### Iteration 3: Processing Vertex $E$
* **What are we doing?** Extracting the minimum-key vertex from $Q = \{ (E, 7), (B, 8), (D, 14) \}$.
* **Why are we starting here?** Vertex $E$ has the minimal key ($d[E] = 7$).
* **Where did this formula originate?** Loop Invariant: $d[E]$ is guaranteed to equal $\delta(A, E)$.
* **How do we execute the step mechanically?**
  $$\text{ExtractMin}(Q) \implies u = E. \quad S \leftarrow \{A, C, E\}$$
  $$\text{Examine outgoing edges from } E: \ Adj[E] = \{ (E, D, 6) \}$$
  $$\text{Edge } (E, D): d[D] > d[E] + w(E, D) \implies 14 > 7 + 6 = 13 \implies \mathbf{d[D] \leftarrow 13, \; \pi[D] \leftarrow E \quad (\text{Decrease-Key!})}$$
* **What changed from previous step?** $E$ is finalized ($d[E] = 7$). $d[D]$ updated from $14$ down to $13$; $\pi[D]$ re-routed to $E$.
  Queue: $Q = \{ (B, 8), (D, 13) \}$.

---

#### Iteration 4: Processing Vertex $B$
* **What are we doing?** Extracting the minimum-key vertex from $Q = \{ (B, 8), (D, 13) \}$.
* **Why are we starting here?** Vertex $B$ has the smaller key ($d[B] = 8 < d[D] = 13$).
* **Where did this formula originate?** Greedy selection of minimal tentative path length.
* **How do we execute the step mechanically?**
  $$\text{ExtractMin}(Q) \implies u = B. \quad S \leftarrow \{A, C, E, B\}$$
  $$\text{Examine outgoing edges from } B: \ Adj[B] = \{ (B, C, 2), (B, D, 1) \}$$
  $$\text{Edge } (B, C): \text{Target } C \in S \implies d[C] = 5 \le d[B] + w(B, C) = 8 + 2 = 10 \implies \text{No update.}$$
  $$\text{Edge } (B, D): d[D] > d[B] + w(B, D) \implies 13 > 8 + 1 = 9 \implies \mathbf{d[D] \leftarrow 9, \; \pi[D] \leftarrow B \quad (\text{Decrease-Key!})}$$
* **What changed from previous step?** $B$ is finalized ($d[B] = 8$). $d[D]$ improved significantly from $13$ down to $9$; $\pi[D]$ updated to $B$.
  Queue: $Q = \{ (D, 9) \}$.

---

#### Iteration 5: Processing Vertex $D$
* **What are we doing?** Extracting the final vertex from $Q = \{ (D, 9) \}$.
* **Why are we starting here?** $D$ is the sole remaining element in $Q$.
* **How do we execute the step mechanically?**
  $$\text{ExtractMin}(Q) \implies u = D. \quad S \leftarrow \{A, C, E, B, D\} = V$$
  $$\text{Examine outgoing edges from } D: \ Adj[D] = \{ (D, E, 4) \}$$
  $$\text{Edge } (D, E): \text{Target } E \in S \implies d[E] = 7 \le d[D] + w(D, E) = 9 + 4 = 13 \implies \text{No update.}$$
  $$Q = \emptyset \implies \mathbf{\text{TERMINATE ALGORITHM}}$$
* **What changed from previous step?** All vertices are now finalized in $S$. The priority queue is exhausted.

---

<a id="state-matrix"></a>
### Consolidated State Transition Matrix

<div class="table-wrap">

| Step ($k$) | Vertex Extracted ($u$) | $d[A]$ | $d[B]$ | $d[C]$ | $d[D]$ | $d[E]$ | Priority Queue ($Q$) State After Relaxation | Action / Edges Relaxed |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | *Init* | **$0$** | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\{ (A,0), (B,\infty), (C,\infty), (D,\infty), (E,\infty) \}$ | `InitializeSingleSource` |
| **1** | $A$ | **$0^*$** | $10$ | $5$ | $\infty$ | $\infty$ | $\{ (C,5), (B,10), (D,\infty), (E,\infty) \}$ | Relax $(A, B) \to 10$, $(A, C) \to 5$ |
| **2** | $C$ | $0^*$ | **$8$** | **$5^*$** | $14$ | $7$ | $\{ (E,7), (B,8), (D,14) \}$ | Relax $(C, B) \to 8$, $(C, D) \to 14$, $(C, E) \to 7$ |
| **3** | $E$ | $0^*$ | $8$ | $5^*$ | **$13$** | **$7^*$** | $\{ (B,8), (D,13) \}$ | Relax $(E, D) \to 13$ |
| **4** | $B$ | $0^*$ | **$8^*$** | $5^*$ | **$9$** | $7^*$ | $\{ (D,9) \}$ | Relax $(B, D) \to 9$ |
| **5** | $D$ | $0^*$ | $8^*$ | $5^*$ | **$9^*$** | $7^*$ | $\emptyset$ | No updates; $Q$ exhausted |

</div>

*\* Denotes a distance value permanently finalized in the settled set $S$.*

#### Final Single-Source Shortest Path Results:
* **Distance Vector:**
  $$\mathbf{d = [ d[A]: 0, \; d[B]: 8, \; d[C]: 5, \; d[D]: 9, \; d[E]: 7 ]}$$
* **Predecessor Tree ($\pi$):**
  $$\pi[A] = \text{NIL}, \quad \pi[B] = C, \quad \pi[C] = A, \quad \pi[D] = B, \quad \pi[E] = C$$

#### Reconstructed Shortest Paths:
* $A \to A$: $\langle A \rangle$ (Cost: $0$)
* $A \to C$: $A \to C$ (Cost: $5$)
* $A \to B$: $A \to C \to B$ (Cost: $5 + 3 = 8$)
* $A \to E$: $A \to C \to E$ (Cost: $5 + 2 = 7$)
* $A \to D$: $A \to C \to B \to D$ (Cost: $5 + 3 + 1 = 9$)

---

<a id="complexity-analysis"></a>
## 5. Detailed Asymptotic Complexity Analysis Across Implementations

<a id="frequency-budget"></a>
### Operation Frequency Budget Breakdown

The runtime of Dijkstra's algorithm is parameterized by three primary operations on the priority queue $Q$:

```
                 DIJKSTRA'S INVOCATION FREQUENCY BUDGET
+-----------------------------------+------------------------+------------------------------------+
| Operation                         | Total Call Frequency   | Description                        |
+-----------------------------------+------------------------+------------------------------------+
| `BuildMinHeap` / `Insert`         | |V| times              | Insert all vertices into queue     |
| `ExtractMin`                      | |V| times              | Extract cheapest unvisited vertex  |
| `DecreaseKey` (Inside Relaxation) | At most |E| times      | Tighten upper bounds of neighbors  |
+-----------------------------------+------------------------+------------------------------------+
```

Total execution time as a generic functional recurrence:
$$T(V, E) = T_{\text{build}}(|V|) + |V| \cdot T_{\text{extract}}(|V|) + |E| \cdot T_{\text{decrease}}(|V|)$$

---

<a id="impl-array"></a>
### Implementation A: Unordered Array / Linear Search ($O(|V|^2)$)

In this implementation, the tentative distance estimates $d[1 \dots n]$ are held in a standard contiguous array. 
* A boolean array $\text{visited}[1 \dots n]$ tracks membership in $S$.

1. **`ExtractMin` Complexity:**
   Finding the vertex $u \notin S$ with the minimum $d[u]$ requires a linear scan over all $|V|$ elements in the array:
   $$T_{\text{extract}} = O(|V|)$$
   Executed $|V|$ times:
   $$\sum_{i=1}^{|V|} O(|V|) = O(|V|^2)$$

2. **`DecreaseKey` Complexity:**
   Relaxing an edge $(u, v)$ updates the entry $d[v]$ directly by indexing the array:
   $$T_{\text{decrease}} = O(1)$$
   Executed at most $|E|$ times:
   $$\sum_{i=1}^{|E|} O(1) = O(|E|)$$

3. **Total Asymptotic Time Complexity:**
   $$T(V, E) = O(|V|^2) + O(|E|) = \mathbf{O(|V|^2)}$$
   *(Since $|E| \le |V|^2$, the $|V|^2$ term strictly dominates).*

* **Use Case:** Optimal for **Dense Graphs** where $|E| = \Theta(|V|^2)$. It avoids the pointer-chasing and tree-rebalancing overhead of heap structures.

---

<a id="impl-binary-heap"></a>
### Implementation B: Binary Min-Heap ($O((|V| + |E|) \log |V|)$)

In this implementation, $Q$ is structured as a complete binary tree satisfying the min-heap property. 
* To support `DecreaseKey` in logarithmic time, an auxiliary index array maps each vertex ID to its current position in the heap array.

1. **`BuildMinHeap` Complexity:**
   Using Floyd’s bottom-up heap construction algorithm:
   $$T_{\text{build}} = O(|V|)$$

2. **`ExtractMin` Complexity:**
   Extracting the root element takes $O(1)$ time, followed by moving the last leaf to the root and calling `MinHeapify`, which sifts down the tree of height $\lfloor \log_2 |V| \rfloor$:
   $$T_{\text{extract}} = O(\log |V|)$$
   Executed $|V|$ times:
   $$|V| \times O(\log |V|) = O(|V| \log |V|)$$

3. **`DecreaseKey` Complexity:**
   Decreasing a key requires locating the vertex via the index map and bubbling it up toward the root to restore the heap property:
   $$T_{\text{decrease}} = O(\log |V|)$$
   Triggered at most $|E|$ times:
   $$|E| \times O(\log |V|) = O(|E| \log |V|)$$

4. **Total Asymptotic Time Complexity:**
   $$T(V, E) = O(|V|) + O(|V| \log |V|) + O(|E| \log |V|) = \mathbf{O((|V| + |E|) \log |V|)}$$
   For any connected graph where $|E| \ge |V| - 1$, this simplifies to:
   $$\mathbf{T(V, E) = O(|E| \log |V|)}$$

* **Use Case:** Highly efficient for **Sparse Graphs** where $|E| \ll |V|^2$ (e.g., planar graphs, road networks where $|E| = \Theta(|V|)$).

---

<a id="impl-fib-heap"></a>
### Implementation C: Fibonacci Heap ($O(|E| + |V| \log |V|)$)

A Fibonacci Heap is a collection of min-heap-ordered trees that provides superior **amortized** time bounds for priority queue operations.

1. **`ExtractMin` Complexity:**
   Extracting the minimum root node and consolidating the remaining tree roots has an amortized cost of:
   $$T_{\text{extract}} = O(\log |V|) \quad (\text{amortized})$$
   Executed $|V|$ times:
   $$|V| \times O(\log |V|) = O(|V| \log |V|)$$

2. **`DecreaseKey` Complexity:**
   Decreasing a key cuts the node from its parent, turning it into a new root in the root list, and performs cascading cuts if necessary. The amortized cost is:
   $$T_{\text{decrease}} = O(1) \quad (\text{amortized})$$
   Executed at most $|E|$ times:
   $$|E| \times O(1) = O(|E|)$$

3. **Total Asymptotic Time Complexity:**
   $$\mathbf{T(V, E) = O(|E| + |V| \log |V|)}$$

* **Theoretical Significance:** 
  For dense graphs where $|E| = \Theta(|V|^2)$, the runtime evaluates to $O(|V|^2)$. For sparse graphs where $|E| = \Theta(|V|)$, it evaluates to $O(|V| \log |V|)$. 
  *Note:* While asymptotically optimal, the constant factors hidden within Fibonacci heaps are substantial, making binary heaps faster in many practical software implementations.

---

<a id="comparative-matrix"></a>
### Comparative Implementation Trade-Off Matrix

<div class="table-wrap">

| Dimension | Unordered Array | Binary Min-Heap | Fibonacci Heap |
| :--- | :--- | :--- | :--- |
| **`ExtractMin` Time** | $O(|V|)$ | $O(\log |V|)$ | $O(\log |V|)$ (amortized) |
| **`DecreaseKey` Time**| $O(1)$ | $O(\log |V|)$ | $O(1)$ (amortized) |
| **Total Runtime (General)** | $O(|V|^2 + |E|)$ | $O((|V| + |E|) \log |V|)$ | $O(|E| + |V| \log |V|)$ |
| **Sparse Graph ($|E| \approx |V|$)** | $O(|V|^2)$ (Slow) | $\mathbf{O(|V| \log |V|)}$ (Fast) | $\mathbf{O(|V| \log |V|)}$ (Fast) |
| **Dense Graph ($|E| \approx |V|^2$)** | $\mathbf{O(|V|^2)}$ (Optimal) | $O(|V|^2 \log |V|)$ (Suboptimal) | $\mathbf{O(|V|^2)}$ (Optimal) |
| **Implementation Complexity** | Trivial ($\approx 10$ lines) | Moderate (array-based heap) | Very High (complex tree-pointer manipulation) |
| **Constant Factor Overhead** | Extremely Low | Low / Cache-Friendly | High |

</div>

---

<a id="exam-summary"></a>
## 6. KTU Exam High-Yield Summary

<a id="three-mark-questions"></a>
### Frequently Asked 3-Mark Questions & Model Answers

#### Q1: Define the relaxation step in shortest path algorithms.
**Model Answer:**
Relaxing an edge $(u, v)$ with weight $w(u, v)$ tests whether the shortest path to $v$ can be improved by passing through $u$. If the current estimate satisfies $d[v] > d[u] + w(u, v)$, the algorithm updates $d[v] \leftarrow d[u] + w(u, v)$ and sets the predecessor pointer $\pi[v] \leftarrow u$.

---

#### Q2: State the Triangle Inequality property of shortest path distances.
**Model Answer:**
For any directed, weighted graph $G = (V, E, w)$ with source $s$, and for any edge $(u, v) \in E$, the shortest path distance satisfies:
$$\delta(s, v) \le \delta(s, u) + w(u, v)$$
This states that the shortest path from $s$ to $v$ cannot exceed the cost of traveling via the shortest path to $u$ followed by the direct edge $(u, v)$.

---

#### Q3: Why does Dijkstra’s algorithm fail when directed edges have negative weights?
**Model Answer:**
Dijkstra's algorithm is greedy; it permanently finalizes a vertex $u$ when it is extracted from the unvisited set ($d[u] = \delta(s, u)$), assuming subsequent paths can only increase in cost. If negative edges exist, a path extended through another vertex could yield a smaller overall cost, but Dijkstra will not re-evaluate already finalized nodes, leading to incorrect results.

---

#### Q4: What is the optimal substructure property of shortest paths?
**Model Answer:**
Any subpath of a shortest path is itself a shortest path. Formally, if path $p$ from $v_0$ to $v_k$ is a shortest path, then for any intermediate vertices $v_i, v_j$ on $p$, the subpath $p_{ij}$ is a shortest path between $v_i$ and $v_j$.

---

<a id="marking-traps"></a>
### High-Frequency Student Pitfalls & Marking Traps

::: callout-exam Exam Traps & Avoidance Strategies
1. **The Negative Weight Constant Fallacy:**
   * *The Error:* Proposing to eliminate negative weights by finding the minimum negative weight $-W_{\min}$, adding $|W_{\min}|$ to all edges, and then running Dijkstra.
   * *The Fix:* State clearly on exams why this fails: paths with different numbers of edges have different total adjustments added to them. A path with 5 edges receives $+5|W_{\min}|$, while an alternative path with 2 edges receives only $+2|W_{\min}|$, fundamentally altering which path is shortest.

2. **The Prim vs. Dijkstra Relaxation Distinction:**
   * *The Error:* Writing Dijkstra's relaxation condition as `d[v] > w(u, v)`.
   * *The Fix:*
     * Prim's Algorithm (MST): $\text{key}[v] > w(u, v)$ (Only considers local edge weight).
     * Dijkstra's Algorithm (SSSP): $d[v] > \mathbf{d[u]} + w(u, v)$ (Considers cumulative path weight from source).

3. **Omitting the Non-Negative Assumption in Proofs:**
   * *The Error:* Forgetting to explicitly cite $w(e) \ge 0$ during the loop invariant contradiction proof.
   * *The Fix:* The step $\delta(s, y) \le \delta(s, u)$ holds *if and only if* edge weights are non-negative. Always write: *"Since all edge weights are non-negative ($w(e) \ge 0$), subpaths cannot have negative sums; therefore, $\delta(s, y) \le \delta(s, u)$."*

4. **Heap Implementation Complexity Notation:**
   * *The Error:* Stating that binary heap Dijkstra runs in $O(E \log E)$ and failing to convert it to $O(E \log V)$.
   * *The Fix:* Show the algebraic equivalence: $E \le V^2 \implies \log E \le \log(V^2) = 2 \log V \implies O(E \log E) = O(E \log V)$.
:::
