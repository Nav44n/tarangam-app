# Progressive Problems: Graph Traversals (BFS & DFS)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Shared Graph Definition

To keep our mental model crystal clear across Levels 1 and 2, we will use the exact same undirected graph containing $6$ vertices (labeled alphabetically: $A, B, C, D, E, F$) connected by the following undirected edges:
- $(A, B)$
- $(A, C)$
- $(B, D)$
- $(B, E)$
- $(C, F)$

```text
       A
      / \
     B   C
    / \   \
   D   E   F
```

In adjacency list representation (sorted alphabetically for deterministic tie-breaking):
- $\text{Adj}[A] = [B, C]$
- $\text{Adj}[B] = [A, D, E]$
- $\text{Adj}[C] = [A, F]$
- $\text{Adj}[D] = [B]$
- $\text{Adj}[E] = [B]$
- $\text{Adj}[F] = [C]$

---

## Level 1: Breadth-First Search (BFS)

### Problem 1.1: Layer-by-Layer Traversal from Vertex A

Starting at node $A$, trace Breadth-First Search (BFS) on this undirected graph.  
At every single step, we will explicitly record:
1. The node currently being processed (`Current Node`).
2. The exact state of the `Queue` ordered from `[front ... back]`.
3. The contents of the `Visited Set`.
4. The running `Output Order`.

::: callout-intuition Core Mental Model
Imagine dropping a pebble into a calm pond at point $A$.
- The splash creates concentric ripples of water expanding outwards.
- The ripple first hits everything exactly $1$ step away from $A$ ($B$ and $C$).
- Only *after* that entire circle is wet does the ripple push further out to hit things $2$ steps away from $A$ ($D, E,$ and $F$).
- A **Queue** works on a **FIFO** basis ("First-In, First-Out"), like people waiting in a line at a grocery store checkout: whoever gets in line first gets served first. Because $1$-step neighbors get in line before $2$-step neighbors, they are guaranteed to be processed before the deeper nodes!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Initialization & Enqueue Start Node A</div>

**What are we doing?** We initialize an empty queue, an empty visited set, and an empty output list. Then, we mark our starting vertex $A$ as visited and push it into the queue.

**Why are we starting here?** A graph has no inherent "top" or "root" like a tree. We must explicitly pick an entry door ($A$). We must mark $A$ as visited immediately upon queuing it so that we never accidentally add it again later when looking back from its neighbors.

**How do we do it?** 1. Create `Queue = []`, `Visited = {}`, `Output = []`.
2. Add $A$ to `Visited`: `Visited = {A}`.
3. Push $A$ into `Queue`: `Queue = [A]`.

**Where did this concept come from?** The definition of BFS: all nodes at distance $d=0$ (the start node itself) must be queued before exploring nodes at distance $d=1$.

**System State:**
- **Current Node:** None (algorithm loop has not popped yet)
- **Queue [front ... back]:** `[A]`
- **Visited Set:** `{A}`
- **Output:** `[]`
</div>

<div class="step-card">
<div class="step-badge">Step 2: Dequeue A and Inspect Neighbors</div>

**What changed from Step 1?** We enter the main loop: `while Queue is not empty`. We remove the front item from the queue.

**What are we doing?** 1. Dequeue the front item: this is $A$.
2. Append $A$ to our `Output` list.
3. Look at all outgoing edges from $A$ in alphabetical order: $\text{Adj}[A] = [B, C]$.
4. For each neighbor, check if it is already in `Visited`. If not, add it to `Visited` and enqueue it.

**How do we do it?** - Current node $= A$.
- Output becomes: `[A]`.
- Neighbor 1 ($B$): Is $B \in \text{Visited}$? No.
  - Add $B$ to `Visited`: `{A, B}`.
  - Enqueue $B$: `Queue = [B]`.
- Neighbor 2 ($C$): Is $C \in \text{Visited}$? No.
  - Add $C$ to `Visited`: `{A, B, C}`.
  - Enqueue $C$: `Queue = [B, C]`.

**System State:**
- **Current Node:** $A$
- **Queue [front ... back]:** `[B, C]` (These represent Distance $1$ from $A$)
- **Visited Set:** `{A, B, C}`
- **Output:** `[A]`
</div>

<div class="step-card">
<div class="step-badge">Step 3: Dequeue B and Inspect Neighbors</div>

**What changed from Step 2?** Node $A$ is completely finished. Node $B$ is now at the front of the queue.

**What are we doing?** Dequeue $B$, output it, and discover its unvisited neighbors.

**How do we do it?** 1. Dequeue front: $B$.
2. Append $B$ to `Output`: `[A, B]`.
3. Check $\text{Adj}[B] = [A, D, E]$:
   - Neighbor $A$: Is $A \in \text{Visited}$? Yes ($A \in \{A, B, C\}$). **Skip $A$!** (Prevents an infinite loop back to the parent).
   - Neighbor $D$: Is $D \in \text{Visited}$? No.
     - Add to `Visited`: `{A, B, C, D}`.
     - Enqueue $D$: `Queue = [C, D]`.
   - Neighbor $E$: Is $E \in \text{Visited}$? No.
     - Add to `Visited`: `{A, B, C, D, E}`.
     - Enqueue $E$: `Queue = [C, D, E]`.

**Why did $D$ and $E$ go behind $C$?** Because a queue is FIFO. Node $C$ was discovered in the previous layer ($d=1$). $D$ and $E$ are in layer $d=2$. $C$ was waiting first, so $C$ stays ahead of $D$ and $E$!

**System State:**
- **Current Node:** $B$
- **Queue [front ... back]:** `[C, D, E]`
- **Visited Set:** `{A, B, C, D, E}`
- **Output:** `[A, B]`
</div>

<div class="step-card">
<div class="step-badge">Step 4: Dequeue C and Inspect Neighbors</div>

**What changed from Step 3?** Node $B$ is finished. Node $C$ is now at the front of the queue.

**What are we doing?** Dequeue $C$, output it, and discover its neighbors.

**How do we do it?** 1. Dequeue front: $C$.
2. Append $C$ to `Output`: `[A, B, C]`.
3. Check $\text{Adj}[C] = [A, F]$:
   - Neighbor $A$: Is $A \in \text{Visited}$? Yes. **Skip $A$.**
   - Neighbor $F$: Is $F \in \text{Visited}$? No.
     - Add to `Visited`: `{A, B, C, D, E, F}`.
     - Enqueue $F$: `Queue = [D, E, F]`.

**System State:**
- **Current Node:** $C$
- **Queue [front ... back]:** `[D, E, F]` (All nodes here are at Distance $2$ from $A$)
- **Visited Set:** `{A, B, C, D, E, F}`
- **Output:** `[A, B, C]`
</div>

<div class="step-card">
<div class="step-badge">Step 5: Dequeue D, E, and F (Leaves of the BFS Tree)</div>

**What changed from Step 4?** All remaining items in the queue ($D, E, F$) have no unvisited neighbors.

**What are we doing?** Processing the final layer one-by-one:
- **Sub-step 5a (Process $D$):**
  - Dequeue $D \implies$ `Output = [A, B, C, D]`.
  - $\text{Adj}[D] = [B]$. $B$ is already visited $\implies$ Nothing enqueued.
  - `Queue = [E, F]`.
- **Sub-step 5b (Process $E$):**
  - Dequeue $E \implies$ `Output = [A, B, C, D, E]`.
  - $\text{Adj}[E] = [B]$. $B$ is already visited $\implies$ Nothing enqueued.
  - `Queue = [F]`.
- **Sub-step 5c (Process $F$):**
  - Dequeue $F \implies$ `Output = [A, B, C, D, E, F]`.
  - $\text{Adj}[F] = [C]$. $C$ is already visited $\implies$ Nothing enqueued.
  - `Queue = []`.

**System State:**
- **Queue [front ... back]:** `[]` (Empty $\implies$ while loop terminates)
- **Visited Set:** `{A, B, C, D, E, F}`
- **Output:** `[A, B, C, D, E, F]`
</div>

<div class="step-card">
<div class="step-badge">Final Step: Conclusion & Complexity</div>

**What is the final BFS traversal order?**
$$[A, B, C, D, E, F]$$

**Why does this answer make sense?**
- Layer $0$ (Distance $0$): $[A]$
- Layer $1$ (Distance $1$): $[B, C]$
- Layer $2$ (Distance $2$): $[D, E, F]$

BFS processed every vertex at distance $d$ strictly before any vertex at distance $d+1$.

**Time Complexity:** Every vertex is enqueued and dequeued exactly once ($V$ nodes). Every edge is inspected from both ends ($2E$ checks).  
$$\text{Total Time} = O(V + E)$$
**Space Complexity:** Storing `Queue` and `Visited` requires memory proportional to the number of vertices:  
$$\text{Total Space} = O(V)$$
</div>

</div>

---

## Level 2: Depth-First Search (DFS)

### Problem 2.1: Tracing Recursive Call Stack & Backtracking

Using the exact same graph, trace recursive **Depth-First Search (DFS)** starting from node $A$.  
We will break ties alphabetically when choosing which neighbor to visit next.  
At every step, we will explicitly trace:
1. The **Call Stack** (showing paused vs. active function calls).
2. The node currently being discovered.
3. The **Dead Ends** where no further unvisited neighbors exist.
4. The **Backtracking Points** where a function finishes and control returns to its caller.

::: callout-intuition Core Mental Model
Imagine exploring a dark labyrinth with a ball of string and a piece of chalk:
- You walk down a corridor as far as you can go, unwinding your string behind you.
- Whenever you reach an intersection, you pick the first unexplored door on your left (alphabetical order) and keep running forward.
- When you hit a room with no new exits (a **Dead End**), you don't panic! You follow your string backwards (**Backtrack**) to the room you just came from and try the next unexplored door.
- The **Call Stack** is that ball of string: it remembers exactly which path you walked down so you can safely rewind your steps.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Call DFS(A) - The Root Call</div>

**What are we doing?** We initiate the recursion by invoking `DFS(A)`.

**Why are we starting here?** $A$ is our designated source node.

**How do we do it?** 1. Push `DFS(A)` onto the Call Stack.
2. Mark $A$ as visited: `Visited = {A}`.
3. Append $A$ to discovery sequence: `Discovery = [A]`.
4. Look at neighbors: $\text{Adj}[A] = [B, C]$.
5. The first unvisited neighbor is $B$.
6. `DFS(A)` **pauses** its execution right here and calls `DFS(B)`.

**Call Stack State (Bottom $\to$ Top):**
1. `DFS(A)` [Paused: waiting for neighbor B to finish]

**State:**
- **Visited:** `{A}`
- **Discovery Order:** `[A]`
</div>

<div class="step-card">
<div class="step-badge">Step 2: Call DFS(B) - Diving Deeper</div>

**What changed from Step 1?** A new stack frame `DFS(B)` is pushed on top of `DFS(A)`.

**What are we doing?** Executing `DFS(B)`.

**How do we do it?** 1. Mark $B$ as visited: `Visited = {A, B}`.
2. Append $B$ to discovery sequence: `Discovery = [A, B]`.
3. Check neighbors: $\text{Adj}[B] = [A, D, E]$:
   - Neighbor $A$: Already in `Visited` $\implies$ skip.
   - Neighbor $D$: Not in `Visited`!
4. `DFS(B)` pauses and immediately calls `DFS(D)`.

**Call Stack State (Bottom $\to$ Top):**
1. `DFS(A)` [Paused at B]
2. `DFS(B)` [Paused: waiting for neighbor D to finish]

**State:**
- **Visited:** `{A, B}`
- **Discovery Order:** `[A, B]`
</div>

<div class="step-card">
<div class="step-badge">Step 3: Call DFS(D) & Hit First Dead End</div>

**What changed from Step 2?** `DFS(D)` is pushed onto the stack.

**What are we doing?** Executing `DFS(D)`, hitting a dead end, and backtracking.

**How do we do it?** 1. Mark $D$ as visited: `Visited = {A, B, D}`.
2. Append $D$ to discovery sequence: `Discovery = [A, B, D]`.
3. Inspect neighbors: $\text{Adj}[D] = [B]$:
   - Neighbor $B$: Already in `Visited` $\implies$ skip.
4. **Dead End reached!** Node $D$ has zero remaining unvisited neighbors.
5. `DFS(D)` has completed all lines of code. It **pops off the stack** (terminates) and returns control back to `DFS(B)`.

**Call Stack State (After D pops):**
1. `DFS(A)` [Paused at B]
2. `DFS(B)` [Resumes: finished with D, now moves to next neighbor in its list]

**State:**
- **Visited:** `{A, B, D}`
- **Discovery Order:** `[A, B, D]`
</div>

<div class="step-card">
<div class="step-badge">Step 4: Resume DFS(B) and Call DFS(E)</div>

**What changed from Step 3?** We backtracked to `DFS(B)`. Its neighbor list was $\text{Adj}[B] = [A, D, E]$. We checked $A$ (visited), finished $D$, and now check $E$.

**What are we doing?** Since $E \notin \text{Visited}$, `DFS(B)` pauses again and invokes `DFS(E)`.

**How do we do it?** 1. Push `DFS(E)` to stack.
2. Mark $E$ as visited: `Visited = {A, B, D, E}`.
3. Append $E$: `Discovery = [A, B, D, E]`.
4. Inspect neighbors: $\text{Adj}[E] = [B]$. $B$ is already visited $\implies$ skip.
5. **Dead End reached!** `DFS(E)` has no more neighbors.
6. `DFS(E)` terminates and **pops off the stack**, returning to `DFS(B)`.

**Call Stack State:**
- `DFS(E)` pops.
- Control returns to `DFS(B)`.
- `DFS(B)` has now exhausted all its neighbors ($A, D, E$).
- Therefore, `DFS(B)` also finishes and **pops off the stack**!
- Control returns all the way back to the root call: `DFS(A)`.

**Call Stack State (Bottom $\to$ Top):**
1. `DFS(A)` [Resumes: finished with neighbor B, now checks neighbor C]

**State:**
- **Visited:** `{A, B, D, E}`
- **Discovery Order:** `[A, B, D, E]`
</div>

<div class="step-card">
<div class="step-badge">Step 5: Resume DFS(A) and Explore Right Subtree (C and F)</div>

**What changed from Step 4?** Entire branch under $B$ is fully explored. `DFS(A)` resumes and looks at its next neighbor from $\text{Adj}[A] = [B, C]$, which is $C$.

**What are we doing?** Calling `DFS(C)`, which subsequently calls `DFS(F)`.

**How do we do it?**
- **Sub-step 5a (Invoke `DFS(C)`):**
  - Push `DFS(C)`. `Visited = {A, B, D, E, C}`.
  - Append $C$: `Discovery = [A, B, D, E, C]`.
  - $\text{Adj}[C] = [A, F]$. $A$ is visited $\implies$ skip.
  - $F$ is not visited $\implies$ `DFS(C)` pauses and calls `DFS(F)`.
- **Sub-step 5b (Invoke `DFS(F)`):**
  - Push `DFS(F)`. `Visited = {A, B, D, E, C, F}`.
  - Append $F$: `Discovery = [A, B, D, E, C, F]`.
  - $\text{Adj}[F] = [C]$. $C$ is visited $\implies$ skip.
  - **Dead End!** `DFS(F)` pops $\implies$ returns to `DFS(C)`.
- **Sub-step 5c (Clean up):**
  - `DFS(C)` has no more neighbors $\implies$ pops $\implies$ returns to `DFS(A)`.
  - `DFS(A)` has no more neighbors $\implies$ pops $\implies$ Stack is empty!

**Call Stack State:** `[]` (Empty $\implies$ traversal complete)
</div>

<div class="step-card">
<div class="step-badge">Final Step: Comparison with BFS</div>

**What is the final DFS discovery order?**
$$[A, B, D, E, C, F]$$

**Compare directly against BFS from Level 1:**
- **BFS Order:** $[A, B, C, D, E, F]$ (Wider first: visited all neighbors of $A$ before going deeper)
- **DFS Order:** $[A, B, D, E, C, F]$ (Deeper first: went all the way to bottom leaf $D$ before ever visiting sibling $C$)

**Complexity:**
- **Time:** $O(V + E)$ (visits every vertex once, checks every adjacency edge once).
- **Space:** $O(h)$ where $h$ is the maximum depth of the call stack (in worst-case linear graph, $h = V \implies O(V)$).
</div>

</div>

---

## Level 3: Edge Classification & Cycle Detection

### Problem 3.1: Detecting Cycles in a Directed Graph Using DFS Colors

Consider the following **directed graph** with $4$ vertices ($0, 1, 2, 3$):
- $0 \to 1$
- $1 \to 2$
- $2 \to 3$
- $3 \to 1$  *(Notice this arrow points backwards!)*

```text
  0 ----> 1 ----> 2
          ^       |
          |       |
          +------ 3
```

We must:
1. Explain the three edge classifications in DFS: **Tree Edges**, **Back Edges**, and **Forward/Cross Edges**.
2. Define the three vertex states (**White**, **Gray**, and **Black**).
3. Trace DFS step-by-step from node $0$ to detect the back-edge and mathematically prove the existence of a cycle.

::: callout-intuition Core Mental Model
Imagine a family ancestry tree where time moves forward:
- **Tree Edge:** A parent having a child. You move forward into a new, never-before-seen generation.
- **Back Edge:** A sci-fi time traveler going back in time to meet their own grandparent! 
- If a person can meet their own direct ancestor who is currently pregnant with them, you have created a **time loop (a cycle)**!
- In DFS, a **Gray node** is someone who is currently active on the stack (an ancestor waiting for their descendants to finish). If you ever bump into a **Gray node**, you just ran into your own ancestor! That guarantees a cycle.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: The 3-Color Vertex Classification</div>

**What are we doing?** Defining the three colors used to track node status in cycle detection.

**Why do we need 3 colors instead of a simple boolean visited flag?** In a directed graph, a simple `visited = true` flag cannot distinguish between:
1. Returning to a node that is **currently being explored** on the active path (an ancestor $\implies$ cycle!).
2. Visiting a node that was already completely explored and finished in an earlier, unrelated branch (not a cycle).

**How do we define them?**
- **WHITE (0):** Unvisited. The algorithm hasn't touched this vertex yet.
- **GRAY (1):** Currently exploring. The vertex is on the active **Call Stack**. Its descendants are currently being searched.
- **BLACK (2):** Fully finished. The vertex and all of its descendants have been completely explored. The vertex has been popped off the stack.

**Where did this concept come from?** Cormen, Leiserson, Rivest, Stein (CLRS) *Introduction to Algorithms* standard DFS state machine.

**Initial State Table:**
| Node | Color | Meaning |
| :---: | :---: | :--- |
| **0** | WHITE | Unvisited |
| **1** | WHITE | Unvisited |
| **2** | WHITE | Unvisited |
| **3** | WHITE | Unvisited |

**Call Stack:** `[]`
</div>

<div class="step-card">
<div class="step-badge">Step 2: Start DFS(0) - Mark Gray</div>

**What changed from Step 1?** We begin traversal at node $0$.

**What are we doing?** Push node $0$ to the call stack and turn its color from WHITE to GRAY.

**How do we do it?** 1. Set `Color[0] = GRAY`.
2. Push `0` onto Call Stack: `Stack = [0]`.
3. Look at outgoing edges from $0$: only edge is $0 \to 1$.
4. Check color of node $1$: `Color[1]` is WHITE.
5. **Edge Type Encountered:** **Tree Edge** ($0 \to 1$).
   - *Definition:* A Tree Edge is an edge pointing to a completely unvisited (WHITE) node. It forms the backbone of our traversal search tree.
6. Recursively call `DFS(1)`.

**State Table:**
| Node | Color | Meaning |
| :---: | :---: | :--- |
| **0** | **GRAY** | Active on Call Stack |
| **1** | WHITE | Unvisited |
| **2** | WHITE | Unvisited |
| **3** | WHITE | Unvisited |

**Call Stack (Bottom $\to$ Top):** `[0]`
</div>

<div class="step-card">
<div class="step-badge">Step 3: Execute DFS(1) and DFS(2) - Tree Edges</div>

**What changed from Step 2?** We dive forward down the chain $0 \to 1 \to 2$.

**What are we doing?** Processing nodes $1$ and $2$ sequentially.

**How do we do it?**
- **Processing node 1:**
  - `Color[1] = GRAY`.
  - Push $1$ onto stack: `Stack = [0, 1]`.
  - Outgoing edge: $1 \to 2$.
  - Check `Color[2]`: WHITE $\implies$ **Tree Edge**.
  - Call `DFS(2)`.

- **Processing node 2:**
  - `Color[2] = GRAY`.
  - Push $2$ onto stack: `Stack = [0, 1, 2]`.
  - Outgoing edge: $2 \to 3$.
  - Check `Color[3]`: WHITE $\implies$ **Tree Edge**.
  - Call `DFS(3)`.

**State Table:**
| Node | Color | Meaning |
| :---: | :---: | :--- |
| **0** | **GRAY** | Ancestor 1 on Stack |
| **1** | **GRAY** | Ancestor 2 on Stack |
| **2** | **GRAY** | Ancestor 3 on Stack |
| **3** | WHITE | About to be visited |

**Call Stack (Bottom $\to$ Top):** `[0, 1, 2]`
</div>

<div class="step-card">
<div class="step-badge">Step 4: Execute DFS(3) & Encounter the Back Edge</div>

**What changed from Step 3?** Node $3$ is reached.

**What are we doing?** 1. `Color[3] = GRAY`.
2. Push $3$ onto stack: `Stack = [0, 1, 2, 3]`.
3. Check outgoing edges from node $3$: edge $3 \to 1$.
4. Check the color of target node $1$:
   $$\text{Color}[1] == \mathbf{GRAY}$$

**What does meeting a GRAY node mean?** Because node $1$ is **GRAY**, it is currently sitting on the active Call Stack! This means node $1$ is an **ancestor** of node $3$.  
By following the directed path, we started at $1 \to 2 \to 3$, and from $3$ we are directed back to $1$.

**Where did this concept come from?**
- **Definition of Back Edge:** A directed edge $(u, v)$ is a **Back Edge** if and only if $v$ is an ancestor of $u$ in the DFS tree (`Color[v] == GRAY`).
- **Fundamental Cycle Theorem:** A directed graph has a cycle **if and only if** a depth-first search yields at least one back edge.

**Action:** **Cycle Confirmed!** Cycle path:
$$1 \longrightarrow 2 \longrightarrow 3 \longrightarrow 1$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary of All Edge Types & Cycle Rule</div>

**What are the formal edge types in DFS?**
1. **Tree Edge:** An edge $(u, v)$ where $v$ was WHITE (a child discovered for the first time).
2. **Back Edge:** An edge $(u, v)$ where $v$ is GRAY (points back to an active ancestor on the recursion stack). $\implies$ **Direct proof of a cycle!**
3. **Forward Edge:** An edge $(u, v)$ where $v$ is BLACK and $v$ is a descendant of $u$ (shortcuts from an ancestor to a grandchild). Not a cycle.
4. **Cross Edge:** An edge $(u, v)$ between two nodes with no ancestor/descendant relationship (crosses between two different completed subtrees). Target node is BLACK. Not a cycle.

**Algorithmic Rule to Remember:**
$$\text{If neighbor is WHITE} \implies \text{Tree Edge (Recurse)}$$
$$\text{If neighbor is GRAY} \implies \text{Back Edge (CYCLE DETECTED!)}$$
$$\text{If neighbor is BLACK} \implies \text{Forward or Cross Edge (Safe, ignore)}$$
</div>

</div>
