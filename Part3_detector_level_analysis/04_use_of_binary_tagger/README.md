# Exercise 4 — Use of Binary Tagger and Performance Metrics

## Scientific Question
*How does a binary ML classifier rank reconstructed jets, how is a threshold applied to define a signal-enriched region, and how are selection metrics evaluated using MC truth labels?*

---

## 📚 Background & Concepts

### 1. Binary Tagger Discriminant Scores
- A binary classifier maps reconstructed jet features to a single scalar output score in range $[0, 1]$ (e.g. W-vs-QCD score).
- **Score Ranking**: Score values rank jet candidates according to signal-like classifier preference, but raw scores are not calibrated probabilities.

### 2. Working Points (WPs) & Performance Metrics
- **Scalar Cut / WP**: Converts continuous score into a binary pass/fail selection decision ($y > y_{\rm cut}$).
- **Signal Efficiency ($\epsilon_{\rm sig}$)**: Fraction of true signal jets ($W\to qq$) passing the tagger threshold (expressed in percent `[%]`).
- **Background Mistag Rate ($\epsilon_{\rm bkg}$)**: Fraction of background jets (QCD dijets) incorrectly passing the threshold (expressed in percent `[%]`).
- **Background Rejection ($R_{\text{bkg}}$)**: Inverse background mistag rate $1/\epsilon_{\text{bkg}}$ (a dimensionless unitless number).
- **Functional WPs**: Dynamic $p_T$-dependent polynomial thresholds (e.g. `ParT_W_50_NOSYS`, `ParT_W_80_NOSYS`, mass-decorrelated variants) designed to maintain flat 50% or 80% signal efficiency across $p_T$.

---

## 🛠 Steps & Hands-on Tasks

### Step 1: `step1_tagger_scores.py`
- **Example**: Extract ANN and ParT W-tagger score distributions for $W\to qq$ signal and QCD background.
- **Task**: Overlay signal vs. background binary score distributions on a 2-panel figure.

### Step 2: `step2_working_points_and_roc.py`
- **Example**: Evaluate ParT functional working point (`ParT_W_50_MassDec_NOSYS`) using `helpers.eval_part_wp()`.
- **Task**: Calculate signal efficiency $\epsilon_{\rm sig}$ (in %), background mistag rate $\epsilon_{\rm bkg}$ (in %), and background rejection $1/\epsilon_{\rm bkg}$ (as a unitless number). Plot ROC curve ($\epsilon_{\rm sig}$ vs. $1 / \epsilon_{\rm bkg}$).

---

## 🚀 How to Run

Navigate to this exercise directory and execute the python scripts:

```bash
cd 04_use_of_binary_tagger

# Run Step 1: Binary Tagger Score Separation
python3 step1_tagger_scores.py

# Run Step 2: Working Point Evaluation & ROC Curves
python3 step2_working_points_and_roc.py
```

---

## ❓ Checkpoint Question

> **Why does applying a higher binary tagger score threshold increase signal purity while reducing signal efficiency, and why must tagger working points be frozen prior to inspecting mass distributions?**
>
> *(Note: Document your answer in your notebook or write-up.)*
