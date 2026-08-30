#!/usr/bin/env python3
"""
Solution: Exercise 6 — Step 3: 2D Multi-Discriminant Performance (D_bb vs D_qq)
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, setup_mplhep_style, MAX_EVENTS

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
        events = uproot.open(fpath)["reco"].arrays(branches, entry_stop=MAX_EVENTS)
        hbb = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_phbb"]), 0.0))
        wqq = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pWqq"]), 0.0))
        qcd = (ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDbb"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDbx"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDcx"]), 0.0)) +
               ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDll"]), 0.0)))
        # ----------------------------------------------------
        # Ratio Discriminants Calculation with Zero-Division Protection
        # ----------------------------------------------------
        # Explanation:
        # 1. What code does: Computes composite D_bb = P_hbb / (P_hbb + P_wqq + P_qcd) and two-class D_qq = P_wqq / (P_wqq + P_qcd).
        # 2. Data type/shape: Pair of 1D NumPy float arrays bounded in [0, 1].
        # 3. HEP meaning: D_bb separates b-quark jets from light/charm and QCD, while D_qq isolates light-quark W/Z decays directly against QCD background.
        # 4. Common pitfall: Division by zero when probability sums equal zero (safely handled using np.where).
        denom_bb = hbb + wqq + qcd
        dbb = np.where(denom_bb > 0, hbb / denom_bb, 0.0)
        
        denom_qq = wqq + qcd
        dqq = np.where(denom_qq > 0, wqq / denom_qq, 0.0)
        
        return dbb, dqq

    dbb_zbb, dqq_zbb = get_discriminants(zbb_path)
    dbb_wqq, dqq_wqq = get_discriminants(wqq_path)
    dbb_qcd, dqq_qcd = get_discriminants(qcd_path)
    
    # ----------------------------------------------------
    # EXAMPLE 1: 1D D_qq Score Distribution Across 3 Processes
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Overlays 1D D_qq ratio score distributions for Zbb signal, Wqq background, and QCD background.
    # 2. Data type/shape: 1D step histogram.
    # 3. HEP meaning: Visualizes D_qq score separation power between light-quark Wqq decays and QCD dijets.
    # 4. Beginner mistake: Forgetting to normalize 1D histograms when comparing different sample sizes.
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.hist(dqq_zbb, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='crimson', label=r'$Z\to b\bar{b}$ MC')
    ax.hist(dqq_wqq, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='dodgerblue', label=r'$W\to q\bar{q}$ MC')
    ax.hist(dqq_qcd, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='black', label='Dijet QCD MC')
    ax.set_xlabel(r"GN3X $D_{qq}$ Discriminant Score")
    ax.set_ylabel("Normalized Density")
    ax.set_title(r"Multiclass $D_{qq}$ Score Separation")
    ax.legend()
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("exercise6_step3_example_1d_dqq_score.png", dpi=200)
    print("Saved example 1D plot to 'exercise6_step3_example_1d_dqq_score.png'.")

    # ----------------------------------------------------
    # EXAMPLE 2: 2D Histogram of D_bb vs D_qq for Zbb Signal
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Plots 2D density histogram of D_bb vs D_qq for Zbb signal events.
    # 2. Data type/shape: Matplotlib 2D histogram.
    # 3. HEP meaning: Demonstrates high D_bb and low D_qq clustering for Zbb signal.
    # 4. Beginner mistake: Omitting logarithmic scaling on colorbar.
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
    # SOLUTION: EXERCISE TASK 3
    # ====================================================
    # Explanation:
    # 1. What code does: Creates a 3-panel 2D comparison plot of (D_bb vs D_qq) across Zbb, Wqq, and QCD processes.
    # 2. Data type/shape: 3-panel Matplotlib figure.
    # 3. HEP meaning: Shows multi-class separation topology: Zbb clusters near (1,0), Wqq near (0,1), and QCD near (0,0).
    # 4. Beginner mistake: Using un-normalized colorbars or non-matching axis limits across panels.
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    samples_data = [
        (dbb_zbb, dqq_zbb, r"$Z\to b\bar{b}$ Signal MC"),
        (dbb_wqq, dqq_wqq, r"$W\to q\bar{q}$ Background MC"),
        (dbb_qcd, dqq_qcd, r"Dijet QCD Background MC")
    ]
    
    for ax_i, (dbb_i, dqq_i, title_i) in zip(axes, samples_data):
        h2d = ax_i.hist2d(dbb_i, dqq_i, bins=[30, 30], range=[[0, 1], [0, 1]], norm=LogNorm(), cmap='viridis')
        ax_i.set_xlabel(r"GN3X $D_{bb}$ Score")
        ax_i.set_ylabel(r"GN3X $D_{qq}$ Score")
        ax_i.set_title(title_i)
        fig.colorbar(h2d[3], ax=ax_i, label="Events")
        
    plt.tight_layout()
    plt.savefig("exercise6_step3_2d_discriminants_sol.png", dpi=300)
    print("Saved solution plot to 'exercise6_step3_2d_discriminants_sol.png'.")

if __name__ == "__main__":
    main()
