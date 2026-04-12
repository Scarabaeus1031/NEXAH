# =========================================
# IMPORTS
# =========================================

import numpy as np
from scipy.ndimage import gaussian_filter1d
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.nexah_ieee9.simulation.powerflow_solver_real import RealPowerFlowSolver

from APPLICATIONS.power_systems.nexah_ieee9.overlay.manifold_fit import fit_manifold
from APPLICATIONS.power_systems.nexah_ieee9.overlay.residual_distance import (
    compute_residual,
    compute_distance,
)
from APPLICATIONS.power_systems.nexah_ieee9.context.gh_filter import gh_filter

from APPLICATIONS.power_systems.nexah_ieee9.features.structural_state import compute_structural_state
from APPLICATIONS.power_systems.nexah_ieee9.decision.state_classifier import classify_states
from APPLICATIONS.power_systems.nexah_ieee9.analysis.predictor import run_predictor
from APPLICATIONS.power_systems.nexah_ieee9.decision.intervention_policy import run_intervention_policy

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
    axes[0].set_title("Voltage Collapse (REAL Solver)")

    axes[1].plot(lambdas, c, label="c")
    axes[1].plot(lambdas, d2c, label="d2c")
    axes[1].plot(lambdas, frag, label="frag")
    axes[1].legend()

    axes[2].scatter(distance, residual, c=distance)

    state_to_y = {"WARNING":0,"CRITICAL":1,"SAFE":2,"COLLAPSED":3}
    y = [state_to_y.get(s, -1) for s in states]

    axes[3].scatter(np.arange(len(states)), y)
    axes[3].set_yticks([0,1,2,3])
    axes[3].set_yticklabels(["WARNING","CRITICAL","SAFE","COLLAPSED"])

    return fig


# =========================================
# 1. SIMULATION (REAL SOLVER)
# =========================================

np.random.seed(42)

solver = RealPowerFlowSolver()

lambdas = np.linspace(0.5, 2.5, 120)

results = []
prev_action = None

for lam in lambdas:

    res = solver.step(lam, action=prev_action)

    results.append({
        "lambda": lam,
        "V": res["V"],
        "theta": res["theta"],
        "converged": res["converged"]
    })

    # simple fallback control (baseline loop)
    if not res["converged"]:
        prev_action = "NONE"
    else:
        vmin = np.min(res["V"])
        if vmin < 0.82:
            prev_action = "EMERGENCY_SHED"
        elif vmin < 0.88:
            prev_action = "REDUCE_LOAD"
        elif vmin < 0.94:
            prev_action = "PREEMPTIVE_STABILIZE"
        else:
            prev_action = "STABILIZE"


# =========================================
# 2. FEATURES
# =========================================

Vmin, c_list, frag_list = [], [], []

for r in results:

    if not r["converged"] or np.any(np.isnan(r["V"])):
        Vmin.append(np.nan)
        c_list.append(np.nan)
        frag_list.append(np.nan)
        continue

    Vmin.append(np.min(r["V"]))

    c_val, R, spread = compute_structural_state(
        r["V"], r["theta"], r["lambda"]
    )

    c_list.append(c_val)
    frag_list.append((1 - R) * spread)

c = np.array(c_list)
frag = np.array(frag_list)
Vmin = np.array(Vmin)


# =========================================
# 3. DERIVATIVES
# =========================================

def compute_derivatives_smooth(x, y):
    y_smooth = gaussian_filter1d(y, sigma=1.0)
    dy = np.gradient(y_smooth, x)
    d2y = np.gradient(dy, x)
    return dy, d2y

dc, d2c = compute_derivatives_smooth(lambdas, c)


# =========================================
# 4. MANIFOLD
# =========================================

valid = np.isfinite(c) & np.isfinite(dc) & np.isfinite(d2c)

threshold = np.percentile(np.abs(d2c[valid]), 95)
stable = valid & (np.abs(d2c) < threshold)

params = fit_manifold(
    c[stable],
    dc[stable],
    d2c[stable]
)

print("Manifold params:", params)


# =========================================
# 5. OVERLAY
# =========================================

residual = compute_residual(c, dc, d2c, params)

rift = np.column_stack([c[-15:-5], dc[-15:-5]])
distance = compute_distance(c, dc, rift)


# =========================================
# 6. CLUSTERING
# =========================================

labels, centers = cluster_overlay_safe(distance, residual)
print("Cluster centers:", centers)


# =========================================
# 6.5 PREDICTION
# =========================================

pred = run_predictor(distance, d2c, labels)

risk = pred["risk"]
warnings = pred["warnings"]
ttc = pred["time_to_collapse"]

print("Max risk:", np.nanmax(risk))


# =========================================
# 7. GH FILTER
# =========================================

gh_clusters = gh_filter(labels, centers)


# =========================================
# 8. DECISION
# =========================================

states = classify_states(c, dc, d2c, frag, labels, gh_clusters)


# =========================================
# 8.5 POLICY
# =========================================

policy = run_intervention_policy(risk, warnings, ttc, states)

signal = policy["signal"]
actions = policy["actions"]

print("First 30 actions:", actions[:30])


# =========================================
# 9. PLOTS
# =========================================

fig = plot_all(lambdas, Vmin, c, dc, d2c, frag, distance, residual, states)

fig_risk, ax = plt.subplots()
ax.plot(lambdas, risk)
ax.scatter(lambdas[warnings], risk[warnings])

fig_int, ax2 = plt.subplots()
ax2.plot(lambdas, signal)


# =========================================
# 10. SAVE
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = f"APPLICATIONS/power_systems/nexah_ieee9/results/run_{timestamp}"
os.makedirs(results_dir, exist_ok=True)

np.save(os.path.join(results_dir, "risk.npy"), risk)

with open(os.path.join(results_dir, "actions.txt"), "w") as f:
    for a in actions:
        f.write(f"{a}\n")

fig.savefig(os.path.join(results_dir, "plot.png"))

print("Saved to:", results_dir)
