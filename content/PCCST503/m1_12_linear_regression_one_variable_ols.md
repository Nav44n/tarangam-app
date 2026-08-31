# Simple Linear Regression: Analytical Ordinary Least Squares

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
