# Progressive Problems: Single-Source Shortest Paths (Dijkstra's Algorithm & Failure Modes)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic algebra.

---

## Level 1: Full Step-by-Step Dijkstra Trace with Table Evolution

### Problem 1.1: Tracing Shortest Paths from Source $S$

Given directed graph $G = (V, E)$ with non-negative edge weights:
* Vertices: $V = \{S, A, B, C, D\}$
* Directed edges and weights:
  * $(S, A): 10$
  * $(S, C): 5$
  * $(A, B): 1$
  * $(A, C): 2$
  * $(C, A): 3$
  * $(C, B): 9$
  * $(C, D): 2$
  * $(B, D): 4$
  * $(D, B): 6$
  * $(D, S): 7$

Compute the shortest path distances and predecessors from source vertex $S$ to all other vertices using Dijkstra's algorithm.

::: callout-intuition Core Mental Model
Imagine you drop a pebble into water at source vertex $S$.
A ripple expands outward at constant speed.
* The first town the ripple hits is the closest town to $S$. Because all travel times are positive, no future path can ever reach this town faster than the current direct ripple!
* We finalize this town's distance permanently, and use it as a new springboard to send ripples further down the road network.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Initialization</summary>

**What are we doing?** Initialize distance estimates $d[u]$ to infinity, $d[S] = 0$, and predecessors $\pi[u] = \text{NIL}$.

| Vertex | $d[v]$ | $\pi[v]$ | Finalized? |
| :---: | :---: | :---: | :---: |
| **$S$** | **0** | NIL | No |
| $A$ | $\infty$ | NIL | No |
| $B$ | $\infty$ | NIL | No |
| $C$ | $\infty$ | NIL | No |
| $D$ | $\infty$ | NIL | No |

Unvisited set $Q = \{S, A, B, C, D\}$.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Extract Min Vertex S (d[S] = 0)</summary>

* Minimum vertex in $Q$ is $S$ with $d[S] = 0$.
* Mark $S$ as finalized ($S \in \text{Visited}$).
* **Relax outgoing edges from $S$:**
  * Edge $(S, A)$: $d[A] > d[S] + w(S, A) \implies \infty > 0 + 10 \implies \mathbf{d[A] = 10, \pi[A] = S}$.
  * Edge $(S, C)$: $d[C] > d[S] + w(S, C) \implies \infty > 0 + 5 \implies \mathbf{d[C] = 5, \pi[C] = S}$.

Table after Step 2:
* $d$: $S: 0^*, A: 10, B: \infty, C: 5, D: \infty$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Extract Min Vertex C (d[C] = 5)</summary>

* Minimum unvisited vertex is $C$ with $d[C] = 5$.
* Mark $C$ as finalized.
* **Relax outgoing edges from $C$ ($\{(C, A), (C, B), (C, D)\}$):**
  * Edge $(C, A)$: $d[A] > d[C] + w(C, A) \implies 10 > 5 + 3 = 8 \implies \mathbf{d[A] = 8, \pi[A] = C}$. (Path $S \to C \to A$ is shorter than $S \to A$!)
  * Edge $(C, B)$: $d[B] > d[C] + w(C, B) \implies \infty > 5 + 9 = 14 \implies \mathbf{d[B] = 14, \pi[B] = C}$.
  * Edge $(C, D)$: $d[D] > d[C] + w(C, D) \implies \infty > 5 + 2 = 7 \implies \mathbf{d[D] = 7, \pi[D] = C}$.

Table after Step 3:
* $d$: $S: 0^*, A: 8, B: 14, C: 5^*, D: 7$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Extract Min Vertex D (d[D] = 7)</summary>

* Minimum unvisited vertex is $D$ with $d[D] = 7$.
* Mark $D$ as finalized.
* **Relax outgoing edges from $D$ ($\{(D, B), (D, S)\}$):**
  * Edge $(D, B)$: $d[B] > d[D] + w(D, B) \implies 14 > 7 + 6 = 13 \implies \mathbf{d[B] = 13, \pi[B] = D}$.
  * Edge $(D, S)$: $S$ is already finalized; $0 \le 7 + 7 = 14$, no update.

Table after Step 4:
* $d$: $S: 0^*, A: 8, B: 13, C: 5^*, D: 7^*$
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Extract Min Vertex A (d[A] = 8)</summary>

* Minimum unvisited vertex is $A$ with $d[A] = 8$.
* Mark $A$ as finalized.
* **Relax outgoing edges from $A$ ($\{(A, B), (A, C)\}$):**
  * Edge $(A, B)$: $d[B] > d[A] + w(A, B) \implies 13 > 8 + 1 = 9 \implies \mathbf{d[B] = 9, \pi[B] = A}$.
  * Edge $(A, C)$: $C$ is finalized; $5 \le 8 + 2 = 10$, no update.

Table after Step 5:
* $d$: $S: 0^*, A: 8^*, B: 9, C: 5^*, D: 7^*$
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Extract Min Vertex B (d[B] = 9)</summary>

* Minimum unvisited vertex is $B$ with $d[B] = 9$.
* Mark $B$ as finalized.
* Outgoing edge $(B, D)$: $7 \le 9 + 4 = 13$, no update.
* All vertices are now finalized ($Q = \emptyset$). Algorithm terminates.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Complete Shortest Path Summary</summary>

**Final Distances and Paths from Source $S$:**

| Destination | Shortest Distance | Path String |
| :---: | :---: | :---: |
| **$S$** | **0** | $S$ |
| **$A$** | **8** | $S \to C \to A$ |
| **$B$** | **9** | $S \to C \to A \to B$ |
| **$C$** | **5** | $S \to C$ |
| **$D$** | **7** | $S \to C \to D$ |

</details>

</div>

---

## Level 2: Negative Edge Counterexample (Proof of Greedy Failure)

### Problem 2.1: Constructing the Minimal Counterexample

Demonstrate using a 3-vertex directed graph that Dijkstra's algorithm produces an incorrect shortest path distance when a negative edge weight is present.

::: callout-intuition Core Mental Model
Dijkstra's algorithm is greedy: once it closes the book on a vertex and marks it "finalized," it assumes that no detour down other roads could ever make the path to that vertex shorter.
A negative edge acts like a "time machine" or a "rebate voucher." If you take a longer road that suddenly offers a massive cash-back rebate (negative cost), your total trip cost drops below what Dijkstra thought was impossible.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Graph Construction</summary>

Consider the 3-vertex directed graph $V = \{A, B, C\}$:
* $(A, B): 3$
* $(A, C): 5$
* $(C, B): -4$  *(Negative weight edge!)*
Source vertex is $A$.

```
                        ( A )
                       /     \
                   3  /       \  5
                     v         v
                   ( B ) <---- ( C )
                           -4
```
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Trace Dijkstra's Algorithm (Greedy Execution)</summary>

1. **Init:** $d[A] = 0$, $d[B] = \infty$, $d[C] = \infty$.
2. **Extract $A$ ($0$):**
   * Relax $(A, B)$: $d[B] = \min(\infty, 0 + 3) = 3, \; \pi[B] = A$.
   * Relax $(A, C)$: $d[C] = \min(\infty, 0 + 5) = 5, \; \pi[C] = A$.
   * $A$ is finalized.
3. **Extract Min from $\{B, C\}$:**
   * $\min(d[B] = 3, \; d[C] = 5) \implies \mathbf{B \text{ is extracted!}}$
   * **Dijkstra marks $B$ as PERMANENTLY FINALIZED with $d[B] = 3$.**
4. **Extract $C$ ($5$):**
   * Relax $(C, B)$: Dijkstra's standard invariant dictates that $B$ is already finalized and cannot be re-opened, or if checked:
     $$d[C] + w(C, B) = 5 + (-4) = 1 < d[B] (3)$$
   * Because $B$ was already closed, the greedy assumption that $d[B] = 3$ was optimal is **falsified**.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Comparative Conclusion</summary>

* **Dijkstra's Output:** $d[B] = \mathbf{3}$ via path $A \to B$.
* **True Shortest Distance:** $d[B] = \mathbf{1}$ via path $A \to C \to B$ (Cost: $5 - 4 = 1$).
* **Conclusion:** Dijkstra fails because greedy finalization breaks when edge weights can decrease total path cost. Negative edges require algorithms designed for them, such as **Bellman-Ford** ($O(V \cdot E)$).
</details>

</div>
