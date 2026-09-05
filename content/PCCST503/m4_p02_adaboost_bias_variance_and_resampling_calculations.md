# Module 4: Worked Problems — AdaBoost & Bias-Variance Calculations
## Progressive Problem Workbook: AdaBoost Step-by-Step Traces, Expected Error Decomposition, and Cross-Validation Mathematics

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Topic:** Module 4 (Boosting Algorithm Traces & Bias-Variance Decomposition)  
> **Format:** Step-by-step arithmetic and numerical solutions with zero skipped steps.

---

# Problem 1: Complete Numerical Trace of AdaBoost (One Full Iteration)

### Problem Statement (Classic KTU 9-Mark Core Exam Problem)
A binary classification dataset has $N = 5$ training instances in 1D space with labels $y_i \in \{-1, +1\}$:

| Instance ($i$) | Feature ($x$) | True Label ($y$) |
| :---: | :---: | :---: |
| 1 | 1.0 | +1 |
| 2 | 2.0 | +1 |
| 3 | 3.0 | -1 |
| 4 | 4.0 | -1 |
| 5 | 5.0 | +1 |

In Round 1 ($t = 1$):
- Assume uniform initial sample weights: $w_i^{(1)} = \frac{1}{N} = 0.20$ for all $i = 1, \dots, 5$.
- A weak classifier (decision stump) $h_1(x)$ predicts:
  $$h_1(x) = \begin{cases} +1 & \text{if } x \le 2.5 \\ -1 & \text{if } x > 2.5 \end{cases}$$

Calculate:
1. The predictions $h_1(x_i)$ for all 5 instances and identify which instances are misclassified.
2. The weighted classification error $\epsilon_1$.
3. The learner voting weight $\alpha_1$.
4. The unnormalized updated sample weights.
5. The normalization constant $Z_1$ and the final normalized weights $w_i^{(2)}$ for Round 2.

---

### Step-by-Step Solution

#### Step 1: Predictions & Error Identification
- Instance 1: $x = 1.0 \le 2.5 \implies h_1(1.0) = +1$. True $y = +1$. **(Correct)**
- Instance 2: $x = 2.0 \le 2.5 \implies h_1(2.0) = +1$. True $y = +1$. **(Correct)**
- Instance 3: $x = 3.0 > 2.5 \implies h_1(3.0) = -1$. True $y = -1$. **(Correct)**
- Instance 4: $x = 4.0 > 2.5 \implies h_1(4.0) = -1$. True $y = -1$. **(Correct)**
- Instance 5: $x = 5.0 > 2.5 \implies h_1(5.0) = -1$. True $y = +1$. **(MISCLASSIFIED!)**

Only Instance 5 is misclassified.

#### Step 2: Compute Weighted Error $\epsilon_1$
$$\epsilon_1 = \sum_{i: h_1(x_i) \ne y_i} w_i^{(1)} = w_5^{(1)} = \mathbf{0.20}$$

#### Step 3: Compute Learner Weight $\alpha_1$
$$\alpha_1 = \frac{1}{2} \ln\left( \frac{1 - \epsilon_1}{\epsilon_1} \right) = \frac{1}{2} \ln\left( \frac{1 - 0.20}{0.20} \right) = \frac{1}{2} \ln\left( \frac{0.80}{0.20} \right) = \frac{1}{2} \ln(4)$$
$$\alpha_1 = \frac{1}{2} \times 1.3863 = \mathbf{0.69315}$$

#### Step 4: Compute Unnormalized Updated Weights
The update rule is:
$$\tilde{w}_i^{(2)} = w_i^{(1)} \exp(-\alpha_1 y_i h_1(x_i))$$

Note that:
- $e^{-\alpha_1} = e^{-0.69315} = \frac{1}{e^{0.69315}} = \frac{1}{2} = 0.5$ (for correctly classified points)
- $e^{+\alpha_1} = e^{+0.69315} = 2.0$ (for misclassified points)

Calculate for each instance:
- Instance 1 (Correct): $\tilde{w}_1^{(2)} = 0.20 \times 0.5 = \mathbf{0.10}$
- Instance 2 (Correct): $\tilde{w}_2^{(2)} = 0.20 \times 0.5 = \mathbf{0.10}$
- Instance 3 (Correct): $\tilde{w}_3^{(2)} = 0.20 \times 0.5 = \mathbf{0.10}$
- Instance 4 (Correct): $\tilde{w}_4^{(2)} = 0.20 \times 0.5 = \mathbf{0.10}$
- Instance 5 (Misclassified): $\tilde{w}_5^{(2)} = 0.20 \times 2.0 = \mathbf{0.40}$

#### Step 5: Compute Normalization Constant $Z_1$ and Normalized Weights
$$Z_1 = \sum_{i=1}^5 \tilde{w}_i^{(2)} = 0.10 + 0.10 + 0.10 + 0.10 + 0.40 = \mathbf{0.80}$$

Now divide each unnormalized weight by $Z_1 = 0.80$:
- $w_1^{(2)} = \frac{0.10}{0.80} = \mathbf{0.125}$
- $w_2^{(2)} = \frac{0.10}{0.80} = \mathbf{0.125}$
- $w_3^{(2)} = \frac{0.10}{0.80} = \mathbf{0.125}$
- $w_4^{(2)} = \frac{0.10}{0.80} = \mathbf{0.125}$
- $w_5^{(2)} = \frac{0.40}{0.80} = \mathbf{0.500}$

**Check sum:** $0.125 + 0.125 + 0.125 + 0.125 + 0.500 = 1.000 \quad \checkmark$
*Interpretation: In Round 2, the misclassified Instance 5 now commands 50% of the entire dataset's focus, forcing the next weak learner to correctly categorize it!*

---

# Problem 2: Expected Prediction Error Decomposition (Bias-Variance)

### Problem Statement
At a fixed query point $x_0 = 2.0$:
- The true underlying relationship is $y = f(x_0) + \epsilon = 5.0 + \epsilon$, where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ with noise variance $\sigma^2 = 0.25$.
- Three different machine learning models trained on independent datasets produce the following prediction statistics at $x_0$:
  - **Model A:** $\mathbb{E}[\hat{f}_A(x_0)] = 5.1$, $\text{Var}(\hat{f}_A(x_0)) = 0.10$
  - **Model B:** $\mathbb{E}[\hat{f}_B(x_0)] = 4.0$, $\text{Var}(\hat{f}_B(x_0)) = 0.04$
  - **Model C:** $\mathbb{E}[\hat{f}_C(x_0)] = 5.0$, $\text{Var}(\hat{f}_C(x_0)) = 0.85$

For each model:
1. Compute the $\text{Bias}$ and $\text{Bias}^2$.
2. Compute the total Expected Prediction Error $\mathbb{E}[(y - \hat{f}(x_0))^2] = \text{Bias}^2 + \text{Variance} + \sigma^2$.
3. Determine which model achieves the best overall performance and diagnose whether each suffers from underfitting or overfitting.

---

### Step-by-Step Solution

::: callout-formula Decomposition Formula
$$\text{Expected Prediction Error} = (f(x_0) - \mathbb{E}[\hat{f}(x_0)])^2 + \text{Var}(\hat{f}(x_0)) + \sigma^2$$
:::

#### 1. Model A:
- $\text{Bias} = f(x_0) - \mathbb{E}[\hat{f}_A(x_0)] = 5.0 - 5.1 = -0.1$
- $\text{Bias}^2 = (-0.1)^2 = 0.01$
- $\text{Variance} = 0.10$
- $\sigma^2 = 0.25$
- $\text{Expected Error} = 0.01 + 0.10 + 0.25 = \mathbf{0.36}$
- *Diagnosis:* Well-balanced model with low bias and low variance.

#### 2. Model B:
- $\text{Bias} = f(x_0) - \mathbb{E}[\hat{f}_B(x_0)] = 5.0 - 4.0 = 1.0$
- $\text{Bias}^2 = (1.0)^2 = 1.00$
- $\text{Variance} = 0.04$
- $\sigma^2 = 0.25$
- $\text{Expected Error} = 1.00 + 0.04 + 0.25 = \mathbf{1.29}$
- *Diagnosis:* **High Bias (Underfitting)**. Although variance is extremely small, the model fails to capture the true function, resulting in large systematic error.

#### 3. Model C:
- $\text{Bias} = f(x_0) - \mathbb{E}[\hat{f}_C(x_0)] = 5.0 - 5.0 = 0.0$
- $\text{Bias}^2 = 0.0$
- $\text{Variance} = 0.85$
- $\sigma^2 = 0.25$
- $\text{Expected Error} = 0.0 + 0.85 + 0.25 = \mathbf{1.10}$
- *Diagnosis:* **High Variance (Overfitting)**. Perfectly unbiased on average, but wildly sensitive across training sets.

**Optimal Model Selection:**
Model A achieves the lowest expected prediction error ($\mathbf{0.36}$).

---

# Problem 3: Resampling & Cross-Validation Calculations

### Problem Statement
A medical dataset has $N = 1,200$ patient records.
1. In standard 5-fold cross-validation, how many samples are in each fold, and how many samples are used for training vs. validation in each iteration?
2. If Leave-One-Out Cross-Validation (LOOCV) is used instead, how many total training runs must be executed, and how many samples are in each training set?
3. In a bootstrap sample of size $N = 1,200$ drawn with replacement, calculate the expected number of distinct patient records included and the expected number of Out-of-Bag (OOB) patient records.

---

### Step-by-Step Solution

#### 1. 5-Fold Cross-Validation:
- Fold size: $\frac{N}{K} = \frac{1,200}{5} = \mathbf{240 \text{ patients per fold}}$.
- In each fold iteration:
  - **Training Set:** $(K - 1) \times 240 = 4 \times 240 = \mathbf{960 \text{ patients } (80\%)}$.
  - **Validation Set:** $1 \times 240 = \mathbf{240 \text{ patients } (20\%)}$.

#### 2. Leave-One-Out Cross-Validation (LOOCV):
- Total iterations / models trained: $K = N = \mathbf{1,200 \text{ iterations}}$.
- In each iteration:
  - **Training Set:** $N - 1 = \mathbf{1,199 \text{ patients}}$.
  - **Validation Set:** $\mathbf{1 \text{ patient}}$.

#### 3. Bootstrapping & Out-of-Bag (OOB) Expected Counts:
- Probability of an individual patient NOT being selected in a single random draw: $1 - \frac{1}{N} = 1 - \frac{1}{1,200}$.
- Probability of NOT being selected in all $N$ independent draws:
  $$P(\text{OOB}) = \left(1 - \frac{1}{1,200}\right)^{1,200} \approx \frac{1}{e} \approx 0.36788 \quad (36.79\%)$$
- **Expected Out-of-Bag (OOB) Patients:**
  $$\mathbb{E}[\text{OOB}] = 1,200 \times 0.36788 \approx \mathbf{441 \text{ patients}}$$
- **Expected Unique Patients in Bootstrap Sample:**
  $$\mathbb{E}[\text{Included}] = 1,200 - 441 = \mathbf{759 \text{ unique patients } (63.21\%)}$$
