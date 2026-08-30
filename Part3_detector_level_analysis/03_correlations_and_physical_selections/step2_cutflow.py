#!/usr/bin/env python3
"""
Exercise 3 — Step 2: Baseline Selection Cutflow Table (OPTIONAL)
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import load_metadata

def main():
    metadata = load_metadata()
    file_path = metadata["samples"]["Zbb"]["file_path"]
    
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        return
        
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays([
        "largeRjet_pt_NOSYS", "largeRjet_m_NOSYS",
        "largeRjet_Tau1_wta", "largeRjet_Tau2_wta"
    ], entry_stop=20000)
    
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
    n_initial = len(pt)
    cut1_mask = pt > 250.0
    print(f"Initial Events:       {n_initial:8d} (100.00%)")
    print(f"Cut 1 (pT > 250 GeV): {np.sum(cut1_mask):8d} ({np.sum(cut1_mask)/n_initial*100:6.2f}%)")

    # ====================================================
    # TODO: EXERCISE TASK 2
    # ====================================================
    # Task Instructions:
    # 1. Define Cut 2: cut1_mask & (mass > 50.0) & (mass < 200.0).
    # 2. Define Cut 3: cut2_mask & (tau21 < 0.45).
    # 3. Compute passing event counts and percentage efficiencies for Cut 2 and Cut 3.
    # 4. Print a clean, formatted cutflow table!
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Calculate Cut 2 and Cut 3 masks and print cutflow table

if __name__ == "__main__":
    main()
