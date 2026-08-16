# Experimental High-Energy Physics (HEP) Monte Carlo & Analysis Training Series

Welcome to the **Experimental High-Energy Physics (HEP) Training Series**. This repository contains a modular sequence of Google Colab-compatible Jupyter notebooks, configuration cards, datasets, and analysis scripts designed to guide students through matrix-element generation, detector-level analysis, jet clustering, and boosted physics observables.

## Curriculum & Simulation Pipeline

The training program covers the physics simulation and analysis workflow:

$$\underbrace{\text{Process Cards} \rightarrow \text{Matrix Element (LHE)}}_{\mathbf{\text{Part 1: MadGraph (Skill 1)}}} \rightarrow \underbrace{\text{Uproot/Awkward} \rightarrow \text{Taggers \& Normalization}}_{\mathbf{\text{Part 2: Detector-Level Analysis (Skill 3)}}} \rightarrow \underbrace{\text{FastJet Anti-}k_t \rightarrow \text{Subjet Clustering}}_{\mathbf{\text{Part 3: Jet Clustering \& Subjets (Skill 4)}}}$$

---

## Program Structure & Modular Parts

The repository is organized into three self-contained parts:

### 1. [Part 1: MadGraph-Based Boosted Z->bb Production & LHE Exploration](file:///home/a/temp/intern-tut/Part1_MadGraph_Zbb) *(Skill 1)*
- **Directory**: `Part1_MadGraph_Zbb/`
- **Core Focus**: Hard-scattering matrix element calculation ($pp \to Z+j, Z \to b\bar{b}$), run card boost cuts (`ptj = 150.0 GeV`, `ptZmin = 150.0 GeV`), non-interactive MadGraph batch execution, LHE XML event parsing (`pylhe`), four-vector kinematics, and generator-level histograms with `mplhep`.
- **Deliverables**:
  - `Part1_01_process_to_lhe.ipynb`: MadGraph setup, cards configuration, test run (10 events), production run (1000 events), and LHE XML inspection.
  - `Part1_02_read_lhe_and_plot_kinematics.ipynb`: LHE parsing, 4-vector reconstruction, 1D/2D histograms with `mplhep`, and analytical boost guide comparison ($\Delta R_{b\bar{b}} \approx \frac{2m_Z}{p_T^Z}$).

### 2. Part 2: Detector-Level ROOT Analysis, EDA, Taggers, Sculpting, & MC Normalization *(Skill 3)*
- **Directory**: `Part2_Detector_Analysis/` *(In development)*
- **Core Focus**: Exploratory data analysis of detector-level ROOT TTrees using Uproot and Awkward Array.
- **Topics**:
  - Distinguishing generator-truth partons from reconstructed detector objects.
  - Inspecting reconstructed jet kinematics ($p_T, \eta, \phi, m$), pileup proxy ($\mu$), and Monte Carlo event weights.
  - Evaluating W-vs-QCD and multi-class machine learning tagger scores (`bb`, `qq`, QCD).
  - Understanding tagger mass sculpting and cross-section luminosity normalization.

### 3. Part 3: Jet Clustering, Radius Dependence, & Subjet Exploration *(Skill 4)*
- **Directory**: `Part3_Jet_Clustering_FastJet/` *(In development)*
- **Core Focus**: Hands-on jet physics using Python `fastjet` to understand sequential recombination jet algorithms.
- **Topics**:
  - Anti-$k_t$ clustering on particle/constituent collections across multiple radius parameters ($R = 0.4, 0.8, 1.0$).
  - Comparing small-$R$ vs. large-$R$ jet multiplicity, constituent containment, and energy fraction.
  - Reclustering large-$R$ jets into subjets to expose two-prong $Z \to b\bar{b}$ decayed resonance geometry.

---

## Technical Environment & Prerequisites

All notebooks are designed to run in **Google Colab** or standard Linux/macOS Python 3 environments.
- **Compilers & Runtimes**: Python 3.10+, C++/Fortran (`gfortran`).
- **Core Python Ecosystem**: `numpy`, `matplotlib`, `mplhep`, `pylhe`, `uproot`, `awkward`, `fastjet`.

For part-specific instructions and card files, see the `README.md` in each subfolder (e.g., [Part1_MadGraph_Zbb/README.md](file:///home/a/temp/intern-tut/Part1_MadGraph_Zbb/README.md)).
