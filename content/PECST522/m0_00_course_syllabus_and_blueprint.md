# KTU Official Syllabus: Artificial Intelligence (PECST522)

Welcome to the comprehensive academic and examination blueprint for **Artificial Intelligence (PECST522)**, prescribed under the **APJ Abdul Kalam Technological University (KTU) 2024 Scheme for Semester 5 (S5) Computer Science and allied engineering branches**.

---

## 📋 Course Overview

<div class="table-wrap">

| Parameter | Specification Details |
| :--- | :--- |
| **Course Name** | **Artificial Intelligence** |
| **Course Code** | `PECST522` |
| **Semester** | **Semester 5 (S5)** |
| **Degree & Branch** | **B.Tech (Computer Science and Allied Streams)** |
| **Teaching Hours / Week** | **3:0:0:0** *(Lecture: 3 hrs, Tutorial: 0, Practical: 0, Remedial: 0)* |
| **Total Contact Hours** | **36 Contact Hours (8 + 10 + 8 + 10 Hours)** |
| **Course Credits** | **3 Credits** |
| **Course Type** | **Theory (Professional Elective)** |
| **Prerequisites** | **None** |
| **Continuous Internal Evaluation (CIE)** | **40 Marks** *(Min. 45% / 18 marks required for ESE eligibility)* |
| **End Semester Examination (ESE)** | **60 Marks** *(Min. 40% / 24 marks required to pass)* |
| **Total Marks** | **100 Marks** |
| **Examination Duration** | **2 Hours 30 Minutes (150 Minutes)** |

</div>

::: callout-intuition Rational Agents and Intelligent Reasoning
Artificial Intelligence is the study of building **rational agents**—computational entities that perceive their environment through sensors and act upon that environment through actuators to maximize expected performance. From uninformed state-space search and heuristic graph exploration ($A^*$), to logical theorem proving (Resolution, Unification) and reward-driven decision making (Reinforcement Learning), AI formalizes human cognition into rigorous algorithmic frameworks.
:::

---

## 🎯 Course Objectives

The primary pedagogical objectives of the course are:

1. **Foundations & Reasoning Abstractions**: To lay a solid mathematical and conceptual foundation of the important abstractions, state-space representations, search techniques, and logical reasoning for intelligent systems.
2. **Reinforcement Learning Principles**: To enable learners to understand the core principles, Bellman optimality formulations, and algorithmic architectures of Reinforcement Learning.

---

## 📚 Module-by-Module Syllabus Breakdown

### Module 1: Introduction to AI, Agents, and Problem Formulation (8 Contact Hours)

::: callout-exam Module 1 High-Yield Focus
Module 1 introduces agent theory and search problem formulation. Frequent KTU exam questions: Turing Test & definition of AI (Thinking vs Acting, Humanly vs Rationally), The PEAS framework specification for real-world agents (e.g., Automated Taxi, Medical Diagnosis, Robot Vacuum), Taxonomy of Task Environments (Observable, Deterministic, Episodic, Static, Discrete, Single-agent), Agent architectures (Simple reflex, Model-based, Goal-based, Utility-based, Learning agents), and 5-tuple state-space formulation for 8-Puzzle, Vacuum World, and 8-Queens.
:::

* **Foundations & History of Artificial Intelligence**:
  * Definitions of AI: Thinking Humanly (Cognitive Science), Thinking Rationally (Laws of Thought), Acting Humanly (Turing Test), Acting Rationally (Rational Agent approach).
  * Philosophical, mathematical, psychological, linguistic, and neurological roots; Dartmouth 1956 workshop; Milestones and AI winters.
* **Agents and Task Environments**:
  * **Agent Concept**: Sensors, Actuators, Percepts, Percept Sequences, and Agent Functions ($f: P^* \rightarrow A$).
  * **The Concept of Rationality**: Ideal rational agent, performance measures, autonomy, difference between rationality and omniscience.
  * **The PEAS Framework**: Specifying **P**erformance measure, **E**nvironment, **A**ctuators, and **S**ensors for diverse autonomous systems.
  * **The Nature of Task Environments**:
    * Fully Observable vs Partially Observable (vs Unobservable).
    * Single-Agent vs Multi-Agent (Competitive vs Cooperative).
    * Deterministic vs Stochastic vs Non-deterministic.
    * Episodic vs Sequential.
    * Static vs Dynamic (vs Semidynamic).
    * Discrete vs Continuous.
    * Known vs Unknown.
* **Structure and Types of Agents**:
  * Simple Reflex Agents (condition-action rules, sensory limitations).
  * Model-Based Reflex Agents (internal state tracking).
  * Goal-Based Agents (planning and future projection).
  * Utility-Based Agents (trade-off optimization and preference curves).
  * Learning Agents (Critic, Learning Element, Performance Element, Problem Generator).
* **Problem-Solving Agents & Problem Formulation**:
  * Well-defined problems and solutions: Initial State, Actions, Transition Model (`Result(s, a)`), Goal Test, Path Cost ($c(s, a, s')$).
  * Toy Problem Formulations:
    * **Vacuum Cleaner World**: 2-location states, movement actions, clean goal.
    * **8-Puzzle Problem**: Tile sliding, state space size ($9! / 2 = 181,440$), parity invariants.
    * **8-Queens Problem**: Incremental formulation vs Complete-state formulation.

---

### Module 2: Uninformed, Heuristic, Adversarial Search & CSPs (10 Contact Hours)

::: callout-exam Module 2 High-Yield Focus
Module 2 is the core problem-solving engine. High-yield KTU exam topics: Complete mathematical trace and criteria comparison (Time, Space, Completeness, Optimality) for BFS, DFS, UCS, and Iterative Deepening (IDS); $A^*$ algorithm graph exploration, admissible & consistent heuristics proofs ($h(n) \le c(n, a, n') + h(n')$); Constraint Satisfaction Problems (Constraint graph, Backtracking search, AC-3 algorithm); Minimax tree evaluations and step-by-step **Alpha-Beta Pruning** trace with branch cutoffs.
:::

* **Uninformed (Blind) Search Strategies**:
  * Breadth-First Search (BFS): Queue implementation, completeness, time $O(b^d)$, space $O(b^d)$, optimality for unit costs.
  * Depth-First Search (DFS): LIFO stack implementation, space efficiency $O(bm)$, vulnerability to infinite paths.
  * Uniform Cost Search (Dijkstra-based search for general positive step costs).
  * Depth-Limited Search (DLS) and **Iterative Deepening Search (IDS)**: Combines space efficiency of DFS ($O(bd)$) with completeness and optimality of BFS.
* **Heuristic (Informed) Search Strategies**:
  * Heuristic functions $h(n)$ (estimating cost from node $n$ to closest goal state); Effect of heuristic accuracy, effective branching factor ($b^*$).
  * Generate-and-Test search paradigms; Greedy Best-First Search (evaluating $f(n) = h(n)$).
  * **$A^*$ Search Algorithm**:
    * Evaluation function: $f(n) = g(n) + h(n)$ (cost so far + estimated remaining cost).
    * **Admissibility**: $h(n) \le h^*(n)$ guarantees optimality in tree search.
    * **Consistency (Monotonicity)**: $h(n) \le c(n, a, n') + h(n')$ guarantees optimality in graph search without reopening closed nodes.
    * Dominance between heuristics: If $h_2(n) \ge h_1(n)$ for all $n$, then $h_2$ dominates $h_1$ and explores fewer nodes.
* **Constraint Satisfaction Problems (CSP)**:
  * Formal CSP definition: Variables $X = \{X_1, \dots, X_n\}$, Domains $D = \{D_1, \dots, D_n\}$, Constraints $C = \{C_1, \dots, C_m\}$.
  * Constraint graphs; Example domains: Map Coloring (Australia), Cryptarithmetic puzzles (`SEND + MORE = MONEY`), N-Queens as CSP.
  * Backtracking search for CSPs: Variable selection heuristics (Minimum Remaining Values - MRV, Degree Heuristic), Value selection (Least Constraining Value - LCV).
  * Constraint Propagation: Forward Checking, Arc Consistency (**AC-3 Algorithm**).
* **Adversarial Search & Game Playing**:
  * Games as search problems: Deterministic, turn-taking, two-player, zero-sum games with perfect information.
  * **Minimax Algorithm**: Computing minimax values recursively; Depth-first game tree evaluation; Optimal decision against rational opponents.
  * **Alpha-Beta Pruning**:
    * $\alpha$ (best choice found so far along the path for MAX) and $\beta$ (best choice found so far for MIN).
    * Pruning condition: If $\alpha \ge \beta$, prune the remaining child branches.
    * Move ordering impact: Ideal ordering achieves time complexity $O(b^{d/2})$, doubling solvable search depth.

---

### Module 3: Knowledge-Based Agents and Logical Reasoning (8 Contact Hours)

::: callout-exam Module 3 High-Yield Focus
Module 3 formalizes declarative symbolic reasoning. High-yield KTU exam topics: The Wumpus World environment PEAS and knowledge base sentences; Propositional logic syntax, semantics, and truth tables; Inference rules (Modus Ponens, Resolution); CNF conversion steps; First-Order Logic (FOL) syntax (quantifiers $\forall, \exists$, predicates, functions); Unification algorithm step-by-step ($MGU$); Forward Chaining vs Backward Chaining algorithms for Horn clauses.
:::

* **Knowledge-Based Agents**:
  * Architecture of Knowledge-Based Agents: Knowledge Base (KB), `TELL` and `ASK` operations, inference engine.
  * **The Wumpus World Benchmark Environment**:
    * PEAS description: Pits (Breeze), Wumpus (Stench), Gold (Glitter), Arrow (Scream).
    * Exploring the environment safely via logical deduction; Handling partial observability and danger.
* **Propositional Logic**:
  * Syntax: Propositional symbols, logical connectives ($\neg, \land, \lor, \Rightarrow, \Leftrightarrow$).
  * Semantics: Truth tables, models, validity (tautologies), satisfiability, unsatisfiability (contradictions).
  * **Logical Entailment ($KB \models \alpha$)**: Model checking algorithm (`TT-Entails`).
  * **Reasoning Patterns & Inference Rules**:
    * Modus Ponens, And-Elimination, Resolution rule ($\frac{\alpha \lor \beta, \, \neg \beta \lor \gamma}{\alpha \lor \gamma}$).
    * Converting formulas into **Conjunctive Normal Form (CNF)**: 8-step mechanical algorithm (eliminate $\Leftrightarrow, \Rightarrow$, push $\neg$ inside via De Morgan's, distribute $\lor$ over $\land$).
    * Proof by Refutation: Resolution algorithm for propositional logic.
* **First-Order Logic (FOL / Predicate Calculus)**:
  * Expressive power and limitations of Propositional Logic; Syntax of FOL: Constants, Variables, Predicates, Functions, Quantifiers ($\forall, \exists$).
  * Translating English natural language assertions into First-Order Logic formulas.
  * Semantics of FOL: Domain of discourse, interpretations, models.
* **Inference in First-Order Logic**:
  * Propositional vs First-Order Inference: Universal Instantiation (UI) and Existential Instantiation (EI) with Skolem constants/functions.
  * **Unification & Generalized Modus Ponens**:
    * Finding Most General Unifier ($MGU$) for two first-order expressions.
    * Lifting propositional inference rules to first-order representations.
  * **Forward Chaining Algorithm**:
    * Data-driven reasoning starting from known facts; Triggering rules whose premises are satisfied until goal is reached; Soundness and completeness for Datalog.
  * **Backward Chaining Algorithm**:
    * Goal-driven reasoning starting from query; Decomposing goals into sub-goals; Depth-first recursive exploration; Relationship to logic programming (Prolog).

---

### Module 4: Reinforcement Learning (10 Contact Hours)

::: callout-exam Module 4 High-Yield Focus
Module 4 explores learning optimal decision policies through reward signals. High-yield KTU exam topics: Markov Decision Process (MDP) 5-tuple ($\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma$); Bellman Expectation and Optimality equations; Passive RL (Direct Utility Estimation, Adaptive Dynamic Programming, Temporal Difference learning $TD(0)$); Active RL (Exploration vs Exploitation, $\epsilon$-greedy, Q-Learning update rule $Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$); Policy Search and Inverse Reinforcement Learning.
:::

* **Reinforcement Learning Foundations & Learning from Rewards**:
  * The RL paradigm: Agent-Environment interaction loop, states $s_t$, actions $a_t$, immediate scalar reward $r_{t+1}$, discount factor $\gamma \in [0, 1)$.
  * Cumulative discounted return: $G_t = \sum_{k=0}^\infty \gamma^k R_{t+k+1}$.
  * Formalizing environments as **Markov Decision Processes (MDPs)**: The Markov property ($P(s_{t+1}|s_t, a_t, \dots, s_0) = P(s_{t+1}|s_t, a_t)$).
  * Policies ($\pi(s)$ deterministic, $\pi(a|s)$ stochastic) and Value Functions: State-Value $V^\pi(s)$ and Action-Value $Q^\pi(s, a)$.
  * The **Bellman Equations**: Recursive decomposition of value functions into immediate reward plus discounted downstream value.
* **Passive Reinforcement Learning**:
  * Task: Evaluating the utility $V^\pi(s)$ of a fixed policy $\pi$ in an environment with unknown transition probabilities.
  * **Direct Utility Estimation**: Monte Carlo averaging of observed episode returns; Ignores Bellman constraints between states.
  * **Adaptive Dynamic Programming (ADP)**: Learning empirical transition model $\hat{P}(s'|s, a)$ and solving the Bellman system via Value Iteration.
  * **Temporal Difference (TD) Learning**:
    * Bootstrapping from subsequent state estimates: $V(s) \leftarrow V(s) + \alpha [r + \gamma V(s') - V(s)]$.
    * TD error $\delta_t = r_{t+1} + \gamma V(s_{t+1}) - V(s_t)$; Convergence guarantees.
* **Active Reinforcement Learning**:
  * Transition from passive evaluation to optimal control: Agent must explore actions to discover optimal policy $\pi^*$.
  * **Exploration vs Exploitation Dilemma**:
    * $\epsilon$-Greedy action selection strategy.
    * Exploration functions: $f(u, n) = u + \frac{k}{n}$ prioritizing infrequently visited state-action pairs.
  * **$Q$-Learning (Off-Policy TD Control)**:
    * Learning action values directly without a transition model:
      $$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$
    * Model-free nature, off-policy exploration independence, convergence to $Q^*$ under infinite visitation.
* **Generalization & Advanced Paradigms in Reinforcement Learning**:
  * Function Approximation: Overcoming large or continuous state spaces using linear function approximators or Deep Q-Networks (DQN).
  * **Policy Search**: Parameterizing policy $\pi_\theta(s, a)$ directly; Stochastic gradient ascent (REINFORCE algorithm).
  * **Apprenticeship Learning & Inverse Reinforcement Learning (IRL)**:
    * Inferring the latent reward function $R(s)$ from expert demonstrations rather than hand-crafting reward signals.
  * **Real-World Applications of Reinforcement Learning**:
    * Autonomous driving (lane centering, traffic navigation), Game mastery (AlphaGo, Chess, Atari), Robotics manipulation, Resource scheduling in cloud data centers, Automated algorithmic trading.

---

## 📖 Prescribed Textbooks & Reference Books

### Prescribed Core Textbooks

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Artificial Intelligence: A Modern Approach** | **Stuart Russell, Peter Norvig** | **Pearson Education** | **4th Edition, 2021** |
| **2** | **Artificial Intelligence** | **Kevin Knight, Elaine Rich, Shivashankar B. Nair** | **Tata McGraw-Hill** | **3rd Edition, 2009** |

</div>

### Prescribed Reference Books

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Introduction to Artificial Intelligence and Expert Systems** | Dan W. Patterson | Pearson Education | 1st Edition, 2015 |
| **2** | **Artificial Intelligence: Structures and Strategies for Complex Problem Solving** | George F. Luger | Pearson Education | 6th Edition, 2009 |
| **3** | **Artificial Intelligence: Making a System Intelligent** | Nilakshi Jain | Wiley | 1st Edition, 2019 |

</div>

---

## 🎥 Video Lectures & Online Course Resources

<div class="table-wrap">

| Module | Platform | Resource Link | Focus Areas |
| :---: | :---: | :--- | :--- |
| **Module 1** | **YouTube / Stanford & Berkeley** | [AI Definition, Agents & Environments](https://www.youtube.com/watch?v=X_Qt0U66aH0) | Intelligent agents, PEAS framework, rationality, and problem formulation. |
| **Module 2** | **YouTube / NPTEL & MIT** | [Informed Search & Game Playing](https://www.youtube.com/watch?v=te1K8on1Pk0) | A* heuristic search, admissible heuristics, Minimax, and Alpha-Beta pruning. |
| **Module 3** | **YouTube / Stanford AI Series** | [Knowledge Representation & Logic](https://www.youtube.com/watch?v=SEJhMO1IXZs) | Propositional logic, inference rules, First-Order Logic, and unification. |
| **Module 4** | **YouTube / DeepMind RL Series** | [Reinforcement Learning Foundations](https://youtu.be/YaPSPu7K9S0?si=DizMPlZ9uVSy50iG) | MDPs, Bellman equations, Temporal Difference learning, and Q-Learning. |

</div>

---

## ⚖️ Course Assessment Method (CIE & ESE)

The course carries **100 Total Marks**, structured into **40 Marks for Continuous Internal Evaluation (CIE)** and **60 Marks for the University End Semester Examination (ESE)**.

### Continuous Internal Evaluation (CIE: 40 Marks)

<div class="table-wrap">

| Component | Marks Allocated | Evaluation Details & Regulations |
| :--- | :---: | :--- |
| **Attendance** | **5 Marks** | Minimum 75% attendance mandatory. |
| **Assignment / Microproject** | **15 Marks** | Minimum of two rigorous conceptual assignments or one AI implementation microproject (e.g., $A^*$ pathfinder visualizer, Alpha-Beta Tic-Tac-Toe / Connect-4 game engine, or Gridworld Q-Learning simulation). |
| **Internal Examination - 1 (Written)** | **10 Marks** | Written test covering **Module 1 and first half of Module 2** (scaled to 10 marks). |
| **Internal Examination - 2 (Written)** | **10 Marks** | Written test covering **second half of Module 2, Module 3, and Module 4** (scaled to 10 marks). |
| **Total CIE Marks** | **40 Marks** | **Eligibility: Minimum 45% (18/40 marks) required in CIE to be eligible for ESE.** |

</div>

---

### End Semester Examination (ESE: 60 Marks)

* **Total Examination Duration**: **2 Hours 30 Minutes (150 Minutes)**
* **Total Question Paper Valuation**: **96 Marks** (Students write for a maximum of **60 Marks**)
* **Passing Requirement**: **Minimum 40% (24/60 marks) in ESE AND minimum 50% aggregate (50/100) combining CIE + ESE**.

<div class="table-wrap">

| Section | Question Distribution & Marks | Choice Rules | Section Marks |
| :---: | :--- | :--- | :---: |
| **Part A** | • **2 Questions from each module** (Modules 1, 2, 3, 4).<br>• Total of **8 Questions** (Questions 1 to 8).<br>• Each question carries **3 marks** ($8 \times 3 = 24$). | **Compulsory**<br>*(No internal choice)* | **24 Marks** |
| **Part B** | • **Two full questions from each module** (Questions 9 & 10 from M1, 11 & 12 from M2, 13 & 14 from M3, 15 & 16 from M4).<br>• Each full question carries **9 marks** ($4 \times 9 = 36$).<br>• Each full question can have **maximum 3 subdivisions** (e.g., 5+4, 6+3, or 3+3+3). | **Choice-based**<br>*(Answer any 1 full question from each module)* | **36 Marks** |
| **Total** | **Part A (24 Marks) + Part B (36 Marks)** | | **60 Marks** |

</div>

---

## 🎓 Course Outcomes (COs)

Upon successful completion of the Artificial Intelligence course, students will demonstrate mastery across the following outcomes:

<div class="table-wrap">

| CO Identifier | Course Outcome (CO) Statement | Bloom's Knowledge Level |
| :---: | :--- | :---: |
| **CO1** | **Explain** how intelligent agents can solve problems. | **K2 (Understand)** |
| **CO2** | **Use** the different types of search methods to solve various problems. | **K3 (Apply)** |
| **CO3** | **Formulate** knowledge representation and examine resolution in propositional logic and first order logic. | **K3 (Apply)** |
| **CO4** | **Utilize** reinforcement learning techniques to create intelligent agents. | **K3 (Apply)** |

</div>

---

## 🗺️ CO-PO Mapping Table

The Course Outcomes directly map to the **National Board of Accreditation (NBA) Program Outcomes (POs)**:

*Correlation Scale: **3 = Substantial (High)** | **2 = Moderate (Medium)** | **1 = Slight (Low)** | **— = No Correlation***

<div class="table-wrap">

| Course Outcome | PO1<br><small>Engg Knowledge</small> | PO2<br><small>Problem Analysis</small> | PO3<br><small>Design/Dev</small> | PO4<br><small>Investigations</small> | PO5<br><small>Modern Tools</small> | PO6<br><small>Engineer & Society</small> | PO7<br><small>Environment</small> | PO8<br><small>Ethics</small> | PO9<br><small>Individual/Team</small> | PO10<br><small>Communication</small> | PO11<br><small>Project Mgmt</small> | PO12<br><small>Life-long Learning</small> |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CO1** | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | — | — | — | — | — | — | — | <span class="matrix-med">2</span> |
| **CO2** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | — | — | — | — | — | — | — | <span class="matrix-med">2</span> |
| **CO3** | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | — | — | — | — | — | — | — | <span class="matrix-med">2</span> |
| **CO4** | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | — | — | — | — | — | — | — | <span class="matrix-med">2</span> |

</div>

### CO-PO Mapping Justification & Insights:
* **PO1 to PO3 (Engineering Foundations & Design)**: Addressed substantially (Level 2 and 3) as students construct search graphs, formulate consistent heuristics, implement theorem provers, and design Bellman reward models.
* **PO4 (Conduct Investigations of Complex Problems)**: Addressed at Level 2 across all COs through search space analysis, heuristic dominance testing, and reinforcement learning policy evaluations.
* **PO12 (Life-Long Learning)**: Addressed at Level 2 across all four outcomes because AI foundations directly underpin rapidly evolving frontier fields such as Large Language Models, autonomous driving, and cognitive robotics.

---

## ⚡ Interactive Syllabus Self-Check Quiz

::: quiz Heuristic Search: Admissibility and A* Optimality
In Module 2, what condition must a heuristic function $h(n)$ satisfy to guarantee that tree-search $A^*$ is optimal?
(*) The heuristic must be admissible: it must never overestimate the true minimum cost to reach the goal ($h(n) \le h^*(n)$).
( ) The heuristic must equal the exact path cost from the root ($h(n) = g(n)$).
( ) The heuristic must be greater than or equal to the actual cost to force greedy exploration.
( ) The heuristic must be zero for all states in the state space.
::: explanation
For tree-search $A^*$, **admissibility** ($h(n) \le h^*(n)$ for all nodes $n$) guarantees that the algorithm will always return an optimal (shortest/lowest cost) path. If an admissible heuristic is also **consistent (monotonic)**, meaning $h(n) \le c(n, a, n') + h(n')$, graph-search $A^*$ is guaranteed to find optimal paths without needing to re-evaluate already visited nodes.
:::

::: quiz Reinforcement Learning: Temporal Difference vs Monte Carlo
In Module 4 of the Artificial Intelligence syllabus, what is the key computational distinction between Temporal Difference (TD) learning and Monte Carlo (Direct Utility Estimation) methods?
(*) TD learning updates its utility estimate after each single step by bootstrapping from subsequent state estimates, whereas Monte Carlo methods must wait until the full episode terminates.
( ) Monte Carlo methods can only be applied to continuous spaces, whereas TD learning only works in chess.
( ) TD learning requires knowing the exact transition probability matrix $P(s'|s, a)$, while Monte Carlo is completely model-free.
( ) Both methods are identical in update frequency and bootstrapping behavior.
::: explanation
**Temporal Difference (TD) learning** updates value estimates online at each transition step using **bootstrapping**: $V(s) \leftarrow V(s) + \alpha [r + \gamma V(s') - V(s)]$, where it estimates downstream return using the current value of $s'$. In contrast, **Monte Carlo (Direct Utility Estimation)** does not bootstrap; it must run each episode to completion to measure the actual total observed return $G_t$ before performing any parameter updates.
:::

---

## 🧭 Next Steps in Your Study Journey

* Begin with **[Module 1: 1.1 AI Definition, Foundations, and History](m1_01_ai_definition_foundations_and_history.html)**.
* Master PEAS modeling with **[Module 1: 1.2 Agents and Environments (PEAS Framework)](m1_02_agents_and_environments_peas.html)**.
* Practice real-world scenarios in **[Module 1: Practice Lab - Agents and Problem Formulation](m1_99_practice_lab_agents_and_problem_formulation.html)**.
* Explore search algorithms in **[Module 2: 2.1 Uninformed Search (DFS, BFS, UCS)](m2_01_uninformed_search_dfs_bfs_ucs.html)**.
* Review key algorithms and definitions in the **[Anki-style Spaced Repetition Review Deck](../../review.html)**.
