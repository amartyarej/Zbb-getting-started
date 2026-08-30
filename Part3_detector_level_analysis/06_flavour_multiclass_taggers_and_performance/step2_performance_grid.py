#!/usr/bin/env python3
"""
Exercise 6 — Step 2: Multi-Class Efficiency Grid Evaluation
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
    # ----------------------------------------------------
    # Setup: Dataset metadata loading
    # ----------------------------------------------------
    # 1. What code does: Reads sample paths for Zbb signal, Wqq background, and QCD dijet background.
    # 2. Data type/shape: Python string filepaths.
    # 3. HEP meaning: Prepares 3 distinct decay topology datasets to measure selection efficiency grid.
    # 4. Common beginner mistake: Proceeding without checking ROOT file accessibility across all 3 samples.
    metadata = load_metadata()
    zbb_path = metadata["samples"]["Zbb"]["file_path"]
    wqq_path = metadata["samples"]["Wqq"]["file_path"]
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not (os.path.exists(zbb_path) and os.path.exists(wqq_path) and os.path.exists(qcd_path)):
        print("[Note]: ROOT files not available locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: D_bb Discriminant Calculation across 3 Samples
    # ----------------------------------------------------
    # 1. What code does: Computes composite D_bb ratio scores for Zbb, Wqq, and QCD dijet events (entry_stop=15000).
    # 2. Data type/shape: 1D NumPy arrays of valid float D_bb values.
    # 3. HEP meaning: Provides classifier discriminant outputs across 3 physics processes (Zbb, Wqq, QCD) to measure signal efficiency and background mistag rates.
    # 4. Common pitfall: Comparing process metrics without applying identical kinematic cuts across samples.
    branches = [
        "largeRjet_pt_NOSYS", "largeRjet_GN3X_phbb", "largeRjet_GN3X_pWqq",
        "largeRjet_GN3X_pQCDbb", "largeRjet_GN3X_pQCDbx", "largeRjet_GN3X_pQCDcx", "largeRjet_GN3X_pQCDll"
    ]
    
    def get_dbb(fpath):
        events = uproot.open(fpath)["reco"].arrays(branches, entry_stop=15000)
        hbb = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_phbb"]), 0.0))
        wqq = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pWqq"]), 0.0))
        qcd = (ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDbb"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDbx"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDcx"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDll"]), 0.0)))
        denom = hbb + wqq + qcd
        return np.where(denom > 0, hbb / denom, 0.0)

    dbb_zbb = get_dbb(zbb_path)
    
    # ----------------------------------------------------
    # EXAMPLE: Evaluating Zbb Signal Selection Efficiency
    # ----------------------------------------------------
    thresh = 0.60
    eff_zbb = np.mean(dbb_zbb > thresh)
    print(f"Working Point Cut: D_bb > {thresh:.2f}")
    print(f"Z -> bb Selection Efficiency: {eff_zbb * 100:.2f}%")

    # ====================================================
    # TODO: EXERCISE TASK 2
    # ====================================================
    # Task Instructions:
    # 1. Compute D_bb scores for Wqq background and QCD background.
    # 2. Evaluate selection efficiency (mistag rate in %) and rejection factor (1 / mistag as a unitless number) for Wqq and QCD at D_bb > 0.60 threshold.
    # 3. Print a summary table listing Zbb signal efficiency (%), Wqq & QCD mistag rates (%), and Wqq & QCD rejection factors!
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Compute Wqq and QCD mistag rates (%) and rejection factors (number), then print summary table

if __name__ == "__main__":
    main()
