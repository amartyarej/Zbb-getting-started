#!/usr/bin/env python3
"""
Solution: Exercise 4 — Step 1: Binary Tagger Score Separation
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
    
    wqq_path = metadata["samples"]["Wqq"]["file_path"]
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not (os.path.exists(wqq_path) and os.path.exists(qcd_path)):
        print("[Note]: ROOT files not accessible locally.")
        return
        
    branches = [
        "largeRjet_pt_NOSYS",
        "largeRjet_ANN50Tagger_score_NOSYS",
        "largeRjet_ParT_W_massDec_score"
    ]
    
    events_wqq = uproot.open(wqq_path)["reco"].arrays(branches, entry_stop=15000)
    events_qcd = uproot.open(qcd_path)["reco"].arrays(branches, entry_stop=15000)
    
    score_ann_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_ANN50Tagger_score_NOSYS"]), -1.0))
    score_ann_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_ANN50Tagger_score_NOSYS"]), -1.0))
    
    score_part_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_ParT_W_massDec_score"]), -1.0))
    score_part_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_ParT_W_massDec_score"]), -1.0))
    
    pt_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    pt_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    
    mask_wqq = (score_ann_wqq >= 0) & (pt_wqq > 200.0)
    mask_qcd = (score_ann_qcd >= 0) & (pt_qcd > 200.0)
    
    s_ann_wqq, s_ann_qcd = score_ann_wqq[mask_wqq], score_ann_qcd[mask_qcd]
    s_part_wqq, s_part_qcd = score_part_wqq[mask_wqq], score_part_qcd[mask_qcd]
    
    # ----------------------------------------------------
    # EXAMPLE: Overlaying ANN W-Tagger Score
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Extracts ANN W-tagger score for Wqq signal vs QCD background.
    # 2. Data type/shape: 1D NumPy array of scores in range [0, 1].
    # 3. HEP meaning: Ranks jets according to boosted 2-prong topology preference.
    # 4. Beginner mistake: Assuming classifier outputs are calibrated true probabilities.
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.hist(s_ann_wqq, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='crimson', label=r'$W\to qq$ Signal')
    ax.hist(s_ann_qcd, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='black', label='Dijet QCD Bkg')
    ax.set_xlabel("ANN W-Tagger Score")
    ax.set_ylabel("Normalized Density")
    ax.set_title("ANN W-Tagger Score Separation")
    ax.legend()
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("example_ann_score.png", dpi=200)
    print("Saved example score plot to 'example_ann_score.png'.")

    # ====================================================
    # SOLUTION: EXERCISE TASK 1
    # ====================================================
    # Explanation:
    # 1. What code does: Plots 2-panel comparison of ANN score vs ParT W-MassDec score.
    # 2. Data type/shape: matplotlib 2-panel figure.
    # 3. HEP meaning: Compares discriminant performance across different machine learning architectures.
    # 4. Beginner mistake: Omitting background score overlays when evaluating classifier separation.
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].hist(s_ann_wqq, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='crimson', label=r'$W\to qq$ Signal')
    axes[0].hist(s_ann_qcd, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='black', label='Dijet QCD Bkg')
    axes[0].set_xlabel("ANN W-Tagger Score")
    axes[0].set_ylabel("Normalized Density")
    axes[0].set_title("ANN W-Tagger Score")
    axes[0].legend()
    axes[0].grid(True, alpha=0.4)
    
    axes[1].hist(s_part_wqq, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='dodgerblue', label=r'$W\to qq$ Signal')
    axes[1].hist(s_part_qcd, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='black', label='Dijet QCD Bkg')
    axes[1].set_xlabel("ParT W-MassDec Tagger Score")
    axes[1].set_ylabel("Normalized Density")
    axes[1].set_title("ParT W-MassDec Score")
    axes[1].legend()
    axes[1].grid(True, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig("exercise4_scores_sol.png", dpi=300)
    print("Saved solution plot to 'exercise4_scores_sol.png'.")

if __name__ == "__main__":
    main()
