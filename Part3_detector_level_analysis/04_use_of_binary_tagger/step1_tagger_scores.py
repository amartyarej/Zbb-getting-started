#!/usr/bin/env python3
"""
Exercise 4 — Step 1: Binary Tagger Score Separation
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import load_metadata, setup_mplhep_style, MAX_EVENTS

def main():
    # ----------------------------------------------------
    # Setup: Figure styling & metadata loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and reads sample paths for Wqq, Zqq, Zbb, and QCD dijets.
    # 2. Data type/shape: Python string filepaths.
    # 3. HEP meaning: Accesses process samples for binary tagger performance comparison.
    # 4. Common beginner mistake: Proceeding without checking ROOT file existence.
    setup_mplhep_style()
    metadata = load_metadata()
    
    wqq_path = metadata["samples"]["Wqq"]["file_path"]
    zqq_path = metadata["samples"]["Zqq"]["file_path"]
    zbb_path = metadata["samples"]["Zbb"]["file_path"]
    qcd_path = metadata["samples"]["Dijet_JZ4"]["file_path"]
    
    if not all(os.path.exists(p) for p in [wqq_path, zqq_path, zbb_path, qcd_path]):
        print("[Note]: One or more ROOT files not found locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: Binary Tagger Scores & Jet Kinematics
    # ----------------------------------------------------
    # 1. What code does: Loads ANN and ParT W-tagger scores and pT branches for Wqq, Zqq, Zbb, and QCD events (entry_stop=MAX_EVENTS).
    # 2. Data type/shape: 1D NumPy arrays of float scores in [0.0, 1.0].
    # 3. HEP meaning: Extracts ML tagger outputs to compare signal/background separation power.
    # 4. Common beginner mistake: Mixing up binary W-taggers with b-taggers or mass-decorrelated taggers.
    branches = ["largeRjet_pt_NOSYS", "largeRjet_ANN50Tagger_score_NOSYS", "largeRjet_ParT_W_massDec_score"]
    
    events_wqq = uproot.open(wqq_path)["reco"].arrays(branches, entry_stop=MAX_EVENTS)
    events_zqq = uproot.open(zqq_path)["reco"].arrays(branches, entry_stop=MAX_EVENTS)
    events_zbb = uproot.open(zbb_path)["reco"].arrays(branches, entry_stop=MAX_EVENTS)
    events_qcd = uproot.open(qcd_path)["reco"].arrays(branches, entry_stop=MAX_EVENTS)
    
    score_ann_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_ANN50Tagger_score_NOSYS"]), -1.0))
    score_ann_zqq = ak.to_numpy(ak.fill_none(ak.firsts(events_zqq["largeRjet_ANN50Tagger_score_NOSYS"]), -1.0))
    score_ann_zbb = ak.to_numpy(ak.fill_none(ak.firsts(events_zbb["largeRjet_ANN50Tagger_score_NOSYS"]), -1.0))
    score_ann_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_ANN50Tagger_score_NOSYS"]), -1.0))
    
    pt_wqq = ak.to_numpy(ak.fill_none(ak.firsts(events_wqq["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    pt_zqq = ak.to_numpy(ak.fill_none(ak.firsts(events_zqq["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    pt_zbb = ak.to_numpy(ak.fill_none(ak.firsts(events_zbb["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    pt_qcd = ak.to_numpy(ak.fill_none(ak.firsts(events_qcd["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    
    mask_wqq = (score_ann_wqq >= 0) & (pt_wqq > 200.0)
    mask_zqq = (score_ann_zqq >= 0) & (pt_zqq > 200.0)
    mask_zbb = (score_ann_zbb >= 0) & (pt_zbb > 200.0)
    mask_qcd = (score_ann_qcd >= 0) & (pt_qcd > 200.0)
    
    s_ann_wqq, s_ann_zqq, s_ann_zbb, s_ann_qcd = score_ann_wqq[mask_wqq], score_ann_zqq[mask_zqq], score_ann_zbb[mask_zbb], score_ann_qcd[mask_qcd]
    
    # ----------------------------------------------------
    # EXAMPLE: Overlaying ANN W-Tagger Score
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.hist(s_ann_wqq, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='crimson', label=r'$W\to qq$ Signal')
    ax.hist(s_ann_zqq, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='mediumseagreen', label=r'$Z\to qq$ Sample')
    ax.hist(s_ann_zbb, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='darkorange', label=r'$Z\to bb$ Sample')
    ax.hist(s_ann_qcd, bins=50, range=(0, 1), density=True, histtype='step', linewidth=2, color='black', label='Dijet QCD Bkg')
    ax.set_xlabel("ANN W-Tagger Score")
    ax.set_ylabel("Normalized Density")
    ax.set_title("ANN W-Tagger Score Separation")
    ax.legend()
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("exercise4_step1_example_ann_score.png", dpi=200)
    print("Saved example score plot to 'exercise4_step1_example_ann_score.png'.")

    # ====================================================
    # TODO: EXERCISE TASK 1
    # ====================================================
    # Task Instructions:
    # 1. Extract ParT W mass-decorrelated score 'largeRjet_ParT_W_massDec_score' for Wqq and QCD.
    # 2. Create a 2-panel figure comparing ANN W-tagger score vs ParT W-MassDec tagger score.
    # 3. Add proper labels, titles, legends, and save to 'exercise4_step1_scores.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Extract ParT scores and plot 2-panel comparison

if __name__ == "__main__":
    main()
