# Module 2: Foundations of Classification
## Theoretical Foundations: Generative vs. Discriminative Paradigms & Parametric vs. Non-Parametric Architectures

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Module Alignment:** Module 2 (Classification & Supervised Learning Foundations)  
> **Prerequisites:** Multivariable Calculus (gradients, partial derivatives), Linear Algebra (matrix inversion, covariance matrices, vector spaces), and Probability Theory (Bayes' Theorem, conditional probability distributions, multivariate Gaussians).

---

# Table of Contents
1. [The Taxonomy of Supervised Classification](#1-the-taxonomy-of-supervised-classification)
   - [Formal Problem Statement and Probability Spaces](#formal-problem-statement-and-probability-spaces)
   - [Decision Theory: Loss Matrices and the Bayes Optimal Classifier](#decision-theory-loss-matrices-and-the-bayes-optimal-classifier)
   - [The Bayes Error Rate: The Incompressible Noise Floor](#the-bayes-error-rate-the-incompressible-noise-floor)
2. [Conceptual Foundations: Generative vs. Discriminative Paradigms](#2-conceptual-foundations-generative-vs-discriminative-paradigms)
   - [Pedagogical Intuition: The Master Forger vs. The Customs Detective](#pedagogical-intuition-the-master-forger-vs-the-customs-detective)
   - [Mathematical Anatomy of the Two Paradigms](#mathematical-anatomy-of-the-two-paradigms)
   - [Probabilistic Topography: Modeling the Entire Space vs. The Decision Margin](#probabilistic-topography-modeling-the-entire-space-vs-the-decision-margin)
   - [Asymptotic Error Floors vs. Convergence Rates: The Ng & Jordan Regime](#asymptotic-error-floors-vs-convergence-rates-the-ng--jordan-regime)
   - [Diagnostic Capabilities: Missing Features, Novelty Detection, and Semi-Supervision](#diagnostic-capabilities-missing-features-novelty-detection-and-semi-supervision)
3. [Algorithmic Mechanics: Parametric vs. Non-Parametric Models](#3-algorithmic-mechanics-parametric-vs-non-parametric-models)
   - [Defining the Structural Constraint: Fixed vs. Variable Parameter Cardinality](#defining-the-structural-constraint-fixed-vs-variable-parameter-cardinality)
   - [The Spectrum of Inductive Rigidity](#the-spectrum-of-inductive-rigidity)
   - [The Bias-Variance Trade-Off in Representation](#the-bias-variance-trade-off-in-representation)
   - [Computational Scaling Profiles: Training, Inference, and Storage Complexity](#computational-scaling-profiles-training-inference-and-storage-complexity)
   - [The Curse of Dimensionality on Local Geometries](#the-curse-of-dimensionality-on-local-geometries)
4. [Master Comparative Synthesis for Academic Examinations](#4-master-comparative-synthesis-for-academic-examinations)
   - [Generative vs. Discriminative Dimensions Matrix](#generative-vs-discriminative-dimensions-matrix)
   - [Parametric vs. Non-Parametric Dimensions Matrix](#parametric-vs-non-parametric-dimensions-matrix)
   - [The 2x2 Model Taxonomy Quad-Grid](#the-2x2-model-taxonomy-quad-grid)
5. [Theoretical Derivations & Mathematical Proofs](#5-theoretical-derivations--mathematical-proofs)
   - [Derivation 1: Generative Gaussian Distribution Induces a Linear Discriminant Boundary](#derivation-1-generative-gaussian-distribution-induces-a-linear-discriminant-boundary)
   - [Derivation 2: Optimal Bayes Decision Rule Under Asymmetric Cost Matrices](#derivation-2-optimal-bayes-decision-rule-under-asymmetric-cost-matrices)
   - [Derivation 3: Exact Parameter Scaling in Quadratic vs. Linear Generative Models](#derivation-3-exact-parameter-scaling-in-quadratic-vs-linear-generative-models)
6. [Exhaustive Suite of Worked Numerical Problems](#6-exhaustive-suite-of-worked-numerical-problems)
   - [Worked Problem 1: Generative Posterior vs. Discriminative Boundary in 1D Space](#worked-problem-1-generative-posterior-vs-discriminative-boundary-in-1d-space)
   - [Worked Problem 2: Asymmetric Risk Minimization with Heavy Penalty Discrepancy](#worked-problem-2-asymmetric-risk-minimization-with-heavy-penalty-discrepancy)
   - [Worked Problem 3: Complete Parameter Count Derivation for Multi-Class Architectures](#worked-problem-3-complete-parameter-count-derivation-for-multi-class-architectures)
   - [Worked Problem 4: Non-Parametric Metric Boundary Computation ($k$-NN Distance Ties)](#worked-problem-4-non-parametric-metric-boundary-computation-k-nn-distance-ties)
   - [Worked Problem 5: Non-Parametric Density Estimation Classification (Parzen Windows)](#worked-problem-5-non-parametric-density-estimation-classification-parzen-windows)
   - [Worked Problem 6: Empirical Convergence Crossover Point (The Ng-Jordan Sample Bound)](#worked-problem-6-empirical-convergence-crossover-point-the-ng-jordan-sample-bound)
7. [KTU University Exam Style Review Exercises](#7-ktu-university-exam-style-review-exercises)
   - [Short-Answer Analytical Problems (Part A)](#short-answer-analytical-problems-part-a)
   - [Comprehensive Essay & Derivation Questions (Part B)](#comprehensive-essay--derivation-questions-part-b)

---

# 1. The Taxonomy of Supervised Classification

## Formal Problem Statement and Probability Spaces
In machine learning, **classification** is the process of learning a mapping from an input observation space to a qualitative, categorical output space. Formally, we define:

> **Definition (Classification):** Let $\mathcal{X} \subseteq \mathbb{R}^d$ denote the $d$-dimensional **instance space** (feature space), and let $\mathcal{Y} = \{c_1, c_2, \dots, c_K\}$ denote the discrete **label space** consisting of $K$ mutually exclusive categories. We assume there exists a joint probability distribution $\mathcal{D}$ over $\mathcal{X} \times \mathcal{Y}$. A supervised training set consists of $N$ independent and identically distributed (i.i.d.) observations:
> $$\mathcal{S} = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \dots, (\mathbf{x}_N, y_N)\} \sim \mathcal{D}^N$$
> The objective of a classifier is to construct a decision rule $h: \mathcal{X} \to \mathcal{Y}$ that minimizes the expected loss on unseen instances drawn from $\mathcal{D}$.

When $K = 2$, the problem is a **binary classification** task, conventionally indexed as $\mathcal{Y} = \{0, 1\}$ or $\mathcal{Y} = \{-1, +1\}$. When $K > 2$, it constitutes a **multi-class classification** task.

```
       [ Continuous Observation Space X in R^d ]
                          |
                          v
         +---------------------------------+
         |       Classifier Function       |
         |         h(x; \theta)            |
         +---------------------------------+
                          |
                          v
        [ Discrete Category Space Y in {c_1, ..., c_K} ]
```

---

## Decision Theory: Loss Matrices and the Bayes Optimal Classifier
To evaluate whether a decision rule $h(\mathbf{x})$ is optimal, we formalize the cost of errors using statistical decision theory.

> **Definition (Loss Function):** A loss function $L(y, h(\mathbf{x}))$ assigns a real-valued penalty to the decision $h(\mathbf{x})$ when the true underlying state of nature is $y$. 

In symmetric scenarios, we employ the **0-1 Loss Function**:
$$L_{0-1}(y, h(\mathbf{x})) = \mathbb{I}(y \neq h(\mathbf{x})) = \begin{cases} 0 & \text{if } y = h(\mathbf{x}) \\ 1 & \text{if } y \neq h(\mathbf{x}) \end{cases}$$
where $\mathbb{I}(\cdot)$ is the indicator function.

In real-world settings (e.g., oncology, fraud detection), the penalty for a False Negative differs drastically from a False Positive. We express this via a **Cost/Loss Matrix** $\mathbf{\Lambda} \in \mathbb{R}^{K \times K}$, where $\lambda_{ik} = L(Y = c_i, h(\mathbf{x}) = c_k)$ is the exact cost incurred by predicting class $c_k$ when the true class is $c_i$.

```
                       True State of Nature (Y)
                     Class c_1           Class c_2
                 +-------------------+-------------------+
      Action     |     \lambda_{11}  |     \lambda_{21}  |
Predict c_1      |   (True Positive) |  (False Positive) |
h(x)             +-------------------+-------------------+
      Action     |     \lambda_{12}  |     \lambda_{22}  |
Predict c_2      |  (False Negative) |   (True Negative) |
                 +-------------------+-------------------+
```

The conditional risk (expected loss) of deciding $h(\mathbf{x}) = c_k$ given an observation $\mathbf{x}$ is:
$$R(c_k \mid \mathbf{x}) = \sum_{i=1}^K L(c_i, c_k) P(Y = c_i \mid X = \mathbf{x})$$

The **Bayes Optimal Classifier** is the decision function $h^*(\mathbf{x})$ that chooses the action minimizing this conditional risk:
$$h^*(\mathbf{x}) = \arg\min_{c_k \in \mathcal{Y}} R(c_k \mid \mathbf{x})$$

Under standard symmetric 0-1 loss ($\lambda_{ii} = 0$, and $\lambda_{ik} = 1$ for all $i \neq k$), this reduces to:
$$R(c_k \mid \mathbf{x}) = \sum_{i \neq k} P(Y = c_i \mid X = \mathbf{x}) = 1 - P(Y = c_k \mid X = \mathbf{x})$$
Minimizing risk is identical to maximizing the posterior probability. Thus, the **Bayes Decision Rule** for 0-1 loss is:
$$h^*(\mathbf{x}) = \arg\max_{c_k \in \mathcal{Y}} P(Y = c_k \mid X = \mathbf{x})$$

---

## The Bayes Error Rate: The Incompressible Noise Floor
No statistical model can outperform the Bayes Optimal Classifier. Even with infinite data and unlimited computation, an irreducible error persists if the class-conditional distributions overlap in the feature space.

> **Definition (Bayes Error Rate):** The minimum achievable probability of error across all possible decision rules operating on $\mathcal{X}$:
> $$\epsilon^* = 1 - \mathbb{E}_{\mathbf{x}}\left[ \max_{c_k \in \mathcal{Y}} P(Y = c_k \mid X = \mathbf{x}) \right] = \int_{\mathcal{X}} \left(1 - \max_{k} P(Y = c_k \mid X = \mathbf{x})\right) p(\mathbf{x}) \, d\mathbf{x}$$

For a binary classification task over $\mathbb{R}$:
$$\epsilon^* = \int_{-\infty}^{x^*} P(Y = c_2) p(x \mid Y = c_2) \, dx + \int_{x^*}^{\infty} P(Y = c_1) p(x \mid Y = c_1) \, dx$$
where $x^*$ is the optimal threshold where $P(Y = c_1 \mid x^*) = P(Y = c_2 \mid x^*)$.

```
   Density p(x, c_k)
       ^
       |          Class 1                       Class 2
       |        +---------+                   +---------+
       |       /           \                 /           \
       |      /             \   Overlap     /             \
       |     /               \  (Bayes     /               \
       |    /                 \  Error)   /                 \
       |   /                   \ ::::::  /                   \
       +--+---------------------X::::::X----------------------+----> Feature x
                                x* (Threshold)
```
The shaded region represents the fundamental ambiguity of nature: instances generated by Class 1 that appear on the right side of $x^*$, and instances generated by Class 2 that appear on the left side of $x^*$.

---

# 2. Conceptual Foundations: Generative vs. Discriminative Paradigms

## Pedagogical Intuition: The Master Forger vs. The Customs Detective
To understand the divergence between generative and discriminative modeling, consider the problem of identifying whether a piece of artwork is an authentic masterwork by Johannes Vermeer ($Y = 1$) or a modern counterfeit ($Y = 0$).

### The Generative Approach: The Master Forger
A master forger must learn **everything about how a Vermeer painting comes into existence**. They must learn:
- The exact chemical composition of 17th-century lapis lazuli pigments.
- The thread count and weaving geometry of 350-year-old Dutch canvas.
- The statistical distribution of brush stroke velocities, oil drying craquelure patterns, and light reflections.

Mathematically, the forger learns the complete joint probability $P(X, Y) = P(X \mid Y)P(Y)$. Because they model how the data is generated, **they can paint an authentic-looking Vermeer from scratch**. When handed an unknown canvas $\mathbf{x}$, they calculate: *"What is the probability that the physical process of Vermeer painting would produce these exact brushstrokes?"*

### The Discriminative Approach: The Customs Detective
A customs detective does not need to know how to paint a masterpiece. They have no interest in mixing oil pigments or weaving linen. Instead, they look for **telltale boundaries of separation**:
- Does the white pigment contain Titanium Dioxide (an element never used in paint prior to 1920)?
- Is there modern plastic resin in the wood frame glue?

The detective directly models $P(Y \mid X)$—the conditional probability of authenticity given the observed features. They ignore how a painting is produced; they focus exclusively on the **decision boundary** that separates genuine art from modern fakes.

```
+-------------------------------------------------------------------------------+
| GENERATIVE PARADIGM: Models the complete physical reality of every class.      |
| P(X, Y) = P(X | Y) * P(Y)                                                     |
| Capability: Can synthesize synthetic data; models internal structure.        |
+-------------------------------------------------------------------------------+
                                      vs.
+-------------------------------------------------------------------------------+
| DISCRIMINATIVE PARADIGM: Ignores internal mechanics; models the boundary.     |
| Directly models P(Y | X) or f(x) -> Y                                         |
| Capability: High discriminative precision; cannot synthesize synthetic data.   |
+-------------------------------------------------------------------------------+
```

---

## Mathematical Anatomy of the Two Paradigms

### The Generative Architecture
A generative classifier decomposes the prediction pipeline using **Bayes' Theorem**:

$$P(Y = c_k \mid X = \mathbf{x}) = \frac{P(X = \mathbf{x} \mid Y = c_k) P(Y = c_k)}{P(X = \mathbf{x})} = \frac{P(X = \mathbf{x} \mid Y = c_k) P(Y = c_k)}{\sum_{j=1}^K P(X = \mathbf{x} \mid Y = c_j) P(Y = c_j)}$$

To execute this, the model must estimate two independent statistical structures from the empirical training data:
1. **The Class Prior $P(Y = c_k)$:** The base rate distribution of categories in the natural universe.
2. **The Class-Conditional Likelihood $P(X = \mathbf{x} \mid Y = c_k)$:** The probability density function of observing feature vector $\mathbf{x}$ given that the class is known to be $c_k$.

Once trained, inference requires computing the joint probability $P(\mathbf{x}, c_k) = P(\mathbf{x} \mid c_k) P(c_k)$ for all $k$, and normalizing by the evidence $P(\mathbf{x})$.

*Exemplar Models:* Gaussian Discriminant Analysis (QDA/LDA), Naive Bayes, Hidden Markov Models (HMMs), Bayesian Networks, Gaussian Mixture Models (GMMs).

---

### The Discriminative Architecture
A discriminative classifier bypasses the intermediate class-conditional density estimation entirely. It optimizes its parameter set $\mathbf{w}$ to directly map features $\mathbf{x}$ to class probabilities $P(Y \mid X)$ or deterministic labels $h(\mathbf{x})$.

For probabilistic discriminative models (e.g., Logistic Regression), the relationship is modeled directly via a link function:
$$P(Y = 1 \mid X = \mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$$

For deterministic discriminative models (e.g., Support Vector Machines), the architecture seeks a separating hyperplane:
$$h(\mathbf{x}) = \text{sign}(\mathbf{w}^T \mathbf{x} + b)$$
without calculating class probabilities.

*Exemplar Models:* Logistic Regression, Support Vector Machines (SVM), Multi-Layer Perceptrons (Neural Networks), Decision Trees, Random Forests, Gradient Boosted Trees (XGBoost).

---

## Probabilistic Topography: Modeling the Entire Space vs. The Decision Margin

The operational difference between these two paradigms lies in how they allocate statistical modeling capacity across the input domain $\mathcal{X}$.

```
GENERATIVE TOPOGRAPHY:                               DISCRIMINATIVE TOPOGRAPHY:
Full Probability Landscapes                         Only the Boundary Matters

      x2 ^                                                x2 ^
         |      ( Class 1 )                                  |           /
         |     .-'""'-.                                      |          /
         |    /  .---. \                                     |         /  Boundary:
         |   |  ( Max ) |                                    |        /   P(Y=1|x) = 0.5
         |    \  '---' /                                     |       /
         |     '-.__.-'                                      |      /
         |                                                   |     /
         |                  ( Class 2 )                      |    /
         |                 .-'""'-.                          |   /
         |                /  .---. \                         |  /
         |               |  ( Max ) |                        | /
         |                \  '---' /                         |/
         +-----------------------------> x1                  +-----------------------------> x1
   Models the contours of P(x|c_1) and P(x|c_2)         Models ONLY the separating line w^T x = 0
```

1. **Generative Modeling allocates capacity everywhere:** A generative model expends mathematical parameters fitting the probability density of instances throughout the entire feature space—including regions far away from the decision boundary. If 90% of the training points for Class 1 lie in a dense cluster far from Class 2, a generative model spends most of its capacity fitting the shape, covariance, and tails of that distant cluster.

2. **Discriminative Modeling concentrates capacity on the boundary:** A discriminative model allocates its parameters solely to regions where classes overlap. It does not care whether the instances of Class 1 form a spherical Gaussian, a spiral, or a multi-modal distribution; it only cares whether a hyper-plane or non-linear surface can separate Class 1 from Class 2.

> **Vapnik's Statistical Maxim (The Empirical Principle):** > *"If you possess a restricted amount of information to solve a specific problem, do not solve a more general problem as an intermediate step. Solve the target problem directly."* > *(Vladimir Vapnik, Estimation of Dependences Based on Empirical Data, 1982)*

Vapnik's maxim formalizes why discriminative models dominate predictive classification: estimating $P(\mathbf{x} \mid y)$ is solving a far more difficult intermediate problem (density estimation) than the target problem of finding a boundary where $P(y=1 \mid \mathbf{x}) = 0.5$.

---

## Asymptotic Error Floors vs. Convergence Rates: The Ng & Jordan Regime
In their seminal 2001 NIPS paper, *"On Discriminative vs. Generative Classifiers: A comparison of logistic regression and naive Bayes,"* Andrew Ng and Michael I. Jordan proved that the choice between generative and discriminative paradigms involves a fundamental trade-off between **sample efficiency** and **asymptotic accuracy**.

```
Generalization
Error (E)
   ^
   |
   | \
   |  \
   |   \  Naive Bayes (Generative) Hits asymptote fast: O(log d) samples
   |----\================================== Asymptotic Error E_gen
   |     \
   |      \
   |       \  Logistic Regression (Discriminative) Slow convergence: O(d) samples
   |        \
   |         \----------------------------- Lower Asymptotic Error E_dis
   |
   +--------------------------------------------------------> Sample Size (N)
              N_crossover
```

### 1. The Generative Regime (Low Sample Size $N$)
Generative models (like Naive Bayes) treat features as governed by structural assumptions (e.g., conditional independence). Because of this strong inductive bias, the model parameters converge to their optimal values very rapidly:
$$N = \mathcal{O}(\log d)$$
where $d$ is the feature dimensionality. With very few training samples, a generative model quickly learns the means and variances of the data. Thus, for small datasets, **generative classifiers often outperform discriminative models**.

### 2. The Discriminative Regime (High Sample Size $N \to \infty$)
Discriminative models (like Logistic Regression) make fewer structural assumptions about the data distributions. However, their convergence rate scales linearly with feature dimensionality:
$$N = \mathcal{O}(d)$$
Because they make fewer distributional assumptions, discriminative models are less constrained by model misspecification. As $N \to \infty$, the asymptotic error of the discriminative model ($\epsilon_{\text{dis}}$) is strictly lower than or equal to the asymptotic error of the generative model ($\epsilon_{\text{gen}}$):
$$\lim_{N \to \infty} \epsilon_{\text{dis}} \le \lim_{N \to \infty} \epsilon_{\text{gen}}$$

If the generative model's distributional assumption (e.g., Gaussianity or conditional independence) is wrong, its error will remain high no matter how much data is provided. The discriminative model adjusts its weights to separate the true boundary, reaching a superior asymptotic performance floor.

---

## Diagnostic Capabilities: Missing Features, Novelty Detection, and Semi-Supervision
Because generative models capture the full joint distribution $P(X, Y)$, they can perform inference tasks that are impossible for purely discriminative architectures:

### 1. Marginalization Over Missing Features
Suppose during deployment, an incomplete sensor vector $\mathbf{x} = [x_1, \text{NaN}, x_3]^T$ arrives, where feature $x_2$ is unobserved.
- **Discriminative Model Failure:** A model relying on $f(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b = w_1 x_1 + w_2 x_2 + w_3 x_3 + b$ cannot compute the linear combination without $x_2$. It requires ad-hoc imputation (e.g., mean replacement, iterative regression).
- **Generative Model Natural Solution:** The missing variable is integrated (marginalized) out:
  $$P(X_1 = x_1, X_3 = x_3 \mid Y = c_k) = \int_{-\infty}^\infty P(X_1 = x_1, X_2 = \xi, X_3 = x_3 \mid Y = c_k) \, d\xi$$
  The model computes the exact posterior probability conditioned strictly on the observed features without heuristic imputation.

### 2. Outlier and Novelty Detection
Because a generative model estimates the marginal data evidence:
$$p(\mathbf{x}) = \sum_{k=1}^K P(X = \mathbf{x} \mid Y = c_k) P(Y = c_k)$$
it can identify anomalies. If an incoming query $\mathbf{x}^*$ falls in a region where $p(\mathbf{x}^*) < \tau$ (where $\tau$ is a density threshold), the system flags the instance as an **out-of-distribution (OOD) anomaly** or novel input. 
A discriminative model cannot do this: an observation located 1,000 standard deviations away from the training clusters can still produce a confident classification (e.g., $P(Y=1 \mid \mathbf{x}) = 0.999$) simply because it lies deep on one side of the separating hyperplane.

### 3. Semi-Supervised Learning Capacity
Generative models naturally incorporate unlabelled data pools $\mathcal{U} = \{\mathbf{x}_{N+1}, \dots, \mathbf{x}_{N+M}\}$ alongside labelled data $\mathcal{S}$ via the Expectation-Maximization (EM) algorithm. Unlabelled instances help shape the overall density estimates $p(\mathbf{x})$, stabilizing the cluster parameters without human annotations.

---

# 3. Algorithmic Mechanics: Parametric vs. Non-Parametric Models

## Defining the Structural Constraint: Fixed vs. Variable Parameter Cardinality
The second foundational axis of classification taxonomy governs how a model's complexity changes as training data increases.

```
                    PARAMETRIC:                          NON-PARAMETRIC:
       Model complexity is locked at design time.    Model complexity expands with data.

                     +---------+                          +---------+
       Train Data:   | 100 pts |            Train Data:   | 100 pts |
                     +---------+                          +---------+
                          |                                    |
                          v                                    v
       Parameters:   [\theta_1, \theta_2]   Parameters:   [\theta_1, ..., \theta_100]
                     (Cardinality = 2)                    (Cardinality = 100)

                     +-------------+                      +-------------+
       Train Data:   | 100,000 pts |        Train Data:   | 100,000 pts |
                     +-------------+                      +-------------+
                          |                                    |
                          v                                    v
       Parameters:   [\theta_1, \theta_2]   Parameters:   [\theta_1, ..., \theta_100000]
                     (Cardinality = 2)                    (Cardinality = 100,000)
```

> **Definition (Parametric Model):** A learning model governed by a fixed set of parameters $\mathbf{\Theta} \in \mathbb{R}^m$, where the dimensionality $m$ is finite, predetermined, and strictly independent of the number of training samples $N$:
> $$|\mathbf{\Theta}| = \mathcal{O}(1) \quad \text{with respect to } N$$
> A parametric model summarizes the entire training history into a static parameter vector $\mathbf{\Theta}$. Once $\mathbf{\Theta}$ is estimated, the original training data $\mathcal{S}$ can be discarded.

> **Definition (Non-Parametric Model):** A learning model where the functional form is not predetermined, and the effective number of parameters grows dynamically with the size of the training dataset $N$:
> $$|\mathbf{\Theta}| = f(N) \implies \lim_{N \to \infty} |\mathbf{\Theta}| = \infty$$
> Non-parametric models do not mean "zero parameters"; rather, they represent an infinite-dimensional hypothesis space where the data points themselves act as the parameters of the model.

---

## The Spectrum of Inductive Rigidity
The divide between parametric and non-parametric algorithms reflects a trade-off in **inductive bias**:

### 1. High Inductive Rigidity (Parametric Models)
A parametric model makes strong prior assumptions about the shape of the target function.
- *Linear Regression / Logistic Regression:* Assumes the log-odds or output surface is a flat hyperplane.
- *Linear Discriminant Analysis (LDA):* Assumes the data for every class was generated by a multivariate Gaussian distribution with an identical covariance matrix.

If these assumptions are correct, the model performs well, requires minimal data, and is easy to interpret. However, if the ground-truth function does not match this form (e.g., if the true boundary is sinusoidal, toroidal, or disjoint), the model fails due to high bias.

### 2. High Structural Flexibility (Non-Parametric Models)
Non-parametric models make weak prior assumptions about the underlying distribution. They assume local properties, such as smoothness: *"Points close to one another in feature space should share similar class labels."*
- *$k$-Nearest Neighbors ($k$-NN):* Makes no global shape assumption; the decision boundary flexes around local neighborhoods.
- *Kernel Density Estimation (Parzen Windows):* Fits a small local probability bump (kernel) over every single training observation.
- *Decision Trees (Unpruned CART):* Recursively partitions the feature space into arbitrary hyper-rectangles based on sample density.

---

## The Bias-Variance Trade-Off in Representation
The classification risk decomposes into three distinct sources: **Bias**, **Variance**, and irreducible **Bayes Error**:

$$\mathbb{E}_{\mathcal{S}} \left[ (y - \hat{h}(\mathbf{x}; \mathcal{S}))^2 \right] = \underbrace{\left(\text{Bias}[\hat{h}(\mathbf{x})]\right)^2}_{\text{Structural Inadequacy}} + \underbrace{\text{Var}[\hat{h}(\mathbf{x})]}_{\text{Sample Sensitivity}} + \underbrace{\sigma^2}_{\text{Bayes Noise Floor}}$$

```
Error
  ^
  |       Total Error Curve
  |        \             /
  |         \   .-.     /
  |          \ /   \   /
  |  Bias^2   V     \ /   Variance
  |   \              X             /
  |    \            / \           /
  |     '--.__     /   '--.______/
  |           '---'
  +---------------------------------------------> Model Flexibility
     PARAMETRIC                        NON-PARAMETRIC
     (Rigid, High Bias,                (Flexible, Low Bias,
      Low Variance)                     High Variance)
```

1. **Parametric models sit on the High-Bias / Low-Variance end:** Because their functional form is constrained, training them on different subsets of data yields very similar models (low variance). However, if the true relationship is non-linear, a linear parametric model cannot fit it, leading to underfitting (high bias).

2. **Non-Parametric models sit on the Low-Bias / High-Variance end:** Because they can take on almost any shape, they can model intricate boundaries with minimal bias. However, they are sensitive to variations in the training set: changing a few data points can shift the decision boundary, leading to overfitting (high variance). Regularization (e.g., increasing the neighborhood size $k$ in $k$-NN, or pruning decision trees) helps control this variance.

---

## Computational Scaling Profiles: Training, Inference, and Storage Complexity

| Dimension | Parametric Architectures (e.g., Logistic Regression) | Non-Parametric Architectures (e.g., $k$-NN) |
| :--- | :--- | :--- |
| **Training Time Complexity** | **Heavy:** $\mathcal{O}(N \cdot d \cdot \text{iterations})$ to run gradient descent / optimization. | **Zero to Minimal (Lazy Learning):** $\mathcal{O}(1)$ or $\mathcal{O}(N d)$ to build index trees (kd-tree). |
| **Inference Time Complexity** | **Lightweight:** $\mathcal{O}(d)$ to evaluate $h(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b$. | **Heavy:** $\mathcal{O}(N \cdot d)$ to calculate distances across all stored training samples. |
| **Memory / Storage Profile** | **Constant:** $\mathcal{O}(d)$ to store the weight vector $\mathbf{w}$. Discards raw data $\mathcal{S}$. | **Linear Growth:** $\mathcal{O}(N \cdot d)$ because all training observations must remain in RAM. |
| **Data Requirement ($N$)** | Low sample requirements if assumptions are valid. | Needs large sample sizes to populate high-dimensional neighborhoods. |

---

## The Curse of Dimensionality on Local Geometries
Non-parametric metric models (like $k$-NN) rely on distance metrics (e.g., Euclidean distance) to identify local neighborhoods. In high-dimensional spaces ($d \gg 1$), these methods run into the **Curse of Dimensionality** (introduced by Richard Bellman in 1957).

### 1. Exponential Growth of Volume
To capture a fixed fraction $r$ of the data volume in a $d$-dimensional unit hypercube, the side length of the neighborhood sub-cube $e_d(r)$ is:
$$e_d(r) = r^{1/d}$$

```
DIMENSION d = 1:                    DIMENSION d = 2:                  DIMENSION d = 10:
To capture 10% volume:              To capture 10% volume:            To capture 10% volume:
e_1(0.1) = 0.10                     e_2(0.1) = sqrt(0.1) = 0.316      e_10(0.1) = (0.1)^0.1 = 0.794

[===       ]                        +----------+                      +--------------------+
Length = 10% of axis                |   |      |                      |         |          |
                                    |---+--    |                      |         |          |
                                    |   |      |                      |---------+--        |
                                    +----------+                      |         |          |
                                    Length = 31.6% of axis            +--------------------+
                                                                      Length = 79.4% of axis!
```
In $d = 100$ dimensions, capturing just $1\%$ of the volume requires a hypercube spanning $e_{100}(0.01) = 0.01^{0.01} \approx 0.955$ ($95.5\%$ of the entire length of every coordinate axis). The concept of a "local neighborhood" breaks down—the nearest neighbors are located on the far edges of the space.

### 2. Metric Degeneration (Distance Concentration Phenomenon)
Let $\mathbf{x} \in \mathbb{R}^d$ be a random vector with independent coordinates. As the dimensionality $d \to \infty$, the distance to the nearest neighbor ($D_{\min}$) and the distance to the furthest neighbor ($D_{\max}$) converge to the same value:
$$\lim_{d \to \infty} \frac{D_{\max} - D_{\min}}{D_{\min}} \to 0$$
In high dimensions, every point becomes roughly equidistant from every other point. Distance metrics lose their discriminative power, causing non-parametric nearest-neighbor classifiers to degrade toward random guessing unless dimensionality reduction is applied first.

---

# 4. Master Comparative Synthesis for Academic Examinations

## Generative vs. Discriminative Dimensions Matrix

| Evaluation Dimension | Generative Models (e.g., GDA, Naive Bayes) | Discriminative Models (e.g., Logistic Regression, SVM) |
| :--- | :--- | :--- |
| **Mathematical Objective** | Models the Joint Distribution: $P(X, Y) = P(X \mid Y)P(Y)$ | Models the Conditional Probability $P(Y \mid X)$ or direct boundary $h(X)$ |
| **Statistical Optimization Target** | Maximizes the Joint Likelihood: $\prod_{i=1}^N P(\mathbf{x}_i, y_i)$ | Maximizes the Conditional Likelihood: $\prod_{i=1}^N P(y_i \mid \mathbf{x}_i)$ |
| **Inference Mechanism** | Uses Bayes' Theorem: $P(Y \mid X) = \frac{P(X \mid Y)P(Y)}{\sum P(X \mid Y)P(Y)}$ | Directly computes the model equation: $\sigma(\mathbf{w}^T \mathbf{x} + b)$ |
| **Decision Boundary Construction** | Implicit: Arises where $P(X \mid c_1)P(c_1) = P(X \mid c_2)P(c_2)$ | Explicit: Solves directly for the separating surface $\mathbf{w}^T \mathbf{x} = 0$ |
| **Sample Complexity (Convergence Rate)** | Faster: Converges with $N = \mathcal{O}(\log d)$ samples | Slower: Converges with $N = \mathcal{O}(d)$ samples |
| **Asymptotic Error Floor ($\lim N \to \infty$)** | Higher error floor if distributional assumptions are violated | Lower error floor; robust to distribution shapes |
| **Handling Missing Features** | Natural: Marginalizes unobserved features via integration | Difficult: Requires ad-hoc data imputation |
| **Outlier / Novelty Detection** | Strong: Evaluates the marginal data likelihood $p(\mathbf{x}) < \tau$ | Weak: Produces overconfident classifications on distant anomalies |
| **Generative Synthesis** | Capable: Can sample from $P(X \mid Y)$ to generate synthetic data | Incapable: Cannot generate input feature vectors $\mathbf{x}$ |

---

## Parametric vs. Non-Parametric Dimensions Matrix

| Evaluation Dimension | Parametric Models (e.g., Logistic Regression, LDA) | Non-Parametric Models (e.g., $k$-NN, Decision Trees) |
| :--- | :--- | :--- |
| **Parameter Cardinality ($|\mathbf{\Theta}|$)** | Fixed: Finite constant independent of dataset size $N$ | Dynamic: Scales with the number of training samples $N$ |
| **Inductive Assumptions** | Strong: Assumes explicit functional forms (e.g., linear, Gaussian) | Weak: Assumes broad smoothness or locality |
| **Bias-Variance Profile** | High structural bias; low sample variance | Low structural bias; high sample variance |
| **Risk of Structural Misspecification** | High: Fails if the true boundary does not match assumptions | Low: Can adjust to complex non-linear boundaries |
| **Computational Cost (Training)** | Typically high: Requires iterative numerical optimization | Low: Often lazy (stores points with $\mathcal{O}(1)$ training) |
| **Computational Cost (Inference)** | Fast: $\mathcal{O}(d)$ vector dot product computation | Slow: $\mathcal{O}(Nd)$ distance scans over training data |
| **Memory Footprint** | Constant $\mathcal{O}(d)$: Training dataset can be discarded | High $\mathcal{O}(Nd)$: Must keep training data in memory |
| **Curse of Dimensionality** | Relatively robust: Directly regularizes the $d$ feature weights | Highly vulnerable: Distances collapse as $d \to \infty$ |
| **Model Interpretability** | High: Direct access to feature weights $\mathbf{w}$ | Variable: Often acts as a local black-box lookup |

---

## The 2x2 Model Taxonomy Quad-Grid

Every classical machine learning classification algorithm maps into one of four taxonomic categories:

```
                          +-----------------------------------+-----------------------------------+
                          |            PARAMETRIC             |          NON-PARAMETRIC           |
+-------------------------+-----------------------------------+-----------------------------------+
|                         | • Gaussian Discriminant Analysis  | • Kernel Density Estimation       |
|                         |   (LDA / QDA)                     |   (Parzen Windows Classifier)     |
|       GENERATIVE        | • Naive Bayes (Gaussian, Multi)   | • Non-Parametric Bayesian Nets    |
|                         | • Hidden Markov Models (HMM)      | • Dirichlet Process Mixture       |
|                         | • Mixture of Gaussians (GMM)      |   Models (DPMM)                   |
+-------------------------+-----------------------------------+-----------------------------------+
|                         | • Logistic Regression             | • k-Nearest Neighbors (k-NN)      |
|                         | • Linear / Quadratic SVMs         | • Kernel Support Vector Machines  |
|      DISCRIMINATIVE     | • Multi-Layer Perceptrons (MLPs)  | • Decision Trees (CART, C4.5)     |
|                         | • Linear Perceptron               | • Random Forests / Boosted Trees  |
+-------------------------+-----------------------------------+-----------------------------------+
```

---

# 5. Theoretical Derivations & Mathematical Proofs

## Derivation 1: Generative Gaussian Distribution Induces a Linear Discriminant Boundary

A fundamental result in statistical learning theory shows that **a generative model with Gaussian class-conditionals and equal covariance matrices induces a posterior distribution that has the exact mathematical form of logistic regression**.

### Assumptions
1. Binary classification: $\mathcal{Y} = \{0, 1\}$.
2. Class-conditional likelihoods follow multivariate normal distributions:
   $$P(\mathbf{x} \mid Y = k) = \frac{1}{(2\pi)^{d/2} |\mathbf{\Sigma}_k|^{1/2}} \exp\left( -\frac{1}{2} (\mathbf{x} - \mathbf{\mu}_k)^T \mathbf{\Sigma}_k^{-1} (\mathbf{x} - \mathbf{\mu}_k) \right)$$
3. **Homoscedasticity Assumption:** The covariance matrices are shared across classes:
   $$\mathbf{\Sigma}_0 = \mathbf{\Sigma}_1 = \mathbf{\Sigma}$$
4. Class priors are $P(Y = 1) = \pi_1$ and $P(Y = 0) = \pi_0 = 1 - \pi_1$.

### Algebraic Derivation
We express the posterior log-odds ratio:
$$\log \frac{P(Y = 1 \mid \mathbf{x})}{P(Y = 0 \mid \mathbf{x})} = \log \left( \frac{\frac{P(\mathbf{x} \mid Y = 1)P(Y = 1)}{P(\mathbf{x})}}{\frac{P(\mathbf{x} \mid Y = 0)P(Y = 0)}{P(\mathbf{x})}} \right) = \log \frac{P(\mathbf{x} \mid Y = 1)}{P(\mathbf{x} \mid Y = 0)} + \log \frac{P(Y = 1)}{P(Y = 0)}$$

Substitute the Gaussian likelihoods into the ratio:
$$\frac{P(\mathbf{x} \mid Y = 1)}{P(\mathbf{x} \mid Y = 0)} = \frac{\frac{1}{(2\pi)^{d/2}|\mathbf{\Sigma}|^{1/2}} \exp\left( -\frac{1}{2}(\mathbf{x} - \mathbf{\mu}_1)^T \mathbf{\Sigma}^{-1} (\mathbf{x} - \mathbf{\mu}_1) \right)}{\frac{1}{(2\pi)^{d/2}|\mathbf{\Sigma}|^{1/2}} \exp\left( -\frac{1}{2}(\mathbf{x} - \mathbf{\mu}_0)^T \mathbf{\Sigma}^{-1} (\mathbf{x} - \mathbf{\mu}_0) \right)}$$

Cancel normalization constants and take the natural logarithm:
$$\log \frac{P(\mathbf{x} \mid Y = 1)}{P(\mathbf{x} \mid Y = 0)} = -\frac{1}{2} \left[ (\mathbf{x} - \mathbf{\mu}_1)^T \mathbf{\Sigma}^{-1} (\mathbf{x} - \mathbf{\mu}_1) - (\mathbf{x} - \mathbf{\mu}_0)^T \mathbf{\Sigma}^{-1} (\mathbf{x} - \mathbf{\mu}_0) \right]$$

Expand the quadratic matrix products:
$$(\mathbf{x} - \mathbf{\mu}_k)^T \mathbf{\Sigma}^{-1} (\mathbf{x} - \mathbf{\mu}_k) = \mathbf{x}^T \mathbf{\Sigma}^{-1} \mathbf{x} - 2 \mathbf{\mu}_k^T \mathbf{\Sigma}^{-1} \mathbf{x} + \mathbf{\mu}_k^T \mathbf{\Sigma}^{-1} \mathbf{\mu}_k$$

Substitute the expansions into the difference:
$$\log \frac{P(\mathbf{x} \mid Y = 1)}{P(\mathbf{x} \mid Y = 0)} = -\frac{1}{2} \left[ \mathbf{x}^T \mathbf{\Sigma}^{-1}\mathbf{x} - 2\mathbf{\mu}_1^T \mathbf{\Sigma}^{-1}\mathbf{x} + \mathbf{\mu}_1^T \mathbf{\Sigma}^{-1}\mathbf{\mu}_1 - \left( \mathbf{x}^T \mathbf{\Sigma}^{-1}\mathbf{x} - 2\mathbf{\mu}_0^T \mathbf{\Sigma}^{-1}\mathbf{x} + \mathbf{\mu}_0^T \mathbf{\Sigma}^{-1}\mathbf{\mu}_0 \right) \right]$$

The quadratic term $\mathbf{x}^T \mathbf{\Sigma}^{-1} \mathbf{x}$ cancels out:
$$\log \frac{P(\mathbf{x} \mid Y = 1)}{P(\mathbf{x} \mid Y = 0)} = (\mathbf{\mu}_1 - \mathbf{\mu}_0)^T \mathbf{\Sigma}^{-1} \mathbf{x} - \frac{1}{2}\mathbf{\mu}_1^T \mathbf{\Sigma}^{-1}\mathbf{\mu}_1 + \frac{1}{2}\mathbf{\mu}_0^T \mathbf{\Sigma}^{-1}\mathbf{\mu}_0$$

Add the log prior ratio:
$$\log \frac{P(Y = 1 \mid \mathbf{x})}{P(Y = 0 \mid \mathbf{x})} = \underbrace{\left[ (\mathbf{\mu}_1 - \mathbf{\mu}_0)^T \mathbf{\Sigma}^{-1} \right]}_{\mathbf{w}^T} \mathbf{x} + \underbrace{\left[ -\frac{1}{2}\mathbf{\mu}_1^T \mathbf{\Sigma}^{-1}\mathbf{\mu}_1 + \frac{1}{2}\mathbf{\mu}_0^T \mathbf{\Sigma}^{-1}\mathbf{\mu}_0 + \log \frac{\pi_1}{\pi_0} \right]}_{w_0}$$

This matches the linear equation:
$$\log \frac{P(Y = 1 \mid \mathbf{x})}{1 - P(Y = 1 \mid \mathbf{x})} = \mathbf{w}^T \mathbf{x} + w_0$$

Solve for $P(Y = 1 \mid \mathbf{x})$ using the logistic sigmoid function $\sigma(z) = \frac{1}{1 + e^{-z}}$:
$$P(Y = 1 \mid \mathbf{x}) = \frac{1}{1 + \exp(-(\mathbf{w}^T \mathbf{x} + w_0))} = \sigma(\mathbf{w}^T \mathbf{x} + w_0)$$

$$\blacksquare$$

> **Key Takeaway:** Both Linear Discriminant Analysis (Generative) and Logistic Regression (Discriminative) share the identical linear log-odds form $\sigma(\mathbf{w}^T \mathbf{x} + w_0)$. However, **LDA computes $\mathbf{w}$ and $w_0$ empirically using sample means and pooled covariance**, whereas **Logistic Regression optimizes $\mathbf{w}$ and $w_0$ directly using maximum conditional likelihood (gradient ascent)** without assuming the inputs $\mathbf{x}$ are normally distributed.

---

## Derivation 2: Optimal Bayes Decision Rule Under Asymmetric Cost Matrices

Let $\mathcal{Y} = \{c_1, c_2\}$. Let the loss incurred by decision $h(\mathbf{x}) = \alpha_i$ given true class $c_j$ be denoted $\lambda_{ij} = L(c_j, \alpha_i)$.

The conditional risk of selecting action $\alpha_1$ (predicting class $c_1$) is:
$$R(\alpha_1 \mid \mathbf{x}) = \lambda_{11} P(c_1 \mid \mathbf{x}) + \lambda_{21} P(c_2 \mid \mathbf{x})$$

The conditional risk of selecting action $\alpha_2$ (predicting class $c_2$) is:
$$R(\alpha_2 \mid \mathbf{x}) = \lambda_{12} P(c_1 \mid \mathbf{x}) + \lambda_{22} P(c_2 \mid \mathbf{x})$$

The Bayes decision rule dictates deciding class $c_1$ if and only if:
$$R(\alpha_1 \mid \mathbf{x}) < R(\alpha_2 \mid \mathbf{x})$$

Substitute the risk definitions:
$$\lambda_{11} P(c_1 \mid \mathbf{x}) + \lambda_{21} P(c_2 \mid \mathbf{x}) < \lambda_{12} P(c_1 \mid \mathbf{x}) + \lambda_{22} P(c_2 \mid \mathbf{x})$$

Group identical posterior terms:
$$(\lambda_{21} - \lambda_{22}) P(c_2 \mid \mathbf{x}) < (\lambda_{12} - \lambda_{11}) P(c_1 \mid \mathbf{x})$$

Assuming standard conditions where misclassification is penalized more heavily than correct classification ($\lambda_{12} > \lambda_{11}$):
$$\frac{P(c_1 \mid \mathbf{x})}{P(c_2 \mid \mathbf{x})} > \frac{\lambda_{21} - \lambda_{22}}{\lambda_{12} - \lambda_{11}}$$

Apply Bayes' theorem to convert posteriors into likelihoods and priors:
$$\frac{p(\mathbf{x} \mid c_1) P(c_1) / p(\mathbf{x})}{p(\mathbf{x} \mid c_2) P(c_2) / p(\mathbf{x})} > \frac{\lambda_{21} - \lambda_{22}}{\lambda_{12} - \lambda_{11}}$$

$$\Lambda(\mathbf{x}) = \frac{p(\mathbf{x} \mid c_1)}{p(\mathbf{x} \mid c_2)} > \underbrace{\left( \frac{\lambda_{21} - \lambda_{22}}{\lambda_{12} - \lambda_{11}} \right) \left( \frac{P(c_2)}{P(c_1)} \right)}_{\theta_{\text{critical}}}$$

$$\blacksquare$$

> **Conclusion:** The optimal decision rule computes the **Likelihood Ratio** $\Lambda(\mathbf{x})$ and compares it against a threshold $\theta_{\text{critical}}$. When loss is symmetric (0-1 loss) and priors are balanced ($P(c_1) = P(c_2)$), $\theta_{\text{critical}} = 1.0$. As the cost of missing class $c_1$ ($\lambda_{12}$) grows large, $\theta_{\text{critical}} \to 0$, shifting the threshold to predict class $c_1$ even under low posterior probability.

---

## Derivation 3: Exact Parameter Scaling in Quadratic vs. Linear Generative Models

Let the instance space dimension be $d$, and let the number of classes be $K$. We analyze the parameter complexity of two classical generative models:

### 1. Quadratic Discriminant Analysis (QDA)
In QDA, each class $k \in \{1, \dots, K\}$ has its own mean $\mathbf{\mu}_k$ and unique covariance matrix $\mathbf{\Sigma}_k$.
- **Prior Probabilities:** $K - 1$ independent parameters (since $\sum \pi_k = 1$).
- **Mean Vectors:** Each mean $\mathbf{\mu}_k \in \mathbb{R}^d$ contains $d$ parameters. For $K$ classes:
  $$\text{Parameters}_{\text{means}} = K \cdot d$$
- **Covariance Matrices:** Each covariance matrix $\mathbf{\Sigma}_k \in \mathbb{R}^{d \times d}$ is symmetric. The number of independent entries in a $d \times d$ symmetric matrix is:
  $$\frac{d(d + 1)}{2}$$
  For $K$ independent classes:
  $$\text{Parameters}_{\text{cov}} = K \cdot \frac{d(d + 1)}{2}$$

Summing all components:
$$\text{Total Parameters}_{\text{QDA}} = (K - 1) + K \cdot d + K \cdot \frac{d(d + 1)}{2} = \mathcal{O}(K \cdot d^2)$$

### 2. Linear Discriminant Analysis (LDA)
In LDA, the classes share a single pooled covariance matrix $\mathbf{\Sigma}$.
- **Prior Probabilities:** $K - 1$ parameters.
- **Mean Vectors:** $K \cdot d$ parameters.
- **Covariance Matrix:** A single shared symmetric matrix:
  $$\text{Parameters}_{\text{cov}} = \frac{d(d + 1)}{2}$$

Summing all components:
$$\text{Total Parameters}_{\text{LDA}} = (K - 1) + K \cdot d + \frac{d(d + 1)}{2} = \mathcal{O}(K \cdot d + d^2)$$

### 3. Comparison with Discriminative Multi-Class Logistic Regression (Softmax)
Softmax regression estimates $K - 1$ independent linear weight vectors $\mathbf{w}_k \in \mathbb{R}^d$ and bias terms:
$$\text{Total Parameters}_{\text{Softmax}} = (K - 1) \cdot (d + 1) = \mathcal{O}(K \cdot d)$$

```
Parameter
Cardinality
    ^
    |                                                 QDA: O(K * d^2)
    |                                                  /
    |                                                 /
    |                                                /
    |                                               /  LDA: O(K*d + d^2)
    |                                             /
    |                                            /
    |                                           /
    |                                          /
    |                                         /    Softmax: O(K * d)
    |                                        /----------------------
    +-------------------------------------------------------------> Feature Dimension (d)
```
When $d$ is large (e.g., in computer vision where $d = 10,000$ pixels), QDA requires estimating millions of parameters, causing severe overfitting unless regularized. Softmax regression scales linearly with $d$, making it more computationally stable in high-dimensional settings.

---

# 6. Exhaustive Suite of Worked Numerical Problems

## Worked Problem 1: Generative Posterior vs. Discriminative Boundary in 1D Space

### Problem Statement
A laboratory uses a single biometric measurement $x \in \mathbb{R}$ to classify an organism as either a common bacterial strain ($Y = 0$) or a dangerous pathogen ($Y = 1$). The data follows Gaussian class-conditional distributions:
- Class 0 ($Y = 0$): $\mu_0 = 10$, $\sigma_0^2 = 4$, Prior $P(Y = 0) = 0.80$
- Class 1 ($Y = 1$): $\mu_1 = 14$, $\sigma_1^2 = 4$, Prior $P(Y = 1) = 0.20$

1. Find the exact mathematical expression for the generative posterior probability $P(Y = 1 \mid x)$.
2. Calculate the exact numeric location of the Bayes decision boundary $x^*$ under symmetric 0-1 loss.
3. Classify a new patient observation with measurement $x = 11.5$.
4. Determine the equivalent discriminative logistic parameterization: find $w$ and $w_0$ such that $P(Y = 1 \mid x) = \sigma(w \cdot x + w_0)$.

---

### Step-by-Step Solution

#### Step 1: Formulate Likelihood Functions
Both distributions share the variance $\sigma^2 = 4$ (standard deviation $\sigma = 2$).
The 1D Gaussian probability density function is:
$$p(x \mid Y = k) = \frac{1}{\sqrt{2\pi \sigma^2}} \exp\left( -\frac{(x - \mu_k)^2}{2\sigma^2} \right)$$

For Class 0:
$$p(x \mid Y = 0) = \frac{1}{\sqrt{8\pi}} \exp\left( -\frac{(x - 10)^2}{8} \right)$$

For Class 1:
$$p(x \mid Y = 1) = \frac{1}{\sqrt{8\pi}} \exp\left( -\frac{(x - 14)^2}{8} \right)$$

---

#### Step 2: Compute Decision Boundary $x^*$
Under 0-1 loss, the decision boundary occurs where the two class posteriors are equal:
$$P(Y = 1 \mid x) = P(Y = 0 \mid x) \iff p(x \mid Y = 1) P(Y = 1) = p(x \mid Y = 0) P(Y = 0)$$

Substitute the density functions and priors:
$$\frac{1}{\sqrt{8\pi}} \exp\left( -\frac{(x - 14)^2}{8} \right) \cdot 0.20 = \frac{1}{\sqrt{8\pi}} \exp\left( -\frac{(x - 10)^2}{8} \right) \cdot 0.80$$

Cancel the common factor $\frac{1}{\sqrt{8\pi}}$:
$$0.20 \cdot \exp\left( -\frac{(x - 14)^2}{8} \right) = 0.80 \cdot \exp\left( -\frac{(x - 10)^2}{8} \right)$$

Divide both sides by $0.20$:
$$\exp\left( -\frac{(x - 14)^2}{8} \right) = 4 \cdot \exp\left( -\frac{(x - 10)^2}{8} \right)$$

Take the natural logarithm of both sides:
$$-\frac{(x - 14)^2}{8} = \ln(4) - \frac{(x - 10)^2}{8}$$

Multiply through by $-8$:
$$(x - 14)^2 = -8 \ln(4) + (x - 10)^2$$

Given $\ln(4) \approx 1.38629$, we compute $-8 \ln(4) = -8 \times 1.38629 = -11.09035$:
$$x^2 - 28x + 196 = -11.09035 + x^2 - 20x + 100$$

Subtract $x^2$ from both sides:
$$-28x + 196 = -20x + 88.90965$$

Isolate $x$:
$$196 - 88.90965 = 28x - 20x$$
$$107.09035 = 8x$$
$$x^* = \frac{107.09035}{8} \approx \mathbf{13.386}$$

*Intuitive Verification:* The midpoint between the two class means is $\frac{10 + 14}{2} = 12.0$. Because the prior for Class 0 ($0.80$) is much larger than Class 1 ($0.20$), the decision boundary shifts toward Class 1 (from $12.0$ up to $13.386$). An observation must be closer to $\mu_1 = 14$ to overcome the lower prior probability.

---

#### Step 3: Classify Observation $x = 11.5$
Compare the observation directly to the decision boundary:
$$x = 11.5 < x^* = 13.386$$
Because $x$ lies below the threshold, the classifier predicts:
$$\hat{y} = \mathbf{0} \quad (\text{Common Strain})$$

To compute the exact posterior probability:
$$p(11.5 \mid Y = 0) = \frac{1}{\sqrt{8\pi}} \exp\left( -\frac{(11.5 - 10)^2}{8} \right) = \frac{1}{\sqrt{8\pi}} \exp\left( -\frac{2.25}{8} \right) = \frac{1}{\sqrt{8\pi}} e^{-0.28125} \approx \frac{0.7548}{\sqrt{8\pi}}$$

$$p(11.5 \mid Y = 1) = \frac{1}{\sqrt{8\pi}} \exp\left( -\frac{(11.5 - 14)^2}{8} \right) = \frac{1}{\sqrt{8\pi}} \exp\left( -\frac{6.25}{8} \right) = \frac{1}{\sqrt{8\pi}} e^{-0.78125} \approx \frac{0.4578}{\sqrt{8\pi}}$$

Now apply Bayes' theorem:
$$P(Y = 1 \mid 11.5) = \frac{p(11.5 \mid 1) P(1)}{p(11.5 \mid 1)P(1) + p(11.5 \mid 0)P(0)}$$
$$P(Y = 1 \mid 11.5) = \frac{0.4578 \times 0.20}{(0.4578 \times 0.20) + (0.7548 \times 0.80)} = \frac{0.09156}{0.09156 + 0.60384} = \frac{0.09156}{0.6954} \approx \mathbf{0.1317} \quad (13.17\%)$$
Since $P(Y = 1 \mid 11.5) = 13.17\% < 50\%$, we confirm $\hat{y} = 0$.

---

#### Step 4: Map to Equivalent Discriminative Logistic Form
From Derivation 1, the parameters for the logistic form $\sigma(wx + w_0)$ in 1D are:
$$w = \frac{\mu_1 - \mu_0}{\sigma^2} = \frac{14 - 10}{4} = \frac{4}{4} = \mathbf{1.0}$$

The intercept $w_0$ is:
$$w_0 = -\frac{\mu_1^2 - \mu_0^2}{2\sigma^2} + \ln\left(\frac{\pi_1}{\pi_0}\right)$$
$$w_0 = -\frac{14^2 - 10^2}{2(4)} + \ln\left(\frac{0.20}{0.80}\right) = -\frac{196 - 100}{8} + \ln(0.25) = -\frac{96}{8} - 1.38629 = -12 - 1.38629 = \mathbf{-13.3863}$$

Thus, the exact discriminative logistic model is:
$$P(Y = 1 \mid x) = \sigma(1.0 \cdot x - 13.3863) = \frac{1}{1 + e^{-(x - 13.3863)}}$$
Setting this argument to zero ($x - 13.3863 = 0$) recovers the exact decision threshold $x^* = 13.3863$.

---

## Worked Problem 2: Asymmetric Risk Minimization with Heavy Penalty Discrepancy

### Problem Statement
An autonomous manufacturing robotic cell uses high-resolution imaging to detect whether an engine block has a structural fracture.
- Normal Engine Block ($c_1$): $P(c_1) = 0.95$
- Fractured Engine Block ($c_2$): $P(c_2) = 0.05$

The cost matrix $\mathbf{\Lambda}$ (in thousands of dollars) is defined as:
```
                     True State
                 c_1 (Normal)    c_2 (Fractured)
Action \alpha_1
Predict Normal         0              500   (Catastrophic recall)
Action \alpha_2
Predict Fractured      5                0   (Scrap cost)
```
Assume the visual feature measurement $x \in \mathbb{R}$ produces the following class-conditional likelihood values for an incoming engine block:
$$p(x \mid c_1) = 0.040, \quad p(x \mid c_2) = 0.005$$

1. Calculate the conditional risk $R(\alpha_1 \mid x)$ and $R(\alpha_2 \mid x)$.
2. Determine the Bayes optimal action under this asymmetric risk profile.
3. Show how a naive classifier using 0-1 loss makes the opposite (incorrect) decision.

---

### Step-by-Step Solution

#### Step 1: Calculate Posterior Probabilities
First, compute the evidence denominator $p(x)$:
$$p(x) = p(x \mid c_1)P(c_1) + p(x \mid c_2)P(c_2)$$
$$p(x) = (0.040)(0.95) + (0.005)(0.05) = 0.0380 + 0.00025 = 0.03825$$

Now calculate the posterior probabilities:
$$P(c_1 \mid x) = \frac{0.0380}{0.03825} \approx \mathbf{0.99346} \quad (99.35\%)$$
$$P(c_2 \mid x) = \frac{0.00025}{0.03825} \approx \mathbf{0.00654} \quad (0.654\%)$$

---

#### Step 2: Compute Conditional Risks
From the problem definition, the costs are:
- $\lambda_{11} = 0$
- $\lambda_{21} = 500$ (False Negative: predicting normal when it is fractured)
- $\lambda_{12} = 5$ (False Alarm: predicting fractured when it is normal)
- $\lambda_{22} = 0$

**Risk of Action $\alpha_1$ (Predict Normal):**
$$R(\alpha_1 \mid x) = \lambda_{11} P(c_1 \mid x) + \lambda_{21} P(c_2 \mid x)$$
$$R(\alpha_1 \mid x) = 0 \times (0.99346) + 500 \times (0.00654) = 500 \times 0.00654 = \mathbf{\$3.27} \text{ thousand (\$3,270)}$$

**Risk of Action $\alpha_2$ (Predict Fractured):**
$$R(\alpha_2 \mid x) = \lambda_{12} P(c_1 \mid x) + \lambda_{22} P(c_2 \mid x)$$
$$R(\alpha_2 \mid x) = 5 \times (0.99346) + 0 \times (0.00654) = 5 \times 0.99346 = \mathbf{\$4.967} \text{ thousand (\$4,967)}$$

---

#### Step 3: Optimal Decision
Compare the two risks:
$$R(\alpha_1 \mid x) = \$3,270 < R(\alpha_2 \mid x) = \$4,967$$
Because the risk of predicting normal is lower, the Bayes optimal decision is:
$$\text{Choose } \mathbf{\alpha_1} \quad (\text{Pass as Normal})$$

---

#### Step 4: Sensitivity Analysis - Finding the Tipping Point
At what probability $P(c_2 \mid x)$ does it become optimal to scrap the engine block?
We equate the two risks:
$$500 \cdot P(c_2 \mid x) = 5 \cdot (1 - P(c_2 \mid x))$$
$$500 P(c_2 \mid x) + 5 P(c_2 \mid x) = 5$$
$$505 P(c_2 \mid x) = 5 \implies P(c_2 \mid x) = \frac{5}{505} \approx \mathbf{0.0099} \quad (\approx 0.99\%)$$

If the probability of a fracture exceeds just **$0.99\%$**, the optimal decision flips to scrapping the engine ($\alpha_2$).

A naive classifier using 0-1 loss requires $P(c_2 \mid x) > 50\%$ to flag a fracture. In this industrial setting, that naive threshold would allow dangerous, fractured engines into circulation, leading to catastrophic recalls.

---

## Worked Problem 3: Complete Parameter Count Derivation for Multi-Class Architectures

### Problem Statement
A medical diagnostics laboratory is designing a disease profiling system with the following specifications:
- Input feature vector size: $d = 64$ continuous biomarkers.
- Classification categories: $K = 8$ distinct pathological conditions.

Compute the exact number of scalar parameters that must be estimated for each of the following candidate architectures:
1. **QDA (Quadratic Discriminant Analysis):** Fully unconstrained, class-specific covariance matrices.
2. **LDA (Linear Discriminant Analysis):** Shared pooled covariance matrix across all classes.
3. **Diagonal-Covariance Gaussian Naive Bayes:** Class-conditional Gaussian distributions with assumed feature independence.
4. **Multi-Class Logistic Regression (Softmax):** Parametric discriminative linear network.

---

### Step-by-Step Solution

#### 1. Quadratic Discriminant Analysis (QDA)
- **Priors:** $K - 1 = 8 - 1 = \mathbf{7}$ independent priors.
- **Means:** $K \times d = 8 \times 64 = \mathbf{512}$ mean values.
- **Covariances:** $K$ symmetric matrices of size $64 \times 64$.
  $$\text{Entries per matrix} = \frac{d(d + 1)}{2} = \frac{64 \times 65}{2} = \frac{4160}{2} = 2,080$$
  For $K = 8$ classes:
  $$8 \times 2,080 = \mathbf{16,640}$$
- **Total Parameters (QDA):**
  $$\text{Total} = 7 + 512 + 16,640 = \mathbf{17,159} \text{ parameters}$$

---

#### 2. Linear Discriminant Analysis (LDA)
- **Priors:** $K - 1 = \mathbf{7}$.
- **Means:** $K \times d = 8 \times 64 = \mathbf{512}$.
- **Covariance:** Exactly one shared $64 \times 64$ symmetric matrix:
  $$\frac{64 \times 65}{2} = \mathbf{2,080}$$
- **Total Parameters (LDA):**
  $$\text{Total} = 7 + 512 + 2,080 = \mathbf{2,599} \text{ parameters}$$

---

#### 3. Diagonal Gaussian Naive Bayes
Because features are assumed conditionally independent, the off-diagonal covariance entries are zero. Only the diagonal variances need to be estimated:
- **Priors:** $K - 1 = \mathbf{7}$.
- **Means:** $K \times d = 8 \times 64 = \mathbf{512}$.
- **Variances:** $K \times d$ diagonal variance terms:
  $$8 \times 64 = \mathbf{512}$$
- **Total Parameters (Naive Bayes):**
  $$\text{Total} = 7 + 512 + 512 = \mathbf{1,031} \text{ parameters}$$

---

#### 4. Multi-Class Logistic Regression (Softmax)
Softmax models class probabilities using $K - 1$ independent linear weight vectors, plus bias terms:
- **Weights:** $(K - 1) \times d = (8 - 1) \times 64 = 7 \times 64 = \mathbf{448}$ weights.
- **Biases:** $K - 1 = \mathbf{7}$ bias terms.
- **Total Parameters (Softmax):**
  $$\text{Total} = 448 + 7 = \mathbf{455} \text{ parameters}$$
  *(Note: If parameterized with redundant weights for all $K$ classes before regularization, the model has $8 \times (64 + 1) = 520$ parameters).*

---

### Architectural Parameter Comparison Summary

```
+----------------------------------+-----------------------+---------------------+
| Algorithm                        | Exact Parameter Count | Asymptotic Scaling  |
+----------------------------------+-----------------------+---------------------+
| QDA (Generative)                 |        17,159         | O(K * d^2)          |
| LDA (Generative)                 |         2,599         | O(K*d + d^2)        |
| Naive Bayes (Generative)         |         1,031         | O(K * d)            |
| Softmax Regression (Discrimin.)  |           455         | O(K * d)            |
+----------------------------------+-----------------------+---------------------+
```
*Takeaway:* Softmax regression achieves linear scaling with fewer parameters than Naive Bayes, because it does not model variance terms for the inputs.

---

## Worked Problem 4: Non-Parametric Metric Boundary Computation ($k$-NN Distance Ties)

### Problem Statement
A 2D non-parametric classification dataset has six training instances:

```
Sample Index   x_1    x_2    Class Label (Y)
--------------------------------------------
s_1            1.0    2.0    Red   (0)
s_2            2.0    1.0    Red   (0)
s_3            2.0    3.0    Red   (0)
s_4            3.0    2.0    Blue  (1)
s_5            4.0    3.0    Blue  (1)
s_6            4.0    1.0    Blue  (1)
```

A query observation arrives at $\mathbf{x}_{\text{query}} = (2.0, 2.0)$.
1. Classify the query point using a standard $k$-NN classifier with $k = 3$ under Euclidean distance.
2. If a distance tie occurs, apply **Inverse Distance Weighting (IDW)** where each neighbor receives weight $w_i = \frac{1}{d(\mathbf{x}_i, \mathbf{x}_{\text{query}})^2}$.
3. Repeat the classification for $k = 5$.

---

### Step-by-Step Solution

#### Step 1: Compute Distances to All Training Points
The squared Euclidean distance is:
$$d^2(\mathbf{x}_i, \mathbf{x}_{\text{query}}) = (x_{i1} - 2.0)^2 + (x_{i2} - 2.0)^2$$

- For $s_1 (1.0, 2.0)$:
  $$d^2 = (1.0 - 2.0)^2 + (2.0 - 2.0)^2 = (-1)^2 + 0^2 = 1.0 \implies d = \mathbf{1.0}$$
- For $s_2 (2.0, 1.0)$:
  $$d^2 = (2.0 - 2.0)^2 + (1.0 - 2.0)^2 = 0^2 + (-1)^2 = 1.0 \implies d = \mathbf{1.0}$$
- For $s_3 (2.0, 3.0)$:
  $$d^2 = (2.0 - 2.0)^2 + (3.0 - 2.0)^2 = 0^2 + 1^2 = 1.0 \implies d = \mathbf{1.0}$$
- For $s_4 (3.0, 2.0)$:
  $$d^2 = (3.0 - 2.0)^2 + (2.0 - 2.0)^2 = 1^2 + 0^2 = 1.0 \implies d = \mathbf{1.0}$$
- For $s_5 (4.0, 3.0)$:
  $$d^2 = (4.0 - 2.0)^2 + (3.0 - 2.0)^2 = 2^2 + 1^2 = 4 + 1 = 5.0 \implies d = \sqrt{5} \approx \mathbf{2.236}$$
- For $s_6 (4.0, 1.0)$:
  $$d^2 = (4.0 - 2.0)^2 + (1.0 - 2.0)^2 = 2^2 + (-1)^2 = 4 + 1 = 5.0 \implies d = \sqrt{5} \approx \mathbf{2.236}$$

---

#### Step 2: Evaluate $k = 3$ with Distance Ties
We observe a four-way tie at distance $d = 1.0$:
$$\{s_1, s_2, s_3, s_4\} \quad \text{all have } d = 1.0$$

- Red class has 3 candidates: $\{s_1, s_2, s_3\}$
- Blue class has 1 candidate: $\{s_4\}$

If we select three neighbors at random from these four tied points, the outcome depends on the random draw. To resolve this deterministically, we evaluate class membership across all points at the tied boundary radius:
- Total tied neighbors at $d = 1.0$: 3 Red, 1 Blue.
- Probability assignment based on the full neighborhood:
  $$P(\text{Red} \mid \mathbf{x}) = \frac{3}{4} = 0.75, \quad P(\text{Blue} \mid \mathbf{x}) = \frac{1}{4} = 0.25$$

The classifier assigns the query to:
$$\hat{y} = \mathbf{Red} \quad (\text{Class } 0)$$

---

#### Step 3: Evaluate Using Inverse Distance Weighting (IDW)
Under IDW, each neighbor receives a vote weighted by $w_i = \frac{1}{d^2}$:
For the four closest neighbors ($s_1, s_2, s_3, s_4$), $d^2 = 1.0$, so:
$$w_1 = w_2 = w_3 = w_4 = \frac{1}{1.0} = 1.0$$

Sum of votes for Red:
$$V_{\text{Red}} = w_1 + w_2 + w_3 = 1.0 + 1.0 + 1.0 = \mathbf{3.0}$$

Sum of votes for Blue:
$$V_{\text{Blue}} = w_4 = \mathbf{1.0}$$

Normalized probabilities:
$$P(\text{Red}) = \frac{3.0}{3.0 + 1.0} = \mathbf{0.75}, \quad P(\text{Blue}) = \frac{1.0}{4.0} = \mathbf{0.25}$$
$$\hat{y} = \mathbf{Red}$$

---

#### Step 4: Evaluate $k = 5$
For $k = 5$, the neighborhood includes the first four points plus one of the points at $d = \sqrt{5}$:
- 4 nearest neighbors ($d = 1.0$): $s_1 (\text{Red}), s_2 (\text{Red}), s_3 (\text{Red}), s_4 (\text{Blue})$
- 5th neighbor ($d = \sqrt{5} \approx 2.236$): Either $s_5 (\text{Blue})$ or $s_6 (\text{Blue})$

In either case, the 5th neighbor is **Blue**.
The vote tally among the 5 nearest neighbors is:
$$\text{Red Votes} = 3 \quad (s_1, s_2, s_3)$$
$$\text{Blue Votes} = 2 \quad (s_4, \text{ and either } s_5 \text{ or } s_6)$$

Majority vote yields:
$$3 > 2 \implies \hat{y} = \mathbf{Red} \quad (P = 3/5 = 0.60)$$

---

## Worked Problem 5: Non-Parametric Density Estimation Classification (Parzen Windows)

### Problem Statement
A continuous 1D dataset contains four training points:
- Class 0 ($Y = 0$): $x_1 = 2.0, \quad x_2 = 4.0$
- Class 1 ($Y = 1$): $x_3 = 5.0, \quad x_4 = 7.0$

Assume uniform class priors: $P(Y = 0) = P(Y = 1) = 0.50$.
We implement a **Parzen Window (Kernel Density Estimation)** generative classifier using a standard Gaussian kernel:
$$K(u) = \frac{1}{\sqrt{2\pi}} \exp\left(-\frac{u^2}{2}\right)$$
with a fixed bandwidth parameter $h = 1.0$.
The class-conditional density estimate is given by:
$$p_n(x \mid Y = c) = \frac{1}{N_c \cdot h} \sum_{i=1}^{N_c} K\left(\frac{x - x_i^{(c)}}{h}\right)$$

1. Compute the estimated densities $p(x = 4.2 \mid Y = 0)$ and $p(x = 4.2 \mid Y = 1)$ at the test point $x = 4.2$.
2. Compute the posterior probability $P(Y = 1 \mid x = 4.2)$.
3. Assign the optimal class label under 0-1 loss.

---

### Step-by-Step Solution

#### Step 1: Calculate Density for Class 0 ($Y = 0$)
Class 0 has $N_0 = 2$ instances: $x_1 = 2.0$ and $x_2 = 4.0$. With bandwidth $h = 1.0$:
$$p(4.2 \mid Y = 0) = \frac{1}{2 \cdot 1.0} \left[ K\left(\frac{4.2 - 2.0}{1.0}\right) + K\left(\frac{4.2 - 4.0}{1.0}\right) \right]$$
$$p(4.2 \mid Y = 0) = \frac{1}{2} \left[ K(2.2) + K(0.2) \right]$$

Compute the Gaussian kernel evaluations:
$$K(2.2) = \frac{1}{\sqrt{2\pi}} e^{-(2.2)^2 / 2} = \frac{1}{\sqrt{2\pi}} e^{-4.84 / 2} = \frac{1}{\sqrt{2\pi}} e^{-2.42} \approx \frac{0.08892}{\sqrt{2\pi}}$$
$$K(0.2) = \frac{1}{\sqrt{2\pi}} e^{-(0.2)^2 / 2} = \frac{1}{\sqrt{2\pi}} e^{-0.04 / 2} = \frac{1}{\sqrt{2\pi}} e^{-0.02} \approx \frac{0.98020}{\sqrt{2\pi}}$$

Sum the evaluations:
$$p(4.2 \mid Y = 0) = \frac{1}{2\sqrt{2\pi}} [0.08892 + 0.98020] = \frac{1.06912}{2\sqrt{2\pi}} \approx \frac{0.53456}{\sqrt{2\pi}}$$
Using $\frac{1}{\sqrt{2\pi}} \approx 0.39894$:
$$p(4.2 \mid Y = 0) \approx 0.53456 \times 0.39894 \approx \mathbf{0.21326}$$

---

#### Step 2: Calculate Density for Class 1 ($Y = 1$)
Class 1 has $N_1 = 2$ instances: $x_3 = 5.0$ and $x_4 = 7.0$.
$$p(4.2 \mid Y = 1) = \frac{1}{2 \cdot 1.0} \left[ K\left(\frac{4.2 - 5.0}{1.0}\right) + K\left(\frac{4.2 - 7.0}{1.0}\right) \right]$$
$$p(4.2 \mid Y = 1) = \frac{1}{2} \left[ K(-0.8) + K(-2.8) \right]$$

Compute the Gaussian kernel evaluations (using symmetry $K(-u) = K(u)$):
$$K(-0.8) = \frac{1}{\sqrt{2\pi}} e^{-(-0.8)^2 / 2} = \frac{1}{\sqrt{2\pi}} e^{-0.64 / 2} = \frac{1}{\sqrt{2\pi}} e^{-0.32} \approx \frac{0.72615}{\sqrt{2\pi}}$$
$$K(-2.8) = \frac{1}{\sqrt{2\pi}} e^{-(-2.8)^2 / 2} = \frac{1}{\sqrt{2\pi}} e^{-7.84 / 2} = \frac{1}{\sqrt{2\pi}} e^{-3.92} \approx \frac{0.01984}{\sqrt{2\pi}}$$

Sum the evaluations:
$$p(4.2 \mid Y = 1) = \frac{1}{2\sqrt{2\pi}} [0.72615 + 0.01984] = \frac{0.74599}{2\sqrt{2\pi}} \approx \frac{0.37300}{\sqrt{2\pi}}$$
$$p(4.2 \mid Y = 1) \approx 0.37300 \times 0.39894 \approx \mathbf{0.14880}$$

---

#### Step 3: Compute Posterior Probability
Using Bayes' theorem with balanced priors ($P(0) = P(1) = 0.5$):
$$P(Y = 1 \mid 4.2) = \frac{p(4.2 \mid 1) P(1)}{p(4.2 \mid 0)P(0) + p(4.2 \mid 1)P(1)} = \frac{0.14880 \times 0.5}{(0.21326 \times 0.5) + (0.14880 \times 0.5)}$$
$$P(Y = 1 \mid 4.2) = \frac{0.14880}{0.21326 + 0.14880} = \frac{0.14880}{0.36206} \approx \mathbf{0.411} \quad (41.1\%)$$

$$P(Y = 0 \mid 4.2) = 1 - 0.411 = \mathbf{0.589} \quad (58.9\%)$$

---

#### Step 4: Decision Assignment
Under 0-1 loss, we select the class with the higher posterior probability:
$$P(Y = 0 \mid 4.2) = 58.9\% > P(Y = 1 \mid 4.2) = 41.1\%$$
$$\hat{y} = \mathbf{0} \quad (\text{Class } 0)$$

---

## Worked Problem 6: Empirical Convergence Crossover Point (The Ng-Jordan Sample Bound)

### Problem Statement
A data scientist evaluates two classification algorithms on a dataset with dimension $d = 128$:
- **Model A (Generative - Naive Bayes):** Its generalization error as a function of training size $N$ follows:
  $$\epsilon_{\text{gen}}(N) = \epsilon_{\text{gen},\infty} + \frac{\alpha \ln(d)}{N}$$
- **Model B (Discriminative - Logistic Regression):** Its generalization error follows:
  $$\epsilon_{\text{dis}}(N) = \epsilon_{\text{dis},\infty} + \frac{\beta d}{N}$$

The empirical parameters for this problem domain are:
- Asymptotic Error of Generative Model: $\epsilon_{\text{gen},\infty} = 0.16$ ($16\%$ error)
- Asymptotic Error of Discriminative Model: $\epsilon_{\text{dis},\infty} = 0.08$ ($8\%$ error)
- Learning rate coefficients: $\alpha = 1.8$, $\beta = 0.35$

1. Compute the critical sample size $N_{\text{crossover}}$ where both models achieve identical test error.
2. Determine which model is preferred when the available training budget is limited to $N = 300$ samples.
3. Determine which model is preferred when the training budget expands to $N = 2,000$ samples.

---

### Step-by-Step Solution

#### Step 1: Set Up the Crossover Equality
We equate the two generalization error functions:
$$\epsilon_{\text{gen}}(N^*) = \epsilon_{\text{dis}}(N^*)$$
$$\epsilon_{\text{gen},\infty} + \frac{\alpha \ln(d)}{N^*} = \epsilon_{\text{dis},\infty} + \frac{\beta d}{N^*}$$

Isolate the terms involving $N^*$:
$$\epsilon_{\text{gen},\infty} - \epsilon_{\text{dis},\infty} = \frac{\beta d - \alpha \ln(d)}{N^*}$$

Solve for $N^*$:
$$N^* = \frac{\beta d - \alpha \ln(d)}{\epsilon_{\text{gen},\infty} - \epsilon_{\text{dis},\infty}}$$

---

#### Step 2: Compute the Numerical Quantities
Given:
- $d = 128$
- $\ln(128) = \ln(2^7) = 7 \cdot \ln(2) \approx 7 \times 0.693147 = 4.8520$
- $\alpha = 1.8 \implies \alpha \ln(d) = 1.8 \times 4.8520 = \mathbf{8.7336}$
- $\beta = 0.35 \implies \beta d = 0.35 \times 128 = \mathbf{44.80}$
- Denominator difference: $\epsilon_{\text{gen},\infty} - \epsilon_{\text{dis},\infty} = 0.16 - 0.08 = \mathbf{0.08}$

---

#### Step 3: Compute $N_{\text{crossover}}$
Substitute the computed values into the formula for $N^*$:
$$N^* = \frac{44.80 - 8.7336}{0.08} = \frac{36.0664}{0.08} = \mathbf{450.83}$$
Rounding up to the nearest integer yields:
$$N_{\text{crossover}} = \mathbf{451} \text{ samples}$$

---

#### Step 4: Evaluate Regimes

**Scenario 1: Training sample size $N = 300$ ($N < N_{\text{crossover}}$)**
- Generative Model Error:
  $$\epsilon_{\text{gen}}(300) = 0.16 + \frac{8.7336}{300} = 0.16 + 0.02911 = \mathbf{0.1891} \quad (18.91\%)$$
- Discriminative Model Error:
  $$\epsilon_{\text{dis}}(300) = 0.08 + \frac{44.80}{300} = 0.08 + 0.14933 = \mathbf{0.2293} \quad (22.93\%)$$

*Conclusion for $N = 300$:* **The Generative Model (Naive Bayes) is superior**, achieving a lower error rate ($18.91\%$ vs. $22.93\%$). The discriminative model has not yet seen enough data to accurately estimate its $d = 128$ weights.

---

**Scenario 2: Training sample size $N = 2,000$ ($N > N_{\text{crossover}}$)**
- Generative Model Error:
  $$\epsilon_{\text{gen}}(2000) = 0.16 + \frac{8.7336}{2000} = 0.16 + 0.00437 = \mathbf{0.1644} \quad (16.44\%)$$
- Discriminative Model Error:
  $$\epsilon_{\text{dis}}(2000) = 0.08 + \frac{44.80}{2000} = 0.08 + 0.02240 = \mathbf{0.1024} \quad (10.24\%)$$

*Conclusion for $N = 2,000$:* **The Discriminative Model (Logistic Regression) is superior**, achieving a substantially lower error rate ($10.24\%$ vs. $16.44\%$). With ample data, the discriminative model approaches its lower asymptotic error floor, while the generative model remains bottlenecked by its naive conditional independence assumption.

---

# 7. KTU University Exam Style Review Exercises

## Short-Answer Analytical Problems (Part A)

### Question 1: Mathematical Justification for Vapnik's Maxim
> **Question:** State Vapnik's Maxim regarding solving intermediate problems. Explain how this principle distinguishes the core design philosophies of generative versus discriminative classifiers. *(3 Marks)*

**Model Answer:** Vapnik's Maxim states: *"When solving a problem of interest, do not solve a more general problem as an intermediate step. Solve the target problem directly."* - **Generative classifiers** violate this principle: to solve the target problem of classification ($P(Y \mid X)$), they solve the more complex intermediate task of estimating the full class-conditional density $P(X \mid Y)$ and evidence $P(X)$ over the entire feature space.
- **Discriminative classifiers** adhere to this principle: they estimate the decision boundary or posterior $P(Y \mid X)$ directly, focusing parameter capacity only on separating the classes.

---

### Question 2: Lazy vs. Eager Learning Complexity
> **Question:** Differentiate between "Eager" and "Lazy" learners in terms of training and inference computational complexity. Map parametric and non-parametric classifiers to these paradigms with examples. *(3 Marks)*

**Model Answer:** - **Eager Learners (Parametric):** Process training data immediately to optimize a fixed set of parameters $\mathbf{\Theta}$, then discard the raw data. 
  - *Training Complexity:* High (requires iterative optimization, $\mathcal{O}(N d)$).
  - *Inference Complexity:* Low ($\mathcal{O}(d)$ dot product evaluation).
  - *Example:* Logistic Regression, Linear Discriminant Analysis.
- **Lazy Learners (Non-Parametric):** Defer computation until an inference query arrives; they store the training data without building an explicit global model.
  - *Training Complexity:* Minimal to zero ($\mathcal{O}(1)$ or $\mathcal{O}(N d)$ indexing).
  - *Inference Complexity:* High (must scan stored samples, $\mathcal{O}(N d)$).
  - *Example:* $k$-Nearest Neighbors ($k$-NN).

---

### Question 3: Handling Missing Features in Classification
> **Question:** Why are generative classifiers fundamentally better equipped to handle missing feature values during inference compared to discriminative classifiers? Provide the governing integral equation. *(3 Marks)*

**Model Answer:** Generative models capture the joint probability distribution $P(X, Y) = P(X \mid Y)P(Y)$. If a feature component $x_j$ is unobserved, the model can integrate (marginalize) it out over its probability density:
$$P(X_{\text{observed}} \mid Y = c_k) = \int_{-\infty}^\infty P(X_{\text{observed}}, X_j = \xi \mid Y = c_k) \, d\xi$$
This allows exact computation of the posterior probability using only the observed features.  
In contrast, discriminative models compute a direct functional mapping (e.g., $\mathbf{w}^T \mathbf{x} + b$). If any feature $x_j$ is missing, the dot product cannot be evaluated without heuristic data imputation.

---

## Comprehensive Essay & Derivation Questions (Part B)

### Question 4: Equivalence of LDA to Logistic Regression
> **Question:** > (a) Prove that a binary generative classification model with multivariate Gaussian class-conditional distributions and a shared covariance matrix induces a posterior distribution that has the logistic sigmoid form:  
> $$P(Y = 1 \mid \mathbf{x}) = \frac{1}{1 + \exp(-(\mathbf{w}^T \mathbf{x} + w_0))}$$  
> Derive explicit expressions for the weight vector $\mathbf{w}$ and bias $w_0$ in terms of the Gaussian parameters $(\mathbf{\mu}_0, \mathbf{\mu}_1, \mathbf{\Sigma}, \pi_0, \pi_1)$. *(9 Marks)* > (b) If the equal covariance assumption is violated ($\mathbf{\Sigma}_0 \neq \mathbf{\Sigma}_1$), show mathematically why the resulting decision boundary becomes quadratic (QDA) rather than linear. *(5 Marks)*

**Model Answer Outline:** - **Part (a):** Follow the complete algebraic proof provided in **Section 5 (Derivation 1)**. Show the log-odds formulation, expand the quadratic matrix terms, demonstrate the cancellation of the quadratic $\mathbf{x}^T \mathbf{\Sigma}^{-1} \mathbf{x}$ terms due to the shared covariance matrix $\mathbf{\Sigma}$, and collect the resulting linear vector $\mathbf{w} = \mathbf{\Sigma}^{-1}(\mathbf{\mu}_1 - \mathbf{\mu}_0)$ and scalar intercept $w_0$.
- **Part (b):** When $\mathbf{\Sigma}_0 \neq \mathbf{\Sigma}_1$, the quadratic term in the log-odds ratio does not cancel:
  $$\log \frac{p(\mathbf{x} \mid Y = 1)}{p(\mathbf{x} \mid Y = 0)} = -\frac{1}{2}\mathbf{x}^T \left( \mathbf{\Sigma}_1^{-1} - \mathbf{\Sigma}_0^{-1} \right)\mathbf{x} + \left( \mathbf{\mu}_1^T \mathbf{\Sigma}_1^{-1} - \mathbf{\mu}_0^T \mathbf{\Sigma}_0^{-1} \right)\mathbf{x} + C$$
  Because $\mathbf{\Sigma}_1^{-1} - \mathbf{\Sigma}_0^{-1} \neq \mathbf{0}$, the term $\mathbf{x}^T \mathbf{A} \mathbf{x}$ remains. Setting the posterior log-odds to zero yields a **quadratic surface** (hyper-ellipsoid, paraboloid, or hyperboloid) rather than a linear hyperplane, defining the Quadratic Discriminant Analysis (QDA) model.

---

### Question 5: Comparative Analysis of Classification Paradigms
> **Question:** > (a) Compare Generative and Discriminative paradigms across the following dimensions: (i) Empirical optimization objective, (ii) Sample complexity and convergence rate to asymptotic error, (iii) Outlier and out-of-distribution anomaly detection. *(6 Marks)* > (b) Explain the Curse of Dimensionality and its impact on non-parametric metric classifiers. Prove that as dimension $d \to \infty$, the distance to the nearest neighbor approaches the distance to the furthest neighbor. *(8 Marks)*

**Model Answer Outline:** - **Part (a):** Synthesize the points from **Section 2.3, 2.4, and 2.5**. Contrast joint likelihood maximization vs. conditional likelihood maximization. Discuss Ng & Jordan's sample complexity bounds ($\mathcal{O}(\log d)$ for generative vs. $\mathcal{O}(d)$ for discriminative). Detail how marginal evidence $p(\mathbf{x}) < \tau$ detects anomalies in generative models, whereas discriminative models yield overconfident predictions on outliers far from the training data.
- **Part (b):** Present the volume ratio proof: $e_d(r) = r^{1/d}$, showing that local neighborhoods expand to cover the entire space as $d$ grows. Provide the analytical proof for distance concentration:
  Let $D_d(\mathbf{x}) = \|\mathbf{x}\|_2$ be the Euclidean distance to a random point in $d$ dimensions with i.i.d. coordinates. Show that:
  $$\text{Var}[D_d^2] = \mathcal{O}(d), \quad \mathbb{E}[D_d^2] = \mathcal{O}(d) \implies \frac{\sqrt{\text{Var}[D_d^2]}}{\mathbb{E}[D_d^2]} = \mathcal{O}\left(\frac{\sqrt{d}}{d}\right) = \mathcal{O}\left(\frac{1}{\sqrt{d}}\right) \to 0$$
  As $d \to \infty$, the relative variance of distances drops to zero. Consequently, $(D_{\max} - D_{\min}) / D_{\min} \to 0$, meaning all points become approximately equidistant from the query, which invalidates proximity-based classifications like $k$-NN.
