# Module 1 Practice Problems

Master these exact numerical types for the university exam.

## Type 1.1: Maximum Likelihood Estimation (MLE)

You flip a coin $n = 10$ times, and get $k = 7$ heads. Find the Maximum Likelihood Estimate for the probability of heads, $p$.

::: toggle Show Step-by-Step Solution
**Step 1: Write the Log-Likelihood equation**

\ell(p) = 7 \log(p) + 3 \log(1-p)

**Step 2: Take the derivative with respect to $p$**

The derivative of $?\log(x)$ is $1/x$. So, taking the derivative gives us: <br><br> \frac{d}{dp}\ell(p) = \frac{7}{p} - \frac{3}{1-p} <br><em>(Note: The minus sign comes from applying the chain rule to the $1-p$ term).</em>

**Step 3: Set to zero to find the peak of the hill**

\frac{7}{p} - \frac{3}{1-p} = 0

**Step 4: Solve for $p$ with basic algebra**

Move the negative term over: \frac{7}{p} = \frac{3}{1-p} <br> Cross multiply: 7(1-p) = 3p <br> Expand: 7 - 7p = 3p <br> Move $p$s to one side: 7 = 10p <br><br> <strong>Answer:</strong> p = \frac{7}{10} = 0.7

:::

---

## Type 1.2: Maximum A Posteriori (MAP)

You run an e-commerce website. A brand new product gets exactly 1 rating, and it's a 5-star positive review. Using MLE, the product has a perfect 100% score. Use MAP to find a safer estimate, assuming a Prior belief of 2 positive and 2 negative reviews.

::: toggle Show Step-by-Step Solution
**Step 1: Identify the Likelihood (Real Data)**

Actual data: $k = 1$ positive rating out of $n = 1$ total ratings.

**Step 2: Identify the Prior (Virtual Data)**

Virtual data: $?\alpha = 2$ positive ratings, $?\beta = 2$ negative ratings. Total virtual ratings = 4.

**Step 3: Combine them (The Posterior)**

Total positive = $1 \text{ (real)} + 2 \text{ (virtual)} = 3$.<br> Total ratings = $1 \text{ (real)} + 4 \text{ (virtual)} = 5$.

**Step 4: Calculate the MAP estimate**

\hat{p}_{MAP} = \frac{3}{5} = 0.60 <br><br><strong>Answer:</strong> The algorithm rates the product at 60% positive, protecting your store from ranking a product at #1 just because it got a single lucky review.

:::

---

## Type 1.3: Calculating the Cost (MSE)

You have a tiny dataset of 3 students. You try to predict their test scores out of 100. Calculate the Mean Squared Error (MSE) Cost for your model.<br><br><strong>True Scores ($y$):</strong> [80, 90, 70]<br><strong>Model's Predictions ($\hat{y}$):</strong> [75, 90, 78]

::: toggle Show Step-by-Step Solution
**Step 1: Calculate the individual errors ($y - \hat{y}$)**

Student 1: $80 - 75 = 5$<br>Student 2: $90 - 90 = 0$<br>Student 3: $70 - 78 = -8$

**Step 2: Square the errors**

Student 1: $5^2 = 25$<br>Student 2: $0^2 = 0$<br>Student 3: $(-8)^2 = 64$

**Step 3: Find the Average (Mean) to get the final Cost**

J = \frac{25 + 0 + 64}{3} = \frac{89}{3} \approx 29.67<br><br><strong>Result:</strong> Your model's total Cost is 29.67.

:::

---

## Type 1.4: Linear Regression (Ordinary Least Squares)

You have a tiny dataset of 3 houses. Size $x = [1, 2, 3]$. Price $y = [2, 4, 5]$. Find the perfect straight line ($w_1$ and $w_0$) using the Least Squares formula.

::: toggle Show Step-by-Step Solution
**Step 1: Find the Averages (Means)**

Average of $x$ ($\bar{x}$) = \frac{1+2+3}{3} = 2$<br> Average of $y$ ($\bar{y}$) = \frac{2+4+5}{3} = 3.67$

**Step 2: Calculate the Deviations for the Numerator**

Subtract the mean from each $x$ and $y$, then multiply them together: $(x_i - \bar{x}) \times (y_i - \bar{y})$.<br><br> House 1: $(1 - 2) \times (2 - 3.67) = (-1) \times (-1.67) = 1.67$<br> House 2: $(2 - 2) \times (4 - 3.67) = (0) \times (0.33) = 0$<br> House 3: $(3 - 2) \times (5 - 3.67) = (1) \times (1.33) = 1.33$<br><br> <em>Sum of Numerator:</em> $1.67 + 0 + 1.33 = 3.0$.

**Step 3: Calculate the Denominator**

Square the $x$ deviations: $(x_i - \bar{x})^2$.<br><br> House 1: $(-1)^2 = 1$<br> House 2: $(0)^2 = 0$<br> House 3: $(1)^2 = 1$<br><br> <em>Sum of Denominator:</em> $1 + 0 + 1 = 2.0$.

**Step 4: Find the Slope ($w_1$) and Intercept ($w_0$)**

w_1 = \frac{\text{Numerator}}{\text{Denominator}} = \frac{3.0}{2.0} = 1.5<br><br> w_0 = \bar{y} - w_1\bar{x} = 3.67 - (1.5 \times 2) = 0.67<br><br><strong>Answer:</strong> The best fit line is $\hat{y} = 0.67 + 1.5x$.

:::

---

## Type 1.5: Feature Scaling (Standardization)

You have a feature vector for a house: Size = 2000 sqft, Bedrooms = 3. Let's scale the 'Size' feature so it doesn't overwhelm the math. Assume you checked your whole dataset and found the average house size is 1500 sqft with a standard deviation of 500 sqft.

::: toggle Show Step-by-Step Solution
**Step 1: Identify Mean and Standard Deviation**

$\mu = 1500<br>$\sigma = 500

**Step 2: Apply the Z-Score Standardization formula**

x_{scaled} = \frac{x - \mu}{\sigma}

**Step 3: Calculate**

x_{scaled} = \frac{2000 - 1500}{500} = \frac{500}{500} = 1.0<br><br><strong>Result:</strong> The massive number '2000' is now represented simply as '1.0' (meaning it is exactly 1 standard deviation above average). The algorithm can now compare it safely against the smaller bedroom numbers.

:::

---

