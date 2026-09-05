# Module 3.2: Minimum Cost Spanning Trees — Theoretical Foundations, Kruskal's, and Prim's Algorithms
**Course Code: PCCST502 | Design and Analysis of Algorithms | KTU 2024 Scheme**

---

### Table of Contents
1. [Spanning Tree Foundations & Core Theorems](#spanning-tree-foundations)
   - [Formal Graph Theoretic Definitions](#formal-definitions)
   - [Fundamental Properties of Spanning Trees](#spanning-tree-properties)
   - [The Cut Property: Theorem & Formal Exchange Proof](#cut-property)
   - [The Cycle Property: Theorem & Formal Contradiction Proof](#cycle-property)
2. [Kruskal's Algorithm (Edge-Centric Greedy Strategy)](#kruskals-algorithm)
   - [Algorithmic Intuition: Forest Coalescence](#kruskal-intuition)
   - [Cycle Detection Mechanics via Disjoint Set Union (DSU)](#dsu-mechanics)
   - [Complete Pseudocode with Union-by-Rank & Path Compression](#kruskal-pseudocode)
   - [Asymptotic Time and Space Complexity Derivations](#kruskal-complexity)
   - [Step-by-Step 5W1H Stepped Execution Trace](#kruskal-trace)
3. [Prim's Algorithm (Vertex-Centric Greedy Strategy)](#prims-algorithm)
   - [Algorithmic Intuition & Dynamic Cut Interpretation](#prim-intuition)
   - [Priority Queue Mechanics: Keys, Parents, and Decrease-Key](#prim-priority-queue)
   - [Complete Algorithm Pseudocode](#prim-pseudocode)
   - [Detailed Complexity Analysis Across Three Implementations](#prim-complexity)
   - [Step-by-Step 5W1H Stepped Execution Trace](#prim-trace)
4. [Comparative Architectural Analysis: Kruskal vs. Prim](#comparative-analysis)
   - [Side-by-Side Structural Comparison Matrix](#comparison-matrix)
   - [Graph Topology and Data Structure Selection Guide](#selection-guide)
5. [KTU Exam High-Yield Summary](#exam-summary)
   - [Frequently Asked 3-Mark Questions & Model Answers](#three-mark-questions)
   - [High-Frequency Student Pitfalls & Marking Scheme Traps](#marking-traps)

---

<a id="spanning-tree-foundations"></a>
## 1. Spanning Tree Foundations & Core Theorems

<a id="formal-definitions"></a>
### Formal Graph Theoretic Definitions

Let $G = (V, E)$ be an undirected, connected, weighted graph where:
* $V$ is the finite set of vertices, with $|V| = n$.
* $E$ is the finite set of unordered pairs of distinct vertices called edges, with $|E| = m$.
* $w: E \to \mathbb{R}$ is a weight function that assigns an arbitrary real-valued cost $w(e)$ to each edge $e = (u, v) \in E$.

```
                        GENERAL GRAPH vs. SPANNING TREE
         Given Graph G = (V, E)                   Spanning Tree T = (V, E_T)
             |V| = 5, |E| = 7                          |V| = 5, |E_T| = 4
             
               (1)---[4]---(2)                           (1)---[4]---(2)
              /   \       /   \                         /           /
            [2]   [1]   [3]   [5]                     [2]         [3]
            /       \   /       \                     /           /
          (3)---[6]---(4)---[7]---(5)               (3)         (4)---[7]---(5)
          
          Contains cycles:                        Acyclic, connected, spans all
          (1)-(2)-(4)-(1), etc.                   5 vertices with exactly 4 edges.
```

#### Definition 1: Spanning Tree
A **Spanning Tree** $T = (V, E_T)$ of an undirected, connected graph $G = (V, E)$ is an acyclic subgraph containing **every** vertex of $G$ such that $E_T \subseteq E$ and $T$ is connected.

#### Definition 2: Minimum Cost Spanning Tree (MST)
For a weighted graph $G = (V, E, w)$, the cost of a spanning tree $T = (V, E_T)$ is the sum of the weights of the edges comprising $T$:
$$w(T) = \sum_{e \in E_T} w(e)$$

A **Minimum Cost Spanning Tree** (MST) is a spanning tree $T^*$ whose total cost is minimal among the set $\mathcal{T}(G)$ of all possible spanning trees of $G$:
$$w(T^*) = \min_{T \in \mathcal{T}(G)} w(T)$$

---

<a id="spanning-tree-properties"></a>
### Fundamental Properties of Spanning Trees

For any connected, undirected graph $G = (V, E)$ with $|V| = n$:

1. **Cardinals Invariant:** Every spanning tree $T$ of $G$ contains **exactly** $|V| - 1 = n - 1$ edges.
2. **Minimally Connected:** Removing any edge $e \in E_T$ disconnects $T$ into exactly two separate connected components.
3. **Maximally Acyclic:** Adding any edge $e \in E \setminus E_T$ to $T$ creates **exactly one** unique simple cycle.
4. **Unique Path Property:** For any two vertices $u, v \in V$, there exists one and only one simple path between $u$ and $v$ in $T$.

::: callout-intuition Why "Spanning" and Why "Tree"?
* **Spanning:** The subgraph must cover (span) the entire population of vertices $V$. No vertex is left behind or isolated.
* **Tree:** The configuration must maintain global connectivity with zero redundant wiring. Any cycle introduces redundancy, which can be broken by removing an edge, reducing the total cost without disconnecting the network.
:::

---

<a id="cut-property"></a>
### The Cut Property: Theorem & Formal Exchange Proof

The greedy strategy for finding an MST relies on two dual properties: the **Cut Property** (which justifies adding safe edges) and the **Cycle Property** (which justifies discarding dangerous edges).

#### Definition 3: Cut and Crossing Edges
* A **cut** $(S, V \setminus S)$ of an undirected graph $G = (V, E)$ is a partition of the vertex set $V$ into two disjoint, non-empty subsets $S$ and $V \setminus S$.
* An edge $e = (u, v) \in E$ **crosses** the cut $(S, V \setminus S)$ if one endpoint lies in $S$ and the other lies in $V \setminus S$ (i.e., $u \in S$ and $v \in V \setminus S$, or vice versa).
* A cut **respects** a set of edges $A \subseteq E$ if no edge in $A$ crosses the cut.
* An edge $e$ is a **light edge** crossing a cut if its weight is the minimum among all edges crossing that specific cut.

```
                         THE CUT PROPERTY TOPOLOGY
               Partition S                      Partition V \ S
          +-----------------------+        +-----------------------+
          |         ( u )         |        |         ( v )         |
          |        /     \        |        |        /     \        |
          |      (a)-----(b)      |        |      (c)-----(d)      |
          +-----------|-----------+        +-----------|-----------+
                      |                                |
                      +====[ e = (u,v) (LIGHTEST) ]====+  w(e) = 2
                      |                                |
                      +-----[ e' = (b,c) (OTHER) ]-----+  w(e') = 6
                      
           Cut (S, V \ S) divides the graph. Edge e is the light edge.
           Any spanning tree lacking e can be improved or matched by
           exchanging e' for e.
```

#### Theorem 1 (The Cut Property):
Let $G = (V, E)$ be a connected, undirected, weighted graph. Let $(S, V \setminus S)$ be any valid cut of $G$. If $e = (u, v)$ is a light edge crossing $(S, V \setminus S)$, then this edge belongs to some Minimum Spanning Tree of $G$. Furthermore, if $e$ is the *strictly* unique light edge crossing $(S, V \setminus S)$, then $e$ belongs to **every** Minimum Spanning Tree of $G$.

#### Mathematical Proof (Cut-and-Paste / Exchange Argument):
1. **Initial Assumption:** Let $T = (V, E_T)$ be an arbitrary Minimum Spanning Tree of $G$. 
2. **Case A (Trivial Inclusion):** If $e \in E_T$, then the light edge $e$ is already part of this MST, and the theorem holds immediately.
3. **Case B (Non-Inclusion):** Suppose $e = (u, v) \notin E_T$. We must prove that we can construct an alternative spanning tree $T'$ containing $e$ such that $w(T') \le w(T)$.
4. **Cycle Formation:** Because $T$ is a spanning tree, it already contains a unique simple path $P$ connecting vertex $u$ to vertex $v$. Since $u \in S$ and $v \in V \setminus S$, the path $P$ starts in partition $S$ and ends in partition $V \setminus S$. Therefore, $P$ must cross the cut boundary $(S, V \setminus S)$ at least once. Let $e' = (x, y)$ be an edge on path $P$ that crosses the cut $(S, V \setminus S)$, where $x \in S$ and $y \in V \setminus S$. Note that $e' \ne e$ because $e \notin E_T$.
5. **The Exchange Step:** Adding the edge $e = (u, v)$ to $T$ produces a graph $T \cup \{e\}$ that contains exactly one simple cycle $C$, consisting of the edge $e$ together with the path $P$. Because $e'$ lies on path $P$, $e'$ is part of this cycle $C$.
   We construct a new subgraph $T'$ by removing $e'$ and adding $e$:
   $$T' = (T \setminus \{e'\}) \cup \{e\}$$
6. **Verification of Tree Topology for $T'$:**
   * **Acyclicity:** Removing $e'$ breaks the cycle $C$. Since $e'$ was the only edge removed from the single cycle formed by adding $e$, $T'$ contains no cycles.
   * **Connectivity:** Removing $e'$ splits $T$ into two disconnected trees: $T_S$ containing $x$, and $T_{V \setminus S}$ containing $y$. Because $e = (u, v)$ also has endpoints $u \in S$ and $v \in V \setminus S$, adding $e$ provides a path between $T_S$ and $T_{V \setminus S}$, restoring global connectivity.
   * **Edge Count:** $|E_{T'}| = |E_T| - 1 + 1 = |V| - 1$.
   Therefore, $T'$ is a valid spanning tree of $G$.
7. **Cost Comparison:**
   The total weight of $T'$ is:
   $$w(T') = w(T) - w(e') + w(e)$$
   By definition, $e$ is a light edge crossing the cut $(S, V \setminus S)$, and $e'$ is an edge crossing the same cut. Hence:
   $$w(e) \le w(e') \implies w(e) - w(e') \le 0$$
   Substituting this inequality into the cost equation:
   $$w(T') = w(T) + \underbrace{(w(e) - w(e'))}_{\le 0} \le w(T)$$
8. **Optimality Conclusion:**
   Since $T$ was defined as a Minimum Spanning Tree, its weight $w(T)$ is minimal; no spanning tree can have a weight strictly less than $w(T)$. Therefore, $w(T') \ge w(T)$.
   Coupled with $w(T') \le w(T)$, we obtain:
   $$w(T') = w(T)$$
   Thus, $T'$ is also a Minimum Spanning Tree of $G$, and $e \in T'$. $\blacksquare$

---

<a id="cycle-property"></a>
### The Cycle Property: Theorem & Formal Contradiction Proof

#### Theorem 2 (The Cycle Property):
Let $G = (V, E)$ be a connected, undirected, weighted graph, and let $C \subseteq E$ be any simple cycle in $G$. If $e \in C$ is an edge whose weight is **strictly greater** than the weight of every other edge in $C$, then $e$ cannot belong to any Minimum Spanning Tree of $G$.

```
                        THE CYCLE PROPERTY TOPOLOGY
                              (u)---------[ e ]---------(v)   w(e) = 9 (MAX!)
                             /                             \
                          [ 2 ]                           [ 3 ]
                           /                                 \
                         (a)-------------[ 4 ]---------------(b)
                         
             Cycle C: (u)-(v)-(b)-(a)-(u)
             Edge e = (u, v) is strictly the heaviest edge in cycle C.
             If an alleged MST includes e, deleting e and replacing it
             with any other edge on the alternative cycle path reduces
             total weight, contradicting optimality.
```

#### Mathematical Proof (Proof by Contradiction):
1. **Hypothesis for Contradiction:** Assume that $e = (u, v) \in C$ is strictly the heaviest edge in simple cycle $C$, yet $e$ belongs to an MST $T = (V, E_T)$ of $G$ (i.e., $e \in E_T$).
2. **Disconnection via Deletion:** Delete edge $e$ from $T$. Because $T$ is a tree, removing an edge partitions the vertex set into two disjoint connected components, $V_1$ and $V_2$, such that $u \in V_1$ and $v \in V_2$. This establishes a valid cut $(V_1, V_2)$ of $G$.
3. **Alternate Path Existence:** Because $C$ is a simple cycle containing $e = (u, v)$, the set of edges $C \setminus \{e\}$ forms an alternate simple path connecting $u$ and $v$. 
4. **Crossing Edge Identification:** Since $u \in V_1$ and $v \in V_2$, the path $C \setminus \{e\}$ starts in $V_1$ and terminates in $V_2$. By the intermediate value property of cuts, there must exist at least one edge $e' = (x, y) \in C \setminus \{e\}$ such that $x \in V_1$ and $y \in V_2$. That is, $e'$ crosses the cut $(V_1, V_2)$.
5. **Synthesis of Modified Tree $T'$:** Add edge $e'$ to $T \setminus \{e\}$:
   $$T' = (T \setminus \{e\}) \cup \{e'\}$$
   Because $e'$ bridges the two disconnected components $V_1$ and $V_2$, $T'$ is connected, acyclic, spans all $V$, and contains $|V| - 1$ edges. Thus, $T'$ is a valid spanning tree.
6. **Strict Weight Reduction:** By the theorem's premise, $e$ is strictly the heaviest edge in cycle $C$. Because $e' \in C \setminus \{e\}$, we have:
   $$w(e') < w(e) \implies w(e') - w(e) < 0$$
   Now evaluate the weight of $T'$:
   $$w(T') = w(T) - w(e) + w(e') = w(T) + (w(e') - w(e)) < w(T)$$
   $$w(T') < w(T)$$
7. **Contradiction:** The existence of spanning tree $T'$ with $w(T') < w(T)$ contradicts the initial premise that $T$ was a *Minimum* Spanning Tree.
   Therefore, the assumption that $e \in T$ must be false. Edge $e$ cannot belong to any MST of $G$. $\blacksquare$

---

<a id="kruskals-algorithm"></a>
## 2. Kruskal's Algorithm (Edge-Centric Greedy Strategy)

<a id="kruskal-intuition"></a>
### Algorithmic Intuition: Forest Coalescence

Kruskal's algorithm operates on an **edge-centric** greedy philosophy. Rather than expanding a single tree outward from a source vertex, Kruskal's algorithm treats every vertex as an isolated tree in a growing **spanning forest**.

```
                   KRUSKAL'S FOREST COALESCENCE MODEL
 Stage 0: Initial Forest (n disconnected components)
   (A)      (B)      (C)      (D)      (E)      (F)

 Stage 1: Add Lightest Edges (Safe components merge)
   (A)------(C)      (B)      (D)------(E)      (F)

 Stage 2: Intermediate Mergers (Larger components form)
   (A)------(C)------(B)      (D)------(E)------(F)
   
 Stage 3: Final Unification (|E_T| = n - 1, Single MST attained)
   (A)------(C)------(B)======(D)------(E)------(F)
                           ^
                           |-- Critical Bridge Edge Merges Forest
```

1. Sort all $m$ edges of $G$ in non-decreasing order of their weights: $w(e_1) \le w(e_2) \le \dots \le w(e_m)$.
2. Iterate through the sorted edges sequentially. For each candidate edge $e = (u, v)$:
   * Check whether $u$ and $v$ belong to the same tree component.
   * **If different components:** Adding $e$ cannot introduce a cycle. Accept $e$ into the MST and merge the two components into one.
   * **If same component:** A path already exists between $u$ and $v$. Adding $e$ would create a cycle. Reject $e$.
3. Terminate as soon as $|V| - 1$ edges have been committed, or when the candidate edge list is exhausted.

---

<a id="dsu-mechanics"></a>
### Cycle Detection Mechanics via Disjoint Set Union (DSU)

Checking for cycles using standard Depth-First Search (DFS) or Breadth-First Search (BFS) takes $O(V)$ time per candidate edge, yielding an impractical $O(E \cdot V)$ total runtime. 

To achieve optimal efficiency, Kruskal's algorithm uses the **Disjoint Set Union (DSU)** data structure (also known as Union-Find) equipped with two heuristics: **Union by Rank** and **Path Compression**.

```
                PATH COMPRESSION & UNION-BY-RANK DYNAMICS
  
  Path Compression: Flattens tree on Find(x)
  Before Find(4):                      After Find(4):
        (1) [Root]                           (1) [Root]
         |                                 /  |  \
        (2)                              (2) (3) (4)
         |                             (All point directly to root!)
        (3)
         |
        (4)
  ------------------------------------------------------------------------
  Union-by-Rank: Attaches shallower tree under deeper tree root
        Root r1 (Rank 2)         Root r2 (Rank 1)      Merged Tree (Root r1)
             (A)                      (D)                     (A) [Rank 2]
            /   \                      |                     / | \
          (B)   (C)                   (E)                  (B)(C) (D)
                                                                   |
                                                                  (E)
```

#### DSU Core Primitives:
1. **`MakeSet(x)`:** Creates a new set containing the single element $x$. The parent pointer points to itself (`parent[x] = x`), and the tree height metric is initialized to zero (`rank[x] = 0`).
2. **`Find(x)` (with Path Compression):** Traverses the parent pointers from $x$ upward until locating the unique representative root of the set. During the recursive unspooling, it resets the parent pointer of every visited node directly to that root.
3. **`Union(x, y)` (with Union by Rank):** Finds the representative roots $r_x = \text{Find}(x)$ and $r_y = \text{Find}(y)$. If $r_x \ne r_y$, it attaches the root with the smaller rank as a child of the root with the larger rank. If both roots have identical ranks, one is chosen arbitrarily as the parent and its rank is incremented by 1.

#### Why `Find(u) == Find(v)` Accurately Detects Cycles:
* In the DSU model, each disjoint set corresponds to a connected component in the spanning forest.
* The query $\text{Find}(u)$ returns the unique identifier (root) of the component containing $u$.
* If $\text{Find}(u) = \text{Find}(v)$, then $u$ and $v$ reside within the same connected component, meaning a path already connects them using previously accepted MST edges.
* By Property 3 of Spanning Trees, adding an edge between two vertices already connected in an acyclic graph introduces **exactly one cycle**.
* Therefore, the condition $\text{Find}(u) == \text{Find}(v)$ is a necessary and sufficient test for cycle generation.

---

<a id="kruskal-pseudocode"></a>
### Complete Pseudocode with Union-by-Rank & Path Compression

```text
Algorithm MakeSet(v)
begin
    parent[v] ← v;
    rank[v] ← 0;
end;

Algorithm Find(v)
// Path Compression: Flattens the traversal tree recursively
begin
    if v ≠ parent[v] then
        parent[v] ← Find(parent[v]);
    return parent[v];
end;

Algorithm Union(u, v)
// Union-by-Rank: Prevents tree degeneration by attaching based on rank
begin
    rootU ← Find(u);
    rootV ← Find(v);
    
    if rootU ≠ rootV then
    begin
        if rank[rootU] < rank[rootV] then
            parent[rootU] ← rootV;
        else if rank[rootU] > rank[rootV] then
            parent[rootV] ← rootU;
        else
        begin
            parent[rootV] ← rootU;
            rank[rootU] ← rank[rootU] + 1;
        end;
    end;
end;

Algorithm KruskalMST(G = (V, E, w))
// Input: Connected, undirected, weighted graph G
// Output: Set of edges E_T forming a Minimum Cost Spanning Tree
begin
    E_T ← ∅;                         // Initialize MST edge set to empty
    
    // Phase 1: Initialize disjoint sets for every vertex: O(V)
    for each vertex v ∈ V do
        MakeSet(v);
        
    // Phase 2: Sort edges into non-decreasing order by weight: O(E log E)
    Sort edges E in non-decreasing order such that w(e_1) ≤ w(e_2) ≤ ... ≤ w(e_m);
    
    // Phase 3: Greedy Edge Selection Loop
    for each edge e = (u, v) ∈ E in sorted order do
    begin
        rootU ← Find(u);             // Identify component of vertex u
        rootV ← Find(v);             // Identify component of vertex v
        
        if rootU ≠ rootV then         // If endpoints belong to different components:
        begin
            E_T ← E_T ∪ {e};          // Commit edge e to the MST
            Union(rootU, rootV);     // Merge the two components
            
            if |E_T| = |V| - 1 then   // Early termination check
                break;
        end;
    end;
    
    return E_T;
end;
```

---

<a id="kruskal-complexity"></a>
### Asymptotic Time and Space Complexity Derivations

#### 1. Time Complexity Breakdown:
* **DSU Initialization:** Invoking `MakeSet(v)` across $|V|$ vertices takes:
  $$T_{\text{init}}(V) = \Theta(|V|)$$
* **Edge Sorting:** Sorting $|E|$ edges using an optimal comparison sort (Merge Sort or Heap Sort):
  $$T_{\text{sort}}(E) = \Theta(|E| \log |E|)$$
  Because the graph is simple, $|E| \le |V|^2$. Applying logarithm rules:
  $$\log |E| \le \log(|V|^2) = 2 \log |V| \implies \log |E| = \Theta(\log |V|)$$
  Therefore:
  $$T_{\text{sort}}(E) = \Theta(|E| \log |V|)$$
* **DSU Operations in the Greedy Loop:**
  The algorithm performs at most $2|E|$ `Find` operations and at most $|V| - 1$ `Union` operations. With both **Path Compression** and **Union-by-Rank** enabled, any sequence of $m$ operations on $n$ elements executes in:
  $$T_{\text{DSU}}(V, E) = O(|E| \cdot \alpha(|V|))$$
  where $\alpha$ is the **Inverse Ackermann function**. The function $\alpha(n)$ grows so slowly that for any practical input size ($n \le 10^{80}$, the estimated number of atoms in the observable universe), $\alpha(n) \le 4$. Thus, $\alpha(|V|)$ is treated as an effective constant:
  $$T_{\text{DSU}}(V, E) = O(|E|)$$
* **Total Worst-Case Time Complexity:**
  $$T(V, E) = T_{\text{init}}(V) + T_{\text{sort}}(E) + T_{\text{DSU}}(V, E) = O(|V|) + O(|E| \log |V|) + O(|E| \cdot \alpha(|V|))$$
  $$\mathbf{T(V, E) = O(|E| \log |V|) \quad \text{or} \quad O(|E| \log |E|)}$$

#### 2. Space Complexity Breakdown:
* **DSU Arrays:** Storing the `parent[1..n]` and `rank[1..n]` arrays requires $2|V| \times \text{sizeof(int)} = \Theta(|V|)$ space.
* **Edge List Storage:** Storing the sorted list of edges requires $\Theta(|E|)$ space.
* **Output Set ($E_T$):** Stores $|V| - 1$ edges, taking $\Theta(|V|)$ space.
* **Total Auxiliary Space Complexity:** $\mathbf{\Theta(|V| + |E|)}$ (or $\mathbf{\Theta(|V|)}$ if edge sorting is done in-place on existing structures).

---

<a id="kruskal-trace"></a>
### Step-by-Step 5W1H Stepped Execution Trace

We trace Kruskal's algorithm on the following 6-vertex, 9-edge connected graph.

#### Reference Graph Specification:
* Vertices: $V = \{A, B, C, D, E, F\}$, so $|V| = 6$. Target MST edge count $= |V| - 1 = 5$.
* Edges:
  $$E = \{ (A, B, 4), (A, C, 2), (B, C, 1), (B, D, 5), (C, D, 8), (C, E, 10), (D, E, 2), (D, F, 6), (E, F, 3) \}$$

```
                          REFERENCE GRAPH TOPOLOGY
                                   [4]
                            (A)-----------(B)
                             |  \       /  |
                            [2]   \   /   [5]
                             |     [1]     |
                             |    /   \    |
                            (C)           (D)
                             |  \       /  |
                           [10]   \   /   [6]
                             |     [2]     |
                             |    /   \    |
                            (E)-----------(F)
                                   [3]
```

---

#### Phase 1: Edge Sorting and Prioritization

<div class="table-wrap">

| Rank ($k$) | Edge ($u, v$) | Weight ($w$) | Status Prior to Inspection |
| :---: | :---: | :---: | :---: |
| **1** | $(B, C)$ | $1$ | Pending Evaluation |
| **2** | $(A, C)$ | $2$ | Pending Evaluation |
| **3** | $(D, E)$ | $2$ | Pending Evaluation |
| **4** | $(E, F)$ | $3$ | Pending Evaluation |
| **5** | $(A, B)$ | $4$ | Pending Evaluation |
| **6** | $(B, D)$ | $5$ | Pending Evaluation |
| **7** | $(D, F)$ | $6$ | Pending Evaluation |
| **8** | $(C, D)$ | $8$ | Pending Evaluation |
| **9** | $(C, E)$ | $10$ | Pending Evaluation |

</div>

---

#### Phase 2: DSU Initialization
* `parent` map: $\{A: A, B: B, C: C, D: D, E: E, F: F\}$
* `rank` map: $\{A: 0, B: 0, C: 0, D: 0, E: 0, F: 0\}$
* $E_T = \emptyset$, $|E_T| = 0$.

---

#### Phase 3: The 5W1H Stepped Execution Trace

##### Iteration 1: Edge $(B, C)$, Weight $= 1$
* **What are we doing?** Evaluating the globally lightest available edge $(B, C)$ for inclusion in $E_T$.
* **Why are we starting here?** Edge $(B, C)$ has the absolute minimum weight ($w=1$) in the sorted list.
* **Where did this formula originate?** The condition `Find(B) != Find(C)`.
* **How do we execute the step mechanically?**
  $$\text{Find}(B) = B, \quad \text{Find}(C) = C$$
  $$\text{Since } B \ne C \implies \text{No cycle detected. Accept edge.}$$
  $$E_T \leftarrow E_T \cup \{(B, C)\}$$
  $$\text{Union}(B, C): \text{rank}[B] = \text{rank}[C] = 0 \implies \text{Set } parent[C] \leftarrow B, \; \text{rank}[B] \leftarrow 1$$
* **What changed from previous step?** Edge $(B, C)$ added to $E_T$ ($|E_T| = 1$). Vertices $B$ and $C$ now share root $B$.

---

##### Iteration 2: Edge $(A, C)$, Weight $= 2$
* **What are we doing?** Evaluating candidate edge $(A, C)$ with weight $2$.
* **Why are we starting here?** $(A, C)$ is the next edge in sorted priority order.
* **Where did this formula originate?** Cycle check via `Find(A)` and `Find(C)`.
* **How do we execute the step mechanically?**
  $$\text{Find}(A) = A$$
  $$\text{Find}(C) \implies parent[C] = B \implies parent[B] = B \implies \text{Root is } B$$
  $$\text{Since } A \ne B \implies \text{Endpoints are in different components. Accept edge.}$$
  $$E_T \leftarrow E_T \cup \{(A, C)\}$$
  $$\text{Union}(A, B): \text{rank}[A] = 0, \; \text{rank}[B] = 1 \implies \text{rank}[A] < \text{rank}[B] \implies parent[A] \leftarrow B$$
* **What changed from previous step?** Edge $(A, C)$ committed ($|E_T| = 2$). Component $\{A, B, C\}$ is now unified under root $B$.

---

##### Iteration 3: Edge $(D, E)$, Weight $= 2$
* **What are we doing?** Evaluating candidate edge $(D, E)$ with weight $2$.
* **Why are we starting here?** Next edge in sorted order ($w=2$).
* **Where did this formula originate?** Cycle check via `Find(D)` and `Find(E)`.
* **How do we execute the step mechanically?**
  $$\text{Find}(D) = D, \quad \text{Find}(E) = E$$
  $$\text{Since } D \ne E \implies \text{Endpoints are in different components. Accept edge.}$$
  $$E_T \leftarrow E_T \cup \{(D, E)\}$$
  $$\text{Union}(D, E): \text{rank}[D] = \text{rank}[E] = 0 \implies parent[E] \leftarrow D, \; \text{rank}[D] \leftarrow 1$$
* **What changed from previous step?** Edge $(D, E)$ committed ($|E_T| = 3$). Vertices $D$ and $E$ form a new component under root $D$.

---

##### Iteration 4: Edge $(E, F)$, Weight $= 3$
* **What are we doing?** Evaluating candidate edge $(E, F)$ with weight $3$.
* **Why are we starting here?** Next edge in sorted order ($w=3$).
* **Where did this formula originate?** Cycle check via `Find(E)` and `Find(F)`.
* **How do we execute the step mechanically?**
  $$\text{Find}(E) \implies parent[E] = D \implies \text{Root is } D$$
  $$\text{Find}(F) = F$$
  $$\text{Since } D \ne F \implies \text{Different components. Accept edge.}$$
  $$E_T \leftarrow E_T \cup \{(E, F)\}$$
  $$\text{Union}(D, F): \text{rank}[D] = 1, \; \text{rank}[F] = 0 \implies \text{rank}[F] < \text{rank}[D] \implies parent[F] \leftarrow D$$
* **What changed from previous step?** Edge $(E, F)$ committed ($|E_T| = 4$). Component $\{D, E, F\}$ is now unified under root $D$.

---

##### Iteration 5: Edge $(A, B)$, Weight $= 4$ (Cycle Rejection)
* **What are we doing?** Evaluating candidate edge $(A, B)$ with weight $4$.
* **Why are we starting here?** Next edge in sorted order ($w=4$).
* **Where did this formula originate?** Cycle test: `Find(A) == Find(B)`.
* **How do we execute the step mechanically?**
  $$\text{Find}(A) \implies parent[A] = B \implies \text{Root is } B$$
  $$\text{Find}(B) = B \implies \text{Root is } B$$
  $$\mathbf{\text{Find}(A) == \text{Find}(B) == B \implies \text{CYCLE DETECTED!}}$$
  $$\text{REJECT EDGE } (A, B). \quad E_T \text{ remains unchanged.}$$
* **What changed from previous step?** Edge $(A, B)$ is discarded. $E_T$ count remains $4$. DSU states are unchanged.

---

##### Iteration 6: Edge $(B, D)$, Weight $= 5$ (Final Edge)
* **What are we doing?** Evaluating candidate edge $(B, D)$ with weight $5$.
* **Why are we starting here?** Next edge in sorted order ($w=5$).
* **Where did this formula originate?** Cycle check via `Find(B)` and `Find(D)`.
* **How do we execute the step mechanically?**
  $$\text{Find}(B) = B, \quad \text{Find}(D) = D$$
  $$\text{Since } B \ne D \implies \text{Different components. Accept edge.}$$
  $$E_T \leftarrow E_T \cup \{(B, D)\}$$
  $$\text{Union}(B, D): \text{rank}[B] = 1, \; \text{rank}[D] = 1 \implies \text{Equal ranks. Set } parent[D] \leftarrow B, \; \text{rank}[B] \leftarrow 2$$
  $$\text{Test Termination: } |E_T| = 5 == |V| - 1 \ (6 - 1 = 5) \implies \mathbf{\text{TERMINATE ALGORITHM}}$$
* **What changed from previous step?** Edge $(B, D)$ committed ($|E_T| = 5$). All vertices merged into a single component rooted at $B$. Halting criteria satisfied; remaining edges ($(D, F), (C, D), (C, E)$) are skipped.

---

#### Consolidated Kruskal Execution Trace Table

<div class="table-wrap">

| Step | Edge Examined | Weight | `Find(u)` | `Find(v)` | Decision | Action Taken / DSU Update | MST Edge Count ($|E_T|$) | Cumulative Cost |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | *Init* | - | - | - | Initialize | Sets $\{A\}, \{B\}, \{C\}, \{D\}, \{E\}, \{F\}$ | $0$ | $0$ |
| **1** | $(B, C)$ | $1$ | $B$ | $C$ | **ACCEPT** | $parent[C] \leftarrow B$; Union $\{B, C\}$ | $1$ | $1$ |
| **2** | $(A, C)$ | $2$ | $A$ | $B$ | **ACCEPT** | $parent[A] \leftarrow B$; Union $\{A, B, C\}$ | $2$ | $1 + 2 = 3$ |
| **3** | $(D, E)$ | $2$ | $D$ | $E$ | **ACCEPT** | $parent[E] \leftarrow D$; Union $\{D, E\}$ | $3$ | $3 + 2 = 5$ |
| **4** | $(E, F)$ | $3$ | $D$ | $F$ | **ACCEPT** | $parent[F] \leftarrow D$; Union $\{D, E, F\}$ | $4$ | $5 + 3 = 8$ |
| **5** | $(A, B)$ | $4$ | $B$ | $B$ | **REJECT** | Cycle detected ($B == B$). Discarded. | $4$ | $8$ |
| **6** | $(B, D)$ | $5$ | $B$ | $D$ | **ACCEPT** | $parent[D] \leftarrow B$; Union all into $\{A..F\}$ | $\mathbf{5}$ | $\mathbf{8 + 5 = 13}$ |

</div>

#### Final Kruskal MST Result:
$$E_T = \{ (B, C), (A, C), (D, E), (E, F), (B, D) \}$$
$$\mathbf{\text{Total Minimum Cost} = 1 + 2 + 2 + 3 + 5 = 13}$$

---

<a id="prims-algorithm"></a>
## 3. Prim's Algorithm (Vertex-Centric Greedy Strategy)

<a id="prim-intuition"></a>
### Algorithmic Intuition & Dynamic Cut Interpretation

Unlike Kruskal's algorithm, which builds a forest, Prim's algorithm operates on a **vertex-centric** paradigm. It begins at an arbitrary starting vertex and grows a **single connected tree** $T = (S, E_T)$ by iteratively adding one vertex at a time.

```
                    PRIM'S DYNAMIC CUT TRANSITION MODEL
 Active Tree Partition S                           Unvisited Partition V \ S
+---------------------------------------+         +-------------------------+
|                                       |         |                         |
|   (Root A)                            |         |   (B)     (D)           |
|      |                                |         |                         |
|     [2] (Accepted Tree Edge)          |  Active |        (E)              |
|      v                                |   Cut   |                         |
|     (C) <--- Tree boundary expands    |=======> |             (F)         |
|              to include vertex C      |         |                         |
|                                       |         |  Picks LIGHTEST edge    |
+---------------------------------------+         |  crossing the cut!      |
                                                  +-------------------------+
```

#### The Cut Invariant in Prim's Algorithm:
At every stage of execution:
1. The vertex set is partitioned into two sets:
   * $S$: The set of vertices already incorporated into the growing MST.
   * $V \setminus S$: The set of vertices not yet added to the tree.
2. The boundary between $S$ and $V \setminus S$ forms an **active cut** $(S, V \setminus S)$.
3. Prim's algorithm examines all crossing edges $e = (u, v)$ such that $u \in S$ and $v \in V \setminus S$, and selects the **lightest crossing edge**.
4. By the **Cut Property (Theorem 1)**, this light edge is guaranteed to belong to the MST. The endpoint $v$ is transferred from $V \setminus S$ to $S$.

---

<a id="prim-priority-queue"></a>
### Priority Queue Mechanics: Keys, Parents, and Decrease-Key

To efficiently select the minimum-weight crossing edge at each step, Prim's algorithm maintains a **Min-Priority Queue ($Q$)** containing all vertices currently in $V \setminus S$.

Each vertex $v \in V$ is assigned two state variables:
* **`key[v]`:** The minimum weight among all edges connecting $v$ to any vertex already in $S$. If no such edge exists, $\text{key}[v] = \infty$. For the chosen root vertex $r$, $\text{key}[r] = 0$.
* **`parent[v]`:** The specific vertex $u \in S$ that achieves this minimum-weight connection: $w(u, v) = \text{key}[v]$.

#### Priority Queue Operations:
* **`Extract-Min(Q)`:** Extracts the vertex $u \in Q$ that possesses the minimal `key` value. This vertex is formally transferred into $S$.
* **`Decrease-Key(Q, v, new_weight)`:** When $u$ is added to $S$, the algorithm checks all of $u$'s incident edges $(u, v)$. If $v \in Q$ and $w(u, v) < \text{key}[v]$, the algorithm updates:
  $$\text{key}[v] \leftarrow w(u, v)$$
  $$\text{parent}[v] \leftarrow u$$
  This decreases $v$'s key in $Q$, adjusting its priority dynamically.

---

<a id="prim-pseudocode"></a>
### Complete Algorithm Pseudocode

```text
Algorithm PrimMST(G = (V, E, w), root)
// Input: Connected, undirected, weighted graph G, and a chosen start vertex 'root'
// Output: Arrays parent[1..n] and key[1..n] encoding the MST
begin
    // Step 1: Initialization of vertex state variables: O(V)
    for each vertex v ∈ V do
    begin
        key[v] ← ∞;                  // Initial tentative distance from tree is infinite
        parent[v] ← NIL;             // No parent assigned yet
        inMST[v] ← false;            // Boolean tracking membership in set S
    end;

    key[root] ← 0;                   // Root is extracted first with zero weight
    
    // Step 2: Build priority queue Q containing all vertices in V: O(V)
    Q ← BuildMinHeap(V, key);
    
    // Step 3: Main Extraction and Relaxation Loop
    while Q ≠ ∅ do
    begin
        u ← ExtractMin(Q);           // Extract vertex with smallest key: O(log V)
        inMST[u] ← true;             // Commit vertex u to set S
        
        // Step 4: Traverse all incident edges to relax neighbors
        for each neighbor v of u do
        begin
            weight ← w(u, v);
            
            // Relaxation condition: v must be in V \ S, and edge (u, v)
            // must provide a cheaper connection to the tree than key[v]
            if inMST[v] = false and weight < key[v] then
            begin
                parent[v] ← u;       // Update prospective tree parent
                key[v] ← weight;     // Update connection cost
                DecreaseKey(Q, v, weight); // Rebalance priority queue: O(log V)
            end;
        end;
    end;
    
    return (parent, key);
end;
```

---

<a id="prim-complexity"></a>
### Detailed Complexity Analysis Across Three Implementations

The time complexity of Prim's algorithm depends on the data structures used for the graph representation and the priority queue $Q$.

```
                 OPERATION FREQUENCY BUDGET IN PRIM'S ALGORITHM
+-----------------------------+-----------------------+-----------------------------+
| Operation Class             | Call Frequency        | Purpose                     |
+-----------------------------+-----------------------+-----------------------------+
| `Insert` / `BuildHeap`      | |V| times             | Populate queue initially    |
| `Extract-Min`               | |V| times             | Extract cheapest vertex     |
| `Decrease-Key` (Relaxation) | At most |E| times     | Update neighbor key values  |
+-----------------------------+-----------------------+-----------------------------+
```

<div class="table-wrap">

| Priority Queue Data Structure | Graph Representation | `Extract-Min` Time | `Decrease-Key` Time | Total Asymptotic Time Complexity | Optimal Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unordered Array** | Adjacency Matrix | $O(|V|)$ | $O(1)$ | $O(|V|^2 + |E|) = \mathbf{O(|V|^2)}$ | **Dense Graphs** ($|E| \approx |V|^2$) |
| **Binary Min-Heap** | Adjacency List | $O(\log |V|)$ | $O(\log |V|)$ | $O(|V| \log |V| + |E| \log |V|) = \mathbf{O(|E| \log |V|)}$ | **Sparse Graphs** ($|E| \ll |V|^2$) |
| **Fibonacci Heap** | Adjacency List | $O(\log |V|)$ (amortized) | $O(1)$ (amortized) | $\mathbf{O(|E| + |V| \log |V|)}$ | **Theoretical Best Bound** |

</div>

#### Rigorous Algebraic Derivations:

1. **Implementation A: Adjacency Matrix & Unordered Array**
   * Searching an unsorted array for the minimum key requires scanning all elements: $O(|V|)$ per `Extract-Min`. For $|V|$ extractions:
     $$T_{\text{extract}} = |V| \times O(|V|) = O(|V|^2)$$
   * Checking neighbors via an adjacency matrix requires inspecting all $|V|$ cells in row $u$. Updating a key in an unsorted array takes $O(1)$ time. Summed across all vertices, the neighbor checks take $O(|V|^2)$ total time.
   * **Total Time:** $T(V, E) = O(|V|^2) + O(|V|^2) = \mathbf{O(|V|^2)}$.
   * *Significance:* For dense graphs where $|E| = \Theta(|V|^2)$, this array-based approach matches the binary heap's asymptotic bound while avoiding heap pointer overhead.

2. **Implementation B: Adjacency List & Binary Min-Heap**
   * Building the initial heap takes $O(|V|)$ time using Floyd's heap construction algorithm.
   * There are $|V|$ `Extract-Min` operations, each requiring $O(\log |V|)$ to restore the heap invariant:
     $$T_{\text{extract}} = |V| \times O(\log |V|) = O(|V| \log |V|)$$
   * The inner loop examines each directed edge representation at most twice (once from each endpoint for an undirected edge). Thus, the relaxation condition triggers at most $|E|$ times. Each `Decrease-Key` in a binary heap bubbles an element up the tree in $O(\log |V|)$ time:
     $$T_{\text{decrease}} = |E| \times O(\log |V|) = O(|E| \log |V|)$$
   * **Total Time:**
     $$T(V, E) = O(|V| \log |V| + |E| \log |V|) = \mathbf{O((|V| + |E|) \log |V|)}$$
     Since $G$ is connected, $|E| \ge |V| - 1$, so this simplifies to $\mathbf{O(|E| \log |V|)}$.

3. **Implementation C: Adjacency List & Fibonacci Heap**
   * A Fibonacci heap supports `Extract-Min` in $O(\log |V|)$ amortized time, and `Decrease-Key` in $O(1)$ amortized time.
   * **Total Time:**
     $$T(V, E) = |V| \cdot O(\log |V|) + |E| \cdot O(1) = \mathbf{O(|E| + |V| \log |V|)}$$
   * *Significance:* For dense graphs where $|E| = \Theta(|V|^2)$, this evaluates to $O(|V|^2)$. For sparse graphs where $|E| = \Theta(|V|)$, it evaluates to $O(|V| \log |V|)$.

---

<a id="prim-trace"></a>
### Step-by-Step 5W1H Stepped Execution Trace

We trace Prim's algorithm on the same 6-vertex reference graph, selecting **Vertex $A$** as the starting root.

#### Graph Parameters:
* $V = \{A, B, C, D, E, F\}$, $|V| = 6$.
* Edge set $E$:
  $$(A, B): 4, \; (A, C): 2, \; (B, C): 1, \; (B, D): 5, \; (C, D): 8, \; (C, E): 10, \; (D, E): 2, \; (D, F): 6, \; (E, F): 3$$

---

#### Phase 1: Initialization
* Set `key[A] = 0`, and `key[v] = ∞` for all $v \in \{B, C, D, E, F\}$.
* Set `parent[v] = NIL` for all $v \in V$.
* Set `inMST[v] = false` for all $v \in V$.
* $Q = \{ (A, 0), (B, \infty), (C, \infty), (D, \infty), (E, \infty), (F, \infty) \}$.
* $S = \emptyset$.

---

#### Phase 2: The 5W1H Stepped Execution Trace

##### Iteration 1: Processing Root Vertex $A$
* **What are we doing?** Extracting the minimum key vertex from $Q$ and relaxing its neighbors.
* **Why are we starting here?** `key[A] = 0` is the globally minimal value in $Q$.
* **Where did this formula originate?** The condition `w(u, v) < key[v]`.
* **How do we execute the step mechanically?**
  $$\text{Extract-Min}(Q) \implies u = A. \quad \text{Set } inMST[A] \leftarrow true. \quad S = \{A\}$$
  $$\text{Examine incident edges from } A \text{ to neighbors } v \notin S:$$
  $$\text{Neighbor } B: w(A, B) = 4 < key[B] \ (\infty) \implies key[B] \leftarrow 4, \; parent[B] \leftarrow A$$
  $$\text{Neighbor } C: w(A, C) = 2 < key[C] \ (\infty) \implies key[C] \leftarrow 2, \; parent[C] \leftarrow A$$
* **What changed from previous step?** Vertex $A$ entered $S$. $Q$ values for $B$ and $C$ updated from $\infty$ to $4$ and $2$, respectively.

---

##### Iteration 2: Processing Vertex $C$
* **What are we doing?** Extracting the minimum key vertex from remaining $Q = \{ (B, 4), (C, 2), (D, \infty), (E, \infty), (F, \infty) \}$.
* **Why are we starting here?** $C$ has the smallest key: $\text{key}[C] = 2$.
* **Where did this formula originate?** Active cut $(S, V \setminus S)$ has crossing edges $(A, B)$ with cost 4, and $(A, C)$ with cost 2. Light edge is $(A, C)$.
* **How do we execute the step mechanically?**
  $$\text{Extract-Min}(Q) \implies u = C. \quad \text{Set } inMST[C] \leftarrow true. \quad S = \{A, C\}$$
  $$\text{MST edge committed: } (parent[C], C) = (A, C) \text{ with weight } 2.$$
  $$\text{Relax neighbors } v \notin S \text{ of } C \ (B, D, E):$$
  $$\text{Neighbor } B: w(C, B) = 1 < key[B] \ (4) \implies \mathbf{key[B] \leftarrow 1, \; parent[B] \leftarrow C \quad (\text{Decrease-Key!})}$$
  $$\text{Neighbor } D: w(C, D) = 8 < key[D] \ (\infty) \implies key[D] \leftarrow 8, \; parent[D] \leftarrow C$$
  $$\text{Neighbor } E: w(C, E) = 10 < key[E] \ (\infty) \implies key[E] \leftarrow 10, \; parent[E] \leftarrow C$$
* **What changed from previous step?** Vertex $C$ committed to $S$. Edge $(A, C)$ added to tree. Key of $B$ decreased from $4$ to $1$ because edge $(C, B)$ provides a cheaper connection to the tree.

---

##### Iteration 3: Processing Vertex $B$
* **What are we doing?** Extracting minimum from $Q = \{ (B, 1), (D, 8), (E, 10), (F, \infty) \}$.
* **Why are we starting here?** $B$ has the smallest key ($\text{key}[B] = 1$).
* **Where did this formula originate?** Light edge across cut $(\{A, C\}, \{B, D, E, F\})$ is $(C, B)$ with weight $1$.
* **How do we execute the step mechanically?**
  $$\text{Extract-Min}(Q) \implies u = B. \quad \text{Set } inMST[B] \leftarrow true. \quad S = \{A, C, B\}$$
  $$\text{MST edge committed: } (parent[B], B) = (C, B) \text{ with weight } 1.$$
  $$\text{Relax neighbors } v \notin S \text{ of } B \ (D):$$
  $$\text{Neighbor } D: w(B, D) = 5 < key[D] \ (8) \implies \mathbf{key[D] \leftarrow 5, \; parent[D] \leftarrow B \quad (\text{Decrease-Key!})}$$
* **What changed from previous step?** Vertex $B$ committed to $S$. Edge $(C, B)$ added to tree. Key of $D$ decreased from $8$ to $5$.

---

##### Iteration 4: Processing Vertex $D$
* **What are we doing?** Extracting minimum from $Q = \{ (D, 5), (E, 10), (F, \infty) \}$.
* **Why are we starting here?** $D$ has the smallest key ($\text{key}[D] = 5$).
* **Where did this formula originate?** Light edge across cut $(\{A, B, C\}, \{D, E, F\})$ is $(B, D)$ with weight $5$.
* **How do we execute the step mechanically?**
  $$\text{Extract-Min}(Q) \implies u = D. \quad \text{Set } inMST[D] \leftarrow true. \quad S = \{A, B, C, D\}$$
  $$\text{MST edge committed: } (parent[D], D) = (B, D) \text{ with weight } 5.$$
  $$\text{Relax neighbors } v \notin S \text{ of } D \ (E, F):$$
  $$\text{Neighbor } E: w(D, E) = 2 < key[E] \ (10) \implies \mathbf{key[E] \leftarrow 2, \; parent[E] \leftarrow D \quad (\text{Decrease-Key!})}$$
  $$\text{Neighbor } F: w(D, F) = 6 < key[F] \ (\infty) \implies key[F] \leftarrow 6, \; parent[F] \leftarrow D$$
* **What changed from previous step?** Vertex $D$ committed to $S$. Edge $(B, D)$ added to tree. Key of $E$ updated from $10$ down to $2$, and $F$ updated from $\infty$ down to $6$.

---

##### Iteration 5: Processing Vertex $E$
* **What are we doing?** Extracting minimum from $Q = \{ (E, 2), (F, 6) \}$.
* **Why are we starting here?** $E$ has the smallest key ($\text{key}[E] = 2$).
* **Where did this formula originate?** Light edge across cut $(\{A, B, C, D\}, \{E, F\})$ is $(D, E)$ with weight $2$.
* **How do we execute the step mechanically?**
  $$\text{Extract-Min}(Q) \implies u = E. \quad \text{Set } inMST[E] \leftarrow true. \quad S = \{A, B, C, D, E\}$$
  $$\text{MST edge committed: } (parent[E], E) = (D, E) \text{ with weight } 2.$$
  $$\text{Relax neighbors } v \notin S \text{ of } E \ (F):$$
  $$\text{Neighbor } F: w(E, F) = 3 < key[F] \ (6) \implies \mathbf{key[F] \leftarrow 3, \; parent[F] \leftarrow E \quad (\text{Decrease-Key!})}$$
* **What changed from previous step?** Vertex $E$ committed to $S$. Edge $(D, E)$ added to tree. Key of $F$ reduced from $6$ to $3$.

---

##### Iteration 6: Processing Final Vertex $F$
* **What are we doing?** Extracting the final vertex from $Q = \{ (F, 3) \}$.
* **Why are we starting here?** $F$ is the sole remaining vertex in $Q$.
* **Where did this formula originate?** Crossing edge to remaining vertex $F$ is $(E, F)$ with weight $3$.
* **How do we execute the step mechanically?**
  $$\text{Extract-Min}(Q) \implies u = F. \quad \text{Set } inMST[F] \leftarrow true. \quad S = \{A, B, C, D, E, F\} = V$$
  $$\text{MST edge committed: } (parent[F], F) = (E, F) \text{ with weight } 3.$$
  $$Q \text{ is now empty } (\emptyset) \implies \text{HALT ALGORITHM.}$$
* **What changed from previous step?** All vertices are now members of $S$. Exactly $|V| - 1 = 5$ edges have been committed. Algorithm terminates.

---

#### Consolidated Prim Priority Queue and State Transition Matrix

<div class="table-wrap">

| Step ($k$) | Vertex Extracted ($u$) | Edge Committed | Edge Cost | `key[A]` | `key[B]` | `key[C]` | `key[D]` | `key[E]` | `key[F]` | Priority Queue State ($Q$) After Relaxation |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | *Init* | - | - | **$0$** | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\{ (A,0), (B,\infty), (C,\infty), (D,\infty), (E,\infty), (F,\infty) \}$ |
| **1** | $A$ | *Root* | $0$ | *in S* | $4$ | $2$ | $\infty$ | $\infty$ | $\infty$ | $\{ (C,2), (B,4), (D,\infty), (E,\infty), (F,\infty) \}$ |
| **2** | $C$ | $(A, C)$ | $2$ | *in S* | **$1$** | *in S* | $8$ | $10$ | $\infty$ | $\{ (B,1), (D,8), (E,10), (F,\infty) \}$ |
| **3** | $B$ | $(C, B)$ | $1$ | *in S* | *in S* | *in S* | **$5$** | $10$ | $\infty$ | $\{ (D,5), (E,10), (F,\infty) \}$ |
| **4** | $D$ | $(B, D)$ | $5$ | *in S* | *in S* | *in S* | *in S* | **$2$** | $6$ | $\{ (E,2), (F,6) \}$ |
| **5** | $E$ | $(D, E)$ | $2$ | *in S* | *in S* | *in S* | *in S* | *in S* | **$3$** | $\{ (F,3) \}$ |
| **6** | $F$ | $(E, F)$ | $3$ | *in S* | *in S* | *in S* | *in S* | *in S* | *in S* | $\emptyset$ (Queue fully exhausted) |

</div>

#### Final Prim MST Result:
$$E_T = \{ (A, C), (C, B), (B, D), (D, E), (E, F) \}$$
$$\mathbf{\text{Total Minimum Cost} = 2 + 1 + 5 + 2 + 3 = 13}$$
*(Note: The computed set of edges and total cost are identical to those generated by Kruskal's algorithm).*

---

<a id="comparative-analysis"></a>
## 4. Comparative Architectural Analysis: Kruskal vs. Prim

<a id="comparison-matrix"></a>
### Side-by-Side Structural Comparison Matrix

<div class="table-wrap">

| Evaluation Dimension | Kruskal's Algorithm | Prim's Algorithm |
| :--- | :--- | :--- |
| **Core Paradigm** | **Edge-Centric** greedy strategy | **Vertex-Centric** greedy strategy |
| **State Evolution** | Grows a **forest of subtrees** that merges into one tree | Grows a **single tree** by expanding outward |
| **Primary Data Structure** | **Disjoint Set Union (DSU)** with Rank & Path Compression | **Min-Priority Queue** (Binary Heap or Fibonacci Heap) |
| **Initial Preprocessing** | Requires sorting **all** $|E|$ edges globally | Requires no global edge sort; initializes vertex keys |
| **Time: Sparse Graphs ($|E| \approx |V|$)** | $\mathbf{O(|E| \log |V|)}$ | $\mathbf{O(|E| \log |V|)}$ (with Binary Heap) |
| **Time: Dense Graphs ($|E| \approx |V|^2$)** | $O(|V|^2 \log |V|)$ | $\mathbf{O(|V|^2)}$ (with Adjacency Matrix) |
| **Cycle Prevention Mechanism** | Cycle check via set query: $\text{Find}(u) == \text{Find}(v)$ | Only selects edges to unvisited vertices ($v \notin S$) |
| **Behavior on Disconnected Graphs**| Naturally outputs a **Minimum Spanning Forest** | Fails unless restarted across remaining components |
| **Memory Space Consumption** | $\Theta(|V| + |E|)$ to store and sort edge array | $\Theta(|V|)$ auxiliary space for priority queue |

</div>

---

<a id="selection-guide"></a>
### Graph Topology and Data Structure Selection Guide

```
                         ENGINEERING SELECTION LOGIC
                             Graph Input G = (V, E)
                                       |
                                       v
                           Is the graph sparse or dense?
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v Sparse (|E| << |V|^2)                 v Dense (|E| ≈ |V|^2)
         Is the edge list ALREADY                          Use PRIM'S ALGORITHM
         sorted or integers in small range?                with ADJACENCY MATRIX
                   |                                       Time Complexity: O(V^2)
          +--------+--------+                              (No heap overhead!)
          |                 |
          v YES             v NO
      KRUSKAL           KRUSKAL or PRIM
    with DSU:         with BINARY HEAP:
    O(E * α(V))           O(E log V)
```

1. **When to Select Kruskal's Algorithm:**
   * When the graph is **sparse** ($|E| \ll |V|^2$), such as planar road networks or electrical grids where vertex degrees are bounded by small constants.
   * When the edges are **already pre-sorted** (or can be sorted in linear time via Counting Sort). In this case, Kruskal runs in almost linear time: $O(|E| \cdot \alpha(|V|))$.
   * When the input graph is not guaranteed to be connected. Kruskal automatically outputs the optimal Minimum Spanning Forest without requiring modification.

2. **When to Select Prim's Algorithm:**
   * When the graph is **dense** ($|E| \approx |V|^2$). Prim's algorithm implemented with a simple adjacency matrix and an unordered array executes in $O(|V|^2)$ time, outperforming Kruskal's $O(|V|^2 \log |V|)$ approach.
   * When edges arrive dynamically as a continuous stream originating from an anchor node, allowing the tree to grow without waiting for the complete graph topology to stabilize.

---

<a id="exam-summary"></a>
## 5. KTU Exam High-Yield Summary

<a id="three-mark-questions"></a>
### Frequently Asked 3-Mark Questions & Model Answers

#### Q1: State the Cut Property of Minimum Spanning Trees.
**Model Answer:**
Let $G = (V, E)$ be a connected, undirected, weighted graph, and let $(S, V \setminus S)$ be any cut of $G$. If an edge $e = (u, v)$ is a light edge (minimum weight) crossing $(S, V \setminus S)$, then $e$ belongs to some Minimum Spanning Tree of $G$. If this light edge is unique, it belongs to every MST of $G$.

---

#### Q2: Explain why Kruskal's algorithm uses the Disjoint Set Union (DSU) data structure.
**Model Answer:**
Kruskal's algorithm must determine whether adding candidate edge $(u, v)$ creates a cycle. Using DSU:
* $\text{Find}(u) == \text{Find}(v)$ tests whether $u$ and $v$ already share the same tree component (detecting a cycle in $O(\alpha(V))$ time).
* If roots differ, $\text{Union}(u, v)$ merges the components.
DSU replaces an $O(V)$ DFS cycle check with an effective $O(1)$ operation, reducing the greedy loop time to $O(E \cdot \alpha(V))$.

---

#### Q3: Contrast the behavior of Prim's and Kruskal's algorithms on a disconnected graph.
**Model Answer:**
* **Kruskal's Algorithm:** Automatically handles disconnected graphs. It processes all components in parallel, producing a **Minimum Spanning Forest** (an MST for each connected component).
* **Prim's Algorithm:** Halts after spanning only the component containing the root vertex, leaving other components unvisited unless an outer loop restarts the algorithm on remaining vertices.

---

#### Q4: State the Cycle Property and explain its significance in MST algorithms.
**Model Answer:**
For any simple cycle $C$ in graph $G$, the edge with the strictly maximum weight in $C$ cannot belong to any Minimum Spanning Tree.
* *Significance:* It forms the theoretical dual to the Cut Property, justifying why greedy algorithms can safely discard heavy edges when a cycle is detected.

---

<a id="marking-traps"></a>
### High-Frequency Student Pitfalls & Marking Scheme Traps

::: callout-warning Exam Traps & Avoidance Strategies
1. **The Prim's Decrease-Key Omission:**
   * *The Error:* When executing Prim's algorithm by hand, students often record the weight of edge $(u, v)$ into `key[v]` without checking if an earlier edge already assigned a smaller value to `key[v]`.
   * *The Fix:* Always write the check: `new_weight < current_key`. Only overwrite if the new edge is strictly cheaper:
     $$\text{key}[v] \leftarrow \min(\text{key}[v], \; w(u, v))$$

2. **The Kruskal Cycle Test Slip:**
   * *The Error:* Attempting to stop Kruskal's algorithm only when the edge list runs out, rather than halting at $|V| - 1$ edges.
   * *The Fix:* Track an explicit counter: `edgeCount`. Stop as soon as `edgeCount == |V| - 1`. Evaluating the remaining edges wastes exam time and introduces risk of cycle errors.

3. **Confusing Heap Decrease-Key with Insert:**
   * *The Error:* Treating Prim's priority queue updates as inserting duplicate vertices rather than updating existing keys.
   * *The Fix:* In standard textbook descriptions (CLRS/KTU), all $|V|$ vertices are inserted into $Q$ at the start. Relaxation *decreases* the key of an existing vertex rather than adding a new element.

4. **Kruskal Logarithm Reduction Mistake in Complexity Questions:**
   * *The Error:* Stating that Kruskal's sorting step is $O(E \log E)$ and failing to simplify it to $O(E \log V)$, losing the simplification mark.
   * *The Fix:* Write out the algebraic step:
     $$E \le V^2 \implies \log E \le \log(V^2) = 2 \log V \implies O(E \log E) = O(E \log V)$$
:::
