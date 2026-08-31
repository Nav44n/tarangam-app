import os

CONTENT_DIR = os.path.join("content", "PCCST503")

m1_practice = r"""# Module 1 Practice Lab: The Complete Numerical Vault

**Every major numerical problem type, variation, and in-depth derivation required for university exams, GATE, and ML technical interviews.**

---

<a id="the-intuition"></a>
## Overview of Module 1 Problem Types

| Problem Category | Core Concept | What is Evaluated? | Typical Exam Marks |
| :--- | :--- | :--- | :--- |
| **Type 1.1** | Maximum Likelihood Estimation (MLE) | First-order calculus condition $\frac{d}{d\theta}\ln L(\theta) = 0$ on Bernoulli & Gaussian distributions | 7 – 10 Marks |
| **Type 1.2** | Maximum A Posteriori (MAP) | Incorporating Beta & Gaussian priors to regularize small datasets | 7 – 10 Marks |
| **Type 1.3** | Loss & Error Metric Computation | Mean Squared Error (MSE), Root MSE, Mean Absolute Error (MAE), and Cross-Entropy | 3 – 5 Marks |
| **Type 1.4** | Simple Linear Regression (OLS) | Closed-form slope $\theta_1 = \frac{\text{Cov}(x,y)}{\text{Var}(x)}$ and intercept $\theta_0$ | 10 Marks |
| **Type 1.5** | Manual Gradient Descent Execution | Computing gradient updates step-by-step for 1–2 iterations | 7 – 10 Marks |
| **Type 1.6** | Multiple Linear Regression (Normal Eq) | Matrix formulation $\theta = (X^TX)^{-1}X^TY$ and singularity conditions | 10 – 15 Marks |

---

<a id="the-math"></a>
## Category 1.1: Maximum Likelihood Estimation (MLE)

### Problem 1.1.1: Discrete Coin Toss / Quality Control (Standard Bernoulli)
**Problem Statement:** A quality inspection machine tests $n = 20$ semiconductor chips and finds $k = 6$ defective chips. Derive the Maximum Likelihood Estimator (MLE) from first principles and calculate the estimated defect rate $\hat{p}_{\text{MLE}}$.

::: callout-intuition Conceptual Breakdown
- **WHAT:** Find the parameter value $p \in [0, 1]$ that maximizes the joint likelihood of observing our 20 test results.
- **WHY:** We use the Log-Likelihood trick ($\ln L(p)$) because multiplying 20 probabilities causes numerical underflow and makes calculus derivatives intractable. The log function turns products into clean additions.
- **WHEN & WHERE:** Used in sensor calibration, binary click-through-rate (CTR) estimation, and QA testing.
:::

::: step [Step 1: Write Joint Likelihood] Product of Independent Probabilities
Let $x_i = 1$ for defective and $x_i = 0$ for non-defective. Assuming i.i.d. trials:
$$ L(p) = \prod_{i=1}^n P(x_i \mid p) = p^k (1-p)^{n-k} = p^6 (1-p)^{14} $$
:::

::: step [Step 2: Apply Natural Logarithm] Convert to Sum
$$ \ell(p) = \ln L(p) = 6 \ln(p) + 14 \ln(1-p) $$
:::

::: step [Step 3: Compute First Derivative] First-Order Condition
$$ \frac{d}{dp}\ell(p) = \frac{6}{p} - \frac{14}{1-p} $$
*(Note: By chain rule, $\frac{d}{dp}\ln(1-p) = \frac{1}{1-p} \cdot (-1) = -\frac{1}{1-p}$).*
:::

::: step [Step 4: Set to Zero & Solve for Parameter] Find Global Maximum
$$ \frac{6}{p} - \frac{14}{1-p} = 0 \implies \frac{6}{p} = \frac{14}{1-p} $$
Cross-multiplying:
$$ 6(1-p) = 14p \implies 6 - 6p = 14p \implies 6 = 20p $$
$$ \hat{p}_{\text{MLE}} = \frac{6}{20} = 0.30 \quad (30\% \text{ Defect Rate}) $$
:::

---

### Variation 1.1.2: Continuous 1D Normal (Gaussian) Distribution
**Problem Statement:** Derive the Maximum Likelihood Estimator for the mean parameter $\mu$ of a Normal Distribution $\mathcal{N}(\mu, \sigma^2)$ given $m$ samples $x = \{x_1, x_2, \dots, x_m\}$.

::: step [Step 1: Gaussian Likelihood Function] Probability Density Function
$$ P(x_i \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x_i - \mu)^2}{2\sigma^2} \right) $$
$$ L(\mu, \sigma^2) = \prod_{i=1}^m \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x_i - \mu)^2}{2\sigma^2} \right) = \left( 2\pi\sigma^2 \right)^{-\frac{m}{2}} \exp\left( -\sum_{i=1}^m \frac{(x_i - \mu)^2}{2\sigma^2} \right) $$
:::

::: step [Step 2: Log-Likelihood Formulation]
$$ \ell(\mu, \sigma^2) = -\frac{m}{2} \ln(2\pi) - \frac{m}{2} \ln(\sigma^2) - \frac{1}{2\sigma^2} \sum_{i=1}^m (x_i - \mu)^2 $$
:::

::: step [Step 3: Partial Derivative with respect to Mean $\mu$]
$$ \frac{\partial}{\partial \mu} \ell(\mu, \sigma^2) = 0 - 0 - \frac{1}{2\sigma^2} \sum_{i=1}^m 2(x_i - \mu)(-1) = \frac{1}{\sigma^2} \sum_{i=1}^m (x_i - \mu) $$
:::

::: step [Step 4: Set to Zero & Solve]
$$ \frac{1}{\sigma^2} \sum_{i=1}^m (x_i - \mu) = 0 \implies \sum_{i=1}^m x_i - m\mu = 0 \implies \hat{\mu}_{\text{MLE}} = \frac{1}{m} \sum_{i=1}^m x_i $$
*Key Pedagogical Insight:* The Maximum Likelihood Estimator of a Gaussian mean is mathematically identical to the arithmetic sample average!
:::

---

## Category 1.2: Maximum A Posteriori (MAP) Estimation

### Problem 1.2.1: The Cold-Start Rating Problem (Beta Prior)
**Problem Statement:** An e-commerce product is launched. It receives $n = 2$ customer reviews, and both are 5-star positive ($k = 2$). 
1. Compute the pure MLE rating score.
2. Assuming a Beta prior $\text{Beta}(\alpha = 4, \beta = 4)$ representing past historical knowledge of average product quality, compute the Bayesian MAP rating estimate.

::: callout-pitfall Why MAP is Crucial Here
- **MLE Result:** $\hat{p}_{\text{MLE}} = \frac{2}{2} = 1.00$ (100% perfect rating). If an e-commerce ranking algorithm used pure MLE, a product with only 2 reviews would rank higher than a top-rated product with 50,000 positive reviews and 1 negative review!
- **MAP Solution:** MAP acts as a regularizer by adding "pseudo-counts" to both the numerator and denominator.
:::

::: step [Step 1: Formulate Conjugate Posterior] Beta-Binomial Conjugacy
Prior: $P(p) \propto p^{\alpha - 1} (1-p)^{\beta - 1} = p^{4-1} (1-p)^{4-1} = p^3 (1-p)^3$
Likelihood: $L(p) \propto p^k (1-p)^{n-k} = p^2 (1-p)^0$
Posterior: $P(p \mid D) \propto p^{k + \alpha - 1} (1-p)^{n - k + \beta - 1} = p^{2+3} (1-p)^{0+3} = p^5 (1-p)^3$
:::

::: step [Step 2: Compute Mode of Posterior Distribution] MAP Formula
$$ \hat{p}_{\text{MAP}} = \frac{k + \alpha - 1}{n + \alpha + \beta - 2} $$
Substituting the values ($k = 2, n = 2, \alpha = 4, \beta = 4$):
$$ \hat{p}_{\text{MAP}} = \frac{2 + 4 - 1}{2 + 4 + 4 - 2} = \frac{5}{8} = 0.625 \quad (62.5\%) $$
:::

---

## Category 1.3: Cost & Loss Function Computations

### Problem 1.3.1: MSE vs MAE Outlier Sensitivity Analysis
**Problem Statement:** Given 4 actual house prices $y = [200, 300, 400, 500]$ (in thousands) and model predictions $\hat{y} = [210, 290, 410, 800]$:
1. Compute Mean Squared Error (MSE).
2. Compute Root Mean Squared Error (RMSE).
3. Compute Mean Absolute Error (MAE).
4. Explain why MSE is drastically higher due to sample 4.

::: step [Step 1: Compute Individual Residuals]
| Sample $i$ | Actual $y^{(i)}$ | Predicted $\hat{y}^{(i)}$ | Residual $(y - \hat{y})$ | Absolute $|y - \hat{y}|$ | Squared $(y - \hat{y})^2$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 200 | 210 | $-10$ | 10 | 100 |
| 2 | 300 | 290 | $+10$ | 10 | 100 |
| 3 | 400 | 410 | $-10$ | 10 | 100 |
| 4 (Outlier) | 500 | 800 | $-300$ | 300 | 90,000 |
| **Sum** | | | | **330** | **90,300** |
:::

::: step [Step 2: Calculate Metrics]
- **MAE:** $\frac{1}{4}(330) = 82.5\text{k}$
- **MSE:** $\frac{1}{4}(90,300) = 22,575$
- **RMSE:** $\sqrt{22,575} \approx 150.25\text{k}$
- **Why?** Squaring the single 300k error in sample 4 $(300^2 = 90,000)$ accounts for $99.6\%$ of the entire MSE! MAE treats errors linearly, making it far more robust to corrupted outlier data.
:::

---

## Category 1.4: Simple Linear Regression (Ordinary Least Squares)

### Problem 1.4.1: End-to-End Analytical Model Fitting
**Problem Statement:** Fit an optimal linear regression line $\hat{y} = \theta_0 + \theta_1 x$ for the following training data:

| Student | Study Hours ($x$) | Exam Score ($y$) |
| :--- | :--- | :--- |
| A | 1 | 2 |
| B | 2 | 4 |
| C | 3 | 5 |
| D | 4 | 4 |
| E | 5 | 5 |

Calculate:
1. Sample means $\bar{x}$ and $\bar{y}$.
2. Covariance $\text{Cov}(x, y)$ and Variance $\text{Var}(x)$.
3. Optimal slope $\theta_1$ and intercept $\theta_0$.
4. Predicted score for a student who studies $x = 6$ hours.

::: step [Step 1: Compute Sample Means]
$$ \bar{x} = \frac{1 + 2 + 3 + 4 + 5}{5} = \frac{15}{5} = 3.0 $$
$$ \bar{y} = \frac{2 + 4 + 5 + 4 + 5}{5} = \frac{20}{5} = 4.0 $$
:::

::: step [Step 2: Construct the Computation Table]
| $x_i$ | $y_i$ | $(x_i - \bar{x})$ | $(y_i - \bar{y})$ | $(x_i - \bar{x})(y_i - \bar{y})$ | $(x_i - \bar{x})^2$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 2 | $-2$ | $-2$ | $+4$ | 4 |
| 2 | 4 | $-1$ | $0$ | $0$ | 1 |
| 3 | 5 | $0$ | $+1$ | $0$ | 0 |
| 4 | 4 | $+1$ | $0$ | $0$ | 1 |
| 5 | 5 | $+2$ | $+1$ | $+2$ | 4 |
| **Sum** | | | | **$\sum = 6.0$** | **$\sum = 10.0$** |
:::

::: step [Step 3: Solve Slope & Intercept]
$$ \theta_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = \frac{6.0}{10.0} = 0.60 $$
$$ \theta_0 = \bar{y} - \theta_1 \bar{x} = 4.0 - (0.60 \times 3.0) = 4.0 - 1.8 = 2.20 $$
**Fitted Regression Model:** $\hat{y} = 2.20 + 0.60x$
:::

::: step [Step 4: Inference Prediction for $x=6$]
$$ \hat{y}(6) = 2.20 + 0.60(6) = 2.20 + 3.60 = 5.80\text{ Marks} $$
:::

---

## Category 1.5: Manual Gradient Descent Execution

### Problem 1.5.1: 2-Step Hand-Calculated Optimization
**Problem Statement:** Given a simple hypothesis $h_\theta(x) = \theta_1 x$ (with no bias term $\theta_0 = 0$), initial weight $\theta_1^{(0)} = 0.0$, learning rate $\alpha = 0.1$, and training dataset:
$(x^{(1)}, y^{(1)}) = (1, 2)$, $(x^{(2)}, y^{(2)}) = (2, 4)$.
Manually execute **Iteration 1** and **Iteration 2** of Gradient Descent using MSE cost $J(\theta_1) = \frac{1}{2m}\sum (h(x) - y)^2$.

::: step [Step 1: Gradient Formula]
$$ \frac{\partial J}{\partial \theta_1} = \frac{1}{m} \sum_{i=1}^m \left( \theta_1 x^{(i)} - y^{(i)} \right) x^{(i)} $$
:::

::: step [Step 2: Iteration 1 ($\theta_1^{(0)} = 0.0$)]
- Sample 1 error: $(0 \cdot 1 - 2) \cdot 1 = -2$
- Sample 2 error: $(0 \cdot 2 - 4) \cdot 2 = -8$
- Average Gradient: $\frac{1}{2}(-2 + -8) = \frac{-10}{2} = -5.0$
- **Weight Update:**
$$ \theta_1^{(1)} = \theta_1^{(0)} - \alpha \cdot \text{Gradient} = 0.0 - (0.1 \times -5.0) = 0.0 + 0.5 = 0.50 $$
:::

::: step [Step 3: Iteration 2 ($\theta_1^{(1)} = 0.50$)]
- Sample 1 error: $(0.5 \cdot 1 - 2) \cdot 1 = (0.5 - 2) \cdot 1 = -1.5$
- Sample 2 error: $(0.5 \cdot 2 - 4) \cdot 2 = (1.0 - 4) \cdot 2 = -6.0$
- Average Gradient: $\frac{1}{2}(-1.5 + -6.0) = \frac{-7.5}{2} = -3.75$
- **Weight Update:**
$$ \theta_1^{(2)} = 0.50 - (0.1 \times -3.75) = 0.50 + 0.375 = 0.875 $$
*Notice how $\theta_1$ is climbing smoothly toward the true optimal value $\theta_1^* = 2.0$!*
:::

---

## Category 1.6: Multiple Linear Regression via Normal Equations

### Problem 1.6.1: Matrix Form Inversion $(X^TX)^{-1}X^TY$
**Problem Statement:** Find the parameter vector $\theta = [\theta_0, \theta_1]^T$ for the dataset $(1, 1), (2, 3), (3, 2)$ using the Normal Equation.

::: step [Step 1: Construct Design Matrix $X$ and Target Vector $Y$]
$$ X = \begin{bmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{bmatrix}, \quad Y = \begin{bmatrix} 1 \\ 3 \\ 2 \end{bmatrix} $$
:::

::: step [Step 2: Compute $X^T X$ and $X^T Y$]
$$ X^T X = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 2 & 3 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{bmatrix} = \begin{bmatrix} 1+1+1 & 1+2+3 \\ 1+2+3 & 1+4+9 \end{bmatrix} = \begin{bmatrix} 3 & 6 \\ 6 & 14 \end{bmatrix} $$
$$ X^T Y = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 2 & 3 \end{bmatrix} \begin{bmatrix} 1 \\ 3 \\ 2 \end{bmatrix} = \begin{bmatrix} 1+3+2 \\ 1+6+6 \end{bmatrix} = \begin{bmatrix} 6 \\ 13 \end{bmatrix} $$
:::

::: step [Step 3: Compute Matrix Inverse $(X^T X)^{-1}$]
Determinant: $\det(X^TX) = (3)(14) - (6)(6) = 42 - 36 = 6$.
Adjugate matrix: $\begin{bmatrix} 14 & -6 \\ -6 & 3 \end{bmatrix}$.
$$ (X^T X)^{-1} = \frac{1}{6} \begin{bmatrix} 14 & -6 \\ -6 & 3 \end{bmatrix} $$
:::

::: step [Step 4: Solve $\theta^* = (X^T X)^{-1} X^T Y$]
$$ \theta = \frac{1}{6} \begin{bmatrix} 14 & -6 \\ -6 & 3 \end{bmatrix} \begin{bmatrix} 6 \\ 13 \end{bmatrix} = \frac{1}{6} \begin{bmatrix} (14 \times 6) + (-6 \times 13) \\ (-6 \times 6) + (3 \times 13) \end{bmatrix} = \frac{1}{6} \begin{bmatrix} 84 - 78 \\ -36 + 39 \end{bmatrix} = \frac{1}{6} \begin{bmatrix} 6 \\ 3 \end{bmatrix} = \begin{bmatrix} 1.0 \\ 0.5 \end{bmatrix} $$
**Final Model:** $\hat{y} = 1.0 + 0.5x$
:::
"""

with open(os.path.join(CONTENT_DIR, "m1_99_practice.md"), "w", encoding="utf-8") as f:
    f.write(m1_practice)

print("Module 1 Practice Numerical Vault generated successfully.")
