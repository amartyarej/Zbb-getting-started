#!/usr/bin/env python3
"""
Exercise 7 — Step 2: Stacked Process Histogram & MC Uncertainty Bands
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import load_metadata, compute_event_weight, setup_mplhep_style

def main():
    # ----------------------------------------------------
    # Setup: Figure styling, metadata, & luminosity loading
    # ----------------------------------------------------
    # 1. What code does: Configures ATLAS plot aesthetics and loads sample metadata for background & signal samples.
    # 2. Data type/shape: Python dict metadata and target luminosity float (44 fb^-1).
    # 3. HEP meaning: Prepares process definitions and luminosity target for stack histogram construction.
    # 4. Common beginner mistake: Proceeding without checking if sample ROOT files exist.
    setup_mplhep_style()
    metadata = load_metadata()
    target_lumi_fb = metadata["target_luminosity_fb"]
    
    # ----------------------------------------------------
    # Data Loading & Event Weighting across Processes
    # ----------------------------------------------------
    # 1. What code does: Reads jet mass and generator weights for each sample and calculates per-event w_norm.
    # 2. Data type/shape: Dictionary mapping process names to arrays of mass and w_norm.
    # 3. HEP meaning: Scales each MC process (QCD, Wqq, Zqq, Zbb) to expected yields for 44 fb^-1.
    # 4. Common beginner mistake: Summing errors linearly instead of using sqrt(sum(w^2)) for weighted histogram bins.
    samples_info = metadata["samples"]
    
    proc_order = ["Dijet_JZ4", "Wqq", "Zqq", "Zbb"]
    proc_colors = {"Dijet_JZ4": "gold", "Wqq": "lightskyblue", "Zqq": "mediumseagreen", "Zbb": "crimson"}
    
    mass_hist_list = []
    weight_hist_list = []
    labels_list = []
    colors_list = []
    
    for key in proc_order:
        sinfo = samples_info[key]
        fpath = sinfo["file_path"]
        if not os.path.exists(fpath):
            print(f"[Note]: Sample file {key} not accessible locally.")
            return
            
        tree = uproot.open(fpath)["reco"]
        events = tree.arrays(["largeRjet_pt_NOSYS", "largeRjet_m_NOSYS", "weight_mc_NOSYS"], entry_stop=20000)
        
        w_norm = compute_event_weight(events, sinfo["xsec_pb"], sinfo["sum_of_weights"], target_lumi_fb)
        mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), 0.0))
        pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
        w_norm = ak.to_numpy(w_norm)
        
        mask = (pt > 250.0) & (mass > 0.0)
        mass_hist_list.append(mass[mask])
        weight_hist_list.append(w_norm[mask])
        labels_list.append(sinfo["process_name"])
        colors_list.append(proc_colors[key])

    # ----------------------------------------------------
    # EXAMPLE: Plotting Stacked Process Histogram
    # ----------------------------------------------------
    bins = np.linspace(0, 300, 31)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(mass_hist_list, bins=bins, weights=weight_hist_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    ax.set_xlabel("Leading Large-R Jet Mass [GeV]")
    ax.set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    ax.set_title("Luminosity-Normalized Stack Plot")
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("exercise7_step2_example_stack_plot.png", dpi=200)
    print("Saved example stack plot to 'exercise7_step2_example_stack_plot.png'.")

    # ====================================================
    # TODO: EXERCISE TASK 2
    # ====================================================
    # Task Instructions:
    # 1. Compute total bin statistical uncertainty band:
    #    - Loop over processes and accumulate sum of squared weights: sum_w2, _ = np.histogram(m, bins=bins, weights=w**2).
    #    - Calculate total_stat_err = np.sqrt(total_var).
    # 2. Overlay statistical uncertainty band using ax.bar() with hatch='///' and alpha=0.5.
    # 3. Save your figure to 'exercise7_step2_stack_plot.png'.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Compute sum(w^2) error bands and overlay on stack plot

if __name__ == "__main__":
    main()
