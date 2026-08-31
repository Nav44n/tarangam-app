# Learning Paradigms: Semi-Supervised & Reinforcement Learning

**Leveraging cheap unlabeled data and training goal-oriented agents through scalar reward feedback.**

<a id="the-intuition"></a>
## 1. The Intuition: The Goldmine of Unlabeled Data & The Video Game Player

::: callout-intuition Real-World Contexts
- **Semi-Supervised Learning:** Labeling medical X-rays requires expensive radiologist time (\$200/hr). You have only 500 labeled scans, but 100,000 free unlabeled scans. Semi-supervised learning uses the small labeled set to anchor categories and the large unlabeled set to learn data geometry.
- **Reinforcement Learning:** An AI plays Super Mario. Nobody tells it which exact button to press at millisecond 42. It presses buttons randomly, receives $+100$ score for finishing the level or $-50$ for dying, and learns the optimal policy over millions of attempts.
:::

---

<a id="the-math"></a>
## 2. Reinforcement Learning Mathematical Setup

An RL agent interacts with an **Environment** modeled as a **Markov Decision Process (MDP)**:

$$ (S, A, P, R, \gamma) $$

Where:
- $s_t \in S$: Current state at time $t$.
- $a_t \in A$: Action taken by the agent.
- $r_t \in \mathbb{R}$: Immediate scalar reward received.
- $\gamma \in [0, 1)$: Discount factor for future rewards.

### Bellman Optimality Equation:
$$ Q^*(s, a) = \mathbb{E}\left[ r + \gamma \max_{a'} Q^*(s', a') \;\middle|\; s, a \right] $$

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: RL Core Mechanics
What provides the training feedback signal to a Reinforcement Learning agent?
(A) Human-annotated gradient vectors for each step
(*B) Scalar rewards and penalties from the environment
(C) Mean Squared Error calculated against a test dataset
(D) Information gain splits
::: explanation
RL agents optimize their actions to maximize the cumulative discounted scalar reward ($G_t = \sum \gamma^k r_{t+k+1}$) received from environment interactions.
:::
