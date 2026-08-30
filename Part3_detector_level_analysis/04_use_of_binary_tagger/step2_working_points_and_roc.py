#!/usr/bin/env python3
"""
Exercise 4 — Step 2: Working Point Evaluation & ROC Curves
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import load_metadata, eval_part_wp, setup_mplhep_style

def main():
    setup_mplhep_style()
    metadata = load_metadata()
    
    wqq_path = metadata["samples"]["Wqq"]["file_path"]
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not (os.path.exists(wqq_path) and os.path.exists(qcd_path)):
        print("[Note]: ROOT files not accessible locally.")
        return
        
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
    thresh_w50_wqq = eval_part_wp(pt_wqq, "ParT_W_50_MassDec_NOSYS")
    thresh_w50_qcd = eval_part_wp(pt_qcd, "ParT_W_50_MassDec_NOSYS")
    
    eff_sig_w50 = np.mean(score_wqq > thresh_w50_wqq)
    mistag_bkg_w50 = np.mean(score_qcd > thresh_w50_qcd)
    
    print(f"ParT 50% MassDec WP Signal Efficiency:   {eff_sig_w50 * 100:.2f}%")
    print(f"ParT 50% MassDec WP Background Mistag:    {mistag_bkg_w50 * 100:.2f}%")
    print(f"Background Rejection Factor:             {1.0 / mistag_bkg_w50:.1f}")

    # ====================================================
    # TODO: EXERCISE TASK 2
    # ====================================================
    # Task Instructions:
    # 1. Scan tagger thresholds from 0 to 1 with 100 steps: thresholds = np.linspace(0, 1, 100).
    # 2. Compute signal efficiency list eff_sig_list and background mistag rate list mistag_bkg_list.
    # 3. Plot ROC curve: Signal Efficiency (x-axis) vs. Background Rejection 1 / mistag_bkg (y-axis, log scale).
    # 4. Save figure to 'exercise4_roc_curve.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Compute ROC curve scan and plot efficiency vs rejection

if __name__ == "__main__":
    main()
