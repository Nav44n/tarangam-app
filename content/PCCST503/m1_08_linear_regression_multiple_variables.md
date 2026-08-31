# Multiple Linear Regression & Normal Equations

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
