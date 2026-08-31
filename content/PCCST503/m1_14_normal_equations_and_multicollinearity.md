# The Normal Equation & Matrix Inversion Singularities

**Solving multiple linear regression in a single analytical step and diagnosing multicollinearity.**

<a id="the-math"></a>
## 1. Derivation of the Normal Equation

Expanding the vectorized cost function:
$$ J(\theta) = \frac{1}{2m} \left( \theta^T X^T X \theta - 2 Y^T X \theta + Y^T Y \right) $$

Taking the matrix gradient with respect to $\theta$ and setting to 0:
$$ \nabla_\theta J(\theta) = X^T X \theta - X^T Y = 0 \implies \theta^* = (X^T X)^{-1} X^T Y $$

---

<a id="worked-example"></a>
## 2. Non-Invertibility & Multicollinearity

::: callout-pitfall When is $(X^TX)$ Singular (Non-Invertible)?
$(X^TX)$ cannot be inverted if:
1. **Linearly Dependent Features (Multicollinearity):** E.g. $x_1 = \text{size in } \text{ft}^2$ and $x_2 = \text{size in } \text{m}^2$.
2. **Too Few Samples ($m < d$):** More features than training examples.
*Remedy:* Drop redundant features or apply Ridge Regularization $(X^TX + \lambda I)^{-1}$.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Normal Equation Scaling
What is the computational complexity of solving the Normal Equation for $d$ features?
(A) $O(d)$
(B) $O(d^2)$
(*C) $O(d^3)$ due to matrix inversion
(D) $O(\log d)$
::: explanation
Inverting a $(d+1) \times (d+1)$ matrix $(X^TX)$ scales as $O(d^3)$, making it computationally prohibitive when $d > 10,000$.
:::
