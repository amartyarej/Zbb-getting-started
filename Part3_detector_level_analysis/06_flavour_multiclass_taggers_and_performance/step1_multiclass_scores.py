#!/usr/bin/env python3
"""
Exercise 6 — Step 1: GN3X Multiclass Score Extraction & Composite Ratio Discriminant
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
    setup_mplhep_style()
    metadata = load_metadata()
    
    zbb_path = metadata["samples"]["Zbb"]["file_path"]
    
    if not os.path.exists(zbb_path):
        print(f"[Note]: ROOT file {zbb_path} is not accessible locally.")
        return
        
    branches = [
        "largeRjet_pt_NOSYS",
        "largeRjet_GN3X_phbb",
        "largeRjet_GN3X_pWqq",
        "largeRjet_GN3X_pQCDbb",
        "largeRjet_GN3X_pQCDbx",
        "largeRjet_GN3X_pQCDcx",
        "largeRjet_GN3X_pQCDll"
    ]
    
    events_zbb = uproot.open(zbb_path)["reco"].arrays(branches, entry_stop=15000)
    
    # ----------------------------------------------------
    # EXAMPLE: Extracting GN3X Probabilities & Summing QCD Classes
    # ----------------------------------------------------
    p_hbb = ak.to_numpy(ak.fill_none(ak.firsts(events_zbb["largeRjet_GN3X_phbb"]), 0.0))
    p_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_zbb["largeRjet_GN3X_pWqq"]), 0.0))
    p_qcd_bb = ak.to_numpy(ak.fill_none(ak.firsts(events_zbb["largeRjet_GN3X_pQCDbb"]), 0.0))
    p_qcd_bx = ak.to_numpy(ak.fill_none(ak.firsts(events_zbb["largeRjet_GN3X_pQCDbx"]), 0.0))
    p_qcd_cx = ak.to_numpy(ak.fill_none(ak.firsts(events_zbb["largeRjet_GN3X_pQCDcx"]), 0.0))
    p_qcd_ll = ak.to_numpy(ak.fill_none(ak.firsts(events_zbb["largeRjet_GN3X_pQCDll"]), 0.0))
    
    p_qcd_all = p_qcd_bb + p_qcd_bx + p_qcd_cx + p_qcd_ll
    
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.hist(p_hbb, bins=40, range=(0, 1), density=True, histtype='step', linewidth=2, color='crimson', label=r'Raw $P_{hbb}$')
    ax.hist(p_wqq, bins=40, range=(0, 1), density=True, histtype='step', linewidth=2, color='dodgerblue', label=r'Raw $P_{Wqq}$')
    ax.set_xlabel("GN3X Score")
    ax.set_ylabel("Normalized Density")
    ax.set_title(r"Raw GN3X Class Scores ($Z\to b\bar{b}$ MC)")
    ax.legend()
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("example_gn3x_raw.png", dpi=200)
    print("Saved example plot to 'example_gn3x_raw.png'.")

    # ====================================================
    # TODO: EXERCISE TASK 1
    # ====================================================
    # Task Instructions:
    # 1. Compute composite ratio discriminant: D_bb = P_hbb / (P_hbb + P_wqq + P_qcd_all).
    # 2. Extract D_bb for Zbb signal, Wqq background, and Dijet QCD background.
    # 3. Overlay the 1D D_bb score distributions for all 3 processes.
    # 4. Save figure to 'exercise6_dbb_score.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Compute D_bb ratio and plot 3-process overlay

if __name__ == "__main__":
    main()
