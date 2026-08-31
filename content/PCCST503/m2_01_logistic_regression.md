# Logistic Regression

**A probabilistic approach to binary classification using the logistic sigmoid function.**

While Linear Regression is suited for predicting continuous values, it fails when applied to classification tasks. **Logistic Regression** is a classification algorithm used to assign observations to a discrete set of classes. Unlike linear regression which outputs continuous number values, logistic regression transforms its output using the logistic sigmoid function to return a probability value which can then be mapped to two or more discrete classes.

## The Sigmoid Function

To map predicted values to probabilities, we use the Sigmoid function. The function maps any real value into another value between 0 and 1. In machine learning, we use sigmoid to map predictions to probabilities.

$$ \sigma(z) = \frac{1}{1 + e^{-z}} $$

Where:
- $\sigma(z)$ is the output between 0 and 1 (probability estimate)
- $z$ is the input to the function (your algorithm's prediction e.g. $mx + b$)
- $e$ is the base of natural log

## Visualizing the Concept

::: manim assets/videos/m2_logistic_sigmoid.mp4 :::

*The Sigmoid Activation Function shaping the decision boundary.*

## Decision Boundary

We expect our classifier to give us a set of outputs or classes based on probability when we pass the inputs through a prediction function and returns a probability score between 0 and 1. 

For example, if we have a binary classification problem (e.g. spam or not spam), we can set a threshold value (decision boundary) of 0.5. 

$$ \hat{y} = \begin{cases} 1 & \text{if } p \geq 0.5 \\ 0 & \text{if } p < 0.5 \end{cases} $$

## Cost Function (Log Loss)

We cannot use the Mean Squared Error (MSE) cost function for Logistic Regression because the Sigmoid function causes the cost function to become non-convex, meaning it has multiple local minimums, making it difficult for gradient descent to find the global minimum. 

Instead, we use **Cross-Entropy** (also known as Log Loss):

$$ J(\theta) = -\frac{1}{m} \sum_{i=1}^{m} [y^{(i)} \log(h_\theta(x^{(i)})) + (1 - y^{(i)}) \log(1 - h_\theta(x^{(i)}))] $$

This cost function guarantees a convex optimization landscape.

## Self Check

::: toggle Q1: Why is MSE not suitable for Logistic Regression?
**Answer:** It makes the cost function non-convex.

*Explanation:* Because of the non-linear sigmoid transformation, applying MSE creates a wavy, non-convex error surface with multiple local minima. Cross-entropy ensures a convex surface where gradient descent can easily find the global minimum.
:::

::: toggle Q2: If the sigmoid output is 0.8 and our threshold is 0.5, what is the predicted class?
**Answer:** Class 1.

*Explanation:* Since 0.8 is strictly greater than the decision boundary threshold of 0.5, the model will confidently predict the positive class (1).
:::
