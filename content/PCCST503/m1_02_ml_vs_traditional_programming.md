# Machine Learning vs Traditional Programming

**Why hardcoded IF-ELSE rules fail in complex domains and how inductive learning replaces them.**

<a id="the-intuition"></a>
## 1. The Intuition: The Cake Recipe Paradigm

::: callout-intuition The Paradigm Shift
- **Traditional Software:** $\text{Data} + \text{Rules (Code)} \implies \text{Output}$
  - A human software engineer writes every single logical condition by hand. If input $A$ happens, do $B$.
- **Machine Learning:** $\text{Data} + \text{Output} \implies \text{Rules (The Model)}$
  - You provide raw observations and historical outcomes. The learning algorithm discovers the underlying statistical mapping $f: X \to Y$.
:::

---

<a id="the-math"></a>
## 2. In-Depth Comparison Table

| Dimension | Traditional Programming (Deductive) | Machine Learning (Inductive) |
| :--- | :--- | :--- |
| **Primary Input** | Raw Data + Explicit Algorithm | Input Features ($X$) + Ground Truth Labels ($Y$) |
| **Generated Artifact** | Program Execution Output | Model Weights / Hypothesis $h_\theta(x)$ |
| **Logic Formulation** | Handcrafted by human domain experts | Inferred statistically via numerical optimization |
| **Edge Case Handling** | Requires manual bug fixes and patch rules | Improves automatically when retrained on new edge cases |
| **Ideal Problem Domain** | Deterministic calculations (Taxes, Compilers, Banking) | Fuzzy, high-dimensional patterns (Vision, Audio, NLP) |

::: callout-pitfall When NOT to use Machine Learning
Never use Machine Learning when exact, deterministic business rules already exist! For example, calculating GST/VAT (e.g. $\text{Tax} = \text{Total} \times 0.18$) should **always** be traditional code.
:::

---

<a id="simulation"></a>
## 3. Visualizing the Paradigm Shift

::: manim assets/videos/m1_paradigms.mp4 Paradigm Shift Architecture
Observe how 'Rules' and 'Output' swap places in the engineering pipeline.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Architectural Decision
Which of the following problems should NEVER be implemented using Machine Learning?
(A) Transcribing spoken Malayalam voice notes into text
(B) Recommending relevant research papers to college students
(*C) Calculating exact bank account interest using government-mandated rate tiers
(D) Detecting credit card fraud from spending anomalies
::: explanation
Banking interest formulas are exact legal equations. Using ML introduces statistical uncertainty, variance, and latency to a problem that requires 1 line of exact deterministic code.
:::
