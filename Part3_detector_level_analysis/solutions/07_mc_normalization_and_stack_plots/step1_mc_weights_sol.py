#!/usr/bin/env python3
"""
Solution: Exercise 7 — Step 1: Per-Event Normalization Weight Calculation
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import uproot
import awkward as ak

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
    # 1. What code does: Reads generator weight branch 'weight_mc_NOSYS' and computes normalized per-event weights.
    # 2. Data type/shape: 1D NumPy array of per-event weights w_norm.
    # 3. HEP meaning: w_norm = w_gen * (sigma * L) / sum(w_gen) converts simulation counts to expected physical events.
    # 4. Common beginner mistake: Forgetting that generator weights can be negative (e.g. NLO MC interference).
    tree = uproot.open(file_path)["reco"]
    events = tree.arrays(["largeRjet_pt_NOSYS", "largeRjet_m_NOSYS", "weight_mc_NOSYS"])
    
    # ----------------------------------------------------
    # EXAMPLE: Calculating Normalization Weights for Zbb
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Calculates normalized event weights for Zbb sample.
    # 2. Data type/shape: 1D NumPy array of float weights.
    # 3. HEP meaning: Converts MC event count to expected physical events for target integrated luminosity.
    # 4. Beginner mistake: Using un-weighted entry counts for cross-section calculations.
    w_norm_zbb = compute_event_weight(
        events,
        xsec_pb=zbb_info["xsec_pb"],
        sum_of_weights=zbb_info["sum_of_weights"],
        target_lumi_fb=target_lumi_fb
    )
    
    mass = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_m_NOSYS"] / 1000.0), 0.0))
    pt = ak.to_numpy(ak.fill_none(ak.firsts(events["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
    w_norm_zbb = ak.to_numpy(w_norm_zbb)
    
    mask = (pt > 200.0) & (mass > 50.0)
    raw_count = len(mass[mask])
    exp_yield = np.sum(w_norm_zbb[mask])
    
    print(f"Zbb Sample | Raw Selected Events: {raw_count} | Expected Yield ({target_lumi_fb} fb^-1): {exp_yield:.2f}")

    # ====================================================
    # SOLUTION: EXERCISE TASK 1
    # ====================================================
    # Explanation:
    # 1. What code does: Loops over all MC samples and prints raw selected count vs expected yield summary table.
    # 2. Data type/shape: Formatted summary yield table.
    # 3. HEP meaning: Compares raw simulated entry statistics vs physical signal/background yields.
    # 4. Beginner mistake: Assuming raw event counts reflect physical cross-section ratios across samples.
    samples_info = metadata["samples"]
    
    print("\n" + "=" * 60)
    print("SOLUTION: Exercise 7 — Step 1: MC Weight Summary Table")
    print("=" * 60)
    
    for key, sinfo in samples_info.items():
        fpath = sinfo["file_path"]
        if not os.path.exists(fpath):
            print(f"[Note]: Sample file {key} not present locally.")
            continue
            
        t = uproot.open(fpath)["reco"]
        evts = t.arrays(["largeRjet_pt_NOSYS", "largeRjet_m_NOSYS", "weight_mc_NOSYS"])
        
        w_n = compute_event_weight(evts, sinfo["xsec_pb"], sinfo["sum_of_weights"], target_lumi_fb)
        m = ak.to_numpy(ak.fill_none(ak.firsts(evts["largeRjet_m_NOSYS"] / 1000.0), 0.0))
        p = ak.to_numpy(ak.fill_none(ak.firsts(evts["largeRjet_pt_NOSYS"] / 1000.0), 0.0))
        w_n = ak.to_numpy(w_n)
        
        m_mask = (p > 200.0) & (m > 50.0)
        r_cnt = len(m[m_mask])
        e_yld = np.sum(w_n[m_mask])
        print(f"Sample {key:10s} | Raw Selected: {r_cnt:7d} | Expected Yield ({target_lumi_fb} fb^-1): {e_yld:10.2f}")

if __name__ == "__main__":
    main()
