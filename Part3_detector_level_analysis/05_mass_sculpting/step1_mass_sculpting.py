#!/usr/bin/env python3
"""
Exercise 5 — Step 1: Mass Sculpting Comparison
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
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not os.path.exists(qcd_path):
        print(f"[Note]: ROOT file {qcd_path} not found.")
        return
        
    branches = [
        "largeRjet_pt_NOSYS",
        "largeRjet_m_NOSYS",
        "largeRjet_ParT_W_score",
        "largeRjet_ParT_W_massDec_score"
    ]
    
    events = uproot.open(qcd_path)["reco"].arrays(branches, entry_stop=25000)
    
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), 0.0))
    score_std = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_ParT_W_score"]), -1.0))
    score_dec = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_ParT_W_massDec_score"]), -1.0))
    
    mask = (pt > 250.0) & (mass > 0.0) & (score_std >= 0.0) & (score_dec >= 0.0)
    pt, mass, score_std, score_dec = pt[mask], mass[mask], score_std[mask], score_dec[mask]
    
    # ----------------------------------------------------
    # EXAMPLE: Standard Tagger Score Quantile Cut
    # ----------------------------------------------------
    cut_std_80 = score_std > np.percentile(score_std, 80.0)
    
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.hist(mass, bins=40, range=(0, 250), density=True, histtype='step', linewidth=2, color='black', label='Inclusive QCD')
    ax.hist(mass[cut_std_80], bins=40, range=(0, 250), density=True, histtype='step', linewidth=2, color='crimson', label='Standard Score > 80% Quantile')
    ax.set_xlabel("QCD Jet Mass [GeV]")
    ax.set_ylabel("Normalized Density")
    ax.set_title("Standard ParT W-Tagger (Mass Sculpted)")
    ax.legend()
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("example_sculpting.png", dpi=200)
    print("Saved example plot to 'example_sculpting.png'.")

    # ====================================================
    # TODO: EXERCISE TASK 1
    # ====================================================
    # Task Instructions:
    # 1. Apply mass-decorrelated score cuts: cut_dec_80 = score_dec > np.percentile(score_dec, 80.0).
    # 2. Create a 2-panel figure comparing Standard Tagger mass sculpting vs. Mass-Decorrelated Tagger.
    # 3. Add labels, legends, and save figure to 'exercise5_mass_sculpting.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Create 2-panel comparison figure

if __name__ == "__main__":
    main()
