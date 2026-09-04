# Module 2: Supervised Learning — Decision Trees Theory
## Splitting Criteria, Information-Theoretic Foundations, and the ID3 Inductive Framework

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Module Alignment:** Module 2 (Supervised Learning & Symbolic Classifiers)  
> **Prerequisites:** Probability Foundations (Joint & Conditional Distributions), Summations, and Basic Calculus.

---

# Table of Contents
1. [Geometric Intuition: Axis-Parallel Orthogonal Partitioning](#1-geometric-intuition-axis-parallel-orthogonal-partitioning)
   - [Recursive Space Decomposition](#recursive-space-decomposition)
   - [Piecewise Constant Decision Surfaces](#piecewise-constant-decision-surfaces)
   - [Comparison with Slanted Hyperplanes](#comparison-with-slanted-hyperplanes)
2. [Information Theory Foundations: Measuring Surprise and Uncertainty](#2-information-theory-foundations-measuring-surprise-and-uncertainty)
   - [Claude Shannon’s Intuition of Information Content](#claude-shannons-intuition-of-information-content)
   - [Mathematical Formulation of Shannon Entropy](#mathematical-formulation-of-shannon-entropy)
   - [Behavioral Extremes: Homogeneity vs. Maximum Uncertainty](#behavioral-extremes-homogeneity-vs-maximum-uncertainty)
   - [Base of the Logarithm and Units of Information](#base-of-the-logarithm-and-units-of-information)
3. [The Criterion of Purity: Information Gain](#3-the-criterion-of-purity-information-gain)
   - [Conditional Entropy of a Split](#conditional-entropy-of-a-split)
   - [Formal Derivation of Information Gain](#formal-derivation-of-information-gain)
   - [The High-Cardinality Multi-Valued Attribute Pathological Bias](#the-high-cardinality-multi-valued-attribute-pathological-bias)
4. [Alternative Impurity Metrics: The Gini Index](#4-alternative-impurity-metrics-the-gini-index)
   - [Statistical Derivation from Misclassification Probability](#statistical-derivation-from-misclassification-probability)
   - [Gini Impurity of a Single Node](#gini-impurity-of-a-single-node)
   - [Gini Impurity of a Split (Weighted Gini)](#gini-impurity-of-a-split-weighted-gini)
   - [Entropy vs. Gini: Analytical & Computational Comparison](#entropy-vs-gini-analytical--computational-comparison)
5. [Algorithmic Mechanics of the ID3 Algorithm](#5-algorithmic-mechanics-of-the-id3-algorithm)
   - [The Top-Down Induction of Decision Trees (TDIDT) Framework](#the-top-down-induction-of-decision-trees-tdidt-framework)
   - [Complete Algorithmic Pseudocode](#complete-algorithmic-pseudocode)
   - [Recursive Base Cases and Termination Criteria](#recursive-base-cases-and-termination-criteria)
   - [Inductive Bias in Decision Tree Search](#inductive-bias-in-decision-tree-search)
6. [Structural Vulnerabilities and Remedies](#6-structural-vulnerabilities-and-remedies)
   - [Overfitting and the Infinite Hypothesis Space Trap](#overfitting-and-the-infinite-hypothesis-space-trap)
   - [Pre-Pruning (Early Stopping) vs. Post-Pruning (Reduced Error Pruning)](#pre-pruning-early-stopping-vs-post-pruning-reduced-error-pruning)
   - [Handling Continuous-Valued Features via Dynamical Thresholding](#handling-continuous-valued-features-via-dynamical-thresholding)
   - [Handling Missing Attributes During Induction](#handling-missing-attributes-during-induction)
7. [Comprehensive Step-by-Step Numerical Walkthroughs](#7-comprehensive-step-by-step-numerical-walkthroughs)
   - [Worked Problem 1: Manual Calculation of Entropy and Multi-Class Information Gain](#worked-problem-1-manual-calculation-of-entropy-and-multi-class-information-gain)
   - [Worked Problem 2: Full Iteration of ID3 Tree Building (Root Node Selection)](#worked-problem-2-full-iteration-of-id3-tree-building-root-node-selection)
   - [Worked Problem 3: Gini Impurity vs. Information Gain Conflict Analysis](#worked-problem-3-gini-impurity-vs-information-gain-conflict-analysis)
   - [Worked Problem 4: Finding the Optimal Split Point for a Continuous Attribute](#worked-problem-4-finding-the-optimal-split-point-for-a-continuous-attribute)
8. [KTU University Examination Practice Questions](#8-ktu-university-examination-practice-questions)
   - [Short-Answer Analytical Problems (Part A)](#short-answer-analytical-problems-part-a)
   - [Comprehensive Essay & Derivation Questions (Part B)](#comprehensive-essay--derivation-questions-part-b)

---

# 1. Geometric Intuition: Axis-Parallel Orthogonal Partitioning

## Recursive Space Decomposition
A decision tree is a hierarchical, non-parametric supervised learning model that represents decisions and decision-making processes visually and explicitly. Unlike linear classifiers (such as Logistic Regression or Perceptrons) that attempt to divide the feature space using a single flat hyperplane, a decision tree segments the input feature space $\mathcal{X} \subseteq \mathbb{R}^d$ into a set of mutually exclusive, collectively exhaustive hyper-rectangles (or "boxes").

```
Feature X2
   ^
   |-----------------------------+-----------------------------|
   |                             |                             |
   |                             |          Region R2          |
   |          Region R1          |          (Class +)          |
   |          (Class -)          |                             |
t2 |-----------------------------+-----------------------------|
   |                             |                             |
   |          Region R3          |          Region R4          |
   |          (Class +)          |          (Class -)          |
   |                             |                             |
   +-----------------------------+-----------------------------> Feature X1
                                 t1
```

Each non-leaf node represents a test on a specific feature, splitting the feature space along a line parallel to one of the coordinate axes.
1. The first internal node splits the entire space into two half-spaces using the threshold rule $X_1 \le t_1$.
2. In the right half-space ($X_1 > t_1$), another independent split is created using the rule $X_2 \le t_2$.
3. The process continues recursively until a designated stopping criterion is met.

## Piecewise Constant Decision Surfaces
Within each resulting terminal region $R_m$, the predicted probability or label is modeled as a constant value. 

> **Definition (Piecewise Constant Predictor):** For a partition of the feature space into $M$ disjoint regions $R_1, R_2, \dots, R_M$, the decision tree hypothesis $h(\mathbf{x})$ can be formally written as:
> $$h(\mathbf{x}) = \sum_{m=1}^M c_m \cdot \mathbb{I}(\mathbf{x} \in R_m)$$
> where:
> - $c_m$ is the class label assigned to region $R_m$ (typically the majority class among training points inside $R_m$).
> - $\mathbb{I}(\cdot)$ is the indicator function, returning $1$ if the condition is true and $0$ otherwise.

## Comparison with Slanted Hyperplanes
Because every decision split interrogates a **single feature at a time** (e.g., $x_j \le \theta$), the resulting decision boundaries are strictly **axis-parallel (orthogonal to the coordinate axes)**. 

```
TRUE DIAGONAL CONCEPT (x1 + x2 = c)           DECISION TREE STAIRCASE APPROXIMATION
      x2 ^                                          x2 ^
         |        /                                    |        |-----
         |       /                                     |        |
         |      /   Class +                            |   |----+  Class +
         |     /                                       |   |
         |    /                                        |---+
         |   /      Class -                            |         Class -
         +-------------------------> x1                +-------------------------> x1
```

- If the true target boundary is smooth and diagonal (such as $x_1 + x_2 \ge 1$), a standard decision tree must construct an intricate "staircase" pattern using dozens of nested horizontal and vertical cuts.
- While flexible, this axis-parallel constraint can make decision trees inefficient for modeling linear relationships with correlated features, leading to high variance unless an ensemble (like Random Forests) or oblique decision trees (which allow splits like $\mathbf{w}^T \mathbf{x} \le \theta$) are used.

---

# 2. Information Theory Foundations: Measuring Surprise and Uncertainty

## Claude Shannon’s Intuition of Information Content
To build an optimal decision tree, an algorithm needs a metric to quantify the "purity" or "disorder" of class labels at any given node. The mathematical basis comes from Claude Shannon's landmark 1948 paper, *"A Mathematical Theory of Communication."*

Shannon framed the problem around **surprise**:
- If an event is certain to happen ($P(E) = 1$), observing it gives you **zero new information** (0 surprise).
- If an event is extremely rare ($P(E) \to 0$), observing it provides a **high amount of information** (maximum surprise).

> **Definition (Self-Information):** The information content (or "surprisal") of observing an event with probability $p$ is inversely related to its probability:
> $$I(p) = \log_2 \left(\frac{1}{p}\right) = -\log_2(p)$$

If a coin has two heads, $P(\text{Heads}) = 1$. The surprise is:
$$I(1) = -\log_2(1) = 0 \text{ bits}$$
If a fair coin lands on heads, $P(\text{Heads}) = 0.5$. The surprise is:
$$I(0.5) = -\log_2(0.5) = -(-1) = 1 \text{ bit}$$

## Mathematical Formulation of Shannon Entropy
**Entropy** is the expected (average) value of surprise over all possible outcomes in a discrete probability distribution.

> **Formal Definition (Shannon Entropy):** Let $S$ be a set of training examples, and let $\mathcal{Y} = \{c_1, c_2, \dots, c_K\}$ be the set of $K$ mutually exclusive target classes. Let $p_i$ denote the empirical probability of class $c_i$ in $S$:
> $$p_i = \frac{| \{ (\mathbf{x}, y) \in S \mid y = c_i \} |}{|S|}$$
> The Shannon Entropy $H(S)$ is defined as:
> $$H(S) = \sum_{i=1}^K p_i \cdot I(p_i) = -\sum_{i=1}^K p_i \log_2(p_i)$$
> *Axiomatic Convention:* If $p_i = 0$, we define $0 \log_2(0) = \lim_{p \to 0^+} p \log_2(p) = 0$.

## Behavioral Extremes: Homogeneity vs. Maximum Uncertainty
Consider a binary classification problem ($K = 2$) where the target label is either Positive ($+$) or Negative ($-$). Let $p = p_+$ be the proportion of positive examples. Then $p_- = 1 - p$. The binary entropy function is:
$$H(p) = -p \log_2(p) - (1 - p) \log_2(1 - p)$$

```
Entropy H(p) in Bits
   1.0 ^                     * * * (Maximum uncertainty: p = 0.5, H = 1.0)
       |                 * * * *
   0.8 |               * *
       |             * *
   0.6 |           * *
       |          * *
   0.4 |         * *
       |        * *
   0.2 |       * *
       |      * *
   0.0 +------*---------------------------------*------> Proportion of Positive Instances (p)
      0.0   0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9   1.0
   (Pure -)                                                   (Pure +)
```

1. **Perfect Homogeneity / Minimum Uncertainty ($p = 1$ or $p = 0$):**
   $$H(S) = -1 \log_2(1) - 0 \log_2(0) = 0 - 0 = 0 \text{ bits}$$
   When every instance in the node belongs to the same class, entropy drops to zero. No additional information is needed to describe the node.
2. **Maximum Disorder / Maximum Uncertainty ($p = 0.5$):**
   $$H(S) = -0.5 \log_2(0.5) - 0.5 \log_2(0.5) = -0.5(-1) - 0.5(-1) = 1.0 \text{ bit}$$
   When the classes are evenly split, uncertainty is maximized. Predicting the class of an unobserved point is equivalent to a fair coin toss.
3. **Multi-Class Upper Bound:**
   For a general $K$-class distribution, entropy is maximized when the distribution is uniform: $p_i = \frac{1}{K}$ for all $i$:
   $$H_{\max} = -\sum_{i=1}^K \frac{1}{K} \log_2\left(\frac{1}{K}\right) = -\log_2\left(\frac{1}{K}\right) = \log_2(K)$$
   For an 8-class problem, maximum entropy is $\log_2(8) = 3$ bits.

## Base of the Logarithm and Units of Information
While base $2$ is standard in machine learning and computer science (measuring information in **bits** or **shannons**), other bases can be used:
- Base $e$ ($\ln$): Measures information in **nats** (commonly used when differentiating cost functions in neural network cross-entropy).
- Base $10$ ($\log_{10}$): Measures information in **Hartleys** or **bans**.

To change bases, use the change-of-base identity:
$$\log_2(x) = \frac{\ln(x)}{\ln(2)} \approx \frac{\ln(x)}{0.693147}$$

---

# 3. The Criterion of Purity: Information Gain

## Conditional Entropy of a Split
When a parent dataset $S$ is partitioned using an attribute $A$, the data is divided into smaller subsets. If attribute $A$ has $V$ distinct categorical values $\{v_1, v_2, \dots, v_V\}$, the split divides $S$ into $V$ subsets:
$$S_v = \{ (\mathbf{x}, y) \in S \mid x_A = v \}$$
where $S = \bigcup_{v \in \text{Values}(A)} S_v$, and $S_u \cap S_v = \emptyset$ for $u \neq v$.

Each resulting subset $S_v$ has its own internal disorder, measured by its entropy $H(S_v)$. To evaluate the overall quality of the split, we calculate the **Conditional Entropy** (or weighted residual entropy):

> **Definition (Conditional Entropy of a Partition):**
> $$H(S \mid A) = \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v)$$
> This represents the expected remaining uncertainty in the dataset after conditioning on attribute $A$.

## Formal Derivation of Information Gain
**Information Gain (IG)** measures the reduction in uncertainty achieved by partitioning the dataset according to attribute $A$.

> **Formal Definition (Information Gain):**
> $$IG(S, A) = H(S) - H(S \mid A) = H(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v)$$
> - $H(S)$ is the **prior entropy** of the node before splitting.
> - $H(S \mid A)$ is the **expected posterior entropy** after splitting along $A$.

In the language of probability theory, Information Gain is equivalent to the **Mutual Information** $I(Y; X_A)$ between the class label $Y$ and feature $X_A$:
$$I(Y; X_A) = H(Y) - H(Y \mid X_A)$$
Because conditioning cannot increase expected entropy ($H(Y \mid X_A) \le H(Y)$), Information Gain is always non-negative:
$$IG(S, A) \ge 0$$
$IG(S, A) = 0$ if and only if the class label distribution inside every partition $S_v$ is identical to the prior class distribution in the parent node $S$.

## The High-Cardinality Multi-Valued Attribute Pathological Bias
Standard Information Gain has a known pathological weakness: **it favors attributes with a large number of distinct values**.

### The Unique Identifier Failure Mode
Suppose a patient dataset includes a unique identification attribute: `Patient_ID` (e.g., $1, 2, 3, \dots, N$).
- If the tree splits on `Patient_ID`, it creates $N$ distinct branches, with each branch containing exactly one instance ($|S_v| = 1$).
- Because each child node contains only one sample, it is perfectly pure:
  $$H(S_v) = 0 \quad \text{for all } v$$
- The conditional entropy collapses to zero:
  $$H(S \mid \text{Patient\_ID}) = \sum_{v=1}^N \frac{1}{N} (0) = 0$$
- The resulting Information Gain is maximal:
  $$IG(S, \text{Patient\_ID}) = H(S) - 0 = H(S)$$

The algorithm selects `Patient_ID` as the root split because it maximizes Information Gain. However, this creates a shallow, broad tree with no generalization ability. It memorizes the training data perfectly, resulting in 100% training accuracy but near-zero test accuracy.

### The Remedy: Gain Ratio (C4.5)
To address this bias, Ross Quinlan introduced the **Gain Ratio** in the C4.5 algorithm. It penalizes attributes with high cardinality by dividing Information Gain by the **Split Information** (the intrinsic entropy of the partition itself):

$$\text{SplitInfo}_A(S) = -\sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} \log_2\left(\frac{|S_v|}{|S|}\right)$$

$$\text{GainRatio}(S, A) = \frac{IG(S, A)}{\text{SplitInfo}_A(S)}$$

For `Patient_ID`, $\text{SplitInfo} = \log_2(N)$, which heavily penalizes the metric and prevents the tree from selecting it.

---

# 4. Alternative Impurity Metrics: The Gini Index

## Statistical Derivation from Misclassification Probability
The **Gini Impurity** is an alternative metric used in the **CART (Classification and Regression Trees)** algorithm, developed by Leo Breiman et al. (1984).

Instead of using information theory, Gini impurity is derived from a simple probabilistic thought experiment:
1. Suppose we draw an item at random from node $S$.
2. We then assign it a class label randomly, drawn according to the class probability distribution of that same node.
3. **What is the probability that this randomly labeled item will be misclassified?**

Let $p_i$ be the true probability that an item belongs to class $c_i$.  
The probability that we randomly assign it to class $c_k$ (where $k \neq i$) is $p_k$.  
The total probability of misclassifying an item across all classes is:

$$G(S) = \sum_{i=1}^K P(\text{Item is Class } c_i) \cdot P(\text{Assigned Label } \neq c_i)$$
$$G(S) = \sum_{i=1}^K p_i \left(\sum_{k \neq i} p_k\right) = \sum_{i=1}^K p_i (1 - p_i)$$
$$G(S) = \sum_{i=1}^K (p_i - p_i^2) = \sum_{i=1}^K p_i - \sum_{i=1}^K p_i^2$$

Since probabilities sum to one ($\sum_{i=1}^K p_i = 1$):
$$G(S) = 1 - \sum_{i=1}^K p_i^2$$

## Gini Impurity of a Single Node
> **Formal Definition (Gini Impurity):** For a dataset $S$ containing instances distributed across $K$ classes with probabilities $\{p_1, p_2, \dots, p_K\}$:
> $$G(S) = 1 - \sum_{i=1}^K p_i^2$$

- **Pure Node:** If all instances belong to a single class ($p_1 = 1$, all other $p_i = 0$):
  $$G(S) = 1 - (1^2 + 0 + \dots + 0) = 0$$
- **Maximum Impurity (Binary Case, $K = 2$):** When $p_1 = p_2 = 0.5$:
  $$G(S) = 1 - (0.5^2 + 0.5^2) = 1 - (0.25 + 0.25) = 0.50$$
- **Maximum Impurity (Multi-Class Case):** Under a uniform distribution ($p_i = \frac{1}{K}$):
  $$G_{\max} = 1 - \sum_{i=1}^K \left(\frac{1}{K}\right)^2 = 1 - K \left(\frac{1}{K^2}\right) = 1 - \frac{1}{K} = \frac{K - 1}{K}$$
  As $K \to \infty$, $G_{\max} \to 1.0$.

## Gini Impurity of a Split (Weighted Gini)
When an attribute $A$ partitions dataset $S$ into subsets $\{S_v\}_{v=1}^V$, the impurity of the split is the weighted sum of the child impurities:

$$G(S \mid A) = \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} G(S_v)$$

The best split is the one that minimizes $G(S \mid A)$, or equivalently, maximizes the Gini reduction:
$$\Delta G(S, A) = G(S) - G(S \mid A)$$

## Entropy vs. Gini: Analytical & Computational Comparison

```
Impurity
  ^
1.0 |                   - - - Shannon Entropy: H(p) / 2 (Scaled by 0.5 for visual comparison)
    |                  /     \
0.8 |                 /       \
    |                /         \
0.6 |               /           \
    |              /             \
0.4 |             * * * * * * * * * Gini Impurity: G(p) = 2p(1 - p)
    |            /                 \
0.2 |           /                   \
    |          /                     \
0.0 +---------+-----------+-----------+---------> Class Probability p
             0.0         0.5         1.0
```

To compare their shapes directly, we can scale binary entropy by $0.5$. Notice that both curves are concave and share the same roots ($p=0, p=1$) and peak ($p=0.5$). 

Using the Taylor expansion of $\ln(x)$ around $x=1$:
$$\ln(p_i) = (p_i - 1) - \frac{(p_i - 1)^2}{2} + \dots$$
Approximating to the first order gives $\ln(p_i) \approx p_i - 1$. Substituting this into Shannon Entropy:
$$H_{\text{nat}}(S) = -\sum p_i \ln(p_i) \approx -\sum p_i (p_i - 1) = \sum (p_i - p_i^2) = 1 - \sum p_i^2 = G(S)$$

**Gini Impurity is a first-order Taylor approximation of Shannon Entropy.**

| Evaluation Metric | Shannon Entropy ($H(S)$) | Gini Impurity ($G(S)$) |
| :--- | :--- | :--- |
| **Mathematical Formula** | $-\sum_{i=1}^K p_i \log_2(p_i)$ | $1 - \sum_{i=1}^K p_i^2$ |
| **Origin Algorithm** | ID3, C4.5 | CART |
| **Scale Limits (Binary)** | Minimum: $0.0$, Maximum: $1.0$ | Minimum: $0.0$, Maximum: $0.5$ |
| **Computational Complexity** | **Heavy:** Requires computing logarithms for every branch ($\log_2$). | **Light:** Requires only basic multiplication and subtraction (squaring). |
| **Sensitivity to Outliers** | Slightly favors balanced class splits due to logarithmic scaling. | Tends to isolate the most frequent class into its own pure node. |
| **Empirical Disparity** | Splits agree in over **98%** of real-world scenarios. Model performance is rarely different. |

---

# 5. Algorithmic Mechanics of the ID3 Algorithm

## The Top-Down Induction of Decision Trees (TDIDT) Framework
The **ID3 (Iterative Dichotomiser 3)** algorithm, introduced by J. Ross Quinlan in 1986, is the standard baseline for recursive decision tree induction. 

ID3 uses a **greedy, top-down search**:
- **Greedy Strategy:** At each step, it selects the locally optimal split (maximizing Information Gain) without backtracking.
- **Top-Down Induction:** It starts at the root node and recursively splits the training set into smaller subsets.

```
                         [ Dataset S at Node ]
                                   |
                     Is S Pure or Stop Condition Met?
                                  / \
                            YES  /   \  NO
                                /     \
            [ Create Leaf Node ]       [ Evaluate All Unused Attributes ]
            (Assign Majority Label)    [ Compute IG(S, A) for Each A     ]
                                                        |
                                            [ Select A* with Max IG ]
                                                        |
                                           Create Child Branches for
                                            Each Value v of A*
                                                        |
                                          Recursively Call ID3(S_v)
```

## Complete Algorithmic Pseudocode

```python
def ID3(Examples, TargetAttribute, Attributes):
    """
    Induces a decision tree using recursive top-down selection via Information Gain.

    Parameters:
    - Examples: The subset of training instances reaching this node.
    - TargetAttribute: The categorical label to be predicted.
    - Attributes: The set of categorical candidate features available to split on.

    Returns:
    - A Decision Tree Node (either a Decision Fork or a Terminal Leaf).
    """
    Root = NewNode()

    # --- BASE CASE 1: All examples share the exact same class label ---
    if all(x[TargetAttribute] == Examples[0][TargetAttribute] for x in Examples):
        Root.label = Examples[0][TargetAttribute]
        return Root

    # --- BASE CASE 2: The attribute set is completely exhausted ---
    if len(Attributes) == 0:
        Root.label = MostFrequentTargetValue(Examples, TargetAttribute)
        return Root

    # --- INDUCTIVE STEP: Select the Best Splitting Attribute ---
    CurrentEntropy = ComputeEntropy(Examples, TargetAttribute)
    BestAttribute = None
    MaxGain = -1.0

    for A in Attributes:
        # Calculate conditional entropy across all values of feature A
        SplittedSubsets = Partition(Examples, A)
        ConditionalEntropy = 0.0
        
        for Subset in SplittedSubsets.values():
            Weight = len(Subset) / len(Examples)
            ConditionalEntropy += Weight * ComputeEntropy(Subset, TargetAttribute)
        
        Gain = CurrentEntropy - ConditionalEntropy
        
        if Gain > MaxGain:
            MaxGain = Gain
            BestAttribute = A

    Root.decision_attribute = BestAttribute

    # --- RECURSIVE SUBTREE CREATION ---
    for v in DomainValues(BestAttribute):
        # Subset of examples where BestAttribute equals v
        Subset_v = [x for x in Examples if x[BestAttribute] == v]

        # --- BASE CASE 3: No examples have this specific attribute value ---
        if len(Subset_v) == 0:
            ChildLeaf = NewNode()
            ChildLeaf.label = MostFrequentTargetValue(Examples, TargetAttribute)
            Root.AddChild(branch_value=v, target_node=ChildLeaf)
        else:
            RemainingAttributes = [attr for attr in Attributes if attr != BestAttribute]
            SubTree = ID3(Subset_v, TargetAttribute, RemainingAttributes)
            Root.AddChild(branch_value=v, target_node=SubTree)

    return Root
```

## Recursive Base Cases and Termination Criteria
The recursive algorithm stops based on three explicit conditions:

1. **Base Case 1: Purity Achieved ($H(S) = 0$).** Every training sample inside subset $S$ belongs to the same class. A leaf node is created and labeled with that class.
2. **Base Case 2: Feature Space Exhaustion ($\text{Attributes} = \emptyset$).** All available attributes have been used higher up in the branch, but the remaining examples still have conflicting labels (due to label noise or overlapping features). A leaf node is created and assigned the **majority class** among the examples at that node.
3. **Base Case 3: Empty Partitions ($|S_v| = 0$).** A chosen attribute has a possible value $v$ that appears in the general domain, but no training examples in $S$ take that value. A leaf node is created and assigned the **majority class of the parent node $S$**.

## Inductive Bias in Decision Tree Search
Because a decision tree searches an hypothesis space $\mathcal{H}$ containing all possible trees, its **inductive bias** determines which solutions it prefers:

1. **Preference for Shorter Trees (Occam's Razor):** By choosing the attribute with the highest Information Gain at each step, ID3 tries to place the most informative attributes near the root, encouraging the creation of shorter trees.
2. **Preference for High Information Gain Near the Root:** Unlike algorithms with a restricted hypothesis space (like Perceptrons, which can only represent linear functions), ID3 has an expressive, unrestricted hypothesis space (it can represent any discrete function). Its bias is primarily a **search bias (preference bias)** rather than a **language bias (restriction bias)**.
3. **Susceptibility to Local Optima:** Because ID3 is greedy and never backtracks, it can miss simpler trees that require a weaker initial split to unlock a much better subsequent split (e.g., in XOR-like data).

---

# 6. Structural Vulnerabilities and Remedies

## Overfitting and the Infinite Hypothesis Space Trap
An unconstrained decision tree will continue splitting until every leaf is pure ($H(S) = 0$), memorizing any noise or sample-specific patterns in the training data.

```
Accuracy
  ^
  |       Training Accuracy (Continuously approaches 100%)
  |      .--------------------------------------------------
  |     /
  |    /      Validation / Test Accuracy
  |   /      . - - - - .  (Peak Generalization Point)
  |  /      /           \
  | /      /             \  Generalization Breakdown
  |/      /               \   (Severe Overfitting)
  +------+-----------------\-----------------------------> Tree Depth / Node Count
         Low Complexity     Optimal Depth      Overparameterized
```

If an unconstrained tree is trained on a dataset with $N$ samples, it can grow until it has $N$ leaves, achieving 100% training accuracy while failing to generalize to new data.

## Pre-Pruning (Early Stopping) vs. Post-Pruning (Reduced Error Pruning)

### 1. Pre-Pruning (Early Stopping)
Pre-pruning halts tree construction during induction if a node fails to meet a predefined threshold.
- **Stopping Conditions:**
  - Stop if node depth reaches `max_depth`.
  - Stop if the number of samples in the node falls below `min_samples_split`.
  - Stop if the maximum Information Gain at the node is below a threshold: $\max_A IG(S, A) < \epsilon$.
- **Disadvantage:** Prone to **premature stopping**. A split with low Information Gain might unlock a split with high Information Gain immediately below it (the XOR problem).

### 2. Post-Pruning (Reduced-Error Pruning)
Post-pruning allows the tree to grow to its maximum possible depth (until all leaves are pure), and then simplifies it from the bottom up.
- **Procedure:**
  1. Split the data into a **Training Set** and an independent **Validation Set**.
  2. Grow a fully unconstrained tree $T$ using the training set.
  3. Evaluate each non-leaf node $n$: evaluate how validation accuracy changes if the subtree rooted at $n$ is collapsed into a single leaf node (labeled with the majority class of examples at $n$).
  4. If pruning the node does not decrease validation accuracy, prune the subtree.
  5. Repeat until no further pruning improves validation performance.

```
UNPRUNED FULL TREE (HIGH VARIANCE)            POST-PRUNED BALANCED TREE
             (Root)                                     (Root)
            /      \                                   /      \
          (N1)    (N2)                               (N1)    (N2)
         /    \   /   \                             /    \   /   \
       [+]   [-] (N3) [+]                         [+]   [-] [+]  [-]
                /    \                            (Collapses noisy sub-branches)
              [+]    [-]
```

## Handling Continuous-Valued Features via Dynamical Thresholding
While the original ID3 algorithm was restricted to discrete categorical attributes, Fayyad and Irani (1992) developed a dynamic thresholding approach (adopted in C4.5) to handle continuous variables.

### The Algorithm for Continuous Attributes:
1. Let $A$ be a continuous-valued numeric attribute. Extract all values of $A$ present in dataset $S$ and sort them in ascending order:
   $$\{a_1, a_2, a_3, \dots, a_m\} \quad \text{where } a_1 \le a_2 \le \dots \le a_m$$
2. Identify **candidate threshold cut-points** $c_i$ as the midpoints between adjacent, distinct values where the sorted class label changes:
   $$c_i = \frac{a_i + a_{i+1}}{2} \quad \text{for } y(a_i) \neq y(a_{i+1})$$
3. For each candidate threshold $c_i$, treat the feature as a temporary binary attribute:
   - Branch 1: $A \le c_i$
   - Branch 2: $A > c_i$
4. Compute the Information Gain $IG(S, A \le c_i)$ for every candidate cut-point.
5. Select the threshold $c^*$ that maximizes Information Gain:
   $$c^* = \arg\max_{c_i} IG(S, A \le c_i)$$

Unlike categorical attributes, a continuous feature can be reused multiple times along the same path in the tree with different thresholds.

## Handling Missing Attributes During Induction
In practical applications, some feature values might be missing (`NaN`). The C4.5 algorithm handles this by assigning fractional weights to instances:

1. **Calculating Information Gain with Missing Values:** If an attribute $A$ is missing in some examples, Information Gain is weighted by the proportion of known examples:
   $$IG(S, A) = F \times \left( H(S_{\text{known}}) - \sum_{v} \frac{|S_{v,\text{known}}|}{|S_{\text{known}}|} H(S_{v,\text{known}}) \right)$$
   where $F = \frac{|S_{\text{known}}|}{|S|}$ is the fraction of examples where $A$ is observed.
2. **Assigning Instances to Branches:** If an example reaches a test node on attribute $A$ and its value is missing, it is sent down **all branches**. However, its sample weight $w$ is scaled down for each branch according to that branch's frequency in the training data:
   $$w_v = w \times \frac{|S_v|}{|S|}$$
   These fractional weights are used to compute probabilities at the leaves.

---

# 7. Comprehensive Step-by-Step Numerical Walkthroughs

## Worked Problem 1: Manual Calculation of Entropy and Multi-Class Information Gain

### Problem Statement
A medical training node $S$ contains $N = 20$ patient records classified into three categories: **Healthy ($C_1$)**, **Mildly Ill ($C_2$)**, and **Severely Ill ($C_3$)**.
The distribution of classes is:
- $|C_1| = 10$ examples
- $|C_2| = 6$ examples
- $|C_3| = 4$ examples

A clinical test attribute $T$ with three outcomes $\{t_1, t_2, t_3\}$ splits the dataset as follows:
- **Branch $T = t_1$ ($|S_1| = 8$):** $C_1 = 6, \quad C_2 = 2, \quad C_3 = 0$
- **Branch $T = t_2$ ($|S_2| = 6$):** $C_1 = 1, \quad C_2 = 3, \quad C_3 = 2$
- **Branch $T = t_3$ ($|S_3| = 6$):** $C_1 = 3, \quad C_2 = 1, \quad C_3 = 2$

Calculate:
1. The prior Shannon Entropy of the parent node $H(S)$ in bits.
2. The entropy of each child branch: $H(S_1), H(S_2), H(S_3)$.
3. The conditional entropy of the split $H(S \mid T)$.
4. The Information Gain $IG(S, T)$.

---

### Step-by-Step Solution

#### Step 1: Compute Prior Entropy of the Parent Node $H(S)$
The total count is $|S| = 20$. The empirical class probabilities are:
- $p_1 = P(C_1) = \frac{10}{20} = 0.50$
- $p_2 = P(C_2) = \frac{6}{20} = 0.30$
- $p_3 = P(C_3) = \frac{4}{20} = 0.20$

Using the Shannon Entropy formula:
$$H(S) = - \left[ p_1 \log_2(p_1) + p_2 \log_2(p_2) + p_3 \log_2(p_3) \right]$$

Compute each term:
- $p_1 \log_2(p_1) = 0.50 \times \log_2(0.50) = 0.50 \times (-1.0000) = -0.5000$
- $p_2 \log_2(p_2) = 0.30 \times \log_2(0.30) = 0.30 \times (-1.7370) = -0.5211$
- $p_3 \log_2(p_3) = 0.20 \times \log_2(0.20) = 0.20 \times (-2.3219) = -0.4644$

Sum the negative terms:
$$H(S) = - \left[ -0.5000 - 0.5211 - 0.4644 \right] = -[-1.4855] = \mathbf{1.4855} \text{ bits}$$

---

#### Step 2: Compute the Entropies of the Child Branches

**Branch 1 ($T = t_1$):**
- Total samples: $|S_1| = 8$
- $p_{1,1} = \frac{6}{8} = 0.75$
- $p_{1,2} = \frac{2}{8} = 0.25$
- $p_{1,3} = \frac{0}{8} = 0.0$ (Convention: $0 \log_2(0) = 0$)

$$H(S_1) = -\left[ 0.75 \log_2(0.75) + 0.25 \log_2(0.25) + 0 \right]$$
- $0.75 \log_2(0.75) = 0.75 \times (-0.4150) = -0.3113$
- $0.25 \log_2(0.25) = 0.25 \times (-2.0000) = -0.5000$

$$H(S_1) = -[-0.3113 - 0.5000] = \mathbf{0.8113} \text{ bits}$$

**Branch 2 ($T = t_2$):**
- Total samples: $|S_2| = 6$
- $p_{2,1} = \frac{1}{6} \approx 0.1667$
- $p_{2,2} = \frac{3}{6} = 0.50$
- $p_{2,3} = \frac{2}{6} \approx 0.3333$

$$H(S_2) = -\left[ \frac{1}{6}\log_2\left(\frac{1}{6}\right) + \frac{1}{2}\log_2\left(\frac{1}{2}\right) + \frac{1}{3}\log_2\left(\frac{1}{3}\right) \right]$$
- $\frac{1}{6} \log_2\left(\frac{1}{6}\right) = 0.1667 \times (-2.5850) = -0.4308$
- $\frac{1}{2} \log_2\left(\frac{1}{2}\right) = 0.5000 \times (-1.0000) = -0.5000$
- $\frac{1}{3} \log_2\left(\frac{1}{3}\right) = 0.3333 \times (-1.5850) = -0.5283$

$$H(S_2) = -[-0.4308 - 0.5000 - 0.5283] = -[-1.4591] = \mathbf{1.4591} \text{ bits}$$

**Branch 3 ($T = t_3$):**
- Total samples: $|S_3| = 6$
- $p_{3,1} = \frac{3}{6} = 0.50$
- $p_{3,2} = \frac{1}{6} \approx 0.1667$
- $p_{3,3} = \frac{2}{6} \approx 0.3333$

Because this distribution is a permutation of Branch 2, its entropy is identical:
$$H(S_3) = \mathbf{1.4591} \text{ bits}$$

---

#### Step 3: Compute Conditional Entropy $H(S \mid T)$
Take the weighted average of the child entropies:
$$H(S \mid T) = \frac{|S_1|}{|S|} H(S_1) + \frac{|S_2|}{|S|} H(S_2) + \frac{|S_3|}{|S|} H(S_3)$$
$$H(S \mid T) = \left(\frac{8}{20}\right)(0.8113) + \left(\frac{6}{20}\right)(1.4591) + \left(\frac{6}{20}\right)(1.4591)$$
$$H(S \mid T) = (0.40)(0.8113) + (0.30)(1.4591) + (0.30)(1.4591)$$
$$H(S \mid T) = 0.32452 + 0.43773 + 0.43773 = \mathbf{1.19998} \approx \mathbf{1.2000} \text{ bits}$$

---

#### Step 4: Compute Information Gain $IG(S, T)$
$$IG(S, T) = H(S) - H(S \mid T)$$
$$IG(S, T) = 1.4855 - 1.2000 = \mathbf{0.2855} \text{ bits}$$

---

## Worked Problem 2: Full Iteration of ID3 Tree Building (Root Node Selection)

### Problem Statement
A banking institution uses four categorical attributes to evaluate loan default risk:
- **Credit_History ($C$):** $\{\text{Good}, \text{Bad}\}$
- **Employed ($E$):** $\{\text{Yes}, \text{No}\}$
- **Has_Collateral ($K$):** $\{\text{Yes}, \text{No}\}$

The goal is to predict the target attribute **Default ($Y$)** $\in \{\text{Yes}, \text{No}\}$ based on the following $N = 10$ historical applications:

| ID | Credit_History ($C$) | Employed ($E$) | Has_Collateral ($K$) | Default ($Y$) |
| :---: | :---: | :---: | :---: | :---: |
| 1 | Good | Yes | Yes | **No** |
| 2 | Good | Yes | No | **No** |
| 3 | Good | No | Yes | **No** |
| 4 | Good | No | No | **Yes** |
| 5 | Bad | Yes | Yes | **No** |
| 6 | Bad | Yes | No | **Yes** |
| 7 | Bad | No | Yes | **Yes** |
| 8 | Bad | No | No | **Yes** |
| 9 | Good | Yes | Yes | **No** |
| 10 | Bad | Yes | Yes | **No** |

Determine the optimal attribute for the **root node split** using the ID3 algorithm with Information Gain.

---

### Step-by-Step Solution

#### Step 1: Base Entropy of the Entire Dataset $H(S)$
Total applications $|S| = 10$. Count target outcomes:
- $\text{Default} = \text{No}$: $6$ instances (IDs: 1, 2, 3, 5, 9, 10)
- $\text{Default} = \text{Yes}$: $4$ instances (IDs: 4, 6, 7, 8)

Probabilities:
$$P(\text{No}) = \frac{6}{10} = 0.60, \quad P(\text{Yes}) = \frac{4}{10} = 0.40$$

$$H(S) = - \left[ 0.60 \log_2(0.60) + 0.40 \log_2(0.40) \right]$$
$$H(S) = - \left[ 0.60(-0.7370) + 0.40(-1.3219) \right] = - \left[ -0.4422 - 0.5288 \right] = \mathbf{0.9710} \text{ bits}$$

---

#### Step 2: Evaluate Attribute 1 — Credit_History ($C$)
Values: $\{\text{Good}, \text{Bad}\}$.

**Subset 1: $C = \text{Good}$**
- Matching records: IDs 1, 2, 3, 4, 9 $\implies |S_{\text{Good}}| = 5$.
- Target classes:
  - $\text{No} = 4$ (IDs: 1, 2, 3, 9)
  - $\text{Yes} = 1$ (ID: 4)
- Probabilities: $p_{\text{No}} = \frac{4}{5} = 0.80, \quad p_{\text{Yes}} = \frac{1}{5} = 0.20$
$$H(S_{\text{Good}}) = -[0.80 \log_2(0.80) + 0.20 \log_2(0.20)] = -[0.80(-0.3219) + 0.20(-2.3219)] = \mathbf{0.7219} \text{ bits}$$

**Subset 2: $C = \text{Bad}$**
- Matching records: IDs 5, 6, 7, 8, 10 $\implies |S_{\text{Bad}}| = 5$.
- Target classes:
  - $\text{No} = 2$ (IDs: 5, 10)
  - $\text{Yes} = 3$ (IDs: 6, 7, 8)
- Probabilities: $p_{\text{No}} = \frac{2}{5} = 0.40, \quad p_{\text{Yes}} = \frac{3}{5} = 0.60$
$$H(S_{\text{Bad}}) = -[0.40 \log_2(0.40) + 0.60 \log_2(0.60)] = \mathbf{0.9710} \text{ bits}$$

**Expected Conditional Entropy $H(S \mid C)$:**
$$H(S \mid C) = \frac{5}{10} H(S_{\text{Good}}) + \frac{5}{10} H(S_{\text{Bad}}) = 0.5(0.7219) + 0.5(0.9710) = \mathbf{0.8465} \text{ bits}$$

**Information Gain for Credit_History:**
$$IG(S, C) = H(S) - H(S \mid C) = 0.9710 - 0.8465 = \mathbf{0.1245} \text{ bits}$$

---

#### Step 3: Evaluate Attribute 2 — Employed ($E$)
Values: $\{\text{Yes}, \text{No}\}$.

**Subset 1: $E = \text{Yes}$**
- Matching records: IDs 1, 2, 5, 6, 9, 10 $\implies |S_{\text{Yes}}| = 6$.
- Target classes:
  - $\text{No} = 5$ (IDs: 1, 2, 5, 9, 10)
  - $\text{Yes} = 1$ (ID: 6)
- Probabilities: $p_{\text{No}} = \frac{5}{6} \approx 0.8333, \quad p_{\text{Yes}} = \frac{1}{6} \approx 0.1667$
$$H(S_{E=\text{Yes}}) = - \left[ \frac{5}{6}\log_2\left(\frac{5}{6}\right) + \frac{1}{6}\log_2\left(\frac{1}{6}\right) \right]$$
$$H(S_{E=\text{Yes}}) = - [0.8333(-0.2630) + 0.1667(-2.5850)] = -[-0.2192 - 0.4309] = \mathbf{0.6501} \text{ bits}$$

**Subset 2: $E = \text{No}$**
- Matching records: IDs 3, 4, 7, 8 $\implies |S_{\text{No}}| = 4$.
- Target classes:
  - $\text{No} = 1$ (ID: 3)
  - $\text{Yes} = 3$ (IDs: 4, 7, 8)
- Probabilities: $p_{\text{No}} = \frac{1}{4} = 0.25, \quad p_{\text{Yes}} = \frac{3}{4} = 0.75$
$$H(S_{E=\text{No}}) = - [0.25(-2.0000) + 0.75(-0.4150)] = -[-0.5000 - 0.3113] = \mathbf{0.8113} \text{ bits}$$

**Expected Conditional Entropy $H(S \mid E)$:**
$$H(S \mid E) = \frac{6}{10}(0.6501) + \frac{4}{10}(0.8113) = 0.39006 + 0.32452 = \mathbf{0.7146} \text{ bits}$$

**Information Gain for Employed:**
$$IG(S, E) = H(S) - H(S \mid E) = 0.9710 - 0.7146 = \mathbf{0.2564} \text{ bits}$$

---

#### Step 4: Evaluate Attribute 3 — Has_Collateral ($K$)
Values: $\{\text{Yes}, \text{No}\}$.

**Subset 1: $K = \text{Yes}$**
- Matching records: IDs 1, 3, 5, 7, 9, 10 $\implies |S_{K=\text{Yes}}| = 6$.
- Target classes:
  - $\text{No} = 5$ (IDs: 1, 3, 5, 9, 10)
  - $\text{Yes} = 1$ (ID: 7)
- Probabilities: $p_{\text{No}} = \frac{5}{6}, \quad p_{\text{Yes}} = \frac{1}{6}$
$$H(S_{K=\text{Yes}}) = \mathbf{0.6501} \text{ bits}$$

**Subset 2: $K = \text{No}$**
- Matching records: IDs 2, 4, 6, 8 $\implies |S_{K=\text{No}}| = 4$.
- Target classes:
  - $\text{No} = 1$ (ID: 2)
  - $\text{Yes} = 3$ (IDs: 4, 6, 8)
- Probabilities: $p_{\text{No}} = \frac{1}{4}, \quad p_{\text{Yes}} = \frac{3}{4}$
$$H(S_{K=\text{No}}) = \mathbf{0.8113} \text{ bits}$$

**Expected Conditional Entropy $H(S \mid K)$:**
$$H(S \mid K) = \frac{6}{10}(0.6501) + \frac{4}{10}(0.8113) = \mathbf{0.7146} \text{ bits}$$

**Information Gain for Has_Collateral:**
$$IG(S, K) = H(S) - H(S \mid K) = 0.9710 - 0.7146 = \mathbf{0.2564} \text{ bits}$$

---

#### Step 5: Root Node Selection

| Candidate Attribute | Expected Conditional Entropy $H(S \mid A)$ | Information Gain $IG(S, A)$ |
| :--- | :---: | :---: |
| **Credit_History ($C$)** | $0.8465 \text{ bits}$ | $0.1245 \text{ bits}$ |
| **Employed ($E$)** | $0.7146 \text{ bits}$ | **$0.2564 \text{ bits}$** |
| **Has_Collateral ($K$)** | $0.7146 \text{ bits}$ | **$0.2564 \text{ bits}$** |

Both **Employed** and **Has_Collateral** are tied with the highest Information Gain ($0.2564\text{ bits}$). The ID3 algorithm can choose either attribute to form the root node. Choosing **Employed** creates two branches:
- **Branch $E = \text{Yes}$ ($6$ examples):** 5 No Default, 1 Default. (ID3 will recurse on this subset using $\{C, K\}$).
- **Branch $E = \text{No}$ ($4$ examples):** 1 No Default, 3 Default. (ID3 will recurse on this subset using $\{C, K\}$).

---

## Worked Problem 3: Gini Impurity vs. Information Gain Conflict Analysis

### Problem Statement
A binary classification dataset ($N = 100$) has a parent distribution of $50$ Positive and $50$ Negative samples. Two candidate splits, $A$ and $B$, are proposed:

- **Split $A$ creates two branches:**
  - Branch $A_1$: $40$ Positive, $10$ Negative ($|A_1| = 50$)
  - Branch $A_2$: $10$ Positive, $40$ Negative ($|A_2| = 50$)
- **Split $B$ creates two branches:**
  - Branch $B_1$: $30$ Positive, $0$ Negative ($|B_1| = 30$)
  - Branch $B_2$: $20$ Positive, $50$ Negative ($|B_2| = 70$)

1. Compute the **Information Gain** for both splits. Which split does Entropy prefer?
2. Compute the **Gini Impurity Reduction** for both splits. Which split does Gini prefer?
3. Explain any differences in preference between the two metrics.

---

### Step-by-Step Solution

#### Parent Metrics:
Total $N = 100$, with $p_+ = 0.50$ and $p_- = 0.50$:
$$H(S) = -0.5 \log_2(0.5) - 0.5 \log_2(0.5) = 1.0000 \text{ bit}$$
$$G(S) = 1 - (0.5^2 + 0.5^2) = 1 - (0.25 + 0.25) = 0.5000$$

---

#### Part 1: Information Gain Evaluation

**Evaluating Split $A$:**
- Branch $A_1$ ($N = 50$): $p_+ = \frac{40}{50} = 0.80, \quad p_- = \frac{10}{50} = 0.20$
  $$H(A_1) = -[0.8 \log_2(0.8) + 0.2 \log_2(0.2)] = 0.7219 \text{ bits}$$
- Branch $A_2$ ($N = 50$): $p_+ = \frac{10}{50} = 0.20, \quad p_- = \frac{40}{50} = 0.80$
  $$H(A_2) = 0.7219 \text{ bits}$$
- Weighted Entropy:
  $$H(S \mid A) = \frac{50}{100}(0.7219) + \frac{50}{100}(0.7219) = \mathbf{0.7219} \text{ bits}$$
- Information Gain:
  $$IG(S, A) = 1.0000 - 0.7219 = \mathbf{0.2781} \text{ bits}$$

**Evaluating Split $B$:**
- Branch $B_1$ ($N = 30$): $p_+ = \frac{30}{30} = 1.0, \quad p_- = 0$
  $$H(B_1) = 0.0000 \text{ bits} \quad (\text{Pure Node})$$
- Branch $B_2$ ($N = 70$): $p_+ = \frac{20}{70} \approx 0.2857, \quad p_- = \frac{50}{70} \approx 0.7143$
  $$H(B_2) = -[0.2857 \log_2(0.2857) + 0.7143 \log_2(0.7143)]$$
  $$H(B_2) = -[0.2857(-1.8074) + 0.7143(-0.4854)] = -[-0.5164 - 0.3467] = \mathbf{0.8631} \text{ bits}$$
- Weighted Entropy:
  $$H(S \mid B) = \frac{30}{100}(0.0) + \frac{70}{100}(0.8631) = 0 + 0.6042 = \mathbf{0.6042} \text{ bits}$$
- Information Gain:
  $$IG(S, B) = 1.0000 - 0.6042 = \mathbf{0.3958} \text{ bits}$$

**Comparison:** $IG(S, B) = 0.3958 > IG(S, A) = 0.2781$.  
**Entropy prefers Split $B$.**

---

#### Part 2: Gini Impurity Reduction Evaluation

**Evaluating Split $A$:**
- Branch $A_1$: $p_+ = 0.80, \quad p_- = 0.20$
  $$G(A_1) = 1 - (0.80^2 + 0.20^2) = 1 - (0.64 + 0.04) = 1 - 0.68 = \mathbf{0.3200}$$
- Branch $A_2$: $p_+ = 0.20, \quad p_- = 0.80$
  $$G(A_2) = 1 - (0.04 + 0.64) = \mathbf{0.3200}$$
- Weighted Gini:
  $$G(S \mid A) = \frac{50}{100}(0.3200) + \frac{50}{100}(0.3200) = \mathbf{0.3200}$$
- Gini Reduction:
  $$\Delta G(S, A) = 0.5000 - 0.3200 = \mathbf{0.1800}$$

**Evaluating Split $B$:**
- Branch $B_1$: $p_+ = 1.0, \quad p_- = 0.0$
  $$G(B_1) = 1 - (1.0^2 + 0.0^2) = \mathbf{0.0000} \quad (\text{Pure Node})$$
- Branch $B_2$: $p_+ = \frac{2}{7}, \quad p_- = \frac{5}{7}$
  $$G(B_2) = 1 - \left[ \left(\frac{2}{7}\right)^2 + \left(\frac{5}{7}\right)^2 \right] = 1 - \left[ \frac{4}{49} + \frac{25}{49} \right] = 1 - \frac{29}{49} = \frac{20}{49} \approx \mathbf{0.4082}$$
- Weighted Gini:
  $$G(S \mid B) = \frac{30}{100}(0.0000) + \frac{70}{100}(0.4082) = 0 + 0.2857 = \mathbf{0.2857}$$
- Gini Reduction:
  $$\Delta G(S, B) = 0.5000 - 0.2857 = \mathbf{0.2143}$$

**Comparison:** $\Delta G(S, B) = 0.2143 > \Delta G(S, A) = 0.1800$.  
**Gini also prefers Split $B$.**

---

#### Part 3: Analytical Insight
Both metrics favor Split $B$ because it **isolates a perfectly pure node ($B_1$ with 30 samples)**. 
- In Split $A$, both child nodes show a modest improvement in purity ($0.5 \to 0.32$).
- In Split $B$, one child node achieves absolute purity ($0.5 \to 0.0$).
Because both Gini impurity and Shannon Entropy are strictly concave, both metrics strongly reward identifying pure subsets, even if the remaining partition stays relatively mixed.

---

## Worked Problem 4: Finding the Optimal Split Point for a Continuous Attribute

### Problem Statement
A classification dataset contains a continuous real-valued biological marker $X$ and a binary outcome label $Y \in \{+, -\}$:

```
Sample Index:   s1     s2     s3     s4     s5     s6     s7
Attribute X:   1.5    2.0    3.2    4.0    5.5    6.2    7.1
Class Label Y:  -      -      +      +      -      +      +
```

1. Identify all candidate threshold cut-points.
2. Calculate the Information Gain for each candidate cut-point.
3. Determine the optimal decision threshold $c^*$ for this continuous feature.

---

### Step-by-Step Solution

#### Step 1: Base Entropy of the Entire Dataset
Total instances $N = 7$:
- Positive Class ($+$): $4$ instances ($s_3, s_4, s_6, s_7$)
- Negative Class ($- $): $3$ instances ($s_1, s_2, s_5$)

Probabilities: $p_+ = \frac{4}{7} \approx 0.5714, \quad p_- = \frac{3}{7} \approx 0.4286$
$$H(S) = - \left[ \frac{4}{7} \log_2\left(\frac{4}{7}\right) + \frac{3}{7} \log_2\left(\frac{3}{7}\right) \right]$$
$$H(S) = - [0.5714(-0.8074) + 0.4286(-1.2224)] = - [-0.4613 - 0.5239] = \mathbf{0.9852} \text{ bits}$$

---

#### Step 2: Identify Candidate Split Thresholds
Sort the data by $X$ and observe where the class label changes:
1. $s_1 (1.5, -)$ to $s_2 (2.0, -)$: No class change.
2. $s_2 (2.0, -)$ to $s_3 (3.2, +)$: **Class change ($-$ to $+$).**
   $$c_1 = \frac{2.0 + 3.2}{2} = \mathbf{2.6}$$
3. $s_3 (3.2, +)$ to $s_4 (4.0, +)$: No class change.
4. $s_4 (4.0, +)$ to $s_5 (5.5, -)$: **Class change ($+$ to $-$).**
   $$c_2 = \frac{4.0 + 5.5}{2} = \mathbf{4.75}$$
5. $s_5 (5.5, -)$ to $s_6 (6.2, +)$: **Class change ($-$ to $+$).**
   $$c_3 = \frac{5.5 + 6.2}{2} = \mathbf{5.85}$$
6. $s_6 (6.2, +)$ to $s_7 (7.1, +)$: No class change.

There are three candidate cut-points: $\{2.6, 4.75, 5.85\}$.

---

#### Step 3: Evaluate Candidate Thresholds

##### Candidate Threshold $c_1 = 2.6$:
- **Left Branch ($X \le 2.6$):** Contains $\{s_1, s_2\}$.
  - Count: $N_L = 2$ ($0$ positive, $2$ negative) $\implies$ **Pure Node!**
  - $H(S_{L}) = \mathbf{0.0000} \text{ bits}$
- **Right Branch ($X > 2.6$):** Contains $\{s_3, s_4, s_5, s_6, s_7\}$.
  - Count: $N_R = 5$ ($4$ positive, $1$ negative)
  - $p_+ = \frac{4}{5} = 0.80, \quad p_- = \frac{1}{5} = 0.20$
  - $H(S_{R}) = -[0.8 \log_2(0.8) + 0.2 \log_2(0.2)] = \mathbf{0.7219} \text{ bits}$
- **Conditional Entropy:**
  $$H(S \mid X \le 2.6) = \frac{2}{7}(0.0000) + \frac{5}{7}(0.7219) = 0 + 0.5156 = \mathbf{0.5156} \text{ bits}$$
- **Information Gain:**
  $$IG(S, X \le 2.6) = 0.9852 - 0.5156 = \mathbf{0.4696} \text{ bits}$$

---

##### Candidate Threshold $c_2 = 4.75$:
- **Left Branch ($X \le 4.75$):** Contains $\{s_1, s_2, s_3, s_4\}$.
  - Count: $N_L = 4$ ($2$ positive, $2$ negative) $\implies$ **Maximal Impurity**
  - $p_+ = 0.50, \quad p_- = 0.50$
  - $H(S_{L}) = \mathbf{1.0000} \text{ bit}$
- **Right Branch ($X > 4.75$):** Contains $\{s_5, s_6, s_7\}$.
  - Count: $N_R = 3$ ($2$ positive, $1$ negative)
  - $p_+ = \frac{2}{3} \approx 0.6667, \quad p_- = \frac{1}{3} \approx 0.3333$
  - $H(S_{R}) = -[\frac{2}{3}\log_2(\frac{2}{3}) + \frac{1}{3}\log_2(\frac{1}{3})] = \mathbf{0.9183} \text{ bits}$
- **Conditional Entropy:**
  $$H(S \mid X \le 4.75) = \frac{4}{7}(1.0000) + \frac{3}{7}(0.9183) = 0.5714 + 0.3936 = \mathbf{0.9650} \text{ bits}$$
- **Information Gain:**
  $$IG(S, X \le 4.75) = 0.9852 - 0.9650 = \mathbf{0.0202} \text{ bits}$$

---

##### Candidate Threshold $c_3 = 5.85$:
- **Left Branch ($X \le 5.85$):** Contains $\{s_1, s_2, s_3, s_4, s_5\}$.
  - Count: $N_L = 5$ ($2$ positive, $3$ negative)
  - $p_+ = \frac{2}{5} = 0.40, \quad p_- = \frac{3}{5} = 0.60$
  - $H(S_{L}) = -[0.4 \log_2(0.4) + 0.6 \log_2(0.6)] = \mathbf{0.9710} \text{ bits}$
- **Right Branch ($X > 5.85$):** Contains $\{s_6, s_7\}$.
  - Count: $N_R = 2$ ($2$ positive, $0$ negative) $\implies$ **Pure Node!**
  - $H(S_{R}) = \mathbf{0.0000} \text{ bits}$
- **Conditional Entropy:**
  $$H(S \mid X \le 5.85) = \frac{5}{7}(0.9710) + \frac{2}{7}(0.0000) = 0.6936 + 0 = \mathbf{0.6936} \text{ bits}$$
- **Information Gain:**
  $$IG(S, X \le 5.85) = 0.9852 - 0.6936 = \mathbf{0.2916} \text{ bits}$$

---

#### Step 4: Optimal Split Selection

| Candidate Threshold | Resulting Left Partition | Resulting Right Partition | Conditional Entropy | Information Gain |
| :---: | :---: | :---: | :---: | :---: |
| **$c_1 = 2.60$** | **$[0+, 2-]$** | **$[4+, 1-]$** | **$0.5156 \text{ bits}$** | **$0.4696 \text{ bits}$** |
| $c_2 = 4.75$ | $[2+, 2-]$ | $[2+, 1-]$ | $0.9650 \text{ bits}$ | $0.0202 \text{ bits}$ |
| $c_3 = 5.85$ | $[2+, 3-]$ | $[2+, 0-]$ | $0.6936 \text{ bits}$ | $0.2916 \text{ bits}$ |

The optimal decision rule is:
$$\mathbf{X \le 2.60}$$
It achieves the highest Information Gain ($0.4696\text{ bits}$) and creates a completely pure negative leaf on the left branch.

---

# 8. KTU University Examination Practice Questions

## Short-Answer Analytical Problems (Part A)

### Question 1: Mathematical Limits of Entropy
> **Question:** Define Shannon Entropy. What are its minimum and maximum values for a 4-class classification problem? When are these boundary values reached? *(3 Marks)*

**Model Answer:** Shannon Entropy measures the expected disorder in a distribution:
$$H(S) = -\sum_{i=1}^K p_i \log_2(p_i)$$
For $K = 4$:
- **Minimum Value:** $H_{\min} = 0 \text{ bits}$. Occurs when the node is completely pure (one class has $p_1 = 1$, and all others have $p_i = 0$).
- **Maximum Value:** $H_{\max} = \log_2(K) = \log_2(4) = 2 \text{ bits}$. Occurs when instances are uniformly distributed across all classes ($p_1 = p_2 = p_3 = p_4 = 0.25$).

---

### Question 2: Computational Overhead: Gini vs. Entropy
> **Question:** Why is the Gini Impurity metric computationally faster than Shannon Entropy during decision tree induction? Show how Gini approximates Entropy. *(3 Marks)*

**Model Answer:** - Computing Shannon Entropy requires calculating logarithms for every class at every candidate split:
  $$H(S) = -\sum p_i \log_2(p_i)$$
  Calculating logarithms is computationally expensive, especially on large datasets with thousands of continuous splits.
- Gini Impurity relies only on squaring probabilities:
  $$G(S) = 1 - \sum p_i^2$$
  This requires only basic multiplication and subtraction, which executes much faster on modern processors.
- Using the first-order Taylor expansion $\ln(p_i) \approx p_i - 1$, the natural entropy simplifies to:
  $$-\sum p_i (p_i - 1) = 1 - \sum p_i^2 = G(S)$$
  This shows that Gini is a direct first-order approximation of entropy.

---

### Question 3: Pathological Failure Mode of Information Gain
> **Question:** What is the primary weakness of Information Gain when evaluating multi-valued attributes like `Credit_Card_Number` or `Transaction_ID`? How does Gain Ratio address this? *(3 Marks)*

**Model Answer:** Information Gain is biased toward attributes with many distinct values. If an attribute has unique values for every instance (like a transaction ID), splitting on it produces $N$ child nodes, each containing a single example. 
Every child node is completely pure ($H = 0$), driving the conditional entropy to zero:
$$H(S \mid A) = 0 \implies IG(S, A) = H(S)$$
The algorithm selects this split because it maximizes Information Gain, but the resulting tree merely memorizes the data and fails to generalize.

The C4.5 algorithm resolves this using the **Gain Ratio**, which normalizes Information Gain by the attribute's **Split Information**:
$$\text{SplitInfo}_A(S) = -\sum_{v} \frac{|S_v|}{|S|} \log_2\left(\frac{|S_v|}{|S|}\right)$$
$$\text{GainRatio}(S, A) = \frac{IG(S, A)}{\text{SplitInfo}_A(S)}$$
For a unique identifier attribute, $\text{SplitInfo} = \log_2(N)$, which heavily penalizes the ratio and prevents the tree from selecting it.

---

## Comprehensive Essay & Derivation Questions (Part B)

### Question 4: Algorithmic Mechanics and Failure Modes of ID3
> **Question:** > (a) Detail the complete top-down recursive strategy of the ID3 algorithm. Specify its three termination base cases. *(8 Marks)* > (b) Explain how the inductive bias of decision tree learning compares with the inductive bias of a Linear Perceptron. *(4 Marks)* > (c) Differentiate between pre-pruning and post-pruning techniques. Why is post-pruning generally preferred? *(2 Marks)*

**Model Answer Outline:**
- **Part (a):** Outline the Top-Down Induction of Decision Trees (TDIDT) framework. Provide the pseudocode or execution sequence: calculate parent entropy, evaluate $IG(S, A)$ across all unused features, split on the attribute with $\max(IG)$, and recurse. Detail the three base cases from Section 5.3:
  1. All examples belong to the same class ($H = 0$).
  2. The attribute set is empty (assign the majority class of the current node).
  3. A branch receives an empty subset (assign the majority class of the parent node).
- **Part (b):** Contrast their inductive biases:
  - *Perceptron:* Uses a **language/restriction bias**. Its hypothesis space is strictly limited to linear separating hyperplanes, but its search over that space is complete.
  - *ID3:* Uses a **search/preference bias**. Its hypothesis space includes all possible discrete trees (it can represent any discrete function), but its search is greedy and incomplete. It prefers shorter trees that place high-information-gain attributes near the root (Occam's razor).
- **Part (c):** Explain pre-pruning (stopping early based on thresholds like depth or minimum sample size) versus post-pruning (growing a full tree and pruning subtrees that do not hurt validation accuracy). Note that post-pruning is preferred because pre-pruning is vulnerable to premature stopping when attributes are interdependent (e.g., in XOR problems).

---

### Question 5: End-to-End Decision Tree Construction Problem
> **Question:** > The following training dataset records weather conditions and whether a soccer match was played:
>
> | Day | Outlook | Humidity | Wind | PlaySoccer |
> | :---: | :---: | :---: | :---: | :---: |
> | D1 | Sunny | High | Weak | **No** |
> | D2 | Sunny | High | Strong | **No** |
> | D3 | Overcast | High | Weak | **Yes** |
> | D4 | Rain | High | Weak | **Yes** |
> | D5 | Rain | Normal | Weak | **Yes** |
> | D6 | Rain | Normal | Strong | **No** |
> | D7 | Overcast | Normal | Strong | **Yes** |
> | D8 | Sunny | High | Weak | **No** |
> | D9 | Sunny | Normal | Weak | **Yes** |
> | D10 | Rain | Normal | Weak | **Yes** |
> | D11 | Sunny | Normal | Strong | **Yes** |
> | D12 | Overcast | High | Strong | **Yes** |
> | D13 | Overcast | Normal | Weak | **Yes** |
> | D14 | Rain | High | Strong | **No** |
>
> (a) Compute the prior entropy $H(S)$ of the target variable `PlaySoccer`. *(3 Marks)* > (b) Compute the Information Gain for `Outlook`, `Humidity`, and `Wind`. *(8 Marks)* > (c) Identify the optimal root attribute and draw the resulting child subsets. *(3 Marks)*

**Model Answer Outline:**
- **Part (a):** Total $N = 14$. Class counts: $\text{Yes} = 9$, $\text{No} = 5$.
  $$H(S) = -\left[\frac{9}{14}\log_2\left(\frac{9}{14}\right) + \frac{5}{14}\log_2\left(\frac{5}{14}\right)\right] = \mathbf{0.9403} \text{ bits}$$
- **Part (b):** - **Outlook:** Values $\{\text{Sunny } (5), \text{Overcast } (4), \text{Rain } (5)\}$.
    - Sunny ($2\text{ Yes}, 3\text{ No}$): $H = 0.9710$
    - Overcast ($4\text{ Yes}, 0\text{ No}$): $H = 0.0$ (Pure)
    - Rain ($3\text{ Yes}, 2\text{ No}$): $H = 0.9710$
    - $H(S \mid \text{Outlook}) = \frac{5}{14}(0.9710) + \frac{4}{14}(0) + \frac{5}{14}(0.9710) = 0.6936 \text{ bits}$
    - $IG(S, \text{Outlook}) = 0.9403 - 0.6936 = \mathbf{0.2467} \text{ bits}$
  - **Humidity:** Values $\{\text{High } (7), \text{Normal } (7)\}$.
    - High ($3\text{ Yes}, 4\text{ No}$): $H = 0.9852$
    - Normal ($6\text{ Yes}, 1\text{ No}$): $H = 0.5917$
    - $H(S \mid \text{Humidity}) = \frac{7}{14}(0.9852) + \frac{7}{14}(0.5917) = 0.7885 \text{ bits}$
    - $IG(S, \text{Humidity}) = 0.9403 - 0.7885 = \mathbf{0.1518} \text{ bits}$
  - **Wind:** Values $\{\text{Weak } (8), \text{Strong } (6)\}$.
    - Weak ($6\text{ Yes}, 2\text{ No}$): $H = 0.8113$
    - Strong ($3\text{ Yes}, 3\text{ No}$): $H = 1.0000$
    - $H(S \mid \text{Wind}) = \frac{8}{14}(0.8113) + \frac{6}{14}(1.0000) = 0.8922 \text{ bits}$
    - $IG(S, \text{Wind}) = 0.9403 - 0.8922 = \mathbf{0.0481} \text{ bits}$
- **Part (c):** Compare the Information Gains:
  $$IG(\text{Outlook}) = 0.2467 > IG(\text{Humidity}) = 0.1518 > IG(\text{Wind}) = 0.0481$$
  **Outlook** is chosen as the root node attribute. It splits into three branches:
  1. **Overcast:** Perfectly pure ($4\text{ Yes}, 0\text{ No}$). Terminates immediately as a leaf labeled **Yes**.
  2. **Sunny:** Contains $5$ samples ($2\text{ Yes}, 3\text{ No}$). Requires a recursive call on $\{\text{Humidity}, \text{Wind}\}$.
  3. **Rain:** Contains $5$ samples ($3\text{ Yes}, 2\text{ No}$). Requires a recursive call on $\{\text{Humidity}, \text{Wind}\}$.
