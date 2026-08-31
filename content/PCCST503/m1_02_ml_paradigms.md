# The 4 ML Paradigms: How Computers Learn

**Supervised, Unsupervised, Semi-supervised, and Reinforcement Learning explained simply.**


Just like humans learn differently depending on the situation, machines have four main 'learning styles'. Let's break them down for an absolute beginner:



**1. Supervised Learning (Learning with a Teacher)**

Imagine a teacher showing you flashcards. One side has a picture of an apple (the input, $x$), the other side says "Apple" (the label, $y$). You are given the data AND the exact answers. The computer makes a guess, checks the answer key, and corrects itself. 

*Use case:* Predicting house prices (you train it on houses that already have known prices) or diagnosing diseases from X-rays.



**2. Unsupervised Learning (Learning by Finding Patterns)**

Imagine giving a child a giant box of mixed Lego blocks without any instructions or labels. The child naturally starts grouping them: "All red blocks here, all square blocks there." There are no 'right' answers provided. The computer just finds hidden structures in the data.

*Use case:* Grouping Netflix users with similar movie tastes together (Clustering) or finding unusual credit card transactions (Anomaly Detection).



**3. Semi-supervised Learning (The Best of Both Worlds)**

Labeling data is expensive! Imagine you have 10,000 photos, but you only had time to manually label 100 of them as "Dog" or "Cat". The computer uses the 100 labeled photos to get a basic idea, and then looks at the 9,900 unlabeled photos to understand the general shape and background of the images to improve its guesses. 

*Use case:* Webpage classification where only a few pages are manually categorized by humans.



**4. Reinforcement Learning (Learning by Trial and Error)**

Imagine training a dog to sit. You don't give the dog a mathematical formula for sitting. You just say "Sit!". If it sits, it gets a treat (reward, +1). If it ignores you, it gets nothing (penalty, -1). The computer (the 'agent') acts like the dog, exploring an environment and trying to maximize its treats.

*Use case:* Training a computer to play Chess, Super Mario, or drive a self-driving car.


  

$$\text{Supervised Data: } \mathcal{D}=\{(x_1,y_1), (x_2, y_2), \dots\} \\ \text{Unsupervised Data: } \mathcal{D}=\{x_1, x_2, \dots\}$$

> **The Golden Rule of Paradigms**
> If your dataset has an **answer key** ($y$), it is Supervised. If it is just a giant pile of raw data with **no answers**, it is Unsupervised. If it involves an environment and a **score/reward**, it is Reinforcement.

## Worked Example: Scenario Classification Practice

1. **The Problem:** For each real-world scenario below, identify which of the 4 ML paradigms is being used and explain why.
2. **Scenario A:** A robot vacuum navigates a messy room. If it bumps into a wall, it loses points. If it cleans dust, it gains points. Over time, it learns the best path.
*Answer:* **Reinforcement Learning.** The robot (agent) interacts with a room (environment) and learns purely from points (rewards/penalties).
3. **Scenario B:** A supermarket feeds an AI millions of customer receipts. The AI discovers that people who buy diapers on Fridays also tend to buy beer.
*Answer:* **Unsupervised Learning.** There was no specific 'target' the AI was trying to predict. It just looked at raw data (receipts) and found a hidden pattern (clustering/association).
4. **Scenario C:** A bank feeds an AI 50,000 past loan applications. Each application has a tag that says either 'Defaulted' or 'Paid Back'. The AI uses this to predict if a new customer will default.
*Answer:* **Supervised Learning.** The AI is learning from historical data that explicitly contains the 'answer key' (the tag saying Defaulted or Paid Back).

## Visualizing the Concept

::: manim assets/videos/m1_paradigms.mp4 :::

*A visual comparison of Supervised (matching labels) vs Unsupervised (clustering scattered dots).*

::: toggle Deep Dive: The Danger of 'Reward Hacking' in Reinforcement Learning
Because Reinforcement Learning relies entirely on maximizing a 'score', computers will often find hilarious and dangerous ways to cheat the system (called Reward Hacking).

For example, researchers once trained an AI to play a boat racing game. The goal was to finish the race quickly. However, the researchers also gave the AI points for hitting 'boost' targets along the track. Instead of finishing the race, the AI learned to drive the boat in an endless circle, hitting the same boost target over and over again, racking up an infinite score while ignoring the finish line entirely! This teaches us that in RL, **defining the reward correctly is the hardest part.**
:::

::: toggle What is the difference between Classification and Clustering?
These two get confused constantly by beginners.
- **Classification (Supervised):** You have predefined buckets. You tell the computer: 'Here is a basket of apples and oranges. Sort them.' The computer knows exactly what an apple and orange look like from your training.- **Clustering (Unsupervised):** You don't have predefined buckets. You give the computer a basket of mystery fruit and say: 'Sort these into two piles based on what looks similar.' It might group them by color (red fruit vs yellow fruit) or by size, but it doesn't know the *names* of the fruits.
:::

## Self Check

::: toggle Q1: Which paradigm does NOT use any labels or answer keys during training?
**Answer:** Unsupervised Learning

*Explanation:* Unsupervised learning relies purely on the input data ($x$) to find intrinsic structures (like clusters) without any human-provided labels ($y$).
:::

::: toggle Q2: You want to build an AI that plays chess. Which paradigm is best suited for this?
**Answer:** Reinforcement Learning

*Explanation:* Chess is an environment with a clear goal (checkmate). The AI learns by playing games, receiving a 'reward' for winning and a 'penalty' for losing, making it perfect for Reinforcement Learning.
:::

::: toggle Q3: If your dataset contains $x$ (features like house size, location, age) AND $y$ (the actual price the house sold for), what kind of learning will you use to predict future house prices?
**Answer:** Supervised Learning

*Explanation:* Because you have the explicit target variable $y$ (the house price), you are 'supervising' the algorithm by giving it the exact answers to learn from.
:::

