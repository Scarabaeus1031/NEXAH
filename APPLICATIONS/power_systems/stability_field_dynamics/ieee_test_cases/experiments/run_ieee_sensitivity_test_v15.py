# run_ieee_sensitivity_test_v15.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    detect_gh_corridor,
)

print("RUNNING IEEE SENSITIVITY TEST V15 (PHYSICAL COUPLING + TRANSITION CARTOGRAPHY)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

LOADS = np.linspace(0.6, 5.0, 12)
FOCUS_LOAD = 2.5

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []
focus_data = None


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def fit_axis(x: np.ndarray, y: np.ndarray):
    pts = np.column_stack([x, y])
    pts = pts - pts.mean(axis=0)
    cov = np.cov(pts.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    vec = eigvecs[:, np.argmax(eigvals)]
    angle = np.arctan2(vec[1], vec[0])
    return angle, vec


# ------------------------------------------------------------
# MAIN LOOP (PHYSICAL SYSTEM)
# ------------------------------------------------------------

for load in LOADS:

    # 🔥 PHYSICAL INPUT + CONVERGENCE FLAG
    theta, c, loops, converged = ieee_to_nexah("ieee14", load_scale=load)

    if not converged:
        print(f"[!] Load {load:.2f} -> NOT CONVERGED (collapse fallback active)")

    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)

    gh = detect_gh_corridor(theta, c, loops)

    gh_points = len(gh["theta_corridor"])
    gh_width_theta = np.ptp(gh["theta_corridor"]) if gh_points > 0 else 0.0
    gh_width_c = np.ptp(gh["c_corridor"]) if gh_points > 0 else 0.0

    # --------------------------------------------------------
    # STRUCTURAL METRICS (PHYSICAL)
    # --------------------------------------------------------

    regime_separation = theta_std * c_std
    corridor_anisotropy = gh_width_theta / (gh_width_c + 1e-9)

    c_struct = regime_separation * loops_mean

    c_struct_norm = (
        (theta_std / (1.0 + theta_std))
        * (c_std / (1.0 + c_std))
        * (loops_mean / (1.0 + loops_mean))
    )

    row = {
        "load": load,
        "converged": converged,
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,
        "gh_points": gh_points,
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "corridor_anisotropy": corridor_anisotropy,
        "regime_separation": regime_separation,
        "c_struct": c_struct,
        "c_struct_norm": c_struct_norm,
    }

    results.append(row)

    if abs(load - FOCUS_LOAD) < 1e-6:
        focus_data = (theta, c, gh)


# ------------------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------------------

df = pd.DataFrame(results)

csv_path = os.path.join(
    OUTPUT_DIR,
    "ieee_sensitivity_test_v15_physical.csv"
)

df.to_csv(csv_path, index=False)

print("\n--- RESULTS ---")
print(df)
print(f"\nSaved: {csv_path}")


# ------------------------------------------------------------
# TRANSITION CARTOGRAPHY OVERLAY
# ------------------------------------------------------------

if focus_data is not None:

    theta, c, gh = focus_data

    x = np.cos(theta) * (1 + c)
    y = np.sin(theta) * (1 + c)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Scatter
    ax.scatter(x, y, s=20, alpha=0.5)

    # GH corridor
    if len(gh["theta_corridor"]) > 0:
        x_gh = np.cos(gh["theta_corridor"]) * (1 + gh["c_corridor"])
        y_gh = np.sin(gh["theta_corridor"]) * (1 + gh["c_corridor"])
        ax.scatter(x_gh, y_gh, s=40, color="gold", label="GH Corridor")

    # White circle
    circle = Circle((0, 0), radius=2.0, fill=False, linestyle="--", linewidth=1.5)
    ax.add_patch(circle)

    # Cross
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    # PCA axis
    angle, vec = fit_axis(x, y)
    t = np.linspace(-3, 3, 100)
    ax.plot(t * vec[0], t * vec[1], linewidth=2, label="PCA Axis")

    # Pentagons
    for r in [0.5, 1.0, 1.5]:
        pent = RegularPolygon(
            (0, 0),
            numVertices=5,
            radius=r,
            fill=False,
            linewidth=1.5
        )
        ax.add_patch(pent)

    ax.set_aspect("equal")
    ax.set_title("Transition Cartography — Knick Field (Physical IEEE)")
    ax.legend()

    plt.show()
