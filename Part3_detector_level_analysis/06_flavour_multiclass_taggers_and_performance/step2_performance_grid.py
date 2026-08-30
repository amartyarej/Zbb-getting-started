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
    metadata = load_metadata()
    zbb_path = metadata["samples"]["Zbb"]["file_path"]
    wqq_path = metadata["samples"]["Wqq"]["file_path"]
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not (os.path.exists(zbb_path) and os.path.exists(wqq_path) and os.path.exists(qcd_path)):
        print("[Note]: ROOT files not available locally.")
        return
        
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
    # 2. Evaluate selection efficiency (mistag rate) on Wqq and QCD at D_bb > 0.60 threshold.
    # 3. Print a 3-class efficiency grid table comparing Zbb, Wqq, and QCD!
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Compute Wqq and QCD mistag rates and print efficiency grid

if __name__ == "__main__":
    main()
