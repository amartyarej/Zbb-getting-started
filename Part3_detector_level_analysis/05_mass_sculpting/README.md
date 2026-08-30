# Exercise 5 — Mass Sculpting Diagnostics and Decorrelation

## Scientific Question
*How can binary tagger selections distort and sculpt the background mass spectrum, and how can 2D diagnostic plots distinguish true signal mass peaks from tagger-induced shape artifacts?*

---

## 📚 Background & Concepts

### 1. Mass Sculpting Mechanism
- Substructure input variables used in ML taggers (such as $N$-subjettiness $\tau_{21}$ or energy correlation functions) scale naturally with jet mass ($m \propto p_T \sqrt{\tau_{21}}$).
- **Shape Distortion**: Applying a high score cut on a standard non-decorrelated tagger artificially sculpts the smooth, falling QCD background mass spectrum into a localized bump, mimicking a physical resonance (e.g. $W$ or $Z$ boson peak).

### 2. Mass Decorrelation (DDT / MassDec Taggers)
- Mass-decorrelated taggers (e.g. `ParT_W_massDec_score`) explicitly decorrelate tagger outputs from jet mass, preserving the natural smooth QCD mass shape across working points.

---

## 🛠 Steps & Hands-on Tasks

### Step 1: `step1_mass_sculpting.py`
- **Example**: Plot inclusive background QCD jet mass vs. mass after applying standard ParT W-tagger score cut.
- **Task**: Compare mass distributions after standard score cuts vs. mass-decorrelated score cuts (`ParT_W_massDec_score`). Demonstrate how mass-decorrelated taggers preserve the background mass shape.

### Step 2: `step2_2d_mass_vs_score.py`
- **Example**: Create a 2D diagnostic histogram of QCD Jet Mass vs. Standard Tagger Score.
- **Task**: Plot working point threshold lines (50% and 80% ParT WPs) on the 2D Mass vs. Score histogram and explain why standard taggers sculpt a fake background peak.

---

## 🚀 How to Run

Navigate to this exercise directory and execute the python scripts:

```bash
cd 05_mass_sculpting

# Run Step 1: Mass Sculpting Comparison
python3 step1_mass_sculpting.py

# Run Step 2: 2D Diagnostic: Jet Mass vs Tagger Score
python3 step2_2d_mass_vs_score.py
```

---

## ❓ Checkpoint Question

> **Why can a tagger-selected mass distribution differ significantly from the inclusive mass distribution in background events even when no physical resonance is present?**
>
> *(Note: Document your answer in your notebook or write-up.)*
