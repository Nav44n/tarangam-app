# Simple Linear Regression (One Variable)

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
