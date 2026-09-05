# Module 4 - Problem Worklab 5: 2-Approximation Algorithm for Vertex Cover

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search, Computational Complexity & Approximation Algorithms  
**Document Classification:** Publication-Grade Problem Worklab & Rigorous Algorithmic Trace  

---

## 1. Executive Summary & Foundational Approximation Theory

The **Minimum Vertex Cover Problem** is one of Richard Karp's canonical $\text{NP}$-complete decision problems (1972) and an archetypal $\text{NP}$-hard combinatorial optimization problem. Unless $\text{P} = \text{NP}$, no deterministic algorithm can compute the exact minimum vertex cover of an arbitrary graph in polynomial time. 

To overcome this intractability in real-world networks, compiler design, and facility location, we utilize **Approximation Algorithms**. Instead of searching for the exact mathematical minimum, we design polynomial-time heuristics that guarantee a provable mathematical ceiling on the sub-optimality of the returned solution.

```text
========================================================================================================
                      THE 2-APPROXIMATION MAXIMAL MATCHING PRINCIPLE
========================================================================================================

          Original Graph G = (V, E)
                     |
                     v   Greedy Arbitrary Edge Extraction
          Maximal Matching M ⊆ E
          (Pairwise disjoint edges: no two share a vertex)
                     |
          +----------+----------+
          |                     |
          v                     v
   Lower Bound on C*     Upper Bound on Approx C
     |C*| ≥ |M|            |C| = 2|M|
          |                     |
          +----------+----------+
                     |
                     v   Divide Upper Bound by Lower Bound
           Approximation Ratio ρ:
           |C| / |C*| ≤ 2|M| / |M| = 2.0
```

### 1.1 Mathematical Formulation of Minimum Vertex Cover
Given an undirected, unweighted simple graph $G = (V, E)$ without self-loops:
- **Optimization Objective:** Find a subset of vertices $V' \subseteq V$ such that:
  $$\min |V'|$$
- **Subject to the Covering Constraint:** Every edge in the graph must be incident to at least one vertex in $V'$:
  $$\forall \; e = (u, v) \in E \implies (u \in V' \lor v \in V')$$

### 1.2 The Performance Ratio Metric ($\rho$)
For a minimization problem, an algorithm has an **approximation ratio** $\rho \ge 1$ if for every input instance of size $n$, the returned solution cost $C$ and the true optimal cost $C^*$ satisfy:

$$\frac{C}{C^*} \le \rho \iff C \le \rho \cdot C^*$$

An algorithm achieving $\rho = 2$ guarantees that the cardinality of the computed vertex cover will **never exceed twice the cardinality of the optimal cover**, regardless of the graph's size, density, or pathological topology.

::: callout-intuition
**Mental Model: The Edge-Guarding Contract**  
Imagine every edge in a graph is a dark corridor requiring surveillance. You must station guards at room intersections (vertices). 
- If you find a set of completely separate corridors that share no common doors (a **matching** $M$), an optimal security chief is forced to station **at least one guard** for each such corridor: $|C^*| \ge |M|$.
- Instead of solving the puzzle of which specific door to guard, the **2-Approximation Algorithm** conservatively stations guards at **both ends** of each isolated corridor: $|C| = 2|M|$.
- Because you hired exactly 2 guards per corridor, while the optimal chief must hire at least 1, your payroll is guaranteed to be at most double the optimal expenditure: $|C| \le 2|C^*|$.
:::

---

## 2. Level 1: Step-by-Step Execution of Approx-Vertex-Cover

### Problem 1.1 Specification
Let $G = (V, E)$ be an undirected graph with:
- **Vertex Set ($|V| = 7$):** $V = \{A, B, C, D, E, F, G\}$
- **Edge Set ($|E| = 7$):**
  $$e_1 = (A, B), \quad e_2 = (B, C), \quad e_3 = (C, D), \quad e_4 = (C, E), \quad e_5 = (D, E), \quad e_6 = (D, F), \quad e_7 = (E, G)$$

```text
========================================================================================================
                                     INPUT GRAPH TOPOLOGY G = (V, E)
========================================================================================================

          (A)
           |
           | e_1
           |
          (B)
           |
           | e_2
           |
          (C)-----------------(D)-----------------(F)
            \                 / |                  
             \               /  | e_6             
              \             /   |                  
           e_4 \       e_5 /    |                  
                \         /     |                  
                 \       /      |                  
                  \     /       |                  
                   \   /        |                  
                    (E)---------+                  
                     |
                     | e_7
                     |
                    (G)

   Topological Observations:
   - Pendant Vertices (Degree 1): A, F, G.
   - Bridge/Articulation Vertex: B (Degree 2).
   - Dense Central Triangle: {C, D, E} induced by edges e_3, e_4, e_5.
   - Degrees: deg(A)=1, deg(B)=2, deg(C)=3, deg(D)=3, deg(E)=3, deg(F)=1, deg(G)=1.
========================================================================================================
```

---

### Step-Card 1.1: Initialization & Baseline State Setup

#### 1. What are we doing?
Initializing the working candidate cover set $C$, the working dynamic edge set $E'$, and the selected maximal matching set $M$.

#### 2. Why are we starting here?
The Gavril-Yannakakis algorithm operates by iteratively shrinking the set of uncovered edges. We must begin with an empty cover ($|C| = 0$) and the complete edge set ($E' = E$).

#### 3. How do we execute the step mechanically?
- Initialize Cover Set:
  $$C = \emptyset \quad (|C| = 0)$$
- Initialize Selected Matching Set:
  $$M = \emptyset \quad (|M| = 0)$$
- Initialize Working Uncovered Edge Pool:
  $$E' = E = \{e_1, e_2, e_3, e_4, e_5, e_6, e_7\}$$
  $$|E'| = 7$$

#### 4. Where did this formula / invariant originate?
From the initialization preconditions of the Gavril-Yannakakis algorithm (1974).

#### 5. What changed from the previous step?
Global system state established:
$$\text{State}_0: \quad C = \emptyset, \quad M = \emptyset, \quad |E'| = 7$$

---

### Step-Card 1.2: Iteration 1 — Selection of Edge $e_1 = (A, B)$

#### 1. What are we doing?
Extracting an arbitrary edge from the remaining edge pool $E'$, placing both of its endpoints into the candidate vertex cover $C$, adding the edge to matching $M$, and removing all edges incident to either endpoint from $E'$.

#### 2. Why this choice?
The algorithm allows an arbitrary choice. We select edge $e_1 = (A, B) \in E'$.

#### 3. How do we execute the step mechanically?

##### Phase 1: Edge Extraction & Cover Insertion
- Pick edge:
  $$e^*_1 = (A, B)$$
- Commit to Matching:
  $$M \leftarrow M \cup \{(A, B)\} = \{(A, B)\} \quad (|M| = 1)$$
- Commit Endpoints to Cover:
  $$C \leftarrow C \cup \{A, B\} = \{A, B\} \quad (|C| = 2)$$

##### Phase 2: Incidence Invalidation Audit on $E'$
We inspect every remaining edge $e = (u, v) \in E'$ and discard it if $(u \in \{A, B\}) \lor (v \in \{A, B\})$:

| Edge Index | Edge $e = (u, v)$ | Endpoint $u$ | Endpoint $v$ | Incidence Check: Does $u \in \{A, B\} \lor v \in \{A, B\}$? | Action on Edge |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $e_1$ | $(A, B)$ | $A \in \{A, B\}$ | $B \in \{A, B\}$ | $\text{True} \lor \text{True} = \mathbf{TRUE}$ | **REMOVE (Chosen Edge)** |
| $e_2$ | $(B, C)$ | $B \in \{A, B\}$ | $C \notin \{A, B\}$ | $\text{True} \lor \text{False} = \mathbf{TRUE}$ | **REMOVE (Incident via $B$)** |
| $e_3$ | $(C, D)$ | $C \notin \{A, B\}$ | $D \notin \{A, B\}$ | $\text{False} \lor \text{False} = \mathbf{FALSE}$ | **RETAIN** |
| $e_4$ | $(C, E)$ | $C \notin \{A, B\}$ | $E \notin \{A, B\}$ | $\text{False} \lor \text{False} = \mathbf{FALSE}$ | **RETAIN** |
| $e_5$ | $(D, E)$ | $D \notin \{A, B\}$ | $E \notin \{A, B\}$ | $\text{False} \lor \text{False} = \mathbf{FALSE}$ | **RETAIN** |
| $e_6$ | $(D, F)$ | $D \notin \{A, B\}$ | $F \notin \{A, B\}$ | $\text{False} \lor \text{False} = \mathbf{FALSE}$ | **RETAIN** |
| $e_7$ | $(E, G)$ | $E \notin \{A, B\}$ | $G \notin \{A, B\}$ | $\text{False} \lor \text{False} = \mathbf{FALSE}$ | **RETAIN** |

##### Phase 3: Active Subgraph Update
The remaining edge set becomes:
$$E' = E' \setminus \{(A, B), (B, C)\} = \{(C, D), (C, E), (D, E), (D, F), (E, G)\}$$
$$|E'| = 7 - 2 = 5 \text{ edges remaining}$$

#### 4. Where did this formula / invariant originate?
From the maximal matching definition: removing all incident edges guarantees that no subsequently selected edge will share any vertex with $(A, B)$, ensuring $M$ remains a set of independent edges.

#### 5. What changed from the previous step?
- Candidate cover grew by $2$: $C = \{A, B\}$.
- Matching grew by $1$: $M = \{(A, B)\}$.
- Edge pool decreased by $2$: $|E'| = 5$.

```text
========================================================================================================
                               REMAINING UNCOVERED SUBGRAPH AFTER ITERATION 1
========================================================================================================

   [ Covered Subgraph ]                 [ Active Uncovered Edge Pool E' ]
   
       (A)*                                   (C)-----------------(D)-----------------(F)
        |                                       \                 / |                  
        | e_1 [IN MATCHING]                      \               /  | e_6             
        |                                         \             /   |                  
       (B)*                                    e_4 \       e_5 /    |                  
        :                                           \         /     |                  
        : e_2 [Covered by B]                         \       /      |                  
        :                                             \     /       |                  
                                                       (E)---------+                  
                                                        |
                                                        | e_7
                                                        |
                                                       (G)
   * indicates vertex in Cover C
========================================================================================================
```

---

### Step-Card 1.3: Iteration 2 — Selection of Edge $e_3 = (C, D)$

#### 1. What are we doing?
Selecting the next arbitrary edge from the updated edge pool $E'$, adding both endpoints to $C$, recording the edge in $M$, and purging incident edges.

#### 2. Why this choice?
Active edges in $E'$ are $\{(C, D), (C, E), (D, E), (D, F), (E, G)\}$. We arbitrarily select edge $e_3 = (C, D)$.

#### 3. How do we execute the step mechanically?

##### Phase 1: Edge Extraction & Cover Insertion
- Pick edge:
  $$e^*_2 = (C, D)$$
- Commit to Matching:
  $$M \leftarrow M \cup \{(C, D)\} = \{(A, B), (C, D)\} \quad (|M| = 2)$$
- Commit Endpoints to Cover:
  $$C \leftarrow C \cup \{C, D\} = \{A, B, C, D\} \quad (|C| = 4)$$

##### Phase 2: Incidence Invalidation Audit on $E'$
Inspect remaining edges in $E'$ for incidence with $\{C, D\}$:

| Edge Index | Edge $e = (u, v)$ | Endpoint $u$ | Endpoint $v$ | Incidence Check: Does $u \in \{C, D\} \lor v \in \{C, D\}$? | Action on Edge |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $e_3$ | $(C, D)$ | $C \in \{C, D\}$ | $D \in \{C, D\}$ | $\text{True} \lor \text{True} = \mathbf{TRUE}$ | **REMOVE (Chosen Edge)** |
| $e_4$ | $(C, E)$ | $C \in \{C, D\}$ | $E \notin \{C, D\}$ | $\text{True} \lor \text{False} = \mathbf{TRUE}$ | **REMOVE (Incident via $C$)** |
| $e_5$ | $(D, E)$ | $D \in \{C, D\}$ | $E \notin \{C, D\}$ | $\text{True} \lor \text{False} = \mathbf{TRUE}$ | **REMOVE (Incident via $D$)** |
| $e_6$ | $(D, F)$ | $D \in \{C, D\}$ | $F \notin \{C, D\}$ | $\text{True} \lor \text{False} = \mathbf{TRUE}$ | **REMOVE (Incident via $D$)** |
| $e_7$ | $(E, G)$ | $E \notin \{C, D\}$ | $G \notin \{C, D\}$ | $\text{False} \lor \text{False} = \mathbf{FALSE}$ | **RETAIN** |

##### Phase 3: Active Subgraph Update
The remaining edge set becomes:
$$E' = E' \setminus \{(C, D), (C, E), (D, E), (D, F)\} = \{(E, G)\}$$
$$|E'| = 5 - 4 = 1 \text{ edge remaining}$$

#### 4. Where did this formula / invariant originate?
Purging all edges incident to $\{C, D\}$ simultaneously covers the entire central triangle $\{C, D, E\}$ and the leaf edge $(D, F)$.

#### 5. What changed from the previous step?
- Candidate cover grew by $2$: $C = \{A, B, C, D\}$.
- Matching grew by $1$: $M = \{(A, B), (C, D)\}$.
- Edge pool dropped to exactly $1$ edge: $E' = \{(E, G)\}$.

```text
========================================================================================================
                               REMAINING UNCOVERED SUBGRAPH AFTER ITERATION 2
========================================================================================================

   [ Covered Subgraph ]                                 [ Active Uncovered Pool E' ]
   
       (A)*                                             
        |                                               
        | e_1 [IN MATCHING]                             
        |                                               
       (B)*                                             
        :                                               
        : e_2 [Covered by B]                             
        :                                               
       (C)*.................(D)*................:(F)    
        :                 :   :                         
        :                 :   : e_6 [Covered by D]      
        :                 :   :                         
     e_4:              e_5:   :                         
 [by C] :          [by D] :   :                         
        :                 :   :                         
        :                 :   :                         
        :........(E)......:...+                         
                  |                                     (E)
                  | e_7                                  |
                  |                                      | e_7
                 (G)                                    (G)
========================================================================================================
```

---

### Step-Card 1.4: Iteration 3 — Selection of Edge $e_7 = (E, G)$ & Termination

#### 1. What are we doing?
Selecting the final remaining edge from $E'$, adding both endpoints to $C$, adding the edge to $M$, and confirming loop termination.

#### 2. Why this choice?
$E'$ contains only a single edge: $e_7 = (E, G)$. There are no other choices available.

#### 3. How do we execute the step mechanically?

##### Phase 1: Edge Extraction & Cover Insertion
- Pick edge:
  $$e^*_3 = (E, G)$$
- Commit to Matching:
  $$M \leftarrow M \cup \{(E, G)\} = \{(A, B), (C, D), (E, G)\} \quad (|M| = 3)$$
- Commit Endpoints to Cover:
  $$C \leftarrow C \cup \{E, G\} = \{A, B, C, D, E, G\} \quad (|C| = 6)$$

##### Phase 2: Incidence Invalidation Audit on $E'$
- Removing edge $e_7 = (E, G)$ exhausts the pool:
  $$E' \leftarrow E' \setminus \{(E, G)\} = \emptyset$$

##### Phase 3: Termination Verification
- The loop predicate evaluates:
  $$\text{while } (E' \ne \emptyset) \implies \emptyset \ne \emptyset \quad (\mathbf{FALSE})$$
- The algorithm halts.

#### 4. Output of Approx-Vertex-Cover:
- Resulting Vertex Cover:
  $$C_{\text{approx}} = \{A, B, C, D, E, G\}$$
- Cardinality of Approximate Cover:
  $$|C_{\text{approx}}| = 6$$
- Certified Maximal Matching Witness:
  $$M = \{(A, B), (C, D), (E, G)\} \quad \text{with } |M| = 3$$

---

### Step-Card 1.5: 7-Edge Verification Audit Table for $C_{\text{approx}}$

To verify that $C_{\text{approx}} = \{A, B, C, D, E, G\}$ is a valid vertex cover, we test every edge in $E$:

| Edge Index | Edge $e = (u, v)$ | Endpoint $u \in C$? | Endpoint $v \in C$? | Covering Evaluation ($u \in C \lor v \in C$) | Covering Status | Covering Witness Vertex |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $e_1$ | $(A, B)$ | $A \in C \implies \text{True}$ | $B \in C \implies \text{True}$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $A, B$ |
| $e_2$ | $(B, C)$ | $B \in C \implies \text{True}$ | $C \in C \implies \text{True}$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $B, C$ |
| $e_3$ | $(C, D)$ | $C \in C \implies \text{True}$ | $D \in C \implies \text{True}$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $C, D$ |
| $e_4$ | $(C, E)$ | $C \in C \implies \text{True}$ | $E \in C \implies \text{True}$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $C, E$ |
| $e_5$ | $(D, E)$ | $D \in C \implies \text{True}$ | $E \in C \implies \text{True}$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $D, E$ |
| $e_6$ | $(D, F)$ | $D \in C \implies \text{True}$ | $F \notin C \implies \text{False}$ | $\text{True} \lor \text{False} = \text{True}$ | **COVERED** | $D$ |
| $e_7$ | $(E, G)$ | $E \in C \implies \text{True}$ | $G \in C \implies \text{True}$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $E, G$ |

All 7 edges are covered. $C_{\text{approx}}$ is a certified, valid Vertex Cover.

---

### Step-Card 1.6: Mathematical Derivation of True Optimal Vertex Cover $C^*$

#### 1. What are we doing?
Determining the true optimal minimum vertex cover $C^*$ of graph $G$ and calculating its exact cardinality $|C^*|$.

#### 2. Why are we doing this?
To establish the ground-truth denominator for calculating the empirical approximation ratio $\rho = \frac{|C|}{|C^*|}$.

#### 3. How do we execute the step mechanically?

##### Phase 1: Theoretical Lower Bound via Matching
The algorithm extracted matching:
$$M = \{(A, B), (C, D), (E, G)\}$$
- Observe that these 3 edges are **pairwise vertex-disjoint**:
  $$\{A, B\} \cap \{C, D\} = \emptyset$$
  $$\{C, D\} \cap \{E, G\} = \emptyset$$
  $$\{A, B\} \cap \{E, G\} = \emptyset$$
- A single vertex can cover at most one edge in any matching.
- Therefore, to cover all 3 mutually disjoint edges, any valid vertex cover must contain at least one vertex from each matching edge:
  $$|C^*| \ge |M| = 3$$
- **Conclusion:** The optimal cover cannot have fewer than 3 vertices ($|C^*| \ge 3$).

##### Phase 2: Candidate Evaluation for Size $k = 3$
Can we cover all 7 edges with exactly 3 vertices?
1. To cover $(A, B)$ and $(B, C)$, vertex **$B$** is the optimal shared endpoint.  
   Choosing $B$ covers both $e_1 = (A, B)$ and $e_2 = (B, C)$.
2. To cover the remaining 5 edges:
   $$E_{\text{uncovered}} = \{(C, D), (C, E), (D, E), (D, F), (E, G)\}$$
   We have a budget of $3 - 1 = 2$ vertices remaining.
3. Notice that:
   - Edge $(D, F)$ requires either $D$ or $F$. If we pick $F$, $F$ covers *only* $(D, F)$, leaving 4 edges for 1 remaining vertex (impossible). Thus, we must select **$D$**.
   - Edge $(E, G)$ requires either $E$ or $G$. If we pick $G$, $G$ covers *only* $(E, G)$. Thus, we must select **$E$**.
4. Test candidate subset $C^* = \{B, D, E\}$ ($|C^*| = 3$):
   - $e_1 = (A, B)$: covered by $B \in C^*$
   - $e_2 = (B, C)$: covered by $B \in C^*$
   - $e_3 = (C, D)$: covered by $D \in C^*$
   - $e_4 = (C, E)$: covered by $E \in C^*$
   - $e_5 = (D, E)$: covered by $D, E \in C^*$
   - $e_6 = (D, F)$: covered by $D \in C^*$
   - $e_7 = (E, G)$: covered by $E \in C^*$

```text
========================================================================================================
                                     OPTIMAL VERTEX COVER C* = {B, D, E}
========================================================================================================

          (A)
           |
           | e_1 [covered by B]
           |
          (B)* <--- KEY COVERING VERTEX 1 (covers e_1, e_2)
           |
           | e_2 [covered by B]
           |
          (C)-----------------(D)*----------------(F)
            \                 / |  \               
             \               /  |   \ e_6 [covered by D]
              \             /   |    \             
           e_4 \       e_5 /    |e_3  (F)          
        [by E]  \   [by D,E]    |[by D]            
                 \       /      |                  
                  \     /       |                  
                   \   /        |                  
                    (E)*--------+                  
                     |
                     | e_7 [covered by E]
                     |
                    (G)

   Vertices in C*: {B, D, E}  (|C*| = 3)
   Unselected Independent Set: {A, C, F, G} (|S| = 4)
========================================================================================================
```

##### Phase 3: Optimality Certification
- Every edge in $E$ is covered by $\{B, D, E\}$.
- Since $|C^*| \ge 3$ and $|\{B, D, E\}| = 3$:
  $$C^* = \{B, D, E\} \quad \text{with } |C^*| = \mathbf{3}$$

---

### Step-Card 1.7: Empirical Approximation Ratio Calculation

#### 1. What are we doing?
Computing the empirical approximation ratio $\rho_{\text{actual}}$ for this execution trace.

#### 2. How do we execute the calculation?
$$\rho_{\text{actual}} = \frac{|C_{\text{approx}}|}{|C^*|}$$
Substituting our calculated cardinalities:
$$\rho_{\text{actual}} = \frac{6}{3} = \mathbf{2.0}$$

#### 3. Verification of Theoretical Bound:
$$\rho_{\text{actual}} \le \rho_{\text{theoretical}} \iff 2.0 \le 2.0 \quad (\mathbf{TRUE})$$
The returned cover meets the theoretical performance ceiling of $2.0$.

---

### Step-Card 1.8: Alternative Execution Trace (Order Sensitivity Analysis)

::: callout-intuition
**Algorithmic Insight: Arbitrary Choice Variance**  
Because the algorithm picks edges *arbitrarily*, different edge selection sequences can produce different vertex covers. However, **every** valid maximal matching will yield an approximation ratio $\le 2.0$.
:::

#### What if Iteration 2 picked edge $e_5 = (D, E)$ instead of $e_3 = (C, D)$?
Let us trace this alternative execution path:

1. **Iteration 1:** Select edge $e_1 = (A, B)$.
   - $C = \{A, B\}$.
   - $M = \{(A, B)\}$.
   - Incident edges $(A, B)$ and $(B, C)$ removed.
   - Remaining edges: $E' = \{(C, D), (C, E), (D, E), (D, F), (E, G)\}$.
2. **Iteration 2 (Alternative Choice):** Select edge $e_5 = (D, E)$.
   - Add both endpoints:
     $$C_{\text{alt}} = \{A, B\} \cup \{D, E\} = \{A, B, D, E\}$$
   - Add to matching:
     $$M_{\text{alt}} = \{(A, B), (D, E)\} \quad (|M_{\text{alt}}| = 2)$$
   - Purge all edges incident to $D$ or $E$:
     * $(C, D)$ contains $D \implies$ **REMOVE**
     * $(C, E)$ contains $E \implies$ **REMOVE**
     * $(D, E)$ contains $D, E \implies$ **REMOVE**
     * $(D, F)$ contains $D \implies$ **REMOVE**
     * $(E, G)$ contains $E \implies$ **REMOVE**
   - The remaining edge pool becomes:
     $$E' = \emptyset$$
3. **Termination:** The algorithm halts after only 2 iterations!
   - Alternative Cover: $C_{\text{alt}} = \{A, B, D, E\}$ with size $|C_{\text{alt}}| = 4$.
   - Ratio:
     $$\rho_{\text{alt}} = \frac{|C_{\text{alt}}|}{|C^*|} = \frac{4}{3} \approx \mathbf{1.333} \le 2.0$$

#### Takeaway:
Depending on the order of edge choices, `Approx-Vertex-Cover` on graph $G$ returns either a cover of size 4 ($\rho \approx 1.33$) or size 6 ($\rho = 2.0$). In both scenarios, the approximation ratio never exceeds $2.0$.

---

## 3. Level 2: Path Graph Tightness Example ($P_4$)

A bound is defined as **tight** if there exists an infinite family of problem instances for which the ratio $\frac{|C|}{|C^*|}$ asymptotically reaches or equals the theoretical bound. We now prove that the factor of 2 for `Approx-Vertex-Cover` is mathematically tight using a simple path graph $P_4$.

### Problem 2.1 Specification
Let $P_4 = (V, E)$ be a simple linear path graph with 4 vertices and 3 edges:
- **Vertex Set ($n = 4$):** $V = \{1, 2, 3, 4\}$
- **Edge Set ($m = 3$):** $E = \{(1, 2), (2, 3), (3, 4)\}$

```text
========================================================================================================
                                     PATH GRAPH TOPOLOGY P_4
========================================================================================================

          (1)-----------------(2)-----------------(3)-----------------(4)
                   e_1                  e_2                  e_3
========================================================================================================
```

---

### Step-Card 2.1: Algorithmic Execution on $P_4$

#### 1. What are we doing?
Tracing `Approx-Vertex-Cover` on path graph $P_4$ under an adversarial edge selection sequence.

#### 2. How do we execute the step mechanically?

##### Iteration 1: Selection of Edge $(1, 2)$
- Select edge:
  $$e^*_1 = (1, 2)$$
- Add endpoints to Cover:
  $$C = \{1, 2\}$$
- Add to Matching:
  $$M = \{(1, 2)\}$$
- Purge incident edges:
  * Edge $(1, 2)$ contains $1$ and $2 \implies$ **REMOVE**
  * Edge $(2, 3)$ contains $2 \implies$ **REMOVE**
- Remaining edge pool:
  $$E' = E \setminus \{(1, 2), (2, 3)\} = \{(3, 4)\}$$

##### Iteration 2: Selection of Edge $(3, 4)$
- Edge $(3, 4)$ is the only remaining edge in $E'$.
- Select edge:
  $$e^*_2 = (3, 4)$$
- Add endpoints to Cover:
  $$C = \{1, 2\} \cup \{3, 4\} = \{1, 2, 3, 4\}$$
- Add to Matching:
  $$M = \{(1, 2), (3, 4)\} \quad (|M| = 2)$$
- Purge incident edges:
  * Edge $(3, 4)$ contains $3$ and $4 \implies$ **REMOVE**
- Remaining edge pool:
  $$E' = \emptyset$$

##### Final Output on $P_4$:
- Approximate Cover:
  $$C_{\text{approx}} = \{1, 2, 3, 4\} = V$$
- Cardinality:
  $$|C_{\text{approx}}| = \mathbf{4}$$

---

### Step-Card 2.2: Determination of Optimal Vertex Cover for $P_4$

#### 1. Lower Bound via Matching:
The edges selected into matching $M$ are:
$$M = \{(1, 2), (3, 4)\}$$
Because $\{1, 2\} \cap \{3, 4\} = \emptyset$, these edges are vertex-disjoint. Any valid vertex cover must pick at least one endpoint from each edge:
$$|C^*| \ge |M| = 2$$

#### 2. Upper Bound via Feasible Inspection:
- Consider candidate subset:
  $$C^* = \{2, 3\}$$
- Audit all 3 edges against $C^*$:
  1. Edge $(1, 2)$: covered by $2 \in C^*$
  2. Edge $(2, 3)$: covered by $2, 3 \in C^*$
  3. Edge $(3, 4)$: covered by $3 \in C^*$
- All 3 edges are covered!
- Therefore, $C^* = \{2, 3\}$ is a valid vertex cover of size:
  $$|C^*| = \mathbf{2}$$

```text
========================================================================================================
                              P_4: ALGORITHM COVER VS. OPTIMAL COVER
========================================================================================================

   1. APPROXIMATION COVER C (Size = 4):
      [ (1)* ]=============== [ (2)* ]               [ (3)* ] =============== [ (4)* ]
              Matching Edge 1                                 Matching Edge 2
      (Algorithm selects ALL 4 vertices: {1, 2, 3, 4})

   2. OPTIMAL COVER C* (Size = 2):
        (1) ----------------- [ (2)* ] ============= [ (3)* ] ----------------- (4)
                                     Internal Edge
      (Optimal selects only the 2 internal vertices: {2, 3})
========================================================================================================
```

---

### Step-Card 2.3: Tightness Certification & Asymptotic Generalization

#### 1. Exact Tightness Ratio on $P_4$:
$$\rho = \frac{|C_{\text{approx}}|}{|C^*|} = \frac{4}{2} = \mathbf{2.0}$$
The approximation ratio hits the theoretical upper bound of $2.0$ exactly.

#### 2. Generalization to Path Graphs $P_{2k}$:
Consider a general path graph with an even number of vertices $n = 2k$:
$$P_{2k}: \quad 1 - 2 - 3 - 4 - \dots - (2k-1) - 2k$$
- Total vertices: $2k$.
- Total edges: $2k - 1$.
- If the algorithm selects all odd-positioned edges into the matching:
  $$M = \{(1, 2), (3, 4), (5, 6), \dots, (2k-1, 2k)\}$$
  The algorithm takes both endpoints of each matching edge:
  $$|C| = 2 \cdot |M| = 2k = n$$
- An optimal cover selects the alternate interior vertices:
  $$C^* = \{2, 4, 6, \dots, 2k-2\} \cup \{2k-1\} \implies |C^*| \approx k$$
- The ratio remains:
  $$\lim_{k \to \infty} \frac{|C|}{|C^*|} = \frac{2k}{k} = \mathbf{2.0}$$

#### 3. Generalization to Disjoint Edges ($k \cdot K_2$):
Consider a graph composed of $k$ completely disconnected edges:
$$G = \{(u_1, v_1), (u_2, v_2), \dots, (u_k, v_k)\}$$
- The algorithm selects all $k$ edges into the matching, resulting in:
  $$|C| = 2k$$
- The optimal cover picks exactly 1 vertex per edge (e.g., $\{u_1, u_2, \dots, u_k\}$), resulting in:
  $$|C^*| = k$$
- The ratio is exactly:
  $$\frac{|C|}{|C^*|} = \frac{2k}{k} = \mathbf{2.0}$$

**Definitive Conclusion:**  
The bound $\rho = 2$ for the Gavril-Yannakakis algorithm is **strictly tight** and cannot be lowered without changing the algorithm.

---

## 4. Algorithmic Pseudocode & Formal Verification Proof

### 4.1 Algorithmic Specification

```text
Algorithm ApproxVertexCover(G = (V, E))
// Input: An undirected, unweighted simple graph G = (V, E)
// Output: A vertex cover C ⊆ V such that |C| ≤ 2 * |C*|
begin
    C := ∅;                          // Initialize vertex cover to empty set
    M := ∅;                          // Initialize maximal matching to empty set
    E_prime := E;                    // Create working copy of edge set
    
    while (E_prime ≠ ∅) do
        // Step 1: Arbitrarily pick an edge e = (u, v) from E_prime
        select an arbitrary edge (u, v) ∈ E_prime;
        
        // Step 2: Record edge in matching and add both endpoints to cover
        M := M ∪ {(u, v)};
        C := C ∪ {u, v};
        
        // Step 3: Remove all edges incident to either u or v from E_prime
        for each edge (x, y) ∈ E_prime do
            if (x = u or x = v or y = u or y = v) then
                E_prime := E_prime \ {(x, y)};
            end if;
        end for;
    end while;
    
    return C;
end;
```

---

### 4.2 Formal Mathematical Proof of 2-Approximation

#### Theorem 4.1 (Approximation Bound of Gavril-Yannakakis)
*Algorithm `ApproxVertexCover` runs in deterministic polynomial time $\mathcal{O}(|V| + |E|)$ and returns a valid vertex cover $C$ satisfying $|C| \le 2 \cdot |C^*|$, where $C^*$ is an optimal minimum vertex cover.*

#### Complete Proof with Zero Logical Leaps:

##### Part 1: Proof of Validity (Covering Invariant)
1. Suppose for the sake of contradiction that the returned set $C$ is **not** a valid vertex cover.
2. Then there exists at least one edge $e = (x, y) \in E$ such that:
   $$x \notin C \quad \text{and} \quad y \notin C$$
3. Consider the termination condition of the algorithm:
   $$\text{The while-loop halts if and only if } E' = \emptyset$$
4. Edge $e = (x, y)$ initially belonged to $E'$. For $e$ to be eliminated from $E'$, one of two events must have occurred:
   - **Case A:** Edge $e$ was selected during Step 1. But Step 2 adds both endpoints of any selected edge to $C$, meaning $\{x, y\} \subseteq C$, contradicting the premise.
   - **Case B:** Edge $e$ was purged during Step 3 because it shared an endpoint with another edge $(u, v)$ selected in Step 1. In this case, either $x \in \{u, v\}$ or $y \in \{u, v\}$. But since $\{u, v\} \subseteq C$, at least one endpoint of $e$ was added to $C$, contradicting the premise.
5. Therefore, no edge in $E$ can have both endpoints outside $C$.
6. Thus, $C$ is a valid vertex cover.

##### Part 2: Proof of the Matching Invariant
1. Let $M$ be the sequence of edges selected in Step 1:
   $$M = \{e^*_1, e^*_2, \dots, e^*_k\}$$
2. In each iteration, when edge $e^*_i = (u, v)$ is selected, Step 3 removes **every** edge incident to $u$ or $v$ from $E'$.
3. Consequently, no edge subsequently chosen for $M$ can share a vertex with $(u, v)$.
4. Thus, all edges in $M$ are pairwise vertex-disjoint:
   $$\forall \; e_i, e_j \in M \quad (i \ne j \implies e_i \cap e_j = \emptyset)$$
5. By mathematical definition, $M$ is a valid **matching**.
6. Furthermore, because the loop terminates with $E' = \emptyset$, every edge in $E$ is incident to at least one edge in $M$. Thus, $M$ is a **maximal matching**.

##### Part 3: Proof of the Lower Bound ($|C^*| \ge |M|$)
1. Let $C^*$ be an arbitrary optimal minimum vertex cover of $G$.
2. By definition, $C^*$ must cover every edge in $E$.
3. Because $M \subseteq E$, $C^*$ must cover every edge in matching $M$.
4. Because $M$ is a matching, no two edges in $M$ share a vertex. A single vertex can cover **at most one edge** in $M$.
5. Therefore, to cover all $|M|$ completely independent edges, $C^*$ must contain at least one distinct vertex per matching edge:
   $$|C^*| \ge |M|$$

##### Part 4: Proof of the Upper Bound ($|C| = 2|M|$)
1. For each edge $(u, v) \in M$, the algorithm adds **both** endpoints $u$ and $v$ to $C$.
2. Since all edges in $M$ are pairwise vertex-disjoint, no vertex is added to $C$ more than once.
3. Therefore:
   $$|C| = 2 \cdot |M|$$

##### Part 5: Synthesizing the Approximation Ratio
1. Multiplying both sides of the lower-bound inequality $|M| \le |C^*|$ by 2:
   $$2 \cdot |M| \le 2 \cdot |C^*|$$
2. Substituting $|C| = 2|M|$ into the left-hand side:
   $$|C| \le 2 \cdot |C^*|$$
3. Dividing both sides by $|C^*|$:
   $$\frac{|C|}{|C^*|} \le 2.0$$
The algorithm is a guaranteed $2$-approximation. $\blacksquare$

---

### 4.3 Computational Complexity Analysis

1. **Adjacency Representation:** Store graph $G$ using adjacency lists alongside a boolean array `in_cover` of size $|V|$ initialized to `FALSE`.
2. **Edge Traversal:** We iterate through the edge list:
   - For each edge $e = (u, v)$:
     * Check if `in_cover[u] == FALSE` and `in_cover[v] == FALSE`.
     * If true, add $(u, v)$ to $M$, set `in_cover[u] = TRUE` and `in_cover[v] = TRUE`, and append $u$ and $v$ to $C$.
     * If false, at least one endpoint is already in the cover, so skip the edge.
3. **Runtime:**
   - Initializing the boolean array takes $\mathcal{O}(|V|)$ time.
   - Scanning the edge list evaluates each edge in $\mathcal{O}(1)$ time, taking $\mathcal{O}(|E|)$ time.
   - Total Time Complexity:
     $$\mathcal{T}(|V|, |E|) = \mathcal{O}(|V| + |E|)$$
   This runtime is linear in the size of the graph.
4. **Space Complexity:**
   - The boolean array and output list require $\mathcal{O}(|V|)$ auxiliary space.

---

### 4.4 Why the Greedy Degree Heuristic Fails

::: callout-exam
**KTU Examination Scoring Trap: The Degree-Greedy Fallacy**  
In KTU examinations, students often intuitively propose:  
*"Repeatedly pick the vertex with the highest remaining degree, add it to the cover, remove its incident edges, and repeat."*  
**Warning:** This greedy heuristic does **NOT** achieve a constant approximation ratio $\rho = 2$!
:::

#### Counterexample:
On bipartite graphs designed as projective planes or harmonic constructions (e.g., Johnson 1974, Chvátal 1979):
- The greedy degree-based heuristic achieves an approximation ratio of:
  $$\rho_{\text{greedy}} = \mathcal{O}(\ln |V|)$$
- As $|V| \to \infty$, the ratio $\ln |V|$ grows unbounded ($3, 4, 5, \dots$), whereas the maximal matching algorithm is strictly bounded by $\rho \le 2.0$.
- Therefore, the matching-based algorithm is theoretically superior to the greedy degree heuristic.

---

## 5. Master Reference & Graph Topology Comparison Matrix

```text
+======================================================================================================================+
|                                    MASTER TOPOLOGY APPROXIMATION MATRIX                                              |
+==================+======================+====================+======================+================================+
| Graph Topology   | Sample Instance      | Optimal Cover |C*| | Approx Cover Size |C| | Empirical Ratio (|C| / |C*|)   |
+==================+======================+====================+======================+================================+
| Path Graph       | $P_4$ (4 vertices,   | $2$ vertices       | $4$ vertices         | $4 / 2 = \mathbf{2.0}$         |
|                  | 3 edges)             | (internal nodes)   | (all vertices)       | (Strictly Tight)               |
+------------------+----------------------+--------------------+----------------------+--------------------------------+
| Disjoint Edges   | $k \cdot K_2$        | $k$ vertices       | $2k$ vertices        | $2k / k = \mathbf{2.0}$        |
|                  | (Matching of size k) | (1 per edge)       | (both endpoints)     | (Strictly Tight)               |
+------------------+----------------------+--------------------+----------------------+--------------------------------+
| Star Graph       | $K_{1, n-1}$         | $1$ vertex         | $2$ vertices         | $2 / 1 = \mathbf{2.0}$         |
|                  | (Central hub + leaves| (center hub)       | (hub + 1 leaf)       | (Worst-case on star)           |
+------------------+----------------------+--------------------+----------------------+--------------------------------+
| Complete Graph   | $K_n$                | $n - 1$ vertices   | $2 \lfloor n/2 \rfloor$ | $\approx 1.0$ (Asymptotic)  |
|                  | (Clique of size n)   |                    | vertices             | (Near Optimal)                 |
+------------------+----------------------+--------------------+----------------------+--------------------------------+
| Odd Cycle        | $C_5$ (Pentagon,     | $3$ vertices       | $4$ vertices         | $4 / 3 \approx \mathbf{1.33}$  |
|                  | 5 vertices, 5 edges) |                    | (2 matching edges)   |                                |
+------------------+----------------------+--------------------+----------------------+--------------------------------+
| Worklab Level 1  | 7 vertices,          | $3$ vertices       | Trace A: $6$ vertices| Trace A: $6 / 3 = \mathbf{2.0}$|
| Graph $G$        | 7 edges              | $\{B, D, E\}$      | Trace B: $4$ vertices| Trace B: $4 / 3 \approx 1.33$  |
+==================+======================+====================+======================+================================+
```

---

## 6. KTU Examination Scoring Blueprint (10-Mark Rubric)

When a question on the 2-approximation algorithm for Vertex Cover appears in KTU exams under course code **PCCST502 / CST306**, marks are allocated strictly according to the following criteria:

| Evaluation Phase | Expected Answer Components | Allocated Marks |
| :--- | :--- | :---: |
| **Phase 1: Algorithm Formulation** | Clear, syntactically correct pseudocode for `ApproxVertexCover` showing edge selection, cover set update ($C \cup \{u, v\}$), and incident edge removal. | **2 Marks** |
| **Phase 2: Step-by-Step Execution Trace** | Iteration-by-iteration trace on the provided problem graph showing chosen matching edges, remaining edge pool ($E'$), and updated cover $C$ at each step. | **3 Marks** |
| **Phase 3: Optimal Cover & Ratio Computation** | Correct determination of the true minimum vertex cover $C^*$, calculation of $|C^*|$, and division $\frac{|C|}{|C^*|}$ confirming $\le 2.0$. | **2 Marks** |
| **Phase 4: Formal Proof of Approximation Ratio** | Mathematical proof demonstrating: (1) $M$ is a matching, (2) $|C^*| \ge |M|$, (3) $|C| = 2|M|$, concluding $|C| \le 2|C^*|$. | **2 Marks** |
| **Phase 5: Tightness Example** | Presentation of a tightness counterexample (such as $P_4$ or $k \cdot K_2$) proving the ratio achieves exactly $2.0$. | **1 Mark** |
| **Total Marks** | | **10 Marks** |
