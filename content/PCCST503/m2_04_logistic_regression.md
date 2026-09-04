# Module 2: Supervised Learning — Logistic Regression
## Linear Decision Boundaries, Sigmoid Activation, and Maximum Likelihood Estimation

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Module Alignment:** Module 2 (Supervised Learning & Discriminative Classifiers)  
> **Prerequisites:** Multivariable Calculus, Linear Algebra (Vector Products), Probability Foundations, and Ordinary Least Squares (OLS) Regression.

---

# Table of Contents
1. [The Discriminative Classification Paradigm](#1-the-discriminative-classification-paradigm)
   - [Generative vs. Discriminative Models](#generative-vs-discriminative-models)
   - [The Failure of Ordinary Least Squares (OLS) for Classification](#the-failure-of-ordinary-least-squares-ols-for-classification)
   - [Structural Requirements of a Probabilistic Classifier](#structural-requirements-of-a-probabilistic-classifier)
2. [Mathematical Architecture of Logistic Regression](#2-mathematical-architecture-of-logistic-regression)
   - [The Sigmoid (Logistic) Function and Its Properties](#the-sigmoid-logistic-function-and-its-properties)
   - [Mapping the Linear Combiner to Probability Space](#mapping-the-linear-combiner-to-probability-space)
   - [The Decision Boundary: Equating to the Hyperplane](#the-decision-boundary-equating-to-the-hyperplane)
3. [The Odds Ratio and Logit Transformation](#3-the-odds-ratio-and-logit-transformation)
   - [Deriving the Odds Ratio](#deriving-the-odds-ratio)
   - [The Log-Odds (Logit) Function](#the-log-odds-logit-function)
   - [Interpretability of the Weights (Coefficients)](#interpretability-of-the-weights-coefficients)
4. [Parameter Estimation via Maximum Likelihood](#4-parameter-estimation-via-maximum-likelihood)
   - [Formulating the Bernoulli Likelihood Function](#formulating-the-bernoulli-likelihood-function)
   - [Deriving the Binary Cross-Entropy (Log Loss) Cost Function](#deriving-the-binary-cross-entropy-log-loss-cost-function)
   - [Convexity and Global Optimization](#convexity-and-global-optimization)
5. [Optimization Mechanics: Gradient Descent Formulation](#5-optimization-mechanics-gradient-descent-formulation)
   - [Derivation of the Gradient Vector](#derivation-of-the-gradient-vector)
   - [The Gradient Descent Update Rule](#the-gradient-descent-update-rule)
   - [Batch vs. Stochastic Gradient Descent](#batch-vs-stochastic-gradient-descent)
6. [Extension to Multiclass: Multinomial Logistic Regression](#6-extension-to-multiclass-multinomial-logistic-regression)
   - [The Softmax Activation Function](#the-softmax-activation-function)
   - [One-vs-Rest (OvR) vs. Cross-Entropy Optimization](#one-vs-rest-ovr-vs-cross-entropy-optimization)
7. [Comprehensive Step-by-Step Numerical Walkthroughs](#7-comprehensive-step-by-step-numerical-walkthroughs)
   - [Worked Problem 1: Manual Calculation of the Logistic Forward Pass](#worked-problem-1-manual-calculation-of-the-logistic-forward-pass)
   - [Worked Problem 2: Interpretation of Odds Ratios in Medical Data](#worked-problem-2-interpretation-of-odds-ratios-in-medical-data)
   - [Worked Problem 3: Execution of a Single Gradient Descent Update Step](#worked-problem-3-execution-of-a-single-gradient-descent-update-step)
   - [Worked Problem 4: Defining the Equation of the Linear Decision Boundary](#worked-problem-4-defining-the-equation-of-the-linear-decision-boundary)
8. [KTU University Examination Practice Questions](#8-ktu-university-examination-practice-questions)
   - [Short-Answer Analytical Problems (Part A)](#short-answer-analytical-problems-part-a)
   - [Comprehensive Essay & Derivation Questions (Part B)](#comprehensive-essay--derivation-questions-part-b)

---

# 1. The Discriminative Classification Paradigm

## Generative vs. Discriminative Models
Statistical classifiers fall into two broad architectural categories:

1. **Generative Models (e.g., Naive Bayes, Hidden Markov Models):**
   Generative models construct a full joint probability distribution $P(\mathbf{X}, Y)$. They attempt to learn *how the data was generated* for each class by modeling the class priors $P(Y)$ and the class-conditional likelihoods $P(\mathbf{X} \mid Y)$. Classification is performed indirectly using Bayes' Theorem.
2. **Discriminative Models (e.g., Logistic Regression, Support Vector Machines):**
   Discriminative models skip the intermediate step of modeling the joint distribution. Instead, they directly estimate the posterior probability mapping $P(Y \mid \mathbf{X})$ or directly construct a decision boundary separating the classes in the feature space.

**Logistic Regression** is a discriminative probabilistic classifier. It models the conditional probability $P(Y=1 \mid \mathbf{x})$ directly as a parameterized function of $\mathbf{x}$.

## The Failure of Ordinary Least Squares (OLS) for Classification
Suppose we have a binary classification task where $Y \in \{0, 1\}$. Why can't we simply apply a standard Linear Regression model, $\hat{y} = \mathbf{w}^T \mathbf{x} + b$, and threshold the output?

Applying OLS to classification fails for three critical reasons:
1. **Unbounded Output Range:** Linear regression outputs values in the domain $(-\infty, +\infty)$. For a classification model to output valid probabilities, its output must be strictly bounded within the range $[0, 1]$. An output of $\hat{y} = 2.5$ or $\hat{y} = -1.2$ has no valid probabilistic interpretation.
2. **Sensitivity to Outliers:** OLS optimizes the Mean Squared Error (MSE). A point correctly classified but lying very far past the decision boundary will generate a massive squared error (because $\mathbf{w}^T\mathbf{x} \gg 1$), skewing the decision boundary away from the optimal separation point to compensate for the "outlier."
3. **Non-Normal Error Distributions:** OLS assumes that the residual errors are normally distributed. In binary classification, the residuals $\epsilon = y - \hat{y}$ can only take on two distinct values for any given $\hat{y}$, severely violating the normality assumption.

## Structural Requirements of a Probabilistic Classifier
To construct a valid probabilistic classifier using a linear combination of features, we require a mathematical "squashing" function $g(z)$ that satisfies:
1. **Boundedness:** $\lim_{z \to -\infty} g(z) = 0$ and $\lim_{z \to +\infty} g(z) = 1$.
2. **Monotonicity:** $g'(z) > 0$ for all $z$, ensuring that as the linear score increases, the probability strictly increases.
3. **Symmetry and Smoothness:** Continuous and differentiable everywhere, allowing for gradient-based optimization.

---

# 2. Mathematical Architecture of Logistic Regression

## The Sigmoid (Logistic) Function and Its Properties
The standard function fulfilling these requirements is the **logistic sigmoid function**:

$$g(z) = \sigma(z) = \frac{1}{1 + e^{-z}}$$

```
Probability P(Y=1)
 1.0 ^                                        .-------
     |                                   . -
 0.8 |                               . -
     |                             .
 0.6 |                           .
     |                         .
 0.5 +-------------------------*-------------------------
     |                       . |
 0.4 |                     .   |
     |                   .     |
 0.2 |               . -       |
     |           . -           |
 0.0 +-------*-----------------+-----------------------> Linear Score (z)
           -4.0      -2.0     0.0      2.0      4.0
```

**Key Mathematical Properties:**
1. **Domain and Range:** Maps $z \in (-\infty, +\infty)$ into the open interval $(0, 1)$.
2. **Symmetry Point:** When $z = 0$, $\sigma(0) = \frac{1}{1 + 1} = 0.5$.
3. **Complementary Property:** $\sigma(-z) = 1 - \sigma(z)$.
4. **Derivative:** The derivative of the sigmoid function can be elegantly expressed in terms of the function itself:
   $$\frac{d}{dz}\sigma(z) = \sigma(z)(1 - \sigma(z))$$

*Proof of the Derivative:*
$$\frac{d}{dz} (1 + e^{-z})^{-1} = -1(1 + e^{-z})^{-2}(-e^{-z}) = \frac{e^{-z}}{(1 + e^{-z})^2}$$
$$= \left( \frac{1}{1 + e^{-z}} \right) \left( \frac{e^{-z}}{1 + e^{-z}} \right) = \sigma(z) \left( \frac{1 + e^{-z} - 1}{1 + e^{-z}} \right) = \sigma(z)(1 - \sigma(z)) \quad \blacksquare$$

## Mapping the Linear Combiner to Probability Space
Logistic regression constructs a linear combination of the input features $\mathbf{x} = [x_1, x_2, \dots, x_d]^T$ and a weight vector $\mathbf{w} = [w_1, w_2, \dots, w_d]^T$ with a bias scalar $b$.

The intermediate scalar score $z$ (often called the *logit* or *activation*) is:
$$z = \mathbf{w}^T \mathbf{x} + b = w_1x_1 + w_2x_2 + \dots + w_dx_d + b$$

To simplify notation, we absorb the bias $b$ into the weight vector by appending a constant $x_0 = 1$ to every feature vector:
$$\mathbf{w} = [b, w_1, w_2, \dots, w_d]^T$$
$$\mathbf{x} = [1, x_1, x_2, \dots, x_d]^T$$
$$z = \mathbf{w}^T \mathbf{x}$$

The final hypothesis function defines the probability that the instance belongs to the positive class ($Y=1$):
$$h_{\mathbf{w}}(\mathbf{x}) = P(Y = 1 \mid \mathbf{x}; \mathbf{w}) = \sigma(\mathbf{w}^T \mathbf{x}) = \frac{1}{1 + e^{-\mathbf{w}^T \mathbf{x}}}$$

By the axiom of probability, the probability of the negative class ($Y=0$) is the complement:
$$P(Y = 0 \mid \mathbf{x}; \mathbf{w}) = 1 - P(Y = 1 \mid \mathbf{x}; \mathbf{w}) = 1 - \sigma(\mathbf{w}^T \mathbf{x}) = \frac{e^{-\mathbf{w}^T \mathbf{x}}}{1 + e^{-\mathbf{w}^T \mathbf{x}}}$$

## The Decision Boundary: Equating to the Hyperplane
To output a discrete classification label $\hat{y}$, we establish a decision threshold (typically $0.5$):

$$\hat{y} = \begin{cases} 1 & \text{if } P(Y=1 \mid \mathbf{x}) \ge 0.5 \\ 0 & \text{if } P(Y=1 \mid \mathbf{x}) < 0.5 \end{cases}$$

When does the model predict exactly $0.5$?
$$P(Y=1 \mid \mathbf{x}) = 0.5 \implies \frac{1}{1 + e^{-\mathbf{w}^T \mathbf{x}}} = 0.5$$
$$1 + e^{-\mathbf{w}^T \mathbf{x}} = 2 \implies e^{-\mathbf{w}^T \mathbf{x}} = 1 \implies -\mathbf{w}^T \mathbf{x} = \ln(1) = 0$$
$$\mathbf{w}^T \mathbf{x} = 0$$

> **The Linear Decision Boundary:**
> The decision boundary of Logistic Regression is the $(d-1)$-dimensional linear hyperplane defined by the equation $\mathbf{w}^T \mathbf{x} = 0$.

If $\mathbf{w}^T \mathbf{x} > 0$, the model predicts Class 1.  
If $\mathbf{w}^T \mathbf{x} < 0$, the model predicts Class 0.

Unlike Decision Trees (which construct orthogonal, staircase-like boundaries), Logistic Regression constructs a single, optimal linear hyperplane capable of cutting diagonally across the feature space.

---

# 3. The Odds Ratio and Logit Transformation

## Deriving the Odds Ratio
While probability measures the likelihood of an event occurring (e.g., $P = 0.80$), the **Odds Ratio** compares the probability of an event occurring against the probability of it not occurring.

$$\text{Odds} = \frac{P(Y = 1 \mid \mathbf{x})}{P(Y = 0 \mid \mathbf{x})} = \frac{P(Y = 1 \mid \mathbf{x})}{1 - P(Y = 1 \mid \mathbf{x})}$$

Substituting the logistic hypothesis $p = \frac{1}{1 + e^{-z}}$:
$$\text{Odds} = \frac{\frac{1}{1 + e^{-z}}}{\frac{e^{-z}}{1 + e^{-z}}} = \frac{1}{e^{-z}} = e^z$$

$$\text{Odds} = \exp(\mathbf{w}^T \mathbf{x})$$

## The Log-Odds (Logit) Function
Taking the natural logarithm of the odds ratio yields the **Logit** function:

$$\text{Logit}(P) = \ln\left(\frac{P(Y = 1 \mid \mathbf{x})}{1 - P(Y = 1 \mid \mathbf{x})}\right) = \mathbf{w}^T \mathbf{x}$$

This derivation reveals a profound statistical truth: **Logistic Regression is simply a linear regression model operating in the log-odds space.** It maps non-linear probabilities into a linear space where weights can be additively combined.

## Interpretability of the Weights (Coefficients)
Because $\ln(\text{Odds}) = w_1x_1 + w_2x_2 + \dots + w_dx_d + b$:
- A **positive weight** ($w_j > 0$) means that as feature $x_j$ increases, the log-odds of the positive class increase (moving the instance toward Class 1).
- A **negative weight** ($w_j < 0$) means that as feature $x_j$ increases, the log-odds of the positive class decrease (moving the instance toward Class 0).
- An increase of $1$ unit in feature $x_j$ changes the log-odds by exactly $w_j$, which corresponds to multiplying the overall Odds Ratio by a factor of $e^{w_j}$.

---

# 4. Parameter Estimation via Maximum Likelihood

## Formulating the Bernoulli Likelihood Function
Given a dataset $S = \{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^N$ where $y^{(i)} \in \{0, 1\}$, how do we find the optimal weight vector $\mathbf{w}$? 

We assume that the dataset labels are drawn from a Bernoulli distribution parameterized by $p_i = h_{\mathbf{w}}(\mathbf{x}^{(i)})$.
The probability of observing the correct label $y^{(i)}$ for a single instance is:
$$P(y^{(i)} \mid \mathbf{x}^{(i)}; \mathbf{w}) = (h_{\mathbf{w}}(\mathbf{x}^{(i)}))^{y^{(i)}} \cdot (1 - h_{\mathbf{w}}(\mathbf{x}^{(i)}))^{1 - y^{(i)}}$$

Assuming all $N$ instances are independently and identically distributed (i.i.d.), the joint **Likelihood Function** of the entire dataset is the product of the individual probabilities:
$$L(\mathbf{w}) = \prod_{i=1}^N P(y^{(i)} \mid \mathbf{x}^{(i)}; \mathbf{w}) = \prod_{i=1}^N (h_{\mathbf{w}}(\mathbf{x}^{(i)}))^{y^{(i)}} \cdot (1 - h_{\mathbf{w}}(\mathbf{x}^{(i)}))^{1 - y^{(i)}}$$

## Deriving the Binary Cross-Entropy (Log Loss) Cost Function
To maximize the likelihood $L(\mathbf{w})$, we maximize its natural logarithm (the Log-Likelihood, $\ell(\mathbf{w})$) to prevent underflow and simplify the products into summations:

$$\ell(\mathbf{w}) = \ln L(\mathbf{w}) = \sum_{i=1}^N \left[ y^{(i)} \ln(h_{\mathbf{w}}(\mathbf{x}^{(i)})) + (1 - y^{(i)}) \ln(1 - h_{\mathbf{w}}(\mathbf{x}^{(i)})) \right]$$

In machine learning, convention dictates that we **minimize a cost function** $J(\mathbf{w})$ rather than maximize a likelihood. Thus, we define the cost function as the **Negative Log-Likelihood** (divided by $N$ to get the average error per instance):

> **The Binary Cross-Entropy (Log Loss) Cost Function:**
> $$J(\mathbf{w}) = -\frac{1}{N} \sum_{i=1}^N \left[ y^{(i)} \ln(h_{\mathbf{w}}(\mathbf{x}^{(i)})) + (1 - y^{(i)}) \ln(1 - h_{\mathbf{w}}(\mathbf{x}^{(i)})) \right]$$

**Analysis of the Cost Function:**
- **If $y = 1$:** The second term disappears. $J(\mathbf{w}) = -\ln(h_{\mathbf{w}}(\mathbf{x}))$. As the predicted probability $h \to 1$ (correct), the cost drops to $0$. As $h \to 0$ (incorrect), the cost approaches $+\infty$.
- **If $y = 0$:** The first term disappears. $J(\mathbf{w}) = -\ln(1 - h_{\mathbf{w}}(\mathbf{x}))$. As the predicted probability $h \to 0$ (correct), the cost drops to $0$. As $h \to 1$ (incorrect), the cost approaches $+\infty$.

## Convexity and Global Optimization
Unlike the cost functions of deep neural networks, the Binary Cross-Entropy cost function for Logistic Regression is **strictly convex**. This means it resembles a single, smooth, bowl-like surface. 
- It has exactly one global minimum.
- It has no local minima or saddle points.
- Gradient descent is guaranteed to converge to the optimal parameter vector $\mathbf{w}^*$ (provided the learning rate is chosen correctly).

---

# 5. Optimization Mechanics: Gradient Descent Formulation

## Derivation of the Gradient Vector
To minimize $J(\mathbf{w})$, we must find the derivative of the cost function with respect to the weight vector $\mathbf{w}$.

By applying the chain rule, the partial derivative of the cost function with respect to a single weight component $w_j$ is:
$$\frac{\partial J}{\partial w_j} = \frac{1}{N} \sum_{i=1}^N (h_{\mathbf{w}}(\mathbf{x}^{(i)}) - y^{(i)}) x_j^{(i)}$$

*Remarkable Observation:* The gradient of Logistic Regression (Binary Cross-Entropy Loss) is mathematically identical to the gradient of Linear Regression (Mean Squared Error Loss). The only difference is the definition of the hypothesis function $h_{\mathbf{w}}(\mathbf{x})$.

Expressed as a vectorized matrix operation over the entire dataset:
$$\nabla_{\mathbf{w}} J(\mathbf{w}) = \frac{1}{N} \mathbf{X}^T (\mathbf{h} - \mathbf{y})$$
where:
- $\mathbf{X}$ is the $(N \times d)$ design matrix of features.
- $\mathbf{h}$ is the $(N \times 1)$ vector of sigmoid predictions.
- $\mathbf{y}$ is the $(N \times 1)$ vector of true target labels.

## The Gradient Descent Update Rule
Because there is no closed-form analytical solution to set $\nabla_{\mathbf{w}} J(\mathbf{w}) = 0$ (due to the non-linear sigmoid), we must use iterative numerical optimization.

Starting with random or zero initialization ($\mathbf{w}_0 = \mathbf{0}$), the weights are iteratively updated in the direction opposite to the gradient:

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla_{\mathbf{w}} J(\mathbf{w}_t)$$
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \left[ \frac{1}{N} \sum_{i=1}^N (h_{\mathbf{w}}(\mathbf{x}^{(i)}) - y^{(i)}) \mathbf{x}^{(i)} \right]$$

where $\alpha$ is the scalar **learning rate** controlling the step size.

## Batch vs. Stochastic Gradient Descent
1. **Batch Gradient Descent (BGD):** Computes the gradient using the entire dataset of $N$ instances before executing a single update. Extremely stable but computationally slow for large datasets.
2. **Stochastic Gradient Descent (SGD):** Computes the gradient and updates the weights using only **a single randomly selected instance** ($N=1$) per step. Highly efficient and stochastic, bouncing around the loss surface but converging much faster.
3. **Mini-Batch Gradient Descent:** The modern compromise, computing the gradient on small subsets (e.g., $N=32$ or $64$ instances) utilizing vectorized hardware architectures (GPUs).

---

# 6. Extension to Multiclass: Multinomial Logistic Regression

Binary Logistic Regression models two classes ($K=2$). When $K > 2$ (e.g., classifying an image into 10 digit classes), the binary sigmoid must be generalized.

## The Softmax Activation Function
Instead of estimating a single scalar probability, Multinomial Logistic Regression assigns an independent weight vector $\mathbf{w}_k$ to every class $c_k$.

The raw linear score (logit) for class $k$ is $z_k = \mathbf{w}_k^T \mathbf{x}$.

To convert the vector of $K$ logits $\mathbf{z} = [z_1, z_2, \dots, z_K]$ into a valid probability distribution that sums to exactly $1.0$, we apply the **Softmax Function**:

$$P(Y = c_k \mid \mathbf{x}) = \frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}} = \frac{e^{\mathbf{w}_k^T \mathbf{x}}}{\sum_{j=1}^K e^{\mathbf{w}_j^T \mathbf{x}}}$$

- Exponentiating $e^{z_k}$ ensures every value is strictly positive.
- Dividing by the sum $\sum e^{z_j}$ ensures the outputs sum to $1.0$.

## One-vs-Rest (OvR) vs. Cross-Entropy Optimization
When training a multi-class model, two approaches exist:
1. **One-vs-Rest (OvR) or One-vs-All:** Train $K$ independent binary logistic regression classifiers, where classifier $k$ predicts "Class $k$" versus "All other classes." At inference, select the class whose classifier outputs the highest confidence.
2. **Multinomial Cross-Entropy Optimization:** Train all $K$ weight vectors simultaneously using the generalized Categorical Cross-Entropy loss function (the standard architecture for modern deep learning neural networks).

---

# 7. Comprehensive Step-by-Step Numerical Walkthroughs

## Worked Problem 1: Manual Calculation of the Logistic Forward Pass

### Problem Statement
A university admissions model predicts the probability of student admission ($Y \in \{0, 1\}$) based on three standardized test scores: Math ($x_1$), Physics ($x_2$), and Chemistry ($x_3$).

After training, the optimized weight vector $\mathbf{w}$ and bias $b$ are:
- $w_1 = 0.50$
- $w_2 = 0.20$
- $w_3 = 0.30$
- $b = -60.0$

A student applies with scores: $x_1 = 80$, $x_2 = 70$, $x_3 = 90$.
1. Compute the linear decision score $z$.
2. Compute the predicted probability of admission $P(Y=1 \mid \mathbf{x})$ using the sigmoid function.
3. Will the student be admitted if the decision threshold is $0.5$?
*(Assume $e^x \approx 2.718^x$)*

---

### Step-by-Step Solution

#### Step 1: Compute the Linear Logit Score ($z$)
$$z = \mathbf{w}^T \mathbf{x} + b = w_1x_1 + w_2x_2 + w_3x_3 + b$$
$$z = (0.50 \times 80) + (0.20 \times 70) + (0.30 \times 90) - 60.0$$
$$z = 40.0 + 14.0 + 27.0 - 60.0$$
$$z = 81.0 - 60.0 = \mathbf{21.0}$$

#### Step 2: Apply the Sigmoid Activation
$$P(Y=1 \mid \mathbf{x}) = \sigma(z) = \frac{1}{1 + e^{-z}}$$
$$P(Y=1 \mid \mathbf{x}) = \frac{1}{1 + e^{-21.0}}$$

Evaluate the exponential:
$e^{-21.0} \approx 7.58 \times 10^{-10}$ (an extremely small positive number).
$$P(Y=1 \mid \mathbf{x}) = \frac{1}{1 + 0.000000000758} = \frac{1}{1.000000000758} \approx \mathbf{0.999999999}$$

#### Step 3: Classification Decision
$$P(Y=1 \mid \mathbf{x}) = 0.9999 \ge 0.5$$
The model predicts $\hat{y} = 1$. The student **will be admitted** with extremely high confidence.

---

## Worked Problem 2: Interpretation of Odds Ratios in Medical Data

### Problem Statement
A clinical Logistic Regression model predicts the risk of cardiovascular disease based on two scaled features:
- $x_1$: Blood Pressure (Scaled)
- $x_2$: Age (Scaled)

The fitted weights are: $w_{\text{bp}} = 1.2$, $w_{\text{age}} = 0.8$, $b = -2.5$.
1. If a patient's scaled blood pressure increases by $1.0$ unit (while age remains constant), by what multiplicative factor does their **Odds Ratio** of developing cardiovascular disease change?
2. If patient A has an odds ratio of $0.5$, calculate their precise probability of cardiovascular disease $P(Y=1)$.

---

### Step-by-Step Solution

#### Step 1: Calculate the Multiplicative Change in Odds
The Log-Odds equation is:
$$\ln(\text{Odds}) = w_1x_1 + w_2x_2 + b$$
$$\text{Odds} = \exp(w_1x_1 + w_2x_2 + b)$$

Let the initial state be $\mathbf{x}_{\text{old}}$ and the new state be $\mathbf{x}_{\text{new}}$, where $x_1$ increases by $1$:
$$\text{Odds}_{\text{new}} = \exp(w_1(x_1 + 1) + w_2x_2 + b) = \exp(w_1x_1 + w_1 + w_2x_2 + b)$$
Using exponentiation properties:
$$\text{Odds}_{\text{new}} = \exp(w_1) \times \exp(w_1x_1 + w_2x_2 + b) = \exp(w_1) \times \text{Odds}_{\text{old}}$$

The odds ratio is multiplied by a factor of $e^{w_1}$:
$$\text{Factor} = e^{1.2} \approx \mathbf{3.32}$$
An increase of 1 unit in scaled blood pressure multiplies the patient's odds of disease by $3.32\times$.

#### Step 2: Convert Odds Back to Probability
$$\text{Odds} = \frac{P}{1 - P}$$
$$0.5 = \frac{P}{1 - P}$$
$$0.5(1 - P) = P \implies 0.5 - 0.5P = P$$
$$0.5 = 1.5P \implies P = \frac{0.5}{1.5} = \frac{1}{3}$$
$$P(Y=1) \approx \mathbf{0.3333} \quad (33.33\%)$$

---

## Worked Problem 3: Execution of a Single Gradient Descent Update Step

### Problem Statement
You are training a Logistic Regression model via Stochastic Gradient Descent. The model currently has the following parameters:
- $\mathbf{w}_t = [0.1, -0.2]^T$ (Assume bias $b$ is integrated into $\mathbf{w}$ using $x_0 = 1$)

You evaluate a single training instance:
- Feature vector: $\mathbf{x}^{(1)} = [1.0, 2.0]^T$
- True label: $y^{(1)} = 1$

The learning rate is $\alpha = 0.5$.
Execute one iteration of Stochastic Gradient Descent to calculate the updated weight vector $\mathbf{w}_{t+1}$.

---

### Step-by-Step Solution

#### Step 1: Forward Pass (Compute Prediction)
Compute the logit score $z$:
$$z = \mathbf{w}_t^T \mathbf{x}^{(1)} = (0.1 \times 1.0) + (-0.2 \times 2.0) = 0.1 - 0.4 = -0.3$$

Apply the sigmoid function:
$$h_{\mathbf{w}}(\mathbf{x}^{(1)}) = \frac{1}{1 + e^{-(-0.3)}} = \frac{1}{1 + e^{0.3}}$$
Using $e^{0.3} \approx 1.34986$:
$$h = \frac{1}{1 + 1.34986} = \frac{1}{2.34986} \approx \mathbf{0.4255}$$

The model predicts $0.4255$, but the true label is $y = 1$. The error is:
$$\text{Error} = (h - y) = 0.4255 - 1.0 = \mathbf{-0.5745}$$

#### Step 2: Compute the Gradient Vector
The gradient for a single instance ($N=1$) is:
$$\nabla_{\mathbf{w}} J = (h - y) \mathbf{x}^{(1)}$$
$$\nabla_{\mathbf{w}} J = -0.5745 \times [1.0, 2.0]^T = \mathbf{[-0.5745, -1.1490]^T}$$

#### Step 3: Apply the Gradient Descent Update Rule
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla_{\mathbf{w}} J$$
$$\mathbf{w}_{t+1} = \begin{bmatrix} 0.1 \\ -0.2 \end{bmatrix} - 0.5 \begin{bmatrix} -0.5745 \\ -1.1490 \end{bmatrix}$$
$$\mathbf{w}_{t+1} = \begin{bmatrix} 0.1 \\ -0.2 \end{bmatrix} - \begin{bmatrix} -0.28725 \\ -0.5745 \end{bmatrix} = \begin{bmatrix} 0.1 + 0.28725 \\ -0.2 + 0.5745 \end{bmatrix} = \mathbf{\begin{bmatrix} 0.38725 \\ 0.3745 \end{bmatrix}}$$

The weights have moved in a direction that will increase the linear score $z$ on the next pass, driving the prediction closer to $1.0$.

---

## Worked Problem 4: Defining the Equation of the Linear Decision Boundary

### Problem Statement
A Logistic Regression classifier is trained on 2D geometric data $(x_1, x_2)$. The optimized parameters are:
- $w_1 = 2.0$
- $w_2 = -4.0$
- Bias $b = 10.0$

1. Derive the standard geometric equation of the line representing the model's decision boundary.
2. Determine the slope and the $x_2$-intercept of this boundary line.
3. If an input point is $\mathbf{x} = [2.0, 4.0]^T$, will it be classified as Class 1 or Class 0?

---

### Step-by-Step Solution

#### Step 1: Set Up the Decision Boundary Equation
The decision boundary occurs precisely where the predicted probability is $0.5$, which corresponds to the linear logit score equaling zero:
$$z = w_1x_1 + w_2x_2 + b = 0$$
Substitute the parameters:
$$2.0x_1 - 4.0x_2 + 10.0 = 0$$

#### Step 2: Convert to Slope-Intercept Form ($x_2 = mx_1 + c$)
Isolate $x_2$:
$$-4.0x_2 = -2.0x_1 - 10.0$$
$$x_2 = \frac{-2.0}{-4.0}x_1 + \frac{-10.0}{-4.0}$$
$$x_2 = 0.5x_1 + 2.5$$

- **Slope ($m$):** $0.5$
- **Intercept ($c$):** $2.5$

#### Step 3: Classify the Input Point $\mathbf{x} = [2.0, 4.0]^T$
Evaluate the logit function $z$:
$$z = 2.0(2.0) - 4.0(4.0) + 10.0$$
$$z = 4.0 - 16.0 + 10.0 = \mathbf{-2.0}$$

Because $z < 0$, the point lies on the negative side of the decision boundary.
The model will output a probability $\sigma(-2.0) \approx 0.119 < 0.5$, resulting in a prediction of **Class 0**.

---

# 8. KTU University Examination Practice Questions

## Short-Answer Analytical Problems (Part A)

### Question 1: Activation Function Mechanics
> **Question:** Define the Sigmoid (Logistic) activation function and state its mathematical domain and range. Why is this specific function chosen for binary classification over a simple linear step function? *(3 Marks)*

**Model Answer:** The Sigmoid function is defined as $\sigma(z) = \frac{1}{1 + e^{-z}}$. Its domain is the set of all real numbers $(-\infty, +\infty)$, and its range is the open interval $(0, 1)$.
It is preferred over a hard step function because:
1. **Differentiability:** It is continuous and smoothly differentiable everywhere ($\sigma'(z) = \sigma(z)(1 - \sigma(z))$), allowing for gradient-based numerical optimization (Gradient Descent). A hard step function has a derivative of zero everywhere (except at the origin where it is undefined), stalling optimization.
2. **Probabilistic Semantics:** It outputs a continuous probability score reflecting the model's confidence, rather than just a hard categorical label.

---

### Question 2: Generative vs. Discriminative Models
> **Question:** Explain the structural difference between a Generative classifier (like Naive Bayes) and a Discriminative classifier (like Logistic Regression). Which paradigm generally requires fewer assumptions? *(3 Marks)*

**Model Answer:** 
- **Generative Models** attempt to model the joint distribution $P(\mathbf{X}, Y)$ by explicitly modeling the class-conditional data distributions $P(\mathbf{X} \mid Y)$. They require strong structural assumptions about the data (e.g., conditional independence in Naive Bayes, or Gaussian shapes) to be computationally tractable.
- **Discriminative Models** bypass the joint distribution entirely. They define an explicit decision boundary by modeling the posterior mapping $P(Y \mid \mathbf{X})$ directly. They require fewer assumptions about the distribution of the features themselves, focusing only on distinguishing between classes, often leading to better predictive accuracy on complex, overlapping datasets.

---

### Question 3: Why MSE Fails for Classification
> **Question:** Why is the Mean Squared Error (MSE) cost function mathematically inappropriate for optimizing Logistic Regression? *(3 Marks)*

**Model Answer:** Applying MSE to the non-linear sigmoid hypothesis creates a **non-convex cost function**. The resulting error surface contains multiple local minima and saddle points, meaning Gradient Descent is likely to get stuck and fail to find the global optimum. Furthermore, MSE penalizes large confident errors linearly (or quadratically in score space), while the Binary Cross-Entropy (Log Loss) cost function heavily penalizes highly confident wrong predictions logarithmically (driving cost to infinity), ensuring stronger gradients when the model makes a severe mistake.

---

## Comprehensive Essay & Derivation Questions (Part B)

### Question 4: Maximum Likelihood and Cost Function Derivation
> **Question:** > (a) Starting from the Bernoulli distribution, derive the Binary Cross-Entropy (Log Loss) cost function used in Logistic Regression. *(8 Marks)* > (b) State the Gradient Descent update rule for this cost function, and define the terms vector $\mathbf{w}$, learning rate $\alpha$, and gradient $\nabla J$. *(4 Marks)*

**Model Answer Outline:**
- **Part (a):**
  1. Define the Bernoulli likelihood for a single instance: $P(y^{(i)} \mid \mathbf{x}^{(i)}) = h^{y^{(i)}} (1-h)^{1-y^{(i)}}$.
  2. Define the joint likelihood $L(\mathbf{w})$ over the full i.i.d. dataset as the product of all $N$ instances.
  3. Apply the natural logarithm to formulate the Log-Likelihood $\ell(\mathbf{w})$, converting the product into a sum.
  4. Multiply by $-1/N$ to frame the optimization as a minimization problem, yielding the final Negative Log-Likelihood / Binary Cross-Entropy formula.
- **Part (b):**
  - Write the gradient descent update equation: $\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla_{\mathbf{w}} J(\mathbf{w}_t)$.
  - Define $\mathbf{w}$ as the parameter weight vector (including bias).
  - Define $\alpha$ as the learning rate, the scalar step size governing how aggressively the weights update per iteration.
  - State the analytical gradient vector formula: $\nabla_{\mathbf{w}} J = \frac{1}{N} \sum_{i=1}^N (h_{\mathbf{w}}(\mathbf{x}^{(i)}) - y^{(i)}) \mathbf{x}^{(i)}$.

---

### Question 5: Multiclass Extension and Network Architecture
> **Question:** > A machine learning system must classify images of handwritten digits into 10 distinct classes ($0-9$). 
> (a) Explain how Multinomial Logistic Regression (Softmax Regression) extends standard binary Logistic Regression for this task. Include the Softmax equation. *(5 Marks)* > (b) Explain how the One-vs-Rest (OvR) approach solves the same multiclass problem using binary classifiers. How many models must be trained? *(4 Marks)* > (c) What is the fundamental geometry of the decision boundaries constructed by Logistic Regression in a 3-dimensional feature space? *(3 Marks)*

**Model Answer Outline:**
- **Part (a):** Multinomial Logistic Regression replaces the single sigmoid activation with the Softmax function. Instead of one weight vector, it learns a weight matrix $W$ containing 10 independent weight vectors (one for each class). The Softmax normalizes the 10 raw logit scores into a valid probability distribution: $P(Y=k \mid \mathbf{x}) = \frac{e^{\mathbf{w}_k^T \mathbf{x}}}{\sum_{j=1}^{10} e^{\mathbf{w}_j^T \mathbf{x}}}$.
- **Part (b):** In One-vs-Rest (OvR), the algorithm breaks the 10-class problem into 10 separate binary classification problems. It trains 10 independent standard Logistic Regression models (e.g., "Is the image a 0, or is it NOT a 0?"). At test time, all 10 models evaluate the image, and the class associated with the model outputting the highest confidence score is selected.
- **Part (c):** In a 3-dimensional feature space, the decision boundary $\mathbf{w}^T \mathbf{x} = 0$ is a **2-dimensional flat plane** (hyperplane).
