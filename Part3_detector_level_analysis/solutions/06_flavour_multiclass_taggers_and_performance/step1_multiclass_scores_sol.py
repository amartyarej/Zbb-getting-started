#!/usr/bin/env python3
"""
Solution: Exercise 6 — Step 1: GN3X Multiclass Score Extraction & Composite Ratio Discriminant
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, setup_mplhep_style

def main():
    setup_mplhep_style()
    metadata = load_metadata()
    
    zbb_path = metadata["samples"]["Zbb"]["file_path"]
    wqq_path = metadata["samples"]["Wqq"]["file_path"]
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not (os.path.exists(zbb_path) and os.path.exists(wqq_path) and os.path.exists(qcd_path)):
        print("[Note]: ROOT files not accessible locally.")
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
    # Explanation:
    # 1. What code does: Extracts raw GN3X class probabilities for phbb, pWqq, and sums 4 QCD classes.
    # 2. Data type/shape: 1D NumPy float arrays in range [0, 1].
    # 3. HEP meaning: GN3X outputs multi-class probabilities for distinct decay topologies.
    # 4. Beginner mistake: Using a single raw probability instead of building composite discriminant ratios.
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
    # SOLUTION: EXERCISE TASK 1
    # ====================================================
    # Explanation:
    # 1. What code does: Computes composite ratio D_bb = P_hbb / (P_hbb + P_wqq + P_qcd) and overlays 3 processes.
    # 2. Data type/shape: 1D NumPy float array in [0, 1].
    # 3. HEP meaning: Composite ratio isolates Zbb signal against Wqq and QCD backgrounds.
    # 4. Beginner mistake: Division by zero when denominator is small (use np.where).
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
    dbb_wqq = get_dbb(wqq_path)
    dbb_qcd = get_dbb(qcd_path)
    
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.hist(dbb_zbb, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='crimson', label=r'$Z\to b\bar{b}$ MC')
    ax.hist(dbb_wqq, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='dodgerblue', label=r'$W\to q\bar{q}$ MC')
    ax.hist(dbb_qcd, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='black', label='Dijet QCD MC')
    ax.set_xlabel(r"GN3X $D_{bb}$ Discriminant Score")
    ax.set_ylabel("Normalized Density")
    ax.set_title(r"Multiclass $D_{bb}$ Score Solution")
    ax.legend()
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("exercise6_dbb_score_sol.png", dpi=300)
    print("Saved solution plot to 'exercise6_dbb_score_sol.png'.")

if __name__ == "__main__":
    main()
