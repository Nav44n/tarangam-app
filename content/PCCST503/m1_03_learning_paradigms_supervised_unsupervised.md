# Learning Paradigms: Supervised vs Unsupervised

**Comparing learning with an answer key against discovering latent geometric structures.**

<a id="the-intuition"></a>
## 1. The Intuition: Flashcards vs Lego Sorting

::: callout-intuition Two Core Styles of Learning
- **Supervised Learning (The Flashcard):** You are shown an image ($x$) and told its true label ($y$). You guess, check the answer key, and adjust your weights.
- **Unsupervised Learning (Lego Sorting):** You are given 10,000 unsorted Lego pieces with zero labels. You naturally group them into piles based on inherent color, geometry, and size.
:::

---

<a id="the-math"></a>
## 2. Mathematical Formalization

### 1. Supervised Learning
Given dataset $\mathcal{D} = \{(x^{(i)}, y^{(i)})\}_{i=1}^m$:
- **Regression:** $y \in \mathbb{R}$ (Continuous prediction, e.g. Stock Prices, House Valuations).
- **Classification:** $y \in \{0, 1\}$ or $\{1, \dots, K\}$ (Discrete category, e.g. Cancer Diagnosis, Spam Detection).

### 2. Unsupervised Learning
Given dataset $\mathcal{D} = \{x^{(i)}\}_{i=1}^m$ with no target labels $y$:
- **Clustering:** Discovering natural group assignments $c^{(i)} \in \{1, \dots, K\}$ (K-Means, Hierarchical).
- **Dimensionality Reduction:** Compressing high-dimensional $x \in \mathbb{R}^D$ to $z \in \mathbb{R}^d$ ($d \ll D$) while preserving maximum variance (PCA).

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Paradigm Selection
An airline wants to analyze passenger baggage weight records to automatically identify 4 distinct traveler personas without predefined tags. Which paradigm applies?
(A) Supervised Regression
(*B) Unsupervised Clustering
(C) Reinforcement Learning
(D) Supervised Classification
::: explanation
Because there are no predefined class labels or target outputs $y$, the model must uncover hidden cluster structures on its own.
:::
