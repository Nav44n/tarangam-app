# Loss Functions & Optimization: Gradient Descent

**How machine learning models measure their own mistakes and iteratively correct them.**

<a id="the-intuition"></a>
## 1. The Intuition: Walking Down a Foggy Mountain

Imagine you are blindfolded on a foggy mountain and need to reach the lowest point in the valley.

::: callout-intuition The Gradient Descent Strategy
1. You feel the slope of the ground beneath your feet with your foot (**Compute the Gradient $\nabla J(\theta)$**).
2. If the ground slopes downward to your right, you take a step to the right (**Move in the negative gradient direction**).
3. If you take tiny baby steps ($\alpha = 0.0001$), you will take 10 years to reach the bottom.
4. If you take giant blind leaps ($\alpha = 10.0$), you might leap clear across the valley and crash into the opposite peak.
5. The ideal step size is the **Learning Rate ($\alpha$)**.
:::

---

<a id="the-math"></a>
## 2. Loss Functions: Measuring Mistakes

A **Loss Function** $\mathcal{L}(\hat{y}, y)$ quantifies the error for a single training example, while the **Cost Function** $J(\theta)$ computes the average loss across the entire dataset.

### 1. Mean Squared Error (MSE) — for Regression:
$$ J(\theta) = \frac{1}{2m} \sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)} \right)^2 $$
*(Note: The factor of $\frac{1}{2}$ is a mathematical convenience that cleanly cancels when taking derivatives).*

### 2. Binary Cross-Entropy (Log Loss) — for Classification:
$$ J(\theta) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln(h_\theta(x^{(i)})) + (1-y^{(i)}) \ln(1-h_\theta(x^{(i)})) \right] $$

---

<a id="worked-example"></a>
## 3. The Gradient Descent Update Rule

To minimize $J(\theta)$, we iteratively update every parameter $\theta_j$ simultaneously:

$$ \theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta) $$

For Linear Regression with MSE cost, the partial derivative simplifies to:

$$ \frac{\partial}{\partial \theta_j} J(\theta) = \frac{1}{m} \sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_j^{(i)} $$

::: step [Step 1: Compute Prediction] Forward Pass
Calculate $\hat{y}^{(i)} = h_\theta(x^{(i)})$ for all samples.
:::

::: step [Step 2: Calculate Residual Error] Error Calculation
Compute error $e^{(i)} = (\hat{y}^{(i)} - y^{(i)})$.
:::

::: step [Step 3: Compute Gradient Vector] Differentiation
Multiply error by feature values $x_j^{(i)}$ and average across the batch.
:::

::: step [Step 4: Update Parameters] Step Down
Adjust parameters: $\theta_j \leftarrow \theta_j - \alpha \cdot \text{Gradient}$.
:::

---

<a id="simulation"></a>
## 4. Visualizing Gradient Optimization

::: manim assets/videos/m2_gradient_descent.mp4 Convex Optimization Convergence
Watch the red optimization ball take steps down the parabolic cost curve toward the global minimum.
:::

---

<a id="self-check"></a>
## 5. Active Recall Checkpoint

::: quiz Q1: Hyperparameter Dynamics
What occurs if the learning rate $\alpha$ is set too large in Gradient Descent?
(A) The model converges prematurely to a saddle point
(*B) The cost function can oscillate wildly and diverge away from the minimum
(C) The gradient becomes zero on the first iteration
(D) The weights automatically shrink to zero
::: explanation
When $\alpha$ is excessively large, each parameter update overshoots the minimum point, landing higher up on the opposite wall of the cost surface. This causes the cost $J(\theta)$ to increase with every iteration (divergence).
:::
