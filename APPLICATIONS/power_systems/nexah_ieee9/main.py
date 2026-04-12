# =========================================
# IMPORTS
# =========================================

import numpy as np
from scipy.ndimage import gaussian_filter1d
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.nexah_ieee9.simulation.load_sweep import run_load_sweep
from APPLICATIONS.power_systems.nexah_ieee9.simulation.powerflow_solver_real import RealPowerFlowSolver

solver = RealPowerFlowSolver()

res = solver.step(lam, action=prev_action)
from APPLICATIONS.power_systems.nexah_ieee9.overlay.manifold_fit import fit_manifold
from APPLICATIONS.power_systems.nexah_ieee9.overlay.residual_distance import (
    compute_residual,
    compute_distance,
)
from APPLICATIONS.power_systems.nexah_ieee9.context.gh_filter import gh_filter

from APPLICATIONS.power_systems.nexah_ieee9.features.structural_state import compute_structural_state
from APPLICATIONS.power_systems.nexah_ieee9.decision.state_classifier import classify_states
from APPLICATIONS.power_systems.nexah_ieee9.analysis.predictor import run_predictor
from APPLICATIONS.power_systems.nexah_ieee9.control.intervention import run_intervention

from sklearn.cluster import KMeans


# =========================================
# FIXED CLUSTERING
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
# FIXED PLOT FUNCTION
# =========================================

def plot_all(
    lambdas,
    Vmin,
    c,
    dc,
    d2c,
    frag,
    distance,
    residual,
    states
):
    fig, axes = plt.subplots(4, 1, figsize=(10, 12))

    # --- Voltage ---
    axes[0].plot(lambdas, Vmin)
    axes[0].set_title("Voltage Collapse (Baseline)")

    # --- Features ---
    axes[1].plot(lambdas, c, label="c")
    axes[1].plot(lambdas, d2c, label="d2c")
    axes[1].plot(lambdas, frag, label="frag")
    axes[1].legend()

    # --- Residual vs Distance ---
    axes[2].scatter(distance, residual, c=distance)
    axes[2].set_title("Residual vs Distance")

    # --- States ---
    state_to_y = {
        "WARNING": 0,
        "CRITICAL": 1,
        "SAFE": 2,
        "COLLAPSED": 3,
    }

    y = [state_to_y.get(s, -1) for s in states]
    axes[3].scatter(np.arange(len(states)), y, s=30)
    axes[3].set_yticks([0, 1, 2, 3])
    axes[3].set_yticklabels(["WARNING", "CRITICAL", "SAFE", "COLLAPSED"])
    axes[3].set_title("NEXAH Decision Timeline")

    return fig


# =========================================
# TEMP POWERFLOW SOLVER
# =========================================

def powerflow_solver(lam):
    n = 9

    V = np.ones(n) * (1.0 - 0.15 * (lam - 1.0))
    V += np.random.normal(0, 0.01, n)

    theta = np.random.uniform(-0.1, 0.1, n)

    if lam > 2.2:
        V[:] = np.nan
        converged = False
    else:
        converged = True

    return {
        "V": V,
        "theta": theta,
        "converged": converged
    }


# =========================================
# 1. SIMULATION
# =========================================

np.random.seed(42)

lambdas = np.linspace(0.5, 2.5, 120)
results = run_load_sweep(powerflow_solver, lambdas)


# =========================================
# 2. FEATURES
# =========================================

Vmin = []
c_list = []
frag_list = []

for r in results:
    V = r["V"]
    theta = r["theta"]

    if not r["converged"] or np.any(np.isnan(V)):
        Vmin.append(np.nan)
        c_list.append(np.nan)
        frag_list.append(np.nan)
        continue

    Vmin.append(np.min(V))

    c_val, R, spread = compute_structural_state(V, theta, r["lambda"])
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

if np.sum(valid) < 20:
    raise ValueError("Not enough valid points for manifold fit")

threshold = np.percentile(np.abs(d2c[valid]), 95)
stable = valid & (np.abs(d2c) < threshold)

c_clean = c[stable]
dc_clean = dc[stable]
d2c_clean = d2c[stable]

cut = int(len(c_clean) * 0.85)

params = fit_manifold(
    c_clean[:cut],
    dc_clean[:cut],
    d2c_clean[:cut]
)

print("Manifold params:", params)


# =========================================
# 5. OVERLAY
# =========================================

residual = compute_residual(c, dc, d2c, params)

valid_indices = np.where(valid)[0]
if len(valid_indices) < 15:
    raise ValueError("Not enough valid indices to define rift")

rift_indices = valid_indices[-15:-5]

rift_points = np.column_stack([
    c[rift_indices],
    dc[rift_indices]
])

distance = compute_distance(c, dc, rift_points)


# =========================================
# 6. CLUSTERING
# =========================================

labels, centers = cluster_overlay_safe(distance, residual)
print("Cluster centers:", centers)


# =========================================
# 6.5 PREDICTION
# =========================================

pred = run_predictor(distance, d2c, labels)

risk = np.asarray(pred["risk"])
warnings = np.asarray(pred["warnings"], dtype=bool)
ttc = np.asarray(pred["time_to_collapse"])

print("Max risk:", np.nanmax(risk))
print("Warning count:", np.sum(warnings))


# =========================================
# 6.75 INTERVENTION
# =========================================

intervention = run_intervention(risk, ttc, warnings)

signal = np.asarray(intervention["signal"])
actions = intervention["actions"]

print("First 30 actions:")
print(actions[:30])


# =========================================
# 7. GH FILTER
# =========================================

gh_clusters = gh_filter(labels, centers)
print("GH clusters:", gh_clusters)


# =========================================
# 8. DECISION
# =========================================

states = classify_states(c, dc, d2c, frag, labels, gh_clusters)
print(states[:30])


# =========================================
# 9. VISUALIZATION
# =========================================

fig = plot_all(
    lambdas,
    Vmin,
    c,
    dc,
    d2c,
    frag,
    distance,
    residual,
    states
)
fig.tight_layout()

fig_risk, ax_risk = plt.subplots(figsize=(10, 4))
ax_risk.plot(lambdas, risk, label="risk")
ax_risk.scatter(lambdas[warnings], risk[warnings], label="warnings")
ax_risk.legend()
ax_risk.set_title("Collapse Risk")
fig_risk.tight_layout()

fig_int, ax_int = plt.subplots(figsize=(10, 4))
ax_int.plot(lambdas, signal, label="intervention signal")
ax_int.legend()
ax_int.set_title("Intervention Field")
fig_int.tight_layout()


# =========================================
# 10. SAVE RESULTS
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = f"APPLICATIONS/power_systems/nexah_ieee9/results/run_{timestamp}"
os.makedirs(results_dir, exist_ok=True)

# save arrays
np.save(os.path.join(results_dir, "c.npy"), c)
np.save(os.path.join(results_dir, "dc.npy"), dc)
np.save(os.path.join(results_dir, "d2c.npy"), d2c)
np.save(os.path.join(results_dir, "frag.npy"), frag)
np.save(os.path.join(results_dir, "distance.npy"), distance)
np.save(os.path.join(results_dir, "residual.npy"), residual)
np.save(os.path.join(results_dir, "risk.npy"), risk)
np.save(os.path.join(results_dir, "warnings.npy"), warnings)
np.save(os.path.join(results_dir, "ttc.npy"), ttc)
np.save(os.path.join(results_dir, "signal.npy"), signal)

# save states
with open(os.path.join(results_dir, "states.txt"), "w") as f:
    for s in states:
        f.write(f"{s}\n")

# save actions
with open(os.path.join(results_dir, "actions.txt"), "w") as f:
    for a in actions:
        f.write(f"{a}\n")

# save meta
meta = {
    "params": params.tolist(),
    "centers": centers.tolist(),
    "gh_clusters": gh_clusters,
    "max_risk": float(np.nanmax(risk)),
    "warning_count": int(np.sum(warnings)),
    "max_signal": float(np.nanmax(signal)),
}

with open(os.path.join(results_dir, "meta.json"), "w") as f:
    json.dump(meta, f, indent=2)

# save plots
fig.savefig(os.path.join(results_dir, "plot.png"))
fig_risk.savefig(os.path.join(results_dir, "risk.png"))
fig_int.savefig(os.path.join(results_dir, "intervention.png"))

print("Saved to:", results_dir)
