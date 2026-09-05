# Progressive Problems: Topological Sort & Kosaraju's Algorithm

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Level 1: Topological Sort via DFS Finish Times

### Problem 1.1: Ordering Prerequisites on a Directed Acyclic Graph (DAG)

Consider a student preparing for a software engineering job. They must complete tasks with strict prerequisite dependencies represented by directed edges:
- Task $0$ (Learn Math) $\to$ Task $1$ (Learn Algorithms)
- Task $1$ (Learn Algorithms) $\to$ Task $2$ (Pass Interviews)
- Task $0$ (Learn Math) $\to$ Task $3$ (Learn Machine Learning)
- Task $3$ (Learn Machine Learning) $\to$ Task $2$ (Pass Interviews)

```text
       0 (Math)
      / \
     v   v
(Algo) 1   3 (ML)
     \   /
      v v
   2 (Interviews)
```

In adjacency list format (alphabetical/numerical tie-breaking):
- $\text{Adj}[0] = [1, 3]$
- $\text{Adj}[1] = [2]$
- $\text{Adj}[2] = []$ (Sink node / No prerequisites depend on passing interviews)
- $\text{Adj}[3] = [2]$

We will:
1. Maintain a global simulation clock initialized to $t = 0$.
2. Track the discovery time $d[u]$ (when we first step on a node) and the finish time $f[u]$ (when all outgoing paths from that node have been completely searched).
3. Push nodes onto a finishing stack as they complete.
4. Show why sorting nodes in descending order of finish time $f[u]$ guarantees a valid topological order.

::: callout-intuition Core Mental Model
Imagine getting dressed in the morning:
- You cannot put on your shoes before your socks, and you cannot put on socks before your underwear.
- In DFS, you run as far forward along a chain of prerequisites as possible until you reach the very end (the **leaf** or **sink** node, like "Putting on Shoes").
- Because the sink node has no remaining chores waiting on it, it finishes its checklist **first**!
- If you drop each finished item into a tall cardboard box as it finishes, the last thing in the sequence (the sink) lands at the very bottom. The foundational starting item (like "Underwear" or "Math") finishes last and lands at the very top.
- When you dump the box out from top to bottom, you get the perfect order: do the earliest prerequisites first!
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Initialization of Timers and Arrays</summary>

**What are we doing?** We initialize our discovery time array $d$, finish time array $f$, a `Visited` set, an empty `Finish Stack`, and set a global integer variable $\text{time} = 0$.

**Why are we starting here?** To track the order of events during DFS without guessing, every entry into and exit from a function call is timestamped by incrementing a global clock.

**How do we do it?** - Number of vertices: $N = 4$ (nodes $0, 1, 2, 3$).
- Arrays initialized:
  - $d = [\infty, \infty, \infty, \infty]$
  - $f = [\infty, \infty, \infty, \infty]$
  - $\text{Visited} = \emptyset$
  - $\text{Finish Stack} = []$
  - $\text{time} = 0$

**Where did this concept come from?** CLRS (Introduction to Algorithms) standard timestamped DFS. For each node $u$, the interval $[d[u], f[u]]$ represents the active lifetime of $u$ on the call stack.

**System State:**
- **Global Time:** $t = 0$
- **Finish Stack [top ... bottom]:** `[]`
- **Visited:** $\emptyset$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Start DFS(0) and Discover Node 0</summary>

**What changed from Step 1?** We begin the outer DFS loop. The first unvisited node is $0$.

**What are we doing?** Call `DFS(0)`. We advance the clock and record the discovery time of node $0$.

**How do we do it?** 1. Advance clock: $\text{time} = \text{time} + 1 = 0 + 1 = 1$.
2. Record discovery: $d[0] = 1$.
3. Mark visited: $\text{Visited} = \{0\}$.
4. Look at outgoing edges: $\text{Adj}[0] = [1, 3]$.
5. First neighbor is $1$. Since $1 \notin \text{Visited}$, pause `DFS(0)` and call `DFS(1)`.

**System State:**
- **Global Time:** $t = 1$
- **Discovery Times:** $d[0] = 1$
- **Call Stack:** `[DFS(0)]`
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Discover Node 1 and Node 2</summary>

**What changed from Step 2?** Recursion pushes deeper into the graph: $0 \to 1 \to 2$.

**What are we doing?** Advance time for node $1$, then discover sink node $2$.

**How do we do it?**
- **Discovering Node 1:**
  - Advance clock: $\text{time} = 1 + 1 = 2$.
  - Record: $d[1] = 2$.
  - $\text{Visited} = \{0, 1\}$.
  - $\text{Adj}[1] = [2]$. Since $2 \notin \text{Visited}$, pause `DFS(1)` and call `DFS(2)`.
- **Discovering Node 2:**
  - Advance clock: $\text{time} = 2 + 1 = 3$.
  - Record: $d[2] = 3$.
  - $\text{Visited} = \{0, 1, 2\}$.
  - $\text{Adj}[2] = []$ (No outgoing edges!).

**System State:**
- **Global Time:** $t = 3$
- **Discovery Times:** $d[0] = 1, d[1] = 2, d[2] = 3$
- **Call Stack:** `[DFS(0), DFS(1), DFS(2)]`
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Finish Node 2 (First Dead End)</summary>

**What changed from Step 3?** Node $2$ has no neighbors to explore. Its task is fully done.

**What are we doing?** Timestamp the completion of node $2$, push it onto the `Finish Stack`, and pop its call frame.

**Why are we pushing onto the stack right now?** In topological sort, a node is ready to be finalized only when all of its downstream dependencies are completely explored. Because node $2$ has no prerequisites that depend on it, it finishes first.

**How do we do it?** 1. Advance clock: $\text{time} = 3 + 1 = 4$.
2. Record finish time: $f[2] = 4$.
3. Push $2$ to stack: `Finish Stack = [2]`.
4. `DFS(2)` returns to caller `DFS(1)`.

**System State:**
- **Global Time:** $t = 4$
- **Active Intervals:** Node $2$ is closed: $[d[2], f[2]] = [3, 4]$.
- **Finish Stack [top ... bottom]:** `[2]`
- **Call Stack:** `[DFS(0), DFS(1)]`
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Finish Node 1</summary>

**What changed from Step 4?** Control returned to `DFS(1)`. Its only neighbor was $2$, which is now finished.

**What are we doing?** Finalize node $1$, stamp its finish time, push it onto the stack, and backtrack to `DFS(0)`.

**How do we do it?** 1. Advance clock: $\text{time} = 4 + 1 = 5$.
2. Record finish time: $f[1] = 5$.
3. Push $1$ onto stack: `Finish Stack = [1, 2]` (node $1$ sits on top of $2$).
4. `DFS(1)` returns to `DFS(0)`.

**System State:**
- **Global Time:** $t = 5$
- **Closed Intervals:** Node $1$: $[2, 5]$, Node $2$: $[3, 4]$.
- **Finish Stack [top ... bottom]:** `[1, 2]`
- **Call Stack:** `[DFS(0)]`
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Explore Remaining Neighbor of Node 0 (Node 3)</summary>

**What changed from Step 5?** `DFS(0)` resumes. It checked neighbor $1$ (now finished). Its next neighbor in $\text{Adj}[0] = [1, 3]$ is $3$.

**What are we doing?** Discover node $3$, observe that its neighbor $2$ is already visited, and finish node $3$.

**How do we do it?** 1. Advance clock: $\text{time} = 5 + 1 = 6$.
2. Record discovery: $d[3] = 6$.
3. Mark visited: $\text{Visited} = \{0, 1, 2, 3\}$.
4. Check $\text{Adj}[3] = [2]$:
   - Node $2$ is already in $\text{Visited}$ $\implies$ skip! (Do not re-explore).
5. Node $3$ has no more neighbors.
6. Advance clock: $\text{time} = 6 + 1 = 7$.
7. Record finish time: $f[3] = 7$.
8. Push $3$ to stack: `Finish Stack = [3, 1, 2]` (node $3$ sits on top).

**System State:**
- **Global Time:** $t = 7$
- **Closed Intervals:** Node $3$: $[6, 7]$.
- **Finish Stack [top ... bottom]:** `[3, 1, 2]`
- **Call Stack:** `[DFS(0)]`
</details>

<details class="step-card">
<summary class="step-badge">Step 7: Finish Node 0 (Root Completes Last)</summary>

**What changed from Step 6?** Node $0$ has exhausted all its neighbors ($1$ and $3$).

**What are we doing?** Stamp the final finish time on node $0$, push it onto the top of the stack, and terminate the entire algorithm.

**How do we do it?** 1. Advance clock: $\text{time} = 7 + 1 = 8$.
2. Record finish time: $f[0] = 8$.
3. Push $0$ to stack: `Finish Stack = [0, 3, 1, 2]`.
4. Call stack is now empty.

**Final Timestamp Table:**
| Node | Task Name | Discovery $d[u]$ | Finish $f[u]$ | Active Lifespan $[d, f]$ |
| :---: | :---: | :---: | :---: | :---: |
| **0** | Math | 1 | 8 | $[1, 8]$ |
| **1** | Algorithms | 2 | 5 | $[2, 5]$ |
| **2** | Interviews | 3 | 4 | $[3, 4]$ |
| **3** | Machine Learning | 6 | 7 | $[6, 7]$ |
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Pop the Stack to Get Topological Order</summary>

**What is the final answer?** Pop elements from the `Finish Stack` from top to bottom:
$$[0, 3, 1, 2]$$
*(Alternatively: $[0, 1, 3, 2]$, both are completely valid topological sorts!)*

**Why does sorting by decreasing finish times mathematically guarantee a valid order?**
For any directed edge $u \to v$ in a Directed Acyclic Graph:
- When DFS is at node $u$, node $v$ must be explored and must completely finish before the function call for $u$ can finish.
- Therefore, $f[u] > f[v]$ **always holds**.
- Because $u$ finishes after $v$, $u$ is pushed onto the stack after $v$.
- Thus, $u$ pops off the stack **before** $v$. The prerequisite $u$ will always appear before its dependent $v$ in the output!
</details>

</div>

---

## Level 2: Kosaraju's Two-Pass Algorithm for SCCs

### Problem 2.1: Isolating Cyclic Communities Connected by a One-Way Bridge

Consider the following directed graph with $5$ vertices ($A, B, C, D, E$):
- Component 1 has a cycle: $A \to B$, $B \to C$, and $C \to A$.
- Component 2 has a cycle: $D \to E$ and $E \to D$.
- There is a **one-way bridge** from Component 1 to Component 2: edge $C \to D$.

```text
    A ----> B
    ^      /
    |     /
    |    v
    +--- C ----> D <====> E
        [Bridge]
```

We must find all **Strongly Connected Components (SCCs)**. A set of nodes is strongly connected if every node in the set can reach every other node in the set.
- Here, the SCCs are $\{A, B, C\}$ and $\{D, E\}$.
- You can go from $\{A, B, C\}$ to $\{D, E\}$ via bridge $C \to D$, but you can **never** return from $D$ back to $A, B,$ or $C$.

We will trace Kosaraju's algorithm through its 3 fundamental stages:
1. **Pass 1:** Run DFS on the original graph $G$ to order vertices by decreasing finish times onto a stack $S$.
2. **Graph Inversion:** Reverse the direction of every single edge to build the transpose graph $G^T$.
3. **Pass 2:** Pop vertices from stack $S$ and run DFS on $G^T$. Show how the reversed bridge acts like a closed one-way valve, preventing the search from leaking across components.

::: callout-intuition Core Mental Model
Imagine two islands, Island 1 and Island 2, connected by a one-way waterslide from Island 1 down to Island 2.
- On each island, there are circular roads so anyone can visit anyone else on their own island.
- If you start a search on Island 1, water washes you down the waterslide into Island 2. You accidentally mix up both islands into one giant puddle!
- **The Genius Trick (Reversing the Arrows):** Suppose we turn the waterslide around so it flows backwards from Island 2 up into Island 1.
- Now, if you start searching on Island 1 (which finished last in Pass 1), you cannot slide into Island 2 because the slide now points *against* you! You are trapped inside Island 1. You discover $\{A, B, C\}$ and nothing else.
- Edge reversal turns outgoing bridges into incoming walls!
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Pass 1 - DFS on Original Graph G for Finish Times</summary>

**What are we doing?** We run a full DFS on the original graph $G$, pushing nodes onto stack $S$ when each node finishes.

**How do we do it?** Start DFS at $A$:
- Discover $A \implies$ edge $A \to B \implies$ discover $B$.
- Discover $B \implies$ edge $B \to C \implies$ discover $C$.
- From $C$, check neighbor $A$: already visited.
- From $C$, check neighbor $D$ (across the bridge):
  - Discover $D \implies$ edge $D \to E \implies$ discover $E$.
  - From $E$, check neighbor $D$: already visited.
  - Node $E$ has no other neighbors $\implies$ **$E$ finishes!** Push $E$ to stack: $S = [E]$.
  - Return to $D$. $D$ has no more neighbors $\implies$ **$D$ finishes!** Push $D$ to stack: $S = [D, E]$.
- Return to $C$. $C$ has no more neighbors $\implies$ **$C$ finishes!** Push $C$ to stack: $S = [C, D, E]$.
- Return to $B$. $B$ has no more neighbors $\implies$ **$B$ finishes!** Push $B$ to stack: $S = [B, C, D, E]$.
- Return to $A$. $A$ has no more neighbors $\implies$ **$A$ finishes!** Push $A$ to stack: $S = [A, B, C, D, E]$.

**Pass 1 Result:**
Stack $S$ (top to bottom):
$$\text{Stack } S = [A, B, C, D, E]$$

**Why did $A$ end up at the top?** Because $A$ is the source ancestor of the entire chain. Everything downstream had to finish before $A$ could finish. The top of the stack always belongs to the "source" component.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Construct the Transposed Graph G^T</summary>

**What changed from Step 1?** We invert every single directed edge in the graph.

**What are we doing?** If edge $(u \to v)$ exists in $G$, replace it with $(v \to u)$ in $G^T$.

**Why are we doing this?** Within any cycle (like $A \to B \to C \to A$), flipping the arrows ($A \leftarrow B \leftarrow C \leftarrow A$) leaves it as a cycle! Strong connectivity inside a component is completely preserved.  
However, the one-way bridge between components ($C \to D$) becomes $D \to C$. It now points backwards.

**Concrete Edge Inversion:**
- Original $A \to B \implies$ Reversed: $B \to A$
- Original $B \to C \implies$ Reversed: $C \to B$
- Original $C \to A \implies$ Reversed: $A \to C$
- Original $D \to E \implies$ Reversed: $E \to D$
- Original $E \to D \implies$ Reversed: $D \to E$
- **Bridge $C \to D \implies$ Reversed Bridge: $D \to C$**

```text
Transposed Graph G^T:
    A <---- B
    |      ^
    |     /
    v    /
    C <---- D <====> E
     [Reversed Bridge]
```

**Adjacency List of $G^T$:**
- $\text{Adj}_{T}[A] = [C]$
- $\text{Adj}_{T}[B] = [A]$
- $\text{Adj}_{T}[C] = [B]$  *(Notice: $C$ cannot reach $D$ anymore!)*
- $\text{Adj}_{T}[D] = [C, E]$
- $\text{Adj}_{T}[E] = [D]$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Pass 2 - First Pop from Stack (Isolating SCC 1)</summary>

**What changed from Step 2?** We reset our visited set: $\text{Visited} = \emptyset$. We start popping nodes from stack $S = [A, B, C, D, E]$.

**What are we doing?** Pop the top element: it is $A$. Since $A \notin \text{Visited}$, launch a new DFS traversal on the **transposed graph** $G^T$.

**How do we do it?** 1. Mark $A$ as visited: $\text{Visited} = \{A\}$.
2. Current SCC accumulator: $\text{SCC}_1 = [A]$.
3. Explore edges from $A$ in $G^T$:
   - Outgoing edge is $A \to C$.
   - Visit $C$: $\text{Visited} = \{A, C\}$, $\text{SCC}_1 = [A, C]$.
4. Explore edges from $C$ in $G^T$:
   - Outgoing edge is $C \to B$. *(Notice: edge to $D$ no longer exists! The bridge was reversed!)*
   - Visit $B$: $\text{Visited} = \{A, C, B\}$, $\text{SCC}_1 = [A, C, B]$.
5. Explore edges from $B$ in $G^T$:
   - Outgoing edge is $B \to A$.
   - $A$ is already visited $\implies$ stop!
6. No more edges to explore. Traversal terminates!

**Result of First Pop:**
$$\mathbf{SCC}_1 = \{A, B, C\}$$

**Why didn't the search leak into $D$ and $E$?** In the original graph, $C$ pointed to $D$. But in $G^T$, the arrow was flipped to $D \to C$. Node $C$ has zero outgoing paths to $D$. The search was trapped inside $\{A, B, C\}$!
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Pass 2 - Inspecting Stack and Isolating SCC 2</summary>

**What changed from Step 3?** $\text{SCC}_1$ is recorded. $\text{Visited} = \{A, B, C\}$. Stack currently holds:
$$S = [B, C, D, E]$$

**What are we doing?** Continue popping from the stack until we find the next unvisited node.

**How do we do it?** - Pop $B$: Already in $\text{Visited}$ $\implies$ skip.
- Pop $C$: Already in $\text{Visited}$ $\implies$ skip.
- Pop $D$: $D \notin \text{Visited}$!
  - Launch new DFS on $G^T$ from $D$:
  - Mark $D$: $\text{Visited} = \{A, B, C, D\}$, $\text{SCC}_2 = [D]$.
  - Check outgoing edges from $D$ in $G^T$: $\text{Adj}_T[D] = [C, E]$.
    - Neighbor $C$: $C \in \text{Visited}$ already! $\implies$ **Blocked!**
    - Neighbor $E$: $E \notin \text{Visited}$. Visit $E$:
      - $\text{Visited} = \{A, B, C, D, E\}$, $\text{SCC}_2 = [D, E]$.
      - Explore edges from $E$ in $G^T$: $E \to D$.
      - $D \in \text{Visited}$ $\implies$ stop.
- Traversal terminates!

**Result of Second Pop:**
$$\mathbf{SCC}_2 = \{D, E\}$$

- Pop $E$: Already in $\text{Visited}$ $\implies$ skip.
- Stack is empty!
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Summary of Kosaraju's Invariants & Complexity</summary>

**What are the discovered Strongly Connected Components?**
$$\text{Component 1: } \{A, B, C\}$$
$$\text{Component 2: } \{D, E\}$$

**Why does Kosaraju's Algorithm always work? (The Component DAG Principle)**
1. If you collapse every SCC into a single super-node, the graph becomes a Directed Acyclic Graph (the **Component DAG**).
2. Pass 1 finishes the **source** SCC last, ensuring a node from the source SCC sits at the top of the stack.
3. Inverting the edges turns the **source** SCC into a **sink** SCC in $G^T$.
4. A sink has arrows coming in, but **no edges going out**.
5. When Pass 2 begins at the top of the stack, it explores this sink in $G^T$. Because there are no exits, the DFS is physically trapped inside that exact SCC, discovering every node in it and not a single node outside it.

**Time Complexity:**
- Pass 1 (DFS on $G$): $O(V + E)$
- Transpose Graph ($G^T$): $O(V + E)$
- Pass 2 (DFS on $G^T$): $O(V + E)$
$$\text{Total Time} = O(V + E) \quad (\text{Optimal Linear Time})$$

**Space Complexity:**
- Auxiliary Stack + Visited + Transpose adjacency list: $O(V + E)$.
</details>

</div>
