import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    detect_gh_corridor,
)

print("RUNNING IEEE SENSITIVITY TEST V14 (TRANSITION CARTOGRAPHY OVERLAY)")

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

LOADS = np.linspace(1.0, 5.0, 10)
N = 200

ALPHA_THETA = 0.08
BETA_LOOPS = 2.0
GAMMA_C = 0.5

FOCUS_LOAD = 3.0

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []
focus_data = None


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def structure_coupled_state(load: float, n: int = N):
    theta, c, loops = generate_phase_data(N=n)

    theta = theta * (1.0 + ALPHA_THETA * (load - 1.0))
    theta_std = np.std(theta)

    loops = loops + BETA_LOOPS * theta_std
    c = c * (1.0 + GAMMA_C * theta_std)

    return theta, c, loops, theta_std


def fit_axis(x: np.ndarray, y: np.ndarray):
    pts = np.column_stack([x, y])
    pts = pts - pts.mean(axis=0)

    cov = np.cov(pts.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    vec = eigvecs[:, np.argmax(eigvals)]

    angle = np.arctan2(vec[1], vec[0])
    return angle, vec


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for load in LOADS:
    theta, c, loops, theta_std = structure_coupled_state(load)

    gh = detect_gh_corridor(theta, c, loops)

    gh_points = len(gh["theta_corridor"])
    gh_width_theta = np.ptp(gh["theta_corridor"]) if gh_points > 0 else 0.0
    gh_width_c = np.ptp(gh["c_corridor"]) if gh_points > 0 else 0.0

    c_std = np.std(c)
    loops_mean = np.mean(loops)
    regime_separation = theta_std * c_std
    corridor_anisotropy = gh_width_theta / (gh_width_c + 1e-9)
    c_struct = regime_separation * loops_mean
    c_struct_norm = (
        (theta_std / (1.0 + theta_std))
        * (c_std / (1.0 + c_std))
        * (loops_mean / (1.0 + loops_mean))
    )

    results.append({
        "load": load,
        "theta_std": theta_std,
       
