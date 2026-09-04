# Module 2: Worked Problem — Information Gain Calculation
## Step-by-Step Derivation of Entropy and Split Selection

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Topic:** Decision Trees & Information Theory (Part B / Numerical Problem)

---

## 1. Problem Statement

A financial dataset contains 12 applicant records with two categorical features:
- **Income_Level ($I$):** $\{ \text{High}, \text{Medium}, \text{Low} \}$
- **Credit_Score ($C$):** $\{ \text{Good}, \text{Bad} \}$

The target variable is **Loan_Approved ($Y$)** $\in \{ \text{Yes}, \text{No} \}$.

| ID | Income_Level | Credit_Score | Loan_Approved |
| :---: | :---: | :---: | :---: |
| 1 | High | Good | **Yes** |
| 2 | High | Good | **Yes** |
| 3 | Medium | Good | **Yes** |
| 4 | Low | Bad | **No** |
| 5 | Low | Good | **No** |
| 6 | Low | Good | **Yes** |
| 7 | Medium | Bad | **No** |
| 8 | High | Bad | **Yes** |
| 9 | High | Good | **Yes** |
| 10 | Low | Bad | **No** |
| 11 | Medium | Bad | **Yes** |
| 12 | Medium | Good | **Yes** |

**Objective:**
Determine which attribute (`Income_Level` or `Credit_Score`) should be selected as the root node of a Decision Tree using the **Information Gain** criterion.

*(Note: Use $\log_2$. You may use standard approximations, e.g., $\log_2(0.5) = -1.0$, $\log_2(0.75) \approx -0.415$, $\log_2(0.333) \approx -1.585$.)*

---

## 2. Step 1: Compute Prior Entropy of the Dataset $H(S)$

First, evaluate the overall class distribution in the dataset ($N=12$).

- **Total "Yes":** 8 instances (IDs: 1, 2, 3, 6, 8, 9, 11, 12)
- **Total "No":** 4 instances (IDs: 4, 5, 7, 10)

Probabilities:
$$P(\text{Yes}) = \frac{8}{12} = \frac{2}{3} \approx 0.667$$
$$P(\text{No}) = \frac{4}{12} = \frac{1}{3} \approx 0.333$$

Applying the Shannon Entropy formula:
$$H(S) = - \left[ P(\text{Yes}) \log_2(P(\text{Yes})) + P(\text{No}) \log_2(P(\text{No})) \right]$$
$$H(S) = - \left[ \frac{2}{3} \log_2\left(\frac{2}{3}\right) + \frac{1}{3} \log_2\left(\frac{1}{3}\right) \right]$$

Compute terms:
- $\frac{2}{3} \log_2(0.667) \approx 0.667 \times (-0.585) \approx -0.390$
- $\frac{1}{3} \log_2(0.333) \approx 0.333 \times (-1.585) \approx -0.528$

$$H(S) = -[-0.390 - 0.528] = \mathbf{0.918 \text{ bits}}$$

*Interpretation:* The dataset is slightly skewed towards "Yes" (8 vs 4), so the entropy is close to, but slightly less than, the maximum uncertainty of 1.0 bit.

---

## 3. Step 2: Evaluate Split on `Income_Level` ($I$)

The attribute `Income_Level` partitions the dataset into three subsets: High, Medium, and Low.

### Subset 1: $I = \text{High}$
- Instances: 4 (IDs: 1, 2, 8, 9)
- Outcomes: 4 "Yes", 0 "No"
- Entropy $H(S_{\text{High}})$:
  Because all instances belong to the same class, this is a **pure node**.
  $$H(S_{\text{High}}) = \mathbf{0.0 \text{ bits}}$$

### Subset 2: $I = \text{Medium}$
- Instances: 4 (IDs: 3, 7, 11, 12)
- Outcomes: 3 "Yes" (IDs 3, 11, 12), 1 "No" (ID 7)
- Probabilities: $p_{\text{Yes}} = \frac{3}{4} = 0.75$, $p_{\text{No}} = \frac{1}{4} = 0.25$
- Entropy $H(S_{\text{Medium}})$:
  $$H(S_{\text{Medium}}) = - \left[ 0.75 \log_2(0.75) + 0.25 \log_2(0.25) \right]$$
  $$H(S_{\text{Medium}}) = - [0.75(-0.415) + 0.25(-2.0)] = -[-0.311 - 0.500] = \mathbf{0.811 \text{ bits}}$$

### Subset 3: $I = \text{Low}$
- Instances: 4 (IDs: 4, 5, 6, 10)
- Outcomes: 1 "Yes" (ID 6), 3 "No" (IDs 4, 5, 10)
- Probabilities: $p_{\text{Yes}} = \frac{1}{4} = 0.25$, $p_{\text{No}} = \frac{3}{4} = 0.75$
- Entropy $H(S_{\text{Low}})$:
  Because the distribution is symmetric to the Medium subset, the entropy is identical.
  $$H(S_{\text{Low}}) = \mathbf{0.811 \text{ bits}}$$

### Conditional Entropy $H(S \mid \text{Income\_Level})$
$$H(S \mid I) = \sum_{v \in \{\text{High, Med, Low}\}} \frac{|S_v|}{|S|} H(S_v)$$
$$H(S \mid I) = \frac{4}{12}(0.0) + \frac{4}{12}(0.811) + \frac{4}{12}(0.811)$$
$$H(S \mid I) = \frac{1}{3}(0.0) + \frac{1}{3}(0.811) + \frac{1}{3}(0.811) = 0.0 + 0.2703 + 0.2703 = \mathbf{0.541 \text{ bits}}$$

### Information Gain for `Income_Level`
$$IG(S, I) = H(S) - H(S \mid I) = 0.918 - 0.541 = \mathbf{0.377 \text{ bits}}$$

---

## 4. Step 3: Evaluate Split on `Credit_Score` ($C$)

The attribute `Credit_Score` partitions the dataset into two subsets: Good and Bad.

### Subset 1: $C = \text{Good}$
- Instances: 7 (IDs: 1, 2, 3, 5, 6, 9, 12)
- Outcomes: 6 "Yes" (IDs 1, 2, 3, 6, 9, 12), 1 "No" (ID 5)
- Probabilities: $p_{\text{Yes}} = \frac{6}{7} \approx 0.857$, $p_{\text{No}} = \frac{1}{7} \approx 0.143$
- Entropy $H(S_{\text{Good}})$:
  $$H(S_{\text{Good}}) = - \left[ \frac{6}{7} \log_2\left(\frac{6}{7}\right) + \frac{1}{7} \log_2\left(\frac{1}{7}\right) \right]$$
  $$H(S_{\text{Good}}) = - [0.857(-0.222) + 0.143(-2.807)] = -[-0.190 - 0.401] = \mathbf{0.591 \text{ bits}}$$

### Subset 2: $C = \text{Bad}$
- Instances: 5 (IDs: 4, 7, 8, 10, 11)
- Outcomes: 2 "Yes" (IDs 8, 11), 3 "No" (IDs 4, 7, 10)
- Probabilities: $p_{\text{Yes}} = \frac{2}{5} = 0.40$, $p_{\text{No}} = \frac{3}{5} = 0.60$
- Entropy $H(S_{\text{Bad}})$:
  $$H(S_{\text{Bad}}) = - \left[ 0.40 \log_2(0.40) + 0.60 \log_2(0.60) \right]$$
  $$H(S_{\text{Bad}}) = - [0.40(-1.322) + 0.60(-0.737)] = -[-0.529 - 0.442] = \mathbf{0.971 \text{ bits}}$$

### Conditional Entropy $H(S \mid \text{Credit\_Score})$
$$H(S \mid C) = \frac{7}{12} H(S_{\text{Good}}) + \frac{5}{12} H(S_{\text{Bad}})$$
$$H(S \mid C) = \left(\frac{7}{12} \times 0.591\right) + \left(\frac{5}{12} \times 0.971\right)$$
$$H(S \mid C) = 0.3448 + 0.4046 = \mathbf{0.749 \text{ bits}}$$

### Information Gain for `Credit_Score`
$$IG(S, C) = H(S) - H(S \mid C) = 0.918 - 0.749 = \mathbf{0.169 \text{ bits}}$$

---

## 5. Final Decision and Conclusion

Compare the Information Gain for both attributes:
- $IG(\text{Income\_Level}) = \mathbf{0.377 \text{ bits}}$
- $IG(\text{Credit\_Score}) = \mathbf{0.169 \text{ bits}}$

**Conclusion:** 
The algorithm will select **Income_Level** as the root node for the decision tree because it provides a higher Information Gain. It reduces the uncertainty regarding the loan approval outcome by $0.377$ bits, whereas Credit Score only reduces uncertainty by $0.169$ bits. 

Notably, splitting on Income_Level immediately isolates a perfectly pure node (Income = High $\implies$ 100% Yes), which strongly drives down the conditional entropy.
