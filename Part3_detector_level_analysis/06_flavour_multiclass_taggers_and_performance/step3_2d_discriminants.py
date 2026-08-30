#!/usr/bin/env python3
"""
Exercise 6 — Step 3: 2D Multi-Discriminant Performance (D_bb vs D_qq)
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import load_metadata, setup_mplhep_style

def main():
    # ----------------------------------------------------
    # Setup: Figure styling & metadata loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and reads sample paths for Zbb, Wqq, and QCD dijets.
    # 2. Data type/shape: Python string filepaths.
    # 3. HEP meaning: Prepares datasets to visualize 2D multi-discriminant plane separation (D_bb vs D_qq).
    # 4. Common pitfall: Proceeding without verifying all 3 ROOT file paths exist.
    setup_mplhep_style()
    metadata = load_metadata()
    zbb_path = metadata["samples"]["Zbb"]["file_path"]
    wqq_path = metadata["samples"]["Wqq"]["file_path"]
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not (os.path.exists(zbb_path) and os.path.exists(wqq_path) and os.path.exists(qcd_path)):
        print("[Note]: ROOT files not available locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: D_bb and D_qq Discriminants Calculation
    # ----------------------------------------------------
    # 1. What code does: Loads GN3X probabilities and computes D_bb and D_qq ratio discriminants (entry_stop=15000).
    # 2. Data type/shape: Pair of 1D NumPy arrays in range [0, 1].
    # 3. HEP meaning: Formulates 2D classification plane separating b-jets, light/charm jets, and QCD background.
    # 4. Common pitfall: Division by zero when total sum of probabilities is zero.
    branches = [
        "largeRjet_pt_NOSYS", "largeRjet_GN3X_phbb", "largeRjet_GN3X_pWqq",
        "largeRjet_GN3X_pQCDbb", "largeRjet_GN3X_pQCDbx", "largeRjet_GN3X_pQCDcx", "largeRjet_GN3X_pQCDll"
    ]
    
    def get_discriminants(fpath):
        events = uproot.open(fpath)["reco"].arrays(branches, entry_stop=15000)
        hbb = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_phbb"]), 0.0))
        wqq = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pWqq"]), 0.0))
        qcd = (ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDbb"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDbx"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDcx"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDll"]), 0.0)))
        denom = hbb + wqq + qcd
        dbb = np.where(denom > 0, hbb / denom, 0.0)
        dqq = np.where(denom > 0, wqq / denom, 0.0)
        return dbb, dqq

    dbb_zbb, dqq_zbb = get_discriminants(zbb_path)
    dbb_wqq, dqq_wqq = get_discriminants(wqq_path)
    dbb_qcd, dqq_qcd = get_discriminants(qcd_path)
    
    # ----------------------------------------------------
    # EXAMPLE: 2D Histogram of D_bb vs D_qq for Zbb Signal
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(6.5, 5))
    h2d = ax.hist2d(dbb_zbb, dqq_zbb, bins=[30, 30], range=[[0, 1], [0, 1]], norm=LogNorm(), cmap='viridis')
    ax.set_xlabel(r"GN3X $D_{bb}$ Score")
    ax.set_ylabel(r"GN3X $D_{qq}$ Score")
    ax.set_title(r"2D Discriminant Plane ($Z\to b\bar{b}$ MC)")
    fig.colorbar(h2d[3], ax=ax, label="Events")
    plt.tight_layout()
    plt.savefig("exercise6_step3_example_2d_dbb_dqq.png", dpi=200)
    print("Saved example 2D plot to 'exercise6_step3_example_2d_dbb_dqq.png'.")

    # ====================================================
    # TODO: EXERCISE TASK 3
    # ====================================================
    # Task Instructions:
    # 1. Create a 3-panel figure comparing 2D histograms of (D_bb vs D_qq) across Zbb signal, Wqq background, and QCD background.
    # 2. Use range=[[0, 1], [0, 1]], norm=LogNorm(), and cmap='viridis' for each panel.
    # 3. Set proper axis labels (D_bb on x-axis, D_qq on y-axis), panel titles, and add colorbars.
    # 4. Save your figure to 'exercise6_step3_2d_discriminants.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Build 3-panel 2D histogram figure comparing (D_bb vs D_qq) for Zbb, Wqq, and QCD

if __name__ == "__main__":
    main()
