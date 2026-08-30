# Exercise 2 — Histograms, Kinematics, 2D Relationships, and Selection Effects

## Scientific Question
*What do major reconstructed large-R-jet variables look like, what does a histogram summarize, and how do baseline selection cuts reshape multidimensional phase space?*

---

## 📚 Background & Concepts

### 1. Histogram Pedagogy & Conventions
- **Bin Width & Rebinning**: Changing binning alters visual resolution but must not alter invariant physical conclusions.
- **Normalization Conventions**:
  - Raw counts ($N_{\rm raw}$) vs. weighted yields vs. unit-normalized density ($\int \frac{dN}{dx} dx = 1$).
- **Linear vs. Logarithmic Axes**: Logarithmic y-axes are necessary for high-$p_T$ tails or background distributions spanning several orders of magnitude.

### 2. Multidimensional Phase-Space Distortion
- Applying a 1D selection cut on one variable (e.g. $p_T > 250\text{ GeV}$ or $|\eta| < 2.0$) shifts and reshapes the distributions of correlated observables (such as jet mass or substructure).
- 2D histograms (e.g. mass vs. $p_T$) reveal phase-space boundaries and conditional correlations invisible in 1D projections.

---

## 🛠 Steps & Hands-on Tasks

### Step 1: `step1_1d_and_binning.py`
- **Example**: Plot jet mass with fine binning (5 GeV width) vs. coarse binning (20 GeV width).
- **Task**: Compare fine vs. coarse binnings and state a physical conclusion that remains invariant under rebinning. Identify a plot where a log y-axis is necessary.

### Step 2: `step2_2d_and_selections.py`
- **Example**: Apply a baseline cut ($p_T > 250\text{ GeV}$, $|\eta| < 2.0$) and overlay 1D mass distributions before vs. after selection.
- **Task**: Create a 2D histogram of jet mass vs. $p_T$ with a vertical cut boundary line. Explain why 2D histograms expose phase-space distortions invisible in 1D projections.

---

## ❓ Checkpoint Question

> **Why should the y-axis label distinguish ‘events’, ‘weighted events’, and ‘normalized density’?**
>
> *(Note: Document your answer in your notebook or write-up.)*
