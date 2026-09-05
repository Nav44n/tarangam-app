# Progressive Problems: Regression Metrics, ANOVA Decomposition & R² Score

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped square roots or fraction-to-decimal conversions, and full line-by-line arithmetic for every single error metric.

---

## Level 1: Full Error Metric Decomposition (MAE, MSE, RMSE, and $R^2$)

### Problem 1.1: Calculating and Comparing MAE, MSE, RMSE, and the Coefficient of Determination ($R^2$)

**Problem Statement:** A real-estate pricing algorithm is tested against $n = 4$ actual house sale prices (recorded in hundreds of thousands of dollars for clean arithmetic):

$$\text{Actual Ground Truth Targets: } y = [3.0, -0.5, 2.0, 7.0]$$
$$\text{Model Predicted Values: } \hat{y} = [2.5, 0.0, 2.0, 8.0]$$

Perform the following calculations step-by-step with zero skipped arithmetic:
1. Build an error table containing $y_i$, $\hat{y}_i$, the raw error $(y_i - \hat{y}_i)$, absolute error $|y_i - \hat{y}_i|$, and squared error $(y_i - \hat{y}_i)^2$.
2. Compute the **Mean Absolute Error (MAE)**.
3. Compute the **Mean Squared Error (MSE)**.
4. Compute the **Root Mean Squared Error (RMSE)**.
5. Explain the mathematical difference in how MAE and RMSE penalize large errors (outliers).
6. Calculate the sample mean of the actual targets ($\bar{y}$).
7. Compute the **Total Sum of Squares ($SST$ or $SS_{\text{tot}}$)**.
8. Compute the **Sum of Squared Residuals ($SSE$ or $SS_{\text{res}}$)**.
9. Compute the **Explained Sum of Squares ($SSR$ or $SS_{\text{reg}}$)**.
10. Compute the **$R^2$ Score (Coefficient of Determination)** using $R^2 = 1 - \frac{SSE}{SST}$ and interpret the percentage of variance explained by the model.

::: callout-intuition Core Mental Model
Imagine an archery contest where targets represent actual house prices ($y$), and your arrows represent your model's predictions ($\hat{y}$):
- **Raw Error ($y_i - \hat{y}_i$):** How many inches your arrow landed to the left ($-$) or right ($+$) of the bullseye. If you simply average these raw errors, positive and negative misses cancel each other out, making you look like a perfect marksman even if every shot completely missed the target!
- **MAE:** You take a ruler and measure the absolute tape-measure distance between each arrow and the bullseye, treating all inches equally. An arrow off by 4 inches is penalized exactly 4 times as much as an arrow off by 1 inch.
- **MSE / RMSE:** You square each distance before averaging. An arrow off by 4 inches gets a penalty of $4^2 = 16$, which is **16 times** worse than an arrow off by 1 inch! RMSE severely punishes wild misses.
- **$R^2$ Score:** A comparison against the "laziest archer in the world." The lazy archer never even looks at the house features; they close their eyes and guess the overall average price ($\bar{y}$) for every single house. $R^2$ tells you: *"What percentage of the lazy archer's errors did your smart model eliminate?"*
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Construct the Individual Error and Residual Table</summary>

**What are we doing?** Computing the raw prediction errors, their absolute values, and their squared values for each of the $n = 4$ observations.

**Why are we starting here?** Every single regression evaluation metric (MAE, MSE, RMSE, $R^2$) is constructed directly from these fundamental error columns.

**How do we do it?** For each observation $i$:
1. Raw error / residual: $e_i = y_i - \hat{y}_i$
2. Absolute error: $|e_i| = |y_i - \hat{y}_i|$
3. Squared error: $e_i^2 = (y_i - \hat{y}_i)^2$

Compute row-by-row:
- **Sample 1:** $y_1 = 3.0,\quad \hat{y}_1 = 2.5$
  $$e_1 = 3.0 - 2.5 = +0.5$$
  $$|e_1| = |+0.5| = 0.5$$
  $$e_1^2 = (0.5)^2 = 0.25$$

- **Sample 2:** $y_2 = -0.5,\quad \hat{y}_2 = 0.0$
  $$e_2 = -0.5 - 0.0 = -0.5$$
  $$|e_2| = |-0.5| = 0.5$$
  $$e_2^2 = (-0.5)^2 = 0.25$$

- **Sample 3:** $y_3 = 2.0,\quad \hat{y}_3 = 2.0$
  $$e_3 = 2.0 - 2.0 = 0.0$$
  $$|e_3| = |0.0| = 0.0$$
  $$e_3^2 = (0.0)^2 = 0.00$$

- **Sample 4:** $y_4 = 7.0,\quad \hat{y}_4 = 8.0$
  $$e_4 = 7.0 - 8.0 = -1.0$$
  $$|e_4| = |-1.0| = 1.0$$
  $$e_4^2 = (-1.0)^2 = 1.00$$

Let us assemble these calculations into a clean working table:

| $i$ | Actual $y_i$ | Predicted $\hat{y}_i$ | Raw Error $(y_i - \hat{y}_i)$ | Absolute Error $\|y_i - \hat{y}_i\|$ | Squared Error $(y_i - \hat{y}_i)^2$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | $3.0$ | $2.5$ | $+0.5$ | $0.5$ | $0.25$ |
| 2 | $-0.5$ | $0.0$ | $-0.5$ | $0.5$ | $0.25$ |
| 3 | $2.0$ | $2.0$ | $0.0$ | $0.0$ | $0.00$ |
| 4 | $7.0$ | $8.0$ | $-1.0$ | $1.0$ | $1.00$ |
| **Sum ($\sum$)** | **11.5** | **12.5** | **-1.0** | **2.0** | **1.50** |

**Where did this formula/concept come from?** The definition of a residual: the vertical distance between the observed data point and the model's fitted prediction surface.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Calculate Mean Absolute Error (MAE)</summary>

**What changed from Step 1?** We have the sum of absolute errors ($\sum |y_i - \hat{y}_i| = 2.0$). Now we compute their average across the $n = 4$ observations.

**What are we doing?** Evaluating $\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$.

**Why are we doing this?** MAE gives an intuitive, easily interpretable answer in the exact same physical units as the target variable ($Y$). It answers: *"On average, by how many units is our prediction off?"*

**How do we do it?**
1. Substitute the sum of absolute errors into the formula:
   $$\text{MAE} = \frac{1}{4} \sum_{i=1}^{4} |y_i - \hat{y}_i|$$
2. Insert our values:
   $$\text{MAE} = \frac{0.5 + 0.5 + 0.0 + 1.0}{4} = \frac{2.0}{4} = \mathbf{0.50}$$

**Interpretation:** On average, the model's predictions miss the true house prices by $0.50$ units ($50{,}000$ dollars).

**Where did this formula/concept come from?** $L_1$-norm loss formulation in statistical estimation.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Calculate Mean Squared Error (MSE)</summary>

**What changed from Step 2?** Instead of averaging absolute values, we now average the squared errors from Step 1.

**What are we doing?** Evaluating $\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$.

**Why are we doing this?** Squaring errors eliminates negative signs and makes the loss function differentiable everywhere (unlike the absolute value function, which has a sharp, non-differentiable corner at 0).

**How do we do it?**
1. Substitute the sum of squared errors into the formula:
   $$\text{MSE} = \frac{1}{4} \sum_{i=1}^{4} (y_i - \hat{y}_i)^2$$
2. Insert our values:
   $$\text{MSE} = \frac{0.25 + 0.25 + 0.00 + 1.00}{4} = \frac{1.50}{4} = \frac{3}{8} = \mathbf{0.375}$$

**Interpretation:** The Mean Squared Error is $0.375\text{ units}^2$. Notice the units are "squared units," which are not directly comparable to raw dollars.

**Where did this formula/concept come from?** $L_2$-norm loss formulation, foundational to Gauss's classical least squares regression.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Calculate Root Mean Squared Error (RMSE)</summary>

**What changed from Step 3?** We have $\text{MSE} = 0.375\text{ units}^2$. Now we convert the metric back into the original target units by taking the square root.

**What are we doing?** Evaluating $\text{RMSE} = \sqrt{\text{MSE}}$.

**Why are we doing this?** While MSE is algebraically convenient for gradient descent, humans cannot easily interpret "squared dollars." Taking the square root brings the scale back to standard dollars while retaining the outlier-punishing nature of the squared penalty.

**How do we do it?**
1. State the formula:
   $$\text{RMSE} = \sqrt{\text{MSE}} = \sqrt{0.375}$$
2. Calculate the square root step-by-step:
   $$\sqrt{0.375} = \sqrt{\frac{375}{1{,}000}} = \sqrt{\frac{3}{8}} = \frac{\sqrt{3}}{\sqrt{8}} = \frac{\sqrt{3}}{2\sqrt{2}} = \frac{\sqrt{6}}{4}$$
   Using standard decimal approximations ($\sqrt{6} \approx 2.4494897$):
   $$\text{RMSE} = \frac{2.4494897}{4} \approx \mathbf{0.6124}$$

**Where did this formula/concept come from?** Standard deviation and Euclidean ($L_2$) distance in vector spaces.
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Compare MAE vs. RMSE (Outlier Penalty Dynamics)</summary>

**What changed from Step 4?** We now have two unit-aligned metrics: $\text{MAE} = 0.50$ and $\text{RMSE} \approx 0.6124$. Notice that $\text{RMSE} > \text{MAE}$.

**What are we doing?** Explaining why RMSE is strictly greater than or equal to MAE, and analyzing how each metric responds to an extreme outlier.

**Why are we doing this?** Beginners often wonder why both metrics exist and which one to report to stakeholders.

**How do we do it?**
1. **Mathematical Inequality:**
   By Jensen's Inequality, for any set of numbers:
   $$\text{RMSE} \ge \text{MAE}$$
   They are equal *if and only if* all individual errors have the exact same absolute magnitude (e.g., if every single prediction missed by exactly $0.5$). The larger the spread of errors, the further RMSE pulls away above MAE.

2. **The Outlier Stress-Test:**
   Suppose we add a 5th house where the model makes a massive prediction mistake of $e_5 = 10\text{ units}$:
   - **MAE impact:** Adds $|10| = 10$ to the sum of errors. The error is penalized **linearly**:
     $$\Delta \text{Sum}_{\text{MAE}} = 10$$
   - **MSE / RMSE impact:** Adds $(10)^2 = 100$ to the sum of squared errors. The error is penalized **quadratically**:
     $$\Delta \text{Sum}_{\text{MSE}} = 100$$

**Rule of Thumb:**
- Use **MAE** when you want a robust metric that is not overly influenced by rare, extreme anomalies.
- Use **RMSE** when large mistakes are catastrophic (e.g., medical dosage prediction, flight autopilot control) and must be heavily penalized.
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Compute Target Mean (ȳ) and Total Sum of Squares (SST)</summary>

**What changed from Step 5?** We have evaluated absolute model error. Now we prepare to compute $R^2$, which requires measuring the baseline variation of the raw target data itself.

**What are we doing?** Calculating the sample mean $\bar{y}$ and the Total Sum of Squares ($SST$).

**Why are we doing this?** $SST$ represents the total variance in the data before any predictive model is applied. It measures the errors made by a naive "dummy model" that simply predicts the overall average score for every single home.

**How do we do it?**
1. Compute target mean $\bar{y}$:
   $$\bar{y} = \frac{1}{n} \sum_{i=1}^{4} y_i = \frac{3.0 + (-0.5) + 2.0 + 7.0}{4} = \frac{11.5}{4} = \mathbf{2.875}$$

2. Compute deviations from the mean $(y_i - \bar{y})$:
   - For $y_1 = 3.0$: $3.0 - 2.875 = +0.125 \implies (0.125)^2 = 0.015625$
   - For $y_2 = -0.5$: $-0.5 - 2.875 = -3.375 \implies (-3.375)^2 = 11.390625$
   - For $y_3 = 2.0$: $2.0 - 2.875 = -0.875 \implies (-0.875)^2 = 0.765625$
   - For $y_4 = 7.0$: $7.0 - 2.875 = +4.125 \implies (4.125)^2 = 17.015625$

3. Sum the squared deviations to find $SST$:
   $$SST = \sum_{i=1}^{4} (y_i - \bar{y})^2 = 0.015625 + 11.390625 + 0.765625 + 17.015625 = \mathbf{29.1875}$$

**Where did this formula/concept come from?** Analysis of Variance (ANOVA). $SST$ is proportional to the sample variance of the target variable: $\text{Var}(Y) = \frac{SST}{n-1}$.
</details>

<details class="step-card">
<summary class="step-badge">Step 7: Identify Sum of Squared Errors (SSE)</summary>

**What changed from Step 6?** We have $SST = 29.1875$. Now we compute the unmodelled error of our smart model ($SSE$).

**What are we doing?** Finding the Sum of Squared Errors: $SSE = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$.

**Why are we doing this?** $SSE$ measures the variation that our model *failed* to explain (the remaining noise).

**How do we do it?** We already summed the squared errors in the last column of Step 1:
$$SSE = \sum_{i=1}^{4} (y_i - \hat{y}_i)^2 = 0.25 + 0.25 + 0.00 + 1.00 = \mathbf{1.50}$$

Notice the relationship between MSE and SSE:
$$\text{MSE} = \frac{SSE}{n} \implies SSE = n \times \text{MSE} = 4 \times 0.375 = 1.50$$
</details>

<details class="step-card">
<summary class="step-badge">Step 8: Compute Explained Sum of Squares (SSR)</summary>

**What changed from Step 7?** We have total variation $SST = 29.1875$ and unexplained variation $SSE = 1.50$. Now we compute the variation explained by the model ($SSR$).

**What are we doing?** Evaluating $SSR = \sum_{i=1}^{n} (\hat{y}_i - \bar{y})^2$ and understanding the ANOVA decomposition.

**Why are we doing this?** In linear regression models fitted via OLS with an intercept, total variation splits cleanly into two pieces:
$$\text{Total Variation } (SST) = \text{Explained Variation } (SSR) + \text{Unexplained Variation } (SSE)$$

**How do we do it?**
1. Compute deviations of predictions from the target mean $(\hat{y}_i - \bar{y})$ where $\bar{y} = 2.875$:
   - For $\hat{y}_1 = 2.5$: $2.5 - 2.875 = -0.375 \implies (-0.375)^2 = 0.140625$
   - For $\hat{y}_2 = 0.0$: $0.0 - 2.875 = -2.875 \implies (-2.875)^2 = 8.265625$
   - For $\hat{y}_3 = 2.0$: $2.0 - 2.875 = -0.875 \implies (-0.875)^2 = 0.765625$
   - For $\hat{y}_4 = 8.0$: $8.0 - 2.875 = +5.125 \implies (5.125)^2 = 26.265625$

2. Sum the squared terms:
   $$SSR = \sum_{i=1}^{4} (\hat{y}_i - \bar{y})^2 = 0.140625 + 8.265625 + 0.765625 + 26.265625 = \mathbf{35.4375}$$

*(Note: The Pythagorean identity $SST = SSR + SSE$ strictly holds if predictions come from an OLS-fitted line with an intercept where $\sum e_i = 0$ and $\sum e_i \hat{y}_i = 0$. For general machine learning models—such as Neural Networks, Random Forests, or arbitrary test values—the universal definition of $R^2$ is strictly $1 - \frac{SSE}{SST}$).*
</details>

<details class="step-card">
<summary class="step-badge">Step 9: Compute the R² Score and Interpret the Result</summary>

**What changed from Step 8?** We have $SST = 29.1875$ and $SSE = 1.50$. Now we compute the formal $R^2$ score.

**What are we doing?** Calculating $R^2 = 1 - \frac{SSE}{SST}$.

**Why are we doing this?** $R^2$ standardizes performance onto a scale where $1.0$ represents a perfect predictor, eliminating the scale dependence of raw MSE.

**How do we do it?**
1. State the formula:
   $$R^2 = 1 - \frac{SSE}{SST}$$
2. Substitute our numbers:
   $$\frac{SSE}{SST} = \frac{1.50}{29.1875} = \frac{1.50}{\frac{467}{16}} = \frac{24}{467} \approx 0.05139$$
3. Subtract from 1:
   $$R^2 = 1.0 - 0.05139 = \mathbf{0.94861} \approx 94.86\%$$

**Interpretation:** The model achieves an $R^2$ score of approximately **$0.9486$**. This means that the model's predictions successfully explain **$94.86\%$** of the total variance in home prices, eliminating nearly $95\%$ of the error that a naive mean-predictor would have made.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Complete Metric Summary Table</summary>

**What is the final answer?** The full suite of regression evaluation metrics for this dataset:

| Evaluation Metric | Mathematical Formula | Numerical Value | Units |
| :--- | :---: | :---: | :--- |
| **Mean Absolute Error (MAE)** | $\frac{1}{n}\sum \|y_i - \hat{y}_i\|$ | **$0.5000$** | Original Units (Dollars) |
| **Mean Squared Error (MSE)** | $\frac{1}{n}\sum (y_i - \hat{y}_i)^2$ | **$0.3750$** | Squared Units ($\text{Dollars}^2$) |
| **Root Mean Squared Error (RMSE)** | $\sqrt{\text{MSE}}$ | **$0.6124$** | Original Units (Dollars) |
| **Total Sum of Squares (SST)** | $\sum (y_i - \bar{y})^2$ | **$29.1875$** | Squared Units |
| **Residual Sum of Squares (SSE)** | $\sum (y_i - \hat{y}_i)^2$ | **$1.5000$** | Squared Units |
| **$R^2$ Score (Variance Explained)** | $1 - \frac{SSE}{SST}$ | **$0.9486$** | Dimensionless ($94.86\%$) |

**Why does this answer make sense?** The true values range from $-0.5$ to $7.0$ (a total spread of $7.5$ units). The model's largest single error is only $1.0$ unit, and two of its predictions miss by just $0.5$ units (with one exact hit). Because the errors are small compared to the overall data spread ($SST = 29.1875$), the $R^2$ score is very close to $1.0$.
</details>

</div>

::: quiz Checkpoint 1: MAE vs. RMSE Outlier Sensitivity
A housing price model is evaluated on two different neighborhoods with $n = 2$ houses each:
- Neighborhood 1 errors: $e = [3, 3]$
- Neighborhood 2 errors: $e = [0, 6]$
Which statement correctly describes how MAE and RMSE evaluate these two neighborhoods?
(A) Both Neighborhood 1 and Neighborhood 2 will have the exact same MAE and the exact same RMSE.
(B) Neighborhood 1 has a higher MAE than Neighborhood 2, but their RMSE values are identical.
(*C) Both neighborhoods have the exact same MAE ($3.0$), but Neighborhood 2 has a significantly higher RMSE ($4.24$ vs. $3.0$) because RMSE heavily penalizes the single large mistake of $6$.
(D) RMSE is always smaller than MAE when errors exceed 1.0.
::: explanation
For Neighborhood 1: $\text{MAE} = \frac{3+3}{2} = 3.0$. $\text{MSE} = \frac{3^2 + 3^2}{2} = \frac{18}{2} = 9.0 \implies \text{RMSE} = \sqrt{9} = 3.0$.  
For Neighborhood 2: $\text{MAE} = \frac{0+6}{2} = 3.0$. $\text{MSE} = \frac{0^2 + 6^2}{2} = \frac{36}{2} = 18.0 \implies \text{RMSE} = \sqrt{18} \approx 4.24$.  
Even though the average error magnitude is identical ($\text{MAE} = 3.0$ for both), RMSE penalizes the variance of errors, highlighting that a single $6$-unit miss is far more disruptive than two consistent $3$-unit misses.
:::

---

## Level 2: The Negative $R^2$ Phenomenon & The Baseline Predictor

### Problem 2.1: Constructing and Proving a Model with $R^2 < 0$

**Problem Statement:** Many introductory students believe that because $R^2$ is called "the square of $R$," it can never be negative (i.e., $R^2 \ge 0$).  
1. Prove that for a simple horizontal baseline model that always predicts the sample mean ($\hat{y}_i = \bar{y}$ for all $i$), the $R^2$ score is identically $0.0$.
2. Construct a concrete dataset of $n = 3$ actual values:
   $$y = [10.0, 20.0, 30.0]$$
   and evaluate a flawed prediction model that outputs:
   $$\hat{y} = [50.0, 60.0, 70.0]$$
3. Compute $SST$, $SSE$, and the resulting $R^2$ score for this flawed model.
4. Show algebraically why any model whose Mean Squared Error is worse than the variance of the target variable produces $R^2 < 0$.

::: callout-intuition Core Mental Model
Think of $R^2$ as an efficiency rating for a weather forecaster compared to a broken analog thermometer stuck at room temperature:
- **$R^2 = 1.0$ (100%):** You predict the temperature tomorrow to the exact decimal degree every single day.
- **$R^2 = 0.0$ (0%):** You are completely lazy. You don't read weather maps or look outside; you simply guess the annual city average ($68^\circ\text{F}$) every single day. Your predictions have zero predictive power, but at least you aren't doing worse than the baseline average.
- **$R^2 < 0$ (Negative):** Tomorrow is a mild spring day ($65^\circ\text{F}$), but your model screams that it will be a blizzard at $-40^\circ\text{F}$! You are doing **worse than the lazy broken thermometer**. A negative $R^2$ means: *"Throw this model in the trash; you would get more accurate predictions by closing your eyes and guessing the historical average!"*
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Prove that the Baseline Mean Model Yields R² = 0.0</summary>

**What are we doing?** Evaluating the performance of the trivial baseline model $\hat{y}_i = \bar{y}$.

**Why are we starting here?** To establish the mathematical anchor point of $R^2 = 0$.

**How do we do it?**
1. By definition, the Sum of Squared Errors is:
   $$SSE = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$
2. If our model predicts the sample mean for every sample ($\hat{y}_i = \bar{y}$), substitute $\bar{y}$ for $\hat{y}_i$:
   $$SSE_{\text{baseline}} = \sum_{i=1}^{n} (y_i - \bar{y})^2$$
3. Look at the definition of the Total Sum of Squares ($SST$):
   $$SST = \sum_{i=1}^{n} (y_i - \bar{y})^2$$
   Notice that $SSE_{\text{baseline}}$ is **identical** to $SST$:
   $$SSE_{\text{baseline}} = SST$$
4. Plug this into the $R^2$ equation:
   $$R^2 = 1 - \frac{SSE}{SST} = 1 - \frac{SST}{SST} = 1 - 1 = \mathbf{0.0}$$

**Conclusion:** A model that simply outputs the mean of the training data has an $R^2$ of exactly $0.0$. It explains $0\%$ of the target variance beyond the baseline average.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Calculate SST for the Flawed Scenario Dataset</summary>

**What changed from Step 1?** We established that the baseline model gives $R^2 = 0$. Now we evaluate our concrete test dataset:
$$y = [10.0, 20.0, 30.0]$$

**What are we doing?** Computing the sample mean $\bar{y}$ and the Total Sum of Squares ($SST$).

**Why are we doing this?** We need the baseline variance of this 3-point dataset to serve as the denominator in the $R^2$ formula.

**How do we do it?**
1. Compute target mean $\bar{y}$:
   $$\bar{y} = \frac{10.0 + 20.0 + 30.0}{3} = \frac{60.0}{3} = 20.0$$

2. Compute squared deviations from the mean $(y_i - \bar{y})^2$:
   - For $y_1 = 10.0$: $(10.0 - 20.0)^2 = (-10.0)^2 = 100.0$
   - For $y_2 = 20.0$: $(20.0 - 20.0)^2 = (0.0)^2 = 0.0$
   - For $y_3 = 30.0$: $(30.0 - 20.0)^2 = (+10.0)^2 = 100.0$

3. Sum the squared deviations:
   $$SST = 100.0 + 0.0 + 100.0 = \mathbf{200.0}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Calculate SSE for Flawed Model Predictions</summary>

**What changed from Step 2?** We know $SST = 200.0$. Now we evaluate the errors of the flawed model:
$$\hat{y} = [50.0, 60.0, 70.0]$$

**What are we doing?** Computing the Sum of Squared Errors: $SSE = \sum_{i=1}^{3} (y_i - \hat{y}_i)^2$.

**Why are we doing this?** To quantify how far off this model's predictions are from reality.

**How do we do it?** Calculate individual errors:
- For Sample 1: $y_1 = 10.0,\quad \hat{y}_1 = 50.0$
  $$e_1 = 10.0 - 50.0 = -40.0 \implies (-40.0)^2 = 1{,}600.0$$
- For Sample 2: $y_2 = 20.0,\quad \hat{y}_2 = 60.0$
  $$e_2 = 20.0 - 60.0 = -40.0 \implies (-40.0)^2 = 1{,}600.0$$
- For Sample 3: $y_3 = 30.0,\quad \hat{y}_3 = 70.0$
  $$e_3 = 30.0 - 70.0 = -40.0 \implies (-40.0)^2 = 1{,}600.0$$

Sum the squared errors:
$$SSE = 1{,}600.0 + 1{,}600.0 + 1{,}600.0 = \mathbf{4{,}800.0}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Compute the Resulting R² Score</summary>

**What changed from Step 3?** We have $SST = 200.0$ and $SSE = 4{,}800.0$. Notice that $SSE > SST$!

**What are we doing?** Calculating $R^2 = 1 - \frac{SSE}{SST}$.

**Why are we doing this?** To demonstrate numerically that $R^2$ can be strongly negative.

**How do we do it?**
1. Substitute $SSE$ and $SST$ into the equation:
   $$R^2 = 1 - \frac{4{,}800.0}{200.0}$$
2. Divide the fractions:
   $$\frac{4{,}800.0}{200.0} = 24.0$$
3. Perform the subtraction:
   $$R^2 = 1 - 24.0 = \mathbf{-23.0}$$

**Interpretation:** An $R^2$ of **$-23.0$** means that the model's squared error is **24 times larger** than the error you would get by simply predicting the mean $\bar{y} = 20.0$ for every single sample!
</details>

<details class="step-card">
<summary class="step-badge">Step 5: General Algebraic Condition for Negative R²</summary>

**What changed from Step 4?** We proved it with numbers. Now we state the universal algebraic rule that dictates when $R^2 < 0$.

**What are we doing?** Deriving the condition under which $R^2$ drops below zero.

**Why are we doing this?** To eliminate the misconception that $R^2$ is literally the square of Pearson's correlation coefficient $r$.

**How do we do it?**
1. Set up the inequality:
   $$R^2 < 0 \iff 1 - \frac{SSE}{SST} < 0$$
2. Add $\frac{SSE}{SST}$ to both sides:
   $$\frac{SSE}{SST} > 1 \iff \mathbf{SSE > SST}$$
3. Divide both numerator and denominator by $n$:
   $$\frac{SSE / n}{SST / n} > 1 \iff \frac{\text{MSE}}{\text{Var}(Y)} > 1 \iff \mathbf{\text{MSE} > \text{Var}(Y)}$$

**The Crucial Distinction:**
- In **simple linear regression on training data** fitted via OLS with an intercept, $R^2$ is mathematically guaranteed to equal the square of Pearson's correlation ($r^2$), so it is constrained to the interval $[0, 1]$.
- In **all other contexts**—including evaluating on a test set, using non-linear models (Decision Trees, Neural Networks), or models without an intercept—$R^2$ is defined by $1 - \frac{SSE}{SST}$ and has the range:
$$(-\infty, 1.0]$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Summary of the R² Spectrum</summary>

**What is the final answer?** The universal scale of the $R^2$ metric across all machine learning models:

| $R^2$ Value | Meaning | Model Quality |
| :---: | :--- | :--- |
| **$1.0$** | $SSE = 0$. Perfect predictions on every sample. | Ideal theoretical maximum |
| **$0.0 < R^2 < 1.0$** | Model performs better than predicting the mean $\bar{y}$. | Functional predictive model |
| **$0.0$** | $SSE = SST$. Model performs identically to predicting $\bar{y}$. | Zero added predictive value |
| **$< 0.0$** | $SSE > SST$. Model performs **worse** than predicting $\bar{y}$. | Flawed / completely untrustworthy |

**Why does this answer make sense?** The baseline benchmark for any regression problem is predicting the constant average $\bar{y}$. If a complex machine learning model makes mistakes larger than the natural spread of the data itself ($SSE > SST$), it has added noise rather than extracting signal, producing a negative score.
</details>

</div>

::: quiz Checkpoint 2: The Meaning of Negative R² on Test Data
A machine learning engineer trains a high-capacity polynomial regression model. On the training set, the model achieves $R_{\text{train}}^2 = 0.99$. However, on the unseen test set, the model yields $R_{\text{test}}^2 = -1.45$. What does this result indicate?
(A) The test set was corrupted because $R^2$ can never be negative under any circumstances.
(*B) The model has severely overfitted to the training data; its test-set predictions are so erratic that predicting the simple training mean would yield smaller overall error.
(C) The model has high bias and needs more polynomial features to capture the true underlying pattern.
(D) The learning rate was too small during gradient descent optimization.
::: explanation
An $R^2$ of $0.99$ on training data combined with a negative $R^2$ on test data is the textbook hallmark of severe **overfitting** (high variance). The model memorized the training noise so tightly that when faced with new test inputs, its predictions swing wildly, generating a Residual Sum of Squares ($SSE$) that is $2.45\text{ times}$ larger than the Total Sum of Squares ($SST$) of the test set.
:::
