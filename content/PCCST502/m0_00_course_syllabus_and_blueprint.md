# KTU Official Syllabus: Design and Analysis of Algorithms (PCCST502)

Welcome to the comprehensive academic and examination blueprint for **Design and Analysis of Algorithms (PCCST502)**, prescribed under the **APJ Abdul Kalam Technological University (KTU) 2024 Scheme for Semester 5 (S5) Computer Science and allied engineering branches**.

---

## 📋 Course Overview

<div class="table-wrap">

| Parameter | Specification Details |
| :--- | :--- |
| **Course Name** | **Design and Analysis of Algorithms** |
| **Course Code** | `PCCST502` |
| **Semester** | **Semester 5 (S5)** |
| **Degree & Branch** | **B.Tech (Common to CS / CD / CM / AM / CB / CN / CU / CG)** |
| **Teaching Hours / Week** | **3:1:0:0** *(Lecture: 3 hrs, Tutorial: 1 hr, Practical: 0, Remedial: 0)* |
| **Total Contact Hours** | **44 Contact Hours (11 Hours / Module)** |
| **Course Credits** | **4 Credits** |
| **Course Type** | **Theory** |
| **Prerequisites** | `PCCST303` *(Data Structures)* |
| **Continuous Internal Evaluation (CIE)** | **40 Marks** *(Min. 45% / 18 marks required for ESE eligibility)* |
| **End Semester Examination (ESE)** | **60 Marks** *(Min. 40% / 24 marks required to pass)* |
| **Total Marks** | **100 Marks** |
| **Examination Duration** | **2 Hours 30 Minutes (150 Minutes)** |

</div>

::: callout-intuition Why Design and Analysis of Algorithms is the Engine of Computing
While Data Structures teaches you how to organize information in memory, Algorithm Design teaches you how to process that information optimally. This course equips you with universal algorithmic frameworks—Divide & Conquer, Greedy, Dynamic Programming, Backtracking, and Branch & Bound—while demystifying the boundary between what computers can solve efficiently ($P$) and what lies beyond tractable computation ($NP$-Complete).
:::

---

## 🎯 Course Objectives

The primary pedagogical goals of this course are structured to develop mathematical rigor and problem-solving intuition:

1. **Foundational Algorithm Analysis**: To gain a foundational understanding of algorithms, asymptotic notations, recurrence equations, and formal criteria for analyzing time and space complexities.
2. **Algorithmic Design Paradigms**: To develop rigorous problem-solving skills across major algorithm design paradigms including Divide and Conquer, Greedy Strategy, Dynamic Programming, Backtracking, and Branch & Bound.
3. **Complexity & Intractability**: To understand the fundamental concepts of computationally tractable and intractable problems, the theory of $NP$-Completeness ($P$, $NP$, $NP$-Hard, $NP$-Complete), reduction techniques, and strategies to handle intractability (Approximation and Randomized algorithms).

---

## 📚 Module-by-Module Syllabus Breakdown

### Module 1: Foundations, Recurrences & Balanced Trees (11 Contact Hours)

::: callout-exam Module 1 High-Yield Focus
Module 1 carries **15 compulsory/choice marks in ESE** (Two 3-mark questions in Part A + One 9-mark question with choice in Part B). High-probability exam questions: Solving recurrences using Master's Theorem and Iteration/Recursion Tree methods, computing Big-O of nested loops, and step-by-step AVL Tree insertion/deletion with single/double rotations (LL, RR, LR, RL).
:::

* **Algorithms Fundamentals & Criteria**:
  * Definition of an Algorithm, characteristics (Finiteness, Definiteness, Input, Output, Effectiveness).
  * Criteria for analyzing algorithms; Performance analysis: Time complexity and Space complexity (fixed vs variable part).
  * Best-case, Worst-case, and Average-case complexities; Amortized analysis overview.
* **Asymptotic Notations & Properties**:
  * Formal mathematical definitions and bounds: Big-O ($O$), Big-Omega ($\Omega$), Big-Theta ($\Theta$), Little-o ($o$), and Little-omega ($\omega$).
  * Algebraic properties of asymptotic notations (transitivity, reflexivity, symmetry, transpose symmetry).
  * Time and space complexity calculations of simple iterative algorithms (single, nested, dependent, and logarithmic loops).
* **Analysis of Recursive Algorithms**:
  * Setting up Recurrence Equations for recursive procedures.
  * **Solution of Recurrence Equations**:
    1. **Iteration Method (Back-substitution)**: Expanding recurrences step-by-step to general patterns and summations.
    2. **Recursion Tree Method**: Visualizing recurrence tree depth, branching factor, cost per level, and total cost evaluation.
    3. **Substitution Method**: Mathematical induction approach (guessing bounds and proving via base case and induction step).
    4. **Master's Theorem**: Standard recurrence form $T(n) = aT(n/b) + f(n)$ with $a \ge 1, b > 1$; three canonical cases comparing $f(n)$ with $n^{\log_b a}$ *(proof not expected in exam)*.
* **Balanced Search Trees (AVL Trees)**:
  * Motivation for balanced search trees: preventing worst-case $O(n)$ degeneracy in Binary Search Trees.
  * Definition of AVL Tree, Balance Factor ($BF = h_L - h_R \in \{-1, 0, 1\}$).
  * **AVL Rotations in Detail**:
    * Single Rotations: Left-Left (LL) rotation, Right-Right (RR) rotation.
    * Double Rotations: Left-Right (LR) rotation, Right-Left (RL) rotation.
  * AVL Insertion and Deletion operations with rebalancing *(step-by-step trace expected, pseudocode/algorithm implementation not expected)*.

---

### Module 2: Disjoint Sets, Graph Algorithms & Divide-and-Conquer (11 Contact Hours)

::: callout-exam Module 2 High-Yield Focus
Module 2 focuses on advanced graph representations, connected components, and divide-and-conquer recurrences. Frequent exam topics: Union-Find with rank and path compression ($O(\alpha(n))$ time complexity), BFS vs DFS traversal order & edge classifications, Kosaraju's algorithm for Strongly Connected Components (SCC), Topological Sorting (Kahn's algorithm vs DFS), and Strassen's matrix multiplication recurrence derivation ($7$ multiplications vs $8$).
:::

* **Disjoint Sets (Union-Find Data Structure)**:
  * Disjoint set operations: `MakeSet(x)`, `Find(x)`, `Union(x, y)`.
  * Naive tree representation vs optimized heuristics: **Union by Rank** and **Path Compression**.
  * Detailed time complexity analysis of Union by Rank with Path Compression (amortized time $O(\alpha(n))$, where $\alpha$ is the Inverse Ackermann function).
  * Application: Finding connected components in an undirected graph and cycle detection.
* **Graph Representations & Traversals**:
  * Graph representations: Adjacency Matrix vs Adjacency List (space and time trade-offs).
  * **Breadth-First Search (BFS)**: Algorithm, queue-based exploration, shortest path in unweighted graphs, edge classification, time complexity $O(V + E)$.
  * **Depth-First Search (DFS)**: Algorithm, recursion stack, discovery and finish timestamps, tree, back, forward, and cross edges, time complexity $O(V + E)$.
  * **Strongly Connected Components (SCC)**: Directed graphs, Kosaraju's Two-Pass DFS Algorithm using graph transpose $G^T$, Tarjan's algorithm overview.
  * **Topological Sorting**: Directed Acyclic Graphs (DAGs), DFS-based topological sort using finish times, Kahn's algorithm using in-degrees.
* **Divide and Conquer Strategy**:
  * Control abstraction of the Divide and Conquer design paradigm.
  * **Merge Sort**: Divide, conquer, combine steps, recurrence relation $T(n) = 2T(n/2) + \Theta(n)$, detailed proof of $\Theta(n \log n)$ complexity.
  * **Strassen's Matrix Multiplication**: Standard matrix multiplication algorithm ($\Theta(n^3)$), Strassen's block sub-matrix formulation using 7 recursive multiplications, recurrence $T(n) = 7T(n/2) + \Theta(n^2)$, closed-form derivation $O(n^{\log_2 7}) \approx O(n^{2.807})$.

---

### Module 3: Greedy Strategy, Dynamic Programming & Backtracking (11 Contact Hours)

::: callout-exam Module 3 High-Yield Focus
Module 3 is the core algorithmic paradigms module. Must-know exam derivations and traces: Greedy Choice Property vs Optimal Substructure, Fractional Knapsack vs 0/1 Knapsack, Kruskal's vs Prim's MST with dry-run on graphs, Dijkstra's algorithm trace, Matrix Chain Multiplication DP table construction, Floyd-Warshall all-pairs shortest paths, and $N$-Queens state-space tree generation.
:::

* **Greedy Strategy**:
  * Control abstraction of the Greedy design paradigm; Greedy Choice Property and Optimal Substructure.
  * **Fractional Knapsack Problem**: Greedy formulation based on value-to-weight ratio ($v_i / w_i$), sorting, step-by-step algorithm, $O(n \log n)$ complexity analysis.
  * **Minimum Cost Spanning Tree (MST)**:
    * Cut Property and Cycle Property of spanning trees.
    * **Kruskal's Algorithm**: Edge-centric greedy choice, cycle prevention using Disjoint Sets (Union-Find), time complexity $O(E \log E)$ or $O(E \log V)$.
    * **Prim's Algorithm**: Vertex-centric growing tree, Priority Queue (Min-Heap) implementation, time complexity $O((V + E) \log V)$.
  * **Single-Source Shortest Path Problem**:
    * **Dijkstra's Algorithm**: Greedy node extraction, edge relaxation, non-negative weight constraint, time complexity with binary min-heap $O((V + E) \log V)$ and Fibonacci heap $O(E + V \log V)$.
* **Dynamic Programming (DP)**:
  * Control abstraction of Dynamic Programming; Principle of Optimality (Bellman's equation), Overlapping Subproblems vs Optimal Substructure.
  * Top-down Memoization vs Bottom-up Tabulation.
  * **Matrix Chain Multiplication (MCM)**: Formulation, recurrence $m[i, j] = \min_{i \le k < j} \{m[i, k] + m[k+1, j] + p_{i-1}p_k p_j\}$, DP table construction, parenthesization extraction, time complexity $O(n^3)$ and space $O(n^2)$.
  * **All-Pairs Shortest Path Problem**:
    * **Floyd-Warshall Algorithm**: Intermediate vertex formulation $d^{(k)}[i, j] = \min(d^{(k-1)}[i, j], d^{(k-1)}[i, k] + d^{(k-1)}[k, j])$, $k$-step matrix transformations, negative cycle detection, time complexity $\Theta(V^3)$.
* **Backtracking Paradigm**:
  * Control abstraction of Backtracking; State-Space Tree representation, Depth-First search with pruning (bounding functions).
  * **$N$-Queens Problem**: Formulation, explicit and implicit constraints, safe placement validation, backtracking algorithm, 4-Queens and 8-Queens state-space tree exploration.

---

### Module 4: Branch and Bound, Complexity Theory & Advanced Paradigms (11 Contact Hours)

::: callout-exam Module 4 High-Yield Focus
Module 4 explores advanced search and theoretical computer science. High-yield KTU exam topics: LC Branch and Bound state-space tree for Travelling Salesman Problem (TSP) using reduced cost matrices, definitions of $P$, $NP$, $NP$-Hard, and $NP$-Complete, formal reduction proof showing Clique $\le_P$ Vertex Cover or 3-SAT reductions, Approximation ratio for Bin Packing heuristics (Next Fit, First Fit, Best Fit), and Las Vegas vs Monte Carlo randomized algorithms (Randomized QuickSort expected $\Theta(n \log n)$ analysis).
:::

* **Branch and Bound Strategy**:
  * Control abstraction of Branch and Bound; Comparison: Backtracking (DFS) vs Branch and Bound (BFS / FIFO / LIFO / Least Cost - LC search).
  * Bounding functions, lower bounds, upper bounds, and state pruning.
  * **Travelling Salesman Problem (TSP)**: Least-Cost Branch and Bound formulation using **Reduced Cost Matrices**, calculation of cost of root node, step-by-step branch expansion, pruned state-space search, complete algorithm.
* **Computational Complexity Theory**:
  * Tractable vs Intractable problems; Polynomial-time algorithms vs exponential/factorial growth.
  * **Complexity Classes**:
    * **Class $P$**: Problems solvable in polynomial time by a Deterministic Turing Machine.
    * **Class $NP$**: Problems verifiable in polynomial time by a Deterministic Turing Machine (or solvable in polynomial time by a Non-deterministic Turing Machine).
    * **Class $NP$-Hard**: Problems to which every problem in $NP$ can be polynomial-time reduced ($L' \le_P L$).
    * **Class $NP$-Complete**: Problems that are both in $NP$ and $NP$-Hard ($L \in NP$ and $L \in NP\text{-Hard}$).
    * The open millennium problem: $P \stackrel{?}{=} NP$.
  * **$NP$-Completeness Proofs**:
    * Polynomial-time reduction technique ($L_1 \le_P L_2$).
    * Proof that **Clique Problem** is $NP$-Complete (reduction from 3-SAT).
    * Proof that **Vertex Cover Problem** is $NP$-Complete (reduction from Independent Set / Clique).
* **Approximation Algorithms**:
  * Motivation: Coping with $NP$-Hard optimization problems using polynomial-time heuristics with guaranteed approximation bounds ($\rho(n)$-approximation).
  * **Bin Packing Problem**: Formulation; Heuristics and approximation ratios:
    * Next Fit (NF) heuristic ($\le 2 \cdot \text{OPT}$).
    * First Fit (FF) and Best Fit (BF) heuristics ($\le 1.7 \cdot \text{OPT}$).
    * First Fit Decreasing (FFD) and Best Fit Decreasing (BFD) heuristics ($\le \frac{11}{9} \cdot \text{OPT} + 1$).
* **Randomized Algorithms**:
  * Introduction to randomized algorithms; Use of random bits/decisions.
  * **Taxonomy of Randomized Algorithms**:
    * **Las Vegas Algorithms**: Always produce the correct result; execution running time is a random variable (e.g., Randomized QuickSort).
    * **Monte Carlo Algorithms**: Have a deterministic running time; output is correct with a high probability (e.g., Miller-Rabin Primality Test, Karger's Min-Cut).
  * **Randomized QuickSort**: Randomized pivot selection, indicator random variables, expected number of comparisons, rigorous mathematical proof of expected time complexity $\Theta(n \log n)$ and worst-case $\Theta(n^2)$.

---

## 📖 Prescribed Textbooks & Reference Books

### Prescribed Core Textbooks

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Introduction to Algorithms (CLRS)** | **T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein** | **Prentice-Hall India (PHI)** | **4th Edition, 2018** |
| **2** | **Fundamentals of Computer Algorithms** | **Ellis Horowitz, Sartaj Sahni, Sanguthevar Rajasekaran** | **Universities Press / Orient Longman** | **2nd Edition, 2008** |
| **3** | **Computer Algorithms: Introduction to Design and Analysis** | **Sara Baase, Allen Van Gelder** | **Pearson Education** | **3rd Edition, 2009** |

</div>

### Prescribed Reference Books

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Design and Analysis of Algorithms** | Michael T. Goodrich, Roberto Tamassia | Wiley | 1st Edition, 2021 |
| **2** | **Algorithm Design** | Jon Kleinberg, Éva Tardos | Pearson Education | 1st Edition, 2005 |
| **3** | **Algorithms** | Robert Sedgewick, Kevin Wayne | Pearson Education | 4th Edition, 2011 |
| **4** | **Fundamentals of Algorithmics** | Gilles Brassard, Paul Bratley | Pearson Education | 1st Edition, 1996 |
| **5** | **The Algorithm Design Manual** | Steven S. Skiena | Springer | 2nd Edition, 2008 |

</div>

---

## 🎥 Video Lectures & Online Course Resources

<div class="table-wrap">

| Module | Platform / Institute | Course Title & Online Resource Link | Focus Areas |
| :---: | :--- | :--- | :--- |
| **Module 1** | **NPTEL / IIT Madras** | [Design and Analysis of Algorithms (NPTEL Course 106106131)](https://archive.nptel.ac.in/courses/106/106/106106131/) | Asymptotic notations, recurrence relations, and AVL balance. |
| **Module 2** | **Coursera / UC San Diego** | [Dynamic Programming, Greedy Algorithms & Graphs](https://www.coursera.org/learn/dynamic-programming-greedy-algorithms) | Disjoint sets, BFS/DFS, SCC, and divide & conquer. |
| **Module 3** | **Stanford Online** | [Algorithms: Design and Analysis (Part 1)](https://online.stanford.edu/courses/soe-ycsalgorithms1-algorithms-design-and-analysispart-1) | Greedy algorithms, MST, Dijkstra, and dynamic programming. |
| **Module 4** | **Stanford Online** | [Algorithms: Design and Analysis (Part 2)](https://online.stanford.edu/courses/soe-ycs0001-algorithms-design-and-analysis-part-2) | Branch & Bound, NP-Completeness, and randomized algorithms. |

</div>

---

## ⚖️ Course Assessment Method (CIE & ESE)

The evaluation consists of **40 Marks for Continuous Internal Evaluation (CIE)** and **60 Marks for the End Semester Examination (ESE)**, totaling 100 Marks.

### Continuous Internal Evaluation (CIE: 40 Marks)

<div class="table-wrap">

| Component | Marks Allocated | Evaluation Criteria & Format |
| :--- | :---: | :--- |
| **Attendance** | **5 Marks** | Minimum 75% attendance mandatory. Scaled as per university regulations. |
| **Assignment / Microproject** | **15 Marks** | Minimum of two rigorous algorithm problem sets or one integrated coding microproject (e.g., implementing Strassen's matrix multiplication, AVL tree visualizer, or TSP Branch & Bound solver). |
| **Internal Examination - 1 (Written)** | **10 Marks** | Centralized written test covering **Module 1 and first half of Module 2** (scaled to 10 marks). |
| **Internal Examination - 2 (Written)** | **10 Marks** | Centralized written test covering **second half of Module 2, Module 3, and Module 4** (scaled to 10 marks). |
| **Total CIE Marks** | **40 Marks** | **Eligibility: Minimum 45% (18/40 marks) required in CIE to appear for the End Semester Examination.** |

</div>

---

### End Semester Examination (ESE: 60 Marks)

* **Total Duration**: **2 Hours 30 Minutes (150 Minutes)**
* **Total Paper Valuation**: **96 Marks** (Students answer for a maximum of **60 Marks**)
* **Passing Requirement**: **Minimum 40% (24/60 marks) in ESE AND minimum 50% aggregate (50/100) combining CIE + ESE**.

<div class="table-wrap">

| Section | Question Format & Mark Distribution | Choice Rules | Total Marks |
| :---: | :--- | :--- | :---: |
| **Part A** | • **2 Questions from each module** (Modules 1, 2, 3, 4).<br>• Total of **8 Questions** (Questions 1 to 8).<br>• Each question carries **3 marks** ($8 \times 3 = 24$). | **Compulsory**<br>*(No internal choice)* | **24 Marks** |
| **Part B** | • **Two full questions from each module** (Questions 9 & 10 from M1, 11 & 12 from M2, 13 & 14 from M3, 15 & 16 from M4).<br>• Each full question carries **9 marks** ($4 \times 9 = 36$).<br>• Each full question can have **maximum 3 subdivisions** (e.g., 5+4, 6+3, or 3+3+3). | **Choice-based**<br>*(Answer any 1 full question from each module)* | **36 Marks** |
| **Total** | **Part A (24 Marks) + Part B (36 Marks)** | | **60 Marks** |

</div>

---

## 🎓 Course Outcomes (COs)

Upon successful completion of the course, students will be able to:

<div class="table-wrap">

| CO Identifier | Course Outcome (CO) Statement | Bloom's Knowledge Level |
| :---: | :--- | :---: |
| **CO1** | **Analyze** any given algorithm and express its time and space complexities in asymptotic notations. | **K4 (Analyse)** |
| **CO2** | **Solve** the recurrence equations using Iteration, Recurrence Tree, Substitution and Master’s Method to compute time complexity of algorithms. | **K3 (Apply)** |
| **CO3** | **Illustrate** the operations of advanced data structures like AVL trees and Disjoint sets. | **K3 (Apply)** |
| **CO4** | **Illustrate** the representation, traversal and different operations on Graphs. | **K3 (Apply)** |
| **CO5** | **Demonstrate** Divide-and-conquer, Greedy Strategy, Dynamic programming, Branch-and-Bound and Backtracking algorithm design techniques. | **K2 (Understand)** |
| **CO6** | **Classify** a problem as computationally tractable or intractable, and **discuss** strategies to address intractability. | **K4 (Analyse)** |

</div>

::: callout-formula Bloom's Revised Taxonomy Levels Key
* **K1 - Remember**: Recalling recurrence definitions, complexity bounds, and algorithm steps.
* **K2 - Understand**: Explaining algorithm paradigms (Greedy vs DP, Backtracking vs Branch & Bound).
* **K3 - Apply**: Applying Master's Theorem, tracing AVL rotations, executing Dijkstra / Prim / Kruskal algorithms, and executing Union-Find operations.
* **K4 - Analyse**: Analyzing worst/average case complexities, constructing polynomial-time reductions for $NP$-Completeness proofs, and deriving approximation ratios.
* **K5 - Evaluate**: Comparing algorithmic efficiency, evaluating lower bound trade-offs.
* **K6 - Create**: Formulating custom dynamic programming recurrences or state-space bounding functions for novel engineering problems.
:::

---

## 🗺️ CO-PO Mapping Table

The Course Outcomes directly map to the **National Board of Accreditation (NBA) Program Outcomes (POs)** for undergraduate computer science and engineering:

*Correlation Scale: **3 = Substantial (High)** | **2 = Moderate (Medium)** | **1 = Slight (Low)** | **— = No Correlation***

<div class="table-wrap">

| Course Outcome | PO1<br><small>Engg Knowledge</small> | PO2<br><small>Problem Analysis</small> | PO3<br><small>Design/Dev</small> | PO4<br><small>Investigations</small> | PO5<br><small>Modern Tools</small> | PO6<br><small>Engineer & Society</small> | PO7<br><small>Environment</small> | PO8<br><small>Ethics</small> | PO9<br><small>Individual/Team</small> | PO10<br><small>Communication</small> | PO11<br><small>Project Mgmt</small> | PO12<br><small>Life-long Learning</small> |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CO1** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — |
| **CO2** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | — | — | — | — | — | — | — | — |
| **CO3** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO4** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO5** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | — | — | — | — | — | — | — |
| **CO6** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | — | — | — | — | — | — | — |

</div>

### CO-PO Mapping Justification & Insights:
* **PO1 (Engineering Knowledge)**: Strongly addressed across all six COs ($\text{Level } 3$) as algorithm analysis relies heavily on discrete mathematics, recurrence relations, summations, and graph theory.
* **PO2 (Problem Analysis)**: Addressed at the highest level ($\text{Level } 3$) across all COs through rigorous complexity determination, asymptotic classification, and identification of $NP$-Complete computational bottlenecks.
* **PO3 (Design/Development of Solutions)**: Substantially addressed ($\text{Level } 3$) as students design algorithms across Divide & Conquer, Greedy, DP, Backtracking, and Branch & Bound paradigms.
* **PO4 (Conduct Investigations of Complex Problems)**: Addressed in investigating optimal substructure properties, empirical benchmarking, and graph component connectivity.
* **PO5 (Modern Tool Usage)**: Addressed in CO1, CO5, and CO6 through algorithmic profiling tools, state-space tree analyzers, and computational complexity simulators.

---

## ⚡ Interactive Syllabus Self-Check Quiz

::: quiz DAA Recurrence & Master's Theorem Assessment
Under the KTU 2024 PCCST502 syllabus, which of the following statements regarding the study of recurrence equations in Module 1 is true?
(*) Students are expected to solve recurrences using Iteration, Recursion Tree, Substitution, and Master's Theorem, but formal proofs of the Master's Theorem are not expected in the exam.
( ) Mathematical proofs of all cases of Master's Theorem are mandatory for 9-mark questions.
( ) Only the Iteration method is included; Master's Theorem has been removed from the 2024 scheme.
( ) AVL tree balance algorithms must be coded in C++, but recurrence equations are excluded.
::: explanation
The KTU PCCST502 syllabus explicitly specifies for Module 1: "Solution of Recurrence Equations: Iteration Method, Recursion Tree Method, Substitution method and Master’s Theorem (proof not expected); Balanced Search Trees - AVL Trees (Insertion and deletion operations with all rotations in detail, algorithms not expected)."
:::

::: quiz Complexity Classes & Randomized Algorithms Assessment
In Module 4 of PCCST502, how are Randomized QuickSort and Monte Carlo / Las Vegas algorithms classified?
(*) Randomized QuickSort is a Las Vegas algorithm because it always produces the sorted array correctly, but its running time is a random variable with expected $\Theta(n \log n)$ time.
( ) Randomized QuickSort is a Monte Carlo algorithm because it may fail to sort the input with a small probability.
( ) Randomized QuickSort is in class NP-Complete because of its worst-case $\Theta(n^2)$ complexity.
( ) Las Vegas algorithms have a bounded running time but uncertain output correctness.
::: explanation
By definition in the KTU syllabus: **Las Vegas algorithms** always produce the correct result, but their running time is a random variable (e.g., Randomized QuickSort with expected $\Theta(n \log n)$ time). In contrast, **Monte Carlo algorithms** have deterministic running times, but their answer is correct with a high probability (e.g., Miller-Rabin primality testing).
:::

---

## 🧭 Next Steps in Your Study Journey

* Begin with **[Module 1: 1.1 Algorithm Definition and Criteria](m1_01_algorithm_definition_and_criteria.html)** to master asymptotic notation and complexity analysis.
* Practice rigorous step-by-step problem sets in the **[Module 1 Workbook: Asymptotics & Summations](m1_p01_asymptotics.html)**.
* Practice master theorem and recurrences in the **[Module 1 Workbook: Master Theorem](m1_p05_master_theorem.html)**.
* Test your active recall anytime using the **[Anki-style Spaced Repetition Review Deck](../../review.html)**.
