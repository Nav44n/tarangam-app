# Multiple Linear Regression: Matrix Design Formulation

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
