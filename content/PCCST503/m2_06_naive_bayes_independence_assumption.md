# The Naïve Conditional Independence Assumption

**Why multiplying individual feature probabilities simplifies computation from exponential to linear.**

<a id="the-math"></a>
## 1. The Independence Assumption

To compute $P(x_1, x_2, \dots, x_d \mid C_k)$ without assumptions requires estimating $2^d - 1$ joint parameters.

**The "Naïve" Simplification:** Assume all features are conditionally independent given class $C_k$:

$$ P(x_1, x_2, \dots, x_d \mid C_k) = \prod_{j=1}^d P(x_j \mid C_k) $$

### The Classification Decision Rule:
$$ \hat{y} = \arg\max_{k} \left[ \ln P(C_k) + \sum_{j=1}^d \ln P(x_j \mid C_k) \right] $$

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Parameter Scaling
How many parameters must be estimated for $d$ binary features under the Naïve Bayes independence assumption?
(*A) $O(d)$ per class
(B) $O(2^d)$
(C) $O(d^3)$
(D) $O(1)$
::: explanation
Assuming conditional independence reduces the parameter count from exponential $O(2^d)$ to linear $O(d)$.
:::
