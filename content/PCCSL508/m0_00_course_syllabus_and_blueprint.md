# KTU Official Syllabus: Machine Learning Lab (PCCSL508)

Welcome to the official practical syllabus and laboratory examination blueprint for **Machine Learning Lab (PCCSL508)**, prescribed under the **APJ Abdul Kalam Technological University (KTU) 2024 Scheme for Semester 5 (S5) Computer Science and allied branches (Common to CS/CA)**.

---

## 📋 Course Overview

<div class="table-wrap">

| Parameter | Specification Details |
| :--- | :--- |
| **Course Name** | **Machine Learning Lab** |
| **Course Code** | `PCCSL508` |
| **Semester** | **Semester 5 (S5)** |
| **Degree & Branch** | **B.Tech (Common to CS / CA)** |
| **Teaching Hours / Week** | **0:0:3:0** *(Lecture: 0, Tutorial: 0, Practical: 3 hrs/week, Remedial: 0)* |
| **Total Practical Hours** | **36–42 Contact Lab Hours (20 Prescribed Experiments)** |
| **Course Credits** | **2 Credits** |
| **Course Type** | **Laboratory (Practical)** |
| **Prerequisites** | **None** |
| **Continuous Internal Evaluation (CIE)** | **50 Marks** *(Continuous Lab Assessment: 25, Lab Test: 20, Attendance: 5)* |
| **End Semester Examination (ESE)** | **50 Marks** *(External Practical Exam with Certified Record)* |
| **Total Marks** | **100 Marks** |
| **Examination Duration** | **2 Hours 30 Minutes (150 Minutes)** |

</div>

::: callout-intuition From Equations to Code: Practical Machine Learning
While theoretical machine learning introduces mathematical loss surfaces, parameter estimation, and vector calculus, true mastery requires building end-to-end pipelines. In this laboratory, students implement algorithms from scratch and using industry-standard libraries (Scikit-Learn, NumPy, Matplotlib, PyTorch/TensorFlow) across 20 benchmark datasets—mastering data preprocessing, convergence debugging, hyperparameter tuning, and error diagnosis.
:::

---

## 🎯 Course Objectives

The primary pedagogical objective of the laboratory course is:

* **Practical Machine Learning Fluency**: To give the learner practical experience implementing and evaluating the full spectrum of machine learning techniques (regression, parameter estimation, classification, margin classifiers, deep neural networks, clustering, and ensemble methods) on real-world benchmark datasets using Python.

---

## 🧪 Comprehensive List of 20 Lab Experiments

The laboratory curriculum is structured across **5 core experimental domains**:

1. **Regression & Parameter Estimation** (Experiments 1 – 5)
2. **Supervised Classification & Decision Trees** (Experiments 6 – 10)
3. **Support Vector Machines & Neural Networks** (Experiments 11 – 15)
4. **Unsupervised Clustering & Resampling** (Experiments 16 – 18)
5. **Ensemble Methods & Bias-Variance Analysis** (Experiments 19 – 20)

---

### Domain 1: Regression & Parameter Estimation

#### Experiment 1: Simple Linear Regression (California Housing Dataset)
* **Objective**: Predict housing prices based on average rooms per dwelling using univariate linear regression.
* **Experimental Tasks**:
  1. Load and preprocess California Housing data; perform standard train-test split.
  2. Implement linear regression using **Batch Gradient Descent** (iterative parameter updates).
  3. Implement linear regression using the **Normal Equation** closed-form solution: $\theta = (X^T X)^{-1} X^T y$.
  4. Evaluate model performance using Mean Squared Error (MSE) and Coefficient of Determination ($R^2$ score).
  5. Visualize fitted regression line alongside empirical scatter data points.

#### Experiment 2: Polynomial Regression & Degree Comparison (Auto MPG Dataset)
* **Objective**: Predict miles per gallon (MPG) based on engine displacement using non-linear polynomial features.
* **Experimental Tasks**:
  1. Load and clean Auto MPG dataset (handling missing values in horsepower/displacement).
  2. Generate polynomial feature transformations ($x, x^2, \dots, x^d$) across varying degrees ($d = 1, 2, 3, 5, 8$).
  3. Compare polynomial regression performance against baseline linear regression using MSE and $R^2$.
  4. Plot non-linear polynomial fit curves over the data scatter plot.

#### Experiment 3: Regularized Regression: Ridge & Lasso (Diabetes Dataset)
* **Objective**: Prevent overfitting on high-dimensional biomedical regression features via regularized shrinkage.
* **Experimental Tasks**:
  1. Load and standardize Diabetes dataset features.
  2. Implement **Ridge Regression (L2 norm)** and **LASSO Regression (L1 norm)**.
  3. Perform hyperparameter tuning for penalty parameter $\lambda / \alpha$ using $K$-fold cross-validation (`RidgeCV`, `LassoCV`).
  4. Compare MSE, $R^2$, and inspect weight shrinkage vs feature zeroing (sparsity in Lasso).

#### Experiment 4: Logistic Regression Parameter Estimation: MLE vs MAP (Breast Cancer Wisconsin)
* **Objective**: Contrast Maximum Likelihood Estimation with Maximum A Posteriori estimation on medical diagnostics.
* **Experimental Tasks**:
  1. Load and normalize Breast Cancer Wisconsin diagnostic dataset.
  2. Train Logistic Regression using Maximum Likelihood Estimation (unregularized Log-Loss).
  3. Apply MAP estimation incorporating Gaussian prior (L2 Ridge) and Laplace prior (L1 Lasso).
  4. Compare parameter coefficient trajectories and classification accuracy between MLE and MAP.

#### Experiment 5: Multinomial Parameter Estimation with Dirichlet Priors (20 Newsgroups)
* **Objective**: Estimate vocabulary distribution parameters using MLE and MAP smoothing on NLP document text.
* **Experimental Tasks**:
  1. Vectorize text documents using Bag-of-Words / CountVectorizer.
  2. Implement MLE for multinomial distribution word probabilities ($P(w_k | c) = \frac{n_k}{n}$).
  3. Apply MAP estimation using symmetric **Dirichlet priors** (Additive / Laplace smoothing with varying $\alpha$).
  4. Evaluate the impact of different prior pseudo-counts on rare word probabilities and test classification.

---

### Domain 2: Supervised Classification & Decision Trees

#### Experiment 6: Logistic Regression & Feature Scaling (Pima Indians Diabetes Dataset)
* **Objective**: Analyze the operational significance of feature normalization in gradient-based classification.
* **Experimental Tasks**:
  1. Load Pima Indians Diabetes dataset; analyze heterogeneous feature scales (glucose, insulin, BMI).
  2. Train Logistic Regression model directly without feature scaling.
  3. Train a parallel Logistic Regression model with Standard Scaling ($z = \frac{x - \mu}{\sigma}$) / MinMax scaling.
  4. Compare convergence rate (iterations to converge), weights, and metrics: Accuracy, Precision, Recall, $F_1$-Score.

#### Experiment 7: Multinomial vs Bernoulli Naïve Bayes (20 Newsgroups Dataset)
* **Objective**: Compare count-based vs binary presence feature representations for text classification.
* **Experimental Tasks**:
  1. Extract Bag-of-Words word counts (for Multinomial NB) and boolean word occurrence flags (for Bernoulli NB).
  2. Train Multinomial Naïve Bayes and Bernoulli Naïve Bayes classifiers.
  3. Evaluate accuracy, micro/macro $F_1$-scores across newsgroup topics.
  4. Document strengths and weaknesses of each variant regarding document length variability.

#### Experiment 8: $K$-Nearest Neighbors (KNN) Image Classification (Fashion MNIST)
* **Objective**: Classify multi-class fashion apparel grayscale images ($28 \times 28$) using instance-based learning.
* **Experimental Tasks**:
  1. Load Fashion MNIST dataset; flatten image matrices into 784-dimensional feature vectors.
  2. Implement KNN classifier across varying neighborhood values: $K \in \{1, 3, 5, 7, 11, 21\}$.
  3. Plot accuracy vs $K$ curve and analyze the computational latency trade-off during the testing phase.

#### Experiment 9: Decision Tree ID3 & Customer Segmentation (Online Retail Dataset)
* **Objective**: Segment e-commerce customer behavior (Recency, Frequency, Monetary value) using Information Gain.
* **Experimental Tasks**:
  1. Load Online Retail transaction data and compute customer RFM metrics.
  2. Construct Decision Tree classifier using Quinlan's **ID3 algorithm** (Shannon Entropy and Information Gain).
  3. Visualize tree branching architecture (Root node, decision splits, leaf nodes).
  4. Compute and interpret Gini / Entropy feature importance scores.

#### Experiment 10: Model Comparison: Logistic Regression vs Decision Trees (Adult Income)
* **Objective**: Compare linear probabilistic modeling vs non-linear axis-aligned partitioning on census demographic data.
* **Experimental Tasks**:
  1. Preprocess Adult Income census data (one-hot encoding categorical variables, handling missing markers).
  2. Train Logistic Regression and Decision Tree classifiers to predict binary income threshold ($> 50\text{K}$).
  3. Compare models via Confusion Matrix, Precision, Recall, $F_1$, and ROC/AUC curves.
  4. Critically discuss model interpretability (coefficients vs decision rules) and suitability for credit/legal domains.

---

### Domain 3: Support Vector Machines & Neural Networks

#### Experiment 11: Linear SVM & Margin Visualization (Iris Dataset)
* **Objective**: Formalize maximum margin classification and support vector geometry on 2D flower measurements.
* **Experimental Tasks**:
  1. Extract two linearly separable features from Iris dataset (e.g., Petal Length vs Petal Width).
  2. Implement Linear Support Vector Machine for binary classification (Setosa vs Non-Setosa).
  3. Plot the optimal separating hyperplane ($w^T x + b = 0$) and the two margin boundaries ($w^T x + b = \pm 1$).
  4. Highlight the exact **Support Vectors** that define the margin width ($\frac{2}{\|w\|}$).

#### Experiment 12: Non-Linear SVM Kernels Comparison (Fashion MNIST Dataset)
* **Objective**: Evaluate non-linear boundary projection using Mercer kernels on complex visual apparel data.
* **Experimental Tasks**:
  1. Load Fashion MNIST feature subset; normalize pixel intensities.
  2. Train SVM classifiers across different kernel functions: **Linear**, **Polynomial** ($d=3$), and **Radial Basis Function (RBF / Gaussian)**.
  3. Compare cross-validation classification accuracy, training runtimes, and support vector counts.
  4. Discuss hyperparameter sensitivity ($\gamma$ bandwidth and soft-margin penalty $C$).

#### Experiment 13: Multilayer Perceptron (MLP) Architectural Exploration (Wine Quality Dataset)
* **Objective**: Design and train feedforward neural networks with varying hidden depth and neuron capacity.
* **Experimental Tasks**:
  1. Load physicochemical properties from Wine Quality dataset.
  2. Architect MLPs with diverse topology variations: shallow (1 hidden layer), balanced (2 hidden layers), deep (3+ hidden layers).
  3. Train networks using Backpropagation and Adam optimizer.
  4. Analyze train/validation loss curves to identify underfitting vs capacity saturation.

#### Experiment 14: Activation Function Impact: Sigmoid vs ReLU vs Tanh (MNIST Dataset)
* **Objective**: Investigate gradient flow, convergence velocity, and training dynamics across non-linear activations.
* **Experimental Tasks**:
  1. Load handwritten digits dataset (MNIST).
  2. Build identical 3-layer neural network architectures swapping only the hidden layer activation: **Logistic Sigmoid**, **Hyperbolic Tangent (Tanh)**, and **Rectified Linear Unit (ReLU)**.
  3. Record and plot training loss decay and epoch convergence over time.
  4. Analyze vanishing gradient phenomena in Sigmoid/Tanh vs high-speed training in ReLU.

#### Experiment 15: Deep Learning Hyperparameter Optimization (Fashion MNIST)
* **Objective**: Systematically optimize learning rates, mini-batch dimensions, and training duration.
* **Experimental Tasks**:
  1. Setup baseline convolutional or dense neural network on Fashion MNIST.
  2. Experiment with varied learning rates ($\alpha \in \{0.1, 0.01, 0.001, 0.0001\}$), batch sizes (16, 32, 64, 128, 256), and epoch schedules.
  3. Plot validation loss trajectories to demonstrate training divergence (too high $\alpha$) vs sluggish learning (too low $\alpha$).
  4. Document optimal parameter configurations for generalized testing accuracy.

---

### Domain 4: Unsupervised Clustering & Resampling

#### Experiment 16: Hierarchical vs Partitional Clustering (Mall Customers Dataset)
* **Objective**: Uncover customer spending segments without ground-truth labels using distance metrics.
* **Experimental Tasks**:
  1. Load Mall Customer dataset (Annual Income vs Spending Score).
  2. Apply **$K$-Means Partitional Clustering**; identify optimal cluster count using the **Elbow Method (WCSS)**.
  3. Apply **Agglomerative Hierarchical Clustering**; plot dendrogram across Single, Complete, and Ward linkage.
  4. Compare cluster quality using **Silhouette Coefficient scores** and visual cluster boundary plots.

#### Experiment 17: $K$-Means Clustering & Silhouette Analysis (Optical Digits Dataset)
* **Objective**: Unsupervised digit grouping and cluster quality verification.
* **Experimental Tasks**:
  1. Load 8x8 handwritten Digits dataset ($n=1797$).
  2. Execute $K$-Means clustering for cluster counts $K \in [2, 15]$.
  3. Compute Inertia (Within-Cluster Sum of Squares) and Silhouette Scores for each $K$.
  4. Analyze how well cluster centers map to visual digit templates when $K=10$.

#### Experiment 18: Resampling Techniques: Bootstrapping vs $K$-Fold Cross Validation (Iris Dataset)
* **Objective**: Quantify model estimator variance and evaluation confidence bounds via statistical resampling.
* **Experimental Tasks**:
  1. Implement **Bootstrapping**: generate $B=1000$ resampled datasets with replacement, train base classifiers, and calculate 95% bootstrap confidence intervals for accuracy.
  2. Implement **$K$-Fold Cross Validation** ($K=5, 10$) and Stratified $K$-Fold.
  3. Contrast computational complexity, bias in performance estimation, and data efficiency.

---

### Domain 5: Ensemble Methods & Bias-Variance Analysis

#### Experiment 19: Ensemble Learning: Bagging vs Boosting (Titanic Dataset)
* **Objective**: Evaluate variance reduction (Random Forest) vs bias reduction (AdaBoost) on tabular survival data.
* **Experimental Tasks**:
  1. Preprocess Titanic passenger data (imputing missing ages, encoding categorical embarkation/sex).
  2. Train **Bagging Ensemble** using Decision Tree base estimators (Bootstrap Aggregation / Random Forest).
  3. Train **Boosting Ensemble** using Adaptive Boosting (**AdaBoost** with sequential sample re-weighting).
  4. Compare Accuracy, Precision, Recall, $F_1$, and analyze why ensembles outperform single decision stumps.

#### Experiment 20: Empirical Bias-Variance Tradeoff Decomposition (Boston Housing Dataset)
* **Objective**: Measure training error vs validation error across polynomial model complexities.
* **Experimental Tasks**:
  1. Load Boston Housing dataset (predicting median home values).
  2. Fit polynomial regression models across increasing polynomial degrees ($d \in [1, 10]$).
  3. Plot **Mean Squared Error on Training Set** vs **Mean Squared Error on Validation Set** against degree $d$.
  4. Identify Underfitting regime (High Bias), Overfitting regime (High Variance), and the Sweet Spot of optimal generalization.

---

## ⚖️ Course Assessment Method (CIE: 50 Marks, ESE: 50 Marks)

### Continuous Internal Evaluation (CIE: 50 Marks)

<div class="table-wrap">

| Component | Marks Allocated | Evaluation Details |
| :--- | :---: | :--- |
| **Attendance** | **5 Marks** | Minimum 75% attendance mandatory. |
| **Continuous Assessment** | **25 Marks** | Continuous assessment averaged across all 20 lab sessions: |
| ↳ *1. Preparation & Pre-Lab Work* | *(7 Marks)* | Pre-lab assignments, conceptual quizzes, algorithm readiness. |
| ↳ *2. Conduct of Experiments* | *(7 Marks)* | Adherence to procedures, correct coding, troubleshooting skill, teamwork. |
| ↳ *3. Lab Reports & Record Keeping* | *(6 Marks)* | Completeness of rough record, prompt submission of certified fair record. |
| ↳ *4. Lab Viva Voce* | *(5 Marks)* | Oral defense of experiment logic, math formulations, and metric analysis. |
| **Internal Lab Examination** | **20 Marks** | Model practical test (coding, model training, metric evaluation, viva). |
| **Total CIE Marks** | **50 Marks** | **Minimum 45% (23/50 marks) in CIE required for ESE eligibility.** |

</div>

---

### End Semester Examination (ESE: 50 Marks)

* **Examination Duration**: **2 Hours 30 Minutes (150 Minutes)**
* **Certified Record Requirement**: Duly certified laboratory record signed by the faculty-in-charge and external examiner is mandatory for exam entry.

<div class="table-wrap">

| Sl. No. | Evaluation Stage | Marks | Assessment Rubric |
| :---: | :--- | :---: | :--- |
| **1** | **Procedure / Preparatory Work / Design / Algorithm** | **10 Marks** | Clarity of procedure, mathematical loss function formulation, data preprocessing pipeline design. |
| **2** | **Conduct of Experiment / Execution / Troubleshooting / Programming** | **15 Marks** | Accurate Python script execution, proper use of NumPy / Pandas / Scikit-Learn APIs, convergence debugging. |
| **3** | **Result with Valid Inference / Quality of Output** | **10 Marks** | Correct evaluation metrics (MSE, $R^2$, Accuracy, $F_1$, ROC/AUC), plots (decision boundary, loss curve, elbow curve). |
| **4** | **Viva Voce** | **10 Marks** | Oral examination testing theoretical foundations, optimization math, hyperparameter behavior, and model assumptions. |
| **5** | **Lab Record** | **5 Marks** | Neatness, completeness, and accuracy of endorsed lab record. |
| **Total** | **End Semester Practical Examination** | **50 Marks** | **Minimum 40% (20/50 marks) required in ESE.** |

</div>

---

## 📖 Prescribed Textbooks & Reference Books

### Prescribed Core Textbooks

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Introduction to Machine Learning** | **Ethem Alpaydin** | **MIT Press** | **4th Edition, 2020** |
| **2** | **Machine Learning using Python** | **Manaranjan Pradhan, U. Dinesh Kumar** | **Wiley** | **1st Edition, 2019** |
| **3** | **Machine Learning: Theory and Practice** | **M. N. Murty, V. S. Ananthanarayana** | **Universities Press** | **1st Edition, 2024** |

</div>

### Prescribed Reference Books

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Data Mining and Analysis: Fundamental Concepts and Algorithms** | Mohammed J. Zaki, Wagner Meira | Cambridge University Press | 1st Edition, 2016 |
| **2** | **Neural Networks for Pattern Recognition** | Christopher Bishop | Oxford University Press | 1st Edition, 1998 |

</div>

---

## 🎥 Video Lectures & Online Lab Tutorials

<div class="table-wrap">

| Platform | Course ID / Link | Focus Areas |
| :---: | :--- | :--- |
| **NPTEL / IIT Kharagpur** | [Machine Learning (Course 106105152)](https://archive.nptel.ac.in/courses/106/105/106105152/) | Regression, Decision Trees, SVM, and Clustering implementations. |
| **NPTEL / IIT Madras** | [Introduction to Machine Learning (Course 106106139)](https://archive.nptel.ac.in/courses/106/106/106106139/) | Optimization, Backpropagation, and Bayesian estimation practicals. |
| **NPTEL / IIT Madras** | [Applied Machine Learning / Data Science (Course 106106202)](https://nptel.ac.in/courses/106106202) | Pipeline construction, cross-validation, and ROC/AUC metrics. |

</div>

---

## 🎓 Course Outcomes (COs)

Upon successful completion of the Machine Learning Lab, students will demonstrate mastery across the following outcomes:

<div class="table-wrap">

| CO Identifier | Course Outcome (CO) Statement | Bloom's Knowledge Level |
| :---: | :--- | :---: |
| **CO1** | **Understand** complexity of Machine Learning algorithms and their limitations. | **K2 (Understand)** |
| **CO2** | **Understand** modern notions in data analysis-oriented computing. | **K2 (Understand)** |
| **CO3** | **Apply** common Machine Learning algorithms in practice and implement their own. | **K3 (Apply)** |
| **CO4** | **Performing** experiments in Machine Learning using real-world data. | **K3 (Apply)** |

</div>

---

## 🗺️ CO-PO Mapping Table

*Correlation Scale: **3 = Substantial (High)** | **2 = Moderate (Medium)** | **1 = Slight (Low)** | **— = No Correlation***

<div class="table-wrap">

| Course Outcome | PO1<br><small>Engg Knowledge</small> | PO2<br><small>Problem Analysis</small> | PO3<br><small>Design/Dev</small> | PO4<br><small>Investigations</small> | PO5<br><small>Modern Tools</small> | PO6<br><small>Engineer & Society</small> | PO7<br><small>Environment</small> | PO8<br><small>Ethics</small> | PO9<br><small>Individual/Team</small> | PO10<br><small>Communication</small> | PO11<br><small>Project Mgmt</small> | PO12<br><small>Life-long Learning</small> |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CO1** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — |
| **CO2** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — |
| **CO3** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — |
| **CO4** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — |

</div>

---

## ⚡ Interactive Lab Self-Check Quiz

::: quiz Linear Regression: Gradient Descent vs Normal Equation
In Experiment 1 of the Machine Learning Lab, under what scenario is Gradient Descent preferred over the Normal Equation closed-form solution $\theta = (X^T X)^{-1} X^T y$?
(*) When the number of features $n$ is very large (e.g., $n > 10,000$), because matrix inversion $(X^T X)^{-1}$ has an intractable computational complexity of $O(n^3)$.
( ) When the dataset is very small, because the normal equation only works on billions of records.
( ) Gradient Descent is always slower and less accurate than the normal equation regardless of dataset size.
( ) Normal Equation requires tuning the learning rate $\alpha$, whereas Gradient Descent has no hyperparameters.
::: explanation
The **Normal Equation** requires computing the inverse of an $n \times n$ matrix $(X^T X)^{-1}$, which carries a computational time complexity of approximately $\mathcal{O}(n^3)$. When the number of features $n$ is large (thousands or millions, common in text/image processing), inverting $(X^T X)$ becomes computationally prohibitive and memory-exhausting. In contrast, **Gradient Descent** scales gracefully as $\mathcal{O}(k n m)$, making it the standard choice for large-scale high-dimensional data.
:::

::: quiz Regularization Geometry: Ridge vs Lasso
In Experiment 3, why does LASSO regression (L1 regularization) produce sparse models with exact zero coefficients, while Ridge regression (L2 regularization) only shrinks coefficients close to zero?
(*) The L1 constraint region has sharp corners (diamond vertices) on the coordinate axes where the elliptical loss contours typically intersect first, setting coordinates exactly to zero.
( ) Ridge regression penalizes absolute values, while Lasso penalizes squared values.
( ) Lasso is strictly an unsupervised clustering algorithm, not a regression penalty.
( ) Ridge regression removes all negative coefficients from the model.
::: explanation
Geometrically, the **L1 regularization constraint** forms a diamond/polytope with sharp vertices aligned along the coordinate axes ($\beta_j = 0$). When the elliptical contours of the unconstrained OLS sum-of-squares loss surface expand, they are geometrically most likely to touch a corner vertex of the diamond first, forcing that coefficient $\beta_j$ to become exactly zero. The **L2 constraint** is a smooth hypersphere without corners, resulting in continuous coefficient shrinkage toward zero without exact zeroing.
:::

---

## 🧭 Next Steps in Your Study Journey

* Master the theoretical foundations in **[Machine Learning Module 1: Foundations and Regression](../PCCST503/m1_01_introduction_to_machine_learning_and_paradigms.html)**.
* Practice hands-on regression derivations in the **[Module 1 Workbook: Linear Regression OLS](../PCCST503/m1_p01_linear_regression_ols.html)**.
* Review key formulas and algorithms in the **[Anki-style Spaced Repetition Review Deck](../../review.html)**.
