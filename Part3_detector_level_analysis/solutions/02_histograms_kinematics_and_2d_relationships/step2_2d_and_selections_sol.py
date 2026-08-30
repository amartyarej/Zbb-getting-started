#!/usr/bin/env python3
"""
Solution: Exercise 2 — Step 2: 2D Phase Space and Selection Cut Effects
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, setup_mplhep_style, MAX_EVENTS

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
    # 1. What code does: Reads jet pT, eta, mass (first MAX_EVENTS events via entry_stop=MAX_EVENTS); converts MeV to GeV; cleans NaN entries.
    # 2. Data type/shape: 1D NumPy arrays of valid floats.
    # 3. HEP meaning: Extracts jet kinematics to construct 2D pT-vs-mass correlations and evaluate kinematic cuts.
    # 4. Common beginner mistake: Forgetting that cutflow step statistics change when cut thresholds are modified.
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays(["largeRjet_pt_NOSYS", "largeRjet_eta", "largeRjet_m_NOSYS"], entry_stop=MAX_EVENTS)
    
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), np.nan))
    eta = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_eta"]), np.nan))
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), np.nan))
    
    valid = ~np.isnan(pt) & ~np.isnan(eta) & ~np.isnan(mass)
    pt, eta, mass = pt[valid], eta[valid], mass[valid]
    
    # ----------------------------------------------------
    # EXAMPLE: Multidimensional Cut Effect on 1D Mass Spectrum
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Applies pT > 250 GeV and |eta| < 2.0 cuts and overlays 1D mass spectrum.
    # 2. Data type/shape: 1D Boolean mask of shape (N_events,).
    # 3. HEP meaning: Demonstrates how cutting in 1D phase space shifts correlated mass shapes.
    # 4. Beginner mistake: Assuming pT cuts leave mass distributions unchanged.
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
    plt.savefig("exercise2_step2_example_mass_cut_effect.png", dpi=200)
    print("Saved example plot to 'exercise2_step2_example_mass_cut_effect.png'.")

    # ====================================================
    # SOLUTION: EXERCISE TASK 2
    # ====================================================
    # Explanation:
    # 1. What code does: Creates 2D histogram of Mass vs pT with cut line.
    # 2. Data type/shape: 2D histogram array.
    # 3. HEP meaning: Exposes kinematic phase-space boundary lines and correlations.
    # 4. Beginner mistake: Omitting colorbars or threshold cut lines on 2D plots.
    fig, ax = plt.subplots(figsize=(7, 5))
    h2d = ax.hist2d(pt, mass, bins=[30, 30], range=[[200, 800], [0, 300]], cmap='viridis')
    ax.axvline(250.0, color='red', linestyle='--', linewidth=2, label=r'Cut $p_T = 250$ GeV')
    ax.set_xlabel(r"Large-R Jet $p_T$ [GeV]")
    ax.set_ylabel("Large-R Jet Mass [GeV]")
    ax.set_title(r"2D Phase Space Solution: Jet Mass vs $p_T$")
    ax.legend()
    fig.colorbar(h2d[3], ax=ax, label="Jet Candidates")
    
    plt.tight_layout()
    plt.savefig("exercise2_step2_2d_phase_space_sol.png", dpi=300)
    print("Saved solution plot to 'exercise2_step2_2d_phase_space_sol.png'.")

if __name__ == "__main__":
    main()
