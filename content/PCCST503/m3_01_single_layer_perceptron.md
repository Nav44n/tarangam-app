# Single-Layer Perceptron: Architecture, Weights, and Threshold Logic

**Frank Rosenblatt's 1958 artificial neuron that launched the connectionist revolution.**

Welcome to Module 3 of Machine Learning. Before we can build deep, complex neural networks, we must understand their foundational building block: the Single-Layer Perceptron. This mathematical model is where biological inspiration meets computational power.

<a id="the-intuition"></a>
## 1. The Intuition: The Biological Neuron Analogy

To understand how a machine "learns," it helps to look at how humans think. The perceptron is highly inspired by the biological neurons in our brains.

::: callout-intuition ELI5 Analogy: The Brain Switch
Imagine a biological neuron as a tiny decision-making switch in your brain:
- **Dendrites (Inputs, $x_i$):** These are the "ears" of the neuron, listening to signals from other connected neurons.
- **Synapse Weights (Importance, $w_i$):** Not all signals are equally important. Synapses amplify or dampen incoming signals based on how critical they are.
- **Cell Nucleus (The Summation):** The body of the cell collects all these weighted signals and adds them together.
- **Axon (Firing Threshold):** If the total combined signal crosses a certain threshold, the neuron "fires" an electrical pulse down its axon. If it doesn't reach the threshold, it stays completely silent. It is an "all-or-nothing" switch.
:::

In artificial intelligence, simple binary threshold units mimic these biological brain switches. The perceptron takes in multiple numerical inputs, weighs their importance, sums them up, and outputs a strict 1 (fire) or 0 (don't fire) based on a threshold.

---

<a id="the-math"></a>
## 2. Mathematical Formalism

Let us translate this biological analogy into formal mathematics. The Perceptron operates in two distinct phases: forward propagation (making a prediction) and learning (updating weights based on mistakes).

### Forward Propagation (Making a Decision)
First, we calculate the Net Input, which is the linear combination of inputs, weights, and a bias term:
$$ z = \sum_{i=1}^d w_i x_i + b = w^T x + b $$

Next, we apply the Activation Function. The perceptron uses a Hard Threshold (Heaviside step) function to make its final all-or-nothing decision:
$$ \hat{y} = \begin{cases} 1 & \text{if } z \ge 0 \\ 0 & \text{if } z < 0 \end{cases} $$

### The Perceptron Learning Rule (Fixing Mistakes)
If the perceptron makes a mistake, it must adjust its weights. The weight update equation is defined as:
$$ w_i := w_i + \Delta w_i $$

Where the change in weight ($\Delta w_i$) is calculated by:
$$ \Delta w_i = \eta (y - \hat{y}) x_i $$
*(Note: The bias $b$ is updated similarly, treating its input $x_0$ as always being $1$.)*

### Perceptron Convergence Theorem
Rosenblatt mathematically proved that if a dataset is linearly separable (meaning a straight line or flat hyperplane can perfectly divide the classes), the perceptron algorithm is guaranteed to find that separating boundary in a finite number of steps.

**Proof Intuition:** Every time the perceptron misclassifies a point, the update rule algebraically nudges the weight vector a tiny fraction ($\eta$) in the direction of the misclassified point, eventually rotating the decision boundary until all points fall on the correct side.

| Symbol | Name | Description |
| :--- | :--- | :--- |
| $x_i$ | Input Feature | The $i$-th feature of the input data point. |
| $w_i$ | Weight | The learned importance of the $i$-th input. |
| $b$ | Bias | The threshold offset that shifts the activation function. |
| $z$ | Net Input | The weighted sum of inputs plus the bias. |
| $y$ | Target Label | The actual, true class of the data point ($0$ or $1$). |
| $\hat{y}$ | Predicted Label | The perceptron's guessed output ($0$ or $1$). |
| $\eta$ | Learning Rate | A small constant (e.g., $0.1$) dictating step size during updates. |

---

<a id="worked-example"></a>
## 3. Stepped Numerical Example: Learning the Logical AND Gate

Let's watch the perceptron learn a 2-input logical AND gate.

**The AND Gate Truth Table:**
- $(0, 0) \rightarrow 0$
- $(0, 1) \rightarrow 0$
- $(1, 0) \rightarrow 0$
- $(1, 1) \rightarrow 1$

**Initial State Setup:**
- Weights: $w_1 = 0.3$, $w_2 = -0.1$
- Bias: $b = -0.2$
- Learning Rate: $\eta = 0.1$

Here is the step-by-step breakdown of Epoch 1 (one full pass through all four training examples).

::: step [Step 1: Input (0,0)]
- **Input:** $x_1=0, x_2=0$ | **Target:** $y=0$
- **Calculate $z$:** $z = (0.3)(0) + (-0.1)(0) - 0.2 = -0.2$
- **Predict $\hat{y}$:** Since $-0.2 < 0$, $\hat{y} = 0$
- **Error:** $y - \hat{y} = 0 - 0 = 0$
- **Update:** No error, weights remain unchanged. ($w_1 = 0.3, w_2 = -0.1, b = -0.2$)
:::

::: step [Step 2: Input (0,1)]
- **Input:** $x_1=0, x_2=1$ | **Target:** $y=0$
- **Calculate $z$:** $z = (0.3)(0) + (-0.1)(1) - 0.2 = -0.3$
- **Predict $\hat{y}$:** Since $-0.3 < 0$, $\hat{y} = 0$
- **Error:** $y - \hat{y} = 0 - 0 = 0$
- **Update:** No error, weights remain unchanged. ($w_1 = 0.3, w_2 = -0.1, b = -0.2$)
:::

::: step [Step 3: Input (1,0)]
- **Input:** $x_1=1, x_2=0$ | **Target:** $y=0$
- **Calculate $z$:** $z = (0.3)(1) + (-0.1)(0) - 0.2 = 0.1$
- **Predict $\hat{y}$:** Since $0.1 \ge 0$, $\hat{y} = 1$  *(Mistake!)*
- **Error:** $y - \hat{y} = 0 - 1 = -1$
- **Update:** 
  - $w_1 := 0.3 + 0.1(-1)(1) = 0.2$
  - $w_2 := -0.1 + 0.1(-1)(0) = -0.1$
  - $b := -0.2 + 0.1(-1)(1) = -0.3$
:::

::: step [Step 4: Input (1,1)]
- **Input:** $x_1=1, x_2=1$ | **Target:** $y=1$
- **Calculate $z$:** *(Using new weights!)* $z = (0.2)(1) + (-0.1)(1) - 0.3 = -0.2$
- **Predict $\hat{y}$:** Since $-0.2 < 0$, $\hat{y} = 0$ *(Mistake!)*
- **Error:** $y - \hat{y} = 1 - 0 = 1$
- **Update:**
  - $w_1 := 0.2 + 0.1(1)(1) = 0.3$
  - $w_2 := -0.1 + 0.1(1)(1) = 0.0$
  - $b := -0.3 + 0.1(1)(1) = -0.2$
:::

After Epoch 1, our new weights are $w_1=0.3$, $w_2=0.0$, $b=-0.2$. The algorithm will continue looping through the table in subsequent epochs until it makes zero mistakes!

---

<a id="simulation"></a>
## 4. Visualizing the Decision Boundary

::: manim assets/videos/m3_perceptron.mp4 Perceptron Linear Separating Line
Watch the 2D linear decision line rotate and translate after each weight update until all points are correctly classified.
:::

---

<a id="self-check"></a>
## 5. Active Recall Checkpoints

Test your understanding of the concepts covered in this micro-lesson.

::: quiz Q1: Convergence Conditions
According to the Perceptron Convergence Theorem, under what condition is the single-layer perceptron mathematically guaranteed to find a solution?
(A) When the learning rate $\eta$ is exactly $1.0$
(*B) When the dataset is linearly separable
(C) When the dataset contains only continuous numerical values
(D) When the Heaviside step function is replaced by a Sigmoid function
::: explanation
The Perceptron Convergence Theorem specifically states that if a dataset can be perfectly divided by a straight line (or hyperplane), the algorithm will always converge. If the data is not linearly separable (like an XOR gate), a single-layer perceptron will loop forever without converging.
:::

::: quiz Q2: Weight Update Logic
During training, a perceptron receives an input $x_1 = 1$, and its prediction is $\hat{y} = 1$. However, the true target label is $y = 0$. Assuming the learning rate $\eta = 0.1$, what will happen to the weight $w_1$?
(A) It will increase by $0.1$
(*B) It will decrease by $0.1$
(C) It will remain unchanged
(D) It will decrease by $1.0$
::: explanation
Let's plug the values into the update rule: $\Delta w_1 = \eta (y - \hat{y}) x_1$.
$\Delta w_1 = 0.1(0 - 1)(1) = 0.1(-1)(1) = -0.1$. Therefore, the weight $w_1$ will decrease by $0.1$.
:::
