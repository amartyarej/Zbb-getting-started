#!/usr/bin/env python3
"""
Exercise 3 — Step 1: Pearson Matrix & Non-Linear Distance Correlation (OPTIONAL)
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import load_metadata, compute_distance_correlation

def main():
    # ----------------------------------------------------
    # Setup: Dataset metadata loading
    # ----------------------------------------------------
    # 1. What code does: Reads sample path for Z->bb MC from metadata JSON.
    # 2. Data type/shape: Python string filepath.
    # 3. HEP meaning: Provides dataset reference path for correlation studies.
    # 4. Common beginner mistake: Proceeding without checking file existence.
    metadata = load_metadata()
    file_path = metadata["samples"]["Zbb"]["file_path"]
    
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: Kinematics, Substructure, & ML Scores
    # ----------------------------------------------------
    # 1. What code does: Reads pT, mass, tau1, tau2, ParT score, mu from 'reco' tree (first 15,000 events via entry_stop=15000); cleans NaN values.
    # 2. Data type/shape: 1D NumPy arrays of valid floats.
    # 3. HEP meaning: Extracts multi-dimensional observable space to calculate linear and non-linear correlation metrics.
    # 4. Common beginner mistake: Calculating correlation coefficients on uncleaned arrays containing NaN values.
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
    # Subsample size N=2000 chosen due to O(N^2) distance matrix memory/CPU scaling in dcor
    n_calc = 10000
    r_pt_mass = np.corrcoef(pt[:n_calc], mass[:n_calc])[0, 1]
    print(f"Pearson Correlation r(pT, Mass) [N={n_calc}]: {r_pt_mass:.4f}")

    # ====================================================
    # TODO: EXERCISE TASK 1
    # ====================================================
    # Task Instructions:
    # 1. Compute Distance Correlation dcor(pT, Mass) using compute_distance_correlation(pt[:n_calc], mass[:n_calc]).
    # 2. Compute Distance Correlation dcor(Mass, ParT Score) using compute_distance_correlation(mass[:n_calc], score[:n_calc]).
    # 3. Print both distance correlation values alongside their Pearson correlation values.
    # 4. Explain why distance correlation is sensitive to non-linear relationships that Pearson misses!
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Compute and print distance correlations vs Pearson r

if __name__ == "__main__":
    main()
