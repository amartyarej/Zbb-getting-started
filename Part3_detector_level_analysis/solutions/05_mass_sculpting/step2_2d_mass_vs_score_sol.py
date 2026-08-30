#!/usr/bin/env python3
"""
Solution: Exercise 5 — Step 2: 2D Diagnostic: Jet Mass vs Tagger Score
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, eval_part_wp, setup_mplhep_style

def main():
    # ----------------------------------------------------
    # Setup: Figure styling & metadata loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and reads Dijet QCD background path.
    # 2. Data type/shape: Python string filepath.
    # 3. HEP meaning: Prepares sample reference for 2D mass vs score diagnostic plots.
    # 4. Common beginner mistake: Proceeding without checking ROOT file existence.
    setup_mplhep_style()
    metadata = load_metadata()
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not os.path.exists(qcd_path):
        print(f"[Note]: ROOT file {qcd_path} not found.")
        return
        
    # ----------------------------------------------------
    # Data Loading: Jet Mass & Standard ParT Score
    # ----------------------------------------------------
    # 1. What code does: Loads jet mass and standard ParT W-tagger score for QCD dijets (entry_stop=25000).
    # 2. Data type/shape: 1D NumPy arrays of valid floats.
    # 3. HEP meaning: Provides 2D observable space (mass vs score) to inspect conditional quantiles.
    # 4. Common beginner mistake: Plotting 2D histograms without setting explicit bin boundaries.
    branches = ["largeRjet_pt_NOSYS", "largeRjet_m_NOSYS", "largeRjet_ParT_W_score"]
    
    events = uproot.open(qcd_path)["reco"].arrays(branches, entry_stop=25000)
    
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), 0.0))
    score_std = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_ParT_W_score"]), -1.0))
    
    mask = (pt > 250.0) & (mass > 0.0) & (score_std >= 0.0)
    pt, mass, score_std = pt[mask], mass[mask], score_std[mask]
    
    # ----------------------------------------------------
    # EXAMPLE: Plotting 2D Mass vs Tagger Score
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Plots 2D histogram of QCD Jet Mass vs Standard Tagger Score.
    # 2. Data type/shape: 2D histogram object with colorbar.
    # 3. HEP meaning: Diagnoses conditional mass dependence across score quantile slices.
    # 4. Beginner mistake: Ignoring score-mass correlation across different score ranges.
    fig, ax = plt.subplots(figsize=(6.5, 5))
    h2d = ax.hist2d(score_std, mass, bins=[30, 30], range=[[0, 1], [0, 250]], cmap='inferno')
    ax.set_xlabel("Standard ParT W-Tagger Score")
    ax.set_ylabel("QCD Jet Mass [GeV]")
    ax.set_title("2D Diagnostic: Jet Mass vs Tagger Score")
    fig.colorbar(h2d[3], ax=ax, label="QCD Events")
    plt.tight_layout()
    plt.savefig("exercise5_step2_example_2d_sculpting.png", dpi=200)
    print("Saved 2D diagnostic plot to 'exercise5_step2_example_2d_sculpting.png'.")

    # ====================================================
    # SOLUTION: EXERCISE TASK 2
    # ====================================================
    # Explanation:
    # 1. What code does: Computes actual 50% and 80% ParT working point thresholds and averages thresholds per mass bin.
    # 2. Data type/shape: matplotlib 2D histogram plot with overlaid threshold curves.
    # 3. HEP meaning: Visualizes mean score threshold profile across mass bins to diagnose mass correlation.
    # 4. Beginner mistake: Forgetting to plot 2D density alongside working point threshold curves.
    thresh_50 = eval_part_wp(pt, "ParT_W_50_NOSYS")
    thresh_80 = eval_part_wp(pt, "ParT_W_80_NOSYS")
    
    mass_bins = np.linspace(0, 250, 31)
    mass_centers = 0.5 * (mass_bins[:-1] + mass_bins[1:])
    
    t50_per_mass = []
    t80_per_mass = []
    
    for i in range(len(mass_bins) - 1):
        bin_mask = (mass >= mass_bins[i]) & (mass < mass_bins[i+1])
        if np.any(bin_mask):
            t50_per_mass.append(np.mean(thresh_50[bin_mask]))
            t80_per_mass.append(np.mean(thresh_80[bin_mask]))
        else:
            t50_per_mass.append(np.nan)
            t80_per_mass.append(np.nan)
            
    fig, ax = plt.subplots(figsize=(7, 5))
    h2d = ax.hist2d(score_std, mass, bins=[30, 30], range=[[0, 1], [0, 250]], cmap='inferno')
    ax.plot(t50_per_mass, mass_centers, color='orange', linestyle='--', linewidth=2, label='ParT 50% WP (mean per mass bin)')
    ax.plot(t80_per_mass, mass_centers, color='cyan', linestyle='--', linewidth=2, label='ParT 80% WP (mean per mass bin)')
    ax.set_xlabel("Standard ParT W-Tagger Score")
    ax.set_ylabel("QCD Jet Mass [GeV]")
    ax.set_title("2D Diagnostic Solution with Mass-Binned WP Threshold Curves")
    ax.legend()
    fig.colorbar(h2d[3], ax=ax, label="QCD Events")
    
    plt.tight_layout()
    plt.savefig("exercise5_step2_2d_diagnostic_sol.png", dpi=300)
    print("Saved solution plot to 'exercise5_step2_2d_diagnostic_sol.png'.")

if __name__ == "__main__":
    main()
