# Gradient Descent Optimization & Learning Rate Dynamics

**The iterative calculus engine powering linear models, support vector machines, and deep neural networks.**

<a id="the-intuition"></a>
## 1. The Intuition: Walking Down a Foggy Mountain

You are blindfolded on a foggy mountain and must reach the valley floor. You feel the slope with your feet ($\nabla J(\theta)$) and take a step in the steepest downward direction.

---

<a id="the-math"></a>
## 2. The Parameter Update Rule

Simultaneously update all parameters for $j = 0, \dots, d$:

$$ \theta_j := \theta_j - \alpha \frac{\partial J(\theta)}{\partial \theta_j} $$

Where $\alpha > 0$ is the **Learning Rate**.

::: callout-pitfall Learning Rate Dynamics
- **$\alpha$ too small:** Extremely slow convergence; high computational cost.
- **$\alpha$ too large:** Overshoots the minimum, oscillates wildly, and diverges to infinity.
:::

---

<a id="simulation"></a>
## 3. Visualizing Optimization

::: manim assets/videos/m2_gradient_descent.mp4 Gradient Descent Surface
Watch parameter updates step down the parabolic cost bowl toward the global minimum.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Gradient at Minimum
What is the mathematical value of the gradient vector $\nabla J(\theta^*)$ when parameters reach the exact local or global minimum?
(*A) Zero vector $\vec{0}$
(B) $1.0$
(C) $-\alpha$
(D) Infinity
::: explanation
At the minimum of a smooth convex function, the tangent slope is completely flat, meaning $\nabla J(\theta) = 0$.
:::
