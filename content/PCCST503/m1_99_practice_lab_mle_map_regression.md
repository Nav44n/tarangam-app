# Module 1 Practice Lab: The Complete Numerical Vault

**Step-by-step master numerical solutions for all Module 1 examination categories.**

---

## Category 1: Maximum Likelihood Estimation (MLE)
**Problem:** In $n = 20$ semiconductor chips, $k = 6$ are defective. Calculate $\hat{p}_{\text{MLE}}$.
::: step [Solution] Step-by-Step
1. $L(p) = p^6 (1-p)^{14} \implies \ell(p) = 6\ln(p) + 14\ln(1-p)$.
2. $\frac{d\ell}{dp} = \frac{6}{p} - \frac{14}{1-p} = 0 \implies 6(1-p) = 14p$.
3. $6 = 20p \implies \hat{p} = \frac{6}{20} = 0.30 \quad (30\%)$.
:::

---

## Category 2: Maximum A Posteriori (MAP)
**Problem:** An e-commerce item gets $k=2$ 5-star reviews out of $n=2$ total ratings. Prior is $\text{Beta}(\alpha=4, \beta=4)$.
::: step [Solution] Step-by-Step
$$ \hat{p}_{\text{MAP}} = \frac{k + \alpha - 1}{n + \alpha + \beta - 2} = \frac{2 + 4 - 1}{2 + 4 + 4 - 2} = \frac{5}{8} = 0.625 \quad (62.5\%) $$
:::

---

## Category 3: Ordinary Least Squares (OLS)
**Problem:** Fit a line for points $(1, 2), (2, 4), (3, 5), (4, 4), (5, 5)$.
::: step [Solution] Step-by-Step
1. $\bar{x} = 3.0, \bar{y} = 4.0$.
2. $\sum (x-\bar{x})(y-\bar{y}) = 6.0, \quad \sum (x-\bar{x})^2 = 10.0$.
3. $\theta_1 = \frac{6.0}{10.0} = 0.60, \quad \theta_0 = 4.0 - (0.60 \times 3.0) = 2.20$.
**Fitted Line:** $\hat{y} = 2.20 + 0.60x$.
:::
