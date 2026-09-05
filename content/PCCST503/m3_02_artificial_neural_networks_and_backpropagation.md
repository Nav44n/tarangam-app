# Module 3: Artificial Neural Networks & Backpropagation
## Comprehensive Theory: Biological Analogs, Perceptron Convergence, Activation Functions, and Calculus Chain Rule Backpropagation

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Module Alignment:** Module 3 (Neural Networks & Deep Learning Foundations)  
> **Target Audience:** Absolute beginners with no prior knowledge of neural computing or calculus chain rule.

---

# Table of Contents
1. [From Biology to Silicon: The Artificial Neuron](#1-from-biology-to-silicon-the-artificial-neuron)
2. [The McCulloch-Pitts (M-P) Neuron Model](#2-the-mcculloch-pitts-m-p-neuron-model)
3. [Rosenblatt's Perceptron & The Learning Algorithm](#3-rosenblatts-perceptron--the-learning-algorithm)
4. [The Perceptron Convergence Theorem & XOR Limitation](#4-the-perceptron-convergence-theorem--xor-limitation)
5. [Multilayer Feedforward Networks (MLP) & Hidden Representations](#5-multilayer-feedforward-networks-mlp--hidden-representations)
6. [Mathematical Anatomy of Activation Functions](#6-mathematical-anatomy-of-activation-functions)
7. [The Backpropagation Algorithm: Step-by-Step Derivation](#7-the-backpropagation-algorithm-step-by-step-derivation)
8. [Training Dynamics: Learning Rates, Batches & Symmetry Breaking](#8-training-dynamics-learning-rates-batches--symmetry-breaking)
9. [Interactive Knowledge Check Quizzes](#9-interactive-knowledge-check-quizzes)
10. [KTU University Exam Review: Part A & Part B](#10-ktu-university-exam-review-part-a--part-b)

---

# 1. From Biology to Silicon: The Artificial Neuron

::: callout-intuition The Brain as an Electric Circuit
The human brain contains approximately $86$ billion neurons interconnected via $100$ trillion synapses.
- **Dendrites:** Tree-like fibers that receive chemical signals from other neurons.
- **Soma (Cell Body):** Sums up all incoming electric charges.
- **Axon:** If the cumulative charge exceeds a physical threshold, the cell fires an electric pulse ("action potential") down the axon cable.
- **Synapses:** Tiny gaps where connection strengths can be adjusted through experience (learning!).

In machine learning, we strip away the biology to create a simple mathematical abstraction:
1. Inputs $x_i$ represent dendrite signals.
2. Weights $w_i$ represent synaptic strengths.
3. Summation junction $\sum w_i x_i + b$ models the soma's accumulation.
4. An activation function $f(z)$ decides whether and how strongly the artificial neuron fires!
:::

```
  Biological Neuron                    Artificial Neuron
  -----------------                    -----------------
  Dendrites (Inputs)       =======>    Input Vector [x1, x2, ..., xd]
  Synaptic Strengths       =======>    Weights [w1, w2, ..., wd]
  Soma Accumulation        =======>    Net Sum: z = Sum(wi * xi) + b
  Action Potential Fire    =======>    Activation Output: a = f(z)
```

---

# 2. The McCulloch-Pitts (M-P) Neuron Model

Introduced by Warren McCulloch and Walter Pitts in 1943, this was the very first computational model of a neuron.

### Mathematical Specification:
- Inputs are strictly binary: $x_i \in \{0, 1\}$.
- Connections are of two types:
  1. **Excitatory:** Add $+1$ to the neuron's potential.
  2. **Inhibitory:** Possess absolute veto power ($-\infty$). If ANY inhibitory input is active ($1$), the neuron CANNOT fire.
- A threshold $\theta \in \mathbb{Z}^+$ controls firing:
  $$y = \begin{cases} 1 & \text{if } \sum_{i=1}^n x_i \ge \theta \text{ AND no inhibitory input is 1} \\ 0 & \text{otherwise} \end{cases}$$

### Synthesizing Logic Gates with M-P Neurons:
- **2-Input AND Gate:** Both $x_1$ and $x_2$ must be $1$. Set $\theta = 2$.
  - For $(1, 1)$, sum $= 2 \ge 2 \implies y = 1$.
  - For $(1, 0)$ or $(0, 1)$, sum $= 1 < 2 \implies y = 0$.
- **2-Input OR Gate:** Either $x_1$ or $x_2$ must be $1$. Set $\theta = 1$.
- **NOT Gate ($x_1 \text{ AND NOT } x_2$):** Feed $x_1$ to an excitatory input and $x_2$ to an inhibitory input with $\theta = 1$.

*Limitation:* M-P neurons cannot learn. All weights and thresholds must be hard-coded by human engineers.

---

# 3. Rosenblatt's Perceptron & The Learning Algorithm

In 1958, Frank Rosenblatt introduced the **Perceptron**, adding real-valued weights and an automatic **Learning Algorithm**.

### Mathematical Model:
$$\hat{y} = f(z) = f\left(\sum_{i=1}^d w_i x_i + b\right) = f(\mathbf{w}^T \mathbf{x} + b)$$
where $f(z)$ is the **Heaviside step function**:
$$f(z) = \begin{cases} +1 & \text{if } z \ge 0 \\ -1 \text{ (or } 0\text{)} & \text{if } z < 0 \end{cases}$$

### The Perceptron Learning Rule:
Given training pairs $(\mathbf{x}_i, y_i)$ where $y_i \in \{-1, +1\}$:
1. Initialize weights $\mathbf{w} = \mathbf{0}$ and bias $b = 0$.
2. For each sample $(\mathbf{x}_i, y_i)$, compute predicted output $\hat{y}_i = \text{sign}(\mathbf{w}^T \mathbf{x}_i + b)$.
3. If $\hat{y}_i \ne y_i$ (misclassification error), update weights:
   $$\mathbf{w} := \mathbf{w} + \eta \, (y_i - \hat{y}_i) \, \mathbf{x}_i$$
   $$b := b + \eta \, (y_i - \hat{y}_i)$$
   where $\eta \in (0, 1]$ is the **learning rate**.

::: callout-intuition Geometric Meaning of the Weight Update
If a positive point ($y_i = +1$) was misclassified as negative ($\hat{y}_i = -1$), $(y_i - \hat{y}_i) = +2$. The rule adds a multiple of $\mathbf{x}_i$ to $\mathbf{w}$. Since the dot product $\mathbf{w}^T \mathbf{x}_i$ measures alignment, adding $\mathbf{x}_i$ rotates $\mathbf{w}$ towards the misclassified point, pulling it onto the correct side of the boundary!
:::

---

# 4. The Perceptron Convergence Theorem & XOR Limitation

### Perceptron Convergence Theorem (Novikoff, 1962):
If a dataset is **linearly separable** (meaning there exists some hyperplane that separates the classes with a positive margin $\gamma > 0$), then the Perceptron learning algorithm is **guaranteed to converge** and find a separating hyperplane in a finite number of mistakes $k$:
$$k \le \left(\frac{R}{\gamma}\right)^2$$
where $R = \max_i \|\mathbf{x}_i\|$ is the radius of the smallest sphere enclosing the data.

### The XOR Linear Separability Barrier (Minsky & Papert, 1969):
In their historic book *Perceptrons*, Marvin Minsky and Seymour Papert proved that a single-layer perceptron **cannot compute the simple XOR (Exclusive-OR) logic function**:

| $x_1$ | $x_2$ | $y = x_1 \oplus x_2$ |
| :---: | :---: | :---: |
| 0 | 0 | **0** |
| 0 | 1 | **1** |
| 1 | 0 | **1** |
| 1 | 1 | **0** |

```
   x2 ^
    1 |   (0, 1) [Class 1]         (1, 1) [Class 0]
      |          o                       x
      |
      |          x                       o
    0 |   (0, 0) [Class 0]         (1, 0) [Class 1]
      +---------------------------------------------> x1
                 0                       1
```

**Algebraic Proof of Impossible Linear Separation:**
Assume there exist weights $w_1, w_2$ and threshold $\theta$ separating XOR:
1. For $(0, 0) \to 0$: $w_1(0) + w_2(0) < \theta \implies 0 < \theta$
2. For $(1, 0) \to 1$: $w_1(1) + w_2(0) \ge \theta \implies w_1 \ge \theta$
3. For $(0, 1) \to 1$: $w_1(0) + w_2(1) \ge \theta \implies w_2 \ge \theta$
4. For $(1, 1) \to 0$: $w_1(1) + w_2(1) < \theta \implies w_1 + w_2 < \theta$

Add inequalities (2) and (3):
$$w_1 + w_2 \ge 2\theta$$
From (1), we know $\theta > 0$, so $2\theta > \theta$. Therefore:
$$w_1 + w_2 > \theta$$
This directly contradicts inequality (4) ($w_1 + w_2 < \theta$)! No such line can exist.

---

# 5. Multilayer Feedforward Networks (MLP) & Hidden Representations

To solve non-linearly separable problems like XOR, we assemble neurons into multiple connected layers:
- **Input Layer:** Distributes the features without computation.
- **Hidden Layer(s):** Transform inputs into internal non-linear representations.
- **Output Layer:** Produces final predictions.

### Solving XOR with One Hidden Layer:
Notice that $A \oplus B = (A \text{ OR } B) \text{ AND NOT } (A \text{ AND } B)$.
- Hidden Neuron 1 computes $h_1 = \text{OR}(x_1, x_2)$.
- Hidden Neuron 2 computes $h_2 = \text{NAND}(x_1, x_2)$.
- Output Neuron computes $y = \text{AND}(h_1, h_2)$.
By projecting into the intermediate representation space $(h_1, h_2)$, XOR becomes linearly separable!

### The Universal Approximation Theorem (Cybenko, 1989):
A feedforward neural network with a **single hidden layer** containing a finite number of non-linear neurons can approximate any continuous function on a compact domain to any desired degree of accuracy.
*(Depth vs. Width: While 1 wide hidden layer can theoretically approximate anything, deep networks with multiple hierarchical layers require exponentially fewer neurons to achieve the same expressive power).*

---

# 6. Mathematical Anatomy of Activation Functions

If neurons used purely linear activations ($f(z) = c \cdot z$), composing multiple layers would just yield another linear function:
$$\mathbf{W}_3 (\mathbf{W}_2 (\mathbf{W}_1 \mathbf{x})) = (\mathbf{W}_3 \mathbf{W}_2 \mathbf{W}_1) \mathbf{x} = \mathbf{W}_{\text{combined}} \mathbf{x}$$
**Non-linear activation functions are required to enable deep networks to learn complex decision boundaries.**

### A. Sigmoid (Logistic) Function
$$\sigma(z) = \frac{1}{1 + e^{-z}}, \quad \text{Range: } (0, 1)$$

::: callout-formula Calculus Derivation of Sigmoid Derivative
$$\sigma'(z) = \frac{d}{dz} (1 + e^{-z})^{-1} = - (1 + e^{-z})^{-2} (-e^{-z}) = \frac{e^{-z}}{(1 + e^{-z})^2}$$
$$= \left(\frac{1}{1 + e^{-z}}\right) \left(\frac{e^{-z}}{1 + e^{-z}}\right) = \left(\frac{1}{1 + e^{-z}}\right) \left(1 - \frac{1}{1 + e^{-z}}\right) = \sigma(z) (1 - \sigma(z))$$
:::
- **Critical Flaw: Vanishing Gradient Problem.** Maximum derivative $\sigma'(0) = 0.25$. When $|z|$ is large, $\sigma'(z) \approx 0$. Multiplying many small derivatives causes error signals to vanish in early layers.

### B. Hyperbolic Tangent ($\tanh$) Function
$$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}, \quad \text{Range: } (-1, +1)$$
- **Derivative:** $\tanh'(z) = 1 - \tanh^2(z)$.
- **Advantage over Sigmoid:** It is **zero-centered**, which prevents zigzagging weight updates during gradient descent. Still suffers from saturation and vanishing gradients at the extremes.

### C. Rectified Linear Unit (ReLU)
$$f(z) = \max(0, z), \quad \text{Range: } [0, \infty)$$
- **Derivative:** $f'(z) = 1$ if $z > 0$, and $0$ if $z < 0$.
- **Advantages:** Does not saturate for $z > 0$ (cures vanishing gradient!), computationally cheap (simple threshold at 0), induces biological sparsity.
- **Flaw: Dying ReLU Problem.** If a neuron gets pushed into $z < 0$ for all training data, its gradient is permanently $0$ and it never learns again.
- **Solution:** **Leaky ReLU:** $f(z) = \max(0.01z, z)$.

---

# 7. The Backpropagation Algorithm: Step-by-Step Derivation

Backpropagation (Rumelhart, Hinton, & Williams, 1986) uses the **calculus chain rule** to calculate the partial derivative of the loss with respect to every weight in the network.

Consider a 3-layer network:
- Input $x_i$, Hidden neuron $j$, Output neuron $k$.
- Total Squared Error Loss: $E = \frac{1}{2} \sum_k (y_k - a_k)^2$.

```
  x_i  --(w_ij)-->  [ Hidden Node j ]  --(w_jk)-->  [ Output Node k ]  --> a_k
                    z_j = Sum w_ij*x_i + b_j        z_k = Sum w_jk*a_j + b_k
                    a_j = g(z_j)                    a_k = g(z_k)
```

### Step 1: Gradients for Output Layer Weights ($w_{jk}$)
By the chain rule:
$$\frac{\partial E}{\partial w_{jk}} = \frac{\partial E}{\partial a_k} \cdot \frac{\partial a_k}{\partial z_k} \cdot \frac{\partial z_k}{\partial w_{jk}}$$

Evaluate each component:
1. $\frac{\partial E}{\partial a_k} = -(y_k - a_k) = (a_k - y_k)$
2. $\frac{\partial a_k}{\partial z_k} = g'(z_k)$
3. $\frac{\partial z_k}{\partial w_{jk}} = a_j$

Define the **Output Error Delta** $\delta_k$:
$$\delta_k \equiv \frac{\partial E}{\partial z_k} = (a_k - y_k) g'(z_k)$$
$$\frac{\partial E}{\partial w_{jk}} = \delta_k \cdot a_j$$

### Step 2: Gradients for Hidden Layer Weights ($w_{ij}$)
Hidden neuron $j$ contributes to the error of **all** output neurons $k$. Sum across all outputs:
$$\frac{\partial E}{\partial w_{ij}} = \sum_k \left( \frac{\partial E}{\partial z_k} \frac{\partial z_k}{\partial a_j} \right) \cdot \frac{\partial a_j}{\partial z_j} \cdot \frac{\partial z_j}{\partial w_{ij}}$$

Evaluate terms:
1. $\frac{\partial E}{\partial z_k} = \delta_k$
2. $\frac{\partial z_k}{\partial a_j} = w_{jk}$
3. $\frac{\partial a_j}{\partial z_j} = g'(z_j)$
4. $\frac{\partial z_j}{\partial w_{ij}} = x_i$

Define the **Hidden Error Delta** $\delta_j$:
$$\delta_j \equiv \left( \sum_k \delta_k w_{jk} \right) g'(z_j)$$
$$\frac{\partial E}{\partial w_{ij}} = \delta_j \cdot x_i$$

### Step 3: Gradient Descent Parameter Updates:
$$w_{jk} := w_{jk} - \eta \frac{\partial E}{\partial w_{jk}} = w_{jk} - \eta \, \delta_k \, a_j$$
$$w_{ij} := w_{ij} - \eta \frac{\partial E}{\partial w_{ij}} = w_{ij} - \eta \, \delta_j \, x_i$$

---

# 8. Training Dynamics: Learning Rates, Batches & Symmetry Breaking

1. **Why Weights Must NEVER Be Initialized to Zero:**
   - If all weights start at $0$, every hidden neuron in a layer computes the exact same activation and receives the exact same error delta. They remain identical clones forever (**Symmetry Lock**).
   - *Remedy:* Initialize weights with small random numbers (e.g., Xavier/Glorot or He initialization).
2. **Gradient Descent Variants:**
   - **Batch Gradient Descent:** Computes error on the entire dataset before updating. Very stable, but slow on large datasets.
   - **Stochastic Gradient Descent (SGD):** Updates weights after every single sample. Fast and noisy, can escape local minima.
   - **Mini-Batch Gradient Descent:** Updates weights on small batches (e.g., 32 or 64 samples). The standard deep learning standard.

---

# 9. Interactive Knowledge Check Quizzes

::: quiz XOR Problem
Why did the original single-layer Perceptron fail to solve the XOR logic problem?
(A) The learning rate was set too high
(*B) The four XOR points cannot be separated by any single straight line in 2D space
(C) Step activation functions cannot compute binary outputs
(D) XOR requires negative weights which the Perceptron prohibits
::: explanation
XOR is non-linearly separable. Its positive targets $(0, 1)$ and $(1, 0)$ and negative targets $(0, 0)$ and $(1, 1)$ lie diagonally opposite each other, requiring at least two lines (a hidden layer) to isolate.
:::

::: quiz Activation Functions
Why is the maximum derivative of the Sigmoid activation function equal to 0.25 a hazard for deep neural networks?
(A) It causes weights to grow infinitely large
(*B) Multiplying values $\le 0.25$ across multiple layers causes error deltas to vanish exponentially
(C) It forces all activations to be zero
(D) It makes the cost function non-convex
::: explanation
Because $\sigma'(z) \le 0.25$, backpropagating gradients through $L$ layers scales the gradient by approximately $(0.25)^L$. For deep architectures, early layers receive almost zero gradient updates (the Vanishing Gradient Problem).
:::

::: quiz Backpropagation
In the backpropagation algorithm, what does the error delta $\delta_j$ for a hidden neuron represent?
(A) The actual prediction minus the target
(B) The magnitude of the input features
(*C) The partial derivative of total error with respect to the neuron's weighted input sum ($\partial E / \partial z_j$)
(D) The learning rate divided by the number of neurons
::: explanation
By definition, the error delta at any node $j$ is $\delta_j = \frac{\partial E}{\partial z_j}$. It encapsulates how sensitive the total network error is to changes in the net incoming excitation to that node.
:::

---

# 10. KTU University Exam Review: Part A & Part B

### Part A: Rapid 3-Mark Questions
1. **Differentiate between McCulloch-Pitts Neuron and Rosenblatt's Perceptron.**  
   *Answer:* M-P neurons use fixed binary inputs, hardcoded integer thresholds, and cannot learn. Rosenblatt's Perceptron accepts continuous inputs, uses real-valued adjustable synaptic weights, and features an automated iterative learning algorithm.
2. **State the Universal Approximation Theorem.**  
   *Answer:* A standard feedforward neural network with a single hidden layer containing a finite number of non-linear neurons can approximate any continuous function on a compact domain to arbitrary precision.
3. **Why must weights in an MLP be initialized randomly rather than to zero?**  
   *Answer:* Initializing weights to zero causes all hidden neurons to produce identical activations and receive identical backpropagated gradients, preventing the network from learning distinct features (symmetry lock).

### Part B: 9-Mark Master Derivation Outline
1. **Derive the backpropagation weight update equations for a two-layer feedforward network.**
   - Define network architecture, forward pass notation ($z_j, a_j, z_k, a_k$), and MSE loss $E$.
   - Apply the multivariable chain rule to output weights: show $\frac{\partial E}{\partial w_{jk}} = \delta_k a_j$ where $\delta_k = (a_k - y_k) g'(z_k)$.
   - Apply the chain rule across all output paths to hidden weights: show $\frac{\partial E}{\partial w_{ij}} = \delta_j x_i$ where $\delta_j = \left(\sum_k \delta_k w_{jk}\right) g'(z_j)$.
   - State the gradient descent parameter updates with learning rate $\eta$.
