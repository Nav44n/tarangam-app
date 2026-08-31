# Loss Functions & Error Metrics: MSE, MAE, and Cross-Entropy

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
