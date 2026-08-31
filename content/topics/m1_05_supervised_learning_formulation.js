window.addTopic(1, {
  id: "m1-supervised-learning-formulation",
  title: "Feature Representation & Problem Formulation",
  dek: "How to translate the messy real world into a language of numbers that math can understand.",
  theory: `
    <p>Algorithms cannot "see" a house, "read" an email, or "look" at a patient. Algorithms only understand one thing: <strong>Numbers</strong>.</p>
    
    <p>Before we can do any Machine Learning, we must translate the real-world object into a list of numbers. This list of numbers is called a <strong>Feature Vector</strong> ($x$). Every individual trait we measure is called a <strong>Feature</strong>.</p>

    <p><strong>1. Feature Representation (The Translation)</strong><br>
    Imagine you are describing a suspect to a police sketch artist. You don't just say "a guy." You break him down into features: Height (numeric), Eye Color (category), Age (numeric). In ML, we do the exact same thing:
    <ul>
      <li><strong>Continuous Features:</strong> Things you can measure (e.g., Age = 25, Salary = 50000.50, House Size = 1500 sqft).</li>
      <li><strong>Categorical Features:</strong> Things that fall into buckets (e.g., Color = Red, City = Kochi, Blood Type = O+).</li>
    </ul>
    Since computers can't do math on the word "Red", we have to convert categories into numbers. A bad way is assigning Red=1, Green=2, Blue=3 (because the computer will think Blue is 3 times "greater" than Red). The correct way is <strong>One-Hot Encoding</strong>.</p>

    <p><strong>2. Problem Formulation (The Formal Setup)</strong><br>
    Once we have our features, we mathematically define the supervised learning problem using specific symbols. Don't let them scare you; they are just shorthand for simple concepts:
    <ul>
      <li><strong>Input Space ($\\mathcal{X}$):</strong> The set of all possible feature vectors (e.g., all possible houses). Let's call a single house $x$.</li>
      <li><strong>Output Space ($\\mathcal{Y}$):</strong> What we are trying to predict. If $\\mathcal{Y}$ is continuous (like Price = $50,000), it's a <strong>Regression</strong> problem. If $\\mathcal{Y}$ is a set of buckets (like {Spam, Not Spam}), it's a <strong>Classification</strong> problem. Let's call a single answer $y$.</li>
      <li><strong>Dataset ($\\mathcal{D}$):</strong> Your historical data. A list of pairs: $\\{(x_1, y_1), (x_2, y_2), \\dots\\}$. (e.g., House 1 and its Price, House 2 and its Price).</li>
      <li><strong>Hypothesis ($f$ or $h$):</strong> The function or "rule" the computer learns. Our goal is to find a function where $f(x) \\approx y$ (the prediction matches the real answer).</li>
    </ul></p>
  `,
  formula: `\\text{Dataset: } \\mathcal{D} = \\{(x_1, y_1), (x_2, y_2), \\dots, (x_n, y_n)\\} \\\\ \\text{Goal: Find } f: \\mathcal{X} \\to \\mathcal{Y} \\text{ such that } f(x_i) \\approx y_i`,
  worked: {
    title: "Step-by-Step Scenario: One-Hot Encoding a Used Car",
    steps: [
      "<strong>The Problem:</strong> You want an algorithm to predict the price of a used car. The car is a 2018 model, driven 50,000 km, and the Color is 'Red'. Create its Feature Vector $x$.",
      "<strong>Step 1: Identify Continuous Features.</strong><br> Age = 2024 - 2018 = 6 years. Mileage = 50,000. These are already numbers. Great!",
      "<strong>Step 2: Identify Categorical Features.</strong><br> Color = 'Red'. We know the possible colors in our dataset are {Red, Green, Blue}.",
      "<strong>Step 3: Apply One-Hot Encoding.</strong><br> Instead of 1 column for color, we create 3 binary (0 or 1) columns: <em>Is_Red</em>, <em>Is_Green</em>, <em>Is_Blue</em>.",
      "<strong>Step 4: Translate the car's color.</strong><br> Since the car is Red, <em>Is_Red</em> = 1, <em>Is_Green</em> = 0, <em>Is_Blue</em> = 0.",
      "<strong>Step 5: Assemble the final Feature Vector $x$.</strong><br> $x = [6, 50000, 1, 0, 0]$. This list of 5 numbers is what the algorithm actually 'sees'!"
    ]
  },
  callout: { 
    label: "Why is it called a 'Hypothesis'?", 
    text: "In science, a hypothesis is an educated guess. In ML, until the model sees *all* data in the universe (which is impossible), the rules it generates are just a very good 'guess' at how the universe works. Therefore, the function $f(x)$ is often called a Hypothesis $h(x)$." 
  },
  extra: [
    { 
      title: "Deep Dive: The Danger of Feature Scaling", 
      body: "Look at our car vector: $[6, 50000, 1, 0, 0]$. The mileage (50,000) is a massive number compared to the age (6). Many ML algorithms (like Gradient Descent or KNN) will look at this and mathematically assume that Mileage is 10,000 times more important than Age just because the number is bigger!<br><br>To fix this, we apply <strong>Feature Scaling (Normalization or Standardization)</strong>. We squish all features so they live on the same scale, like between 0 and 1, or giving them a mean of 0 and variance of 1. This levels the playing field so the algorithm judges features on their actual pattern, not their raw size." 
    },
    {
      title: "Problem Variation: Identifying X and Y",
      body: "Let's practice Formulation. <br><strong>Scenario:</strong> Given a student's hours studied and attendance percentage, predict if they will Pass or Fail.<br><ul><li><strong>Input $x$:</strong> $[\\text{Hours}, \\text{Attendance}]$</li><li><strong>Input Space $\\mathcal{X}$:</strong> $\\mathbb{R}^2$ (A 2-dimensional vector of real numbers)</li><li><strong>Output $y$:</strong> Pass or Fail</li><li><strong>Output Space $\\mathcal{Y}$:</strong> $\\{0, 1\\}$ (Discrete categories)</li><li><strong>Problem Type:</strong> Binary Classification</li></ul>"
    }
  ],
  video: {
    script: "manim_scripts/m1_05_formulation.py",
    caption: "Watch how a real-world house is translated into a vector, and passed through a Hypothesis function to output a price prediction."
  },
  quiz: [
    { 
      q: "If you have a categorical feature 'City' with 4 possible values (Kochi, Trivandrum, Kozhikode, Calicut), how many new columns will One-Hot Encoding create?", 
      options: ["1 column with values 1 to 4", "4 separate columns", "0 columns (it deletes the feature)", "2 columns"], 
      answer: 1, 
      explain: "One-Hot Encoding creates one new binary column for every possible category. So 4 cities = 4 new columns (Is_Kochi, Is_Trivandrum, etc)." 
    },
    { 
      q: "In the formal mathematical notation of ML, what does $\\mathcal{D} = \\{(x_1, y_1), \\dots\\}$ represent?", 
      options: ["The unlabelled test data", "The set of all possible mathematical functions", "The labelled historical training dataset", "The One-Hot Encoded matrix"], 
      answer: 2, 
      explain: "The script $\\mathcal{D}$ stands for Dataset. The pairs $(x_i, y_i)$ mean it contains both the input features ($x$) and the correct output labels ($y$)." 
    },
    {
      q: "Why is assigning 'Red=1, Green=2, Blue=3' a bad idea for most Machine Learning algorithms?",
      options: ["Algorithms cannot read the number 3", "It implies a mathematical order (that Blue is 'greater' or 'more' than Red) which is false", "It takes up too much memory", "Red is always supposed to be 0"],
      answer: 1,
      explain: "Categories usually have no natural numeric order. If you use 1, 2, 3, the algorithm might think Blue (3) is the 'average' of Red (1) and some other color, which makes no logical sense."
    }
  ]
});