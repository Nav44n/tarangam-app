# Feature Representation & Problem Formulation

**How to translate the messy real world into a language of numbers that math can understand.**


Algorithms cannot "see" a house, "read" an email, or "look" at a patient. Algorithms only understand one thing: **Numbers**.



Before we can do any Machine Learning, we must translate the real-world object into a list of numbers. This list of numbers is called a **Feature Vector** ($x$). Every individual trait we measure is called a **Feature**.



**1. Feature Representation (The Translation)**

Imagine you are describing a suspect to a police sketch artist. You don't just say "a guy." You break him down into features: Height (numeric), Eye Color (category), Age (numeric). In ML, we do the exact same thing:

  - **Continuous Features:** Things you can measure (e.g., Age = 25, Salary = 50000.50, House Size = 1500 sqft).
  - **Categorical Features:** Things that fall into buckets (e.g., Color = Red, City = Kochi, Blood Type = O+).

Since computers can't do math on the word "Red", we have to convert categories into numbers. A bad way is assigning Red=1, Green=2, Blue=3 (because the computer will think Blue is 3 times "greater" than Red). The correct way is **One-Hot Encoding**.



**2. Problem Formulation (The Formal Setup)**

Once we have our features, we mathematically define the supervised learning problem using specific symbols. Don't let them scare you; they are just shorthand for simple concepts:

  - **Input Space ($\mathcal{X}$):** The set of all possible feature vectors (e.g., all possible houses). Let's call a single house $x$.
  - **Output Space ($\mathcal{Y}$):** What we are trying to predict. If $\mathcal{Y}$ is continuous (like Price = $50,000), it's a **Regression** problem. If $\mathcal{Y}$ is a set of buckets (like {Spam, Not Spam}), it's a **Classification** problem. Let's call a single answer $y$.
  - **Dataset ($\mathcal{D}$):** Your historical data. A list of pairs: $\{(x_1, y_1), (x_2, y_2), \dots\}$. (e.g., House 1 and its Price, House 2 and its Price).
  - **Hypothesis ($f$ or $h$):** The function or "rule" the computer learns. Our goal is to find a function where $f(x) \approx y$ (the prediction matches the real answer).



  

$$\text{Dataset: } \mathcal{D} = \{(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)\} \\ \text{Goal: Find } f: \mathcal{X} \to \mathcal{Y} \text{ such that } f(x_i) \approx y_i$$

> **Why is it called a 'Hypothesis'?**
> In science, a hypothesis is an educated guess. In ML, until the model sees *all* data in the universe (which is impossible), the rules it generates are just a very good 'guess' at how the universe works. Therefore, the function $f(x)$ is often called a Hypothesis $h(x)$.

## Worked Example: Step-by-Step Scenario: One-Hot Encoding a Used Car

1. **The Problem:** You want an algorithm to predict the price of a used car. The car is a 2018 model, driven 50,000 km, and the Color is 'Red'. Create its Feature Vector $x$.
2. **Step 1: Identify Continuous Features.**
 Age = 2024 - 2018 = 6 years. Mileage = 50,000. These are already numbers. Great!
3. **Step 2: Identify Categorical Features.**
 Color = 'Red'. We know the possible colors in our dataset are {Red, Green, Blue}.
4. **Step 3: Apply One-Hot Encoding.**
 Instead of 1 column for color, we create 3 binary (0 or 1) columns: *Is_Red*, *Is_Green*, *Is_Blue*.
5. **Step 4: Translate the car's color.**
 Since the car is Red, *Is_Red* = 1, *Is_Green* = 0, *Is_Blue* = 0.
6. **Step 5: Assemble the final Feature Vector $x$.**
 $x = [6, 50000, 1, 0, 0]$. This list of 5 numbers is what the algorithm actually 'sees'!

## Visualizing the Concept

::: manim assets/videos/m1_05_formulation.mp4 :::

*Watch how a real-world house is translated into a vector, and passed through a Hypothesis function to output a price prediction.*

::: toggle Deep Dive: The Danger of Feature Scaling
Look at our car vector: $[6, 50000, 1, 0, 0]$. The mileage (50,000) is a massive number compared to the age (6). Many ML algorithms (like Gradient Descent or KNN) will look at this and mathematically assume that Mileage is 10,000 times more important than Age just because the number is bigger!

To fix this, we apply **Feature Scaling (Normalization or Standardization)**. We squish all features so they live on the same scale, like between 0 and 1, or giving them a mean of 0 and variance of 1. This levels the playing field so the algorithm judges features on their actual pattern, not their raw size.
:::

::: toggle Problem Variation: Identifying X and Y
Let's practice Formulation. 
**Scenario:** Given a student's hours studied and attendance percentage, predict if they will Pass or Fail.
- **Input $x$:** $[\text{Hours}, \text{Attendance}]$- **Input Space $\mathcal{X}$:** $\mathbb{R}^2$ (A 2-dimensional vector of real numbers)- **Output $y$:** Pass or Fail- **Output Space $\mathcal{Y}$:** $\{0, 1\}$ (Discrete categories)- **Problem Type:** Binary Classification
:::

## Self Check

::: toggle Q1: If you have a categorical feature 'City' with 4 possible values (Kochi, Trivandrum, Kozhikode, Calicut), how many new columns will One-Hot Encoding create?
**Answer:** 4 separate columns

*Explanation:* One-Hot Encoding creates one new binary column for every possible category. So 4 cities = 4 new columns (Is_Kochi, Is_Trivandrum, etc).
:::

::: toggle Q2: In the formal mathematical notation of ML, what does $\mathcal{D} = \{(x_1, y_1), \dots\}$ represent?
**Answer:** The labelled historical training dataset

*Explanation:* The script $\mathcal{D}$ stands for Dataset. The pairs $(x_i, y_i)$ mean it contains both the input features ($x$) and the correct output labels ($y$).
:::

::: toggle Q3: Why is assigning 'Red=1, Green=2, Blue=3' a bad idea for most Machine Learning algorithms?
**Answer:** It implies a mathematical order (that Blue is 'greater' or 'more' than Red) which is false

*Explanation:* Categories usually have no natural numeric order. If you use 1, 2, 3, the algorithm might think Blue (3) is the 'average' of Red (1) and some other color, which makes no logical sense.
:::

