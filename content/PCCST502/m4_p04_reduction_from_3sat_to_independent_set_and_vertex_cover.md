# Module 4 - Problem Worklab 4: Step-by-Step Reduction from 3-SAT to Independent Set and Vertex Cover

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search & Computational Complexity Theory  
**Document Classification:** Publication-Grade Problem Worklab & Rigorous Reduction Protocol  

---

## 1. Executive Summary & Foundational Reduction Theory

The reduction from **Boolean 3-Satisfiability (3-SAT)** to **Vertex Cover (VC)** and **Independent Set (IS)** is one of Richard Karp's foundational 21 $\text{NP}$-complete reductions (1972). It demonstrates how logical constraints (Boolean truth assignments and clause satisfiability) are translated directly into topological graph structures (cliques, independent sets, and covering subsets).

```text
========================================================================================================
                          THE 3-SAT TO GRAPH COMPLEXITY REDUCTION PIPELINE
========================================================================================================

    3-CNF Boolean Formula ϕ
    (n variables, m clauses)
               |
               v   Polynomial-Time Gadget Transformation f(ϕ)
    Undirected Graph G = (V, E)
    Budget Parameter k = n + 2m
               |
               +----------------------------------+
               |                                  |
               v                                  v
    [ Vertex Cover in G ] <=== Gallai Duality ===> [ Independent Set in G ]
    k_VC = n + 2m = 8     (S_IS = V \ V_VC)       k_IS = |V| - k_VC = 13 - 8 = 5
```

### 1.1 The Mathematical Reduction Invariant
A reduction $f: \text{3-SAT} \to \text{VERTEX-COVER}$ maps a 3-CNF formula $\phi$ to a graph $G = (V, E)$ and an integer budget $k$ such that:
$$\phi \in L_{\text{3-SAT}} \iff \langle G, k \rangle \in L_{\text{VC}}$$

This equivalence requires satisfying two non-negotiable mathematical properties:
1. **Soundness ($\implies$):** If $\phi$ is satisfiable by truth assignment $\tau$, then there exists an explicit vertex subset $V' \subseteq V$ with $|V'| \le k$ that covers every edge in $E$.
2. **Completeness ($\impliedby$):** If $G$ contains a vertex cover $V'$ with $|V'| \le k$, then the vertices selected from the variable gadgets define a consistent, non-contradictory truth assignment $\tau$ that satisfies every clause in $\phi$.

::: callout-intuition
**Mental Model: Gadgets as Physical Logic Gates**  
- A **Variable Gadget** functions as an electrical toggle switch: choosing vertex $v_{x_i}$ forces $x_i = \text{TRUE}$, while choosing $v_{\bar{x}_i}$ forces $x_i = \text{FALSE}$. The connecting edge ensures you cannot leave the switch floating.
- A **Clause Gadget** functions as a 3-way demand circuit: a triangular room with 3 doors. To patrol all 3 corridors between the doors, a guard detachment must station guards at at least 2 doors. The 3rd un-guarded door can only be secure if the corresponding variable switch outside is already manned.
:::

---

## 2. Concrete Problem Specification

### Problem 1.1 Formulation
We are given a 3-CNF Boolean formula $\phi$ over $n = 2$ Boolean variables $X = \{x_1, x_2\}$ consisting of $m = 3$ clauses:
$$\phi = C_1 \land C_2 \land C_3$$

where the clauses are defined as:
$$C_1 = (x_1 \lor \bar{x}_2 \lor x_1)$$
$$C_2 = (\bar{x}_1 \lor x_2 \lor x_2)$$
$$C_3 = (\bar{x}_1 \lor \bar{x}_2 \lor \bar{x}_1)$$

*(Note: Literals may be repeated within clauses, which is valid under standard 3-CNF definitions where each clause contains exactly 3 literal slots).*

---

### 2.1 Exhaustive Truth-Table Analysis of Formula $\phi$
To establish the ground truth of the system before building the graph, we evaluate all $2^n = 2^2 = 4$ possible truth assignments:

| Assignment ($\tau$) | $x_1$ | $x_2$ | $\bar{x}_1$ | $\bar{x}_2$ | $C_1 = (x_1 \lor \bar{x}_2 \lor x_1)$ | $C_2 = (\bar{x}_1 \lor x_2 \lor x_2)$ | $C_3 = (\bar{x}_1 \lor \bar{x}_2 \lor \bar{x}_1)$ | $\phi = C_1 \land C_2 \land C_3$ | Satisfiability Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| $\tau_1$ | $\mathbf{0}$ | $\mathbf{0}$ | $\mathbf{1}$ | $\mathbf{1}$ | $(0 \lor 1 \lor 0) = \mathbf{1}$ | $(1 \lor 0 \lor 0) = \mathbf{1}$ | $(1 \lor 1 \lor 1) = \mathbf{1}$ | $1 \land 1 \land 1 = \mathbf{1}$ | **UNIQUE SATISFYING ASSIGNMENT ($\tau^*$)** |
| $\tau_2$ | $0$ | $1$ | $1$ | $0$ | $(0 \lor 0 \lor 0) = \mathbf{0}$ | $(1 \lor 1 \lor 1) = \mathbf{1}$ | $(1 \lor 0 \lor 1) = \mathbf{1}$ | $0 \land 1 \land 1 = \mathbf{0}$ | Unsatisfiable (Fails $C_1$) |
| $\tau_3$ | $1$ | $0$ | $0$ | $1$ | $(1 \lor 1 \lor 1) = \mathbf{1}$ | $(0 \lor 0 \lor 0) = \mathbf{0}$ | $(0 \lor 1 \lor 0) = \mathbf{1}$ | $1 \land 0 \land 1 = \mathbf{0}$ | Unsatisfiable (Fails $C_2$) |
| $\tau_4$ | $1$ | $1$ | $0$ | $0$ | $(1 \lor 0 \lor 1) = \mathbf{1}$ | $(0 \lor 1 \lor 1) = \mathbf{1}$ | $(0 \lor 0 \lor 0) = \mathbf{0}$ | $1 \land 1 \land 0 = \mathbf{0}$ | Unsatisfiable (Fails $C_3$) |

#### Analytical Ground Truth:
Formula $\phi$ is satisfiable **if and only if** $x_1 = 0$ ($\text{FALSE}$) and $x_2 = 0$ ($\text{FALSE}$). The unique satisfying assignment is:
$$\tau^* = (x_1 = 0, \; x_2 = 0)$$

::: callout-exam
**KTU Examination Scoring Trap: The Satisfiability Check**  
If an exam prompt suggests testing a candidate assignment like $(x_1 = 1, x_2 = 0)$, always evaluate it against all clauses first! As demonstrated in row $\tau_3$, $(x_1 = 1, x_2 = 0)$ produces $C_2 = (0 \lor 0 \lor 0) = 0$, making it an **unsatisfying assignment**. 
A correct reduction must cause an unsatisfying assignment to fail to produce a valid vertex cover of size $k$. We will explicitly trace both the satisfying assignment $\tau^*$ and the failing candidate $\tau_3$ to demonstrate soundness and completeness.
:::

---

## 3. Level 1: Step-by-Step Construction of the Vertex Cover Graph

---

### Step-Card 1.1: Constructing the Variable Gadgets

#### 1. What are we doing?
Constructing the vertex subgraphs and edges corresponding to each Boolean variable $x_i \in \{x_1, x_2\}$.

#### 2. Why are we starting here?
The truth assignment to the variables determines which literals are active. The variable gadgets form the foundational selection layer of the reduction graph.

#### 3. How do we execute the step mechanically?
For each of the $n = 2$ variables, we create a pair of vertices connected by a single undirected edge:

1. **Variable $x_1$ Gadget:**
   - Vertices: $v_{x_1}$ (representing literal $x_1$) and $v_{\bar{x}_1}$ (representing literal $\bar{x}_1$).
   - Edge: $e_{\text{var}, 1} = (v_{x_1}, v_{\bar{x}_1})$.
2. **Variable $x_2$ Gadget:**
   - Vertices: $v_{x_2}$ (representing literal $x_2$) and $v_{\bar{x}_2}$ (representing literal $\bar{x}_2$).
   - Edge: $e_{\text{var}, 2} = (v_{x_2}, v_{\bar{x}_2})$.

```text
========================================================================================================
                                     VARIABLE GADGET TOPOLOGY
========================================================================================================

          Variable x_1 Gadget                     Variable x_2 Gadget
          
               ( v_x1 )                                ( v_x2 )
                  |                                       |
                  |  e_var,1                              |  e_var,2
                  |                                       |
               ( v_¬x1 )                               ( v_¬x2 )

========================================================================================================
```

#### 4. Where did this formula / invariant originate?
From the edge-covering property of simple graphs:
- Edge $(v_{x_i}, v_{\bar{x}_i})$ has two endpoints.
- A vertex cover $V'$ must contain at least one endpoint of every edge. Therefore:
  $$|V' \cap \{v_{x_i}, v_{\bar{x}_i}\}| \ge 1 \quad \forall \; i \in \{1, \dots, n\}$$
- Across all $n$ variable gadgets, any valid vertex cover must select at least:
  $$\sum_{i=1}^n 1 = n \text{ vertices}$$
- To stay strictly within the budget $k = n + 2m$, the vertex cover must select **exactly 1 vertex** from each variable gadget.

#### 5. What changed from the previous step?
We have generated:
- $2n = 2(2) = 4$ vertices: $V_{\text{var}} = \{v_{x_1}, v_{\bar{x}_1}, v_{x_2}, v_{\bar{x}_2}\}$.
- $n = 2$ edges: $E_{\text{var}} = \{(v_{x_1}, v_{\bar{x}_1}), \; (v_{x_2}, v_{\bar{x}_2})\}$.

---

### Step-Card 1.2: Constructing the Clause Gadgets

#### 1. What are we doing?
Constructing the vertex subgraphs and internal edges corresponding to each clause $C_j \in \{C_1, C_2, C_3\}$.

#### 2. Why this choice?
Each clause must be structurally represented such that it enforces an exact local vertex requirement and requires satisfaction by at least one literal.

#### 3. How do we execute the step mechanically?
For each of the $m = 3$ clauses, we create a complete graph $K_3$ (a triangle) consisting of 3 vertices, each representing one of the literal slots in that clause:

1. **Clause $C_1 = (x_1 \lor \bar{x}_2 \lor x_1)$ Gadget:**
   - Vertices: $u_{1, 1}$ (representing slot 1: $x_1$), $u_{1, 2}$ (representing slot 2: $\bar{x}_2$), $u_{1, 3}$ (representing slot 3: $x_1$).
   - Edges forming triangle $T_1$:
     $$E_{C_1} = \{(u_{1, 1}, u_{1, 2}), \; (u_{1, 2}, u_{1, 3}), \; (u_{1, 3}, u_{1, 1})\}$$
2. **Clause $C_2 = (\bar{x}_1 \lor x_2 \lor x_2)$ Gadget:**
   - Vertices: $u_{2, 1}$ (representing slot 1: $\bar{x}_1$), $u_{2, 2}$ (representing slot 2: $x_2$), $u_{2, 3}$ (representing slot 3: $x_2$).
   - Edges forming triangle $T_2$:
     $$E_{C_2} = \{(u_{2, 1}, u_{2, 2}), \; (u_{2, 2}, u_{2, 3}), \; (u_{2, 3}, u_{2, 1})\}$$
3. **Clause $C_3 = (\bar{x}_1 \lor \bar{x}_2 \lor \bar{x}_1)$ Gadget:**
   - Vertices: $u_{3, 1}$ (representing slot 1: $\bar{x}_1$), $u_{3, 2}$ (representing slot 2: $\bar{x}_2$), $u_{3, 3}$ (representing slot 3: $\bar{x}_1$).
   - Edges forming triangle $T_3$:
     $$E_{C_3} = \{(u_{3, 1}, u_{3, 2}), \; (u_{3, 2}, u_{3, 3}), \; (u_{3, 3}, u_{3, 1})\}$$

```text
========================================================================================================
                                      CLAUSE GADGET TOPOLOGY
========================================================================================================

       Clause C_1 Triangle             Clause C_2 Triangle             Clause C_3 Triangle
       
             ( u_1,1 )                       ( u_2,1 )                       ( u_3,1 )
              /     \                         /     \                         /     \
             /       \                       /       \                       /       \
     ( u_1,2 )-------( u_1,3 )       ( u_2,2 )-------( u_2,3 )       ( u_3,2 )-------( u_3,3 )
      [x1, ¬x2, x1]                   [¬x1, x2, x2]                   [¬x1, ¬x2, ¬x1]

========================================================================================================
```

#### 4. Where did this formula / invariant originate?
From the covering mechanics of complete subgraphs ($K_p$):
- In any complete graph $K_p$, a vertex cover must select at least $p - 1$ vertices.
- For a triangle $K_3$ ($p = 3$):
  - If you select $0$ vertices: all 3 edges are uncovered.
  - If you select $1$ vertex: it covers only the 2 edges incident to it, leaving the opposite edge completely uncovered.
  - If you select $2$ vertices: all 3 edges are covered.
- Therefore, for each clause triangle $T_j$:
  $$|V' \cap \{u_{j, 1}, u_{j, 2}, u_{j, 3}\}| \ge 2 \quad \forall \; j \in \{1, \dots, m\}$$
- Across all $m$ clause triangles, any valid vertex cover must select at least:
  $$\sum_{j=1}^m 2 = 2m \text{ vertices}$$
- To satisfy budget $k = n + 2m$, the vertex cover must select **exactly 2 vertices** from each clause triangle. Exactly $1$ vertex per triangle must remain unselected.

#### 5. What changed from the previous step?
We have added:
- $3m = 3(3) = 9$ clause vertices:
  $$V_{\text{clause}} = \{u_{1,1}, u_{1,2}, u_{1,3}, \; u_{2,1}, u_{2,2}, u_{2,3}, \; u_{3,1}, u_{3,2}, u_{3,3}\}$$
- $3m = 3(3) = 9$ clause triangle edges: $E_{\text{clause}} = E_{C_1} \cup E_{C_2} \cup E_{C_3}$.

---

### Step-Card 1.3: Connecting Gadgets via Consistency (Communication) Edges

#### 1. What are we doing?
Adding consistency edges between each clause literal vertex and its corresponding variable gadget vertex.

#### 2. Why are we doing this?
To couple clause satisfaction to variable truth assignments. If a literal in a clause is TRUE, the variable gadget covers the communication edge, allowing the clause triangle to omit that literal's vertex.

#### 3. How do we execute the step mechanically?
For every clause $C_j$ and for each of its 3 positions $k \in \{1, 2, 3\}$, we add an undirected edge connecting clause vertex $u_{j, k}$ to the variable gadget vertex representing that exact literal:

1. **Edges from Clause $C_1 = (x_1 \lor \bar{x}_2 \lor x_1)$:**
   - Slot 1 ($x_1$): Add edge $e_{\text{comm}, 1} = (u_{1, 1}, v_{x_1})$
   - Slot 2 ($\bar{x}_2$): Add edge $e_{\text{comm}, 2} = (u_{1, 2}, v_{\bar{x}_2})$
   - Slot 3 ($x_1$): Add edge $e_{\text{comm}, 3} = (u_{1, 3}, v_{x_1})$
2. **Edges from Clause $C_2 = (\bar{x}_1 \lor x_2 \lor x_2)$:**
   - Slot 1 ($\bar{x}_1$): Add edge $e_{\text{comm}, 4} = (u_{2, 1}, v_{\bar{x}_1})$
   - Slot 2 ($x_2$): Add edge $e_{\text{comm}, 5} = (u_{2, 2}, v_{x_2})$
   - Slot 3 ($x_2$): Add edge $e_{\text{comm}, 6} = (u_{2, 3}, v_{x_2})$
3. **Edges from Clause $C_3 = (\bar{x}_1 \lor \bar{x}_2 \lor \bar{x}_1)$:**
   - Slot 1 ($\bar{x}_1$): Add edge $e_{\text{comm}, 7} = (u_{3, 1}, v_{\bar{x}_1})$
   - Slot 2 ($\bar{x}_2$): Add edge $e_{\text{comm}, 8} = (u_{3, 2}, v_{\bar{x}_2})$
   - Slot 3 ($\bar{x}_1$): Add edge $e_{\text{comm}, 9} = (u_{3, 3}, v_{\bar{x}_1})$

```text
========================================================================================================
                                COMMUNICATION INTERFACE EDGES
========================================================================================================

       Clause Slot Vertex (u_j,k) <-----------------------------> Variable Vertex (v_literal)
       
             u_1,1  (Literal x1)   =============================>  v_x1
             u_1,2  (Literal ¬x2)  =============================>  v_¬x2
             u_1,3  (Literal x1)   =============================>  v_x1
             
             u_2,1  (Literal ¬x1)  =============================>  v_¬x1
             u_2,2  (Literal x2)   =============================>  v_x2
             u_2,3  (Literal x2)   =============================>  v_x2
             
             u_3,1  (Literal ¬x1)  =============================>  v_¬x1
             u_3,2  (Literal ¬x2)  =============================>  v_¬x2
             u_3,3  (Literal ¬x1)  =============================>  v_¬x1

========================================================================================================
```

#### 4. Where did this formula originate?
From the Boolean consistency requirement:
- Since budget constraints permit selecting only 2 vertices from clause triangle $\{u_{j, 1}, u_{j, 2}, u_{j, 3}\}$, exactly **one vertex $u_{j, k^*}$ must be left unselected**.
- The communication edge $(u_{j, k^*}, v_{l_{j, k^*}})$ must still be covered.
- Because $u_{j, k^*} \notin V'$, the other endpoint **must** be selected:
  $$v_{l_{j, k^*}} \in V'$$
- Selecting $v_{l_{j, k^*}} \in V'$ corresponds to setting literal $l_{j, k^*} = \text{TRUE}$.
- Thus, the clause gadget can only be covered within budget if the unselected vertex corresponds to a literal that evaluates to TRUE under the assignment.

#### 5. What changed from the previous step?
We have added exactly $3m = 3(3) = 9$ communication edges:
$$E_{\text{comm}} = \{e_{\text{comm}, 1}, e_{\text{comm}, 2}, \dots, e_{\text{comm}, 9}\}$$

---

### Step-Card 1.4: Calculation of Graph Parameters and Budget $k$

#### 1. What are we doing?
Computing the total vertex count $|V|$, edge count $|E|$, and target budget $k$ for the reduction instance $\langle G, k \rangle$.

#### 2. Why are we doing this?
A decision problem requires precise parameter bounds. The budget $k$ determines the boundary between accepting and rejecting instances.

#### 3. How do we execute the step mechanically?

##### Calculation 1: Total Vertices ($|V|$)
$$|V| = |V_{\text{var}}| + |V_{\text{clause}}| = 2n + 3m$$
Substituting $n = 2$ and $m = 3$:
$$|V| = 2(2) + 3(3) = 4 + 9 = \mathbf{13 \text{ vertices}}$$

##### Calculation 2: Total Edges ($|E|$)
$$|E| = |E_{\text{var}}| + |E_{\text{clause}}| + |E_{\text{comm}}| = n + 3m + 3m = n + 6m$$
Substituting $n = 2$ and $m = 3$:
$$|E| = 2 + 3(3) + 3(3) = 2 + 9 + 9 = \mathbf{20 \text{ edges}}$$

##### Calculation 3: Target Vertex Cover Budget ($k$)
$$k = n + 2m$$
Substituting $n = 2$ and $m = 3$:
$$k = 2 + 2(3) = 2 + 6 = \mathbf{8}$$

#### 4. Where did this formula originate?
From Karp's Theorem (1972):
- Each of the $n$ variable gadgets requires at least 1 vertex: subtotal $n$.
- Each of the $m$ clause triangles requires at least 2 vertices: subtotal $2m$.
- Total required cardinality: $k = n + 2m$.

#### 5. What changed from the previous step?
The graph instance $\langle G = (V, E), k = 8 \rangle$ is completely specified:
- $|V| = 13$
- $|E| = 20$
- $k = 8$

---

## 4. Complete ASCII Architecture & Graph Topology

```text
========================================================================================================================
                                     FULL REDUCTION GRAPH G = (V, E)
========================================================================================================================

          VARIABLE GADGETS (n = 2)
          ------------------------
                    ( v_x1 )                             ( v_x2 )
                       |                                    |
                       | e_var,1                            | e_var,2
                       |                                    |
                    ( v_¬x1 )                            ( v_¬x2 )
                    /   |   \                            /      \
                   /    |    \                          /        \
                  /     |     \                        /          \
   +-------------+      |      +--------+             /            +-----------------------+
   |                    |               |            /                                     |
   |                    |               |           |                                      |
   |   COMMUNICATION EDGES (3m = 9)     |           |                                      |
   |                    |               |           |                                      |
   |  (e_comm,1)        |               |           | (e_comm,5)                           |
   |  +-----------------+---------------+-----------+---+                                  |
   |  |                 |               |           |   |                                  |
   |  |   (e_comm,3)    | (e_comm,4)    |           |   |                                  |
   |  |   +-------------+---+           |           |   | (e_comm,6)                       |
   |  |   |                 |           |           |   | +--+                             |
   |  |   |                 | (e_comm,7)| (e_comm,9)|   | |  |                             |
   |  |   |                 | +---------+---+       |   | |  |                             |
   |  |   |                 | |             |       |   | |  |                             |
   v  v   v                 v v             v       |   | |  |                             |
 ( u_1,1 ) ( u_1,3 )      ( u_2,1 )       ( u_3,1 ) ( u_3,3 )|                             |
     \     /                  \               \     /        |                             |
      \   /                    \               \   /         |                             |
    ( u_1,2 )             ( u_2,2 )-----------( u_2,3 )      |                             |
        |                                                    |                             |
        +--------------------------------(e_comm,2)----------+                             |
                                                             |                             |
                                        ( u_3,2 )------------+ (e_comm,8)                  |
                                                                                           |
   -----------------------------------------------------------------------------------------
   CLAUSE GADGETS (m = 3 Triangles):
     - Triangle C1: { u_1,1 , u_1,2 , u_1,3 }  representing ( x1  ∨ ¬x2 ∨  x1 )
     - Triangle C2: { u_2,1 , u_2,2 , u_2,3 }  representing (¬x1  ∨  x2 ∨  x2 )
     - Triangle C3: { u_3,1 , u_3,2 , u_3,3 }  representing (¬x1  ∨ ¬x2 ∨ ¬x1 )
========================================================================================================================
```

---

## 5. Dual Verification: Satisfying vs. Unsatisfying Assignments

---

### Step-Card 2.1: Verification of Satisfying Assignment $\tau^* = (x_1 = 0, x_2 = 0)$

#### 1. What are we doing?
Constructing the candidate vertex cover $V'$ of size $k = 8$ from the satisfying truth assignment $\tau^* = (x_1 = 0, x_2 = 0)$ and proving that all 20 edges are covered.

#### 2. Why are we starting here?
To verify **Soundness**: a true $\text{YES}$-instance of 3-SAT must produce a valid vertex cover of size $\le k$.

#### 3. How do we execute the step mechanically?

##### Phase 1: Vertex Selection from Variable Gadgets ($n = 2$ vertices)
Rule: If $\tau(x_i) = 1$, select $v_{x_i}$; if $\tau(x_i) = 0$, select $v_{\bar{x}_i}$.
- For variable $x_1$: $\tau^*(x_1) = 0 \implies$ Select **$v_{\bar{x}_1}$**.
- For variable $x_2$: $\tau^*(x_2) = 0 \implies$ Select **$v_{\bar{x}_2}$**.
- Variable selections:
  $$V'_{\text{var}} = \{v_{\bar{x}_1}, v_{\bar{x}_2}\} \quad (|V'_{\text{var}}| = 2)$$

##### Phase 2: Vertex Selection from Clause Gadgets ($2m = 6$ vertices)
Rule: In each clause $C_j$, identify at least one literal that evaluates to TRUE under $\tau^*$. Leave that literal's vertex **out** of $V'$, and select the remaining **two** vertices of the triangle into $V'$:

1. **Clause $C_1 = (x_1 \lor \bar{x}_2 \lor x_1)$:**
   - Under $\tau^*$: $x_1 = 0$ ($\text{False}$), $\bar{x}_2 = 1$ ($\text{True}$), $x_1 = 0$ ($\text{False}$).
   - Slot 2 ($\bar{x}_2$) is TRUE.
   - Leave vertex $u_{1, 2}$ **OUT**.
   - Select vertices **$u_{1, 1}$** and **$u_{1, 3}$** into $V'$.
2. **Clause $C_2 = (\bar{x}_1 \lor x_2 \lor x_2)$:**
   - Under $\tau^*$: $\bar{x}_1 = 1$ ($\text{True}$), $x_2 = 0$ ($\text{False}$), $x_2 = 0$ ($\text{False}$).
   - Slot 1 ($\bar{x}_1$) is TRUE.
   - Leave vertex $u_{2, 1}$ **OUT**.
   - Select vertices **$u_{2, 2}$** and **$u_{2, 3}$** into $V'$.
3. **Clause $C_3 = (\bar{x}_1 \lor \bar{x}_2 \lor \bar{x}_1)$:**
   - Under $\tau^*$: $\bar{x}_1 = 1$ ($\text{True}$), $\bar{x}_2 = 1$ ($\text{True}$), $\bar{x}_1 = 1$ ($\text{True}$).
   - All three literals are TRUE. We can arbitrarily designate Slot 1 ($\bar{x}_1$) as the satisfying witness.
   - Leave vertex $u_{3, 1}$ **OUT**.
   - Select vertices **$u_{3, 2}$** and **$u_{3, 3}$** into $V'$.

##### Total Candidate Vertex Cover ($V'$):
$$V' = \{v_{\bar{x}_1}, v_{\bar{x}_2}, \; u_{1, 1}, u_{1, 3}, \; u_{2, 2}, u_{2, 3}, \; u_{3, 2}, u_{3, 3}\}$$
$$\text{Total Size: } |V'| = 2 + 2 + 2 + 2 = 8 \le k(8) \quad \implies \quad \text{\textbf{BUDGET CONSTRAINT SATISFIED!}}$$

---

### Step-Card 2.2: Comprehensive 20-Edge Coverage Audit Table

We evaluate every edge $e = (u, v) \in E$ against $V'$ to check whether $(u \in V') \lor (v \in V')$:

| Edge Index | Edge Class | Edge $e = (u, v)$ | Endpoint $u \in V'$? | Endpoint $v \in V'$? | Boolean Evaluation ($u \in V' \lor v \in V'$) | Coverage Status | Covering Witness Vertex |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Variable | $(v_{x_1}, v_{\bar{x}_1})$ | $v_{x_1} \notin V'$ | $v_{\bar{x}_1} \in V'$ | $\text{False} \lor \text{True} = \text{True}$ | **COVERED** | $v_{\bar{x}_1}$ |
| **2** | Variable | $(v_{x_2}, v_{\bar{x}_2})$ | $v_{x_2} \notin V'$ | $v_{\bar{x}_2} \in V'$ | $\text{False} \lor \text{True} = \text{True}$ | **COVERED** | $v_{\bar{x}_2}$ |
| **3** | Clause $C_1$ | $(u_{1, 1}, u_{1, 2})$ | $u_{1, 1} \in V'$ | $u_{1, 2} \notin V'$ | $\text{True} \lor \text{False} = \text{True}$ | **COVERED** | $u_{1, 1}$ |
| **4** | Clause $C_1$ | $(u_{1, 2}, u_{1, 3})$ | $u_{1, 2} \notin V'$ | $u_{1, 3} \in V'$ | $\text{False} \lor \text{True} = \text{True}$ | **COVERED** | $u_{1, 3}$ |
| **5** | Clause $C_1$ | $(u_{1, 3}, u_{1, 1})$ | $u_{1, 3} \in V'$ | $u_{1, 1} \in V'$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $u_{1, 1}, u_{1, 3}$ |
| **6** | Clause $C_2$ | $(u_{2, 1}, u_{2, 2})$ | $u_{2, 1} \notin V'$ | $u_{2, 2} \in V'$ | $\text{False} \lor \text{True} = \text{True}$ | **COVERED** | $u_{2, 2}$ |
| **7** | Clause $C_2$ | $(u_{2, 2}, u_{2, 3})$ | $u_{2, 2} \in V'$ | $u_{2, 3} \in V'$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $u_{2, 2}, u_{2, 3}$ |
| **8** | Clause $C_2$ | $(u_{2, 3}, u_{2, 1})$ | $u_{2, 3} \in V'$ | $u_{2, 1} \notin V'$ | $\text{True} \lor \text{False} = \text{True}$ | **COVERED** | $u_{2, 3}$ |
| **9** | Clause $C_3$ | $(u_{3, 1}, u_{3, 2})$ | $u_{3, 1} \notin V'$ | $u_{3, 2} \in V'$ | $\text{False} \lor \text{True} = \text{True}$ | **COVERED** | $u_{3, 2}$ |
| **10** | Clause $C_3$ | $(u_{3, 2}, u_{3, 3})$ | $u_{3, 2} \in V'$ | $u_{3, 3} \in V'$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $u_{3, 2}, u_{3, 3}$ |
| **11** | Clause $C_3$ | $(u_{3, 3}, u_{3, 1})$ | $u_{3, 3} \in V'$ | $u_{3, 1} \notin V'$ | $\text{True} \lor \text{False} = \text{True}$ | **COVERED** | $u_{3, 3}$ |
| **12** | Comm $C_1$ | $(u_{1, 1}, v_{x_1})$ | $u_{1, 1} \in V'$ | $v_{x_1} \notin V'$ | $\text{True} \lor \text{False} = \text{True}$ | **COVERED** | $u_{1, 1}$ |
| **13** | Comm $C_1$ | $(u_{1, 2}, v_{\bar{x}_2})$ | $u_{1, 2} \notin V'$ | $v_{\bar{x}_2} \in V'$ | $\text{False} \lor \text{True} = \text{True}$ | **COVERED** | $v_{\bar{x}_2}$ |
| **14** | Comm $C_1$ | $(u_{1, 3}, v_{x_1})$ | $u_{1, 3} \in V'$ | $v_{x_1} \notin V'$ | $\text{True} \lor \text{False} = \text{True}$ | **COVERED** | $u_{1, 3}$ |
| **15** | Comm $C_2$ | $(u_{2, 1}, v_{\bar{x}_1})$ | $u_{2, 1} \notin V'$ | $v_{\bar{x}_1} \in V'$ | $\text{False} \lor \text{True} = \text{True}$ | **COVERED** | $v_{\bar{x}_1}$ |
| **16** | Comm $C_2$ | $(u_{2, 2}, v_{x_2})$ | $u_{2, 2} \in V'$ | $v_{x_2} \notin V'$ | $\text{True} \lor \text{False} = \text{True}$ | **COVERED** | $u_{2, 2}$ |
| **17** | Comm $C_2$ | $(u_{2, 3}, v_{x_2})$ | $u_{2, 3} \in V'$ | $v_{x_2} \notin V'$ | $\text{True} \lor \text{False} = \text{True}$ | **COVERED** | $u_{2, 3}$ |
| **18** | Comm $C_3$ | $(u_{3, 1}, v_{\bar{x}_1})$ | $u_{3, 1} \notin V'$ | $v_{\bar{x}_1} \in V'$ | $\text{False} \lor \text{True} = \text{True}$ | **COVERED** | $v_{\bar{x}_1}$ |
| **19** | Comm $C_3$ | $(u_{3, 2}, v_{\bar{x}_2})$ | $u_{3, 2} \in V'$ | $v_{\bar{x}_2} \in V'$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $u_{3, 2}, v_{\bar{x}_2}$ |
| **20** | Comm $C_3$ | $(u_{3, 3}, v_{\bar{x}_1})$ | $u_{3, 3} \in V'$ | $v_{\bar{x}_1} \in V'$ | $\text{True} \lor \text{True} = \text{True}$ | **COVERED** | $u_{3, 3}, v_{\bar{x}_1}$ |

#### 4. Definitive Conclusion on Satisfying Assignment:
- All 20 edges in $E$ are covered by at least one vertex in $V'$.
- The candidate set size is exactly $|V'| = 8 = k$.
- Thus, $V'$ is a certified, valid Vertex Cover of size $8$.
$$V(\langle G, k=8 \rangle, V') = \text{\textbf{ACCEPT}}$$

---

### Step-Card 2.3: Diagnostic Trace of Unsatisfying Assignment $\tau_3 = (x_1 = 1, x_2 = 0)$

#### 1. What are we doing?
Tracing the failure mode when attempting to construct a vertex cover of size $k = 8$ using the unsatisfying truth assignment $\tau_3 = (x_1 = 1, x_2 = 0)$.

#### 2. Why are we doing this?
To verify **Completeness**: if an assignment does not satisfy $\phi$, any candidate set derived from it must fail to cover the graph within budget $k = 8$.

#### 3. How do we execute the step mechanically?

##### Phase 1: Variable Gadget Selection ($n = 2$ vertices)
Under $\tau_3$: $x_1 = 1 \implies$ select $v_{x_1}$; $x_2 = 0 \implies$ select $v_{\bar{x}_2}$.
$$V'_{\text{var}} = \{v_{x_1}, v_{\bar{x}_2}\}$$

##### Phase 2: Clause Gadget Allocation
Recall that the budget allows only **2 vertices** per clause triangle:
1. **Clause $C_1 = (x_1 \lor \bar{x}_2 \lor x_1)$:**  
   $x_1 = 1$ is TRUE. Leave $u_{1, 1}$ OUT; select $\{u_{1, 2}, u_{1, 3}\}$. (Valid).
2. **Clause $C_3 = (\bar{x}_1 \lor \bar{x}_2 \lor \bar{x}_1)$:**  
   $\bar{x}_2 = 1$ is TRUE. Leave $u_{3, 2}$ OUT; select $\{u_{3, 1}, u_{3, 3}\}$. (Valid).
3. **Clause $C_2 = (\bar{x}_1 \lor x_2 \lor x_2)$ (The False Clause):**  
   Under $\tau_3 = (x_1 = 1, x_2 = 0)$:
   $$\bar{x}_1 = 0 \quad (\text{False}), \quad x_2 = 0 \quad (\text{False}), \quad x_2 = 0 \quad (\text{False})$$
   **Every literal in $C_2$ is FALSE.**  
   Because the triangle $\{u_{2, 1}, u_{2, 2}, u_{2, 3}\}$ has only 2 vertices in the budget, exactly **one vertex must be left unselected**.
   - **Case A: Suppose we leave $u_{2, 1}$ OUT.**  
     Then $u_{2, 1} \notin V'$. Examine consistency edge 15:
     $$e_{\text{comm}, 4} = (u_{2, 1}, v_{\bar{x}_1})$$
     Endpoint $u_{2, 1} \notin V'$.  
     Endpoint $v_{\bar{x}_1} \notin V'$ (since $\tau_3(x_1) = 1$, we selected $v_{x_1}$, not $v_{\bar{x}_1}$).  
     $$\text{Both endpoints are absent from } V' \implies \mathbf{Edge } (u_{2, 1}, v_{\bar{x}_1}) \mathbf{ IS UNCOVERED!}$$
   - **Case B: Suppose we leave $u_{2, 2}$ OUT.**  
     Then $u_{2, 2} \notin V'$. Examine consistency edge 16:
     $$e_{\text{comm}, 5} = (u_{2, 2}, v_{x_2})$$
     Endpoint $u_{2, 2} \notin V'$.  
     Endpoint $v_{x_2} \notin V'$ (since $\tau_3(x_2) = 0$, we selected $v_{\bar{x}_2}$, not $v_{x_2}$).  
     $$\text{Both endpoints are absent from } V' \implies \mathbf{Edge } (u_{2, 2}, v_{x_2}) \mathbf{ IS UNCOVERED!}$$
   - **Case C: Suppose we leave $u_{2, 3}$ OUT.**  
     Similarly, consistency edge 17 $(u_{2, 3}, v_{x_2})$ is left **UNCOVERED!**

#### 4. The Inevitable Trade-Off:
To cover the remaining edge, the verifier would need to select a 3rd vertex from triangle $C_2$ (or an additional vertex from a variable gadget), which requires a budget of:
$$k' \ge 9 > 8$$
Because the budget is strictly capped at $k = 8$, no valid vertex cover can be formed from an unsatisfying assignment.

---

## 6. Level 2: Duality & Independent Set Derivation

The constructed graph $G$ simultaneously yields an instance of the **Independent Set** problem through Gallai's Duality Theorem.

### 6.1 Gallai's Set Complement Duality

#### Theorem 6.1 (T. Gallai, 1959)
*In any undirected graph $G = (V, E)$, a subset $V' \subseteq V$ is a vertex cover if and only if its complement $S = V \setminus V'$ is an independent set.*

$$\alpha(G) + \tau(G) = |V|$$
where $\alpha(G)$ is the maximum independent set size, and $\tau(G)$ is the minimum vertex cover size.

---

### Step-Card 3.1: Deriving the Independent Set from $V'$

#### 1. What are we doing?
Constructing the certified Independent Set $S_{\text{IS}}$ directly from the valid Vertex Cover $V'$.

#### 2. Why this choice?
By Gallai's Theorem, taking the set difference $V \setminus V'$ yields an independent set in linear time $\mathcal{O}(|V|)$ without additional search.

#### 3. How do we execute the step mechanically?
- The total vertex set is:
  $$V = \{v_{x_1}, v_{\bar{x}_1}, v_{x_2}, v_{\bar{x}_2}, \; u_{1,1}, u_{1,2}, u_{1,3}, \; u_{2,1}, u_{2,2}, u_{2,3}, \; u_{3,1}, u_{3,2}, u_{3,3}\}$$
  $$|V| = 13$$
- The valid Vertex Cover is:
  $$V' = \{v_{\bar{x}_1}, v_{\bar{x}_2}, \; u_{1, 1}, u_{1, 3}, \; u_{2, 2}, u_{2, 3}, \; u_{3, 2}, u_{3, 3}\}$$
  $$|V'| = 8$$
- Compute the set difference $S_{\text{IS}} = V \setminus V'$:
  $$S_{\text{IS}} = \{v_{x_1}, v_{x_2}, \; u_{1, 2}, \; u_{2, 1}, \; u_{3, 1}\}$$
- Compute the target size bound:
  $$k_{\text{IS}} = |V| - k_{\text{VC}} = 13 - 8 = \mathbf{5}$$

```text
========================================================================================================
                                GALLAI PARTITION OF VERTICES (|V| = 13)
========================================================================================================

   [ Vertex Cover V' (Size = 8) ]               [ Independent Set S_IS (Size = 5) ]
   ------------------------------               -----------------------------------
   Variable:  { v_¬x1, v_¬x2 }                  Variable:  { v_x1, v_x2 }
   Clause C1: { u_1,1, u_1,3 }                  Clause C1: { u_1,2 }
   Clause C2: { u_2,2, u_2,3 }                  Clause C2: { u_2,1 }
   Clause C3: { u_3,2, u_3,3 }                  Clause C3: { u_3,1 }

========================================================================================================
```

---

### Step-Card 3.2: Pairwise Independence Verification

We check all $\binom{5}{2} = 10$ pairs of vertices in $S_{\text{IS}} = \{v_{x_1}, v_{x_2}, u_{1, 2}, u_{2, 1}, u_{3, 1}\}$ to verify that no edge connects any pair:

| Pair Index | Vertex $a \in S_{\text{IS}}$ | Vertex $b \in S_{\text{IS}}$ | Edge $(a, b) \in E$? | Physical Reason for Non-Adjacency | Independence Status |
| :---: | :---: | :---: | :---: | :--- | :---: |
| **1** | $v_{x_1}$ | $v_{x_2}$ | **NO** | Variable gadgets share no cross-variable edges | **INDEPENDENT** |
| **2** | $v_{x_1}$ | $u_{1, 2}$ | **NO** | $u_{1, 2}$ represents $\bar{x}_2$; connects only to $v_{\bar{x}_2}$ | **INDEPENDENT** |
| **3** | $v_{x_1}$ | $u_{2, 1}$ | **NO** | $u_{2, 1}$ represents $\bar{x}_1$; connects only to $v_{\bar{x}_1}$ | **INDEPENDENT** |
| **4** | $v_{x_1}$ | $u_{3, 1}$ | **NO** | $u_{3, 1}$ represents $\bar{x}_1$; connects only to $v_{\bar{x}_1}$ | **INDEPENDENT** |
| **5** | $v_{x_2}$ | $u_{1, 2}$ | **NO** | $u_{1, 2}$ represents $\bar{x}_2$; connects only to $v_{\bar{x}_2}$ | **INDEPENDENT** |
| **6** | $v_{x_2}$ | $u_{2, 1}$ | **NO** | $u_{2, 1}$ represents $\bar{x}_1$; connects only to $v_{\bar{x}_1}$ | **INDEPENDENT** |
| **7** | $v_{x_2}$ | $u_{3, 1}$ | **NO** | $u_{3, 1}$ represents $\bar{x}_1$; connects only to $v_{\bar{x}_1}$ | **INDEPENDENT** |
| **8** | $u_{1, 2}$ | $u_{2, 1}$ | **NO** | Reside in completely different clause triangles | **INDEPENDENT** |
| **9** | $u_{1, 2}$ | $u_{3, 1}$ | **NO** | Reside in completely different clause triangles | **INDEPENDENT** |
| **10** | $u_{2, 1}$ | $u_{3, 1}$ | **NO** | Reside in completely different clause triangles | **INDEPENDENT** |

#### Definitive Conclusion on Independent Set:
- All 10 pairwise comparisons confirm non-adjacency:
  $$\forall \; a, b \in S_{\text{IS}} \quad (a \ne b \implies (a, b) \notin E)$$
- The set cardinality is $|S_{\text{IS}}| = 5 \ge k_{\text{IS}}(5)$.
- $S_{\text{IS}}$ is a certified Independent Set in graph $G$.

---

### 6.2 Comparison: Gallai's Duality vs. Direct 3-SAT to Independent Set Reduction

Students must distinguish between two standard ways of reducing 3-SAT to Independent Set:

| Attribute | Method 1: Gallai Duality via $G_{\text{VC}}$ | Method 2: Direct 3-SAT to IS Reduction |
| :--- | :--- | :--- |
| **Target Graph** | Graph $G$ constructed with variable edges, clause triangles, and consistency edges. | Graph $G'$ containing **only** clause triangles and conflict edges between complementary literals. |
| **Vertex Count** | $|V| = 2n + 3m$ ($13$ vertices). | $|V| = 3m$ ($9$ vertices, no variable gadgets). |
| **Target Budget $k$** | $k_{\text{IS}} = |V| - k_{\text{VC}} = (2n + 3m) - (n + 2m) = \mathbf{n + m} = 5$. | $k_{\text{IS}} = \mathbf{m} = 3$ (select exactly 1 true literal per clause). |
| **Significance** | Proves the equivalence of Vertex Cover and Independent Set on the same graph structure. | Directly embeds the choice of 1 true literal per clause into an independent set. |

---

## 7. Master Reduction Reference Matrix

```text
+======================================================================================================================+
|                                    GADGET DECOMPOSITION REFERENCE MATRIX                                             |
+=====================+==========================+=============================+=======================================+
| Structural Layer    | Combinatorial Objects    | Formal Graph Entity         | Sizing Formula / Value                |
+=====================+==========================+=============================+=======================================+
| Variables           | $n = 2$ ($x_1, x_2$)     | 2 Disjoint Edges ($K_2$)    | Vertices: $2n = 4$                    |
|                     |                          |                             | Edges: $n = 2$                        |
+---------------------+--------------------------+-----------------------------+---------------------------------------+
| Clauses             | $m = 3$ ($C_1, C_2, C_3$)| 3 Disjoint Triangles ($K_3$)| Vertices: $3m = 9$                    |
|                     |                          |                             | Edges: $3m = 9$                       |
+---------------------+--------------------------+-----------------------------+---------------------------------------+
| Communication Layer | Literal-Variable Binding | Cross-cluster Bipartite     | Edges: $3m = 9$                       |
|                     |                          | Incidence Edges             |                                       |
+---------------------+--------------------------+-----------------------------+---------------------------------------+
| Total System Graph  | Complete Graph $G$       | $G = (V, E)$                | $|V| = 2n + 3m = 13$                  |
|                     |                          |                             | $|E| = n + 6m = 20$                   |
+---------------------+--------------------------+-----------------------------+---------------------------------------+
| Vertex Cover Target | Covering Subset Bound    | $V' \subseteq V$            | $k_{\text{VC}} = n + 2m = 8$          |
+---------------------+--------------------------+-----------------------------+---------------------------------------+
| Independent Set     | Non-adjacent Subset      | $S \subseteq V$             | $k_{\text{IS}} = |V| - k = n + m = 5$ |
+=====================+==========================+=============================+=======================================+
```

---

## 8. KTU Examination Scoring Blueprint (10-Mark Rubric)

When a question on gadget reductions appears in KTU exams under course code **PCCST502 / CST306**, marks are allocated strictly according to the following criteria:

| Evaluation Phase | Expected Answer Components | Allocated Marks |
| :--- | :--- | :---: |
| **Phase 1: Gadget Construction Specification** | Clear definition of variable gadgets ($K_2$, edge $(v_{x_i}, v_{\bar{x}_i})$) with proof that $\ge 1$ vertex is required; clause gadgets ($K_3$ triangles) with proof that $\ge 2$ vertices are required; definition of consistency edges. | **2 Marks** |
| **Phase 2: Formal Parameter Derivation** | Line-by-line calculation showing $|V| = 2n + 3m = 13$, $|E| = n + 6m = 20$, and the target budget $k = n + 2m = 8$. | **2 Marks** |
| **Phase 3: Graph Topology Diagram** | Labeled ASCII schematic or clear structural drawing depicting variable pairs, clause triangles, and the 9 communication edges. | **2 Marks** |
| **Phase 4: Truth Assignment & Cover Verification** | Truth-table evaluation of $\phi$; selection of the 8 vertices corresponding to satisfying assignment $\tau^* = (0, 0)$; and an explicit audit showing that all variable, clause, and communication edges are covered. | **3 Marks** |
| **Phase 5: Duality & Independent Set Derivation** | Application of Gallai's Theorem ($S = V \setminus V'$) to derive the 5-vertex Independent Set with pairwise independence verification. | **1 Mark** |
| **Total Marks** | | **10 Marks** |
