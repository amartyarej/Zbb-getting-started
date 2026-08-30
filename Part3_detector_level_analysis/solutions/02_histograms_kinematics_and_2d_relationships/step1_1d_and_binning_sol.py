#!/usr/bin/env python3
"""
Solution: Exercise 2 — Step 1: 1D Kinematics, Binning Pedagogy, and Log Axes
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
    events = tree.arrays(["largeRjet_pt_NOSYS", "largeRjet_m_NOSYS"], entry_stop=20000)
    
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), np.nan))
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), np.nan))
    
    valid = ~np.isnan(pt) & ~np.isnan(mass)
    pt, mass = pt[valid], mass[valid]
    
    # ----------------------------------------------------
    # EXAMPLE: Comparing Fine vs Coarse Binning
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Plots jet mass with 5 GeV vs 20 GeV binning.
    # 2. Data type/shape: matplotlib Axes subplot object.
    # 3. HEP meaning: Demonstrates visual resolution changes without altering physical conclusion.
    # 4. Beginner mistake: Drawing new physical conclusions purely from bin width choice.
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
    # SOLUTION: EXERCISE TASK 1
    # ====================================================
    # Explanation:
    # 1. What code does: Plots jet pT spectrum on linear vs log y-axis.
    # 2. Data type/shape: matplotlib Axes subplot object with set_yscale('log').
    # 3. HEP meaning: Exponentially falling high-pT tail requires logarithmic scale for visual inspection.
    # 4. Beginner mistake: Truncating falling tail data on linear scale plots.
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Linear scale
    axes[0].hist(pt, bins=40, range=(200, 1000), color='crimson', alpha=0.7, edgecolor='black')
    axes[0].set_xlabel(r"Large-R Jet $p_T$ [GeV]")
    axes[0].set_ylabel("Jets / Bin")
    axes[0].set_title("Linear Scale $p_T$ Spectrum")
    axes[0].grid(True, alpha=0.4)
    
    # Log scale
    axes[1].hist(pt, bins=40, range=(200, 1000), color='crimson', alpha=0.7, edgecolor='black')
    axes[1].set_yscale('log')
    axes[1].set_xlabel(r"Large-R Jet $p_T$ [GeV]")
    axes[1].set_ylabel("Jets / Bin (Log Scale)")
    axes[1].set_title("Logarithmic Scale $p_T$ Spectrum")
    axes[1].grid(True, which='both', linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    plt.savefig("exercise2_pt_logscale_sol.png", dpi=300)
    print("Saved solution plot to 'exercise2_pt_logscale_sol.png'.")

if __name__ == "__main__":
    main()
