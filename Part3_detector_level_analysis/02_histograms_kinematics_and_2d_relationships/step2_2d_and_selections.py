#!/usr/bin/env python3
"""
Exercise 2 — Step 2: 2D Phase Space and Selection Cut Effects
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
    # ----------------------------------------------------
    # Setup: Figure styling & metadata loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and reads Z->bb sample path.
    # 2. Data type/shape: Python dict and string filepath.
    # 3. HEP meaning: Prepares plot parameters for 2D phase-space visualization.
    # 4. Common beginner mistake: Proceeding without checking ROOT file existence.
    setup_mplhep_style()
    metadata = load_metadata()
    file_path = metadata["samples"]["Zbb"]["file_path"]
    
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: Kinematics (pT, eta, mass) & NaN Cleanup
    # ----------------------------------------------------
    # 1. What code does: Reads jet pT, eta, mass (first 20,000 events via entry_stop=20000); converts MeV to GeV; cleans NaN entries.
    # 2. Data type/shape: 1D NumPy arrays of valid floats for pT, eta, mass.
    # 3. HEP meaning: Extracts reconstructed leading jet four-vector components for cut evaluation.
    # 4. Common beginner mistake: Evaluating eta cut on uncleaned arrays containing None values.
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays(["largeRjet_pt_NOSYS", "largeRjet_eta", "largeRjet_m_NOSYS"], entry_stop=20000)
    
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), np.nan))
    eta = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_eta"]), np.nan))
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), np.nan))
    
    valid = ~np.isnan(pt) & ~np.isnan(eta) & ~np.isnan(mass)
    pt, eta, mass = pt[valid], eta[valid], mass[valid]
    
    # ----------------------------------------------------
    # EXAMPLE: Multidimensional Cut Effect on 1D Mass Spectrum
    # ----------------------------------------------------
    cut_mask = (pt > 250.0) & (np.abs(eta) < 2.0)
    
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.hist(mass, bins=40, range=(0, 300), density=True, histtype='step', linewidth=2, color='black', label='Inclusive')
    ax.hist(mass[cut_mask], bins=40, range=(0, 300), density=True, histtype='step', linewidth=2, color='dodgerblue', label=r'$p_T > 250$ GeV, $|\eta| < 2.0$')
    ax.set_xlabel("Large-R Jet Mass [GeV]")
    ax.set_ylabel("Normalized Density")
    ax.set_title("Multidimensional Selection Cut Effect")
    ax.legend()
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("example_mass_cut_effect.png", dpi=200)
    print("Saved example plot to 'example_mass_cut_effect.png'.")

    # ====================================================
    # TODO: EXERCISE TASK 2
    # ====================================================
    # Task Instructions:
    # 1. Create a 2D histogram of Large-R Jet Mass vs. Jet pT using plt.hist2d().
    # 2. Set range to pT in [200, 800] GeV and Mass in [0, 300] GeV with [30, 30] bins.
    # 3. Add a vertical dashed line at pT = 250 GeV representing the selection cut boundary.
    # 4. Add a colorbar with label 'Jet Candidates'.
    # 5. Save figure to 'exercise2_2d_phase_space.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Create 2D histogram of Mass vs pT with cut line and colorbar

if __name__ == "__main__":
    main()
