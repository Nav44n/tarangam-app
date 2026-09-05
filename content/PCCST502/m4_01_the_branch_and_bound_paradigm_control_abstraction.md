# Module 4.1: The Branch and Bound Paradigm — Control Abstraction, Search Strategies, and Bounding

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search: Branch & Bound Paradigm  
**Document Classification:** Publication-Grade Theoretical Lecture Note & Algorithmic Foundation  

---

## 1. Executive Overview: The Optimization Challenge

Combinatorial optimization problems require finding a configuration $X^*$ from a finite (or countably infinite) candidate set $S$ that minimizes or maximizes an objective cost function $f(X)$:

$$\text{Minimize (or Maximize) } f(X) \quad \text{subject to} \quad X \in S_{\text{feasible}}$$

When such problems belong to the class of $NP$-hard problems—such as the Traveling Salesperson Problem (TSP), 0/1 Knapsack, Quadratic Assignment, or Job-Shop Scheduling—exhaustive brute-force enumeration incurs exponential time complexity $\mathcal{O}(k^n)$ or factorial time complexity $\mathcal{O}(n!)$.

The **Branch and Bound (B&B)** design paradigm, introduced by A. H. Land and A. G. Doig (1960) and generalized by Little et al. (1963), provides a systematic, non-heuristic state-space search framework. It guarantees finding the global mathematically optimal solution without exhaustively enumerating every candidate, pruning entire subtrees of the state-space tree whose computed numeric bounds prove they cannot contain an optimal solution.

::: callout-intuition
**Mental Model: The Rigorous Real Estate Appraiser**  
Imagine hunting for the cheapest house in an entire country divided into states, counties, and neighborhoods. 
- **Branching** is partitioning the country into geographical zones.
- **Bounding** is having an expert appraiser give an infallible guarantee: *"No house in Zone A costs less than \$500,000."*
- If you have already found a complete, habitable house in Zone B for \$420,000 (your **Global Upper Bound**), you can immediately discard Zone A and every single street inside it without stepping foot there.
:::

---

## 2. Paradigmatic Comparison: Backtracking vs. Branch and Bound

Students frequently conflate Backtracking and Branch & Bound because both traverse state-space trees. However, their underlying mathematical foundations, search mechanics, and operational domains differ fundamentally.

### 2.1 Comparative Analysis Matrix

| Evaluation Dimension | Backtracking Paradigm | Branch and Bound Paradigm |
| :--- | :--- | :--- |
| **Primary Problem Class** | **Decision Problems** (e.g., $N$-Queens, Hamiltonian Cycle) or **Enumeration Problems** (Find all valid configurations satisfying constraints). | **Combinatorial Optimization Problems** (Find the single configuration minimizing or maximizing an objective function $f(X)$). |
| **Tree Exploration Strategy** | **Depth-First Search (DFS)**. Explores deeply along a single path; backs up to the parent upon encountering a dead end. | **Breadth-First Search (BFS)** or **Best-First / Least-Cost Search**. Explores level-by-level or follows the most promising node globally. |
| **State Storage Data Structure** | Implicit or explicit **LIFO Stack** (the system call stack via recursion). | Explicit **FIFO Queue** (Breadth-First) or **Min/Max Priority Queue (Heap)** (Least-Cost). |
| **Pruning Mechanism** | **Feasibility Criteria (Implicit Constraints)**. Prunes when partial solution violates a Boolean rule (e.g., two queens attack each other, sum exceeds target $M$). | **Numeric Bounding Functions** ($\hat{c}(x)$ or $\hat{u}(x)$). Prunes when a subtree's theoretical best estimate is worse than the best known feasible solution $U$. |
| **Worst-Case Space Complexity** | $\mathcal{O}(d)$, where $d$ is the maximum depth of the state-space tree (Linear auxiliary memory). | $\mathcal{O}(b^d)$, where $b$ is the branching factor (Exponential auxiliary memory to retain active live nodes in heap/queue). |
| **Node Expansion Schedule** | Generates one child at a time; explores the subtree fully before generating siblings. | **Full Expansion**: Once a node is chosen as the E-node, **all** its valid children are generated simultaneously before selecting the next E-node. |
| **Optimality Guarantee** | Requires exhaustive tree completion to guarantee optimality if applied to optimization problems. | Discards sub-optimal regions dynamically; terminates as soon as the priority queue extracts a goal node. |

::: callout-exam
**KTU Examination Scoring Alert: The 4-Mark Comparison Question**  
A recurring KTU question asks: *"Distinguish between Backtracking and Branch and Bound approaches."*  
To secure maximum marks:
1. Always state the traversal difference: **DFS** (Backtracking) vs. **BFS / Best-First** (B&B).
2. Contrast their pruning criteria: **Constraint violation** vs. **Mathematical lower/upper bounds**.
3. Emphasize space complexity: Backtracking requires **linear space** $\mathcal{O}(n)$, whereas B&B requires **exponential space** $\mathcal{O}(2^n)$ in the worst case due to active live-node queues.
:::

---

## 3. Formal Terminology & Mathematical Foundations

To formulate algorithms under Branch and Bound, we formalize the states of nodes in the state-space tree.

```
                         [Root State]
                             |
             +---------------+---------------+
             |                               |
        (Live Node)                     (Live Node)
             |                               |
       [Chosen as E-Node]               (Unexpanded)
             |
      +------+------+
      |             |
  (Child 1)     (Child 2)
  [Evaluated]   [Evaluated]
      |             |
      v             v
  (Live Node)   [DEAD NODE] (Pruned: ĉ(x) ≥ U)
```

### 3.1 Node Classifications
1. **Live Node:** A node that has been generated in the state-space tree and whose children have not yet been produced, but which has not been pruned by the bounding function. It resides in the active queue/heap waiting for expansion.
2. **E-Node (Expansion Node):** The unique, currently active live node whose children are being generated at this precise execution instant. Once an E-node generates all its children, it ceases to be an E-node.
3. **Dead Node:** A generated node that is no longer candidate for further expansion. A node becomes dead if:
   - It is pruned immediately by the bounding function ($\hat{c}(node) \ge U$).
   - It represents an infeasible state violating explicit/implicit constraints.
   - It is a leaf node (a complete solution).
   - It has already served as an E-node and fully generated all its immediate children.

---

### 3.2 Mathematical Bounding Functions (Minimization Formulation)

Let the optimization objective be:
$$\min_{X \in S} c(X)$$

For any internal node $x$ in the state-space tree, let $S_x \subseteq S$ denote the set of all complete candidate solutions residing in the subtree rooted at $x$.

Let $c^*(x)$ denote the true minimum cost among all solutions in the subtree rooted at $x$:
$$c^*(x) = \min_{Y \in S_x} c(Y)$$

Because calculating $c^*(x)$ directly is computationally equivalent to solving the original $NP$-hard problem, we introduce an admissible bounding function $\hat{c}(x)$.

#### Definition 3.1: Admissibility (Lower Bound Property)
A lower-bounding function $\hat{c}(x)$ is **admissible** if and only if it provides a valid lower bound on the true optimal cost achievable in the subtree rooted at $x$:
$$\hat{c}(x) \le c^*(x) \quad \forall \; x \in \text{State-Space Tree}$$

Furthermore, at any terminal leaf node $z$ representing a complete feasible solution $X$:
$$\hat{c}(z) = c(X)$$

#### Definition 3.2: The Global Upper Bound ($U$)
Let $U \in \mathbb{R} \cup \{\infty\}$ denote the **Global Upper Bound**, defined as the cost of the lowest-cost complete feasible solution discovered so far during search:

$$U = \begin{cases} 
\infty, & \text{before any complete feasible solution is discovered} \\
\min \{ c(X_{\text{discovered}}) \}, & \text{the minimum cost among all discovered feasible solutions}
\end{cases}$$

#### Definition 3.3: The Pruning Invariant (Minimization)
For any candidate node $x$ generated in the tree:
$$\text{If } \hat{c}(x) \ge U, \quad \text{then Prune Node } x \text{ (Declare Dead)}$$

**Mathematical Proof of Correctness of the Pruning Invariant:**
1. Let $x$ be an active node with $\hat{c}(x) \ge U$.
2. By the admissibility condition, $\hat{c}(x) \le c^*(x)$, which implies:
   $$c^*(x) \ge \hat{c}(x)$$
3. Combining this with the condition $\hat{c}(x) \ge U$:
   $$c^*(x) \ge U$$
4. Therefore, every complete solution $Y$ in the subtree rooted at $x$ has cost:
   $$c(Y) \ge c^*(x) \ge U$$
5. Because an existing, already materialized solution achieves cost $U$, no solution derived from $x$ can strictly improve upon $U$.
6. Discarding the subtree rooted at $x$ preserves the global optimum. $\blacksquare$

::: callout-warning
**Algorithmic Trap: Dual Formulation for Maximization Problems**  
In a **Maximization Problem** (e.g., 0/1 Knapsack maximizing profit):
- We compute an **Upper Bounding Function** $\hat{u}(x)$ such that $\hat{u}(x) \ge c^*(x)$ (it must never underestimate the maximum possible profit).
- We maintain a **Global Lower Bound** $L$, representing the profit of the best feasible solution discovered so far ($L_{\text{initial}} = -\infty$).
- **Pruning Rule:** Discard node $x$ if $\hat{u}(x) \le L$.
Confusing upper and lower bounds between minimization and maximization is an immediate source of zero credit in university examinations.
:::

---

## 4. State-Space Tree Search Strategies

The sequence in which live nodes are selected to become the E-node distinguishes the three canonical Branch and Bound strategies.

```
       Search Strategies in Branch and Bound
       |
       +---> 1. FIFO Branch and Bound  (Queue / BFS)
       |
       +---> 2. LIFO Branch and Bound  (Stack / DFS-bounded)
       |
       +---> 3. LC (Least-Cost) B&B    (Min-Priority Queue / Best-First)
```

---

### 4.1 FIFO (First-In, First-Out) Branch and Bound

#### Mechanics:
- Live nodes are maintained in a standard **FIFO Queue**.
- The algorithm proceeds in pure **Breadth-First Search (BFS)** order.
- The root node is enqueued first. When a node is dequeued, it becomes the E-node. All its valid, non-pruned children are generated and enqueued at the tail of the FIFO queue.
- Search explores the state-space tree strictly level by level ($Level \; 0 \to Level \; 1 \to \dots \to Level \; d$).

#### Queue State Dynamics:
Let nodes be generated as shown:

```text
Level 0:                 (1)
                       /     \
Level 1:             (2)     (3)
                    /   \   /   \
Level 2:          (4)   (5)(6)  (7)
```

1. Insert Node 1 $\implies Queue: [1]$
2. Dequeue 1 (E-node). Generate children 2 and 3 $\implies Queue: [2, 3]$
3. Dequeue 2 (E-node). Generate children 4 and 5 $\implies Queue: [3, 4, 5]$
4. Dequeue 3 (E-node). Generate children 6 and 7 $\implies Queue: [4, 5, 6, 7]$

#### Structural Limitations:
- FIFO B&B is blind to the quality of intermediate nodes. It explores mediocre and superior subtrees with equal priority.
- Complete solutions reside at deeper levels. In FIFO, an initial feasible solution is not reached until the search reaches maximum depth across the entire width of the tree, keeping the global bound $U = \infty$ for a long period and delaying effective pruning.

---

### 4.2 LIFO (Last-In, First-Out) Branch and Bound

#### Mechanics:
- Live nodes are placed onto an explicit **LIFO Stack**.
- The most recently generated live child node becomes the next E-node.
- This mimics Depth-First Search, but with full node expansion: the E-node generates *all* its children simultaneously, pushes them onto the stack, and pops the top child for subsequent expansion.

#### Stack State Dynamics:
1. Push Node 1 $\implies Stack: [1]$
2. Pop 1 (E-node). Generate children 2 and 3. Push onto stack $\implies Stack: [2, 3]$ (assuming 3 is on top)
3. Pop 3 (E-node). Generate children 6 and 7 $\implies Stack: [2, 6, 7]$ (assuming 7 is on top)
4. Rapidly plunges down to the leaves to materialize a full feasible solution early, quickly lowering $U$ from $\infty$ to a real finite value.

#### Structural Limitations:
- Susceptible to descending deeply into sub-optimal subtrees if early branching decisions are suboptimal.

---

### 4.3 LC (Least-Cost) Branch and Bound

#### Mechanics:
- Rather than relying on arbitrary structural order (FIFO/LIFO), LC-B&B employs an intelligent **heuristic evaluation function** $\hat{c}(x)$.
- Live nodes are maintained in a **Min-Priority Queue** (typically implemented as a Binary Min-Heap or Fibonacci Heap) keyed on their lower bound estimate $\hat{c}(x)$.
- **Selection Policy:** The E-node is always the live node with the globally smallest lower bound:
  $$\text{Next E-Node } e = \arg\min_{x \in \text{LiveNodes}} \hat{c}(x)$$

```
                                [Min-Priority Queue]
                                 /        |        \
                             [Node A]  [Node B]  [Node C]
                             ĉ(A)=12   ĉ(B)=19   ĉ(C)=25
                                |
                        Extract Min (ĉ = 12)
                                |
                                v
                           New E-Node: A
```

#### Why Least-Cost Search Dominates FIFO and LIFO:
LC-B&B is provably the most node-efficient search strategy under consistent bounding functions.

1. **Greedy Traversal Towards Optimality:** By expanding nodes with minimal $\hat{c}(x)$, the search gravitates directly toward the global minimum, uncovering near-optimal or optimal feasible solutions much earlier than BFS.
2. **Accelerated Pruning:** Because an optimal or near-optimal leaf is discovered quickly, the Global Upper Bound $U$ drops rapidly to its optimal value $c^*$. Once $U = c^*$, any node $y$ in the priority queue with $\hat{c}(y) \ge c^*$ is pruned without expansion.
3. **No Redundant Expansion of Inferior Nodes:** In FIFO, every node at level $k$ must be expanded before any node at level $k+1$, even if its lower bound indicates it is hopelessly sub-optimal. In LC-B&B, such nodes remain unexpanded at the bottom of the priority queue until search terminates.

---

## 5. Comparative Execution Trace: FIFO vs. LC-B&B

To trace the fundamental differences between FIFO and LC search strategies, consider an abstract minimization problem with the state-space tree below.

### 5.1 The Problem Graph & Bounds
Every node $i$ has an associated lower bound estimate $\hat{c}(i)$. Terminal leaf nodes represent complete feasible solutions with true cost $c(x) = \hat{c}(x)$. Target: **Find the minimum cost solution.**

```text
                         [Node 1] (ĉ = 10)
                        /                 \
            [Node 2] (ĉ = 12)         [Node 3] (ĉ = 25)
             /            \             /            \
     [Node 4] (Leaf)  [Node 5]     [Node 6]      [Node 7] (Leaf)
       c = 15          ĉ = 18       ĉ = 30           c = 28
                         |
                    [Node 8] (Leaf)
                       c = 14
```

---

### 5.2 Execution Trace: FIFO Branch and Bound

We track:
- Active Queue State
- Current E-node
- Global Upper Bound $U$ (Initialized to $U = \infty$)
- Total Nodes Generated and Expanded

#### FIFO Step-by-Step State Evolution:

| Step | Current E-Node | Action / Generated Children | $\hat{c}$ of Children | FIFO Queue State (Head $\to$ Tail) | Global Bound $U$ | Pruning Decisions |
| :---: | :---: | :--- | :---: | :--- | :---: | :--- |
| **0** | — | Root initialization | — | `[1]` | $\infty$ | None |
| **1** | **Node 1** | Expand 1. Generate 2, 3. | $\hat{c}(2)=12, \; \hat{c}(3)=25$ | `[2, 3]` | $\infty$ | Both $\hat{c} < U$; Enqueued |
| **2** | **Node 2** | Expand 2. Generate 4, 5. | $\hat{c}(4)=15, \; \hat{c}(5)=18$ | `[3, 4, 5]` | $\infty$ | Both $\hat{c} < U$; Enqueued |
| **3** | **Node 3** | Expand 3. Generate 6, 7. | $\hat{c}(6)=30, \; \hat{c}(7)=28$ | `[4, 5, 6, 7]` | $\infty$ | Both $\hat{c} < U$; Enqueued |
| **4** | **Node 4** | Node 4 is Leaf! Solution found. | $c(4) = 15$ | `[5, 6, 7]` | **15** | $U \leftarrow \min(\infty, 15) = 15$. Pruning threshold now 15! |
| **5** | **Node 5** | Evaluate: $\hat{c}(5) = 18 \ge 15$. | — | `[6, 7]` | 15 | **PRUNED!** $\hat{c}(5) \ge U$. Node 5 killed! |
| **6** | **Node 6** | Evaluate: $\hat{c}(6) = 30 \ge 15$. | — | `[7]` | 15 | **PRUNED!** $\hat{c}(6) \ge U$. Node 6 killed! |
| **7** | **Node 7** | Evaluate: $c(7) = 28 \ge 15$. | — | `[]` (Empty) | 15 | **PRUNED!** $c(7) \ge U$. Search Ends. |

::: callout-warning
**Disaster in FIFO Search:**  
Notice that Node 5 was **pruned** at Step 5 because $U = 15$ had already been established by Node 4. However, hidden inside Node 5's subtree was Node 8 with cost **$c(8) = 14$**! 

Why did this happen? Because $\hat{c}(5) = 18 > 14$, the bounding function was **inadmissible** (it overestimated the cost in Node 5's subtree). This demonstrates why lower bounds **must be admissible** ($\hat{c}(x) \le c^*(x)$). If $\hat{c}$ were admissible, say $\hat{c}(5) = 13$, Node 5 would not have been incorrectly pruned.
:::

---

### 5.3 Execution Trace: LC (Least-Cost) Branch and Bound

Assuming an admissible estimate: let $\hat{c}(5) = 13 \le 14$. Let us trace LC-B&B.

#### Initial Setup:
- Priority Queue (Min-Heap): `PQ = []`
- $U = \infty$
- Root Node 1 with $\hat{c}(1) = 10$.

#### LC Step-by-Step State Evolution:

| Step | Selected E-Node ($\min \hat{c}$) | Generated Children | Bounds ($\hat{c}$) | Min-Priority Queue State (Key: $\hat{c}$) | Global Bound $U$ | Operational Remarks |
| :---: | :---: | :--- | :---: | :--- | :---: | :--- |
| **0** | — | Initialize Root | — | `[(1, ĉ=10)]` | $\infty$ | Heap initialized |
| **1** | **Node 1** ($\hat{c}=10$) | Generate 2, 3 | $\hat{c}(2)=12, \; \hat{c}(3)=25$ | `[(2, ĉ=12), (3, ĉ=25)]` | $\infty$ | Both enqueued into Min-Heap |
| **2** | **Node 2** ($\hat{c}=12$) | Generate 4, 5 | $\hat{c}(4)=15, \; \hat{c}(5)=13$ | `[(5, ĉ=13), (4, ĉ=15), (3, ĉ=25)]` | $\infty$ | Node 5 is smallest, moves to top! |
| **3** | **Node 5** ($\hat{c}=13$) | Generate 8 | $c(8) = 14$ (Leaf) | `[(8, c=14), (4, ĉ=15), (3, ĉ=25)]` | $\infty$ | Node 8 is a leaf; enqueued |
| **4** | **Node 8** ($c=14$) | **Leaf Node Extracted!** | $c(8) = 14$ | `[(4, ĉ=15), (3, ĉ=25)]` | **14** | **Optimal Solution Established!** |
| **5** | **Termination** | Next in PQ: Node 4 ($\hat{c}=15$) | — | `[]` | 14 | Since $\min_{x \in PQ} \hat{c}(x) = 15 \ge U = 14$, all remaining nodes are pruned! |

#### Comparison of Search Efficiency:
- **FIFO Nodes Expanded:** 1, 2, 3 (expanded completely blind of cost).
- **LC-B&B Nodes Expanded:** 1, 2, 5 (Node 3 was never expanded; Nodes 6 and 7 were never even generated!).
- **LC-B&B saved generation of 2 entire nodes** and uncovered the true global optimum $X^* = \text{Node } 8$ with cost $14$.

---

## 6. General Control Abstraction for LC-Branch and Bound

Below is the general, deterministic control abstraction for Least-Cost Branch and Bound applied to a minimization problem.

```text
Algorithm LeastCostBranchAndBound(root)
// Input: root of the state-space tree
// Output: An optimal solution vector X* and its minimum cost U
begin
    // Step 1: Initialize Global Tracking Variables
    U := infinity;                     // Global Upper Bound of best solution
    best_solution := NIL;              // Pointer to optimal leaf state
    
    // Step 2: Initialize Min-Priority Queue (Heap)
    PQ := CreateEmptyMinPriorityQueue();
    
    // Evaluate root node bounding estimate
    c_hat_root := ComputeLowerBound(root);
    
    if (c_hat_root >= U) then
        return NIL;                    // Root is infeasible
    end if;
    
    // Assign root attributes and insert into PQ
    root.cost_estimate := c_hat_root;
    Insert(PQ, root);
    
    // Step 3: Central Expansion Loop
    while (not IsEmpty(PQ)) do
        // Extract the live node with the lowest lower bound
        e_node := DeleteMin(PQ);
        
        // Critical Pruning Check:
        // If the lowest bound in the queue meets or exceeds U,
        // no remaining node can beat the current best solution.
        if (e_node.cost_estimate >= U) then
            break;                     // Global optimality certified; terminate!
        end if;
        
        // Step 4: Full Child Generation for E-Node
        for each child in GenerateChildren(e_node) do
            
            if (IsFeasible(child)) then
                
                if (IsLeafSolution(child)) then
                    // Child represents a complete candidate solution
                    solution_cost := ComputeTrueCost(child);
                    
                    if (solution_cost < U) then
                        U := solution_cost;             // Tighten Global Upper Bound
                        best_solution := child;         // Update optimal solution
                        Print("New best solution found with cost: ", U);
                    end if;
                    // Leaves are dead nodes; do not insert into PQ
                    
                else
                    // Child is an internal state; compute its lower bound
                    c_hat := ComputeLowerBound(child);
                    
                    // Branch and Bound Pruning Test
                    if (c_hat < U) then
                        child.cost_estimate := c_hat;
                        Insert(PQ, child);              // Enqueue as Live Node
                    else
                        // Pruning event: Kill child immediately
                        Discard(child);                 // Dead Node
                    end if;
                    
                end if; // end leaf check
                
            else
                Discard(child);                         // Infeasible; Dead Node
            end if; // end feasibility check
            
        end for; // end child loop
        
        // e_node is now fully expanded and becomes a Dead Node
    end while;
    
    return best_solution, U;
end;
```

---

## 7. Theoretical Principles of Bounding Functions

The performance of Branch and Bound hinges on the mathematical tightness of the bounding function.

```
       Under-estimation gap (Search Waste)
  0 ------------------ ĉ(x) ============ c*(x) ---------------- True Optimum
                     [Lower Bound]      [Exact Min]
```

### 7.1 The Precision-Tractability Tradeoff
1. **Trivial Lower Bound ($\hat{c}(x) = 0$ or $-\infty$):**
   - Computation time: $\mathcal{O}(1)$.
   - Pruning capacity: **Zero**. No nodes pruned; LC-B&B degenerates into brute-force Breadth-First Search.
2. **Exact Minimum Bound ($\hat{c}(x) = c^*(x)$):**
   - Computation time: Exponential $\mathcal{NP}$-hard. Computing the bound takes as long as solving the entire problem.
   - Pruning capacity: **Optimal**. Explores only nodes along the exact optimal path.
3. **Ideal Practical Lower Bound:**
   - Computation time: Polynomial ($\mathcal{O}(n)$, $\mathcal{O}(n \log n)$, or $\mathcal{O}(n^2)$).
   - Pruning capacity: Close to $c^*(x)$ so that large portions of the state-space tree are pruned early.

### 7.2 Monotonicity (Consistency) Condition
A lower bounding function $\hat{c}$ is said to be **monotone** (or consistent) if for every node $x$ and every child $y$ of $x$:
$$\hat{c}(x) \le \hat{c}(y)$$

**Implication:** As search descends deeper into the state-space tree, the accumulated choices provide more information, causing the lower bound to monotonically increase toward the true solution cost. Monotonicity prevents premature or contradictory pruning decisions down a path.

---

## 8. KTU High-Yield Examination Preparation

This section provides concise, examination-targeted answers to questions frequently asked in KTU examinations under the 2024 scheme.

---

### Question 1 (3 Marks): Distinguish between an E-node and a Live Node in Branch and Bound.

#### Model Answer:
| Attribute | Live Node | E-Node (Expansion Node) |
| :--- | :--- | :--- |
| **Definition** | Any generated node that has not been pruned and whose children have not yet been generated. | The single active live node currently being processed to generate all of its children. |
| **Cardinality** | Multiple live nodes can exist simultaneously (stored in the queue or heap). | Exactly **one** E-node exists at any single instant of algorithmic execution. |
| **Storage Location** | Resides inside the FIFO Queue, LIFO Stack, or Min-Priority Queue. | Extracted from the front of the queue/heap; resides in CPU local execution variables. |

---

### Question 2 (3 Marks): Explain why Least-Cost (LC) search is superior to FIFO search in Branch and Bound.

#### Model Answer:
1. **Guided Traversal:** FIFO search explores nodes blindly in level-by-level order (Breadth-First Search). In contrast, LC search uses an admissible lower-bound heuristic function $\hat{c}(x)$ inside a Min-Priority Queue to systematically expand the globally most promising node first.
2. **Rapid Bound Tightening:** LC-B&B reaches high-quality or optimal complete solutions much earlier than FIFO. This drops the Global Upper Bound $U$ rapidly.
3. **Maximized Pruning:** Once $U$ is low, any sub-optimal nodes in the priority queue with $\hat{c}(node) \ge U$ are pruned immediately without being expanded. Consequently, LC search is guaranteed to generate and expand fewer (or at most equal) nodes compared to FIFO search.

---

### Question 3 (3 Marks): State the pruning rule for a minimization problem in Branch and Bound and explain the role of $U$.

#### Model Answer:
- **Formal Pruning Rule:** A candidate node $x$ is pruned (declared dead) if:
  $$\hat{c}(x) \ge U$$
  where $\hat{c}(x)$ is an admissible lower bound of the subtree rooted at $x$, and $U$ is the Global Upper Bound.
- **Role of $U$:** $U$ represents the cost of the best complete, valid solution discovered anywhere in the state-space tree so far ($U$ is initialized to $\infty$). Because $\hat{c}(x) \le c^*(x)$, if $\hat{c}(x) \ge U$, no solution inside $x$'s subtree can yield a cost strictly less than $U$. Thus, evaluating the subtree rooted at $x$ is guaranteed to be redundant, and it can be safely pruned without compromising global optimality.

---

### Question 4 (3 Marks): Why does Branch and Bound require exponential space in the worst case, unlike Backtracking?

#### Model Answer:
- **Backtracking (DFS):** Traverses one branch at a time. The only memory consumed is the active recursion stack, which is proportional to the tree height $d$. Thus, its auxiliary space complexity is strictly linear:
  $$\text{Space}_{\text{Backtracking}} = \mathcal{O}(d)$$
- **Branch and Bound (BFS / LC):** Must generate **all children** of an E-node simultaneously and retain all active, unexpanded candidate nodes in a FIFO queue or Min-Heap across all unexplored subtrees. In the worst case (such as when pruning is ineffective until the leaf level), the priority queue must hold all leaf-level states simultaneously:
  $$\text{Space}_{\text{B\&B}} = \mathcal{O}(b^d)$$
  where $b$ is the branching factor and $d$ is the tree depth. For binary branching ($b=2$), this requires $\mathcal{O}(2^d)$ exponential space, which can lead to memory exhaustion on large instances.

---

## 9. Comprehensive Architectural Summary

```text
================================================================================
                    THE BRANCH AND BOUND CORE ENGINE
================================================================================

      Problem Type: Combinatorial Optimization (Minimization / Maximization)
      Primary Data Structures: Min-Priority Queue (LC) / FIFO Queue (BFS)

   [ Generate Root Node ]
            |
            v
   [ Compute Bound ĉ(root) ] ---> If ĉ(root) >= U  ==> TERMINATE (Infeasible)
            |
            v
   [ Insert into Heap (PQ) ]
            |
+---------> |
|           v
|     Is PQ Empty? --------(YES)--------> [ Return Best Solution & U ]
|           |
|          (NO)
|           v
|     [ e_node = DeleteMin(PQ) ]
|           |
|     Is ĉ(e_node) >= U? --(YES)--------> [ Prune entire remaining Queue! Terminate ]
|           |
|          (NO)
|           v
|     [ Generate ALL Immediate Children ]
|           |
|     +-----+----------------------------------+
|     | For each Child:                        |
|     |                                        |
|     |   1. Is Child Infeasible?              |
|     |      --> [ KILL Child (Dead Node) ]    |
|     |                                        |
|     |   2. Is Child a Complete Solution?     |
|     |      --> If TrueCost < U:              |
|     |             U = TrueCost               |
|     |             best_solution = Child      |
|     |          [ Child is now Dead Node ]    |
|     |                                        |
|     |   3. Is Child an Internal State?       |
|     |      --> Compute ĉ(Child)              |
|     |          If ĉ(Child) < U:              |
|     |             [ Insert(PQ, Child) ]      |
|     |          Else:                         |
|     |             [ PRUNE Child (Dead Node) ]|
|     +----------------------------------------+
|           |
+-----------+
```
