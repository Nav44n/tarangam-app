# Progressive Problems: AVL Tree Rotations & Insertions

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior experience with balanced search trees beyond basic binary search tree ordering ($L < \text{Root} < R$).

---

## The AVL Blueprint: Core Definitions & Ground Rules

Before solving problems, we establish the exact rules and mathematical formulas used by AVL trees.

### 1. Height Definition
To eliminate any ambiguity, we define the height of a node as the number of nodes along the longest downward path to a leaf:
* An **empty subtree (null)** has height:
  $$\text{height}(\text{null}) = 0$$
* A **leaf node** (a node with two null children) has height:
  $$\text{height}(\text{leaf}) = 1 + \max(0, 0) = 1$$
* Any **internal node** $X$ with left child $L$ and right child $R$ has height:
  $$\text{height}(X) = 1 + \max(\text{height}(L), \text{height}(R))$$

### 2. Balance Factor ($BF$) Formula
For every node $X$, the balance factor is defined as the height of its left subtree minus the height of its right subtree:

$$BF(X) = \text{height}(X.\text{left}) - \text{height}(X.\text{right})$$

* **Balanced:** $BF(X) \in \{-1, 0, +1\}$ (the subtrees differ in height by at most 1).
* **Critically Unbalanced:** $|BF(X)| \ge 2$:
  * $BF(X) = +2 \implies$ The node is **Left-Heavy** (leaning to the left).
  * $BF(X) = -2 \implies$ The node is **Right-Heavy** (leaning to the right).

### 3. The 4 Imbalance Signatures
When a new key is inserted, we travel back up the path toward the root and find the **lowest ancestor node** with $|BF| = 2$. Call this node $Z$. We inspect the path taken by the newly inserted key relative to $Z$:
1. **LL (Left-Left):** Key was inserted into the **L**eft subtree of $Z$'s **L**eft child $\implies$ Fixed by **1 Right Rotation**.
2. **RR (Right-Right):** Key was inserted into the **R**ight subtree of $Z$'s **R**ight child $\implies$ Fixed by **1 Left Rotation**.
3. **LR (Left-Right):** Key was inserted into the **R**ight subtree of $Z$'s **L**eft child $\implies$ Fixed by **Double Rotation: Left then Right**.
4. **RL (Right-Left):** Key was inserted into the **L**eft subtree of $Z$'s **R**ight child $\implies$ Fixed by **Double Rotation: Right then Left**.

---

## Level 1: Left-Left (LL) Imbalance & Single Right Rotation

In this level, three keys are added in strictly descending order, causing the tree to tilt into a straight leftward line. We fix this by pulling the tree clockwise (Right Rotation).

---

### Problem 1.1: The Minimal LL Imbalance (Insert 30, then 20, then 10)

**Problem Statement:** Starting with an empty AVL tree, insert the keys $30$, $20$, and $10$ in that order. Show the imbalance that occurs, calculate the balance factor of every node, perform the required rotation, and verify that the BST ordering is preserved.

::: callout-intuition Core Mental Model
Imagine three people standing on the left side of a playground see-saw: a heavy grandfather ($30$), a parent ($20$), and a child ($10$). The see-saw slams into the ground on the left side because there is no counterweight on the right. To balance the see-saw without rearranging who is older or younger, you place the middle person ($20$) right on the central pivot, let the grandfather ($30$) slide down to the right, and let the child ($10$) stay on the left.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Perform standard BST insertion of 30, 20, and 10</summary>
**What are we doing?** We place the three numbers into the tree using standard binary search tree rules ($L < \text{Root} < R$).  
**Why are we starting here?** An AVL tree is first and foremost a binary search tree. Every rotation happens *after* a BST insertion introduces an imbalance.  
**How do we do it?** * Insert $30$: It becomes the root node.
* Insert $20$: Since $20 < 30$, $20$ becomes the left child of $30$.
* Insert $10$: Compare with root $30$ ($10 < 30 \to$ go left to $20$). Compare with $20$ ($10 < 20 \to$ go left). $10$ becomes the left child of $20$.

The tree before rotation looks like this:

```
        [30]
        /
      [20]
      /
    [10]
```
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Calculate heights and Balance Factors ($BF$) from bottom to top</summary>
**What are we doing?** We calculate the height and balance factor of every node along the insertion path, starting from the leaf and working upwards.  
**Why are we starting here?** Imbalances can only occur along the ancestor path of the newly inserted leaf. Working bottom-up identifies the first node that violates the AVL property.  
**How do we do it?**
* **For Node 10 (Leaf):**
  * $\text{height}(\text{left}) = 0$ (null)
  * $\text{height}(\text{right}) = 0$ (null)
  * $\text{height}(10) = 1 + \max(0, 0) = 1$
  * $BF(10) = 0 - 0 = 0 \implies \text{Balanced}$

* **For Node 20:**
  * $\text{height}(\text{left}) = \text{height}(10) = 1$
  * $\text{height}(\text{right}) = 0$ (null)
  * $\text{height}(20) = 1 + \max(1, 0) = 2$
  * $BF(20) = \text{height}(\text{left}) - \text{height}(\text{right}) = 1 - 0 = +1 \implies \text{Balanced}$

* **For Node 30 (Root):**
  * $\text{height}(\text{left}) = \text{height}(20) = 2$
  * $\text{height}(\text{right}) = 0$ (null)
  * $\text{height}(30) = 1 + \max(2, 0) = 3$
  * $BF(30) = \text{height}(\text{left}) - \text{height}(\text{right}) = 2 - 0 = +2 \implies \textbf{CRITICAL IMBALANCE!}$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Diagnose the Imbalance Case (LL vs. LR)</summary>
**What changed from Step 2?** Node $30$ has $BF = +2$. We must classify the exact nature of the tilt.  
**How do we do it?**
Look at the path from the unbalanced node ($30$) toward the newly inserted leaf ($10$):
* From $30$, we go **Left** to child $20$.
* From $20$, the newly inserted key $10$ was placed in its **Left** subtree ($BF(20) = +1$).
* Two consecutive Left moves $\implies$ **LL Imbalance**.
* **Prescribed Cure:** A single **Right Rotation** centered at Node $30$.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Execute the Right Rotation mechanically (Clockwise Twist)</summary>
**What are we doing?** We rearrange the pointers between node $30$ and node $20$ without losing any data.  
**How do we do it?**
1. Let $Z = 30$ (the unbalanced node).
2. Let $Y = 20$ (the left child of $Z$).
3. In a Right Rotation:
   * $Y$ ($20$) rises up to take $Z$'s spot as the new root of this subtree.
   * $Z$ ($30$) is pulled down and to the right, becoming the **right child** of $Y$.
   * Node $10$ remains untouched as the left child of $Y$.

The tree transforms into:

```
        [20]
       /    \
    [10]    [30]
```
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Verify the Binary Search Tree (BST) property</summary>
**What changed from Step 4?** We must prove that no keys were scrambled or misplaced during the rotation.  
**Where did this rule come from?** The fundamental invariant of a BST: for every node $X$, $\text{all left descendants} < X < \text{all right descendants}$.  
**How do we verify?**
* Check left subtree of $20$: Contains $\{10\}$. Since $10 < 20$, the left property holds.
* Check right subtree of $20$: Contains $\{30\}$. Since $30 > 20$, the right property holds.
* The BST invariant is 100% preserved.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Recalculate heights and state final answer</summary>
**What is the final answer?**
* $\text{height}(10) = 1 \implies BF(10) = 1 - 1 = 0$
* $\text{height}(30) = 1 \implies BF(30) = 1 - 1 = 0$
* $\text{height}(20) = 1 + \max(1, 1) = 2 \implies BF(20) = 1 - 1 = 0$

**Why does this answer make sense?**
All three nodes now have balance factor $0$. The tree height dropped from $3$ down to $2$. The tree is perfectly symmetrical and completely balanced.
</details>

</div>

---

### Problem 1.2: LL Rotation with Subtree Reattachment (The "Adopted" Subtree)

**Problem Statement:** In an existing AVL tree, node $50$ has left child $30$ and right child $70$. Node $30$ has left child $20$ and right child $40$. A new key $10$ is inserted as the left child of $20$. Show why node $40$ must change parents during the right rotation at $50$.

::: callout-intuition Core Mental Model
Think of node $40$ as a piece of luggage caught between two people. Node $40$ is larger than $30$ (so it must stay to the right of $30$), but smaller than $50$ (so it must stay to the left of $50$). When $30$ moves up to become the boss and $50$ moves down to become its right hand, $50$'s old left hand becomes vacant. Node $40$ is handed over to $50$ as its new left child!
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Draw the initial tree and locate the imbalance</summary>
**What are we doing?** We draw the tree after inserting $10$ and calculate the balance factor of $50$.  
**How do we do it?**

```
            [50] (BF: +2)
           /    \
        [30]    [70]
       /    \
    [20]    [40]
    /
  [10]
```

Heights and balance factors:
* Leaf $10$: height $= 1$, $BF = 0$
* Node $20$: left height $= 1$, right height $= 0 \implies BF = +1$, height $= 2$
* Node $40$: height $= 1$, $BF = 0$
* Node $30$: left height $= 2$, right height $= 1 \implies BF = 2 - 1 = +1$, height $= 3$
* Node $70$: height $= 1$, $BF = 0$
* Node $50$ (Root): left height $= 3$, right height $= 1 \implies BF = 3 - 1 = +2 \implies \textbf{Unbalanced!}$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Identify the conflict with subtree $T_2$ (Node 40)</summary>
**What changed from Step 1?** In a right rotation, node $30$ will take node $50$'s place, and node $50$ will become the **right child** of $30$.  
**Why is there a conflict?** Node $30$ *already* has a right child: node $40$! A binary tree node can only have ONE right child.  
**Where does node 40 go?** Look at the value of $40$:
* $40 > 30$ (it belongs to the right of $30$)
* $40 < 50$ (it belongs to the left of $50$)

Since node $50$ is moving down to the right of $30$, node $50$'s old left pointer is now completely empty! Therefore, node $50$ adopts node $40$ as its new **left child**.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Execute the Right Rotation with the Handover</summary>
**What are we doing?** We update the three pointers:
1. $30$'s right child becomes $50$.
2. $50$'s left child becomes $40$ (the transferred subtree).
3. $30$'s left child remains $20$ (and $20$'s left child remains $10$).

```
            [30]
           /    \
        [20]    [50]
        /       /  \
     [10]    [40]  [70]
```
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Verify BST Invariant and Heights</summary>
**What is the final answer?**
* In-order traversal before rotation: $10, 20, 30, 40, 50, 70$ (strictly sorted).
* In-order traversal after rotation: $10, 20, 30, 40, 50, 70$ (strictly sorted).
* Balance factors:
  * Node $10$: $BF = 0$, height $= 1$
  * Node $40$: $BF = 0$, height $= 1$
  * Node $70$: $BF = 0$, height $= 1$
  * Node $20$: $BF = +1$, height $= 2$
  * Node $50$: left height $= 1$, right height $= 1 \implies BF = 0$, height $= 2$
  * Root $30$: left height $= 2$, right height $= 2 \implies BF = 0$, height $= 3$

**Why does this answer make sense?**
The tree is completely balanced ($|BF| \le 1$ everywhere). The transferred subtree $40$ found its natural home as $50$'s left child, preserving the sorted order.
</details>

</div>

---

## Level 2: Right-Right (RR) Imbalance & Single Left Rotation

In this level, three keys are added in strictly ascending order, causing the tree to tilt into a straight rightward line. We fix this by pulling the tree counter-clockwise (Left Rotation).

---

### Problem 2.1: The Minimal RR Imbalance (Insert 10, then 20, then 30)

**Problem Statement:** Starting with an empty AVL tree, insert the keys $10$, $20$, and $30$ in that order. Show the resulting imbalance, calculate all balance factors, perform the required rotation, and verify the result.

::: callout-intuition Core Mental Model
This is the mirror opposite of Problem 1.1. Imagine three people standing on the right side of the see-saw: $10$ at the pivot, $20$ in the middle, and $30$ on the outer edge. The right side crashes down. We perform a counter-clockwise Left Rotation: $20$ rises to the top, $10$ swings down to the left, and $30$ stays on the right.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Perform standard BST insertion of 10, 20, and 30</summary>
**What are we doing?** We insert the keys sequentially using BST rules.  
**How do we do it?** * Insert $10$: Root node.
* Insert $20$: $20 > 10 \implies$ right child of $10$.
* Insert $30$: $30 > 10 \implies$ go right to $20$; $30 > 20 \implies$ right child of $20$.

```
    [10]
       \
       [20]
          \
          [30]
```
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Calculate heights and Balance Factors ($BF$)</summary>
**What are we doing?** We calculate heights and balance factors from the bottom leaf up to the root.  
**How do we do it?**
* **Node 30 (Leaf):**
  * $\text{height}(30) = 1$
  * $BF(30) = 0 - 0 = 0 \implies \text{Balanced}$
* **Node 20:**
  * $\text{height}(\text{left}) = 0$
  * $\text{height}(\text{right}) = 1$
  * $\text{height}(20) = 1 + \max(0, 1) = 2$
  * $BF(20) = 0 - 1 = -1 \implies \text{Balanced}$
* **Node 10 (Root):**
  * $\text{height}(\text{left}) = 0$
  * $\text{height}(\text{right}) = 2$
  * $\text{height}(10) = 1 + \max(0, 2) = 3$
  * $BF(10) = 0 - 2 = -2 \implies \textbf{CRITICAL IMBALANCE!}$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Diagnose the Imbalance Case</summary>
**What changed from Step 2?** The root node $10$ has $BF = -2$ (critically right-heavy).  
**How do we do it?**
Inspect the path from unbalanced node $10$ down to leaf $30$:
* Step 1: Go **Right** from $10$ to $20$.
* Step 2: Key $30$ was placed in the **Right** subtree of $20$ ($BF(20) = -1$).
* Two consecutive Right moves $\implies$ **RR Imbalance**.
* **Prescribed Cure:** A single **Left Rotation** centered at Node $10$.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Execute the Left Rotation mechanically (Counter-Clockwise Twist)</summary>
**What are we doing?** We elevate the right child $20$ and pull the root $10$ down to the left.  
**How do we do it?**
1. Let $Z = 10$ (unbalanced node).
2. Let $Y = 20$ (right child of $Z$).
3. In a Left Rotation:
   * $Y$ ($20$) becomes the new root of this subtree.
   * $Z$ ($10$) becomes the **left child** of $Y$.
   * Node $30$ remains the right child of $Y$.

```
        [20]
       /    \
    [10]    [30]
```
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Verify Heights, Balance Factors, and BST Invariant</summary>
**What is the final answer?**
* Node $10$: height $= 1$, $BF = 0$
* Node $30$: height $= 1$, $BF = 0$
* Root $20$: height $= 2$, $BF = 1 - 1 = 0$
* BST check: $10 < 20 < 30$ holds strictly.

**Why does this answer make sense?**
A single counter-clockwise rotation leveled the right-leaning chain into a balanced binary tree of height 2 with zero balance factor on every node.
</details>

</div>

---

## Level 3: Double Rotations (Zig-Zag Imbalances: LR and RL)

In this level, the newly inserted key forms a "kink" or "elbow" shape (a zig-zag). A single rotation cannot fix a zig-zag. We demonstrate why a single rotation fails, and how a two-step rotation straightens the kink before balancing the tree.

---

### Problem 3.1: The Left-Right (LR) Imbalance (Insert 30, then 10, then 20)

**Problem Statement:** Starting with an empty AVL tree, insert keys $30$, $10$, and $20$ in that order. 
1. Show why a single Right Rotation fails.
2. Fix the tree using the LR Double Rotation (Left Rotation on child, then Right Rotation on root).

::: callout-intuition Core Mental Model
Imagine a crooked bent pipe shaped like a lightning bolt: $30$ goes left to $10$, and $10$ goes right to $20$. If you try to pull the top pipe to the right with a single turn, the kink in the middle flips around and becomes crooked in the opposite direction! To fix a bent pipe:
* **Step 1 (Straighten):** Turn the lower bend so the whole pipe forms a single, straight line ($10 \to 20 \to 30$).
* **Step 2 (Balance):** Now that it is straight, do a standard simple turn to balance it!
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Insert keys and calculate initial Balance Factors</summary>
**What are we doing?** We insert $30$, then $10$ ($< 30 \to$ left), then $20$ ($< 30 \to$ left, $> 10 \to$ right).  
**How do we do it?**

```
        [30] (BF: +2)
        /
      [10]   (BF: -1)
         \
         [20] (BF: 0)
```

Calculate bottom-up:
* Node $20$ (Leaf): height $= 1$, $BF = 0$
* Node $10$: left height $= 0$, right height $= 1 \implies BF = 0 - 1 = -1$, height $= 2$
* Node $30$ (Root): left height $= 2$, right height $= 0 \implies BF = 2 - 0 = +2 \implies \textbf{CRITICAL IMBALANCE!}$
* Diagnosis: Unbalanced node has $BF = +2$, but its left child has $BF = -1$. The signs **differ** ($+2$ and $-1$). This is the unmistakable fingerprint of an **LR Imbalance**!
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Prove why a single Right Rotation FAILS</summary>
**What are we doing?** We show what disaster occurs if a student blindly applies a single Right Rotation at $30$.  
**Why are we showing this?** To prove beyond doubt why double rotations are mathematically necessary.  
**What happens?**
If we perform a single Right Rotation at $30$:
* Node $10$ rises to the top.
* Node $30$ becomes the right child of $10$.
* Node $20$ (which was the right child of $10$) must be handed over to $30$'s left:

```
        [10] (BF: -2)
           \
           [30]
           /
        [20]
```

Calculate the new $BF$ at root $10$:
* Left height $= 0$
* Right height $= 2$
* $BF(10) = 0 - 2 = -2 \implies \textbf{STILL UNBALANCED!}$

A single rotation did not fix the imbalance; it merely flipped an LR imbalance into an RL imbalance! The tree is still broken.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Part 1 of Double Rotation — Left Rotate the Child (Node 10)</summary>
**What are we doing?** We keep root $30$ fixed in place. We perform a **Left Rotation** exclusively on the subproblem formed by child $10$ and grandchild $20$.  
**Why are we doing this?** To straighten the kink $\{30 \to 10 \to 20\}$ into a clean, straight LL line $\{30 \to 20 \to 10\}$.  
**How do we do it?**
* In the subtree rooted at $10$: $20$ rises up to become $30$'s new left child.
* Node $10$ moves down to become the **left child** of $20$.

```
        [30] (BF: +2)
        /
      [20]   (BF: +1)
      /
    [10]     (BF: 0)
```

Look at the tree now! The signs of the balance factors now match ($BF(30) = +2$ and $BF(20) = +1$). The kink has been completely converted into a standard **LL Imbalance**!
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Part 2 of Double Rotation — Right Rotate the Grandparent (Node 30)</summary>
**What changed from Step 3?** We now have a pure LL tree. We can solve it using the familiar single Right Rotation from Problem 1.1.  
**How do we do it?**
* Right Rotate at $30$:
  * Node $20$ rises up to become the new global root.
  * Node $30$ swings down to become the **right child** of $20$.
  * Node $10$ remains the left child of $20$.

```
        [20]
       /    \
    [10]    [30]
```
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Recalculate Balance Factors and State Conclusion</summary>
**What is the final answer?**
* Node $10$: height $= 1$, $BF = 0$
* Node $30$: height $= 1$, $BF = 0$
* Root $20$: height $= 2$, $BF = 1 - 1 = 0$
* In-order sorted order: $10 < 20 < 30$ (BST verified).

**Why does this answer make sense?**
The middle value among the three keys ($20$) was buried at the bottom of the zig-zag. The first rotation lifted $20$ to the middle tier. The second rotation lifted $20$ to the very top, placing the smallest ($10$) on the left and largest ($30$) on the right.
</details>

</div>

---

### Problem 3.2: The Right-Left (RL) Imbalance (Insert 10, then 30, then 20)

**Problem Statement:** Starting with an empty AVL tree, insert keys $10$, $30$, and $20$ in that order. Show the resulting RL imbalance, execute the required double rotation, and trace all pointer adjustments.

::: callout-intuition Core Mental Model
This is the exact mirror image of the LR imbalance. Node $10$ goes right to $30$, and $30$ goes left to $20$. We have a zig-zag leaning to the right. We first rotate the child rightward to straighten the line, then rotate the grandparent leftward to level the tree.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Insert keys and calculate initial Balance Factors</summary>
**What are we doing?** We insert $10$, then $30$ ($> 10 \to$ right), then $20$ ($> 10 \to$ right, $< 30 \to$ left).  
**How do we do it?**

```
    [10]       (BF: -2)
       \
       [30]    (BF: +1)
       /
     [20]      (BF: 0)
```

Heights and balance factors:
* Node $20$ (Leaf): height $= 1$, $BF = 0$
* Node $30$: left height $= 1$, right height $= 0 \implies BF = 1 - 0 = +1$, height $= 2$
* Node $10$ (Root): left height $= 0$, right height $= 2 \implies BF = 0 - 2 = -2 \implies \textbf{CRITICAL IMBALANCE!}$
* Diagnosis: Unbalanced node has $BF = -2$, but its right child has $BF = +1$. The signs differ ($-2$ and $+1$). This is an **RL Imbalance**.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Part 1 of Double Rotation — Right Rotate Child (Node 30)</summary>
**What are we doing?** We keep root $10$ fixed. We perform a **Right Rotation** on the subtree rooted at $30$.  
**Why are we doing this?** To straighten the kink $\{10 \to 30 \to 20\}$ into a straight RR line $\{10 \to 20 \to 30\}$.  
**How do we do it?**
* In the subtree at $30$: $20$ rises up to become $10$'s new right child.
* Node $30$ moves down to become the **right child** of $20$.

```
    [10]       (BF: -2)
       \
       [20]    (BF: -1)
          \
          [30] (BF: 0)
```

The tree is now in a clean **RR Imbalance** configuration ($BF(10) = -2$ and $BF(20) = -1$).
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Part 2 of Double Rotation — Left Rotate Grandparent (Node 10)</summary>
**What changed from Step 2?** We now perform the standard single Left Rotation at root $10$.  
**How do we do it?**
* Left Rotate at $10$:
  * Node $20$ rises to become the new root.
  * Node $10$ moves down to become the **left child** of $20$.
  * Node $30$ remains the right child of $20$.

```
        [20]
       /    \
    [10]    [30]
```
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Recalculate Balance Factors and State Conclusion</summary>
**What is the final answer?**
* Node $10$: height $= 1$, $BF = 0$
* Node $30$: height $= 1$, $BF = 0$
* Root $20$: height $= 2$, $BF = 1 - 1 = 0$
* BST check: $10 < 20 < 30$ holds strictly.

**Why does this answer make sense?**
The RL rotation successfully straightened the rightward kink into a linear chain and then balanced it. Across all 4 rotation scenarios (LL, RR, LR, RL), the middle of the three values ($20$) always ends up as the root, with the smallest on the left and largest on the right.
</details>

</div>

---

## Master Summary: The AVL Rotation Decision Matrix

When inserting a key into an AVL tree, use this universal reference table:

| Unbalanced Node $Z$ ($BF$) | Child $Y$ ($BF$) | Imbalance Type | Action 1 | Action 2 | Final Root of Subtree |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $+2$ (Left-heavy) | $+1$ or $0$ | **LL** | Right Rotate at $Z$ | *None* | $Y$ |
| $-2$ (Right-heavy) | $-1$ or $0$ | **RR** | Left Rotate at $Z$ | *None* | $Y$ |
| $+2$ (Left-heavy) | $-1$ (Opposite sign) | **LR** | Left Rotate at $Y$ | Right Rotate at $Z$ | Grandchild $X$ |
| $-2$ (Right-heavy) | $+1$ (Opposite sign) | **RL** | Right Rotate at $Y$ | Left Rotate at $Z$ | Grandchild $X$ |
