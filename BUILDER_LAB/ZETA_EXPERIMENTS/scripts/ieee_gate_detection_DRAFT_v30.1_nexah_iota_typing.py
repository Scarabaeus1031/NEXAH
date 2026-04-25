# V30.1 — CLEAN PIPELINE (NEXAH IOTA SYSTEM)

import numpy as np
from scipy.spatial import KDTree
from scipy.ndimage import gaussian_filter
import os

# =========================
# LOAD
# =========================
def load_data(path):
    if os.path.exists(path):
        data = np.load(path)
        return data["theta"], data["r"]
    else:
        raise FileNotFoundError("Data file not found")

# =========================
# DERIVATIVES
# =========================
def compute_derivatives(theta, r):
    dr = np.gradient(r) / np.gradient(theta)
    yugo = np.arctan2(dr, np.gradient(theta))
    return dr, yugo

# =========================
# FIELD
# =========================
def compute_density(theta, r, bins=80):
    heatmap, xedges, yedges = np.histogram2d(theta, r, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=2)
    return heatmap, xedges, yedges

# =========================
# RIDGE
# =========================
def compute_ridge(heatmap, xedges, yedges):
    mask = heatmap > np.percentile(heatmap, 85)

    x_centers = (xedges[:-1] + xedges[1:]) / 2
    y_centers = (yedges[:-1] + yedges[1:]) / 2

    pts = []
    for i in range(len(x_centers)):
        for j in range(len(y_centers)):
            if mask[i, j]:
                pts.append([x_centers[i], y_centers[j]])

    return np.array(pts)

# =========================
# GREYSPACE
# =========================
def compute_greyspace(theta, r, heatmap, xedges, yedges):
    vals = []

    for t, rv in zip(theta, r):
        xi = np.searchsorted(xedges, t) - 1
        yi = np.searchsorted(yedges, rv) - 1

        if 0 <= xi < heatmap.shape[0] and 0 <= yi < heatmap.shape[1]:
            vals.append(heatmap[xi, yi])
        else:
            vals.append(0)

    vals = np.array(vals)

    gs = 1 / (vals + 1e-3)
    gs = (gs - gs.min()) / (gs.max() - gs.min())

    return gs

# =========================
# IOTA DETECTOR
# =========================
def detect_iota(dr):
    threshold = np.percentile(np.abs(dr), 98)
    return np.where(np.abs(dr) > threshold)[0]

# =========================
# CLASSIFIER
# =========================
def classify_iota(theta, r, ridge_pts, greyspace, iota_idx):

    tree = KDTree(ridge_pts) if len(ridge_pts) > 0 else None
    types = []
    distances = []

    for i in range(len(theta)):
        if tree:
            d, _ = tree.query([theta[i], r[i]])
        else:
            d = np.nan
        distances.append(d)

    distances = np.array(distances)
    distances = (distances - np.nanmin(distances)) / (
        np.nanmax(distances) - np.nanmin(distances)
    )

    for idx in iota_idx:
        if greyspace[idx] > 0.6 and distances[idx] > 0.6:
            types.append("GAP_ESCAPE")
        else:
            types.append("BOUNDARY_COLLAPSE")

    return types, distances

# =========================
# MAIN
# =========================
def run_pipeline():

    theta, r = load_data(
        "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/v28_data.npz"
    )

    dr, yugo = compute_derivatives(theta, r)

    heatmap, xedges, yedges = compute_density(theta, r)

    ridge_pts = compute_ridge(heatmap, xedges, yedges)

    greyspace = compute_greyspace(theta, r, heatmap, xedges, yedges)

    iota_idx = detect_iota(dr)

    types, distances = classify_iota(theta, r, ridge_pts, greyspace, iota_idx)

    print("\n--- V30.1 PIPELINE ---")
    print("IOTA:", len(iota_idx))
    print("GAP:", types.count("GAP_ESCAPE"))
    print("BOUNDARY:", types.count("BOUNDARY_COLLAPSE"))

    return theta, r, iota_idx, types

# RUN
if __name__ == "__main__":
    run_pipeline()
