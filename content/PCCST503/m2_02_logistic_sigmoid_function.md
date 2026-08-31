# The Logistic Sigmoid Function & Probabilistic Activation

**The S-shaped mathematical squashing function that maps any real number into valid probabilities.**

<a id="the-math"></a>
## 1. The Sigmoid Mathematical Definition

$$ \sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{1 + e^z} $$

Where $z = \theta^T x = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d$.

### Fundamental Properties:
1. **Bounded Range:** As $z \to +\infty$, $\sigma(z) \to 1$. As $z \to -\infty$, $\sigma(z) \to 0$.
2. **Symmetry:** $\sigma(-z) = 1 - \sigma(z)$.
3. **Midpoint Threshold:** $\sigma(0) = \frac{1}{1 + 1} = 0.50$.
4. **Calculus Derivative:**
$$ \frac{d\sigma(z)}{dz} = \sigma(z)(1 - \sigma(z)) $$

---

<a id="simulation"></a>
## 2. Visualizing Sigmoid Activation

::: manim assets/videos/m2_logistic_sigmoid.mp4 Sigmoid Activation
Watch how real numbers from $-\infty$ to $+\infty$ are smoothly compressed into the probability range $(0, 1)$.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Sigmoid Midpoint
What is the exact output of the standard logistic sigmoid function $\sigma(z)$ when input $z = 0$?
(A) 0.00
(*B) 0.50
(C) 1.00
(D) -1.00
::: explanation
$\sigma(0) = \frac{1}{1 + e^{-0}} = \frac{1}{1 + 1} = 0.50$, which defines the default decision boundary in binary classification.
:::
