# Progressive Problems: Minimum Spanning Trees (Kruskal's Algorithm & DSU)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic algebra.

---

## Level 1: Small Graph Kruskal Trace with Explicit DSU Sets

### Problem 1.1: 5-Vertex Connected Network MST

Find the Minimum Spanning Tree (MST) of the undirected connected graph $G = (V, E)$ with $V = \{A, B, C, D, E\}$ ($|V| = 5$) and edge weights given by:
* $(A, B): 1$
* $(B, C): 2$
* $(A, C): 7$
* $(C, D): 3$
* $(B, D): 4$
* $(D, E): 5$
* $(C, E): 6$

Track the Disjoint Set Union (DSU) sets explicitly at every edge evaluation.

::: callout-intuition Core Mental Model
Imagine $5$ towns that need to be connected by roads with the minimum total paving cost.
Kruskal's strategy is simple:
1. List all possible roads in order of cheapest to most expensive.
2. Build the cheapest road on the list.
3. Keep building the next cheapest road unless it connects two towns that are already linked by roads (which would form an unnecessary loop/cycle).
4. Stop as soon as you have built $|V| - 1 = 4$ roads.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Sort All Edges by Non-Decreasing Weight</div>

**What are we doing?** We create a sorted list of all $7$ edges in ascending order of their numeric weight.

**Why are we starting here?** Kruskal's algorithm greedily considers edges in order of smallest weight first.

| Edge | Weight | Status |
| :---: | :---: | :---: |
| $(A, B)$ | **1** | Pending |
| $(B, C)$ | **2** | Pending |
| $(C, D)$ | **3** | Pending |
| $(B, D)$ | **4** | Pending |
| $(D, E)$ | **5** | Pending |
| $(C, E)$ | **6** | Pending |
| $(A, C)$ | **7** | Pending |

Initial DSU partition: $\{A\}, \{B\}, \{C\}, \{D\}, \{E\}$.
Target edge count for MST: $|V| - 1 = 5 - 1 = 4$ edges.
MST edge set $T = \emptyset$, Total weight = $0$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Evaluate Edge (A, B) with Weight 1</div>

**What are we doing?** Find the set containing $A$ and the set containing $B$.
* $\text{Find}(A) = \{A\}$
* $\text{Find}(B) = \{B\}$
* Since $\text{Find}(A) \ne \text{Find}(B)$, adding $(A, B)$ **does not create a cycle**.
* **Action:** Accept edge $(A, B)$.
* **DSU Update:** $\text{Union}(A, B) \implies \{A, B\}, \{C\}, \{D\}, \{E\}$.
* $T = \{(A, B)\}$, Total weight $= 1$. Edges accepted $= 1 / 4$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Evaluate Edge (B, C) with Weight 2</div>

* $\text{Find}(B) = \{A, B\}$
* $\text{Find}(C) = \{C\}$
* Since $\{A, B\} \ne \{C\}$, no cycle is formed.
* **Action:** Accept edge $(B, C)$.
* **DSU Update:** $\text{Union}(\{A, B\}, \{C\}) \implies \{A, B, C\}, \{D\}, \{E\}$.
* $T = \{(A, B), (B, C)\}$, Total weight $= 1 + 2 = 3$. Edges accepted $= 2 / 4$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Evaluate Edge (C, D) with Weight 3</div>

* $\text{Find}(C) = \{A, B, C\}$
* $\text{Find}(D) = \{D\}$
* Sets are disjoint.
* **Action:** Accept edge $(C, D)$.
* **DSU Update:** $\text{Union}(\{A, B, C\}, \{D\}) \implies \{A, B, C, D\}, \{E\}$.
* $T = \{(A, B), (B, C), (C, D)\}$, Total weight $= 3 + 3 = 6$. Edges accepted $= 3 / 4$.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Evaluate Edge (B, D) with Weight 4 (Cycle Rejection!)</div>

* **What changed from Step 4?** Both endpoints belong to the same component!
* $\text{Find}(B) = \{A, B, C, D\}$
* $\text{Find}(D) = \{A, B, C, D\}$
* $\text{Find}(B) == \text{Find}(D)$. Adding $(B, D)$ would form cycle $B - C - D - B$.
* **Action:** **REJECT edge $(B, D)$**.
* DSU state unchanged: $\{A, B, C, D\}, \{E\}$.
* Edges accepted remains $3 / 4$.
</div>

<div class="step-card">
<div class="step-badge">Step 6: Evaluate Edge (D, E) with Weight 5</div>

* $\text{Find}(D) = \{A, B, C, D\}$
* $\text{Find}(E) = \{E\}$
* Disjoint components.
* **Action:** Accept edge $(D, E)$.
* **DSU Update:** $\text{Union}(\{A, B, C, D\}, \{E\}) \implies \{A, B, C, D, E\}$.
* $T = \{(A, B), (B, C), (C, D), (D, E)\}$.
* Total weight $= 6 + 5 = 11$. Edges accepted $= 4 / 4$.
* **Stop condition reached:** Exactly $|V| - 1 = 4$ edges chosen. Remaining edges $(C, E)$ and $(A, C)$ are skipped.
</div>

<div class="step-card">
<div class="step-badge">Final Step: MST Summary & Verification</div>

* **Selected Edges:** $\{(A, B), (B, C), (C, D), (D, E)\}$
* **Total MST Weight:** $1 + 2 + 3 + 5 = \mathbf{11}$.
* **Verification:** The resulting subgraph connects all 5 vertices with 4 edges and contains zero cycles $\implies$ valid Spanning Tree.
</div>

</div>
