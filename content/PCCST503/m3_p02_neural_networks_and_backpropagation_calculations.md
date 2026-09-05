# Module 3: Worked Problems — Neural Networks & Backpropagation
## Progressive Problem Workbook: McCulloch-Pitts Logic Synthesis, Perceptron Learning Traces, and End-to-End Backpropagation Calculations

> **Course Code:** KTU PCCST503 / CST306: Machine Learning  
> **Topic:** Module 3 (Neural Network Traces & Gradient Backpropagation)  
> **Format:** Step-by-step arithmetic and numerical solutions with zero skipped steps.

---

# Problem 1: McCulloch-Pitts Neuron Design for Logic Gates

### Problem Statement
Design individual McCulloch-Pitts neurons for the following boolean functions with binary inputs $x_1, x_2 \in \{0, 1\}$:
1. A 2-input **AND** gate.
2. A 2-input **OR** gate.
3. The logic function **$f(x_1, x_2) = x_1 \text{ AND NOT } x_2$**.

For each, determine the input weights ($w_1, w_2$), nature of connection (excitatory or inhibitory), and threshold $\theta$.

---

### Step-by-Step Solution

::: callout-formula McCulloch-Pitts Firing Rule
For excitatory inputs with weights $w_i = 1$ and threshold $\theta$:
$$y = 1 \quad \text{if } \sum x_{\text{excitatory}} \ge \theta \quad \text{AND no inhibitory input is 1; else } 0$$
:::

#### 1. AND Gate ($y = x_1 \land x_2$)
- Truth table:
  - $(0, 0) \to 0$ (sum = 0)
  - $(0, 1) \to 0$ (sum = 1)
  - $(1, 0) \to 0$ (sum = 1)
  - $(1, 1) \to 1$ (sum = 2)
- **Inequality:** Firing occurs if and only if $\text{sum} \ge 2$.
- **Design:** Both inputs excitatory ($w_1 = 1, w_2 = 1$), threshold $\boldsymbol{\theta = 2}$.

#### 2. OR Gate ($y = x_1 \lor x_2$)
- Truth table:
  - $(0, 0) \to 0$ (sum = 0)
  - $(0, 1) \to 1$ (sum = 1)
  - $(1, 0) \to 1$ (sum = 1)
  - $(1, 1) \to 1$ (sum = 2)
- **Inequality:** Firing occurs if at least one input is $1$, so $\text{sum} \ge 1$.
- **Design:** Both inputs excitatory ($w_1 = 1, w_2 = 1$), threshold $\boldsymbol{\theta = 1}$.

#### 3. $x_1 \text{ AND NOT } x_2$
- Truth table:
  - $(0, 0) \to 0$
  - $(0, 1) \to 0$ (vetoed by $x_2$)
  - $(1, 0) \to 1$ (only firing case)
  - $(1, 1) \to 0$ (vetoed by $x_2$)
- **Design:**
  - $x_1$ connects via an **excitatory connection** ($w_1 = 1$).
  - $x_2$ connects via an **inhibitory connection** (veto).
  - Threshold $\boldsymbol{\theta = 1}$.
  - Verification: At $(1, 0)$, $x_1 = 1 \ge \theta$ and $x_2 = 0$ (no veto) $\implies y = 1$. At $(1, 1)$, $x_2 = 1$ inhibits the neuron immediately $\implies y = 0$. $\checkmark$

---

# Problem 2: Complete Numerical Trace of Perceptron Learning Algorithm

### Problem Statement
Train a single-layer perceptron to learn the 2-input **OR** function.
- Inputs: Binary $x_1, x_2 \in \{0, 1\}$, with target $y \in \{0, 1\}$.
- Activation: Step function: $f(z) = 1$ if $z \ge 0$, else $0$.
- Initial parameters: $w_1 = 0.0, \; w_2 = 0.0$, bias $b = 0.0$.
- Learning rate: $\eta = 0.2$.
- Weight update rules:
  $$\Delta w_1 = \eta (y - \hat{y}) x_1, \quad \Delta w_2 = \eta (y - \hat{y}) x_2, \quad \Delta b = \eta (y - \hat{y})$$
  $$w_1 := w_1 + \Delta w_1, \quad w_2 := w_2 + \Delta w_2, \quad b := b + \Delta b$$

Trace the algorithm row-by-row until convergence.

---

### Step-by-Step Solution

#### Epoch 1:
Starting weights: $w_1 = 0, w_2 = 0, b = 0$.

| Sample | $x_1$ | $x_2$ | $y$ | Net $z = w_1 x_1 + w_2 x_2 + b$ | $\hat{y} = f(z)$ | Error $(y - \hat{y})$ | $\Delta w_1$ | $\Delta w_2$ | $\Delta b$ | New $w_1, w_2, b$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | 0 | 0 | $0(0) + 0(0) + 0 = 0$ | $1$ | $0 - 1 = -1$ | $0.2(-1)(0) = 0$ | $0.2(-1)(0) = 0$ | $0.2(-1) = -0.2$ | $w=[0, 0], b=-0.2$ |
| 2 | 0 | 1 | 1 | $0(0) + 0(1) - 0.2 = -0.2$ | $0$ | $1 - 0 = +1$ | $0.2(1)(0) = 0$ | $0.2(1)(1) = 0.2$ | $0.2(1) = +0.2$ | $w=[0, 0.2], b=0.0$ |
| 3 | 1 | 0 | 1 | $0(1) + 0.2(0) + 0 = 0$ | $1$ | $1 - 1 = 0$ | 0 | 0 | 0 | $w=[0, 0.2], b=0.0$ |
| 4 | 1 | 1 | 1 | $0(1) + 0.2(1) + 0 = 0.2$ | $1$ | $1 - 1 = 0$ | 0 | 0 | 0 | $w=[0, 0.2], b=0.0$ |

*End of Epoch 1:* Weights are $w_1 = 0.0, w_2 = 0.2, b = 0.0$. There were errors, so proceed to Epoch 2.

#### Epoch 2:
Starting weights: $w_1 = 0.0, w_2 = 0.2, b = 0.0$.

| Sample | $x_1$ | $x_2$ | $y$ | Net $z = w_1 x_1 + w_2 x_2 + b$ | $\hat{y} = f(z)$ | Error $(y - \hat{y})$ | $\Delta w_1$ | $\Delta w_2$ | $\Delta b$ | New $w_1, w_2, b$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | 0 | 0 | $0(0) + 0.2(0) + 0 = 0$ | $1$ | $0 - 1 = -1$ | $0$ | $0$ | $-0.2$ | $w=[0, 0.2], b=-0.2$ |
| 2 | 0 | 1 | 1 | $0(0) + 0.2(1) - 0.2 = 0$ | $1$ | $1 - 1 = 0$ | 0 | 0 | 0 | $w=[0, 0.2], b=-0.2$ |
| 3 | 1 | 0 | 1 | $0(1) + 0.2(0) - 0.2 = -0.2$ | $0$ | $1 - 0 = +1$ | $0.2(1)(1) = 0.2$ | $0$ | $+0.2$ | $w=[0.2, 0.2], b=0.0$ |
| 4 | 1 | 1 | 1 | $0.2(1) + 0.2(1) + 0 = 0.4$ | $1$ | $1 - 1 = 0$ | 0 | 0 | 0 | $w=[0.2, 0.2], b=0.0$ |

#### Epoch 3:
Starting weights: $w_1 = 0.2, w_2 = 0.2, b = 0.0$.

| Sample | $x_1$ | $x_2$ | $y$ | Net $z$ | $\hat{y}$ | Error | Updates |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | 0 | 0 | $0.2(0) + 0.2(0) + 0 = 0$ | $1$ | $-1$ | $b := 0 - 0.2 = -0.2$ |
| 2 | 0 | 1 | 1 | $0.2(0) + 0.2(1) - 0.2 = 0.0$ | $1$ | $0$ | None |
| 3 | 1 | 0 | 1 | $0.2(1) + 0.2(0) - 0.2 = 0.0$ | $1$ | $0$ | None |
| 4 | 1 | 1 | 1 | $0.2(1) + 0.2(1) - 0.2 = 0.2$ | $1$ | $0$ | None |

#### Epoch 4 (Verification Epoch):
Current parameters: $w_1 = 0.2, w_2 = 0.2, b = -0.2$.
- Sample 1: $(0, 0) \to z = -0.2 < 0 \implies \hat{y} = 0 = y$ (Correct!)
- Sample 2: $(0, 1) \to z = 0.2(1) - 0.2 = 0.0 \ge 0 \implies \hat{y} = 1 = y$ (Correct!)
- Sample 3: $(1, 0) \to z = 0.2(1) - 0.2 = 0.0 \ge 0 \implies \hat{y} = 1 = y$ (Correct!)
- Sample 4: $(1, 1) \to z = 0.4 - 0.2 = 0.2 \ge 0 \implies \hat{y} = 1 = y$ (Correct!)

**Convergence Achieved!** Total errors in Epoch 4 = 0.
Final learned boundary: $0.2 x_1 + 0.2 x_2 - 0.2 = 0 \iff x_1 + x_2 - 1 = 0$.

---

# Problem 3: End-to-End Backpropagation Step-by-Step Numerical Computation

### Problem Statement (Classic KTU 9-Mark Core Exam Problem)
Consider a 2-layer neural network with 2 inputs, 2 hidden neurons, and 1 output neuron:
- **Inputs:** $x_1 = 0.05, \; x_2 = 0.10$
- **Target Output:** $y = 0.01$
- **Hidden Weights & Biases:**
  - $w_{11} = 0.15, \; w_{21} = 0.20, \; b_1 = 0.35$ (for hidden neuron $h_1$)
  - $w_{12} = 0.25, \; w_{22} = 0.30, \; b_2 = 0.35$ (for hidden neuron $h_2$)
- **Output Weights & Bias:**
  - $w_{h1\_o} = 0.40, \; w_{h2\_o} = 0.45, \; b_o = 0.60$
- **Activation:** Sigmoid $\sigma(z) = \frac{1}{1 + e^{-z}}$ on both hidden and output layers.
- **Learning Rate:** $\eta = 0.5$
- **Loss Function:** Squared Error $E = \frac{1}{2}(y - a_o)^2$.

Execute:
1. Forward Pass: compute all net inputs and activations.
2. Backward Pass (Output Layer): compute error delta $\delta_o$ and update $w_{h1\_o}, w_{h2\_o}, b_o$.
3. Backward Pass (Hidden Layer): compute error deltas $\delta_{h1}, \delta_{h2}$ and update input-to-hidden weights.

---

### Step-by-Step Solution

#### Part 1: Forward Pass

**1. Hidden Neuron $h_1$:**
$$z_{h1} = w_{11} x_1 + w_{21} x_2 + b_1 = (0.15 \times 0.05) + (0.20 \times 0.10) + 0.35$$
$$z_{h1} = 0.0075 + 0.0200 + 0.35 = 0.3775$$
$$a_{h1} = \sigma(0.3775) = \frac{1}{1 + e^{-0.3775}} = \frac{1}{1 + 0.68557} \approx \mathbf{0.5933}$$

**2. Hidden Neuron $h_2$:**
$$z_{h2} = w_{12} x_1 + w_{22} x_2 + b_2 = (0.25 \times 0.05) + (0.30 \times 0.10) + 0.35$$
$$z_{h2} = 0.0125 + 0.0300 + 0.35 = 0.3925$$
$$a_{h2} = \sigma(0.3925) = \frac{1}{1 + e^{-0.3925}} = \frac{1}{1 + 0.67536} \approx \mathbf{0.5969}$$

**3. Output Neuron $o$:**
$$z_o = w_{h1\_o} a_{h1} + w_{h2\_o} a_{h2} + b_o = (0.40 \times 0.5933) + (0.45 \times 0.5969) + 0.60$$
$$z_o = 0.23732 + 0.268605 + 0.60 = 1.1059$$
$$a_o = \sigma(1.1059) = \frac{1}{1 + e^{-1.1059}} = \frac{1}{1 + 0.33091} \approx \mathbf{0.7514}$$

**4. Total Error $E$:**
$$E = \frac{1}{2}(y - a_o)^2 = \frac{1}{2}(0.01 - 0.7514)^2 = \frac{1}{2}(-0.7414)^2 = \frac{1}{2}(0.54967) \approx \mathbf{0.2748}$$

---

#### Part 2: Backward Pass (Output Layer Updates)

**1. Calculate Output Error Delta $\delta_o$:**
$$\delta_o = \frac{\partial E}{\partial z_o} = (a_o - y) \cdot a_o(1 - a_o)$$
$$(a_o - y) = 0.7514 - 0.01 = 0.7414$$
$$\sigma'(z_o) = a_o(1 - a_o) = 0.7514 \times (1 - 0.7514) = 0.7514 \times 0.2486 = 0.1868$$
$$\delta_o = 0.7414 \times 0.1868 \approx \mathbf{0.1385}$$

**2. Update Output Weights:**
- Gradient for $w_{h1\_o}$:
  $$\frac{\partial E}{\partial w_{h1\_o}} = \delta_o \cdot a_{h1} = 0.1385 \times 0.5933 = 0.08217$$
  $$w_{h1\_o}^{\text{new}} = w_{h1\_o} - \eta \frac{\partial E}{\partial w_{h1\_o}} = 0.40 - (0.5 \times 0.08217) = 0.40 - 0.04108 = \mathbf{0.3589}$$

- Gradient for $w_{h2\_o}$:
  $$\frac{\partial E}{\partial w_{h2\_o}} = \delta_o \cdot a_{h2} = 0.1385 \times 0.5969 = 0.08267$$
  $$w_{h2\_o}^{\text{new}} = w_{h2\_o} - \eta \frac{\partial E}{\partial w_{h2\_o}} = 0.45 - (0.5 \times 0.08267) = 0.45 - 0.04134 = \mathbf{0.4087}$$

- Update Output Bias $b_o$:
  $$b_o^{\text{new}} = b_o - \eta \cdot \delta_o = 0.60 - (0.5 \times 0.1385) = 0.60 - 0.06925 = \mathbf{0.5308}$$

---

#### Part 3: Backward Pass (Hidden Layer Updates)

**1. Calculate Hidden Error Delta $\delta_{h1}$:**
$$\delta_{h1} = (\delta_o \cdot w_{h1\_o}) \cdot a_{h1}(1 - a_{h1})$$
$$(\delta_o \cdot w_{h1\_o}) = 0.1385 \times 0.40 = 0.0554$$
$$\sigma'(z_{h1}) = a_{h1}(1 - a_{h1}) = 0.5933 \times (1 - 0.5933) = 0.5933 \times 0.4067 = 0.2413$$
$$\delta_{h1} = 0.0554 \times 0.2413 \approx \mathbf{0.01337}$$

**2. Calculate Hidden Error Delta $\delta_{h2}$:**
$$\delta_{h2} = (\delta_o \cdot w_{h2\_o}) \cdot a_{h2}(1 - a_{h2})$$
$$(\delta_o \cdot w_{h2\_o}) = 0.1385 \times 0.45 = 0.062325$$
$$\sigma'(z_{h2}) = a_{h2}(1 - a_{h2}) = 0.5969 \times (1 - 0.5969) = 0.5969 \times 0.4031 = 0.2406$$
$$\delta_{h2} = 0.062325 \times 0.2406 \approx \mathbf{0.01500}$$

**3. Update Input-to-Hidden Weights:**
- For $w_{11}$ (connected to input $x_1 = 0.05$):
  $$w_{11}^{\text{new}} = 0.15 - 0.5 \times (\delta_{h1} \times x_1) = 0.15 - 0.5 \times (0.01337 \times 0.05) = 0.15 - 0.000334 = \mathbf{0.1497}$$
- For $w_{21}$ (connected to input $x_2 = 0.10$):
  $$w_{21}^{\text{new}} = 0.20 - 0.5 \times (\delta_{h1} \times x_2) = 0.20 - 0.5 \times (0.01337 \times 0.10) = 0.20 - 0.000668 = \mathbf{0.1993}$$
- For $w_{12}$ (connected to input $x_1 = 0.05$):
  $$w_{12}^{\text{new}} = 0.25 - 0.5 \times (\delta_{h2} \times x_1) = 0.25 - 0.5 \times (0.01500 \times 0.05) = 0.25 - 0.000375 = \mathbf{0.2496}$$
- For $w_{22}$ (connected to input $x_2 = 0.10$):
  $$w_{22}^{\text{new}} = 0.30 - 0.5 \times (\delta_{h2} \times x_2) = 0.30 - 0.5 \times (0.01500 \times 0.10) = 0.30 - 0.000750 = \mathbf{0.2993}$$

**Summary of One Step of Backpropagation:**
All weights and biases have been updated in the direction of the negative gradient! If we compute the forward pass again with these new parameters, the total squared error $E$ will drop from $0.2748$ to approximately $0.251$.
