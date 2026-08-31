# Module 3 Practice Problems

Master these exact numerical types for the university exam.

## Type 3.1: Regression Evaluation (RMSE)

You are evaluating a regression model. The true house prices (in $100k) are $y = [3, -0.5, 2, 7]$ and the model predicts $\hat{y} = [2.5, 0.0, 2, 8]$. Calculate the Root Mean Squared Error (RMSE).

::: toggle Show Step-by-Step Solution
**Step 1: Calculate the Error (Residuals)**

$e_i = y_i - \hat{y}_i$
House 1: $3 - 2.5 = 0.5$
House 2: $-0.5 - 0.0 = -0.5$
House 3: $2 - 2 = 0$
House 4: $7 - 8 = -1.0$

**Step 2: Square the Errors**

$e_i^2$
House 1: $0.5^2 = 0.25$
House 2: $(-0.5)^2 = 0.25$
House 3: $0^2 = 0$
House 4: $(-1.0)^2 = 1.0$

**Step 3: Calculate the Mean (MSE)**

MSE = \frac{0.25 + 0.25 + 0 + 1.0}{4} = \frac{1.5}{4} = 0.375

**Step 4: Take the Square Root (RMSE)**

RMSE = \sqrt{0.375} \approx 0.612

**Result:** The RMSE is 0.612 (or $61,200).

:::

---

## Type 3.2: Perceptron Weight Update

A perceptron has weights $w_1 = 0.5, w_2 = -0.5$ and bias $b = 0$. An input vector $x = [1, 2]$ belongs to class $y = 1$ (positive). The learning rate $\eta = 0.1$. First, find if the perceptron classifies it correctly (using a step function where output is 1 if sum $\ge 0$, else -1). If incorrect, update the weights.

::: toggle Show Step-by-Step Solution
**Step 1: Calculate the weighted sum**

z = (w_1 \times x_1) + (w_2 \times x_2) + b
z = (0.5 \times 1) + (-0.5 \times 2) + 0
z = 0.5 - 1.0 = -0.5

**Step 2: Apply the activation function**

Since $z = -0.5 < 0$, the predicted output $\hat{y} = -1$.
The true target is $y = 1$. The prediction is incorrect.

**Step 3: Apply the update rule**

Formula: $w_i \leftarrow w_i + \eta (y - \hat{y}) x_i$
Error term: $(y - \hat{y}) = 1 - (-1) = 2$

Update $w_1$:
w_1 = 0.5 + 0.1 \times 2 \times 1 = 0.5 + 0.2 = 0.7

Update $w_2$:
w_2 = -0.5 + 0.1 \times 2 \times 2 = -0.5 + 0.4 = -0.1

Update $b$:
b = 0 + 0.1 \times 2 \times 1 = 0.2

:::

---

