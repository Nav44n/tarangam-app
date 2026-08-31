# Parameter Estimation: Maximum Likelihood Estimation (MLE)

**A scary name for a simple question: 'What underlying rule makes the data I just saw the most probable?'**


Imagine you find a strange coin on the street. You flip it 10 times, and it lands on Heads 7 times. You ask yourself: *"Is this a fair 50/50 coin? Or is it rigged?"*



**Maximum Likelihood Estimation (MLE)** is how a computer plays detective. It asks: "Out of all the possible biases this coin could have (maybe it favors heads 10% of the time, or 90% of the time), which bias makes getting exactly 7 heads the *most mathematically likely* (least surprising) outcome?"



Common sense tells you the coin probably favors heads 70% of the time. MLE is the rigorous math proving your common sense is right.



**Step 1: The Likelihood Function ($L$)**

We write a formula for the probability of getting our exact data. If the probability of Heads is $p$, getting 7 Heads and 3 Tails means we multiply $p$ seven times, and $(1-p)$ three times.



**Step 2: The Log Trick (Log-Likelihood)**

Multiplying many tiny probabilities (like $0.5 \times 0.5 \times 0.5 \dots$) gives us microscopic numbers that computers struggle to calculate (this is called "underflow"). But here is a math cheat code: The peak of a graph is at the exact same location as the peak of the *logarithm* of that graph. Log turns messy multiplication into simple addition, which is much easier to do math on!



**Step 3: Finding the peak (Calculus)**

If you look at the Likelihood curve, it looks like a hill. To find the highest peak of a hill in calculus, we take the derivative (which measures the slope), set it to zero (a flat slope means we are exactly at the top), and solve for $p$.


  

$$\text{Likelihood: } L(p) = p^k (1-p)^{n-k} \\ \text{Log-Likelihood: } \ell(p) = k \log(p) + (n-k) \log(1-p)$$

> **Key Takeaway**
> MLE doesn't give you the absolute, universal truth. It just gives you the parameter that makes the data you *actually collected* the most statistically probable. If you flipped the coin only 3 times and got 3 heads, MLE would tell you $p=1.0$ (100% heads), which is why MLE requires lots of data to be reliable.

## Worked Example: Step-by-Step Proof: The Rigged Coin

1. **The Problem:** You flip a coin $n = 10$ times, and get $k = 7$ heads. Find the Maximum Likelihood Estimate for the probability of heads, $p$.
2. **Step 1: Write the Log-Likelihood equation.**
 $\ell(p) = 7 \log(p) + 3 \log(1-p)$
3. **Step 2: Take the derivative with respect to $p$.**
 The derivative of $\log(x)$ is $1/x$. So, taking the derivative gives us: 
 $\frac{d}{dp}\ell(p) = \frac{7}{p} - \frac{3}{1-p}$. 
*(Note: The minus sign comes from applying the chain rule to the $1-p$ term).*
4. **Step 3: Set to zero to find the peak of the hill.**
 $\frac{7}{p} - \frac{3}{1-p} = 0$
5. **Step 4: Solve for p with basic algebra.**
 Move the negative term over: $\frac{7}{p} = \frac{3}{1-p}$ 
 Cross multiply: $7(1-p) = 3p$ 
 Expand: $7 - 7p = 3p$ 
 Move $p$s to one side: $7 = 10p$ 
 **Answer:** $p = \frac{7}{10} = 0.7$.

## Visualizing the Concept

::: manim assets/videos/m1_mle.mp4 :::

*Visualizing the Likelihood 'Hill'. Watch how the peak perfectly aligns with the ratio of Heads to Total Tosses.*

::: toggle Variation Problem: What if we flip it 100 times?
If we flip a coin $n=100$ times and get $k=32$ heads, the math remains exactly the same. The derivative becomes $\frac{32}{p} - \frac{68}{1-p} = 0$. Solving this gives $32(1-p) = 68p$, which simplifies to $32 = 100p$, so $p = 0.32$. The beauty of MLE is that for a Bernoulli (coin toss) distribution, $\hat{p}_{MLE}$ will ALWAYS simplify to $\frac{k}{n}$.
:::

::: toggle Deep Dive: MLE for a Gaussian (Normal) Distribution
We just did MLE for a simple coin toss (Bernoulli). But what if you are measuring the heights of 1,000 students and want to find the MLE for the average height ($\mu$)? 

The math is longer because you use the bell curve formula instead of the coin toss formula, but the steps are IDENTICAL: 
1. Multiply the bell curve formulas together. 
2. Take the Logarithm. 
3. Take the derivative with respect to $\mu$ and set to zero. 

If you do this, the answer magically simplifies to $\hat{\mu}_{MLE} = \frac{1}{n}\sum x_i$ ... which is literally just the standard formula for an average!
:::

## Self Check

::: toggle Q1: Why do we take the derivative and set it to zero in MLE?
**Answer:** To find the highest point (maximum) of the likelihood curve

*Explanation:* In calculus, the derivative represents the slope of a curve. At the very peak of a hill, the ground is completely flat (slope = 0). Setting the derivative to 0 is how we mathematically pinpoint that maximum peak.
:::

::: toggle Q2: Why is the 'Log' (Log-Likelihood) step so important in computer science?
**Answer:** It turns a massive product of tiny probabilities into a sum, preventing computer underflow errors.

*Explanation:* Multiplying $0.5 \times 0.5$ hundreds of times creates a number too small for a computer to store (underflow). Taking the log turns that multiplication into addition ($log(0.5) + log(0.5)$), while keeping the peak in the exact same spot.
:::

::: toggle Q3: You roll a strange, rigged 6-sided die. Out of 100 rolls, it lands on the number 'Four' exactly 15 times. What is the MLE for the probability of rolling a 'Four'?
**Answer:** 0.15

*Explanation:* For this type of trial, the Maximum Likelihood Estimate is simply the observed frequency: $k/n$. Therefore, $15/100 = 0.15$.
:::

