window.addTopic(1, {
  id: "m1-linear-regression-one-variable",
  title: "Linear Regression with One Variable",
  dek: "Drawing the perfect straight line through a scatter of points to predict the future.",
  theory: `
    <p>Imagine you have a blank piece of paper. On the horizontal axis (X), you put <strong>House Size</strong>. On the vertical axis (Y), you put <strong>House Price</strong>. You plot 5 houses you recently saw for sale. The dots roughly go from the bottom-left to the top-right.</p>
    
    <p>If your friend asks, <em>"How much would a 2000 sqft house cost?"</em>, what do you do? Your brain naturally draws an imaginary straight line right through the middle of those dots, finds 2000 on the X-axis, and looks at where it hits your imaginary line on the Y-axis. <strong>That is Linear Regression!</strong></p>

    <p><strong>1. The Math of a Line</strong><br>
    In high school, you learned the equation of a straight line is $y = mx + c$ (where $m$ is the slope and $c$ is where the line hits the Y-axis). In Machine Learning, we just change the letters to make it sound fancier:
    <br><br>
    $\\hat{y} = w_0 + w_1x$
    <ul>
      <li>$\\hat{y}$ (y-hat): The <em>predicted</em> price of the house.</li>
      <li>$x$: The input feature (Size of the house).</li>
      <li>$w_1$ (Weight): The slope. (e.g., How much the price goes up for every 1 extra sqft).</li>
      <li>$w_0$ (Bias): The Y-intercept. (e.g., The base price of a plot of land before any house is built on it).</li>
    </ul></p>

    <p><strong>2. Ordinary Least Squares (OLS)</strong><br>
    You can draw a million different lines through your dots. How does the computer know which one is the "Best Fit"? <br>
    For any line you draw, measure the vertical distance from each real dot to your line. This gap is the <strong>Error (or Residual)</strong>. The computer squares every single error (to get rid of negative numbers and heavily punish giant mistakes), and adds them all up. The line that produces the absolute lowest total sum is the winner. This is called the <strong>Least Squares</strong> method.</p>
  `,
  formula: `\\text{Model: } \\hat{y} = w_0 + w_1x \\\\ \\text{Cost Function (MSE): } J(w_0,w_1) = \\frac{1}{2n}\\sum_{i=1}^n (\\hat{y}_i - y_i)^2 \\\\ \\text{To find the best line instantly: } w_1 = \\frac{\\sum (x_i-\\bar{x})(y_i-\\bar{y})}{\\sum (x_i - \\bar{x})^2}, \\quad w_0 = \\bar{y} - w_1\\bar{x}`,
  worked: {
    title: "Step-by-Step Scenario: Finding the Best Fit Line Manually",
    steps: [
      "<strong>The Problem:</strong> You have a tiny dataset of 3 houses. Size $x = [1, 2, 3]$. Price $y = [2, 4, 5]$. Find the perfect straight line ($w_1$ and $w_0$) using the Least Squares formula.",
      "<strong>Step 1: Find the Averages (Means).</strong><br> Average of $x$ ($\\bar{x}$) $= (1+2+3)/3 = 2$.<br> Average of $y$ ($\\bar{y}$) $= (2+4+5)/3 = 3.67$.",
      "<strong>Step 2: Calculate the Deviations for the Numerator.</strong><br> Subtract the mean from each $x$ and $y$, then multiply them together: $(x_i - \\bar{x}) \\times (y_i - \\bar{y})$.<br> House 1: $(1 - 2) \\times (2 - 3.67) = (-1) \\times (-1.67) = 1.67$<br> House 2: $(2 - 2) \\times (4 - 3.67) = (0) \\times (0.33) = 0$<br> House 3: $(3 - 2) \\times (5 - 3.67) = (1) \\times (1.33) = 1.33$<br> <em>Sum of Numerator:</em> $1.67 + 0 + 1.33 = 3.0$.",
      "<strong>Step 3: Calculate the Denominator.</strong><br> Square the $x$ deviations: $(x_i - \\bar{x})^2$.<br> House 1: $(-1)^2 = 1$<br> House 2: $(0)^2 = 0$<br> House 3: $(1)^2 = 1$<br> <em>Sum of Denominator:</em> $1 + 0 + 1 = 2.0$.",
      "<strong>Step 4: Find the Slope ($w_1$).</strong><br> $w_1 = \\text{Numerator} / \\text{Denominator} = 3.0 / 2.0 = 1.5$.",
      "<strong>Step 5: Find the Intercept ($w_0$).</strong><br> $w_0 = \\bar{y} - w_1\\bar{x} = 3.67 - (1.5 \\times 2) = 3.67 - 3.0 = 0.67$.",
      "<strong>Result:</strong> Your perfectly fitted Machine Learning model is: <strong>$\\hat{y} = 0.67 + 1.5x$</strong>. You can now plug any new house size ($x$) into this formula to predict its price!"
    ]
  },
  callout: { 
    label: "Why Square the Errors?", 
    text: "Why don't we just take the absolute value of the errors? 1. Squaring heavily punishes the model if it is <em>way</em> off on a single point, forcing the line to stay closer to the middle. 2. A squared curve forms a smooth 'bowl' shape (a parabola). In calculus, a smooth bowl has a single, easily calculable bottom point (global minimum). Absolute values have a sharp 'V' shape which makes the calculus harder!" 
  },
  extra: [
    { 
      title: "Deep Dive: Interpolation vs Extrapolation", 
      body: "Linear Regression is great at <strong>Interpolation</strong> (predicting values inside the range of your training data). If you train a model on houses between 1,000 and 3,000 sqft, it will accurately predict a 2,000 sqft house.<br><br>However, it is terrible at <strong>Extrapolation</strong> (predicting values way outside the training data). If you use that same model to predict the price of a 10 sqft dog house, or a 1,000,000 sqft mega-mansion, the straight line will give you completely absurd, mathematically incorrect real-world prices. Always be careful using a model outside its comfort zone!" 
    }
  ],
  video: {
    script: "manim_scripts/m1_07_linear_regression.py",
    caption: "Watch how the computer tests different lines, measures the vertical 'errors' (red lines), and adjusts until those errors are minimized."
  },
  quiz: [
    { 
      q: "In the Linear Regression equation $\\hat{y} = w_0 + w_1x$, what does $w_0$ represent physically on a graph?", 
      options: ["The steepness of the line", "The Y-intercept (where the line crosses the vertical axis)", "The X-intercept", "The average error"], 
      answer: 1, 
      explain: "$w_0$ is the bias or Y-intercept. It is the predicted value of $\\hat{y}$ when the input $x$ is exactly 0." 
    },
    { 
      q: "When finding the 'Best Fit' line, what exactly is the Ordinary Least Squares method trying to minimize?", 
      options: ["The number of data points", "The slope of the line", "The sum of the squared vertical distances between the real data points and the predicted line", "The sum of the X values"], 
      answer: 2, 
      explain: "Least Squares calculates the vertical gap (error) between each real dot and the line, squares it, adds them all up, and finds the line that makes that total sum the smallest possible." 
    },
    {
      q: "Why do we prefer squaring the errors instead of simply taking the absolute value?",
      options: ["Because squares result in smaller numbers", "Because squares create a smooth, convex 'bowl' shape that is easy to optimize using calculus", "Because absolute values cannot be calculated by computers", "Because squares allow for negative predictions"],
      answer: 1,
      explain: "Squared errors ($x^2$) form a smooth, continuous, differentiable parabola. This makes finding the mathematical minimum (the bottom of the bowl) much easier than the sharp corner created by absolute values ($|x|$)."
    }
  ]
});