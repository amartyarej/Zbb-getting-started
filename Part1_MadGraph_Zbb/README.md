# Part 1 — MadGraph-Based Boosted $Z \to b\bar{b}$ Production and LHE Exploration

This directory contains the standalone package for **Part 1** of the experimental High-Energy Physics (HEP) Monte Carlo training series.

## Overview & Pedagogical Purpose

Part 1 guides you from process definition to matrix element event generation and LHE kinematic exploration:

```text
Process Definition ──> MadGraph Cards ──> Parton-Level LHE File ──> Event Record Inspection ──> Generator Kinematics
```

In this module, you will study proton-proton production of a $Z$ boson recoiling against a hard matrix-element jet ($pp \to Z + j$), with the $Z$ forced to decay to a bottom-quark pair ($Z \to b\bar{b}$):
```text
p p > z j, z > b b~
```

## Execution Environment Modes (Google Colab vs. Local Machine)

Both notebooks support dual execution modes selectable via the `USE_COLAB` flag at the top of Step 1:

- **Google Colab Mode (`USE_COLAB = True`)**: Mounts Google Drive at `/content/drive` so all MadGraph installations, cards, generated LHE files, and Feynman diagram PDFs persist in `/content/drive/MyDrive/MadGraph_Zbb_Outputs`. Missing system tools (`gfortran`, `ghostscript`, `poppler-utils`) are automatically installed via `apt-get`.
- **Local Machine Mode (`USE_COLAB = False`)**: Runs locally without Google Drive or Colab dependencies. You can specify a base directory path by setting `LOCAL_OUTPUT_DIR = "/path/to/base/dir"` (or leave as `None` to use your current working directory), and output files will be created in `LOCAL_OUTPUT_DIR/MadGraph_Zbb_Outputs`. System dependencies (`gfortran`, `gs`, `pdftoppm`) are checked against your system `PATH` with clear installation guidance.

## Directory Organization

All Part 1 deliverables are strictly contained in this `Part1_MadGraph_Zbb/` folder:

```text
Part1_MadGraph_Zbb/
├── Part1_01_process_to_lhe.ipynb                  # Notebook 01 (MadGraph Process Setup & LHE Generation)
├── Part1_02_read_lhe_and_plot_kinematics.ipynb   # Notebook 02 (Read LHE & Plot Kinematics)
├── requirements.txt
├── README.md
└── cards/
    ├── zbbj_proc_card.dat                         # Process Card
    └── zbbj_run_card.dat                          # Run Card
```

## Notebook Sequence

1. **`Part1_01_process_to_lhe.ipynb`**: Learn Standard Model physics foundations, set up your execution environment, configure MadGraph process cards, and generate parton-level Les Houches Event (LHE) files for boosted $Z \to b\bar{b}$ production.
2. **`Part1_02_read_lhe_and_plot_kinematics.ipynb`**: Stream LHE event records with `pylhe`, reconstruct four-vector kinematics of the $Z$ boson, plot CMS-style 1D/2D histograms with `mplhep`, and verify relativistic boost collimation ($\Delta R_{b\bar{b}} \approx 2m_Z / p_T^Z$).

## Technical Parameters

- **MadGraph Release**: MadGraph5_aMC@NLO
- **Process**: `generate p p > z j, z > b b~`
- **Test Event Count**: $N = 10$ events (`Zbbj_test/`)
- **Production Event Count**: $N = 1000$ unweighted events (`Zbbj_LO/`)
