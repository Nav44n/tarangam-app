# KNN Hyperparameters: Bias-Variance & Feature Scaling

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
