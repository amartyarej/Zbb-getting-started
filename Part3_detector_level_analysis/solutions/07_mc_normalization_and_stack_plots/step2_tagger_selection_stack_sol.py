#!/usr/bin/env python3
"""
Solution: Exercise 7 — Step 2: Tagger-Selected Stack Plot (ParT MassDec 50% WP)
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, compute_event_weight, eval_part_wp, setup_mplhep_style

def main():
    # ----------------------------------------------------
    # Setup: Figure styling, metadata, & luminosity loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and loads sample metadata.
    # 2. Data type/shape: Python dict metadata and target luminosity float (44 fb^-1).
    # 3. HEP meaning: Prepares process definitions and target luminosity for tagger-selected stack plots.
    # 4. Common pitfall: Proceeding without checking if sample ROOT files exist.
    setup_mplhep_style()
    metadata = load_metadata()
    target_lumi_fb = metadata["target_luminosity_fb"]
    samples_info = metadata["samples"]
    
    proc_order = ["Zbb", "Zqq", "Wqq", "Dijet_JZ4"]
    proc_colors = {"Zbb": "crimson", "Zqq": "mediumseagreen", "Wqq": "lightskyblue", "Dijet_JZ4": "gold"}
    
    mass_base_list = []
    w_base_list = []
    mass_tag_list = []
    w_tag_list = []
    labels_list = []
    colors_list = []
    
    # ----------------------------------------------------
    # Data Loading & Tagger Selection Application
    # ----------------------------------------------------
    # 1. What code does: Loads jet pT, mass, generator weights, ParT scores, and GN3X probabilities.
    # 2. Data type/shape: Arrays of mass and weights passing baseline, ParT, and GN3X cuts.
    # 3. HEP meaning: Evaluates ParT MassDec 50% WP and GN3X D_bb > 0.60 cuts to isolate Z->bb signal against backgrounds.
    # 4. Common pitfall: Zero division when computing D_bb ratio discriminant (use np.where).
    branches = [
        "largeRjet_pt_NOSYS", "largeRjet_m_NOSYS", "weight_mc_NOSYS",
        "largeRjet_ParT_W_massDec_score",
        "largeRjet_GN3X_phbb", "largeRjet_GN3X_pWqq",
        "largeRjet_GN3X_pQCDbb", "largeRjet_GN3X_pQCDbx",
        "largeRjet_GN3X_pQCDcx", "largeRjet_GN3X_pQCDll"
    ]
    
    mass_gn3x_list = []
    w_gn3x_list = []
    
    for key in proc_order:
        sinfo = samples_info[key]
        fpath = sinfo["file_path"]
        if not os.path.exists(fpath):
            print(f"[Note]: Sample file {key} not accessible locally.")
            return
            
        tree = uproot.open(fpath)["reco"]
        events = tree.arrays(branches)
        
        w_norm = compute_event_weight(events, sinfo["xsec_pb"], sinfo["sum_of_weights"], target_lumi_fb)
        mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), 0.0))
        pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
        score_mdec = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_ParT_W_massDec_score"]), -1.0))
        
        # Calculate GN3X D_bb discriminant = P_hbb / (P_hbb + P_wqq + P_qcd_all)
        hbb = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_phbb"]), 0.0))
        wqq = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pWqq"]), 0.0))
        qcd_all = (ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDbb"]), 0.0)) +
                   ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDbx"]), 0.0)) +
                   ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDcx"]), 0.0)) +
                   ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_GN3X_pQCDll"]), 0.0)))
        denom = hbb + wqq + qcd_all
        dbb = np.where(denom > 0, hbb / denom, 0.0)
        
        w_norm = ak.to_numpy(w_norm)
        
        # Baseline pre-selection: pT > 200 GeV and Mass > 50 GeV
        mask_base = (pt > 200.0) & (mass > 50.0)
        
        # Tagger working point selection: ParT MassDec 50% WP
        thresh_50 = eval_part_wp(pt, "ParT_W_50_MassDec_NOSYS")
        mask_tag = mask_base & (score_mdec > thresh_50)
        
        # GN3X D_bb > 0.60 selection
        mask_gn3x = mask_base & (dbb > 0.60)
        
        mass_base_list.append(mass[mask_base])
        w_base_list.append(w_norm[mask_base])
        mass_tag_list.append(mass[mask_tag])
        w_tag_list.append(w_norm[mask_tag])
        mass_gn3x_list.append(mass[mask_gn3x])
        w_gn3x_list.append(w_norm[mask_gn3x])
        labels_list.append(sinfo["process_name"])
        colors_list.append(proc_colors[key])

    # ----------------------------------------------------
    # EXAMPLE: 2-Panel Inclusive Baseline Stack Plot (Linear & Log Scales)
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Plots inclusive baseline jet mass stack distribution on Linear (left) and Log (right) y-scales.
    # 2. Data type/shape: 2-panel matplotlib figure.
    # 3. HEP meaning: Visualizes pre-selection process composition (W/Z signal at bottom, Dijet QCD on top) across full dynamic ranges.
    # 4. Beginner mistake: Omitting log-scale view when QCD background yield dominates signal by orders of magnitude.
    bins = np.linspace(50, 250, 21)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # Linear Scale
    axes[0].hist(mass_base_list, bins=bins, weights=w_base_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    axes[0].set_xlabel("Leading Large-R Jet Mass [GeV]")
    axes[0].set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    axes[0].set_title("Inclusive Baseline Stack Plot (Linear Scale)")
    axes[0].legend(loc='upper right')
    axes[0].grid(True, alpha=0.4)
    
    # Log Scale
    axes[1].hist(mass_base_list, bins=bins, weights=w_base_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    axes[1].set_yscale('log')
    axes[1].set_ylim(1e-1, None)
    axes[1].set_xlabel("Leading Large-R Jet Mass [GeV]")
    axes[1].set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    axes[1].set_title("Inclusive Baseline Stack Plot (Log Scale)")
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.4, which='both')
    
    plt.tight_layout()
    plt.savefig("exercise7_step2_example_inclusive_stack.png", dpi=200)
    print("Saved example inclusive baseline stack plot to 'exercise7_step2_example_inclusive_stack.png'.")

    # ====================================================
    # SOLUTION: EXERCISE TASK 1 (ParT MassDec 50% WP Selection Stack)
    # ====================================================
    # Explanation:
    # 1. What code does: Plots ParT MassDec 50% WP selected stack plot in Linear (left) and Log (right) scales.
    # 2. Data type/shape: 2-panel matplotlib figure.
    # 3. HEP meaning: Reveals signal resonance peaks (W/Z) emerging above suppressed QCD background.
    # 4. Beginner mistake: Omitting log scale view when background yields remain larger than signal peaks.
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # Linear Scale
    axes[0].hist(mass_tag_list, bins=bins, weights=w_tag_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    axes[0].set_xlabel("Leading Large-R Jet Mass [GeV]")
    axes[0].set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    axes[0].set_title("ParT MassDec 50% WP Selected (Linear Scale)")
    axes[0].legend(loc='upper right')
    axes[0].grid(True, alpha=0.4)
    
    # Log Scale
    axes[1].hist(mass_tag_list, bins=bins, weights=w_tag_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    axes[1].set_yscale('log')
    axes[1].set_ylim(1e-1, None)
    axes[1].set_xlabel("Leading Large-R Jet Mass [GeV]")
    axes[1].set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    axes[1].set_title("ParT MassDec 50% WP Selected (Log Scale)")
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.4, which='both')
    
    plt.tight_layout()
    plt.savefig("exercise7_step2_part_selection_stack_sol.png", dpi=300)
    print("Saved ParT selection solution plot to 'exercise7_step2_part_selection_stack_sol.png'.")

    # ====================================================
    # SOLUTION: EXERCISE TASK 2 (GN3X D_bb > 0.60 Selection Stack)
    # ====================================================
    # Explanation:
    # 1. What code does: Plots GN3X D_bb > 0.60 selected stack plot in Linear (left) and Log (right) scales.
    # 2. Data type/shape: 2-panel matplotlib figure.
    # 3. HEP meaning: Reveals Z->bb signal peak standing prominently above suppressed QCD background after b-jet tagging.
    # 4. Beginner mistake: Omitting log scale view when background yields remain larger than signal peaks.
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # Linear Scale
    axes[0].hist(mass_gn3x_list, bins=bins, weights=w_gn3x_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    axes[0].set_xlabel("Leading Large-R Jet Mass [GeV]")
    axes[0].set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    axes[0].set_title(r"GN3X $D_{bb} > 0.60$ Selected (Linear Scale)")
    axes[0].legend(loc='upper right')
    axes[0].grid(True, alpha=0.4)
    
    # Log Scale
    axes[1].hist(mass_gn3x_list, bins=bins, weights=w_gn3x_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    axes[1].set_yscale('log')
    axes[1].set_ylim(1e-1, None)
    axes[1].set_xlabel("Leading Large-R Jet Mass [GeV]")
    axes[1].set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    axes[1].set_title(r"GN3X $D_{bb} > 0.60$ Selected (Log Scale)")
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.4, which='both')
    
    plt.tight_layout()
    plt.savefig("exercise7_step2_gn3x_dbb_selection_stack_sol.png", dpi=300)
    print("Saved GN3X D_bb selection solution plot to 'exercise7_step2_gn3x_dbb_selection_stack_sol.png'.")

if __name__ == "__main__":
    main()
