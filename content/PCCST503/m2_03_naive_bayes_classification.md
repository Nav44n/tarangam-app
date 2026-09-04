# Module 2: Supervised Learning — Naive Bayes Classification
## Probabilistic Modeling, Conditional Independence, and Smoothing Techniques

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Module Alignment:** Module 2 (Supervised Learning & Generative Classifiers)  
> **Prerequisites:** Probability Foundations (Axioms of Probability, Joint/Marginal/Conditional Distributions, Bayes' Theorem).

---

# Table of Contents
1. [The Probabilistic Framework of Classification](#1-the-probabilistic-framework-of-classification)
   - [Foundations of Bayes' Rule for Pattern Recognition](#foundations-of-bayes-rule-for-pattern-recognition)
   - [Anatomy of the Posterior: Prior, Likelihood, and Evidence](#anatomy-of-the-posterior-prior-likelihood-and-evidence)
   - [The Maximum A Posteriori (MAP) vs. Maximum Likelihood (ML) Criteria](#the-maximum-a-posteriori-map-vs-maximum-likelihood-ml-criteria)
2. [The "Naive" Assumption: Class-Conditional Independence](#2-the-naive-assumption-class-conditional-independence)
   - [Combinatorial Explosion of Unconstrained Joint Likelihoods](#combinatorial-explosion-of-unconstrained-joint-likelihoods)
   - [Formal Definition of Conditional Independence](#formal-definition-of-conditional-independence)
   - [Reduction of Parameter Cardinality](#reduction-of-parameter-cardinality)
   - [Violation of Independence in Real-World Domains](#violation-of-independence-in-real-world-domains)
3. [Mathematical Formulation of the Naive Bayes Classifier](#3-mathematical-formulation-of-the-naive-bayes-classifier)
   - [Line-by-Line Derivation of the MAP Decision Rule](#line-by-line-derivation-of-the-map-decision-rule)
   - [Elimination of the Marginal Evidence $P(\mathbf{x})$](#elimination-of-the-marginal-evidence-px)
   - [The Underflow Problem: Log-Space Transformation](#the-underflow-problem-log-space-transformation)
4. [Event Models: Feature Type Handling](#4-event-models-feature-type-handling)
   - [Categorical / Discrete Features (Multivariate Bernoulli vs. Multinomial)](#categorical--discrete-features-multivariate-bernoulli-vs-multinomial)
   - [Continuous Features via Gaussian Naive Bayes](#continuous-features-via-gaussian-naive-bayes)
5. [The Zero-Probability Pathology and Smoothing Mechanics](#5-the-zero-probability-pathology-and-smoothing-mechanics)
   - [The Multiplicative Veto Phenomenon](#the-multiplicative-veto-phenomenon)
   - [Bayesian Priors as Pseudo-Counts](#bayesian-priors-as-pseudo-counts)
   - [Laplace (Add-1) Smoothing Derivation](#laplace-add-1-smoothing-derivation)
   - [Lidstone (Add-$\alpha$) Smoothing](#lidstone-add-alpha-smoothing)
6. [Comprehensive Step-by-Step Numerical Walkthroughs](#6-comprehensive-step-by-step-numerical-walkthroughs)
   - [Worked Problem 1: Discrete Text Document Classification (Spam Detection)](#worked-problem-1-discrete-text-document-classification-spam-detection)
   - [Worked Problem 2: Full Categorical Dataset Classification with Laplace Correction](#worked-problem-2-full-categorical-dataset-classification-with-laplace-correction)
   - [Worked Problem 3: Continuous Gaussian Naive Bayes Parameterization & Inference](#worked-problem-3-continuous-gaussian-naive-bayes-parameterization--inference)
   - [Worked Problem 4: Resolving the Zero-Frequency Trap in Tabular Data](#worked-problem-4-resolving-the-zero-frequency-trap-in-tabular-data)
7. [KTU University Examination Practice Questions](#7-ktu-university-examination-practice-questions)
   - [Short-Answer Analytical Problems (Part A)](#short-answer-analytical-problems-part-a)
   - [Comprehensive Essay & Derivation Questions (Part B)](#comprehensive-essay--derivation-questions-part-b)

---

# 1. The Probabilistic Framework of Classification

## Foundations of Bayes' Rule for Pattern Recognition
In machine learning, **statistical classification** seeks to determine the most probable class label $y \in \mathcal{Y} = \{c_1, c_2, \dots, c_K\}$ for a given observation represented by a $d$-dimensional feature vector:

$$\mathbf{x} = [x_1, x_2, \dots, x_d]^T \in \mathcal{X}$$

Instead of evaluating a deterministic decision boundary, a **generative probabilistic classifier** models the uncertainty of nature using the calculus of probabilities. 

Let the class label $Y$ and the feature vector $\mathbf{X}$ be random variables defined over the joint probability space $\mathcal{X} \times \mathcal{Y}$. The relationship between the joint probability $P(\mathbf{X} = \mathbf{x}, Y = c_k)$ and the conditional probabilities is governed by the product rule:

$$P(\mathbf{X} = \mathbf{x}, Y = c_k) = P(Y = c_k \mid \mathbf{X} = \mathbf{x}) P(\mathbf{X} = \mathbf{x}) = P(\mathbf{X} = \mathbf{x} \mid Y = c_k) P(Y = c_k)$$

Equating the right-hand expressions yields **Bayes' Theorem**:

$$P(Y = c_k \mid \mathbf{X} = \mathbf{x}) = \frac{P(\mathbf{X} = \mathbf{x} \mid Y = c_k) P(Y = c_k)}{P(\mathbf{X} = \mathbf{x})}$$

---

## Anatomy of the Posterior: Prior, Likelihood, and Evidence
Every component of Bayes' Theorem plays a distinct statistical role:

```
                                  [ Likelihood ]         [ Prior ]
                              P(X = x | Y = c_k)   * P(Y = c_k)
       [ Posterior ]       = --------------------------------------
    P(Y = c_k | X = x)                 P(X = x)
                                     [ Evidence ]
```

1. **The Posterior Probability $P(Y = c_k \mid \mathbf{X} = \mathbf{x})$:**
   The updated probability that the unobserved class is $c_k$ *after* observing the empirical feature evidence $\mathbf{x}$. This represents the final basis for classification.

2. **The Prior Probability $P(Y = c_k)$:**
   The baseline probability of encountering class $c_k$ across the global population *before* any feature measurements are collected. It models the natural prevalence of the category:
   $$P(Y = c_k) = \frac{N_k}{N} = \frac{\sum_{i=1}^N \mathbb{I}(y_i = c_k)}{N}$$

3. **The Class-Conditional Likelihood $P(\mathbf{X} = \mathbf{x} \mid Y = c_k)$:**
   The probability (or density value) of observing the exact feature combination $\mathbf{x}$, given that the true class is known to be $c_k$. It answers: *"If nature were generating an instance of class $c_k$, how typical is the observation $\mathbf{x}$?"*

4. **The Marginal Evidence $P(\mathbf{X} = \mathbf{x})$:**
   The total probability of observing the feature vector $\mathbf{x}$ across all possible classes. By the Law of Total Probability:
   $$P(\mathbf{X} = \mathbf{x}) = \sum_{j=1}^K P(\mathbf{X} = \mathbf{x}, Y = c_j) = \sum_{j=1}^K P(\mathbf{X} = \mathbf{x} \mid Y = c_j) P(Y = c_j)$$
   The evidence is a strictly positive scalar normalizer ensuring that:
   $$\sum_{k=1}^K P(Y = c_k \mid \mathbf{X} = \mathbf{x}) = 1.0$$

---

## The Maximum A Posteriori (MAP) vs. Maximum Likelihood (ML) Criteria
A decision rule maps an observation $\mathbf{x}$ to a predicted category $\hat{y}$. Two statistical principles guide this selection:

### 1. Maximum Likelihood (ML) Criterion
The ML criterion selects the class that maximizes the likelihood of the observed features, ignoring prior distributions:
$$\hat{y}_{\text{ML}} = \arg\max_{c_k \in \mathcal{Y}} P(\mathbf{X} = \mathbf{x} \mid Y = c_k)$$
*Limitation:* The ML rule implicitly assumes a uniform prior ($P(c_k) = \frac{1}{K}$ for all $k$). In medical diagnostics or fraud detection, where positive classes are rare ($P(\text{Cancer}) = 0.001$), the ML criterion results in unacceptable rates of false alarms.

### 2. Maximum A Posteriori (MAP) Criterion
The MAP criterion minimizes the probability of misclassification under a symmetric $0\text{--}1$ loss function by incorporating both the prior prevalence and the feature likelihood:
$$\hat{y}_{\text{MAP}} = \arg\max_{c_k \in \mathcal{Y}} P(Y = c_k \mid \mathbf{X} = \mathbf{x}) = \arg\max_{c_k \in \mathcal{Y}} \left[ \frac{P(\mathbf{X} = \mathbf{x} \mid Y = c_k) P(Y = c_k)}{P(\mathbf{X} = \mathbf{x})} \right]$$

---

# 2. The "Naive" Assumption: Class-Conditional Independence

## Combinatorial Explosion of Unconstrained Joint Likelihoods
To apply the MAP decision rule without structural assumptions, we must estimate the full joint likelihood function $P(\mathbf{X} = \mathbf{x} \mid Y = c_k) = P(x_1, x_2, \dots, x_d \mid c_k)$.

Consider a simple scenario where all $d$ features are binary: $x_j \in \{0, 1\}$.
- For a single class $c_k$, the input space contains $2^d$ possible feature combinations.
- To specify the complete probability distribution over these configurations, we must estimate the probability of each configuration.
- Since probabilities sum to one ($\sum_{\mathbf{x}} P(\mathbf{x} \mid c_k) = 1$), an unconstrained model requires:
  $$\text{Free Parameters per Class} = 2^d - 1$$
- For a problem with $K$ classes, the total parameters required are:
  $$\text{Total Parameters} = K \cdot (2^d - 1)$$

```
Feature Dimension (d)    Possible States (2^d)    Parameters (K=2)
-------------------------------------------------------------------
d = 1                    2                        2
d = 5                    32                       62
d = 10                   1,024                    2,046
d = 20                   1,048,576                ~2.1 x 10^6
d = 100                  ~1.27 x 10^30            ~2.5 x 10^30
```

For $d = 100$ (a tiny fraction of a standard vocabulary in natural language processing), $2^{100} \approx 10^{30}$. This exceeds the number of grains of sand on Earth. No training set could ever observe even a tiny fraction of these combinations, making empirical estimation of an unconstrained joint likelihood impossible.

---

## Formal Definition of Conditional Independence
To make this problem tractable, the **Naive Bayes** model introduces a structural assumption:

> **The Class-Conditional Independence Assumption:** > Given the class label $Y = c_k$, every feature $X_i$ is statistically independent of every other feature $X_j$ (for all $i \neq j$).

Mathematically, by the chain rule of probability, any joint distribution can be factored as:
$$P(x_1, x_2, \dots, x_d \mid c_k) = P(x_1 \mid c_k) \cdot P(x_2 \mid x_1, c_k) \cdot P(x_3 \mid x_1, x_2, c_k) \cdots P(x_d \mid x_1, \dots, x_{d-1}, c_k)$$

Under the conditional independence assumption, all conditioning dependencies between features drop out:
$$P(x_j \mid x_1, x_2, \dots, x_{j-1}, c_k) = P(x_j \mid c_k)$$

The joint class-conditional likelihood factors directly into a product of $d$ independent, one-dimensional probabilities:
$$P(\mathbf{X} = \mathbf{x} \mid Y = c_k) = \prod_{j=1}^d P(X_j = x_j \mid Y = c_k)$$

---

## Reduction of Parameter Cardinality
This assumption changes the parameter scaling behavior:
- For binary features, estimating $P(X_j = 1 \mid c_k)$ requires only **one parameter per feature**.
- For $d$ features across $K$ classes:
  $$\text{Total Parameters}_{\text{Naive Bayes}} = K \cdot d$$

```
Parameters
  ^
  |                                        Unconstrained Joint: O(K * 2^d)
  |                                         /
  |                                        /
  |                                       /
  |                                      /
  |                                     /
  |                                    /
  |                                   /    Naive Bayes: O(K * d)
  |                                  /--------------------------------
  +------------------------------------------------------------------> Feature Dimension (d)
```

The complexity drops from **exponential** $\mathcal{O}(K \cdot 2^d)$ to **strictly linear** $\mathcal{O}(K \cdot d)$. A problem with $d = 1,000$ binary features and $K = 2$ classes requires just $2,000$ parameters, easily learned from standard datasets.

---

## Violation of Independence in Real-World Domains
The conditional independence assumption is almost universally violated in practical applications:
- **Natural Language Processing:** Words correlate strongly with nearby words (e.g., observing "Hong" dramatically increases the probability of observing "Kong").
- **Medicine:** Symptoms co-occur (e.g., high fever, chills, and elevated white blood cell counts are physiologically linked).
- **Computer Vision:** Neighboring pixel intensities in an image are heavily dependent.

### Why Does Naive Bayes Perform Well Despite False Assumptions?
Empirically, Naive Bayes often performs well in ranking and classification tasks even when its probability estimates are poorly calibrated. 

> **The Separation of Calibration and Classification:** > The MAP rule depends only on the **relative order (argmax)** of the class probabilities, not their calibrated numerical precision.

$$\hat{y} = \arg\max_{c_k} P(c_k \mid \mathbf{x}) = \arg\max_{c_k} \left[ P(c_k) \prod_{j=1}^d P(x_j \mid c_k) \right]$$

Even if feature correlations shift the output probabilities toward extreme values ($0.0$ or $1.0$), the classification boundary remains unchanged as long as the correct class maintains the highest value among candidates. Domingos and Pazzani (1997) proved that Naive Bayes remains optimal under zero-one loss for certain classes of problems where feature dependencies distribute evenly across classes.

---

# 3. Mathematical Formulation of the Naive Bayes Classifier

## Line-by-Line Derivation of the MAP Decision Rule
We now derive the complete decision rule of the Naive Bayes classifier:

$$\hat{y} = \arg\max_{c_k \in \mathcal{Y}} P(Y = c_k \mid X_1 = x_1, X_2 = x_2, \dots, X_d = x_d)$$

**Step 1: Apply Bayes' Rule:**
$$\hat{y} = \arg\max_{c_k \in \mathcal{Y}} \left[ \frac{P(X_1 = x_1, \dots, X_d = x_d \mid Y = c_k) P(Y = c_k)}{P(X_1 = x_1, \dots, X_d = x_d)} \right]$$

**Step 2: Eliminate the Denominator:** The denominator $P(\mathbf{X} = \mathbf{x}) = \sum_j P(\mathbf{x} \mid c_j) P(c_j)$ depends solely on the observed features $\mathbf{x}$ and is strictly invariant to the class index $c_k$. Because it is a positive constant with respect to the optimization argument $c_k$, it does not alter the location of the maximum:
$$\hat{y} = \arg\max_{c_k \in \mathcal{Y}} \Big[ P(X_1 = x_1, \dots, X_d = x_d \mid Y = c_k) P(Y = c_k) \Big]$$

**Step 3: Apply the Class-Conditional Independence Assumption:** Replace the unconstrained joint likelihood with the product of individual marginal likelihoods:
$$P(X_1 = x_1, \dots, X_d = x_d \mid Y = c_k) = \prod_{j=1}^d P(X_j = x_j \mid Y = c_k)$$

**Step 4: Formulate the Final Decision Rule:**
$$\hat{y}_{\text{NB}} = \arg\max_{c_k \in \mathcal{Y}} \left[ P(Y = c_k) \prod_{j=1}^d P(X_j = x_j \mid Y = c_k) \right]$$

---

## Elimination of the Marginal Evidence $P(\mathbf{x})$
Although $P(\mathbf{x})$ is dropped during label assignment, it is required if the system must output **calibrated posterior probabilities**:

$$P(Y = c_k \mid \mathbf{x}) = \frac{P(c_k) \prod_{j=1}^d P(x_j \mid c_k)}{\sum_{l=1}^K \left( P(c_l) \prod_{j=1}^d P(x_j \mid c_l) \right)}$$

---

## The Underflow Problem: Log-Space Transformation
In high-dimensional feature spaces (e.g., text processing with $d = 10,000$), multiplying thousands of small probabilities produces **arithmetic underflow**:

$$P(x_j \mid c_k) \in [0, 1] \implies \prod_{j=1}^d P(x_j \mid c_k) \to 0$$

In standard IEEE 754 64-bit floating point arithmetic, values below $\approx 2.22 \times 10^{-308}$ underflow directly to zero, destroying the classification signal.

### The Solution: Monotonic Logarithmic Transformation
Because the natural logarithm $\ln(z)$ is a strictly monotonically increasing function for $z > 0$:
$$\arg\max_z f(z) \equiv \arg\max_z \ln(f(z))$$

Applying the natural logarithm transforms the product of probabilities into a sum of log-probabilities:

$$\ln \left( P(Y = c_k) \prod_{j=1}^d P(X_j = x_j \mid Y = c_k) \right) = \ln P(Y = c_k) + \sum_{j=1}^d \ln P(X_j = x_j \mid Y = c_k)$$

> **The Log-Space Naive Bayes Decision Rule:**
> $$\hat{y}_{\text{NB}} = \arg\max_{c_k \in \mathcal{Y}} \left[ \ln P(Y = c_k) + \sum_{j=1}^d \ln P(X_j = x_j \mid Y = c_k) \right]$$

This formulation replaces multiplication with addition, prevents floating-point underflow, and improves computational efficiency.

---

# 4. Event Models: Feature Type Handling

Depending on the feature space $\mathcal{X}$, different probabilistic models parameterize the likelihood terms $P(x_j \mid c_k)$:

```
                         +-----------------------------------+
                         |    Naive Bayes Event Models       |
                         +-----------------+-----------------+
                                           |
         +---------------------------------+---------------------------------+
         |                                                                   |
         v                                                                   v
+-------------------------+                                       +---------------------+
|   Categorical Models    |                                       |  Continuous Models  |
+------------+------------+                                       +----------+----------+
             |                                                               |
    +--------+--------+                                                      v
    |                 |                                            Gaussian Naive Bayes
    v                 v                                            p(x|c) ~ N(mu, sigma^2)
Bernoulli NB      Multinomial NB
(Binary 0/1)      (Word Counts/Frequencies)
```

---

## Categorical / Discrete Features (Multivariate Bernoulli vs. Multinomial)

### 1. Multivariate Bernoulli Naive Bayes
- **Input Domain:** Features are binary indicator variables: $x_j \in \{0, 1\}$ (e.g., a word is either present or absent in a document).
- **Likelihood Equation:**
  $$P(\mathbf{x} \mid c_k) = \prod_{j=1}^d p_{kj}^{x_j} (1 - p_{kj})^{(1 - x_j)}$$
  where $p_{kj} = P(X_j = 1 \mid c_k)$ is the probability that feature $j$ occurs in class $c_k$.

### 2. Multinomial Naive Bayes
- **Input Domain:** Features represent integer frequencies or counts: $\mathbf{x} = [x_1, x_2, \dots, x_d]^T$ where $x_j \in \{0, 1, 2, \dots\}$ represents the number of times word $j$ appears in the document.
- **Likelihood Equation:**
  $$P(\mathbf{x} \mid c_k) = \frac{\left( \sum_{j=1}^d x_j \right)!}{\prod_{j=1}^d (x_j!)} \prod_{j=1}^d \theta_{kj}^{x_j}$$
  where $\theta_{kj} = P(\text{Word } j \mid c_k)$ is the probability of generating word $j$ in an instance of class $c_k$, with the constraint $\sum_{j=1}^d \theta_{kj} = 1$. The factorial term can be dropped during classification because it depends only on $\mathbf{x}$.

---

## Continuous Features via Gaussian Naive Bayes
When features are real-valued continuous scalars ($x_j \in \mathbb{R}$), we cannot use frequency counts. Instead, we model each class-conditional distribution as a **one-dimensional Gaussian (Normal) distribution**:

$$p(X_j = x_j \mid Y = c_k) = \frac{1}{\sqrt{2\pi \sigma_{kj}^2}} \exp\left( -\frac{(x_j - \mu_{kj})^2}{2\sigma_{kj}^2} \right)$$

### Parameter Estimation:
For each class $c_k$ and each feature $j$, calculate the sample mean $\mu_{kj}$ and sample variance $\sigma_{kj}^2$:

$$\mu_{kj} = \frac{1}{N_k} \sum_{i: y_i = c_k} x_{ij}$$

$$\sigma_{kj}^2 = \frac{1}{N_k} \sum_{i: y_i = c_k} (x_{ij} - \mu_{kj})^2$$

In log-space, the Gaussian log-likelihood simplifies to:
$$\ln p(X_j = x_j \mid Y = c_k) = -\frac{1}{2}\ln(2\pi) - \frac{1}{2}\ln(\sigma_{kj}^2) - \frac{(x_j - \mu_{kj})^2}{2\sigma_{kj}^2}$$

---

# 5. The Zero-Probability Pathology and Smoothing Mechanics

## The Multiplicative Veto Phenomenon
The primary vulnerability of the standard maximum likelihood formulation for Naive Bayes is the **Zero-Probability Problem** (also called the *Zero-Frequency Trap*).

Suppose we are training a text classifier on a corpus with vocabulary $\mathcal{V}$. During deployment, we evaluate a test document containing the word *"cryptocurrency"*.
Assume *"cryptocurrency"* appeared zero times in the training examples for class $c_{\text{Spam}}$:

$$P(\text{"cryptocurrency"} \mid c_{\text{Spam}}) = \frac{N_{\text{crypto, spam}}}{N_{\text{spam}}} = \frac{0}{N_{\text{spam}}} = 0.0$$

When computing the posterior likelihood for $c_{\text{Spam}}$:
$$P(c_{\text{Spam}} \mid \mathbf{x}) \propto P(c_{\text{Spam}}) \prod_{j=1}^d P(x_j \mid c_{\text{Spam}}) = P(c_{\text{Spam}}) \times \dots \times 0.0 \times \dots = 0$$

```
P(word_1 | c) * P(word_2 | c) * ... * [ P(unseen_word | c) = 0 ] * ... * P(word_d | c)
                                                    |
                                                    v
                   Zero completely zeroes out the entire product!
```

A single feature value unseen during training acts as a **multiplicative veto**. It reduces the entire product to zero, regardless of how strongly the remaining $999$ features support class $c_{\text{Spam}}$.

---

## Bayesian Priors as Pseudo-Counts
To fix this pathology, we incorporate a **Dirichlet prior** over the categorical likelihood distribution, shifting from maximum likelihood estimation to a Maximum A Posteriori (MAP) parameter estimate.

We introduce imaginary observations called **pseudo-counts**. Before inspecting the training data, we assume that every possible feature outcome has already been observed a baseline number of times.

---

## Laplace (Add-1) Smoothing Derivation
The most common variant is **Laplace Smoothing** (Pierre-Simon Laplace, 1795), where the pseudo-count is set to $1$.

Let $X_j$ be a categorical attribute taking values in a finite domain of cardinality $V_j = |\text{Domain}(X_j)|$.
- Let $N_{kj} = \text{Count}(X_j = v, Y = c_k)$ be the number of training examples in class $c_k$ where feature $j$ takes value $v$.
- Let $N_k = \sum_v N_{kj}$ be the total number of training examples in class $c_k$.

The standard unsmoothed maximum likelihood estimate is:
$$P_{\text{MLE}}(X_j = v \mid Y = c_k) = \frac{N_{kj}}{N_k}$$

To ensure non-zero probabilities, add $1$ to the numerator for every possible outcome. To preserve a valid probability distribution that sums to $1$ ($\sum_{v} P(X_j = v \mid c_k) = 1$), the denominator must increase by the cardinality $V_j$:

> **The Laplace (Add-1) Smoothing Formula:**
> $$\hat{P}_{\text{Laplace}}(X_j = v \mid Y = c_k) = \frac{N_{kj} + 1}{N_k + V_j}$$

### Proof of Valid Probability Distribution:
$$\sum_{v=1}^{V_j} \hat{P}_{\text{Laplace}}(X_j = v \mid Y = c_k) = \sum_{v=1}^{V_j} \frac{N_{kj} + 1}{N_k + V_j} = \frac{\sum_{v=1}^{V_j} N_{kj} + \sum_{v=1}^{V_j} 1}{N_k + V_j} = \frac{N_k + V_j}{N_k + V_j} = 1.0 \quad \blacksquare$$

---

## Lidstone (Add-$\alpha$) Smoothing
Laplace smoothing can over-allocate probability mass to unseen events if the vocabulary size $V$ is large relative to $N$. **Lidstone Smoothing** generalizes this by replacing $1$ with a tunable hyperparameter $\alpha \in (0, 1]$:

$$\hat{P}_{\text{Lidstone}}(X_j = v \mid Y = c_k) = \frac{N_{kj} + \alpha}{N_k + \alpha V_j}$$

- When $\alpha = 1.0$: Recovers standard **Laplace Smoothing**.
- When $\alpha \to 0.0$: Approaches the unsmoothed **Maximum Likelihood Estimate**.
- When $\alpha \ll 1.0$ (e.g., $\alpha = 0.01$): Used in large-vocabulary settings to prevent pseudo-counts from diluting strong empirical evidence.

---

# 6. Comprehensive Step-by-Step Numerical Walkthroughs

## Worked Problem 1: Discrete Text Document Classification (Spam Detection)

### Problem Statement
An email classification engine uses a vocabulary of five words:
$$\mathcal{V} = \{\text{"viagra"}, \text{"lottery"}, \text{"meeting"}, \text{"project"}, \text{"invoice"}\}$$
Vocabulary size $|\mathcal{V}| = 5$.

The system is trained on a small labeled corpus of $N = 8$ documents:
- **Spam ($S$):** 4 documents
- **Ham / Not-Spam ($H$):** 4 documents

The total word occurrence counts across all documents in each class are:

| Vocabulary Word | Count in Spam ($N_{\text{word}, S}$) | Count in Ham ($N_{\text{word}, H}$) |
| :--- | :---: | :---: |
| "viagra" | 12 | 0 |
| "lottery" | 8 | 1 |
| "meeting" | 1 | 14 |
| "project" | 0 | 10 |
| "invoice" | 4 | 5 |
| **Total Word Tokens ($N_{\text{total}}$)** | **$N_S = 25$** | **$N_H = 30$** |

A new test document $D_{\text{test}}$ arrives with the following text:
$$D_{\text{test}} = \text{"invoice project lottery"}$$

1. Calculate the class prior probabilities $P(S)$ and $P(H)$.
2. Calculate the class-conditional likelihoods using **Laplace (Add-1) Smoothing**.
3. Compute the unnormalized posterior values in both standard probability space and log-probability space.
4. Normalize the posteriors to calculate $P(\text{Spam} \mid D_{\text{test}})$ and assign the optimal class label.

---

### Step-by-Step Solution

#### Step 1: Compute Class Priors
Total training documents $N = 8$:
$$P(S) = \frac{4}{8} = 0.50, \quad P(H) = \frac{4}{8} = 0.50$$
In log space:
$$\ln P(S) = \ln(0.50) \approx -0.69315, \quad \ln P(H) = \ln(0.50) \approx -0.69315$$

---

#### Step 2: Compute Smoothed Word Likelihoods
Using the Multinomial Laplace smoothing formula:
$$P(w \mid c) = \frac{\text{Count}(w, c) + 1}{N_c + |\mathcal{V}|}$$
where the vocabulary size $|\mathcal{V}| = 5$.

Denominator terms:
- For Spam ($S$): $N_S + |\mathcal{V}| = 25 + 5 = \mathbf{30}$
- For Ham ($H$): $N_H + |\mathcal{V}| = 30 + 5 = \mathbf{35}$

Compute likelihoods for words in $D_{\text{test}}$:

**For Spam ($S$):**
- $P(\text{"invoice"} \mid S) = \frac{4 + 1}{30} = \frac{5}{30} = \frac{1}{6} \approx \mathbf{0.16667}$
- $P(\text{"project"} \mid S) = \frac{0 + 1}{30} = \frac{1}{30} \approx \mathbf{0.03333}$ *(Resolved zero-frequency)*
- $P(\text{"lottery"} \mid S) = \frac{8 + 1}{30} = \frac{9}{30} = \frac{3}{10} = \mathbf{0.30000}$

**For Ham ($H$):**
- $P(\text{"invoice"} \mid H) = \frac{5 + 1}{35} = \frac{6}{35} \approx \mathbf{0.17143}$
- $P(\text{"project"} \mid H) = \frac{10 + 1}{35} = \frac{11}{35} \approx \mathbf{0.31429}$
- $P(\text{"lottery"} \mid H) = \frac{1 + 1}{35} = \frac{2}{35} \approx \mathbf{0.05714}$

---

#### Step 3: Compute Unnormalized Joint Posteriors

**Standard Probability Space:**

For Spam ($S$):
$$\tilde{P}(S \mid D_{\text{test}}) = P(S) \times P(\text{"invoice"} \mid S) \times P(\text{"project"} \mid S) \times P(\text{"lottery"} \mid S)$$
$$\tilde{P}(S \mid D_{\text{test}}) = 0.50 \times \left(\frac{5}{30}\right) \times \left(\frac{1}{30}\right) \times \left(\frac{9}{30}\right)$$
$$\tilde{P}(S \mid D_{\text{test}}) = 0.50 \times 0.16667 \times 0.03333 \times 0.30000 \approx \mathbf{0.0008333} \quad \left(\frac{45}{54000} = \frac{1}{1200}\right)$$

For Ham ($H$):
$$\tilde{P}(H \mid D_{\text{test}}) = P(H) \times P(\text{"invoice"} \mid H) \times P(\text{"project"} \mid H) \times P(\text{"lottery"} \mid H)$$
$$\tilde{P}(H \mid D_{\text{test}}) = 0.50 \times \left(\frac{6}{35}\right) \times \left(\frac{11}{35}\right) \times \left(\frac{2}{35}\right)$$
$$\tilde{P}(H \mid D_{\text{test}}) = 0.50 \times 0.17143 \times 0.31429 \times 0.05714 \approx \mathbf{0.0015394} \quad \left(\frac{66}{85750} \approx \frac{1}{649.6}\right)$$

---

**Log-Space Verification:**
$$\mathcal{L}(S) = \ln(0.50) + \ln\left(\frac{5}{30}\right) + \ln\left(\frac{1}{30}\right) + \ln\left(\frac{9}{30}\right)$$
$$\mathcal{L}(S) = -0.69315 - 1.79176 - 3.40120 - 1.20397 = \mathbf{-7.09008}$$

$$\mathcal{L}(H) = \ln(0.50) + \ln\left(\frac{6}{35}\right) + \ln\left(\frac{11}{35}\right) + \ln\left(\frac{2}{35}\right)$$
$$\mathcal{L}(H) = -0.69315 - 1.76359 - 1.15745 - 2.86220 = \mathbf{-6.47639}$$

Compare log scores:
$$\mathcal{L}(H) = -6.47639 > \mathcal{L}(S) = -7.09008$$

---

#### Step 4: Normalization and Label Assignment
Compute the marginal evidence:
$$P(D_{\text{test}}) = \tilde{P}(S \mid D_{\text{test}}) + \tilde{P}(H \mid D_{\text{test}}) = 0.0008333 + 0.0015394 = \mathbf{0.0023727}$$

Normalized posterior probabilities:
$$P(\text{Spam} \mid D_{\text{test}}) = \frac{0.0008333}{0.0023727} \approx \mathbf{0.3512} \quad (35.12\%)$$
$$P(\text{Ham} \mid D_{\text{test}}) = \frac{0.0015394}{0.0023727} \approx \mathbf{0.6488} \quad (64.88\%)$$

**Decision:** The classifier assigns $D_{\text{test}}$ to **Ham (Not-Spam)**:
$$\hat{y} = \mathbf{Ham}$$

---

## Worked Problem 2: Full Categorical Dataset Classification with Laplace Correction

### Problem Statement
A banking dataset classifies customer fraud risk ($Y \in \{\text{Low}, \text{High}\}$) using three categorical attributes:
- **Income ($X_1$):** $\{\text{Low}, \text{Medium}, \text{High}\}$ $\implies V_1 = 3$
- **Job_Stability ($X_2$):** $\{\text{Unstable}, \text{Stable}\}$ $\implies V_2 = 2$
- **Payment_History ($X_3$):** $\{\text{Poor}, \text{Fair}, \text{Good}\}$ $\implies V_3 = 3$

The training corpus contains $N = 10$ records:

| Record | Income ($X_1$) | Job_Stability ($X_2$) | Payment_History ($X_3$) | Fraud_Risk ($Y$) |
| :---: | :---: | :---: | :---: | :---: |
| 1 | Low | Unstable | Poor | **High** |
| 2 | Low | Unstable | Fair | **High** |
| 3 | Medium | Unstable | Poor | **High** |
| 4 | High | Stable | Good | **Low** |
| 5 | High | Stable | Fair | **Low** |
| 6 | Medium | Stable | Good | **Low** |
| 7 | High | Unstable | Poor | **High** |
| 8 | Low | Stable | Poor | **High** |
| 9 | Medium | Stable | Good | **Low** |
| 10 | High | Stable | Good | **Low** |

A new applicant presents the profile:
$$\mathbf{x}^* = [\text{Income}=\text{Medium}, \text{Job\_Stability}=\text{Unstable}, \text{Payment\_History}=\text{Good}]^T$$

Classify the applicant using **Naive Bayes with Laplace (Add-1) Smoothing**.

---

### Step-by-Step Solution

#### Step 1: Compute Class Counts and Prior Probabilities
Total samples $N = 10$:
- Target Class $Y = \text{High}$: $N_{\text{High}} = 5$ (Records 1, 2, 3, 7, 8)
- Target Class $Y = \text{Low}$: $N_{\text{Low}} = 5$ (Records 4, 5, 6, 9, 10)

Priors:
$$P(\text{High}) = \frac{5}{10} = 0.50, \quad P(\text{Low}) = \frac{5}{10} = 0.50$$

---

#### Step 2: Compute Feature Counts Conditioned on Class

**Counts for Class $Y = \text{High}$ ($N_{\text{High}} = 5$):**
- **Income ($X_1$):** Low: 3, Medium: 1, High: 1
- **Job_Stability ($X_2$):** Unstable: 4, Stable: 1
- **Payment_History ($X_3$):** Poor: 4, Fair: 1, Good: 0 *(Note the zero count)*

**Counts for Class $Y = \text{Low}$ ($N_{\text{Low}} = 5$):**
- **Income ($X_1$):** Low: 0, Medium: 2, High: 3
- **Job_Stability ($X_2$):** Unstable: 0, Stable: 5
- **Payment_History ($X_3$):** Poor: 0, Fair: 1, Good: 4

---

#### Step 3: Compute Smoothed Likelihoods for Query $\mathbf{x}^*$
Using $\hat{P}(X_j = v \mid c) = \frac{N_{c, X_j=v} + 1}{N_c + V_j}$:

**For Class $Y = \text{High}$ ($N_{\text{High}} = 5$):**
- Income = Medium ($V_1 = 3$):
  $$P(X_1 = \text{Medium} \mid \text{High}) = \frac{1 + 1}{5 + 3} = \frac{2}{8} = \mathbf{0.250}$$
- Job_Stability = Unstable ($V_2 = 2$):
  $$P(X_2 = \text{Unstable} \mid \text{High}) = \frac{4 + 1}{5 + 2} = \frac{5}{7} \approx \mathbf{0.71429}$$
- Payment_History = Good ($V_3 = 3$):
  $$P(X_3 = \text{Good} \mid \text{High}) = \frac{0 + 1}{5 + 3} = \frac{1}{8} = \mathbf{0.125}$$

**For Class $Y = \text{Low}$ ($N_{\text{Low}} = 5$):**
- Income = Medium ($V_1 = 3$):
  $$P(X_1 = \text{Medium} \mid \text{Low}) = \frac{2 + 1}{5 + 3} = \frac{3}{8} = \mathbf{0.375}$$
- Job_Stability = Unstable ($V_2 = 2$):
  $$P(X_2 = \text{Unstable} \mid \text{Low}) = \frac{0 + 1}{5 + 2} = \frac{1}{7} \approx \mathbf{0.14286}$$
- Payment_History = Good ($V_3 = 3$):
  $$P(X_3 = \text{Good} \mid \text{Low}) = \frac{4 + 1}{5 + 3} = \frac{5}{8} = \mathbf{0.625}$$

---

#### Step 4: Compute Posterior Numerators
$$\tilde{P}(\text{High} \mid \mathbf{x}^*) = P(\text{High}) \cdot P(X_1=\text{Med} \mid \text{High}) \cdot P(X_2=\text{Unst} \mid \text{High}) \cdot P(X_3=\text{Good} \mid \text{High})$$
$$\tilde{P}(\text{High} \mid \mathbf{x}^*) = 0.50 \times \left(\frac{2}{8}\right) \times \left(\frac{5}{7}\right) \times \left(\frac{1}{8}\right)$$
$$\tilde{P}(\text{High} \mid \mathbf{x}^*) = 0.50 \times 0.250 \times 0.71429 \times 0.125 = \mathbf{0.011161}$$

$$\tilde{P}(\text{Low} \mid \mathbf{x}^*) = P(\text{Low}) \cdot P(X_1=\text{Med} \mid \text{Low}) \cdot P(X_2=\text{Unst} \mid \text{Low}) \cdot P(X_3=\text{Good} \mid \text{Low})$$
$$\tilde{P}(\text{Low} \mid \mathbf{x}^*) = 0.50 \times \left(\frac{3}{8}\right) \times \left(\frac{1}{7}\right) \times \left(\frac{5}{8}\right)$$
$$\tilde{P}(\text{Low} \mid \mathbf{x}^*) = 0.50 \times 0.375 \times 0.14286 \times 0.625 = \mathbf{0.016741}$$

---

#### Step 5: Posterior Probabilities and Classification Decision
Normalizing factor:
$$P(\mathbf{x}^*) = 0.011161 + 0.016741 = \mathbf{0.027902}$$

Final posterior probabilities:
$$P(\text{High} \mid \mathbf{x}^*) = \frac{0.011161}{0.027902} \approx \mathbf{0.4000} \quad (40.0\%)$$
$$P(\text{Low} \mid \mathbf{x}^*) = \frac{0.016741}{0.027902} \approx \mathbf{0.6000} \quad (60.0\%)$$

**Decision:**
$$P(\text{Low} \mid \mathbf{x}^*) > P(\text{High} \mid \mathbf{x}^*) \implies \hat{y} = \mathbf{Low}$$

---

## Worked Problem 3: Continuous Gaussian Naive Bayes Parameterization & Inference

### Problem Statement
A medical diagnostics team classifies whether a patient has diabetes ($Y \in \{0, 1\}$) using two continuous blood biomarkers:
- **Glucose ($X_1$)** in $\text{mg/dL}$
- **Insulin ($X_2$)** in $\mu\text{U/mL}$

The training process yields the following parameter estimates:

| Parameter | Class 0 (Non-Diabetic) | Class 1 (Diabetic) |
| :--- | :---: | :---: |
| **Class Prior $P(Y)$** | $0.70$ | $0.30$ |
| **Mean Glucose $\mu_1$** | $100.0$ | $160.0$ |
| **Variance Glucose $\sigma_1^2$** | $225.0$ ($\sigma_1 = 15.0$) | $400.0$ ($\sigma_1 = 20.0$) |
| **Mean Insulin $\mu_2$** | $80.0$ | $140.0$ |
| **Variance Insulin $\sigma_2^2$** | $100.0$ ($\sigma_2 = 10.0$) | $625.0$ ($\sigma_2 = 25.0$) |

A patient arrives with biomarker readings:
$$\mathbf{x} = [x_1 = 130.0, x_2 = 110.0]^T$$

1. Formulate the Gaussian probability density function for each feature conditioned on each class.
2. Evaluate the conditional likelihoods for the patient.
3. Compute the unnormalized posteriors and classify the patient.
4. Calculate the exact calibrated posterior probability of diabetes $P(Y = 1 \mid \mathbf{x})$.

---

### Step-by-Step Solution

#### Step 1: The 1D Gaussian Density Equation
$$p(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi \sigma^2}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$

---

#### Step 2: Evaluate Likelihoods for Class 0 ($Y = 0$)

**Feature 1: Glucose ($x_1 = 130.0$):**
- $\mu_{0,1} = 100.0, \quad \sigma_{0,1}^2 = 225.0$
- Normalized distance: $(x_1 - \mu)^2 = (130 - 100)^2 = 30^2 = 900$
- Exponent: $-\frac{900}{2 \times 225} = -\frac{900}{450} = -2.0$
$$p(x_1 = 130 \mid Y = 0) = \frac{1}{\sqrt{2\pi \times 225}} e^{-2.0} = \frac{1}{15 \sqrt{2\pi}} e^{-2.0}$$
Using $\sqrt{2\pi} \approx 2.50663$:
$$p(x_1 = 130 \mid Y = 0) = \frac{1}{37.5994} \times 0.135335 \approx \mathbf{0.0035994}$$

**Feature 2: Insulin ($x_2 = 110.0$):**
- $\mu_{0,2} = 80.0, \quad \sigma_{0,2}^2 = 100.0$
- Normalized distance: $(x_2 - \mu)^2 = (110 - 80)^2 = 30^2 = 900$
- Exponent: $-\frac{900}{2 \times 100} = -\frac{900}{200} = -4.5$
$$p(x_2 = 110 \mid Y = 0) = \frac{1}{\sqrt{2\pi \times 100}} e^{-4.5} = \frac{1}{10 \sqrt{2\pi}} e^{-4.5}$$
$$p(x_2 = 110 \mid Y = 0) = \frac{1}{25.0663} \times 0.011109 \approx \mathbf{0.00044319}$$

**Joint Feature Likelihood for Class 0:**
$$p(\mathbf{x} \mid Y = 0) = p(x_1 \mid 0) \times p(x_2 \mid 0) = 0.0035994 \times 0.00044319 \approx \mathbf{1.5952 \times 10^{-6}}$$

---

#### Step 3: Evaluate Likelihoods for Class 1 ($Y = 1$)

**Feature 1: Glucose ($x_1 = 130.0$):**
- $\mu_{1,1} = 160.0, \quad \sigma_{1,1}^2 = 400.0$
- Normalized distance: $(x_1 - \mu)^2 = (130 - 160)^2 = (-30)^2 = 900$
- Exponent: $-\frac{900}{2 \times 400} = -\frac{900}{800} = -1.125$
$$p(x_1 = 130 \mid Y = 1) = \frac{1}{\sqrt{2\pi \times 400}} e^{-1.125} = \frac{1}{20 \sqrt{2\pi}} e^{-1.125}$$
$$p(x_1 = 130 \mid Y = 1) = \frac{1}{50.1326} \times 0.32465 \approx \mathbf{0.0064759}$$

**Feature 2: Insulin ($x_2 = 110.0$):**
- $\mu_{1,2} = 140.0, \quad \sigma_{1,2}^2 = 625.0$
- Normalized distance: $(x_2 - \mu)^2 = (110 - 140)^2 = (-30)^2 = 900$
- Exponent: $-\frac{900}{2 \times 625} = -\frac{900}{1250} = -0.720$
$$p(x_2 = 110 \mid Y = 1) = \frac{1}{\sqrt{2\pi \times 625}} e^{-0.720} = \frac{1}{25 \sqrt{2\pi}} e^{-0.720}$$
$$p(x_2 = 110 \mid Y = 1) = \frac{1}{62.6657} \times 0.48675 \approx \mathbf{0.0077674}$$

**Joint Feature Likelihood for Class 1:**
$$p(\mathbf{x} \mid Y = 1) = p(x_1 \mid 1) \times p(x_2 \mid 1) = 0.0064759 \times 0.0077674 \approx \mathbf{5.0301 \times 10^{-5}}$$

---

#### Step 4: Compute Posterior Numerators
Multiply by class priors:

**For Class 0:**
$$\tilde{P}(Y = 0 \mid \mathbf{x}) = P(Y = 0) \cdot p(\mathbf{x} \mid Y = 0) = 0.70 \times (1.5952 \times 10^{-6}) = \mathbf{1.1166 \times 10^{-6}}$$

**For Class 1:**
$$\tilde{P}(Y = 1 \mid \mathbf{x}) = P(Y = 1) \cdot p(\mathbf{x} \mid Y = 1) = 0.30 \times (5.0301 \times 10^{-5}) = \mathbf{1.5090 \times 10^{-5}}$$

---

#### Step 5: Normalization and Final Classification
Sum the unnormalized terms to calculate the evidence $p(\mathbf{x})$:
$$p(\mathbf{x}) = (1.1166 \times 10^{-6}) + (1.5090 \times 10^{-5}) = (1.1166 \times 10^{-6}) + (15.0903 \times 10^{-6}) = \mathbf{1.6207 \times 10^{-5}}$$

Posterior probabilities:
$$P(Y = 0 \mid \mathbf{x}) = \frac{1.1166 \times 10^{-6}}{1.6207 \times 10^{-5}} \approx \mathbf{0.0689} \quad (6.89\%)$$
$$P(Y = 1 \mid \mathbf{x}) = \frac{1.5090 \times 10^{-5}}{1.6207 \times 10^{-5}} \approx \mathbf{0.9311} \quad (93.11\%)$$

**Decision:** The classifier predicts **Diabetic**:
$$\hat{y} = \mathbf{1} \quad (P = 93.11\%)$$

---

## Worked Problem 4: Resolving the Zero-Frequency Trap in Tabular Data

### Problem Statement
An autonomous IT operations classifier flags server log metrics as either **Normal Operation ($C_1$)** or **Under Attack ($C_2$)**. A discrete audit feature $X_A$ indicates protocol status across three states:
$$\text{Domain}(X_A) = \{\text{TCP\_ERR}, \text{AUTH\_FAIL}, \text{PORT\_SCAN}\} \implies V_A = 3$$

The training distribution contains:
- Total Normal sessions ($C_1$): $N_1 = 500$
- Total Attack sessions ($C_2$): $N_2 = 100$

Counts for attribute $X_A$:
- $C_1 (Normal): \text{TCP\_ERR} = 150, \quad \text{AUTH\_FAIL} = 5, \quad \text{PORT\_SCAN} = 0$
- $C_2 (Attack): \text{TCP\_ERR} = 10, \quad \text{AUTH\_FAIL} = 40, \quad \text{PORT\_SCAN} = 50$

A log entry arrives with $X_A = \text{PORT\_SCAN}$.
1. Compute the raw maximum likelihood estimate $P_{\text{MLE}}(\text{PORT\_SCAN} \mid C_1)$. Show how it creates a zero-frequency pathology.
2. Apply **Laplace Smoothing** ($\alpha = 1$). Recompute the probabilities for all three states in $C_1$ and verify they sum to $1.0$.
3. Apply **Lidstone Smoothing** with parameter $\alpha = 0.1$. Compare the result with Laplace smoothing.

---

### Step-by-Step Solution

#### Step 1: Raw MLE Evaluation
$$P_{\text{MLE}}(\text{PORT\_SCAN} \mid C_1) = \frac{N_{C_1, \text{PORT\_SCAN}}}{N_1} = \frac{0}{500} = \mathbf{0.0}$$
Because the term is $0.0$, observing a single port scan sets the posterior probability of Normal Operation to zero:
$$P(C_1 \mid \mathbf{x}) \propto P(C_1) \cdot P(X_1 \mid C_1) \cdots 0.0 \cdots P(X_d \mid C_1) = 0$$
even if all other features are typical of normal server activity.

---

#### Step 2: Laplace (Add-1) Smoothing
Formula:
$$\hat{P}_{\text{Laplace}}(X_A = v \mid C_1) = \frac{N_{C_1, v} + 1}{N_1 + V_A}$$
where $V_A = 3$ and $N_1 = 500$. Denominator = $500 + 3 = \mathbf{503}$.

Compute smoothed estimates:
- $P(\text{TCP\_ERR} \mid C_1) = \frac{150 + 1}{503} = \frac{151}{503} \approx \mathbf{0.30020}$
- $P(\text{AUTH\_FAIL} \mid C_1) = \frac{5 + 1}{503} = \frac{6}{503} \approx \mathbf{0.01193}$
- $P(\text{PORT\_SCAN} \mid C_1) = \frac{0 + 1}{503} = \frac{1}{503} \approx \mathbf{0.00199}$

**Summation Check:**
$$\sum_v P(X_A = v \mid C_1) = \frac{151 + 6 + 1}{503} = \frac{503}{503} = \mathbf{1.00000} \quad \checkmark$$

The zero has been replaced with a small probability ($0.00199$), eliminating the multiplicative veto while properly reflecting that port scans are rare during normal operations.

---

#### Step 3: Lidstone ($\alpha = 0.1$) Smoothing
Formula:
$$\hat{P}_{\text{Lidstone}}(X_A = v \mid C_1) = \frac{N_{C_1, v} + 0.1}{N_1 + (0.1 \times 3)} = \frac{N_{C_1, v} + 0.1}{500 + 0.3} = \frac{N_{C_1, v} + 0.1}{500.3}$$

Compute estimates:
- $P(\text{TCP\_ERR} \mid C_1) = \frac{150 + 0.1}{500.3} = \frac{150.1}{500.3} \approx \mathbf{0.30002}$
- $P(\text{AUTH\_FAIL} \mid C_1) = \frac{5 + 0.1}{500.3} = \frac{5.1}{500.3} \approx \mathbf{0.01019}$
- $P(\text{PORT\_SCAN} \mid C_1) = \frac{0 + 0.1}{500.3} = \frac{0.1}{500.3} \approx \mathbf{0.00020}$

**Comparison:**
- Under Laplace ($\alpha = 1.0$), $P(\text{PORT\_SCAN} \mid C_1) = \frac{1}{503} \approx 0.00199$
- Under Lidstone ($\alpha = 0.1$), $P(\text{PORT\_SCAN} \mid C_1) = \frac{0.1}{500.3} \approx 0.00020$

Lidstone smoothing with $\alpha = 0.1$ assigns less probability mass to unobserved events, keeping probability estimates closer to the empirical sample frequencies.

---

# 7. KTU University Examination Practice Questions

## Short-Answer Analytical Problems (Part A)

### Question 1: Mathematical Basis of the Conditional Independence Assumption
> **Question:** State the class-conditional independence assumption in Naive Bayes. Why is this assumption necessary for high-dimensional feature spaces? *(3 Marks)*

**Model Answer:** The class-conditional independence assumption states that all features $X_1, X_2, \dots, X_d$ are statistically independent of each other given the class label $Y = c_k$:
$$P(X_1, X_2, \dots, X_d \mid Y = c_k) = \prod_{j=1}^d P(X_j \mid Y = c_k)$$
This assumption is necessary to avoid the **combinatorial explosion** of parameters. Without it, an unconstrained joint distribution over $d$ binary attributes requires estimating $K(2^d - 1)$ parameters, which quickly becomes computationally intractable. Conditional independence reduces parameter complexity to $K \cdot d$, making learning linear with respect to dimension $d$.

---

### Question 2: Eliminating the Denominator Evidence
> **Question:** In the derivation of the Naive Bayes classification rule, explain why the marginal evidence $P(\mathbf{x})$ can be safely omitted during the argmax step. *(3 Marks)*

**Model Answer:** Bayes' Theorem expresses the posterior as:
$$P(Y = c_k \mid \mathbf{x}) = \frac{P(\mathbf{x} \mid c_k)P(c_k)}{P(\mathbf{x})}$$
The denominator is:
$$P(\mathbf{x}) = \sum_{j=1}^K P(\mathbf{x} \mid c_j)P(c_j)$$
This value is strictly a function of the input feature vector $\mathbf{x}$ and the model parameters. It is constant across all candidate classes $c_k$. Because $P(\mathbf{x}) > 0$, dividing by it scales all posterior values uniformly without changing their relative order:
$$\arg\max_{c_k} \frac{P(\mathbf{x} \mid c_k)P(c_k)}{P(\mathbf{x})} \equiv \arg\max_{c_k} \Big[ P(\mathbf{x} \mid c_k)P(c_k) \Big]$$
Thus, the denominator can be omitted when selecting the most likely class.

---

### Question 3: The Zero-Probability Problem and Laplace Correction
> **Question:** What is the zero-probability problem in Naive Bayes classification? State the Laplace smoothing formula and explain the purpose of the denominator term. *(3 Marks)*

**Model Answer:** The zero-probability problem occurs when a test instance contains a feature value unseen in the training set for a given class ($N_{kj} = 0$). Its maximum likelihood estimate evaluates to zero ($P(x_j \mid c_k) = 0$). In the product rule:
$$\prod_{j=1}^d P(x_j \mid c_k)$$
this zero acts as a multiplicative veto, forcing the entire joint likelihood to zero regardless of other supporting evidence.

The **Laplace smoothing formula** resolves this by adding pseudo-counts:
$$\hat{P}(X_j = v \mid c_k) = \frac{N_{kj} + 1}{N_k + V_j}$$
The term $V_j = |\text{Domain}(X_j)|$ is added to the denominator to balance the $V_j$ ones added to the numerator, ensuring the probabilities across all categories sum to $1.0$.

---

## Comprehensive Essay & Derivation Questions (Part B)

### Question 4: End-to-End Derivation and Comparison of Event Models
> **Question:** > (a) Derive the log-space decision rule of the Naive Bayes classifier from first principles. Explain the computational reason for adopting the log transform. *(8 Marks)* > (b) Contrast Multivariate Bernoulli Naive Bayes with Multinomial Naive Bayes regarding input representations, likelihood formulations, and typical use cases. *(6 Marks)*

**Model Answer Outline:**
- **Part (a):**
  1. Define the probabilistic classification objective using the Maximum A Posteriori (MAP) criterion: $\hat{y} = \arg\max_{c_k} P(c_k \mid \mathbf{x})$.
  2. Apply Bayes' theorem to express the posterior in terms of prior and likelihood.
  3. Show the cancellation of the class-invariant denominator $P(\mathbf{x})$.
  4. Apply the class-conditional independence assumption to factor the joint likelihood into $\prod_{j=1}^d P(x_j \mid c_k)$.
  5. Apply the monotonic natural log transform $\ln(\cdot)$ to convert the product into a summation:
     $$\hat{y} = \arg\max_{c_k} \left[ \ln P(c_k) + \sum_{j=1}^d \ln P(x_j \mid c_k) \right]$$
  6. Explain the computational motivation: in high dimensions ($d > 1,000$), multiplying small probabilities causes **arithmetic underflow** in IEEE 754 floating-point systems. Log transformation converts these operations into stable summations.
- **Part (b):**
  - **Multivariate Bernoulli Naive Bayes:**
    - *Features:* Binary vectors $\mathbf{x} \in \{0, 1\}^d$ indicating word presence or absence.
    - *Likelihood:* $P(\mathbf{x} \mid c) = \prod_{j=1}^d p_{cj}^{x_j}(1 - p_{cj})^{1 - x_j}$. Penalizes both the presence of unexpected words and the absence of expected words.
    - *Applications:* Short text classification, sentiment detection.
  - **Multinomial Naive Bayes:**
    - *Features:* Integer count vectors $\mathbf{x} \in \mathbb{N}^d$ representing word frequencies.
    - *Likelihood:* $P(\mathbf{x} \mid c) \propto \prod_{j=1}^d \theta_{cj}^{x_j}$. Scales with the frequency of occurrences and ignores words not present in the document.
    - *Applications:* Long-form document classification, topic modeling, spam filtering.

---

### Question 5: Complete Tabular Classification Problem
> **Question:** > The following training dataset records clinical data for predicting heart disease ($Y \in \{\text{Yes}, \text{No}\}$):
>
> | Patient | Chest_Pain | High_BP | High_Chol | Heart_Disease |
> | :---: | :---: | :---: | :---: | :---: |
> | 1 | Yes | Yes | High | **Yes** |
> | 2 | Yes | Yes | Normal | **Yes** |
> | 3 | No | Yes | High | **Yes** |
> | 4 | No | No | Normal | **No** |
> | 5 | Yes | No | High | **No** |
> | 6 | No | Yes | Normal | **No** |
> | 7 | No | No | High | **No** |
> | 8 | Yes | No | Normal | **Yes** |
>
> (a) Compute the prior probabilities $P(\text{Heart\_Disease} = \text{Yes})$ and $P(\text{Heart\_Disease} = \text{No})$. *(2 Marks)* > (b) Using Laplace (Add-1) smoothing, construct the probability lookup tables for all features conditioned on each class. *(8 Marks)* > (c) Classify a new patient presenting with:  
> $\mathbf{x}_{\text{new}} = [\text{Chest\_Pain}=\text{No}, \text{High\_BP}=\text{No}, \text{High\_Chol}=\text{High}]^T$.  
> Show all intermediate calculations and output the calibrated posterior probabilities. *(4 Marks)*

**Model Answer Outline:**
- **Part (a):** Total $N = 8$. Counts: $\text{Yes} = 4, \quad \text{No} = 4$.
  $$P(\text{Yes}) = \frac{4}{8} = 0.50, \quad P(\text{No}) = \frac{4}{8} = 0.50$$
- **Part (b):** Cardinals: $V_{\text{Chest}} = 2$, $V_{\text{BP}} = 2$, $V_{\text{Chol}} = 2$. Denominators for both classes: $N_c + V = 4 + 2 = 6$.
  - *Class Yes ($N=4$):*
    - Chest_Pain: $\text{Yes} = \frac{3+1}{6} = \frac{4}{6}$, $\text{No} = \frac{1+1}{6} = \frac{2}{6}$
    - High_BP: $\text{Yes} = \frac{3+1}{6} = \frac{4}{6}$, $\text{No} = \frac{1+1}{6} = \frac{2}{6}$
    - High_Chol: $\text{High} = \frac{2+1}{6} = \frac{3}{6}$, $\text{Normal} = \frac{2+1}{6} = \frac{3}{6}$
  - *Class No ($N=4$):*
    - Chest_Pain: $\text{Yes} = \frac{1+1}{6} = \frac{2}{6}$, $\text{No} = \frac{3+1}{6} = \frac{4}{6}$
    - High_BP: $\text{Yes} = \frac{2+1}{6} = \frac{3}{6}$, $\text{No} = \frac{2+1}{6} = \frac{3}{6}$
    - High_Chol: $\text{High} = \frac{2+1}{6} = \frac{3}{6}$, $\text{Normal} = \frac{2+1}{6} = \frac{3}{6}$
- **Part (c):** For query $\mathbf{x}_{\text{new}} = [\text{No}, \text{No}, \text{High}]$:
  - Unnormalized Yes:
    $$\tilde{P}(\text{Yes} \mid \mathbf{x}) = 0.50 \times \left(\frac{2}{6}\right) \times \left(\frac{2}{6}\right) \times \left(\frac{3}{6}\right) = 0.50 \times \frac{12}{216} = \frac{6}{216} \approx \mathbf{0.02778}$$
  - Unnormalized No:
    $$\tilde{P}(\text{No} \mid \mathbf{x}) = 0.50 \times \left(\frac{4}{6}\right) \times \left(\frac{3}{6}\right) \times \left(\frac{3}{6}\right) = 0.50 \times \frac{36}{216} = \frac{18}{216} \approx \mathbf{0.08333}$$
  - Evidence:
    $$P(\mathbf{x}) = \frac{6}{216} + \frac{18}{216} = \frac{24}{216} \approx 0.11111$$
  - Normalized Posteriors:
    $$P(\text{Yes} \mid \mathbf{x}_{\text{new}}) = \frac{6}{24} = \mathbf{0.250} \quad (25.0\%)$$
    $$P(\text{No} \mid \mathbf{x}_{\text{new}}) = \frac{18}{24} = \mathbf{0.750} \quad (75.0\%)$$
  - **Decision:** The classifier predicts **No Heart Disease**:
    $$\hat{y} = \mathbf{No}$$
