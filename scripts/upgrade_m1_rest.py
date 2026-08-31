import os

CONTENT_DIR = os.path.join("content", "PCCST503")

# m1_04_parameter_estimation_map.md
m1_04 = r"""# Parameter Estimation: Maximum A Posteriori (MAP)

**How to inject prior common sense into parameter estimation so small datasets don't mislead your model.**

<a id="the-intuition"></a>
## 1. The Intuition: When MLE Fails Spectacularly

Imagine a friend hands you a brand-new, standard coin. You flip it **3 times**, and it lands on **Heads all 3 times**.

::: callout-intuition Why Common Sense Matters
- **Pure MLE says:** $\hat{p}_{\text{MLE}} = \frac{3}{3} = 1.00$ (*"This coin is physically incapable of landing on Tails!"*).
- **Your Brain says:** *"No, I have flipped thousands of normal coins in my life. The probability is almost certainly around $0.50$, and 3 heads was just a lucky streak."*
- **Maximum A Posteriori (MAP)** is Bayesian parameter estimation. It combines your **Prior Belief ($P(\theta)$)** with the **Observed Likelihood ($P(D|\theta)$)** to find the balanced posterior truth.
:::

---

<a id="the-math"></a>
## 2. Bayes' Theorem Formulation

From Bayes' Theorem:

$$ P(\theta | D) = \frac{P(D | \theta) P(\theta)}{P(D)} $$

Where:
- $P(\theta | D)$ is the **Posterior Probability** (the probability of parameter $\theta$ given the observed data).
- $P(D | \theta)$ is the **Likelihood** (how probable the data is under parameter $\theta$).
- $P(\theta)$ is the **Prior** (our belief about $\theta$ before seeing the experiment).
- $P(D) = \int P(D|\theta)P(\theta)d\theta$ is the **Evidence** (a constant scaling factor independent of $\theta$).

### The MAP Optimization Objective:
Since the denominator $P(D)$ does not depend on $\theta$, the MAP estimate solves:

$$ \hat{\theta}_{\text{MAP}} = \arg\max_\theta P(\theta | D) = \arg\max_\theta \left[ \ln P(D | \theta) + \ln P(\theta) \right] $$

::: callout-formula MLE vs MAP Head-to-Head
| Feature | Maximum Likelihood (MLE) | Maximum A Posteriori (MAP) |
| :--- | :--- | :--- |
| **Philosophical School** | Frequentist | Bayesian |
| **Formula** | $\arg\max_\theta \ln P(D\|\theta)$ | $\arg\max_\theta [\ln P(D\|\theta) + \ln P(\theta)]$ |
| **Small Data Performance** | Prone to extreme overfitting | Robust (anchored by prior) |
| **Infinite Data Limit ($N \to \infty$)** | Converges to true parameter | Converges to MLE (Data overwhelms the prior!) |
| **Regularization Link** | Unregularized model | Equivalent to L2 (Ridge) / L1 (Lasso) regularization |
:::

---

<a id="worked-example"></a>
## 3. Deriving MAP for a Coin Toss (Beta Prior)

Let the prior on $p$ be modeled by a **Beta distribution** $\text{Beta}(\alpha, \beta)$, which acts as pseudo-counts ($\alpha-1$ prior heads, $\beta-1$ prior tails):

$$ P(p) \propto p^{\alpha - 1} (1-p)^{\beta - 1} $$

::: step [Step 1: Joint Likelihood & Prior] Setup
$$ P(D | p) P(p) = \left[ p^k (1-p)^{n-k} \right] \cdot \left[ p^{\alpha - 1} (1-p)^{\beta - 1} \right] = p^{k + \alpha - 1} (1-p)^{n - k + \beta - 1} $$
:::

::: step [Step 2: Log-Posterior] Log Transformation
$$ \ln P(p | D) = (k + \alpha - 1) \ln(p) + (n - k + \beta - 1) \ln(1-p) + \text{const} $$
:::

::: step [Step 3: Differentiation & Solution] Finding Peak
Taking derivative with respect to $p$ and setting to zero yields:
$$ \hat{p}_{\text{MAP}} = \frac{k + \alpha - 1}{n + \alpha + \beta - 2} $$
:::

::: callout-exam Example with Numbers
If our prior is $\text{Beta}(5, 5)$ (representing a strong prior belief of a fair coin) and we observe $k=3$ heads in $n=3$ tosses:
$$ \hat{p}_{\text{MAP}} = \frac{3 + 5 - 1}{3 + 5 + 5 - 2} = \frac{7}{11} \approx 0.636 $$
Notice how MAP wisely pulled the extreme $1.0$ estimate back toward the sensible $0.50$ baseline!
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Asymptotic Behavior
What happens to the MAP estimate $\hat{\theta}_{\text{MAP}}$ as the sample size $N \to \infty$ (approaches infinity)?
(A) The prior completely dominates the data
(*B) The MAP estimate converges exactly to the MLE estimate
(C) The variance of the parameter estimate increases
(D) The posterior probability collapses to zero
::: explanation
As the volume of observed empirical data grows infinitely large ($N \to \infty$), the likelihood term $\ln P(D|\theta)$ grows linearly with $N$ and completely overwhelms the fixed prior $\ln P(\theta)$, making MAP identical to MLE.
:::

::: quiz Q2: Regularization Equivalence
In linear regression, placing a zero-mean Gaussian (Normal) prior on the weight vector $w \sim \mathcal{N}(0, \sigma^2)$ is mathematically equivalent to which technique?
(A) L1 Regularization (Lasso)
(*B) L2 Regularization (Ridge Regression / Weight Decay)
(C) Dropout
(D) Early Stopping
::: explanation
A Gaussian prior adds $-\frac{\lambda}{2}\|w\|_2^2$ to the log-likelihood objective, which is the exact penalty term used in Ridge Regression ($L_2$). A Laplace prior conversely yields L1 (Lasso) regularization.
:::
"""

# m1_05_supervised_learning_formulation.md
m1_05 = r"""# Supervised Learning Formulation

**The mathematical framework of inputs, outputs, hypothesis functions, and hypothesis spaces.**

<a id="the-intuition"></a>
## 1. The Intuition: The Mathematical Function Machine

In supervised learning, our goal is to build an artificial function machine that takes a set of input measurements (like house size, location, age) and outputs an accurate target prediction (like price).

::: callout-intuition The Formal Setup
- **The Feature Vector ($x$):** An ordered list of numerical attributes describing an instance.
- **The Ground Truth Label ($y$):** The verified outcome we wish to predict.
- **The Hypothesis ($h_\theta(x)$):** Our candidate mathematical equation that approximates the true underlying relationship $f(x)$.
:::

---

<a id="the-math"></a>
## 2. Formal Mathematical Definitions

Let the training dataset be denoted as:

$$ \mathcal{D} = \left\{ (x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), \dots, (x^{(m)}, y^{(m)}) \right\} $$

Where:
- $m$ is the total number of training examples.
- $x^{(i)} \in \mathbb{R}^d$ is a $d$-dimensional feature vector for example $i$:
  $$ x^{(i)} = \begin{bmatrix} x_1^{(i)} \\ x_2^{(i)} \\ \vdots \\ x_d^{(i)} \end{bmatrix} $$
- $y^{(i)} \in \mathcal{Y}$ is the corresponding target label:
  - In **Regression**, $\mathcal{Y} = \mathbb{R}$ (continuous values like house prices, temperature).
  - In **Binary Classification**, $\mathcal{Y} = \{0, 1\}$ or $\{-1, +1\}$ (spam vs not spam, malignant vs benign).
  - In **Multi-Class Classification**, $\mathcal{Y} = \{1, 2, \dots, K\}$ (handwritten digit recognition 0–9).

### The Hypothesis Space $\mathcal{H}$
The hypothesis space $\mathcal{H}$ represents the entire family of candidate functions our algorithm is permitted to explore. 
For a linear model:

$$ \mathcal{H} = \left\{ h_\theta(x) = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d \mid \theta \in \mathbb{R}^{d+1} \right\} $$

::: callout-formula Variable Decoder Table
| Symbol | Formal Term | Plain English Meaning |
| :--- | :--- | :--- |
| $m$ | Sample size | Total number of training rows/examples |
| $d$ | Dimensionality | Number of input features per example |
| $x^{(i)}$ | Feature vector | The $i$-th row of measurements |
| $y^{(i)}$ | Target label | The verified correct answer for row $i$ |
| $\theta$ | Parameter vector | The internal dial settings / weights of the model |
| $h_\theta(x)$ | Hypothesis function | The model's prediction equation for a given $x$ |
:::

---

<a id="worked-example"></a>
## 3. Dataset Splitting & Generalization Protocol

To ensure the model does not merely memorize the training examples (overfitting), we partition the dataset:

::: step [Partition 1: Training Set (70%)] Model Optimization
Used exclusively by the optimization algorithm to compute gradients and adjust parameters $\theta$.
:::

::: step [Partition 2: Validation Set (15%)] Hyperparameter Tuning
Used to evaluate model performance, select model architecture, and tune hyperparameters (e.g. learning rate $\alpha$, polynomial degree).
:::

::: step [Partition 3: Test Set (15%)] Final Benchmark
Locked away until the very end. Serves as an unbiased estimate of real-world generalization performance on unseen data.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Problem Categorization
A hospital wants to predict the **exact duration (in days and hours)** a patient will spend in the ICU based on admission vitals. What type of supervised learning problem is this?
(A) Binary Classification
(B) Multi-Class Classification
(*C) Regression
(D) Unsupervised Density Estimation
::: explanation
Because the target variable (time spent in ICU) is a continuous numerical value ($\mathbb{R}$), this is a Regression task. If it were predicting "ICU stay $> 5$ days: Yes/No", it would be Binary Classification.
:::
"""

# m1_06_loss_functions_optimization.md
m1_06 = r"""# Loss Functions & Optimization: Gradient Descent

**How machine learning models measure their own mistakes and iteratively correct them.**

<a id="the-intuition"></a>
## 1. The Intuition: Walking Down a Foggy Mountain

Imagine you are blindfolded on a foggy mountain and need to reach the lowest point in the valley.

::: callout-intuition The Gradient Descent Strategy
1. You feel the slope of the ground beneath your feet with your foot (**Compute the Gradient $\nabla J(\theta)$**).
2. If the ground slopes downward to your right, you take a step to the right (**Move in the negative gradient direction**).
3. If you take tiny baby steps ($\alpha = 0.0001$), you will take 10 years to reach the bottom.
4. If you take giant blind leaps ($\alpha = 10.0$), you might leap clear across the valley and crash into the opposite peak.
5. The ideal step size is the **Learning Rate ($\alpha$)**.
:::

---

<a id="the-math"></a>
## 2. Loss Functions: Measuring Mistakes

A **Loss Function** $\mathcal{L}(\hat{y}, y)$ quantifies the error for a single training example, while the **Cost Function** $J(\theta)$ computes the average loss across the entire dataset.

### 1. Mean Squared Error (MSE) — for Regression:
$$ J(\theta) = \frac{1}{2m} \sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)} \right)^2 $$
*(Note: The factor of $\frac{1}{2}$ is a mathematical convenience that cleanly cancels when taking derivatives).*

### 2. Binary Cross-Entropy (Log Loss) — for Classification:
$$ J(\theta) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln(h_\theta(x^{(i)})) + (1-y^{(i)}) \ln(1-h_\theta(x^{(i)})) \right] $$

---

<a id="worked-example"></a>
## 3. The Gradient Descent Update Rule

To minimize $J(\theta)$, we iteratively update every parameter $\theta_j$ simultaneously:

$$ \theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta) $$

For Linear Regression with MSE cost, the partial derivative simplifies to:

$$ \frac{\partial}{\partial \theta_j} J(\theta) = \frac{1}{m} \sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_j^{(i)} $$

::: step [Step 1: Compute Prediction] Forward Pass
Calculate $\hat{y}^{(i)} = h_\theta(x^{(i)})$ for all samples.
:::

::: step [Step 2: Calculate Residual Error] Error Calculation
Compute error $e^{(i)} = (\hat{y}^{(i)} - y^{(i)})$.
:::

::: step [Step 3: Compute Gradient Vector] Differentiation
Multiply error by feature values $x_j^{(i)}$ and average across the batch.
:::

::: step [Step 4: Update Parameters] Step Down
Adjust parameters: $\theta_j \leftarrow \theta_j - \alpha \cdot \text{Gradient}$.
:::

---

<a id="simulation"></a>
## 4. Visualizing Gradient Optimization

::: manim assets/videos/m2_gradient_descent.mp4 Convex Optimization Convergence
Watch the red optimization ball take steps down the parabolic cost curve toward the global minimum.
:::

---

<a id="self-check"></a>
## 5. Active Recall Checkpoint

::: quiz Q1: Hyperparameter Dynamics
What occurs if the learning rate $\alpha$ is set too large in Gradient Descent?
(A) The model converges prematurely to a saddle point
(*B) The cost function can oscillate wildly and diverge away from the minimum
(C) The gradient becomes zero on the first iteration
(D) The weights automatically shrink to zero
::: explanation
When $\alpha$ is excessively large, each parameter update overshoots the minimum point, landing higher up on the opposite wall of the cost surface. This causes the cost $J(\theta)$ to increase with every iteration (divergence).
:::
"""

# m1_07_linear_regression_one_variable.md
m1_07 = r"""# Simple Linear Regression (One Variable)

**Fitting the optimal line of best fit to uncover linear relationships between two continuous variables.**

<a id="the-intuition"></a>
## 1. The Intuition: The Study Hours vs Exam Score Line

Suppose you collect data on student study hours ($x$) and their resulting exam scores ($y$).

::: callout-intuition Line of Best Fit
You want to draw a straight line through the scatter plot such that the total vertical distance (residuals) from every data point to your line is as small as possible.
:::

---

<a id="the-math"></a>
## 2. Mathematical Formulation

### The Hypothesis Equation:
$$ h_\theta(x) = \theta_0 + \theta_1 x $$
Where:
- $\theta_0$ is the $y$-intercept (the predicted score when study hours $x = 0$).
- $\theta_1$ is the slope (the expected increase in exam score for every 1 additional hour studied).

### The Objective Function (Ordinary Least Squares):
$$ J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^m \left( (\theta_0 + \theta_1 x^{(i)}) - y^{(i)} \right)^2 $$

### Analytical Closed-Form Solution:
Instead of running iterative Gradient Descent, Simple Linear Regression can be solved directly via calculus in $O(m)$ time:

$$ \theta_1 = \frac{\sum_{i=1}^m (x^{(i)} - \bar{x})(y^{(i)} - \bar{y})}{\sum_{i=1}^m (x^{(i)} - \bar{x})^2} = \frac{\text{Cov}(x, y)}{\text{Var}(x)} $$

$$ \theta_0 = \bar{y} - \theta_1 \bar{x} $$

Where $\bar{x} = \frac{1}{m}\sum x^{(i)}$ and $\bar{y} = \frac{1}{m}\sum y^{(i)}$ are the sample means.

---

<a id="worked-example"></a>
## 3. Stepped Numerical Example

Let's calculate the line of best fit for a 3-point dataset: $(1, 2), (2, 3), (3, 5)$.

::: step [Step 1: Compute Means] Average Values
- $\bar{x} = \frac{1 + 2 + 3}{3} = 2.0$
- $\bar{y} = \frac{2 + 3 + 5}{3} = 3.333$
:::

::: step [Step 2: Compute Covariance Numerator] $\sum (x-\bar{x})(y-\bar{y})$
- $(1-2)(2-3.333) = (-1)(-1.333) = 1.333$
- $(2-2)(3-3.333) = (0)(-0.333) = 0.000$
- $(3-2)(5-3.333) = (1)(1.667) = 1.667$
- **Numerator Sum:** $1.333 + 0.000 + 1.667 = 3.0$
:::

::: step [Step 3: Compute Variance Denominator] $\sum (x-\bar{x})^2$
- $(1-2)^2 = 1$
- $(2-2)^2 = 0$
- $(3-2)^2 = 1$
- **Denominator Sum:** $1 + 0 + 1 = 2.0$
:::

::: step [Step 4: Solve Parameters] Final Equation
- $\theta_1 = \frac{3.0}{2.0} = 1.5$
- $\theta_0 = \bar{y} - \theta_1 \bar{x} = 3.333 - (1.5 \times 2.0) = 0.333$
- **Optimal Model:** $\hat{y} = 0.333 + 1.5x$
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Slope Interpretation
In the fitted model $\hat{y} = 25 + 4.5x$, where $x$ is years of experience and $y$ is salary in thousands of dollars, what does the value $4.5$ represent?
(A) The base salary for someone with zero years experience
(*B) The expected salary increase of \$4,500 for every additional year of experience
(C) The maximum possible salary attainable
(D) The variance of the residuals
::: explanation
The slope coefficient $\theta_1 = 4.5$ represents the marginal rate of change: for every 1-unit increase in $x$, the predicted target $\hat{y}$ increases by $4.5$ units (\$4,500).
:::
"""

# m1_08_linear_regression_multiple_variables.md
m1_08 = r"""# Multiple Linear Regression & Normal Equations

**Extending regression to multidimensional feature spaces using compact matrix algebra.**

<a id="the-intuition"></a>
## 1. The Intuition: Multi-Factor Predictions

Real-world phenomena rarely depend on a single variable. A house's value depends on **square footage ($x_1$)**, **number of bedrooms ($x_2$)**, **distance to metro ($x_3$)**, and **crime rate ($x_4$)**.

::: callout-intuition The Multiple Linear Model
$$ h_\theta(x) = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \dots + \theta_d x_d $$
Instead of a 2D line of best fit, we are fitting a $d$-dimensional **hyperplane** through high-dimensional feature space!
:::

---

<a id="the-math"></a>
## 2. Matrix Vectorization & The Normal Equation

We bundle all $m$ training examples into a single Design Matrix $X \in \mathbb{R}^{m \times (d+1)}$ (including an initial column of $1$s for the intercept bias $\theta_0$):

$$ X = \begin{bmatrix} 1 & x_1^{(1)} & x_2^{(1)} & \dots & x_d^{(1)} \\ 1 & x_1^{(2)} & x_2^{(2)} & \dots & x_d^{(2)} \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 1 & x_1^{(m)} & x_2^{(m)} & \dots & x_d^{(m)} \end{bmatrix}, \quad Y = \begin{bmatrix} y^{(1)} \\ y^{(2)} \\ \vdots \\ y^{(m)} \end{bmatrix}, \quad \theta = \begin{bmatrix} \theta_0 \\ \theta_1 \\ \vdots \\ \theta_d \end{bmatrix} $$

### The Vectorized Cost Function:
$$ J(\theta) = \frac{1}{2m} (X\theta - Y)^T (X\theta - Y) $$

### The Normal Equation (Analytical Global Minimum):
Setting the matrix gradient $\nabla_\theta J(\theta) = 0$ yields the celebrated **Normal Equation**:

$$ X^T X \theta = X^T Y \implies \theta^* = (X^T X)^{-1} X^T Y $$

::: callout-formula Normal Equation vs Gradient Descent
| Dimension | Normal Equation | Gradient Descent |
| :--- | :--- | :--- |
| **Learning Rate $\alpha$** | Not needed! | Must be chosen carefully |
| **Iterations** | Zero (Solves in 1 analytical step) | Many iterative epochs required |
| **Feature Scaling** | Not required | Mandatory for fast convergence |
| **Time Complexity** | $O(d^3)$ due to $(X^TX)^{-1}$ matrix inversion | $O(k \cdot m \cdot d)$ |
| **When to use** | Small to moderate features ($d < 10,000$) | Huge feature spaces ($d > 100,000$) |
:::

---

<a id="worked-example"></a>
## 3. Non-Invertibility & Multicollinearity Pitfall

::: callout-pitfall When is $(X^TX)$ Singular (Non-Invertible)?
The matrix $X^TX$ cannot be inverted if:
1. **Redundant Features (Multicollinearity):** E.g., $x_1$ is size in $\text{feet}^2$ and $x_2$ is size in $\text{meters}^2$ ($x_1 = 10.76 x_2$). They are linearly dependent.
2. **Too Few Examples ($m < d$):** More features than training samples.
*Fix:* Remove redundant features or use Regularization (Ridge regression ensures $(X^TX + \lambda I)$ is strictly invertible!).
:::

---

<a id="simulation"></a>
## 4. Visualizing Multi-Variable Regression

::: manim assets/videos/m1_08_multiple_regression.mp4 3D Regression Plane Optimization
Watch how the 3D plane adjusts its tilt and pitch to minimize the sum of squared distances to 3D point clusters.
:::

---

<a id="self-check"></a>
## 5. Active Recall Checkpoint

::: quiz Q1: Computational Complexity
If a dataset contains $d = 200,000$ features and $m = 1,000,000$ training records, which method should you choose to train linear regression?
(A) The Normal Equation $(X^TX)^{-1}X^TY$
(*B) Mini-batch Gradient Descent
(C) Inverting the Design Matrix $X^{-1}$ directly
(D) Exhaustive grid search
::: explanation
Inverting a $200,000 \times 200,000$ matrix $(X^TX)$ takes $O(d^3) \approx 8 \times 10^{15}$ operations, which will crash your computer's memory. Gradient descent scales linearly with $d$ and is the only viable method for large-scale ML.
:::
"""

with open(os.path.join(CONTENT_DIR, "m1_04_parameter_estimation_map.md"), "w", encoding="utf-8") as f:
    f.write(m1_04)
with open(os.path.join(CONTENT_DIR, "m1_05_supervised_learning_formulation.md"), "w", encoding="utf-8") as f:
    f.write(m1_05)
with open(os.path.join(CONTENT_DIR, "m1_06_loss_functions_optimization.md"), "w", encoding="utf-8") as f:
    f.write(m1_06)
with open(os.path.join(CONTENT_DIR, "m1_07_linear_regression_one_variable.md"), "w", encoding="utf-8") as f:
    f.write(m1_07)
with open(os.path.join(CONTENT_DIR, "m1_08_linear_regression_multiple_variables.md"), "w", encoding="utf-8") as f:
    f.write(m1_08)

print("All Module 1 topics upgraded to production standard.")
