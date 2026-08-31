# Optimized Union by Rank & Path Compression

**Rank heuristics, tree flattening during Find, and Inverse Ackermann complexity.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
The previous topic ended on a problem: naive union-find can degrade into a long, skinny chain, making `Find` slow. Two independent, complementary fixes solve this — and the fact that they were invented separately but combine so powerfully is one of the nicer stories in algorithm design.

**Union by rank** is a *preventive* fix: instead of arbitrarily attaching one tree under the other during Union, always attach the *shorter* tree under the *taller* one's root (like always adding the smaller stack of boxes on top of the bigger, sturdier stack, rather than the other way round) — this alone caps how tall the tree can ever get.

**Path compression** is a *corrective, self-healing* fix: every time you do a `Find(x)` and walk up a possibly-long chain to reach the root, you take the opportunity — while you're already there, having done the walk — to reattach every element you passed through *directly* to the root, flattening the path for next time. It's like, after walking up a long, winding staircase once to check something, installing an elevator direct to the top before you leave, so that everyone who follows takes the direct route from now on.

Individually, each trick already helps a lot. Combined, something remarkable happens: the *amortized* cost per operation becomes so close to constant that it's described using one of the slowest-growing functions in all of mathematics — the inverse Ackermann function.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Union by rank.** Maintain a `rank[x]` value for each representative — an upper bound on the height of the tree rooted at `x` (not tracked exactly for non-roots, but bounded correctly at roots, which is all that matters). During `Union(x, y)`:
- Find both roots, `rootX` and `rootY`.
- If `rank[rootX] < rank[rootY]`, attach `rootX` under `rootY` (`parent[rootX] = rootY`).
- If `rank[rootX] > rank[rootY]`, attach `rootY` under `rootX`.
- If ranks are equal, attach either under the other arbitrarily, and **increment** the resulting root's rank by 1 (this is the *only* situation where a tree's height can actually increase).

This guarantees a tree's height only grows when merging two trees of *equal* rank — which, by an inductive argument, means a tree of rank $r$ must contain at least $2^r$ elements, so the height of any tree is bounded by $O(\log n)$ — matching the same logarithmic guarantee AVL trees achieve, but through an entirely different mechanism.

**Path compression.** During `Find(x)`, after locating the root by walking up the parent chain, make a *second* pass, resetting every node visited along the way to point *directly* to the root, instead of to its immediate former parent:
$$\text{Find}(x): \text{if } parent[x] \ne x: \ parent[x] \leftarrow \text{Find}(parent[x]); \ \text{return } parent[x]$$
(This recursive formulation naturally implements path compression: the recursive call finds the true root, and the assignment `parent[x] = Find(parent[x])` rewires `x` to point directly at that root on the way back out of the recursion.) Path compression doesn't just help the current call — it permanently shortens the path for *every future* `Find` call on any node that was on this path.

**Combined complexity — the inverse Ackermann function.** When union by rank and path compression are used *together*, the amortized time per operation (across a sequence of $m$ Union/Find operations on $n$ elements) is:
$$O(\alpha(n))$$
where $\alpha(n)$ is the **inverse Ackermann function** — the functional inverse of the notoriously fast-growing Ackermann function. $\alpha(n)$ grows so slowly that for *any* input size conceivable in the real world (up to numbers vastly larger than the number of atoms in the observable universe), $\alpha(n) \le 4$. In every practical sense, this makes each operation *effectively* constant time, even though it's not, technically, a fixed constant in the strict mathematical sense.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Suppose (before any optimisation) a chain exists: `parent[1]=2, parent[2]=3, parent[3]=4, parent[4]=4` (so 4 is the root, and 1→2→3→4 is a chain of length 3). Call `Find(1)` with path compression enabled, and describe the structure afterward.
:::

::: step [Step 2: Execution] Applying Core Algorithm
`Find(1)` walks: `1 → 2 → 3 → 4` (root, since `parent[4]=4`). Using the recursive path-compression formulation, as the recursion unwinds back down from the root: node 3's parent is reset directly to 4 (already true, no change); node 2's parent is reset directly to 4 (was 3, now 4); node 1's parent is reset directly to 4 (was 2, now 4).
:::

::: step [Step 3: Conclusion] Final Result
After this single `Find(1)` call, the structure becomes: `parent[1]=4, parent[2]=4, parent[3]=4, parent[4]=4` — every element on the original chain now points *directly* to the root. Any future `Find` call on 1, 2, or 3 will now take just one step, instead of retracing the original 3-step chain. This is exactly the "install an elevator after the first long climb" behaviour described in the intuition — the tree gets flatter every time it's touched, which is precisely why the amortized cost across many operations stays so low.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
Under union by rank, when does a tree's height actually increase during a Union operation?
(A) Every single time two trees are merged
(*B) Only when the two trees being merged have equal rank
(C) Only when the smaller tree is attached under the larger
(D) Height never increases under union by rank
::: explanation
Union by rank always attaches the lower-rank (shorter) tree beneath the higher-rank (taller) one's root, which never increases the taller tree's height. Height only increases in the tie-breaking case, when both trees have equal rank — attaching one under the other in that case does add one level, so the rank (and height bound) is incremented by exactly 1.
:::

::: quiz Q2: Foundational Concept
What does path compression do during a `Find` operation?
(A) It deletes all but the last element on the path
(*B) After locating the root, it reattaches every node visited along the way to point directly at the root, flattening the tree for future operations
(C) It merges the tree with a completely unrelated tree
(D) It reverses the direction of the parent pointers only, without changing which node they point to
::: explanation
Path compression is a "while I'm here anyway" optimisation: having walked the full path to find the root, it rewires every visited node's parent pointer to point straight at that root, so any future `Find` call on those same nodes takes a direct, one-hop path instead of retracing the original chain.
:::

::: quiz Q3: Foundational Concept
When union by rank and path compression are used together, the amortized time per operation is described by which function?
(A) $O(\log n)$
(B) $O(n)$
(*C) $O(\alpha(n))$, the inverse Ackermann function, which is effectively constant for any realistic input size
(D) $O(n \log n)$
::: explanation
The combination of these two optimisations yields the famous $O(\alpha(n))$ amortized bound, where $\alpha(n)$ (inverse Ackermann) grows so slowly that it never exceeds 4 for any input size that could realistically occur, making the practical behaviour essentially constant time per operation.
:::
