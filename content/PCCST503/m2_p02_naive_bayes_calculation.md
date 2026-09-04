# Module 2: Worked Problem — Naive Bayes Classification
## Multi-Feature Probability Estimation with Add-1 (Laplace) Smoothing

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Topic:** Generative Classifiers & Smoothing (Part B / Numerical Problem)

---

## 1. Problem Statement

An IT security system analyzes access logs to detect potential insider threats. It classifies employee sessions into two classes:
- **Target Variable ($Y$):** `Normal` vs. `Suspicious`

The system monitors three categorical behavioral features:
- **After_Hours ($X_1$):** $\{ \text{Yes}, \text{No} \}$ (Session occurred outside 9 AM - 5 PM)
- **Data_Volume ($X_2$):** $\{ \text{Low}, \text{High} \}$ (Amount of data downloaded)
- **VPN_Location ($X_3$):** $\{ \text{Local}, \text{Foreign} \}$ (IP origin)

The training dataset ($N = 10$ records) is as follows:

| Session ID | After_Hours | Data_Volume | VPN_Location | Threat_Class |
| :---: | :---: | :---: | :---: | :---: |
| 1 | No | Low | Local | **Normal** |
| 2 | No | Low | Local | **Normal** |
| 3 | Yes | Low | Local | **Normal** |
| 4 | No | High | Local | **Normal** |
| 5 | No | Low | Foreign | **Normal** |
| 6 | Yes | Low | Local | **Normal** |
| 7 | Yes | High | Local | **Suspicious** |
| 8 | Yes | High | Foreign | **Suspicious** |
| 9 | No | High | Foreign | **Suspicious** |
| 10 | Yes | Low | Foreign | **Suspicious** |

**Objective:**
A new session log is captured with the following attributes:
$$\mathbf{x}_{\text{new}} = [\text{After\_Hours} = \text{Yes}, \text{Data\_Volume} = \text{High}, \text{VPN\_Location} = \text{Local}]^T$$

Classify $\mathbf{x}_{\text{new}}$ using the Naive Bayes algorithm. 
**Constraint:** You MUST apply Laplace (Add-1) Smoothing to all likelihood probabilities to prevent zero-frequency pathology, even if empirical counts are non-zero.

---

## 2. Step 1: Compute Prior Class Probabilities

The total number of training records is $N = 10$.
Count the occurrences of each class:
- $N_{\text{Normal}} = 6$ (IDs: 1, 2, 3, 4, 5, 6)
- $N_{\text{Suspicious}} = 4$ (IDs: 7, 8, 9, 10)

Prior probabilities:
$$P(\text{Normal}) = \frac{6}{10} = \mathbf{0.60}$$
$$P(\text{Suspicious}) = \frac{4}{10} = \mathbf{0.40}$$

---

## 3. Step 2: Compute Smoothed Class-Conditional Likelihoods

The Laplace smoothing formula for a feature $X_j$ taking value $v$ given class $c$ is:
$$\hat{P}(X_j = v \mid Y = c) = \frac{N_{c, v} + 1}{N_c + V_j}$$
where $V_j$ is the cardinality (number of possible values) of attribute $X_j$.
For all three attributes in this problem, $V_j = 2$.

Therefore, the smoothed denominators will be:
- For Normal ($N=6$): Denominator = $6 + 2 = \mathbf{8}$
- For Suspicious ($N=4$): Denominator = $4 + 2 = \mathbf{6}$

We need to calculate the likelihoods only for the feature values present in the query vector $\mathbf{x}_{\text{new}} = [\text{Yes}, \text{High}, \text{Local}]$.

### Feature 1: After_Hours = Yes
- **Given Normal ($N_{\text{Normal}} = 6$):** 
  Looking at IDs (1-6), `After_Hours = Yes` appears 2 times (IDs 3, 6).
  $$P(\text{After\_Hours} = \text{Yes} \mid \text{Normal}) = \frac{2 + 1}{6 + 2} = \frac{3}{8} = \mathbf{0.375}$$
- **Given Suspicious ($N_{\text{Suspicious}} = 4$):** 
  Looking at IDs (7-10), `After_Hours = Yes` appears 3 times (IDs 7, 8, 10).
  $$P(\text{After\_Hours} = \text{Yes} \mid \text{Suspicious}) = \frac{3 + 1}{4 + 2} = \frac{4}{6} \approx \mathbf{0.6667}$$

### Feature 2: Data_Volume = High
- **Given Normal ($N_{\text{Normal}} = 6$):** 
  Looking at IDs (1-6), `Data_Volume = High` appears 1 time (ID 4).
  $$P(\text{Data\_Volume} = \text{High} \mid \text{Normal}) = \frac{1 + 1}{6 + 2} = \frac{2}{8} = \mathbf{0.250}$$
- **Given Suspicious ($N_{\text{Suspicious}} = 4$):** 
  Looking at IDs (7-10), `Data_Volume = High` appears 3 times (IDs 7, 8, 9).
  $$P(\text{Data\_Volume} = \text{High} \mid \text{Suspicious}) = \frac{3 + 1}{4 + 2} = \frac{4}{6} \approx \mathbf{0.6667}$$

### Feature 3: VPN_Location = Local
- **Given Normal ($N_{\text{Normal}} = 6$):** 
  Looking at IDs (1-6), `VPN_Location = Local` appears 5 times (IDs 1, 2, 3, 4, 6).
  $$P(\text{VPN\_Location} = \text{Local} \mid \text{Normal}) = \frac{5 + 1}{6 + 2} = \frac{6}{8} = \mathbf{0.750}$$
- **Given Suspicious ($N_{\text{Suspicious}} = 4$):** 
  Looking at IDs (7-10), `VPN_Location = Local` appears 1 time (ID 7).
  $$P(\text{VPN\_Location} = \text{Local} \mid \text{Suspicious}) = \frac{1 + 1}{4 + 2} = \frac{2}{6} \approx \mathbf{0.3333}$$

---

## 4. Step 3: Compute Unnormalized Posteriors (Joint Likelihoods)

Using the conditional independence assumption, we multiply the prior by the product of the likelihoods.

### Evaluate for Class = Normal
$$\tilde{P}(\text{Normal} \mid \mathbf{x}_{\text{new}}) = P(\text{Normal}) \times P(\text{Yes} \mid \text{Normal}) \times P(\text{High} \mid \text{Normal}) \times P(\text{Local} \mid \text{Normal})$$
$$\tilde{P}(\text{Normal} \mid \mathbf{x}_{\text{new}}) = 0.60 \times 0.375 \times 0.250 \times 0.750$$
$$\tilde{P}(\text{Normal} \mid \mathbf{x}_{\text{new}}) = 0.60 \times 0.0703125 = \mathbf{0.0421875}$$

*(Fractional Check: $\frac{6}{10} \times \frac{3}{8} \times \frac{2}{8} \times \frac{6}{8} = \frac{216}{5120} \approx 0.0421875$)*

### Evaluate for Class = Suspicious
$$\tilde{P}(\text{Suspicious} \mid \mathbf{x}_{\text{new}}) = P(\text{Suspicious}) \times P(\text{Yes} \mid \text{Suspicious}) \times P(\text{High} \mid \text{Suspicious}) \times P(\text{Local} \mid \text{Suspicious})$$
$$\tilde{P}(\text{Suspicious} \mid \mathbf{x}_{\text{new}}) = 0.40 \times \left(\frac{4}{6}\right) \times \left(\frac{4}{6}\right) \times \left(\frac{2}{6}\right)$$
$$\tilde{P}(\text{Suspicious} \mid \mathbf{x}_{\text{new}}) = 0.40 \times 0.148148 = \mathbf{0.059259}$$

*(Fractional Check: $\frac{4}{10} \times \frac{4}{6} \times \frac{4}{6} \times \frac{2}{6} = \frac{128}{2160} \approx 0.059259$)*

---

## 5. Step 4: Normalization and Final Classification

To calculate the exact posterior probabilities, divide the unnormalized scores by the marginal evidence $P(\mathbf{x}_{\text{new}})$.

$$P(\mathbf{x}_{\text{new}}) = \tilde{P}(\text{Normal} \mid \mathbf{x}_{\text{new}}) + \tilde{P}(\text{Suspicious} \mid \mathbf{x}_{\text{new}})$$
$$P(\mathbf{x}_{\text{new}}) = 0.0421875 + 0.059259 = \mathbf{0.1014465}$$

**Normalized Probabilities:**
$$P(\text{Normal} \mid \mathbf{x}_{\text{new}}) = \frac{0.0421875}{0.1014465} \approx \mathbf{0.4159} \quad (41.59\%)$$
$$P(\text{Suspicious} \mid \mathbf{x}_{\text{new}}) = \frac{0.059259}{0.1014465} \approx \mathbf{0.5841} \quad (58.41\%)$$

### Final Decision:
Because $P(\text{Suspicious} \mid \mathbf{x}_{\text{new}}) > P(\text{Normal} \mid \mathbf{x}_{\text{new}})$, the Naive Bayes classifier predicts the new session as **Suspicious**.

*(Note: Even though the prior probability heavily favored 'Normal' (60%), the strong empirical evidence from `After_Hours = Yes` and `Data_Volume = High` overwhelmed the prior, shifting the posterior prediction to 'Suspicious'.)*
