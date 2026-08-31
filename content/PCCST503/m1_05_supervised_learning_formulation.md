# Supervised Learning Formulation

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
