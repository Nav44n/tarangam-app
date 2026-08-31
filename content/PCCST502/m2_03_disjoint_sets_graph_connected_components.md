# Application: Connected Components & Cycle Detection in Graphs

**Detecting cycles in undirected graphs and incremental dynamic connectivity.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
Now that Union-Find is fast (thanks to union by rank and path compression), here's where it earns its keep in practice: **graphs**. Picture a map of towns connected by roads, where roads are being built one at a time, and you're constantly asked two questions as construction proceeds: "can you currently get from town A to town B by some sequence of roads?" and "does the road we're about to build create a loop (a way to leave a town and eventually come back to it without retracing your steps)?"

Union-Find answers both, elegantly, using the machinery you already have: represent each town as an element, and each time a road is built between two towns, that's a `Union` call on those two towns. To check "are A and B connected?", just check `Find(A) == Find(B)`. To check "does adding this new road create a cycle?" — check *before* performing the union: if `Find(A) == Find(B)` already (they're already in the same group through some other path), then this new direct road would create a redundant, cycle-forming connection; only if they're currently in *different* groups does adding this edge genuinely connect two previously-separate pieces without forming a loop.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Connected components via Union-Find.** Given an undirected graph $G=(V,E)$, initialise a disjoint-set structure with `MakeSet(v)` for every vertex $v \in V$. Then, for every edge $(u,v) \in E$, call `Union(u,v)`. After processing all edges, two vertices are in the same **connected component** if and only if `Find(u) == Find(v)`. The total number of distinct connected components equals the number of distinct representatives (roots) remaining across all vertices.

**Cycle detection in an undirected graph.** Process edges one at a time. For each edge $(u,v)$:
- If `Find(u) == Find(v)`: $u$ and $v$ are *already* connected through some other existing path — adding this edge directly would create a **cycle**. Report the cycle (or simply skip adding this edge, depending on the application — this is exactly the core check inside Kruskal's Minimum Spanning Tree algorithm, which skips any edge that would create a cycle).
- If `Find(u) \ne Find(v)`: they are currently in different components — call `Union(u,v)` to merge them; this edge is "safe" (doesn't create a cycle).

This gives an efficient algorithm, running in roughly $O(E \cdot \alpha(V))$ time overall (near-linear, thanks to the near-constant amortized cost of each Union-Find operation) — far better than re-running a full traversal (like DFS/BFS, covered in upcoming topics) from scratch after every single edge addition.

**Incremental dynamic connectivity.** In many real applications, edges arrive *over time* (a social network gaining new friend connections, a network of computers gaining new links) rather than all being known upfront. Union-Find is naturally suited to this **incremental** ("edges only ever added, never removed") setting: each new edge triggers one `Union` call, and any "are $u$ and $v$ connected?" query is answered by a single `Find`-and-compare, without ever needing to re-scan the whole graph from scratch. This is a genuine practical advantage over graph-traversal algorithms like BFS/DFS, which would need to be re-run entirely (or at least substantially) whenever the graph structure changes.

**An important limitation.** Plain Union-Find, as covered so far, handles edges being *added* efficiently, but does *not* efficiently support edges being *removed* — there's no simple, cheap way to "undo" a Union once performed, since after a union you've lost track of exactly which original edge caused the merge. Handling edge deletions efficiently requires substantially more advanced data structures beyond this module's scope.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Given an undirected graph with vertices $\{A,B,C,D\}$ and edges added in this order: $(A,B)$, $(B,C)$, $(A,C)$, $(C,D)$. Using Union-Find, determine which edge (if any) creates a cycle, and identify the final connected component(s).
:::

::: step [Step 2: Execution] Applying Core Algorithm
Start: `MakeSet` for A, B, C, D — four separate singleton groups.
Edge $(A,B)$: `Find(A)=A`, `Find(B)=B` — different, so no cycle; `Union(A,B)`.
Edge $(B,C)$: `Find(B)` traces to (say) $A$ (the merged group's representative), `Find(C)=C` — different, so no cycle; `Union(B,C)` merges C's group into A's group too. Now $\{A,B,C\}$ are one group.
Edge $(A,C)$: `Find(A)` and `Find(C)` both now trace to the same representative (since A, B, C are all one group already) — **equal!** This means A and C are already connected via the earlier edges (A–B–C), so adding a direct A–C edge creates a **cycle**.
Edge $(C,D)$: `Find(C)` traces to the $\{A,B,C\}$ group's representative, `Find(D)=D` — different, so no cycle; `Union(C,D)` merges D into the group too.
:::

::: step [Step 3: Conclusion] Final Result
The edge $(A,C)$ is identified as creating a cycle (since A and C were already connected through B before this edge was even added). After processing all four edges, all four vertices $\{A,B,C,D\}$ end up in a **single connected component** — even though the direct edge A–C was redundant for connectivity purposes, it was still useful information (it tells us a cycle A–B–C–A exists in the graph), which is exactly the kind of detection Kruskal's algorithm relies on to build a cycle-free spanning tree.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
When processing an edge $(u,v)$ for cycle detection using Union-Find, what does `Find(u) == Find(v)` (checked *before* performing the union) indicate?
(A) The graph has no edges at all
(*B) $u$ and $v$ are already connected via some other existing path, so adding this edge directly would create a cycle
(C) $u$ and $v$ are guaranteed to never be connected
(D) The graph must be re-initialised
::: explanation
If `Find(u)` and `Find(v)` already return the same representative before this edge is processed, it means some earlier sequence of edges already connects $u$ and $v$ — so this new edge would form a redundant, loop-closing connection: a cycle.
:::

::: quiz Q2: Foundational Concept
Why is Union-Find particularly well-suited to answering connectivity queries as new edges arrive incrementally over time, compared to re-running a full graph traversal (BFS/DFS) after every new edge?
(A) Union-Find and graph traversal have identical costs in every scenario
(*B) Each new edge only requires a single, fast `Union` call, and each query only requires a single `Find`-and-compare — no need to re-scan the entire graph from scratch each time
(C) Union-Find can only be used on graphs with no edges
(D) Graph traversal is always faster for incremental updates
::: explanation
Union-Find's whole design supports cheap, localized updates: adding an edge is one `Union` call (near-constant amortized time), and checking connectivity is one `Find`-and-compare — no need to revisit the entire graph structure, unlike re-running BFS/DFS from scratch, which examines the whole graph each time.
:::

::: quiz Q3: Foundational Concept
What is a key limitation of plain Union-Find in the context of dynamic graph connectivity?
(A) It cannot handle graphs with more than 100 vertices
(*B) It efficiently supports edges being *added* but does not efficiently support edges being *removed* (deleted)
(C) It can only be used on trees, never general graphs
(D) It requires the entire graph to be known in advance, with no incremental updates possible
::: explanation
Union-Find naturally handles the "edges only ever added" (incremental) case very efficiently, but once two groups have been merged via a Union, there's no simple, cheap way to "split" them back apart if the edge that caused the merge is later removed — handling deletions requires more advanced (and more complex) data structures beyond plain Union-Find.
:::
