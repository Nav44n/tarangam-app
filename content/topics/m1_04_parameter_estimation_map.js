window.addTopic(1, {
  id: "m1-parameter-estimation-map",
  title: "Parameter Estimation: Maximum A Posteriori (MAP)",
  dek: "MLE only trusts the data. MAP introduces 'common sense' by adding your prior beliefs to the equation.",
  theory: `
    <p>Remember MLE? If you flip a coin 3 times and get 3 heads, MLE strictly follows the math of the data and concludes the coin will land on heads 100% of the time ($p=1.0$). Your brain knows this is silly because you have a <strong>prior belief</strong> that coins are usually fair.</p>
    
    <p><strong>Maximum A Posteriori (MAP)</strong> fixes this naive behavior by combining two things using Bayes' Theorem:</p>
    <ol>
      <li><strong>The Likelihood:</strong> What the newly collected data is telling you (this is just the MLE part).</li>
      <li><strong>The Prior:</strong> What you firmly believed <em>before</em> you ever saw the data.</li>
    </ol>
    
    <p>MAP multiplies the Likelihood by the Prior to create a new curve called the <strong>Posterior</strong>, and then finds the peak of <em>that</em> new curve.</p>

    <p><strong>The Tug-of-War</strong><br>
    Think of MAP as a tug-of-war. The Prior pulls the guess towards your initial belief, while the Likelihood pulls it towards the new data. 
    <br><br>
    If you have very little data (e.g., 3 flips), the data is weak, so your Prior wins the tug-of-war. But if you have massive amounts of data (e.g., 10,000 flips), the data becomes overwhelming. The Likelihood pulls so hard that your Prior belief is completely ignored. Because of this, <strong>as you get infinite data, MAP becomes exactly equal to MLE.</strong></p>
  `,
  formula: `\\text{Posterior} \\propto \\text{Likelihood} \\times \\text{Prior} \\\\ \\hat{\\theta}_{MAP} = \\arg\\max_{\\theta} \\left[ \\log P(\\mathcal{D} \\mid \\theta) + \\log P(\\theta) \\right]`,
  callout: { 
    label: "The 'Virtual Data' Trick (Laplace Smoothing)", 
    text: "A very common way to apply a Prior in machine learning is by injecting 'virtual' or 'fake' data points before you even start calculating. For a coin, a prior belief that it is fair might look like secretly adding 2 Heads and 2 Tails to your total count. Now, if you flip 3 real Heads, your total becomes 5 Heads out of 7 total flips. The MAP estimate is $5/7 = 0.71$, which is much more reasonable than MLE's $3/3 = 1.0$!" 
  },
  worked: {
    title: "MAP with Virtual Counts (Beta Prior)",
    steps: [
      "<strong>The Problem:</strong> You run an e-commerce website. A brand new product gets exactly 1 rating, and it's a 5-star positive review. Using MLE, the product has a perfect 100% score. Use MAP to find a safer estimate, assuming a Prior belief of 2 positive and 2 negative reviews.",
      "<strong>Step 1: Identify the Likelihood (Real Data).</strong><br> Actual data: $k = 1$ positive rating out of $n = 1$ total ratings.",
      "<strong>Step 2: Identify the Prior (Virtual Data).</strong><br> Virtual data: $\\alpha = 2$ positive ratings, $\\beta = 2$ negative ratings. Total virtual ratings = 4.",
      "<strong>Step 3: Combine them (The Posterior).</strong><br> Total positive = $1 \\text{ (real)} + 2 \\text{ (virtual)} = 3$.<br> Total ratings = $1 \\text{ (real)} + 4 \\text{ (virtual)} = 5$.",
      "<strong>Step 4: Calculate the MAP estimate.</strong><br> $\\hat{p}_{MAP} = \\frac{3}{5} = 0.60$. <br><strong>Answer:</strong> The algorithm rates the product at 60% positive, protecting your store from ranking a product at #1 just because it got a single lucky review."
    ]
  },
  extra: [
    { 
      title: "Wait, isn't MAP just adding Regularization?", 
      body: "<strong>Yes!</strong> If you have studied L2 Regularization (Ridge) in linear regression, you have actually been doing MAP estimation without knowing it. <br><br>In machine learning, we often add a 'penalty' to our loss function to stop weights from getting too big (overfitting). Mathematically, assuming that your weights should be close to zero (a Gaussian Prior) and doing MAP estimation is <strong>exactly identical</strong> to doing MLE with an L2 Regularization penalty. The math equations are the same, just written in different fonts!" 
    }
  ],
  quiz: [
    { 
      q: "What happens to the MAP estimate as you gather an infinite amount of data?", 
      options: ["It becomes 1.0", "It becomes exactly equal to your Prior", "It becomes identical to the MLE estimate", "It drops to zero"], 
      answer: 2, 
      explain: "As the dataset grows infinitely large, the Likelihood function (the data) completely dominates the math, making the Prior mathematically insignificant. The data speaks for itself." 
    },
    { 
      q: "In Bayes' Theorem (used for MAP), what does the 'Prior' represent?", 
      options: ["The probability of the data given the parameters", "Our belief about the parameters before observing any data", "The denominator that normalizes the equation", "The final estimate after the data is observed"], 
      answer: 1, 
      explain: "The Prior represents our existing knowledge or assumptions (like 'most coins are fair' or 'most network weights should be small') before we even look at the new data." 
    },
    {
      q: "If MLE gives $p=1.0$ after 2 coin flips (2 Heads), what is the main reason MAP would give a lower estimate like $p=0.66$?",
      options: ["MAP factored in a prior belief that the coin is likely fair.", "MAP ignores the actual data.", "MLE cannot handle 2 coin flips.", "MAP always divides the MLE estimate by 2."],
      answer: 0,
      explain: "MAP tugs the naive MLE estimate (100% heads) closer to 50%, because the Prior belief introduces skepticism that a coin is perfectly rigged after only 2 flips."
    }
  ]
});