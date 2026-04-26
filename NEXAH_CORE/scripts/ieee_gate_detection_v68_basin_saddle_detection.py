# ============================================================
# NEXAH — IEEE GATE DETECTION v68
# Basin Map + Saddle Detection
# ============================================================
#
# FILE:
# ieee_gate_detection_v68_basin_saddle_detection.py
#
# PURPOSE:
# --------
# Replace heuristic gate detection from v67 with a more structural
# potential-field approach.
#
# v67:
#   Gate ≈ control_energy > barrier
#
# v68:
#   1. Build stability potential:
#        V(r, theta) = -log(rho(r, theta))
#
#   2. Detect basin candidates as local minima of V
#
#   3. Detect saddle / gate candidates as high-potential regions
#      lying between nearby basin minima
#
# CORE IDEA:
# ----------
# A gate is not merely a high-energy point.
#
# A gate is a structural passage between stable regions:
#
#     basin_i  →  saddle / gate  →  basin_j
#
# OUTPUTS:
# --------
# v68_basin_saddle_map.png
# v68_potential_profile.png
# v68_basin_saddle_summary.txt
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.ndimage import minimum_filter, maximum_filter

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control


# ------------------------------------------------------------
# Utilities
# ------------------------------------------------------------

def wrap_theta(theta):
    return (theta + np.pi) % (2 * np.pi) - np.pi


# ------------------------------------------------------------
# Build base data
# ------------------------------------------------------------

def build_pipeline():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([
        result["r"],
        result["theta"]
    ])

    return states


# ------------------------------------------------------------
# Potential grid
# ------------------------------------------------------------

def build_potential_grid(states, nr=140, nt=180):

    r_min = max(0.0, np.min(states[:, 0]) - 0.1)
    r_max = np.max(states[:, 0]) + 0.1

    theta_min = -np.pi
    theta_max = np.pi

    r_grid = np.linspace(r_min, r_max, nr)
    theta_grid = np.linspace(theta_min, theta_max, nt)

    R, T = np.meshgrid(r_grid, theta_grid, indexing="ij")

    data = np.vstack([states[:, 0], states[:, 1]])
    kde = gaussian_kde(data)

    points = np.vstack([R.ravel(), T.ravel()])
    rho = kde(points).reshape(R.shape)

    V = -np.log(rho + 1e-9)

    # normalize potential
    V = V - np.nanmin(V)
    if np.nanmax(V) > 1e-12:
        V = V / np.nanmax(V)

    return r_grid, theta_grid, R, T, rho, V


# ------------------------------------------------------------
# Detect basin minima
# ------------------------------------------------------------

def detect_basins(V, R, T, rho, min_distance=7, max_basins=12):

    local_min = V == minimum_filter(V, size=min_distance)

    # keep only meaningful density regions
    rho_threshold = np.percentile(rho, 65)
    candidates = np.argwhere(local_min & (rho > rho_threshold))

    basins = []

    for i, j in candidates:

        basins.append({
            "grid": (int(i), int(j)),
            "r": float(R[i, j]),
            "theta": float(T[i, j]),
            "V": float(V[i, j]),
            "rho": float(rho[i, j]),
        })

    basins = sorted(basins, key=lambda b: b["V"])[:max_basins]

    return basins


# ------------------------------------------------------------
# Detect saddle / gate candidates between basin pairs
# ------------------------------------------------------------

def sample_line_indices(i0, j0, i1, j1, n=120):

    ii = np.linspace(i0, i1, n).astype(int)
    jj = np.linspace(j0, j1, n).astype(int)

    return ii, jj


def detect_saddles_between_basins(V, R, T, basins, max_pairs=40):

    saddles = []

    pair_count = 0

    for a in range(len(basins)):
        for b in range(a + 1, len(basins)):

            if pair_count >= max_pairs:
                break

            i0, j0 = basins[a]["grid"]
            i1, j1 = basins[b]["grid"]

            ii, jj = sample_line_indices(i0, j0, i1, j1)

            values = V[ii, jj]

            # saddle proxy = maximum potential along minimum straight connector
            k = int(np.argmax(values))

            si = int(ii[k])
            sj = int(jj[k])

            saddle_V = float(V[si, sj])
            barrier_height = saddle_V - max(basins[a]["V"], basins[b]["V"])

            saddles.append({
                "between": (a, b),
                "grid": (si, sj),
                "r": float(R[si, sj]),
                "theta": float(T[si, sj]),
                "V": saddle_V,
                "barrier_height": float(barrier_height),
            })

            pair_count += 1

    # strongest structural barriers first
    saddles = sorted(
        saddles,
        key=lambda s: s["barrier_height"],
        reverse=True
    )

    return saddles


# ------------------------------------------------------------
# Potential profile along trajectory
# ------------------------------------------------------------

def trajectory_potential(states, r_grid, theta_grid, V):

    vals = []

    for r, th in states:

        i = np.argmin(np.abs(r_grid - r))
        j = np.argmin(np.abs(theta_grid - th))

        vals.append(V[i, j])

    return np.array(vals)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    states = build_pipeline()

    r_grid, theta_grid, R, T, rho, V = build_potential_grid(
        states,
        nr=140,
        nt=180
    )

    basins = detect_basins(
        V,
        R,
        T,
        rho,
        min_distance=7,
        max_basins=10
    )

    saddles = detect_saddles_between_basins(
        V,
        R,
        T,
        basins,
        max_pairs=40
    )

    V_traj = trajectory_potential(
        states,
        r_grid,
        theta_grid,
        V
    )

    # --------------------------------------------------------
    # Plot basin / saddle map
    # --------------------------------------------------------

    plt.figure(figsize=(9, 8))

    plt.contourf(
        T,
        R,
        V,
        levels=40,
        alpha=0.65
    )

    plt.colorbar(label="stability potential V = -log(rho)")

    plt.scatter(
        states[:, 1],
        states[:, 0],
        s=1,
        alpha=0.12,
        color="white",
        label="trajectory"
    )

    if len(basins) > 0:
        plt.scatter(
            [b["theta"] for b in basins],
            [b["r"] for b in basins],
            s=70,
            marker="o",
            color="cyan",
            edgecolor="black",
            label="basin minima"
        )

        for idx, b in enumerate(basins):
            plt.text(
                b["theta"],
                b["r"],
                f"B{idx}",
                fontsize=8,
                color="black"
            )

    top_saddles = saddles[:15]

    if len(top_saddles) > 0:
        plt.scatter(
            [s["theta"] for s in top_saddles],
            [s["r"] for s in top_saddles],
            s=80,
            marker="x",
            color="red",
            label="saddle / gate candidates"
        )

        for idx, s in enumerate(top_saddles[:8]):
            plt.text(
                s["theta"],
                s["r"],
                f"G{idx}",
                fontsize=8,
                color="red"
            )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v68 — Basin Minima + Saddle Gate Candidates")

    plt.legend(fontsize=7)
    plt.tight_layout()

    map_path = os.path.join(
        OUT_DIR,
        "v68_basin_saddle_map.png"
    )

    plt.savefig(map_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot potential along trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(10, 4))

    plt.plot(V_traj, linewidth=1.2)

    plt.xlabel("trajectory index")
    plt.ylabel("potential V")
    plt.title("NEXAH v68 — Potential Along Trajectory")

    plt.tight_layout()

    profile_path = os.path.join(
        OUT_DIR,
        "v68_potential_profile.png"
    )

    plt.savefig(profile_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        "v68_basin_saddle_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:

        f.write("NEXAH v68 — Basin Map + Saddle Detection\n")
        f.write("========================================\n\n")

        f.write(f"States: {len(states)}\n")
        f.write(f"Basins detected: {len(basins)}\n")
        f.write(f"Saddle candidates: {len(saddles)}\n\n")

        f.write("Basins:\n")
        for idx, b in enumerate(basins):
            f.write(
                f"  B{idx}: "
                f"r={b['r']:.4f}, "
                f"theta={b['theta']:.4f}, "
                f"V={b['V']:.4f}, "
                f"rho={b['rho']:.6f}\n"
            )

        f.write("\nTop saddle / gate candidates:\n")
        for idx, s in enumerate(saddles[:20]):
            a, b = s["between"]
            f.write(
                f"  G{idx}: B{a}->B{b}, "
                f"r={s['r']:.4f}, "
                f"theta={s['theta']:.4f}, "
                f"V={s['V']:.4f}, "
                f"barrier={s['barrier_height']:.4f}\n"
            )

    print("NEXAH v68 complete")
    print(f"Basins detected: {len(basins)}")
    print(f"Saddle candidates: {len(saddles)}")
    print(f"Saved: {map_path}")
    print(f"Saved: {profile_path}")
    print(f"Saved: {summary_path}")
