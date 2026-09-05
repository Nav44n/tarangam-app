# Progressive Problems: Minimum Spanning Trees (Prim's Algorithm & Priority Queue)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic algebra.

---

## Level 1: Prim's Algorithm Trace with Explicit Priority Queue State

### Problem 1.1: Tracing Prim's Algorithm from Start Vertex $A$

Find the Minimum Spanning Tree of graph $G = (V, E)$ using Prim's algorithm starting from vertex $A$.
$V = \{A, B, C, D, E\}$, with edge weights:
* $(A, B): 4$
* $(A, C): 2$
* $(B, C): 1$
* $(B, D): 5$
* $(C, D): 8$
* $(C, E): 10$
* $(D, E): 2$
* $(D, F): 6$ (Omit $F$; 5 vertices $A, B, C, D, E$)

Vertices: $\{A, B, C, D, E\}$. Edge weights:
* $(A, B): 4$, $(A, C): 2$
* $(B, C): 1$, $(B, D): 5$
* $(C, D): 8$, $(C, E): 10$
* $(D, E): 2$

::: callout-intuition Core Mental Model
Think of Prim's algorithm as an expanding ink stain or tree root:
1. Plant a seed at root vertex $A$. The tree consists only of $\{A\}$.
2. Look at all the edges connecting a vertex **inside** the tree to a vertex **outside** the tree.
3. Pick the single cheapest crossing edge and pull that new vertex into the tree.
4. Update the distances to the remaining outside vertices.
5. Repeat until all vertices have been absorbed into the tree.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Initialize Distance Keys and Parent Pointers</summary>

**What are we doing?** For every vertex $v \in V$, we initialize its minimum connection key `key[v]` and its parent pointer `parent[v]`.

**How do we do it?**
* Start vertex $A$: `key[A] = 0`, `parent[A] = NIL`
* Other vertices: `key[B] = ∞, key[C] = ∞, key[D] = ∞, key[E] = ∞`
* `parent[B..E] = NIL`
* Visited set: $S = \emptyset$. Total MST weight = $0$.

**Priority Queue State:**
$$Q = \{ (A: 0), \; (B: \infty), \; (C: \infty), \; (D: \infty), \; (E: \infty) \}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Extract Minimum Vertex A (Cost 0)</summary>

* Minimum in $Q$ is $A$ with key $0$.
* Add $A$ to visited set: $S = \{A\}$.
* **Relax neighbors of $A$:**
  * Neighbor $B$: Edge $(A, B)$ weight $= 4 < \text{key}[B] (\infty) \implies \text{key}[B] = 4, \text{parent}[B] = A$.
  * Neighbor $C$: Edge $(A, C)$ weight $= 2 < \text{key}[C] (\infty) \implies \text{key}[C] = 2, \text{parent}[C] = A$.
* **Priority Queue after relaxation:**
  $$Q = \{ (C: 2), \; (B: 4), \; (D: \infty), \; (E: \infty) \}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Extract Minimum Vertex C (Cost 2)</summary>

* Minimum in $Q$ is $C$ with key $2$.
* Add $C$ to tree: $S = \{A, C\}$.
* Edge added to MST: $(A, C)$ with weight $2$. Total weight $= 2$.
* **Relax unvisited neighbors of $C$ ($\{B, D, E\}$):**
  * Neighbor $B$: Edge $(C, B)$ weight $= 1 < \text{key}[B] (4) \implies \mathbf{key}[B] \text{ updated to } 1, \text{parent}[B] = C$.
  * Neighbor $D$: Edge $(C, D)$ weight $= 8 < \text{key}[D] (\infty) \implies \text{key}[D] = 8, \text{parent}[D] = C$.
  * Neighbor $E$: Edge $(C, E)$ weight $= 10 < \text{key}[E] (\infty) \implies \text{key}[E] = 10, \text{parent}[E] = C$.
* **Priority Queue:**
  $$Q = \{ (B: 1), \; (D: 8), \; (E: 10) \}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Extract Minimum Vertex B (Cost 1)</summary>

* Minimum in $Q$ is $B$ with key $1$.
* Add $B$ to tree: $S = \{A, B, C\}$.
* Edge added: $(C, B)$ with weight $1$. Total weight $= 2 + 1 = 3$.
* **Relax unvisited neighbors of $B$ ($\{D\}$):**
  * Neighbor $D$: Edge $(B, D)$ weight $= 5 < \text{key}[D] (8) \implies \mathbf{key}[D] \text{ updated to } 5, \text{parent}[D] = B$.
* **Priority Queue:**
  $$Q = \{ (D: 5), \; (E: 10) \}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Extract Minimum Vertex D (Cost 5)</summary>

* Minimum in $Q$ is $D$ with key $5$.
* Add $D$ to tree: $S = \{A, B, C, D\}$.
* Edge added: $(B, D)$ with weight $5$. Total weight $= 3 + 5 = 8$.
* **Relax unvisited neighbors of $D$ ($\{E\}$):**
  * Neighbor $E$: Edge $(D, E)$ weight $= 2 < \text{key}[E] (10) \implies \mathbf{key}[E] \text{ updated to } 2, \text{parent}[E] = D$.
* **Priority Queue:**
  $$Q = \{ (E: 2) \}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Extract Minimum Vertex E (Cost 2)</summary>

* Minimum in $Q$ is $E$ with key $2$.
* Add $E$ to tree: $S = \{A, B, C, D, E\}$.
* Edge added: $(D, E)$ with weight $2$. Total weight $= 8 + 2 = 10$.
* All vertices are now visited ($Q = \emptyset$). Algorithm terminates.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: MST Summary & Edge List</summary>

* **Spanning Tree Edges:**
  * $(A, C)$: Weight $2$
  * $(C, B)$: Weight $1$
  * $(B, D)$: Weight $5$
  * $(D, E)$: Weight $2$
* **Total MST Weight:** $2 + 1 + 5 + 2 = \mathbf{10}$.
* Both Kruskal and Prim produce the identical total weight of 10 on this graph.
</details>

</div>
