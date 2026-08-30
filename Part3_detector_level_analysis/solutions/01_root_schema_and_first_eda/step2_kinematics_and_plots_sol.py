#!/usr/bin/env python3
"""
Solution: Exercise 1 — Step 2: Kinematic Spectrum & Multiplicity Plotting
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, setup_mplhep_style

def main():
    setup_mplhep_style()
    metadata = load_metadata()
    file_path = metadata["samples"]["Zbb"]["file_path"]
    
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        return
        
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays([
        "actualInteractionsPerCrossing",
        "largeRjet_pt_NOSYS"
    ], entry_stop=10000)
    
    mu = events["actualInteractionsPerCrossing"]
    largeR_pt = events["largeRjet_pt_NOSYS"] / 1000.0  # GeV
    
    # ----------------------------------------------------
    # EXAMPLE: Plotting Event-Level Pileup Proxy mu
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Plots 1D histogram of pileup parameter mu.
    # 2. Data type/shape: matplotlib Axes subplot object.
    # 3. HEP meaning: Shows distribution of average pp interactions per beam crossing.
    # 4. Beginner mistake: Forgetting axis labels or units on HEP plots.
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.hist(mu, bins=30, range=(10, 70), color='navy', alpha=0.7, edgecolor='black')
    ax.set_xlabel(r"Actual Interactions per Crossing $\mu$")
    ax.set_ylabel("Events")
    ax.set_title("Event-Level Pileup Proxy")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("example_mu_distribution.png", dpi=200)
    print("Saved example plot to 'example_mu_distribution.png'.")

    # ====================================================
    # SOLUTION: EXERCISE TASK 2
    # ====================================================
    # Explanation:
    # 1. What code does: Computes jet multiplicity with ak.num() and flattens array for pT spectrum.
    # 2. Data type/shape: n_largeR -> 1D array (N_events,); flat_largeR_pt -> 1D array (N_jets,).
    # 3. HEP meaning: Multiplicity tracks object counts; flat array creates inclusive jet spectrum.
    # 4. Beginner mistake: Mixing event-level counts with object-level jet spectra on the same y-axis.
    n_largeR_jets = ak.num(largeR_pt)
    flat_largeR_pt = ak.flatten(largeR_pt)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    
    # Panel 1: Pileup mu
    axes[0].hist(mu, bins=30, range=(10, 70), color='navy', alpha=0.7, edgecolor='black')
    axes[0].set_xlabel(r"Actual Interactions per Crossing $\mu$")
    axes[0].set_ylabel("Events")
    axes[0].set_title("Event-Level Pileup Proxy")
    axes[0].grid(True, linestyle='--', alpha=0.5)
    
    # Panel 2: Large-R Jet Multiplicity
    axes[1].hist(n_largeR_jets, bins=np.arange(-0.5, 6.5, 1), color='darkgreen', alpha=0.7, edgecolor='black')
    axes[1].set_xlabel("Large-R Jet Multiplicity")
    axes[1].set_ylabel("Events")
    axes[1].set_title("Large-R Jet Count per Event")
    axes[1].grid(True, linestyle='--', alpha=0.5)
    
    # Panel 3: Inclusive Large-R Jet pT
    axes[2].hist(flat_largeR_pt, bins=40, range=(200, 1000), color='crimson', alpha=0.7, edgecolor='black')
    axes[2].set_xlabel(r"Large-R Jet $p_T$ [GeV]")
    axes[2].set_ylabel("Jets / Bin")
    axes[2].set_title("Inclusive Large-R Jet $p_T$ Spectrum")
    axes[2].grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig("exercise1_plots_sol.png", dpi=300)
    print("Saved solution plot to 'exercise1_plots_sol.png'.")

if __name__ == "__main__":
    main()
