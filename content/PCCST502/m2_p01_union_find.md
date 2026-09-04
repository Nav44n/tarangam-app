# Progressive Problems: Disjoint Sets & Union-Find (DSU)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Level 1: Naive Union-Find

### Problem 1.1: Building a Group from Scratch (MakeSet and Linear Chain Union)

Suppose we have $4$ students labeled with identification numbers: $0, 1, 2,$ and $3$. Initially, nobody knows anybody. We need to:
1. Initialize the disjoint set structure (`MakeSet`).
2. Perform `Union(0, 1)`, where student $0$ becomes the parent of student $1$.
3. Perform `Union(1, 2)`, where the root of $1$ becomes the parent of student $2$.
4. Perform `Union(2, 3)`, where the root of $2$ becomes the parent of student $3$.
5. Run `Find(3)` to determine which student is the ultimate group leader (root).

::: callout-intuition Core Mental Model
Imagine each student is standing in a room holding a piece of paper. On that paper, they write down the name of their direct "team leader." 
- At the start, nobody knows anyone, so every student writes down their **own** number on their paper. They are their own boss!
- When two groups merge, the leader of one group agrees to report to the leader of the other group.
- To find out who is running the whole show for any student, you follow the names on the papers up the chain until you reach someone whose paper says their own name. That person is the **Root (Ultimate Leader)**.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Initialize Sets with MakeSet</div>

**What are we doing?** We are creating an array called `parent` of size $4$ (indices $0$ to $3$). For every index $i$, we set `parent[i] = i`.

**Why are we starting here?** Before we can group people together, every person must exist as an independent single-person group.

**How do we do it?** We iterate from $i = 0$ to $3$, assigning each slot its own index:
- `parent[0] = 0`
- `parent[1] = 1`
- `parent[2] = 2`
- `parent[3] = 3`

**Where did this formula/concept come from?** In a forest of trees, a node is defined as a "root" if it points to itself:
$$\text{is\_root}(i) \iff \text{parent}[i] == i$$
By pointing each item to itself, we create $4$ separate trees, each with height $0$.

**Array State:**
| Index ($i$) | 0 | 1 | 2 | 3 |
| :--- | :---: | :---: | :---: | :---: |
| **`parent[i]`** | **0** | **1** | **2** | **3** |

*Tree Structure:* $(0)$, $(1)$, $(2)$, $(3)$ (All isolated roots)
</div>

<div class="step-card">
<div class="step-badge">Step 2: Perform Union(0, 1)</div>

**What changed from Step 1?** We are connecting student $0$ and student $1$ for the first time.

**What are we doing?** We want to combine the set containing $0$ and the set containing $1$. In Naive Union:
1. Find the root of $0$: $\text{Find}(0) = 0$ (since `parent[0] == 0`).
2. Find the root of $1$: $\text{Find}(1) = 1$ (since `parent[1] == 1`).
3. Attach root $1$ under root $0$: set `parent[1] = 0`.

**Why are we doing this step?** To merge two disjoint components, we attach the root of one component to the root of the other so they share a common ancestor.

**How do we do it?** Update the array at index $1$:
$$\text{parent}[1] \leftarrow 0$$

**Where did this concept come from?** The core definition of Union in an up-tree: to join set $A$ and set $B$, make the root of set $B$ a direct child of the root of set $A$.

**Array State:**
| Index ($i$) | 0 | 1 | 2 | 3 |
| :--- | :---: | :---: | :---: | :---: |
| **`parent[i]`** | **0** | **0** | **2** | **3** |

*Tree Structure:*
```text
  0        (2)    (3)
  |
  1
```
Student $1$ points to $0$. Student $0$ still points to $0$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Perform Union(1, 2)</div>

**What changed from Step 2?** Student $1$ is now part of group $\{0, 1\}$. We now merge group of student $1$ with student $2$.

**What are we doing?** We run `Union(1, 2)`:
1. Find root of $1$:
   - Look at `parent[1]`, which is $0$.
   - Look at `parent[0]`, which is $0$.
   - Root is $0$.
2. Find root of $2$:
   - Look at `parent[2]`, which is $2$.
   - Root is $2$.
3. Since Root $0 \neq$ Root $2$, we attach Root $2$ under Root $1$ (or Root $0$). In standard naive implementations without rank/size checks, an implementation might attach Root $2$ under the node returned or its root. Let us attach Root $2$ as a child of node $1$ (creating a pure linked list chain) to see worst-case naive behavior:
   $$\text{parent}[2] = 1$$

**Why are we doing this?** Without balancing rules, arbitrary attachments make one node point directly to another without checking tree depth.

**How do we do it?** Update `parent[2]`:
$$\text{parent}[2] \leftarrow 1$$

**Array State:**
| Index ($i$) | 0 | 1 | 2 | 3 |
| :--- | :---: | :---: | :---: | :---: |
| **`parent[i]`** | **0** | **0** | **1** | **3** |

*Tree Structure:*
```text
    0       (3)
    |
    1
    |
    2
```
</div>

<div class="step-card">
<div class="step-badge">Step 4: Perform Union(2, 3)</div>

**What changed from Step 3?** We have a chain of length $3$ ($2 \to 1 \to 0$). We now bring student $3$ into the chain.

**What are we doing?** We attach student $3$ under student $2$:
$$\text{parent}[3] \leftarrow 2$$

**How do we do it?** Update index $3$ in `parent`:
$$\text{parent}[3] = 2$$

**Array State:**
| Index ($i$) | 0 | 1 | 2 | 3 |
| :--- | :---: | :---: | :---: | :---: |
| **`parent[i]`** | **0** | **0** | **1** | **2** |

*Tree Structure:*
```text
      0
      |
      1
      |
      2
      |
      3
```
</div>

<div class="step-card">
<div class="step-badge">Step 5: Trace Find(3) Step-by-Step</div>

**What changed from Step 4?** All $4$ elements are now in one set. We now run the query `Find(3)` to find the representative.

**What are we doing?** We follow the parent pointers starting at index $3$ until we reach an index $x$ where `parent[x] == x`.

**How do we do it?**
- **Hop 1:** Current node is $3$.  
  Check: Is `parent[3] == 3`?  
  $2 \neq 3 \implies$ No. Move to $2$.
- **Hop 2:** Current node is $2$.  
  Check: Is `parent[2] == 2`?  
  $1 \neq 2 \implies$ No. Move to $1$.
- **Hop 3:** Current node is $1$.  
  Check: Is `parent[1] == 1`?  
  $0 \neq 1 \implies$ No. Move to $0$.
- **Hop 4:** Current node is $0$.  
  Check: Is `parent[0] == 0`?  
  $0 == 0 \implies$ **Yes!** Stop. Return $0$.

**Where did this formula/concept come from?** The recursive or iterative definition of `Find`:
$$\text{Find}(x) = \begin{cases} x & \text{if } \text{parent}[x] == x \\ \text{Find}(\text{parent}[x]) & \text{otherwise} \end{cases}$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Conclusion & Complexity</div>

**What is the final answer?** `Find(3)` returns $0$.

**Why does this answer make sense?** All $4$ elements belong to the same component, whose root ancestor is $0$.

**Complexity Warning:** Notice that to find the root of element $3$, we had to take $3$ hops across $4$ nodes. For $N$ elements arranged in a single line, a single `Find` takes:
$$T(N) = O(N) \text{ operations (Linear Time)}$$
This is inefficient. If we do $M$ queries on a chain of length $N$, the total time is $O(M \times N)$, which is as slow as an unindexed search.
</div>

</div>

---

## Level 2: Union by Rank

### Problem 2.1: Preventing Tall Chains (Equal vs. Unequal Ranks)

We have $6$ items: $0, 1, 2, 3, 4, 5$.  
We maintain two arrays:
1. `parent[]`: Stores the immediate parent of each node.
2. `rank[]`: Stores an upper bound on the height of the subtree rooted at that node.

We will trace:
1. `MakeSet` for elements $0, 1, 2, 3$.
2. `Union(0, 1)` (Ties in rank).
3. `Union(2, 3)` (Ties in rank).
4. `Union(0, 2)` (Merging two trees of equal rank: what happens to the rank?).
5. `Union(0, 4)` (Merging an existing tree with a fresh single node: what happens to the rank?).

::: callout-intuition Core Mental Model
Think of **Rank** as the number of levels (floors) in a building.
- If a 1-story building merges with another 1-story building, you must put one building on top of the other. The resulting building now has **2 stories** (height increases by 1).
- But if a 10-story skyscraper merges with a small 1-story shed, you simply park the shed next to the skyscraper and run an elevator walkway from the shed roof directly into the skyscraper ground floor. The skyscraper **does not get taller**; its maximum height is still 10 stories!
- **Rule:** The shorter tree is always hung under the taller tree. The height only increases when both trees have the exact same height.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Initialize parent[] and rank[]</div>

**What are we doing?** We initialize arrays `parent` and `rank` for elements $0, 1, 2, 3, 4, 5$.

**Why are we starting here?** Every single-node tree has a height of $0$. Therefore, every node starts with `rank = 0`.

**How do we do it?** For each $i \in \{0, 1, 2, 3, 4, 5\}$:
- `parent[i] = i`
- `rank[i] = 0`

**Where did this formula come from?** By definition, the height of a tree with only $1$ node is $0$.

**State Table:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | 0 | 1 | 2 | 3 | 4 | 5 |
| **`rank[i]`** | **0** | **0** | **0** | **0** | **0** | **0** |
</div>

<div class="step-card">
<div class="step-badge">Step 2: Trace Union(0, 1) - Equal Rank Merge</div>

**What changed from Step 1?** We are joining elements $0$ and $1$. Both currently have `rank = 0`.

**What are we doing?** 1. Find roots:
   - $\text{root}_X = \text{Find}(0) = 0$
   - $\text{root}_Y = \text{Find}(1) = 1$
2. Compare ranks:
   - `rank[0]` $= 0$
   - `rank[1]` $= 0$
3. Tie-breaker rule:
   - When $\text{rank}[\text{root}_X] == \text{rank}[\text{root}_Y]$, choose one to be the parent (say, $\text{root}_X = 0$), make the other ($\text{root}_Y = 1$) its child, and **increment** the rank of the chosen root by $1$:
   $$\text{parent}[1] = 0$$
   $$\text{rank}[0] = \text{rank}[0] + 1 = 0 + 1 = 1$$

**Why does rank increment here?** Because both trees had height $0$. Hanging node $1$ under node $0$ creates a new level: node $0$ is at level $0$, node $1$ is at level $1$. The height is now $1$.

**State Table:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | **0** | **0** | 2 | 3 | 4 | 5 |
| **`rank[i]`** | **1** | **0** | 0 | 0 | 0 | 0 |

*Tree Structure for $\{0, 1\}$:*
```text
  0 (rank 1)
  |
  1 (rank 0)
```
</div>

<div class="step-card">
<div class="step-badge">Step 3: Trace Union(2, 3) - Equal Rank Merge</div>

**What changed from Step 2?** Now we merge $2$ and $3$, both of which are still untouched singletons with `rank = 0`.

**What are we doing?** 1. $\text{root}_X = \text{Find}(2) = 2$ (`rank[2] = 0`)
2. $\text{root}_Y = \text{Find}(3) = 3$ (`rank[3] = 0`)
3. Ranks are equal ($0 == 0$):
   - Make $2$ the parent of $3$: `parent[3] = 2`
   - Increment rank of root $2$: `rank[2] = 0 + 1 = 1`

**State Table:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | 0 | 0 | **2** | **2** | 4 | 5 |
| **`rank[i]`** | 1 | 0 | **1** | **0** | 0 | 0 |

*Tree Structures:*
```text
  0 (rank 1)        2 (rank 1)      (4) rank 0      (5) rank 0
  |                 |
  1 (rank 0)        3 (rank 0)
```
</div>

<div class="step-card">
<div class="step-badge">Step 4: Trace Union(0, 2) - Merging Two Trees of Rank 1</div>

**What changed from Step 3?** We now merge the tree rooted at $0$ (which contains $\{0, 1\}$) with the tree rooted at $2$ (which contains $\{2, 3\}$).

**What are we doing?** 1. Find roots:
   - $\text{root}_A = \text{Find}(0) = 0$
   - $\text{root}_B = \text{Find}(2) = 2$
2. Inspect ranks:
   - `rank[0]` $= 1$
   - `rank[2]` $= 1$
3. Ranks are equal ($1 == 1$):
   - Choose root $0$ to stay root.
   - Attach root $2$ under root $0$:
     $$\text{parent}[2] = 0$$
   - Increase `rank[0]` by $1$:
     $$\text{rank}[0] = 1 + 1 = 2$$
   - `rank[2]` stays $1$ (its subtree structure did not change internally).

**Why does rank become 2?** Root $2$ was already $1$ level deep (with node $3$ below it). When we put root $2$ underneath root $0$, the path from $0 \to 2 \to 3$ now has length $2$. The tree grew taller!

**State Table:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | **0** | 0 | **0** | 2 | 4 | 5 |
| **`rank[i]`** | **2** | 0 | **1** | 0 | 0 | 0 |

*Tree Structure:*
```text
        0  (rank 2)
       / \
      1   2  (rank 1)
          |
          3  (rank 0)
```
</div>

<div class="step-card">
<div class="step-badge">Step 5: Trace Union(0, 4) - Unequal Rank Merge</div>

**What changed from Step 4?** We now merge the large tree (rooted at $0$, rank $2$) with a single node $4$ (rooted at $4$, rank $0$).

**What are we doing?** 1. Find roots:
   - $\text{root}_A = \text{Find}(0) = 0$
   - $\text{root}_B = \text{Find}(4) = 4$
2. Compare ranks:
   - `rank[0]` $= 2$
   - `rank[4]` $= 0$
3. Since $\text{rank}[0] > \text{rank}[4]$:
   - The shorter tree (node $4$) is attached directly under the taller root (node $0$):
     $$\text{parent}[4] = 0$$
   - **Crucial Rule:** `rank[0]` DOES NOT CHANGE! It stays $2$.

**Why does the rank NOT change?** Node $4$ is placed directly under node $0$ at depth $1$. But node $0$ already has a deeper branch going down to node $3$ at depth $2$. The maximum depth of the tree is still $2$. Hanging a shorter stick next to a longer stick does not make the overall structure any longer!

**State Table:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | 0 | 0 | 0 | 2 | **0** | 5 |
| **`rank[i]`** | **2** | 0 | 1 | 0 | **0** | 0 |

*Tree Structure:*
```text
          0  (rank 2)
        / | \
       1  4  2  (rank 1)
             |
             3  (rank 0)
```
</div>

<div class="step-card">
<div class="step-badge">Final Step: Mathematical Guarantee of Union by Rank</div>

**What is the final state?** The set $\{0, 1, 2, 3, 4\}$ has root $0$ with rank $2$.

**Why is Union by Rank guaranteed to be fast?** A tree of rank $k$ can only be formed by merging two trees of rank $k-1$.  
Let $N(k)$ be the minimum number of nodes required to produce a root of rank $k$:
$$N(0) = 1$$
$$N(k) = 2 \times N(k-1) = 2^k$$
To have a tree of rank $k$, you need at least $2^k$ nodes:
$$N \ge 2^k \implies k \le \log_2(N)$$
Because the height of the tree is bounded by $\log_2(N)$, the longest path any `Find` operation can ever traverse is:
$$O(\log N)$$
Without rank balancing, height could become $O(N)$. Union by rank reduces maximum depth from linear to logarithmic.
</div>

</div>

---

## Level 3: Path Compression

### Problem 3.1: Flattening a Deep Tree During Find

Suppose prior operations without path compression produced the following linear chain of $5$ nodes:
$$4 \to 3 \to 2 \to 1 \to 0$$
Where node $0$ is the root (`parent[0] = 0`).

We call:
$$\text{Find}(4)$$
using the standard **two-pass recursive path compression algorithm**:
```python
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Unwinding step assigns root directly!
    return parent[x]
```

We will trace:
1. Every downward recursive call (seeking the root).
2. The base case encounter at node $0$.
3. Every upward unwinding step, showing the pointer update to `parent[]` for every node.
4. The final flattened tree structure.

::: callout-intuition Core Mental Model
Imagine a game of telephone in an office hierarchy:
- Employee $4$ asks their manager $3$, who asks Director $2$, who asks VP $1$, who asks CEO $0$: *"Who is our ultimate boss?"*
- CEO $0$ replies: *"I am!"*
- As the message travels back down the hallway, every person on the chain has a lightbulb moment:
  - VP $1$ says: *"Great, I will report directly to CEO 0 from now on."*
  - Director $2$ says: *"Why was I reporting to VP 1? I'm going to report directly to CEO 0!"*
  - Manager $3$ says: *"I'm also skipping the middle managers and reporting directly to CEO 0!"*
  - Employee $4$ says: *"Me too! Direct line to CEO 0!"*
- Next time *anyone* asks who the boss is, they don't walk down a long hallway. They look at CEO $0$ directly in $1$ step!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Initial State Before Find(4)</div>

**What are we doing?** Inspecting our array before any search begins.

**How do we do it?** Write down the array indices and their parent values:
- Node $4$ points to $3$: `parent[4] = 3`
- Node $3$ points to $2$: `parent[3] = 2`
- Node $2$ points to $1$: `parent[2] = 1`
- Node $1$ points to $0$: `parent[1] = 0`
- Node $0$ points to $0$: `parent[0] = 0` (Root)

**Initial Array Table:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | **0** | **0** | **1** | **2** | **3** |

*Tree Structure:*
$$4 \longrightarrow 3 \longrightarrow 2 \longrightarrow 1 \longrightarrow 0$$
Total tree depth to reach node $4$ is $4$ edges.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Recursive Forward Call Stack (Drilling Down)</div>

**What changed from Step 1?** The program executes `Find(4)`. We dive deeper into recursion until we hit the root.

**What are we doing?** Tracing the call stack frame by frame.

**How do we do it?**
- **Call 1:** `Find(4)`  
  Check: `parent[4] == 4`? $\implies 3 == 4$ is **False**.  
  Must evaluate: `parent[4] = Find(parent[4])` $\implies$ calls `Find(3)`. *(Call 1 pauses)*

- **Call 2:** `Find(3)`  
  Check: `parent[3] == 3`? $\implies 2 == 3$ is **False**.  
  Must evaluate: `parent[3] = Find(parent[3])` $\implies$ calls `Find(2)`. *(Call 2 pauses)*

- **Call 3:** `Find(2)`  
  Check: `parent[2] == 2`? $\implies 1 == 2$ is **False**.  
  Must evaluate: `parent[2] = Find(parent[2])` $\implies$ calls `Find(1)`. *(Call 3 pauses)*

- **Call 4:** `Find(1)`  
  Check: `parent[1] == 1`? $\implies 0 == 1$ is **False**.  
  Must evaluate: `parent[1] = Find(parent[1])` $\implies$ calls `Find(0)`. *(Call 4 pauses)*

- **Call 5:** `Find(0)`  
  Check: `parent[0] == 0`? $\implies 0 == 0$ is **True!** **Base Case Reached!** This call immediately returns $0$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Unwinding Call 4 for Node 1</div>

**What changed from Step 2?** `Find(0)` returned $0$ back to paused Call 4 (`Find(1)`).

**What are we doing?** Executing line `parent[1] = result_of_find(0)` in the code of `Find(1)`.

**How do we do it?**
- Result received from child call $= 0$.
- Pointer assignment:
  $$\text{parent}[1] = 0$$
- Value returned to previous caller: return $0$.

**Did `parent[1]` change?** It was already $0$, so it remains $0$.

**Array State:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | 0 | **0** | 1 | 2 | 3 |
</div>

<div class="step-card">
<div class="step-badge">Step 4: Unwinding Call 3 for Node 2</div>

**What changed from Step 3?** `Find(1)` finished and returned value $0$ back to paused Call 3 (`Find(2)`).

**What are we doing?** Executing line `parent[2] = result_of_find(1)` in `Find(2)`.

**How do we do it?**
- Result received $= 0$.
- Pointer assignment:
  $$\text{parent}[2] = 0$$
- Value returned to previous caller: return $0$.

**What changed in the array?** `parent[2]` was previously $1$. It is now reassigned directly to $0$! Node $2$ has bypassed node $1$.

**Array State:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | 0 | 0 | **0** | 2 | 3 |
</div>

<div class="step-card">
<div class="step-badge">Step 5: Unwinding Call 2 for Node 3</div>

**What changed from Step 4?** `Find(2)` finished and returned value $0$ back to paused Call 2 (`Find(3)`).

**What are we doing?** Executing line `parent[3] = result_of_find(2)` in `Find(3)`.

**How do we do it?**
- Result received $= 0$.
- Pointer assignment:
  $$\text{parent}[3] = 0$$
- Value returned to previous caller: return $0$.

**What changed in the array?** `parent[3]` was previously $2$. It is now directly connected to $0$!

**Array State:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | 0 | 0 | 0 | **0** | 3 |
</div>

<div class="step-card">
<div class="step-badge">Step 6: Unwinding Call 1 for Node 4</div>

**What changed from Step 5?** `Find(3)` finished and returned value $0$ back to the original top-level call `Find(4)`.

**What are we doing?** Executing line `parent[4] = result_of_find(3)` in `Find(4)`.

**How do we do it?**
- Result received $= 0$.
- Pointer assignment:
  $$\text{parent}[4] = 0$$
- Final return value to user: return $0$.

**What changed in the array?** `parent[4]` was previously $3$. It is now directly connected to $0$!

**Final Array State:**
| Index ($i$) | 0 | 1 | 2 | 3 | 4 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`parent[i]`** | **0** | **0** | **0** | **0** | **0** |

*Tree Structure:*
```text
           0
       / /   \ \
      1 2     3 4
```
Every single node now points directly to root $0$!
</div>

<div class="step-card">
<div class="step-badge">Final Step: Time Complexity with Both Optimizations</div>

**What is the final answer?** `Find(4)` returned $0$, and every node along the path $\{4, 3, 2, 1\}$ was compressed into a direct child of root $0$.

**Why does this matter for future queries?** If we call `Find(4)` again right now:
- Look at `parent[4]`: it is $0$.
- Look at `parent[0]`: it is $0$.
- Done in **$1$ step** ($O(1)$ time)!

**The Ultimate Complexity Theorem (Tarjan, 1975):** When both **Union by Rank** and **Path Compression** are combined, any sequence of $M$ operations on $N$ elements takes:
$$O(M \cdot \alpha(N))$$
Where $\alpha(N)$ is the **Inverse Ackermann Function**.

**How small is $\alpha(N)$?** The Ackermann function grows so fast that for any input size $N$ conceivable in our physical universe (e.g., $N = 10^{80}$, the estimated number of atoms in the observable universe):
$$\alpha(N) \le 4$$
For all practical computer programs, $\alpha(N)$ is a constant $\le 4$. This means Disjoint Set Union operations run in **amortized nearly constant time, $O(1)$ per operation**.
</div>

</div>
