# Linear Regression with One Variable

**Drawing the perfect straight line through a scatter of points to predict the future.**


Imagine you have a blank piece of paper. On the horizontal axis (X), you put **House Size**. On the vertical axis (Y), you put **House Price**. You plot 5 houses you recently saw for sale. The dots roughly go from the bottom-left to the top-right.



If your friend asks, *"How much would a 2000 sqft house cost?"*, what do you do? Your brain naturally draws an imaginary straight line right through the middle of those dots, finds 2000 on the X-axis, and looks at where it hits your imaginary line on the Y-axis. **That is Linear Regression!**



**1. The Math of a Line**

In high school, you learned the equation of a straight line is $y = mx + c$ (where $m$ is the slope and $c$ is where the line hits the Y-axis). In Machine Learning, we just change the letters to make it sound fancier:



$\hat{y} = w_0 + w_1x$

  - $\hat{y}$ (y-hat): The *predicted* price of the house.
  - $x$: The input feature (Size of the house).
  - $w_1$ (Weight): The slope. (e.g., How much the price goes up for every 1 extra sqft).
  - $w_0$ (Bias): The Y-intercept. (e.g., The base price of a plot of land before any house is built on it).




**2. Ordinary Least Squares (OLS)**

You can draw a million different lines through your dots. How does the computer know which one is the "Best Fit"? 

For any line you draw, measure the vertical distance from each real dot to your line. This gap is the **Error (or Residual)**. The computer squares every single error (to get rid of negative numbers and heavily punish giant mistakes), and adds them all up. The line that produces the absolute lowest total sum is the winner. This is called the **Least Squares** method.


  

$$\text{Model: } \hat{y} = w_0 + w_1x \\ \text{Cost Function (MSE): } J(w_0,w_1) = \frac{1}{2n}\sum_{i=1}^n (\hat{y}_i - y_i)^2 \\ \text{To find the best line instantly: } w_1 = \frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum (x_i - \bar{x})^2}, \quad w_0 = \bar{y} - w_1\bar{x}$$

> **Why Square the Errors?**
> Why don't we just take the absolute value of the errors? 1. Squaring heavily punishes the model if it is *way* off on a single point, forcing the line to stay closer to the middle. 2. A squared curve forms a smooth 'bowl' shape (a parabola). In calculus, a smooth bowl has a single, easily calculable bottom point (global minimum). Absolute values have a sharp 'V' shape which makes the calculus harder!

## Worked Example: Step-by-Step Scenario: Finding the Best Fit Line Manually

1. **The Problem:** You have a tiny dataset of 3 houses. Size $x = [1, 2, 3]$. Price $y = [2, 4, 5]$. Find the perfect straight line ($w_1$ and $w_0$) using the Least Squares formula.
2. **Step 1: Find the Averages (Means).**
 Average of $x$ ($\bar{x}$) $= (1+2+3)/3 = 2$.
 Average of $y$ ($\bar{y}$) $= (2+4+5)/3 = 3.67$.
3. **Step 2: Calculate the Deviations for the Numerator.**
 Subtract the mean from each $x$ and $y$, then multiply them together: $(x_i - \bar{x}) \times (y_i - \bar{y})$.
 House 1: $(1 - 2) \times (2 - 3.67) = (-1) \times (-1.67) = 1.67$
 House 2: $(2 - 2) \times (4 - 3.67) = (0) \times (0.33) = 0$
 House 3: $(3 - 2) \times (5 - 3.67) = (1) \times (1.33) = 1.33$
 *Sum of Numerator:* $1.67 + 0 + 1.33 = 3.0$.
4. **Step 3: Calculate the Denominator.**
 Square the $x$ deviations: $(x_i - \bar{x})^2$.
 House 1: $(-1)^2 = 1$
 House 2: $(0)^2 = 0$
 House 3: $(1)^2 = 1$
 *Sum of Denominator:* $1 + 0 + 1 = 2.0$.
5. **Step 4: Find the Slope ($w_1$).**
 $w_1 = \text{Numerator} / \text{Denominator} = 3.0 / 2.0 = 1.5$.
6. **Step 5: Find the Intercept ($w_0$).**
 $w_0 = \bar{y} - w_1\bar{x} = 3.67 - (1.5 \times 2) = 3.67 - 3.0 = 0.67$.
7. **Result:** Your perfectly fitted Machine Learning model is: **$\hat{y} = 0.67 + 1.5x$**. You can now plug any new house size ($x$) into this formula to predict its price!

## Visualizing the Concept

::: manim assets/videos/m1_07_linear_regression.mp4 :::

*Watch how the computer tests different lines, measures the vertical 'errors' (red lines), and adjusts until those errors are minimized.*

::: toggle Deep Dive: Interpolation vs Extrapolation
Linear Regression is great at **Interpolation** (predicting values inside the range of your training data). If you train a model on houses between 1,000 and 3,000 sqft, it will accurately predict a 2,000 sqft house.

However, it is terrible at **Extrapolation** (predicting values way outside the training data). If you use that same model to predict the price of a 10 sqft dog house, or a 1,000,000 sqft mega-mansion, the straight line will give you completely absurd, mathematically incorrect real-world prices. Always be careful using a model outside its comfort zone!
:::

## Self Check

::: toggle Q1: In the Linear Regression equation $\hat{y} = w_0 + w_1x$, what does $w_0$ represent physically on a graph?
**Answer:** The Y-intercept (where the line crosses the vertical axis)

*Explanation:* $w_0$ is the bias or Y-intercept. It is the predicted value of $\hat{y}$ when the input $x$ is exactly 0.
:::

::: toggle Q2: When finding the 'Best Fit' line, what exactly is the Ordinary Least Squares method trying to minimize?
**Answer:** The sum of the squared vertical distances between the real data points and the predicted line

*Explanation:* Least Squares calculates the vertical gap (error) between each real dot and the line, squares it, adds them all up, and finds the line that makes that total sum the smallest possible.
:::

::: toggle Q3: Why do we prefer squaring the errors instead of simply taking the absolute value?
**Answer:** Because squares create a smooth, convex 'bowl' shape that is easy to optimize using calculus

*Explanation:* Squared errors ($x^2$) form a smooth, continuous, differentiable parabola. This makes finding the mathematical minimum (the bottom of the bowl) much easier than the sharp corner created by absolute values ($|x|$).
:::

