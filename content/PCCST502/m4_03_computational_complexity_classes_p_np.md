# Module 4.3: Computational Complexity Theory — Classes P, NP, NP-Hard, and NP-Complete

**Course Code:** PCCST502 / CST306  
**Course Title:** Design and Analysis of Algorithms (DAA)  
**Academic Scheme:** APJ Abdul Kalam Technological University (KTU) 2024 Scheme  
**Module:** Module 4 — Advanced State-Space Search & Computational Complexity  
**Document Classification:** Publication-Grade Theoretical Lecture Note & Mathematical Foundation  

---

## 1. Executive Overview & Foundational Framework

Throughout algorithmic analysis, we typically classify algorithms by their asymptotic time complexity $\mathcal{O}(n)$, $\mathcal{O}(n \log n)$, $\mathcal{O}(n^2)$, or $\mathcal{O}(2^n)$. However, **Computational Complexity Theory** investigates the intrinsic difficulty of *problems* rather than the performance of specific algorithms. 

Instead of asking:  
> *"What is the running time of algorithm $A$ on input of size $n$?"*

Complexity theory asks:  
> *"What is the minimal computational resource (time, space, non-determinism) required by **any possible** algorithm to solve problem $\Pi$?"*

To establish mathematical universality independent of programming languages, hardware architectures, and instruction sets, complexity theory frames all computations on abstract machines—primarily the **Deterministic Turing Machine (DTM)** and the **Nondeterministic Turing Machine (NDTM)**—over formal languages defined on finite alphabets $\Sigma = \{0, 1\}$.

::: callout-intuition
**Mental Model: The Spectrum of Hardness**  
Imagine an escalating scale of computational friction:
1. **Class P (The Solvable Realm):** Problems where finding a solution is easy (polynomial time, e.g., finding the shortest path on a map).
2. **Class NP (The Verifiable Realm):** Problems where *finding* a solution may require searching through a needle in an exponential haystack, but *verifying* a proposed solution takes mere moments (e.g., solving a Sudoku puzzle vs. checking a completed grid).
3. **Class NP-Complete (The Universal Bottlenecks):** The absolute hardest problems in NP. If an efficient, polynomial-time algorithm exists for any single one of them, then **every** problem in NP instantly collapses into P.
4. **Class NP-Hard (The Limitless Horizon):** Problems at least as hard as the hardest problems in NP, which might not even be verifiable in polynomial time, or might even be undecidable (e.g., the Halting Problem).
:::

---

## 2. Decision Problems vs. Optimization Problems

In standard computing, algorithmic challenges are predominantly framed as **Optimization Problems**. However, complexity theory is almost entirely formulated in terms of **Decision Problems**.

### 2.1 Formal Definitions

#### Definition 2.1 (Optimization Problem)
An optimization problem consists of:
1. A set of valid instances $I \subseteq \Sigma^*$.
2. For each instance $x \in I$, a finite set of feasible candidate solutions $S(x)$.
3. An objective function $f: S(x) \to \mathbb{R}$ that assigns a numerical value (cost, weight, or profit) to each candidate solution $y \in S(x)$.
4. An objective: Find an optimal solution $y^* \in S(x)$ such that:
   $$f(y^*) = \min_{y \in S(x)} f(y) \quad (\text{Minimization}) \quad \text{or} \quad f(y^*) = \max_{y \in S(x)} f(y) \quad (\text{Maximization})$$

#### Definition 2.2 (Decision Problem)
A decision problem is a function $D: I \to \{\text{YES}, \text{NO}\}$ (or $\{1, 0\}$). In formal language theory, a decision problem is equivalent to deciding membership in a formal language $L \subseteq \Sigma^*$:
$$L = \{x \in \Sigma^* \mid D(x) = \text{YES}\}$$
The computational goal is purely binary: determine whether a given instance $x$ belongs to language $L$.

---

### 2.2 Threshold Reduction: Converting Optimization to Decision

Every optimization problem can be cast into an equivalent decision problem by introducing a scalar threshold parameter $k \in \mathbb{R}$.

| Problem Class | Optimization Formulation | Decision Formulation ($\Pi_D$) |
| :--- | :--- | :--- |
| **Travelling Salesperson (TSP)** | Find a Hamiltonian cycle in $G$ with the **minimum total edge cost**. | Given graph $G$, cost matrix $C$, and integer $k$, does there exist a Hamiltonian cycle with total cost $\le k$? |
| **0/1 Knapsack** | Find a binary vector $X \in \{0, 1\}^n$ maximizing profit $\sum p_i x_i$ subject to $\sum w_i x_i \le W$. | Given weights, profits, capacity $W$, and target profit $k$, does there exist $X \in \{0, 1\}^n$ with weight $\le W$ and profit $\ge k$? |
| **Graph Coloring** | Find the chromatic number $\chi(G)$ (minimum colors needed to color $V(G)$ validly). | Given graph $G and integer $k$, is $G$ $k$-colorable (can $V(G)$ be colored with $\le k$ colors without adjacent clashes)? |
| **Clique** | Find the maximum complete subgraph size $\omega(G)$ in graph $G$. | Given graph $G$ and integer $k$, does $G$ contain a clique of size $\ge k$? |

---

### 2.3 Mathematical Equivalence: Optimization $\equiv_p$ Decision

A foundational theorem in complexity theory states that an optimization problem can be solved in polynomial time if and only if its corresponding decision version can be solved in polynomial time.

#### Theorem 2.1 (Polynomial Equivalence of Decision and Optimization)
*For any combinatorial problem $\Pi$ where costs are integers bounded by a polynomial number of bits, the optimization problem $\Pi_{\text{opt}}$ can be solved in polynomial time if and only if the decision problem $\Pi_{\text{dec}}$ can be solved in polynomial time.*

```
                       [ Optimization Problem ]
                                |
               Binary Search on Threshold Parameter k
                   (at most ⌈log2(Range)⌉ calls)
                                |
                                v
               [ Repeated Calls to Decision Oracle ]
                       (YES / NO Responses)
```

**Proof (Constructive Reduction via Binary Search):**
1. **Direction 1 ($\Pi_{\text{dec}} \le_p \Pi_{\text{opt}}$):**  
   Suppose we have an algorithm $A_{\text{opt}}$ that solves the optimization version in time $\mathcal{T}_{\text{opt}}(n)$. To solve the decision version for instance $(I, k)$:
   - Run $A_{\text{opt}}(I)$ to compute the true optimal cost $C^*$.
   - For a minimization problem: If $C^* \le k$, return $\text{YES}$; else return $\text{NO}$.
   - Time complexity: $\mathcal{O}(\mathcal{T}_{\text{opt}}(n)) + \mathcal{O}(1)$. Thus, $\Pi_{\text{dec}}$ is no harder than $\Pi_{\text{opt}}$.

2. **Direction 2 ($\Pi_{\text{opt}} \le_p \Pi_{\text{dec}}$):**  
   Suppose we have a black-box decider (an oracle) $A_{\text{dec}}$ that solves the decision version in time $\mathcal{T}_{\text{dec}}(n)$. Let the optimal cost $C^*$ reside in a known discrete integer interval $[C_{\min}, C_{\max}]$.
   - Let the range of possible costs be $R = C_{\max} - C_{\min}$.
   - Using **Binary Search** over the range $[C_{\min}, C_{\max}]$, we query $A_{\text{dec}}$ with midpoint $k = \lfloor (C_{\min} + C_{\max}) / 2 \rfloor$:
     * If $A_{\text{dec}}(I, k) = \text{YES}$, we know $C^* \le k$; search the lower half $[C_{\min}, k]$.
     * If $A_{\text{dec}}(I, k) = \text{NO}$, we know $C^* > k$; search the upper half $[k + 1, C_{\max}]$.
   - The binary search terminates after exactly $\lceil \log_2 R \rceil$ iterations.
   - If costs are encoded in binary with length $B$, then $R \le 2^B$, meaning $\lceil \log_2 R \rceil \le B$, which is strictly polynomial in the input size.
   - Total time to find the optimal numerical value $C^*$ is:
     $$\mathcal{O}(B \cdot \mathcal{T}_{\text{dec}}(n)) = \text{Polynomial in input size}$$

3. **Materializing the Optimal Solution Structure:**  
   Once the exact numerical optimal cost $C^*$ is known, we can reconstruct the actual combinatorial solution (e.g., the exact sequence of edges in TSP) in polynomial time:
   - For each edge $e \in E$:
     * Temporarily remove $e$ from graph $G$ (set its cost to $\infty$).
     * Query the decision oracle: *"Does there still exist a tour of cost $\le C^*$?"*
     * If the oracle answers $\text{YES}$, edge $e$ was redundant; permanently delete $e$.
     * If the oracle answers $\text{NO}$, edge $e$ is essential to achieving cost $C^*$; restore $e$.
   - This requires exactly $|E|$ calls to the decision oracle.
   - Since $|E| \le n^2$, the entire structural reconstruction takes polynomial time: $\mathcal{O}(|E| \cdot \mathcal{T}_{\text{dec}}(n))$. $\blacksquare$

::: callout-exam
**KTU Examination Scoring Alert: Why Focus on Decision Problems?**  
Students often ask why theoretical computer science focuses on YES/NO questions instead of finding numbers or graphs.  
When answering this in university exams:
1. State that decision problems map directly to **formal language recognition** ($L \subseteq \Sigma^*$).
2. Note that proving a decision problem is hard ($NP$-complete) immediately implies that its optimization problem is at least as hard ($NP$-hard), because solving the optimization version automatically solves the decision version.
:::

---

## 3. The Complexity Class P (Polynomial Time)

The complexity class **P** represents the gold standard of algorithmic tractability.

### 3.1 Formal Mathematical Definition
Let $\Sigma$ be a finite alphabet, and let $L \subseteq \Sigma^*$ be a formal language.

#### Definition 3.1 (Deterministic Turing Machine Decidability)
A Deterministic Turing Machine (DTM) is a 7-tuple:
$$M = (Q, \Sigma, \Gamma, \delta, q_0, q_{\text{accept}}, q_{\text{reject}})$$
where the transition function is deterministic:
$$\delta: Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$$

For any input string $w \in \Sigma^*$, machine $M$ executes a unique sequence of configurations. $M$ decides language $L$ if for all $w \in \Sigma^*$:
- If $w \in L$, $M$ halts in state $q_{\text{accept}}$.
- If $w \notin L$, $M$ halts in state $q_{\text{reject}}$.

#### Definition 3.2 (The Class P)
A language $L$ is in the class $\text{P}$ if there exists a Deterministic Turing Machine $M$ and a polynomial function $p: \mathbb{N} \to \mathbb{N}$ such that for every string $w \in \Sigma^*$:
1. $M$ halts on $w$ within at most $p(|w|)$ execution steps.
2. $M$ accepts $w$ if and only if $w \in L$.

Formally, using deterministic time complexity classes:
$$\text{P} = \bigcup_{k=1}^{\infty} \text{TIME}(n^k)$$

---

### 3.2 The Cobham-Edmonds Thesis
The **Cobham-Edmonds Thesis** (Alan Cobham, 1965; Jack Edmonds, 1965) asserts that computational problems are **efficiently tractable** if and only if they can be solved in polynomial time ($n^{\mathcal{O}(1)}$) on a deterministic sequential computing model.

#### Why Polynomial Time Distinguishes Feasibility:
1. **Invariance Across Machine Models:** A polynomial-time algorithm on a single-tape Turing machine remains polynomial on multi-tape Turing machines, Random Access Machines (RAM models), and modern digital computers. The polynomial degree may shift (e.g., from $n^2$ to $n$), but the property of being bounded by $n^{\mathcal{O}(1)}$ is universal.
2. **Closure Properties:** The class P is closed under fundamental mathematical operations:
   - **Complement:** If $L \in \text{P}$, then $\overline{L} \in \text{P}$ (simply swap $q_{\text{accept}}$ and $q_{\text{reject}}$).
   - **Union & Intersection:** If $L_1, L_2 \in \text{P}$, then $L_1 \cup L_2 \in \text{P}$ and $L_1 \cap L_2 \in \text{P}$.
   - **Concatenation & Kleene Closure:** If $L_1, L_2 \in \text{P}$, then $L_1 L_2 \in \text{P}$ and $L_1^* \in \text{P}$.
3. **Asymptotic Scalability:** For an input increase from $n = 50$ to $n = 100$:
   - An $\mathcal{O}(n^3)$ algorithm scales by a factor of $(100/50)^3 = 8$.
   - An $\mathcal{O}(2^n)$ algorithm scales by a factor of $2^{50} \approx 1.125 \times 10^{15}$, turning a 1-second computation into over 35 million years.

---

### 3.3 Canonical Problems Residing in Class P

```
+-------------------------------------------------------------------------------+
|                       CANONICAL PROBLEMS IN CLASS P                           |
+------------------------------------+------------------------------------------+
| Problem                            | Most Efficient Asymptotic Runtime        |
+------------------------------------+------------------------------------------+
| Single-Source Shortest Path        | O(|E| + |V| log |V|)  (Dijkstra / Heap)  |
| Minimum Spanning Tree (MST)        | O(|E| α(|V|))         (Kruskal / Disjoint)|
| Maximum Network Flow               | O(|V| |E|^2)          (Edmonds-Karp)     |
| Bipartite Matching                 | O(|E| √|V|)           (Hopcroft-Karp)    |
| Linear Programming                 | Polynomial            (Karmarkar's Alg)  |
| 2-Satisfiability (2-SAT)           | O(|V| + |E|)          (Strong Components)|
| Primality Testing                  | O((log n)^6)          (AKS Algorithm)    |
+------------------------------------+------------------------------------------+
```

---

## 4. The Complexity Class NP (Nondeterministic Polynomial Time)

A common student error is defining NP as *"Not Polynomial"*. **NP stands for Nondeterministic Polynomial Time.** It represents the collection of decision problems whose positive instances can be efficiently *verified*, even if finding the solution is extraordinarily difficult.

NP can be formalized through two fundamentally equivalent paradigms:
1. The **Nondeterministic Turing Machine (Guess-and-Check)** formulation.
2. The **Polynomial Verifier and Certificate (Witness)** formulation.

---

### 4.1 Formulation 1: The Nondeterministic Turing Machine (NDTM)

#### Definition 4.1 (Nondeterministic Turing Machine)
An NDTM differs from a standard DTM in its transition function:
$$\delta: Q \times \Gamma \to \mathcal{P}(Q \times \Gamma \times \{L, R\})$$
where $\mathcal{P}(S)$ denotes the power set. At any computation state, the machine has a finite choice of valid next moves, forming a computation tree of execution paths.

```
                         [Initial State]
                                |
                   +------------+------------+
                   |                         |
               [Branch 1]                [Branch 2]
                   |                         |
              +----+----+               +----+----+
              |         |               |         |
           [Accept]  [Reject]        [Reject]  [Reject]
```

#### Acceptance Criterion for an NDTM:
An NDTM $M$ accepts an input string $w$ if and only if **there exists at least one computation branch** that halts in state $q_{\text{accept}}$. It rejects $w$ only if *all* possible computation branches halt in $q_{\text{reject}}$.

#### The Two-Stage Nondeterministic Execution Model:
Every polynomial-time NDTM program can be factored into two distinct phases:

```text
Algorithm NondeterministicFramework(w)
begin
    // Phase 1: The Guessing Stage (Pure Nondeterminism)
    // Non-deterministically write a candidate certificate string 'c' on tape
    certificate := GuessCandidateString(); 

    // Phase 2: The Checking Stage (Pure Determinism)
    // Execute a deterministic polynomial-time algorithm to verify 'certificate'
    result := DeterministicVerifier(w, certificate);

    if (result == TRUE) then
        accept;
    else
        reject;
    end if;
end;
```

#### Definition 4.2 (Class NP via NTIME)
$$\text{NP} = \bigcup_{k=1}^{\infty} \text{NTIME}(n^k)$$
A language $L \in \text{NP}$ if there exists an NDTM $M$ that decides $L$ in time bounded by a polynomial $p(n)$ along its accepting path.

---

### 4.2 Formulation 2: Deterministic Verifier & Polynomial Certificate

In modern complexity theory, NP is almost universally analyzed through deterministic verifiers and polynomial certificates.

#### Definition 4.3 (Polynomial-Time Verifier)
A deterministic Turing machine $V$ is a **polynomial-time verifier** for language $L \subseteq \Sigma^*$ if:
1. $V$ takes two input strings: an instance string $x$ and a certificate string $y$ (often called a *witness* or *proof*).
2. $V$ halts and executes in polynomial time bounded by $p(|x|)$ for some polynomial $p$.
3. Language membership satisfies:
   $$x \in L \iff \exists \; y \in \Sigma^* \quad \text{such that } |y| \le p(|x|) \quad \text{and} \quad V(x, y) = \text{ACCEPT}$$

```
   Candidate Instance x ────+
                            |
                            v
                      +───────────+
                      | Deterministic |
                      | Polynomial-   | ────> { ACCEPT (x ∈ L)
                      | Time Verifier |       { REJECT (x ∉ L)
                      |     V(x, y)   |
                      +───────────+
                            ^
                            |
   Polynomial Witness y ────+
   (|y| ≤ p(|x|))
```

#### The Asymmetry of Certificates in NP:
- **YES-Instances ($x \in L$):** There must exist at least one valid certificate $y$ of length bounded by $p(|x|)$ that convinces verifier $V$ to accept.
- **NO-Instances ($x \notin L$):** **No certificate on Earth** can convince verifier $V$ to accept. For every possible string $y$, $V(x, y) = \text{REJECT}$.

---

### 4.3 Rigorous Proof of Equivalence of the Two Definitions

#### Theorem 4.1 (Equivalence Theorem)
*A language $L$ is decided by an NDTM in polynomial time if and only if $L$ has a deterministic polynomial-time verifier with polynomial-length certificates.*

**Proof:**

**Part 1 ($\implies$): If $L \in \text{NTIME}(p(n))$, then $L$ has a polynomial verifier.**
1. Let $M$ be an NDTM that decides $L$ in time $p(n)$.
2. For any string $x \in L$, there exists an accepting computation path of length at most $p(|x|)$.
3. At each computation step, let $d$ be the maximum branching degree of $M$'s transition function $\delta$. The choice made at step $t$ can be encoded by an integer $c_t \in \{1, 2, \dots, d\}$.
4. We define the **certificate $y$** as the sequence of choices made along the accepting path:
   $$y = (c_1, c_2, \dots, c_m) \quad \text{where } m \le p(|x|)$$
5. The length of certificate $y$ in bits is:
   $$|y| = m \cdot \lceil \log_2 d \rceil \le p(|x|) \cdot \lceil \log_2 d \rceil = \mathcal{O}(p(|x|))$$
   which is strictly polynomial in $|x|$.
6. We construct a deterministic verifier $V$:
   - $V(x, y)$ simulates the transitions of $M$ on input $x$.
   - At step $t$, $V$ reads choice $c_t$ from certificate $y$ and deterministically executes that specific branch.
   - If the simulated path reaches $q_{\text{accept}}$ within $p(|x|)$ steps, $V$ outputs $\text{ACCEPT}$; otherwise, it outputs $\text{REJECT}$.
7. Because simulating a single step takes $\mathcal{O}(1)$ time on a multi-track tape, the total time for $V(x, y)$ is $\mathcal{O}(p(|x|))$. Thus, $V$ is a polynomial-time verifier.

**Part 2 ($\impliedby$): If $L$ has a polynomial verifier, then $L \in \text{NTIME}(p(n))$.**
1. Suppose $L$ has a deterministic polynomial-time verifier $V(x, y)$ where $|y| \le q(|x|)$ for polynomial $q$, and $V$ runs in time $r(|x|, |y|) \le r(|x|, q(|x|))$.
2. We construct an NDTM $M$:
   - On input $x$ of length $n$:
   - **Guessing Phase:** $M$ non-deterministically writes a binary string $y$ of length $q(n)$ on an auxiliary tape. With binary alphabet $\{0, 1\}$, this takes exactly $q(n)$ non-deterministic branch steps.
   - **Verification Phase:** $M$ runs the deterministic verifier $V(x, y)$ on $x$ and the guessed string $y$.
   - If $V(x, y)$ accepts, $M$ enters $q_{\text{accept}}$. If $V(x, y)$ rejects, $M$ enters $q_{\text{reject}}$.
3. The total running time of $M$ along any path is:
   $$\mathcal{T}_M(n) = \text{Time}(\text{Guess}) + \text{Time}(\text{Verify}) \le q(n) + r(n, q(n)) = \text{Polynomial in } n$$
4. Therefore, $L \in \text{NTIME}(p(n))$. $\blacksquare$

---

### 4.4 Concrete NP Problems and Their Certificates

To prove a problem is in NP, one must explicitly specify:
1. What the certificate $y$ consists of.
2. The verification algorithm $V(x, y)$.
3. The verification algorithm's polynomial runtime.

```
+--------------------------------------------------------------------------------------------------------+
|                                    VERIFICATION PROFILES FOR NP PROBLEMS                               |
+---------------------+-------------------------------+------------------------------+-------------------+
| Problem             | Polynomial Certificate (y)    | Deterministic Verifier Check | Verifier Runtime  |
+---------------------+-------------------------------+------------------------------+-------------------+
| Hamiltonian Cycle   | An ordered list of vertices   | Check that:                  | O(|V| + |E|)      |
|                     | (v_1, v_2, ..., v_n)          | 1. Every v ∈ V appears once. |                   |
|                     |                               | 2. (v_i, v_{i+1}) ∈ E.       |                   |
|                     |                               | 3. (v_n, v_1) ∈ E.           |                   |
+---------------------+-------------------------------+------------------------------+-------------------+
| Boolean 3-SAT       | A truth assignment vector     | Substitute assignments into  | O(m)              |
|                     | τ: {x_1, ..., x_n} -> {0, 1}  | all m clauses; check if      | (m clauses)       |
|                     |                               | every clause evaluates to 1. |                   |
+---------------------+-------------------------------+------------------------------+-------------------+
| Clique (≥ k)        | A subset of vertices          | Check that:                  | O(k^2) ≤ O(|V|^2) |
|                     | S ⊆ V with |S| = k            | For every pair u, v ∈ S,     |                   |
|                     |                               | edge (u, v) exists in E.     |                   |
+---------------------+-------------------------------+------------------------------+-------------------+
| Subset Sum (= M)    | A sub-collection of weights   | Sum the chosen weights;      | O(n)              |
|                     | S' ⊆ S                        | verify that ∑_{w ∈ S'} w = M.|                   |
+---------------------+-------------------------------+------------------------------+-------------------+
| TSP Decision (≤ k)  | A cyclic sequence of cities   | Check that it visits all     | O(n)              |
|                     | (c_1, c_2, ..., c_n, c_1)     | cities once and sum of edge  |                   |
|                     |                               | costs ≤ k.                   |                   |
+---------------------+-------------------------------+------------------------------+-------------------+
```

---

### 4.5 The Inclusion $P \subseteq NP$ and the Millennium Prize Problem

#### Theorem 4.2
$$\text{P} \subseteq \text{NP}$$

**Proof:**
1. Let $L \in \text{P}$. By definition, there exists a Deterministic Turing Machine $M_D$ that decides $L$ in polynomial time $p(n)$.
2. We construct a verifier $V(x, y)$:
   - The verifier completely ignores the certificate $y$ (we can set certificate length to empty string $\epsilon$, so $|y| = 0$).
   - $V(x, y)$ runs machine $M_D$ directly on input $x$.
   - If $M_D(x)$ accepts, $V$ outputs $\text{ACCEPT}$; otherwise, it outputs $\text{REJECT}$.
3. The running time of $V$ is bounded by $p(|x|)$, which is polynomial.
4. Hence, $L$ satisfies the definition of NP. Therefore, $\text{P} \subseteq \text{NP}$. $\blacksquare$

#### The Fundamental Open Question: Does $P = NP$?
Stated by Stephen Cook in 1971 and designated as one of the seven **Millennium Prize Problems** by the Clay Mathematics Institute in 2000 (with a \$1,000,000 bounty):
$$\text{Does } \text{P} = \text{NP}?$$

- **Philosophical Meaning:** Does the ability to *verify* solutions efficiently imply the ability to *find* solutions efficiently? 
  - If $\text{P} = \text{NP}$, then whenever a mathematical proof can be verified by computer in polynomial time, that proof can also be discovered by computer in polynomial time.
  - As Donald Knuth noted: *"If $P = NP$, the world would be a profoundly different place... every creative task that can be appreciated quickly could be automated entirely."*
- **Current Consensus:** The overwhelming majority of computer scientists conjecture that:
  $$\text{P} \ne \text{NP}$$
  No polynomial-time algorithm has ever been discovered for any NP-Complete problem, despite decades of intense research.

---

### 4.6 The Class Co-NP

To understand the boundaries of NP, consider **Co-NP**.

#### Definition 4.4 (Class Co-NP)
A language $L$ is in **Co-NP** if and only if its set complement $\overline{L} = \Sigma^* \setminus L$ is in NP:
$$L \in \text{Co-NP} \iff \overline{L} \in \text{NP}$$

- **NP:** Problems with short, verifiable proofs for **YES-instances**.  
  *(Example: Is formula $\phi$ satisfiable? Certificate: a single satisfying assignment).*
- **Co-NP:** Problems with short, verifiable proofs for **NO-instances** (or equivalently, universal validity for all instances).  
  *(Example: Is formula $\phi$ a tautology? To prove YES, every single assignment must evaluate to 1. A short certificate would be an assignment where $\phi = 0$, which is a proof for a NO-instance).*

It is unknown whether $\text{NP} = \text{Co-NP}$, but it is widely believed that $\text{NP} \ne \text{Co-NP}$.

---

## 5. Polynomial-Time Reductions (Karp Reductions)

Reductions are the primary tool used to compare the relative difficulty of computational problems. If problem $A$ can be transformed into problem $B$, then an algorithm for $B$ immediately yields an algorithm for $A$.

### 5.1 Formal Mathematical Definition

#### Definition 5.1 (Polynomial-Time Many-One Reduction / Karp Reduction)
Let $A \subseteq \Sigma^*$ and $B \subseteq \Gamma^*$ be two decision problems (languages).  
Language $A$ is **polynomial-time many-one reducible** to language $B$, denoted as:
$$A \le_p B$$
if there exists a function $f: \Sigma^* \to \Gamma^*$ such that:
1. **Computability:** The reduction function $f$ is computable by a deterministic Turing machine in polynomial time $\mathcal{O}(n^c)$ for some constant $c > 0$.
2. **Equivalence (Validity):** For every string $x \in \Sigma^*$:
   $$x \in A \iff f(x) \in B$$

```
   Instance x ∈ A ──────[ Reduction f ]──────> Instance f(x) ∈ B
        |                                             |
        | (YES / NO)                                  | (YES / NO)
        v                                             v
   Is x in Language A? <════ IDENTICAL ═══════> Is f(x) in Language B?
```

::: callout-warning
**Algorithmic Trap: The Bi-Directional Condition**  
The equivalence condition $x \in A \iff f(x) \in B$ requires **two** explicit proofs:
1. **Soundness (Forward):** If $x \in A$, then $f(x) \in B$.
2. **Completeness (Reverse / Contrapositive):** If $x \notin A$, then $f(x) \notin B$ (which is logically equivalent to: If $f(x) \in B$, then $x \in A$).  
Failing to prove both directions in an exam results in losing half the proof marks!
:::

---

### 5.2 The Hardness Conveyor Belt: Mechanics of $A \le_p B$

The notation $A \le_p B$ reads: *"Problem $A$ is polynomial-time reducible to Problem $B$"*.  
Mathematically, this establishes that **$B$ is at least as hard as $A$** (up to polynomial factors).

```
                      A ≤_p B
   Difficulty of A  ───────────>  Difficulty of B
   
   If B is EASY (B ∈ P)    ===>   A must be EASY (A ∈ P)
   If A is HARD (A ∉ P)    ===>   B must be HARD (B ∉ P)
```

#### Theorem 5.1 (Tractability Transfer)
*If $A \le_p B$ and $B \in \text{P}$, then $A \in \text{P}$.*

**Formal Proof:**
1. Since $B \in \text{P}$, there exists a DTM $M_B$ that decides $B$ in polynomial time bounded by $p_B(m)$, where $m$ is the input size to $M_B$.
2. Since $A \le_p B$, there exists an algorithm that computes reduction function $f$ in polynomial time bounded by $p_f(n)$, where $n = |x|$ is the size of instance $x$.
3. The size of the reduced output $f(x)$ cannot exceed the time taken to write it:
   $$|f(x)| \le p_f(n)$$
4. We construct algorithm $M_A$ to decide $A$ on input $x$:
   - **Step 1:** Compute $f(x)$ in time $p_f(n)$.
   - **Step 2:** Run $M_B$ on the transformed string $f(x)$.
   - **Step 3:** If $M_B(f(x))$ accepts, accept; otherwise, reject.
5. Correctness follows directly from the reduction invariant:
   $$M_A(x) = \text{ACCEPT} \iff M_B(f(x)) = \text{ACCEPT} \iff f(x) \in B \iff x \in A$$
6. The total running time of $M_A$ on input $x$ of length $n$ is:
   $$\mathcal{T}_{M_A}(n) = \mathcal{T}_{\text{reduction}}(n) + \mathcal{T}_{M_B}(|f(x)|) \le p_f(n) + p_B(p_f(n))$$
7. Because the composition of two polynomials $p_B(p_f(n))$ is itself a polynomial, the total runtime is bounded by a polynomial in $n$.
8. Hence, $A \in \text{P}$. $\blacksquare$

#### Corollary 5.2 (Intractability Propagation — The Contrapositive)
*If $A \le_p B$ and $A \notin \text{P}$, then $B \notin \text{P}$.*

---

### 5.3 Transitivity of Polynomial Reductions

#### Theorem 5.3 (Transitivity)
*If $A \le_p B$ and $B \le_p C$, then $A \le_p C$.*

**Formal Proof:**
1. Let $f: \Sigma_A^* \to \Sigma_B^*$ be the reduction from $A$ to $B$, running in time $p_f(n)$ such that:
   $$x \in A \iff f(x) \in B$$
2. Let $g: \Sigma_B^* \to \Sigma_C^*$ be the reduction from $B$ to $C$, running in time $p_g(m)$ such that:
   $$y \in B \iff g(y) \in C$$
3. Define the composite function $h: \Sigma_A^* \to \Sigma_C^*$ as:
   $$h(x) = g(f(x))$$
4. Equivalence check:
   $$x \in A \iff f(x) \in B \iff g(f(x)) \in C \iff h(x) \in C$$
5. Time complexity:
   - Computing $f(x)$ takes time $p_f(|x|)$ and produces an output string of length at most $p_f(|x|)$.
   - Computing $g(f(x))$ takes time $p_g(|f(x)|) \le p_g(p_f(|x|))$.
   - Total time: $p_f(|x|) + p_g(p_f(|x|))$, which is a polynomial in $|x|$.
6. Thus, $h$ is a valid polynomial-time reduction, establishing $A \le_p C$. $\blacksquare$

---

## 6. The Classes NP-Hard and NP-Complete

With polynomial reductions established, we can now define the apex classes of complexity theory.

### 6.1 Formal Definitions

#### Definition 6.1 (NP-Hard)
A language or problem $H$ is **NP-Hard** if every language $L$ in NP is polynomial-time reducible to $H$:
$$\forall \; L \in \text{NP}, \quad L \le_p H$$

*Crucial Architectural Distinction:* An NP-Hard problem **does not need to be in NP**. In fact:
- It does not even need to be a decision problem (e.g., optimization versions like TSP-Optimization are NP-Hard).
- It does not even need to be decidable (e.g., Turing's **Halting Problem** is NP-Hard because any NP problem can be reduced to the Halting Problem, yet the Halting Problem is undecidable).

#### Definition 6.2 (NP-Complete)
A language $X$ is **NP-Complete (NPC)** if and only if it satisfies two conditions:
1. $X \in \text{NP}$ (Membership: its solutions can be verified in polynomial time).
2. $X$ is **NP-Hard** (Hardness: $\forall L \in \text{NP}, \; L \le_p X$).

```
                    +─────────────────────────────────────+
                    |               NP-HARD               |
                    |  (At least as hard as all of NP)    |
                    |                                     |
                    |   +─────────────────────────────+   |
                    |   |             NP              |   |
                    |   |  +───────────────────────+  |   |
                    |   |  |      NP-COMPLETE      |  |   |
                    |   |  |   (NP ∩ NP-Hard)      |  |   |
                    |   |  +───────────────────────+  |   |
                    |   +─────────────────────────────+   |
                    +─────────────────────────────────────+
```

---

### 6.2 Venn Diagrams: The Structure of the Computational Universe

The structural relationship between P, NP, NP-Complete, and NP-Hard depends entirely on whether $\text{P} \ne \text{NP}$ or $\text{P} = \text{NP}$.

#### Scenario A: If $\text{P} \ne \text{NP}$ (The Widely Accepted Consensus)

```text
================================================================================
                           COMPLEXITY UNIVERSE (P ≠ NP)
================================================================================

      NP-HARD (Outside NP)
      +----------------------------------------------------------------+
      |  Halting Problem, TSP Optimization, Generalized Chess (n x n)   |
      |                                                                |
      |   NP (Nondeterministic Polynomial Time)                        |
      |   +--------------------------------------------------------+   |
      |   |                                                        |   |
      |   |   NP-COMPLETE                                          |   |
      |   |   +------------------------------------------------+   |   |
      |   |   | 3-SAT, SAT, Hamiltonian Cycle, CLIQUE,         |   |   |
      |   |   | Vertex Cover, Subset Sum, TSP Decision         |   |   |
      |   |   +------------------------------------------------+   |   |
      |   |                                                        |   |
      |   |   NP-INTERMEDIATE (Ladner's Theorem: Neither P nor NPC)|   |
      |   |   [ Graph Isomorphism, Integer Factorization ]         |   |
      |   |                                                        |   |
      |   |   P (Polynomial Time)                                  |   |
      |   |   +------------------------------------------------+   |   |
      |   |   | Shortest Path (Dijkstra), MST (Kruskal),       |   |   |
      |   |   | 2-SAT, Sorting, Matrix Mult, Max-Flow          |   |   |
      |   |   +------------------------------------------------+   |   |
      |   +--------------------------------------------------------+   |
      +----------------------------------------------------------------+
```

#### Scenario B: If $\text{P} = \text{NP}$ (The Algorithmic Collapse)

```text
================================================================================
                           COMPLEXITY UNIVERSE (P = NP)
================================================================================

      NP-HARD (Outside NP)
      +----------------------------------------------------------------+
      |  Halting Problem, TSP Optimization                             |
      |                                                                |
      |   P = NP = NP-COMPLETE                                         |
      |   +--------------------------------------------------------+   |
      |   |                                                        |   |
      |   |   All problems in NP are solvable in polynomial time   |   |
      |   |   Every non-trivial problem in P is NP-Complete!       |   |
      |   |                                                        |   |
      |   |   3-SAT = Shortest Path = Graph Coloring = Sorting     |   |
      |   |                                                        |   |
      |   +--------------------------------------------------------+   |
      +----------------------------------------------------------------+
```

---

## 7. The Cook-Levin Theorem

Before 1971, the concept of NP-Completeness did not exist because there was a fundamental **bootstrapping problem**:
> *To prove that a problem $B$ is NP-Complete, you must show that **every single problem** in NP reduces to $B$ ($L \le_p B$ for all $L \in \text{NP}$). But how do you prove this for the very first problem, when there are infinitely many problems in NP?*

Stephen Cook (1971) in the USA and Leonid Levin (1973) independently in the USSR resolved this paradox by proving that the **Boolean Satisfiability Problem (SAT)** is NP-Complete directly from first principles.

### 7.1 The Boolean Satisfiability Problem (SAT)
- **Input:** A Boolean propositional formula $\phi$ consisting of $n$ variables $x_1, x_2, \dots, x_n$, logical operators $\land$ (AND), $\lor$ (OR), and $\neg$ (NOT).
- **Question:** Does there exist a truth assignment $\tau: \{x_1, \dots, x_n\} \to \{0, 1\}$ such that $\phi(\tau) = 1$ (evaluates to TRUE)?

---

### 7.2 Proof Blueprint of the Cook-Levin Theorem

#### Theorem 7.1 (Cook-Levin Theorem)
$$\text{SAT is NP-Complete}$$

**High-Level Proof Architecture:**
1. **SAT is in NP:** Given a candidate truth assignment $\tau$, evaluate the formula in $\mathcal{O}(|\phi|)$ time. This is polynomial.
2. **SAT is NP-Hard:** We must prove that for **any** arbitrary language $L \in \text{NP}$, $L \le_p \text{SAT}$.
   - Since $L \in \text{NP}$, there exists an NDTM $M = (Q, \Sigma, \Gamma, \delta, q_0, q_{\text{accept}}, q_{\text{reject}})$ that decides $L$ in polynomial time $p(n)$ on input $x$ of length $n$.
   - Any computation of $M$ running for $T = p(n)$ steps can be laid out as a two-dimensional **Computation Tableau** of size $T \times T$:
     * Rows represent time steps $t \in \{0, 1, \dots, T\}$.
     * Columns represent tape cells $i \in \{1, 2, \dots, T\}$.

```text
Time (t)
   0   | q0 | x1 | x2 | x3 |  _ |  _ | ... |  _ |   <-- Initial Configuration
   1   |  _ | q1 | x2 | x3 |  _ |  _ | ... |  _ |   <-- Head moves right
   2   |  _ | a  | q2 | x3 |  _ |  _ | ... |  _ |
  ...  | ...
   T   |  _ | ...| q_acc | ...                     <-- Reaches Accepting State
       +-----------------------------------------
         1    2    3    4    5    6  ...   T       Tape Cells (i)
```

Cook encoded the physical validity of this entire computation tableau into a single Boolean formula:
$$\Phi_{M, x} = \phi_{\text{cell}} \land \phi_{\text{state}} \land \phi_{\text{head}} \land \phi_{\text{init}} \land \phi_{\text{trans}} \land \phi_{\text{accept}}$$

Each sub-formula enforces a non-negotiable physical constraint of the Turing machine:
1. **$\phi_{\text{cell}}$ (Single Symbol Invariant):** Every tape cell $(i, t)$ contains exactly one symbol from tape alphabet $\Gamma$ at time $t$.
2. **$\phi_{\text{state}}$ (Single State Invariant):** At each time step $t$, machine $M$ is in exactly one state $q \in Q$.
3. **$\phi_{\text{head}}$ (Single Head Position):** At each time step $t$, the read/write head is situated over exactly one tape cell $i$.
4. **$\phi_{\text{init}}$ (Valid Start):** At time $t = 0$, the tape contains the input string $x$, the head is at cell 1, and the control state is $q_0$.
5. **$\phi_{\text{trans}}$ (Local Transition Logic):** The contents of cell $i$ at time $t+1$ depend solely on the contents of the $2 \times 3$ window around cell $i$ at time $t$, matching a valid transition in $\delta$.
6. **$\phi_{\text{accept}}$ (Acceptance):** At the final step $T$, the machine enters $q_{\text{accept}}$.

**The Crucial Insight:**  
Formula $\Phi_{M, x}$ is satisfiable **if and only if** there exists an accepting computation history for machine $M$ on input $x$.  
Furthermore:
- The size of formula $\Phi_{M, x}$ is $\mathcal{O}(T^2) = \mathcal{O}(p(n)^2)$, which is polynomial in $n$.
- Constructing the formula takes polynomial time.
- Thus, $x \in L \iff \Phi_{M, x} \in \text{SAT}$.

Because this reduction holds for *any* arbitrary language $L \in \text{NP}$, **SAT is NP-Hard**. Combined with $\text{SAT} \in \text{NP}$, SAT is **NP-Complete**. $\blacksquare$

---

## 8. The 4-Step Recipe for Proving NP-Completeness

With the Cook-Levin theorem establishing the foundation, proving any subsequent problem $Q$ is NP-Complete no longer requires modeling Turing machines. Instead, we use **transitivity of polynomial reductions**.

```
Known NPC Problem (Q') ──────────[ Polynomial Reduction f ]──────────> New Target Problem (Q)
```

### The Universal 4-Step Protocol:

```
[ Step 1: Prove Q ∈ NP ]
  - Define a polynomial certificate y.
  - Write deterministic verifier V(x, y).
  - Prove V runs in O(n^k) time.
            |
            v
[ Step 2: Select Known NPC Problem Q' ]
  - Choose Q' closely matching the combinatorial structure of Q.
            |
            v
[ Step 3: Construct Reduction Function f: Q' -> Q ]
  - Detail algorithmic transformation converting any instance x ∈ Q' to f(x) ∈ Q.
  - Prove the construction executes in polynomial time O(n^c).
            |
            v
[ Step 4: Prove Correctness (Bi-Directional Invariant) ]
  - (=>) Forward: If x ∈ Q', then f(x) ∈ Q (Soundness).
  - (<=) Reverse: If f(x) ∈ Q, then x ∈ Q' (Completeness).
```

---

## 9. Comprehensive 5W1H Reduction Trace: 3-SAT to CLIQUE

To see the 4-step recipe in action, we trace a complete reduction from **3-SAT** to **CLIQUE**.

### 9.1 Problem Specifications
- **3-SAT:** Given a Boolean formula in Conjunctive Normal Form (CNF) where each clause contains exactly 3 distinct literals:
  $$\phi = C_1 \land C_2 \land \dots \land C_m \quad \text{with } C_r = (l_{r, 1} \lor l_{r, 2} \lor l_{r, 3})$$
  Is $\phi$ satisfiable? (Known to be NP-Complete).
- **CLIQUE:** Given an undirected graph $G = (V, E)$ and integer $k$, does $G$ contain a clique (a complete subgraph where every pair is connected) of size $\ge k$?

---

### Step 1: Membership in NP (CLIQUE $\in$ NP)

- **What are we doing?** Demonstrating that CLIQUE satisfies the polynomial verifier condition.
- **Why are we starting here?** A problem cannot be NP-Complete unless it is proven to be in NP.
- **How do we execute the step mechanically?**
  1. **Certificate $y$:** A subset of vertices $V' \subseteq V$.
  2. **Polynomial Verifier Algorithm:**
     - Check if $|V'| = k$. If not, output $\text{REJECT}$.
     - For every pair of vertices $u, v \in V'$ with $u \ne v$:
       * Query the adjacency matrix of $G$ to determine if edge $(u, v) \in E$.
       * If edge $(u, v) \notin E$, output $\text{REJECT}$.
     - If all $\binom{k}{2} = \frac{k(k-1)}{2}$ edges exist, output $\text{ACCEPT}$.
  3. **Runtime Analysis:** The number of vertex pairs checked is $\mathcal{O}(k^2) \le \mathcal{O}(|V|^2)$. Each edge check takes $\mathcal{O}(1)$ time. Total verification time is $\mathcal{O}(|V|^2)$, which is strictly polynomial.
- **Conclusion:** $\text{CLIQUE} \in \text{NP}$.

---

### Step 2: Source Problem Selection

- **What are we doing?** Selecting $Q' = \text{3-SAT}$.
- **Why this choice?** 3-SAT provides a natural clause-literal structure that maps directly to clusters of vertices in a graph.

---

### Step 3: Reduction Construction ($f: \text{3-SAT} \to \text{CLIQUE}$)

- **What are we doing?** Converting an arbitrary 3-CNF formula $\phi$ with $m$ clauses into a graph $G = (V, E)$ and target integer $k$.
- **How do we execute the step mechanically?**
  1. **Vertex Set $V$:** For each clause $C_r = (l_{r, 1} \lor l_{r, 2} \lor l_{r, 3})$ ($r \in \{1, \dots, m\}$), create a cluster of 3 vertices, one for each literal position:
     $$V = \{v_{r, 1}, v_{r, 2}, v_{r, 3} \mid r \in \{1, 2, \dots, m\}\}$$
     Total number of vertices: $|V| = 3m$.
  2. **Edge Set $E$:** Add an undirected edge between two vertices $v_{r, i}$ and $v_{s, j}$ if and only if:
     - **Different Clauses:** $r \ne s$ (never connect vertices residing in the same clause cluster).
     - **Consistency:** Literals are not complementary ($l_{r, i} \ne \neg l_{s, j}$).
  3. **Target Clique Size:**
     $$k = m \quad (\text{the total number of clauses})$$
- **Where did this formula originate?** To satisfy formula $\phi$, we must pick at least one true literal from every clause without selecting contradictory literals ($x$ and $\neg x$). The graph encodes this: an edge represents a mutually compatible assignment between different clauses.
- **Runtime of Reduction:**
  - Generating $3m$ vertices takes $\mathcal{O}(m)$ time.
  - Evaluating pairs of vertices takes $\binom{3m}{2} \approx \frac{9m^2}{2} = \mathcal{O}(m^2)$ comparisons.
  - Total reduction runtime is $\mathcal{O}(m^2)$, which is polynomial.

---

### Step 4: Concrete Instance Construction Trace

Let us trace the reduction on a concrete 3-CNF formula with $m = 2$ clauses over variables $\{x_1, x_2, x_3\}$:
$$\phi = C_1 \land C_2 = (x_1 \lor x_2 \lor x_3) \land (\neg x_1 \lor \neg x_2 \lor x_3)$$

#### Generated Graph Components:
1. **Target Clique Size:** $k = m = 2$.
2. **Vertices ($3 \times 2 = 6$ vertices):**
   - Cluster 1 ($C_1$): $v_{1, 1} = x_1, \; v_{1, 2} = x_2, \; v_{1, 3} = x_3$
   - Cluster 2 ($C_2$): $v_{2, 1} = \neg x_1, \; v_{2, 2} = \neg x_2, \; v_{2, 3} = x_3$
3. **Edges (Connect between $C_1$ and $C_2$ if not contradictory):**
   - From $v_{1, 1} = x_1$:
     * To $v_{2, 1} = \neg x_1$: **NO EDGE** (Contradiction: $x_1$ conflicts with $\neg x_1$).
     * To $v_{2, 2} = \neg x_2$: **EDGE EXISTS** ($(x_1, \neg x_2) \in E$).
     * To $v_{2, 3} = x_3$: **EDGE EXISTS** ($(x_1, x_3) \in E$).
   - From $v_{1, 2} = x_2$:
     * To $v_{2, 1} = \neg x_1$: **EDGE EXISTS** ($(x_2, \neg x_1) \in E$).
     * To $v_{2, 2} = \neg x_2$: **NO EDGE** (Contradiction: $x_2$ conflicts with $\neg x_2$).
     * To $v_{2, 3} = x_3$: **EDGE EXISTS** ($(x_2, x_3) \in E$).
   - From $v_{1, 3} = x_3$:
     * To $v_{2, 1} = \neg x_1$: **EDGE EXISTS** ($(x_3, \neg x_1) \in E$).
     * To $v_{2, 2} = \neg x_2$: **EDGE EXISTS** ($(x_3, \neg x_2) \in E$).
     * To $v_{2, 3} = x_3$: **EDGE EXISTS** ($(x_3, x_3) \in E$).

```text
       Cluster C1 (Clause 1)              Cluster C2 (Clause 2)
       +--------------------+            +--------------------+
       |  (v_1,1: x1)       |            |  (v_2,1: ¬x1)      |
       |                    |     \ /    |                    |
       |  (v_1,2: x2)       |======X=====|  (v_2,2: ¬x2)      |
       |                    |     / \    |                    |
       |  (v_1,3: x3)-------|------------|--(v_2,3: x3)       |
       +--------------------+            +--------------------+
```

---

### Step 5: Equivalence Proof ($\phi \in \text{3-SAT} \iff G \text{ has Clique of Size } k$)

- **What are we doing?** Proving both forward (soundness) and backward (completeness) directions.

#### Forward Direction ($\implies$): If $\phi$ is satisfiable, then $G$ contains a clique of size $k = m$.
1. If $\phi$ is satisfiable, there exists a truth assignment $\tau$ such that every clause $C_r$ evaluates to TRUE.
2. Therefore, in every clause $C_r$, there exists at least one literal $l_{r, i_r}$ that evaluates to TRUE under $\tau$.
3. Select the corresponding vertex $v_{r, i_r}$ from each of the $m$ clusters. This yields a set $V'$ of exactly $m$ vertices:
   $$V' = \{v_{1, i_1}, v_{2, i_2}, \dots, v_{m, i_m}\} \quad \text{with } |V'| = m$$
4. Consider any pair of vertices $u = v_{r, i_r}$ and $w = v_{s, i_s}$ in $V'$ with $r \ne s$:
   - By selection, both literals $l_{r, i_r}$ and $l_{s, i_s}$ are TRUE under truth assignment $\tau$.
   - Two literals that are both TRUE under the same valid assignment cannot be complementary ($l_{r, i_r} \ne \neg l_{s, i_s}$).
   - Furthermore, $r \ne s$ because they come from different clause clusters.
   - Therefore, by our edge construction rules, edge $(u, w)$ must exist in $E$.
5. Since every pair in $V'$ is connected by an edge, $V'$ forms a complete subgraph (a clique) of size $m = k$.

#### Backward Direction ($\impliedby$): If $G$ contains a clique of size $k = m$, then $\phi$ is satisfiable.
1. Suppose $G$ contains a clique $V'$ of size $|V'| = m$.
2. By construction, no edge exists between any two vertices in the same clause cluster.
3. Therefore, a clique cannot contain more than one vertex from any single cluster.
4. Because $|V'| = m$ and there are exactly $m$ clusters, **clique $V'$ must contain exactly one vertex from each cluster**:
   $$V' \cap \{v_{r, 1}, v_{r, 2}, v_{r, 3}\} = \{v_{r, i_r}\} \quad \forall \; r \in \{1, \dots, m\}$$
5. Because $V'$ is a clique, every pair of vertices in $V'$ is connected by an edge.
6. By our edge rule, no two vertices in $V'$ can represent complementary literals (edges between complementary literals were explicitly prohibited).
7. Construct truth assignment $\tau$:
   - For every vertex $v_{r, i_r} \in V'$, assign its literal $l_{r, i_r} = 1$.
   - If a variable $x_j$ does not appear in $V'$ (in either positive or negated form), assign it an arbitrary truth value (e.g., $x_j = 0$).
8. Because no complementary literals were chosen, assignment $\tau$ is mathematically consistent (no variable is simultaneously set to 0 and 1).
9. Under $\tau$, at least one literal in each clause $C_r$ is TRUE. Thus, all $m$ clauses are satisfied, meaning $\phi(\tau) = 1$.
10. Formula $\phi$ is satisfiable. $\blacksquare$

---

## 10. The Classical Web of NP-Complete Reductions

Richard Karp's seminal 1972 paper, *"Reducibility Among Combinatorial Problems"*, proved that 21 diverse problems across graph theory, set theory, and number theory are all NP-Complete by establishing a chain of reductions originating from Cook's SAT.

```text
                                [ SAT ]
                                   |
                                   v
                               [ 3-SAT ]
                                   |
          +------------------------+------------------------+
          |                        |                        |
          v                        v                        v
      [ CLIQUE ]            [ 3D-MATCHING ]           [ SUBSET-SUM ]
          |                        |                        |
          v                        v                        v
   [ VERTEX-COVER ]         [ EXACT-COVER ]            [ KNAPSACK ]
          |                        |                        |
          +--------+               v                        v
          |        |       [ HAMILTONIAN-CYCLE ]      [ PARTITION ]
          v        v               |
    [ INDEP-SET ] [ GRAPH-COLOR]   v
                             [ TSP-DECISION ]
```

---

## 11. KTU High-Yield Examination Preparation

This section provides model answers for questions frequently set in KTU examinations under the 2024 scheme for course code **PCCST502 / CST306**.

---

### Question 1 (3 Marks): Distinguish between NP-Hard and NP-Complete classes.

#### Model Answer:
| Attribute | NP-Hard Class | NP-Complete Class |
| :--- | :--- | :--- |
| **Membership in NP** | Not required to be in NP ($H \notin \text{NP}$ is allowed). | **Must belong to NP** ($X \in \text{NP}$). |
| **Verification Property** | Solutions might not be verifiable in polynomial time (can be undecidable). | Solutions are guaranteed to be verifiable in deterministic polynomial time. |
| **Problem Formulation** | Can be optimization problems, decision problems, or undecidable problems (e.g., TSP-Optimization, Halting Problem). | Strictly **decision problems** (e.g., 3-SAT, Clique, Hamiltonian Cycle). |
| **Formal Definition** | $H$ is NP-Hard if $\forall L \in \text{NP}, \; L \le_p H$. | $X$ is NP-Complete if $X \in \text{NP}$ and $X$ is NP-Hard. |

---

### Question 2 (3 Marks): What is a polynomial-time reduction? State its significance.

#### Model Answer:
- **Definition:** A language $A$ is polynomial-time reducible to language $B$ ($A \le_p B$) if there exists a function $f: \Sigma^* \to \Sigma^*$ computable in deterministic polynomial time such that for all instances $x$:
  $$x \in A \iff f(x) \in B$$
- **Significance:**
  1. **Tractability Transfer:** If $B \in \text{P}$, then $A \in \text{P}$ (an efficient solver for $B$ solves $A$).
  2. **Intractability Propagation:** If $A$ is known to be hard ($A \notin \text{P}$), then $B$ must also be hard ($B \notin \text{P}$). This provides the primary mathematical mechanism for proving problems are NP-Complete.

---

### Question 3 (5 Marks): Prove that if any NP-Complete problem can be solved in polynomial time, then $P = NP$.

#### Model Answer:
1. Let $X$ be an NP-Complete problem, and suppose $X \in \text{P}$.
2. We must prove that every language $L \in \text{NP}$ is also in $\text{P}$, which will establish $\text{NP} \subseteq \text{P}$.
3. Take any arbitrary language $L \in \text{NP}$.
4. By the definition of NP-Completeness, $X$ is NP-Hard, meaning every language in NP reduces to $X$ in polynomial time:
   $$L \le_p X$$
5. By Theorem 5.1 (Tractability Transfer), if $L \le_p X$ and $X \in \text{P}$, then:
   $$L \in \text{P}$$
6. Because language $L$ was chosen arbitrarily from NP, this inclusion holds for all languages in NP:
   $$\text{NP} \subseteq \text{P}$$
7. Since it is already mathematically established that $\text{P} \subseteq \text{NP}$ (Theorem 4.2), combining both inclusions gives:
   $$\text{P} \subseteq \text{NP} \quad \text{and} \quad \text{NP} \subseteq \text{P} \implies \text{P} = \text{NP}$$
Thus, solving a single NP-Complete problem in polynomial time causes the entire class NP to collapse into P. $\blacksquare$

---

### Question 4 (10 Marks): Explain the Cook-Levin Theorem. Outline the four steps required to prove that a new problem is NP-Complete, and illustrate with a neat diagram.

#### Model Answer Structure:
1. **Cook-Levin Theorem Statement:** State Theorem 7.1. Explain its historical significance in solving the bootstrapping problem of NP-completeness. *(2 Marks)*
2. **Proof Blueprint Overview:** Briefly describe how an arbitrary NDTM $M$ deciding language $L$ in polynomial time is mapped to a Boolean formula $\Phi_{M, x}$ using a $T \times T$ computation tableau, showing that $\Phi_{M, x}$ is satisfiable if and only if $M$ accepts $x$. *(3 Marks)*
3. **The 4-Step NP-Completeness Proof Recipe:**
   - Step 1: Prove $Q \in \text{NP}$ by providing a polynomial certificate and deterministic verifier.
   - Step 2: Select a known NP-Complete problem $Q'$.
   - Step 3: Construct a reduction function $f: Q' \to Q$ and prove it runs in polynomial time.
   - Step 4: Prove correctness in both directions ($x \in Q' \iff f(x) \in Q$). *(3 Marks)*
4. **Venn Diagram & Reduction Pipeline:** Draw the relationships between P, NP, NP-Complete, and NP-Hard (for $\text{P} \ne \text{NP}$), and diagram the reduction pipeline $Q' \xrightarrow{f} Q$. *(2 Marks)*

---

## 12. Summary Reference Matrix of Complexity Classes

```text
+==================================================================================================+
|                                MASTER COMPLEXITY CLASSIFICATION                                  |
+==============+=======================================+======================+====================+
| Class        | Formal Operational Definition         | Verification Bound   | Prototypical Member|
+==============+=======================================+======================+====================+
| P            | Decidable in deterministic poly-time  | Poly-time solvable   | Shortest Path,     |
|              | TIME(n^k)                             | (Verification=Solve) | MST, 2-SAT         |
+--------------+---------------------------------------+----------------------+--------------------+
| NP           | Verifiable in deterministic poly-time | Poly-time verifiable | 3-SAT, CLIQUE,     |
|              | with polynomial certificate           | with given witness   | Hamiltonian Cycle  |
+--------------+---------------------------------------+----------------------+--------------------+
| Co-NP        | Languages whose complement is in NP   | Poly-time verifiable | Tautology,         |
|              | (L ∈ Co-NP <=> L^c ∈ NP)              | NO-instances         | Unsatisfiability   |
+--------------+---------------------------------------+----------------------+--------------------+
| NP-Complete  | In NP and NP-Hard                     | Poly-time verifiable | 3-SAT, CLIQUE,     |
|              | (X ∈ NP and ∀L∈NP, L ≤_p X)           | hardest in NP        | Vertex Cover, TSP-D|
+--------------+---------------------------------------+----------------------+--------------------+
| NP-Hard      | At least as hard as any NP problem    | May not be in NP;    | Halting Problem,   |
|              | (∀L∈NP, L ≤_p H)                      | can be undecidable   | TSP Optimization   |
+==============+=======================================+======================+====================+
```
