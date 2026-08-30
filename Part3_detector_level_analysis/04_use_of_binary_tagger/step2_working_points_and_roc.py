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
    # Data Loading: ParT & ANN Scores & Kinematics Extraction
    # ----------------------------------------------------
    # 1. What code does: Loads ParT score, ANN score, and jet pT from 'reco' tree for Wqq signal and QCD background (entry_stop=15000).
    # 2. Data type/shape: 1D NumPy arrays of score floats and pT in GeV.
    # 3. HEP meaning: Provides classifier inputs to calculate signal efficiency vs background rejection.
    # 4. Common beginner mistake: Calculating ROC curves with uncleaned NaN score arrays.
    branches = [
        "largeRjet_pt_NOSYS",
        "largeRjet_ANN50Tagger_score_NOSYS",
        "largeRjet_ParT_W_massDec_score"
    ]
    
    events_wqq = uproot.open(wqq_path)["reco"].arrays(branches, entry_stop=15000)
    events_qcd = uproot.open(qcd_path)["reco"].arrays(branches, entry_stop=15000)
    
    pt_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    score_ann_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_ANN50Tagger_score_NOSYS"]), -1.0))
    score_part_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_ParT_W_massDec_score"]), -1.0))
    
    pt_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    score_ann_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_ANN50Tagger_score_NOSYS"]), -1.0))
    score_part_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_ParT_W_massDec_score"]), -1.0))
    
    mask_wqq = (pt_wqq > 200.0) & (score_ann_wqq >= 0) & (score_part_wqq >= 0)
    mask_qcd = (pt_qcd > 200.0) & (score_ann_qcd >= 0) & (score_part_qcd >= 0)
    
    pt_wqq, score_ann_wqq, score_part_wqq = pt_wqq[mask_wqq], score_ann_wqq[mask_wqq], score_part_wqq[mask_wqq]
    pt_qcd, score_ann_qcd, score_part_qcd = pt_qcd[mask_qcd], score_ann_qcd[mask_qcd], score_part_qcd[mask_qcd]
    
    # ----------------------------------------------------
    # EXAMPLE: Evaluating ParT 50% MassDec Working Point
    # ----------------------------------------------------
    thresh_w50_wqq = eval_part_wp(pt_wqq, "ParT_W_50_MassDec_NOSYS")
    thresh_w50_qcd = eval_part_wp(pt_qcd, "ParT_W_50_MassDec_NOSYS")
    
    eff_sig_w50 = np.mean(score_part_wqq > thresh_w50_wqq)
    mistag_bkg_w50 = np.mean(score_part_qcd > thresh_w50_qcd)
    
    print(f"ParT 50% MassDec WP Signal Efficiency:   {eff_sig_w50 * 100:.2f}%")
    print(f"ParT 50% MassDec WP Background Mistag:    {mistag_bkg_w50 * 100:.2f}%")
    print(f"Background Rejection Factor:             {1.0 / mistag_bkg_w50:.1f}")

    # ====================================================
    # EXERCISE TASK 2: ROC Curve Comparison (ANN vs ParT)
    # ====================================================
    # Scanning tagger thresholds from 0 to 1 with 100 steps
    thresholds = np.linspace(0, 1, 100)
    
    # ParT W-MassDec Tagger ROC
    eff_sig_part = [np.mean(score_part_wqq > t) for t in thresholds]
    mistag_bkg_part = [np.mean(score_part_qcd > t) for t in thresholds]
    rej_bkg_part = 1.0 / np.maximum(1e-5, np.array(mistag_bkg_part))
    
    # ANN W-Tagger ROC
    eff_sig_ann = [np.mean(score_ann_wqq > t) for t in thresholds]
    mistag_bkg_ann = [np.mean(score_ann_qcd > t) for t in thresholds]
    rej_bkg_ann = 1.0 / np.maximum(1e-5, np.array(mistag_bkg_ann))

    # Task Instructions:
    # 1. Plot ROC curve: Signal Efficiency (x-axis) vs. Background Rejection 1 / mistag_bkg (y-axis, log scale).
    # 2. Save figure to 'exercise4_step2_roc_curve.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Plot efficiency vs rejection as ROC curve for both the taggers

if __name__ == "__main__":
    main()
