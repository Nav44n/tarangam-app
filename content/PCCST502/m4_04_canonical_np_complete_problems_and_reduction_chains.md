# Module 4.4: Canonical NP-Complete Problems and Reduction Chains

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search & Computational Complexity  
**Document Classification:** Publication-Grade Theoretical Lecture Note & Mathematical Foundation  

---

## 1. Executive Overview: Karp's Web of Reductions

In 1971, Stephen Cook and Leonid Levin proved that the Boolean Satisfiability problem ($\text{SAT}$) is $\text{NP}$-Complete from first principles. However, proving that thousands of natural problems across graph theory, combinatorial optimization, operations research, and algebra are also $\text{NP}$-Complete required a systemic methodology.

In 1972, Richard M. Karp published the landmark paper *"Reducibility Among Combinatorial Problems"*, proving that 21 foundational combinatorial problems are $\text{NP}$-Complete. Karp showed that once a single problem (like $\text{SAT}$) is proven $\text{NP}$-Complete, any new problem $Q$ can be certified $\text{NP}$-Complete simply by demonstrating a polynomial-time reduction from an already-established $\text{NP}$-Complete problem:

$$Q_{\text{known}} \le_p Q_{\text{target}}$$

By transitivity of polynomial-time many-one reductions (Theorem 5.3, Module 4.3), if every language in $\text{NP}$ reduces to $Q_{\text{known}}$, and $Q_{\text{known}} \le_p Q_{\text{target}}$, then every language in $\text{NP}$ reduces to $Q_{\text{target}}$.

```text
================================================================================
                    THE CLASSICAL KARP REDUCTION PIPELINE
================================================================================

                           [ Turing Machine Computation ]
                                         |
                                         v  (Cook-Levin Theorem)
                                     [  SAT  ]
                                         |
                                         v
                                     [ 3-SAT ]
                                         |
                       +-----------------+-----------------+
                       |                                   |
                       v                                   v
                  [ CLIQUE ]                         [ SUBSET-SUM ]
                       |                                   |
                       v                                   v
             [ INDEPENDENT-SET ]                    [ 0/1 KNAPSACK ]
                       |                                   |
                       v                                   v
                [ VERTEX-COVER ]                      [ PARTITION ]
                       |
                       +-----------------+
                       |                 |
                       v                 v
             [ HAMILTONIAN-CYCLE ] [ GRAPH-COLORING ]
                       |
                       v
                [ TSP-DECISION ]
```

::: callout-intuition
**Mental Model: The Universal Translation Machine**  
Think of polynomial-time reductions as writing a lossless "compiler" or "adapter". If you have a universal program that can solve target problem $B$, and you can translate any instance of difficult problem $A$ into an equivalent instance of $B$ in polynomial time, then a solver for $B$ immediately gives you a solver for $A$. Therefore, $B$ cannot be computationally easier than $A$.
:::

---

## 2. Formal Mathematical Definitions of Canonical Problems

Before constructing formal reduction proofs, we must establish unambiguous, set-theoretic mathematical definitions for each canonical decision problem over finite alphabets.

### 2.1 Boolean 3-Satisfiability (3-SAT)
- **Instance:** A Boolean formula $\phi$ in **Conjunctive Normal Form (CNF)** over a finite set of $n$ Boolean variables $X = \{x_1, x_2, \dots, x_n\}$, consisting of $m$ clauses:
  $$\phi = C_1 \land C_2 \land \dots \land C_m$$
  where each clause $C_j$ contains **exactly 3 distinct literals** joined by disjunctions:
  $$C_j = (l_{j, 1} \lor l_{j, 2} \lor l_{j, 3}) \quad \text{with } l_{j, k} \in \{x_1, \bar{x}_1, x_2, \bar{x}_2, \dots, x_n, \bar{x}_n\}$$
- **Question:** Does there exist a truth assignment $\tau: X \to \{0, 1\}$ such that $\phi(\tau) = 1$ (i.e., every clause $C_j$ evaluates to TRUE)?
- **Language Formalization:**
  $$L_{\text{3-SAT}} = \{\langle \phi \rangle \mid \phi \text{ is a 3-CNF formula that is satisfiable}\}$$

---

### 2.2 The Clique Problem (CLIQUE)
- **Instance:** An undirected, unweighted simple graph $G = (V, E)$ and a target integer threshold $k \in \mathbb{N}$ such that $1 \le k \le |V|$.
- **Question:** Does $G$ contain a **clique** of size at least $k$? That is, does there exist a vertex subset $V' \subseteq V$ with $|V'| \ge k$ such that every pair of distinct vertices in $V'$ is connected by an edge:
  $$\forall \; u, v \in V' \quad (u \ne v \implies (u, v) \in E)$$
- **Language Formalization:**
  $$L_{\text{CLIQUE}} = \{\langle G, k \rangle \mid G \text{ contains a complete subgraph of size } \ge k\}$$

---

### 2.3 The Independent Set Problem (INDEPENDENT-SET)
- **Instance:** An undirected, unweighted simple graph $G = (V, E)$ and a target integer threshold $k \in \mathbb{N}$ such that $1 \le k \le |V|$.
- **Question:** Does $G$ contain an **independent set** of size at least $k$? That is, does there exist a vertex subset $S \subseteq V$ with $|S| \ge k$ such that no two vertices in $S$ are joined by an edge:
  $$\forall \; u, v \in S \quad ((u, v) \notin E)$$
- **Language Formalization:**
  $$L_{\text{IS}} = \{\langle G, k \rangle \mid G \text{ contains an independent set of size } \ge k\}$$

---

### 2.4 The Vertex Cover Problem (VERTEX-COVER)
- **Instance:** An undirected, unweighted simple graph $G = (V, E)$ and a target integer budget $k \in \mathbb{N}$ such that $1 \le k \le |V|$.
- **Question:** Does $G$ contain a **vertex cover** of size at most $k$? That is, does there exist a subset $V' \subseteq V$ with $|V'| \le k$ such that every edge in $E$ has at least one endpoint in $V'$:
  $$\forall \; (u, v) \in E \quad (u \in V' \lor v \in V')$$
- **Language Formalization:**
  $$L_{\text{VC}} = \{\langle G, k \rangle \mid G \text{ contains a vertex cover of size } \le k\}$$

---

### 2.5 The Subset Sum Problem (SUBSET-SUM)
- **Instance:** A finite multiset of positive integers $S = \{s_1, s_2, \dots, s_n\} \subset \mathbb{N}$ and a positive integer target capacity $T \in \mathbb{N}$.
- **Question:** Does there exist a sub-multiset $S' \subseteq S$ whose elements aggregate exactly to target $T$:
  $$\sum_{s_i \in S'} s_i = T$$
- **Language Formalization:**
  $$L_{\text{SS}} = \{\langle S, T \rangle \mid \exists \; S' \subseteq S \text{ such that } \sum_{x \in S'} x = T\}$$

---

### 2.6 The 0/1 Knapsack Decision Problem (KNAPSACK-DEC)
- **Instance:** A collection of $n$ items where each item $i$ has an integer weight $w_i \in \mathbb{N}$ and an integer profit value $v_i \in \mathbb{N}$, a maximum weight capacity $W \in \mathbb{N}$, and a minimum target profit threshold $P \in \mathbb{N}$.
- **Question:** Does there exist a binary selection vector $X = (x_1, x_2, \dots, x_n) \in \{0, 1\}^n$ that satisfies both capacity and profit constraints:
  $$\sum_{i=1}^n w_i x_i \le W \quad \text{and} \quad \sum_{i=1}^n v_i x_i \ge P$$
- **Language Formalization:**
  $$L_{\text{KP}} = \{\langle W, P, w, v \rangle \mid \exists \; X \in \{0, 1\}^n \text{ with } \sum w_i x_i \le W \text{ and } \sum v_i x_i \ge P\}$$

---

## 3. The Graph Trio Duality: CLIQUE, INDEPENDENT-SET, and VERTEX-COVER

A core pedagogical insight of graph complexity theory is that **CLIQUE**, **INDEPENDENT-SET**, and **VERTEX-COVER** are mathematically equivalent manifestations of the same structural problem viewed through complementary lenses.

```text
               Graph Complementation (G <---> Ḡ)
       [ CLIQUE ] <===========================> [ INDEPENDENT-SET ]
                                                        ^
                                                        |
                                          Complement Set Duality
                                          (S <---> V \ S)
                                                        |
                                                        v
                                                 [ VERTEX-COVER ]
```

---

### 3.1 Formal Definition of Graph Complement
Let $G = (V, E)$ be an undirected simple graph. The **graph complement** of $G$, denoted by $\overline{G} = (V, \overline{E})$, is defined on the exact same vertex set $V$, with edge set:
$$\overline{E} = \{(u, v) \mid u, v \in V, \; u \ne v, \; (u, v) \notin E\}$$

The union of edge sets satisfies $E \cup \overline{E} = \{\{u, v\} \mid u \ne v \in V\}$, and $E \cap \overline{E} = \emptyset$. Total edges sum to:
$$|E| + |\overline{E}| = \binom{|V|}{2} = \frac{|V|(|V| - 1)}{2}$$

---

### 3.2 Theorem 3.1: Reduction from CLIQUE to INDEPENDENT-SET ($\text{CLIQUE} \le_p \text{INDEP-SET}$)

#### Formal Theorem Statement
*A subset $S \subseteq V$ is a clique in $G = (V, E)$ if and only if $S$ is an independent set in the complement graph $\overline{G} = (V, \overline{E})$.*

#### Mathematical Proof (Bi-Directional):

**Direction 1 ($\implies$): If $S$ is a clique in $G$, then $S$ is an independent set in $\overline{G}$.**
1. Let $S \subseteq V$ be a clique in graph $G$.
2. By the mathematical definition of a clique, every pair of distinct vertices $u, v \in S$ has an edge in $G$:
   $$\forall \; u, v \in S \quad (u \ne v \implies (u, v) \in E)$$
3. By the mathematical definition of the complement edge set $\overline{E}$:
   $$(u, v) \in E \iff (u, v) \notin \overline{E}$$
4. Therefore:
   $$\forall \; u, v \in S \quad (u \ne v \implies (u, v) \notin \overline{E})$$
5. By the definition of an independent set, a vertex subset in which no two distinct vertices share an edge is an independent set.
6. Thus, $S$ is an independent set in $\overline{G}$.

**Direction 2 ($\impliedby$): If $S$ is an independent set in $\overline{G}$, then $S$ is a clique in $G$.**
1. Let $S \subseteq V$ be an independent set in complement graph $\overline{G} = (V, \overline{E})$.
2. By the mathematical definition of an independent set:
   $$\forall \; u, v \in S \quad (u \ne v \implies (u, v) \notin \overline{E})$$
3. By complement construction, if $(u, v) \notin \overline{E}$, it must be that:
   $$(u, v) \in E$$
4. Therefore:
   $$\forall \; u, v \in S \quad (u \ne v \implies (u, v) \in E)$$
5. Every pair of distinct vertices in $S$ shares an edge in $G$.
6. Thus, $S$ is a clique in $G$. $\blacksquare$

#### Complexity of the Reduction Function:
Given instance $\langle G, k \rangle$ of CLIQUE:
1. Construct complement graph $\overline{G} = (V, \overline{E})$:
   - Initialize an $n \times n$ adjacency matrix with zeros.
   - For all $\binom{n}{2}$ pairs $(u, v)$, set $\overline{A}[u, v] = 1 - A[u, v]$.
   - This takes exactly $\mathcal{O}(|V|^2)$ operations.
2. Output the instance $\langle \overline{G}, k \rangle$ for INDEPENDENT-SET.
3. Total reduction time is $\mathcal{O}(|V|^2)$, which is strictly polynomial.  
Hence, $\text{CLIQUE} \le_p \text{INDEP-SET}$.

---

### 3.3 Theorem 3.2: Gallai's Duality Theorem ($\text{INDEP-SET} \le_p \text{VERTEX-COVER}$)

#### Formal Theorem Statement (T. Gallai, 1959)
*Let $G = (V, E)$ be an undirected graph, and let $S \subseteq V$.  
$S$ is an independent set in $G$ if and only if its set-theoretic complement $V \setminus S$ is a vertex cover in $G$.*

```text
                             Set of all Vertices: V
      +-----------------------------------+-----------------------------------+
      |        Independent Set S          |         Vertex Cover V \ S        |
      |   (No edges between any u, v ∈ S) |   (Hits at least one endpoint of  |
      |                                   |    EVERY edge in the graph)       |
      +-----------------------------------+-----------------------------------+
                                            <------- Size: |V| - |S| --------->
```

#### Mathematical Proof (Bi-Directional):

**Direction 1 ($\implies$): If $S$ is an independent set in $G$, then $V \setminus S$ is a vertex cover in $G$.**
1. Let $S \subseteq V$ be an independent set in $G$.
2. Suppose for the sake of contradiction that $V \setminus S$ is **not** a vertex cover in $G$.
3. By definition of a vertex cover, if $V \setminus S$ fails to cover all edges, there must exist at least one edge $e = (u, v) \in E$ such that neither endpoint belongs to $V \setminus S$:
   $$u \notin (V \setminus S) \quad \text{and} \quad v \notin (V \setminus S)$$
4. By elementary set theory, for any element $x \in V$:
   $$x \notin (V \setminus S) \implies x \in S$$
5. Therefore:
   $$u \in S \quad \text{and} \quad v \in S$$
6. But since $e = (u, v) \in E$, this means two vertices in $S$ are joined by an edge in $E$.
7. This directly contradicts the premise that $S$ is an independent set.
8. Therefore, no such edge can exist; $V \setminus S$ must cover every edge in $E$.
9. Thus, $V \setminus S$ is a vertex cover in $G$.

**Direction 2 ($\impliedby$): If $V \setminus S$ is a vertex cover in $G$, then $S$ is an independent set in $G$.**
1. Let $V \setminus S$ be a vertex cover in $G$.
2. Suppose for the sake of contradiction that $S$ is **not** an independent set in $G$.
3. By definition of an independent set, if $S$ is not independent, there must exist at least two vertices $u, v \in S$ with $u \ne v$ such that:
   $$(u, v) \in E$$
4. Since $V \setminus S$ is a vertex cover, it must cover edge $(u, v)$, which requires:
   $$u \in (V \setminus S) \quad \text{or} \quad v \in (V \setminus S)$$
5. However, by set definition:
   $$u \in S \implies u \notin (V \setminus S)$$
   $$v \in S \implies v \notin (V \setminus S)$$
6. Therefore, neither $u$ nor $v$ belongs to $V \setminus S$, meaning edge $(u, v)$ is not covered by $V \setminus S$.
7. This directly contradicts the premise that $V \setminus S$ is a vertex cover.
8. Therefore, no such edge can exist between vertices in $S$.
9. Thus, $S$ is an independent set in $G$. $\blacksquare$

#### Corollary 3.3 (Gallai's Identity)
*For any graph $G = (V, E)$ without isolated vertices, let $\alpha(G)$ denote the maximum independent set size, and let $\tau(G)$ denote the minimum vertex cover size. Then:*
$$\alpha(G) + \tau(G) = |V|$$

#### The Reduction Function:
Given instance $\langle G, k \rangle$ of INDEPENDENT-SET:
1. Keep the graph $G = (V, E)$ unchanged.
2. Set the target vertex cover budget:
   $$k' = |V| - k$$
3. Equivalence:
   $$G \text{ has an independent set of size } \ge k \iff G \text{ has a vertex cover of size } \le |V| - k$$
4. Time Complexity: Subtracting $k$ from $|V|$ takes $\mathcal{O}(1)$ time. The graph is passed directly in $\mathcal{O}(|V| + |E|)$ time.
5. Thus, $\text{INDEP-SET} \le_p \text{VERTEX-COVER}$.

---

### 3.4 Concrete Visual Walkthrough: The Graph Trio

Consider graph $G = (V, E)$ on $|V| = 5$ vertices:
$$V = \{1, 2, 3, 4, 5\}$$
$$E = \{(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)\}$$

```text
       Original Graph G                       Complement Graph Ḡ
       
          (1)-------(2)                           (1)       (2)
            \       /                              : \     / :
             \     /                               :  \   /  :
              \   /                                :   \ /   :
               (3)                                 :   (3)   :
                |                                  :         :
               (4)                                (4)-------(5)
                |                                  [Edges missing in G]
               (5)
```

#### Step-by-Step Numerical Verification:
1. **In Original Graph $G$:**
   - **Clique of size $k = 3$:** The triangle $S = \{1, 2, 3\}$. Every pair has an edge: $(1, 2), (1, 3), (2, 3) \in E$.
2. **In Complement Graph $\overline{G}$:**
   - Edges in $\overline{E}$: Pairs not connected in $G$:
     $$\overline{E} = \{(1, 4), (1, 5), (2, 4), (2, 5), (3, 5)\}$$
   - The set $S = \{1, 2, 3\}$ has **zero** edges between any pair in $\overline{E}$.
   - Thus, $S = \{1, 2, 3\}$ is an **Independent Set** in $\overline{G}$ of size $3$.
3. **Vertex Cover in $G$ using Duality:**
   - Maximum Independent Set in $G$: $S_{\text{IS}} = \{1, 4\}$ or $\{2, 4\}$ or $\{1, 5\}$ or $\{2, 5\}$.  
     Let $S_{\text{IS}} = \{1, 4, \dots\}$? Test size 2: $\{1, 5\}$ has no edge. $S_{\text{IS}} = \{2, 5\}$ has no edge. Size $= 2$.
   - By Gallai's Identity:
     $$\tau(G) = |V| - \alpha(G) = 5 - 2 = 3$$
   - A minimum Vertex Cover of size 3 is $V' = V \setminus \{2, 5\} = \{1, 3, 4\}$.
   - Edge verification for $V' = \{1, 3, 4\}$:
     * $(1, 2)$: covered by $1 \in V'$
     * $(1, 3)$: covered by $1, 3 \in V'$
     * $(2, 3)$: covered by $3 \in V'$
     * $(3, 4)$: covered by $3, 4 \in V'$
     * $(4, 5)$: covered by $4 \in V'$
   - Every single edge is covered!

---

## 4. Formal Reduction: 3-SAT to VERTEX-COVER

We now prove that **Vertex Cover is $\text{NP}$-Complete** by establishing a polynomial-time reduction directly from **3-SAT**:

$$\text{3-SAT} \le_p \text{VERTEX-COVER}$$

---

### 4.1 Step 1: Membership in NP ($\text{VERTEX-COVER} \in \text{NP}$)

#### 1. What are we doing?
Proving that positive instances of Vertex Cover can be verified deterministically in polynomial time.

#### 2. Why are we starting here?
By Definition 6.2 (Module 4.3), an $\text{NP}$-Completeness proof requires proving both membership in $\text{NP}$ and $\text{NP}$-Hardness.

#### 3. How do we execute the step mechanically?
1. **Certificate ($y$):** A subset of vertices $V' \subseteq V$.
2. **Deterministic Polynomial Verifier Algorithm $V(\langle G, k \rangle, V')$:**
   - **Check 1 (Cardinality Bound):** Count the number of vertices in $V'$. If $|V'| > k$, output $\text{REJECT}$.
   - **Check 2 (Edge Coverage):** For each edge $e = (u, v) \in E$:
     * Check whether $(u \in V')$ OR $(v \in V')$.
     * If neither $u$ nor $v$ is in $V'$, output $\text{REJECT}$.
   - If all $|E|$ edges satisfy the condition, output $\text{ACCEPT}$.
3. **Runtime Analysis:**
   - Checking cardinality takes $\mathcal{O}(|V|)$ steps.
   - Checking all edges takes $\mathcal{O}(|E|)$ lookups using a hash set or boolean array for $V'$, with $\mathcal{O}(1)$ time per lookup.
   - Total verifier running time: $\mathcal{O}(|V| + |E|)$, which is strictly linear and polynomial in input size.
4. **Conclusion:** $\text{VERTEX-COVER} \in \text{NP}$.

---

### 4.2 Step 2: Source Problem Selection
We select $Q' = \text{3-SAT}$, proven $\text{NP}$-Complete via the Cook-Levin reduction chain ($\text{Circuit-SAT} \le_p \text{SAT} \le_p \text{3-SAT}$).

---

### 4.3 Step 3: Gadget Construction Architecture ($f: \text{3-SAT} \to \text{VERTEX-COVER}$)

Let $\phi$ be an arbitrary 3-CNF formula with:
- $n$ Boolean variables: $X = \{x_1, x_2, \dots, x_n\}$
- $m$ Clauses: $C = \{C_1, C_2, \dots, C_m\}$, where $C_j = (l_{j, 1} \lor l_{j, 2} \lor l_{j, 3})$

We describe an algorithmic function $f$ that transforms $\phi$ into an undirected graph $G = (V, E)$ and integer budget $k$.

#### 1. Variable Gadgets:
For each variable $x_i$ ($i \in \{1, 2, \dots, n\}$):
- Create two vertices labeled with the positive and negated literals:
  $$v_{x_i} \quad \text{and} \quad v_{\bar{x}_i}$$
- Add an edge between them:
  $$e_i = (v_{x_i}, v_{\bar{x}_i})$$
- *Structural Invariant:* To cover edge $e_i$, any valid vertex cover must select **at least one** vertex from $\{v_{x_i}, v_{\bar{x}_i}\}$. Selecting exactly 1 vertex corresponds to a consistent truth assignment:
  $$\text{Selecting } v_{x_i} \iff \text{Assigning } x_i = 1$$
  $$\text{Selecting } v_{\bar{x}_i} \iff \text{Assigning } x_i = 0$$

```text
                 Variable Gadget (for variable x_i)
                 
                          ( v_xi )
                             |
                             |  Edge e_i
                             |
                          ( v_¬xi )
```

#### 2. Clause Gadgets:
For each clause $C_j = (l_{j, 1} \lor l_{j, 2} \lor l_{j, 3})$ ($j \in \{1, 2, \dots, m\}$):
- Create a **triangle** (complete graph $K_3$) consisting of 3 vertices, each representing one of the literal occurrences in clause $C_j$:
  $$u_{j, 1}, \quad u_{j, 2}, \quad u_{j, 3}$$
- Add 3 internal edges connecting the triangle:
  $$E_{\text{clause}, j} = \{(u_{j, 1}, u_{j, 2}), \; (u_{j, 2}, u_{j, 3}), \; (u_{j, 3}, u_{j, 1})\}$$
- *Structural Invariant:* A triangle $K_3$ cannot be covered by 1 vertex because a single vertex covers at most 2 edges of the triangle, leaving the 3rd edge uncovered. Therefore, any valid vertex cover must select **at least 2 vertices** from each clause triangle.

```text
                 Clause Gadget (for clause C_j)
                 
                          ( u_j,1 )
                           /     \
                          /       \
                         /         \
                    ( u_j,2 )-----( u_j,3 )
```

#### 3. Communication / Consistency Edges:
We connect the clause triangles to the variable gadgets to enforce logical satisfaction:
- For each clause $C_j$ and for each position $k \in \{1, 2, 3\}$:
  * Literal $l_{j, k}$ in clause $C_j$ corresponds to some variable literal $x_i$ or $\bar{x}_i$.
  * Add an undirected edge connecting clause vertex $u_{j, k}$ to the matching variable gadget vertex:
    $$(u_{j, k}, \; v_{l_{j, k}})$$
  * There are exactly $3$ communication edges per clause, giving $3m$ total communication edges.

```text
             Variable Gadgets                  Clause Gadget C_j
             
          ( v_x1 )     ( v_¬x2 )                   ( u_j,1 )
             \            /                         /     \
              \          /                         /       \
               \        /                         /         \
                \      /                     ( u_j,2 )-----( u_j,3 )
                 \    +-------------------------+              |
                  \                                            |
                   +-------------------------------------------+
```

#### 4. The Exact Budget Specification:
We define the target vertex cover size $k$ as:
$$k = n + 2m$$
where:
- $n$: exactly 1 vertex chosen per variable gadget.
- $2m$: exactly 2 vertices chosen per clause triangle.

---

### 4.4 Graph Size and Reduction Runtime Analysis

Let us calculate the exact combinatorial parameters of the constructed graph $G = (V, E)$:

1. **Vertex Count ($|V|$):**
   - From $n$ variable gadgets: $2n$ vertices.
   - From $m$ clause gadgets: $3m$ vertices.
   - Total vertices:
     $$|V| = 2n + 3m$$

2. **Edge Count ($|E|$):**
   - Variable gadget edges: $n$ edges.
   - Clause triangle edges: $3m$ edges.
   - Communication edges: $3m$ edges.
   - Total edges:
     $$|E| = n + 3m + 3m = n + 6m$$

3. **Time Complexity of Reduction:**
   - Generating $2n + 3m$ vertices takes $\mathcal{O}(n + m)$ operations.
   - Inserting $n + 6m$ edges into an adjacency list takes $\mathcal{O}(n + m)$ operations.
   - Calculating integer $k = n + 2m$ takes $\mathcal{O}(1)$ operations.
   - Total transformation runtime is $\mathcal{O}(n + m)$, which is strictly linear in the size of the 3-CNF formula.

---

### 4.5 Concrete 5W1H Instance Walkthrough

To eliminate any ambiguity, we trace the reduction on a concrete 3-CNF formula with $n = 3$ variables and $m = 2$ clauses:
$$\phi = C_1 \land C_2 = (x_1 \lor x_2 \lor x_3) \land (\bar{x}_1 \lor \bar{x}_2 \lor x_3)$$

#### Parameter Calculation:
- Number of variables: $n = 3$
- Number of clauses: $m = 2$
- Target vertex cover budget:
  $$k = n + 2m = 3 + 2(2) = 3 + 4 = 7$$
- Total vertices:
  $$|V| = 2(3) + 3(2) = 6 + 6 = 12$$
- Total edges:
  $$|E| = 3 + 6(2) = 3 + 12 = 15$$

#### Graph Inventory:
- **Vertices (12 total):**
  - Variable vertices: $\{v_{x_1}, v_{\bar{x}_1}, v_{x_2}, v_{\bar{x}_2}, v_{x_3}, v_{\bar{x}_3}\}$
  - Clause 1 triangle: $\{u_{1, 1}, u_{1, 2}, u_{1, 3}\}$ (representing literals $x_1, x_2, x_3$)
  - Clause 2 triangle: $\{u_{2, 1}, u_{2, 2}, u_{2, 3}\}$ (representing literals $\bar{x}_1, \bar{x}_2, x_3$)
- **Edges (15 total):**
  - Variable edges (3): $(v_{x_1}, v_{\bar{x}_1}), \; (v_{x_2}, v_{\bar{x}_2}), \; (v_{x_3}, v_{\bar{x}_3})$
  - Clause triangle edges (6):
    * $C_1$: $(u_{1, 1}, u_{1, 2}), \; (u_{1, 2}, u_{1, 3}), \; (u_{1, 3}, u_{1, 1})$
    * $C_2$: $(u_{2, 1}, u_{2, 2}), \; (u_{2, 2}, u_{2, 3}), \; (u_{2, 3}, u_{2, 1})$
  - Communication edges (6):
    * From $C_1$: $(u_{1, 1}, v_{x_1}), \; (u_{1, 2}, v_{x_2}), \; (u_{1, 3}, v_{x_3})$
    * From $C_2$: $(u_{2, 1}, v_{\bar{x}_1}), \; (u_{2, 2}, v_{\bar{x}_2}), \; (u_{2, 3}, v_{x_3})$

```text
================================================================================
                    CONSTRUCTED GRAPH G FOR CONCRETE INSTANCE
================================================================================

   [ VARIABLE GADGETS ]
   
       ( v_x1 )--------( v_¬x1 )         ( v_x2 )--------( v_¬x2 )         ( v_x3 )--------( v_¬x3 )
          |                |                |                |                |
          |                |                |                |                |
   +------+----------------+----------------+----------------+----------------+
   |      |                |                |                |                |
   |   [ COMMUNICATION EDGES ]              |                |                |
   |      |                |                |                |                |
   |      |                +-----------+    |    +-----------+                |
   |      |                            |    |    |           +----------------+
   |      |                            |    |    |           |                |
   |      v                            v    v    v           v                v
   |  ( u_1,1 )                    ( u_2,1 )   ( u_1,2 )  ( u_2,2 )        ( u_1,3 )     ( u_2,3 )
   |    /   \                        /   \                                    \         /
   |   /     \                      /     \                                    \       /
   |  /       \                    /       \                                    \     /
   | ( u_1,2 )-( u_1,3 )          ( u_2,2 )-( u_2,3 )                            \   /
   +------------------------------------------------------------------------------+
         [ Triangle C_1 ]               [ Triangle C_2 ]
```

---

### 4.6 Step 4: Rigorous Bi-Directional Correctness Proof

$$\phi \in \text{3-SAT} \iff \langle G, k \rangle \in \text{VERTEX-COVER}$$

---

#### Direction 1 ($\implies$): Soundness (If $\phi$ is satisfiable, then $G$ has a vertex cover of size $k = n + 2m$)

1. **Premise:** Suppose $\phi$ is satisfiable. Then there exists a valid truth assignment $\tau: \{x_1, \dots, x_n\} \to \{0, 1\}$ such that every clause $C_j$ evaluates to TRUE.
2. **Construction of Candidate Vertex Cover $V'$:**  
   We select exactly $k = n + 2m$ vertices into $V'$ according to the following two rules:
   - **Rule A (From Variable Gadgets):** For each variable $x_i$ ($i \in \{1, 2, \dots, n\}$):
     * If $\tau(x_i) = 1$, add vertex $v_{x_i}$ to $V'$.
     * If $\tau(x_i) = 0$, add vertex $v_{\bar{x}_i}$ to $V'$.
     * Because $\tau$ assigns a unique truth value to each variable, we select **exactly 1 vertex per variable gadget**.
     * Subtotal vertices from variable gadgets: $n$.
   - **Rule B (From Clause Gadgets):** For each clause $C_j$ ($j \in \{1, 2, \dots, m\}$):
     * Since $\phi(\tau) = 1$, clause $C_j = (l_{j, 1} \lor l_{j, 2} \lor l_{j, 3})$ contains at least one literal that evaluates to TRUE under $\tau$.
     * Choose one such true literal. Let its index in the clause be $k^* \in \{1, 2, 3\}$ (i.e., $\tau(l_{j, k^*}) = 1$).
     * For the other two literal positions in the clause triangle, $p, q \in \{1, 2, 3\} \setminus \{k^*\}$, add their corresponding vertices $u_{j, p}$ and $u_{j, q}$ to $V'$.
     * Leave vertex $u_{j, k^*}$ **out** of $V'$.
     * Subtotal vertices from clause gadgets: exactly $2$ vertices per clause $\implies 2m$.
3. **Total Size of $V'$:**
   $$|V'| = n + 2m = k$$
4. **Verification that $V'$ covers every edge in $E$:**
   - **Class 1 (Variable Edges):** For each edge $(v_{x_i}, v_{\bar{x}_i})$, Rule A explicitly selects either $v_{x_i}$ or $v_{\bar{x}_i}$ into $V'$. Thus, all $n$ variable edges are covered.
   - **Class 2 (Clause Triangle Edges):** In each clause triangle $\{u_{j, 1}, u_{j, 2}, u_{j, 3}\}$, Rule B selects 2 of the 3 vertices into $V'$. In any triangle $K_3$, selecting 2 vertices covers all 3 edges:
     * If vertices $\{u_{j, 2}, u_{j, 3}\} \in V'$, the edges $(u_{j, 1}, u_{j, 2})$, $(u_{j, 2}, u_{j, 3})$, and $(u_{j, 3}, u_{j, 1})$ are all incident on at least one chosen vertex.
     * Thus, all $3m$ clause edges are covered.
   - **Class 3 (Communication Edges):** Consider any communication edge $e = (u_{j, k}, v_{l_{j, k}})$ connecting clause vertex $u_{j, k}$ to literal vertex $v_{l_{j, k}}$:
     * **Case A:** Vertex $u_{j, k} \in V'$. Then edge $e$ is covered by endpoint $u_{j, k}$.
     * **Case B:** Vertex $u_{j, k} \notin V'$. By Rule B, the only vertex excluded from clause triangle $j$ is $u_{j, k^*}$, corresponding to the literal $l_{j, k^*}$ that is **TRUE** under $\tau$.
       Since $\tau(l_{j, k^*}) = 1$, Rule A explicitly placed the corresponding literal vertex $v_{l_{j, k^*}}$ into $V'$.
       Therefore, edge $(u_{j, k^*}, v_{l_{j, k^*}})$ is covered by its other endpoint $v_{l_{j, k^*}} \in V'$.
5. Every edge in $E$ is covered by at least one vertex in $V'$.
6. Therefore, $V'$ is a valid vertex cover of size $k = n + 2m$.

---

#### Direction 2 ($\impliedby$): Completeness (If $G$ has a vertex cover of size $\le k = n + 2m$, then $\phi$ is satisfiable)

1. **Premise:** Suppose $G$ has a vertex cover $V'$ with $|V'| \le k = n + 2m$.
2. **Lower Bound on Variable Gadget Selection:**
   - There are $n$ disjoint variable edges $(v_{x_i}, v_{\bar{x}_i})$.
   - Because these edges do not share any vertices, any valid vertex cover must select **at least 1 vertex** from each variable gadget to cover these $n$ edges:
     $$|V' \cap \{v_{x_i}, v_{\bar{x}_i}\}| \ge 1 \quad \forall \; i \in \{1, 2, \dots, n\}$$
   - Summing across all $n$ variable gadgets:
     $$|V' \cap V_{\text{var}}| \ge n$$
3. **Lower Bound on Clause Triangle Selection:**
   - There are $m$ disjoint clause triangles $T_j = \{u_{j, 1}, u_{j, 2}, u_{j, 3}\}$.
   - As established, a single vertex can cover at most 2 edges of a triangle, leaving the 3rd edge uncovered.
   - Therefore, any valid vertex cover must select **at least 2 vertices** from each clause triangle:
     $$|V' \cap \{u_{j, 1}, u_{j, 2}, u_{j, 3}\}| \ge 2 \quad \forall \; j \in \{1, 2, \dots, m\}$$
   - Summing across all $m$ clause gadgets:
     $$|V' \cap V_{\text{clause}}| \ge 2m$$
4. **Exact Partition Deduction:**
   - Summing the two minimum requirements:
     $$|V'| = |V' \cap V_{\text{var}}| + |V' \cap V_{\text{clause}}| \ge n + 2m$$
   - But by the initial premise, $|V'| \le n + 2m$.
   - Combining these inequalities:
     $$n + 2m \le |V'| \le n + 2m \implies |V'| = n + 2m$$
   - Therefore, the inequalities must hold with **exact equality**:
     * For every variable $x_i$, $V'$ contains **exactly 1 vertex** from $\{v_{x_i}, v_{\bar{x}_i}\}$.
     * For every clause $C_j$, $V'$ contains **exactly 2 vertices** from $\{u_{j, 1}, u_{j, 2}, u_{j, 3}\}$.
5. **Truth Assignment Construction:**
   - Define assignment $\tau: \{x_1, \dots, x_n\} \to \{0, 1\}$ by:
     $$\tau(x_i) = \begin{cases} 1, & \text{if } v_{x_i} \in V' \\ 0, & \text{if } v_{\bar{x}_i} \in V' \end{cases}$$
   - **Consistency:** Since $|V' \cap \{v_{x_i}, v_{\bar{x}_i}\}| = 1$, exactly one of $\{v_{x_i}, v_{\bar{x}_i}\}$ is in $V'$. No variable is assigned both 0 and 1, or left unassigned. Thus, $\tau$ is a well-defined, consistent truth assignment.
6. **Verification that $\tau$ Satisfies Every Clause $C_j$:**
   - Consider an arbitrary clause $C_j = (l_{j, 1} \lor l_{j, 2} \lor l_{j, 3})$.
   - Since $V'$ contains exactly 2 vertices from clause triangle $j$, there is **exactly 1 vertex** in the triangle that is **not** in $V'$.
   - Let this unselected vertex be $u_{j, k^*}$ (where $k^* \in \{1, 2, 3\}$).
   - Now examine the communication edge incident on this vertex:
     $$e_{\text{comm}} = (u_{j, k^*}, \; v_{l_{j, k^*}})$$
   - Because $V'$ is a valid vertex cover, it must cover edge $e_{\text{comm}}$.
   - Since $u_{j, k^*} \notin V'$, the other endpoint **must** belong to $V'$:
     $$v_{l_{j, k^*}} \in V'$$
   - By our truth assignment rule:
     * If $v_{l_{j, k^*}} = v_{x_i}$, then $v_{x_i} \in V' \implies \tau(x_i) = 1$, making literal $l_{j, k^*} = x_i$ TRUE.
     * If $v_{l_{j, k^*}} = v_{\bar{x}_i}$, then $v_{\bar{x}_i} \in V' \implies \tau(x_i) = 0$, making literal $l_{j, k^*} = \bar{x}_i$ TRUE.
   - In either case, literal $l_{j, k^*}$ evaluates to TRUE under $\tau$.
   - Because clause $C_j$ contains at least one literal ($l_{j, k^*}$) that evaluates to TRUE, clause $C_j$ is satisfied.
7. Since this holds for all $m$ clauses, $\phi(\tau) = 1$.
8. Formula $\phi$ is satisfiable. $\blacksquare$

---

### 4.7 Numerical Verification on the Concrete Instance

Let us test a satisfying assignment for our instance:
$$\phi = (x_1 \lor x_2 \lor x_3) \land (\bar{x}_1 \lor \bar{x}_2 \lor x_3)$$

- Let truth assignment be: $\tau = (x_1 = 1, \; x_2 = 0, \; x_3 = 0)$.
  * Clause 1: $(1 \lor 0 \lor 0) = 1$ (Satisfied by $x_1$, literal position 1).
  * Clause 2: $(0 \lor 1 \lor 0) = 1$ (Satisfied by $\bar{x}_2$, literal position 2).

#### Selected Vertex Cover $V'$ of Size $k = 7$:
1. **From Variable Gadgets ($n = 3$):**
   - $\tau(x_1) = 1 \implies \text{Pick } v_{x_1}$
   - $\tau(x_2) = 0 \implies \text{Pick } v_{\bar{x}_2}$
   - $\tau(x_3) = 0 \implies \text{Pick } v_{\bar{x}_3}$
   - Variable subset: $\{v_{x_1}, v_{\bar{x}_2}, v_{\bar{x}_3}\}$ (Size = 3).
2. **From Clause 1 Triangle ($2m = 4$):**
   - Clause 1 satisfied by literal 1 ($x_1$). Leave $u_{1, 1}$ OUT.
   - Pick $u_{1, 2}$ and $u_{1, 3}$ into $V'$.
3. **From Clause 2 Triangle:**
   - Clause 2 satisfied by literal 2 ($\bar{x}_2$). Leave $u_{2, 2}$ OUT.
   - Pick $u_{2, 1}$ and $u_{2, 3}$ into $V'$.

#### Complete Candidate Cover:
$$V' = \{v_{x_1}, v_{\bar{x}_2}, v_{\bar{x}_3}, \; u_{1, 2}, u_{1, 3}, \; u_{2, 1}, u_{2, 3}\}$$
$$\text{Total size } |V'| = 3 + 2 + 2 = 7 = k$$

#### Edge-by-Edge Coverage Audit:
| Edge Index | Edge $(u, v)$ | Endpoints in $V'$ | Covered? | Covering Vertex |
| :---: | :---: | :---: | :---: | :---: |
| 1 | $(v_{x_1}, v_{\bar{x}_1})$ | $v_{x_1} \in V'$ | **YES** | $v_{x_1}$ |
| 2 | $(v_{x_2}, v_{\bar{x}_2})$ | $v_{\bar{x}_2} \in V'$ | **YES** | $v_{\bar{x}_2}$ |
| 3 | $(v_{x_3}, v_{\bar{x}_3})$ | $v_{\bar{x}_3} \in V'$ | **YES** | $v_{\bar{x}_3}$ |
| 4 | $(u_{1, 1}, u_{1, 2})$ | $u_{1, 2} \in V'$ | **YES** | $u_{1, 2}$ |
| 5 | $(u_{1, 2}, u_{1, 3})$ | $u_{1, 2}, u_{1, 3} \in V'$ | **YES** | $u_{1, 2}, u_{1, 3}$ |
| 6 | $(u_{1, 3}, u_{1, 1})$ | $u_{1, 3} \in V'$ | **YES** | $u_{1, 3}$ |
| 7 | $(u_{2, 1}, u_{2, 2})$ | $u_{2, 1} \in V'$ | **YES** | $u_{2, 1}$ |
| 8 | $(u_{2, 2}, u_{2, 3})$ | $u_{2, 3} \in V'$ | **YES** | $u_{2, 3}$ |
| 9 | $(u_{2, 3}, u_{2, 1})$ | $u_{2, 1}, u_{2, 3} \in V'$ | **YES** | $u_{2, 1}, u_{2, 3}$ |
| 10 | $(u_{1, 1}, v_{x_1})$ | $v_{x_1} \in V'$ | **YES** | $v_{x_1}$ |
| 11 | $(u_{1, 2}, v_{x_2})$ | $u_{1, 2} \in V'$ | **YES** | $u_{1, 2}$ |
| 12 | $(u_{1, 3}, v_{x_3})$ | $u_{1, 3} \in V'$ | **YES** | $u_{1, 3}$ |
| 13 | $(u_{2, 1}, v_{\bar{x}_1})$ | $u_{2, 1} \in V'$ | **YES** | $u_{2, 1}$ |
| 14 | $(u_{2, 2}, v_{\bar{x}_2})$ | $v_{\bar{x}_2} \in V'$ | **YES** | $v_{\bar{x}_2}$ |
| 15 | $(u_{2, 3}, v_{x_3})$ | $u_{2, 3} \in V'$ | **YES** | $u_{2, 3}$ |

Every single one of the 15 edges is covered by at least one vertex in $V'$. Zero uncovered edges remain!

---

## 5. Formal Reduction: SUBSET-SUM to 0/1 KNAPSACK

The reduction from **SUBSET-SUM** to **0/1 KNAPSACK Decision** demonstrates how a number-theoretic problem maps into a resource allocation optimization problem.

```text
Instance of SUBSET-SUM:
Multiset S = {s1, s2, ..., sn}, Target T
                 |
                 v   Linear Transformation:
                     Weight w_i = s_i
                     Profit v_i = s_i
                     Capacity W = T
                     Target Profit P = T
                 |
                 v
Instance of 0/1 KNAPSACK:
Can we achieve Profit >= T with Weight <= T?
```

---

### 5.1 Theorem 5.1
$$\text{SUBSET-SUM} \le_p \text{0/1 KNAPSACK-DECISION}$$

#### Proof:

**Step 1: Membership in NP ($\text{KNAPSACK-DEC} \in \text{NP}$)**
1. **Certificate:** A binary vector $X = (x_1, x_2, \dots, x_n) \in \{0, 1\}^n$.
2. **Verifier Algorithm:**
   - Compute total weight: $W_{\text{total}} = \sum_{i=1}^n w_i x_i$.
   - Compute total profit: $P_{\text{total}} = \sum_{i=1}^n v_i x_i$.
   - Output $\text{ACCEPT}$ if and only if $W_{\text{total}} \le W$ and $P_{\text{total}} \ge P$.
3. Total arithmetic operations: $2n$ additions and multiplications.
4. Verifier executes in $\mathcal{O}(n)$ polynomial time. Thus, $\text{0/1 KNAPSACK-DEC} \in \text{NP}$.

**Step 2: Constructing the Reduction Function $f$**
Given an instance of SUBSET-SUM consisting of multiset $S = \{s_1, s_2, \dots, s_n\}$ and target integer $T$:
1. For each element $s_i \in S$, define an item with:
   - Weight: $w_i = s_i$
   - Profit Value: $v_i = s_i$
2. Set the Knapsack Capacity:
   $$W = T$$
3. Set the Target Profit Threshold:
   $$P = T$$
4. Output the Knapsack instance $\langle \{w_i\}, \{v_i\}, W = T, P = T \rangle$.
5. Computing this reduction requires setting $2n$ variables and 2 scalars, running in $\mathcal{O}(n)$ time.

**Step 3: Bi-Directional Correctness Proof**

**Forward Direction ($\implies$):**
1. Suppose $\langle S, T \rangle \in \text{SUBSET-SUM}$.
2. Then there exists a subset $S' \subseteq S$ such that:
   $$\sum_{s_i \in S'} s_i = T$$
3. Define the binary selection vector $X \in \{0, 1\}^n$ by setting $x_i = 1$ if $s_i \in S'$, and $x_i = 0$ otherwise.
4. The total weight of chosen items is:
   $$\sum_{i=1}^n w_i x_i = \sum_{s_i \in S'} s_i = T \le W \quad (\text{since } W = T)$$
5. The total profit value of chosen items is:
   $$\sum_{i=1}^n v_i x_i = \sum_{s_i \in S'} s_i = T \ge P \quad (\text{since } P = T)$$
6. Both Knapsack conditions are satisfied simultaneously.
7. Thus, the Knapsack instance is a YES-instance.

**Reverse Direction ($\impliedby$):**
1. Suppose the Knapsack instance is a YES-instance.
2. Then there exists a binary vector $X \in \{0, 1\}^n$ such that:
   $$\sum_{i=1}^n w_i x_i \le T \quad \text{and} \quad \sum_{i=1}^n v_i x_i \ge T$$
3. Since our construction explicitly defined $w_i = s_i$ and $v_i = s_i$ for all $i \in \{1, \dots, n\}$:
   $$\sum_{i=1}^n w_i x_i = \sum_{i=1}^n s_i x_i \quad \text{and} \quad \sum_{i=1}^n v_i x_i = \sum_{i=1}^n s_i x_i$$
4. Let $A = \sum_{i=1}^n s_i x_i$. Substituting $A$ into both inequalities yields:
   $$A \le T \quad \text{and} \quad A \ge T$$
5. By the anti-symmetry of partial orders on the real numbers:
   $$(A \le T \land A \ge T) \implies A = T$$
6. Therefore:
   $$\sum_{i=1}^n s_i x_i = T$$
7. Selecting the sub-multiset $S' = \{s_i \mid x_i = 1\}$ gives $\sum_{s_i \in S'} s_i = T$.
8. Thus, $\langle S, T \rangle$ is a YES-instance for SUBSET-SUM. $\blacksquare$

---

## 6. Comprehensive Canonical Problems Comparison Matrix

```text
+======================================================================================================================+
|                                    MASTER NP-COMPLETE REDUCTION REFERENCE MATRIX                                     |
+==================+===========================+===========================+======================+====================+
| Problem Name     | Input Representation      | Target Bound Parameter    | Predecessor Problem  | Reduction Core Idea|
+==================+===========================+===========================+======================+====================+
| 3-SAT            | 3-CNF formula with        | Satisfying truth          | Circuit-SAT / SAT    | Clause resolution &|
|                  | n vars, m clauses         | assignment τ              |                      | literal splitting  |
+------------------+---------------------------+---------------------------+----------------------+--------------------+
| CLIQUE           | Graph G = (V, E),         | Complete subgraph         | 3-SAT                | Clause clusters,   |
|                  | integer k                 | of size ≥ k               |                      | consistency edges  |
+------------------+---------------------------+---------------------------+----------------------+--------------------+
| INDEPENDENT-SET  | Graph G = (V, E),         | Mutually non-adjacent     | CLIQUE               | Graph complement   |
|                  | integer k                 | vertex set of size ≥ k    |                      | Ḡ = (V, Ē)         |
+------------------+---------------------------+---------------------------+----------------------+--------------------+
| VERTEX-COVER     | Graph G = (V, E),         | Edge-covering vertex      | 3-SAT or             | Variable edges +   |
|                  | integer k                 | subset of size ≤ k        | INDEPENDENT-SET      | clause triangles   |
+------------------+---------------------------+---------------------------+----------------------+--------------------+
| SUBSET-SUM       | Multiset of integers S,   | Sub-multiset sum          | 3-SAT or             | Base-10 / base-B   |
|                  | target integer T          | exactly equal to T        | EXACT-COVER          | digit encoding     |
+------------------+---------------------------+---------------------------+----------------------+--------------------+
| 0/1 KNAPSACK     | Weights w_i, values v_i,  | Weight ≤ W and            | SUBSET-SUM           | Set w_i = v_i = s_i|
|                  | capacity W, target P      | Value ≥ P                 |                      | and W = P = T      |
+------------------+---------------------------+---------------------------+----------------------+--------------------+
| HAMILTONIAN-     | Graph G = (V, E)          | Simple cycle visiting     | VERTEX-COVER         | Directed gadget    |
| CYCLE            |                           | every vertex once         |                      | XOR tracking       |
+------------------+---------------------------+---------------------------+----------------------+--------------------+
| TSP-DECISION     | Complete weighted graph   | Hamiltonian tour of       | HAMILTONIAN-CYCLE    | Cost 1 if e ∈ E,   |
|                  | G, cost matrix C, bound k | total cost ≤ k            |                      | Cost 2 if e ∉ E    |
+==================+===========================+===========================+======================+====================+
```

---

## 7. KTU Examination High-Yield Preparation

This section provides examination-targeted model answers formatted for direct scoring under the KTU 2024 scheme for course code **PCCST502 / CST306**.

---

### Question 1 (3 Marks): State Gallai's Duality Theorem and its significance in polynomial reductions.

#### Model Answer:
- **Statement:** For any undirected graph $G = (V, E)$ and any vertex subset $S \subseteq V$, $S$ is an independent set in $G$ if and only if its complement $V \setminus S$ is a vertex cover in $G$.
- **Formula:** $\alpha(G) + \tau(G) = |V|$, where $\alpha(G)$ is the maximum independent set size and $\tau(G)$ is the minimum vertex cover size.
- **Significance:** It establishes an immediate linear-time reduction between the two problems ($\text{INDEP-SET} \le_p \text{VERTEX-COVER}$): an instance $\langle G, k \rangle$ for Independent Set directly translates to instance $\langle G, |V| - k \rangle$ for Vertex Cover, proving that an efficient algorithm for one immediately solves the other.

---

### Question 2 (5 Marks): Prove that the Clique problem polynomial-time reduces to the Independent Set problem.

#### Model Answer:
1. **Reduction Construction:** Given an instance $\langle G = (V, E), k \rangle$ of the Clique problem:
   - Construct the complement graph $\overline{G} = (V, \overline{E})$, where $(u, v) \in \overline{E} \iff (u, v) \notin E$ for all $u \ne v$.
   - Retain the target threshold $k$.
   - Output $\langle \overline{G}, k \rangle$. Construction runs in $\mathcal{O}(|V|^2)$ polynomial time.
2. **Correctness Forward Direction ($\implies$):**  
   If $G$ has a clique $S$ of size $k$, then every pair of vertices in $S$ has an edge in $E$. By definition of complementation, no pair in $S$ shares an edge in $\overline{E}$. Hence, $S$ is an independent set of size $k$ in $\overline{G}$.
3. **Correctness Backward Direction ($\impliedby$):**  
   If $\overline{G}$ has an independent set $S$ of size $k$, then no two vertices in $S$ share an edge in $\overline{E}$. Therefore, every pair in $S$ must share an edge in $E$. Hence, $S$ forms a clique of size $k$ in $G$.
4. **Conclusion:** $G$ has a clique of size $k \iff \overline{G}$ has an independent set of size $k$. Thus, $\text{CLIQUE} \le_p \text{INDEP-SET}$. $\blacksquare$

---

### Question 3 (10 Marks): Explain the gadget construction and prove the NP-Completeness of the Vertex Cover problem by reducing from 3-SAT.

#### Model Answer Structure:
1. **Membership in NP:** Define certificate (vertex subset $V'$) and verifier (checking $|V'| \le k$ and verifying every edge $e \in E$ has at least one endpoint in $V'$ in $\mathcal{O}(|V| + |E|)$ polynomial time). *(2 Marks)*
2. **Gadget Construction:**
   - **Variable Gadget:** For each variable $x_i$, construct an edge $(v_{x_i}, v_{\bar{x}_i})$. Requires at least 1 vertex in cover. *(2 Marks)*
   - **Clause Gadget:** For each clause $C_j$, construct a triangle $K_3$ of 3 vertices $(u_{j, 1}, u_{j, 2}, u_{j, 3})$. Requires at least 2 vertices in cover. *(2 Marks)*
   - **Communication Edges:** Connect each clause literal vertex to its matching variable literal vertex. *(1 Mark)*
   - **Budget Formula:** Set $k = n + 2m$. *(1 Mark)*
3. **Correctness Proof:**
   - **Soundness ($\implies$):** If $\phi$ is satisfiable, pick true literal vertices in variable gadgets ($n$ vertices) and the 2 non-satisfying vertices in each clause triangle ($2m$ vertices). Prove all 3 edge classes are covered.
   - **Completeness ($\impliedby$):** Since any cover requires $\ge n$ variable vertices and $\ge 2m$ clause vertices, a cover of size $n + 2m$ must pick *exactly* 1 per variable and *exactly* 2 per clause. The truth assignment derived from chosen variable vertices is consistent and satisfies all clauses. *(2 Marks)*

---

### Question 4 (5 Marks): Formulate a polynomial-time reduction from the Subset Sum problem to the 0/1 Knapsack decision problem and prove its correctness.

#### Model Answer:
1. **Reduction Construction:**
   - Given Subset Sum instance: Set $S = \{s_1, \dots, s_n\}$ and target integer $T$.
   - Map to Knapsack instance: For each item $i \in \{1, \dots, n\}$, set weight $w_i = s_i$ and profit value $v_i = s_i$. Set maximum capacity $W = T$ and target profit threshold $P = T$.
   - Time Complexity: $\mathcal{O}(n)$ operations, which is polynomial.
2. **Correctness Proof:**
   - **($\implies$):** If there exists $S' \subseteq S$ with $\sum_{s_i \in S'} s_i = T$, set $x_i = 1$ for $s_i \in S'$ and $0$ otherwise. Then $\sum w_i x_i = T \le W$ and $\sum v_i x_i = T \ge P$. Both Knapsack constraints are satisfied.
   - **($\impliedby$):** If there exists $X \in \{0, 1\}^n$ such that $\sum w_i x_i \le T$ and $\sum v_i x_i \ge T$, since $w_i = v_i = s_i$, we have $\sum s_i x_i \le T$ and $\sum s_i x_i \ge T$. This implies $\sum s_i x_i = T$. The elements with $x_i = 1$ form the required subset.
3. **Conclusion:** Subset Sum reduces to 0/1 Knapsack Decision in polynomial time. $\blacksquare$
