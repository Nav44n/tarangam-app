import os

CONTENT_DIR = os.path.join("content", "PCCST503")

m2_practice = r"""# Module 2 Practice Lab: The Complete Numerical Vault

**Every major classification numerical problem, variance analysis, information theory calculation, and distance matrix derivation.**

---

<a id="the-intuition"></a>
## Overview of Module 2 Problem Types

| Problem Category | Core Concept | What is Evaluated? | Typical Exam Marks |
| :--- | :--- | :--- | :--- |
| **Type 2.1** | Logistic Regression & Logit Math | Sigmoid $\sigma(z)$, Log-Odds, Decision Boundary Hyperplane Equations | 7 – 10 Marks |
| **Type 2.2** | Naïve Bayes with Laplace Smoothing | Prior, Likelihood, Evidence, Posterior, and $+1$ Zero-Frequency Correction | 10 – 15 Marks |
| **Type 2.3** | K-Nearest Neighbors (KNN) Distance | Euclidean, Manhattan, Minkowski, Majority Voting, and Min-Max Feature Scaling | 10 Marks |
| **Type 2.4** | Decision Trees (ID3 & CART) | Shannon Entropy $H(S)$, Information Gain $IG$, Gini Impurity, and Continuous Split Thresholds | 12 – 15 Marks |
| **Type 2.5** | Confusion Matrix & Evaluation Metrics | TP, FP, FN, TN, Precision, Recall, Specificity, and $F_1\text{-Score}$ | 7 – 10 Marks |

---

<a id="the-math"></a>
## Category 2.1: Logistic Regression & Logit Math

### Problem 2.1.1: Probability & Odds Ratio Prediction
**Problem Statement:** A logistic regression model has fitted parameter vector $\theta = [\theta_0 = -4.0, \theta_1 = 0.8, \theta_2 = 0.5]^T$. 
A patient presents with Age $x_1 = 5$ (scaled) and Blood Pressure $x_2 = 2$ (scaled).
1. Calculate the linear score $z = \theta^T x$.
2. Compute the predicted probability of Heart Disease $P(y=1 \mid x)$.
3. Calculate the Odds Ratio $\frac{P(y=1)}{P(y=0)}$.
4. Find the equation of the linear Decision Boundary hyperplane where $P(y=1 \mid x) = 0.50$.

::: step [Step 1: Compute Linear Score $z$] Dot Product
$$ z = \theta_0 + \theta_1 x_1 + \theta_2 x_2 = -4.0 + (0.8 \times 5) + (0.5 \times 2) = -4.0 + 4.0 + 1.0 = +1.0 $$
:::

::: step [Step 2: Apply Sigmoid Activation $\sigma(z)$] Bounded Probability
$$ P(y=1 \mid x) = \sigma(1.0) = \frac{1}{1 + e^{-1.0}} = \frac{1}{1 + 0.3679} = \frac{1}{1.3679} \approx 0.7311 \quad (73.11\%) $$
:::

::: step [Step 3: Compute Odds Ratio]
$$ \text{Odds} = \frac{P(y=1)}{1 - P(y=1)} = \frac{0.7311}{1 - 0.7311} = \frac{0.7311}{0.2689} \approx 2.718 \quad (= e^1) $$
*Interpretation:* The patient is $2.72\times$ more likely to have the disease than not have it.
:::

::: step [Step 4: Derive Geometric Decision Boundary Equation]
The boundary occurs at $P(y=1 \mid x) = 0.50 \iff z = 0$:
$$ -4.0 + 0.8 x_1 + 0.5 x_2 = 0 \implies 0.5 x_2 = 4.0 - 0.8 x_1 \implies x_2 = 8.0 - 1.6 x_1 $$
This is a straight 2D line dividing the feature space into Class 1 and Class 0!
:::

---

## Category 2.2: Naïve Bayes with Laplace Smoothing

### Problem 2.2.1: End-to-End Document Text Classification
**Problem Statement:** You have a training dataset of 10 emails: 4 labeled `Spam (C_1)` and 6 labeled `Ham (C_2)`.
Word frequency counts in the training set are given below:

| Word ($w$) | Count in Spam ($C_1$) | Count in Ham ($C_2$) |
| :--- | :--- | :--- |
| `lottery` | 6 | 0 |
| `winner` | 4 | 1 |
| `meeting` | 0 | 5 |
| **Total Words in Class ($N_c$)** | **10** | **6** |

Vocabulary size $|V| = 3$ unique words.
Classify a new test email: **"winner meeting"** using **Laplace ($+1$) Smoothing**.

::: step [Step 1: Compute Class Prior Probabilities]
$$ P(\text{Spam}) = \frac{4}{10} = 0.40, \quad P(\text{Ham}) = \frac{6}{10} = 0.60 $$
:::

::: step [Step 2: Compute Smoothed Likelihoods] Laplace Formula $\frac{\text{Count} + 1}{N_c + |V|}$
- **For Spam ($C_1, N_1 = 10, |V| = 3 \implies \text{Denom} = 13$):**
  - $P(\text{winner} \mid \text{Spam}) = \frac{4 + 1}{10 + 3} = \frac{5}{13} \approx 0.3846$
  - $P(\text{meeting} \mid \text{Spam}) = \frac{0 + 1}{10 + 3} = \frac{1}{13} \approx 0.0769$ *(Saved from zero!)*
- **For Ham ($C_2, N_2 = 6, |V| = 3 \implies \text{Denom} = 9$):**
  - $P(\text{winner} \mid \text{Ham}) = \frac{1 + 1}{6 + 3} = \frac{2}{9} \approx 0.2222$
  - $P(\text{meeting} \mid \text{Ham}) = \frac{5 + 1}{6 + 3} = \frac{6}{9} \approx 0.6667$
:::

::: step [Step 3: Joint Likelihood $\times$ Prior Numerators]
- **Score(Spam):**
$$ P(\text{Spam}) \times P(\text{winner}|\text{Spam}) \times P(\text{meeting}|\text{Spam}) = 0.40 \times \frac{5}{13} \times \frac{1}{13} = \frac{2}{169} \approx 0.01183 $$
- **Score(Ham):**
$$ P(\text{Ham}) \times P(\text{winner}|\text{Ham}) \times P(\text{meeting}|\text{Ham}) = 0.60 \times \frac{2}{9} \times \frac{6}{9} = \frac{7.2}{81} \approx 0.08889 $$
:::

::: step [Step 4: Normalize & Final Prediction]
Evidence $P(X) = 0.01183 + 0.08889 = 0.10072$.
$$ P(\text{Spam} \mid \text{Email}) = \frac{0.01183}{0.10072} \approx 11.75\% $$
$$ P(\text{Ham} \mid \text{Email}) = \frac{0.08889}{0.10072} \approx 88.25\% $$
**Final Decision:** Classify email as **Ham (Not Spam)**.
:::

---

## Category 2.3: K-Nearest Neighbors (KNN)

### Problem 2.3.1: Distance Metrics & $K$-Voting Matrix
**Problem Statement:** Given 5 training points in 2D space:

| Point | Feature $x_1$ | Feature $x_2$ | Class $y$ |
| :--- | :--- | :--- | :--- |
| $A$ | 1 | 2 | Red |
| $B$ | 2 | 3 | Red |
| $C$ | 3 | 1 | Blue |
| $D$ | 6 | 5 | Blue |
| $E$ | 7 | 8 | Blue |

Classify the query point $q = (3, 3)$ using:
1. **$K=1$ Euclidean Distance**
2. **$K=3$ Euclidean Distance**
3. **$K=3$ Manhattan Distance ($L_1$)**

::: step [Step 1: Compute Euclidean Distance to Query $q=(3, 3)$] $d = \sqrt{(x_1 - 3)^2 + (x_2 - 3)^2}$
- $d(q, A) = \sqrt{(1-3)^2 + (2-3)^2} = \sqrt{(-2)^2 + (-1)^2} = \sqrt{4+1} = \sqrt{5} \approx 2.236$
- $d(q, B) = \sqrt{(2-3)^2 + (3-3)^2} = \sqrt{(-1)^2 + 0} = \sqrt{1} = 1.000$
- $d(q, C) = \sqrt{(3-3)^2 + (1-3)^2} = \sqrt{0 + (-2)^2} = \sqrt{4} = 2.000$
- $d(q, D) = \sqrt{(6-3)^2 + (5-3)^2} = \sqrt{3^2 + 2^2} = \sqrt{9+4} = \sqrt{13} \approx 3.606$
- $d(q, E) = \sqrt{(7-3)^2 + (8-3)^2} = \sqrt{4^2 + 5^2} = \sqrt{16+25} = \sqrt{41} \approx 6.403$
:::

::: step [Step 2: Sort Distances & Vote]
Sorted Order: **1st: Point $B$ ($d=1.0$, Red)**, **2nd: Point $C$ ($d=2.0$, Blue)**, **3rd: Point $A$ ($d=2.236$, Red)**.
- **For $K=1$:** Nearest neighbor is Point $B \implies$ **Classify as Red**.
- **For $K=3$:** Top 3 neighbors are $\{B(\text{Red}), C(\text{Blue}), A(\text{Red})\}$.
  - Red votes = 2, Blue votes = 1 $\implies$ **Classify as Red**.
:::

::: step [Step 3: Compute Manhattan Distance $L_1 = |x_1 - 3| + |x_2 - 3|$]
- $d_{L1}(q, A) = |1-3| + |2-3| = 2 + 1 = 3$
- $d_{L1}(q, B) = |2-3| + |3-3| = 1 + 0 = 1$
- $d_{L1}(q, C) = |3-3| + |1-3| = 0 + 2 = 2$
- Nearest 3 points under $L_1$: $\{B, C, A\} \implies$ **Classify as Red**.
:::

---

## Category 2.4: Decision Trees (Entropy & Information Gain)

### Problem 2.4.1: The Complete ID3 Root Split Calculation
**Problem Statement:** A dataset $S$ of 14 days has target `Play Golf` with 9 `Yes` and 5 `No`.
The feature `Windy` has two values: `False` (8 samples: 6 Yes, 2 No) and `True` (6 samples: 3 Yes, 3 No).
Compute the **Information Gain** $IG(S, \text{Windy})$.

::: step [Step 1: Compute Total Root Node Entropy $H(S)$]
$$ H(S) = -\left[ \frac{9}{14}\log_2\left(\frac{9}{14}\right) + \frac{5}{14}\log_2\left(\frac{5}{14}\right) \right] $$
- $\frac{9}{14} \approx 0.6429 \implies \log_2(0.6429) \approx -0.6374$
- $\frac{5}{14} \approx 0.3571 \implies \log_2(0.3571) \approx -1.4854$
$$ H(S) = - [ (0.6429 \times -0.6374) + (0.3571 \times -1.4854) ] = - [ -0.4098 - 0.5304 ] = 0.9402\text{ bits} $$
:::

::: step [Step 2: Compute Entropy of Child Branches]
- **Branch 1: `Windy = False` ($|S_F| = 8$, 6 Yes, 2 No):**
$$ H(S_F) = -\left[ \frac{6}{8}\log_2\left(\frac{6}{8}\right) + \frac{2}{8}\log_2\left(\frac{2}{8}\right) \right] = -\left[ 0.75(-0.415) + 0.25(-2.0) \right] = 0.8113\text{ bits} $$
- **Branch 2: `Windy = True` ($|S_T| = 6$, 3 Yes, 3 No):**
$$ H(S_T) = -\left[ \frac{3}{6}\log_2(0.5) + \frac{3}{6}\log_2(0.5) \right] = 1.000\text{ bit (Maximum Disorder)} $$
:::

::: step [Step 3: Compute Weighted Remaining Entropy]
$$ H(S \mid \text{Windy}) = \frac{|S_F|}{|S|} H(S_F) + \frac{|S_T|}{|S|} H(S_T) = \left( \frac{8}{14} \times 0.8113 \right) + \left( \frac{6}{14} \times 1.000 \right) $$
$$ H(S \mid \text{Windy}) = 0.4636 + 0.4286 = 0.8922\text{ bits} $$
:::

::: step [Step 4: Compute Information Gain]
$$ IG(S, \text{Windy}) = H(S) - H(S \mid \text{Windy}) = 0.9402 - 0.8922 = 0.0480\text{ bits} $$
:::

---

## Category 2.5: Confusion Matrix & Evaluation Metrics

### Problem 2.5.1: Medical Diagnostics Diagnostic Matrix
**Problem Statement:** A cancer detection screening is performed on 1,000 patients. 50 patients actually have cancer, while 950 are healthy.
The diagnostic model outputs the following:
- 45 sick patients correctly flagged as Positive.
- 5 sick patients falsely diagnosed as Negative.
- 30 healthy patients falsely flagged as Positive.
- 920 healthy patients correctly diagnosed as Negative.

Calculate and interpret:
1. Complete $2 \times 2$ Confusion Matrix.
2. Accuracy.
3. Precision (Positive Predictive Value).
4. Recall / Sensitivity (True Positive Rate).
5. Specificity (True Negative Rate).
6. $F_1\text{-Score}$ (Harmonic Mean).

::: step [Step 1: Construct Confusion Matrix]
| | Actual Cancer ($y=1$) | Actual Healthy ($y=0$) |
| :--- | :--- | :--- |
| **Predicted Cancer ($\hat{y}=1$)** | **$TP = 45$** | **$FP = 30$** |
| **Predicted Healthy ($\hat{y}=0$)** | **$FN = 5$** | **$TN = 920$** |
:::

::: step [Step 2: Compute Metrics]
- **Accuracy:** $\frac{TP + TN}{\text{Total}} = \frac{45 + 920}{1000} = \frac{965}{1000} = 96.5\%$
- **Precision:** $\frac{TP}{TP + FP} = \frac{45}{45 + 30} = \frac{45}{75} = 60.0\%$
  *(When the test says "Cancer", there is only a 60% chance it is true).*
- **Recall (Sensitivity):** $\frac{TP}{TP + FN} = \frac{45}{45 + 5} = \frac{45}{50} = 90.0\%$
  *(The model caught 90% of all real cancer patients).*
- **Specificity:** $\frac{TN}{TN + FP} = \frac{920}{920 + 30} = \frac{920}{950} \approx 96.84\%$
- **$F_1\text{-Score}$:**
$$ F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = 2 \times \frac{0.60 \times 0.90}{0.60 + 0.90} = 2 \times \frac{0.54}{1.50} = 2 \times 0.36 = 0.72 \quad (72.0\%) $$
:::

::: callout-pitfall The Accuracy Paradox in Real Systems
Notice how Accuracy is **$96.5\%$**, yet Precision is only **$60.0\%$**!
A dummy model that blindly predicted "Healthy" for every patient would have achieved $95.0\%$ accuracy while killing all 50 cancer patients. **Never rely on pure Accuracy for imbalanced classification tasks!**
:::
"""

with open(os.path.join(CONTENT_DIR, "m2_99_practice.md"), "w", encoding="utf-8") as f:
    f.write(m2_practice)

print("Module 2 Practice Numerical Vault generated successfully.")
