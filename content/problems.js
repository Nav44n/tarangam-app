// --- MODULE 1 PROBLEMS ---
window.addProblemSet(1, {
    type: "Type 1.1",
    title: "Maximum Likelihood Estimation (MLE)",
    scenario: "You flip a coin $n = 10$ times, and get $k = 7$ heads. Find the Maximum Likelihood Estimate for the probability of heads, $p$.",
    steps: [
        {
            title: "Step 1: Write the Log-Likelihood equation",
            body: "\\ell(p) = 7 \\log(p) + 3 \\log(1-p)"
        },
        {
            title: "Step 2: Take the derivative with respect to $p$",
            body: "The derivative of $?\\log(x)$ is $1/x$. So, taking the derivative gives us: <br><br> \\frac{d}{dp}\\ell(p) = \\frac{7}{p} - \\frac{3}{1-p} <br><em>(Note: The minus sign comes from applying the chain rule to the $1-p$ term).</em>"
        },
        {
            title: "Step 3: Set to zero to find the peak of the hill",
            body: "\\frac{7}{p} - \\frac{3}{1-p} = 0"
        },
        {
            title: "Step 4: Solve for $p$ with basic algebra",
            body: "Move the negative term over: \\frac{7}{p} = \\frac{3}{1-p} <br> Cross multiply: 7(1-p) = 3p <br> Expand: 7 - 7p = 3p <br> Move $p$s to one side: 7 = 10p <br><br> <strong>Answer:</strong> p = \\frac{7}{10} = 0.7"
        }
    ]
});

window.addProblemSet(1, {
    type: "Type 1.2",
    title: "Maximum A Posteriori (MAP)",
    scenario: "You run an e-commerce website. A brand new product gets exactly 1 rating, and it's a 5-star positive review. Using MLE, the product has a perfect 100% score. Use MAP to find a safer estimate, assuming a Prior belief of 2 positive and 2 negative reviews.",
    steps: [
        {
            title: "Step 1: Identify the Likelihood (Real Data)",
            body: "Actual data: $k = 1$ positive rating out of $n = 1$ total ratings."
        },
        {
            title: "Step 2: Identify the Prior (Virtual Data)",
            body: "Virtual data: $?\\alpha = 2$ positive ratings, $?\\beta = 2$ negative ratings. Total virtual ratings = 4."
        },
        {
            title: "Step 3: Combine them (The Posterior)",
            body: "Total positive = $1 \\text{ (real)} + 2 \\text{ (virtual)} = 3$.<br> Total ratings = $1 \\text{ (real)} + 4 \\text{ (virtual)} = 5$."
        },
        {
            title: "Step 4: Calculate the MAP estimate",
            body: "\\hat{p}_{MAP} = \\frac{3}{5} = 0.60 <br><br><strong>Answer:</strong> The algorithm rates the product at 60% positive, protecting your store from ranking a product at #1 just because it got a single lucky review."
        }
    ]
});

window.addProblemSet(1, {
    type: "Type 1.3",
    title: "Calculating the Cost (MSE)",
    scenario: "You have a tiny dataset of 3 students. You try to predict their test scores out of 100. Calculate the Mean Squared Error (MSE) Cost for your model.<br><br><strong>True Scores ($y$):</strong> [80, 90, 70]<br><strong>Model's Predictions ($\\hat{y}$):</strong> [75, 90, 78]",
    steps: [
        {
            title: "Step 1: Calculate the individual errors ($y - \\hat{y}$)",
            body: "Student 1: $80 - 75 = 5$<br>Student 2: $90 - 90 = 0$<br>Student 3: $70 - 78 = -8$"
        },
        {
            title: "Step 2: Square the errors",
            body: "Student 1: $5^2 = 25$<br>Student 2: $0^2 = 0$<br>Student 3: $(-8)^2 = 64$"
        },
        {
            title: "Step 3: Find the Average (Mean) to get the final Cost",
            body: "J = \\frac{25 + 0 + 64}{3} = \\frac{89}{3} \\approx 29.67<br><br><strong>Result:</strong> Your model's total Cost is 29.67."
        }
    ]
});

window.addProblemSet(1, {
    type: "Type 1.4",
    title: "Linear Regression (Ordinary Least Squares)",
    scenario: "You have a tiny dataset of 3 houses. Size $x = [1, 2, 3]$. Price $y = [2, 4, 5]$. Find the perfect straight line ($w_1$ and $w_0$) using the Least Squares formula.",
    steps: [
        {
            title: "Step 1: Find the Averages (Means)",
            body: "Average of $x$ ($\\bar{x}$) = \\frac{1+2+3}{3} = 2$<br> Average of $y$ ($\\bar{y}$) = \\frac{2+4+5}{3} = 3.67$"
        },
        {
            title: "Step 2: Calculate the Deviations for the Numerator",
            body: "Subtract the mean from each $x$ and $y$, then multiply them together: $(x_i - \\bar{x}) \\times (y_i - \\bar{y})$.<br><br> House 1: $(1 - 2) \\times (2 - 3.67) = (-1) \\times (-1.67) = 1.67$<br> House 2: $(2 - 2) \\times (4 - 3.67) = (0) \\times (0.33) = 0$<br> House 3: $(3 - 2) \\times (5 - 3.67) = (1) \\times (1.33) = 1.33$<br><br> <em>Sum of Numerator:</em> $1.67 + 0 + 1.33 = 3.0$."
        },
        {
            title: "Step 3: Calculate the Denominator",
            body: "Square the $x$ deviations: $(x_i - \\bar{x})^2$.<br><br> House 1: $(-1)^2 = 1$<br> House 2: $(0)^2 = 0$<br> House 3: $(1)^2 = 1$<br><br> <em>Sum of Denominator:</em> $1 + 0 + 1 = 2.0$."
        },
        {
            title: "Step 4: Find the Slope ($w_1$) and Intercept ($w_0$)",
            body: "w_1 = \\frac{\\text{Numerator}}{\\text{Denominator}} = \\frac{3.0}{2.0} = 1.5<br><br> w_0 = \\bar{y} - w_1\\bar{x} = 3.67 - (1.5 \\times 2) = 0.67<br><br><strong>Answer:</strong> The best fit line is $\\hat{y} = 0.67 + 1.5x$."
        }
    ]
});

window.addProblemSet(1, {
    type: "Type 1.5",
    title: "Feature Scaling (Standardization)",
    scenario: "You have a feature vector for a house: Size = 2000 sqft, Bedrooms = 3. Let's scale the 'Size' feature so it doesn't overwhelm the math. Assume you checked your whole dataset and found the average house size is 1500 sqft with a standard deviation of 500 sqft.",
    steps: [
        {
            title: "Step 1: Identify Mean and Standard Deviation",
            body: "$\\mu = 1500<br>$\\sigma = 500"
        },
        {
            title: "Step 2: Apply the Z-Score Standardization formula",
            body: "x_{scaled} = \\frac{x - \\mu}{\\sigma}"
        },
        {
            title: "Step 3: Calculate",
            body: "x_{scaled} = \\frac{2000 - 1500}{500} = \\frac{500}{500} = 1.0<br><br><strong>Result:</strong> The massive number '2000' is now represented simply as '1.0' (meaning it is exactly 1 standard deviation above average). The algorithm can now compare it safely against the smaller bedroom numbers."
        }
    ]
});


// --- MODULE 2 PROBLEMS ---
window.addProblemSet(2, {
    type: "Type 2.3",
    title: "Decision Trees (Information Gain)",
    scenario: "Given a dataset of 14 samples with a binary target concept (Play Tennis: 9 Yes, 5 No) and a feature 'Outlook' (Sunny: 5, Overcast: 4, Rain: 5). For 'Sunny', the target is (2 Yes, 3 No). For 'Overcast', the target is (4 Yes, 0 No). For 'Rain', the target is (3 Yes, 2 No). Calculate the Information Gain for the 'Outlook' feature.",
    steps: [
        {
            title: "Step 1: Calculate Entropy of the Root Node",
            body: "The total dataset $S$ has 14 instances: 9 'Yes' and 5 'No'.<br><br>E(S) = -\\frac{9}{14}\\log_2\\left(\\frac{9}{14}\\right) - \\frac{5}{14}\\log_2\\left(\\frac{5}{14}\\right) \\approx 0.940 \\text{ bits}"
        },
        {
            title: "Step 2: Calculate Entropy of each Branch (Outlook)",
            body: "<strong>Sunny (5):</strong> 2 Yes, 3 No<br>E(Sunny) = -\\frac{2}{5}\\log_2\\left(\\frac{2}{5}\\right) - \\frac{3}{5}\\log_2\\left(\\frac{3}{5}\\right) \\approx 0.971<br><br><strong>Overcast (4):</strong> 4 Yes, 0 No<br>E(Overcast) = 0 \\text{ (Pure Node)}<br><br><strong>Rain (5):</strong> 3 Yes, 2 No<br>E(Rain) = -\\frac{3}{5}\\log_2\\left(\\frac{3}{5}\\right) - \\frac{2}{5}\\log_2\\left(\\frac{2}{5}\\right) \\approx 0.971"
        },
        {
            title: "Step 3: Calculate Final Information Gain",
            body: "Formula: IG(S, Outlook) = E(S) - \\sum \\frac{|S_v|}{|S|} E(S_v)<br><br>IG = 0.940 - \\left( \\frac{5}{14}(0.971) + \\frac{4}{14}(0) + \\frac{5}{14}(0.971) \\right)<br>IG = 0.940 - (0.347 + 0 + 0.347) = 0.940 - 0.694 = 0.246 \\text{ bits}"
        }
    ]
});

window.addProblemSet(2, {
    type: "Type 2.4",
    title: "Naïve Bayes (Posterior Probability)",
    scenario: "You are building a spam filter. In your dataset, $P(\\text{Spam}) = 0.4$ and $P(\\text{Not Spam}) = 0.6$. The word 'Free' appears in 80% of Spam emails and 10% of Not Spam emails. Calculate the posterior probability that a new email containing the word 'Free' is Spam.",
    steps: [
        {
            title: "Step 1: Identify the Priors and Likelihoods",
            body: "<strong>Priors:</strong><br>$P(\\text{Spam}) = 0.4$<br>$P(\\text{Not Spam}) = 0.6$<br><br><strong>Likelihoods:</strong><br>$P(\\text{Free} \\mid \\text{Spam}) = 0.8$<br>$P(\\text{Free} \\mid \\text{Not Spam}) = 0.1$"
        },
        {
            title: "Step 2: Apply Bayes' Theorem Numerator",
            body: "We want $P(\\text{Spam} \\mid \\text{Free})$. The numerator is Likelihood $\\times$ Prior:<br><br>P(\\text{Free} \\mid \\text{Spam}) \\times P(\\text{Spam}) = 0.8 \\times 0.4 = 0.32"
        },
        {
            title: "Step 3: Calculate the Evidence (Denominator) and Final Probability",
            body: "The total probability of seeing the word 'Free':<br>P(\\text{Free}) = (0.8 \\times 0.4) + (0.1 \\times 0.6) = 0.32 + 0.06 = 0.38<br><br>Final Posterior:<br>P(\\text{Spam} \\mid \\text{Free}) = \\frac{0.32}{0.38} \\approx 0.842 \\text{ (84.2%)}$$"
        }
    ]
});

window.addProblemSet(2, {
    type: "Type 2.5",
    title: "Evaluation Metrics (Confusion Matrix)",
    scenario: "A COVID-19 test is given to 100 people. 10 people actually have COVID. The test correctly identifies 8 of them as Positive. Out of the 90 healthy people, the test incorrectly flags 5 as Positive. Derive the Confusion Matrix and calculate Accuracy, Precision, and Recall.",
    steps: [
        {
            title: "Step 1: Construct the Confusion Matrix",
            body: "Let's map the numbers:<br>- True Positives (TP): 8 (Sick, tested positive)<br>- False Negatives (FN): 2 (Sick, tested negative) [10 total sick - 8 TP]<br>- False Positives (FP): 5 (Healthy, tested positive)<br>- True Negatives (TN): 85 (Healthy, tested negative) [90 total healthy - 5 FP]<br><br> \\begin{bmatrix} TP=8 & FP=5 \\\\ FN=2 & TN=85 \\end{bmatrix} "
        },
        {
            title: "Step 2: Calculate Accuracy",
            body: "Accuracy is the total correct predictions over total population.<br><br>Accuracy = \\frac{TP + TN}{Total} = \\frac{8 + 85}{100} = 0.93 \\text{ (93%)}$$"
        },
        {
            title: "Step 3: Calculate Precision and Recall",
            body: "<strong>Precision</strong> (Out of all positive claims, how many were real?):<br>Precision = \\frac{TP}{TP + FP} = \\frac{8}{8 + 5} = \\frac{8}{13} \\approx 0.615 \\text{ (61.5%)}$$<br><br><strong>Recall</strong> (Out of all actually sick people, how many did we find?):<br>Recall = \\frac{TP}{TP + FN} = \\frac{8}{8 + 2} = \\frac{8}{10} = 0.80 \\text{ (80%)}$$"
        }
    ]
});

// --- MODULE 3 PROBLEMS ---
window.addProblemSet(3, {
    type: "Type 3.1",
    title: "Regression Evaluation (RMSE)",
    scenario: "You are evaluating a regression model. The true house prices (in $100k) are $y = [3, -0.5, 2, 7]$ and the model predicts $\\hat{y} = [2.5, 0.0, 2, 8]$. Calculate the Root Mean Squared Error (RMSE).",
    steps: [
        {
            title: "Step 1: Calculate the Error (Residuals)",
            body: "$e_i = y_i - \\hat{y}_i$<br>House 1: $3 - 2.5 = 0.5$<br>House 2: $-0.5 - 0.0 = -0.5$<br>House 3: $2 - 2 = 0$<br>House 4: $7 - 8 = -1.0$"
        },
        {
            title: "Step 2: Square the Errors",
            body: "$e_i^2$<br>House 1: $0.5^2 = 0.25$<br>House 2: $(-0.5)^2 = 0.25$<br>House 3: $0^2 = 0$<br>House 4: $(-1.0)^2 = 1.0$"
        },
        {
            title: "Step 3: Calculate the Mean (MSE)",
            body: "MSE = \\frac{0.25 + 0.25 + 0 + 1.0}{4} = \\frac{1.5}{4} = 0.375"
        },
        {
            title: "Step 4: Take the Square Root (RMSE)",
            body: "RMSE = \\sqrt{0.375} \\approx 0.612<br><br><strong>Result:</strong> The RMSE is 0.612 (or $61,200)."
        }
    ]
});

window.addProblemSet(3, {
    type: "Type 3.2",
    title: "Perceptron Weight Update",
    scenario: "A perceptron has weights $w_1 = 0.5, w_2 = -0.5$ and bias $b = 0$. An input vector $x = [1, 2]$ belongs to class $y = 1$ (positive). The learning rate $\\eta = 0.1$. First, find if the perceptron classifies it correctly (using a step function where output is 1 if sum $\\ge 0$, else -1). If incorrect, update the weights.",
    steps: [
        {
            title: "Step 1: Calculate the weighted sum",
            body: "z = (w_1 \\times x_1) + (w_2 \\times x_2) + b<br>z = (0.5 \\times 1) + (-0.5 \\times 2) + 0<br>z = 0.5 - 1.0 = -0.5"
        },
        {
            title: "Step 2: Apply the activation function",
            body: "Since $z = -0.5 < 0$, the predicted output $\\hat{y} = -1$.<br>The true target is $y = 1$. The prediction is incorrect."
        },
        {
            title: "Step 3: Apply the update rule",
            body: "Formula: $w_i \\leftarrow w_i + \\eta (y - \\hat{y}) x_i$<br>Error term: $(y - \\hat{y}) = 1 - (-1) = 2$<br><br>Update $w_1$:<br>w_1 = 0.5 + 0.1 \\times 2 \\times 1 = 0.5 + 0.2 = 0.7<br><br>Update $w_2$:<br>w_2 = -0.5 + 0.1 \\times 2 \\times 2 = -0.5 + 0.4 = -0.1<br><br>Update $b$:<br>b = 0 + 0.1 \\times 2 \\times 1 = 0.2"
        }
    ]
});

// --- MODULE 4 PROBLEMS ---
window.addProblemSet(4, {
    type: "Type 4.1",
    title: "K-Means: Centroid Update",
    scenario: "In a K-Means clustering step, a specific cluster has been assigned three 2D points: $P_1(1, 2)$, $P_2(3, 4)$, and $P_3(5, 0)$. Calculate the new coordinate for this cluster's centroid.",
    steps: [
        {
            title: "Step 1: Understand the Centroid Formula",
            body: "The new centroid is simply the mean of all points assigned to that cluster, calculated separately for each dimension ($x$ and $y$)."
        },
        {
            title: "Step 2: Calculate the mean of X coordinates",
            body: "C_x = \\frac{1 + 3 + 5}{3} = \\frac{9}{3} = 3"
        },
        {
            title: "Step 3: Calculate the mean of Y coordinates",
            body: "C_y = \\frac{2 + 4 + 0}{3} = \\frac{6}{3} = 2<br><br><strong>Result:</strong> The updated centroid is located at $(3, 2)$."
        }
    ]
});

window.addProblemSet(4, {
    type: "Type 4.2",
    title: "Distance Metrics: Euclidean & Manhattan",
    scenario: "You are comparing two data points representing users: $A(2, 7)$ and $B(5, 3)$. Calculate both the Euclidean Distance (L2 norm) and Manhattan Distance (L1 norm) between them.",
    steps: [
        {
            title: "Step 1: Calculate Euclidean Distance (L2)",
            body: "Formula: $d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$<br><br>d = \\sqrt{(5 - 2)^2 + (3 - 7)^2}<br>d = \\sqrt{3^2 + (-4)^2}<br>d = \\sqrt{9 + 16} = \\sqrt{25} = 5"
        },
        {
            title: "Step 2: Calculate Manhattan Distance (L1)",
            body: "Formula: $d = |x_2 - x_1| + |y_2 - y_1|$<br><br>d = |5 - 2| + |3 - 7|<br>d = |3| + |-4| = 3 + 4 = 7<br><br><strong>Result:</strong> Euclidean distance is 5, Manhattan distance is 7."
        }
    ]
});
