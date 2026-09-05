# Progressive Problems: Gradient Descent Optimization & Weight Updates

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped fraction-to-decimal conversions, and full line-by-line arithmetic for every derivative and weight update.

---

## Level 1: Two-Epoch Weight Update Trace with Learning Rate $\alpha$

### Problem 1.1: Complete Hand-Calculated Trace of Batch Gradient Descent

**Problem Statement:** You are training a simple linear regression model $h_\theta(x) = \theta_0 + \theta_1 x$ on a miniature dataset of $m = 3$ training examples:

$$\{(x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), (x^{(3)}, y^{(3)})\} = \{(1, 1), (2, 3), (3, 2)\}$$

We use the standard Mean Squared Error (MSE) cost function with the $\frac{1}{2m}$ convention:

$$J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^{m} \big(h_\theta(x^{(i)}) - y^{(i)}\big)^2$$

- **Initial Parameters:** $\theta_0^{(0)} = 0.0,\quad \theta_1^{(0)} = 0.0$
- **Learning Rate:** $\alpha = 0.1$

Perform the following calculations step-by-step without skipping any intermediate arithmetic:
1. Compute the initial cost $J(\theta_0^{(0)}, \theta_1^{(0)})$.
2. Trace **Epoch 1**:
   - Compute the model's predictions $h_\theta(x^{(i)})$ for all three samples.
   - Compute the individual error terms $(h_\theta(x^{(i)}) - y^{(i)})$.
   - Calculate the partial derivative with respect to the intercept: $\frac{\partial J}{\partial \theta_0} = \frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})$.
   - Calculate the partial derivative with respect to the slope: $\frac{\partial J}{\partial \theta_1} = \frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)}) \cdot x^{(i)}$.
   - Perform simultaneous updates to obtain $\theta_0^{(1)}$ and $\theta_1^{(1)}$.
   - Calculate the new cost $J(\theta_0^{(1)}, \theta_1^{(1)})$ to confirm the loss decreased.
3. Trace **Epoch 2**:
   - Recompute predictions, errors, gradients, and update parameters to obtain $\theta_0^{(2)}$ and $\theta_1^{(2)}$.
   - Calculate the updated cost $J(\theta_0^{(2)}, \theta_1^{(2)})$.

::: callout-intuition Core Mental Model
Imagine you are blindfolded on a foggy mountain in the dark, trying to reach the bottom of the valley (the lowest point of cost $J$).  
- You cannot see the global map, but you can feel the slope of the ground under your boots with your feet (**the gradient**).  
- If the ground slopes downward to your right, you step to your right.  
- The size of your stride is controlled by your **learning rate $\alpha$**.  
- If you take carefully sized steps in the direction of steepest descent, each step brings you closer to the valley floor, steadily decreasing your altitude (**the loss**).
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Understand Data, Initial Weights, and Cost Function</summary>

**What are we doing?** Writing down the training examples, initial weights, and the mathematical formula for measuring model error.

**Why are we starting here?** Before taking any step down the hill, we need to know our starting location ($\theta_0 = 0, \theta_1 = 0$) and the altitude measurement formula ($J$).

**How do we do it?**
1. Dataset with $m = 3$ samples:
- Sample 1: $x^{(1)} = 1,\quad y^{(1)} = 1$
- Sample 2: $x^{(2)} = 2,\quad y^{(2)} = 3$
- Sample 3: $x^{(3)} = 3,\quad y^{(3)} = 2$

2. Initial hypothesis model:
$$h_\theta(x) = \theta_0 + \theta_1 x = 0.0 + 0.0 \cdot x = 0.0$$
At this initial state, the model predicts $0.0$ for every input.

3. Cost function definition:
$$J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^{m} \big(h_\theta(x^{(i)}) - y^{(i)}\big)^2$$
Here $m = 3$, so the denominator is $2m = 2 \times 3 = 6$:
$$J(\theta_0, \theta_1) = \frac{1}{6} \sum_{i=1}^{3} \big(h_\theta(x^{(i)}) - y^{(i)}\big)^2$$

**Where did this formula/concept come from?** Gauss and Legendre's principle of least squares. The extra $\frac{1}{2}$ factor is introduced so that when we take the derivative with respect to the parameters, the power of $2$ cancels out cleanly ($2 \times \frac{1}{2} = 1$).
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Calculate the Initial Cost J(0.0, 0.0)</summary>

**What changed from Step 1?** We have our cost equation. Now we plug in our initial predictions to establish a baseline error value.

**What are we doing?** Evaluating $J(0.0, 0.0)$.

**Why are we doing this?** We must measure our starting altitude before starting gradient descent so we can later verify that our updates reduce error.

**How do we do it?** Compute the error for each sample when $h(x) = 0.0$:
- For $i=1$: $h_\theta(x^{(1)}) - y^{(1)} = 0.0 - 1 = -1.0 \implies (-1.0)^2 = 1.0$
- For $i=2$: $h_\theta(x^{(2)}) - y^{(2)} = 0.0 - 3 = -3.0 \implies (-3.0)^2 = 9.0$
- For $i=3$: $h_\theta(x^{(3)}) - y^{(3)} = 0.0 - 2 = -2.0 \implies (-2.0)^2 = 4.0$

Sum the squared errors:
$$\sum_{i=1}^{3} \big(h_\theta(x^{(i)}) - y^{(i)}\big)^2 = 1.0 + 9.0 + 4.0 = 14.0$$

Multiply by $\frac{1}{2m} = \frac{1}{6}$:
$$J(0.0, 0.0) = \frac{14.0}{6} = \frac{7}{3} \approx 2.3333$$

Our baseline cost at the start of training is **$2.3333$**.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Epoch 1 — Derive the Gradient Formulas</summary>

**What changed from Step 2?** We know our starting error. Now we compute the direction of steepest ascent by calculating partial derivatives.

**What are we doing?** Finding the rate of change of $J$ with respect to $\theta_0$ and $\theta_1$.

**Why are we doing this?** The gradient tells us which way is "uphill." Gradient descent moves in the opposite direction (downhill) by subtracting the gradient multiplied by $\alpha$.

**How do we do it?** Apply the chain rule of calculus to $J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^{m} (\theta_0 + \theta_1 x^{(i)} - y^{(i)})^2$:

1. For $\theta_0$:
   $$\frac{\partial J}{\partial \theta_0} = \frac{1}{2m} \sum_{i=1}^{m} 2 \cdot \big(h_\theta(x^{(i)}) - y^{(i)}\big) \cdot \frac{\partial}{\partial \theta_0}(\theta_0 + \theta_1 x^{(i)} - y^{(i)})$$
   $$\frac{\partial}{\partial \theta_0}(\theta_0 + \theta_1 x^{(i)} - y^{(i)}) = 1$$
   $$\frac{\partial J}{\partial \theta_0} = \frac{1}{m} \sum_{i=1}^{m} \big(h_\theta(x^{(i)}) - y^{(i)}\big)$$

2. For $\theta_1$:
   $$\frac{\partial J}{\partial \theta_1} = \frac{1}{2m} \sum_{i=1}^{m} 2 \cdot \big(h_\theta(x^{(i)}) - y^{(i)}\big) \cdot \frac{\partial}{\partial \theta_1}(\theta_0 + \theta_1 x^{(i)} - y^{(i)})$$
   $$\frac{\partial}{\partial \theta_1}(\theta_0 + \theta_1 x^{(i)} - y^{(i)}) = x^{(i)}$$
   $$\frac{\partial J}{\partial \theta_1} = \frac{1}{m} \sum_{i=1}^{m} \big(h_\theta(x^{(i)}) - y^{(i)}\big) \cdot x^{(i)}$$

Notice how the $2$ from the exponent cancelled with the $\frac{1}{2}$.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Epoch 1 — Compute Gradients Numerically</summary>

**What changed from Step 3?** We have the formulas. Now we insert our numbers for Epoch 1.

**What are we doing?** Calculating $\frac{\partial J}{\partial \theta_0}$ and $\frac{\partial J}{\partial \theta_1}$ at $(\theta_0, \theta_1) = (0.0, 0.0)$.

**How do we do it?**
1. Calculate gradient for $\theta_0$:
   $$\sum_{i=1}^{3} \big(h_\theta(x^{(i)}) - y^{(i)}\big) = (-1.0) + (-3.0) + (-2.0) = -6.0$$
   $$\frac{\partial J}{\partial \theta_0} = \frac{1}{3} \times (-6.0) = -2.0$$

2. Calculate gradient for $\theta_1$:
   - For $i=1$: $(h - y) \cdot x^{(1)} = (-1.0) \times 1 = -1.0$
   - For $i=2$: $(h - y) \cdot x^{(2)} = (-3.0) \times 2 = -6.0$
   - For $i=3$: $(h - y) \cdot x^{(3)} = (-2.0) \times 3 = -6.0$

   Sum the products:
   $$\sum_{i=1}^{3} \big(h_\theta(x^{(i)}) - y^{(i)}\big) \cdot x^{(i)} = (-1.0) + (-6.0) + (-6.0) = -13.0$$
   $$\frac{\partial J}{\partial \theta_1} = \frac{1}{3} \times (-13.0) = -\frac{13}{3} \approx -4.3333$$
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Epoch 1 — Perform Simultaneous Parameter Updates</summary>

**What changed from Step 4?** We have our gradients: $\frac{\partial J}{\partial \theta_0} = -2.0$ and $\frac{\partial J}{\partial \theta_1} = -\frac{13}{3}$. Now we update both weights.

**What are we doing?** Applying the gradient descent update rules:
$$\theta_0 := \theta_0 - \alpha \frac{\partial J}{\partial \theta_0}$$
$$\theta_1 := \theta_1 - \alpha \frac{\partial J}{\partial \theta_1}$$
with $\alpha = 0.1$.

**Why are we doing this?** Because the gradients are negative, the slope tilts down to the left. Subtracting a negative gradient increases the parameters, moving them in the direction that decreases the loss.

**How do we do it?**
1. Update $\theta_0$:
   $$\theta_0^{(1)} = 0.0 - 0.1 \times (-2.0) = 0.0 - (-0.2) = 0.0 + 0.2 = \mathbf{0.2}$$

2. Update $\theta_1$:
   $$\theta_1^{(1)} = 0.0 - 0.1 \times \left(-\frac{13}{3}\right) = 0.0 + \frac{1.3}{3} = \frac{13}{30} \approx \mathbf{0.4333}$$

Our model parameters after Epoch 1 are:
$$\theta_0^{(1)} = 0.2,\quad \theta_1^{(1)} = \frac{13}{30} \approx 0.4333$$
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Epoch 1 — Verify Loss Reduction J(θ₀⁽¹⁾, θ₁⁽¹⁾)</summary>

**What changed from Step 5?** We have new parameters. Now we calculate the new cost to confirm the model improved.

**What are we doing?** Calculating $J(0.2, 0.4333)$.

**How do we do it?**
1. Calculate new predictions $h_\theta(x) = 0.2 + \frac{13}{30}x$:
   - For $x^{(1)} = 1$: $h(1) = 0.2 + 0.4333(1) = \frac{6}{30} + \frac{13}{30} = \frac{19}{30} \approx 0.6333$
   - For $x^{(2)} = 2$: $h(2) = 0.2 + 0.4333(2) = \frac{6}{30} + \frac{26}{30} = \frac{32}{30} = \frac{16}{15} \approx 1.0667$
   - For $x^{(3)} = 3$: $h(3) = 0.2 + 0.4333(3) = 0.2 + 1.3 = 1.5000$

2. Calculate errors $(h(x^{(i)}) - y^{(i)})$:
   - For $i=1$: $\frac{19}{30} - 1 = -\frac{11}{30} \approx -0.3667 \implies \left(-\frac{11}{30}\right)^2 = \frac{121}{900} \approx 0.1344$
   - For $i=2$: $\frac{32}{30} - 3 = \frac{32 - 90}{30} = -\frac{58}{30} \approx -1.9333 \implies \left(-\frac{58}{30}\right)^2 = \frac{3364}{900} \approx 3.7378$
   - For $i=3$: $1.5 - 2 = -0.5 = -\frac{15}{30} \implies (-0.5)^2 = 0.25 = \frac{225}{900}$

3. Sum the squared errors:
   $$\text{Sum} = \frac{121 + 3364 + 225}{900} = \frac{3710}{900} = \frac{371}{90} \approx 4.1222$$

4. Multiply by $\frac{1}{2m} = \frac{1}{6}$:
   $$J(0.2, 0.4333) = \frac{1}{6} \times \frac{371}{90} = \frac{371}{540} \approx \mathbf{0.6870}$$

**Check:** Cost dropped from $2.3333 \to 0.6870$ (a $70.5\%$ reduction in error after a single epoch).
</details>

<details class="step-card">
<summary class="step-badge">Step 7: Epoch 2 — Compute Predictions and Gradients</summary>

**What changed from Step 6?** Epoch 1 is complete. Now we repeat the process for Epoch 2 starting from $\theta_0^{(1)} = 0.2$ and $\theta_1^{(1)} = \frac{13}{30}$.

**What are we doing?** Calculating the new gradients $\frac{\partial J}{\partial \theta_0}$ and $\frac{\partial J}{\partial \theta_1}$.

**How do we do it?**
1. We use the error terms calculated in Step 6:
   $$e_1 = -\frac{11}{30},\quad e_2 = -\frac{58}{30},\quad e_3 = -\frac{15}{30}$$

2. Calculate gradient for $\theta_0$:
   $$\sum_{i=1}^{3} e_i = -\frac{11}{30} - \frac{58}{30} - \frac{15}{30} = -\frac{84}{30} = -2.8000$$
   $$\frac{\partial J}{\partial \theta_0} = \frac{1}{3} \times \left(-\frac{84}{30}\right) = -\frac{84}{90} = -\frac{14}{15} \approx \mathbf{-0.9333}$$

3. Calculate gradient for $\theta_1$:
   - $e_1 \cdot x^{(1)} = -\frac{11}{30} \times 1 = -\frac{11}{30}$
   - $e_2 \cdot x^{(2)} = -\frac{58}{30} \times 2 = -\frac{116}{30}$
   - $e_3 \cdot x^{(3)} = -\frac{15}{30} \times 3 = -\frac{45}{30}$

   Sum the weighted errors:
   $$\sum_{i=1}^{3} e_i \cdot x^{(i)} = \frac{-11 - 116 - 45}{30} = -\frac{172}{30} \approx -5.7333$$
   $$\frac{\partial J}{\partial \theta_1} = \frac{1}{3} \times \left(-\frac{172}{30}\right) = -\frac{172}{90} = -\frac{86}{45} \approx \mathbf{-1.9111}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 8: Epoch 2 — Update Parameters to Obtain θ₀⁽²⁾ and θ₁⁽²⁾</summary>

**What changed from Step 7?** We computed the new gradients: $\frac{\partial J}{\partial \theta_0} \approx -0.9333$ and $\frac{\partial J}{\partial \theta_1} \approx -1.9111$.

**What are we doing?** Applying the learning step with $\alpha = 0.1$.

**How do we do it?**
1. Update $\theta_0$:
   $$\theta_0^{(2)} = \theta_0^{(1)} - \alpha \frac{\partial J}{\partial \theta_0}$$
   $$\theta_0^{(2)} = 0.2 - 0.1 \times \left(-\frac{14}{15}\right) = 0.2 + \frac{14}{150} = \frac{30}{150} + \frac{14}{150} = \frac{44}{150} = \frac{22}{75} \approx \mathbf{0.2933}$$

2. Update $\theta_1$:
   $$\theta_1^{(2)} = \theta_1^{(1)} - \alpha \frac{\partial J}{\partial \theta_1}$$
   $$\theta_1^{(2)} = \frac{13}{30} - 0.1 \times \left(-\frac{86}{45}\right) = \frac{13}{30} + \frac{86}{450} = \frac{195}{450} + \frac{86}{450} = \frac{281}{450} \approx \mathbf{0.6244}$$

Our updated weights after Epoch 2 are:
$$\theta_0^{(2)} \approx 0.2933,\quad \theta_1^{(2)} \approx 0.6244$$
</details>

<details class="step-card">
<summary class="step-badge">Step 9: Epoch 2 — Calculate Updated Cost J(θ₀⁽²⁾, θ₁⁽²⁾)</summary>

**What changed from Step 8?** We updated our weights to $(0.2933, 0.6244)$. Now we verify that the cost continues to decrease.

**What are we doing?** Evaluating $J(0.2933, 0.6244)$.

**How do we do it?**
1. Compute new predictions with $h(x) = \frac{44}{150} + \frac{281}{450}x = \frac{132 + 281x}{450}$:
   - For $x^{(1)} = 1$: $h(1) = \frac{132 + 281(1)}{450} = \frac{413}{450} \approx 0.9178$
   - For $x^{(2)} = 2$: $h(2) = \frac{132 + 281(2)}{450} = \frac{132 + 562}{450} = \frac{694}{450} \approx 1.5422$
   - For $x^{(3)} = 3$: $h(3) = \frac{132 + 281(3)}{450} = \frac{132 + 843}{450} = \frac{975}{450} = \frac{13}{6} \approx 2.1667$

2. Compute errors $(h - y)$:
   - For $i=1$: $0.9178 - 1 = -0.0822 \implies (-0.0822)^2 \approx 0.0068$
   - For $i=2$: $1.5422 - 3 = -1.4578 \implies (-1.4578)^2 \approx 2.1252$
   - For $i=3$: $2.1667 - 2 = +0.1667 \implies (+0.1667)^2 \approx 0.0278$

3. Sum the squared errors:
   $$\text{Sum} \approx 0.0068 + 2.1252 + 0.0278 = 2.1598$$

4. Multiply by $\frac{1}{2m} = \frac{1}{6}$:
   $$J(0.2933, 0.6244) \approx \frac{2.1598}{6} \approx \mathbf{0.3600}$$

**Check:** Cost dropped from $0.6870 \to 0.3600$.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Summary of Two-Epoch Optimization Trace</summary>

**What is the final answer?** The parameter trajectory and cost progression across both epochs:

| Epoch | $\theta_0$ (Intercept) | $\theta_1$ (Slope) | $\frac{\partial J}{\partial \theta_0}$ | $\frac{\partial J}{\partial \theta_1}$ | Cost $J(\theta_0, \theta_1)$ | % Reduction |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0 (Init)** | $0.0000$ | $0.0000$ | $-2.0000$ | $-4.3333$ | $2.3333$ | — |
| **1** | $0.2000$ | $0.4333$ | $-0.9333$ | $-1.9111$ | $0.6870$ | $-70.5\%$ |
| **2** | $0.2933$ | $0.6244$ | — | — | $0.3600$ | $-47.6\%$ |

**Why does this answer make sense?** As the weights move toward the optimal solution, the predictions get closer to the true targets, so the errors shrink. Smaller errors make the gradients smaller (from $-4.33 \to -1.91$), which naturally reduces the step size as the model approaches the minimum.
</details>

</div>

::: quiz Checkpoint 1: Simultaneous vs. Sequential Updates
Why does standard Batch Gradient Descent require updating $\theta_0$ and $\theta_1$ *simultaneously* using temporary variables, rather than updating $\theta_0$ first and immediately using the new $\theta_0$ to compute the gradient for $\theta_1$?
(A) Updating $\theta_0$ first causes a divide-by-zero runtime error in the calculation of $\theta_1$.
(*B) Sequential updates compute the gradient for $\theta_1$ using a point that is no longer on the true gradient vector of the original position, altering the descent trajectory.
(C) Simultaneous updates are only necessary when the learning rate is greater than 1.0.
(D) Sequential updates can only be performed if the dataset has an even number of samples.
::: explanation
Gradient descent is defined mathematically as taking a step in the direction of the negative gradient vector $\nabla J(\theta) = \left[\frac{\partial J}{\partial \theta_0}, \frac{\partial J}{\partial \theta_1}\right]^T$ evaluated at the current parameter vector. If you update $\theta_0$ and immediately use the new value to evaluate $\frac{\partial J}{\partial \theta_1}$, you are no longer computing the gradient at the current position (this becomes coordinate descent or Gauss-Seidel iteration, which follows a different path).
:::

---

## Level 2: Learning Rate Dynamics (Underflow, Convergence, and Divergence)

### Problem 2.1: Mathematical Demonstration of Learning Rate Sensitivity

**Problem Statement:** Consider a simplified 1D optimization problem where the cost function is a simple bowl:

$$J(\theta) = c \cdot (\theta - \theta^*)^2$$

Where $c = 2$ and the true minimum is at $\theta^* = 0$. The derivative is:

$$\frac{dJ}{d\theta} = 2c(\theta - \theta^*) = 4\theta$$

The gradient descent update rule is:

$$\theta^{(t+1)} = \theta^{(t)} - \alpha \frac{dJ}{d\theta} = \theta^{(t)} - \alpha(4\theta^{(t)}) = (1 - 4\alpha)\theta^{(t)}$$

Using an initial parameter value of $\theta^{(0)} = 10.0$, evaluate the behavior of $\theta$ over 3 iterations for three different choices of the learning rate:
1. **Case A (Too Small):** $\alpha = 0.01$
2. **Case B (Well-Tuned):** $\alpha = 0.25$
3. **Case C (Too Large / Divergent):** $\alpha = 0.60$

Derive the general stability condition on $\alpha$ to guarantee convergence.

::: callout-intuition Core Mental Model
Imagine you are adjusting the water temperature in the shower:  
- **$\alpha$ too small:** You turn the knob by a fraction of a millimeter every 5 minutes. You freeze for an hour before the water gets comfortably warm.  
- **$\alpha$ well-tuned:** You turn the knob directly toward warm in smooth, confident adjustments, finding the ideal temperature in a few seconds.  
- **$\alpha$ too large:** You feel cold, so you crank the knob all the way to maximum hot. The water scalds you, so you slam the knob all the way to maximum cold. Each overreaction is wilder than the last until you break the handle. This is **divergence**.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Understand the Contraction Factor (1 - 4α)</summary>

**What are we doing?** Finding the recurrence multiplier that dictates how $\theta$ evolves from one step to the next.

**Why are we starting here?** The update rule can be rewritten as multiplying the previous parameter by a constant scaling factor:
$$\theta^{(t+1)} = (1 - 4\alpha) \cdot \theta^{(t)}$$

After $t$ iterations, applying this multiplier repeatedly gives:
$$\theta^{(t)} = (1 - 4\alpha)^t \cdot \theta^{(0)}$$

For $\theta^{(t)}$ to converge to the minimum ($\theta^* = 0$), the magnitude of the multiplier must be strictly less than $1$:
$$|1 - 4\alpha| < 1$$

Solving this inequality gives the stability condition:
$$-1 < 1 - 4\alpha < 1$$
$$-2 < -4\alpha < 0$$
$$0 < \alpha < \frac{2}{4} \implies \mathbf{0 < \alpha < 0.5}$$

- If $0 < \alpha < 0.5$: The distance to the minimum shrinks on every step (Convergence).
- If $\alpha > 0.5$: The multiplier $|1 - 4\alpha| > 1$, so the distance grows exponentially on every step (Divergence).

**Where did this formula/concept come from?** Fixed-point iteration and stability analysis of discrete-time linear dynamical systems.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Case A — α is Too Small (α = 0.01)</summary>

**What changed from Step 1?** We test our first concrete learning rate: $\alpha = 0.01$.

**What are we doing?** Tracing 3 iterations starting from $\theta^{(0)} = 10.0$.

**How do we do it?**
1. Calculate the contraction multiplier:
   $$1 - 4\alpha = 1 - 4(0.01) = 1 - 0.04 = \mathbf{0.96}$$

2. Compute values across 3 iterations:
   - Iteration 1: $\theta^{(1)} = 0.96 \times 10.0 = \mathbf{9.6000}$
   - Iteration 2: $\theta^{(2)} = 0.96 \times 9.6000 = \mathbf{9.2160}$
   - Iteration 3: $\theta^{(3)} = 0.96 \times 9.2160 = \mathbf{8.8474}$

**Observation:** After 3 full iterations, $\theta$ has only moved from $10.0$ down to $8.85$. It will take roughly $100$ steps just to get close to the target $\theta^* = 0$. The descent is safe, but computationally slow.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Case B — α is Well-Tuned (α = 0.25)</summary>

**What changed from Step 2?** We now test an optimal learning rate: $\alpha = 0.25$.

**What are we doing?** Evaluating the update with $\alpha = 0.25$.

**How do we do it?**
1. Calculate the contraction multiplier:
   $$1 - 4\alpha = 1 - 4(0.25) = 1 - 1.0 = \mathbf{0.0}$$

2. Compute values across 3 iterations:
   - Iteration 1: $\theta^{(1)} = 0.0 \times 10.0 = \mathbf{0.0000}$
   - Iteration 2: $\theta^{(2)} = 0.0 \times 0.0 = \mathbf{0.0000}$
   - Iteration 3: $\theta^{(3)} = 0.0$

**Observation:** Because $1 - 4\alpha = 0$, the algorithm lands directly on the exact minimum $\theta^* = 0$ on the very first step. While real-world high-dimensional loss surfaces are rarely this simple, a well-tuned $\alpha$ drives the error down efficiently without unnecessary oscillation.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Case C — α is Too Large / Divergent (α = 0.60)</summary>

**What changed from Step 3?** We test an unstable learning rate: $\alpha = 0.60$, which violates our stability condition $\alpha < 0.5$.

**What are we doing?** Tracing the path of $\theta$ when the learning rate causes overshooting.

**How do we do it?**
1. Calculate the contraction multiplier:
   $$1 - 4\alpha = 1 - 4(0.60) = 1 - 2.40 = \mathbf{-1.40}$$

2. Compute values across 3 iterations:
   - Iteration 1: $\theta^{(1)} = (-1.40) \times 10.0 = \mathbf{-14.0000}$  
     *(Overshot the minimum and landed farther away on the opposite side).*
   - Iteration 2: $\theta^{(2)} = (-1.40) \times (-14.0000) = \mathbf{+19.6000}$  
     *(Overshot again, bouncing back with a larger magnitude).*
   - Iteration 3: $\theta^{(3)} = (-1.40) \times 19.6000 = \mathbf{-27.4400}$  
     *(Distance continues to explode).*

3. Compare the cost values:
   - Initial Cost: $J(10.0) = 2(10.0)^2 = 200.0$
   - After Step 1: $J(-14.0) = 2(-14.0)^2 = 392.0$
   - After Step 2: $J(19.6) = 2(19.6)^2 = 768.32$
   - After Step 3: $J(-27.44) = 2(-27.44)^2 = 1{,}505.90$

The cost is diverging toward infinity ($J \to \infty$).
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Summary of Learning Rate Regimes</summary>

**What is the final answer?** The behavior of Gradient Descent is governed by the multiplier $(1 - \alpha \cdot \text{curvature})$:

| Regime | Learning Rate ($\alpha$) | Multiplier ($1 - 4\alpha$) | Parameter Trajectory ($\theta$) | Cost Behavior $J(\theta)$ |
| :---: | :---: | :---: | :---: | :---: |
| **Too Small** | $0.01$ | $+0.96$ | $10 \to 9.6 \to 9.22 \to 8.85$ | Decreases slowly (high compute cost) |
| **Optimal** | $0.25$ | $0.00$ | $10 \to 0.0 \to 0.0$ | Converges directly to minimum |
| **Too Large** | $0.60$ | $-1.40$ | $10 \to -14 \to +19.6 \to -27.4$ | Bounces, explodes, and diverges to $\infty$ |

**Why does this answer make sense?** The gradient tells us the slope at our current point, not how far the slope continues downward. If we take a step that is too large, we step completely over the valley and land higher up on the opposite ridge. Taking another step based on the even steeper slope on that ridge results in an even larger overshoot, triggering an explosive feedback loop.
</details>

</div>

::: quiz Checkpoint 2: Diagnosing Divergence in Training Plots
While training a neural network using gradient descent, you plot the cost $J(\theta)$ against the epoch number. You notice that after epoch 3, the cost starts oscillating between positive and negative extremes and rapidly reaches `NaN` (Not a Number). What is the primary cause, and what is the immediate fix?
(A) The learning rate $\alpha$ is too small; increase $\alpha$ by a factor of 10.
(B) The dataset has too many samples; remove half the training data.
(*C) The learning rate $\alpha$ is too large, causing the parameters to overshoot the valley and explode; reduce $\alpha$ significantly.
(D) The cost function requires an intercept term to prevent numerical overflow.
::: explanation
An exploding cost that oscillates with growing magnitude until it reaches numerical overflow (`NaN` or `inf`) is the classic hallmark of an oversized learning rate. The immediate fix is to decrease the learning rate (often by powers of 10, such as from $0.1 \to 0.01$) so the step size respects the local curvature of the loss surface.
:::
