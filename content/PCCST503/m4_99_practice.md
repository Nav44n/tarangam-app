# Module 4 Practice Problems

Master these exact numerical types for the university exam.

## Type 4.1: K-Means: Centroid Update

In a K-Means clustering step, a specific cluster has been assigned three 2D points: $P_1(1, 2)$, $P_2(3, 4)$, and $P_3(5, 0)$. Calculate the new coordinate for this cluster's centroid.

::: toggle Show Step-by-Step Solution
**Step 1: Understand the Centroid Formula**

The new centroid is simply the mean of all points assigned to that cluster, calculated separately for each dimension ($x$ and $y$).

**Step 2: Calculate the mean of X coordinates**

C_x = \frac{1 + 3 + 5}{3} = \frac{9}{3} = 3

**Step 3: Calculate the mean of Y coordinates**

C_y = \frac{2 + 4 + 0}{3} = \frac{6}{3} = 2<br><br><strong>Result:</strong> The updated centroid is located at $(3, 2)$.

:::

---

## Type 4.2: Distance Metrics: Euclidean & Manhattan

You are comparing two data points representing users: $A(2, 7)$ and $B(5, 3)$. Calculate both the Euclidean Distance (L2 norm) and Manhattan Distance (L1 norm) between them.

::: toggle Show Step-by-Step Solution
**Step 1: Calculate Euclidean Distance (L2)**

Formula: $d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$<br><br>d = \sqrt{(5 - 2)^2 + (3 - 7)^2}<br>d = \sqrt{3^2 + (-4)^2}<br>d = \sqrt{9 + 16} = \sqrt{25} = 5

**Step 2: Calculate Manhattan Distance (L1)**

Formula: $d = |x_2 - x_1| + |y_2 - y_1|$<br><br>d = |5 - 2| + |3 - 7|<br>d = |3| + |-4| = 3 + 4 = 7<br><br><strong>Result:</strong> Euclidean distance is 5, Manhattan distance is 7.

:::

---

