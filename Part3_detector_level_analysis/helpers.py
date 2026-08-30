"""
Shared Helper Module for Part 3 Detector-Level Analysis Tutorial
Contains utilities for metadata loading, ROOT file reading via Uproot,
MC weight normalization, ParT working point evaluation, and plotting setup.
"""

import json
import os
import numpy as np

# Global event limit for tutorial processing speed
# Set to None to load all events; 20000 for speed
MAX_EVENTS = None

def load_metadata(metadata_path=None):
    """
    Loads dataset metadata including cross sections, sum of weights,
    file paths, and truth label dictionary.
    """
    if metadata_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        metadata_path = os.path.join(base_dir, "metadata_template.json")
    with open(metadata_path, "r") as f:
        return json.load(f)

def load_reco_tree(file_path, tree_name="reco", branches=None):
    """
    Opens a ROOT TTree using uproot and returns an awkward array of events.
    
    Parameters:
    -----------
    file_path : str
        Path to ROOT file
    tree_name : str
        Name of TTree (default: 'reco')
    branches : list of str, optional
        Subset of branches to load. If None, loads all available branches.
        
    Returns:
    --------
    awkward.Array or uproot.ReadOnlyTree
        Loaded tree array
    """
    import uproot
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ROOT file not found: {file_path}")
    
    root_file = uproot.open(file_path)
    tree = root_file[tree_name]
    if branches is not None:
        return tree.arrays(branches)
    return tree.arrays()

def compute_event_weight(events, xsec_pb, sum_of_weights, target_lumi_fb=44.0):
    """
    Computes per-event normalization weight:
    w_norm = w_gen * (xsec_pb * target_lumi_pb) / sum_of_weights
    
    HEP meaning:
    Scaling raw simulated event counts to the physical yield expected in
    target_lumi_fb inverse femtobarn dataset.
    """
    target_lumi_pb = target_lumi_fb * 1000.0  # 1 fb^-1 = 1000 pb^-1
    if "weight_mc_NOSYS" in events.fields:
        w_gen = events["weight_mc_NOSYS"]
    else:
        w_gen = np.ones(len(events))
    
    # Scale factor per event
    w_norm = w_gen * (xsec_pb * target_lumi_pb) / sum_of_weights
    return w_norm

def eval_part_wp(pt_gev, wp_name):
    """
    Evaluates functional pT-dependent ParT binary W-tagger working points (in GeV).
    Returns the required tagger score threshold for a jet with given pt_gev.
    
    Working points:
    - 'ParT_W_50_NOSYS'
    - 'ParT_W_80_NOSYS'
    - 'ParT_W_50_MassDec_NOSYS'
    - 'ParT_W_80_MassDec_NOSYS'
    """
    pt = np.asarray(pt_gev, dtype=float)
    if wp_name == "ParT_W_50_NOSYS":
        return (0.730656 
                + 0.000890239 * pt 
                - 1.38109e-06 * (pt**2) 
                + 1.15325e-09 * (pt**3) 
                - 5.51221e-13 * (pt**4) 
                + 1.50973e-16 * (pt**5) 
                - 2.2043e-20 * (pt**6) 
                + 1.32997e-24 * (pt**7))
    elif wp_name == "ParT_W_80_NOSYS":
        return (0.316462 
                + 0.00112194 * pt 
                - 1.01879e-06 * (pt**2) 
                + 4.95035e-10 * (pt**3) 
                - 1.28396e-13 * (pt**4) 
                + 1.62202e-17 * (pt**5) 
                - 7.4361e-22 * (pt**6))
    elif wp_name == "ParT_W_50_MassDec_NOSYS":
        return (0.757528 
                + 0.000109953 * pt 
                - 9.80266e-08 * (pt**2) 
                + 6.42213e-11 * (pt**3) 
                - 1.85509e-14 * (pt**4) 
                + 1.86352e-18 * (pt**5))
    elif wp_name == "ParT_W_80_MassDec_NOSYS":
        return (0.502123 
                + 9.86498e-05 * pt 
                - 9.4353e-08 * (pt**2) 
                + 6.51485e-11 * (pt**3) 
                - 1.85051e-14 * (pt**4) 
                + 1.80921e-18 * (pt**5))
    else:
        raise ValueError(f"Unknown ParT working point: {wp_name}")

def compute_distance_correlation(x, y):
    """
    Computes distance correlation dcor(X, Y) between two 1D numerical arrays.
    Distance correlation is a non-negative statistic measuring linear and non-linear dependence.
    """
    try:
        import dcor
        return dcor.distance_correlation(x, y)
    except ImportError:
        # Simple distance correlation implementation using scipy distance matrices
        from scipy.spatial.distance import pdist, squareform
        x = np.asarray(x, dtype=float).reshape(-1, 1)
        y = np.asarray(y, dtype=float).reshape(-1, 1)
        n = len(x)
        if n < 2:
            return 0.0
        
        a = squareform(pdist(x, 'euclidean'))
        b = squareform(pdist(y, 'euclidean'))
        
        A = a - a.mean(axis=0)[None, :] - a.mean(axis=1)[:, None] + a.mean()
        B = b - b.mean(axis=0)[None, :] - b.mean(axis=1)[:, None] + b.mean()
        
        dcov2_xy = np.sum(A * B) / (n * n)
        dcov2_xx = np.sum(A * A) / (n * n)
        dcov2_yy = np.sum(B * B) / (n * n)
        
        if dcov2_xx * dcov2_yy <= 0:
            return 0.0
        return np.sqrt(np.maximum(0.0, dcov2_xy) / np.sqrt(dcov2_xx * dcov2_yy))

def setup_mplhep_style():
    """
    Sets up ATLAS-like formatting using mplhep if available, else clean matplotlib defaults.
    """
    import matplotlib.pyplot as plt
    try:
        import mplhep as hep
        plt.style.use(hep.style.ATLAS)
    except ImportError:
        plt.rcParams.update({
            'font.size': 12,
            'axes.labelsize': 14,
            'axes.titlesize': 14,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            'legend.fontsize': 11,
            'figure.autolayout': True
        })
