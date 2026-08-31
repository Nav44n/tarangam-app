# Supervised Learning Formalism & Dataset Splitting

**The rigorous mathematical notation of feature spaces, hypothesis functions, and generalization splits.**

<a id="the-math"></a>
## 1. Mathematical Notation

Let training dataset $\mathcal{D} = \{(x^{(1)}, y^{(1)}), \dots, (x^{(m)}, y^{(m)})\}$:
- $m$: Number of training examples.
- $x^{(i)} \in \mathbb{R}^d$: $d$-dimensional feature vector.
- $y^{(i)}$: Ground truth label.
- $h_\theta(x)$: Candidate hypothesis function parameterized by $\theta$.

---

<a id="worked-example"></a>
## 2. The 3-Way Dataset Split

::: step [Train Set (70%)] Optimization
Used by the optimizer (e.g. Gradient Descent) to update model parameters $\theta$.
:::

::: step [Validation Set (15%)] Hyperparameter Tuning
Used to select model complexity (e.g. polynomial degree, regularization strength $\lambda$).
:::

::: step [Test Set (15%)] Unbiased Evaluation
Locked until the very end to evaluate true generalization on unseen data.
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Data Leakage Prevention
Why must model parameters never be trained on the Test set?
(A) It slows down training time
(*B) It causes optimistic evaluation bias, destroying the ability to measure real-world generalization
(C) It forces gradients to zero
(D) It makes the loss function non-convex
::: explanation
Testing on training data measures memorization rather than generalization. An unbiased test set evaluates performance on unseen distributions.
:::
