# Parameter Estimation: Maximum Likelihood Estimation (MLE)

**A rigorous way of answering: 'What underlying model parameter makes the data we observed the most probable?'**

<a id="the-intuition"></a>
## 1. The Intuition: The Biased Coin Detective

Imagine you find a mysterious coin on the street. You flip it **10 times**, and it lands on **Heads 7 times** and **Tails 3 times**.

::: callout-intuition The Core Question
You ask: *"What is the true probability $p$ that this coin lands on Heads?"*
- Could $p = 0.1$? (If it only gave heads 10% of the time, getting 7 heads would be miraculous).
- Could $p = 0.9$? (Possible, but getting 3 tails is somewhat unlikely).
- **Maximum Likelihood Estimation (MLE)** asks: *"Which specific value of $p \in [0, 1]$ maximizes the mathematical probability of observing exactly 7 Heads and 3 Tails?"*
:::

Common sense tells you $p = 0.7$. MLE is the exact calculus engine that proves your intuition is mathematically optimal!

---

<a id="the-math"></a>
## 2. Mathematical Derivation Step-by-Step

Let $X = \{x_1, x_2, \dots, x_n\}$ be independent and identically distributed (i.i.d.) observations from a Bernoulli distribution with parameter $p$:

$$ P(X=1) = p, \quad P(X=0) = 1-p $$

### Step 1: The Likelihood Function $L(p)$
Because the coin tosses are independent, the joint probability (Likelihood) of observing $k$ heads in $n$ tosses is the product of individual probabilities:

$$ L(p) = \prod_{i=1}^n P(x_i | p) = p^k (1-p)^{n-k} $$

### Step 2: The Log-Likelihood Trick ($\ell(p)$)
Multiplying hundreds of small probabilities (like $0.5 \times 0.5 \times \dots$) causes severe **numerical underflow** in computers. 

Since the natural logarithm $\ln(x)$ is a **strictly monotonic increasing function**, the parameter $p$ that maximizes $\ln(L(p))$ is identical to the parameter that maximizes $L(p)$:

$$ \ell(p) = \ln L(p) = \ln\left( p^k (1-p)^{n-k} 
ight) = k \ln(p) + (n-k) \ln(1-p) $$

### Step 3: Finding the Maximum via Calculus
To locate the peak of the log-likelihood curve, take the first derivative with respect to $p$ and set it to zero:

$$ rac{d}{dp}\ell(p) = rac{k}{p} - rac{n-k}{1-p} = 0 $$

$$ rac{k}{p} = rac{n-k}{1-p} \implies k(1-p) = p(n-k) \implies k - kp = np - kp $$

$$ \hat{p}_{\text{MLE}} = rac{k}{n} $$

::: callout-formula Parameter Decoder Table
| Symbol | Meaning | Example Value |
| :--- | :--- | :--- |
| $n$ | Total number of trials / samples | $10$ tosses |
| $k$ | Count of successful outcomes (Heads) | $7$ heads |
| $L(p)$ | Likelihood Function (Probability of data given $p$) | $p^7 (1-p)^3$ |
| $\ell(p)$ | Log-Likelihood (Converts product to sum) | $7\ln(p) + 3\ln(1-p)$ |
| $\hat{p}_{\text{MLE}}$ | Maximum Likelihood Estimator | $7/10 = 0.70$ |
:::

---

<a id="worked-example"></a>
## 3. Stepped Numerical Example

::: step [Step 1: Given Data] Problem Statement
A quality assurance engineer inspects $n=50$ microchips and finds $k=4$ defective chips. Find the Maximum Likelihood Estimate of the defect rate $p$.
:::

::: step [Step 2: Log-Likelihood Formulation] Setup Equation
$$ \ell(p) = 4 \ln(p) + (50 - 4) \ln(1-p) = 4 \ln(p) + 46 \ln(1-p) $$
:::

::: step [Step 3: First-Order Condition] Derivative
$$ rac{d}{dp}\ell(p) = rac{4}{p} - rac{46}{1-p} = 0 \implies 4(1-p) = 46p $$
:::

::: step [Step 4: Analytical Solution] Final Result
$$ 4 = 50p \implies \hat{p}_{\text{MLE}} = rac{4}{50} = 0.08 \text{ (8% Defect Rate)} $$
:::

---

<a id="simulation"></a>
## 4. Visualizing the Likelihood Hill

::: manim assets/videos/m1_paradigms.mp4 Likelihood Optimization Surface
Watch how the slope of the log-likelihood curve hits zero exactly at the maximum likelihood estimate.
:::

---

<a id="self-check"></a>
## 5. Active Recall Checkpoint

::: quiz Q1: Theoretical Motivation
Why do machine learning algorithms optimize the **Log-Likelihood** $\ln L(\theta)$ instead of the raw Likelihood $L(\theta)$?
(A) Logarithms change the location of the optimal parameter $\theta^*$
(*B) It converts numerically unstable products into stable sums and simplifies differentiation
(C) Logarithms guarantee the function is non-convex
(D) It eliminates the need for computing derivatives
::: explanation
Because probabilities are $\le 1$, multiplying thousands of them causes numerical underflow ($0.00000...$). Taking the logarithm transforms products into sums ($\ln(ab) = \ln a + \ln b$), while preserving the exact same argmax peak due to monotonicity.
:::

::: quiz Q2: Parameter Estimation
If you flip a coin 3 times and get 3 Heads ($n=3, k=3$), what is the Maximum Likelihood Estimate for $p$?
(A) 0.50
(B) 0.75
(*C) 1.00
(D) Undefined
::: explanation
$\hat{p}_{\text{MLE}} = rac{k}{n} = rac{3}{3} = 1.0$. This highlights a critical limitation of pure MLE: with small sample sizes, it completely overfits to the observed data, ignoring prior common sense that coins are usually fair. (This motivates MAP estimation!).
:::
