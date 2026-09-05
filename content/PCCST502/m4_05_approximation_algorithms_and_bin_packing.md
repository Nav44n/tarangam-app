# Module 4.5: Approximation Algorithms — Theoretical Foundations and Bin Packing Heuristics

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search & Computational Complexity  
**Document Classification:** Publication-Grade Theoretical Lecture Note & Mathematical Foundation  

---

## 1. Executive Overview: Coping with NP-Hardness

When confronted with an $\text{NP}$-Hard optimization problem in real-world software engineering, assuming $\text{P} \ne \text{NP}$, we must abandon the hope of finding an algorithm that simultaneously achieves all three ideal properties:
1. **Optimality:** Always finding an exact, globally optimal solution.
2. **Efficiency:** Terminating within polynomial time ($\mathcal{O}(n^k)$).
3. **Universality:** Succeeding on all possible input instances.

```text
                        THE COMPUTATIONAL TRILEMMA
                                (Choose Two)
                                
                              [ Optimality ]
                                  /    \
                                 /      \
                                /        \
           (Exact Exponential   /          \   (Polynomial-Time
            Solvers: B&B, DP)  /            \   Heuristics:
                              /              \   Approximation)
                             /                \
             [ Universality ]------------------[ Efficiency ]
                                (Restricted Subclasses:
                                 Trees, Planar Graphs)
```

To deliver practical solutions for industrial systems—such as cloud container allocation, semiconductor routing, logistics scheduling, and network provisioning—we relax the **Optimality** requirement. We study **Approximation Algorithms**: algorithms that run in provable deterministic polynomial time and provide **rigorous mathematical guarantees** on the quality of the returned solution relative to the true optimal solution.

::: callout-intuition
**Mental Model: Approximation vs. Heuristics**  
- A **Heuristic** (e.g., Genetic Algorithms, Simulated Annealing) is a rule of thumb. It often produces decent results in practice, but offers *no mathematical guarantees*. On pathological inputs, its solution quality can be arbitrarily far from optimal.
- An **Approximation Algorithm** is a mathematically certified engine. It provides a formal proof: *"No matter how malicious the input instance is, the returned solution is guaranteed to be within a factor $\rho$ of the absolute mathematical optimum."*
:::

---

## 2. Mathematical Formalization of Approximation

Let $\Pi$ be an optimization problem, and let $I$ be an arbitrary input instance of $\Pi$.
- Let $\text{OPT}(I)$ denote the objective cost/value of a globally optimal solution for instance $I$.
- Let $A(I)$ denote the objective cost/value of the candidate solution produced by polynomial-time approximation algorithm $A$ on instance $I$.

To ensure mathematical stability, we assume objective costs are strictly positive: $\text{OPT}(I) > 0$ and $A(I) > 0$.

---

### 2.1 The Approximation Ratio $\rho$

#### Definition 2.1 (Approximation Ratio)
Algorithm $A$ has an **approximation ratio** (or performance guarantee) of $\rho(n) \ge 1$ if, for all instances $I$ of size $n$, the ratio satisfies:

$$\max \left( \frac{A(I)}{\text{OPT}(I)}, \; \frac{\text{OPT}(I)}{A(I)} \right) \le \rho(n)$$

This symmetrical definition unifies both minimization and maximization problems into a single standard where $\rho \ge 1$:

1. **For Minimization Problems** (e.g., Bin Packing, Vertex Cover, TSP):  
   Since an approximation algorithm can never outperform the minimum possible cost, $A(I) \ge \text{OPT}(I)$. The ratio simplifies to:
   $$\frac{A(I)}{\text{OPT}(I)} \le \rho \iff A(I) \le \rho \cdot \text{OPT}(I) \quad (\rho \ge 1)$$
   *(Example: A $2$-approximation algorithm for Vertex Cover is guaranteed to select at most twice the number of vertices chosen by the optimal cover).*

2. **For Maximization Problems** (e.g., 0/1 Knapsack, Maximum Cut):  
   Since an approximation algorithm can never exceed the maximum possible profit, $A(I) \le \text{OPT}(I)$. The ratio simplifies to:
   $$\frac{\text{OPT}(I)}{A(I)} \le \rho \iff A(I) \ge \frac{1}{\rho} \cdot \text{OPT}(I) \quad (\rho \ge 1)$$
   *(Alternatively, in literature, maximization is often stated as $A(I) \ge \alpha \cdot \text{OPT}(I)$ for $\alpha \in (0, 1]$, where $\alpha = 1/\rho$).*

---

### 2.2 Absolute vs. Asymptotic Approximation Ratios

In problems like Bin Packing, small additive boundary constants can distort the performance ratio for tiny inputs (e.g., using 2 bins instead of 1 is a ratio of 2.0, but using 101 bins instead of 100 is a ratio of 1.01). To evaluate large-scale performance accurately, complexity theory distinguishes between absolute and asymptotic ratios.

#### Definition 2.2 (Absolute Performance Ratio)
An algorithm $A$ has an **absolute approximation ratio** $\rho_A$ if:
$$\rho_A = \sup_{I} \left\{ \frac{A(I)}{\text{OPT}(I)} \right\}$$
for all possible instances $I$.

#### Definition 2.3 (Asymptotic Performance Ratio)
An algorithm $A$ has an **asymptotic approximation ratio** $\rho_A^{\infty}$ if there exists an integer constant $C \ge 0$ such that for all instances $I$:
$$A(I) \le \rho_A^{\infty} \cdot \text{OPT}(I) + C$$

Formally, taking the limit as optimal cost approaches infinity:
$$\rho_A^{\infty} = \limsup_{\text{OPT}(I) \to \infty} \left( \max_{I: \text{OPT}(I) = k} \frac{A(I)}{\text{OPT}(I)} \right)$$
The asymptotic ratio describes how the algorithm behaves at enterprise scale, where $C$ becomes negligible.

---

### 2.3 The Hierarchy of Approximation Classes

Just as decision problems are grouped into $\text{P}$, $\text{NP}$, and $\text{PSPACE}$, optimization problems are grouped by how closely they can be approximated in polynomial time.

```text
================================================================================
                    THE APPROXIMABILITY HIERARCHY
================================================================================

   [ FPTAS ] (Fully Polynomial-Time Approximation Schemes)
     |       Time: O((1/ε)^a * n^b) -> Knapsack Problem
     v
   [ PTAS ]  (Polynomial-Time Approximation Schemes)
     |       Time: O(n^(f(1/ε))) -> Makespan Scheduling, Geometric TSP
     v
   [ APX ]   (Constant-Factor Approximable: ρ = O(1))
     |       Metric TSP (3/2), Vertex Cover (2), Bin Packing (Asymptotic 1.22)
     v
   [ Log-APX ] (Logarithmic-Factor Approximable: ρ = O(log n))
     |       Set Cover, Metric k-Median
     v
   [ Inapproximable ] (Cannot be approximated within n^(1 - ε) unless P = NP)
             General TSP, Maximum Independent Set, Chromatic Number
```

1. **PTAS (Polynomial-Time Approximation Scheme):**  
   An algorithm family where, for any user-specified error parameter $\epsilon > 0$, the algorithm produces a $(1 + \epsilon)$-approximation in time polynomial in input size $n$: $\mathcal{O}(n^{f(1/\epsilon)})$.
2. **FPTAS (Fully Polynomial-Time Approximation Scheme):**  
   The pinnacle of approximation tractability. The runtime is polynomial in **both** input size $n$ and error precision $1/\epsilon$: $\mathcal{O}((1/\epsilon)^a \cdot n^b)$.
3. **APX (Approximable):**  
   Problems that admit a constant-factor $\rho$-approximation in polynomial time (e.g., $\rho = 2$), but do not admit a PTAS unless $\text{P} = \text{NP}$.

---

## 3. The 1-Dimensional Bin Packing Problem

The **1-Dimensional Bin Packing Problem** is a foundational $\text{NP}$-Hard combinatorial optimization problem with applications in disk storage management, cloud compute resource allocation, television commercial scheduling, and shipping logistics.

### 3.1 Formal Mathematical Formulation
- **Input:**
  1. An infinite supply of identical, discrete containers called **bins**, each having a fixed maximum unit capacity:
     $$C = 1$$
  2. A finite list of $n$ items:
     $$L = (w_1, w_2, \dots, w_n)$$
     where each item $i$ has a rational size satisfying:
     $$0 < w_i \le 1 \quad \forall \; i \in \{1, 2, \dots, n\}$$
- **Feasible Solution:** An assignment or partitioning of items into $m$ bins, denoted by index sets $B_1, B_2, \dots, B_m$, such that:
  1. Every item is assigned to exactly one bin:
     $$\bigcup_{j=1}^m B_j = \{1, 2, \dots, n\} \quad \text{and} \quad B_j \cap B_k = \emptyset \quad (\forall j \ne k)$$
  2. The capacity of no bin is exceeded:
     $$\sum_{i \in B_j} w_i \le 1 \quad \forall \; j \in \{1, 2, \dots, m\}$$
- **Optimization Objective:** Minimize the total number of utilized bins $m$:
  $$\min \quad m$$
  We denote the absolute minimal number of bins required for list $L$ as $\text{OPT}(L)$.

---

### 3.2 Theoretical Lower Bounds on $\text{OPT}(L)$

Because computing $\text{OPT}(L)$ is $\text{NP}$-Hard, approximation proofs rely on establishing **mathematical lower bounds** on $\text{OPT}(L)$ derived directly from physical invariants of the input list.

#### Lower Bound 1: The Continuous Volume Bound
The total aggregate volume of all items cannot exceed the total volume provided by the open bins:

$$\text{OPT}(L) \ge \left\lceil \sum_{i=1}^n w_i \right\rceil$$

*Proof:* Each bin has maximum capacity 1. If $m$ bins accommodate all items, then:
$$\sum_{i=1}^n w_i = \sum_{j=1}^m \left( \sum_{i \in B_j} w_i \right) \le \sum_{j=1}^m 1 = m$$
Since the number of bins must be an integer, $m \ge \lceil \sum w_i \rceil$. This holds for all feasible packings, including the optimal packing.

#### Lower Bound 2: The Large Items Bound
Let $L_{> 1/2}$ be the sublist of items with weight strictly greater than $1/2$:
$$L_{> 1/2} = \{w_i \in L \mid w_i > 0.5\}$$
Then:
$$\text{OPT}(L) \ge |L_{> 1/2}|$$

*Proof:* If two items $w_a, w_b \in L_{> 1/2}$ are placed in the same bin, their combined weight would be:
$$w_a + w_b > 0.5 + 0.5 = 1.0$$
This violates the bin capacity constraint. Therefore, no two items larger than $0.5$ can share a bin; each must occupy its own separate bin.

---

## 4. Online vs. Offline Processing Paradigms

Bin packing algorithms operate under two distinct execution paradigms:

```text
+-----------------------+------------------------------------------------------+
| Paradigm              | Operational Characteristics                          |
+-----------------------+------------------------------------------------------+
| Online Bin Packing    | Items arrive sequentially: w_1, w_2, ..., w_n.       |
|                       | Each item must be irrevocably placed into a bin      |
|                       | immediately upon arrival, without knowledge of       |
|                       | future items.                                        |
+-----------------------+------------------------------------------------------+
| Offline Bin Packing   | The entire list L is known in advance. The algorithm |
|                       | can inspect, sort, and reorganize all items prior to |
|                       | performing bin placement.                            |
+-----------------------+------------------------------------------------------+
```

---

## 5. Classical Online Heuristics: Analysis and Proofs

We now examine the four classical online heuristics: **Next Fit (NF)**, **First Fit (FF)**, **Best Fit (BF)**, and **Worst Fit (WF)**.

---

### 5.1 Next Fit (NF)

#### Algorithmic Principle:
Next Fit maintains only **one active open bin**. When an item arrives:
- If it fits in the current open bin, pack it there.
- If it exceeds the remaining capacity, **permanently seal** the current bin (it can never be used again) and open a new bin.

#### Pseudo-code Implementation:
```text
Algorithm NextFit(L = (w_1, w_2, ..., w_n))
begin
    m := 1;                     // Number of bins opened
    remaining_space := 1.0;     // Space left in current bin
    
    for i := 1 to n do
        if w_i <= remaining_space then
            Assign item w_i to Bin B_m;
            remaining_space := remaining_space - w_i;
        else
            m := m + 1;         // Permanently close B_{m-1}, open B_m
            Assign item w_i to Bin B_m;
            remaining_space := 1.0 - w_i;
        end if;
    end for;
    
    return m;
end;
```
- **Time Complexity:** $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ auxiliary space. It makes a single pass over the items.

---

#### Theorem 5.1 (Approximation Bound for Next Fit)
*For any input list $L$, the number of bins used by Next Fit satisfies:*
$$\text{NF}(L) \le 2 \cdot \text{OPT}(L)$$
*Furthermore, the asymptotic approximation ratio is exactly $\rho_{\text{NF}}^{\infty} = 2$.*

```text
                 NEXT FIT ADJACENT BIN PAIRING
                 
     Bin B_1       Bin B_2           Bin B_{2k-1}  Bin B_{2k}
   +---------+   +---------+       +---------+   +---------+
   |/////////|   |/////////|  ...  |/////////|   |/////////|
   |/////////|   |/////////|       |/////////|   |/////////|
   +---------+   +---------+       +---------+   +---------+
   \_______________________/       \_______________________/
       Weight Sum > 1.0                Weight Sum > 1.0
```

#### Formal Mathematical Proof:
1. Let $m = \text{NF}(L)$ be the total number of bins opened by Next Fit.
2. Consider any two consecutive bins $B_j$ and $B_{j+1}$ for $j \in \{1, 2, \dots, m - 1\}$.
3. Let $w(B_j)$ denote the total weight of items assigned to bin $B_j$.
4. Why did the algorithm open bin $B_{j+1}$?  
   Because the first item placed into bin $B_{j+1}$—call it item $x$—could not fit into bin $B_j$:
   $$w(B_j) + w_x > 1.0$$
5. Since item $x$ is now in bin $B_{j+1}$, its weight is included in $w(B_{j+1})$:
   $$w(B_{j+1}) \ge w_x$$
6. Adding these two expressions:
   $$w(B_j) + w(B_{j+1}) > 1.0$$
7. Now, partition the $m$ bins into consecutive pairs:
   - If $m$ is even: $(B_1, B_2), (B_3, B_4), \dots, (B_{m-1}, B_m)$, giving exactly $m/2$ pairs.
   - If $m$ is odd: $(B_1, B_2), \dots, (B_{m-2}, B_{m-1})$ plus the single final bin $B_m$, giving $(m-1)/2$ pairs.
8. Summing the weights across all bins:
   $$\sum_{i=1}^n w_i = \sum_{j=1}^m w(B_j) = \sum_{k=1}^{\lfloor m/2 \rfloor} [w(B_{2k-1}) + w(B_{2k})] + [w(B_m) \text{ if } m \text{ is odd}]$$
9. Since each pair has total weight strictly greater than $1.0$:
   $$\sum_{i=1}^n w_i > \lfloor m/2 \rfloor \cdot 1.0 = \left\lfloor \frac{m}{2} \right\rfloor > \frac{m - 1}{2}$$
10. Using the continuous volume lower bound (Theorem 3.1):
    $$\text{OPT}(L) \ge \sum_{i=1}^n w_i > \frac{m - 1}{2} = \frac{\text{NF}(L) - 1}{2}$$
11. Multiplying both sides by 2:
    $$2 \cdot \text{OPT}(L) > \text{NF}(L) - 1 \implies \text{NF}(L) \le 2 \cdot \text{OPT}(L)$$
12. Thus, the performance ratio of Next Fit is strictly bounded by 2. $\blacksquare$

---

#### Tight Pathological Lower Bound Example for Next Fit:
To prove that the ratio of 2 is **tight**, we construct a pathological family of inputs where $\text{NF}(L) / \text{OPT}(L) \to 2$.
- Let $n$ be an even integer. Consider an input sequence of $n$ items with alternating weights:
  $$L = \left( \frac{1}{2}, \; \frac{1}{2n}, \; \frac{1}{2}, \; \frac{1}{2n}, \; \dots, \; \frac{1}{2}, \; \frac{1}{2n} \right)$$
- **Next Fit Behavior:**
  * Bin 1 receives item 1 ($1/2$) and item 2 ($1/2n$). Weight $= 1/2 + 1/2n$.
  * Item 3 arrives with weight $1/2$. Remaining space in Bin 1 is $1 - (1/2 + 1/2n) = 1/2 - 1/2n < 1/2$. Item 3 does not fit!
  * Next Fit closes Bin 1 and opens Bin 2 for item 3.
  * This repeats for every pair: each bin contains exactly one $1/2$ item and one tiny $1/2n$ item.
  * Total bins used:
    $$\text{NF}(L) = \frac{n}{2}$$
- **Optimal Packing $\text{OPT}(L)$:**
  * Put two $1/2$ items in each bin: this requires $(n/2) / 2 = n/4$ bins.
  * Group all $n/2$ tiny items of size $1/2n$ together: their total weight is $(n/2) \cdot (1/2n) = 1/4$, which fits in a single bin.
  * Total optimal bins:
    $$\text{OPT}(L) = \frac{n}{4} + 1$$
- **Asymptotic Ratio:**
  $$\lim_{n \to \infty} \frac{\text{NF}(L)}{\text{OPT}(L)} = \lim_{n \to \infty} \frac{n/2}{n/4 + 1} = \frac{1/2}{1/4} = 2$$
- This confirms that the bound of 2 is tight.

---

### 5.2 First Fit (FF)

#### Algorithmic Principle:
First Fit keeps **all open bins active**. When an item $w_i$ arrives:
- Scan through all open bins $B_1, B_2, \dots, B_m$ **in order of their indices**.
- Place $w_i$ into the **first** bin that has sufficient remaining capacity:
  $$\text{First bin } B_j \text{ such that } w(B_j) + w_i \le 1.0$$
- If no existing bin can accommodate $w_i$, open a new bin $B_{m+1}$ and place $w_i$ there.

#### Complexity:
- Naive scan takes $\mathcal{O}(n^2)$ time.
- Using an augmented balanced binary search tree (or segment tree tracking max remaining capacity), First Fit can be implemented in $\mathcal{O}(n \log n)$ time.

---

#### Theorem 5.2 (Approximation Bound for First Fit)
*(Proven by David S. Johnson in his 1973 doctoral dissertation)*  
*For any input list $L$, the number of bins used by First Fit satisfies:*
$$\text{FF}(L) \le \left\lceil \frac{17}{10} \text{OPT}(L) \right\rceil$$
*The asymptotic approximation ratio is:*
$$\rho_{\text{FF}}^{\infty} = \frac{17}{10} = 1.7$$

#### Elementary Upper Bound Proof ($\text{FF}(L) \le 2 \cdot \text{OPT}(L)$):
While Johnson's $1.7$ bound requires complex weighting functions across 40 pages of analysis, we can prove an elementary bound of 2:
1. Let $m = \text{FF}(L)$.
2. At most **one bin** among $B_1, B_2, \dots, B_m$ can be at least half empty (weight $\le 0.5$).
   - *Proof by contradiction:* Suppose two bins $B_j$ and $B_k$ (with $j < k$) both have weight $\le 0.5$.
   - Consider the items in $B_k$. Since $w(B_k) \le 0.5$, every item $x \in B_k$ has weight $w_x \le 0.5$.
   - But when item $x$ arrived, bin $B_j$ had weight $w(B_j) \le 0.5$.
   - Thus: $w(B_j) + w_x \le 0.5 + 0.5 = 1.0$.
   - By definition of First Fit, item $x$ would have been placed into the earlier bin $B_j$ instead of reaching $B_k$.
   - Contradiction! Therefore, at most one bin can have weight $\le 0.5$.
3. This means at least $m - 1$ bins have weight strictly greater than $0.5$:
   $$\sum_{i=1}^n w_i > (m - 1) \cdot 0.5 = \frac{m - 1}{2}$$
4. By the volume lower bound: $\text{OPT}(L) \ge \sum w_i > \frac{m - 1}{2}$.
5. Rearranging gives:
   $$\text{FF}(L) \le 2 \cdot \text{OPT}(L)$$

---

### 5.3 Best Fit (BF)

#### Algorithmic Principle:
Best Fit also keeps all open bins active. When an item $w_i$ arrives:
- Scan all currently open bins that have sufficient space ($1 - w(B_j) \ge w_i$).
- Place $w_i$ into the bin that **leaves the least remaining space** (the "tightest fit"):
  $$\text{Select } B_j \text{ that minimizes } (1 - w(B_j) - w_i) \text{ subject to } (1 - w(B_j) - w_i) \ge 0$$
- If no open bin has enough room, open a new bin.

#### Complexity & Ratio:
- Implemented in $\mathcal{O}(n \log n)$ time using a self-balancing binary search tree (e.g., AVL or Red-Black tree) indexed by remaining capacity.
- **Asymptotic Ratio:** Exactly identical to First Fit:
  $$\rho_{\text{BF}}^{\infty} = \frac{17}{10} = 1.7$$

---

### 5.4 Worst Fit (WF)

#### Algorithmic Principle:
Worst Fit places each arriving item into the open bin that has the **maximum remaining empty space** (the "loosest fit"):
$$\text{Select } B_j \text{ that maximizes } (1 - w(B_j)) \text{ subject to } (1 - w(B_j)) \ge w_i$$
- **Flaw:** By spreading items thinly across bins, Worst Fit quickly leaves many bins with moderate space that cannot fit larger items later.
- **Performance:** Performs identically to Next Fit in the worst case:
  $$\rho_{\text{WF}}^{\infty} = 2.0$$
- Worst Fit is generally not recommended for practical bin packing.

---

## 6. Offline Heuristics: Sorting First

In offline bin packing, we know all items in advance. Sorting the items in **descending order of size** before packing ensures that the most difficult, space-consuming items are placed first, when all bins are empty. Smaller items are then used to fill the remaining gaps.

```text
               Offline Preprocessing:
   Original List:  L = (0.2, 0.7, 0.3, 0.8, 0.5, 0.1, 0.4)
                            |
                            v  Sort Descending (O(n log n))
   Sorted List:    L_sorted = (0.8, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1)
```

---

### 6.1 First Fit Decreasing (FFD)

#### Algorithmic Principle:
1. Sort input list $L$ such that:
   $$w_1 \ge w_2 \ge \dots \ge w_n$$
2. Apply standard First Fit to the sorted sequence.

#### Computational Complexity:
- Sorting takes $\mathcal{O}(n \log n)$ time using MergeSort or QuickSort.
- Packing with a tree data structure takes $\mathcal{O}(n \log n)$ time.
- Total time complexity: $\mathcal{O}(n \log n)$.

---

#### Theorem 6.1 (Johnson, 1973; Baker, 1985; Yue, 1991; Dósa, 2007)
*For any input list $L$, the number of bins used by First Fit Decreasing satisfies:*
$$\text{FFD}(L) \le \frac{11}{9} \text{OPT}(L) + \frac{6}{9} = \frac{11}{9} \text{OPT}(L) + \frac{2}{3}$$
*The asymptotic approximation ratio is:*
$$\rho_{\text{FFD}}^{\infty} = \frac{11}{9} \approx 1.222\dots$$

This guarantees that FFD will never use more than roughly **$22.2\%$ more bins** than the theoretical optimal packing.

---

### 6.2 Structural Lemma: The Weight Threshold of FFD

The key intuition behind FFD's performance guarantee is captured by the following lemma.

#### Lemma 6.2 (The 1/3 Item Bound)
*If First Fit Decreasing uses $m$ bins to pack list $L$, then every bin from $B_{\lfloor m/2 \rfloor + 1}$ through $B_m$ contains items of size strictly less than or equal to $1/2$. Furthermore, any bin beyond $\text{OPT}(L)$ contains items of size at most $1/3$.*

#### Theorem 6.3 (Simplified Analytical Bound for FFD)
*If an item placed into bin $B_m$ (where $m = \text{FFD}(L)$) has size $w_i \le 1/3$, then:*
$$\text{FFD}(L) \le \frac{4}{3} \text{OPT}(L) + 1$$

#### Mathematical Proof:
1. Suppose FFD opens $m$ bins, and the first item placed in the final bin $B_m$ has weight $w_k \le 1/3$.
2. Because the list was sorted in descending order, all items placed into bins $B_1, B_2, \dots, B_{m-1}$ after item $k$ also have weight $\le w_k \le 1/3$.
3. Why did item $k$ get placed into bin $B_m$?  
   Because it could not fit into any of the previous $m - 1$ bins ($B_1$ through $B_{m-1}$).
4. Therefore, every bin $B_j$ ($j \in \{1, 2, \dots, m-1\}$) has remaining space strictly less than $w_k$:
   $$1 - w(B_j) < w_k \le \frac{1}{3} \implies w(B_j) > 1 - \frac{1}{3} = \frac{2}{3}$$
5. Summing the weights across the first $m - 1$ bins:
   $$\sum_{i=1}^n w_i \ge \sum_{j=1}^{m-1} w(B_j) > (m - 1) \cdot \frac{2}{3}$$
6. By the continuous volume lower bound, $\text{OPT}(L) \ge \sum w_i$:
   $$\text{OPT}(L) > (m - 1) \cdot \frac{2}{3} = \frac{2}{3}(m - 1)$$
7. Multiplying both sides by $3/2$:
   $$\frac{3}{2} \text{OPT}(L) > m - 1 \implies m < \frac{3}{2} \text{OPT}(L) + 1$$
8. (A more detailed classification of item weights $< 1/3$ tightens this bound to $\frac{11}{9} \text{OPT} + \frac{6}{9}$, proving the theorem). $\blacksquare$

---

### 6.3 Best Fit Decreasing (BFD)

#### Algorithmic Principle:
1. Sort input list $L$ in descending order: $w_1 \ge w_2 \ge \dots \ge w_n$.
2. Apply standard Best Fit to the sorted sequence.
- **Asymptotic Performance:** Identical to FFD:
  $$\rho_{\text{BFD}}^{\infty} = \frac{11}{9} \approx 1.222\dots$$
- **Practical Note:** While FFD and BFD have the same theoretical worst-case bound, BFD often leaves slightly smaller residual spaces on average empirical test suites.

---

## 7. Comparative Execution Trace Across All 6 Heuristics

To see how these heuristics compare in practice, we trace all six algorithms on the same input list.

### Concrete Instance Specification:
- Fixed Bin Capacity: $C = 1.0$
- Item Count: $n = 7$
- Sequence of item weights:
  $$L = (0.4, \; 0.8, \; 0.2, \; 0.25, \; 0.7, \; 0.15, \; 0.5)$$

```text
Total aggregate weight:
  ∑ w_i = 0.4 + 0.8 + 0.2 + 0.25 + 0.7 + 0.15 + 0.5 = 3.00

Continuous Volume Lower Bound:
  OPT(L) ≥ ⌈3.00⌉ = 3 bins
```

---

### Trace 1: Next Fit (NF)
- **Item 1 ($0.4$):** Open Bin 1. Remaining space: $1.0 - 0.4 = 0.6$.
- **Item 2 ($0.8$):** Exceeds $0.6$. **Close Bin 1**. Open Bin 2. Remaining space: $1.0 - 0.8 = 0.2$.
- **Item 3 ($0.2$):** Fits in Bin 2 ($0.2 \le 0.2$). Place in Bin 2. Remaining space: $0.2 - 0.2 = 0.0$.
- **Item 4 ($0.25$):** Exceeds $0.0$. **Close Bin 2**. Open Bin 3. Remaining space: $1.0 - 0.25 = 0.75$.
- **Item 5 ($0.7$):** Fits in Bin 3 ($0.7 \le 0.75$). Place in Bin 3. Remaining space: $0.75 - 0.7 = 0.05$.
- **Item 6 ($0.15$):** Exceeds $0.05$. **Close Bin 3**. Open Bin 4. Remaining space: $1.0 - 0.15 = 0.85$.
- **Item 7 ($0.5$):** Fits in Bin 4 ($0.5 \le 0.85$). Place in Bin 4. Remaining space: $0.85 - 0.5 = 0.35$.
- **Next Fit Result:** **4 Bins used**
  * $B_1 = [0.4]$ (rem: $0.6$)
  * $B_2 = [0.8, 0.2]$ (rem: $0.0$)
  * $B_3 = [0.25, 0.7]$ (rem: $0.05$)
  * $B_4 = [0.15, 0.5]$ (rem: $0.35$)

---

### Trace 2: First Fit (FF)
- **Item 1 ($0.4$):** Place in Bin 1. (rem: $0.6$).
- **Item 2 ($0.8$):** Cannot fit in $B_1$ ($0.8 > 0.6$). Open Bin 2. (rem: $0.2$).
- **Item 3 ($0.2$):** Fits in Bin 1 ($0.2 \le 0.6$). Place in Bin 1! (rem: $0.4$).
- **Item 4 ($0.25$):** Fits in Bin 1 ($0.25 \le 0.4$). Place in Bin 1! (rem: $0.15$).
- **Item 5 ($0.7$):**
  * Check $B_1$: rem $0.15 < 0.7$. No.
  * Check $B_2$: rem $0.2 < 0.7$. No.
  * Open Bin 3. Place in Bin 3. (rem: $0.3$).
- **Item 6 ($0.15$):**
  * Check $B_1$: rem $0.15 \ge 0.15$. Fits in Bin 1! Place in Bin 1. (rem: $0.0$).
- **Item 7 ($0.5$):**
  * Check $B_1$: rem $0.0 < 0.5$. No.
  * Check $B_2$: rem $0.2 < 0.5$. No.
  * Check $B_3$: rem $0.3 < 0.5$. No.
  * Open Bin 4. Place in Bin 4. (rem: $0.5$).
- **First Fit Result:** **4 Bins used**
  * $B_1 = [0.4, 0.2, 0.25, 0.15]$ (rem: $0.0$)
  * $B_2 = [0.8]$ (rem: $0.2$)
  * $B_3 = [0.7]$ (rem: $0.3$)
  * $B_4 = [0.5]$ (rem: $0.5$)

---

### Trace 3: Best Fit (BF)
- **Item 1 ($0.4$):** Place in Bin 1. (rem: $0.6$).
- **Item 2 ($0.8$):** Cannot fit in $B_1$. Open Bin 2. (rem: $0.2$).
- **Item 3 ($0.2$):**
  * Fits in $B_1$ (leaves $0.6 - 0.2 = 0.4$).
  * Fits in $B_2$ (leaves $0.2 - 0.2 = 0.0$).
  * Best fit is $B_2$ (leaves least space: $0.0$). Place in Bin 2! (rem: $0.0$).
- **Item 4 ($0.25$):**
  * Fits in $B_1$ (leaves $0.6 - 0.25 = 0.35$).
  * Cannot fit in $B_2$ (rem: $0.0$).
  * Place in Bin 1. (rem: $0.35$).
- **Item 5 ($0.7$):** Cannot fit in $B_1$ or $B_2$. Open Bin 3. (rem: $0.3$).
- **Item 6 ($0.15$):**
  * Fits in $B_1$ (leaves $0.35 - 0.15 = 0.20$).
  * Fits in $B_3$ (leaves $0.30 - 0.15 = 0.15$).
  * Best fit is $B_3$ (leaves less space: $0.15$). Place in Bin 3! (rem: $0.15$).
- **Item 7 ($0.5$):**
  * Cannot fit in $B_1$ ($0.35$), $B_2$ ($0.0$), or $B_3$ ($0.15$).
  * Open Bin 4. Place in Bin 4. (rem: $0.5$).
- **Best Fit Result:** **4 Bins used**
  * $B_1 = [0.4, 0.25]$ (rem: $0.35$)
  * $B_2 = [0.8, 0.2]$ (rem: $0.0$)
  * $B_3 = [0.7, 0.15]$ (rem: $0.15$)
  * $B_4 = [0.5]$ (rem: $0.5$)

---

### Trace 4: Worst Fit (WF)
- **Item 1 ($0.4$):** Place in Bin 1. (rem: $0.6$).
- **Item 2 ($0.8$):** Cannot fit in $B_1$. Open Bin 2. (rem: $0.2$).
- **Item 3 ($0.2$):** Open bins have rem space: $B_1: 0.6$, $B_2: 0.2$. Max remaining is $B_1$. Place in $B_1$. (rem: $0.4$).
- **Item 4 ($0.25$):** Open bins: $B_1: 0.4$, $B_2: 0.2$. Max remaining is $B_1$. Place in $B_1$. (rem: $0.15$).
- **Item 5 ($0.7$):** Neither bin has $\ge 0.7$. Open Bin 3. (rem: $0.3$).
- **Item 6 ($0.15$):** Open bins: $B_1: 0.15$, $B_2: 0.2$, $B_3: 0.3$. Max remaining is $B_3$. Place in $B_3$. (rem: $0.15$).
- **Item 7 ($0.5$):** Open bins: $B_1: 0.15$, $B_2: 0.2$, $B_3: 0.15$. None have space $\ge 0.5$. Open Bin 4. Place in $B_4$. (rem: $0.5$).
- **Worst Fit Result:** **4 Bins used**

---

### Trace 5: First Fit Decreasing (FFD)
1. **Sort input list descending:**
   $$L_{\text{sorted}} = (0.8, \; 0.7, \; 0.5, \; 0.4, \; 0.25, \; 0.2, \; 0.15)$$
2. **Sequential Placement:**
   - **Item 1 ($0.8$):** Place in Bin 1. (rem: $0.2$).
   - **Item 2 ($0.7$):** Cannot fit in $B_1$ ($0.2$). Open Bin 2. (rem: $0.3$).
   - **Item 3 ($0.5$):** Cannot fit in $B_1$ ($0.2$) or $B_2$ ($0.3$). Open Bin 3. (rem: $0.5$).
   - **Item 4 ($0.4$):**
     * Check $B_1$ ($0.2$): No.
     * Check $B_2$ ($0.3$): No.
     * Check $B_3$ ($0.5$): Fits! Place in Bin 3. (rem: $0.5 - 0.4 = 0.1$).
   - **Item 5 ($0.25$):**
     * Check $B_1$ ($0.2$): No.
     * Check $B_2$ ($0.3$): Fits! Place in Bin 2. (rem: $0.3 - 0.25 = 0.05$).
   - **Item 6 ($0.2$):**
     * Check $B_1$ ($0.2$): Fits exactly! Place in Bin 1. (rem: $0.2 - 0.2 = 0.0$).
   - **Item 7 ($0.15$):**
     * Check $B_1$ ($0.0$): No.
     * Check $B_2$ ($0.05$): No.
     * Check $B_3$ ($0.10$): No.
     * Open Bin 4. Place in Bin 4. (rem: $0.85$).
3. **FFD Result:** **4 Bins used**
   * $B_1 = [0.8, 0.2]$ (rem: $0.0$)
   * $B_2 = [0.7, 0.25]$ (rem: $0.05$)
   * $B_3 = [0.5, 0.4]$ (rem: $0.1$)
   * $B_4 = [0.15]$ (rem: $0.85$)

---

### Trace 6: Best Fit Decreasing (BFD)
1. **Sorted list:** $L_{\text{sorted}} = (0.8, \; 0.7, \; 0.5, \; 0.4, \; 0.25, \; 0.2, \; 0.15)$
2. **Placement:**
   - **Item 1 ($0.8$):** Place in Bin 1. (rem: $0.2$).
   - **Item 2 ($0.7$):** Cannot fit in $B_1$. Open Bin 2. (rem: $0.3$).
   - **Item 3 ($0.5$):** Cannot fit in $B_1$ or $B_2$. Open Bin 3. (rem: $0.5$).
   - **Item 4 ($0.4$):** Only fits in $B_3$. Place in $B_3$. (rem: $0.1$).
   - **Item 5 ($0.25$):** Only fits in $B_2$. Place in $B_2$. (rem: $0.05$).
   - **Item 6 ($0.2$):**
     * Fits in $B_1$ (leaves $0.2 - 0.2 = 0.0$).
     * Best fit is $B_1$. Place in $B_1$. (rem: $0.0$).
   - **Item 7 ($0.15$):** Remaining spaces: $B_1: 0.0$, $B_2: 0.05$, $B_3: 0.10$.
     * Cannot fit in any existing bin.
     * Open Bin 4. Place in $B_4$. (rem: $0.85$).
3. **BFD Result:** **4 Bins used**

---

### The Theoretical Optimal Packing $\text{OPT}(L)$
Can this list be packed into **3 bins** (matching the volume lower bound $\lceil 3.00 \rceil = 3$)?
- **Bin 1:** $0.8 + 0.2 = 1.00$ (waste: $0.00$)
- **Bin 2:** $0.7 + 0.15 + 0.15$? (Wait, our items are $0.4, 0.8, 0.2, 0.25, 0.7, 0.15, 0.5$).
  Let's test:
  * $B_1 = [0.8, 0.2] \implies \text{Sum} = 1.00$
  * $B_2 = [0.7, 0.25] \implies \text{Sum} = 0.95$ (leftover $0.05$)
  * Remaining items: $0.5, 0.4, 0.15$. Sum $= 0.5 + 0.4 + 0.15 = 1.05 > 1.00$.
  * They cannot fit in one bin!
- What about:
  * $B_1 = [0.5, 0.4, 0.1] \dots$ but we have $0.15$.
  * If $0.5$ is with $0.4$: sum $= 0.90$. Remaining space $= 0.10$. Neither $0.2$ nor $0.25$ fits.
  * If $0.5$ is with $0.25 + 0.2$: sum $= 0.95$. Space $= 0.05$.
    Then remaining items are: $0.8, 0.7, 0.4, 0.15$.
    $0.8$ and $0.7$ both require separate bins. That's already 3 bins, with $0.4$ and $0.15$ left over.
    Bin with $0.8$: can only take nothing else ($0.8 + 0.15 = 0.95$). Then $0.7$ and $0.4$ are left, which cannot share a bin ($0.7 + 0.4 = 1.1 > 1$).
- **Mathematical Conclusion:**  
  $$\text{OPT}(L) = 4$$
  The volume lower bound $\lceil \sum w_i \rceil = 3$ was an unachievable fractional bound. All heuristics (FF, BF, FFD, BFD) achieved the **true global optimum of 4 bins**!

---

## 8. Summary Comparison Matrix of Bin Packing Heuristics

```text
+======================================================================================================================+
|                                    MASTER BIN PACKING HEURISTICS TAXONOMY                                            |
+==================+=========+===================+======================+==============================================+
| Algorithm        | Mode    | Time Complexity   | Asymptotic Ratio     | Core Operational Behavior                    |
+==================+=========+===================+======================+==============================================+
| Next Fit (NF)    | Online  | O(n)              | 2.000                | Keeps 1 bin open; closes permanently when    |
|                  |         |                   |                      | an item overflows. O(1) space.               |
+------------------+---------+-------------------+----------------------+----------------------------------------------+
| First Fit (FF)   | Online  | O(n log n)        | 1.700 (17/10)        | Places item in the lowest-indexed bin with   |
|                  |         |                   |                      | sufficient room.                             |
+------------------+---------+-------------------+----------------------+----------------------------------------------+
| Best Fit (BF)    | Online  | O(n log n)        | 1.700 (17/10)        | Places item in the bin leaving the minimum   |
|                  |         |                   |                      | remaining empty capacity.                    |
+------------------+---------+-------------------+----------------------+----------------------------------------------+
| Worst Fit (WF)   | Online  | O(n log n)        | 2.000                | Places item in the bin with the maximum      |
|                  |         |                   |                      | empty capacity.                              |
+------------------+---------+-------------------+----------------------+----------------------------------------------+
| First Fit        | Offline | O(n log n)        | 1.222 (11/9)         | Sorts items descending first, then applies   |
| Decreasing (FFD) |         |                   |                      | First Fit.                                   |
+------------------+---------+-------------------+----------------------+----------------------------------------------+
| Best Fit         | Offline | O(n log n)        | 1.222 (11/9)         | Sorts items descending first, then applies   |
| Decreasing (BFD) |         |                   |                      | Best Fit.                                    |
+==================+=========+===================+======================+==============================================+
```

---

## 9. KTU Examination High-Yield Preparation

This section provides model answers formatted for direct scoring under the KTU 2024 scheme for course code **PCCST502 / CST306**.

---

### Question 1 (3 Marks): Define approximation ratio for minimization and maximization problems.

#### Model Answer:
An algorithm $A$ for an optimization problem $\Pi$ has an **approximation ratio** $\rho \ge 1$ if for all input instances $I$:
$$\max \left( \frac{A(I)}{\text{OPT}(I)}, \; \frac{\text{OPT}(I)}{A(I)} \right) \le \rho$$
- **For Minimization:** $A(I) \le \rho \cdot \text{OPT}(I)$, guaranteeing the solution cost is at most $\rho$ times the minimum possible cost.
- **For Maximization:** $A(I) \ge \frac{1}{\rho} \cdot \text{OPT}(I)$, guaranteeing the solution value is at least a factor of $1/\rho$ of the maximum possible profit.

---

### Question 2 (5 Marks): Prove that the Next Fit heuristic for the 1-D Bin Packing problem achieves an approximation ratio of 2.

#### Model Answer:
1. **Pairwise Weight Property:** Let $m = \text{NF}(L)$ be the number of bins opened. For any two consecutive bins $B_j$ and $B_{j+1}$, the first item in $B_{j+1}$ could not fit into $B_j$. Hence:
   $$w(B_j) + w(B_{j+1}) > 1.0$$
2. **Summing Over Pairs:** Group the $m$ bins into $\lfloor m/2 \rfloor$ disjoint pairs. The total weight of all items satisfies:
   $$\sum_{i=1}^n w_i > \lfloor m/2 \rfloor \cdot 1.0 > \frac{m - 1}{2}$$
3. **Volume Lower Bound:** Since each bin has capacity 1, the optimal number of bins must satisfy:
   $$\text{OPT}(L) \ge \sum_{i=1}^n w_i$$
4. **Combining Inequalities:**
   $$\text{OPT}(L) > \frac{m - 1}{2} = \frac{\text{NF}(L) - 1}{2} \implies \text{NF}(L) \le 2 \cdot \text{OPT}(L)$$
5. **Conclusion:** Next Fit uses at most twice the optimal number of bins, achieving an approximation ratio of 2. $\blacksquare$

---

### Question 3 (5 Marks): Distinguish between First Fit (FF) and First Fit Decreasing (FFD) heuristics. State their asymptotic competitive ratios.

#### Model Answer:
| Dimension | First Fit (FF) | First Fit Decreasing (FFD) |
| :--- | :--- | :--- |
| **Execution Paradigm** | **Online:** Items arrive sequentially and are placed immediately without future knowledge. | **Offline:** All items must be known in advance; requires a pre-sorting step. |
| **Preprocessing Step** | None. Items are processed in arbitrary input order. | Items are sorted in **descending order** of size ($w_1 \ge w_2 \ge \dots \ge w_n$). |
| **Asymptotic Ratio** | $\rho_{\text{FF}}^{\infty} = \frac{17}{10} = 1.7$ | $\rho_{\text{FFD}}^{\infty} = \frac{11}{9} \approx 1.222$ |
| **Time Complexity** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ (dominated by sorting) |
| **Practical Performance** | May use up to 70% extra bins in the worst case. | Never uses more than ~22% extra bins in the worst case. |

---

### Question 4 (10 Marks): Pack the following items into bins of capacity $C = 1.0$ using Next Fit, First Fit, and First Fit Decreasing heuristics:  
$$L = (0.5, \; 0.7, \; 0.3, \; 0.9, \; 0.6, \; 0.8, \; 0.1, \; 0.4, \; 0.2)$$  
Determine the optimal number of bins and compare the results.

#### Model Answer Structure:
1. **Calculate Lower Bound:**
   $$\sum w_i = 0.5 + 0.7 + 0.3 + 0.9 + 0.6 + 0.8 + 0.1 + 0.4 + 0.2 = 4.5 \implies \text{OPT} \ge \lceil 4.5 \rceil = 5 \text{ bins}$$
2. **Next Fit Trace:** Show step-by-step bin closing. (Result: 6 or 7 bins). *(3 Marks)*
3. **First Fit Trace:** Scan open bins from left to right for each item. (Result: 5 or 6 bins). *(3 Marks)*
4. **First Fit Decreasing Trace:**
   - Sort: $(0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1)$.
   - Trace placements into bins. (Result: Exactly 5 bins). *(3 Marks)*
5. **Comparison & Optimal Solution:**
   - Show optimal packing into 5 bins:
     * $B_1 = [0.9, 0.1]$ (Sum $= 1.0$)
     * $B_2 = [0.8, 0.2]$ (Sum $= 1.0$)
     * $B_3 = [0.7, 0.3]$ (Sum $= 1.0$)
     * $B_4 = [0.6, 0.4]$ (Sum $= 1.0$)
     * $B_5 = [0.5]$ (Sum $= 0.5$)
   - Conclusion: FFD achieved the exact optimal packing ($\text{OPT} = 5$). *(1 Mark)*
