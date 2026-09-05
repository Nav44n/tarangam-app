# KTU Official Syllabus: Machine Learning (PCCST503)

Welcome to the comprehensive academic and examination blueprint for **Machine Learning (PCCST503)**, prescribed under the **APJ Abdul Kalam Technological University (KTU) 2024 Scheme for Semester 5 (S5) Computer Science and allied engineering branches**.

---

## 📋 Course Overview

<div class="table-wrap">

| Parameter | Specification Details |
| :--- | :--- |
| **Course Name** | **Machine Learning** |
| **Course Code** | `PCCST503` |
| **Semester** | **Semester 5 (S5)** |
| **Degree & Branch** | **B.Tech (Common to CS / AD / CR / CA / CC / CD)** |
| **Teaching Hours / Week** | **3:0:0:0** *(Lecture: 3 hrs, Tutorial: 0, Practical: 0, Remedial: 0)* |
| **Total Contact Hours** | **36 Contact Hours (9 Hours / Module)** |
| **Course Credits** | **3 Credits** |
| **Course Type** | **Theory** |
| **Prerequisites** | **None** |
| **Continuous Internal Evaluation (CIE)** | **40 Marks** *(Min. 45% / 18 marks required for ESE eligibility)* |
| **End Semester Examination (ESE)** | **60 Marks** *(Min. 40% / 24 marks required to pass)* |
| **Total Marks** | **100 Marks** |
| **Examination Duration** | **2 Hours 30 Minutes (150 Minutes)** |

</div>

::: callout-intuition Why Machine Learning is the Paradigm Shift of Modern Computing
In traditional programming, human software engineers write explicit rules (code) that take data and produce answers ($Data + Rules \rightarrow Answers$). In Machine Learning, statistical optimization models ingest data and known answers to induce the underlying mathematical rules ($Data + Answers \rightarrow Rules$). From probability-driven parameter estimation (MLE/MAP) to high-dimensional hyperplanes (SVM) and deep gradient backpropagation, this course provides the rigorous mathematical foundations of AI.
:::

---

## 🎯 Course Objectives

The primary pedagogical objectives of the course are:

1. **Fundamental Principles**: To impart the fundamental mathematical principles, loss functions, and statistical formulations of machine learning in computer science.
2. **Supervised & Unsupervised Learning**: To provide a comprehensive understanding of the concepts, optimization mechanics, and algorithms of both supervised learning (regression, classification, neural networks, SVM) and unsupervised learning (clustering, dimensionality reduction, ensemble methods).

---

## 📚 Module-by-Module Syllabus Breakdown

### Module 1: Introduction to ML, Parameter Estimation & Regression (9 Contact Hours)

::: callout-exam Module 1 High-Yield Focus
Module 1 carries **15 compulsory/choice marks in ESE** (Two 3-mark questions in Part A + One 9-mark question with choice in Part B). High-yield exam derivations: MLE vs MAP formulation for Gaussian distributions, Batch Gradient Descent parameter update rule derivations ($\theta_j := \theta_j - \alpha \frac{\partial J}{\partial \theta_j}$), and Ordinary Least Squares (OLS) Normal Equation derivation ($\theta = (X^T X)^{-1} X^T y$).
:::

* **Introduction to Machine Learning**:
  * Machine Learning vs. Traditional Programming; Arthur Samuel and Tom Mitchell operational definitions ($E, T, P$).
  * Machine Learning Paradigms: Supervised learning, Semi-supervised learning, Unsupervised learning, and Reinforcement learning.
* **Statistical Parameter Estimation & Bayesian Formulation**:
  * Prior probability, Likelihood, Posterior probability, and Evidence (Bayes' Theorem: $P(\theta|D) = \frac{P(D|\theta)P(\theta)}{P(D)}$).
  * **Maximum Likelihood Estimation (MLE)**:
    * Likelihood function $L(\theta; D)$ and Log-Likelihood $\ell(\theta) = \ln L(\theta; D)$.
    * Derivation of MLE for Bernoulli trials and univariate Gaussian distribution ($\mu_{\text{MLE}}, \sigma^2_{\text{MLE}}$).
  * **Maximum A Posteriori (MAP) Estimation**:
    * Incorporating prior distribution $P(\theta)$ into estimation: $\hat{\theta}_{\text{MAP}} = \arg\max_\theta [ \ln P(D|\theta) + \ln P(\theta) ]$.
    * Connection between MAP with Gaussian prior and L2 Regularization (Ridge), and Laplace prior with L1 Regularization (Lasso).
* **Supervised Learning Foundations & Problem Formulation**:
  * Feature representation, feature vectors, design matrix $X$, target vector $y$.
  * Role of Loss functions: Squared Error Loss, Absolute Loss, Zero-One Loss, Cross-Entropy Loss.
  * Empirical Risk Minimization (ERM) and Convex Optimization.
* **Regression Modeling**:
  * **Linear Regression with One Variable (Simple Linear Regression)**:
    * Hypothesis $h_\theta(x) = \theta_0 + \theta_1 x$, Mean Squared Error (MSE) cost function $J(\theta_0, \theta_1)$.
  * **Linear Regression with Multiple Variables (Multivariate Regression)**:
    * Vectorized hypothesis $h_\theta(x) = \theta^T x$, cost function $J(\theta) = \frac{1}{2m} (X\theta - y)^T (X\theta - y)$.
    * **Gradient Descent Algorithm**: Learning rate $\alpha$, convergence analysis, Batch vs Stochastic vs Mini-batch Gradient Descent, partial derivative derivations.
    * **Matrix Method (Normal Equation / Closed-form Solution)**: Step-by-step matrix calculus derivation of $\theta = (X^T X)^{-1} X^T y$; computational complexity $O(n^3)$ vs Gradient Descent.

---

### Module 2: Classification, Overfitting, Regularization & Model Evaluation (9 Contact Hours)

::: callout-exam Module 2 High-Yield Focus
Module 2 covers fundamental classifiers and statistical model validation. High-yield KTU exam topics: Information Gain & Entropy calculations for ID3 Decision Tree construction, Naïve Bayes text/tabular probability computations with Laplace smoothing, Logistic Regression sigmoid function and cross-entropy loss derivation, L1 (Lasso) vs L2 (Ridge) geometric sparsity comparison, and Confusion Matrix metrics (Precision, Recall, F1, ROC/AUC).
:::

* **Supervised Classification Algorithms**:
  * **Logistic Regression**:
    * Why Linear Regression fails for classification; Odds and Log-Odds (Logit function).
    * Sigmoid / Logistic activation function $g(z) = \frac{1}{1 + e^{-z}}$; Decision boundary.
    * Binary Cross-Entropy / Log-Loss cost function and gradient descent update rule.
  * **Naïve Bayes Classifier**:
    * Bayes' Rule for classification; The Conditional Independence Assumption $P(x_1, \dots, x_n | y) = \prod_{i=1}^n P(x_i | y)$.
    * Maximum A Posteriori decision rule; Handling zero-frequency problem using **Laplace Smoothing (Additive Smoothing)**.
    * Gaussian Naïve Bayes for continuous features.
  * **$K$-Nearest Neighbors (KNN)**:
    * Instance-based lazy learning; Distance metrics (Euclidean, Manhattan, Minkowski).
    * Effect of choice of $K$ on bias and variance; Voronoi tessellation diagrams.
  * **Decision Trees (ID3 Algorithm)**:
    * Tree structure (Root, Internal nodes, Leaves, Branches).
    * Splitting criteria: **Shannon Entropy** $H(S) = -\sum p_i \log_2 p_i$ and **Information Gain** $IG(S, A) = H(S) - \sum \frac{|S_v|}{|S|} H(S_v)$.
    * Step-by-step trace of Quinlan's ID3 algorithm; Overfitting in decision trees and tree pruning.
* **Generalization, Overfitting & Regularization**:
  * The phenomenon of Overfitting vs Underfitting.
  * Training set, Validation set, and Test set partitioning; $K$-fold Cross-Validation.
  * **Regularization Framework**:
    * **Ridge Regularization (L2 Norm)**: $J_{\text{Ridge}}(\theta) = J(\theta) + \lambda \sum \theta_j^2$; Shrinkage behavior, analytical solution $\theta = (X^T X + \lambda I)^{-1} X^T y$.
    * **LASSO Regularization (L1 Norm)**: $J_{\text{LASSO}}(\theta) = J(\theta) + \lambda \sum |\theta_j|$; Geometric interpretation of diamond L1 constraint vs circular L2 constraint, feature selection via weight sparsity.
* **Model Performance Evaluation Measures**:
  * **Classification Performance Metrics**:
    * Confusion Matrix: True Positives (TP), False Positives (FP), True Negatives (TN), False Negatives (FN).
    * Accuracy, Error Rate, Precision (Positive Predictive Value), Recall (Sensitivity / True Positive Rate), Specificity (True Negative Rate).
    * $F$-Measure / $F_1$-Score (Harmonic mean of Precision and Recall) and general $F_\beta$-score.
    * Receiver Operating Characteristic (ROC) curve: False Positive Rate ($1 - \text{Specificity}$) vs True Positive Rate.
    * Area Under the Curve (AUC-ROC) interpretation and baseline random guessing ($0.5$).
  * **Regression Performance Metrics**:
    * Mean Absolute Error (MAE): $\frac{1}{m} \sum |y_i - \hat{y}_i|$.
    * Mean Squared Error (MSE) and Root Mean Squared Error (RMSE): $\sqrt{\frac{1}{m} \sum (y_i - \hat{y}_i)^2}$.
    * Coefficient of Determination ($R^2$ Score): $R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}$, interpretation of negative, zero, and unitary values.

---

### Module 3: Support Vector Machines & Neural Networks (9 Contact Hours)

::: callout-exam Module 3 High-Yield Focus
Module 3 is the core optimization and deep learning foundations module. High-probability exam derivations and traces: Formulation of Maximum Margin Hyperplane for Linear SVM, Primal and Dual formulations, soft-margin slack variables ($\xi_i$) and $C$ parameter, Kernel Trick (Polynomial, RBF/Gaussian), Single-Layer Perceptron convergence theorem, and Backpropagation chain-rule error gradient derivations for Multi-Layer Perceptrons.
:::

* **Support Vector Machines (SVM)**:
  * Linear SVM for linearly separable data; Definition of Hyperplane: $w^T x + b = 0$.
  * Geometric margin vs Functional margin; Distance of point to hyperplane $\frac{|w^T x_i + b|}{\|w\|}$.
  * **Maximum Margin Hyperplane Formulation**:
    * Constrained optimization: $\min_{w, b} \frac{1}{2} \|w\|^2 \text{ subject to } y_i (w^T x_i + b) \ge 1, \, \forall i$.
    * Concept of **Support Vectors** (critical data points lying on canonical hyperplanes $w^T x + b = \pm 1$).
  * Soft-Margin SVM for non-linearly separable data: Slack variables $\xi_i \ge 0$, penalty parameter $C$, trade-off between margin size and slack penalties.
  * **Non-Linear SVM & The Kernel Trick**:
    * Mapping input space to higher-dimensional feature space $\Phi(x)$.
    * Mercer's Theorem and Kernel functions: $K(x_i, x_j) = \langle \Phi(x_i), \Phi(x_j) \rangle$.
    * Popular Kernels: Linear kernel, Polynomial kernel $K(x, z) = (x^T z + c)^d$, Radial Basis Function (RBF / Gaussian) kernel $K(x, z) = \exp(-\gamma \|x - z\|^2)$, Sigmoid kernel.
* **Artificial Neural Networks (ANN)**:
  * Biological neuron inspiration vs Artificial neuron model (McCulloch-Pitts neuron, Rosenblatt Perceptron).
  * **The Perceptron**:
    * Mathematical model: $y = f(w^T x + b)$; Perceptron learning algorithm and convergence theorem.
    * Linear separability limitation: The XOR problem and Minsky-Papert critique.
  * **Multilayer Feedforward Neural Networks (MLP)**:
    * Architecture: Input layer, hidden layers, output layer, weight matrices, bias vectors.
    * Universal Approximation Theorem.
  * **Activation Functions**:
    * Sigmoid function $\sigma(z) = \frac{1}{1 + e^{-z}}$, derivative $\sigma'(z) = \sigma(z)(1 - \sigma(z))$, vanishing gradient problem.
    * Hyperbolic Tangent ($\tanh(z)$), zero-centered output, derivative $1 - \tanh^2(z)$.
    * Rectified Linear Unit (ReLU) $f(z) = \max(0, z)$, sparsity, dying ReLU problem, Leaky ReLU overview.
  * **Backpropagation Algorithm**:
    * Forward pass: Computing layer-by-layer net inputs $z^{[l]}$ and activations $a^{[l]}$.
    * Backward pass: Applying the Calculus Chain Rule to compute error deltas $\delta^{[l]}$ and weight gradients $\frac{\partial J}{\partial W^{[l]}}$.
    * Weight updates using gradient descent: $W := W - \alpha \nabla_W J$.

---

### Module 4: Unsupervised Learning, Dimensionality Reduction & Ensembles (9 Contact Hours)

::: callout-exam Module 4 High-Yield Focus
Module 4 explores pattern discovery, dimensionality reduction, and meta-learning. Frequent exam questions: Step-by-step trace of K-Means clustering with Centroid convergence, Agglomerative Hierarchical clustering dendrograms (Single, Complete, and Average Linkage), Principal Component Analysis (PCA) eigenvalue/eigenvector derivation and covariance matrix diagonalization, Bagging (Random Forest) vs Boosting (AdaBoost weight re-weighting), and Bias-Variance tradeoff decomposition.
:::

* **Unsupervised Learning & Clustering**:
  * Unsupervised paradigm: Finding inherent structure in unlabeled data $\{x_1, \dots, x_m\}$.
  * Proximity and Similarity measures: Euclidean distance, Manhattan distance, Cosine similarity, Jaccard coefficient.
  * **Partitional Clustering: $K$-Means Algorithm**:
    * Objective function: Minimizing Within-Cluster Sum of Squares (WCSS / Inertia): $J = \sum_{k=1}^K \sum_{x \in C_k} \|x - \mu_k\|^2$.
    * Expectation-Maximization (EM) flavor: Assignment step and Update step; Convergence guarantee to local minimum.
    * Determining optimal $K$: The **Elbow Method** and Silhouette Analysis.
  * **Hierarchical Clustering**:
    * **Agglomerative Clustering (Bottom-Up)**: Pairwise distance matrix, merging closest clusters, dendrogram representation.
    * Linkage criteria: Single Linkage (MIN / chaining effect), Complete Linkage (MAX / spherical bias), Average Linkage, Ward's method.
    * Divisive Clustering (Top-Down) overview.
* **Dimensionality Reduction**:
  * Motivation: The Curse of Dimensionality, visualization, computational efficiency, noise reduction.
  * **Principal Component Analysis (PCA)**:
    * Objective: Maximizing variance of projected data or minimizing reconstruction error.
    * Step-by-step mathematical algorithm:
      1. Mean centering and standardization of the data matrix $X$.
      2. Computing the Sample Covariance Matrix $\Sigma = \frac{1}{m} X^T X$.
      3. Computing Eigenvalues $\lambda_i$ and Eigenvectors $v_i$ of $\Sigma$ via characteristic equation $|\Sigma - \lambda I| = 0$.
      4. Sorting eigenvectors by descending eigenvalues; Selecting top $k$ principal components.
      5. Transforming data into $k$-dimensional subspace: $Y = X V_k$.
    * Explained Variance Ratio $\frac{\lambda_i}{\sum \lambda_j}$ and scree plot analysis.
  * **Multidimensional Scaling (MDS)**:
    * Preserving pairwise dissimilarities/distances in lower-dimensional embedding; Metric vs Non-metric MDS.
* **Ensemble Learning & Resampling Methods**:
  * Philosophy of Ensembles: Combining weak learners into a strong learner; Condorcet's Jury Theorem intuition.
  * **Bagging (Bootstrap Aggregating)**:
    * Resampling with replacement (**Bootstrapping**); Training independent base models in parallel.
    * Aggregation: Majority voting for classification, mean averaging for regression.
    * Out-of-Bag (OOB) error estimation; Application: Random Forests (feature bagging).
  * **Boosting**:
    * Sequential adaptive learning; Converting weak hypotheses to strong hypotheses.
    * **AdaBoost (Adaptive Boosting)**: Sample re-weighting mechanism (increasing weights of misclassified instances), model voting weights ($\alpha_t$).
  * **Resampling Techniques**:
    * Hold-out validation, $K$-Fold Cross Validation, Stratified $K$-Fold, Leave-One-Out Cross Validation (LOOCV).
* **Practical Aspects: The Bias-Variance Tradeoff**:
  * Mathematical decomposition of Expected Prediction Error: $\text{Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise} (\sigma^2)$.
  * High Bias (Underfitting) vs High Variance (Overfitting).
  * Model complexity curves and diagnostic strategies (regularization, increasing dataset size, feature engineering).

---

## 📖 Prescribed Textbooks & Reference Books

### Prescribed Core Textbooks

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Introduction to Machine Learning** | **Ethem Alpaydin** | **MIT Press** | **4th Edition, 2020** |
| **2** | **Data Mining and Analysis: Fundamental Concepts and Algorithms** | **Mohammed J. Zaki, Wagner Meira** | **Cambridge University Press** | **1st Edition, 2016** |
| **3** | **Neural Networks for Pattern Recognition** | **Christopher Bishop** | **Oxford University Press** | **1st Edition, 1998** |

</div>

### Prescribed Reference Books

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Applied Machine Learning** | M. Gopal | McGraw-Hill Education | 2nd Edition, 2018 |
| **2** | **Machine Learning using Python** | Manaranjan Pradhan, U. Dinesh Kumar | Wiley | 1st Edition, 2019 |
| **3** | **Machine Learning: Theory and Practice** | M. N. Murty, V. S. Ananthanarayana | Universities Press | 1st Edition, 2024 |

</div>

---

## 🎥 Video Lectures & Online Course Resources

<div class="table-wrap">

| Platform | Course ID / Title | Resource Link | Focus Areas |
| :---: | :--- | :--- | :--- |
| **NPTEL / IIT Kharagpur** | Course 106105152 | [Machine Learning (Prof. Sudeshna Sarkar)](https://archive.nptel.ac.in/courses/106/105/106105152/) | Regression, Decision Trees, SVM, and Clustering algorithms. |
| **NPTEL / IIT Madras** | Course 106106139 | [Introduction to Machine Learning (Prof. Balaraman Ravindran)](https://archive.nptel.ac.in/courses/106/106/106106139/) | Probability foundations, Bayesian learning, Neural Networks, and PCA. |
| **NPTEL / IIT Madras** | Course 106106202 | [Applied Machine Learning / Data Science Series](https://nptel.ac.in/courses/106106202) | Model evaluation, ROC/AUC, Bagging, Boosting, and Bias-Variance tradeoff. |

</div>

---

## ⚖️ Course Assessment Method (CIE & ESE)

The course carries **100 Total Marks**, structured into **40 Marks for Continuous Internal Evaluation (CIE)** and **60 Marks for the University End Semester Examination (ESE)**.

### Continuous Internal Evaluation (CIE: 40 Marks)

<div class="table-wrap">

| Component | Marks Allocated | Evaluation Format & Regulations |
| :--- | :---: | :--- |
| **Attendance** | **5 Marks** | Minimum 75% attendance mandatory. Awarded on a sliding scale as per KTU B.Tech regulations. |
| **Assignment / Microproject** | **15 Marks** | Minimum of two rigorous conceptual assignments or one applied ML coding microproject (e.g., end-to-end regression/classification pipeline, custom backpropagation implementation from scratch, or PCA clustering visualizer). |
| **Internal Examination - 1 (Written)** | **10 Marks** | Written test covering **Module 1 and first half of Module 2** (scaled to 10 marks). |
| **Internal Examination - 2 (Written)** | **10 Marks** | Written test covering **second half of Module 2, Module 3, and Module 4** (scaled to 10 marks). |
| **Total CIE Marks** | **40 Marks** | **Eligibility: Minimum 45% (18/40 marks) required in CIE to be eligible for the End Semester Examination.** |

</div>

---

### End Semester Examination (ESE: 60 Marks)

* **Total Examination Duration**: **2 Hours 30 Minutes (150 Minutes)**
* **Total Question Paper Valuation**: **96 Marks** (Students write for a maximum of **60 Marks**)
* **Passing Requirement**: **Minimum 40% (24/60 marks) in ESE AND minimum 50% aggregate (50/100) combining CIE + ESE**.

<div class="table-wrap">

| Section | Question Distribution & Marks | Choice Rules | Section Marks |
| :---: | :--- | :--- | :---: |
| **Part A** | • **2 Questions from each module** (Modules 1, 2, 3, 4).<br>• Total of **8 Questions** (Questions 1 to 8).<br>• Each question carries **3 marks** ($8 \times 3 = 24$). | **Compulsory**<br>*(No internal choice)* | **24 Marks** |
| **Part B** | • **Two full questions from each module** (Questions 9 & 10 from M1, 11 & 12 from M2, 13 & 14 from M3, 15 & 16 from M4).<br>• Each full question carries **9 marks** ($4 \times 9 = 36$).<br>• Each full question can have **maximum 3 subdivisions** (e.g., 5+4, 6+3, or 3+3+3). | **Choice-based**<br>*(Answer any 1 full question from each module)* | **36 Marks** |
| **Total** | **Part A (24 Marks) + Part B (36 Marks)** | | **60 Marks** |

</div>

---

## 🎓 Course Outcomes (COs)

Upon successful completion of the Machine Learning course, students will demonstrate mastery across the following outcomes evaluated using **Bloom's Revised Taxonomy**:

<div class="table-wrap">

| CO Identifier | Course Outcome (CO) Statement | Bloom's Knowledge Level |
| :---: | :--- | :---: |
| **CO1** | **Illustrate** Machine Learning concepts and basic parameter estimation methods. | **K2 (Understand)** |
| **CO2** | **Demonstrate** supervised learning concepts (regression, classification). | **K3 (Apply)** |
| **CO3** | **Illustrate** the concepts of Multilayer neural network and Decision trees. | **K3 (Apply)** |
| **CO4** | **Describe** unsupervised learning concepts and dimensionality reduction techniques. | **K3 (Apply)** |
| **CO5** | **Use** appropriate performance measures to evaluate machine learning models. | **K3 (Apply)** |

</div>

::: callout-formula Bloom's Revised Taxonomy Levels Key
* **K1 - Remember**: Recalling definitions, formulas for Bayes' rule, Sigmoid activation, and cost functions.
* **K2 - Understand**: Explaining how learning paradigms differ, explaining overfitting mechanisms, describing kernel transformations.
* **K3 - Apply**: Computing Information Gain in Decision Trees, calculating Laplace-smoothed Naïve Bayes probabilities, deriving gradient updates, evaluating Confusion Matrix metrics ($F_1$, ROC), computing PCA eigenvalues.
* **K4 - Analyse**: Comparing Bias vs Variance tradeoffs, diagnosing underfitting/overfitting from learning curves, selecting optimal kernels.
* **K5 - Evaluate**: Assessing regression metrics (RMSE vs MAE vs $R^2$), evaluating multi-class classification boundaries.
* **K6 - Create**: Formulating custom multi-task loss functions or architectural ensembles for specialized datasets.
:::

---

## 🗺️ CO-PO Mapping Table

The Course Outcomes directly map to the **National Board of Accreditation (NBA) Program Outcomes (POs)** for undergraduate computer science and engineering:

*Correlation Scale: **3 = Substantial (High)** | **2 = Moderate (Medium)** | **1 = Slight (Low)** | **— = No Correlation***

<div class="table-wrap">

| Course Outcome | PO1<br><small>Engg Knowledge</small> | PO2<br><small>Problem Analysis</small> | PO3<br><small>Design/Dev</small> | PO4<br><small>Investigations</small> | PO5<br><small>Modern Tools</small> | PO6<br><small>Engineer & Society</small> | PO7<br><small>Environment</small> | PO8<br><small>Ethics</small> | PO9<br><small>Individual/Team</small> | PO10<br><small>Communication</small> | PO11<br><small>Project Mgmt</small> | PO12<br><small>Life-long Learning</small> |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CO1** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO2** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO3** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO4** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO5** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |

</div>

### CO-PO Mapping Justification & Insights:
* **PO1 (Engineering Knowledge)**: Strongly addressed across all five COs ($\text{Level } 3$) as Machine Learning requires linear algebra (matrices, eigenvalues), multivariable calculus (gradients, chain rule), and probability theory (Bayes, Gaussian distributions).
* **PO2 (Problem Analysis)**: Addressed at $\text{Level } 3$ across all COs through feature analysis, loss minimization, hyperparameter tuning, and error diagnosis.
* **PO3 (Design/Development of Solutions)**: Substantially addressed ($\text{Level } 3$) as students architect predictive regression pipelines, neural networks, decision trees, and clustering engines.
* **PO4 (Conduct Investigations of Complex Problems)**: Addressed at $\text{Level } 3$ via empirical model comparison, cross-validation, ROC/AUC curve investigations, and bias-variance decomposition.

---

## ⚡ Interactive Syllabus Self-Check Quiz

::: quiz KTU PCCST503 Parameter Estimation & Regularization
In Module 1 and 2 of the Machine Learning syllabus, what is the exact mathematical connection between Maximum A Posteriori (MAP) estimation and Regularization?
(*) MAP estimation with a zero-mean Gaussian prior on weights corresponds to L2 Regularization (Ridge), while a Laplace prior corresponds to L1 Regularization (Lasso).
( ) MAP estimation is strictly identical to MLE with no prior assumptions.
( ) MAP estimation with a uniform prior corresponds to L1 regularization.
( ) Regularization is only used in unsupervised learning, not in MAP parameter estimation.
::: explanation
Under Bayesian parameter estimation, maximizing the log posterior probability yields $\hat{\theta}_{\text{MAP}} = \arg\max_\theta [\ln P(D|\theta) + \ln P(\theta)]$. When the prior $P(\theta)$ is modeled as an independent Gaussian distribution $\mathcal{N}(0, \sigma^2)$, $\ln P(\theta) \propto -\frac{1}{2\sigma^2}\sum \theta_j^2$, which is mathematically equivalent to L2 (Ridge) regularization. When $P(\theta)$ is modeled as a Laplace distribution, $\ln P(\theta) \propto -\lambda \sum |\theta_j|$, which is mathematically equivalent to L1 (Lasso) regularization.
:::

::: quiz Ensemble Methods: Bagging vs. Boosting
According to Module 4 of the syllabus, how do Bagging and Boosting differ in their training philosophy and variance/bias reduction?
(*) Bagging trains independent models in parallel on bootstrap samples to reduce model variance, whereas Boosting trains models sequentially by re-weighting errors to reduce model bias.
( ) Bagging trains models sequentially, while Boosting trains models in parallel.
( ) Both Bagging and Boosting only reduce irreducible noise without affecting bias or variance.
( ) Bagging is strictly unsupervised (K-Means), whereas Boosting is strictly for regression.
::: explanation
In Ensemble Learning: **Bagging (Bootstrap Aggregating)** generates multiple bootstrap subsets with replacement and trains models in parallel to average predictions, primarily **reducing variance** (e.g., Random Forests). **Boosting** trains weak learners sequentially where subsequent learners focus on misclassified samples from previous iterations, primarily **reducing bias** (e.g., AdaBoost).
:::

---

## 🧭 Next Steps in Your Study Journey

* Begin with **[Module 1: 1.1 Introduction to Machine Learning and Paradigms](m1_01_introduction_to_machine_learning_and_paradigms.html)** to master traditional vs. machine learning paradigms.
* Master Bayesian estimation in **[Module 1: 1.3 Maximum Likelihood Estimation (MLE)](m1_03_maximum_likelihood_estimation_mle.html)** and **[Module 1: 1.4 Maximum A Posteriori (MAP)](m1_04_maximum_a_posteriori_map_and_bayesian_formulation.html)**.
* Practice hands-on numerical calculations in the **[Module 1 Workbook: Linear Regression OLS](m1_p01_linear_regression_ols.html)** and **[Regularization (Ridge & Lasso)](m1_p04_regularization_ridge_lasso.html)**.
* Practice decision trees in **[Module 2 Workbook: Information Gain Calculation](m2_p01_information_gain_calculation.html)**.
* Review key formulas anytime with the **[Anki-style Spaced Repetition Review Deck](../../review.html)**.
