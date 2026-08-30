#!/usr/bin/env python3
"""
Solution: Exercise 5 — Step 1: Mass Sculpting Comparison
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
    # ----------------------------------------------------
    # Setup: Figure styling & metadata loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and reads Dijet QCD background path.
    # 2. Data type/shape: Python string filepath.
    # 3. HEP meaning: Accesses background QCD sample to study tagger-induced mass sculpting artifacts.
    # 4. Common beginner mistake: Testing mass sculpting on signal samples instead of falling background.
    setup_mplhep_style()
    metadata = load_metadata()
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not os.path.exists(qcd_path):
        print(f"[Note]: ROOT file {qcd_path} not found.")
        return
        
    # ----------------------------------------------------
    # Data Loading: Background Jet Mass & Dual Scores
    # ----------------------------------------------------
    # 1. What code does: Loads jet mass, standard ParT score, and mass-decorrelated ParT score for QCD dijets (entry_stop=25000).
    # 2. Data type/shape: 1D NumPy arrays of valid floats for mass (GeV) and classifier scores.
    # 3. HEP meaning: Compares standard tagger vs mass-decorrelated tagger effects on background mass shape.
    # 4. Common beginner mistake: Comparing mass shapes with different total selection efficiencies.
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
    # Explanation:
    # 1. What code does: Applies 80th percentile score cut on standard ParT W-tagger.
    # 2. Data type/shape: 1D Boolean mask of shape (N_events,).
    # 3. HEP meaning: Demonstrates mass sculpting (fake peak creation) on smooth QCD background.
    # 4. Beginner mistake: Testing mass sculpting on signal MC instead of background QCD.
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
    plt.savefig("exercise5_step1_example_sculpting.png", dpi=200)
    print("Saved example plot to 'exercise5_step1_example_sculpting.png'.")

    # ====================================================
    # SOLUTION: EXERCISE TASK 1
    # ====================================================
    # Explanation:
    # 1. What code does: Plots 2-panel comparison of standard tagger vs mass-decorrelated tagger.
    # 2. Data type/shape: matplotlib 2-panel figure.
    # 3. HEP meaning: Shows how mass decorrelation prevents fake background peaking artifacts.
    # 4. Beginner mistake: Using un-normalized plots when comparing background mass distribution shapes.
    cut_dec_80 = score_dec > np.percentile(score_dec, 80.0)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(mass, bins=40, range=(0, 250), density=True, histtype='step', linewidth=2, color='black', label='Inclusive QCD')
    axes[0].hist(mass[cut_std_80], bins=40, range=(0, 250), density=True, histtype='step', linewidth=2, color='crimson', label='Standard (Sculpted)')
    axes[0].set_xlabel("QCD Jet Mass [GeV]")
    axes[0].set_ylabel("Normalized Density")
    axes[0].set_title("Standard ParT W-Tagger")
    axes[0].legend()
    axes[0].grid(True, alpha=0.4)
    
    axes[1].hist(mass, bins=40, range=(0, 250), density=True, histtype='step', linewidth=2, color='black', label='Inclusive QCD')
    axes[1].hist(mass[cut_dec_80], bins=40, range=(0, 250), density=True, histtype='step', linewidth=2, color='dodgerblue', label='Mass-Decorrelated')
    axes[1].set_xlabel("QCD Jet Mass [GeV]")
    axes[1].set_ylabel("Normalized Density")
    axes[1].set_title("Mass-Decorrelated ParT W-Tagger")
    axes[1].legend()
    axes[1].grid(True, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig("exercise5_step1_mass_sculpting_sol.png", dpi=300)
    print("Saved solution plot to 'exercise5_step1_mass_sculpting_sol.png'.")

if __name__ == "__main__":
    main()
