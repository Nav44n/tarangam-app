# Progressive Problems: Routing Algorithms (Link-State & Distance-Vector)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped steps, and full line-by-line mathematical proofs and routing table state traces.

---

## Level 1: 6-Node Dijkstra's Algorithm Tabular Trace

### Problem 1.1: Shortest Path Tree and Forwarding Table Construction from Root Node $u$

**Problem Statement:** Consider a network graph consisting of $6$ routers represented as nodes:  
$$V = \{u, v, w, x, y, z\}$$  
The links between adjacent nodes have the following symmetric non-negative transmission costs:
- Between $u$ and its neighbors: $c(u,v) = 2$, $c(u,x) = 1$, $c(u,w) = 5$
- Between $x$ and its other neighbors: $c(x,v) = 2$, $c(x,w) = 3$, $c(x,y) = 1$
- Between $v$ and its other neighbors: $c(v,w) = 3$, $c(v,y) = 2$
- Between $w$ and its other neighbors: $c(w,y) = 1$, $c(w,z) = 5$
- Between $y$ and its other neighbor: $c(y,z) = 2$
- Any pair of nodes not listed above does not share a direct link, meaning the direct link cost is $c(a,b) = \infty$.

Execute **Dijkstra's Algorithm** from the perspective of source node $u$:
1. Define every mathematical variable: $N'$, $D(v)$, and $p(v)$.
2. Trace the step-by-step execution across all iterations, building the full execution table.
3. Draw the resulting Shortest Path Tree rooted at $u$.
4. Construct the final local forwarding table for router $u$ (mapping destination node to next-hop interface/neighbor).

::: callout-intuition Core Mental Model
Think of routing algorithms like planning a road trip:
- **Link-State (Dijkstra):** You have a **complete GPS road atlas** of the entire country open on your passenger seat. You see every highway, intersection, and toll cost across the whole continent at once. Before starting your car engine, you run Dijkstra's algorithm in your head to calculate the absolute shortest path to every city.
- **Distance-Vector (Bellman-Ford):** You have **zero map**. You only see the street signs at the intersection right in front of you, plus what your immediate neighbors shout across the fence: *"Hey, Chicago is 300 miles east of me!"* You make routing decisions purely by combining local road signs with gossip from immediate neighbors.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Define Mathematical Notation and Initialization Rules</div>

**What are we doing?** Establishing the three foundational state variables used in Dijkstra's algorithm.

**Why are we starting here?** A student cannot fill out a state table without knowing what the column headers ($N'$, $D(m)$, $p(m)$) physically mean.

**How do we do it?** We define:
1. **$N'$ (Set of Known Nodes):** The set of nodes whose least-cost paths from source $u$ have been permanently calculated and finalized.
2. **$D(m)$ (Current Cost to Node $m$):** The current minimum cost to travel from the source node $u$ to destination node $m$ along currently discovered paths. If no path is known yet, $D(m) = \infty$.
3. **$p(m)$ (Predecessor / Parent of $m$):** The immediate neighbor that comes right before node $m$ along the current shortest path from $u$. In our table, we write each cell as:
$$D(m), p(m)$$
*(Example: "$2, u$" means the path to this node currently costs $2$, and the packet steps directly from $u$ to get there).*

**Where did this formula/concept come from?** Edsger W. Dijkstra (1959), *"A Note on Two Problems in Connexion with Graphs"*. It is the classic greedy algorithm for the single-source shortest path problem on graphs with non-negative edge weights.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Initialization Step (Step 0)</div>

**What changed from Step 1?** We have our definitions. Now we place our source node $u$ into the known set $N'$ and evaluate all its direct immediate neighbors.

**What are we doing?** Computing the initial row (Step 0) of our algorithm.

**Why are we doing this?** Node $u$ is our starting root. The cost to travel from $u$ to itself is zero ($D(u) = 0$). We examine all edges connected directly to $u$:
- If a node $m$ is directly connected to $u$, set $D(m) = c(u,m)$ and parent $p(m) = u$.
- If a node $m$ is not directly connected to $u$, set $D(m) = \infty$.

**How do we do it?** 1. Place $u$ into $N'$:  
$$N' = \{u\}$$
2. Inspect every other node in the graph:
- For node $v$: Direct link exists with cost $2$. Set:  
$$D(v) = 2, \quad p(v) = u \implies \mathbf{2, u}$$
- For node $x$: Direct link exists with cost $1$. Set:  
$$D(x) = 1, \quad p(x) = u \implies \mathbf{1, u}$$
- For node $w$: Direct link exists with cost $5$. Set:  
$$D(w) = 5, \quad p(w) = u \implies \mathbf{5, u}$$
- For node $y$: No direct link exists to $u$. Set:  
$$D(y) = \infty$$
- For node $z$: No direct link exists to $u$. Set:  
$$D(z) = \infty$$

**State of Row 0:**
$$N' = \{u\} \quad\big|\quad D(v),p(v) = 2,u \quad\big|\quad D(w),p(w) = 5,u \quad\big|\quad D(x),p(x) = \mathbf{1,u} \quad\big|\quad D(y),p(y) = \infty \quad\big|\quad D(z),p(z) = \infty$$

Now we find the node not in $N'$ with the absolute smallest $D$:  
$$\min\{D(v)=2, D(w)=5, D(x)=1, D(y)=\infty, D(z)=\infty\} = D(x) = 1$$  
Node **$x$** wins! We permanently lock node $x$ into $N'$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Iteration 1 — Expand from Node $x$</div>

**What changed from Step 2?** Node $x$ has now been added to $N'$. We can now check if traveling through $x$ provides a faster detour to any remaining unfinalized nodes.

**What are we doing?** Updating $N'$ and applying Dijkstra's relaxation formula to all nodes not yet in $N'$.

**Why are we doing this?** The core invariant of Dijkstra's algorithm is the **relaxation step**:  
$$D(m) \leftarrow \min\big(D(m), \; D(w^*) + c(w^*, m)\big)$$  
where $w^*$ is the newly locked node ($x$). We check if $u \to x \to m$ is cheaper than the previously recorded path to $m$.

**How do we do it?** 1. Update known set:  
$$N' = \{u, x\}$$  
Currently, the cost to reach $x$ is $D(x) = 1$.  
2. Evaluate neighbors of $x$ that are not in $N'$ ($\{v, w, y, z\}$):
- **For node $v$:** Old cost was $D(v) = 2$ (via $u$).  
  Path through $x$: $D(x) + c(x,v) = 1 + 2 = 3$.  
  Compare: $\min(2, 3) = 2$.  
  The direct path $u \to v$ is shorter! Retain: $\mathbf{2, u}$.
- **For node $w$:** Old cost was $D(w) = 5$ (via $u$).  
  Path through $x$: $D(x) + c(x,w) = 1 + 3 = 4$.  
  Compare: $\min(5, 4) = 4$.  
  $4 < 5$, so we found a shortcut through $x$!  
  Update: $D(w) = 4, \quad p(w) = x \implies \mathbf{4, x}$.
- **For node $y$:** Old cost was $D(y) = \infty$.  
  Path through $x$: $D(x) + c(x,y) = 1 + 1 = 2$.  
  Compare: $\min(\infty, 2) = 2$.  
  Update: $D(y) = 2, \quad p(y) = x \implies \mathbf{2, x}$.
- **For node $z$:** No direct link from $x$ to $z$ ($c(x,z) = \infty$).  
  Retain: $\infty$.

3. Pick the minimum among unfinalized nodes $\{v, w, y, z\}$:  
$$D(v) = 2, \quad D(w) = 4, \quad D(y) = 2, \quad D(z) = \infty$$  
There is a tie between $v$ and $y$ (both have cost $2$). By standard convention, we can break ties arbitrarily; let us choose node **$v$** (or $y$; choosing $y$ produces the exact same final costs). Let us pick **$y$** here because it directly connects to $z$ and opens new avenues.  
*(Let us lock node **$y$**)*.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Iteration 2 — Expand from Node $y$</div>

**What changed from Step 3?** Node $y$ is now permanently added to $N'$. We check whether going through $y$ offers faster routes to $\{v, w, z\}$.

**What are we doing?** Updating $N'$ and relaxing paths using $D(y) = 2$.

**How do we do it?** 1. Update known set:  
$$N' = \{u, x, y\}$$  
2. Evaluate unfinalized nodes $\{v, w, z\}$ using $D(y) = 2$:
- **For node $v$:** Old cost was $D(v) = 2$ (via $u$).  
  Path through $y$: $D(y) + c(y,v) = 2 + 2 = 4$.  
  $\min(2, 4) = 2$. Keep: $\mathbf{2, u}$.
- **For node $w$:** Old cost was $D(w) = 4$ (via $x$).  
  Path through $y$: $D(y) + c(y,w) = 2 + 1 = 3$.  
  Compare: $\min(4, 3) = 3$.  
  $3 < 4$, so going through $y$ is an even better shortcut!  
  Update: $D(w) = 3, \quad p(w) = y \implies \mathbf{3, y}$.
- **For node $z$:** Old cost was $D(z) = \infty$.  
  Path through $y$: $D(y) + c(y,z) = 2 + 2 = 4$.  
  Compare: $\min(\infty, 4) = 4$.  
  Update: $D(z) = 4, \quad p(z) = y \implies \mathbf{4, y}$.

3. Find the minimum among unfinalized nodes $\{v, w, z\}$:  
$$D(v) = 2, \quad D(w) = 3, \quad D(z) = 4$$  
Minimum is $D(v) = 2$.  
Node **$v$** wins! We lock node $v$ into $N'$.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Iteration 3 — Expand from Node $v$</div>

**What changed from Step 4?** Node $v$ is now added to $N'$. We check whether paths through $v$ can improve our routes to the remaining nodes $\{w, z\}$.

**What are we doing?** Updating $N'$ and checking relaxation through $D(v) = 2$.

**How do we do it?** 1. Update known set:  
$$N' = \{u, x, y, v\}$$  
2. Evaluate remaining nodes $\{w, z\}$ using $D(v) = 2$:
- **For node $w$:** Old cost was $D(w) = 3$ (via $y$).  
  Path through $v$: $D(v) + c(v,w) = 2 + 3 = 5$.  
  Compare: $\min(3, 5) = 3$. Keep: $\mathbf{3, y}$.
- **For node $z$:** Old cost was $D(z) = 4$ (via $y$).  
  $v$ does not have a direct link to $z$ ($c(v,z) = \infty$).  
  Keep: $\mathbf{4, y}$.

3. Find the minimum among remaining nodes $\{w, z\}$:  
$$D(w) = 3, \quad D(z) = 4$$  
Minimum is $D(w) = 3$.  
Node **$w$** wins! We lock node $w$ into $N'$.
</div>

<div class="step-card">
<div class="step-badge">Step 6: Iteration 4 & 5 — Finalize Nodes $w$ and $z$</div>

**What changed from Step 5?** Node $w$ is locked. Only node $z$ remains unfinalized.

**What are we doing?** Checking if traveling through $w$ improves the path to $z$, then locking $z$.

**How do we do it?** 1. Update known set:  
$$N' = \{u, x, y, v, w\}$$  
2. Evaluate node $z$ using $D(w) = 3$:
- **For node $z$:** Old cost was $D(z) = 4$ (via $y$).  
  Path through $w$: $D(w) + c(w,z) = 3 + 5 = 8$.  
  Compare: $\min(4, 8) = 4$.  
  The path through $y$ is much better ($4 < 8$). Keep: $\mathbf{4, y}$.

3. Only node $z$ remains:  
Node **$z$** is selected with cost $D(z) = 4$.  
$$N' = \{u, x, y, v, w, z\}$$  
All 6 nodes are now in $N'$. The algorithm terminates!
</div>

<div class="step-card">
<div class="step-badge">Step 7: Master Dijkstra Execution Table</div>

**What changed from Step 6?** We collect all rows from Step 0 through Step 4 into the standard academic examination table.

**What are we doing?** Presenting the complete, clean Dijkstra trace matrix.

**How do we do it?**

| Step | $N'$ | $D(v), p(v)$ | $D(w), p(w)$ | $D(x), p(x)$ | $D(y), p(y)$ | $D(z), p(z)$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **0** | $\{u\}$ | $2, u$ | $5, u$ | $\mathbf{1, u}$ | $\infty$ | $\infty$ |
| **1** | $\{u, x\}$ | $2, u$ | $4, x$ | — | $\mathbf{2, x}$ | $\infty$ |
| **2** | $\{u, x, y\}$ | $\mathbf{2, u}$ | $3, y$ | — | — | $4, y$ |
| **3** | $\{u, x, y, v\}$ | — | $\mathbf{3, y}$ | — | — | $4, y$ |
| **4** | $\{u, x, y, v, w\}$ | — | — | — | — | $\mathbf{4, y}$ |
| **Final** | $\{u, x, y, v, w, z\}$ | Locked ($2$) | Locked ($3$) | Locked ($1$) | Locked ($2$) | Locked ($4$) |
</div>

<div class="step-card">
<div class="step-badge">Step 8: Construct the Shortest Path Tree and Forwarding Table</div>

**What changed from Step 7?** We trace the predecessor pointers $p(m)$ backwards from each destination to root $u$ to build the routing paths.

**What are we doing?** Reconstructing the Shortest Path Tree (SPT) and generating router $u$'s forwarding table.

**How do we do it?** Trace each destination node back to $u$:
- **Destination $x$:** $p(x) = u$. Path: $u \to x$ (Cost: $1$). First hop: **$x$**.
- **Destination $v$:** $p(v) = u$. Path: $u \to v$ (Cost: $2$). First hop: **$v$**.
- **Destination $y$:** $p(y) = x$, and $p(x) = u$. Path: $u \to x \to y$ (Cost: $1 + 1 = 2$). First hop: **$x$**.
- **Destination $w$:** $p(w) = y$, $p(y) = x$, $p(x) = u$. Path: $u \to x \to y \to w$ (Cost: $1 + 1 + 1 = 3$). First hop: **$x$**.
- **Destination $z$:** $p(z) = y$, $p(y) = x$, $p(x) = u$. Path: $u \to x \to y \to z$ (Cost: $1 + 1 + 2 = 4$). First hop: **$x$**.

```
Shortest Path Tree Rooted at u:

       (u)
      /   \
 (2) /     \ (1)
    v       x
             \
              \ (1)
               y
              / \
         (1) /   \ (2)
            w     z
```

**Final Forwarding Table for Router $u$:**

| Destination | Total Path Cost | Full Path Sequence | Next-Hop Neighbor (Outgoing Interface) |
| :---: | :---: | :---: | :---: |
| **$v$** | $2$ | $u \to v$ | Link $(u, v)$ |
| **$x$** | $1$ | $u \to x$ | Link $(u, x)$ |
| **$y$** | $2$ | $u \to x \to y$ | Link $(u, x)$ |
| **$w$** | $3$ | $u \to x \to y \to w$ | Link $(u, x)$ |
| **$z$** | $4$ | $u \to x \to y \to z$ | Link $(u, x)$ |
</div>

<div class="step-card">
<div class="step-badge">Final Step: Sanity Check and Verification</div>

**What is the final answer?**
- Minimal costs from $u$: $D(x)=1$, $D(v)=2$, $D(y)=2$, $D(w)=3$, $D(z)=4$.  
- All traffic destined for $x, y, w,$ and $z$ exits router $u$ via neighbor $x$. Traffic destined for $v$ exits directly via neighbor $v$.

**Why does this answer make sense?** Even though node $w$ has a direct physical link to $u$ ($c(u,w) = 5$), taking the multi-hop detour through $x$ and $y$ ($u \to x \to y \to w$) only costs $1 + 1 + 1 = 3$. Dijkstra's algorithm discovered that the detour saves $40\%$ of the transmission cost compared to the direct link.
</div>

</div>

---

## Level 2: Bellman-Ford Distance Vector Exchange and the Count-to-Infinity Problem

### Problem 2.1: Distributed Routing and Failure Dynamics in a 3-Node Linear Topology

**Problem Statement:** Consider a linear 3-node network topology:  
$$\text{X} \longleftrightarrow \text{Y} \longleftrightarrow \text{Z}$$  
Initial physical link costs are:
$$c(X,Y) = 1, \quad c(Y,Z) = 1, \quad c(X,Z) = \infty \text{ (no direct link)}$$  
1. State the **Bellman-Ford Equation** used by distance-vector protocols.  
2. Show the initial distance vector tables for nodes $X$, $Y$, and $Z$, and show how they converge to the true shortest distances to destination $X$.  
3. **Simulate a Link Failure:** Suppose the link between $X$ and $Y$ suddenly breaks ($c(X,Y)$ becomes $\infty$). Trace the step-by-step table updates between $Y$ and $Z$ to show how a **routing loop** is created and why the estimated distance counts up incrementally (**Count-to-Infinity Problem**).  
4. Explain how the **Poisoned Reverse** heuristic works and show how it prevents this specific 2-node loop.

::: callout-intuition Core Mental Model
Imagine three people standing in a line in a dark tunnel: **Alice ($X$)**, **Bob ($Y$)**, and **Charlie ($Z$)**.  
- In normal times, Bob tells Charlie: *"Alice is standing right next to me! It takes 1 step to reach her."* Charlie says: *"Great! It takes 1 step to reach Bob, and Bob says Alice is 1 step from him, so Alice is $1 + 1 = 2$ steps from me!"*
- **The Disaster:** Alice quietly walks away and leaves the tunnel. Bob tries to reach her, but finds empty space ($cost = \infty$).  
- Bob turns to Charlie: *"Do you know how to get to Alice?"* Charlie proudly replies: *"Sure! My signpost says Alice is 2 steps away through you!"*
- Bob fails to realize that Charlie's path **goes right back through Bob himself**! Bob thinks: *"Oh! Charlie knows a secret back door to Alice that takes 2 steps! If I go through Charlie, I can reach Alice in $1 + 2 = 3$ steps!"*
- Bob tells Charlie: *"Hey, my cost to Alice is now 3!"* Charlie updates: *"Then my cost is now $1 + 3 = 4$!"* They pass this false hope back and forth, counting up toward infinity ($3 \to 4 \to 5 \to 6 \dots$) while Alice is long gone!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: The Bellman-Ford Equation Defined</div>

**What are we doing?** Stating and explaining the mathematical formula that governs all distance-vector protocols (such as RIP).

**Why are we starting here?** Every numerical update in a distance-vector router is driven directly by this exact equation.

**How do we do it?** Let $d_x(y)$ be the cost of the least-cost path from node $x$ to destination $y$.  
The Bellman-Ford equation states:  
$$d_x(y) = \min_{v} \big\{ c(x,v) + d_v(y) \big\}$$  
where the min is taken over all immediate physical neighbors $v$ of node $x$.

**Meaning of Terms:**
- $c(x,v)$: The physical cost to take one single hop from $x$ to neighbor $v$.
- $d_v(y)$: The neighbor $v$'s advertised estimate of its own shortest path to destination $y$.
- $c(x,v) + d_v(y)$: The total cost of traveling from $x$ to $y$ *if you choose neighbor $v$ as your next hop*.

**Where did this formula/concept come from?** Richard Bellman (1958) and Lester Ford Jr. (1956). Dynamic programming formulation for shortest paths.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Trace Stable Converged State to Destination $X$</div>

**What changed from Step 1?** We apply the equation to our linear network $X - Y - Z$ to see what the tables look like when the network is healthy and stable.

**What are we doing?** Calculating the distance vector entries for destination $X$ across nodes $Y$ and $Z$.

**How do we do it?**
- **At Router $Y$:** Its neighbors are $X$ and $Z$.  
  Cost via neighbor $X$: $c(Y,X) + d_X(X) = 1 + 0 = 1$.  
  Cost via neighbor $Z$: $c(Y,Z) + d_Z(X) = 1 + 2 = 3$.  
  $$d_Y(X) = \min(1, 3) = \mathbf{1} \quad (\text{Next Hop: } X)$$  

- **At Router $Z$:** Its only neighbor is $Y$.  
  Cost via neighbor $Y$: $c(Z,Y) + d_Y(X) = 1 + 1 = 2$.  
  $$d_Z(X) = \mathbf{2} \quad (\text{Next Hop: } Y)$$  

Both nodes have accurate, stable routing information. Packets from $Z$ travel $Z \to Y \to X$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: The Link Failure Event ($c(X,Y) \to \infty$)</div>

**What changed from Step 2?** At time $t_0$, the cable connecting $X$ and $Y$ is cut.

**What are we doing?** Showing the immediate local detection at node $Y$.

**Why are we doing this?** To see how node $Y$ tries to recover using its existing routing table.

**How do we do it?** At time $t_0$, router $Y$ detects that its direct link to $X$ is dead:  
$$c(Y,X) = \infty$$  
Router $Y$ immediately recomputes its shortest path to destination $X$ using the Bellman-Ford equation:  
$$d_Y(X) = \min \big\{ c(Y,X) + d_X(X), \; c(Y,Z) + d_Z(X) \big\}$$  
Substitute the values $Y$ currently has stored in its memory:  
1. Path via neighbor $X$: $\infty + 0 = \infty$.  
2. Path via neighbor $Z$: $c(Y,Z) + d_Z(X) = 1 + 2 = 3$ *(because $Z$ previously advertised $d_Z(X) = 2$)*.  

$$d_Y(X) = \min(\infty, 3) = \mathbf{3}$$  
**The Fatal Error Occurs Here:** Router $Y$ updates its routing table:  
*"To reach $X$, send the packet to neighbor $Z$ with total cost $3$!"* Node $Y$ does not know that $Z$'s path to $X$ originally depended on routing through $Y$ itself! A **Routing Loop** is now formed between $Y$ and $Z$:  
$Y$ forwards to $Z$, and $Z$ forwards to $Y$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Step-by-Step Count-to-Infinity Trace</div>

**What changed from Step 3?** Router $Y$ updated its cost to $3$. Now $Y$ broadcasts its new distance vector to its neighbor $Z$.

**What are we doing?** Tracing the Ping-Pong message exchange between $Y$ and $Z$ that causes the cost to crawl up to infinity.

**How do we do it?** Follow the sequential iteration rounds:

- **Round 1:**
  - $Y$ sends vector update to $Z$: *"My cost to $X$ is now $d_Y(X) = 3$."*
  - Router $Z$ receives this message and re-evaluates its Bellman-Ford equation:  
    $$d_Z(X) = c(Z,Y) + d_Y(X) = 1 + 3 = \mathbf{4}$$  
    $Z$ updates its cost to $4$ (Next Hop still $Y$).

- **Round 2:**
  - $Z$ sends vector update to $Y$: *"My cost to $X$ is now $d_Z(X) = 4$."*
  - Router $Y$ receives this message and recomputes:  
    $$d_Y(X) = c(Y,Z) + d_Z(X) = 1 + 4 = \mathbf{5}$$  
    $Y$ updates its cost to $5$ (Next Hop still $Z$).

- **Round 3:**
  - $Y$ sends vector update to $Z$: *"My cost to $X$ is now $d_Y(X) = 5$."*
  - Router $Z$ receives this message and recomputes:  
    $$d_Z(X) = c(Z,Y) + d_Y(X) = 1 + 5 = \mathbf{6}$$  
    $Z$ updates its cost to $6$.

- **Successive Rounds:** The values iterate relentlessly:  
$$d_Y(X) = 7 \implies d_Z(X) = 8 \implies d_Y(X) = 9 \implies \dots$$  
This loop continues counting up by $+1$ on every iteration until the cost reaches whatever value the protocol defines as "infinity" (for example, in the RIP protocol, $\infty = 16$). Only after reaching $16$ does the protocol finally declare destination $X$ unreachable!
</div>

<div class="step-card">
<div class="step-badge">Step 5: The Poisoned Reverse Solution Explained</div>

**What changed from Step 4?** We saw how the loop formed because $Z$ advertised a path to $Y$ that relied on $Y$. Now we introduce the heuristic designed to stop this: **Poisoned Reverse**.

**What are we doing?** Defining the Poisoned Reverse rule and showing how it modifies distance vector advertisements.

**Why are we doing this?** To prevent node $Y$ from ever choosing $Z$ as a path to $X$ when $Z$'s path already goes through $Y$.

**How do we do it?** **The Poisoned Reverse Rule:**
> *"If node $Z$ routes traffic to destination $X$ through neighbor $Y$, then whenever $Z$ sends its distance vector update to $Y$, $Z$ must intentionally lie and advertise that its distance to $X$ is INFINITY ($d_Z(X) = \infty$)."*

By lying to $Y$, $Z$ ensures that $Y$ will never attempt to route traffic back through $Z$ to reach $X$!

Let us trace what happens when link $(X,Y)$ breaks with Poisoned Reverse enabled:
1. Since $Z$ routes to $X$ through $Y$, $Z$ advertises to $Y$:  
   $$d_Z(X) = \infty$$  
   *(Even though locally $Z$ knows its true cost is $2$ via $Y$, it tells $Y$ that its cost is $\infty$).*
2. At time $t_0$, the link $(X,Y)$ breaks ($c(X,Y) = \infty$).
3. Router $Y$ recomputes Bellman-Ford:  
   - Cost via $X$: $\infty + 0 = \infty$.  
   - Cost via $Z$: $c(Y,Z) + d_Z(X) = 1 + \infty = \infty$.  
   $$d_Y(X) = \min(\infty, \infty) = \mathbf{\infty}$$  
4. Router $Y$ immediately discovers that $X$ is completely unreachable!  
   $Y$ does not select $Z$, no loop is formed, and the count-to-infinity problem is stopped on Step 1.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary Comparison between Link-State and Distance-Vector</div>

**What is the final answer?** A side-by-side comparison of the two routing paradigms:

| Metric / Dimension | Link-State (Dijkstra) | Distance-Vector (Bellman-Ford) |
| :--- | :--- | :--- |
| **Network Knowledge** | Global: Every router knows the complete graph topology. | Local: Routers only know physical neighbor costs and neighbor vector estimates. |
| **Algorithm Used** | Dijkstra's Shortest Path Algorithm. | Bellman-Ford Dynamic Programming Equation. |
| **Message Overhead** | Link-State Advertisements (LSAs) flooded over the entire network. | Distance vectors exchanged strictly between immediate neighbors. |
| **Convergence Speed** | Rapid ($O(V^2)$ or $O(E \log V)$ computation, no loops). | Slow; prone to routing loops and count-to-infinity. |
| **Robustness** | A single malfunctioning router rarely corrupts other routers' map views. | Bad information can propagate from router to router (e.g., false cost gossip). |
| **Loop Mitigation** | Not needed (Shortest Path Tree is loop-free by definition). | Split Horizon, Poisoned Reverse, and finite infinity caps ($\infty = 16$). |

**Why does this answer make sense?** Link-State uses complete global visibility to build a single loop-free tree from the top down. Distance-Vector relies on distributed telephone-game gossip from immediate neighbors; without safeguards like Poisoned Reverse, nodes can easily confuse their own reflected echoes for new valid paths.
</div>

</div>

---

<a id="self-check"></a>
## Active Recall Checkpoint

::: quiz Q1: Shortest Path Predecessors
In Dijkstra's algorithm, if the predecessor array records $p(z) = y$, $p(y) = x$, and $p(x) = u$, what is the complete path from source node $u$ to destination node $z$?
(A) $u \to z$
(B) $u \to y \to z$
(*C) $u \to x \to y \to z$
(D) $u \to v \to w \to z$
::: explanation
Following the predecessor links backwards from $z$: $z \leftarrow y \leftarrow x \leftarrow u$. Reversing gives the path from the root: $u \to x \to y \to z$.
:::

::: quiz Q2: Bellman-Ford Cost Update
In Distance-Vector routing, node A has neighbors B and C. $c(A, B) = 3$, $c(A, C) = 4$. If neighbor B advertises $D_B(D) = 5$, and neighbor C advertises $D_C(D) = 2$, what is node A's least cost to destination D?
(A) 8
(B) 7
(*C) 6
(D) 2
::: explanation
Using Bellman-Ford: $D_A(D) = \min\{ c(A, B) + D_B(D), \; c(A, C) + D_C(D) \} = \min\{ 3 + 5, \; 4 + 2 \} = \min\{ 8, 6 \} = 6$ (via neighbor C).
:::
