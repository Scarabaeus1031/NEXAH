# =========================================
# IMPORTS
# =========================================

import numpy as np
from scipy.ndimage import gaussian_filter1d
import os
from datetime import datetime
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.nexah_ieee9.simulation.powerflow_solver_real import powerflow_solver_real

from APPLICATIONS.power_systems.nexah_ieee9.overlay.manifold_fit import fit_manifold
from APPLICATIONS.power_systems.nexah_ieee9.overlay.residual_distance import (
    compute_residual,
    compute_distance,
)
from APPLICATIONS.power_systems.nexah_ieee9.context.gh_filter import gh_filter
from APPLICATIONS.power_systems.nexah_ieee9.features.structural_state import compute_structural_state
from APPLICATIONS.power_systems.nexah_ieee9.decision.state_classifier import classify_states
from APPLICATIONS.power_systems.nexah_ieee9.analysis.predictor import run_predictor
from APPLICATIONS.power_systems.nexah_ieee9.decision.intervention_policy import (
    run_intervention_policy,
)

from sklearn.cluster import KMeans


# =========================================
# CLUSTERING
# =========================================

def cluster_overlay_safe(distance, residual, k=3):
    X = np.column_stack([distance, residual])
    valid = np.isfinite(X).all(axis=1)

    if np.sum(valid) < k:
        raise ValueError("Not enough valid points for clustering")

    X_valid = X[valid]
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X_valid)

    labels = np.full(len(X), -1)
    labels[valid] = kmeans.labels_

    return labels, kmeans.cluster_centers_


# =========================================
# PLOT
# =========================================

def plot_all(lambdas, Vmin, c, dc, d2c, frag, distance, residual, states):
    fig, axes = plt.subplots(4, 1, figsize=(10, 12))

    axes[0].plot(lambdas, Vmin)
    axes[0].set_title("Voltage Collapse (REAL GRID Closed Loop)")

    axes[1].plot(lambdas, c, label="c")
    axes[1].plot(lambdas, d2c, label="d2c")
    axes[1].plot(lambdas, frag, label="frag")
    axes[1].legend()

    axes[2].scatter(distance, residual, c=distance)
    axes[2].set_title("Residual vs Distance")

    state_to_y = {"WARNING": 0, "CRITICAL": 1, "SAFE": 2, "COLLAPSED": 3}
    y = [state_to_y.get(s, -1) for s in states]

    axes[3].scatter(np.arange(len(states)), y, s=30)
    axes[3].set_yticks([0, 1, 2, 3])
    axes[3].set_yticklabels(["WARNING", "CRITICAL", "SAFE", "COLLAPSED"])

    return fig


# =========================================
# CLOSED LOOP SIMULATION (REAL GRID)
# =========================================

np.random.seed(42)

lambdas = np.linspace(0.5, 2.5, 120)

results = []
applied_actions = []

c_hist, dc_hist, d2c_hist = [], [], []
prev_action = None

for i, lam in enumerate(lambdas):

    # -------------------------------------
    # REAL SOLVER
    # -------------------------------------

    res = powerflow_solver_real(lam, action=prev_action)

    results.append({
        "lambda": lam,
        "V": res["V"],
        "theta": res["theta"],
        "converged": res["converged"]
    })

    applied_actions.append(prev_action if prev_action else "INIT")

    # -------------------------------------
    # FEATURE EXTRACTION
    # -------------------------------------

    if not res["converged"] or np.any(np.isnan(res["V"])):
        c_hist.append(np.nan)
        dc_hist.append(np.nan)
        d2c_hist.append(np.nan)
        prev_action = "NONE"
        continue

    c_val, R, spread = compute_structural_state(res["V"], res["theta"], lam)
    c_hist.append(c_val)

    # derivatives
    if len(c_hist) > 5:
        c_arr = np.array(c_hist)
        x_arr = lambdas[:len(c_arr)]

        dy = np.gradient(c_arr, x_arr)
        d2y = np.gradient(dy, x_arr)

        dc_hist = dy.tolist()
        d2c_hist = d2y.tolist()
    else:
        dc_hist.append(0)
        d2c_hist.append(0)

    # -------------------------------------
    # PREDICTION + POLICY
    # -------------------------------------

    if len(c_hist) > 10:
        try:
            c_arr = np.array(c_hist)
            dc_arr = np.array(dc_hist)
            d2c_arr = np.array(d2c_hist)

            valid = np.isfinite(c_arr) & np.isfinite(dc_arr) & np.isfinite(d2c_arr)

            if np.sum(valid) > 10:
                params = fit_manifold(c_arr[valid], dc_arr[valid], d2c_arr[valid])

                residual = compute_residual(c_arr, dc_arr, d2c_arr, params)

                rift = np.column_stack([c_arr[-10:], dc_arr[-10:]])
                distance = compute_distance(c_arr, dc_arr, rift)

                labels, _ = cluster_overlay_safe(distance, residual)

                pred = run_predictor(distance, d2c_arr, labels)

                policy = run_intervention_policy(
                    pred["risk"],
                    pred["warnings"],
                    pred["time_to_collapse"],
                    ["SAFE"] * len(pred["risk"])
                )

                prev_action = policy["actions"][-1]
            else:
                prev_action = "STABILIZE"

        except:
            prev_action = "STABILIZE"
    else:
        prev_action = "STABILIZE"


# =========================================
# POST ANALYSIS
# =========================================

Vmin, c_list, frag_list = [], [], []

for r in results:
    if not r["converged"] or np.any(np.isnan(r["V"])):
        Vmin.append(np.nan)
        c_list.append(np.nan)
        frag_list.append(np.nan)
        continue

    Vmin.append(np.min(r["V"]))
    c_val, R, spread = compute_structural_state(r["V"], r["theta"], r["lambda"])
    c_list.append(c_val)
    frag_list.append((1 - R) * spread)

c = np.array(c_list)
frag = np.array(frag_list)
Vmin = np.array(Vmin)

dc = np.gradient(c, lambdas)
d2c = np.gradient(dc, lambdas)

params = fit_manifold(c, dc, d2c)

residual = compute_residual(c, dc, d2c, params)
rift = np.column_stack([c[-15:-5], dc[-15:-5]])
distance = compute_distance(c, dc, rift)

labels, centers = cluster_overlay_safe(distance, residual)

pred = run_predictor(distance, d2c, labels)
risk = pred["risk"]
warnings = pred["warnings"]

states = classify_states(c, dc, d2c, frag, labels, gh_filter(labels, centers))
policy = run_intervention_policy(risk, warnings, pred["time_to_collapse"], states)

signal = policy["signal"]


# =========================================
# PLOTS
# =========================================

fig = plot_all(lambdas, Vmin, c, dc, d2c, frag, distance, residual, states)

fig_risk, ax = plt.subplots()
ax.plot(lambdas, risk)
ax.scatter(lambdas[warnings], risk[warnings])

fig_int, ax2 = plt.subplots()
ax2.plot(lambdas, signal)


# =========================================
# SAVE
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = f"APPLICATIONS/power_systems/nexah_ieee9/results/run_{timestamp}"
os.makedirs(results_dir, exist_ok=True)

np.save(os.path.join(results_dir, "c.npy"), c)
np.save(os.path.join(results_dir, "risk.npy"), risk)

with open(os.path.join(results_dir, "actions.txt"), "w") as f:
    for a in applied_actions:
        f.write(f"{a}\n")

fig.savefig(os.path.join(results_dir, "plot.png"))

print("Saved to:", results_dir)
