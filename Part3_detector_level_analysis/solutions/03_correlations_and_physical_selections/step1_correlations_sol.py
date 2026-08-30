#!/usr/bin/env python3
"""
Solution: Exercise 3 — Step 1: Pearson Matrix & Non-Linear Distance Correlation (OPTIONAL)
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, compute_distance_correlation

def main():
    metadata = load_metadata()
    file_path = metadata["samples"]["Zbb"]["file_path"]
    
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        return
        
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays([
        "largeRjet_pt_NOSYS", "largeRjet_m_NOSYS",
        "largeRjet_Tau1_wta", "largeRjet_Tau2_wta",
        "largeRjet_ParT_W_massDec_score", "actualInteractionsPerCrossing"
    ], entry_stop=15000)
    
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), np.nan))
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), np.nan))
    score = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_ParT_W_massDec_score"]), np.nan))
    
    valid = ~np.isnan(pt) & ~np.isnan(mass) & ~np.isnan(score)
    pt, mass, score = pt[valid], mass[valid], score[valid]
    
    # ----------------------------------------------------
    # EXAMPLE: Computing Pearson Linear Correlation Coefficient
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Computes Pearson r_XY = cov(X,Y) / (sigma_X * sigma_Y).
    # 2. Data type/shape: Float scalar in [-1, 1].
    # 3. HEP meaning: Measures linear association between reconstructed observables.
    # 4. Beginner mistake: Assuming r_XY = 0 proves zero dependence.
    r_pt_mass = np.corrcoef(pt, mass)[0, 1]
    r_mass_score = np.corrcoef(mass, score)[0, 1]
    print(f"Pearson Correlation r(pT, Mass): {r_pt_mass:.4f}")

    # ====================================================
    # SOLUTION: EXERCISE TASK 1
    # ====================================================
    # Explanation:
    # 1. What code does: Computes distance correlation dcor(X, Y) for non-linear dependence.
    # 2. Data type/shape: Float scalar in [0, 1].
    # 3. HEP meaning: Detects non-linear dependencies missed by Pearson linear r_XY.
    # 4. Beginner mistake: Using distance correlation as a selection optimization statistic.
    dcor_pt_mass = compute_distance_correlation(pt[:2000], mass[:2000])
    dcor_mass_score = compute_distance_correlation(mass[:2000], score[:2000])
    
    print("=" * 60)
    print("SOLUTION: Exercise 3 — Step 1: Distance Correlation")
    print("=" * 60)
    print(f"r(pT, Mass): {r_pt_mass:.4f} | dcor(pT, Mass): {dcor_pt_mass:.4f}")
    print(f"r(Mass, ParT Score): {r_mass_score:.4f} | dcor(Mass, Score): {dcor_mass_score:.4f}")

if __name__ == "__main__":
    main()
