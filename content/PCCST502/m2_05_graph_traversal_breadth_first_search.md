# Breadth-First Search (BFS) & Shortest Path in Unweighted Graphs

**Queue-based traversal, level-order expansion, BFS tree, and time complexity O(V+E).**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
Imagine dropping a single pebble into a still pond. The ripple it creates spreads outward in perfect, expanding circles — everything exactly 1 metre away is disturbed at the same moment, then everything exactly 2 metres away, then 3, and so on — the ripple never "skips ahead" to disturb something far away before finishing everything closer.

**Breadth-First Search (BFS)** explores a graph in exactly this ripple pattern, starting from a chosen source vertex. It first visits every vertex at distance 1 (directly connected to the source), *then* every vertex at distance 2 (connected to something at distance 1, but not any closer), then distance 3, and so on — visiting the graph in complete, expanding "waves," or **levels**. This level-by-level exploration order is precisely what makes BFS the natural, correct tool for finding the **shortest path** (fewest number of edges) from the source to any other vertex, in an unweighted graph — the moment BFS *first* reaches a vertex, that arrival is guaranteed to be via the shortest possible route, since anything closer would have already been visited in an earlier wave.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**The mechanism: a queue.** BFS uses a **FIFO (first-in, first-out) queue** to control visiting order — this is the data structure that enforces the "finish the current wave completely before starting the next" behaviour. Pseudocode:
```
BFS(G, source):
    for each vertex v: visited[v] = False; dist[v] = infinity
    visited[source] = True; dist[source] = 0
    queue = [source]
    while queue is not empty:
        u = queue.dequeue()
        for each neighbour v of u:
            if not visited[v]:
                visited[v] = True
                dist[v] = dist[u] + 1
                parent[v] = u          # records the BFS tree
                queue.enqueue(v)
```
Every vertex is enqueued exactly once (guarded by the `visited` check), and every edge is examined exactly once per direction while scanning each dequeued vertex's neighbour list.

**Why the queue guarantees shortest paths (unweighted case).** Because vertices are enqueued in the exact order their distance-from-source increases by 1 each wave, and the queue processes them in that same first-in-first-out order, every vertex at distance $k$ is guaranteed to be dequeued (and have its neighbours examined) *before* any vertex at distance $k+1$ is even discovered. So when a previously-unvisited vertex $v$ is first reached via some vertex $u$, $u$ must be at the smallest possible distance that could reach $v$ in one more step — meaning `dist[v] = dist[u]+1` is provably the shortest possible distance to $v$.

**The BFS tree.** The `parent[]` pointers recorded during the traversal form a tree rooted at the source — following `parent` pointers backward from any vertex $v$ traces out one shortest path from the source to $v$. This tree is a genuinely useful byproduct, not just an internal bookkeeping detail — it's frequently used directly to reconstruct and report the actual shortest path, not merely its length.

**Time complexity: $O(V+E)$.** Each vertex is enqueued/dequeued exactly once — contributing $O(V)$ total. Each vertex's full neighbour list is scanned exactly once, and summed across all vertices, this totals exactly $E$ (or $2E$ for undirected graphs, since each edge appears in two neighbour lists — still a constant factor) — contributing $O(E)$ total. Together: $O(V+E)$, the standard "linear in the size of the graph" bound that appears throughout graph algorithms, and notably matches the $\Theta(V+E)$ space cost of the adjacency-list representation from the previous topic — BFS essentially does one unit of work per unit of stored graph data, which is about as efficient as a traversal can be.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Given an undirected graph with edges $A$–$B$, $A$–$C$, $B$–$D$, $C$–$D$, $D$–$E$, run BFS starting from source $A$, and determine the shortest-path distance (in number of edges) from $A$ to every other vertex.
:::

::: step [Step 2: Execution] Applying Core Algorithm
Initialise: `dist[A]=0`, all others infinity; queue = `[A]`.
Dequeue $A$: neighbours are $B, C$ (both unvisited) — mark visited, `dist[B]=1`, `dist[C]=1`, enqueue both. Queue = `[B, C]`.
Dequeue $B$: neighbours are $A$ (visited, skip), $D$ (unvisited) — mark visited, `dist[D] = dist[B]+1 = 2`, enqueue. Queue = `[C, D]`.
Dequeue $C$: neighbours are $A$ (visited, skip), $D$ (already visited via $B$, skip — its distance is already correctly set to 2). Queue = `[D]`.
Dequeue $D$: neighbours are $B$ (visited), $C$ (visited), $E$ (unvisited) — mark visited, `dist[E] = dist[D]+1 = 3`, enqueue. Queue = `[E]`.
Dequeue $E$: neighbours are $D$ (visited). Queue empty — BFS complete.
:::

::: step [Step 3: Conclusion] Final Result
Final shortest distances from $A$: `dist[A]=0, dist[B]=1, dist[C]=1, dist[D]=2, dist[E]=3`. Notice that $D$ was reachable via two different 2-edge paths ($A$-$B$-$D$ and $A$-$C$-$D$), but BFS correctly recorded distance $2$ regardless of which path discovered it first — because *both* paths have exactly 2 edges, either one gives the correct shortest distance; BFS guarantees correctness of the *distance*, though the specific `parent` pointer recorded (and thus which single shortest path gets reconstructed) depends on which neighbour happened to be processed first.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
What data structure does BFS use to control the order in which vertices are visited, and why is this specific structure essential to BFS's correctness?
(A) A stack, because it processes the most recently discovered vertex first
(*B) A FIFO queue, because it ensures all vertices at the current distance level are fully processed before any vertex at the next distance level is discovered, guaranteeing shortest-path correctness
(C) A priority queue ordered by vertex name
(D) No structure is needed; BFS uses random order
::: explanation
A FIFO queue processes elements in the exact order they were added — which, in BFS, corresponds exactly to processing vertices in increasing order of distance from the source. This "finish the current wave before starting the next" property is what guarantees that the first time any vertex is reached, it's via the shortest possible path.
:::

::: quiz Q2: Foundational Concept
What is the overall time complexity of BFS on a graph represented with an adjacency list, and what do the two terms represent?
(A) $O(V^2)$, always, regardless of representation
(*B) $O(V+E)$ — $O(V)$ for enqueuing/dequeuing every vertex exactly once, and $O(E)$ for scanning every edge exactly once (twice for undirected graphs, a constant factor) across all neighbour-list scans
(C) $O(E^2)$, from comparing every pair of edges
(D) $O(\log V)$, since BFS behaves like binary search
::: explanation
Every vertex enters and leaves the queue exactly once (bounded by the `visited` check), contributing $O(V)$; and summed across all vertices, every edge is examined exactly once (or twice, for undirected graphs, when scanning each endpoint's neighbour list) while scanning neighbour lists, contributing $O(E)$. Together, this gives the standard "linear in graph size" bound $O(V+E)$.
:::

::: quiz Q3: Foundational Concept
Why does BFS specifically compute *shortest paths* correctly in an unweighted graph, but would *not* directly work correctly for a graph where edges have different weights (costs)?
(A) BFS cannot handle any graph with more than one edge
(*B) BFS's correctness relies on the fact that every edge contributes exactly "1" to the path length, so processing vertices in queue (FIFO) order exactly matches increasing true distance — this breaks down if edges have varying weights, since a path with more edges could still have smaller total weight than a path with fewer, heavier edges
(C) BFS only works on trees, not general graphs
(D) BFS requires the graph to be directed
::: explanation
BFS's shortest-path guarantee depends entirely on every edge counting as exactly one unit of distance, which makes "discovered earlier in FIFO order" the same thing as "closer in true distance." If edges have different weights, a vertex reached via more edges could still have a smaller total weighted distance than one reached via fewer, heavier edges — breaking BFS's core assumption. (Weighted shortest-path problems require different algorithms, such as Dijkstra's, covered in later modules.)
:::
