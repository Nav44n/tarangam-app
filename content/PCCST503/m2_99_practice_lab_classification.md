# Module 2 Practice Lab: The Complete Numerical Vault

**Step-by-step master numerical solutions for all Module 2 examination categories.**

---

## Category 1: Logistic Regression & Odds
**Problem:** A logistic regression model has $z = \theta^Tx = +1.0$. Calculate predicted probability $\hat{y}$ and Odds.
::: step [Solution] Step-by-Step
1. $P(y=1) = \sigma(1.0) = \frac{1}{1 + e^{-1.0}} = \frac{1}{1 + 0.3679} = 0.7311 \quad (73.11\%)$.
2. $\text{Odds} = \frac{0.7311}{1 - 0.7311} = 2.718 = e^1$.
:::

---

## Category 2: Naïve Bayes with Laplace Smoothing
**Problem:** Classify email *"winner meeting"* given $P(\text{Spam})=0.4, P(\text{Ham})=0.6$, vocabulary $|V|=3$.
::: step [Solution] Step-by-Step
- $\text{Score(Spam)} = 0.40 \times \frac{4+1}{10+3} \times \frac{0+1}{10+3} = 0.40 \times \frac{5}{13} \times \frac{1}{13} = 0.01183$.
- $\text{Score(Ham)} = 0.60 \times \frac{1+1}{6+3} \times \frac{5+1}{6+3} = 0.60 \times \frac{2}{9} \times \frac{6}{9} = 0.08889$.
- $P(\text{Ham} \mid \text{Email}) = \frac{0.08889}{0.01183 + 0.08889} = 88.25\% \implies \text{Classify as Ham}$.
:::

---

## Category 3: Decision Tree Information Gain
**Problem:** $S$ has 9 Yes, 5 No ($H(S)=0.9402$). Feature `Windy` has `False` (6 Yes, 2 No, $H=0.8113$) and `True` (3 Yes, 3 No, $H=1.000$).
::: step [Solution] Step-by-Step
1. $H(S \mid \text{Windy}) = \frac{8}{14}(0.8113) + \frac{6}{14}(1.000) = 0.4636 + 0.4286 = 0.8922\text{ bits}$.
2. $IG(S, \text{Windy}) = 0.9402 - 0.8922 = 0.0480\text{ bits}$.
:::
