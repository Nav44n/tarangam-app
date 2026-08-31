window.addTopic(1, {
  id: "m1-ml-vs-traditional",
  title: "Machine Learning vs Traditional Programming",
  dek: "Why we stopped writing rules by hand and started letting computers figure them out.",
  theory: `
    <p>Welcome to Machine Learning! To understand what ML actually is, you first need to understand how we normally tell computers what to do.</p>
    
    <p><strong>The Old Way: Traditional Programming</strong><br>
    Imagine you want a computer to bake a cake. In traditional programming, you have to provide two things:
    <ul>
      <li><strong>Data:</strong> The raw ingredients (flour, sugar, eggs).</li>
      <li><strong>Rules:</strong> The exact, step-by-step recipe ("crack 2 eggs, bake at 350°F for 30 mins").</li>
    </ul>
    The computer blindly follows your rules, processes the data, and gives you the <strong>Output</strong> (the cake). If you want a chocolate cake instead, <i>you</i> have to write a completely new recipe.</p>

    <p><strong>The New Way: Machine Learning</strong><br>
    Now, imagine you want the computer to bake a cake, but you have <i>no idea</i> how to write a recipe. Machine learning flips the process upside down. You provide two different things:
    <ul>
      <li><strong>Data:</strong> The raw ingredients.</li>
      <li><strong>Output:</strong> 1,000 pictures of perfect, delicious cakes.</li>
    </ul>
    You feed the ingredients and the final cakes into the computer and say: <em>"Figure out the recipe yourself!"</em> The computer analyzes the data and the outputs, looks for patterns, and automatically generates the <strong>Rules</strong> (the recipe). This set of rules it generates is what we call a <strong>"Model"</strong>.</p>
  `,
  callout: { 
    label: "The Golden Equation", 
    text: "<strong>Traditional:</strong> Data + Rules = Output.<br><strong>Machine Learning:</strong> Data + Output = Rules (The Model)." 
  },
  worked: {
    title: "Step-by-Step Scenario: Building a Spam Filter",
    steps: [
      "<strong>The Goal:</strong> Stop spam emails from reaching your inbox.",
      "<strong>Step 1 (Traditional Attempt):</strong> A programmer writes a rule: <code>IF email contains 'Buy Viagra', THEN mark as Spam.</code>",
      "<strong>Step 2 (The Problem):</strong> Spammers are smart. They change their emails to say 'Buy V1agra' or 'Buy V-i-a-g-r-a'. The programmer's rule fails. The programmer has to write 500 new rules to catch every spelling mistake. It becomes an endless, impossible game of whack-a-mole.",
      "<strong>Step 3 (The ML Solution):</strong> Instead of writing rules, we use Machine Learning. We gather 10,000 emails. We manually label 5,000 as 'Spam' (Output) and 5,000 as 'Not Spam' (Output).",
      "<strong>Step 4 (Training):</strong> We feed all 10,000 emails and their labels into an ML algorithm.",
      "<strong>Step 5 (The Result):</strong> The computer analyzes the text and realizes on its own that words in ALL CAPS, suspicious links, and words like 'FREE' appearing together usually mean Spam. It writes its own complex mathematical rules to identify spam. We have successfully created a Spam Filter Model without writing a single 'IF' statement!"
    ]
  },
  video: {
    script: "manim_scripts/m1_ml_vs_traditional.py",
    caption: "Visualizing the paradigm shift: Notice how the 'Rules' and 'Output' boxes swap places between the two approaches."
  },
  extra: [
    { 
      title: "Deep Dive: When should you NOT use Machine Learning?", 
      body: "Machine Learning is powerful, but it is not magic. It is essentially just advanced pattern guessing. <br><br>You should <strong>never</strong> use ML when the rules are simple, exact, and mathematically known. For example, building a calculator app or calculating an employee's income tax. The government provides exact, strict math rules for taxes. Using an AI to 'guess' someone's tax based on previous data would be unreliable, expensive, and legally dangerous.<br><br><strong>Rule of thumb:</strong> Use traditional programming for exact logic. Use ML for 'fuzzy' logic (like recognizing speech, translating languages, or identifying objects in photos) where writing exact rules is impossible." 
    }
  ],
  quiz: [
    { 
      q: "In the Machine Learning paradigm, what exactly is the algorithm producing as its final output?", 
      options: ["The raw data", "The rules (a model) mapping inputs to outputs", "A fixed lookup table", "The programmer's original source code"], 
      answer: 1, 
      explain: "Unlike traditional programming which produces a final answer, ML produces the 'Rules' (the Model). This model can then be used on new, unseen data." 
    },
    { 
      q: "Which of the following problems is BEST suited for Traditional Programming rather than Machine Learning?", 
      options: ["Identifying stop signs in self-driving car cameras", "Translating a paragraph from English to Malayalam", "Calculating the 18% GST on a shopping cart total", "Predicting which Netflix movie a user wants to watch next"], 
      answer: 2, 
      explain: "Calculating GST is a strict, exact mathematical formula (Total * 0.18). It requires 1 line of traditional code. Using ML for this would be highly inefficient and prone to error." 
    },
    {
      q: "Why did traditional programming fail for tasks like Email Spam Filtering?",
      options: ["Computers weren't fast enough", "Spammers constantly adapt, making it impossible for humans to hand-write enough 'IF/THEN' rules to catch every variation", "Emails take up too much storage space", "Traditional code cannot read text"],
      answer: 1,
      explain: "The rules for what makes something 'spam' are fuzzy and constantly changing. Hand-coding strict rules for every possible spam variation is impossible."
    }
  ]
});