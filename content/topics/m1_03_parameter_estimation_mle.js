window.addTopic(1, {
  id: "m1-parameter-estimation-mle",
  title: "Parameter Estimation: Maximum Likelihood Estimation (MLE)",
  dek: "A scary name for a simple question: 'What underlying rule makes the data I just saw the most probable?'",
  theory: `
    <p>Imagine you find a strange coin on the street. You flip it 10 times, and it lands on Heads 7 times. You ask yourself: <em>"Is this a fair 50/50 coin? Or is it rigged?"</em></p>
    
    <p><strong>Maximum Likelihood Estimation (MLE)</strong> is how a computer plays detective. It asks: "Out of all the possible biases this coin could have (maybe it favors heads 10% of the time, or 90% of the time), which bias makes getting exactly 7 heads the <em>most mathematically likely</em> (least surprising) outcome?"</p>
    
    <p>Common sense tells you the coin probably favors heads 70% of the time. MLE is the rigorous math proving your common sense is right.</p>

    <p><strong>Step 1: The Likelihood Function ($L$)</strong><br>
    We write a formula for the probability of getting our exact data. If the probability of Heads is $p$, getting 7 Heads and 3 Tails means we multiply $p$ seven times, and $(1-p)$ three times.</p>

    <p><strong>Step 2: The Log Trick (Log-Likelihood)</strong><br>
    Multiplying many tiny probabilities (like $0.5 \\times 0.5 \\times 0.5 \\dots$) gives us microscopic numbers that computers struggle to calculate (this is called "underflow"). But here is a math cheat code: The peak of a graph is at the exact same location as the peak of the <em>logarithm</em> of that graph. Log turns messy multiplication into simple addition, which is much easier to do math on!</p>
    
    <p><strong>Step 3: Finding the peak (Calculus)</strong><br>
    If you look at the Likelihood curve, it looks like a hill. To find the highest peak of a hill in calculus, we take the derivative (which measures the slope), set it to zero (a flat slope means we are exactly at the top), and solve for $p$.</p>
  `,
  formula: `\\text{Likelihood: } L(p) = p^k (1-p)^{n-k} \\\\ \\text{Log-Likelihood: } \\ell(p) = k \\log(p) + (n-k) \\log(1-p)`,
  worked: {
    title: "Step-by-Step Proof: The Rigged Coin",
    steps: [
      "<strong>The Problem:</strong> You flip a coin $n = 10$ times, and get $k = 7$ heads. Find the Maximum Likelihood Estimate for the probability of heads, $p$.",
      "<strong>Step 1: Write the Log-Likelihood equation.</strong><br> $\\ell(p) = 7 \\log(p) + 3 \\log(1-p)$",
      "<strong>Step 2: Take the derivative with respect to $p$.</strong><br> The derivative of $\\log(x)$ is $1/x$. So, taking the derivative gives us: <br> $\\frac{d}{dp}\\ell(p) = \\frac{7}{p} - \\frac{3}{1-p}$. <br><em>(Note: The minus sign comes from applying the chain rule to the $1-p$ term).</em>",
      "<strong>Step 3: Set to zero to find the peak of the hill.</strong><br> $\\frac{7}{p} - \\frac{3}{1-p} = 0$",
      "<strong>Step 4: Solve for p with basic algebra.</strong><br> Move the negative term over: $\\frac{7}{p} = \\frac{3}{1-p}$ <br> Cross multiply: $7(1-p) = 3p$ <br> Expand: $7 - 7p = 3p$ <br> Move $p$s to one side: $7 = 10p$ <br> <strong>Answer:</strong> $p = \\frac{7}{10} = 0.7$."
    ]
  },
  callout: { 
    label: "Key Takeaway", 
    text: "MLE doesn't give you the absolute, universal truth. It just gives you the parameter that makes the data you <em>actually collected</em> the most statistically probable. If you flipped the coin only 3 times and got 3 heads, MLE would tell you $p=1.0$ (100% heads), which is why MLE requires lots of data to be reliable." 
  },
  widget: "mle", // This activates the interactive React canvas widget you have in app.js!
  video: {
    script: "manim_scripts/m1_mle.py",
    caption: "Visualizing the Likelihood 'Hill'. Watch how the peak perfectly aligns with the ratio of Heads to Total Tosses."
  },
  extra: [
    {
      title: "Variation Problem: What if we flip it 100 times?",
      body: "If we flip a coin $n=100$ times and get $k=32$ heads, the math remains exactly the same. The derivative becomes $\\frac{32}{p} - \\frac{68}{1-p} = 0$. Solving this gives $32(1-p) = 68p$, which simplifies to $32 = 100p$, so $p = 0.32$. The beauty of MLE is that for a Bernoulli (coin toss) distribution, $\\hat{p}_{MLE}$ will ALWAYS simplify to $\\frac{k}{n}$."
    },
    {
      title: "Deep Dive: MLE for a Gaussian (Normal) Distribution",
      body: "We just did MLE for a simple coin toss (Bernoulli). But what if you are measuring the heights of 1,000 students and want to find the MLE for the average height ($\\mu$)? <br><br>The math is longer because you use the bell curve formula instead of the coin toss formula, but the steps are IDENTICAL: <br>1. Multiply the bell curve formulas together. <br>2. Take the Logarithm. <br>3. Take the derivative with respect to $\\mu$ and set to zero. <br><br>If you do this, the answer magically simplifies to $\\hat{\\mu}_{MLE} = \\frac{1}{n}\\sum x_i$ ... which is literally just the standard formula for an average!"
    }
  ],
  quiz: [
    { 
      q: "Why do we take the derivative and set it to zero in MLE?", 
      options: ["To minimize the error", "To find the highest point (maximum) of the likelihood curve", "Because logarithms require it", "To convert multiplication into addition"], 
      answer: 1, 
      explain: "In calculus, the derivative represents the slope of a curve. At the very peak of a hill, the ground is completely flat (slope = 0). Setting the derivative to 0 is how we mathematically pinpoint that maximum peak." 
    },
    {
      q: "Why is the 'Log' (Log-Likelihood) step so important in computer science?",
      options: ["Logarithms make the maximum value much larger.", "It turns a massive product of tiny probabilities into a sum, preventing computer underflow errors.", "It allows us to use Gaussian distributions.", "It changes where the peak of the curve is located."],
      answer: 1,
      explain: "Multiplying $0.5 \\times 0.5$ hundreds of times creates a number too small for a computer to store (underflow). Taking the log turns that multiplication into addition ($log(0.5) + log(0.5)$), while keeping the peak in the exact same spot."
    },
    {
      q: "You roll a strange, rigged 6-sided die. Out of 100 rolls, it lands on the number 'Four' exactly 15 times. What is the MLE for the probability of rolling a 'Four'?",
      options: ["1/6 (0.166)", "0.15", "0.85", "Not enough information"],
      answer: 1,
      explain: "For this type of trial, the Maximum Likelihood Estimate is simply the observed frequency: $k/n$. Therefore, $15/100 = 0.15$."
    }
  ]
});