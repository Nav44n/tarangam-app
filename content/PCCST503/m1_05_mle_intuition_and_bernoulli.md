# Maximum Likelihood Estimation (MLE): The Bernoulli Derivation

**How a computer finds the single model parameter that makes the observed data the most statistically probable.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition The Biased-Coin Detective
Suppose you flip a coin $n = 10$ times, observing $k = 7$ Heads and $3$ Tails. You don't know the coin's true probability of heads, $p$ — but you have to guess it from this one batch of evidence, like a detective reconstructing a crime from the clues left behind.

MLE asks a very specific question: *"Among all possible values of $p \in [0, 1]$, which specific $p$ maximizes the mathematical likelihood of getting our exact observed dataset?"* It doesn't ask what's "fair" or "typical" — it asks what value of $p$ makes the evidence you actually collected look the least surprising.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Step-by-step calculus derivation** for a Bernoulli (coin-flip) process:

**Step 1 — Likelihood Function $L(p)$.** Assuming independent and identically distributed (i.i.d.) tosses:
$$ L(p) = \prod_{i=1}^n P(x_i \mid p) = p^k (1-p)^{n-k} $$

**Step 2 — The Log-Likelihood Trick $\ell(p)$.** Products of many small probabilities underflow numerically and are hard to differentiate, so we take the logarithm (which is monotonic, so it doesn't move the maximizer):
$$ \ell(p) = \ln L(p) = k \ln(p) + (n-k) \ln(1-p) $$

**Step 3 — First Derivative with respect to $p$:**
$$ \frac{d}{dp}\ell(p) = \frac{k}{p} - \frac{n-k}{1-p} $$

**Step 4 — First-Order Condition $\frac{d\ell}{dp} = 0$:**
$$ \frac{k}{p} = \frac{n-k}{1-p} \implies k(1-p) = p(n-k) \implies k - kp = np - kp \implies \hat{p}_{\text{MLE}} = \frac{k}{n} $$

```mermaid
flowchart LR
    A[Observed data:<br/>k heads in n flips] --> B[Likelihood L(p)<br/>= p^k(1-p)^n-k]
    B --> C[Log-Likelihood<br/>ℓ(p) = k ln p + (n-k) ln(1-p)]
    C --> D["Set dℓ/dp = 0"]
    D --> E["p̂_MLE = k / n"]
```

::: callout-formula Summary
For any Bernoulli trial, the Maximum Likelihood Estimator is simply the sample proportion $\frac{k}{n}$ (e.g. $\frac{7}{10} = 0.70$) — a satisfyingly intuitive result for such a formal-looking derivation.
:::

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
An email spam filter observes $n = 500$ historical emails from a particular sender, of which $k = 45$ turned out to be spam. Estimate $\hat{p}_{\text{MLE}}$, the probability that a *future* email from this sender is spam.
:::

::: step [Step 2: Execution] Applying the MLE Formula
Using the derived closed-form result directly (no need to re-derive the calculus each time):
$$ \hat{p}_{\text{MLE}} = \frac{k}{n} = \frac{45}{500} = 0.09 $$
:::

::: step [Step 3: Conclusion] Final Result
The Maximum Likelihood Estimate is $\hat{p}_{\text{MLE}} = 0.09$ (9%) — this is the value of $p$ that makes the observed 45-out-of-500 spam rate the single most probable outcome, among all possible values of $p$. Note that with $n=500$ (a reasonably large sample), this estimate is fairly trustworthy; the next topic covers what happens — and why MLE can misbehave — when $n$ is very small.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Log Transformation
Why do machine learning algorithms optimize $\ln L(\theta)$ instead of $L(\theta)$ directly?
(A) The logarithm alters the location of the optimal parameter
(*B) It converts numerically unstable products into stable sums while preserving the exact location of the maximum
(C) It eliminates the need to compute derivatives
(D) It turns non-convex functions into concave functions in every case
::: explanation
Because $\ln(x)$ is strictly monotonically increasing, $\arg\max L(\theta) = \arg\max \ln L(\theta)$ — the log never moves *where* the maximum occurs. It also prevents numerical underflow, since multiplying many small probabilities together can produce numbers too tiny for a computer to represent accurately, while summing their logs does not.
:::

::: quiz Q2: MLE Computation
A factory samples $n = 200$ manufactured bolts and finds $k = 12$ defective. What is $\hat{p}_{\text{MLE}}$ for the probability that a randomly manufactured bolt is defective?
(A) $0.12$
(*B) $0.06$
(C) $0.94$
(D) $12.0$
::: explanation
Applying $\hat{p}_{\text{MLE}} = k/n = 12/200 = 0.06$ (6%) — directly using the closed-form Bernoulli MLE result derived above.
:::

::: quiz Q3: First-Order Condition
In the derivation of $\hat{p}_{\text{MLE}}$, what is the purpose of setting $\frac{d\ell}{dp} = 0$?
(A) To normalize the probability distribution so it sums to 1
(*B) To find the critical point where the log-likelihood function is at a maximum (its slope is flat), which for this concave function is the global maximizer
(C) To guarantee the likelihood function equals exactly 1
(D) To convert the Bernoulli distribution into a Gaussian distribution
::: explanation
Setting the first derivative to zero locates a critical point of $\ell(p)$. Because the Bernoulli log-likelihood is concave in $p$ over $(0,1)$, this critical point is guaranteed to be the global maximum — precisely the $p$ value the likelihood-maximization principle is searching for.
:::
