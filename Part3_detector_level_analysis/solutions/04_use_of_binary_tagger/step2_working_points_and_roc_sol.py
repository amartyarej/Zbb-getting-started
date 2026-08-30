#!/usr/bin/env python3
"""
Solution: Exercise 4 — Step 2: Working Point Evaluation & ROC Curves
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, eval_part_wp, setup_mplhep_style

def main():
    # ----------------------------------------------------
    # Setup: Figure styling & metadata loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and reads Wqq signal and QCD background paths.
    # 2. Data type/shape: Python string filepaths.
    # 3. HEP meaning: Prepares sample paths for ROC curve generation and WP evaluation.
    # 4. Common beginner mistake: Proceeding without checking ROOT file existence.
    setup_mplhep_style()
    metadata = load_metadata()
    
    wqq_path = metadata["samples"]["Wqq"]["file_path"]
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not (os.path.exists(wqq_path) and os.path.exists(qcd_path)):
        print("[Note]: ROOT files not accessible locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: ParT Score & Kinematics Extraction
    # ----------------------------------------------------
    # 1. What code does: Loads ParT score and jet pT from 'reco' tree for Wqq signal and QCD background (entry_stop=15000).
    # 2. Data type/shape: 1D NumPy arrays of score floats and pT in GeV.
    # 3. HEP meaning: Provides classifier inputs to calculate signal efficiency vs background rejection.
    # 4. Common beginner mistake: Calculating ROC curves with uncleaned NaN score arrays.
    branches = ["largeRjet_pt_NOSYS", "largeRjet_ParT_W_massDec_score"]
    
    events_wqq = uproot.open(wqq_path)["reco"].arrays(branches, entry_stop=15000)
    events_qcd = uproot.open(qcd_path)["reco"].arrays(branches, entry_stop=15000)
    
    pt_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    score_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_ParT_W_massDec_score"]), -1.0))
    
    pt_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    score_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_ParT_W_massDec_score"]), -1.0))
    
    mask_wqq = (pt_wqq > 200.0) & (score_wqq >= 0)
    mask_qcd = (pt_qcd > 200.0) & (score_qcd >= 0)
    
    pt_wqq, score_wqq = pt_wqq[mask_wqq], score_wqq[mask_wqq]
    pt_qcd, score_qcd = pt_qcd[mask_qcd], score_qcd[mask_qcd]
    
    # ----------------------------------------------------
    # EXAMPLE: Evaluating ParT 50% MassDec Working Point
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Evaluates functional pT-dependent ParT WP and computes efficiency.
    # 2. Data type/shape: Float efficiency fraction.
    # 3. HEP meaning: Functional WPs adjust thresholds dynamically to maintain flat efficiency across pT.
    # 4. Beginner mistake: Using a single fixed threshold scalar across all pT ranges.
    thresh_w50_wqq = eval_part_wp(pt_wqq, "ParT_W_50_MassDec_NOSYS")
    thresh_w50_qcd = eval_part_wp(pt_qcd, "ParT_W_50_MassDec_NOSYS")
    
    eff_sig_w50 = np.mean(score_wqq > thresh_w50_wqq)
    mistag_bkg_w50 = np.mean(score_qcd > thresh_w50_qcd)
    
    print(f"ParT 50% MassDec WP Signal Efficiency:   {eff_sig_w50 * 100:.2f}%")
    print(f"ParT 50% MassDec WP Background Mistag:    {mistag_bkg_w50 * 100:.2f}%")
    print(f"Background Rejection Factor:             {1.0 / mistag_bkg_w50:.1f}")

    # ====================================================
    # SOLUTION: EXERCISE TASK 2
    # ====================================================
    # Explanation:
    # 1. What code does: Scans score thresholds from 0 to 1 and plots ROC curve.
    # 2. Data type/shape: matplotlib line plot with log y-axis.
    # 3. HEP meaning: ROC curves map full signal efficiency vs background rejection trade-off profile.
    # 4. Beginner mistake: Plotting background mistag rate on linear scale instead of log rejection.
    thresholds = np.linspace(0, 1, 100)
    eff_sig_list = [np.mean(score_wqq > t) for t in thresholds]
    mistag_bkg_list = [np.mean(score_qcd > t) for t in thresholds]
    
    plt.figure(figsize=(6, 5))
    plt.plot(eff_sig_list, 1.0 / np.maximum(1e-5, np.array(mistag_bkg_list)), color='purple', linewidth=2, label='ParT W-MassDec')
    plt.xlabel(r"Signal Efficiency $\epsilon_{\rm sig}$")
    plt.ylabel(r"Background Rejection $1 / \epsilon_{\rm bkg}$")
    plt.yscale('log')
    plt.title("ROC Curve Solution: W-Tagger Performance")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("exercise4_step2_roc_curve_sol.png", dpi=300)
    print("Saved solution plot to 'exercise4_step2_roc_curve_sol.png'.")

if __name__ == "__main__":
    main()
