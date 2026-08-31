# Disjoint Set Data Structure (Union-Find)

**Set representation, MakeSet, Find, and naive Union operations.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
Imagine you're organising a huge group of people into friend circles, where you only get told, one pair at a time, "these two people are friends." Two questions you'll constantly need to answer: "are person A and person B in the same friend circle (even if not directly friends, but connected through a chain of mutual friends)?" and "please merge these two friend circles into one, because we just learned two people from different circles are actually friends."

A **disjoint set** (also called **union-find**) data structure is built exactly for this: it maintains a collection of non-overlapping ("disjoint") groups, and supports two core operations — **Find** (which group does this element currently belong to?) and **Union** (merge two groups into one). The clever trick used to represent a group is a **tree**: every group is represented as a tree of elements, where each element points to its **parent**, and the very top element (whose parent is itself) is called the **representative** of the whole group. Two elements are in the same group exactly when following the chain of parent-pointers from each of them leads to the *same* representative at the top.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Representation.** Each element is stored in an array (or similar structure) `parent[]`, where `parent[x]` points to `x`'s parent in its group's tree. An element that is its own parent (`parent[x] == x`) is the **representative** (root) of its group.

**MakeSet(x):** initialise a brand-new, singleton group containing only `x`. Set `parent[x] = x` — `x` is its own representative, since it's alone in its own group. This is $O(1)$.

**Find(x):** determine which group `x` belongs to, by returning its group's representative. Mechanically: follow parent-pointers starting at `x` — `x → parent[x] → parent[parent[x]] → ...` — until reaching an element that is its own parent (the root/representative). Return that root.
$$\text{Find}(x) = x \text{ if } parent[x]=x, \quad \text{else Find}(parent[x])$$

**Union(x, y) — the naive version:** first, find the representatives of both `x`'s group and `y`'s group: `rootX = Find(x)`, `rootY = Find(y)`. If they're already equal, `x` and `y` are already in the same group — nothing to do. Otherwise, merge the two groups by making one root point to the other: e.g. `parent[rootX] = rootY` — now every element that used to trace up to `rootX` will, after one more hop, trace up to `rootY` instead, unifying the two trees into one.

**Why "naive" union can be slow.** The naive version always attaches one root arbitrarily under the other, with no regard for which tree is bigger or taller. If you're unlucky (or an adversary deliberately chooses a bad sequence of unions), you can end up always attaching the bigger tree under the smaller one, repeatedly — producing a long, skinny chain (exactly the "degenerate BST" problem from the AVL topics, appearing again in a different data structure!). In the worst case, `Find` on such a skewed structure costs $O(n)$ — you might have to walk all the way up a chain of $n$ elements to find the root. This motivates the next topic's two optimisations (union by rank, path compression), which together bring the amortized cost per operation down to *almost* constant time.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Start with 5 singleton elements $\{1,2,3,4,5\}$, each its own group (via MakeSet). Perform the operations, in order: `Union(1,2)`, `Union(3,4)`, `Union(1,3)`. After all three, answer: are elements $2$ and $4$ in the same group?
:::

::: step [Step 2: Execution] Applying Core Algorithm
Initially: `parent[1]=1, parent[2]=2, parent[3]=3, parent[4]=4, parent[5]=5`.
`Union(1,2)`: `Find(1)=1`, `Find(2)=2`; set `parent[1]=2` (attaching root 1 under root 2, using naive attachment). Now group $\{1,2\}$ has representative $2$.
`Union(3,4)`: `Find(3)=3`, `Find(4)=4`; set `parent[3]=4`. Now group $\{3,4\}$ has representative $4$.
`Union(1,3)`: `Find(1)$: `1 → parent[1]=2 → parent[2]=2` (root), so `Find(1)=2`. `Find(3)`: `3 → parent[3]=4 → parent[4]=4` (root), so `Find(3)=4`. Since these roots (2 and 4) differ, merge: set `parent[2]=4` (attaching root 2 under root 4).
:::

::: step [Step 3: Conclusion] Final Result
Now trace `Find(2)`: `2 → parent[2]=4` (root), so `Find(2)=4`. Trace `Find(4)`: `4` is its own parent, so `Find(4)=4`. Both return the same representative, $4$ — so **yes, elements 2 and 4 are now in the same group**, even though no `Union` call ever directly mentioned both 2 and 4 together — the chain of unions (1 with 2, 3 with 4, then 1 with 3) transitively connected them, exactly the kind of "connected through a chain of mutual friends" reasoning described in the intuition above.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
In a disjoint-set data structure, how do you determine whether two elements $x$ and $y$ belong to the same group?
(A) Check if `parent[x] == y`
(*B) Compute `Find(x)` and `Find(y)` (following parent pointers to each element's root/representative) and check if the two results are equal
(C) Check if $x$ and $y$ have consecutive array indices
(D) Elements are never grouped; only individual comparisons are supported
::: explanation
Two elements are in the same group exactly when their respective chains of parent-pointers lead to the same root/representative element. `Find` is defined precisely to compute this representative, so comparing `Find(x) == Find(y)` is the standard way to test group membership.
:::

::: quiz Q2: Foundational Concept
What can go wrong with the "naive" Union operation, where one root is arbitrarily attached under the other with no size/height consideration?
(A) Nothing — naive union is always optimal
(*B) Repeatedly attaching in an unlucky order can build a long, skewed chain, making `Find` cost up to $O(n)$ in the worst case
(C) Naive union always produces a perfectly balanced tree automatically
(D) Naive union cannot merge more than two groups total
::: explanation
Because naive union doesn't track which tree is taller or has more elements, an adversarial or unlucky sequence of unions can always attach the larger/taller tree beneath the smaller one, producing a long chain — mirroring the same "skewed tree" problem seen with unbalanced BSTs, and making `Find` degrade to linear time in the worst case.
:::

::: quiz Q3: Foundational Concept
What is the time complexity of `MakeSet(x)`?
(A) $O(n)$
(*B) $O(1)$
(C) $O(\log n)$
(D) $O(n^2)$
::: explanation
`MakeSet` simply initialises a brand-new singleton group by setting `parent[x] = x` — a single constant-time assignment, regardless of how many other elements or groups already exist.
:::
