import os

CONTENT_DIR = os.path.join("content", "PCCST503")

# m2_01_logistic_regression.md
m2_01 = r"""# Logistic Regression & Sigmoid Activation

**The quintessential probabilistic classification algorithm: mapping linear predictions to bounded probabilities.**

<a id="the-intuition"></a>
## 1. The Intuition: Why Linear Regression Fails for Classification

Suppose you want to predict whether a medical tumor is **Malignant ($y=1$)** or **Benign ($y=0$)** based on tumor radius ($x$).

::: callout-intuition The Flaws of Linear Regression for Categories
If you fit a straight line $h_\theta(x) = \theta_0 + \theta_1 x$:
1. **Unbounded Outputs:** For very large tumors, linear regression predicts $\hat{y} = 2.45$. What does a "245% probability of cancer" mean? Probabilities must strictly be bounded within $[0, 1]$.
2. **Sensitivity to Outliers:** A single extreme benign outlier far to the right pivots the regression line, shifting your decision threshold and causing dangerous misdiagnoses.
:::

**The Fix:** Wrap the linear score $z = \theta^T x$ inside a non-linear **S-shaped Sigmoid function** $\sigma(z)$ that squashes any input into a valid probability $(0, 1)$.

---

<a id="the-math"></a>
## 2. Mathematical Formulation

### The Logistic Sigmoid Function:
$$ \sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{1 + e^z} $$

Where $z = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d = \theta^T x$.

### The Probabilistic Hypothesis:
$$ h_\theta(x) = P(y=1 \mid x; \theta) = \sigma(\theta^T x) = \frac{1}{1 + e^{-\theta^T x}} $$

$$ P(y=0 \mid x; \theta) = 1 - h_\theta(x) $$

### Odds and Log-Odds (The Logit Function):
The **Odds** of an event is the ratio of probability of occurrence to non-occurrence:

$$ \text{Odds} = \frac{P(y=1|x)}{1 - P(y=1|x)} = \frac{\sigma(z)}{1 - \sigma(z)} = e^z $$

Taking the natural logarithm yields the **Log-Odds (Logit)**:

$$ \ln\left( \frac{P(y=1|x)}{1 - P(y=1|x)} \right) = \ln(e^z) = z = \theta^T x $$

*Insight:* Logistic Regression is fundamentally a **linear model for the log-odds of the positive class!*

---

<a id="worked-example"></a>
## 3. Cost Function & The Non-Convexity Trap

::: callout-pitfall Why MSE is Forbidden in Logistic Regression
If you plug the non-linear sigmoid $\sigma(\theta^Tx)$ into the Mean Squared Error cost function $\frac{1}{2m}\sum (\sigma(\theta^Tx) - y)^2$, the resulting cost surface is **wavy and non-convex** with dozens of local minima. Gradient descent will get stuck in poor local minima!
:::

### The Convex Cross-Entropy Loss (Log Loss):
$$ J(\theta) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln(h_\theta(x^{(i)})) + (1 - y^{(i)}) \ln(1 - h_\theta(x^{(i)})) \right] $$

- When $y = 1$: Cost is $-\ln(h_\theta(x))$. If $h_\theta(x) \to 1$, $\text{Cost} \to 0$. If $h_\theta(x) \to 0$, $\text{Cost} \to \infty$ (infinite penalty for confident wrong guesses!).
- When $y = 0$: Cost is $-\ln(1 - h_\theta(x))$. If $h_\theta(x) \to 0$, $\text{Cost} \to 0$. If $h_\theta(x) \to 1$, $\text{Cost} \to \infty$.

---

<a id="simulation"></a>
## 4. Visualizing the Sigmoid Activation

::: manim assets/videos/m2_logistic_sigmoid.mp4 Sigmoid Decision Boundary
Watch how inputs from $-\infty$ to $+\infty$ are smoothly squashed into the probability interval $(0, 1)$ with threshold at $z=0$.
:::

---

<a id="self-check"></a>
## 5. Active Recall Checkpoint

::: quiz Q1: Decision Boundary
If a fitted binary logistic regression model produces a linear score $z = \theta^T x = 0$, what is the predicted probability of the positive class $\hat{y}$?
(A) 0.00
(*B) 0.50
(C) 1.00
(D) Undefined
::: explanation
$\sigma(0) = \frac{1}{1 + e^{-0}} = \frac{1}{1 + 1} = \frac{1}{2} = 0.50$. In standard binary classification, $z=0$ defines the exact geometric hyperplane of the Decision Boundary.
:::

::: quiz Q2: Optimization Geometry
Why is Binary Cross-Entropy used instead of Mean Squared Error when optimizing Logistic Regression?
(A) MSE produces gradients that explode infinitely
(*B) Sigmoid combined with MSE creates a non-convex error surface with local minima, whereas Cross-Entropy is strictly convex
(C) Cross-Entropy does not require computing derivatives
(D) Cross-Entropy only works on continuous real numbers
::: explanation
The non-linearity of the sigmoid creates wavy valleys when squared. Cross-entropy loss cancels the exponential behavior in the gradient, producing a guaranteed convex bowl where gradient descent always converges to the global minimum.
:::
"""

# m2_02_naive_bayes.md
m2_02 = r"""# Naïve Bayes Classification

**Fast, probabilistic classification based on Bayes' Theorem and feature independence assumptions.**

<a id="the-intuition"></a>
## 1. The Intuition: The "Naïve" Doctor

Imagine a doctor diagnosing whether a patient has the **Flu ($C_1$)** or a **Common Cold ($C_2$)** based on 3 symptoms: **Fever ($x_1$)**, **Cough ($x_2$)**, and **Fatigue ($x_3$)**.

::: callout-intuition Why is it called "Naïve"?
To compute the true joint probability $P(x_1, x_2, x_3 \mid C)$, you would need data on every possible combination of symptoms occurring together. 
- **The Naïve Assumption:** The algorithm assumes that every feature is **conditionally independent** of every other feature given the disease.
- It assumes: having a high fever has zero correlation with feeling fatigued. 
- In the real world, this assumption is completely false! Yet in practice, Naïve Bayes works remarkably well for spam filtering, sentiment analysis, and medical diagnosis.
:::

---

<a id="the-math"></a>
## 2. Mathematical Derivation

From Bayes' Theorem:

$$ P(C_k \mid x) = \frac{P(x \mid C_k) P(C_k)}{P(x)} $$

For a feature vector $x = (x_1, x_2, \dots, x_d)$, applying the Conditional Independence assumption:

$$ P(x \mid C_k) = P(x_1, x_2, \dots, x_d \mid C_k) = \prod_{j=1}^d P(x_j \mid C_k) $$

### The Naïve Bayes Classification Rule:
Since the evidence denominator $P(x) = \sum_k P(x|C_k)P(C_k)$ is identical for all candidate classes, we drop it:

$$ \hat{y} = \arg\max_{k \in \{1, \dots, K\}} P(C_k) \prod_{j=1}^d P(x_j \mid C_k) $$

Taking logs for numerical stability:

$$ \hat{y} = \arg\max_{k} \left[ \ln P(C_k) + \sum_{j=1}^d \ln P(x_j \mid C_k) \right] $$

---

<a id="worked-example"></a>
## 3. The Zero-Probability Trap & Laplace Smoothing

::: callout-pitfall The Zero-Frequency Disaster
Suppose the word *"Crypto"* never appeared in any training email labeled `Not Spam`. 
Then $P(\text{"Crypto"} \mid \text{Not Spam}) = 0$. 
Because we multiply all feature probabilities together:
$$ P(\text{Email} \mid \text{Not Spam}) = P(\text{word}_1) \times \dots \times 0 \times \dots = 0 $$
A single unseen word completely zeroes out the entire probability, wiping out all other evidence!
:::

### The Fix: Laplace ($+1$) Smoothing:
We add a pseudo-count of $\alpha = 1$ to the numerator, and adjust the denominator by the total vocabulary size $|V|$:

$$ \hat{P}(x_j \mid C_k) = \frac{\text{Count}(x_j, C_k) + 1}{\sum_{w \in V} \text{Count}(w, C_k) + |V|} $$

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Assumption Breakdown
What is the core independence assumption made by the Naïve Bayes classifier?
(A) Target classes are uniformly distributed
(*B) All features $x_i$ and $x_j$ are conditionally independent given the class label $y$
(C) Feature values must follow a standard normal distribution
(D) The covariance matrix of features is dense and non-diagonal
::: explanation
Naïve Bayes explicitly assumes that the presence or absence of a particular feature is completely unrelated to the presence or absence of any other feature, conditional on the class variable ($P(x_1, x_2|y) = P(x_1|y)P(x_2|y)$).
:::

::: quiz Q2: Smoothing Mechanics
Why is Laplace smoothing applied during Naïve Bayes text classification?
(A) To normalize text vector lengths
(*B) To prevent unseen words in test data from multiplying the total class probability down to zero
(C) To speed up matrix multiplication
(D) To reduce the number of features
::: explanation
Laplace ($+1$) additive smoothing ensures that every possible word has a tiny non-zero probability baseline, preventing a single unseen vocabulary token from destroying valid classification predictions.
:::
"""

# m2_03_knn.md
m2_03 = r"""# K-Nearest Neighbors (KNN)

**A non-parametric, instance-based lazy learner that classifies query points based on neighborhood voting.**

<a id="the-intuition"></a>
## 1. The Intuition: "Show me your friends, and I'll tell you who you are"

Imagine you move to a new neighborhood and want to guess the political affiliation of a house.

::: callout-intuition The Neighborhood Polling Strategy
1. You find the $K$ geographically closest neighbor houses.
2. You take a majority vote among those $K$ neighbors.
3. If $K=5$, and 4 neighbors are Blue while 1 is Red, you classify the target house as **Blue**.
:::

**Why is it called a "Lazy Learner"?**
KNN has zero training phase ($O(1)$ training time). It doesn't learn any mathematical equation or weights! It simply memorizes the entire training dataset into memory and performs all computational heavy-lifting during **test / query time** ($O(m \cdot d)$).

---

<a id="the-math"></a>
## 2. Distance Metrics & Hyperparameters

To determine which neighbors are "nearest", KNN computes distance in $d$-dimensional space:

### 1. Euclidean Distance ($L_2$ Norm):
$$ d(p, q) = \sqrt{\sum_{j=1}^d (p_j - q_j)^2} $$

### 2. Manhattan Distance ($L_1$ Norm):
$$ d(p, q) = \sum_{j=1}^d |p_j - q_j| $$

### 3. Minkowski Distance ($L_p$ Generalized Norm):
$$ d(p, q) = \left( \sum_{j=1}^d |p_j - q_j|^p \right)^{1/p} $$

---

<a id="worked-example"></a>
## 3. The Impact of $K$ & Feature Scaling

::: callout-pitfall The Critical Role of $K$ (Bias vs Variance)
- **When $K = 1$:** The model fits every single noisy training point. Complex, jagged decision boundary $\implies$ **High Variance / Overfitting**.
- **When $K = m$ (Total dataset size):** The model always predicts the majority class in the entire dataset $\implies$ **High Bias / Underfitting**.
- *Rule of Thumb:* Choose an **odd number** for $K$ (e.g., $K=3, 5, 7$) in binary classification to prevent voting ties!
:::

::: callout-exam Why Feature Scaling is Mandatory for KNN!
Suppose feature $x_1$ is Annual Income (\$20,000 to \$200,000) and feature $x_2$ is Age (18 to 70).
The numerical distance in Income $(\Delta x_1 = 50,000)$ is thousands of times larger than $(\Delta x_2 = 20)$, meaning Income will 100% dominate the distance calculation while Age is completely ignored!
**Always apply Min-Max Normalization or Standard Scaling (Z-Score) before running KNN!**
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Computational Complexity
What is the training time complexity of the standard K-Nearest Neighbors algorithm on a dataset of $m$ examples with $d$ features?
(*A) $O(1)$
(B) $O(m \cdot d)$
(C) $O(m^2)$
(D) $O(d^3)$
::: explanation
Because KNN is a non-parametric lazy learner, "training" simply consists of storing the feature vectors in memory, which takes $O(1)$ model parameter fitting time. All distance computations happen at query/inference time.
:::
"""

# m2_04_decision_trees.md
m2_04 = r"""# Decision Trees & Information Gain

**Hierarchical decision systems that recursively partition data using Information Theory.**

<a id="the-intuition"></a>
## 1. The Intuition: The 20 Questions Game

Imagine playing the game *"20 Questions"* to guess a mystery animal.

::: callout-intuition What makes a good question?
- A bad question: *"Is its name Bob?"* (Only eliminates 1 option).
- A great question: *"Does it live on land or in water?"* (Instantly cuts the possibilities in half!).
- **Decision Trees** operate on the exact same logic. At every step, the algorithm searches across all features to find the single question that **maximizes purity** (reduces uncertainty the most).
:::

---

<a id="the-math"></a>
## 2. Mathematical Metrics: Entropy & Information Gain

### 1. Shannon Entropy ($H(S)$):
Entropy measures the degree of disorder, uncertainty, or impurity in a set of examples $S$:

$$ H(S) = -\sum_{i=1}^C p_i \log_2(p_i) $$

Where $p_i$ is the proportion of examples belonging to class $i$.
- If a node is **100% Pure** (all samples are Spam): $H(S) = - (1 \cdot \log_2(1)) = 0$.
- If a node is **50/50 Balanced** (maximum confusion): $H(S) = - (0.5\log_2(0.5) + 0.5\log_2(0.5)) = 1.0\text{ bit}$.

### 2. Information Gain ($IG(S, A)$):
Information Gain measures the expected reduction in entropy achieved by splitting dataset $S$ on feature $A$:

$$ IG(S, A) = H(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v) $$

### 3. Gini Impurity (Used by CART):
$$ \text{Gini}(S) = 1 - \sum_{i=1}^C p_i^2 $$

---

<a id="worked-example"></a>
## 3. Overfitting & Pruning Techniques

A Decision Tree left unrestricted will grow until every single leaf contains exactly 1 sample ($H(S)=0$), perfectly memorizing all training noise $\implies$ catastrophic overfitting.

::: step [Strategy 1: Pre-Pruning (Early Stopping)] Stopping Criteria
Halt tree growth before completion if:
- Maximum tree depth is reached (`max_depth = 4`).
- Minimum samples required to split a node is not met (`min_samples_split = 10`).
- Information Gain falls below a minimum threshold ($\Delta IG < \epsilon$).
:::

::: step [Strategy 2: Post-Pruning (Cost-Complexity Pruning)] Pruning Back
Grow the tree to full depth, then prune subtrees upward if removing them does not significantly worsen validation accuracy, balancing tree size against error:
$$ \mathcal{L}_\alpha(T) = \text{Error}(T) + \alpha |T| $$
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Metric Interpretation
If a decision tree node contains 20 examples, and all 20 belong to Class 'Approved' (0 belong to 'Rejected'), what is the Shannon Entropy of this node?
(*A) 0.00 bits
(B) 0.50 bits
(C) 1.00 bits
(D) Undefined
::: explanation
Because the subset is completely pure (zero uncertainty), $p_1 = 1.0$. The entropy is $H(S) = - (1.0 \cdot \log_2(1.0)) = 0.00$. Zero entropy corresponds to absolute certainty.
:::

::: quiz Q2: Splitting Objective
During the construction of a classification tree using the ID3 algorithm, which feature is selected at each split?
(A) The feature with the highest variance
(*B) The feature that yields the maximum Information Gain (highest reduction in entropy)
(C) The feature with the smallest number of unique categories
(D) The feature with the lowest correlation to the target
::: explanation
ID3 uses a greedy heuristic that evaluates all available candidate features and selects the one that maximizes Information Gain ($IG = H(S) - H(S|A)$), creating child subsets that are as pure as possible.
:::
"""

with open(os.path.join(CONTENT_DIR, "m2_01_logistic_regression.md"), "w", encoding="utf-8") as f:
    f.write(m2_01)
with open(os.path.join(CONTENT_DIR, "m2_02_naive_bayes.md"), "w", encoding="utf-8") as f:
    f.write(m2_02)
with open(os.path.join(CONTENT_DIR, "m2_03_knn.md"), "w", encoding="utf-8") as f:
    f.write(m2_03)
with open(os.path.join(CONTENT_DIR, "m2_04_decision_trees.md"), "w", encoding="utf-8") as f:
    f.write(m2_04)

print("All Module 2 topics upgraded to production standard.")
