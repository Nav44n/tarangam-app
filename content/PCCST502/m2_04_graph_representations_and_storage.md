# Graph Representations: Adjacency Matrix vs Adjacency List

**Memory bounds O(V^2) vs O(V+E), edge lookup speed, and incidence matrices.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
Suppose you want to record which pairs of people, among a group of $V$ people, are friends. One way: draw a giant $V \times V$ grid (spreadsheet), with every person listed down the rows *and* across the columns, and put a checkmark in cell (row $i$, column $j$) if person $i$ and person $j$ are friends. This grid answers "are $i$ and $j$ friends?" instantly — just look up one cell — but it wastes a *lot* of space if most people *aren't* friends with most other people (most cells are empty), which is exactly the typical situation in most real-world networks (a person has a handful of friends, not thousands).

The other way: give each person their own personal address book, listing *only* the names of their actual friends. This uses space proportional to the actual number of friendships, not the number of *possible* pairs — much more efficient when friendships are sparse — but now, answering "are $i$ and $j$ friends?" means searching through $i$'s address book to see if $j$ is listed, which can be slower than a single grid lookup.

These two approaches are exactly the **adjacency matrix** and the **adjacency list** — the two standard ways to represent a graph in a computer, each with a clear trade-off between memory usage and lookup speed, and the right choice depends entirely on how "dense" (many edges relative to possible pairs) or "sparse" (few edges) the specific graph is.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

Let $V$ = number of vertices, $E$ = number of edges.

**Adjacency Matrix.** A $V \times V$ 2D array `adj[][]`, where `adj[i][j] = 1` (or a weight, for weighted graphs) if there's an edge from vertex $i$ to vertex $j$, and `0` (or $\infty$, for weighted graphs, meaning "no edge") otherwise. For an undirected graph, this matrix is always symmetric (`adj[i][j] == adj[j][i]`).
- **Space:** $\Theta(V^2)$ — fixed, regardless of how many actual edges exist.
- **Edge lookup** ("is there an edge between $i$ and $j$?"): $O(1)$ — a single array access.
- **Listing all neighbours of a vertex $i$:** $O(V)$ — must scan the entire row, even if vertex $i$ has very few actual neighbours.
- **Best suited for:** *dense* graphs (where $E$ is close to $V^2$, i.e. most possible edges actually exist), or applications that need very frequent single-edge existence checks.

**Adjacency List.** An array (or hash map) of $V$ lists, where list $i$ contains only the vertices directly connected to vertex $i$ (i.e. its actual neighbours).
- **Space:** $\Theta(V+E)$ — proportional to the number of vertices *plus* the actual number of edges (each edge appears once, or twice for undirected graphs — once in each endpoint's list — but this is still just a constant factor, not changing the asymptotic bound).
- **Edge lookup** ("is there an edge between $i$ and $j$?"): $O(\deg(i))$ in the worst case (must scan through $i$'s neighbour list) — this is $O(V)$ in the absolute worst case (a vertex connected to everyone), but typically much faster in sparse graphs where each vertex has only a few neighbours.
- **Listing all neighbours of a vertex $i$:** $O(\deg(i))$ — directly returns exactly the list of actual neighbours, no wasted scanning of non-edges.
- **Best suited for:** *sparse* graphs (where $E \ll V^2$), which describes the vast majority of real-world graphs (social networks, road networks, the web graph) — this is why adjacency lists are the default choice in most practical graph algorithm implementations, including the BFS, DFS, and later topics in this module.

**Incidence Matrix (a less commonly used third representation).** A $V \times E$ matrix, with one row per vertex and one *column per edge* (rather than per vertex-pair). Entry `inc[i][j] = 1` if vertex $i$ is one of the endpoints of edge $j$ (for directed graphs, sometimes $+1$/$-1$ is used to distinguish "edge leaves this vertex" from "edge enters this vertex"). This representation is less common in typical algorithm coursework but appears in specialised contexts (e.g., certain linear-algebra-based graph techniques, or representing hypergraphs where an "edge" can connect more than two vertices) — its space cost is $\Theta(VE)$, generally larger than either the adjacency matrix or list for typical simple graphs, but it explicitly represents edges as first-class objects (with their own column), which some algorithms find convenient.

**Choosing between matrix and list — the deciding question.** "Roughly how many edges does this graph actually have, relative to $V^2$?" If $E$ is close to $V^2$ (dense graph), the matrix's $\Theta(V^2)$ space is no worse than the list's $\Theta(V+E)\approx\Theta(V^2)$ space anyway, and the matrix's $O(1)$ edge lookups become a clear win. If $E$ is much smaller than $V^2$ (sparse graph, by far the more common real-world case), the list's $\Theta(V+E)$ space is dramatically smaller, and its neighbour-listing speed (crucial for traversal algorithms like BFS and DFS) is much better.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
A social network has $V = 1{,}000{,}000$ users, and on average each user has about $150$ friends (so $E \approx \frac{1{,}000{,}000 \times 150}{2} = 75{,}000{,}000$ edges, dividing by 2 since each friendship is one undirected edge shared by two people). Compare the space required by an adjacency matrix versus an adjacency list for this graph.
:::

::: step [Step 2: Execution] Applying Core Algorithm
**Adjacency matrix:** $V^2 = (1{,}000{,}000)^2 = 10^{12}$ cells — one trillion entries, regardless of how many are actually "1" (edges) versus "0" (no edge). Even using just 1 bit per cell, that's $10^{12}$ bits $\approx 125$ GB — utterly impractical for a typical machine.
**Adjacency list:** space is $\Theta(V+E) = \Theta(1{,}000{,}000 + 75{,}000{,}000) \approx 76{,}000{,}000$ entries total (counting each undirected edge as appearing in two neighbour lists) — a few hundred megabytes at most with reasonable per-entry storage, easily manageable on ordinary hardware.
:::

::: step [Step 3: Conclusion] Final Result
For this graph — sparse, since each user connects to only about $150$ out of a possible $999{,}999$ other users, an utterly tiny fraction — the adjacency list uses roughly four to five orders of magnitude less memory than the adjacency matrix, while still supporting fast "list this person's friends" queries (exactly what a social network needs constantly). This concretely illustrates why virtually every real-world large-scale graph system (social networks, road networks, the web) uses adjacency-list-style representations, reserving adjacency matrices for smaller or genuinely dense graphs.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
What is the space complexity of an adjacency matrix representation of a graph with $V$ vertices, regardless of how many edges it actually has?
(A) $\Theta(V+E)$
(*B) $\Theta(V^2)$
(C) $\Theta(E)$
(D) $\Theta(\log V)$
::: explanation
An adjacency matrix always allocates a full $V \times V$ grid, one cell for every possible pair of vertices, regardless of how many of those pairs are actually connected by an edge — so its space cost is fixed at $\Theta(V^2)$, independent of the actual edge count.
:::

::: quiz Q2: Foundational Concept
For a sparse graph (where $E$ is much smaller than $V^2$), which representation is generally preferred, and why?
(A) Adjacency matrix, because $O(1)$ edge lookup is always the top priority
(*B) Adjacency list, because its space usage $\Theta(V+E)$ scales with the actual number of edges rather than the number of *possible* pairs, avoiding massive wasted memory on non-existent edges
(C) Incidence matrix, because it is the most memory-efficient in all cases
(D) Neither — sparse graphs cannot be represented efficiently
::: explanation
For a sparse graph, $V^2$ vastly overstates the actual number of edges, so an adjacency matrix wastes enormous amounts of memory storing "no edge" entries. An adjacency list only stores space proportional to vertices plus actual edges, which is dramatically smaller for sparse graphs — the overwhelmingly common case in real-world graph data.
:::

::: quiz Q3: Foundational Concept
Listing all neighbours of a single vertex $i$ takes how long using an adjacency list, versus using an adjacency matrix?
(A) $O(1)$ for both representations
(*B) $O(\deg(i))$ for the adjacency list (directly returns only actual neighbours); $O(V)$ for the adjacency matrix (must scan the entire row, including all non-edges)
(C) $O(V)$ for the adjacency list; $O(1)$ for the adjacency matrix
(D) $O(E)$ for both representations
::: explanation
An adjacency list stores exactly (and only) vertex $i$'s actual neighbours, so listing them takes time proportional to how many neighbours there are, $\deg(i)$. An adjacency matrix requires scanning all $V$ entries in row $i$ to find which ones are marked as edges, even though most of those entries will typically be "no edge" in a sparse graph.
:::
