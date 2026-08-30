#!/usr/bin/env python3
"""
Solution: Exercise 3 — Step 2: Baseline Selection Cutflow Table (OPTIONAL)
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, MAX_EVENTS

def main():
    # ----------------------------------------------------
    # Setup: Dataset metadata loading
    # ----------------------------------------------------
    # 1. What code does: Reads sample path for Z->bb MC from metadata JSON.
    # 2. Data type/shape: Python string filepath.
    # 3. HEP meaning: Accesses sample reference for baseline cutflow evaluation.
    # 4. Common beginner mistake: Hardcoding absolute file paths.
    metadata = load_metadata()
    file_path = metadata["samples"]["Zbb"]["file_path"]
    
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: Kinematics, Substructure (Tau1, Tau2) & Ratio
    # ----------------------------------------------------
    # 1. What code does: Reads pT, mass, tau1, tau2 (first MAX_EVENTS events via entry_stop=MAX_EVENTS); converts MeV to GeV; computes N-subjettiness ratio tau21 = tau2/tau1.
    # 2. Data type/shape: 1D NumPy arrays of valid floats.
    # 3. HEP meaning: Tau21 measures 2-prong vs 1-prong jet substructure topology.
    # 4. Common beginner mistake: Dividing tau2 by tau1 without checking for tau1 == 0 (division by zero).
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays([
        "largeRjet_pt_NOSYS", "largeRjet_m_NOSYS",
        "largeRjet_Tau1_wta", "largeRjet_Tau2_wta"
    ], entry_stop=MAX_EVENTS)
    
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), np.nan))
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), np.nan))
    tau1 = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_Tau1_wta"]), np.nan))
    tau2 = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_Tau2_wta"]), np.nan))
    
    valid = ~np.isnan(pt) & ~np.isnan(mass)
    pt, mass, tau1, tau2 = pt[valid], mass[valid], tau1[valid], tau2[valid]
    tau21 = np.where(tau1 > 0, tau2 / tau1, np.nan)
    
    # ----------------------------------------------------
    # EXAMPLE: Evaluating Sequential Selection Cuts
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Evaluates sequential baseline cuts and prints a cutflow yield table.
    # 2. Data type/shape: Integer event counts and float efficiency percentages.
    # 3. HEP meaning: Tracks event retention through successive baseline selection criteria.
    # 4. Beginner mistake: Forgetting whether cutflow yields represent raw counts or luminosity-weighted yields.
    n_initial = len(pt)
    cut1_mask = pt > 250.0
    print(f"Initial Events:       {n_initial:8d} (100.00%)")
    print(f"Cut 1 (pT > 250 GeV): {np.sum(cut1_mask):8d} ({np.sum(cut1_mask)/n_initial*100:6.2f}%)")

    # ====================================================
    # SOLUTION: EXERCISE TASK 2
    # ====================================================
    # Explanation:
    # 1. What code does: Evaluates Cut 2 (mass window) and Cut 3 (tau21 substructure cut).
    # 2. Data type/shape: Boolean masks and integer event counts.
    # 3. HEP meaning: Isolates candidate signal region while tracking event efficiency.
    # 4. Beginner mistake: Applying non-cumulative cuts instead of sequential masks.
    cut2_mask = cut1_mask & (mass > 50.0) & (mass < 200.0)
    cut3_mask = cut2_mask & (tau21 < 0.45)
    
    print("=" * 60)
    print("SOLUTION: Exercise 3 — Step 2: Cutflow Table")
    print("=" * 60)
    print(f"Initial Events:              {n_initial:8d} (100.00%)")
    print(f"Cut 1 (pT > 250 GeV):        {np.sum(cut1_mask):8d} ({np.sum(cut1_mask)/n_initial*100:6.2f}%)")
    print(f"Cut 2 (50 < Mass < 200 GeV): {np.sum(cut2_mask):8d} ({np.sum(cut2_mask)/n_initial*100:6.2f}%)")
    print(f"Cut 3 (tau21 < 0.45):        {np.sum(cut3_mask):8d} ({np.sum(cut3_mask)/n_initial*100:6.2f}%)")

if __name__ == "__main__":
    main()
