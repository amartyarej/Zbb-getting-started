#!/usr/bin/env python3
"""
Exercise 1 — Step 2: Kinematic Spectrum & Multiplicity Plotting
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    # TODO: EXERCISE TASK 2
    # ====================================================
    # Task Instructions:
    # 1. Compute Large-R jet multiplicity per event using ak.num(largeR_pt).
    # 2. Flatten Large-R jet pT spectrum using ak.flatten(largeR_pt).
    # 3. Create a 3-panel figure (1 row, 3 columns) using plt.subplots(1, 3, figsize=(15, 4.5)):
    #    - Panel 1: Pileup mu (range 10 to 70).
    #    - Panel 2: Large-R jet multiplicity (integer binning from 0 to 6).
    #    - Panel 3: Inclusive Large-R jet pT spectrum (range 200 to 1000 GeV, 40 bins).
    # 4. Save your figure to 'exercise1_plots.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Calculate multiplicity and flat pT
    # TODO: Create 3-panel figure and plot histograms
    # TODO: Add proper x/y labels, titles, legends, and save figure

if __name__ == "__main__":
    main()
