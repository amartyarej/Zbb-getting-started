# Experimental High-Energy Physics (HEP) Monte Carlo & Analysis Training Series

Welcome to the **Experimental High-Energy Physics (HEP) Training Series**. This repository contains a modular sequence of Google Colab-compatible Jupyter notebooks, configuration cards, datasets, and analysis scripts designed to guide students through matrix-element generation, detector-level analysis, jet clustering, and boosted physics observables.

## Curriculum & Simulation Pipeline

The training program covers the physics simulation and analysis workflow:

$$\text{Part 1: MadGraph} \longrightarrow \text{Part 2: Jet Clustering and Subjets} \longrightarrow \text{Part 3: Detector-Level ROOT Analysis and ML}$$

---

## Program Structure & Modular Parts

The repository is organized into three self-contained parts:

### 1. [Part 1: MadGraph-Based Boosted $Z \to b\bar{b}$ Production & LHE Exploration](./Part1_MadGraph_Zbb)
- **Directory**: `Part1_MadGraph_Zbb/`
- **Core Focus**: Hard-scattering matrix element calculation ($pp \to Z + j, Z \to b\bar{b}$), run card cuts, non-interactive MadGraph batch execution, LHE XML event parsing (`pylhe`), four-vector kinematics ($p_T, \eta, \phi, m$), and generator-level histograms with `mplhep`.
- **Deliverables**:
  - `Part1_01_process_to_lhe.ipynb`: MadGraph setup, cards configuration, test run ($N = 10$ events), production run ($N = 1000$ events), and LHE XML inspection.
  - `Part1_02_read_lhe_and_plot_kinematics.ipynb`: LHE parsing, 4-vector reconstruction ($p_Z^\mu = p_b^\mu + p_{\bar{b}}^\mu$), 1D/2D histograms with `mplhep`, and analytical boost guide comparison ($\Delta R_{b\bar{b}} \approx 2m_Z / p_T^Z$).

### 2. [Part 2: Jet Clustering, Radius Dependence, & Subjet Exploration](./Part2_Jets)
- **Directory**: `Part2_Jets/`
- **Core Focus**: Hands-on introduction to jet physics using Python `fastjet`, `uproot`, and `awkward` on constituent-level ROOT events (`data/Zbb_RawConst.root`).
- **Deliverables**: Hadronic physics foundations, sequential recombination algorithms ($anti-k_t$, $k_t$, C/A), constituent $(\eta, \phi)$ visualization, radius parameter scan ($R=0.2, 0.4, 0.8, 1.0$), exclusive $N=2$ subjet reclustering, and Truth vs. EMPFlow comparison.

### 3. [Part 3: Detector-Level ROOT Analysis, Exploratory Data Analysis, Taggers, Sculpting, & MC Normalization](./Part3_detector_level_analysis)
- **Directory**: `Part3_detector_level_analysis/`
- **Core Focus**: Reconstructed collision simulation analysis using ROOT `TTree` objects, `uproot`, and `awkward` array tools.

---

## Technical Environment & Prerequisites

All notebooks are designed to run in **Google Colab** or standard Linux/macOS Python 3 environments.
- **Compilers & Runtimes**: Python 3.10+, C++/Fortran (`gfortran`).
- **Core Python Ecosystem**: `numpy`, `matplotlib`, `mplhep`, `pylhe`, `uproot`, `awkward`, `fastjet`.

For part-specific instructions and card files, see the `README.md` in each subfolder (e.g., [Part1_MadGraph_Zbb/README.md](./Part1_MadGraph_Zbb/README.md)).
