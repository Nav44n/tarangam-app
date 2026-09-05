# Module 4: Ensemble Learning, Resampling & The Bias-Variance Tradeoff
## Comprehensive Theory: Bagging, Random Forests, AdaBoost, Cross-Validation, and Expected Prediction Error Decomposition

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Module Alignment:** Module 4 (Meta-Algorithms & Statistical Learning Theory)  
> **Target Audience:** Absolute beginners with no prior knowledge of probability expectations or ensemble methods.

---

# Table of Contents
1. [The Philosophy of Ensembles: The Wisdom of the Crowd](#1-the-philosophy-of-ensembles-the-wisdom-of-the-crowd)
2. [Bagging (Bootstrap Aggregating) & Random Forests](#2-bagging-bootstrap-aggregating--random-forests)
3. [Boosting: Converting Weak Learners to Strong Learners](#3-boosting-converting-weak-learners-to-strong-learners)
4. [The AdaBoost Algorithm: Step-by-Step Derivation](#4-the-adaboost-algorithm-step-by-step-derivation)
5. [Resampling Techniques: Cross-Validation & Bootstrapping](#5-resampling-techniques-cross-validation--bootstrapping)
6. [The Bias-Variance Tradeoff: Mathematical Decomposition](#6-the-bias-variance-tradeoff-mathematical-decomposition)
7. [Model Complexity Curves & Diagnostic Strategies](#7-model-complexity-curves--diagnostic-strategies)
8. [Interactive Knowledge Check Quizzes](#8-interactive-knowledge-check-quizzes)
9. [KTU University Exam Review: Part A & Part B](#9-ktu-university-exam-review-part-a--part-b)

---

# 1. The Philosophy of Ensembles: The Wisdom of the Crowd

::: callout-intuition Condorcet's Jury Theorem (1785)
Suppose a jury of $N$ citizens must decide whether a defendant is guilty or innocent.
- Assume each juror has an independent probability $p > 0.5$ (better than random guessing) of voting correctly.
- If the jury uses **majority voting**, what is the probability that the group makes the right decision?
As the jury size $N \to \infty$, the probability of the group verdict being correct approaches **100% (certainty)**!

In Machine Learning, an **Ensemble** combines multiple diverse base models ("weak learners") to produce a single superior model ("strong learner") that outperforms every individual member.
:::

---

# 2. Bagging (Bootstrap Aggregating) & Random Forests

**Bagging** (Leo Breiman, 1996) trains multiple models in **parallel** on different random subsets of the data to **reduce model variance**.

```
                           [ Original Dataset D (N samples) ]
                                   /       |       \
     Bootstrapping with        Sub-D1    Sub-D2   Sub-D3   (Samples drawn
     Replacement:             (N size)  (N size) (N size)   with replacement)
                                  |         |        |
     Parallel Base Models:     [Tree 1]  [Tree 2] [Tree 3]
                                  \         |        /
     Aggregation:                 [ Majority Voting / Mean ]
                                            |
                                   [ Final Ensemble ]
```

### A. The Bootstrapping Mechanism
From a training dataset of size $N$, draw $N$ samples **uniformly at random with replacement**.
- Because samples are drawn with replacement, some instances appear multiple times in a bootstrap sample, while others are never picked.
- **Probability of an instance NOT being picked in a single draw:** $1 - \frac{1}{N}$.
- **Probability of an instance NEVER being picked in all $N$ draws:**
  $$\lim_{N \to \infty} \left(1 - \frac{1}{N}\right)^N = e^{-1} \approx 0.368 \quad (36.8\%)$$
- These unpicked instances ($36.8\%$) are called the **Out-of-Bag (OOB)** samples, and can be used as a built-in validation test set!

### B. Aggregation
- **Classification:** Majority voting among trees.
- **Regression:** Simple arithmetic average: $\hat{y} = \frac{1}{B} \sum_{b=1}^B f_b(\mathbf{x})$.

### C. Random Forests (Breiman, 2001)
Standard bagging with decision trees has a weakness: if one feature is overwhelmingly strong, all bootstrap trees will split on it first, making the trees correlated.
**Random Forests introduce Feature Bagging:**
At every split in every tree, the algorithm considers only a random subset of $m$ features (typically $m = \sqrt{d}$ for classification). This **de-correlates the trees**, dramatically reducing variance!

---

# 3. Boosting: Converting Weak Learners to Strong Learners

While Bagging trains trees independently in parallel to reduce variance, **Boosting** trains models **sequentially in series to reduce bias**.

### The Boosting Philosophy:
1. Model 1 is trained on the original dataset.
2. We identify which instances Model 1 got wrong.
3. We **increase the importance (weight)** of those hard, misclassified instances.
4. Model 2 is trained with heavy focus on these penalized mistakes.
5. Repeat for $T$ rounds, and combine all models using a **weighted vote** based on their individual accuracy!

---

# 4. The AdaBoost Algorithm: Step-by-Step Derivation

**AdaBoost (Adaptive Boosting)** by Freund and Schapire (1997) is the canonical boosting algorithm.

### Algorithmic Steps:
Let training data be $\{(\mathbf{x}_1, y_1), \dots, (\mathbf{x}_N, y_N)\}$ with labels $y_i \in \{-1, +1\}$.

#### Step 1: Initialize Sample Weights
Assign uniform weights to all training instances:
$$w_i^{(1)} = \frac{1}{N}, \quad \forall i=1, \dots, N$$

#### Step 2: For Iterations $t = 1, 2, \dots, T$:
1. **Train Weak Learner:** Train a base model $h_t(\mathbf{x})$ (typically a simple 1-split **Decision Stump**) using distribution $\mathbf{w}^{(t)}$.
2. **Compute Weighted Error Rate $\epsilon_t$:**
   $$\epsilon_t = \sum_{i: h_t(\mathbf{x}_i) \ne y_i} w_i^{(t)}$$
   *(If $\epsilon_t \ge 0.5$, the learner is no better than random guessing; stop).*
3. **Compute Model Voting Weight $\alpha_t$:**
   $$\alpha_t = \frac{1}{2} \ln\left(\frac{1 - \epsilon_t}{\epsilon_t}\right)$$
   - If $\epsilon_t \to 0$ (very accurate): $\alpha_t$ becomes large and positive.
   - If $\epsilon_t = 0.5$ (random guess): $\alpha_t = \frac{1}{2} \ln(1) = 0$.
4. **Update Sample Weights for Next Round:**
   $$w_i^{(t+1)} = \frac{w_i^{(t)} \exp(-\alpha_t y_i h_t(\mathbf{x}_i))}{Z_t}$$
   - If correctly classified ($y_i h_t(\mathbf{x}_i) = +1$): weight is multiplied by $e^{-\alpha_t}$ (decreased).
   - If misclassified ($y_i h_t(\mathbf{x}_i) = -1$): weight is multiplied by $e^{+\alpha_t}$ (boosted!).
   - $Z_t$ is the normalization factor ensuring $\sum_{i=1}^N w_i^{(t+1)} = 1$.

#### Step 3: Final Combined Ensemble Hypothesis
$$H(\mathbf{x}) = \text{sign}\left(\sum_{t=1}^T \alpha_t h_t(\mathbf{x})\right)$$

---

# 5. Resampling Techniques: Cross-Validation & Bootstrapping

To estimate how a model will perform on future unseen data without leaking test information:

1. **Hold-out Method:** Split data into Training ($70\%$) and Test ($30\%$). Vulnerable to high variance if the test split happens to be unrepresentative.
2. **$K$-Fold Cross-Validation:**
   - Partition data into $K$ equal folds.
   - Train on $K-1$ folds, evaluate on the remaining fold.
   - Repeat $K$ times and average the $K$ performance scores.
3. **Stratified $K$-Fold:** Ensures each fold contains the exact same percentage of each class label as the complete dataset (vital for imbalanced data).
4. **Leave-One-Out Cross-Validation (LOOCV):** Extreme case where $K = N$. Train on $N-1$ points, test on 1 point. Highly unbiased, but computationally expensive.

---

# 6. The Bias-Variance Tradeoff: Mathematical Decomposition

Any supervised machine learning model's prediction error can be mathematically decomposed into three fundamental components: **Bias**, **Variance**, and **Irreducible Noise**.

Let the true relationship between input $x$ and target $y$ be:
$$y = f(x) + \epsilon, \quad \text{where } \mathbb{E}[\epsilon] = 0 \text{ and } \text{Var}(\epsilon) = \sigma^2$$
Let $\hat{f}(x)$ be the model estimated from a training set $\mathcal{D}$.

::: callout-formula Mathematical Derivation of Expected Prediction Error
The expected squared prediction error on a query point $x$ over all possible training sets $\mathcal{D}$ is:
$$\mathbb{E}[(y - \hat{f}(x))^2] = \mathbb{E}[ (f(x) + \epsilon - \hat{f}(x))^2 ]$$
$$= \mathbb{E}[ ((f(x) - \mathbb{E}[\hat{f}(x)]) + (\mathbb{E}[\hat{f}(x)] - \hat{f}(x)) + \epsilon)^2 ]$$
Cross-terms vanish because $\epsilon$ is independent of the training data and $\mathbb{E}[\hat{f}(x) - \mathbb{E}[\hat{f}(x)]] = 0$:
$$\mathbb{E}[(y - \hat{f}(x))^2] = \underbrace{(f(x) - \mathbb{E}[\hat{f}(x)])^2}_{\text{Bias}^2} + \underbrace{\mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]}_{\text{Variance}} + \underbrace{\sigma^2}_{\text{Irreducible Noise}}$$
:::

### Definitions:
1. **$\text{Bias}^2$:** Difference between the true underlying function and the model's average prediction. High bias $\to$ **Underfitting** (model is too simplistic, like fitting a straight line to a parabola).
2. **$\text{Variance}$:** Variability of model predictions if trained on different random datasets. High variance $\to$ **Overfitting** (model memorizes training noise).
3. **$\sigma^2$ (Irreducible Error):** Intrinsic noise in the universe, sensors, or human labeling. Cannot be eliminated by any algorithm.

---

# 7. Model Complexity Curves & Diagnostic Strategies

```
   Error ^
         |      \                                   / (Validation Error)
         |       \                                _/
         |        \                             _/
         |         \                           /
         |          \__  Optimal Complexity  _/
         |             \________*___________/
         |              \
         |               \_______________________ (Training Error)
         +--------------------------------------------------------> Model Complexity
                 Underfitting (High Bias)       Overfitting (High Variance)
```

### Diagnostic Decision Table:
| Diagnostic Symptom | Diagnosis | Solution Strategies |
| :--- | :--- | :--- |
| **High Training Error & High Test Error** | **High Bias (Underfitting)** | Add more features, use a more complex model (e.g. polynomial/deep net), decrease regularization penalty ($\lambda$). |
| **Low Training Error & High Test Error** | **High Variance (Overfitting)** | Collect more training data, reduce feature count, increase regularization ($\lambda$), apply Bagging / Random Forests. |

---

# 8. Interactive Knowledge Check Quizzes

::: quiz Bagging vs Boosting
What is the fundamental architectural difference between Bagging and Boosting?
(A) Bagging uses neural networks while Boosting uses linear regression
(*B) Bagging trains independent models in parallel to reduce variance, while Boosting trains sequential models to reduce bias
(C) Bagging requires continuous labels while Boosting works only on binary labels
(D) Bagging alters sample weights while Boosting alters feature weights
::: explanation
Bagging reduces variance by averaging independent models trained in parallel on bootstrapped subsets. Boosting reduces bias by iteratively training weak models in series, each correcting the mistakes of its predecessor.
:::

::: quiz Bias-Variance Tradeoff
What happens to model bias and variance as we increase the depth of decision trees in a model?
(A) Bias increases, Variance increases
(B) Bias increases, Variance decreases
(*C) Bias decreases, Variance increases
(D) Bias decreases, Variance decreases
::: explanation
Deeper decision trees can partition the input space into tiny leaves, reducing approximation error (lower bias). However, they become extremely sensitive to training set perturbations, causing predictions to fluctuate widely (higher variance / overfitting).
:::

---

# 9. KTU University Exam Review: Part A & Part B

### Part A: Rapid 3-Mark Questions
1. **Explain the purpose of Out-of-Bag (OOB) error in Random Forests.**  
   *Answer:* In bootstrapping with replacement, approximately $36.8\%$ of instances are omitted from each tree. These Out-of-Bag samples act as a built-in validation test set to estimate generalization error without needing cross-validation.
2. **Define Condorcet's Jury Theorem.**  
   *Answer:* If each independent voter has a probability $p > 0.5$ of being correct, the probability that a majority vote of $N$ voters is correct approaches $1.0$ as $N \to \infty$.
3. **State the three components of Expected Prediction Error.**  
   *Answer:* $\text{Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise } (\sigma^2)$.

### Part B: 9-Mark Master Derivation Outline
1. **Derive the mathematical decomposition of Expected Prediction Error into Bias, Variance, and Irreducible Noise.**
   - Formulate the data model $y = f(x) + \epsilon$ with $\mathbb{E}[\epsilon]=0$ and $\text{Var}(\epsilon)=\sigma^2$.
   - Express expected squared error $\mathbb{E}[(y - \hat{f}(x))^2]$.
   - Add and subtract $\mathbb{E}[\hat{f}(x)]$ inside the expectation.
   - Expand the squared trinomial and prove that cross-product expectations evaluate to zero.
   - Conclude with the sum $\text{Bias}^2(\hat{f}(x)) + \text{Var}(\hat{f}(x)) + \sigma^2$.
