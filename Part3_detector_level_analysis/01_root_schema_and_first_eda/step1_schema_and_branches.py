#!/usr/bin/env python3
"""
Exercise 1 — Step 1: ROOT Schema, TTree Inspection, and Jagged Arrays
Part 3 Detector-Level Analysis Tutorial
"""

import os
import sys
import uproot
import awkward as ak

# Add parent directory to path to import helpers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import load_metadata

def main():
    metadata = load_metadata()
    zbb_meta = metadata["samples"]["Zbb"]
    file_path = zbb_meta["file_path"]
    
    print("=" * 60)
    print("Exercise 1 — Step 1: Schema & Branch Inspection")
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
    events = tree.arrays(["actualInteractionsPerCrossing", "largeRjet_pt_NOSYS"], entry_stop=5000)
    mu = events["actualInteractionsPerCrossing"]
    largeR_pt = events["largeRjet_pt_NOSYS"] / 1000.0  # Convert MeV to GeV

    print(f"\nScalar mu shape: {len(mu)} entries")
    print("First 5 mu values:", mu[:5].tolist())
    print("First 5 events Large-R jet pT (GeV):", largeR_pt[:5].tolist())

    # ====================================================
    # TODO: EXERCISE TASK 1
    # ====================================================
    # Task Instructions:
    # 1. Read the small-R jet pT branch 'jet_pt_NOSYS' (convert MeV to GeV).
    # 2. Print the first 5 events of small-R jet pT.
    # 3. Compute and print:
    #    - Total number of collision events loaded.
    #    - Total number of flattened small-R jets (using ak.flatten()).
    #    - Average number of small-R jets per collision event (using ak.num()).
    # ----------------------------------------------------
    # Write your code below:
    
    # TODO: Load jet_pt_NOSYS from events or tree
    # TODO: Print first 5 events of small-R jet pT
    # TODO: Compute total events, total flattened jets, and average jet multiplicity

if __name__ == "__main__":
    main()
