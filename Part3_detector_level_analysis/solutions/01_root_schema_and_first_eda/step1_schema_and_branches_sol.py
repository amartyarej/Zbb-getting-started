#!/usr/bin/env python3
"""
Solution: Exercise 1 — Step 1: ROOT Schema, TTree Inspection, and Jagged Arrays
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import numpy as np
import uproot
import awkward as ak

# Add parent directory of solutions to path to import helpers
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from helpers import load_metadata

def main():
    metadata = load_metadata()
    zbb_meta = metadata["samples"]["Zbb"]
    file_path = zbb_meta["file_path"]
    
    print("=" * 60)
    print("Solution: Exercise 1 — Step 1: Schema & Branch Inspection")
    print(f"Sample: {zbb_meta['process_name']}")
    print("=" * 60)
    
    if not os.path.exists(file_path):
        print(f"[Note]: ROOT file {file_path} is not accessible locally.")
        print("Run on an EOS-connected node or server to execute with ROOT file.")
        return

    # ----------------------------------------------------
    # EXAMPLE 1: Opening ROOT file & inspecting TTree keys
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Opens ROOT file using uproot and accesses TTree 'reco'.
    # 2. Data type/shape: uproot.ReadOnlyTree.
    # 3. HEP meaning: TTree 'reco' contains collision event data arranged in branches.
    # 4. Beginner mistake: Trying to read branches without opening TTree first.
    root_file = uproot.open(file_path)
    tree = root_file["reco"]
    
    print(f"Successfully opened tree 'reco' with {tree.num_entries} entries.")
    print("First 10 branch keys:", tree.keys()[:10])

    # ----------------------------------------------------
    # EXAMPLE 2: Reading Scalar vs. Jagged Branches
    # ----------------------------------------------------
    # Explanation:
    # 1. What code does: Reads pileup parameter mu (scalar) and jet pT (jagged array).
    # 2. Data type/shape: mu -> 1D array (N_events,); jet_pt -> Jagged array (N_events, var_jets).
    # 3. HEP meaning: mu is event-level; jet_pt is object-level (variable number of jets per event).
    # 4. Beginner mistake: Treating jagged arrays as rectangular 2D matrices.
    events = tree.arrays(["actualInteractionsPerCrossing", "largeRjet_pt_NOSYS", "jet_pt_NOSYS"], entry_stop=5000)
    mu = events["actualInteractionsPerCrossing"]
    largeR_pt = events["largeRjet_pt_NOSYS"] / 1000.0  # Convert MeV to GeV

    print(f"\nScalar mu shape: {len(mu)} entries")
    print("First 5 mu values:", mu[:5].tolist())
    print("First 5 events Large-R jet pT (GeV):", largeR_pt[:5].tolist())

    # ====================================================
    # SOLUTION: EXERCISE TASK 1
    # ====================================================
    # Explanation:
    # 1. What code does: Reads small-R jet pT, flattens jet collection, and computes multiplicity.
    # 2. Data type/shape: smallR_pt -> Jagged array (N_events, var_jets); flat_smallR -> 1D array (N_jets,).
    # 3. HEP meaning: Multiplicity counts reconstructed jets per event; flattening lists all jets.
    # 4. Beginner mistake: Using len(flat_smallR) as total collision event count.
    smallR_pt = events["jet_pt_NOSYS"] / 1000.0  # Convert MeV to GeV
    
    print("\nFirst 5 events Small-R jet pT (GeV):", smallR_pt[:5].tolist())
    
    flat_smallR = ak.flatten(smallR_pt)
    mult_smallR = ak.num(smallR_pt)
    
    print(f"Total collision events loaded: {len(events)}")
    print(f"Total reconstructed small-R jets: {len(flat_smallR)}")
    print(f"Average small-R jets per event: {np.mean(mult_smallR):.2f}")

if __name__ == "__main__":
    main()
