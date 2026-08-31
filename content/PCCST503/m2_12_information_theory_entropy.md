# Information Theory: Shannon Entropy

**Quantifying disorder, impurity, and information content in mathematical bits.**

<a id="the-math"></a>
## 1. Shannon's Entropy Definition

$$ H(S) = -\sum_{i=1}^C p_i \log_2(p_i) $$

Where $p_i$ is the proportion of samples belonging to class $i$.

### Benchmark Values for Binary Classification:
- **100% Pure Node (All Yes):** $H(S) = -(1 \log_2 1) = 0.00\text{ bits}$.
- **50/50 Maximum Disorder (9 Yes, 9 No):** $H(S) = -(0.5 \log_2 0.5 + 0.5 \log_2 0.5) = 1.00\text{ bit}$.

---

<a id="self-check"></a>
## 2. Active Recall Checkpoint

::: quiz Q1: Maximum Uncertainty
For a 4-class classification problem ($C=4$), what is the maximum possible value of Shannon Entropy?
(A) 1.00 bit
(*B) 2.00 bits ($\log_2 4$)
(C) 0.00 bits
(D) 4.00 bits
::: explanation
Maximum entropy occurs when all classes are equally likely ($p_i = 1/C$). $H_{\max} = \log_2 C = \log_2 4 = 2.00\text{ bits}$.
:::
