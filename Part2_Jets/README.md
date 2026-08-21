# Part 2 — Jet Clustering, Radius Dependence, and Subjet Exploration

This directory contains the standalone package for **Part 2** of the experimental High-Energy Physics (HEP) Monte Carlo & Analysis Training Series.

## Overview & Pedagogical Purpose

Part 2 guides you from constituent 4-vector arrays (detector-level EMPFlow & generator-level Truth) to reconstructed jets, sequential recombination algorithms ($anti-k_t$, $k_t$, Cambridge/Aachen), radius parameter scans ($R=0.2, 0.4, 0.8, 1.0$), and large-$R$ subjet reclustering for boosted $Z \to b\bar{b}$ hadronic decays:

```text
Constituent Arrays (EMPFlow/Truth) ──> Sequential Recombination ──> Multi-Radius Scan ──> Subjet Reclustering ──> Boosted Substructure
```

In this module, you will analyze a 10-event Large Hadron Collider (LHC) $Z \to b\bar{b}$ dataset containing charged and neutral final-state constituent particles:
```text
data/Zbb_RawConst.root  (TTree: "analysis")
```

## Execution Environment Modes (Google Colab vs. Local Machine)

The notebook supports dual execution modes selectable via the `USE_COLAB` flag at the top of Step 1:

- **Google Colab Mode (`USE_COLAB = True`)**: Mounts Google Drive at `/content/drive` for persistent storage and installs required HEP analysis packages (`uproot`, `awkward`, `vector`, `fastjet`, `mplhep`).
- **Local Machine Mode (`USE_COLAB = False`)**: Runs locally without Google Drive or Colab dependencies. You can specify a base directory path by setting `LOCAL_OUTPUT_DIR = "/path/to/base/dir"` (or leave as `None` to use your current working directory), reading `data/Zbb_RawConst.root` directly.

## Directory Organization

All Part 2 deliverables are strictly contained in this `Part2_Jets/` folder:

```text
Part2_Jets/
├── Part2_01_jet_clustering_and_subjets.ipynb   # Notebook 01 (Jet Clustering, Radius Scan, & Subjet Reclustering)
├── README.md                                   # Part 2 documentation
├── checksums.sha256                            # SHA-256 integrity checksums
└── data/
    └── Zbb_RawConst.root                       # 10-event hadronic Z->bb ROOT dataset (TTree: "analysis")
```

*(Note: Unified Python package requirements are maintained at the repository root [`requirements.txt`](../requirements.txt)).*

## Notebook Sequence

1. **`Part2_01_jet_clustering_and_subjets.ipynb`**: Learn hadronic physics foundations, inspect detector-level (EMPFlow) and truth-level constituent arrays, run sequential recombination jet algorithms ($anti-k_t$, $k_t$, C/A), perform radius scans ($R=0.2, 0.4, 0.8, 1.0$), and recluster $R=1.0$ large-$R$ jets into $N=2$ subjets to reveal boosted $Z \to b\bar{b}$ decay structure.

## Technical Parameters & Dataset Schema

- **Dataset File**: `data/Zbb_RawConst.root`
- **TTree Name**: `analysis` (10 events)
- **EMPFlow Branches**: `constituents_EMPFlow_pt`, `constituents_EMPFlow_eta`, `constituents_EMPFlow_phi`, `constituents_EMPFlow_m`, `constituents_EMPFlow_e`, `constituents_EMPFlow_pdgId`, `constituents_EMPFlow_charge`
- **Truth Branches**: `constituents_Truth_pt`, `constituents_Truth_eta`, `constituents_Truth_phi`, `constituents_Truth_m`, `constituents_Truth_e`, `constituents_Truth_pdgId`, `constituents_Truth_charge`
- **Jet Algorithms**: $anti-k_t$ ($p=-1$), $k_t$ ($p=+1$), Cambridge/Aachen ($p=0$)
- **Radius Parameters**: $R \in \{0.2, 0.4, 0.8, 1.0\}$
- **Reporting Cut**: Jet $p_T > 20.0\text{ GeV}$
