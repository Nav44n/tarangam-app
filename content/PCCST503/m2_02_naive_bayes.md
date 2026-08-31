# Naive Bayes

**A probabilistic classifier based on applying Bayes' theorem with strong (naive) independence assumptions.**

Naive Bayes methods are a set of supervised learning algorithms based on applying Bayes' theorem with the "naive" assumption of conditional independence between every pair of features given the value of the class variable.

## Bayes' Theorem

Bayes' theorem provides a way of calculating posterior probability $P(c|x)$ from $P(c)$, $P(x)$ and $P(x|c)$:

$$ P(c|x) = rac{P(x|c)P(c)}{P(x)} $$

Where:
- $P(c|x)$ is the posterior probability of class $c$ given predictor $x$.
- $P(c)$ is the prior probability of class.
- $P(x|c)$ is the likelihood which is the probability of predictor given class.
- $P(x)$ is the prior probability of predictor.

## The "Naive" Assumption

The algorithm is called "naive" because it assumes that all features are independent of each other. Mathematically, for a feature vector $X = (x_1, x_2, \dots, x_n)$:

$$ P(X|c) = \prod_{i=1}^{n} P(x_i|c) $$

Despite this oversimplified assumption, Naive Bayes classifiers perform extremely well in many real-world situations, such as document classification and spam filtering.

## Self Check

::: toggle Q1: Why is the Naive Bayes algorithm called "naive"?
**Answer:** Because it assumes all features are independent.

*Explanation:* It assumes that the presence of a particular feature in a class is unrelated to the presence of any other feature, which is rarely true in the real world (e.g., in text, "machine" and "learning" often appear together).
:::
