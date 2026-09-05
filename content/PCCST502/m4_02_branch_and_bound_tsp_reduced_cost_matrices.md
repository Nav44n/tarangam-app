# Module 4.2: Branch and Bound — Travelling Salesperson Problem (TSP) with Reduced Cost Matrices

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search: Branch & Bound Paradigm  
**Document Classification:** Publication-Grade Theoretical Lecture Note & Algorithmic Foundation  

---

## 1. Executive Overview & Formal Problem Formulation

The **Travelling Salesperson Problem (TSP)** is an archetypal $NP$-hard combinatorial optimization problem. Given a collection of cities and the cost of travel between each pair, the objective is to determine the tour of minimum total cost that visits every city exactly once and returns to the origin.

### 1.1 Mathematical Graph Formulation
Let $G = (V, E)$ be a directed, edge-weighted complete graph where:
- $V = \{1, 2, 3, \dots, n\}$ is the set of $n$ vertices representing cities.
- $E = \{(i, j) \mid i, j \in V, \; i \ne j\}$ is the set of directed edges representing paths between cities.
- $C = [c_{ij}]_{n \times n}$ is the cost (or distance) adjacency matrix, where $c_{ij} \in \mathbb{R}_{\ge 0} \cup \{\infty\}$ denotes the cost of traversing edge $(i, j)$.

By convention:
$$c_{ii} = \infty \quad \forall \; i \in \{1, 2, \dots, n\}$$
If no direct edge exists from $i$ to $j$, $c_{ij} = \infty$.

### 1.2 Integer Linear Programming (ILP) Formulation
A tour can be characterized by decision variables $x_{ij} \in \{0, 1\}$, where:
$$x_{ij} = \begin{cases} 1, & \text{if directed edge } (i, j) \text{ is traversed in the tour} \\ 0, & \text{otherwise} \end{cases}$$

The TSP is formalized as the following optimization model:

$$\min \sum_{i=1}^n \sum_{j=1}^n c_{ij} x_{ij}$$

subject to:
1. **Out-degree Conservation:** Exactly one edge leaves every vertex $i$:
   $$\sum_{j=1, j \ne i}^n x_{ij} = 1 \quad \forall \; i \in V$$
2. **In-degree Conservation:** Exactly one edge enters every vertex $j$:
   $$\sum_{i=1, i \ne j}^n x_{ij} = 1 \quad \forall \; j \in V$$
3. **Sub-tour Elimination Constraints (Dantzig-Fulkerson-Johnson Form):**
   $$\sum_{i \in S} \sum_{j \in S, j \ne i} x_{ij} \le |S| - 1 \quad \forall \; S \subset V, \; 2 \le |S| \le n-1$$
   *(This ensures the solution forms a single contiguous cycle of length $n$ spanning all vertices, rather than isolated disjoint sub-loops).*

::: callout-intuition
**Mental Model: The Departure-Arrival Toll Booth**  
Every valid salesperson tour must accomplish two non-negotiable tasks in every single city:
1. **Depart** from the city (requiring payment of at least the cheapest outbound exit toll).
2. **Arrive** at the city (requiring payment of at least the cheapest inbound entrance toll).  
Even if we have not yet decided the exact order of the journey, the salesperson must pay at least the sum of every city's minimum departure toll plus every city's minimum arrival toll. This baseline constitutes our **infallible mathematical lower bound**.
:::

---

## 2. Theoretical Foundations of Reduced Cost Matrices

The effectiveness of Least-Cost Branch and Bound (LC-B&B) for TSP depends on calculating tight, admissible lower bounds at every node in the state-space tree. The canonical technique for generating these bounds is the **Reduced Cost Matrix Method**.

### 2.1 Definition of a Reduced Cost Matrix
A square cost matrix $A \in (\mathbb{R}_{\ge 0} \cup \{\infty\})^{n \times n}$ is defined as a **Reduced Cost Matrix** if and only if:
1. All elements are non-negative:
   $$A[i, j] \ge 0 \quad \forall \; i, j \in \{1, 2, \dots, n\}$$
2. Every row contains at least one zero:
   $$\forall \; i \in \{1, 2, \dots, n\}, \quad \exists \; j \text{ such that } A[i, j] = 0 \quad (\text{unless row } i \text{ is entirely } \infty)$$
3. Every column contains at least one zero:
   $$\forall \; j \in \{1, 2, \dots, n\}, \quad \exists \; i \text{ such that } A[i, j] = 0 \quad (\text{unless column } j \text{ is entirely } \infty)$$

---

### 2.2 The Two-Phase Matrix Reduction Algorithm

Given an arbitrary cost matrix $C$, we convert it into a reduced matrix $A$ in two sequential phases:

```
      Original Cost Matrix C
                 |
                 v
   [ Phase 1: Row Reduction ]    ---> Subtract row minimums r_i
                 |
                 v
  [ Phase 2: Column Reduction ]  ---> Subtract column minimums c_j
                 |
                 v
      Reduced Cost Matrix A      ---> Total Bound: R = ∑ r_i + ∑ c_j
```

#### Phase 1: Row Reduction
For each row $i \in \{1, 2, \dots, n\}$:
1. Find the row minimum among finite elements:
   $$r_i = \min_{1 \le j \le n} C[i, j]$$
2. If $0 < r_i < \infty$, subtract $r_i$ from every element in row $i$:
   $$C'[i, j] = C[i, j] - r_i \quad \forall \; j \in \{1, 2, \dots, n\}$$
   *(If $r_i = 0$ or $r_i = \infty$, the row remains unchanged and $r_i = 0$).*

The total cost extracted during row reduction is:
$$R_{\text{row}} = \sum_{i=1}^n r_i$$

#### Phase 2: Column Reduction
For each column $j \in \{1, 2, \dots, n\}$ of the row-reduced matrix $C'$:
1. Find the column minimum among finite elements:
   $$c_j = \min_{1 \le i \le n} C'[i, j]$$
2. If $0 < c_j < \infty$, subtract $c_j$ from every element in column $j$:
   $$A[i, j] = C'[i, j] - c_j \quad \forall \; i \in \{1, 2, \dots, n\}$$
   *(If $c_j = 0$ or $c_j = \infty$, the column remains unchanged and $c_j = 0$).*

The total cost extracted during column reduction is:
$$R_{\text{col}} = \sum_{j=1}^n c_j$$

The **Total Reduction Cost** for the matrix is:
$$R = R_{\text{row}} + R_{\text{col}} = \sum_{i=1}^n r_i + \sum_{j=1}^n c_j$$

---

### 2.3 Mathematical Proof: Lower Bound Invariant

#### Theorem 2.1 (Admissibility of Matrix Reduction)
*Let $C$ be the original cost matrix of TSP instance $G$, and let $A$ be the matrix obtained by row and column reductions with total reduction cost $R$. Then $R$ is an admissible lower bound on the cost of any complete Hamiltonian tour in $G$.*

**Formal Proof:**
1. Let $T = (e_1, e_2, \dots, e_n)$ be any arbitrary, valid Hamiltonian tour in $G$, represented as a set of $n$ directed edges:
   $$T = \{(v_1, v_2), (v_2, v_3), \dots, (v_n, v_1)\}$$
2. The total true cost of tour $T$ under matrix $C$ is:
   $$\text{Cost}_C(T) = \sum_{(i, j) \in T} C[i, j]$$
3. By the fundamental definition of a Hamiltonian cycle, the out-degree of every vertex in $T$ is exactly 1. Therefore, for every row $i \in \{1, 2, \dots, n\}$, tour $T$ contains **exactly one** edge $(i, k)$ that departs from vertex $i$.
4. When we subtract $r_i$ from all entries in row $i$, the entry corresponding to edge $(i, k)$ decreases by exactly $r_i$:
   $$C'[i, k] = C[i, k] - r_i$$
   Summing across all $n$ unique departing vertices:
   $$\sum_{(i, j) \in T} C'[i, j] = \sum_{(i, j) \in T} C[i, j] - \sum_{i=1}^n r_i = \text{Cost}_C(T) - R_{\text{row}}$$
5. Similarly, by the in-degree conservation of a Hamiltonian cycle, the in-degree of every vertex in $T$ is exactly 1. Tour $T$ contains **exactly one** edge $(m, j)$ that enters vertex $j$.
6. When we subtract $c_j$ from all entries in column $j$, the entry corresponding to edge $(m, j)$ decreases by exactly $c_j$:
   $$A[m, j] = C'[m, j] - c_j$$
   Summing across all $n$ unique arriving vertices:
   $$\sum_{(i, j) \in T} A[i, j] = \sum_{(i, j) \in T} C'[i, j] - \sum_{j=1}^n c_j = \text{Cost}_C(T) - R_{\text{row}} - R_{\text{col}} = \text{Cost}_C(T) - R$$
7. Rearranging this identity gives:
   $$\text{Cost}_C(T) = \text{Cost}_A(T) + R$$
8. Because the reduction algorithm ensures $A[i, j] \ge 0$ for all valid transitions, the cost of any tour under matrix $A$ must be non-negative:
   $$\text{Cost}_A(T) = \sum_{(i, j) \in T} A[i, j] \ge 0$$
9. Substituting this inequality back into the identity:
   $$\text{Cost}_C(T) \ge 0 + R \implies \text{Cost}_C(T) \ge R$$
10. Since this inequality holds for **every** valid Hamiltonian tour $T$, the minimum tour cost satisfies:
    $$\text{Cost}^*(T) = \min_{T \in \text{Tours}} \text{Cost}_C(T) \ge R$$
Thus, $R$ is an admissible lower bound on the optimal tour cost. $\blacksquare$

---

## 3. State-Space Tree Transition Mechanics

In an LC-B&B search for TSP, each node in the state-space tree represents a partial tour. Moving from a parent node to a child node corresponds to committing to a specific directed edge $(i, j)$.

```
                      Parent Node P
               [Partial Path: 1 -> ... -> i]
                   Reduced Matrix: A_P
                   Lower Bound: ĉ(P)
                          |
                          | Branch on Edge (i, j)
                          v
                       Child Node C
             [Partial Path: 1 -> ... -> i -> j]
                   Modified Matrix: M
                   Row/Col Reductions: r
                   Lower Bound: ĉ(C)
```

### 3.1 Four-Step Node Generation Procedure
When branching from parent state $P$ to child state $C$ along edge $(i, j)$:

#### Step 1: Invalidate Row $i$
Set all entries in row $i$ to $\infty$:
$$M[i, k] = \infty \quad \forall \; k \in \{1, 2, \dots, n\}$$
*Physical Justification:* Vertex $i$ has already committed its outbound departure to vertex $j$. The tour can never leave vertex $i$ again.

#### Step 2: Invalidate Column $j$
Set all entries in column $j$ to $\infty$:
$$M[k, j] = \infty \quad \forall \; k \in \{1, 2, \dots, n\}$$
*Physical Justification:* Vertex $j$ has already committed its inbound arrival from vertex $i$. The tour can never enter vertex $j$ again.

#### Step 3: Prevent Premature Sub-Tours
Set the return path to $\infty$:
$$M[j, 1] = \infty$$
More generally, if the partial path built so far is $(v_{\text{start}} \to \dots \to i \to j)$ and the path length is strictly less than $n$, we must prohibit edge $(j, v_{\text{start}})$ by setting:
$$M[j, v_{\text{start}}] = \infty$$
*Physical Justification:* Returning to the starting city before visiting all $n$ cities forms a disconnected sub-cycle, violating the Sub-tour Elimination Constraint.

#### Step 4: Reduce Matrix $M$ and Compute Child Bound
1. Execute the two-phase reduction algorithm on matrix $M$. Let $r$ be the total additional reduction extracted:
   $$r = \sum_{k=1}^n r_k + \sum_{k=1}^n c_k$$
2. Compute the lower bound $\hat{c}(C)$ for the child node:
   $$\hat{c}(C) = \hat{c}(P) + A_P[i, j] + r$$
   where:
   - $\hat{c}(P)$ is the lower bound of the parent node.
   - $A_P[i, j]$ is the value at cell $(i, j)$ in the **parent's reduced matrix** $A_P$.
   - $r$ is the additional reduction cost extracted from the child's modified matrix $M$.

::: callout-warning
**Algorithmic Trap: The Parent Cost Reference Blunder**  
A catastrophic error in university examinations is taking the edge cost from the **original** matrix $C[i, j]$ instead of the **parent's reduced matrix** $A_P[i, j]$.  
- **Incorrect:** $\hat{c}(\text{child}) = \hat{c}(\text{parent}) + C_{\text{orig}}[i, j] + r$ (Double-counts reductions!)
- **Correct:** $\hat{c}(\text{child}) = \hat{c}(\text{parent}) + A_{\text{parent}}[i, j] + r$
:::

---

## 4. Comprehensive 5W1H Execution Trace: 4-City TSP

We now trace a complete execution of LC-B&B on a $4 \times 4$ TSP instance. Every row and column subtraction, matrix state, and priority queue operation is written out with zero logical leaps.

### 4.1 Problem Specification
Let $n = 4$ vertices $V = \{1, 2, 3, 4\}$ with start vertex = $1$.  
The initial cost matrix $C$ is:

$$C = \begin{bmatrix}
\infty & 10 & 15 & 20 \\
5 & \infty & 9 & 10 \\
6 & 13 & \infty & 12 \\
8 & 8 & 9 & \infty
\end{bmatrix}$$

---

### Step 1: Root Node Initialization (Node 1, Path: $[1]$)

- **What are we doing?** Computing the root lower bound $\hat{c}(1)$ and root reduced cost matrix $A_1$.
- **Why are we starting here?** Every tour begins at the designated source vertex $1$.
- **How do we execute the step mechanically?**

#### Phase 1: Row Reduction on Matrix $C$
1. **Row 1:** Entries are $[\infty, 10, 15, 20]$.
   $$r_1 = \min(10, 15, 20) = 10$$
   Subtract $10$ from Row 1:
   $$[\infty - 10, \; 10 - 10, \; 15 - 10, \; 20 - 10] = [\infty, 0, 5, 10]$$
2. **Row 2:** Entries are $[5, \infty, 9, 10]$.
   $$r_2 = \min(5, 9, 10) = 5$$
   Subtract $5$ from Row 2:
   $$[5 - 5, \; \infty - 5, \; 9 - 5, \; 10 - 5] = [0, \infty, 4, 5]$$
3. **Row 3:** Entries are $[6, 13, \infty, 12]$.
   $$r_3 = \min(6, 13, 12) = 6$$
   Subtract $6$ from Row 3:
   $$[6 - 6, \; 13 - 6, \; \infty - 6, \; 12 - 6] = [0, 7, \infty, 6]$$
4. **Row 4:** Entries are $[8, 8, 9, \infty]$.
   $$r_4 = \min(8, 8, 9) = 8$$
   Subtract $8$ from Row 4:
   $$[8 - 8, \; 8 - 8, \; 9 - 8, \; \infty - 8] = [0, 0, 1, \infty]$$

Sum of row reductions:
$$R_{\text{row}} = r_1 + r_2 + r_3 + r_4 = 10 + 5 + 6 + 8 = 29$$

The intermediate matrix $C'$ after row reductions:

| $C'$ | Col 1 | Col 2 | Col 3 | Col 4 | Row Min ($r_i$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Row 1** | $\infty$ | $0$ | $5$ | $10$ | $r_1 = 10$ |
| **Row 2** | $0$ | $\infty$ | $4$ | $5$ | $r_2 = 5$ |
| **Row 3** | $0$ | $7$ | $\infty$ | $6$ | $r_3 = 6$ |
| **Row 4** | $0$ | $0$ | $1$ | $\infty$ | $r_4 = 8$ |

#### Phase 2: Column Reduction on Matrix $C'$
1. **Column 1:** Entries are $[\infty, 0, 0, 0]^T$.
   $$c_1 = \min(\infty, 0, 0, 0) = 0 \implies \text{No change}$$
2. **Column 2:** Entries are $[0, \infty, 7, 0]^T$.
   $$c_2 = \min(0, \infty, 7, 0) = 0 \implies \text{No change}$$
3. **Column 3:** Entries are $[5, 4, \infty, 1]^T$.
   $$c_3 = \min(5, 4, \infty, 1) = 1$$
   Subtract $1$ from Column 3:
   $$[5 - 1, \; 4 - 1, \; \infty - 1, \; 1 - 1]^T = [4, 3, \infty, 0]^T$$
4. **Column 4:** Entries are $[10, 5, 6, \infty]^T$.
   $$c_4 = \min(10, 5, 6, \infty) = 5$$
   Subtract $5$ from Column 4:
   $$[10 - 5, \; 5 - 5, \; 6 - 5, \; \infty - 5]^T = [5, 0, 1, \infty]^T$$

Sum of column reductions:
$$R_{\text{col}} = c_1 + c_2 + c_3 + c_4 = 0 + 0 + 1 + 5 = 6$$

#### Total Reduction & Root Lower Bound:
$$\hat{c}(1) = R_{\text{row}} + R_{\text{col}} = 29 + 6 = 35$$

The fully reduced matrix $A_1$ for Root Node 1:

| $A_1$ | Col 1 | Col 2 | Col 3 | Col 4 |
| :---: | :---: | :---: | :---: | :---: |
| **Row 1** | $\infty$ | $0$ | $4$ | $5$ |
| **Row 2** | $0$ | $\infty$ | $3$ | $0$ |
| **Row 3** | $0$ | $7$ | $\infty$ | $1$ |
| **Row 4** | $0$ | $0$ | $0$ | $\infty$ |

- **Where did this formula originate?** Derived from Theorem 2.1: $\hat{c}(\text{root}) = \sum r_i + \sum c_j$.
- **What changed?** The global search starts with root lower bound $35$.
- **Active Min-Priority Queue:** `PQ = [(Node 1, ĉ = 35)]`

---

### Step 2: Branching from Root — Expanding Node 1

Node 1 is extracted from `PQ`. It becomes the current E-node.  
From vertex $1$, the salesperson can branch to unvisited vertices $\{2, 3, 4\}$.

---

#### 2.1 Evaluation of Child Node 2 (Edge $(1, 2)$)
- **Path:** $1 \to 2$
- **Edge Cost in Parent Matrix:** $A_1[1, 2] = 0$
- **Matrix Transformations on $A_1$:**
  1. Set **Row 1** to $\infty$ (cannot leave city 1 again).
  2. Set **Col 2** to $\infty$ (cannot enter city 2 again).
  3. Prevent sub-tour: set $A[2, 1] = \infty$ (cannot return immediately to start).

Matrix $M_{1 \to 2}$ before reduction:

| $M_{1 \to 2}$ | Col 1 | Col 2 | Col 3 | Col 4 |
| :---: | :---: | :---: | :---: | :---: |
| **Row 1** | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 2** | $\infty$ | $\infty$ | $3$ | $0$ |
| **Row 3** | $0$ | $\infty$ | $\infty$ | $1$ |
| **Row 4** | $0$ | $\infty$ | $0$ | $\infty$ |

##### Row and Column Reductions on $M_{1 \to 2}$:
- Row 1: All $\infty \implies r_1 = 0$
- Row 2: $\min(\infty, \infty, 3, 0) = 0 \implies r_2 = 0$
- Row 3: $\min(0, \infty, \infty, 1) = 0 \implies r_3 = 0$
- Row 4: $\min(0, \infty, 0, \infty) = 0 \implies r_4 = 0$
- Column 1: Entries are $[\infty, \infty, 0, 0]^T \implies \min = 0 \implies c_1 = 0$
- Column 2: All $\infty \implies c_2 = 0$
- Column 3: Entries are $[\infty, 3, \infty, 0]^T \implies \min = 0 \implies c_3 = 0$
- Column 4: Entries are $[\infty, 0, 1, \infty]^T \implies \min = 0 \implies c_4 = 0$

Total additional reduction:
$$r = \sum r_i + \sum c_j = 0 + 0 = 0$$

##### Lower Bound for Node 2:
$$\hat{c}(2) = \hat{c}(1) + A_1[1, 2] + r = 35 + 0 + 0 = 35$$

The reduced matrix $A_2$ is identical to $M_{1 \to 2}$.

---

#### 2.2 Evaluation of Child Node 3 (Edge $(1, 3)$)
- **Path:** $1 \to 3$
- **Edge Cost in Parent Matrix:** $A_1[1, 3] = 4$
- **Matrix Transformations on $A_1$:**
  1. Set **Row 1** to $\infty$.
  2. Set **Col 3** to $\infty$.
  3. Prevent sub-tour: set $A[3, 1] = \infty$.

Matrix $M_{1 \to 3}$ before reduction:

| $M_{1 \to 3}$ | Col 1 | Col 2 | Col 3 | Col 4 |
| :---: | :---: | :---: | :---: | :---: |
| **Row 1** | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 2** | $0$ | $\infty$ | $\infty$ | $0$ |
| **Row 3** | $\infty$ | $7$ | $\infty$ | $1$ |
| **Row 4** | $0$ | $0$ | $\infty$ | $\infty$ |

##### Row and Column Reductions on $M_{1 \to 3}$:
- Row 1: All $\infty \implies r_1 = 0$
- Row 2: $\min(0, \infty, \infty, 0) = 0 \implies r_2 = 0$
- Row 3: $\min(\infty, 7, \infty, 1) = 1 \implies r_3 = 1$.  
  Subtract $1$ from Row 3: $[\infty, 7 - 1, \infty, 1 - 1] = [\infty, 6, \infty, 0]$
- Row 4: $\min(0, 0, \infty, \infty) = 0 \implies r_4 = 0$

Sum of row reductions:
$$R_{\text{row}} = 0 + 0 + 1 + 0 = 1$$

Inspect Columns after row reduction:
- Column 1: $[\infty, 0, \infty, 0]^T \implies \min = 0 \implies c_1 = 0$
- Column 2: $[\infty, \infty, 6, 0]^T \implies \min = 0 \implies c_2 = 0$
- Column 3: All $\infty \implies c_3 = 0$
- Column 4: $[\infty, 0, 0, \infty]^T \implies \min = 0 \implies c_4 = 0$

Total additional reduction:
$$r = 1 + 0 = 1$$

##### Lower Bound for Node 3:
$$\hat{c}(3) = \hat{c}(1) + A_1[1, 3] + r = 35 + 4 + 1 = 40$$

The reduced matrix $A_3$:

| $A_3$ | Col 1 | Col 2 | Col 3 | Col 4 |
| :---: | :---: | :---: | :---: | :---: |
| **Row 1** | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 2** | $0$ | $\infty$ | $\infty$ | $0$ |
| **Row 3** | $\infty$ | $6$ | $\infty$ | $0$ |
| **Row 4** | $0$ | $0$ | $\infty$ | $\infty$ |

---

#### 2.3 Evaluation of Child Node 4 (Edge $(1, 4)$)
- **Path:** $1 \to 4$
- **Edge Cost in Parent Matrix:** $A_1[1, 4] = 5$
- **Matrix Transformations on $A_1$:**
  1. Set **Row 1** to $\infty$.
  2. Set **Col 4** to $\infty$.
  3. Prevent sub-tour: set $A[4, 1] = \infty$.

Matrix $M_{1 \to 4}$ before reduction:

| $M_{1 \to 4}$ | Col 1 | Col 2 | Col 3 | Col 4 |
| :---: | :---: | :---: | :---: | :---: |
| **Row 1** | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 2** | $0$ | $\infty$ | $3$ | $\infty$ |
| **Row 3** | $0$ | $7$ | $\infty$ | $\infty$ |
| **Row 4** | $\infty$ | $0$ | $0$ | $\infty$ |

##### Row and Column Reductions on $M_{1 \to 4}$:
- Row 1: All $\infty \implies r_1 = 0$
- Row 2: $\min(0, \infty, 3, \infty) = 0 \implies r_2 = 0$
- Row 3: $\min(0, 7, \infty, \infty) = 0 \implies r_3 = 0$
- Row 4: $\min(\infty, 0, 0, \infty) = 0 \implies r_4 = 0$
- Column 1: $[\infty, 0, 0, \infty]^T \implies \min = 0 \implies c_1 = 0$
- Column 2: $[\infty, \infty, 7, 0]^T \implies \min = 0 \implies c_2 = 0$
- Column 3: $[\infty, 3, \infty, 0]^T \implies \min = 0 \implies c_3 = 0$
- Column 4: All $\infty \implies c_4 = 0$

Total additional reduction:
$$r = 0$$

##### Lower Bound for Node 4:
$$\hat{c}(4) = \hat{c}(1) + A_1[1, 4] + r = 35 + 5 + 0 = 40$$

The reduced matrix $A_4$ is identical to $M_{1 \to 4}$.

---

### Step 3: Priority Queue Update and Selection of Next E-Node

At this stage, Node 1 is fully expanded and becomes a **Dead Node**.  
The live nodes inside the Min-Priority Queue are:

| Node ID | Partial Path | Lower Bound ($\hat{c}$) | Status |
| :---: | :---: | :---: | :---: |
| **Node 2** | $1 \to 2$ | **35** | **Minimum (Selected as Next E-Node)** |
| **Node 3** | $1 \to 3$ | $40$ | Live Node |
| **Node 4** | $1 \to 4$ | $40$ | Live Node |

- **Selection Decision:** Node 2 has the lowest lower bound ($\hat{c} = 35$).  
- **Action:** Extract Node 2 from `PQ` to become the next E-node.

---

### Step 4: Branching from Node 2 (Path: $1 \to 2$)

From vertex $2$, the unvisited vertices are $\{3, 4\}$.  
Parent matrix is $A_2$, with $\hat{c}(2) = 35$.

---

#### 4.1 Evaluation of Child Node 5 (Edge $(2, 3)$)
- **Path:** $1 \to 2 \to 3$
- **Edge Cost in Parent Matrix:** $A_2[2, 3] = 3$
- **Matrix Transformations on $A_2$:**
  1. Set **Row 2** to $\infty$.
  2. Set **Col 3** to $\infty$.
  3. Prevent sub-tour: The partial tour is $1 \to 2 \to 3$. Traversing edge $(3, 1)$ would prematurely close the cycle $1 \to 2 \to 3 \to 1$. Therefore, set:
     $$A[3, 1] = \infty$$

Matrix $M_{2 \to 3}$ before reduction:

| $M_{2 \to 3}$ | Col 1 | Col 2 | Col 3 | Col 4 |
| :---: | :---: | :---: | :---: | :---: |
| **Row 1** | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 2** | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 3** | $\infty$ | $\infty$ | $\infty$ | $1$ |
| **Row 4** | $0$ | $\infty$ | $\infty$ | $\infty$ |

##### Row and Column Reductions on $M_{2 \to 3}$:
- Row 1: All $\infty \implies r_1 = 0$
- Row 2: All $\infty \implies r_2 = 0$
- Row 3: $\min(\infty, \infty, \infty, 1) = 1 \implies r_3 = 1$.  
  Subtract $1$ from Row 3: $[\infty, \infty, \infty, 0]$
- Row 4: $\min(0, \infty, \infty, \infty) = 0 \implies r_4 = 0$

Sum of row reductions:
$$R_{\text{row}} = 0 + 0 + 1 + 0 = 1$$

Inspect Columns:
- Column 1: $[\infty, \infty, \infty, 0]^T \implies \min = 0 \implies c_1 = 0$
- Column 2: All $\infty \implies c_2 = 0$
- Column 3: All $\infty \implies c_3 = 0$
- Column 4: $[\infty, \infty, 0, \infty]^T \implies \min = 0 \implies c_4 = 0$

Total additional reduction:
$$r = 1 + 0 = 1$$

##### Lower Bound for Node 5:
$$\hat{c}(5) = \hat{c}(2) + A_2[2, 3] + r = 35 + 3 + 1 = 39$$

---

#### 4.2 Evaluation of Child Node 6 (Edge $(2, 4)$)
- **Path:** $1 \to 2 \to 4$
- **Edge Cost in Parent Matrix:** $A_2[2, 4] = 0$
- **Matrix Transformations on $A_2$:**
  1. Set **Row 2** to $\infty$.
  2. Set **Col 4** to $\infty$.
  3. Prevent sub-tour: The partial tour is $1 \to 2 \to 4$. Traversing $(4, 1)$ prematurely closes cycle $1 \to 2 \to 4 \to 1$. Therefore, set:
     $$A[4, 1] = \infty$$

Matrix $M_{2 \to 4}$ before reduction:

| $M_{2 \to 4}$ | Col 1 | Col 2 | Col 3 | Col 4 |
| :---: | :---: | :---: | :---: | :---: |
| **Row 1** | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 2** | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 3** | $0$ | $\infty$ | $\infty$ | $\infty$ |
| **Row 4** | $\infty$ | $\infty$ | $0$ | $\infty$ |

##### Row and Column Reductions on $M_{2 \to 4}$:
- Row 1: All $\infty \implies r_1 = 0$
- Row 2: All $\infty \implies r_2 = 0$
- Row 3: $\min(0, \infty, \infty, \infty) = 0 \implies r_3 = 0$
- Row 4: $\min(\infty, \infty, 0, \infty) = 0 \implies r_4 = 0$
- Column 1: $[\infty, \infty, 0, \infty]^T \implies \min = 0 \implies c_1 = 0$
- Column 2: All $\infty \implies c_2 = 0$
- Column 3: $[\infty, \infty, \infty, 0]^T \implies \min = 0 \implies c_3 = 0$
- Column 4: All $\infty \implies c_4 = 0$

Total additional reduction:
$$r = 0$$

##### Lower Bound for Node 6:
$$\hat{c}(6) = \hat{c}(2) + A_2[2, 4] + r = 35 + 0 + 0 = 35$$

The reduced matrix $A_6$ is identical to $M_{2 \to 4}$.

---

### Step 5: Priority Queue State and E-Node Selection

The Priority Queue contains:
1. **Node 6:** $1 \to 2 \to 4 \quad (\hat{c} = 35)$
2. **Node 5:** $1 \to 2 \to 3 \quad (\hat{c} = 39)$
3. **Node 3:** $1 \to 3 \quad (\hat{c} = 40)$
4. **Node 4:** $1 \to 4 \quad (\hat{c} = 40)$

**Selection:** Node 6 has the minimal bound ($\hat{c} = 35$). Extract Node 6 as E-node.

---

### Step 6: Completing the Tour from Node 6 (Path: $1 \to 2 \to 4$)

From Node 6, the only remaining unvisited vertex is $\{3\}$.
The remaining path is deterministic:
$$\text{From } 4 \to 3, \quad \text{and from } 3 \to 1 \text{ (return to origin)}$$

Let this terminal leaf state be **Node 7**.

Inspect the entries in matrix $A_6$:
- Edge $(4, 3)$: Look at Row 4, Column 3 in $A_6$:
  $$A_6[4, 3] = 0$$
- Edge $(3, 1)$: Look at Row 3, Column 1 in $A_6$:
  $$A_6[3, 1] = 0$$

The final lower bound at the leaf is:
$$\hat{c}(7) = \hat{c}(6) + A_6[4, 3] + A_6[3, 1] + 0 = 35 + 0 + 0 = 35$$

Since Node 7 is a leaf representing a complete, valid Hamiltonian tour:
$$\text{Complete Tour: } 1 \to 2 \to 4 \to 3 \to 1$$
We establish the **Global Upper Bound**:
$$U \leftarrow \min(\infty, 35) = 35$$

---

### Step 7: Verification Against Original Cost Matrix $C$

Let us compute the true cost of tour $1 \to 2 \to 4 \to 3 \to 1$ directly from the original problem input:
$$C[1, 2] = 10$$
$$C[2, 4] = 10$$
$$C[4, 3] = 9$$
$$C[3, 1] = 6$$

Summing the direct edge costs:
$$\text{Total Cost} = 10 + 10 + 9 + 6 = 35$$

The computed bound $\hat{c}(7) = 35$ matches the true tour cost with zero discrepancy.

---

### Step 8: Global Pruning and Search Termination

The algorithm now checks the remaining live nodes in the Priority Queue against the tightened bound $U = 35$:

1. **Next candidate in PQ:** Node 5 ($\hat{c} = 39$).
   $$\text{Check: } \hat{c}(5) \ge U \implies 39 \ge 35 \quad \implies \quad \textbf{PRUNED!}$$
2. **Next candidate in PQ:** Node 3 ($\hat{c} = 40$).
   $$\text{Check: } \hat{c}(3) \ge U \implies 40 \ge 35 \quad \implies \quad \textbf{PRUNED!}$$
3. **Next candidate in PQ:** Node 4 ($\hat{c} = 40$).
   $$\text{Check: } \hat{c}(4) \ge U \implies 40 \ge 35 \quad \implies \quad \textbf{PRUNED!}$$

All remaining candidate branches are eliminated without further expansion.  
The search terminates. The mathematically certified global optimal tour is:
$$1 \to 2 \to 4 \to 3 \to 1 \quad \text{with optimal cost } C^* = 35$$

---

## 5. Complete ASCII State-Space Tree Diagram

```text
                                 [Node 1: Root]
                                 Partial Tour: [1]
                                 ĉ(1) = 35, U = ∞
                     +-------------------+-------------------+
                     | (1,2)             | (1,3)             | (1,4)
                     | A_1[1,2]=0        | A_1[1,3]=4        | A_1[1,4]=5
                     | r=0               | r=1               | r=0
                     v                   v                   v
              [Node 2: 1->2]      [Node 3: 1->3]      [Node 4: 1->4]
              ĉ(2) = 35           ĉ(3) = 40           ĉ(4) = 40
              (Extracted min)     (In PQ)             (In PQ)
             +-------+-------+
             |               |
       (2,3) | A_2[2,3]=3    | (2,4) A_2[2,4]=0
             | r=1           | r=0
             v               v
      [Node 5: 1->2->3]   [Node 6: 1->2->4]
      ĉ(5) = 39           ĉ(6) = 35
      (In PQ)             (Extracted min)
                             |
                       (4,3) | A_6[4,3]=0
                       (3,1) | A_6[3,1]=0
                             v
                     =================================
                     *       [Node 7: LEAF]          *
                     *  Tour: 1 -> 2 -> 4 -> 3 -> 1  *
                     *  True Cost = 35               *
                     *  U is updated: U = 35         *
                     =================================
                             |
          +------------------+------------------+
          |                                     |
          v                                     v
   [Prune Node 5]                        [Prune Nodes 3 & 4]
   ĉ(5) = 39 >= U (35)                  ĉ(3)=40, ĉ(4)=40 >= U (35)
   [DEAD NODE]                           [DEAD NODES]
```

---

## 6. Algorithmic Comparison & Complexity Analysis

The table below contrasts Branch and Bound with alternative paradigms for solving the Traveling Salesperson Problem:

| Paradigm / Algorithm | Design Principle | Worst-Case Time Complexity | Auxiliary Space Complexity | Optimality Guarantee | Practical Scale Limit |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Brute-Force Enumeration** | Exhaustive factorial permutation | $\mathcal{O}((n-1)!)$ | $\mathcal{O}(n)$ | Global Optimum Guaranteed | $n \le 10$ |
| **Dynamic Programming (Held-Karp)** | Overlapping sub-problems & memoization | $\mathcal{O}(n^2 2^n)$ | $\mathcal{O}(n 2^n)$ | Global Optimum Guaranteed | $n \le 22$ |
| **Branch and Bound (LC-B&B)** | State-space pruning via matrix reduction | $\mathcal{O}((n-1)!)$ | $\mathcal{O}((n-1)!)$ | Global Optimum Guaranteed | $n \le 40 - 60$ |
| **Nearest Neighbor Heuristic** | Greedy local choice | $\mathcal{O}(n^2)$ | $\mathcal{O}(n)$ | **No Guarantee** (sub-optimal) | $n > 10,000$ |

### 6.1 Performance Analysis of LC-B&B:
1. **Worst-Case Time Complexity:** If the cost matrix values produce identical bounds across subtrees, pruning cannot eliminate branches early, and LC-B&B deteriorates to factorial search:
   $$\mathcal{T}_{\text{worst}}(n) = \mathcal{O}((n-1)!)$$
2. **Matrix Reduction Overhead:** At each node in the tree, generating the modified matrix and performing row and column reductions on an $n \times n$ table requires:
   $$\mathcal{O}(n^2) \text{ time per node}$$
3. **Space Complexity:** Because unexpanded live nodes must be maintained simultaneously in the Min-Priority Queue, the worst-case space complexity is proportional to the maximum width of the state-space tree:
   $$\mathcal{S}_{\text{worst}}(n) = \mathcal{O}((n-1)!)$$
   This memory consumption is the primary bottleneck of Branch and Bound on large instances, making heuristic methods (e.g., Lin-Kernighan, Simulated Annealing, Genetic Algorithms) preferable when $n > 100$.

---

## 7. KTU Examination High-Yield Preparation

---

### Question 1 (3 Marks): State the four rules for updating the cost matrix when branching on edge $(i, j)$ in TSP Branch and Bound.

#### Model Answer:
When branching from parent state $P$ to child state along edge $(i, j)$:
1. **Row Invalidation:** Change all elements in Row $i$ to $\infty$ (ensures the tour leaves vertex $i$ only once).
2. **Column Invalidation:** Change all elements in Column $j$ to $\infty$ (ensures the tour enters vertex $j$ only once).
3. **Sub-tour Invalidation:** Change entry $M[j, 1]$ (or $M[j, \text{start}]$) to $\infty$ to prevent forming an early disconnected cycle.
4. **Child Matrix Reduction:** Reduce the resulting matrix by subtracting row and column minimums. The child lower bound is:
   $$\hat{c}(\text{child}) = \hat{c}(\text{parent}) + A_{\text{parent}}[i, j] + r$$
   where $r$ is the sum of all row and column reduction subtractions.

---

### Question 2 (5 Marks): Prove that the sum of row and column reductions in a cost matrix is an admissible lower bound for the Travelling Salesperson Problem.

#### Model Answer:
1. Let $C$ be an $n \times n$ TSP cost matrix. Any valid tour $T$ is a simple cycle of $n$ edges visiting each vertex once.
2. **Out-degree Property:** In tour $T$, exactly one edge departs from each row $i$. Subtracting a constant $r_i$ from every entry in row $i$ reduces the cost of every feasible tour by exactly $r_i$. Therefore, subtracting all row minimums reduces total tour cost by:
   $$R_{\text{row}} = \sum_{i=1}^n r_i$$
3. **In-degree Property:** In tour $T$, exactly one edge arrives at each column $j$. Subtracting a constant $c_j$ from every entry in column $j$ reduces the cost of every feasible tour by exactly $c_j$. Total column reduction is:
   $$R_{\text{col}} = \sum_{j=1}^n c_j$$
4. Let $A$ be the resulting reduced matrix, and $R = R_{\text{row}} + R_{\text{col}}$. For every valid tour $T$:
   $$\text{Cost}_C(T) = \text{Cost}_A(T) + R$$
5. Because every entry in $A$ is non-negative ($A[i, j] \ge 0$), the tour cost under $A$ satisfies $\text{Cost}_A(T) \ge 0$.
6. Thus:
   $$\text{Cost}_C(T) \ge R \quad \forall \; T$$
Because $R$ never exceeds the cost of any tour, it is an admissible lower bound.

---

### Question 3 (10-Mark Problem): Solve the 4-City TSP using LC-Branch and Bound.

```text
         [ ∞  10  15  20 ]
     C = [  5   ∞   9  10 ]
         [  6  13   ∞  12 ]
         [  8   8   9   ∞ ]
```

#### Evaluation Checklist:
1. **Root Matrix Reduction:** Show Row Minimums $(10, 5, 6, 8) \implies R_{\text{row}} = 29$. Show Column Minimums $(0, 0, 1, 5) \implies R_{\text{col}} = 6$. Initial Lower Bound $\hat{c}(1) = 35$. *(3 Marks)*
2. **First Level Expansion:** Correctly compute child bounds:
   - Edge $(1, 2) \implies \hat{c}(2) = 35$
   - Edge $(1, 3) \implies \hat{c}(3) = 40$
   - Edge $(1, 4) \implies \hat{c}(4) = 40$ *(3 Marks)*
3. **Second Level Expansion:** Select Node 2 (min bound 35). Correctly branch to Node 5 ($\hat{c} = 39$) and Node 6 ($\hat{c} = 35$). *(2 Marks)*
4. **Leaf Solution & Pruning:** Expand Node 6 to leaf Node 7 ($1 \to 2 \to 4 \to 3 \to 1$) with cost $35$. Set $U = 35$. Formally prune nodes 5, 3, and 4 since their lower bounds ($39, 40, 40$) are $\ge U$. Conclude optimal tour and cost. *(2 Marks)*
