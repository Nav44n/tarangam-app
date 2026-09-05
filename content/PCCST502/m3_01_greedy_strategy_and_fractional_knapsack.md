# Module 3.1: The Greedy Strategy & The Fractional Knapsack Problem
**Course Code: PCCST502 | Design and Analysis of Algorithms | KTU 2024 Scheme**

---

### Table of Contents
1. [The Greedy Paradigm Control Abstraction](#the-greedy-paradigm)
   - [Optimization Problems: Feasible vs. Optimal Solutions](#feasible-vs-optimal)
   - [The General Greedy Template Algorithm](#general-greedy-template)
   - [Theoretical Pillars: Greedy-Choice Property & Optimal Substructure](#theoretical-pillars)
   - [The Exchange Argument (Cut-and-Paste Proof Technique)](#exchange-argument)
2. [The Fractional Knapsack Problem](#fractional-knapsack)
   - [Formal Mathematical Formulation](#mathematical-formulation)
   - [Evaluation of Three Competing Greedy Heuristics](#three-heuristics)
   - [Formal Optimality Proof via the Exchange Argument](#optimality-proof)
   - [Pseudocode & Detailed Algorithmic Implementation](#algorithm-implementation)
   - [Complexity Analysis (Time and Space)](#complexity-analysis)
   - [Step-by-Step Worked Numerical Trace (5W1H Methodology)](#numerical-trace)
3. [Critical Comparative Discussion: Fractional vs. 0/1 Knapsack](#fractional-vs-01)
   - [Why Greedy Succeeds for Fractional but Fails for 0/1](#why-greedy-fails-01)
   - [The 3-Item Concrete Counterexample](#counterexample-01)
   - [Side-by-Side Architectural Comparison Matrix](#comparison-matrix)
4. [KTU Exam High-Yield Summary](#exam-summary)
   - [Frequently Asked 3-Mark Questions & Model Solutions](#three-mark-questions)
   - [High-Frequency Student Pitfalls & Marking Scheme Traps](#student-pitfalls)

---

<a id="the-greedy-paradigm"></a>
## 1. The Greedy Paradigm Control Abstraction

The **Greedy Strategy** is an algorithmic paradigm designed to solve optimization problems by making a sequence of choices. At each decision point, the algorithm selects the alternative that appears best at that specific instant, according to a myopic, locally defined heuristic criterion. 

Unlike dynamic programming or backtracking, a standard greedy algorithm **never reconsiders its past choices**; once an element is accepted into or rejected from the solution set, that decision is irrevocable.

---

<a id="feasible-vs-optimal"></a>
### Optimization Problems: Feasible vs. Optimal Solutions

An optimization problem requires finding an input configuration that minimizes or maximizes an objective function subject to a collection of constraints.

```
                      PROBLEM INSTANCE DOMAIN (Ω)
  +---------------------------------------------------------------+
  |  All Possible Candidate Configurations                        |
  |                                                               |
  |         FEASIBLE REGION (S ⊆ Ω)                               |
  |    +-----------------------------------------------+          |
  |    |  Candidates satisfying all hard constraints   |          |
  |    |                                               |          |
  |    |               OPTIMAL SET (S* ⊆ S)            |          |
  |    |          +--------------------------+         |          |
  |    |          | Candidate(s) maximizing  |         |          |
  |    |          | or minimizing f(x)       |         |          |
  |    |          |                          |         |          |
  |    |          +--------------------------+         |          |
  |    +-----------------------------------------------+          |
  +---------------------------------------------------------------+
```

1. **Candidate Set ($\Omega$):** The universe of all possible structures or assignments constructible from the input data.
2. **Constraint Function ($C$):** A boolean predicate $C: \Omega \to \{0, 1\}$ defining whether a given candidate configuration adheres to all specified problem constraints.
3. **Feasible Solution Set ($S$):** The subset of candidate configurations that satisfy the constraints:
   $$S = \{ x \in \Omega \mid C(x) = 1 \}$$
4. **Objective Function ($f$):** A mapping $f: S \to \mathbb{R}$ that assigns a quantitative performance metric or cost to each feasible solution.
5. **Optimal Solution ($x^*$):** A feasible solution that attains the global extremum:
   $$\text{For a maximization problem: } x^* \in S \quad \text{such that} \quad \forall x \in S, \; f(x^*) \ge f(x)$$
   $$\text{For a minimization problem: } x^* \in S \quad \text{such that} \quad \forall x \in S, \; f(x^*) \le f(x)$$

::: callout-intuition The Difference Between Feasibility and Optimality
Imagine you must pack a suitcase for an airline flight with a strict maximum weight limit of $23\text{ kg}$.
* Packing just a single pair of socks weighs $0.05\text{ kg} \le 23\text{ kg}$. This is a **feasible solution**: it satisfies the flight constraint, but it is practically useless because the value of your packed luggage is near zero.
* Packing items of total weight $22.9\text{ kg}$ that maximize the monetary and practical value of your trip without exceeding $23\text{ kg}$ is an **optimal solution**.
* Packing items of total value $\$10,000$ that weigh $28\text{ kg}$ is an **infeasible candidate**: it violates the weight constraint and will be rejected at check-in.
:::

---

<a id="general-greedy-template"></a>
### The General Greedy Template Algorithm

The operational skeleton of any greedy algorithm can be formalized via the **Greedy Control Abstraction**. The algorithm proceeds in stages, processing an input array $A[1 \dots n]$ containing $n$ candidates.

```
                    THE GREEDY DECISION PIPELINE
                         Candidate Pool C
                                |
                                v
                       +-----------------+
                       |    Select()     | <--- Greedy Criterion (Heuristic)
                       +-----------------+
                                |
                                v Selected Item x
                       +-----------------+
                  NO   |  Feasible(S, x) |
            +--------> |    Check?       |
            |          +-----------------+
            |                   |
            | Discard           v YES
    [Next Candidate]   +-----------------+
            ^          |  Union(S, x)    | ---> Add to Solution Set S
            |          +-----------------+
            |                   |
            |                   v
            |          +-----------------+
            +--------- |  Solution(S)?   |
                  NO   |  Terminated?    |
                       +-----------------+
                                | YES
                                v
                         Final Solution S
```

```text
Algorithm Greedy(A, n)
// Input: An array A[1..n] containing n candidate elements.
// Output: A subset S of A that forms an optimal feasible solution.
begin
    S ← ∅;                           // Initialize solution set to empty
    for i ← 1 to n do
    begin
        x ← Select(A);               // Extract the locally best candidate by heuristic
        A ← A \ {x};                 // Remove x from the remaining candidate pool
        if Feasible(S, x) then       // Verify if adding x preserves constraint validity
        begin
            S ← Union(S, x);         // Commit x into the solution set
            if Solution(S) then      // Check if S has completely solved the problem
                return S;
        end;
    end;
    return S;
end;
```

#### Functions in the Control Abstraction:
* **`Select(A)`:** Extracts the best candidate according to a greedy criterion (e.g., maximum value, minimum weight, maximum ratio).
* **`Feasible(S, x)`:** Returns `true` if $S \cup \{x\}$ satisfies the hard problem constraints.
* **`Union(S, x)`:** Updates the solution state by committing item $x$.
* **`Solution(S)`:** A termination test determining whether a complete feasible solution has been attained.

---

<a id="theoretical-pillars"></a>
### Theoretical Pillars: Greedy-Choice Property & Optimal Substructure

A greedy algorithm does not guarantee an optimal solution for all optimization problems. A problem can be solved to global optimality by a greedy algorithm if and only if it exhibits two structural properties:

#### 1. The Greedy-Choice Property
A globally optimal solution can be arrived at by making locally optimal (greedy) choices without consulting future subproblems or backtracking to previous selections.
$$\text{Formally: } \exists \text{ an optimal solution } S^* \subseteq \Omega \quad \text{such that the first greedy choice } g_1 \in S^*$$

#### 2. Optimal Substructure
An optimal solution to the overall problem contains within it optimal solutions to its subproblems. If $S^*$ is an optimal solution to instance $I$, and we remove the greedy choice $g_1$ from $S^*$, then the remaining partial solution $S^* \setminus \{g_1\}$ must be an optimal solution to the reduced subproblem instance $I' = I \setminus \{g_1\}$.

---

<a id="exchange-argument"></a>
### The Exchange Argument (Cut-and-Paste Proof Technique)

The standard mathematical framework used to prove that a greedy algorithm yields a globally optimal solution is the **Exchange Argument** (also known as the Cut-and-Paste method).

```
                      THE EXCHANGE ARGUMENT METHODOLOGY
                      
 Arbitrary Optimal Solution O:   [ o_1 ]  [ o_2 ]  [ o_3 ] ... [ o_k ] ... [ o_n ]
                                    |        |        |           |           |
                                 Match    Match   Divergence   Replace     Match
                                    |        |        |           |           |
 Greedy Solution G:              [ g_1 ]  [ g_2 ]  [ g_3 ] ... [ g_k ] ... [ g_n ]
                                                      |
                                                      +---> Replace o_k with g_3
                                                            Show f(O') >= f(O)
```

#### Five-Step Proof Template:
1. **Hypothesis:** Let $G = \langle g_1, g_2, \dots, g_k \rangle$ be the ordered sequence of decisions generated by the greedy algorithm. Let $O = \langle o_1, o_2, \dots, o_m \rangle$ be an arbitrary globally optimal solution.
2. **Identification of Divergence:** Assume for contradiction (or progressive transformation) that $G \ne O$. Locate the first decision index $i$ where the greedy solution and the optimal solution disagree:
   $$g_1 = o_1, \quad g_2 = o_2, \quad \dots, \quad g_{i-1} = o_{i-1}, \quad \text{but} \quad g_i \ne o_i$$
3. **The Exchange:** Construct a new modified solution $O'$ by swapping out the non-greedy component from $O$ and splicing in the greedy choice $g_i$:
   $$O' = (O \setminus \{ \text{element from } O \}) \cup \{ g_i \}$$
4. **Feasibility Invariant:** Prove rigorously that the newly synthesized solution $O'$ violates none of the problem constraints ($C(O') = 1$).
5. **Non-Decreasing Optimality:** Prove algebraically that the objective value of the synthesized solution is at least as good as the original optimal solution:
   $$f(O') \ge f(O) \quad (\text{for maximization})$$
   Since $O$ was globally optimal, $f(O') \le f(O)$ is trivially bounded. Thus:
   $$f(O') = f(O)$$
   Repeating this exchange iteratively transforms $O$ into $G$ across all points of divergence without diminishing the objective value, concluding that $f(G) = f(O)$, meaning $G$ is itself optimal.

---

<a id="fractional-knapsack"></a>
## 2. The Fractional Knapsack Problem

<a id="mathematical-formulation"></a>
### Formal Mathematical Formulation

In the **Fractional Knapsack Problem**, a thief carries a knapsack with a maximum carrying weight capacity $W > 0$. There are $n$ distinct items available to steal. Each item $i$ possesses:
* A strictly positive value: $v_i > 0$
* A strictly positive weight: $w_i > 0$

Unlike the discrete 0/1 knapsack variant, items can be subdivided into arbitrary continuous fractions. Taking a fraction $x_i \in [0, 1]$ of item $i$ contributes a weight of $x_i \cdot w_i$ and a profit of $x_i \cdot v_i$.

$$\begin{aligned}
\text{Maximize} \quad & P(X) = \sum_{i=1}^n x_i v_i \\
\text{Subject to} \quad & \sum_{i=1}^n x_i w_i \le W \\
\text{Constraint} \quad & 0 \le x_i \le 1, \quad \forall i \in \{1, 2, \dots, n\}
\end{aligned}$$

Here, the candidate solution vector is $X = \langle x_1, x_2, \dots, x_n \rangle \in [0, 1]^n$.

---

<a id="three-heuristics"></a>
### Evaluation of Three Competing Greedy Heuristics

To design a greedy algorithm for the Fractional Knapsack Problem, we must establish a choice criterion (`Select()`). Three intuitive heuristics emerge:

```
+---------------------------------------------------------------------------------------+
| CANDIDATE HEURISTIC 1: Maximum Absolute Value (v_i)                                   |
| Selection Rule: Pick the item with the highest total value first.                     |
| Hypothesis: "High-value items yield maximum overall profit."                          |
+---------------------------------------------------------------------------------------+
| CANDIDATE HEURISTIC 2: Minimum Absolute Weight (w_i)                                  |
| Selection Rule: Pick the item with the smallest weight first.                         |
| Hypothesis: "Lightweight items conserve capacity, allowing more items to fit."        |
+---------------------------------------------------------------------------------------+
| CANDIDATE HEURISTIC 3: Maximum Value-to-Weight Ratio (r_i = v_i / w_i)                |
| Selection Rule: Pick the item offering the highest profit per unit weight.            |
| Hypothesis: "Maximizing density optimizes profit extraction per unit of capacity."    |
+---------------------------------------------------------------------------------------+
```

We now test these candidates with counterexamples to evaluate whether they yield optimal solutions.

---

#### Strategy 1: Greedy by Maximum Absolute Value ($v_i$)
* **Heuristic Rule:** Sort items such that $v_1 \ge v_2 \ge \dots \ge v_n$. Select items greedily in this order.

::: callout-warning Counterexample to Strategy 1
Let knapsack capacity $W = 50\text{ kg}$. The available items are:
* Item 1: $v_1 = 100$, $w_1 = 50\text{ kg}$
* Item 2: $v_2 = 80$, $w_2 = 20\text{ kg}$
* Item 3: $v_3 = 70$, $w_3 = 20\text{ kg}$

**Execution of Strategy 1:**
1. Sort items by value: $v_1 (100) > v_2 (80) > v_3 (70)$.
2. Pick Item 1: Takes $x_1 = 1.0$. Weight consumed $= 1.0 \times 50 = 50\text{ kg}$.
3. Remaining capacity $= 50 - 50 = 0\text{ kg}$.
4. Knapsack is full.
$$\text{Total Profit under Strategy 1} = 1.0 \times 100 = \mathbf{100}$$

**Alternative Feasible Solution:**
1. Pick Item 2: Takes $x_2 = 1.0$. Weight consumed $= 20\text{ kg}$. Value $= 80$. Remaining capacity $= 30\text{ kg}$.
2. Pick Item 3: Takes $x_3 = 1.0$. Weight consumed $= 20\text{ kg}$. Value $= 70$. Remaining capacity $= 10\text{ kg}$.
3. Pick Item 1 (fractional): Remaining capacity $= 10\text{ kg}$. Take fraction $x_1 = \frac{10}{50} = 0.2$. Weight consumed $= 10\text{ kg}$. Value $= 0.2 \times 100 = 20$.
$$\text{Total Profit of Alternative} = 80 + 70 + 20 = \mathbf{170}$$

**Conclusion:** Since $170 > 100$, Strategy 1 **fails to guarantee optimality**.
:::

---

#### Strategy 2: Greedy by Minimum Absolute Weight ($w_i$)
* **Heuristic Rule:** Sort items such that $w_1 \le w_2 \le \dots \le w_n$. Select items greedily in this order.

::: callout-warning Counterexample to Strategy 2
Let knapsack capacity $W = 10\text{ kg}$. The available items are:
* Item 1: $v_1 = 1$, $w_1 = 1\text{ kg}$
* Item 2: $v_2 = 100$, $w_2 = 10\text{ kg}$

**Execution of Strategy 2:**
1. Sort items by weight: $w_1 (1\text{ kg}) < w_2 (10\text{ kg})$.
2. Pick Item 1: Takes $x_1 = 1.0$. Weight consumed $= 1\text{ kg}$. Value $= 1$. Remaining capacity $= 10 - 1 = 9\text{ kg}$.
3. Pick Item 2 (fractional): Capacity allows $9\text{ kg}$. Take fraction $x_2 = \frac{9}{10} = 0.9$. Weight consumed $= 9\text{ kg}$. Value $= 0.9 \times 100 = 90$.
$$\text{Total Profit under Strategy 2} = 1 + 90 = \mathbf{91}$$

**Alternative Feasible Solution:**
1. Pick Item 2 entirely: Take fraction $x_2 = 1.0$. Weight consumed $= 10\text{ kg}$. Value $= 100$. Remaining capacity $= 0\text{ kg}$.
$$\text{Total Profit of Alternative} = \mathbf{100}$$

**Conclusion:** Since $100 > 91$, Strategy 2 **fails to guarantee optimality**.
:::

---

#### Strategy 3: Greedy by Value-to-Weight Ratio ($r_i = \frac{v_i}{w_i}$)
* **Heuristic Rule:** Define the density $r_i = \frac{v_i}{w_i}$. Sort items in non-increasing order of ratios:
  $$\frac{v_1}{w_1} \ge \frac{v_2}{w_2} \ge \dots \ge \frac{v_n}{w_n}$$
* Pack items with the highest density first. When capacity is insufficient to absorb an entire item, take the exact fraction required to fill the knapsack to capacity $W$.

We will now prove that this strategy is mathematically guaranteed to find an optimal solution.

---

<a id="optimality-proof"></a>
### Formal Optimality Proof via the Exchange Argument

#### Theorem:
The greedy strategy based on sorting items by non-increasing value-to-weight ratio $r_i = \frac{v_i}{w_i}$ produces an optimal solution to the Fractional Knapsack Problem.

#### Mathematical Proof:
Let the $n$ items be indexed such that their densities satisfy:
$$r_1 \ge r_2 \ge \dots \ge r_n, \quad \text{where } r_i = \frac{v_i}{w_i}$$

Let $G = \langle g_1, g_2, \dots, g_n \rangle$ be the solution vector generated by the greedy algorithm. 
* If $\sum_{i=1}^n w_i \le W$, the knapsack can take all items ($g_i = 1, \forall i$). This is trivially optimal.
* Otherwise, the greedy algorithm fills items completely up to some critical index $k$, takes a fractional amount of item $k$, and sets all subsequent items to zero:
  $$g_i = 1 \quad \text{for } 1 \le i < k$$
  $$g_k = \frac{W - \sum_{i=1}^{k-1} w_i}{w_k} \in (0, 1)$$
  $$g_i = 0 \quad \text{for } k < i \le n$$

Note that under this greedy schedule, the knapsack is filled to capacity:
$$\sum_{i=1}^n g_i w_i = W$$

Now, let $O = \langle o_1, o_2, \dots, o_n \rangle$ be an arbitrary optimal solution vector. By definition of feasibility:
$$\sum_{i=1}^n o_i w_i \le W, \quad \text{and} \quad 0 \le o_i \le 1 \quad \forall i$$

We assume $O \ne G$. Since both solutions differ, there must exist at least one index where $g_i \ne o_i$. Let $k$ be the **first index** at which the vectors differ:
$$g_1 = o_1, \quad g_2 = o_2, \quad \dots, \quad g_{k-1} = o_{k-1}, \quad \text{and} \quad g_k \ne o_k$$

```
                           ARRAY DIVERGENCE PROFILE
 Index i:      1       2              k-1           k              k+1            n
 G:         [ 1.0 ] [ 1.0 ]  ...    [ 1.0 ]     [ g_k > o_k ]    [  0.0  ] ... [  0.0  ]
               |       |               |              |                 
             Equal   Equal           Equal        Difference            
               |       |               |              |                 
 O:         [ 1.0 ] [ 1.0 ]  ...    [ 1.0 ]     [    o_k    ]    [  o_j  ] ... [  o_n  ]
                                                      ^                 ^
                                                      |                 |
                                                 Greedy has        Optimal has
                                                 more of this      remnants here
```

By construction of the greedy algorithm:
* For indices $i < k$, $g_i = 1$, so $o_i$ must also equal $1$ (since $g_i = o_i$).
* At index $k$, $g_k$ was chosen to be as large as possible given the remaining capacity. Because $g_i = o_i$ for all $i < k$, the remaining capacity available to both algorithms before item $k$ was identical.
* Therefore, the optimal solution cannot take strictly more of item $k$ than greedy without exceeding capacity. Thus, it must be that:
  $$g_k > o_k \implies (g_k - o_k) > 0$$

Now examine the capacity utilization. Since $G$ completely exhausts the capacity ($W$), and $O$ has strictly less of item $k$ than $G$, there must exist some subsequent item $j > k$ such that:
$$o_j > g_j$$
*(If no such $j$ existed, then $\sum o_i w_i < \sum g_i w_i = W$, and we could increase $o_k$ to improve $P(O)$, contradicting the optimality of $O$.)*

Because $j > k$, and our items are sorted in non-increasing ratio order:
$$r_k = \frac{v_k}{w_k} \ge \frac{v_j}{w_j} = r_j \implies r_k - r_j \ge 0$$

We construct a new solution $O'$ by performing an exchange. We increase the amount of item $k$ in $O$ by an amount $\Delta x_k > 0$ and decrease the amount of item $j$ by an amount $\Delta x_j > 0$ such that the **net change in weight is zero**:
$$\Delta w = \Delta x_k \cdot w_k = \Delta x_j \cdot w_j = \min \left\{ (g_k - o_k) w_k, \; o_j w_j \right\}$$

Set:
$$o'_k = o_k + \frac{\Delta w}{w_k}$$
$$o'_j = o_j - \frac{\Delta w}{w_j}$$
$$o'_i = o_i \quad \forall i \notin \{k, j\}$$

#### 1. Feasibility of $O'$:
The total weight of $O'$ is:
$$\sum_{i=1}^n o'_i w_i = \sum_{i \ne k, j} o_i w_i + \left( o_k + \frac{\Delta w}{w_k} \right) w_k + \left( o_j - \frac{\Delta w}{w_j} \right) w_j$$
$$\sum_{i=1}^n o'_i w_i = \sum_{i=1}^n o_i w_i + \Delta w - \Delta w = \sum_{i=1}^n o_i w_i \le W$$
The bounds on the variables hold because $\Delta w$ was bounded by $(g_k - o_k)w_k$ and $o_j w_j$. Hence, $0 \le o'_i \le 1$ for all $i$. $O'$ is feasible.

#### 2. Profit of $O'$ relative to $O$:
$$\begin{aligned}
P(O') - P(O) &= \left( o'_k v_k + o'_j v_j \right) - \left( o_k v_k + o_j v_j \right) \\
&= \left( \frac{\Delta w}{w_k} \right) v_k - \left( \frac{\Delta w}{w_j} \right) v_j \\
&= \Delta w \cdot \left( \frac{v_k}{w_k} - \frac{v_j}{w_j} \right) \\
&= \Delta w \cdot \left( r_k - r_j \right)
\end{aligned}$$

Because $\Delta w > 0$ and $r_k \ge r_j$, we have:
$$P(O') - P(O) = \Delta w \cdot (r_k - r_j) \ge 0 \implies P(O') \ge P(O)$$

Since $O$ was assumed to be globally optimal, $P(O') \le P(O)$ must also hold. Therefore:
$$P(O') = P(O)$$

The newly constructed solution $O'$ is equally optimal, but its difference from the greedy solution $G$ has been reduced (either $o'_k = g_k$ or $o'_j = 0$). 

By repeating this exchange at most $n$ times, we systematically transform the optimal solution $O$ into the greedy solution $G$ without altering the total profit:
$$P(G) = P(O)$$
Thus, the greedy algorithm produces a globally optimal solution. $\blacksquare$

---

<a id="algorithm-implementation"></a>
### Pseudocode & Detailed Algorithmic Implementation

```text
Algorithm FractionalKnapsack(V, W_arr, W, n)
// Input:
//   V[1..n]: Array of positive values
//   W_arr[1..n]: Array of positive weights
//   W: Total knapsack capacity (scalar, W > 0)
//   n: Number of items (integer, n >= 1)
// Output:
//   X[1..n]: Fraction array where X[i] represents the portion of item i taken
//   totalProfit: Total value of the packed knapsack
begin
    // Step 1: Structure creation and ratio computation
    for i ← 1 to n do
    begin
        Item[i].id ← i;
        Item[i].value ← V[i];
        Item[i].weight ← W_arr[i];
        Item[i].ratio ← V[i] / W_arr[i];
        X[i] ← 0.0;                  // Initialize all fractions to 0
    end;

    // Step 2: Sort items in non-increasing order of value-to-weight ratio
    // Uses MergeSort or QuickSort: O(n log n)
    SortDescendingByRatio(Item, 1, n);

    currentWeight ← 0.0;
    totalProfit ← 0.0;

    // Step 3: Greedy selection loop
    for i ← 1 to n do
    begin
        if currentWeight + Item[i].weight ≤ W then
        begin
            // Case A: Item can be absorbed completely
            X[Item[i].id] ← 1.0;
            currentWeight ← currentWeight + Item[i].weight;
            totalProfit ← totalProfit + Item[i].value;
        end
        else
        begin
            // Case B: Item can only be partially absorbed; fill remaining space
            remainingCapacity ← W - currentWeight;
            fraction ← remainingCapacity / Item[i].weight;
            
            X[Item[i].id] ← fraction;
            totalProfit ← totalProfit + (fraction * Item[i].value);
            currentWeight ← W;       // Knapsack is now fully packed
            
            break;                   // Irrevocably terminate loop
        end;
    end;

    return (X, totalProfit);
end;
```

---

<a id="complexity-analysis"></a>
### Complexity Analysis

```
                    TIME AND SPACE RESOURCE BREAKDOWN
+------------------------------+--------------------+------------------------+
| Algorithm Phase              | Time Complexity    | Space Complexity       |
+------------------------------+--------------------+------------------------+
| 1. Ratio Computation Array   | Θ(n)               | Θ(n) [Struct Array]    |
| 2. Sorting by Ratio          | O(n log n)         | O(log n) to O(n)       |
| 3. Greedy Selection Loop     | O(n)               | O(1)                   |
| 4. Output Generation         | Θ(n)               | Θ(n) [Solution Vector] |
+------------------------------+--------------------+------------------------+
| TOTAL BOUNDS                 | O(n log n)         | O(n)                   |
+------------------------------+--------------------+------------------------+
```

#### Detailed Derivations:

1. **Time Complexity:**
   * **Ratio Computation:** Iterates over $n$ items, performing one division per item:
     $$T_{\text{ratio}}(n) = \sum_{i=1}^n c_1 = c_1 \cdot n = \Theta(n)$$
   * **Sorting:** Sorting $n$ structures using an optimal comparison sort (Merge Sort or Heap Sort) requires:
     $$T_{\text{sort}}(n) = \Theta(n \log n)$$
   * **Greedy Selection Loop:** The loop executes at most $n$ iterations. Each iteration performs constant-time operations: checking an inequality, arithmetic additions, and at most one division (in the `else` branch, which triggers `break`):
     $$T_{\text{loop}}(n) = \sum_{i=1}^k c_2 \le c_2 \cdot n = O(n) \quad (\text{where } k \le n)$$
   * **Total Time:**
     $$T(n) = T_{\text{ratio}}(n) + T_{\text{sort}}(n) + T_{\text{loop}}(n) = \Theta(n) + \Theta(n \log n) + O(n) = \mathbf{O(n \log n)}$$

::: callout-exam Advanced Note for High Marks: Linear Time Variant
If an examiner asks: *"Can Fractional Knapsack be solved in $O(n)$ worst-case time?"* 
**Yes.** Using the **Prune-and-Search** algorithm based on the **Median-of-Medians (Quickselect)** algorithm:
1. Find the median of ratios in $O(n)$ time.
2. Partition items into two sets: $L$ (ratios $>$ median) and $R$ (ratios $<$ median).
3. Compute total weight of $L$, $W_L$:
   * If $W_L \le W$, pack all of $L$, set $W \leftarrow W - W_L$, and recurse on $R$.
   * If $W_L > W$, discard $R$ entirely and recurse on $L$.
The recurrence relation is $T(n) = T(n/2) + O(n)$, which solves to **$O(n)$**.
*(Standard university answers typically expect the $O(n \log n)$ sort-based method unless $O(n)$ is explicitly requested).*
:::

2. **Space Complexity:**
   * An auxiliary structure array of size $n$ is allocated to store values, weights, indices, and ratios: $\Theta(n)$.
   * An output array $X[1 \dots n]$ requires $\Theta(n)$ space.
   * If sorting is performed in-place on existing arrays, auxiliary space is $O(1)$ (or $O(\log n)$ call stack space for sorting). 
   * **Overall Auxiliary Space Complexity:** $\mathbf{O(n)}$ (or $\mathbf{O(1)}$ if modifying inputs in-place).

---

<a id="numerical-trace"></a>
### Step-by-Step Worked Numerical Trace (5W1H Methodology)

We trace the algorithm step by step on a complete numerical instance.

#### Problem Instance:
* Total Knapsack Capacity: $W = 60\text{ kg}$
* Number of Items: $n = 5$
* Values: $V = \langle 120, 100, 60, 100, 40 \rangle$
* Weights: $W_{\text{arr}} = \langle 30, 20, 10, 40, 20 \rangle$

---

#### Phase 1: Ratio Computation and Tabulation

<div class="table-wrap">

| Original Item ($i$) | Value ($v_i$) | Weight ($w_i$) | Density / Ratio ($r_i = \frac{v_i}{w_i}$) |
| :---: | :---: | :---: | :---: |
| **$I_1$** | $120$ | $30\text{ kg}$ | $\frac{120}{30} = 4.00$ |
| **$I_2$** | $100$ | $20\text{ kg}$ | $\frac{100}{20} = 5.00$ |
| **$I_3$** | $60$ | $10\text{ kg}$ | $\frac{60}{10} = 6.00$ |
| **$I_4$** | $100$ | $40\text{ kg}$ | $\frac{100}{40} = 2.50$ |
| **$I_5$** | $40$ | $20\text{ kg}$ | $\frac{40}{20} = 2.00$ |

</div>

---

#### Phase 2: Ordering by Ratio in Non-Increasing Order
Sort descending by $r_i$:
$$r_3 (6.00) > r_2 (5.00) > r_1 (4.00) > r_4 (2.50) > r_5 (2.00)$$

The processing queue order is: **$\langle I_3, I_2, I_1, I_4, I_5 \rangle$**.

<div class="table-wrap">

| Sorted Rank ($k$) | Item Tag | Value ($v$) | Weight ($w$) | Ratio ($r$) |
| :---: | :---: | :---: | :---: | :---: |
| **1** | $I_3$ | $60$ | $10\text{ kg}$ | $6.00$ |
| **2** | $I_2$ | $100$ | $20\text{ kg}$ | $5.00$ |
| **3** | $I_1$ | $120$ | $30\text{ kg}$ | $4.00$ |
| **4** | $I_4$ | $100$ | $40\text{ kg}$ | $2.50$ |
| **5** | $I_5$ | $40$ | $20\text{ kg}$ | $2.00$ |

</div>

---

#### Phase 3: The 5W1H Stepped Execution Trace

```
                      EXECUTION PROGRESSION TIMELINE
  Capacity W = 60
  
  Iter 1: Take I_3 (10 kg) ----> Rem: 50 kg | Value: 60
  Iter 2: Take I_2 (20 kg) ----> Rem: 30 kg | Value: 60 + 100 = 160
  Iter 3: Take I_1 (30 kg) ----> Rem:  0 kg | Value: 160 + 120 = 280 (FULL!)
  Iter 4: Skip I_4 ( 0 kg) ----> Rem:  0 kg | Value: 280
  Iter 5: Skip I_5 ( 0 kg) ----> Rem:  0 kg | Value: 280
```

---

##### Iteration 1: Processing Item $I_3$
* **What are we doing?** Evaluating item $I_3$ for knapsack inclusion.
* **Why are we starting here?** $I_3$ has the globally maximal ratio ($r_3 = 6.00$); it delivers the highest profit per unit weight.
* **Where did this formula originate?** The condition `currentWeight + Item[i].weight <= W`.
* **How do we execute the step mechanically?**
  $$\text{currentWeight} = 0\text{ kg}$$
  $$\text{candidateWeight} = 0 + 10 = 10\text{ kg} \le 60\text{ kg} \implies \text{Condition Holds}$$
  $$x_3 = 1.0$$
  $$\text{currentWeight} = 0 + 10 = 10\text{ kg}$$
  $$\text{totalProfit} = 0 + 60 = 60$$
* **What changed from previous state?** $x_3$ set to $1.0$, remaining capacity decreased from $60\text{ kg}$ to $50\text{ kg}$, total profit increased from $0$ to $60$.

---

##### Iteration 2: Processing Item $I_2$
* **What are we doing?** Evaluating item $I_2$ for knapsack inclusion.
* **Why are we starting here?** $I_2$ has the next highest ratio ($r_2 = 5.00$) among all remaining items.
* **Where did this formula originate?** Feasibility condition `currentWeight + Item[i].weight <= W`.
* **How do we execute the step mechanically?**
  $$\text{currentWeight} = 10\text{ kg}$$
  $$\text{candidateWeight} = 10 + 20 = 30\text{ kg} \le 60\text{ kg} \implies \text{Condition Holds}$$
  $$x_2 = 1.0$$
  $$\text{currentWeight} = 10 + 20 = 30\text{ kg}$$
  $$\text{totalProfit} = 60 + 100 = 160$$
* **What changed from previous state?** $x_2$ set to $1.0$, remaining capacity decreased from $50\text{ kg}$ to $30\text{ kg}$, total profit increased from $60$ to $160$.

---

##### Iteration 3: Processing Item $I_1$
* **What are we doing?** Evaluating item $I_1$ for knapsack inclusion.
* **Why are we starting here?** $I_1$ has the next highest ratio ($r_1 = 4.00$).
* **Where did this formula originate?** Feasibility condition `currentWeight + Item[i].weight <= W`.
* **How do we execute the step mechanically?**
  $$\text{currentWeight} = 30\text{ kg}$$
  $$\text{candidateWeight} = 30 + 30 = 60\text{ kg} \le 60\text{ kg} \implies \text{Condition Holds Exactly}$$
  $$x_1 = 1.0$$
  $$\text{currentWeight} = 30 + 30 = 60\text{ kg}$$
  $$\text{totalProfit} = 160 + 120 = 280$$
* **What changed from previous state?** $x_1$ set to $1.0$, remaining capacity decreased from $30\text{ kg}$ to $0\text{ kg}$, total profit increased from $160$ to $280$. Knapsack capacity is fully exhausted.

---

##### Iteration 4: Processing Item $I_4$
* **What are we doing?** Evaluating item $I_4$ for knapsack inclusion.
* **Why are we starting here?** Next element in sorted priority order ($r_4 = 2.50$).
* **Where did this formula originate?** Check `currentWeight + Item[i].weight <= W`.
* **How do we execute the step mechanically?**
  $$\text{candidateWeight} = 60 + 40 = 100\text{ kg} > 60\text{ kg} \implies \text{Branch to Else}$$
  $$\text{remainingCapacity} = W - \text{currentWeight} = 60 - 60 = 0\text{ kg}$$
  $$\text{fraction} = \frac{\text{remainingCapacity}}{w_4} = \frac{0}{40} = 0.0$$
  $$x_4 = 0.0$$
  $$\text{Execute 'break' statement. Algorithm terminates.}$$
* **What changed from previous state?** Algorithm halted; subsequent elements ($I_5$) implicitly receive $x_5 = 0.0$.

---

#### Consolidated Iteration Tracking Matrix

<div class="table-wrap">

| Iteration | Item Examined | Weight ($w_i$) | Value ($v_i$) | Ratio ($r_i$) | Fraction Taken ($x_i$) | Weight Added | Remaining Capacity ($W'$) | Cumulative Profit |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | *Init* | - | - | - | All $x_i = 0$ | $0\text{ kg}$ | $60\text{ kg}$ | $0$ |
| **1** | $I_3$ | $10$ | $60$ | $6.00$ | $x_3 = 1.0$ | $10\text{ kg}$ | $50\text{ kg}$ | $60$ |
| **2** | $I_2$ | $20$ | $100$ | $5.00$ | $x_2 = 1.0$ | $20\text{ kg}$ | $30\text{ kg}$ | $160$ |
| **3** | $I_1$ | $30$ | $120$ | $4.00$ | $x_1 = 1.0$ | $30\text{ kg}$ | $0\text{ kg}$ | $\mathbf{280}$ |
| **4** | $I_4$ | $40$ | $100$ | $2.50$ | $x_4 = 0.0$ | $0\text{ kg}$ | $0\text{ kg}$ | $280$ |
| **5** | $I_5$ | $20$ | $40$ | $2.00$ | $x_5 = 0.0$ | $0\text{ kg}$ | $0\text{ kg}$ | $280$ |

</div>

#### Final Solution Vector:
$$X = \langle x_1, x_2, x_3, x_4, x_5 \rangle = \mathbf{\langle 1.0, \; 1.0, \; 1.0, \; 0.0, \; 0.0 \rangle}$$
$$\text{Total Maximum Profit} = \mathbf{280}$$
$$\text{Total Weight Consumed} = 30(1.0) + 20(1.0) + 10(1.0) + 40(0.0) + 20(0.0) = \mathbf{60\text{ kg}}$$

---

<a id="fractional-vs-01"></a>
## 3. Critical Comparative Discussion: Fractional vs. 0/1 Knapsack

The distinction between the **Fractional Knapsack** and the **0/1 Knapsack** problem illustrates the boundaries of the greedy paradigm.

```
                  FRACTIONAL vs. 0/1 DECISION DOMAIN
                  
 Fractional Item:  [========================]  <--- Can take ANY slice x_i in [0, 1]
                   0%                      100%
                   
 0/1 Item:         [        LEAVE         ]  OR  [        TAKE         ]
                            x_i = 0                      x_i = 1
```

* **Fractional Knapsack:** $x_i \in [0, 1]$. Items can be cut into pieces. Solvable to global optimality via the Greedy strategy in $O(n \log n)$ time.
* **0/1 Knapsack:** $x_i \in \{0, 1\}$. Items are indivisible. The greedy strategy fails; solving it to optimality requires **Dynamic Programming** or **Branch-and-Bound** in $O(n \cdot W)$ pseudo-polynomial time (it is an **NP-Hard** problem).

---

<a id="why-greedy-fails-01"></a>
### Why Greedy Succeeds for Fractional but Fails for 0/1

The success of the greedy ratio strategy on Fractional Knapsack relies on the ability to take a **continuous fraction** of an item to exhaust knapsack capacity.

In the 0/1 Knapsack problem, choosing an item with a high value-to-weight ratio may leave **unfillable empty space** in the knapsack. The profit lost due to this unused space can exceed the marginal gain achieved by picking high-density items, causing the greedy strategy to miss the optimal combination.

---

<a id="counterexample-01"></a>
### The 3-Item Concrete Counterexample

Let knapsack capacity $W = 50\text{ kg}$, with $n = 3$ items:

<div class="table-wrap">

| Item | Value ($v_i$) | Weight ($w_i$) | Density / Ratio ($r_i = \frac{v_i}{w_i}$) |
| :---: | :---: | :---: | :---: |
| **$I_1$** | $60$ | $10\text{ kg}$ | $6.00$ |
| **$I_2$** | $100$ | $20\text{ kg}$ | $5.00$ |
| **$I_3$** | $120$ | $30\text{ kg}$ | $4.00$ |

</div>

```
                       KNAPSACK PACKING OUTCOMES
 Capacity = 50 kg
 
 1. Greedy Choice for 0/1:
 +--------------------+------------------------+-----------------------------+
 |  Item 1 (10 kg)    |    Item 2 (20 kg)      |    EMPTY WASTED SPACE       |
 |  Value = 60        |    Value = 100         |    20 kg left (Val = 0)     |
 +--------------------+------------------------+-----------------------------+
 Total Value = 160
 
 2. Optimal Choice for 0/1:
 +-----------------------------+---------------------------------------------+
 |      Item 2 (20 kg)         |               Item 3 (30 kg)                |
 |      Value = 100            |               Value = 120                   |
 +-----------------------------+---------------------------------------------+
 Total Value = 220  <--- +60 higher than Greedy!
 
 3. Greedy Choice for Fractional:
 +--------------------+------------------------+-----------------------------+
 |  Item 1 (10 kg)    |    Item 2 (20 kg)      |  2/3 of Item 3 (20 kg)      |
 |  Value = 60        |    Value = 100         |  Value = 2/3 * 120 = 80     |
 +--------------------+------------------------+-----------------------------+
 Total Value = 240
```

#### Step-by-Step Mathematical Comparison:

##### 1. Greedy Strategy on 0/1 Knapsack Instance:
* The greedy algorithm sorts by ratio: $I_1 (6.00) > I_2 (5.00) > I_3 (4.00)$.
* **Step 1:** Select $I_1$ ($w_1 = 10 \le 50$). Commit $x_1 = 1$. Remaining capacity $= 50 - 10 = 40\text{ kg}$. Accumulated Profit $= 60$.
* **Step 2:** Select $I_2$ ($w_2 = 20 \le 40$). Commit $x_2 = 1$. Remaining capacity $= 40 - 20 = 20\text{ kg}$. Accumulated Profit $= 60 + 100 = 160$.
* **Step 3:** Select $I_3$ ($w_3 = 30$). Test feasibility: $w_3 = 30 > 20\text{ kg}$. 
  * Because fractions are forbidden ($x_3 \in \{0, 1\}$), **Item 3 is completely rejected ($x_3 = 0$)**.
* Final Greedy 0/1 Solution: $X_{\text{greedy}} = \langle 1, 1, 0 \rangle$.
  $$\text{Total Weight} = 10 + 20 = 30\text{ kg} \quad (\mathbf{20\text{ kg wasted capacity}})$$
  $$\text{Total Profit} = 60 + 100 = \mathbf{160}$$

##### 2. Globally Optimal 0/1 Knapsack Solution:
* Select $I_2$ and $I_3$:
  $$X_{\text{optimal}} = \langle 0, 1, 1 \rangle$$
  $$\text{Total Weight} = 20 + 30 = 50\text{ kg} \quad (\text{Perfect capacity utilization})$$
  $$\text{Total Profit} = 100 + 120 = \mathbf{220}$$
* **Comparison:** $220 > 160$. The greedy strategy leaves a $20\text{ kg}$ void that it cannot fill, sacrificing $60$ units of potential profit.

##### 3. Contrast with the Fractional Variant:
If fractions are allowed on this same instance:
* The greedy algorithm takes all of $I_1$ ($10\text{ kg}$, value $60$), all of $I_2$ ($20\text{ kg}$, value $100$), and fills the remaining $20\text{ kg}$ with a fraction of $I_3$:
  $$x_3 = \frac{20}{30} = \frac{2}{3}$$
  $$\text{Profit contributed by } I_3 = \frac{2}{3} \times 120 = 80$$
  $$\text{Total Fractional Profit} = 60 + 100 + 80 = \mathbf{240}$$
The fractional capability eliminates the empty space penalty entirely.

---

<a id="comparison-matrix"></a>
### Side-by-Side Architectural Comparison Matrix

<div class="table-wrap">

| Dimension | Fractional Knapsack Problem | 0/1 Knapsack Problem |
| :--- | :--- | :--- |
| **Mathematical Domain** | $x_i \in [0, 1] \subset \mathbb{R}$ (Continuous) | $x_i \in \{0, 1\}$ (Discrete / Binary) |
| **Optimal Algorithmic Paradigm** | **Greedy Strategy** | **Dynamic Programming** / Branch & Bound |
| **Item Divisibility** | Divisible (liquids, grains, fabrics) | Indivisible (laptops, ingots, machinery) |
| **Greedy Choice Property** | **Holds strictly** (Ratio metric $v_i/w_i$) | **Fails** (May leave unfillable capacity) |
| **Optimal Substructure** | Holds | Holds |
| **Worst-Case Time Complexity** | $O(n \log n)$ (Sort-based) or $O(n)$ (Selection) | $O(n \cdot W)$ (DP) or $O(2^n)$ (Brute force) |
| **Computational Complexity Class** | $\mathbf{P}$ (Tractable, polynomial time) | **NP-Hard** (Weakly NP-complete) |
| **Space Complexity** | $O(1)$ auxiliary beyond input | $O(n \cdot W)$ or $O(W)$ auxiliary space |
| **Capacity Utilization** | Knapsack is always $100\%$ filled (if $\sum w_i \ge W$) | May leave empty, unusable slack capacity |

</div>

---

<a id="exam-summary"></a>
## 4. KTU Exam High-Yield Summary

<a id="three-mark-questions"></a>
### Frequently Asked 3-Mark Questions & Model Solutions

#### Q1: Define the Greedy-Choice Property and Optimal Substructure.
**Model Answer:**
* **Greedy-Choice Property:** A global optimum can be attained by making a series of locally optimal, irrevocable choices without examining future subproblems or backtracking.
* **Optimal Substructure:** A problem exhibits optimal substructure if an optimal solution to the problem contains optimal solutions to its subproblems ($S^* = \{g\} \cup S^{*}_{\text{sub}}$).

---

#### Q2: Distinguish between Feasible Solutions and Optimal Solutions with an example.
**Model Answer:**
* A **Feasible Solution** is any configuration that satisfies all problem constraints.
* An **Optimal Solution** is a feasible solution that achieves the maximum or minimum possible value of the objective function.
* *Example:* For a Knapsack with capacity $W = 10\text{ kg}$ and items $I_1(w=2, v=10)$ and $I_2(w=8, v=50)$, packing just $I_1$ is **feasible** ($2\text{ kg} \le 10\text{ kg}$, value $= 10$). Packing both $I_1$ and $I_2$ is **optimal** ($10\text{ kg} \le 10\text{ kg}$, value $= 60$).

---

#### Q3: State why the Greedy algorithm fails for the 0/1 Knapsack problem.
**Model Answer:**
In the 0/1 Knapsack problem, items are indivisible ($x_i \in \{0, 1\}$). A greedy choice based on value-to-weight ratio can leave empty capacity that cannot be filled by remaining items. The lost capacity often causes the greedy solution to fall short of combinations that fill the knapsack more effectively.

---

<a id="student-pitfalls"></a>
### High-Frequency Student Pitfalls & Marking Scheme Traps

::: callout-exam Exam Traps & Avoidance Strategies
1. **The Divisibility Trap:**
   * *The Error:* Attempting to take a fractional item in a problem labeled "0/1 Knapsack", or failing to take a fractional item at the boundary of a "Fractional Knapsack" problem.
   * *The Fix:* Always inspect the problem header:
     $$\text{Fractional} \implies x_k = \frac{\text{Remaining Capacity}}{w_k} \in [0, 1]$$
     $$0/1 \implies x_k \in \{0, 1\} \text{ only!}$$

2. **The Sorting Forgetting Slip:**
   * *The Error:* Applying the while-loop sequentially across the input items without sorting them by ratio $r_i = \frac{v_i}{w_i}$ first.
   * *The Fix:* Step 1 of your answer must always explicitly compute ratios, and Step 2 must show the sorted sequence before any packing occurs.

3. **Fractional Value Computation Arithmetic Error:**
   * *The Error:* Computing the fractional value contribution as $x_i \cdot w_i$ instead of $x_i \cdot v_i$.
   * *The Fix:* Weight tracks capacity ($x_i \cdot w_i$); value tracks profit ($x_i \cdot v_i$). Write them in separate columns in your trace table to avoid mixing them up.

4. **Off-by-One Capacity Subtraction:**
   * *The Error:* Forgetting to subtract the weight of completely packed items from the remaining capacity before calculating the fractional slice for the final item.
   * *The Fix:* Maintain a dedicated $W'$ (Remaining Capacity) column that updates at every single iteration.
:::
