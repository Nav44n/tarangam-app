# Machine Learning vs Traditional Programming

**Why we stopped writing rules by hand and started letting computers figure them out.**


Welcome to Machine Learning! To understand what ML actually is, you first need to understand how we normally tell computers what to do.



**The Old Way: Traditional Programming**

Imagine you want a computer to bake a cake. In traditional programming, you have to provide two things:

  - **Data:** The raw ingredients (flour, sugar, eggs).
  - **Rules:** The exact, step-by-step recipe ("crack 2 eggs, bake at 350°F for 30 mins").

The computer blindly follows your rules, processes the data, and gives you the **Output** (the cake). If you want a chocolate cake instead, *you* have to write a completely new recipe.



**The New Way: Machine Learning**

Now, imagine you want the computer to bake a cake, but you have *no idea* how to write a recipe. Machine learning flips the process upside down. You provide two different things:

  - **Data:** The raw ingredients.
  - **Output:** 1,000 pictures of perfect, delicious cakes.

You feed the ingredients and the final cakes into the computer and say: *"Figure out the recipe yourself!"* The computer analyzes the data and the outputs, looks for patterns, and automatically generates the **Rules** (the recipe). This set of rules it generates is what we call a **"Model"**.


  

> **The Golden Equation**
> **Traditional:** Data + Rules = Output.
> **Machine Learning:** Data + Output = Rules (The Model).

## Worked Example: Step-by-Step Scenario: Building a Spam Filter

1. **The Goal:** Stop spam emails from reaching your inbox.
2. **Step 1 (Traditional Attempt):** A programmer writes a rule: `IF email contains 'Buy Viagra', THEN mark as Spam.`
3. **Step 2 (The Problem):** Spammers are smart. They change their emails to say 'Buy V1agra' or 'Buy V-i-a-g-r-a'. The programmer's rule fails. The programmer has to write 500 new rules to catch every spelling mistake. It becomes an endless, impossible game of whack-a-mole.
4. **Step 3 (The ML Solution):** Instead of writing rules, we use Machine Learning. We gather 10,000 emails. We manually label 5,000 as 'Spam' (Output) and 5,000 as 'Not Spam' (Output).
5. **Step 4 (Training):** We feed all 10,000 emails and their labels into an ML algorithm.
6. **Step 5 (The Result):** The computer analyzes the text and realizes on its own that words in ALL CAPS, suspicious links, and words like 'FREE' appearing together usually mean Spam. It writes its own complex mathematical rules to identify spam. We have successfully created a Spam Filter Model without writing a single 'IF' statement!

## Visualizing the Concept

::: manim assets/videos/m1_ml_vs_traditional.mp4 :::

*Visualizing the paradigm shift: Notice how the 'Rules' and 'Output' boxes swap places between the two approaches.*

::: toggle Deep Dive: When should you NOT use Machine Learning?
Machine Learning is powerful, but it is not magic. It is essentially just advanced pattern guessing. 

You should **never** use ML when the rules are simple, exact, and mathematically known. For example, building a calculator app or calculating an employee's income tax. The government provides exact, strict math rules for taxes. Using an AI to 'guess' someone's tax based on previous data would be unreliable, expensive, and legally dangerous.

**Rule of thumb:** Use traditional programming for exact logic. Use ML for 'fuzzy' logic (like recognizing speech, translating languages, or identifying objects in photos) where writing exact rules is impossible.
:::

## Self Check

::: toggle Q1: In the Machine Learning paradigm, what exactly is the algorithm producing as its final output?
**Answer:** The rules (a model) mapping inputs to outputs

*Explanation:* Unlike traditional programming which produces a final answer, ML produces the 'Rules' (the Model). This model can then be used on new, unseen data.
:::

::: toggle Q2: Which of the following problems is BEST suited for Traditional Programming rather than Machine Learning?
**Answer:** Calculating the 18% GST on a shopping cart total

*Explanation:* Calculating GST is a strict, exact mathematical formula (Total * 0.18). It requires 1 line of traditional code. Using ML for this would be highly inefficient and prone to error.
:::

::: toggle Q3: Why did traditional programming fail for tasks like Email Spam Filtering?
**Answer:** Spammers constantly adapt, making it impossible for humans to hand-write enough 'IF/THEN' rules to catch every variation

*Explanation:* The rules for what makes something 'spam' are fuzzy and constantly changing. Hand-coding strict rules for every possible spam variation is impossible.
:::


