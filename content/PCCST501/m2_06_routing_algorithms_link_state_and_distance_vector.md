# Routing Algorithms: Link-State & Distance-Vector

**Graph abstraction, Dijkstra's Link-State algorithm, the Bellman-Ford Distance-Vector equation, count-to-infinity, and hierarchical routing.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model: The Road Atlas vs. Road Signs
How do you find your way in an unfamiliar country?
* **Link-State (Dijkstra): The Complete GPS Atlas.** Every router collects status reports from every single link in the entire world. It assembles a complete, panoramic topographic map in its memory. Then, sitting with the complete map, it computes the absolute shortest route to every city.
* **Distance-Vector (Bellman-Ford): Reading Local Road Signs.** You don't have a map at all! You stand at an intersection in Munich. A signpost erected by your neighbor Salzburg says: *"Vienna is 300 km via me"*. Another signpost erected by Nuremberg says: *"Vienna is 450 km via me"*. You know Munich-to-Salzburg is 140 km, and Munich-to-Nuremberg is 170 km. You quickly compute:
  * Route via Salzburg: $140 + 300 = 440\text{ km}$
  * Route via Nuremberg: $170 + 450 = 620\text{ km}$
  You pick Salzburg! You didn't need a complete world map — you only combined your **local link costs** with the **estimates whispered by your immediate neighbors**.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

### 2.1 Graph Abstraction of Routing

A network is represented as an undirected graph $G = (V, E)$:
* $V$: Set of routers (vertices).
* $E$: Set of physical links (edges).
* $c(x, y)$: Cost of the link between router $x$ and router $y$. (If no direct link exists, $c(x, y) = \infty$).

---

### 2.2 Link-State (LS) Routing: Dijkstra's Algorithm

In Link-State routing, every router broadcasts its link states (its neighbors and edge costs) to **all routers** in the network using **flooding**. Thus, all nodes share an identical topology map.

#### Dijkstra's Algorithm Definition:
* $N'$: Set of nodes whose least-cost path is definitively determined.
* $D(v)$: Current cost of the shortest path from source node $u$ to destination $v$.
* $p(v)$: Predecessor node along the shortest path from $u$ to $v$.

```
1. Initialization:
   N' = {u}
   For all nodes v adjacent to u:
       D(v) = c(u, v)
       p(v) = u
   For all other nodes v:
       D(v) = infinity

2. Loop:
   Find w not in N' such that D(w) is minimum
   Add w to N'
   Update D(v) for each neighbor v of w not in N':
       D(v) = min( D(v), D(w) + c(w, v) )
       If D(v) changed: p(v) = w

3. Until all nodes are in N'
```

* **Computational Complexity:** $O(|V|^2)$ with standard linear search; $O(|E| \log |V|)$ with a min-heap.
* **Protocol Realization:** **OSPF (Open Shortest Path First)**.

---

### 2.3 Distance-Vector (DV) Routing: Bellman-Ford

Distance-Vector is **distributed, iterative, and asynchronous**:
* Each node $x$ maintains a distance vector $\mathbf{D}_x = [D_x(y) : y \in V]$.
* Each node periodically sends its distance vector to its **immediate neighbors only**.

::: callout-formula KTU Formula Vault: The Bellman-Ford Equation
Let $d_x(y)$ be the cost of the least-cost path from node $x$ to node $y$.
$$d_x(y) = \min_{v \in \text{neighbors}(x)} \left\{ c(x, v) + d_v(y) \right\}$$
where:
* $c(x, v)$ is the cost of the direct link from node $x$ to immediate neighbor $v$.
* $d_v(y)$ is neighbor $v$'s advertised distance to destination $y$.
:::

```mermaid
flowchart LR
    X((Node X)) ---|c(X, V1)| V1((Neighbor V1))
    X ---|c(X, V2)| V2((Neighbor V2))
    V1 -.->|d_V1(Y)| Y((Dest Y))
    V2 -.->|d_V2(Y)| Y
```

---

### 2.4 The Count-to-Infinity Problem & Poisoned Reverse

In Distance-Vector, "good news travels fast, but bad news travels agonizingly slow."

#### The Routing Loop Phenomenon:
Suppose $X - Y - Z$, where $c(X, Y) = 1$ and $c(Y, Z) = 1$. Both $Y$ and $Z$ know they can reach $X$ with costs $1$ and $2$ respectively.
1. Suddenly, link $c(X, Y)$ breaks ($\infty$).
2. $Y$ needs to find a route to $X$. $Y$ sees that neighbor $Z$ advertises: *"I can reach $X$ with cost 2!"*
3. $Y$ thinks: *"Aha! I can reach $X$ via $Z$ with cost $c(Y, Z) + d_Z(X) = 1 + 2 = 3$!"*
4. $Y$ updates its table and tells $Z$: *"My distance to $X$ is 3"*.
5. $Z$ hears this and updates its distance: $1 + 3 = 4$.
6. $Y$ and $Z$ bounce packets back and forth, slowly counting up: $5, 6, 7, \dots$ until reaching $\infty$ (typically defined as $16$ in RIP).

#### Poisoned Reverse Solution:
If node $Z$ routes through node $Y$ to reach destination $X$, $Z$ deliberately advertises to $Y$ that:
$$d_Z(X) = \infty$$
$Z$ tells everyone else its true distance, but "lies" to $Y$ so that $Y$ will never attempt to route back through $Z$ to get to $X$.  
*(Note: Poisoned Reverse prevents 2-node loops, but does not completely prevent loops involving 3 or more nodes).*

---

### 2.5 Link-State vs. Distance-Vector: Comprehensive Comparison

| Metric | Link-State (Dijkstra / OSPF) | Distance-Vector (Bellman-Ford / RIP) |
|---|---|---|
| **Knowledge** | Global topology map at every node | Local link costs + neighbor distance vectors only |
| **Message Complexity** | Higher: $O(|V| \cdot |E|)$ messages flooded globally | Lower: Messages exchanged between immediate neighbors only |
| **Convergence Speed** | Very fast: $O(|V|^2)$ local CPU calculation | Slower: Can suffer routing loops and Count-to-Infinity |
| **Robustness** | High: Node computes its own paths; incorrect advertisements isolated | Vulnerable: A single malfunctioning node can broadcast false zero-cost paths that poison entire network |

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Consider a 4-node network with nodes $u, v, w, x$.
* $c(u, v) = 2$
* $c(u, w) = 5$
* $c(u, x) = 1$
* $c(x, v) = 2$
* $c(x, w) = 3$
* $c(v, w) = 3$
Compute the shortest path from source node $u$ to all other nodes using **Dijkstra's Algorithm**.
:::

::: step [Step 2: Execution] Tabular Trace of Dijkstra's Algorithm
Let columns represent $D(v), p(v) \mid D(w), p(w) \mid D(x), p(x)$:

| Step | $N'$ | $D(v), p(v)$ | $D(w), p(w)$ | $D(x), p(x)$ | Action Taken |
|:---:|:---:|:---:|:---:|:---:|:---|
| **Init** | $\{u\}$ | $2, u$ | $5, u$ | $\mathbf{1, u}$ | Node $x$ has minimum distance ($1$). Add $x$ to $N'$. |
| **1** | $\{u, x\}$ | $\mathbf{2, u}$ | $\min(5, 1 + 3) = 4, x$ | — | Check neighbors of $x$: $D(w)$ updates from $5$ to $4$ via $x$. $D(v)$ remains $2$. Minimum is $v$ ($2$). Add $v$ to $N'$. |
| **2** | $\{u, x, v\}$ | — | $\min(4, 2 + 3) = \mathbf{4, x}$ | — | Neighbors of $v$: Path via $v$ to $w$ is $2 + 3 = 5 > 4$. Keep $D(w) = 4$. Add $w$ to $N'$. |
| **3** | $\{u, x, v, w\}$ | — | — | — | All nodes permanently assigned. Done! |
:::

::: step [Step 3: Conclusion] Final Shortest Path Tree
* Shortest path to $x$: $u \to x$ with cost $= \mathbf{1}$
* Shortest path to $v$: $u \to v$ with cost $= \mathbf{2}$
* Shortest path to $w$: $u \to x \to w$ with cost $= 1 + 3 = \mathbf{4}$ (predecessor is $x$)
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Bellman-Ford Calculation
Node X has two neighbors: A and B. $c(X, A) = 2$, and $c(X, B) = 7$. Neighbor A reports $D_A(Y) = 6$, and Neighbor B reports $D_B(Y) = 1$. What is node X's computed distance $D_X(Y)$ to destination Y?
(A) 9
(*B) 8
(C) 7
(D) 13
::: explanation
Applying the Bellman-Ford equation:  
$D_X(Y) = \min( c(X, A) + D_A(Y), \; c(X, B) + D_B(Y) ) = \min(2 + 6, \; 7 + 1) = \min(8, 8) = 8$.
:::

::: quiz Q2: Poisoned Reverse
What does the Poisoned Reverse technique do in Distance-Vector routing?
(A) It turns off all routing timers
(*B) If node Z routes through node Y to reach destination X, Z advertises to Y that its distance to X is infinity
(C) It deletes all entries in the forwarding table when a packet drops
(D) It switches the network from IPv4 to IPv6
::: explanation
Poisoned reverse prevents a two-node routing loop. By lying to Y that $D_Z(X) = \infty$, node Y will never mistakenly choose to route through Z when its own direct link to X fails.
:::

::: quiz Q3: Link-State Algorithm Scope
Why does Link-State routing converge faster than Distance-Vector routing?
(A) Because Link-State packets travel faster than the speed of light
(B) Because Link-State does not use IP addresses
(*C) Because each node already has the complete global network topology in memory and computes all shortest paths locally using Dijkstra's algorithm
(D) Because Distance-Vector does not use routers
::: explanation
In Link-State routing, once LSAs are flooded, every router has the full topology map and runs Dijkstra's algorithm locally without waiting for multi-hop iterative updates from neighbors.
:::
