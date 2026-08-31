# Cross-Entropy Loss & The Non-Convexity Trap

**Why Mean Squared Error fails for Logistic Regression and how Cross-Entropy guarantees a convex loss landscape.**

<a id="the-math"></a>
## 1. The Non-Convexity Flaw of MSE

If you plug non-linear $\sigma(\theta^Tx)$ into MSE cost $\frac{1}{2m}\sum (\sigma(\theta^Tx) - y)^2$, the loss surface becomes **wavy and non-convex** with dozens of local minima.

---

## 2. The Convex Cross-Entropy Loss (Log Loss)

$$ J(\theta) = -\frac{1}{m}\sum_{i=1}^m \left[ y^{(i)}\ln(h_\theta(x^{(i)})) + (1-y^{(i)})\ln(1-h_\theta(x^{(i)})) \right] $$

- When $y=1$: Cost is $-\ln(h(x))$. If $h(x) \to 1$, $\text{Cost} \to 0$. If $h(x) \to 0$, $\text{Cost} \to \infty$.
- When $y=0$: Cost is $-\ln(1-h(x))$. If $h(x) \to 0$, $\text{Cost} \to 0$. If $h(x) \to 1$, $\text{Cost} \to \infty$.

### Gradient Vector Update Rule:
$$ \frac{\partial J}{\partial \theta_j} = \frac{1}{m}\sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_j^{(i)} $$

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Loss Penalty
If a model confidently predicts $h_\theta(x) = 0.001$ for a true positive instance ($y = 1$), what penalty does Cross-Entropy assign?
(A) Zero penalty
(B) $0.999$
(*C) Near-infinite penalty ($-\ln(0.001) \approx 6.91$)
(D) Negative penalty
::: explanation
Cross-entropy harshly penalizes confident wrong predictions with asymptotic logarithmic explosion.
:::
