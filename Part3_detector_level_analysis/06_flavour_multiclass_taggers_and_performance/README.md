# Exercise 6 — Flavour / Multiclass Taggers and Performance Evaluation

## Scientific Question
*How do multiclass ML taggers categorize jets originating from different decay topologies (such as $b\bar{b}$, $c\bar{c}$, $q\bar{q}$, or gluon jets), and how are multi-output scores interpreted and evaluated?*

---

## 📚 Background & Concepts

### 1. GN3X Multiclass Tagger Architecture
- GN3X is a 9-class deep neural network classifier outputting probabilities for specific origin topologies.
- **Class Grouping**:
  - `phbb`: Used as the $Z\to b\bar{b}$ signal score.
  - `pWqq`: Used as the $W/Z\to q\bar{q}$ hadronic decay score.
  - `pQCDbb + pQCDbx + pQCDcx + pQCDll`: Gathered together as total QCD background probability.

### 2. Composite Ratio Discriminants
Constructing probability ratio discriminants isolates target signal hypotheses:
$$D_{bb} = \frac{P_{hbb}}{P_{hbb} + P_{Wqq} + P_{\rm QCD\_all}}$$

---

## 🛠 Steps & Hands-on Tasks

### Step 1: `step1_multiclass_scores.py`
- **Example**: Extract raw GN3X class probabilities (`phbb`, `pWqq`, and combined `pQCD_all`).
- **Task**: Compute composite ratio discriminant $D_{bb}$ for $Z\to b\bar{b}$ signal MC vs. $W\to q\bar{q}$ and QCD background samples. Overlay 1D $D_{bb}$ score distributions.

### Step 2: `step2_performance_grid.py`
- **Example**: Compute $D_{bb} > 0.60$ selection efficiency on $Z\to b\bar{b}$ signal MC.
- **Task**: Evaluate mistag rates on $W\to q\bar{q}$ MC and QCD background MC. Print a 3-class selection efficiency grid table.

---

## ❓ Checkpoint Question

> **Why can a large `bb` classifier output enrich a Z→bb MC sample without proving that every selected reconstructed jet originated from a b-quark pair?**
>
> *(Note: Document your answer in your notebook or write-up. See `solutions/checkpoint_answers.md` for full solution.)*
