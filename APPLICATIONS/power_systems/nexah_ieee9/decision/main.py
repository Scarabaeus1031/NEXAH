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
# HELPERS
# =========================================

def safe_derivatives(x, y):
    y = np.nan_to_num(y, nan=np.nanmedian(y))
    y_smooth = gaussian_filter1d(y, sigma=1.0)
    dy = np.gradient(y_smooth, x)
    d2y = np.gradient(dy, x)
    return dy, d2y


def cluster_overlay_safe(distance, residual, k=3):
    X = np.column_stack([distance, residual])
    valid = np.isfinite(X).all(axis=1)

    labels = np.full(len(X), -1)

    if np.sum(valid) < k:
        print("⚠️ clustering fallback")
        centers = np.zeros((k, 2))
        return labels, centers, False

    kmeans = KMeans(n_clusters=k, random_state=0).fit(X[valid])
    labels[valid] = kmeans.labels_

    return labels, kmeans.cluster_centers_, True


# =========================================
# SIMULATION (FULL CLOSED LOOP)
# =========================================

np.random.seed(42)

solver = RealPowerFlowSolver()

lambdas = np.linspace(0.5, 2.5, 120)

results = []
actions = []

c_hist = []
frag_hist = []
Vmin_hist = []

risk_hist = []
signal_hist = []
state_hist = []

prev_action = "STABILIZE"

for i, lam in enumerate(lambdas):

    # ---------------------------
    # SOLVER STEP
    # ---------------------------
    res = solver.step(lam, action=prev_action)

    results.append(res)
    actions.append(prev_action)

    if not res["converged"]:
        c_hist.append(np.nan)
        frag_hist.append(np.nan)
        Vmin_hist.append(np.nan)
        state_hist.append("COLLAPSED")
        prev_action = "EMERGENCY_SHED"
        continue

    V = res["V"]
    theta = res["theta"]

    Vmin = np.min(V)
    c_val, R, spread = compute_structural_state(V, theta, lam)

    c_hist.append(c_val)
    frag_hist.append((1 - R) * spread)
    Vmin_hist.append(Vmin)

    # ---------------------------
    # DERIVATIVES
    # ---------------------------
    x = lambdas[:i+1]
    c_arr = np.array(c_hist)

    dc, d2c = safe_derivatives(x, c_arr)

    # ---------------------------
    # MANIFOLD + OVERLAY
    # ---------------------------
    try:
        params = fit_manifold(c_arr, dc, d2c)
        residual = compute_residual(c_arr, dc, d2c, params)
        rift = np.column_stack([c_arr[-10:], dc[-10:]])
        distance = compute_distance(c_arr, dc, rift)
    except:
        residual = np.zeros_like(c_arr)
        distance = np.zeros_like(c_arr)

    # ---------------------------
    # CLUSTERING
    # ---------------------------
    labels, centers, cluster_ok = cluster_overlay_safe(distance, residual)

    # ---------------------------
    # PREDICTOR (ENHANCED)
    # ---------------------------
    pred = run_predictor(distance, d2c, labels)

    risk = np.asarray(pred["risk"])

    # 🔥 NEW: curvature boost
    curvature = np.abs(d2c)
    scale = np.nanmedian(curvature) + 1e-6
    risk = risk + 0.3 * np.tanh(curvature / scale)

    warnings = risk > 0.4
    ttc = pred["time_to_collapse"]

    risk_hist.append(risk[-1] if len(risk) else 0)

    # ---------------------------
    # STATES
    # ---------------------------
    if cluster_ok:
        try:
            gh = gh_filter(labels, centers)
            states = classify_states(c_arr, dc, d2c, frag_hist, labels, gh)
        except:
            states = ["CRITICAL"] * len(c_arr)
    else:
        states = ["CRITICAL"] * len(c_arr)

    current_state = states[-1]
    state_hist.append(current_state)

    # ---------------------------
    # POLICY (IMPROVED)
    # ---------------------------
    policy = run_intervention_policy(risk, warnings, ttc, states)

    signal = np.asarray(policy["signal"])

    # 🔥 NEW: smooth signal
    if len(signal) > 5:
        signal = gaussian_filter1d(signal, sigma=2)

    signal_hist.append(signal[-1] if len(signal) else 0)

    next_action = policy["actions"][-1]

    # 🔥 CRITICAL FIX
    if current_state == "COLLAPSED":
        next_action = "EMERGENCY_SHED"

    prev_action = next_action


# =========================================
# FINAL ARRAYS
# =========================================

c = np.array(c_hist)
frag = np.array(frag_hist)
Vmin = np.array(Vmin_hist)
risk = np.array(risk_hist)
signal = np.array(signal_hist)
states = state_hist

dc, d2c = safe_derivatives(lambdas, c)

params = fit_manifold(c, dc, d2c)
residual = compute_residual(c, dc, d2c, params)
distance = compute_distance(c, dc, np.column_stack([c[-10:], dc[-10:]]))


# =========================================
# PLOTS
# =========================================

fig, axes = plt.subplots(4, 1, figsize=(10, 12))

axes[0].plot(lambdas, Vmin)
axes[0].set_title("Voltage Collapse (Improved Closed Loop)")

axes[1].plot(lambdas, c)
axes[1].plot(lambdas, d2c)
axes[1].plot(lambdas, frag)

axes[2].scatter(distance, residual)

state_map = {"WARNING":0,"CRITICAL":1,"SAFE":2,"COLLAPSED":3}
y = [state_map.get(s,0) for s in states]
axes[3].scatter(range(len(states)), y)

fig_risk, ax = plt.subplots()
ax.plot(lambdas, risk)

fig_int, ax2 = plt.subplots()
ax2.plot(lambdas, signal)


# =========================================
# SAVE
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = f"APPLICATIONS/power_systems/nexah_ieee9/results/run_{timestamp}"
os.makedirs(results_dir, exist_ok=True)

np.save(os.path.join(results_dir, "risk.npy"), risk)

with open(os.path.join(results_dir, "actions.txt"), "w") as f:
    for a in actions:
        f.write(f"{a}\n")

with open(os.path.join(results_dir, "states.txt"), "w") as f:
    for s in states:
        f.write(f"{s}\n")

fig.savefig(os.path.join(results_dir, "plot.png"))
fig_risk.savefig(os.path.join(results_dir, "risk.png"))
fig_int.savefig(os.path.join(results_dir, "intervention.png"))

print("Saved to:", results_dir)
