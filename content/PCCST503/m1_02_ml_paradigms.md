# The 4 Learning Paradigms: How Computers Learn

**Supervised, Unsupervised, Semi-supervised, and Reinforcement Learning explained from zero.**

<a id="the-intuition"></a>
## 1. The Intuition: The 4 Ways Humans Learn

Just as humans learn through different teaching styles, algorithms are grouped into four primary learning paradigms based on the **presence and nature of feedback**.

::: callout-intuition Relatable Real-World Analogies
1. **Supervised Learning (Learning with an Answer Key):** A teacher gives you 1,000 flashcards. The front has a photo of an X-ray ($X$), and the back has the verified doctor's diagnosis ($Y$). You guess, check the back, and correct your mistakes.
2. **Unsupervised Learning (Finding Hidden Patterns):** You are given a bucket containing 10,000 mixed Lego bricks with zero labels or instructions. You naturally group them by color, shape, and size based purely on inherent similarity.
3. **Semi-Supervised Learning (The Guided Boost):** You have 100,000 medical scans, but doctors only had time to label 500 of them. You use the 500 labeled scans to anchor your knowledge, and the 99,500 unlabeled scans to understand overall structural variations.
4. **Reinforcement Learning (Trial, Error & Rewards):** A puppy learns to fetch a ball. If it brings the ball back, it gets a treat (+1 Reward). If it chews your shoe, it gets no treat (-1 Penalty). Over time, it learns the optimal policy to maximize treats.
:::

---

<a id="the-math"></a>
## 2. Mathematical Formalization

| Paradigm | Training Dataset Structure | Target Goal | Core Algorithms |
| :--- | :--- | :--- | :--- |
| **Supervised** | $\mathcal{D} = \{(x^{(i)}, y^{(i)})\}_{i=1}^m$ with known labels $y^{(i)}$ | Learn mapping $f: X 	o Y$ minimizing empirical loss | Linear/Logistic Regression, SVM, Decision Trees, Neural Nets |
| **Unsupervised** | $\mathcal{D} = \{x^{(i)}\}_{i=1}^m$ (No target labels) | Discover latent structure $p(x)$ or cluster assignments | K-Means, Hierarchical Clustering, PCA, Autoencoders |
| **Semi-Supervised** | $\mathcal{D}_L \cup \mathcal{D}_U$ where $|\mathcal{D}_L| \ll |\mathcal{D}_U|$ | Exploit geometric density of unlabeled data to improve $f$ | Self-training, Pseudo-labeling, Graph-based SSL |
| **Reinforcement** | Environment states $s_t$, actions $a_t$, rewards $r_t$ | Maximize expected cumulative return $G_t = \sum \gamma^k r_{t+k+1}$ | Q-Learning, Policy Gradients (PPO), Deep Q-Networks (DQN) |

::: callout-formula Key Objective Functions
- **Supervised Empirical Risk:** $\min_\theta rac{1}{m}\sum_{i=1}^m \mathcal{L}(h_\theta(x^{(i)}), y^{(i)})$
- **RL Bellman Optimality Equation:** $Q^*(s, a) = \mathbb{E}\left[ r + \gamma \max_{a'} Q^*(s', a') 
ight]$
:::

---

<a id="worked-example"></a>
## 3. Comparative Problem Solving

::: step [Scenario A: Housing Market] Supervised Regression
Given historical records of house square footage ($x_1$) and bedrooms ($x_2$), along with final sale price ($y$), train a regression model to predict continuous market prices for new listings.
:::

::: step [Scenario B: Customer Segmentation] Unsupervised Clustering
An e-commerce store has 1,000,000 user purchase logs but no demographic tags. Unsupervised clustering groups users into behavioral personas (e.g. "Weekend Bargain Hunters", "Tech Enthusiasts").
:::

::: step [Scenario C: AlphaGo & Robotics] Reinforcement Learning
A robotic arm attempts to balance a pole. Every second the pole remains upright yields a reward of $+1$. The agent iteratively optimizes its motor torque policy through continuous trial and error.
:::

---

<a id="simulation"></a>
## 4. Visualizing the Paradigms

::: manim assets/videos/m1_paradigms.mp4 The Four Learning Styles
Observe the difference between labeled classification boundaries and unsupervised cluster grouping.
:::

---

<a id="self-check"></a>
## 5. Active Recall Checkpoint

::: quiz Q1: Paradigm Identification
A bank wants to group its credit card customers into 5 distinct spending personas based on transaction histories, without any pre-existing category labels. Which paradigm must they use?
(A) Supervised Regression
(*B) Unsupervised Clustering
(C) Reinforcement Learning
(D) Semi-supervised Classification
::: explanation
Because there are no ground truth target labels provided ($y$), the algorithm must discover intrinsic geometric clusters in the transaction feature space on its own.
:::

::: quiz Q2: Reinforcement Learning Mechanics
In Reinforcement Learning, what guides the agent toward learning the optimal behavior policy?
(A) A human labeling every single state transition
(*B) A scalar reward signal (+/- feedback) from the environment
(C) Mean Squared Error calculated against a validation set
(D) Minimizing entropy across feature splits
::: explanation
RL agents learn by taking actions within an environment and updating their policy or value functions ($Q$-values) based on cumulative scalar rewards ($r_t$).
:::
