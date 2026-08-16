# Experimental High-Energy Physics (HEP) Monte Carlo & Analysis Training Series

Welcome to the **Experimental High-Energy Physics (HEP) Training Series**. This repository contains a modular sequence of Google Colab-compatible Jupyter notebooks, configuration cards, datasets, and analysis scripts designed to guide students through matrix-element generation, detector-level analysis, jet clustering, and boosted physics observables.

## Curriculum & Simulation Pipeline

The training program covers the physics simulation and analysis workflow:

$$\text{Part 1: MadGraph} \longrightarrow \text{Part 2: Detector-Level Analysis} \longrightarrow \text{Part 3: Jet Clustering and Subjets}$$

---

## Program Structure & Modular Parts

The repository is organized into three self-contained parts:

### 1. [Part 1: MadGraph-Based Boosted Z->bb Production & LHE Exploration](./Part1_MadGraph_Zbb)
- **Directory**: `Part1_MadGraph_Zbb/`
- **Core Focus**: Hard-scattering matrix element calculation ($pp \to Z+j, Z \to b\bar{b}$), run card cuts, non-interactive MadGraph batch execution, LHE XML event parsing (`pylhe`), four-vector kinematics, and generator-level histograms with `mplhep`.
- **Deliverables**:
  - `Part1_01_process_to_lhe.ipynb`: MadGraph setup, cards configuration, test run (10 events), production run (1000 events), and LHE XML inspection.
  - `Part1_02_read_lhe_and_plot_kinematics.ipynb`: LHE parsing, 4-vector reconstruction, 1D/2D histograms with `mplhep`, and analytical boost guide comparison ($\Delta R_{b\bar{b}} \approx \frac{2m_Z}{p_T^Z}$).

### 2. Part 2: Detector-Level ROOT Analysis, EDA, Taggers, Sculpting, & MC Normalisation
- **Directory**: `Part2_Detector_Analysis/` *(In development)*
- **Core Focus**: Exploratory data analysis of detector-level ROOT TTrees.
- **Topics** including:
  - Understanding use of multi-class machine learning tagger scores (`bb`, `qq`, `q/g`).
  - Understanding tagger mass sculpting
  - Understanding MC normalisation.

### 3. Part 3: Jet Clustering, Radius Dependence, & Subjet Exploration
- **Directory**: `Part3_Jet_Clustering_FastJet/` *(In development)*
- **Core Focus**: Hands-on jet physics using Python `fastjet` and equivalent scripts to understand sequential recombination jet algorithms.
- **Topics**:
  - $\text{anti-}k_t$ clustering on particle/constituent collections across multiple radius parameters ($R = 0.4, 1.0$).
  - Reclustering large-$R$ jets into subjets to expose two-prong $Z \to b\bar{b}$ decayed resonance geometry.

---

## Technical Environment & Prerequisites

All notebooks are designed to run in **Google Colab** or standard Linux/macOS Python 3 environments.
- **Compilers & Runtimes**: Python 3.10+, C++/Fortran (`gfortran`).
- **Core Python Ecosystem**: `numpy`, `matplotlib`, `mplhep`, `pylhe`, `uproot`, `awkward`, `fastjet`.

For part-specific instructions and card files, see the `README.md` in each subfolder (e.g., [Part1_MadGraph_Zbb/README.md](./Part1_MadGraph_Zbb/README.md)).
