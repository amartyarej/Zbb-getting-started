# Part 1 — MadGraph-Based Boosted $Z \to b\bar{b}$ Production and LHE Exploration

This directory contains the standalone package for **Part 1** of the experimental High-Energy Physics (HEP) Monte Carlo training series.

## Overview & Pedagogical Purpose

Part 1 guides an experimental-HEP student from process definition to matrix element event generation and LHE kinematic exploration:

```text
Process Definition ──> MadGraph Cards ──> Parton-Level LHE File ──> Event Record Inspection ──> Generator Kinematics
```

Students study proton-proton production of a $Z$ boson recoiling against a hard matrix-element jet ($pp \to Z + j$), with the $Z$ forced to decay to a bottom-quark pair ($Z \to b\bar{b}$):
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
├── checksums.sha256
└── cards/
    ├── zbbj_proc_card.dat                         # Process Card
    └── zbbj_run_card.dat                          # Run Card
```

## Notebook Sequence

1. **`Part1_01_process_to_lhe.ipynb`**:
   - **Step 1**: Environment setup (`USE_COLAB` choice) & system dependency check (`gfortran`).
   - **Step 2**: Download & installation of MadGraph5_aMC@NLO `v3.5.16` into persistent output workspace.
   - **Step 3**: Physics foundations (Standard Model electroweak/QCD couplings, $Z \to b\bar{b}$ branching fraction $\text{BR}(Z \to b\bar{b}) \approx 15.1\%$, boosted angular collimation).
   - **Step 4**: Process card & run card configuration (`cards/zbbj_proc_card.dat`, `cards/zbbj_run_card.dat`).
   - **Step 5**: Test run ($N = 10$) with log reading & **Checkpoint 5.1** (stdout cross section, Feynman diagram count, and process `Cards/` directory inspection).
   - **Step 6**: Les Houches Event (LHE) XML structure inspection & inline Feynman diagram visualizer (`feynman_diagrams.pdf`).
   - **Step 7**: Production run ($N = 1000$ events, saved to `Zbbj_LO/Events/run_01/unweighted_events.lhe.gz`).

2. **`Part1_02_read_lhe_and_plot_kinematics.ipynb`**:
   - **Step 1**: Environment setup (`USE_COLAB` choice) & persistent LHE file verification.
   - **Step 2**: Four-vector reconstruction ($p_Z^\mu = p_b^\mu + p_{\bar{b}}^\mu$), version-safe `pylhe` event streaming, and **Checkpoint 2.2** (Breit-Wigner peak physics & Monte Carlo event weights).
   - **Step 3**: 1D kinematic histogram suite formatted with `mplhep` (CMS style), including interactive student exercises (3b: $p_T^b, p_T^{\bar{b}}$, 3c: $\eta_b, \eta_{\bar{b}}$, 3d: $m_{b\bar{b}}$, 3e: $\Delta R_{b\bar{b}}$) with hidden `<details><summary>` reference solutions.
   - **Step 4**: 2D correlation histogram ($\Delta R_{b\bar{b}}$ vs. $p_T^Z$) with theoretical boost guide overlay ($\Delta R_{b\bar{b}} \approx 2m_Z / p_T^Z$) and **Checkpoint 2.3** (opening angle & single large-$R$ jet containment threshold $p_T^Z \ge 228\text{ GeV}$).
   - **Step 5**: Advanced exploration & independent student exercises menu (generation cuts `ptj`, `ptb`, `drbb`, `mmbb`, `ebeam`; new observables $\Delta\phi_{b\bar{b}}$, $\Delta\eta_{b\bar{b}}$, recoiling jet kinematics, decay asymmetry $z$; offline analysis cuts $p_T^Z > 250\text{ GeV}$, $|\eta_b| < 2.5$; student playground code cell).

## Technical Parameters

- **MadGraph Release**: MadGraph5_aMC@NLO `v3.5.16`.
- **Process Syntax**: `import model sm`, `generate p p > z j, z > b b~`, `output Zbbj_LO`, `launch Zbbj_LO`.
- **Test Event Count**: $N = 10$ events (`Zbbj_test/`).
- **Production Event Count**: $N = 1000$ unweighted events (`Zbbj_LO/`).
