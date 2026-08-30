#!/usr/bin/env python3
"""
Solution: Exercise 6 — Step 2: Multi-Class Efficiency Grid Evaluation
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
    # 3. HEP meaning: Provides classifier discriminant outputs across 3 physics processes to build efficiency grid.
    # 4. Common beginner mistake: Comparing efficiency grid metrics without applying identical kinematic cuts across samples.
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
    # Explanation:
    # 1. What code does: Applies D_bb > 0.60 cut to evaluate signal selection efficiency.
    # 2. Data type/shape: Float efficiency fraction.
    # 3. HEP meaning: Fraction of Zbb signal events passing the tagger selection threshold.
    # 4. Beginner mistake: Evaluating efficiency without applying identical cuts to background samples.
    thresh = 0.60
    eff_zbb = np.mean(dbb_zbb > thresh)
    print(f"Working Point Cut: D_bb > {thresh:.2f}")
    print(f"Z -> bb Selection Efficiency: {eff_zbb * 100:.2f}%")

    # ====================================================
    # SOLUTION: EXERCISE TASK 2
    # ====================================================
    # Explanation:
    # 1. What code does: Computes D_bb scores, background mistag rates (in %), and rejection factors (as unitless numbers) for Wqq and QCD samples.
    # 2. Data type/shape: Summary performance table.
    # 3. HEP meaning: Process-dependent selection evaluation measures signal retention (%) vs background rejection factor (1 / mistag).
    # 4. Beginner mistake: Mixing up mistag rate (%) with background rejection (unitless number 1 / mistag).
    dbb_wqq = get_dbb(wqq_path)
    dbb_qcd = get_dbb(qcd_path)
    
    mistag_wqq = np.mean(dbb_wqq > thresh)
    mistag_qcd = np.mean(dbb_qcd > thresh)
    rej_wqq = 1.0 / mistag_wqq if mistag_wqq > 0 else np.nan
    rej_qcd = 1.0 / mistag_qcd if mistag_qcd > 0 else np.nan
    
    print("=" * 60)
    print("SOLUTION: Exercise 6 — Step 2: Selection Efficiency & Rejection Summary")
    print("=" * 60)
    print(f"Working Point Cut: D_bb > {thresh:.2f}")
    print(f"Z->bb Signal Efficiency:     {np.mean(dbb_zbb > thresh)*100:.2f}%")
    print(f"W->qq Background Mistag Rate: {mistag_wqq * 100:.2f}%")
    print(f"W->qq Background Rejection:   {rej_wqq:.1f}")
    print(f"QCD Background Mistag Rate:  {mistag_qcd * 100:.2f}%")
    print(f"QCD Background Rejection:     {rej_qcd:.1f}")

if __name__ == "__main__":
    main()
