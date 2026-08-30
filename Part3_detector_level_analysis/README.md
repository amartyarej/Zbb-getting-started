# Part 3 — Detector-Level ROOT Analysis, EDA, Taggers, Sculpting, and MC Normalization

Welcome to Part 3 of the tutorial! In Parts 1 and 2, you explored parton-level matrix element kinematics and jet reconstruction. In this final section, you will transition to **detector-level reconstructed collision simulation analysis** using ROOT datasets, Uproot, and Awkward Array.

---

## 🎯 Learning Objectives

By completing these exercises, you will learn to:
1. Inspect ROOT-based reconstructed collision-simulation data using `uproot` and columnar `awkward` arrays.
2. Distinguish event-level scalar variables, reconstructed jet object collections, and Monte Carlo (MC) truth labels.
3. Construct 1D and 2D kinematic histograms with proper axis labelling, units, and binning pedagogy.
4. Understand the **multidimensional phase-space distortion** caused by baseline kinematic selection cuts.
5. [Optional] Compute linear (Pearson $r_{XY}$) and non-linear (Distance Correlation $dcor$) dependencies between reconstructed observables.
6. Evaluate binary machine-learning (ML) taggers ($W/Z$-vs-q/g jet tagger scores and working points).
7. Diagnose **mass sculpting** (tagger-induced background shape distortion) and apply mass-decorrelated discriminants.
8. Interpret multi-output flavour classifiers (multiclass probabilities for $b\bar{b}$, $q\bar{q}$, and QCD).
9. Calculate Monte Carlo normalization weights using cross sections, integrated luminosity, and sum of generator weights to build stacked process histograms with statistical uncertainty bands.

---

## 📁 Dataset Schema & Files

The analysis utilizes instructor-provided ROOT datasets containing reconstructed event trees (`reco` TTree):

- **$Z\to b\bar{b}$ MC**
- **$Z\to q\bar{q}$ MC**
- **$W\to q\bar{q}$ MC**
- **Dijet QCD JZ4 MC**

Full cross sections, entry counts, and sample sums of weights are detailed in [`metadata_template.json`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/metadata_template.json).
Branch mapping and schema definitions are detailed in [`branch_mapping_template.json`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/branch_mapping_template.json).

---

## 🛠 Setup & Environment

To set up the required dependencies, run the shell installer from this folder:

```bash
cd Part3_detector_level_analysis
./install_requirements.sh
```

Shared helper functions for loading metadata, reading trees, computing MC weights, evaluating tagger working points, and distance correlation wrappers are located in **[`helpers.py`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/helpers.py)** in this parent folder.

> [!NOTE]
> **Robust Dependency Fallbacks in `helpers.py`:
> - **`mplhep` Alternative**: If `mplhep` is not installed, `helpers.setup_mplhep_style()` automatically falls back to native Matplotlib parameters (`plt.rcParams`).
> - **`dcor` Alternative**: If `dcor` is not installed, `helpers.compute_distance_correlation()` automatically falls back to a native `scipy.spatial.distance` distance matrix calculation.

Note that the provided ROOT files are for exploration purposes only and are not intended for production analysis.

---

## 📂 Exercise Folder Structure

Each exercise is organized into its own dedicated subfolder containing a `README.md` guide (with concepts, steps, and **Checkpoint Questions**) and step-by-step Python scripts with guided examples and **Exercise TODO tasks**:

1. **[`01_root_schema_and_first_eda/`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/01_root_schema_and_first_eda/README.md)**
   - `step1_schema_and_branches.py`: Schema inspection and jagged arrays.
   - `step2_kinematics_and_plots.py`: Event-level $\mu$, jet multiplicity, and $p_T$ spectrum.
2. **[`02_histograms_kinematics_and_2d_relationships/`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/02_histograms_kinematics_and_2d_relationships/README.md)**
   - `step1_1d_and_binning.py`: Rebinning pedagogy and log y-axis.
   - `step2_2d_and_selections.py`: 2D phase space and multidimensional cut effects.
3. **[`03_correlations_and_physical_selections/`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/03_correlations_and_physical_selections/README.md)** *(Optional)*
   - `step1_correlations.py`: Pearson matrix and distance correlation ($dcor$).
   - `step2_cutflow.py`: Baseline selection cutflows.
4. **[`04_use_of_binary_tagger/`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/04_use_of_binary_tagger/README.md)**
   - `step1_tagger_scores.py`: Binary score separation.
   - `step2_working_points_and_roc.py`: Polynomial WPs and ROC curves.
5. **[`05_mass_sculpting/`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/05_mass_sculpting/README.md)**
   - `step1_mass_sculpting.py`: Standard vs. mass-decorrelated tagger comparison.
   - `step2_2d_mass_vs_score.py`: 2D mass vs. score quantile diagnostics.
6. **[`06_flavour_multiclass_taggers_and_performance/`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/06_flavour_multiclass_taggers_and_performance/README.md)**
   - `step1_multiclass_scores.py`: GN3X 9-class probabilities and $D_{bb}$ ratio.
   - `step2_performance_grid.py`: 3-class efficiency grid table.
7. **[`07_mc_normalization_and_stack_plots/`](file:///home/a/temp/intern-tut/Part3_detector_level_analysis/07_mc_normalization_and_stack_plots/README.md)**
   - `step1_mc_weights.py`: Per-event weight scaling for $44\text{ fb}^{-1}$.
   - `step2_stack_plots.py`: Stacked process histograms with $\sum w^2$ error bands.

---