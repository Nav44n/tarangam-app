# Progressive Problems: Simple Linear Regression & OLS Closed-Form

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped arithmetic, and full line-by-line derivations.

---

## Level 1: 5-Point Dataset OLS Calculation & Line of Best Fit

### Problem 1.1: Deriving the Exact OLS Line of Best Fit from Scratch

**Problem Statement:** A teacher observes the relationship between study hours ($X$) and exam scores ($Y$) for $n = 5$ students:

$$\{(x_1, y_1), (x_2, y_2), (x_3, y_3), (x_4, y_4), (x_5, y_5)\} = \{(1, 2), (2, 3), (3, 5), (4, 6), (5, 9)\}$$

Where:
- $X$ is the independent input feature (Study Hours).
- $Y$ is the dependent target variable (Exam Score out of 10).

Using the Ordinary Least Squares (OLS) closed-form formulas:
1. Compute the sample means $\bar{x}$ and $\bar{y}$.
2. Build an explicit step-by-step deviations table computing $(x_i - \bar{x})$, $(y_i - \bar{y})$, their cross-product $(x_i - \bar{x})(y_i - \bar{y})$, and the squared deviation $(x_i - \bar{x})^2$.
3. Compute the sample covariance term $\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})$ and the sample variance term $\sum_{i=1}^{n}(x_i - \bar{x})^2$.
4. Calculate the optimal slope coefficient $\beta_1$.
5. Calculate the optimal vertical intercept coefficient $\beta_0$.
6. Formulate the final regression line equation $\hat{y} = \beta_0 + \beta_1 x$.
7. Use the equation to predict the expected exam score for a student who studies $3.5\text{ hours}$ and a student who studies $6\text{ hours}$.

::: callout-intuition Core Mental Model
Imagine you have a rigid wooden ruler floating over a 2D scatter plot. Each data point is a small magnet trying to pull the ruler toward itself.  
- **Ordinary Least Squares (OLS):** OLS rotates and shifts the ruler until the sum of all the squared vertical distances between each magnet and the ruler is as small as humanly possible.  
- **The Slope ($\beta_1$):** How steep the ruler tilts. For every 1 hour you push to the right, how many points does the ruler rise?  
- **The Intercept ($\beta_0$):** Where the ruler touches the vertical $Y$-axis when study time is exactly zero.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Identify the Dataset and Count Data Points</div>

**What are we doing?** Listing the raw pairs and counting the total number of observations ($n$).

**Why are we starting here?** You cannot calculate an average or sum without knowing your sample size $n$.

**How do we do it?** We write out each coordinate $(x_i, y_i)$:
- Student 1: $x_1 = 1,\quad y_1 = 2$
- Student 2: $x_2 = 2,\quad y_2 = 3$
- Student 3: $x_3 = 3,\quad y_3 = 5$
- Student 4: $x_4 = 4,\quad y_4 = 6$
- Student 5: $x_5 = 5,\quad y_5 = 9$

Total number of observations:
$$n = 5$$

**Where did this formula/concept come from?** Basic sample definition: $n$ represents the cardinal count of elements in a finite dataset.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Calculate the Sample Mean of X (x̄)</div>

**What changed from Step 1?** We have our list of $X$ values. Now we calculate their arithmetic center.

**What are we doing?** Summing all study hour values ($x_i$) and dividing by the count ($n = 5$).

**Why are we doing this?** The OLS formula measures how far each point deviates from the "center of gravity" of the inputs.

**How do we do it?** The formula for the sample mean $\bar{x}$ is:
$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i = \frac{x_1 + x_2 + x_3 + x_4 + x_5}{5}$$

Substitute the values:
$$\sum_{i=1}^{5} x_i = 1 + 2 + 3 + 4 + 5 = 15$$
$$\bar{x} = \frac{15}{5} = 3.0$$

**Where did this formula/concept come from?** The classical definition of arithmetic mean (average).
</div>

<div class="step-card">
<div class="step-badge">Step 3: Calculate the Sample Mean of Y (ȳ)</div>

**What changed from Step 2?** We computed the horizontal center $\bar{x} = 3.0$. Now we compute the vertical center $\bar{y}$.

**What are we doing?** Summing all score values ($y_i$) and dividing by $n = 5$.

**Why are we doing this?** We need to know the baseline average score before we look at how study hours influence scores.

**How do we do it?** The formula for the sample mean $\bar{y}$ is:
$$\bar{y} = \frac{1}{n}\sum_{i=1}^{n} y_i = \frac{y_1 + y_2 + y_3 + y_4 + y_5}{5}$$

Substitute the values:
$$\sum_{i=1}^{5} y_i = 2 + 3 + 5 + 6 + 9 = 25$$
$$\bar{y} = \frac{25}{5} = 5.0$$

The centroid (center of mass) of our data is the point $(\bar{x}, \bar{y}) = (3.0, 5.0)$.

**Where did this formula/concept come from?** Standard arithmetic mean of the target variable $Y$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Compute Individual Deviations (x_i - x̄) and (y_i - ȳ)</div>

**What changed from Step 3?** We now know $\bar{x} = 3.0$ and $\bar{y} = 5.0$. Now we find how far each individual student sits from these center lines.

**What are we doing?** Subtracting $\bar{x}$ from each $x_i$, and subtracting $\bar{y}$ from each $y_i$.

**Why are we doing this?** Raw coordinates can be misleading. Looking at differences from the mean tells us: *"Did this student study more or less than the average student? Did they score higher or lower than the average student?"*

**How do we do it?** Compute row-by-row:
- Student 1:
  $$x_1 - \bar{x} = 1 - 3.0 = -2.0$$
  $$y_1 - \bar{y} = 2 - 5.0 = -3.0$$
- Student 2:
  $$x_2 - \bar{x} = 2 - 3.0 = -1.0$$
  $$y_2 - \bar{y} = 3 - 5.0 = -2.0$$
- Student 3:
  $$x_3 - \bar{x} = 3 - 3.0 = 0.0$$
  $$y_3 - \bar{y} = 5 - 5.0 = 0.0$$
- Student 4:
  $$x_4 - \bar{x} = 4 - 3.0 = +1.0$$
  $$y_4 - \bar{y} = 6 - 5.0 = +1.0$$
- Student 5:
  $$x_5 - \bar{x} = 5 - 3.0 = +2.0$$
  $$y_5 - \bar{y} = 9 - 5.0 = +4.0$$

Notice a key property:
$$\sum (x_i - \bar{x}) = (-2.0) + (-1.0) + 0.0 + 1.0 + 2.0 = 0.0$$
$$\sum (y_i - \bar{y}) = (-3.0) + (-2.0) + 0.0 + 1.0 + 4.0 = 0.0$$
The sum of deviations about the mean is always strictly zero.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Compute Cross-Products and Squared Deviations</div>

**What changed from Step 4?** We have individual deviation columns. Now we multiply them together to measure shared movement (covariance) and input spread (variance).

**What are we doing?** Calculating:
1. Cross-Product: $(x_i - \bar{x})(y_i - \bar{y})$
2. Squared $X$-Deviation: $(x_i - \bar{x})^2$

**Why are we doing this?**
- If $(x_i - \bar{x})$ and $(y_i - \bar{y})$ have the same sign (both positive or both negative), their product is positive. This means studying more than average leads to scoring higher than average, and studying less leads to scoring lower.  
- $(x_i - \bar{x})^2$ measures the dispersion of the input points along the horizontal axis.

**How do we do it?**
- Student 1:
  $$(x_1 - \bar{x})(y_1 - \bar{y}) = (-2.0) \times (-3.0) = +6.0$$
  $$(x_1 - \bar{x})^2 = (-2.0)^2 = 4.0$$
- Student 2:
  $$(x_2 - \bar{x})(y_2 - \bar{y}) = (-1.0) \times (-2.0) = +2.0$$
  $$(x_2 - \bar{x})^2 = (-1.0)^2 = 1.0$$
- Student 3:
  $$(x_3 - \bar{x})(y_3 - \bar{y}) = (0.0) \times (0.0) = 0.0$$
  $$(x_3 - \bar{x})^2 = (0.0)^2 = 0.0$$
- Student 4:
  $$(x_4 - \bar{x})(y_4 - \bar{y}) = (+1.0) \times (+1.0) = +1.0$$
  $$(x_4 - \bar{x})^2 = (+1.0)^2 = 1.0$$
- Student 5:
  $$(x_5 - \bar{x})(y_5 - \bar{y}) = (+2.0) \times (+4.0) = +8.0$$
  $$(x_5 - \bar{x})^2 = (+2.0)^2 = 4.0$$

Let us assemble these rows into the complete working deviations table:

| $i$ | $x_i$ | $y_i$ | $x_i - \bar{x}$ | $y_i - \bar{y}$ | $(x_i - \bar{x})(y_i - \bar{y})$ | $(x_i - \bar{x})^2$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 1 | 2 | $-2.0$ | $-3.0$ | $+6.0$ | $4.0$ |
| 2 | 2 | 3 | $-1.0$ | $-2.0$ | $+2.0$ | $1.0$ |
| 3 | 3 | 5 | $0.0$ | $0.0$ | $0.0$ | $0.0$ |
| 4 | 4 | 6 | $+1.0$ | $+1.0$ | $+1.0$ | $1.0$ |
| 5 | 5 | 9 | $+2.0$ | $+4.0$ | $+8.0$ | $4.0$ |
| **Sum ($\sum$)** | **15** | **25** | **0.0** | **0.0** | **+17.0** | **10.0** |
</div>

<div class="step-card">
<div class="step-badge">Step 6: Calculate the Optimal Slope Coefficient (β₁)</div>

**What changed from Step 5?** We have summed our columns: $\sum(x_i - \bar{x})(y_i - \bar{y}) = 17.0$ and $\sum(x_i - \bar{x})^2 = 10.0$.

**What are we doing?** Calculating $\beta_1$ using the Ordinary Least Squares closed-form equation.

**Why are we doing this?** We need to know how steep our regression line must tilt to minimize the squared vertical errors.

**How do we do it?** The OLS formula for slope is:
$$\beta_1 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n} (x_i - \bar{x})^2} = \frac{\text{Covariance}(X, Y)}{\text{Variance}(X)}$$

Substitute our exact sums:
$$\beta_1 = \frac{17.0}{10.0} = 1.7$$

**Where did this formula/concept come from?** Setting the partial derivative of the Residual Sum of Squares with respect to $\beta_1$ to zero:
$$\frac{\partial}{\partial \beta_1} \sum_{i=1}^{n} \big(y_i - (\beta_0 + \beta_1 x_i)\big)^2 = 0$$
Solving this calculus optimization problem yields this closed-form quotient.
</div>

<div class="step-card">
<div class="step-badge">Step 7: Calculate the Optimal Intercept Coefficient (β₀)</div>

**What changed from Step 6?** We now have $\beta_1 = 1.7$, along with our known center point $(\bar{x}, \bar{y}) = (3.0, 5.0)$.

**What are we doing?** Calculating $\beta_0$.

**Why are we doing this?** Knowing the slope tells us the angle of the line, but the line could be shifted up or down anywhere on the graph. $\beta_0$ anchors the line in vertical space.

**How do we do it?** The OLS formula for the vertical intercept is:
$$\beta_0 = \bar{y} - \beta_1 \bar{x}$$

Substitute our numbers line-by-line:
$$\beta_0 = 5.0 - (1.7 \times 3.0)$$
$$1.7 \times 3.0 = 5.1$$
$$\beta_0 = 5.0 - 5.1 = -0.1$$

**Where did this formula/concept come from?** Setting the partial derivative of the Residual Sum of Squares with respect to $\beta_0$ to zero:
$$\frac{\partial}{\partial \beta_0} \sum_{i=1}^{n} \big(y_i - (\beta_0 + \beta_1 x_i)\big)^2 = 0 \implies \sum_{i=1}^{n} (y_i - \beta_0 - \beta_1 x_i) = 0$$
Dividing across by $n$ produces $\bar{y} - \beta_0 - \beta_1 \bar{x} = 0$, which rearranges directly to $\beta_0 = \bar{y} - \beta_1 \bar{x}$.
</div>

<div class="step-card">
<div class="step-badge">Step 8: Formulate the Regression Hypothesis Line and Make Predictions</div>

**What changed from Step 7?** We now have both coefficients: $\beta_0 = -0.1$ and $\beta_1 = 1.7$.

**What are we doing?** Writing the final predictive model $\hat{y} = \beta_0 + \beta_1 x$, and evaluating it for $x = 3.5$ and $x = 6.0$.

**Why are we doing this?** The goal of fitting a regression line is to predict outcomes for new, unseen inputs.

**How do we do it?**
1. State the final model:
$$\hat{y} = -0.1 + 1.7 x$$

2. **Prediction 1:** For a student studying $x = 3.5\text{ hours}$:
   $$\hat{y} = -0.1 + 1.7(3.5)$$
   $$1.7 \times 3.5 = 1.7 \times \frac{7}{2} = \frac{11.9}{2} = 5.95$$
   $$\hat{y} = -0.1 + 5.95 = 5.85\text{ points}$$

3. **Prediction 2:** For a student studying $x = 6.0\text{ hours}$ (Extrapolation):
   $$\hat{y} = -0.1 + 1.7(6.0)$$
   $$1.7 \times 6.0 = 10.2$$
   $$\hat{y} = -0.1 + 10.2 = 10.1\text{ points}$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary of Level 1 Results</div>

**What is the final answer?**
- Sample Means: $\bar{x} = 3.0$, $\bar{y} = 5.0$
- Sum of Cross-Product Deviations: $\sum(x_i - \bar{x})(y_i - \bar{y}) = 17.0$
- Sum of Squared Input Deviations: $\sum(x_i - \bar{x})^2 = 10.0$
- Slope ($\beta_1$): $1.7$
- Intercept ($\beta_0$): $-0.1$
- Best-fit line: $\hat{y} = -0.1 + 1.7x$
- Predicted score at $3.5\text{ hours}$: $5.85$
- Predicted score at $6.0\text{ hours}$: $10.1$

**Why does this answer make sense?** The slope of $+1.7$ means that for every $1$ additional hour a student studies, their exam score increases by an estimated $1.7$ points. The intercept of $-0.1$ indicates that if a student does zero studying ($x = 0$), their expected baseline score is roughly $0$.
</div>

</div>

::: quiz Checkpoint 1: Understanding OLS Coefficients
What would happen to the slope coefficient $\beta_1$ if every single student in the class scored exactly 5 points regardless of their study hours (i.e., $y = [5, 5, 5, 5, 5]$)?
(A) $\beta_1$ would equal 1.0 because study hours still vary.
(*B) $\beta_1$ would equal 0.0 because $(y_i - \bar{y})$ would be 0 for every student, making the numerator 0.
(C) $\beta_1$ would become undefined because the denominator becomes 0.
(D) $\beta_1$ would equal 5.0, matching the mean score.
::: explanation
If every $y_i = 5$, then $\bar{y} = 5$. The vertical deviation $(y_i - \bar{y}) = 5 - 5 = 0$ for every single point. The numerator $\sum(x_i - \bar{x})(y_i - \bar{y})$ becomes an exact sum of zeros ($0$). Therefore, $\beta_1 = 0 / 10 = 0$. A slope of zero means changes in $X$ have zero relationship with changes in $Y$ (a flat horizontal line).
:::

---

## Level 2: Centroid Property & Residual Zero-Sum Invariant Proof

### Problem 2.1: Mathematical Proof and Numerical Verification of the OLS Invariants

**Problem Statement:** In Ordinary Least Squares regression with an intercept term $\beta_0$, two universal properties always hold for any dataset:
1. **The Centroid Invariant:** The line of best fit strictly passes through the center-of-mass point $(\bar{x}, \bar{y})$.
2. **The Residual Zero-Sum Invariant:** The sum of the raw vertical errors (residuals $e_i = y_i - \hat{y}_i$) is strictly equal to $0$:
$$\sum_{i=1}^{n} e_i = 0$$

Using the Level 1 model ($\beta_0 = -0.1$, $\beta_1 = 1.7$, $\bar{x} = 3.0$, $\bar{y} = 5.0$):
1. Prove algebraically why the regression line must contain the point $(\bar{x}, \bar{y})$.
2. Calculate the fitted prediction $\hat{y}_i$ for each of the 5 students.
3. Compute each individual residual $e_i = y_i - \hat{y}_i$.
4. Sum all residuals explicitly to verify that $\sum e_i = 0$.
5. Provide the formal algebraic proof showing why $\sum e_i = 0$ is a direct mathematical consequence of minimizing squared errors.

::: callout-intuition Core Mental Model
Think of a playground seesaw.  
- The center pivot (fulcrum) is the **centroid** $(\bar{x}, \bar{y})$. If you place the pivot anywhere else, the seesaw will not balance!  
- The children sitting on the seesaw are your data points. The distance each child sits above the seesaw board is a positive residual ($+e_i$), and the distance below is a negative residual ($-e_i$).  
- For the seesaw to be in balance without tipping over, the positive forces pulling up must cancel out the negative forces pulling down. That is why the sum of the residuals **must equal zero**.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Algebraic Proof of the Centroid Invariant</div>

**What are we doing?** Proving that plugging $x = \bar{x}$ into the regression equation always outputs $\hat{y} = \bar{y}$.

**Why are we starting here?** This guarantees that the line is centered directly through the middle of the cloud of data points.

**How do we do it?**
1. Start with the regression hypothesis equation:
$$\hat{y} = \beta_0 + \beta_1 x$$

2. In Level 1 Step 7, we derived the formula for $\beta_0$:
$$\beta_0 = \bar{y} - \beta_1 \bar{x}$$

3. Substitute this definition of $\beta_0$ directly into the hypothesis equation:
$$\hat{y} = (\bar{y} - \beta_1 \bar{x}) + \beta_1 x$$

4. Now evaluate the prediction at $x = \bar{x}$:
$$\hat{y}(\bar{x}) = \bar{y} - \beta_1 \bar{x} + \beta_1 \bar{x}$$
The terms $-\beta_1 \bar{x}$ and $+\beta_1 \bar{x}$ cancel out:
$$\hat{y}(\bar{x}) = \bar{y} + 0 = \bar{y}$$

**Numerical Verification:**
$$\hat{y}(3.0) = -0.1 + 1.7(3.0) = -0.1 + 5.1 = 5.0$$
Since $\bar{y} = 5.0$, the line passes through $(3.0, 5.0)$.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Calculate Fitted Values (ŷ_i) for All 5 Observations</div>

**What changed from Step 1?** We proved the center point is on the line. Now we find the predicted score $\hat{y}_i$ for each individual student.

**What are we doing?** Plugging $x_1, x_2, x_3, x_4, x_5$ into $\hat{y} = -0.1 + 1.7x$.

**Why are we doing this?** A residual is defined as the gap between the actual observed score $y_i$ and the predicted score $\hat{y}_i$. We need all five $\hat{y}_i$ values first.

**How do we do it?**
- Student 1 ($x_1 = 1$):
  $$\hat{y}_1 = -0.1 + 1.7(1) = -0.1 + 1.7 = 1.6$$
- Student 2 ($x_2 = 2$):
  $$\hat{y}_2 = -0.1 + 1.7(2) = -0.1 + 3.4 = 3.3$$
- Student 3 ($x_3 = 3$):
  $$\hat{y}_3 = -0.1 + 1.7(3) = -0.1 + 5.1 = 5.0$$
- Student 4 ($x_4 = 4$):
  $$\hat{y}_4 = -0.1 + 1.7(4) = -0.1 + 6.8 = 6.7$$
- Student 5 ($x_5 = 5$):
  $$\hat{y}_5 = -0.1 + 1.7(5) = -0.1 + 8.5 = 8.4$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Compute Individual Residuals e_i = y_i - ŷ_i</div>

**What changed from Step 2?** We now have both the true observed scores $y_i$ and the model's fitted predictions $\hat{y}_i$.

**What are we doing?** Subtracting predicted score from actual score: $e_i = y_i - \hat{y}_i$.

**Why are we doing this?** Residuals represent the error of the model. Positive residuals mean the student did better than predicted; negative residuals mean the student scored worse than predicted.

**How do we do it?**
- Student 1:
  $$e_1 = y_1 - \hat{y}_1 = 2 - 1.6 = +0.4$$
- Student 2:
  $$e_2 = y_2 - \hat{y}_2 = 3 - 3.3 = -0.3$$
- Student 3:
  $$e_3 = y_3 - \hat{y}_3 = 5 - 5.0 = 0.0$$
- Student 4:
  $$e_4 = y_4 - \hat{y}_4 = 6 - 6.7 = -0.7$$
- Student 5:
  $$e_5 = y_5 - \hat{y}_5 = 9 - 8.4 = +0.6$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Numerically Sum the Residuals</div>

**What changed from Step 3?** We calculated all 5 residual values: $+0.4, -0.3, 0.0, -0.7, +0.6$.

**What are we doing?** Summing them up line-by-line: $\sum_{i=1}^{5} e_i$.

**Why are we doing this?** To verify whether our real-world calculations match the theoretical zero-sum invariant.

**How do we do it?** Group positive and negative terms:
$$\text{Positive errors: } (+0.4) + (+0.6) = +1.0$$
$$\text{Negative errors: } (-0.3) + (-0.7) = -1.0$$
$$\sum_{i=1}^{5} e_i = (+1.0) + (-1.0) + 0.0 = 0.0$$

The sum of the residuals is **identically 0.0**.

| Student $i$ | Actual Score $y_i$ | Fitted Score $\hat{y}_i$ | Residual $e_i = y_i - \hat{y}_i$ | Interpretation |
| :---: | :---: | :---: | :---: | :--- |
| 1 | 2 | 1.6 | $+0.4$ | Scored 0.4 points above line |
| 2 | 3 | 3.3 | $-0.3$ | Scored 0.3 points below line |
| 3 | 5 | 5.0 | $0.0$ | Sits directly on the line |
| 4 | 6 | 6.7 | $-0.7$ | Scored 0.7 points below line |
| 5 | 9 | 8.4 | $+0.6$ | Scored 0.6 points above line |
| **Sum** | **25.0** | **25.0** | **0.0** | **Perfect balance!** |
</div>

<div class="step-card">
<div class="step-badge">Step 5: General Algebraic Proof that Σ e_i = 0 for ANY Linear Regression with Intercept</div>

**What changed from Step 4?** We verified the property on our 5-point dataset. Now we prove this is always true for any dataset of any size $n$.

**What are we doing?** Showing why $\sum e_i = 0$ is guaranteed by the calculus of Ordinary Least Squares.

**Why are we doing this?** To build deep theoretical intuition: $\sum e_i = 0$ is not a coincidence; it is a mathematical consequence of including an intercept $\beta_0$.

**How do we do it?**
1. Define the loss function as the Residual Sum of Squares ($RSS$):
$$RSS(\beta_0, \beta_1) = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 = \sum_{i=1}^{n} \big(y_i - (\beta_0 + \beta_1 x_i)\big)^2$$

2. To find the optimal $\beta_0$, we take the partial derivative of $RSS$ with respect to $\beta_0$ and set it to $0$:
$$\frac{\partial RSS}{\partial \beta_0} = \sum_{i=1}^{n} 2 \cdot \big(y_i - (\beta_0 + \beta_1 x_i)\big) \cdot (-1) = 0$$

3. Divide both sides by $-2$:
$$\sum_{i=1}^{n} \big(y_i - (\beta_0 + \beta_1 x_i)\big) = 0$$

4. Notice the expression inside the summation:
$$y_i - (\beta_0 + \beta_1 x_i) = y_i - \hat{y}_i = e_i$$

5. Substitute $e_i$ back in:
$$\sum_{i=1}^{n} e_i = 0$$

**Where did this formula/concept come from?** First-order optimality condition (stationary point) in multivariate calculus.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary of Level 2 Invariants</div>

**What is the final answer?**
- The line passes through the centroid $(\bar{x}, \bar{y}) = (3.0, 5.0)$ because:
  $$\hat{y}(\bar{x}) = \bar{y} - \beta_1 \bar{x} + \beta_1 \bar{x} = \bar{y}$$
- The 5 fitted values are: $\hat{y} = [1.6, 3.3, 5.0, 6.7, 8.4]$.
- The 5 residuals are: $e = [+0.4, -0.3, 0.0, -0.7, +0.6]$.
- The sum of residuals $\sum e_i = 0$ because the first-order condition $\frac{\partial RSS}{\partial \beta_0} = 0$ requires the sum of errors to be zero.

**Why does this answer make sense?** If the sum of residuals were not zero (say, $+2.5$), it would mean our line consistently underestimated the scores. By simply raising the intercept $\beta_0$ up by $2.5 / 5 = 0.5$, we could reduce the overall squared error. OLS shifts the line until the positive and negative errors cancel each other out.
</div>

</div>

::: quiz Checkpoint 2: The Role of the Intercept in Residuals
A data scientist trains an OLS regression model without an intercept term (forcing the line to pass through the origin $(0,0)$, so $\hat{y} = \beta_1 x$). After computing the residuals, she notices that $\sum e_i = -4.2 \neq 0$. Did she make a calculation mistake?
(A) Yes, the sum of residuals must always equal zero in any linear regression model.
(*B) No, the sum of residuals is only guaranteed to equal zero when the model includes an intercept term ($\beta_0$).
(C) Yes, because the mean of $X$ and $Y$ must still equal zero.
(D) No, the sum of residuals only equals zero if the data points form a perfect line ($R^2 = 1$).
::: explanation
The proof that $\sum e_i = 0$ comes directly from the first-order condition $\frac{\partial RSS}{\partial \beta_0} = 0$. If you remove $\beta_0$ and force the model to be $\hat{y} = \beta_1 x$, there is no $\beta_0$ derivative! The only optimality condition is $\frac{\partial RSS}{\partial \beta_1} = 0$, which guarantees that $\sum e_i x_i = 0$ (residuals are orthogonal to $X$), but the raw residuals $\sum e_i$ generally will not sum to zero.
:::
