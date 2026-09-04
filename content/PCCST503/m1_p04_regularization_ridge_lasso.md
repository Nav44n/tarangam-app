# Progressive Problems: Bias-Variance Tradeoff, Ridge (L2) & Lasso (L1) Regularization

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped algebra, and complete line-by-line derivations for both shrinkage operators.

---

## Level 1: Shrinkage Math for Ridge (L2) and Lasso (L1) on an Orthonormal Feature

### Problem 1.1: Calculating Weight Penalties for a Single Feature

**Problem Statement:** You have trained a simple linear regression model on a specialized (orthonormal) dataset with just one feature weight, $w$. Without any regularization, the Ordinary Least Squares (OLS) algorithm found the perfect weight to fit the training data: $w_{\text{ols}} = 4.0$.

However, your model is overfitting! To fix this, you must apply regularization (a mathematical penalty for having large weights).

1. Formulate and solve the **Ridge (L2)** cost function to find the new optimal weight for $\lambda = 0, 1, 3, 9$.
2. Formulate and solve the **Lasso (L1)** cost function to find the new optimal weight for $\lambda = 1, 2, 4, 6$.
3. Compare how Ridge gently shrinks weights versus how Lasso aggressively forces them to exactly $0.0$.

::: callout-intuition Core Mental Model
Imagine you are packing luggage for a flight. The airline wants to discourage heavy bags to save fuel.
- **Unregularized (OLS):** The airline has no baggage fees. You pack everything you own, resulting in a heavy $4.0\text{ kg}$ bag.
- **Ridge (L2) Regularization:** The airline charges a **strict weight fee based on the SQUARE of your bag's weight**. A $4\text{ kg}$ bag costs $\$16$, but a $1\text{ kg}$ bag costs only $\$1$. Because heavy items are punished exponentially, you shrink everything down—swapping heavy boots for light sandals. Your bag gets lighter and lighter, but you never completely empty it.
- **Lasso (L1) Regularization:** The airline charges a **flat tax per bag**, regardless of its size. If an item isn't valuable enough to justify paying the flat tax, you don't just shrink it—you throw the entire item in the trash! Lasso acts as a ruthless filter, forcing useless items to exactly $0.0\text{ kg}$.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Understand the Baseline OLS Cost Function</div>

**What are we doing?** We are writing down the mathematical equation for the model's error *before* we add any penalties.

**Why are we starting here?** To understand how a penalty changes the weight, we first need to see what the unpenalized error looks like.

**How do we do it?** For a single, perfectly scaled feature, the Mean Squared Error (MSE) forms a simple U-shaped curve (a parabola) centered at the optimal unpenalized weight, $w_{\text{ols}} = 4.0$.

We write this unpenalized cost function as:
$$J_{\text{ols}}(w) = \frac{1}{2}(w - w_{\text{ols}})^2$$

Substitute $w_{\text{ols}} = 4.0$:
$$J_{\text{ols}}(w) = \frac{1}{2}(w - 4.0)^2$$

If we pick $w = 4.0$, the cost is $\frac{1}{2}(4.0 - 4.0)^2 = 0$. The model has zero error!

**Where did this formula/concept come from?** The standard Mean Squared Error formula. The $\frac{1}{2}$ is a standard mathematical convention used in machine learning so that when we take a derivative (which brings down a multiplier of $2$), the fractions cancel out cleanly.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Formulate the Ridge (L2) Cost Function</div>

**What changed from Step 1?** We are now modifying the error equation by adding the Ridge (L2) penalty.

**What are we doing?** We are adding a term that mathematically punishes the model if the weight $w$ gets too large.

**How do we do it?** The Ridge penalty is the squared weight multiplied by a tuning parameter $\lambda$ (lambda), divided by 2:
$$\text{L2 Penalty} = \frac{\lambda}{2}w^2$$

We add this directly to our baseline cost function from Step 1:
$$J_{\text{ridge}}(w) = \frac{1}{2}(w - 4.0)^2 + \frac{\lambda}{2}w^2$$

- If $\lambda = 0$, the penalty disappears, and we are back to plain OLS.
- If $\lambda$ is large, the model will desperately try to make $w$ smaller to avoid a massive penalty score.

**Where did this formula/concept come from?** "L2" refers to the $L_2$-norm (Euclidean distance) in mathematics, which involves squaring the values.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Solve for the Optimal Ridge Weight (w_ridge)</div>

**What changed from Step 2?** We have the formula for the cost. Now we need to find the specific value of $w$ that produces the absolute lowest cost (the bottom of the U-shaped curve).

**What are we doing?** We are using calculus to find the lowest point of the curve by taking the derivative and setting it to zero.

**How do we do it?**
1. Take the derivative (the slope) of $J_{\text{ridge}}(w)$ with respect to $w$:
   - The derivative of $\frac{1}{2}(w - 4.0)^2$ is $(w - 4.0)$.
   - The derivative of $\frac{\lambda}{2}w^2$ is $\lambda w$.
   $$\frac{d J_{\text{ridge}}}{dw} = (w - 4.0) + \lambda w$$

2. To find the minimum cost, set the derivative to exactly $0$:
   $$(w - 4.0) + \lambda w = 0$$

3. Solve for $w$:
   $$w + \lambda w - 4.0 = 0$$
   $$w(1 + \lambda) = 4.0$$
   $$w_{\text{ridge}} = \frac{4.0}{1 + \lambda}$$

**Where did this formula/concept come from?** In calculus, the bottom of a smooth convex curve is flat. A flat line has a slope of $0$. By setting the derivative to $0$, we pinpoint the exact minimum.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Compute Ridge Weights for Specific λ Values</div>

**What changed from Step 3?** We found the closed-form shrinkage equation: $w_{\text{ridge}} = \frac{4.0}{1 + \lambda}$. Now we plug in actual numbers.

**What are we doing?** Calculating the final weight for $\lambda = 0, 1, 3, \text{ and } 9$.

**How do we do it?**
- **For $\lambda = 0$:** $w_{\text{ridge}} = \frac{4.0}{1 + 0} = \frac{4.0}{1} = \mathbf{4.0}$
- **For $\lambda = 1$:** $w_{\text{ridge}} = \frac{4.0}{1 + 1} = \frac{4.0}{2} = \mathbf{2.0}$
- **For $\lambda = 3$:** $w_{\text{ridge}} = \frac{4.0}{1 + 3} = \frac{4.0}{4} = \mathbf{1.0}$
- **For $\lambda = 9$:** $w_{\text{ridge}} = \frac{4.0}{1 + 9} = \frac{4.0}{10} = \mathbf{0.4}$

*Notice the pattern!* Even if $\lambda$ becomes one million ($\lambda = 1{,}000{,}000$), the math becomes $\frac{4.0}{1{,}000{,}001} \approx 0.000004$. It shrinks closer and closer to $0$, but mathematically, division by $(1 + \lambda)$ will **never** let it hit exactly $0.0$.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Formulate the Lasso (L1) Cost Function</div>

**What changed from Step 4?** We are setting aside the L2 (squared) penalty and testing the L1 (absolute value) penalty instead.

**What are we doing?** We are writing the cost function for Lasso regression.

**How do we do it?** The Lasso penalty uses the absolute value of $w$, written as $|w|$, multiplied by $\lambda$:
$$\text{L1 Penalty} = \lambda |w|$$

We add this to our baseline OLS cost function:
$$J_{\text{lasso}}(w) = \frac{1}{2}(w - 4.0)^2 + \lambda |w|$$

**Where did this formula/concept come from?** "L1" refers to the $L_1$-norm (Manhattan distance), which uses absolute values instead of squares. The absolute value function creates a sharp "V" shape at $0$, unlike the smooth "U" shape of a square.
</div>

<div class="step-card">
<div class="step-badge">Step 6: Derive the Lasso Soft-Thresholding Operator</div>

**What changed from Step 5?** We need to find the minimum of this new Lasso cost function.

**What are we doing?** Solving for the optimal Lasso weight. Because absolute value has a sharp corner at zero, we use subgradient calculus and the Soft-Thresholding operator.

**How do we do it?**
1. Assume our weight $w$ is currently positive ($w > 0$). In this region, $|w| = w$:
   - The derivative of $\frac{1}{2}(w - 4.0)^2 + \lambda w$ is: $(w - 4.0) + \lambda$
   - Set to zero: $w - 4.0 + \lambda = 0$
   - Solve for $w$: $w = 4.0 - \lambda$

2. What if the penalty $\lambda$ is larger than $4.0$? For example, $\lambda = 5$:
   - The raw subtraction gives: $w = 4.0 - 5 = -1.0$.
   - But if $w$ becomes negative, the derivative jumps discontinuously! The sharp "V" corner of the absolute value function traps the weight exactly at $0$.

3. We summarize this behavior with the **Soft-Thresholding Operator**:
   $$w_{\text{lasso}} = \text{sign}(w_{\text{ols}}) \times \max(0, |w_{\text{ols}}| - \lambda)$$
   This translates to: *"Take the original weight ($4.0$), subtract the penalty ($\lambda$). If the result falls below $0$, snap it to exactly $0$."*

**Where did this formula/concept come from?** Subgradient optimization of convex, non-smooth functions. The sharp corner prevents the slope from smoothly crossing the zero line, creating an attractor that forces coefficients to exactly zero.
</div>

<div class="step-card">
<div class="step-badge">Step 7: Compute Lasso Weights for Specific λ Values</div>

**What changed from Step 6?** We have our Lasso formula: $w_{\text{lasso}} = \max(0, 4.0 - \lambda)$. Now we calculate.

**What are we doing?** Finding the final weight for $\lambda = 1, 2, 4, \text{ and } 6$.

**How do we do it?**
- **For $\lambda = 1$:** $w_{\text{lasso}} = \max(0, 4.0 - 1) = \max(0, 3.0) = \mathbf{3.0}$
- **For $\lambda = 2$:** $w_{\text{lasso}} = \max(0, 4.0 - 2) = \max(0, 2.0) = \mathbf{2.0}$
- **For $\lambda = 4$:** $w_{\text{lasso}} = \max(0, 4.0 - 4) = \max(0, 0.0) = \mathbf{0.0}$ *(EXACTLY ZERO!)*
- **For $\lambda = 6$:** $w_{\text{lasso}} = \max(0, 4.0 - 6) = \max(0, -2.0) = \mathbf{0.0}$ *(Trapped at zero!)*

**Where did this formula/concept come from?** The $\max(0, \text{value})$ function simply returns whichever number is higher. If the subtraction results in a negative number, $0$ is higher, so it outputs $0$.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary of Ridge vs. Lasso Shrinkage</div>

**What is the final answer?**
- **Ridge (L2) weights** decay towards zero multiplicatively: $4.0 \rightarrow 2.0 \rightarrow 1.0 \rightarrow 0.4$. They approach $0$ asymptotically, but never hit $0.0$.
- **Lasso (L1) weights** march towards zero subtractively: $3.0 \rightarrow 2.0 \rightarrow 0.0 \rightarrow 0.0$. They collapse to exactly $0.0$ once $\lambda \ge |w_{\text{ols}}|$.

| Regularization | Formula | $\lambda = 1$ | $\lambda = 2$ | $\lambda = 4$ | Sparsity (Exact 0)? |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Ridge (L2)** | $\frac{w_{\text{ols}}}{1 + \lambda}$ | $2.0$ | $1.33$ | $0.80$ | No (dense weights) |
| **Lasso (L1)** | $\max(0, w_{\text{ols}} - \lambda)$ | $3.0$ | $2.0$ | **$0.0$** | **Yes (sparse weights)** |

**Why does this answer make sense?** Ridge divides the weight, while Lasso subtracts from the weight. If you keep dividing a positive number, it gets infinitesimally small but never reaches zero. If you keep subtracting from a positive number, it quickly hits zero. Because Lasso hits exactly $0.0$, it effectively **deletes** uninformative features from the model entirely. This is called **Automated Feature Selection**.
</div>

</div>

::: quiz Checkpoint 1: Ridge vs. Lasso Shrinkage
If you have a dataset with 10,000 features, and you suspect that only about 50 of them are actually useful for predicting your target, which regularization method should you use and why?
(A) Ridge, because it will shrink the 9,950 useless features to exactly zero.
(*B) Lasso, because its diamond-shaped constraint will drive the weights of the 9,950 useless features to exactly zero, leaving a simple, readable model.
(C) Ridge, because the circular constraint ensures all features remain non-zero and contribute to the model.
(D) Lasso, because it will divide all 10,000 features by $(1 + \lambda)$.
::: explanation
Lasso (L1) performs Feature Selection. It can force coefficients to exactly $0.0$, effectively removing useless features from the model. Ridge (L2) generally shrinks coefficients toward zero without producing exact zeros.
:::

---

## Level 2: Geometric Contour Proof (L1 Diamond vs. L2 Circle)

### Problem 2.1: Visualizing Why Lasso Causes Sparsity

**Problem Statement:** You have seen the algebra showing that Lasso creates exact zeros while Ridge does not. Now, we will prove it visually using geometry. Imagine a model with two features ($w_1$ and $w_2$).

1. Draw and describe the constraint boundary for Ridge (L2).
2. Draw and describe the constraint boundary for Lasso (L1).
3. Explain the geometric tangency proof that shows why Lasso forces one of the weights to become exactly $0$.
4. Relate this back to the Bias-Variance Tradeoff.

::: callout-intuition Core Mental Model
Imagine an expanding puddle of water (representing your model's error) spreading outward across a patio.
- **Ridge** places a smooth, round hula-hoop on the patio. When the expanding puddle touches the hula-hoop, it almost always touches the smooth curved edge somewhere in the middle.
- **Lasso** places a sharp, spiky square box (rotated like a diamond) on the patio. When the expanding puddle touches the diamond, it almost always touches one of the sharp, pointy corners sticking out. In a graph, those sharp corners sit directly on the $0$ lines (the axes). Hitting a corner means hitting exactly zero!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: The L2 Ridge Constraint Boundary (The Circle)</div>

**What are we doing?** Visualizing the Ridge penalty in a 2-dimensional space ($w_1$ on the x-axis, $w_2$ on the y-axis).

**Why are we starting here?** To understand the geometric interaction, we first have to draw the "fences" (constraints) that limit our weights.

**How do we do it?** Another way to express Ridge Regularization mathematically is saying: *"Minimize the error, subject to the constraint that the sum of your squared weights cannot exceed a budget $C$."*
$$w_1^2 + w_2^2 \le C$$

The equation $x^2 + y^2 = r^2$ is the equation for a **Circle**.  
Therefore, the Ridge constraint boundary is a smooth, perfectly round circle centered at zero $(0,0)$. There are absolutely no sharp corners on this boundary.

**Where did this formula/concept come from?** The Karush-Kuhn-Tucker (KKT) and Lagrangian dual formulation of constrained quadratic optimization.
</div>

<div class="step-card">
<div class="step-badge">Step 2: The L1 Lasso Constraint Boundary (The Diamond)</div>

**What changed from Step 1?** We are switching the squared penalty to an absolute value penalty.

**What are we doing?** Visualizing the Lasso constraint boundary in the same 2-dimensional space.

**How do we do it?** The Lasso constraint limits the sum of the absolute values of the weights:
$$|w_1| + |w_2| \le C$$

If you graph this equation in 2D space, you get a square rotated 45 degrees—a **Diamond**.  
Crucially, look at where the sharp, pointy corners of this diamond lie:
- Top corner: $(0, C) \implies w_1$ is exactly $0$.
- Bottom corner: $(0, -C) \implies w_1$ is exactly $0$.
- Right corner: $(C, 0) \implies w_2$ is exactly $0$.
- Left corner: $(-C, 0) \implies w_2$ is exactly $0$.

Every single sharp corner of the Lasso diamond sits directly on a coordinate axis, forcing one of the feature weights to be exactly zero.
</div>

<div class="step-card">
<div class="step-badge">Step 3: The Tangency Proof (Why Contours Hit the Corners)</div>

**What changed from Step 2?** We have drawn our constraints (a Circle and a Diamond). Now we add the expanding "error puddle" (the cost function contours).

**What are we doing?** Explaining how the error contours interact with the constraint boundaries to pick the final weights.

**How do we do it?**
1. The unpenalized optimal OLS point ($w_{\text{ols}}$) sits somewhere outside the constraint shapes.
2. The model's error forms concentric elliptical rings radiating outward from $w_{\text{ols}}$.
3. The constrained optimization algorithm finds the spot where the expanding elliptical contour **first touches** the constraint boundary.
4. **For Ridge (Circle):** The error ellipse expands and touches the smooth, curved edge of the circle. Because the edge is rounded, the contact point will almost certainly be somewhere floating in the interior of a quadrant (e.g., $w_1 = 1.2$, $w_2 = 2.4$). Neither weight is zero.
5. **For Lasso (Diamond):** The error ellipse expands and touches the diamond. Because the diamond has sharp, pointy corners protruding outward along the axes, the elliptical contour will almost always make first contact directly on one of those corners!
6. Hitting a corner means landing on an axis, which guarantees one weight is exactly $0.0$.

**Where did this formula/concept come from?** Robert Tibshirani's seminal 1996 paper introducing the Lasso to explain its feature selection properties.
</div>

<div class="step-card">
<div class="step-badge">Step 4: The Bias-Variance Tradeoff</div>

**What changed from Step 3?** We understand the math and the geometry. Now we connect this to core machine learning theory.

**What are we doing?** Explaining how increasing our penalty parameter ($\lambda$) affects our model's performance on new, unseen data.

**How do we do it?**
- **Variance (Overfitting):** A model with no regularization ($\lambda = 0$) tries too hard to perfectly fit the training data. The weights become massive and chaotic. The model is too flexible, reacting to random noise.
- **Bias (Underfitting):** A model with excessive regularization (e.g., $\lambda \to \infty$) crushes all the weights to zero. The model becomes a flat, unmoving line. It's too rigid to learn anything.

By carefully tuning $\lambda$, we achieve optimal balance:
1. We introduce a small amount of **Bias** (the model is no longer allowed to memorize training noise).
2. In exchange, we massively reduce the **Variance** (the model becomes stable and resilient).
3. The overall generalization error on unseen test data drops. This fundamental trade is the **Bias-Variance Tradeoff**.

**Where did this formula/concept come from?** The bias-variance decomposition of mean squared error:
$$\mathbb{E}[\text{Error}] = \text{Bias}^2 + \text{Variance} + \sigma_{\text{irreducible}}^2$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary of Regularization Geometry</div>

**What is the final answer?**
- Ridge uses a circular ($L_2$) constraint and smoothly shrinks weights without hitting zero.
- Lasso uses a diamond ($L_1$) constraint, and the sharp corners force expanding error contours to hit the axes, setting weights to exactly zero.
- Both methods prevent overfitting by increasing bias to reduce variance.

**Why does this answer make sense?** Geometrically, smooth surfaces lead to smooth, continuous intersections. Sharp corners act like magnets for intersections. This perfectly matches the algebra we solved in Level 1, confirming that Lasso is the tool of choice when you want a simpler model that completely ignores useless features.
</div>

</div>

::: quiz Checkpoint 2: Bias-Variance Tradeoff
What happens to your linear regression model as you continuously *increase* the penalty parameter $\lambda$?
(A) Bias decreases, Variance increases, and the model overfits the data.
(*B) Bias increases, Variance decreases, and the weights are restricted closer to zero.
(C) Both Bias and Variance decrease, resulting in perfect predictions.
(D) The model's weights expand infinitely, increasing the error.
::: explanation
Increasing $\lambda$ applies a stronger penalty to the weights. This pushes coefficients closer toward zero, making the model less flexible (higher bias) and less sensitive to fluctuations in the training data (lower variance).
:::
