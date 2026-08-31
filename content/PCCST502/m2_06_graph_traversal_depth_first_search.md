# Depth-First Search (DFS) & Edge Classification

**Stack/recursive traversal, discovery and finishing timestamps, tree/back/forward/cross edges, and cycle detection.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
If BFS explores like ripples spreading evenly outward from a pebble, **Depth-First Search (DFS)** explores like a person navigating a corn-maze by always picking a random new direction and committing to it fully — walking as far as possible down one path, only backing up (backtracking) once you hit a dead end or a spot you've already visited, and only *then* trying the next unexplored branch from wherever you last had a choice. Instead of exploring "wide and shallow, one wave at a time," DFS goes "deep and narrow first," diving as far down one branch as it possibly can before ever coming back to explore a sibling branch.

This deep-diving order turns out to reveal something BFS's wave-by-wave order doesn't: by recording *when* you first arrive at a room (discovery time) and *when* you finally leave it for good, having explored everything reachable from it (finishing time), you can classify every corridor (edge) in the maze into one of four distinct categories — and one of those categories, in particular, directly reveals whether the maze contains a loop back on itself (a cycle).
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**The mechanism: a stack (explicit, or implicit via recursion).** DFS is most naturally written recursively, where the call stack itself plays the role of the "stack" data structure, keeping track of the path taken so far so we can backtrack correctly:
```
DFS(G):
    for each vertex v: visited[v] = False; color[v] = WHITE
    time = 0
    for each vertex v:
        if not visited[v]: DFS-Visit(v)

DFS-Visit(u):
    visited[u] = True; color[u] = GRAY   # currently being explored ("on the current path")
    time = time + 1; discovery[u] = time
    for each neighbour v of u:
        classify edge (u,v) based on color[v]     # see classification rules below
        if color[v] == WHITE:
            parent[v] = u
            DFS-Visit(v)
    color[u] = BLACK   # fully finished — everything reachable from u has been explored
    time = time + 1; finish[u] = time
```
The outer loop over "for each vertex v" (calling `DFS-Visit` on any not-yet-visited vertex) ensures the *entire* graph is explored, even if it's disconnected into several separate pieces — unlike BFS, which by default only explores whatever is reachable from a single given source. This produces, in general, a **DFS forest** (a collection of DFS trees, one per connected/reachable component), rather than a single tree.

**Discovery and finishing times.** Each vertex gets timestamped twice: `discovery[u]` (when first reached) and `finish[u]` (when DFS has completely finished exploring everything reachable from `u`, and is about to backtrack away from it for good). These timestamps are what enable edge classification.

**Edge classification (for a directed graph — the general case; some categories coincide for undirected graphs):**
- **Tree edge:** an edge $(u,v)$ where $v$ was WHITE (unvisited) when first examined from $u$ — this is exactly the edge used to *discover* $v$, and becomes part of the DFS tree/forest.
- **Back edge:** an edge $(u,v)$ where $v$ is GRAY (currently on the active path, an ancestor of $u$ in the current DFS tree) when examined — this points "backward" toward an ancestor still being explored. **A back edge is the direct, definitive signature of a cycle** — it means you can walk from $v$ down to $u$ (through tree edges already traversed) and then follow this one extra edge straight back to $v$, closing a loop.
- **Forward edge:** an edge $(u,v)$ where $v$ is BLACK (already fully finished) and $v$ is a *descendant* of $u$ in the DFS tree — points "forward" to something already completely explored, but reachable another way too. (Only possible in directed graphs.)
- **Cross edge:** an edge $(u,v)$ where $v$ is BLACK and $v$ is *not* a descendant of $u$ — connects two unrelated branches of the DFS tree/forest, neither an ancestor nor descendant of the other. (Only possible in directed graphs.)
- For **undirected graphs**, only tree edges and back edges occur (forward and cross edges reduce to being classified as back edges instead, due to how undirected edges are examined from both endpoints).

**Cycle detection via DFS:** a graph contains a cycle if and only if a DFS traversal encounters at least one **back edge**. This is the standard, provably correct way to detect cycles using DFS, applicable to both directed and undirected graphs (with the caveat that, for undirected graphs, you must be careful to not count the trivial "back edge" to your own immediate parent — since an undirected edge $(u,v)$ is naturally seen from both directions — as a false cycle).

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Given a directed graph with edges $A\to B$, $B\to C$, $C\to A$, run DFS starting from $A$, record discovery/finish times, and classify every edge. Determine whether the graph contains a cycle.
:::

::: step [Step 2: Execution] Applying Core Algorithm
`DFS-Visit(A)`: mark $A$ GRAY, `discovery[A]=1`. Examine edge $A\to B$: $B$ is WHITE → **tree edge**; recurse.
`DFS-Visit(B)`: mark $B$ GRAY, `discovery[B]=2`. Examine edge $B\to C$: $C$ is WHITE → **tree edge**; recurse.
`DFS-Visit(C)`: mark $C$ GRAY, `discovery[C]=3`. Examine edge $C\to A$: $A$ is currently **GRAY** (still on the active path — an ancestor of $C$) → this is a **back edge**. No further unvisited neighbours from $C$; mark $C$ BLACK, `finish[C]=4`.
Back to $B$: no further unvisited neighbours; mark $B$ BLACK, `finish[B]=5`.
Back to $A$: no further unvisited neighbours; mark $A$ BLACK, `finish[A]=6`.
:::

::: step [Step 3: Conclusion] Final Result
Edge classification: $A\to B$ and $B\to C$ are **tree edges**; $C\to A$ is a **back edge**. Since a back edge was found, DFS confirms this graph **contains a cycle** — specifically, exactly the cycle $A \to B \to C \to A$ that's visually obvious here, but which DFS's back-edge rule detects systematically and correctly even in graphs far too large or complex to check "by eye."
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
Which type of edge, discovered during a DFS traversal, definitively indicates that the graph contains a cycle?
(A) Tree edge
(*B) Back edge
(C) Forward edge
(D) Cross edge
::: explanation
A back edge points from the current vertex to an ancestor that is still GRAY (currently being explored, i.e. still on the active recursion path) — meaning you can trace a path from that ancestor down to the current vertex via tree edges, then follow this one back edge straight back to the ancestor, forming a closed loop: a cycle.
:::

::: quiz Q2: Foundational Concept
What do the "discovery time" and "finish time" of a vertex represent in DFS?
(A) The number of edges connected to that vertex
(*B) The timestamp when the vertex is first reached (turns GRAY) and the timestamp when DFS has completely finished exploring everything reachable from it (turns BLACK)
(C) The vertex's distance from the source, as in BFS
(D) A random number assigned for identification purposes only
::: explanation
Discovery time marks when a vertex is first encountered and DFS begins exploring from it; finish time marks when DFS has fully explored every vertex reachable from it and is backtracking away for good. These two timestamps, and the color state (WHITE/GRAY/BLACK) they imply at any point in the traversal, are exactly what allow every edge to be classified into one of the four categories.
:::

::: quiz Q3: Foundational Concept
Why does the outer loop of the DFS algorithm ("for each vertex v: if not visited, call DFS-Visit(v)") matter, compared to just calling DFS-Visit once on a single starting vertex?
(A) It has no real purpose and can be removed
(*B) It ensures every vertex is eventually visited even if the graph is disconnected into multiple separate pieces, producing a DFS forest rather than missing unreachable components
(C) It guarantees the traversal finds the shortest path
(D) It converts DFS into BFS
::: explanation
A single call to `DFS-Visit` only explores vertices reachable from that one starting vertex. If the graph has multiple disconnected components (or, in a directed graph, vertices unreachable from the chosen start), those vertices would be missed entirely without the outer loop, which restarts DFS from any still-unvisited vertex, building a full DFS forest that covers the entire graph.
:::
