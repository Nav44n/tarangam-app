# Module 2 Practice Problems

Master these exact numerical types for the university exam.

## Type 2.3: Decision Trees (Information Gain)

Given a dataset of 14 samples with a binary target concept (Play Tennis: 9 Yes, 5 No) and a feature 'Outlook' (Sunny: 5, Overcast: 4, Rain: 5). For 'Sunny', the target is (2 Yes, 3 No). For 'Overcast', the target is (4 Yes, 0 No). For 'Rain', the target is (3 Yes, 2 No). Calculate the Information Gain for the 'Outlook' feature.

::: toggle Show Step-by-Step Solution
**Step 1: Calculate Entropy of the Root Node**

The total dataset $S$ has 14 instances: 9 'Yes' and 5 'No'.<br><br>E(S) = -\frac{9}{14}\log_2\left(\frac{9}{14}\right) - \frac{5}{14}\log_2\left(\frac{5}{14}\right) \approx 0.940 \text{ bits}

**Step 2: Calculate Entropy of each Branch (Outlook)**

<strong>Sunny (5):</strong> 2 Yes, 3 No<br>E(Sunny) = -\frac{2}{5}\log_2\left(\frac{2}{5}\right) - \frac{3}{5}\log_2\left(\frac{3}{5}\right) \approx 0.971<br><br><strong>Overcast (4):</strong> 4 Yes, 0 No<br>E(Overcast) = 0 \text{ (Pure Node)}<br><br><strong>Rain (5):</strong> 3 Yes, 2 No<br>E(Rain) = -\frac{3}{5}\log_2\left(\frac{3}{5}\right) - \frac{2}{5}\log_2\left(\frac{2}{5}\right) \approx 0.971

**Step 3: Calculate Final Information Gain**

Formula: IG(S, Outlook) = E(S) - \sum \frac{|S_v|}{|S|} E(S_v)<br><br>IG = 0.940 - \left( \frac{5}{14}(0.971) + \frac{4}{14}(0) + \frac{5}{14}(0.971) \right)<br>IG = 0.940 - (0.347 + 0 + 0.347) = 0.940 - 0.694 = 0.246 \text{ bits}

:::

---

## Type 2.4: Naïve Bayes (Posterior Probability)

You are building a spam filter. In your dataset, $P(\text{Spam}) = 0.4$ and $P(\text{Not Spam}) = 0.6$. The word 'Free' appears in 80% of Spam emails and 10% of Not Spam emails. Calculate the posterior probability that a new email containing the word 'Free' is Spam.

::: toggle Show Step-by-Step Solution
**Step 1: Identify the Priors and Likelihoods**

<strong>Priors:</strong><br>$P(\text{Spam}) = 0.4$<br>$P(\text{Not Spam}) = 0.6$<br><br><strong>Likelihoods:</strong><br>$P(\text{Free} \mid \text{Spam}) = 0.8$<br>$P(\text{Free} \mid \text{Not Spam}) = 0.1$

**Step 2: Apply Bayes' Theorem Numerator**

We want $P(\text{Spam} \mid \text{Free})$. The numerator is Likelihood $\times$ Prior:<br><br>P(\text{Free} \mid \text{Spam}) \times P(\text{Spam}) = 0.8 \times 0.4 = 0.32

**Step 3: Calculate the Evidence (Denominator) and Final Probability**

The total probability of seeing the word 'Free':<br>P(\text{Free}) = (0.8 \times 0.4) + (0.1 \times 0.6) = 0.32 + 0.06 = 0.38<br><br>Final Posterior:<br>P(\text{Spam} \mid \text{Free}) = \frac{0.32}{0.38} \approx 0.842 \text{ (84.2%)}$$

:::

---

## Type 2.5: Evaluation Metrics (Confusion Matrix)

A COVID-19 test is given to 100 people. 10 people actually have COVID. The test correctly identifies 8 of them as Positive. Out of the 90 healthy people, the test incorrectly flags 5 as Positive. Derive the Confusion Matrix and calculate Accuracy, Precision, and Recall.

::: toggle Show Step-by-Step Solution
**Step 1: Construct the Confusion Matrix**

Let's map the numbers:<br>- True Positives (TP): 8 (Sick, tested positive)<br>- False Negatives (FN): 2 (Sick, tested negative) [10 total sick - 8 TP]<br>- False Positives (FP): 5 (Healthy, tested positive)<br>- True Negatives (TN): 85 (Healthy, tested negative) [90 total healthy - 5 FP]<br><br> \begin{bmatrix} TP=8 & FP=5 \\ FN=2 & TN=85 \end{bmatrix} 

**Step 2: Calculate Accuracy**

Accuracy is the total correct predictions over total population.<br><br>Accuracy = \frac{TP + TN}{Total} = \frac{8 + 85}{100} = 0.93 \text{ (93%)}$$

**Step 3: Calculate Precision and Recall**

<strong>Precision</strong> (Out of all positive claims, how many were real?):<br>Precision = \frac{TP}{TP + FP} = \frac{8}{8 + 5} = \frac{8}{13} \approx 0.615 \text{ (61.5%)}$$<br><br><strong>Recall</strong> (Out of all actually sick people, how many did we find?):<br>Recall = \frac{TP}{TP + FN} = \frac{8}{8 + 2} = \frac{8}{10} = 0.80 \text{ (80%)}$$

:::

---

