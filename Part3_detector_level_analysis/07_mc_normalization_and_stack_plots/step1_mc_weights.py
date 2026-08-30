#!/usr/bin/env python3
"""
Exercise 7 — Step 1: Per-Event Normalization Weight Calculation
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import load_metadata, compute_event_weight

def main():
    # ----------------------------------------------------
    # Setup: Dataset metadata & target luminosity loading
    # ----------------------------------------------------
    # 1. What code does: Reads sample cross sections, sum of weights, and target luminosity from metadata.json.
    # 2. Data type/shape: Python dict metadata and float target luminosity.
    # 3. HEP meaning: Provides physics normalization constants (sigma, sum_w) to scale MC to target integrated luminosity.
    # 4. Common beginner mistake: Using raw unweighted entry counts instead of luminosity-scaled weighted yields.
    metadata = load_metadata()
    target_lumi_fb = metadata["target_luminosity_fb"]
    zbb_info = metadata["samples"]["Zbb"]
    
    file_path = zbb_info["file_path"]
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        return
        
    # ----------------------------------------------------
    # Data Loading: Generator Weights & Event Weight Calculation
    # ----------------------------------------------------
    # 1. What code does: Reads generator weight branch 'weight_mc_NOSYS' (first 20,000 events via entry_stop=20000) and computes normalized per-event weights.
    # 2. Data type/shape: 1D NumPy array of per-event weights w_norm.
    # 3. HEP meaning: w_norm = w_gen * (sigma * L) / sum(w_gen) converts simulation counts to expected physical events.
    # 4. Common beginner mistake: Forgetting that generator weights can be negative (e.g. NLO MC interference).
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays(["largeRjet_pt_NOSYS", "largeRjet_m_NOSYS", "weight_mc_NOSYS"], entry_stop=20000)
    
    # ----------------------------------------------------
    # EXAMPLE: Calculating Normalization Weights for Zbb
    # ----------------------------------------------------
    w_norm_zbb = compute_event_weight(
        events,
        xsec_pb=zbb_info["xsec_pb"],
        sum_of_weights=zbb_info["sum_of_weights"],
        target_lumi_fb=target_lumi_fb
    )
    
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), 0.0))
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    w_norm_zbb = ak.to_numpy(w_norm_zbb)
    
    mask = (pt > 250.0) & (mass > 0.0)
    raw_count = len(mass[mask])
    exp_yield = np.sum(w_norm_zbb[mask])
    
    print(f"Zbb Sample | Raw Selected Events: {raw_count} | Expected Yield ({target_lumi_fb} fb^-1): {exp_yield:.2f}")

    # ====================================================
    # TODO: EXERCISE TASK 1
    # ====================================================
    # Task Instructions:
    # 1. Loop over all samples in metadata["samples"] (Zbb, Zqq, Wqq, Dijet_JZ4).
    # 2. Compute per-event normalization weight w_norm for each sample.
    # 3. Apply baseline cut: pT > 250 GeV and Mass > 0 GeV.
    # 4. Print a summary table listing Sample Name, Raw Selected Count, and Expected Luminosity-Normalized Yield.
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Loop over samples, calculate weights, and print summary yield table

if __name__ == "__main__":
    main()
