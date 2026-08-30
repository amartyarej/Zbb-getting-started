#!/usr/bin/env python3
"""
Exercise 2 — Step 1: 1D Kinematics, Binning Pedagogy, and Log Axes
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
    events = tree.arrays(["largeRjet_pt_NOSYS", "largeRjet_m_NOSYS"], entry_stop=20000)
    
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), np.nan))
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), np.nan))
    
    valid = ~np.isnan(pt) & ~np.isnan(mass)
    pt, mass = pt[valid], mass[valid]
    
    # ----------------------------------------------------
    # EXAMPLE: Comparing Fine vs Coarse Binning
    # ----------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Fine binning
    axes[0].hist(mass, bins=80, range=(0, 400), density=True, histtype='step', color='crimson')
    axes[0].set_xlabel("Leading Large-R Jet Mass [GeV]")
    axes[0].set_ylabel("Normalized Density")
    axes[0].set_title("Fine Binning (5 GeV Width)")
    axes[0].grid(True, alpha=0.4)
    
    # Coarse binning
    axes[1].hist(mass, bins=20, range=(0, 400), density=True, histtype='step', color='navy')
    axes[1].set_xlabel("Leading Large-R Jet Mass [GeV]")
    axes[1].set_ylabel("Normalized Density")
    axes[1].set_title("Coarse Binning (20 GeV Width)")
    axes[1].grid(True, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig("example_binning_comparison.png", dpi=200)
    print("Saved example binning plot to 'example_binning_comparison.png'.")

    # ====================================================
    # TODO: EXERCISE TASK 1
    # ====================================================
    # Task Instructions:
    # 1. Plot the jet pT distribution on linear scale vs. logarithmic y-scale.
    # 2. Use range (200, 1000 GeV) with 40 bins.
    # 3. Create a 2-panel figure:
    #    - Panel 1: Linear y-axis scale.
    #    - Panel 2: Logarithmic y-axis scale (ax.set_yscale('log')).
    # 4. Save your plot to 'exercise2_pt_logscale.png'.
    # 5. Observe why the high-pT tail is visible only on the log scale!
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Create 2-panel figure for linear vs log pT spectrum

if __name__ == "__main__":
    main()
