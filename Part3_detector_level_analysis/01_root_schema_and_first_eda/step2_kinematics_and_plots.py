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
from helpers import load_metadata, setup_mplhep_style, MAX_EVENTS

def main():
    # ----------------------------------------------------
    # Setup: Figure styling & metadata loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and reads sample file path.
    # 2. Data type/shape: Python string filepath.
    # 3. HEP meaning: Standardizes plot typography and layout across detector analyses.
    # 4. Common beginner mistake: Proceeding without verifying local ROOT file existence.
    setup_mplhep_style()
    metadata = load_metadata()
    file_path = metadata["samples"]["Zbb"]["file_path"]
    
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: Columnar TTree extraction & Unit Conversion
    # ----------------------------------------------------
    # 1. What code does: Reads pileup mu and jet pT from 'reco' tree (first 10,000 events via entry_stop=10000); converts pT from MeV to GeV.
    # 2. Data type/shape: mu -> 1D array of shape (10000,); largeR_pt -> Jagged array of shape (10000, var_jets).
    # 3. HEP meaning: Loads reconstructed collision physics observables into memory for exploratory analysis.
    # 4. Common beginner mistake: Forgetting to divide ROOT pT by 1000.0 (MeV to GeV), or omitting entry_stop during prototyping.
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays([
        "actualInteractionsPerCrossing",
        "largeRjet_pt_NOSYS"
    ], entry_stop=MAX_EVENTS)
    
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
    ax.set_title("Actual Pileup in Z->bb sample")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("exercise1_step2_example_mu_distribution.png", dpi=200)
    print("Saved example plot to 'exercise1_step2_example_mu_distribution.png'.")

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
    # 4. Save your figure to 'exercise1_step2_plots.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Calculate multiplicity and flat pT
    # TODO: Create 3-panel figure and plot histograms
    # TODO: Add proper x/y labels, titles, legends, and save figure

if __name__ == "__main__":
    main()
