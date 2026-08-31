# Topological Sorting in Directed Acyclic Graphs (DAGs)

**Kahn's in-degree algorithm vs DFS finishing time algorithm and dependency resolution.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
Think about getting dressed in the morning: you must put on socks before shoes, and underwear before trousers — but the order between "socks" and "underwear" doesn't matter at all, they're independent. This is a **dependency problem**: some tasks must happen before others, but not every pair of tasks has a required order between them. **Topological sorting** takes a set of tasks with "must come before" constraints (naturally represented as a **Directed Acyclic Graph**, or DAG — an edge $u\to v$ means "$u$ must be done before $v$") and produces *one valid linear ordering* of all tasks that respects every single constraint simultaneously — put socks before shoes, underwear before trousers, and arrange everything else however's convenient, as long as no constraint is violated.

This isn't just a cute morning-routine puzzle — it's exactly the algorithm behind resolving software package dependencies (installing library A before the program that needs it), scheduling university courses (a prerequisite must be taken before the course that requires it), compiling code (compiling a module before anything that imports it), and spreadsheet formula evaluation (computing a cell before any formula that references it). There are two standard, equally valid ways to compute a topological order — one built on counting incoming dependencies (Kahn's algorithm), and one built cleverly on the DFS finishing times from the previous topics.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Precondition: topological sort is only well-defined for a DAG.** If the graph contains a cycle, no valid linear order can exist — a cycle means task $A$ depends (directly or transitively) on task $B$, which depends back on task $A$: an impossible, circular requirement (like "put on your shoes before your socks, and your socks before your shoes"). This is exactly why the previous topic's cycle-detection (via a DFS back edge) is often run as a sanity check before attempting a topological sort.

**Method 1 — Kahn's Algorithm (in-degree / BFS-style).**
- Compute the **in-degree** of every vertex (the number of incoming edges — i.e., how many unfulfilled prerequisites it currently has).
- Initialise a queue with all vertices whose in-degree is currently $0$ (tasks with no prerequisites — safe to do first).
- Repeatedly: dequeue a vertex $u$, add it to the output order, and for each of $u$'s outgoing edges $u\to v$, decrement $v$'s in-degree by 1 (since $u$'s requirement on $v$ is now satisfied); if $v$'s in-degree drops to $0$, enqueue it (all of $v$'s prerequisites are now done).
- Continue until the queue is empty. If the final output order contains *all* $V$ vertices, the sort succeeded (and the graph was indeed a DAG); if fewer than $V$ vertices were output, the graph contains a cycle (some vertices' in-degrees never dropped to 0, because they're stuck in a circular dependency), and no valid topological order exists.

**Method 2 — DFS Finishing-Time Algorithm.**
- Run a standard DFS on the entire graph (using the "for each unvisited vertex" outer loop to cover disconnected pieces), recording each vertex's finishing time, exactly as in the previous DFS and Kosaraju topics.
- The topological order is simply the vertices listed in **decreasing order of finish time** — the vertex that finishes *last* comes *first* in the topological order.
- **Why this works:** whenever DFS explores an edge $u \to v$, one of two things happens — either $v$ is still WHITE (unvisited), in which case DFS recurses into $v$ and *must* finish exploring $v$ entirely before returning to finish $u$, guaranteeing `finish[v] < finish[u]`; or $v$ is already visited, and (since the graph is acyclic, so $v$ cannot be a currently-GRAY ancestor — that would be a back edge, meaning a cycle) $v$ must already be BLACK, meaning it finished even earlier, so again `finish[v] < finish[u]`. Either way, for *every* edge $u\to v$ in a DAG, `finish[v]` is always less than `finish[u]` — which is exactly the property needed for "sort by decreasing finish time" to respect every dependency constraint.

**Non-uniqueness.** In general, a DAG can have *multiple* valid topological orderings (exactly like how "socks, underwear, trousers, shoes" and "underwear, socks, trousers, shoes" are both valid morning routines) — both Kahn's algorithm and the DFS method are guaranteed to produce *some* valid ordering, but not necessarily the *same* one as each other, and that's perfectly fine; any output respecting all the dependency constraints is a correct answer.

**Time complexity:** both methods run in $O(V+E)$ — Kahn's algorithm does a constant amount of work per vertex (enqueue/dequeue) and per edge (decrementing in-degree, checked once), and the DFS method is simply one standard DFS traversal, already established as $O(V+E)$.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
A set of course prerequisites forms this DAG: $\text{MATH101} \to \text{MATH201}$, $\text{MATH101} \to \text{CS101}$, $\text{CS101} \to \text{CS201}$, $\text{MATH201} \to \text{CS201}$. Find a valid course-taking order using Kahn's algorithm.
:::

::: step [Step 2: Execution] Applying Core Algorithm
Compute in-degrees: MATH101 = 0 (no prerequisites), MATH201 = 1 (needs MATH101), CS101 = 1 (needs MATH101), CS201 = 2 (needs both CS101 and MATH201).
Initialise queue with all in-degree-0 vertices: `[MATH101]`.
Dequeue MATH101 → output `[MATH101]`. Process its outgoing edges: decrement MATH201's in-degree to 0 (enqueue it); decrement CS101's in-degree to 0 (enqueue it). Queue: `[MATH201, CS101]`.
Dequeue MATH201 → output `[MATH101, MATH201]`. Process its outgoing edge to CS201: decrement CS201's in-degree to 1 (not yet 0, don't enqueue). Queue: `[CS101]`.
Dequeue CS101 → output `[MATH101, MATH201, CS101]`. Process its outgoing edge to CS201: decrement CS201's in-degree to 0 (now enqueue it). Queue: `[CS201]`.
Dequeue CS201 → output `[MATH101, MATH201, CS101, CS201]`. Queue empty.
:::

::: step [Step 3: Conclusion] Final Result
The output order — MATH101, MATH201, CS101, CS201 — includes all 4 vertices, confirming this is indeed a DAG with a valid topological order, and this specific order respects every prerequisite: MATH101 before both MATH201 and CS101; and CS201 only after *both* of its prerequisites (CS101 and MATH201) are satisfied. (Note: MATH201, CS101, MATH101, CS201 in a different relative order between MATH201/CS101 would also be valid, since they don't depend on each other — topological sort just needs to respect the *given* constraints, not impose extra ones.)
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
Why is topological sorting only well-defined for Directed *Acyclic* Graphs (DAGs), and not for graphs containing cycles?
(A) Cyclic graphs always have too many vertices to sort
(*B) A cycle implies a circular dependency (task A requires task B, which requires task A), which has no valid linear order — it's a logical impossibility, like requiring shoes before socks and socks before shoes simultaneously
(C) Topological sorting works fine on cyclic graphs too, just more slowly
(D) Cycles make the in-degree of every vertex equal
::: explanation
If a cycle exists, at least one task in that cycle would need to come both before and after another task in the same cycle — a direct logical contradiction that no linear ordering can satisfy. This is exactly why Kahn's algorithm fails to output all vertices (some in-degrees never reach 0) when run on a graph containing a cycle.
:::

::: quiz Q2: Foundational Concept
In Kahn's algorithm, if the final output list contains fewer than $V$ vertices once the queue becomes empty, what does this indicate?
(A) The graph has too few edges
(*B) The graph contains at least one cycle, so no valid topological order exists
(C) The algorithm needs to be run a second time
(D) All vertices were successfully sorted; this is the expected, normal outcome
::: explanation
If some vertices' in-degrees never drop to 0 (because they're stuck depending on each other in a cycle, so their prerequisites are never fully "satisfied" and removed), those vertices never get enqueued or added to the output — a clear, standard signal that the graph is not a DAG.
:::

::: quiz Q3: Foundational Concept
In the DFS-based topological sort algorithm, why does sorting vertices by *decreasing* finish time (rather than increasing, or by discovery time) produce a valid topological order?
(A) Discovery time and finish time are always identical, so it doesn't matter which is used
(*B) In a DAG, for every edge $u\to v$, DFS guarantees `finish[v] < finish[u]` (since $v$ must be fully explored, or already finished, before $u$'s own exploration completes) — so ordering by decreasing finish time always places $u$ before $v$, respecting every dependency edge
(C) Increasing finish time also works equally well, and both orderings are always identical
(D) Finish time has no relationship to the graph's edge structure
::: explanation
The core DFS property established in this topic's theory section — that every edge in a DAG satisfies `finish[v] < finish[u]` — is exactly what "decreasing finish time" exploits: listing vertices from largest finish time to smallest automatically places every "must come before" vertex ahead of everything it points to, which is the precise definition of a valid topological order.
:::
