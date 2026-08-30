# Exercise 7 — MC Normalization and Stack Plots

## Scientific Question
*How are simulated Monte Carlo event samples scaled to represent expected yields for a target integrated luminosity, and how are process stack plots constructed and interpreted?*

---

## 📚 Background & Concepts

### 1. Per-Event MC Weight Normalization Formula
Nominal yield equation: $N_{\rm expected} = \sigma \cdot \mathcal{L} \cdot \epsilon$.

Per-event normalization weight:
$$w_{\rm norm} = w_{\rm gen} \frac{\sigma \cdot \mathcal{L}}{\sum_i w_{{\rm gen}, i}}$$

Where:
- $w_{\rm gen}$: Generator weight (`weight_mc_NOSYS`).
- $\sigma$: Cross section in pb (from `metadata_template.json`).
- $\mathcal{L}$: Target integrated luminosity in $\text{pb}^{-1}$ ($44\text{ fb}^{-1} = 44000\text{ pb}^{-1}$).
- $\sum_i w_{{\rm gen}, i}$: Sample sum of generator weights (from `metadata_template.json`).

### 2. Statistical Variance with Negative Weights
For a histogram bin with content $Y_{\rm bin} = \sum_{i \in \text{bin}} w_{\rm norm, i}$:
$$\operatorname{Var}(Y_{\rm bin}) = \sum_{i \in \text{bin}} w_{\rm norm, i}^2, \quad \sigma_{\rm stat} = \sqrt{\operatorname{Var}(Y_{\rm bin})}$$

Squaring the weights ($w_{\rm norm, i}^2$) ensures that negative generator weights correctly add positive variance to the total MC statistical uncertainty band.

---

## 🛠 Steps & Hands-on Tasks

### Step 1: `step1_mc_weights.py`
- **Example**: Calculate per-event normalization weight $w_{\rm norm}$ for $Z\to b\bar{b}$ MC sample using `helpers.compute_event_weight()` under baseline selection ($p_T > 200\text{ GeV}$ and $m > 50\text{ GeV}$).
- **Task**: Calculate expected yields for $Z\to q\bar{q}$, $W\to q\bar{q}$, and Dijet QCD JZ4 samples for target luminosity $44\text{ fb}^{-1}$. Compare raw selected entries vs. expected luminosity-normalized yields.

### Step 2: `step2_tagger_selection_stack.py`
- **Example**: Construct a 2-panel stacked histogram (Linear and Log y-scale) of the inclusive baseline jet mass distribution with $W/Z$ processes stacked at the bottom and Dijet QCD on top (`proc_order = ["Zbb", "Zqq", "Wqq", "Dijet_JZ4"]`). Save plot to `exercise7_step2_example_inclusive_stack.png`.
- **Task 1**: Construct a 2-panel stacked histogram (Linear and Log y-scale) of events passing the ParT MassDec 50% WP selection. Save your plot to `exercise7_step2_part_selection_stack.png`.
- **Task 2**: Construct a 2-panel stacked histogram (Linear and Log y-scale) of events passing the GN3X $D_{bb} > 0.60$ tagger selection to demonstrate $Z\to b\bar{b}$ signal emergence above suppressed QCD background. Save your plot to `exercise7_step2_gn3x_dbb_selection_stack.png`.

---

## 🚀 How to Run

Navigate to this exercise directory and execute the python scripts:

```bash
cd 07_mc_normalization_and_stack_plots

# Run Step 1: Per-Event Normalization Weight Calculation
python3 step1_mc_weights.py

# Run Step 2: Stacked Process Plots (Inclusive Baseline & Tagger Selection)
python3 step2_tagger_selection_stack.py
```

---

## ❓ Checkpoint Question

> **Why is taking the sum of squared weights $\sum w^2$ necessary for calculating the statistical uncertainty on a weighted histogram bin, especially when generator weights can be negative?**
>
> *(Note: Document your answer in your notebook or write-up.)*
