# Progressive Problems: NP-Completeness Reduction Gadgets (3-SAT, CLIQUE, and VERTEX-COVER)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps. Assume the reader has zero prior mathematical background beyond basic logic and graph terms.

---

## Level 1: 3-SAT to CLIQUE Gadget Construction & Truth Assignment Extraction

### Problem 1.1: Complete Gadget Construction for a 3-Clause Boolean Formula

Consider the 3-CNF Boolean formula $\phi$ with $m = 3$ clauses over variables $\{x_1, x_2, x_3\}$:

$$\phi = C_1 \land C_2 \land C_3 = (x_1 \lor x_2 \lor \overline{x_3}) \land (\overline{x_1} \lor x_2 \lor x_3) \land (x_1 \lor \overline{x_2} \lor x_3)$$

1. Construct the graph $G = (V, E)$ using the standard 3-SAT to CLIQUE reduction.
2. Determine the target clique size $k$.
3. Identify a clique of size $k$ in the generated graph.
4. Extract the satisfying truth assignment for variables $x_1, x_2, x_3$ from the clique vertices.

::: callout-intuition Core Mental Model
Imagine each clause is a 3-person committee. 
* To make the whole system happy, you need to select exactly one representative from each committee who agrees with everyone else chosen.
* Two people can shake hands (share an edge) if and only if they are from different committees and do not hold opposite opinions (one doesn't say "I am true" while the other says "I am false").
* A clique of size 3 is a trio of representatives from all 3 committees who all shake hands with each other!
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Vertex Set Construction</summary>

Each clause generates 3 vertices (one for each of its literals).
Total vertices: $|V| = 3 \times m = 3 \times 3 = 9$.

* **Clause 1 ($C_1 = x_1 \lor x_2 \lor \overline{x_3}$):**
  $$v_1 = (1, x_1), \quad v_2 = (1, x_2), \quad v_3 = (1, \overline{x_3})$$
* **Clause 2 ($C_2 = \overline{x_1} \lor x_2 \lor x_3$):**
  $$u_1 = (2, \overline{x_1}), \quad u_2 = (2, x_2), \quad u_3 = (2, x_3)$$
* **Clause 3 ($C_3 = x_1 \lor \overline{x_2} \lor x_3$):**
  $$w_1 = (3, x_1), \quad w_2 = (3, \overline{x_2}), \quad w_3 = (3, x_3)$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Edge Connection Rules and Filtering</summary>

An edge exists between vertex $a$ and vertex $b$ if and only if:
1. $a$ and $b$ belong to **different clauses** ($C_r \ne C_s$).
2. The literals of $a$ and $b$ are **not negations of each other** ($l_a \ne \overline{l_b}$).

*Pairs that CANNOT have an edge:*
* Within same clause: No edges among $\{v_1, v_2, v_3\}$, $\{u_1, u_2, u_3\}$, $\{w_1, w_2, w_3\}$.
* Contradictions:
  * $v_1(x_1)$ and $u_1(\overline{x_1})$ $\implies$ NO EDGE.
  * $u_1(\overline{x_1})$ and $w_1(x_1)$ $\implies$ NO EDGE.
  * $v_2(x_2)$ and $w_2(\overline{x_2})$ $\implies$ NO EDGE.
  * $u_2(x_2)$ and $w_2(\overline{x_2})$ $\implies$ NO EDGE.
  * $v_3(\overline{x_3})$ and $u_3(x_3)$ $\implies$ NO EDGE.
  * $v_3(\overline{x_3})$ and $w_3(x_3)$ $\implies$ NO EDGE.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Target Clique Parameter & Clique Discovery</summary>

* Target Clique Size:
  $$\mathbf{k = m = 3}$$

* We seek 3 mutually adjacent vertices, one from each clause:
  * Consider selecting $x_2$ from Clause 1: $v_2 = (1, x_2)$.
  * In Clause 2, select $x_2$: $u_2 = (2, x_2)$.
    * Check edge $(v_2, u_2)$: Different clauses ($1 \ne 2$), non-contradictory ($x_2$ and $x_2$). **Edge exists!**
  * In Clause 3, select $x_1$: $w_1 = (3, x_1)$.
    * Check edge $(v_2, w_1)$: Different clauses ($1 \ne 3$), non-contradictory ($x_2$ and $x_1$). **Edge exists!**
    * Check edge $(u_2, w_1)$: Different clauses ($2 \ne 3$), non-contradictory ($x_2$ and $x_1$). **Edge exists!**

* The vertex set:
  $$\mathbf{V' = \{ (1, x_2), \; (2, x_2), \; (3, x_1) \}}$$
  forms a **complete triangle (clique of size 3)** in graph $G$!
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Truth Assignment Extraction and Verification</summary>

From our clique vertices:
* $(1, x_2) \implies$ Set $x_2 = \mathbf{\text{True}}$.
* $(2, x_2) \implies$ Set $x_2 = \mathbf{\text{True}}$ (Consistent!).
* $(3, x_1) \implies$ Set $x_1 = \mathbf{\text{True}}$.
* Variable $x_3$ did not appear in our clique: Set $x_3 = \text{True}$ (or False arbitrarily).

#### Verification in Formula $\phi$:
* Clause 1: $(x_1 \lor x_2 \lor \overline{x_3}) = (\text{True} \lor \text{True} \lor \text{False}) = \mathbf{\text{True}}$.
* Clause 2: $(\overline{x_1} \lor x_2 \lor x_3) = (\text{False} \lor \text{True} \lor \text{True}) = \mathbf{\text{True}}$.
* Clause 3: $(x_1 \lor \overline{x_2} \lor x_3) = (\text{True} \lor \text{False} \lor \text{True}) = \mathbf{\text{True}}$.

All 3 clauses are satisfied!
$$\mathbf{\phi(\text{True}, \text{True}, \text{True}) = \text{True}}$$
</details>

</div>

---

## Level 2: Graph Complement and Vertex Cover Reduction

### Problem 2.1: Transforming a 5-Vertex Clique Instance into Vertex Cover

Given graph $G = (V, E)$ with $|V| = 5$ and edge set:
$$E = \{ (1, 2), (2, 3), (3, 1), (1, 4), (2, 4), (3, 4), (4, 5) \}$$

1. Identify a maximum clique $V'$ in $G$ and state its size $k$.
2. Construct the exact complement graph $\overline{G} = (V, \overline{E})$.
3. Compute the target vertex cover size $k' = |V| - k$.
4. Verify that $V'' = V \setminus V'$ is a valid vertex cover of size $k'$ in $\overline{G}$.

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Identifying the Clique in G</summary>

Inspect edges among vertices $\{1, 2, 3, 4\}$:
* $(1, 2) \in E$, $(2, 3) \in E$, $(3, 1) \in E$ (Triangle $1-2-3$)
* Vertex 4 is connected to 1, 2, and 3: $(1, 4) \in E, (2, 4) \in E, (3, 4) \in E$.
* All $\binom{4}{2} = 6$ possible edges among $\{1, 2, 3, 4\}$ exist in $E$.
* Therefore:
  $$\mathbf{V' = \{1, 2, 3, 4\} \text{ is a Clique of size } k = 4}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Constructing the Complement Graph \overline{G}</summary>

The complete graph on 5 vertices has $\binom{5}{2} = 10$ edges.
* Original edges in $E$ ($7$ edges): $(1, 2), (2, 3), (3, 1), (1, 4), (2, 4), (3, 4), (4, 5)$.
* Complement edges $\overline{E}$ (pairs NOT in $E$, total $10 - 7 = 3$ edges):
  $$\mathbf{\overline{E} = \{ (1, 5), \; (2, 5), \; (3, 5) \}}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Calculating Target Vertex Cover Parameter</summary>

* $|V| = 5$
* Clique size $k = 4$
* Target Vertex Cover size:
  $$\mathbf{k' = |V| - k = 5 - 4 = 1}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Extracting and Verifying Vertex Cover in \overline{G}</summary>

* Candidate Vertex Cover:
  $$\mathbf{V'' = V \setminus V' = \{1, 2, 3, 4, 5\} \setminus \{1, 2, 3, 4\} = \{ 5 \}}$$
* Size: $|V''| = 1 \le k'$.
* Check if $\{5\}$ covers all edges in $\overline{E} = \{ (1, 5), (2, 5), (3, 5) \}$:
  * Edge $(1, 5)$ has endpoint $5 \in V''$. (Covered!)
  * Edge $(2, 5)$ has endpoint $5 \in V''$. (Covered!)
  * Edge $(3, 5)$ has endpoint $5 \in V''$. (Covered!)

**Every edge in $\overline{G}$ is covered by vertex 5!**
Hence, $\{5\}$ is a valid vertex cover of size $k' = 1$.
</details>

</div>
