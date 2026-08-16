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
   - Environment verification (`gfortran --version`, `python3 --version`).
   - Download & installation of MadGraph5_aMC@NLO `v3.5.16`.
   - Physics foundations (Standard Model, $Z \to b\bar{b}$ branching fraction $\text{BR}(Z \to b\bar{b}) \approx 15.1\%$, boosted topology).
   - Process card & run card configuration (`cards/zbbj_proc_card.dat`, `cards/zbbj_run_card.dat`).
   - 10-event test generation ($N = 10$) with log inspection.
   - 1000-event main production generation ($N = 1000$, output `Zbbj_LO/Events/run_01/unweighted_events.lhe.gz`).
   - LHE XML format inspection (`<event>` block particle attribute breakdown).

2. **`Part1_02_read_lhe_and_plot_kinematics.ipynb`**:
   - Strict check for Notebook 01 output (`Zbbj_LO/Events/run_01/unweighted_events.lhe.gz`).
   - Event loop parsing with Scikit-HEP `pylhe`.
   - Four-vector reconstruction of $Z$ boson ($p_Z^\mu = p_b^\mu + p_{\bar{b}}^\mu$) and kinematic calculations ($p_T^Z, p_T^b, \eta, \phi, \Delta R_{b\bar{b}}, m_{b\bar{b}}$).
   - 1D histogram suite formatted with `mplhep` and weighted by Monte Carlo weights ($w_i$).
   - 2D correlation histogram ($\Delta R_{b\bar{b}}$ vs. $p_T^Z$) with theoretical boost guide overlay ($\Delta R_{b\bar{b}} \approx 2m_Z / p_T^Z$).

## Technical Parameters

- **MadGraph Release**: MadGraph5_aMC@NLO `v3.5.16`.
- **Process Syntax**: `import model sm`, `generate p p > z j, z > b b~`, `output Zbbj_LO`, `launch Zbbj_LO`.
- **Collider Center-of-Mass Energy**: $\sqrt{s} = 13\text{ TeV}$ (`ebeam1 = 6500.0 GeV`, `ebeam2 = 6500.0 GeV`).
- **Boost Cut**: $p_T^j \ge 150.0\text{ GeV}$ / $p_{T,\text{min}}^Z \ge 150.0\text{ GeV}$ (`ptj = 150.0`, `ptZmin = 150.0` in `cards/zbbj_run_card.dat`).
- **Production Event Count**: $N = 1000$ unweighted events.
