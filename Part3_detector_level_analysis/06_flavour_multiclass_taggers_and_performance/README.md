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
$$D_{bb} = \frac{P_{hbb}}{P_{hbb} + P_{Wqq} + P_{\rm QCD\_all}}, \quad D_{qq} = \frac{P_{Wqq}}{P_{Wqq} + P_{\rm QCD\_all}}$$

---

## 🛠 Steps & Hands-on Tasks

### Step 1: `step1_multiclass_scores.py`
- **Example**: Extract raw GN3X class probabilities (`phbb`, `pWqq`, and combined `pQCD_all`).
- **Task**: Compute composite ratio discriminant $D_{bb}$ for $Z\to b\bar{b}$ signal MC vs. $W\to q\bar{q}$ and QCD background samples. Overlay 1D $D_{bb}$ score distributions.

### Step 2: `step2_performance_grid.py`
- **Example**: Compute $D_{bb} > 0.60$ selection efficiency on $Z\to b\bar{b}$ signal MC (in %).
- **Task**: Evaluate background mistag rates (in %) and background rejection factors ($1/\epsilon_{\rm bkg}$, as unitless numbers) on $W\to q\bar{q}$ MC and QCD background MC. Print a performance summary table comparing signal efficiency, mistag rates, and rejection factors.

### Step 3: `step3_2d_discriminants.py`
- **Example**: Overlay 1D $D_{qq}$ score distributions across $Z\to b\bar{b}$, $W\to q\bar{q}$, and QCD dijets, and plot 2D histogram of $D_{bb}$ vs. $D_{qq}$ scores for $Z\to b\bar{b}$ signal MC.
- **Task**: Create a 3-panel 2D comparison figure of ($D_{bb}$ vs $D_{qq}$) across $Z\to b\bar{b}$ signal, $W\to q\bar{q}$ background, and QCD dijet background samples to demonstrate 2D topological class separation.

---

## 🚀 How to Run

Navigate to this exercise directory and execute the python scripts:

```bash
cd 06_flavour_multiclass_taggers_and_performance

# Run Step 1: GN3X Multiclass Score Extraction & Composite Ratio Discriminant
python3 step1_multiclass_scores.py

# Run Step 2: Multi-Class Selection Efficiency & Mistag Evaluation
python3 step2_performance_grid.py

# Run Step 3: 2D Multi-Discriminant Performance (D_bb vs D_qq)
python3 step3_2d_discriminants.py
```

---

## ❓ Checkpoint Question

> **Why can a large `bb` classifier output enrich a Z→bb MC sample without proving that every selected reconstructed jet originated from a b-quark pair?**
>
> *(Note: Document your answer in your notebook or write-up.)*
