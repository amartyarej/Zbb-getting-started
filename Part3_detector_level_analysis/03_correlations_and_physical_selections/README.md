# Exercise 3 — Correlations and Physically Motivated Selections (OPTIONAL)

## Scientific Question
*Which reconstructed jet variables vary together, and how can an analyst apply selections without confusing linear/non-linear correlation with physical causation?*

*(Note: This exercise is optional. Exercises 4, 5, 6, and 7 can be performed without completing this exercise.)*

---

## 📚 Background & Concepts

### 1. Pearson Correlation Coefficient
$$r_{XY} = \frac{\operatorname{cov}(X,Y)}{\sigma_X \sigma_Y}$$
Measures the **linear association** between two continuous variables ($r_{XY} \in [-1, 1]$).
- $r_{XY} \sim 0$ means **no linear dependence**, but does **NOT** prove independence (it misses non-linear relationships).

### 2. Distance Correlation ($dcor$)
Introduced as a dependence measure designed to detect non-linear relationships:
- Non-negative: $dcor(X, Y) \in [0, 1]$.
- $dcor(X, Y) = 0$ if and only if $X$ and $Y$ are independent.

---

## 🛠 Steps & Hands-on Tasks

### Step 1: `step1_correlations.py`
- **Example**: Calculate Pearson correlation matrix for dense jet variables ($p_T$, mass, $\tau_{21}$, ParT score, pileup $\mu$).
- **Task**: Compute distance correlation $dcor(p_T, \text{Mass})$ using `helpers.compute_distance_correlation()` and compare it to Pearson $r_{XY}$.

### Step 2: `step2_cutflow.py`
- **Example**: Define sequential selection cuts on $p_T$, mass, and $\tau_{21}$.
- **Task**: Print a selection cutflow table tracking raw event counts and passing efficiencies.

---

## ❓ Checkpoint Question

> **If mass and $p_T$ have a nonzero correlation, why does that not identify the physical mechanism causing it?**
>
> *(Note: Document your answer in your notebook or write-up.)*
