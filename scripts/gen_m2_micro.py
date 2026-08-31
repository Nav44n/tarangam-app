import os

CONTENT_DIR = os.path.join("content", "PCCST503")

m2_files = {}

m2_files["m2_01_classification_intro_and_linear_flaws.md"] = r"""# Why Linear Regression Fails for Classification

**The structural failure modes of applying continuous regression lines to discrete categorical tasks.**

<a id="the-intuition"></a>
## 1. The Intuition: Tumor Malignancy

Suppose you want to predict whether a medical biopsy is **Malignant ($y=1$)** or **Benign ($y=0$)** based on tumor size ($x$).

::: callout-intuition Why Straight Lines Fail on Categories
If you fit a standard linear model $h_\theta(x) = \theta_0 + \theta_1 x$:
1. **Unbounded Output Values:** For large tumors, linear regression predicts $\hat{y} = 2.85$. A probability must strictly be bounded in $[0, 1]$.
2. **Extreme Outlier Sensitivity:** Adding a single benign tumor with huge radius far to the right pivots the line, drastically altering your classification decision threshold ($h(x) \ge 0.5$) and causing fatal false negatives!
:::

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Linear Model Flaws
Why is linear regression mathematically inappropriate for predicting binary probabilities?
(A) It requires gradient descent
(*B) It can output negative values and values strictly greater than 1.0
(C) It cannot handle continuous features
(D) It only works on 1-dimensional datasets
::: explanation
Probabilities are strictly bounded in the range $[0, 1]$. A linear function $\theta^T x$ has an unbounded range $(-\infty, +\infty)$.
:::
"""

m2_files["m2_02_logistic_sigmoid_function.md"] = r"""# The Logistic Sigmoid Function & Probabilistic Activation

**The S-shaped mathematical squashing function that maps any real number into valid probabilities.**

<a id="the-math"></a>
## 1. The Sigmoid Mathematical Definition

$$ \sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{1 + e^z} $$

Where $z = \theta^T x = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d$.

### Fundamental Properties:
1. **Bounded Range:** As $z \to +\infty$, $\sigma(z) \to 1$. As $z \to -\infty$, $\sigma(z) \to 0$.
2. **Symmetry:** $\sigma(-z) = 1 - \sigma(z)$.
3. **Midpoint Threshold:** $\sigma(0) = \frac{1}{1 + 1} = 0.50$.
4. **Calculus Derivative:**
$$ \frac{d\sigma(z)}{dz} = \sigma(z)(1 - \sigma(z)) $$

---

<a id="simulation"></a>
## 2. Visualizing Sigmoid Activation

::: manim assets/videos/m2_logistic_sigmoid.mp4 Sigmoid Activation
Watch how real numbers from $-\infty$ to $+\infty$ are smoothly compressed into the probability range $(0, 1)$.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Sigmoid Midpoint
What is the exact output of the standard logistic sigmoid function $\sigma(z)$ when input $z = 0$?
(A) 0.00
(*B) 0.50
(C) 1.00
(D) -1.00
::: explanation
$\sigma(0) = \frac{1}{1 + e^{-0}} = \frac{1}{1 + 1} = 0.50$, which defines the default decision boundary in binary classification.
:::
"""

m2_files["m2_03_odds_log_odds_and_logit.md"] = r"""# Odds, Log-Odds, and the Logit Function

**Proving that Logistic Regression is fundamentally a linear model for the log-odds of the positive class.**

<a id="the-math"></a>
## 1. Mathematical Derivation of Log-Odds

Let $p = P(y=1 \mid x) = \sigma(z)$.

### The Odds Ratio:
$$ \text{Odds} = \frac{p}{1 - p} = \frac{\frac{1}{1 + e^{-z}}}{1 - \frac{1}{1 + e^{-z}}} = \frac{\frac{1}{1 + e^{-z}}}{\frac{e^{-z}}{1 + e^{-z}}} = \frac{1}{e^{-z}} = e^z $$

### The Log-Odds (Logit):
Taking the natural logarithm yields:

$$ \text{logit}(p) = \ln\left( \frac{p}{1 - p} \right) = \ln(e^z) = z = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d $$

::: callout-formula Core Insight
While the relationship between features $x$ and probability $p$ is non-linear (S-shaped), the relationship between features $x$ and **Log-Odds** is strictly linear!
:::

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Logit Interpretation
If an event has probability $p = 0.80$, what is the Odds Ratio of that event occurring?
(A) 0.80
(*B) 4.0 (4 to 1)
(C) 0.20
(D) 1.25
::: explanation
$\text{Odds} = \frac{p}{1-p} = \frac{0.80}{1 - 0.80} = \frac{0.80}{0.20} = 4.0$.
:::
"""

m2_files["m2_04_cross_entropy_loss_for_logistic.md"] = r"""# Cross-Entropy Loss & The Non-Convexity Trap

**Why Mean Squared Error fails for Logistic Regression and how Cross-Entropy guarantees a convex loss landscape.**

<a id="the-math"></a>
## 1. The Non-Convexity Flaw of MSE

If you plug non-linear $\sigma(\theta^Tx)$ into MSE cost $\frac{1}{2m}\sum (\sigma(\theta^Tx) - y)^2$, the loss surface becomes **wavy and non-convex** with dozens of local minima.

---

## 2. The Convex Cross-Entropy Loss (Log Loss)

$$ J(\theta) = -\frac{1}{m}\sum_{i=1}^m \left[ y^{(i)}\ln(h_\theta(x^{(i)})) + (1-y^{(i)})\ln(1-h_\theta(x^{(i)})) \right] $$

- When $y=1$: Cost is $-\ln(h(x))$. If $h(x) \to 1$, $\text{Cost} \to 0$. If $h(x) \to 0$, $\text{Cost} \to \infty$.
- When $y=0$: Cost is $-\ln(1-h(x))$. If $h(x) \to 0$, $\text{Cost} \to 0$. If $h(x) \to 1$, $\text{Cost} \to \infty$.

### Gradient Vector Update Rule:
$$ \frac{\partial J}{\partial \theta_j} = \frac{1}{m}\sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_j^{(i)} $$

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Loss Penalty
If a model confidently predicts $h_\theta(x) = 0.001$ for a true positive instance ($y = 1$), what penalty does Cross-Entropy assign?
(A) Zero penalty
(B) $0.999$
(*C) Near-infinite penalty ($-\ln(0.001) \approx 6.91$)
(D) Negative penalty
::: explanation
Cross-entropy harshly penalizes confident wrong predictions with asymptotic logarithmic explosion.
:::
"""

m2_files["m2_05_naive_bayes_fundamentals_and_bayes_rule.md"] = r"""# Naïve Bayes Fundamentals: Bayes' Theorem in Classification

**The foundational Bayesian probability architecture for predictive inference.**

<a id="the-math"></a>
## 1. Bayes' Theorem in Machine Learning

$$ P(C_k \mid x) = \frac{P(x \mid C_k) P(C_k)}{P(x)} $$

Where:
- $P(C_k \mid x)$ is the **Posterior Probability** of class $C_k$ given feature vector $x$.
- $P(x \mid C_k)$ is the **Class-Conditional Likelihood**.
- $P(C_k)$ is the **Class Prior Probability**.
- $P(x) = \sum_k P(x \mid C_k) P(C_k)$ is the **Evidence (Marginal Likelihood)**.

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Evidence Role
Why can the denominator $P(x)$ be dropped when selecting the winning class $\hat{y} = \arg\max_k P(C_k|x)$?
(A) It always equals 1.0
(*B) It is identical across all candidate classes $C_k$ and does not change the ranking
(C) It is non-differentiable
(D) It is an imaginary number
::: explanation
Because $P(x)$ is a constant scaling factor across all classes for a given input $x$, the class that maximizes the numerator also maximizes the posterior.
:::
"""

m2_files["m2_06_naive_bayes_independence_assumption.md"] = r"""# The Naïve Conditional Independence Assumption

**Why multiplying individual feature probabilities simplifies computation from exponential to linear.**

<a id="the-math"></a>
## 1. The Independence Assumption

To compute $P(x_1, x_2, \dots, x_d \mid C_k)$ without assumptions requires estimating $2^d - 1$ joint parameters.

**The "Naïve" Simplification:** Assume all features are conditionally independent given class $C_k$:

$$ P(x_1, x_2, \dots, x_d \mid C_k) = \prod_{j=1}^d P(x_j \mid C_k) $$

### The Classification Decision Rule:
$$ \hat{y} = \arg\max_{k} \left[ \ln P(C_k) + \sum_{j=1}^d \ln P(x_j \mid C_k) \right] $$

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Parameter Scaling
How many parameters must be estimated for $d$ binary features under the Naïve Bayes independence assumption?
(*A) $O(d)$ per class
(B) $O(2^d)$
(C) $O(d^3)$
(D) $O(1)$
::: explanation
Assuming conditional independence reduces the parameter count from exponential $O(2^d)$ to linear $O(d)$.
:::
"""

m2_files["m2_07_naive_bayes_zero_probability_and_laplace.md"] = r"""# The Zero-Frequency Problem & Laplace Smoothing

**How $+1$ additive smoothing rescues Bayesian classifiers from multiplying by zero.**

<a id="the-intuition"></a>
## 1. The Zero-Probability Trap

If an unseen word (e.g. *"Cryptocurrency"*) appears in test data and was never seen in training Spam emails:
$$ P(\text{"Cryptocurrency"} \mid \text{Spam}) = 0 \implies \prod P(x_j \mid \text{Spam}) = 0 $$
A single zero wipes out all other positive evidence!

---

<a id="the-math"></a>
## 2. Laplace ($+1$) Additive Smoothing Formula

$$ \hat{P}(x_j \mid C_k) = \frac{\text{Count}(x_j, C_k) + 1}{\sum_{w \in V} \text{Count}(w, C_k) + |V|} $$

Where $|V|$ is the total unique vocabulary size.

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Smoothing Impact
What does Laplace smoothing add to the denominator of the probability estimate?
(A) $+1$
(*B) $+|V|$ (the total size of the vocabulary)
(C) $+N^2$
(D) The variance
::: explanation
Because a pseudo-count of $+1$ is added to every one of the $|V|$ vocabulary words in the numerator, the denominator must increase by $+|V|$ so total probabilities sum to 1.
:::
"""

m2_files["m2_08_knn_lazy_learning_and_intuition.md"] = r"""# K-Nearest Neighbors: Instance-Based Lazy Learning

**Why KNN has zero training phase and how neighborhood proximity guides non-parametric classification.**

<a id="the-intuition"></a>
## 1. The Intuition: Neighborhood Voting

To classify a new query point $q$:
1. Locate the $K$ closest training samples in feature space.
2. Take a majority vote among those $K$ neighbors.

::: callout-intuition What makes KNN "Lazy"?
- **Eager Learners (Linear Regression, Decision Trees):** Spend time during training learning weights $\theta$ so inference is fast ($O(1)$).
- **Lazy Learners (KNN):** Spend $O(1)$ time during training (just stores data in memory) and perform all heavy distance computations at query time ($O(m \cdot d)$).
:::

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Computational Profile
What is the training time complexity of standard KNN?
(*A) $O(1)$
(B) $O(m \cdot d)$
(C) $O(m^2)$
(D) $O(d^3)$
::: explanation
KNN is a non-parametric instance-based learner; training consists merely of loading dataset vectors into memory.
:::
"""

m2_files["m2_09_knn_distance_metrics.md"] = r"""# Distance Metrics: Euclidean, Manhattan, and Minkowski

**The geometric distance metrics governing multi-dimensional similarity.**

<a id="the-math"></a>
## 1. Distance Metric Formulations

### 1. Euclidean Distance ($L_2$ Norm):
$$ d_E(p, q) = \sqrt{\sum_{j=1}^d (p_j - q_j)^2} $$

### 2. Manhattan Distance ($L_1$ Norm / City Block):
$$ d_M(p, q) = \sum_{j=1}^d |p_j - q_j| $$

### 3. Minkowski Distance ($L_p$ Metric):
$$ d_p(p, q) = \left( \sum_{j=1}^d |p_j - q_j|^p \right)^{1/p} $$

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Metric Equivalence
When $p = 1$ in the Minkowski distance formula, which distance metric does it simplify to?
(A) Euclidean Distance ($L_2$)
(*B) Manhattan Distance ($L_1$)
(C) Chebyshev Distance ($L_\infty$)
(D) Mahalanobis Distance
::: explanation
$d_1(p, q) = (\sum |p_j - q_j|^1)^1 = \sum |p_j - q_j|$, which is the exact definition of Manhattan ($L_1$) distance.
:::
"""

m2_files["m2_10_knn_hyperparameter_k_and_scaling.md"] = r"""# KNN Hyperparameters: Bias-Variance & Feature Scaling

**Mastering the choice of $K$ and understanding why unscaled features break distance algorithms.**

<a id="the-intuition"></a>
## 1. The Impact of $K$ (Bias vs Variance)

- **$K = 1$:** High Variance / Overfitting (fits every noisy outlier point).
- **$K = m$ (Total dataset):** High Bias / Underfitting (always predicts majority class).
- **Best Practice:** Choose an **odd $K$** ($3, 5, 7$) for binary classification to avoid voting ties.

---

<a id="worked-example"></a>
## 2. The Feature Scaling Imperative

::: callout-pitfall Why Unscaled Data Breaks KNN
If Feature 1 is Salary (\$20,000 to \$200,000) and Feature 2 is Age (18 to 70), distance differences in Salary $(\Delta = 50,000)$ are $1000\times$ larger than Age $(\Delta = 20)$. Salary will 100% dominate the distance!
**Always apply Min-Max Normalization or Z-Score Standardization before running KNN!**
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Boundary Shape
What happens to the KNN decision boundary as $K$ increases from $K=1$ to $K=50$?
(A) The boundary becomes more complex and jagged
(*B) The boundary becomes smoother and more generalized
(C) The boundary turns into a circle
(D) The model overfits the training set
::: explanation
Larger $K$ aggregates more votes across a broader region, smoothing out local noise and creating a smoother, higher-bias decision boundary.
:::
"""

m2_files["m2_11_decision_trees_anatomy_and_intuition.md"] = r"""# Decision Tree Anatomy & The 20 Questions Game

**Understanding recursive binary partitioning and tree hierarchy.**

<a id="the-intuition"></a>
## 1. The Intuition: The 20 Questions Game

Decision Trees ask a hierarchical sequence of threshold questions to segment data into pure, homogeneous subsets.

### Tree Components:
- **Root Node:** Top-level node containing 100% of the training dataset.
- **Internal Decision Nodes:** Intermediate questions testing a specific feature ($x_j \le \theta$).
- **Leaf (Terminal) Nodes:** Final prediction outcomes containing class labels or regression averages.

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Terminal Nodes
What does a leaf node in a classification Decision Tree represent?
(A) A feature split threshold
(*B) The final predicted class label
(C) The learning rate
(D) The gradient vector
::: explanation
Leaf nodes are terminal nodes that do not split any further; they contain the model's final prediction for all instances falling into that leaf.
:::
"""

m2_files["m2_12_information_theory_entropy.md"] = r"""# Information Theory: Shannon Entropy

**Quantifying disorder, impurity, and information content in mathematical bits.**

<a id="the-math"></a>
## 1. Shannon's Entropy Definition

$$ H(S) = -\sum_{i=1}^C p_i \log_2(p_i) $$

Where $p_i$ is the proportion of samples belonging to class $i$.

### Benchmark Values for Binary Classification:
- **100% Pure Node (All Yes):** $H(S) = -(1 \log_2 1) = 0.00\text{ bits}$.
- **50/50 Maximum Disorder (9 Yes, 9 No):** $H(S) = -(0.5 \log_2 0.5 + 0.5 \log_2 0.5) = 1.00\text{ bit}$.

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Maximum Uncertainty
For a 4-class classification problem ($C=4$), what is the maximum possible value of Shannon Entropy?
(A) 1.00 bit
(*B) 2.00 bits ($\log_2 4$)
(C) 0.00 bits
(D) 4.00 bits
::: explanation
Maximum entropy occurs when all classes are equally likely ($p_i = 1/C$). $H_{\max} = \log_2 C = \log_2 4 = 2.00\text{ bits}$.
:::
"""

m2_files["m2_13_information_gain_and_id3_algorithm.md"] = r"""# Information Gain & The ID3 Algorithm

**Greedy recursive tree construction by maximizing entropy reduction.**

<a id="the-math"></a>
## 1. Information Gain Formula

$$ IG(S, A) = H(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v) $$

The ID3 algorithm evaluates all available features at each step and splits on feature $A^* = \arg\max_A IG(S, A)$.

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Splitting Rule
Which feature is chosen for splitting at a node during ID3 tree construction?
(A) The feature with the highest variance
(*B) The feature that maximizes Information Gain
(C) The feature with the lowest entropy
(D) The feature with the smallest number of distinct categories
::: explanation
ID3 uses a greedy heuristic that selects the feature achieving the greatest reduction in entropy (highest Information Gain).
:::
"""

m2_files["m2_14_gini_impurity_and_cart_trees.md"] = r"""# Gini Impurity & CART Binary Trees

**The computational alternative to Entropy used in standard production Decision Trees.**

<a id="the-math"></a>
## 1. Gini Impurity Definition

$$ \text{Gini}(S) = 1 - \sum_{i=1}^C p_i^2 $$

- **Pure Node:** $\text{Gini} = 1 - (1^2) = 0.00$.
- **50/50 Balanced Node:** $\text{Gini} = 1 - (0.5^2 + 0.5^2) = 1 - 0.50 = 0.50$.

::: callout-formula Gini vs Entropy
Gini Impurity avoids expensive $\log_2$ calculations, making it computationally faster to compute while yielding virtually identical split choices to Entropy.
:::

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Computational Difference
Why does Scikit-Learn's CART algorithm use Gini Impurity by default instead of Entropy?
(A) Entropy is mathematically inaccurate
(*B) Gini Impurity does not require logarithmic computations, making training faster
(C) Gini Impurity guarantees zero overfitting
(D) Gini works on continuous features whereas Entropy does not
::: explanation
Computing logarithms ($\log_2$) is computationally more expensive on CPUs than simple squaring and subtraction.
:::
"""

m2_files["m2_15_decision_tree_overfitting_and_pruning.md"] = r"""# Decision Tree Overfitting & Pruning Strategies

**Controlling tree growth to prevent complete training set memorization.**

<a id="the-intuition"></a>
## 1. The Overfitting Problem in Trees

An unconstrained Decision Tree will split until every leaf contains exactly 1 sample ($H=0$). It achieves 100% training accuracy but generalizes terribly on test data.

---

<a id="worked-example"></a>
## 2. Pruning Techniques

::: step [Pre-Pruning (Early Stopping)]
Stop tree expansion early if:
- `max_depth` is reached (e.g. 4 layers).
- `min_samples_split` is below threshold (e.g. $< 10$).
- $\Delta IG < \epsilon$.
:::

::: step [Post-Pruning (Cost-Complexity)]
Grow tree to full size, then prune subtrees upward minimizing:
$$ \mathcal{L}_\alpha(T) = \text{Error}(T) + \alpha |T| $$
Where $|T|$ is the number of terminal leaves and $\alpha$ is the complexity penalty.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Regularization Parameter
In cost-complexity pruning ($\mathcal{L}_\alpha = \text{Error} + \alpha |T|$), what happens as $\alpha \to \infty$?
(A) The tree grows infinitely deep
(*B) The tree collapses to a single root node
(C) The training error becomes zero
(D) The tree becomes a neural network
::: explanation
As $\alpha$ becomes huge, the penalty for having leaves ($|T|$) dominates error, forcing the algorithm to prune all branches down to the root.
:::
"""

m2_files["m2_99_practice_lab_classification.md"] = r"""# Module 2 Practice Lab: The Complete Numerical Vault

**Step-by-step master numerical solutions for all Module 2 examination categories.**

---

## Category 1: Logistic Regression & Odds
**Problem:** A logistic regression model has $z = \theta^Tx = +1.0$. Calculate predicted probability $\hat{y}$ and Odds.
::: step [Solution] Step-by-Step
1. $P(y=1) = \sigma(1.0) = \frac{1}{1 + e^{-1.0}} = \frac{1}{1 + 0.3679} = 0.7311 \quad (73.11\%)$.
2. $\text{Odds} = \frac{0.7311}{1 - 0.7311} = 2.718 = e^1$.
:::

---

## Category 2: Naïve Bayes with Laplace Smoothing
**Problem:** Classify email *"winner meeting"* given $P(\text{Spam})=0.4, P(\text{Ham})=0.6$, vocabulary $|V|=3$.
::: step [Solution] Step-by-Step
- $\text{Score(Spam)} = 0.40 \times \frac{4+1}{10+3} \times \frac{0+1}{10+3} = 0.40 \times \frac{5}{13} \times \frac{1}{13} = 0.01183$.
- $\text{Score(Ham)} = 0.60 \times \frac{1+1}{6+3} \times \frac{5+1}{6+3} = 0.60 \times \frac{2}{9} \times \frac{6}{9} = 0.08889$.
- $P(\text{Ham} \mid \text{Email}) = \frac{0.08889}{0.01183 + 0.08889} = 88.25\% \implies \text{Classify as Ham}$.
:::

---

## Category 3: Decision Tree Information Gain
**Problem:** $S$ has 9 Yes, 5 No ($H(S)=0.9402$). Feature `Windy` has `False` (6 Yes, 2 No, $H=0.8113$) and `True` (3 Yes, 3 No, $H=1.000$).
::: step [Solution] Step-by-Step
1. $H(S \mid \text{Windy}) = \frac{8}{14}(0.8113) + \frac{6}{14}(1.000) = 0.4636 + 0.4286 = 0.8922\text{ bits}$.
2. $IG(S, \text{Windy}) = 0.9402 - 0.8922 = 0.0480\text{ bits}$.
:::
"""

for fname, content in m2_files.items():
    with open(os.path.join(CONTENT_DIR, fname), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(m2_files)} micro-topics for Module 2.")
