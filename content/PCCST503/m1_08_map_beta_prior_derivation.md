# MAP with Beta Priors: The Math & Cold-Start Problem

**Step-by-step derivation of conjugate Beta-Binomial MAP estimation.**

<a id="the-intuition"></a>
## 1. The Intuition: Virtual Data (Pseudo-Counts)

A **Beta Distribution** $\text{Beta}(\alpha, \beta)$ serves as the conjugate prior for Bernoulli trials. You can think of $\alpha - 1$ as "virtual prior heads" and $\beta - 1$ as "virtual prior tails".

---

<a id="the-math"></a>
## 2. Mathematical Derivation

$$ P(p) \propto p^{\alpha - 1} (1-p)^{\beta - 1}, \quad L(p) \propto p^k (1-p)^{n-k} $$

### Step 1: Posterior Formulation
$$ P(p \mid D) \propto p^{k + \alpha - 1} (1-p)^{n - k + \beta - 1} $$

### Step 2: Mode of the Beta Posterior
Taking the log, differentiating with respect to $p$, and setting to 0 yields:

$$ \hat{p}_{\text{MAP}} = \frac{k + \alpha - 1}{n + \alpha + \beta - 2} $$

::: callout-exam Concrete Example
If you observe $k=3$ heads in $n=3$ tosses with a prior $\text{Beta}(5, 5)$:
$$ \hat{p}_{\text{MAP}} = \frac{3 + 5 - 1}{3 + 5 + 5 - 2} = \frac{7}{11} \approx 0.636 $$
Instead of an extreme $1.00$, MAP regularizes the estimate to a sensible $0.636$!
:::

---

<a id="self-check"></a>
## 3. Active Recall Checkpoint

::: quiz Q1: Prior Parameters
If $\alpha = 1$ and $\beta = 1$ in a Beta prior (representing a flat uniform prior $U(0, 1)$), what does $\hat{p}_{\text{MAP}}$ equal?
(A) 0.50
(*B) $\frac{k}{n}$ (Identical to MLE)
(C) 0.00
(D) 1.00
::: explanation
Substituting $\alpha=1, \beta=1$ yields $\hat{p}_{\text{MAP}} = \frac{k+0}{n+0} = \frac{k}{n}$, proving that MLE is equivalent to MAP with a uniform, uninformative prior.
:::
