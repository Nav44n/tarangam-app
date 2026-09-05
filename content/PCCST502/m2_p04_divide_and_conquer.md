# Progressive Problems: Merge Sort Step-by-Step

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Level 1: The Recursive Splitting Phase

### Problem 1.1: Deconstructing an Odd-Length Array Down to Base Cases

Given the array of $7$ unsorted integers:
$$A = [38, 27, 43, 3, 9, 82, 10]$$
with $0$-based indices running from $\text{left} = 0$ to $\text{right} = 6$.

Trace the **Divide** phase of Merge Sort. Show every single division calculation using the midpoint formula:
$$\text{mid} = \lfloor \frac{\text{left} + \text{right}}{2} \rfloor$$
Continue splitting each range until every subproblem contains exactly $1$ element (the base case where $\text{left} == \text{right}$).

::: callout-intuition Core Mental Model
Imagine you are handed a messy stack of $7$ test papers and told to sort them alphabetically by student name.
- Sorting $7$ papers at once in your hands is clumsy.
- So, you cut the pile in half: one pile of $4$ papers and one pile of $3$ papers.
- A pile of $4$ is still too big, so you cut that into two piles of $2$.
- A pile of $2$ is cut into two piles of $1$.
- **The Magic Rule of Size 1:** A single paper by itself is **already sorted**! There is nobody else in that pile to be out of order. Once everything is reduced to piles of size $1$, you stop cutting and prepare to weave them back together.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: The Root Problem - Split Range [0 ... 6]</summary>

**What are we doing?** We take the full array of $7$ items spanning indices $0$ to $6$ and calculate its exact midpoint to break it into a Left half and a Right half.

**Why are we starting here?** Merge Sort is a divide-and-conquer algorithm. It cannot begin merging until it splits the overarching problem into the smallest possible subproblems.

**How do we do it?** 1. Identify bounds: $\text{left} = 0$, $\text{right} = 6$.
2. Check base case condition: Is $\text{left} \ge \text{right}$?  
   $0 \ge 6$ is **False**. We must divide!
3. Calculate midpoint:
   $$\text{mid} = \lfloor \frac{0 + 6}{2} \rfloor = \lfloor 3.0 \rfloor = 3$$
4. Form two child ranges:
   - **Left Child Range:** $[\text{left} \dots \text{mid}] = [0 \dots 3]$
   - **Right Child Range:** $[\text{mid} + 1 \dots \text{right}] = [4 \dots 6]$

**Where did this formula come from?** The floor function $\lfloor \cdot \rfloor$ (integer division `(left + right) // 2`) finds the center index. When the number of elements is odd ($7$ elements), integer division assigns the extra element to the left subarray (size $4$ vs size $3$).

**Current Decomposition:**
- Root: `[38, 27, 43, 3, 9, 82, 10]` (indices $0 \dots 6$)
  - Left Half: `[38, 27, 43, 3]` (indices $0 \dots 3$, size $4$)
  - Right Half: `[9, 82, 10]` (indices $4 \dots 6$, size $3$)
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Split Left Subarray [0 ... 3]</summary>

**What changed from Step 1?** In accordance with standard left-first recursion (pre-order traversal), we pause the right half `[9, 82, 10]` and dive into the left range `[38, 27, 43, 3]`.

**What are we doing?** Splitting index range $[0 \dots 3]$.

**How do we do it?** 1. Bounds: $\text{left} = 0$, $\text{right} = 3$.
2. Check base case: $0 \ge 3$ is **False**.
3. Midpoint:
   $$\text{mid} = \lfloor \frac{0 + 3}{2} \rfloor = \lfloor 1.5 \rfloor = 1$$
4. Form child ranges:
   - **Left:** $[0 \dots 1] \implies [38, 27]$
   - **Right:** $[2 \dots 3] \implies [43, 3]$

**Subtree State:**
```text
          [0 ... 3] (size 4)
          /       \
     [0 ... 1]    [2 ... 3]
     [38, 27]      [43, 3]
```
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Split [0 ... 1] into Base-Case Singletons</summary>

**What changed from Step 2?** We dive into the leftmost branch $[0 \dots 1]$.

**What are we doing?** Splitting range $[0 \dots 1]$ down to individual nodes.

**How do we do it?** 1. Bounds: $\text{left} = 0$, $\text{right} = 1$.
2. Base check: $0 \ge 1$ is **False**.
3. Midpoint:
   $$\text{mid} = \lfloor \frac{0 + 1}{2} \rfloor = 0$$
4. Children:
   - Left: $[0 \dots 0] \implies [38]$
   - Right: $[1 \dots 1] \implies [27]$

**Inspect Base Cases:**
- For $[0 \dots 0]$: $\text{left} = 0, \text{right} = 0 \implies \text{left} \ge \text{right}$ is **True!** Base case reached. Stop splitting.
- For $[1 \dots 1]$: $\text{left} = 1, \text{right} = 1 \implies \text{left} \ge \text{right}$ is **True!** Base case reached. Stop splitting.

Both elements `[38]` and `[27]` are now single-element sorted arrays.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Split [2 ... 3] into Base-Case Singletons</summary>

**What changed from Step 3?** Having resolved the left side of $[0 \dots 3]$, the algorithm visits the right sibling $[2 \dots 3]$ (holding elements `[43, 3]`).

**What are we doing?** Splitting range $[2 \dots 3]$.

**How do we do it?** 1. Bounds: $\text{left} = 2$, $\text{right} = 3$.
2. Base check: $2 \ge 3$ is **False**.
3. Midpoint:
   $$\text{mid} = \lfloor \frac{2 + 3}{2} \rfloor = \lfloor 2.5 \rfloor = 2$$
4. Children:
   - Left: $[2 \dots 2] \implies [43]$ ($\text{left} == \text{right} \implies$ **Base Case**)
   - Right: $[3 \dots 3] \implies [3]$ ($\text{left} == \text{right} \implies$ **Base Case**)

At this point, the entire original left half $[0 \dots 3]$ has been broken down into four distinct size-$1$ arrays: `[38]`, `[27]`, `[43]`, `[3]`.
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Split Original Right Subarray [4 ... 6]</summary>

**What changed from Step 4?** Now we resolve the original right half of the array: `[9, 82, 10]` spanning indices $[4 \dots 6]$.

**What are we doing?** Splitting range $[4 \dots 6]$.

**How do we do it?** 1. Bounds: $\text{left} = 4$, $\text{right} = 6$.
2. Base check: $4 \ge 6$ is **False**.
3. Midpoint:
   $$\text{mid} = \lfloor \frac{4 + 6}{2} \rfloor = 5$$
4. Children:
   - **Left:** $[4 \dots 5] \implies [9, 82]$ (size $2$)
   - **Right:** $[6 \dots 6] \implies [10]$ (size $1 \implies \text{left} == \text{right} \implies$ **Base Case!**)

Subarray `[10]` is immediately a base case.
Subarray $[4 \dots 5]$ needs one final split:
- Bounds: $\text{left} = 4, \text{right} = 5$.
- Midpoint: $\text{mid} = \lfloor \frac{4 + 5}{2} \rfloor = 4$.
- Children:
  - Left: $[4 \dots 4] \implies [9]$ (**Base Case**)
  - Right: $[5 \dots 5] \implies [82]$ (**Base Case**)
</details>

<details class="step-card">
<summary class="step-badge">Final Step: The Complete Recursive Decomposition Tree</summary>

**What is the final state of the division phase?**
All $7$ elements are completely isolated into independent subproblems of size $1$:

```text
                     [38, 27, 43, 3, 9, 82, 10]
                            /          \
              [38, 27, 43, 3]          [9, 82, 10]
                /        \                /       \
            [38, 27]    [43, 3]        [9, 82]    [10]
             /    \      /   \          /   \       |
           [38]  [27]  [43]  [3]       [9]  [82]   [10]
```

**Why does this division take $O(\log N)$ levels?**
Each step divides the array length roughly in half:
$$N \longrightarrow \frac{N}{2} \longrightarrow \frac{N}{4} \longrightarrow \dots \longrightarrow 1$$
The number of times an array of length $N$ can be halved until it reaches size $1$ is:
$$\text{Tree Height} = \lceil \log_2(N) \rceil = \lceil \log_2(7) \rceil = 3 \text{ split levels}$$
Because no data is compared during splitting—only indices are halved—the division step takes pure $O(1)$ time per node in the tree.
</details>

</div>

---

## Level 2: The Two-Finger Merge Mechanism

### Problem 2.1: Merging Two Sorted Subarrays Step-by-Step

Suppose the recursive division has completed and smaller merges have already taken place. We have reached the final step where two sorted halves must be merged into one combined sorted array:
- **Left Subarray ($L$):** $[27, 38, 43]$ (length $n_1 = 3$)
- **Right Subarray ($R$):** $[3, 9, 10, 82]$ (length $n_2 = 4$)

We maintain:
- Pointer $i$: Tracks the current element in $L$ (starts at $i = 0$).
- Pointer $j$: Tracks the current element in $R$ (starts at $j = 0$).
- Pointer $k$: Tracks the next open slot in the output buffer `result[]` (starts at $k = 0$).

Trace every single iteration of the merge loop:
```python
while i < len(L) and j < len(R):
    if L[i] <= R[j]:
        result[k] = L[i]
        i += 1
    else:
        result[k] = R[j]
        j += 1
    k += 1
```
Show every pointer movement, comparison, write operation, and the final flush of leftover elements.

::: callout-intuition Core Mental Model
Imagine you have two sorted decks of playing cards face-up on a table: Deck $L$ on your left and Deck $R$ on your right.
- You place your **left index finger** on the top card of Deck $L$.
- You place your **right index finger** on the top card of Deck $R$.
- You look at the two cards your fingers are touching:
  - Whichever card is **smaller** gets picked up and placed face-up into a new merged pile.
  - You slide that specific finger down to the next card in that deck. The other finger **stays exactly where it is**!
- You repeat this until one deck is completely empty. Then, you simply scoop up whatever is left of the remaining deck and set it down at the end of the merged pile.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Initialization of Pointers & Buffers</summary>

**What are we doing?** We prepare our pointers $i, j, k$ and allocate an empty result array of size $n_1 + n_2 = 3 + 4 = 7$.

**Why are we starting here?** A two-finger merge requires comparing the smallest currently unpicked items from both arrays. Since both subarrays are already sorted, their smallest unpicked items are always at the front where indices $i$ and $j$ point.

**How do we do it?** - Left array: $L = [27, 38, 43]$, length $n_1 = 3$
- Right array: $R = [3, 9, 10, 82]$, length $n_2 = 4$
- `result = [_, _, _, _, _, _, _]`
- Set $i = 0$ (points to $L[0] = 27$)
- Set $j = 0$ (points to $R[0] = 3$)
- Set $k = 0$

**System State:**
- $i = 0$ ($L[i] = 27$)
- $j = 0$ ($R[j] = 3$)
- `result = []`
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Iteration 1 - Compare L[0] vs R[0]</summary>

**What changed from Step 1?** We perform our first comparison.

**What are we doing?** Evaluate whether $L[i] \le R[j]$ to determine which element takes slot `result[0]`.

**How do we do it?** 1. Read values: $L[0] = 27$, $R[0] = 3$.
2. Comparison: Is $27 \le 3$?
   $$27 \le 3 \implies \mathbf{False}$$
3. Take the smaller element from the Right array:
   $$\text{result}[0] \leftarrow R[0] = 3$$
4. Advance pointers:
   - $j$ increments: $j = 0 + 1 = 1$ (points to next item in $R$)
   - $k$ increments: $k = 0 + 1 = 1$
   - $i$ stays at $0$ (still waiting to place $27$)

**System State:**
- $i = 0$ ($L[0] = 27$)
- $j = 1$ ($R[1] = 9$)
- `result = [3]`
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Iteration 2 - Compare L[0] vs R[1]</summary>

**What changed from Step 2?** $R[0]$ was placed. Right finger moved to index $1$.

**What are we doing?** Compare current item $L[0]$ with new item $R[1]$.

**How do we do it?** 1. Read values: $L[0] = 27$, $R[1] = 9$.
2. Comparison: Is $27 \le 9$?
   $$27 \le 9 \implies \mathbf{False}$$
3. Take smaller element from Right array:
   $$\text{result}[1] \leftarrow R[1] = 9$$
4. Advance pointers:
   - $j = 1 + 1 = 2$
   - $k = 1 + 1 = 2$
   - $i$ stays at $0$

**System State:**
- $i = 0$ ($L[0] = 27$)
- $j = 2$ ($R[2] = 10$)
- `result = [3, 9]`
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Iteration 3 - Compare L[0] vs R[2]</summary>

**What changed from Step 3?** $R[1]$ was placed. Right finger moved to index $2$.

**What are we doing?** Compare $L[0]$ with $R[2]$.

**How do we do it?** 1. Read values: $L[0] = 27$, $R[2] = 10$.
2. Comparison: Is $27 \le 10$?
   $$27 \le 10 \implies \mathbf{False}$$
3. Take smaller element from Right array:
   $$\text{result}[2] \leftarrow R[2] = 10$$
4. Advance pointers:
   - $j = 2 + 1 = 3$
   - $k = 2 + 1 = 3$
   - $i$ stays at $0$

**System State:**
- $i = 0$ ($L[0] = 27$)
- $j = 3$ ($R[3] = 82$)
- `result = [3, 9, 10]`
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Iteration 4 - Compare L[0] vs R[3]</summary>

**What changed from Step 4?** Right finger moved to index $3$ ($82$). Now the Left element is smaller!

**What are we doing?** Compare $L[0]$ with $R[3]$.

**How do we do it?** 1. Read values: $L[0] = 27$, $R[3] = 82$.
2. Comparison: Is $27 \le 82$?
   $$27 \le 82 \implies \mathbf{True}$$
3. Take smaller element from Left array:
   $$\text{result}[3] \leftarrow L[0] = 27$$
4. Advance pointers:
   - $i$ increments: $i = 0 + 1 = 1$ (Left finger finally moves!)
   - $k$ increments: $k = 3 + 1 = 4$
   - $j$ stays at $3$ (still waiting to place $82$)

**Where did `<=` come from?** Using $\le$ (less than *or equal to*) ensures **stability**. If two elements have equal keys, the element from the Left subarray is chosen first, preserving its original relative order!

**System State:**
- $i = 1$ ($L[1] = 38$)
- $j = 3$ ($R[3] = 82$)
- `result = [3, 9, 10, 27]`
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Iteration 5 - Compare L[1] vs R[3]</summary>

**What changed from Step 5?** $L[0]$ was placed. Left finger moved to index $1$ ($38$).

**What are we doing?** Compare $L[1]$ with $R[3]$.

**How do we do it?** 1. Read values: $L[1] = 38$, $R[3] = 82$.
2. Comparison: Is $38 \le 82$?
   $$38 \le 82 \implies \mathbf{True}$$
3. Take element from Left array:
   $$\text{result}[4] \leftarrow L[1] = 38$$
4. Advance pointers:
   - $i = 1 + 1 = 2$
   - $k = 4 + 1 = 5$
   - $j$ stays at $3$

**System State:**
- $i = 2$ ($L[2] = 43$)
- $j = 3$ ($R[3] = 82$)
- `result = [3, 9, 10, 27, 38]`
</details>

<details class="step-card">
<summary class="step-badge">Step 7: Iteration 6 - Compare L[2] vs R[3] & Exhaust Left Array</summary>

**What changed from Step 6?** $L[1]$ was placed. Left finger moved to index $2$ ($43$).

**What are we doing?** Compare $L[2]$ with $R[3]$.

**How do we do it?** 1. Read values: $L[2] = 43$, $R[3] = 82$.
2. Comparison: Is $43 \le 82$?
   $$43 \le 82 \implies \mathbf{True}$$
3. Take element from Left array:
   $$\text{result}[5] \leftarrow L[2] = 43$$
4. Advance pointers:
   - $i = 2 + 1 = 3$
   - $k = 5 + 1 = 6$
   - $j$ stays at $3$

**Loop Condition Check:**
Is $i < n_1$ and $j < n_2$?
- $i = 3$, $n_1 = 3 \implies 3 < 3$ is **False**!
- The main comparison loop immediately **terminates** because the Left array has run out of elements.

**System State:**
- $i = 3$ (Out of bounds)
- $j = 3$ ($R[3] = 82$)
- `result = [3, 9, 10, 27, 38, 43, _]`
</details>

<details class="step-card">
<summary class="step-badge">Step 8: Residual Flush Phase</summary>

**What changed from Step 7?** The main while loop stopped. Array $R$ still has an uncopied element ($82$ at index $j = 3$).

**What are we doing?** We execute the residual cleanup loops:
```python
while i < len(L):
    result[k] = L[i]; i += 1; k += 1
while j < len(R):
    result[k] = R[j]; j += 1; k += 1
```

**Why do we not need any more comparisons?** Because array $R$ was already sorted before we began! If all elements of $L$ have been placed, every leftover element in $R$ is guaranteed to be greater than or equal to everything currently in `result[]`. We can safely copy them straight into the remaining slots without checking anything.

**How do we do it?** - Left array check: $i = 3 < 3$ is False (nothing to flush).
- Right array check: $j = 3 < 4$ is True.
  - $\text{result}[6] \leftarrow R[3] = 82$
  - $j = 3 + 1 = 4$
  - $k = 6 + 1 = 7$
- Now $j = 4 < 4$ is False. Flush complete!

**Final State of result[]:**
$$\text{result} = [3, 9, 10, 27, 38, 43, 82]$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Time & Space Complexity of the Merge Step</summary>

**What is the final answer?** The combined, fully sorted array:
$$[3, 9, 10, 27, 38, 43, 82]$$

**Why is the merge step $O(N)$?**
- In every iteration of the while loop, exactly **one** element is moved into `result[]`, and pointer $k$ increments by $1$.
- No element is ever inspected or moved twice during a single merge.
- If $N = n_1 + n_2$, the maximum number of comparisons is:
  $$\text{Max Comparisons} = n_1 + n_2 - 1 = 3 + 4 - 1 = 6 \text{ comparisons}$$
- Thus, merging $N$ elements takes strictly linear time:
  $$T_{\text{merge}}(N) = O(N)$$

**Total Merge Sort Complexity:**
- The recursion tree has $\log_2(N)$ levels.
- Across all subproblems at any single level of the tree, the total number of elements merged is always $N$, costing $O(N)$ work per level.
- Multiplying work per level by tree height:
  $$\text{Total Time} = O(N) \times O(\log N) = O(N \log N)$$
- Space complexity requires an auxiliary buffer of size $O(N)$ to hold items during merging.
</details>

</div>
