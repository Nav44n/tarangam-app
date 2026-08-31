window.addTopic(1, {
  id: "m1-linear-regression-multiple-variables",
  title: "Linear Regression with Multiple Variables",
  dek: "What happens when house prices depend on size, bedrooms, AND age? We add more dimensions!",
  theory: `
    <p>In the previous topic, we predicted a house's price using just one variable: its size. But in the real world, price depends on many things: size ($x_1$), number of bedrooms ($x_2$), and age of the house ($x_3$).</p>
    
    <p>To handle this, we just make our equation longer. Instead of one slope ($w_1$), we give every feature its own weight (multiplier).<br>
    $\\hat{y} = w_0 + w_1x_1 + w_2x_2 + w_3x_3$<br>
    If $w_2$ (the bedroom weight) is high, it means bedrooms have a massive impact on the price.</p>

    <p><strong>How do we find all these weights at once? Two Methods:</strong></p>
    
    <p><strong>1. The Normal Equation (The Instant Math Formula)</strong><br>
    Calculus gives us a magical matrix formula that calculates the perfect weights instantly in one step. It's like finding the bottom of the error valley by just teleporting there. 
    <br><em>The Catch:</em> Matrix math is extremely heavy. If you have 100,000 features, calculating the Normal Equation will literally crash your computer's memory. It only works for small datasets.</p>

    <p><strong>2. Gradient Descent (The Blindfolded Hiker)</strong><br>
    Instead of teleporting, Gradient Descent takes small steps down the error valley. It slowly adjusts all the weights simultaneously until the error hits zero. It takes longer for small datasets, but it is the <em>only</em> method that works for massive, modern Machine Learning datasets with millions of features.</p>

    <p><strong>The Danger of Unscaled Data (Feature Scaling)</strong><br>
    Imagine $x_1$ is House Size (range: 1000 to 4000 sqft) and $x_2$ is Bedrooms (range: 1 to 5). The computer looks at these raw numbers and thinks "Size is 1,000 times larger, so it must be 1,000 times more important!" <br>
    This creates an elongated, stretched-out error valley. Gradient Descent will zig-zag wildly back and forth across the valley, taking forever to reach the bottom. <br>
    <strong>The Fix:</strong> We mathematically squish all features so they share the exact same scale (e.g., all numbers fall between -1 and 1). This makes the error valley a perfect circle, allowing Gradient Descent to step straight to the center instantly!</p>
  `,
  formula: `\\text{Model: } \\hat{y} = \\mathbf{w}^\\top \\mathbf{x} \\\\ \\text{Normal Equation: } \\mathbf{w} = (X^\\top X)^{-1}X^\\top \\mathbf{y} \\\\ \\text{Gradient Descent Update: } w_j = w_j - \\eta \\frac{1}{n} \\sum_{i=1}^n (\\hat{y}_i - y_i) x_{ij}`,
  worked: {
    title: "Scenario: Feature Scaling (Standardization)",
    steps: [
      "<strong>The Problem:</strong> You have a feature vector for a house: Size = 2000 sqft, Bedrooms = 3. Let's scale the 'Size' feature so it doesn't overwhelm the math.",
      "<strong>Step 1: Find the Mean (Average).</strong><br> You check your whole dataset and find the average house size is 1500 sqft ($\\mu = 1500$).",
      "<strong>Step 2: Find the Standard Deviation.</strong><br> The standard deviation (how spread out sizes are) is 500 sqft ($\\sigma = 500$).",
      "<strong>Step 3: Apply the Z-Score Standardization formula.</strong><br> $x_{scaled} = \\frac{x - \\mu}{\\sigma}$",
      "<strong>Step 4: Calculate.</strong><br> $x_{scaled} = \\frac{2000 - 1500}{500} = \\frac{500}{500} = 1.0$.",
      "<strong>Result:</strong> The massive number '2000' is now represented simply as '1.0' (meaning it is exactly 1 standard deviation above average). The algorithm can now compare it safely against small bedroom numbers!"
    ]
  },
  callout: { 
    label: "Vectors and Matrices", 
    text: "You will often see the formula written as $\\hat{y} = \\mathbf{w}^\\top \\mathbf{x}$. Don't let the linear algebra scare you! $\\mathbf{w}$ is just a vertical list of all your weights, and $\\mathbf{x}$ is a vertical list of your features. Multiplying them together with that 'T' (Transpose) symbol is just a shorthand programmer's trick to multiply them all out and add them up without writing a giant, ugly math equation." 
  },
  widget: "gd", // Triggers your interactive Gradient Descent visualizer
  video: {
    script: "manim_scripts/m1_08_multiple_regression.py",
    caption: "Watch how unscaled features cause Gradient Descent to zig-zag terribly, while scaled features allow it to step straight to the optimal solution."
  },
  extra: [
    { 
      title: "Deep Dive: The Learning Rate (Alpha/Eta)", 
      body: "In the Gradient Descent formula, $\\eta$ (often also written as $\\alpha$) is the Learning Rate. It controls the size of the steps the algorithm takes. If it's too small, training takes weeks. If it's too large, it takes a giant step, completely jumps over the minimum error at the bottom of the valley, and shoots up the other side! This is called 'divergence', and it causes your computer to spit out 'NaN' (Not a Number) errors." 
    }
  ],
  quiz: [
    { 
      q: "Why don't we just always use the Normal Equation to find the exact weights instantly?", 
      options: ["Because it is less accurate than Gradient Descent", "Because matrix inversion $(X^\\top X)^{-1}$ requires massive computational power and memory, crashing on large datasets", "Because it cannot handle multiple variables", "Because it requires feature scaling"], 
      answer: 1, 
      explain: "The computational complexity of inverting a matrix grows cubically. If you have 100,000 features, your computer has to do quadrillions of calculations, which is practically impossible for standard machines." 
    },
    { 
      q: "What visual effect does Feature Scaling have on the Gradient Descent 'Error Valley'?", 
      options: ["It turns it from an elongated, skewed oval into a symmetric, round bowl, allowing faster convergence", "It makes the valley deeper", "It turns the valley upside down", "It has no visual effect"], 
      answer: 0, 
      explain: "When features have vastly different scales, the cost surface stretches into an oval. Scaling them squishes the surface into a perfect circle, letting the algorithm walk straight to the center." 
    },
    {
      q: "In the multiple regression formula, we usually add a 'dummy' feature $x_0 = 1$. Why?",
      options: ["To prevent division by zero", "To represent the base price (the Y-intercept / bias term $w_0$)", "To scale the other features automatically", "Because matrices require an even number of columns"],
      answer: 1,
      explain: "By setting $x_0 = 1$, the term $w_0 \\times x_0$ simply becomes $w_0$. This is a mathematical trick to absorb the y-intercept (the bias) into the matrix multiplication, making the code much cleaner."
    }
  ]
});