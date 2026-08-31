window.addTopic(1, {
  id: "m1-loss-functions-optimization",
  title: "Loss Functions and Optimization",
  dek: "How a machine measures its own mistakes, and how it mathematically learns to fix them.",
  theory: `
    <p>We know that Machine Learning creates a rule (a Hypothesis function) to map inputs to outputs. But when a model is first born, it is completely stupid. It just guesses randomly. How does it get smarter?</p>
    
    <p><strong>1. The Loss Function (Measuring the Mistake)</strong><br>
    Imagine an archer shooting an arrow at a target. The bullseye is the actual true answer ($y$). The spot where the arrow actually hits is the model's prediction ($\\hat{y}$). The distance between the arrow and the bullseye is the <strong>Loss</strong>.<br><br>
    A Loss Function is a mathematical formula that calculates exactly how "wrong" a single prediction is.
    <ul>
      <li><strong>For Regression (Predicting Numbers):</strong> We usually use <em>Squared Error</em>. If the house costs $100k, and the model guesses $80k, the error is 20k. We square it to heavily penalize really big mistakes.</li>
      <li><strong>For Classification (Predicting Categories):</strong> We use <em>Cross-Entropy (Log Loss)</em>. It heavily penalizes the model if it is extremely confident about the wrong answer (e.g., saying "I am 99% sure this is a dog" when it's actually a cat).</li>
    </ul></p>

    <p><strong>2. Cost Function / Empirical Risk (The Total Mistake)</strong><br>
    "Loss" is for one single example. The <strong>Cost Function</strong> (also called Empirical Risk, $J$) is simply the <em>average</em> of all the losses across the entire training dataset. The ultimate goal of Machine Learning is to find the parameters (weights) that make this Cost Function as close to zero as possible.</p>

    <p><strong>3. Optimization (Fixing the Mistake)</strong><br>
    How do we get the Cost to zero? Imagine a blindfolded hiker dropped on the side of a mountain. Their goal is to get to the very bottom of the valley (zero error). 
    <ul>
      <li>They feel the ground with their feet to see which way is downhill. This slope is called the <strong>Gradient</strong> (the derivative of the cost function).</li>
      <li>They take a step in the steepest downhill direction.</li>
      <li>This step-by-step process of walking down the error mountain is called <strong>Gradient Descent</strong>—the most famous optimization algorithm in all of AI!</li>
    </ul></p>
  `,
  formula: `\\text{Loss (Single): } L(y_i, \\hat{y}_i) = (y_i - \\hat{y}_i)^2 \\\\ \\text{Cost / Risk (Total): } J(\\theta) = \\frac{1}{n} \\sum_{i=1}^{n} L(y_i, \\hat{y}_i) \\\\ \\text{Optimization Step: } \\theta_{new} = \\theta_{old} - \\eta \\nabla J(\\theta)`,
  worked: {
    title: "Step-by-Step Scenario: Calculating the Cost (MSE)",
    steps: [
      "<strong>The Problem:</strong> You have a tiny dataset of 3 students. You try to predict their test scores out of 100. Calculate the Mean Squared Error (MSE) Cost for your model.",
      "<strong>True Scores ($y$):</strong> [80, 90, 70]",
      "<strong>Model's Predictions ($\\hat{y}$):</strong> [75, 90, 78]",
      "<strong>Step 1: Calculate the individual errors ($y - \\hat{y}$).</strong><br>Student 1: $80 - 75 = 5$<br>Student 2: $90 - 90 = 0$<br>Student 3: $70 - 78 = -8$",
      "<strong>Step 2: Square the errors.</strong> (This gets rid of negative signs and punishes the big mistake of Student 3).<br>Student 1: $5^2 = 25$<br>Student 2: $0^2 = 0$<br>Student 3: $(-8)^2 = 64$",
      "<strong>Step 3: Find the Average (Mean) to get the final Cost $J$.</strong><br>$J = \\frac{25 + 0 + 64}{3} = \\frac{89}{3} \\approx 29.67$.",
      "<strong>Result:</strong> Your model's total Cost is 29.67. To 'learn', the optimization algorithm will now adjust its internal weights to try and make this number smaller!"
    ]
  },
  callout: { 
    label: "What is η (Eta)?", 
    text: "In the Optimization formula, $\\eta$ is the <strong>Learning Rate</strong>. It controls the <em>size</em> of the step the blindfolded hiker takes. If $\\eta$ is too small, the AI takes days to learn. If $\\eta$ is too big, the AI takes giant leaps and might accidentally jump entirely over the valley, completely failing to learn!" 
  },
  extra: [
    { 
      title: "Deep Dive: Convex vs. Non-Convex Mountains", 
      body: "Not all Cost Functions look like a perfect, smooth salad bowl (a <strong>Convex</strong> shape). Simple algorithms like Linear Regression have convex cost functions, meaning there is only one true bottom (Global Minimum).<br><br>Deep Neural Networks have <strong>Non-Convex</strong> cost functions. The landscape looks like a bumpy mountain range with hundreds of fake valleys (Local Minima). The blindfolded hiker might walk into a shallow crater, think they've reached the absolute bottom, and stop learning, even though a much deeper valley is just over the next hill! This is why training complex AI models is so difficult." 
    }
  ],
  video: {
    script: "manim_scripts/m1_06_optimization.py",
    caption: "Watch the 'Blindfolded Hiker' concept in action. A model (the dot) calculates its gradient (the slope) and takes steps down the Cost Bowl toward the minimum error."
  },
  quiz: [
    { 
      q: "What is the primary difference between a 'Loss Function' and a 'Cost Function'?", 
      options: ["Loss is for Regression, Cost is for Classification.", "Loss measures the error of ONE single prediction. Cost measures the average error across the ENTIRE dataset.", "They are exactly the same thing in every context.", "Cost is used before training, Loss is used after training."], 
      answer: 1, 
      explain: "Loss is calculated per-example. Cost (or Empirical Risk) aggregates all the individual losses to evaluate the model's overall performance on the dataset." 
    },
    { 
      q: "If you are trying to predict the exact price of a used car, which Loss function should you use?", 
      options: ["0-1 Loss", "Cross-Entropy Loss", "Squared Error (MSE)"], 
      answer: 2, 
      explain: "Predicting a continuous number like a price is a Regression problem. Squared Error is the standard loss function for regression. The others are for Classification." 
    },
    {
      q: "In Gradient Descent, what determines how large a 'step' the algorithm takes down the error mountain?",
      options: ["The number of data points", "The Learning Rate (Eta)", "The size of the dataset", "The Y-intercept"],
      answer: 1,
      explain: "The Learning Rate ($\\eta$) is a hyperparameter that scales the gradient to determine exactly how big the update step will be."
    }
  ]
});