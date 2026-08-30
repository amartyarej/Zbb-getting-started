#!/usr/bin/env python3
"""
Solution: Exercise 7 — Step 2: Stacked Process Histogram & MC Uncertainty Bands
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata, compute_event_weight, setup_mplhep_style

def main():
    setup_mplhep_style()
    metadata = load_metadata()
    target_lumi_fb = metadata["target_luminosity_fb"]
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
    # Explanation:
    # 1. What code does: Accumulates process mass histograms into a stacked distribution.
    # 2. Data type/shape: matplotlib stacked histogram plot.
    # 3. HEP meaning: Visualizes expected physical signal and background composition for target luminosity.
    # 4. Beginner mistake: Plotting processes unstacked or normalized to unit area when showing physical yield composition.
    bins = np.linspace(0, 300, 31)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(mass_hist_list, bins=bins, weights=weight_hist_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    ax.set_xlabel("Leading Large-R Jet Mass [GeV]")
    ax.set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    ax.set_title("Luminosity-Normalized Stack Plot")
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("example_stack_plot.png", dpi=200)
    print("Saved example stack plot to 'example_stack_plot.png'.")

    # ====================================================
    # SOLUTION: EXERCISE TASK 2
    # ====================================================
    # Explanation:
    # 1. What code does: Calculates total MC statistical variance sum(w_norm^2) and overlays uncertainty band.
    # 2. Data type/shape: matplotlib bar chart overlay with hatch='///'.
    # 3. HEP meaning: Propagates statistical variance of weighted MC events into bin uncertainty bands.
    # 4. Beginner mistake: Taking sqrt(N_raw) or sqrt(Y_bin) instead of sqrt(sum(w_norm^2)).
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    bin_width = bins[1] - bins[0]
    
    total_y = np.zeros(len(bins) - 1)
    total_var = np.zeros(len(bins) - 1)
    
    for m, w in zip(mass_hist_list, weight_hist_list):
        counts, _ = np.histogram(m, bins=bins, weights=w)
        sum_w2, _ = np.histogram(m, bins=bins, weights=w**2)
        total_y += counts
        total_var += sum_w2

    total_stat_err = np.sqrt(total_var)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(mass_hist_list, bins=bins, weights=weight_hist_list, stacked=True, color=colors_list, label=labels_list, edgecolor='black')
    
    ax.bar(
        bin_centers,
        2.0 * total_stat_err,
        bottom=total_y - total_stat_err,
        width=bin_width,
        color='gray',
        hatch='///',
        alpha=0.5,
        label='MC Stat. Uncertainty'
    )
    
    ax.set_xlabel("Leading Large-R Jet Mass [GeV]")
    ax.set_ylabel(f"Expected Events / 10 GeV ({target_lumi_fb:.0f} " + r"$\mathrm{fb}^{-1}$)")
    ax.set_title("Luminosity-Normalized Stack Plot Solution")
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig("exercise7_stack_plot_sol.png", dpi=300)
    print("Saved solution plot to 'exercise7_stack_plot_sol.png'.")

if __name__ == "__main__":
    main()
