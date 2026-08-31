import os

CONTENT_DIR = os.path.join("content", "PCCST503")
os.makedirs(CONTENT_DIR, exist_ok=True)

# Remove old M1 and M2 files to avoid naming collisions
old_files = [
    "m1_01_ml_vs_traditional.md", "m1_02_ml_paradigms.md", "m1_03_parameter_estimation_mle.md",
    "m1_04_parameter_estimation_map.md", "m1_05_supervised_learning_formulation.md",
    "m1_06_loss_functions_optimization.md", "m1_07_linear_regression_one_variable.md",
    "m1_08_linear_regression_multiple_variables.md", "m1_99_practice.md",
    "m2_01_logistic_regression.md", "m2_02_naive_bayes.md", "m2_03_knn.md",
    "m2_04_decision_trees.md", "m2_99_practice.md"
]
for f in old_files:
    p = os.path.join(CONTENT_DIR, f)
    if os.path.exists(p): os.remove(p)

# --- Module 1 Micro-Topics ---

m1_files = {}

m1_files["m1_01_ml_definition_and_intuition.md"] = r"""# What is Machine Learning? Definitions & Core Intuition

**Understanding Arthur Samuel and Tom Mitchell's formal definitions of artificial intelligence.**

<a id="the-intuition"></a>
## 1. The Intuition: Teaching vs Programming

Imagine teaching a child to identify a dog. You do not explain canine anatomy with mathematical coordinate equations. You simply point at 50 dogs in the park and say *"Dog!"*. Over time, the child's brain automatically extracts the latent features (fur, 4 legs, barking).

::: callout-intuition Formal Academic Definitions
- **Arthur Samuel (1959):** *"Machine Learning is the field of study that gives computers the ability to learn without being explicitly programmed."*
- **Tom M. Mitchell (1997 - The Engineering Definition):** *"A computer program is said to learn from experience $E$ with respect to some class of tasks $T$ and performance measure $P$, if its performance at tasks in $T$, as measured by $P$, improves with experience $E$."*
:::

---

<a id="the-math"></a>
## 2. Mitchell's $(E, T, P)$ Framework

To mathematically define any Machine Learning problem, you must clearly specify the **Experience ($E$)**, the **Task ($T$)**, and the **Performance Metric ($P$)**.

| Application | Task ($T$) | Experience ($E$) | Performance Metric ($P$) |
| :--- | :--- | :--- | :--- |
| **Spam Filtering** | Classifying emails as Spam or Ham | Database of 100,000 historical emails with human labels | Classification Accuracy / $F_1\text{-Score}$ |
| **Self-Driving Car** | Steering and braking on highways | Video feed, radar telemetry, and human driver actions | Mean distance traveled without human intervention |
| **Medical Diagnosis** | Predicting tumor malignancy | 10,000 patient biopsy scans with pathologist records | Sensitivity / Recall of positive cancer cases |
| **Chess Playing Engine** | Selecting the optimal next move | Playing 1,000,000 self-play simulated games | Elo rating / Win percentage against Grandmasters |

::: callout-formula The Mitchell Triad
Whenever you encounter an exam or interview question asking to *"Formulate problem X as a Machine Learning problem"*, always break it into $T$, $E$, and $P$!
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Mitchell Framework
In an autonomous delivery drone system that learns to navigate city winds, what represents the **Experience ($E$)**?
(A) The percentage of successful parcel deliveries
(B) Calculating the shortest route using Dijkstra's algorithm
(*C) Logged flight telemetry data and wind resistance readings from past flights
(D) The drone's physical battery capacity
::: explanation
Experience $E$ is the historical empirical data gathered over time that the learning algorithm processes to improve future performance.
:::
"""

m1_files["m1_02_ml_vs_traditional_programming.md"] = r"""# Machine Learning vs Traditional Programming

**Why hardcoded IF-ELSE rules fail in complex domains and how inductive learning replaces them.**

<a id="the-intuition"></a>
## 1. The Intuition: The Cake Recipe Paradigm

::: callout-intuition The Paradigm Shift
- **Traditional Software:** $\text{Data} + \text{Rules (Code)} \implies \text{Output}$
  - A human software engineer writes every single logical condition by hand. If input $A$ happens, do $B$.
- **Machine Learning:** $\text{Data} + \text{Output} \implies \text{Rules (The Model)}$
  - You provide raw observations and historical outcomes. The learning algorithm discovers the underlying statistical mapping $f: X \to Y$.
:::

---

<a id="the-math"></a>
## 2. In-Depth Comparison Table

| Dimension | Traditional Programming (Deductive) | Machine Learning (Inductive) |
| :--- | :--- | :--- |
| **Primary Input** | Raw Data + Explicit Algorithm | Input Features ($X$) + Ground Truth Labels ($Y$) |
| **Generated Artifact** | Program Execution Output | Model Weights / Hypothesis $h_\theta(x)$ |
| **Logic Formulation** | Handcrafted by human domain experts | Inferred statistically via numerical optimization |
| **Edge Case Handling** | Requires manual bug fixes and patch rules | Improves automatically when retrained on new edge cases |
| **Ideal Problem Domain** | Deterministic calculations (Taxes, Compilers, Banking) | Fuzzy, high-dimensional patterns (Vision, Audio, NLP) |

::: callout-pitfall When NOT to use Machine Learning
Never use Machine Learning when exact, deterministic business rules already exist! For example, calculating GST/VAT (e.g. $\text{Tax} = \text{Total} \times 0.18$) should **always** be traditional code.
:::

---

<a id="simulation"></a>
## 3. Visualizing the Paradigm Shift

::: manim assets/videos/m1_paradigms.mp4 Paradigm Shift Architecture
Observe how 'Rules' and 'Output' swap places in the engineering pipeline.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Architectural Decision
Which of the following problems should NEVER be implemented using Machine Learning?
(A) Transcribing spoken Malayalam voice notes into text
(B) Recommending relevant research papers to college students
(*C) Calculating exact bank account interest using government-mandated rate tiers
(D) Detecting credit card fraud from spending anomalies
::: explanation
Banking interest formulas are exact legal equations. Using ML introduces statistical uncertainty, variance, and latency to a problem that requires 1 line of exact deterministic code.
:::
"""

m1_files["m1_03_learning_paradigms_supervised_unsupervised.md"] = r"""# Learning Paradigms: Supervised vs Unsupervised

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
"""

m1_files["m1_04_learning_paradigms_semi_and_rl.md"] = r"""# Learning Paradigms: Semi-Supervised & Reinforcement Learning

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
"""

m1_files["m1_05_mle_intuition_and_bernoulli.md"] = r"""# Maximum Likelihood Estimation (MLE): Bernoulli Derivation

**How a computer finds the single model parameter that makes observed data the most statistically probable.**

<a id="the-intuition"></a>
## 1. The Intuition: The Biased Coin Detective

Suppose you flip a coin $n = 10$ times, observing $k = 7$ Heads and $3$ Tails. What is the most mathematically probable value for the true probability of heads $p$?

::: callout-intuition The MLE Principle
MLE asks: *"Among all possible values of $p \in [0, 1]$, which specific $p$ maximizes the mathematical likelihood of getting our exact observed dataset?"*
:::

---

<a id="the-math"></a>
## 2. Step-by-Step Calculus Derivation

### Step 1: Likelihood Function $L(p)$
Assuming independent and identically distributed (i.i.d.) tosses:
$$ L(p) = \prod_{i=1}^n P(x_i \mid p) = p^k (1-p)^{n-k} $$

### Step 2: The Log-Likelihood Trick $\ell(p)$
$$ \ell(p) = \ln L(p) = k \ln(p) + (n-k) \ln(1-p) $$

### Step 3: First Derivative with respect to $p$
$$ \frac{d}{dp}\ell(p) = \frac{k}{p} - \frac{n-k}{1-p} $$

### Step 4: First-Order Condition $\frac{d\ell}{dp} = 0$
$$ \frac{k}{p} = \frac{n-k}{1-p} \implies k(1-p) = p(n-k) \implies k - kp = np - kp \implies \hat{p}_{\text{MLE}} = \frac{k}{n} $$

::: callout-formula Summary
For any Bernoulli trial, the Maximum Likelihood Estimator is simply the sample proportion $\frac{k}{n}$ (e.g. $\frac{7}{10} = 0.70$).
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Log Transformation
Why do machine learning algorithms optimize $\ln L(\theta)$ instead of $L(\theta)$?
(A) The logarithm alters the location of the optimal parameter
(*B) It converts numerically unstable products into stable sums while preserving the exact maximum
(C) It eliminates the need to compute derivatives
(D) It turns non-convex functions into concave functions
::: explanation
Because $\ln(x)$ is strictly monotonically increasing, $\arg\max L(\theta) = \arg\max \ln L(\theta)$. It prevents underflow errors from multiplying tiny probabilities.
:::
"""

m1_files["m1_06_mle_gaussian_distribution.md"] = r"""# MLE for Continuous Variables: 1D Gaussian Distribution

**Deriving why the sample mean and variance are the mathematically optimal parameters of a normal distribution.**

<a id="the-intuition"></a>
## 1. The Intuition: Fitting the Bell Curve

Suppose you measure the heights of 1,000 students. You assume heights follow a normal distribution $\mathcal{N}(\mu, \sigma^2)$. How do you prove mathematically that the best bell curve center is simply the arithmetic average?

---

<a id="the-math"></a>
## 2. Mathematical Proof

For $m$ independent samples $x_1, \dots, x_m$:

$$ P(x_i \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x_i - \mu)^2}{2\sigma^2} \right) $$

### Step 1: Log-Likelihood Formulation
$$ \ell(\mu, \sigma^2) = -\frac{m}{2}\ln(2\pi) - \frac{m}{2}\ln(\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^m (x_i - \mu)^2 $$

### Step 2: Deriving Optimal Mean $\hat{\mu}_{\text{MLE}}$
Take partial derivative with respect to $\mu$ and set to 0:
$$ \frac{\partial \ell}{\partial \mu} = \frac{1}{\sigma^2}\sum_{i=1}^m (x_i - \mu) = 0 \implies \sum_{i=1}^m x_i - m\mu = 0 \implies \hat{\mu}_{\text{MLE}} = \frac{1}{m}\sum_{i=1}^m x_i $$

### Step 3: Deriving Optimal Variance $\hat{\sigma}^2_{\text{MLE}}$
Take partial derivative with respect to $\sigma^2$ and set to 0:
$$ \frac{\partial \ell}{\partial \sigma^2} = -\frac{m}{2\sigma^2} + \frac{1}{2(\sigma^2)^2}\sum_{i=1}^m (x_i - \mu)^2 = 0 \implies \hat{\sigma}^2_{\text{MLE}} = \frac{1}{m}\sum_{i=1}^m (x_i - \mu)^2 $$

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Analytical Result
What is the Maximum Likelihood Estimator for the mean $\mu$ of a 1D Gaussian distribution?
(*A) The sample mean $\frac{1}{m}\sum x_i$
(B) The sample median
(C) The maximum value in the dataset
(D) $\frac{1}{m-1}\sum (x_i - \bar{x})^2$
::: explanation
Setting the derivative of the Gaussian log-likelihood with respect to $\mu$ to zero directly yields the arithmetic average $\frac{1}{m}\sum x_i$.
:::
"""

m1_files["m1_07_map_bayes_theorem_and_priors.md"] = r"""# Maximum A Posteriori (MAP): Bayesian Parameter Estimation

**Overcoming the small-data overfitting flaw of MLE by incorporating prior knowledge.**

<a id="the-intuition"></a>
## 1. The Intuition: Why MLE Fails on 3 Coin Flips

If you flip a normal coin 3 times and get 3 Heads, pure MLE asserts $\hat{p} = 1.00$. This is absurd because you have a lifetime of prior experience knowing coins are fair.

::: callout-intuition Bayes' Theorem Framework
$$ P(\theta \mid D) = \frac{P(D \mid \theta) P(\theta)}{P(D)} $$
- **Posterior:** $P(\theta \mid D)$ (Our belief about $\theta$ after seeing data $D$).
- **Likelihood:** $P(D \mid \theta)$ (The MLE objective).
- **Prior:** $P(\theta)$ (Our background knowledge before seeing data).
:::

---

<a id="the-math"></a>
## 2. The MAP Objective

$$ \hat{\theta}_{\text{MAP}} = \arg\max_\theta P(\theta \mid D) = \arg\max_\theta \left[ \ln P(D \mid \theta) + \ln P(\theta) \right] $$

::: callout-formula Asymptotic Convergence
As dataset size $N \to \infty$, the likelihood $\ln P(D|\theta)$ grows linearly with $N$ and completely overwhelms the fixed prior $\ln P(\theta)$. Thus:
$$ \lim_{N \to \infty} \hat{\theta}_{\text{MAP}} = \hat{\theta}_{\text{MLE}} $$
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Large Data Limit
What happens to the MAP parameter estimate as the number of observed training samples approaches infinity ($N \to \infty$)?
(A) The prior completely overrides the data
(*B) The MAP estimate converges exactly to the MLE estimate
(C) The model severely overfits
(D) The parameter estimate goes to zero
::: explanation
With infinite data, empirical observations overwhelm any prior belief, making Bayesian MAP converge to Frequentist MLE.
:::
"""

m1_files["m1_08_map_beta_prior_derivation.md"] = r"""# MAP with Beta Priors: The Math & Cold-Start Problem

**Step-by-step derivation of conjugate Beta-Binomial MAP estimation.**

<a id="the-intuition"></a>
## 1. The Intuition: Virtual Data (Pseudo-Counts)

A **Beta Distribution** $\text{Beta}(\alpha, \beta)$ serves as the conjugate prior for Bernoulli trials. You can think of $\alpha - 1$ as "virtual prior heads" and $\beta - 1$ as "virtual prior tails".

---

<a id="the-math"></a>
## 2. Mathematical Derivation

$$ P(p) \propto p^{\alpha - 1} (1-p)^{\beta - 1}, \quad L(p) \propto p^k (1-p)^{n-k} $$

### Step 1: Posterior Formulation
$$ P(p \mid D) \propto p^{k + \alpha - 1} (1-p)^{n - k + \beta - 1} $$

### Step 2: Mode of the Beta Posterior
Taking the log, differentiating with respect to $p$, and setting to 0 yields:

$$ \hat{p}_{\text{MAP}} = \frac{k + \alpha - 1}{n + \alpha + \beta - 2} $$

::: callout-exam Concrete Example
If you observe $k=3$ heads in $n=3$ tosses with a prior $\text{Beta}(5, 5)$:
$$ \hat{p}_{\text{MAP}} = \frac{3 + 5 - 1}{3 + 5 + 5 - 2} = \frac{7}{11} \approx 0.636 $$
Instead of an extreme $1.00$, MAP regularizes the estimate to a sensible $0.636$!
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Prior Parameters
If $\alpha = 1$ and $\beta = 1$ in a Beta prior (representing a flat uniform prior $U(0, 1)$), what does $\hat{p}_{\text{MAP}}$ equal?
(A) 0.50
(*B) $\frac{k}{n}$ (Identical to MLE)
(C) 0.00
(D) 1.00
::: explanation
Substituting $\alpha=1, \beta=1$ yields $\hat{p}_{\text{MAP}} = \frac{k+0}{n+0} = \frac{k}{n}$, proving that MLE is equivalent to MAP with a uniform, uninformative prior.
:::
"""

m1_files["m1_09_supervised_learning_formalism.md"] = r"""# Supervised Learning Formalism & Dataset Splitting

**The rigorous mathematical notation of feature spaces, hypothesis functions, and generalization splits.**

<a id="the-math"></a>
## 1. Mathematical Notation

Let training dataset $\mathcal{D} = \{(x^{(1)}, y^{(1)}), \dots, (x^{(m)}, y^{(m)})\}$:
- $m$: Number of training examples.
- $x^{(i)} \in \mathbb{R}^d$: $d$-dimensional feature vector.
- $y^{(i)}$: Ground truth label.
- $h_\theta(x)$: Candidate hypothesis function parameterized by $\theta$.

---

<a id="worked-example"></a>
## 2. The 3-Way Dataset Split

::: step [Train Set (70%)] Optimization
Used by the optimizer (e.g. Gradient Descent) to update model parameters $\theta$.
:::

::: step [Validation Set (15%)] Hyperparameter Tuning
Used to select model complexity (e.g. polynomial degree, regularization strength $\lambda$).
:::

::: step [Test Set (15%)] Unbiased Evaluation
Locked until the very end to evaluate true generalization on unseen data.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Data Leakage Prevention
Why must model parameters never be trained on the Test set?
(A) It slows down training time
(*B) It causes optimistic evaluation bias, destroying the ability to measure real-world generalization
(C) It forces gradients to zero
(D) It makes the loss function non-convex
::: explanation
Testing on training data measures memorization rather than generalization. An unbiased test set evaluates performance on unseen distributions.
:::
"""

m1_files["m1_10_loss_and_cost_functions.md"] = r"""# Loss Functions & Error Metrics: MSE, MAE, and Cross-Entropy

**How algorithms quantify mistakes and why different loss functions suit different problem domains.**

<a id="the-math"></a>
## 1. Core Loss Functions

### 1. Mean Squared Error (MSE) — L2 Loss
$$ J(\theta) = \frac{1}{2m}\sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)} \right)^2 $$
- **Pros:** Smooth, differentiable everywhere, convex for linear models.
- **Cons:** Heavily penalized by outliers due to squaring.

### 2. Mean Absolute Error (MAE) — L1 Loss
$$ J(\theta) = \frac{1}{m}\sum_{i=1}^m |h_\theta(x^{(i)}) - y^{(i)}| $$
- **Pros:** Robust to corrupted outlier data.
- **Cons:** Gradient is non-differentiable at residual $= 0$.

### 3. Binary Cross-Entropy (Log Loss)
$$ J(\theta) = -\frac{1}{m}\sum_{i=1}^m \left[ y^{(i)}\ln(\hat{y}^{(i)}) + (1-y^{(i)})\ln(1-\hat{y}^{(i)}) \right] $$

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Outlier Robustness
Which regression loss function is LEAST sensitive to corrupted outlier measurements?
(A) Mean Squared Error (MSE)
(*B) Mean Absolute Error (MAE)
(C) Root Mean Squared Error (RMSE)
(D) Exponential Loss
::: explanation
MAE penalizes errors linearly ($|e|$), whereas MSE squares errors ($e^2$). An error of 100 contributes 100 to MAE but 10,000 to MSE.
:::
"""

m1_files["m1_11_gradient_descent_optimization.md"] = r"""# Gradient Descent Optimization & Learning Rate Dynamics

**The iterative calculus engine powering linear models, support vector machines, and deep neural networks.**

<a id="the-intuition"></a>
## 1. The Intuition: Walking Down a Foggy Mountain

You are blindfolded on a foggy mountain and must reach the valley floor. You feel the slope with your feet ($\nabla J(\theta)$) and take a step in the steepest downward direction.

---

<a id="the-math"></a>
## 2. The Parameter Update Rule

Simultaneously update all parameters for $j = 0, \dots, d$:

$$ \theta_j := \theta_j - \alpha \frac{\partial J(\theta)}{\partial \theta_j} $$

Where $\alpha > 0$ is the **Learning Rate**.

::: callout-pitfall Learning Rate Dynamics
- **$\alpha$ too small:** Extremely slow convergence; high computational cost.
- **$\alpha$ too large:** Overshoots the minimum, oscillates wildly, and diverges to infinity.
:::

---

<a id="simulation"></a>
## 3. Visualizing Optimization

::: manim assets/videos/m2_gradient_descent.mp4 Gradient Descent Surface
Watch parameter updates step down the parabolic cost bowl toward the global minimum.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Gradient at Minimum
What is the mathematical value of the gradient vector $\nabla J(\theta^*)$ when parameters reach the exact local or global minimum?
(*A) Zero vector $\vec{0}$
(B) $1.0$
(C) $-\alpha$
(D) Infinity
::: explanation
At the minimum of a smooth convex function, the tangent slope is completely flat, meaning $\nabla J(\theta) = 0$.
:::
"""

m1_files["m1_12_linear_regression_one_variable_ols.md"] = r"""# Simple Linear Regression: Analytical Ordinary Least Squares

**Deriving the closed-form line of best fit using single-variable calculus.**

<a id="the-math"></a>
## 1. Mathematical Formulation

$$ h_\theta(x) = \theta_0 + \theta_1 x $$

Minimizing MSE cost $J(\theta_0, \theta_1) = \frac{1}{2m}\sum ((\theta_0 + \theta_1 x^{(i)}) - y^{(i)})^2$ yields the closed-form solutions:

$$ \theta_1 = \frac{\sum_{i=1}^m (x^{(i)} - \bar{x})(y^{(i)} - \bar{y})}{\sum_{i=1}^m (x^{(i)} - \bar{x})^2} = \frac{\text{Cov}(x, y)}{\text{Var}(x)} $$

$$ \theta_0 = \bar{y} - \theta_1 \bar{x} $$

---

<a id="worked-example"></a>
## 2. Stepped Numerical Example

Given 3 points: $(1, 2), (2, 4), (3, 5)$.
1. $\bar{x} = 2.0, \bar{y} = 3.667$.
2. $\text{Cov}(x, y) = (-1)(-1.667) + (0)(0.333) + (1)(1.333) = 1.667 + 1.333 = 3.0$.
3. $\text{Var}(x) = (-1)^2 + 0^2 + 1^2 = 2.0$.
4. $\theta_1 = \frac{3.0}{2.0} = 1.50$.
5. $\theta_0 = 3.667 - (1.50 \times 2.0) = 0.667$.
**Final Line:** $\hat{y} = 0.667 + 1.50x$.

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Slope Interpretation
In $\hat{y} = 10 + 3.2x$, what does $3.2$ represent?
(A) The predicted $y$ when $x=0$
(*B) The expected change in $y$ for every 1-unit increase in $x$
(C) The correlation coefficient $r$
(D) The mean squared error
::: explanation
The slope $\theta_1 = 3.2$ is the rate of change: for every $+1$ unit added to $x$, the predicted $\hat{y}$ increases by $3.2$ units.
:::
"""

m1_files["m1_13_multiple_linear_regression_matrices.md"] = r"""# Multiple Linear Regression: Matrix Design Formulation

**Extending linear models to multidimensional hyperplanes using vectorized matrix equations.**

<a id="the-math"></a>
## 1. Matrix Vectorization

For $m$ samples and $d$ features:

$$ X = \begin{bmatrix} 1 & x_1^{(1)} & \dots & x_d^{(1)} \\ \vdots & \vdots & \ddots & \vdots \\ 1 & x_1^{(m)} & \dots & x_d^{(m)} \end{bmatrix} \in \mathbb{R}^{m \times (d+1)}, \quad Y = \begin{bmatrix} y^{(1)} \\ \vdots \\ y^{(m)} \end{bmatrix} \in \mathbb{R}^m, \quad \theta = \begin{bmatrix} \theta_0 \\ \vdots \\ \theta_d \end{bmatrix} \in \mathbb{R}^{d+1} $$

### Vectorized Prediction & Cost Function:
$$ \hat{Y} = X\theta $$
$$ J(\theta) = \frac{1}{2m} (X\theta - Y)^T (X\theta - Y) $$

---

<a id="simulation"></a>
## 2. Visualizing Multi-Variable Regression

::: manim assets/videos/m1_08_multiple_regression.mp4 3D Hyperplane Fitting
Watch a 2D plane adjust pitch and roll in 3D feature space to fit data point clusters.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Design Matrix Dimensions
If you have 500 training examples with 8 input features, what are the exact matrix dimensions of the Design Matrix $X$ including the bias intercept column?
(A) $500 \times 8$
(*B) $500 \times 9$
(C) $8 \times 500$
(D) $9 \times 9$
::: explanation
Adding the initial column of $1$s for bias $\theta_0$ makes the dimensions $m \times (d+1) = 500 \times (8+1) = 500 \times 9$.
:::
"""

m1_files["m1_14_normal_equations_and_multicollinearity.md"] = r"""# The Normal Equation & Matrix Inversion Singularities

**Solving multiple linear regression in a single analytical step and diagnosing multicollinearity.**

<a id="the-math"></a>
## 1. Derivation of the Normal Equation

Expanding the vectorized cost function:
$$ J(\theta) = \frac{1}{2m} \left( \theta^T X^T X \theta - 2 Y^T X \theta + Y^T Y \right) $$

Taking the matrix gradient with respect to $\theta$ and setting to 0:
$$ \nabla_\theta J(\theta) = X^T X \theta - X^T Y = 0 \implies \theta^* = (X^T X)^{-1} X^T Y $$

---

<a id="worked-example"></a>
## 2. Non-Invertibility & Multicollinearity

::: callout-pitfall When is $(X^TX)$ Singular (Non-Invertible)?
$(X^TX)$ cannot be inverted if:
1. **Linearly Dependent Features (Multicollinearity):** E.g. $x_1 = \text{size in } \text{ft}^2$ and $x_2 = \text{size in } \text{m}^2$.
2. **Too Few Samples ($m < d$):** More features than training examples.
*Remedy:* Drop redundant features or apply Ridge Regularization $(X^TX + \lambda I)^{-1}$.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Normal Equation Scaling
What is the computational complexity of solving the Normal Equation for $d$ features?
(A) $O(d)$
(B) $O(d^2)$
(*C) $O(d^3)$ due to matrix inversion
(D) $O(\log d)$
::: explanation
Inverting a $(d+1) \times (d+1)$ matrix $(X^TX)$ scales as $O(d^3)$, making it computationally prohibitive when $d > 10,000$.
:::
"""

m1_files["m1_99_practice_lab_mle_map_regression.md"] = r"""# Module 1 Practice Lab: The Complete Numerical Vault

**Step-by-step master numerical solutions for all Module 1 examination categories.**

---

## Category 1: Maximum Likelihood Estimation (MLE)
**Problem:** In $n = 20$ semiconductor chips, $k = 6$ are defective. Calculate $\hat{p}_{\text{MLE}}$.
::: step [Solution] Step-by-Step
1. $L(p) = p^6 (1-p)^{14} \implies \ell(p) = 6\ln(p) + 14\ln(1-p)$.
2. $\frac{d\ell}{dp} = \frac{6}{p} - \frac{14}{1-p} = 0 \implies 6(1-p) = 14p$.
3. $6 = 20p \implies \hat{p} = \frac{6}{20} = 0.30 \quad (30\%)$.
:::

---

## Category 2: Maximum A Posteriori (MAP)
**Problem:** An e-commerce item gets $k=2$ 5-star reviews out of $n=2$ total ratings. Prior is $\text{Beta}(\alpha=4, \beta=4)$.
::: step [Solution] Step-by-Step
$$ \hat{p}_{\text{MAP}} = \frac{k + \alpha - 1}{n + \alpha + \beta - 2} = \frac{2 + 4 - 1}{2 + 4 + 4 - 2} = \frac{5}{8} = 0.625 \quad (62.5\%) $$
:::

---

## Category 3: Ordinary Least Squares (OLS)
**Problem:** Fit a line for points $(1, 2), (2, 4), (3, 5), (4, 4), (5, 5)$.
::: step [Solution] Step-by-Step
1. $\bar{x} = 3.0, \bar{y} = 4.0$.
2. $\sum (x-\bar{x})(y-\bar{y}) = 6.0, \quad \sum (x-\bar{x})^2 = 10.0$.
3. $\theta_1 = \frac{6.0}{10.0} = 0.60, \quad \theta_0 = 4.0 - (0.60 \times 3.0) = 2.20$.
**Fitted Line:** $\hat{y} = 2.20 + 0.60x$.
:::
"""

for fname, content in m1_files.items():
    with open(os.path.join(CONTENT_DIR, fname), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(m1_files)} micro-topics for Module 1.")
