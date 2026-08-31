# Strongly Connected Components (SCC): Kosaraju's Algorithm

**Transposed graph G^T, reverse topological ordering, and two-pass linear time decomposition.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
In a directed graph — think of it as a network of one-way streets — two locations $u$ and $v$ are said to be **strongly connected** if you can drive from $u$ to $v$ *and* also drive back from $v$ to $u$, obeying all the one-way restrictions both times. A **strongly connected component (SCC)** is a maximal group of locations where *every* pair within the group can reach each other this way — think of it as a tightly-knit neighbourhood of mutual reachability, sitting inside a bigger city of one-way streets that, overall, might not let you loop back to where you started at all.

**Kosaraju's algorithm** finds all SCCs in a directed graph using a beautifully clever two-pass trick: first, do a DFS on the *original* graph and record the order in which vertices *finish* (are fully explored) — this ordering turns out to encode crucial structural information about which SCCs can "reach" which other SCCs. Then, reverse *every single edge* in the graph (creating the **transpose graph**, $G^T$ — every one-way street now points the opposite direction), and do a *second* DFS on this transposed graph, but crucially, processing vertices in the *reverse* of the finishing order from the first pass. Each individual tree produced by this second DFS turns out to be exactly one complete SCC — no more, no less. It's a strange, almost magical-feeling result the first time you see it work, but it follows from solid graph theory, unpacked below.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Kosaraju's algorithm — the three steps:**

1. **Pass 1:** run DFS on the original graph $G$ (using the standard "for each unvisited vertex, DFS-Visit" outer loop, to cover the whole graph even if disconnected). Record the finishing time of every vertex, and build a list of vertices ordered by *decreasing* finish time (the vertex that finished *last* comes first in this list).

2. **Transpose:** construct $G^T$, the graph with every edge direction reversed — an edge $u \to v$ in $G$ becomes $v \to u$ in $G^T$. Crucially, $G^T$ has *exactly the same SCCs* as $G$ (this is the structural fact the whole algorithm leans on — reversing every edge doesn't change which groups of vertices can mutually reach each other, since "$u$ can reach $v$ and $v$ can reach $u$" is symmetric under simultaneously reversing all edges).

3. **Pass 2:** run DFS on $G^T$, but process vertices in the order determined by Pass 1's list (decreasing original finish time — i.e., process the vertex that finished *last* in Pass 1, first, in Pass 2). Each separate DFS tree produced in this second pass is exactly one SCC.

**Why this works — the key structural insight (informal).** Think of "condensing" each SCC of the original graph down into a single super-vertex; the resulting graph of super-vertices (called the **condensation**) is always a DAG (Directed Acyclic Graph — no cycles among the super-vertices, since if two SCCs could reach each other in *both* directions, they'd actually be the *same* SCC, contradicting maximality). Pass 1's decreasing-finish-time order happens to always list the super-vertex with *no outgoing edges left in the condensation DAG* — a "sink" SCC — *last* to finish, meaning it appears *first* in the Pass-1 ordering used for Pass 2. Working through $G^T$ (where all the condensation DAG's edges are now reversed) in that specific order guarantees that starting a new DFS tree in Pass 2 can never accidentally "leak" into a different SCC, because by the time you'd try to reach another SCC's vertices, they're either already visited (safe) or — thanks to the reversed edges and the careful ordering — genuinely unreachable from where you currently are without first passing back through your own SCC.

**Time complexity:** two full DFS passes, each $O(V+E)$, plus $O(V+E)$ to build the transpose graph — overall, $O(V+E)$, i.e. still linear in the size of the graph, remarkably efficient for a problem that sounds like it should require comparing every pair of vertices.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Given a directed graph with edges $A\to B$, $B\to C$, $C\to A$, $C\to D$, $D\to E$, $E\to D$, find all strongly connected components using Kosaraju's algorithm.
:::

::: step [Step 2: Execution] Applying Core Algorithm
**Pass 1 (DFS on original graph, starting from $A$):** $A\to B\to C$; from $C$, explore $C\to A$ (already GRAY, skip — it's a back edge, not relevant to finish-time bookkeeping here) then $C\to D\to E$; from $E$, explore $E\to D$ (already GRAY, skip). $E$ finishes first (say, at time 5), then $D$ (time 6), then $C$ (time 7), then $B$ (time 8), then $A$ (time 9). Decreasing-finish-time order: $A, B, C, D, E$.
**Transpose $G^T$:** reverse every edge: $B\to A$, $C\to B$, $A\to C$, $D\to C$, $E\to D$, $D\to E$.
**Pass 2 (DFS on $G^T$, processing in order $A, B, C, D, E$):** start `DFS-Visit(A)` on $G^T$: from $A$, follow $A\to C$; from $C$, follow $C\to B$; from $B$, follow $B\to A$ (already visited — stop). This first DFS tree covers $\{A, C, B\}$ — one SCC. Next unvisited in the order: $D$. `DFS-Visit(D)` on $G^T$: from $D$, follow both $D\to C$ (already visited, skip) and $D\to E$; from $E$, follow $E\to D$ (already visited, stop). This second DFS tree covers $\{D, E\}$ — a second SCC.
:::

::: step [Step 3: Conclusion] Final Result
Kosaraju's algorithm correctly identifies exactly two strongly connected components: $\{A, B, C\}$ (which indeed mutually reach each other via the cycle $A\to B\to C\to A$) and $\{D, E\}$ (which mutually reach each other via $D\to E\to D$). Notice $C$ can reach $D$ (via the edge $C\to D$), but $D$ cannot reach back to $C$ (no path exists from $\{D,E\}$ back into $\{A,B,C\}$) — exactly why these are two *separate* SCCs, not one combined SCC, even though the whole graph is connected when direction is ignored.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
What is the correct three-step sequence of Kosaraju's algorithm?
(A) Compute the transpose graph, then run a single DFS, then reverse the results
(*B) Run DFS on the original graph recording finish times, construct the transpose graph $G^T$, then run DFS on $G^T$ processing vertices in decreasing order of the finish times recorded in the first pass
(C) Run BFS twice, once on the original graph and once on the transpose
(D) Sort all vertices alphabetically, then run a single DFS
::: explanation
Kosaraju's algorithm is defined by exactly this two-DFS-pass structure: first pass on the original graph to establish a finishing-time ordering, then transpose the graph, then a second pass on the transpose processed in that specific (decreasing finish-time) order — each resulting DFS tree in the second pass is exactly one SCC.
:::

::: quiz Q2: Foundational Concept
Why does reversing every edge in the graph (constructing $G^T$) not change the set of strongly connected components?
(A) It does change them; SCCs must always be recomputed from scratch for $G^T$
(*B) "$u$ can reach $v$ and $v$ can reach $u$" is a symmetric relationship, so simultaneously reversing every edge in the graph preserves exactly which groups of vertices can mutually reach one another
(C) Reversing edges always merges all SCCs into one
(D) $G^T$ always has zero edges
::: explanation
Strong connectivity between $u$ and $v$ requires a path each way. If you reverse *every* edge in the entire graph, any path from $u$ to $v$ in the original becomes a path from $v$ to $u$ in the transpose, and vice versa — so the mutual-reachability relationship (and therefore the SCC groupings) stays exactly the same, just with the roles of "forward" and "backward" paths swapped.
:::

::: quiz Q3: Foundational Concept
What is the overall time complexity of Kosaraju's algorithm on a graph with $V$ vertices and $E$ edges?
(A) $O(V^2)$
(*B) $O(V+E)$
(C) $O(V \cdot E)$
(D) $O(E \log E)$
::: explanation
Kosaraju's algorithm performs two DFS traversals (each $O(V+E)$) and one graph transposition (also $O(V+E)$) — all linear in the size of the graph — so the total remains $O(V+E)$, the same asymptotic efficiency as a single DFS pass.
:::
