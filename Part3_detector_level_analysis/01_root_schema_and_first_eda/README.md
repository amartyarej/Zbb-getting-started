# Exercise 1 — ROOT Schema and First EDA

## Scientific Question
*What is in the supplied reconstructed-jet ROOT dataset, and how does a spreadsheet-like first inspection become a columnar HEP analysis?*

---

## 📚 Background & Concepts

### 1. ROOT File -> TTree -> Branch Hierarchy
In experimental High-Energy Physics (HEP), collision events are stored in ROOT files containing `TTree` data structures:
- **TTree (`reco`)**: The main data table.
- **Branch**: A column in the table containing a specific variable (e.g. jet transverse momentum $p_T$, pseudorapidity $\eta$, pileup $\mu$, generator weight).
- **Entry**: A row in the table representing a single LHC proton-proton collision event.

### 2. Scalar vs. Jagged Collections
- **Scalar Branches** (e.g. `actualInteractionsPerCrossing` $\mu$): Contain exactly **one scalar value per event**. Represented as 1D arrays of shape `(N_events,)`.
- **Jagged Branches** (e.g. `largeRjet_pt_NOSYS`): Contain a **variable-length list of jets per event** (some events have 1 jet, others 2 or 3). Represented as Awkward jagged arrays of shape `(N_events, var_jets)`.

---

## 🛠 Steps & Hands-on Tasks

### Step 1: `step1_schema_and_branches.py`
- **Example**: Open ROOT file using `uproot.open()`, inspect TTree keys/branches, load a branch subset.
- **Task**: Identify branch data types (scalar vs. jagged array) using `type()` and `len()`. Compute and print event count vs. total jet count.

### Step 2: `step2_kinematics_and_plots.py`
- **Example**: Extract event-level pileup parameter $\mu$ and plot a 1D histogram.
- **Task**: Extract leading Large-R jet $p_T$ (`largeRjet_pt_NOSYS`) and jet multiplicity using `ak.num()`. Produce a 3-panel matplotlib figure showing:
  1. Pileup $\mu$ distribution.
  2. Large-R jet multiplicity distribution per event.
  3. Inclusive Large-R jet $p_T$ distribution in GeV.

---

## ❓ Checkpoint Question

> **What is the difference between a branch holding a reconstructed large-R jet mass (`largeRjet_m_NOSYS`) and a branch holding a truth-matched origin label (`largeRjet_truth_label`)?**
>
> *(Note: Document your answer in your notebook or write-up.)*
