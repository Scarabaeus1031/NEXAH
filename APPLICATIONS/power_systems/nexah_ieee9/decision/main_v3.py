# =========================================
# IMPORTS
# =========================================

import numpy as np
from scipy.ndimage import gaussian_filter1d
import os
from datetime import datetime
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.nexah_ieee9.simulation.load_sweep import run_load_sweep

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
from APPLICATIONS.power_systems.nexah_ieee9.decision.adaptive_policy_v3 import run_adaptive_policy

from sklearn.cluster import KMeans


# =========================================
# CLUSTERING (SAFE)
# =========================================

def cluster_overlay_safe(distance, residual, k=3):
    X = np.column_stack([distance, residual])
    valid = np.isfinite(X).all(axis=1)

    if np.sum(valid) < k:
        print("⚠️ Not enough points for clustering → fallback")
        return np.full(len(X), -1), np.zeros((k, 2))

    X_valid = X[valid]
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X_valid)

    labels = np.full(len(X), -1)
    labels[valid] = kmeans.labels_

    return labels, kmeans.cluster_centers_


# =========================================
# SAFE HELPERS
# =========================================

def safe_fill_nan(x, fill_value=0.0):
    x = np.asarray(x, dtype=float)
    if np.all(np.isnan(x)):
        return np.full_like(x, fill_value, dtype=float)
    med = np.nanmedian(x)
    return np.nan_to_num(x, nan=med, posinf=med, neginf=med)


def safe_max(x, default=0.0):
    x = np.asarray(x, dtype=float)
    if np.all(np.isnan(x)):
        return default
    return float(np.nanmax(x))


# =========================================
# PLOT
# =========================================

def plot_all(lambdas, Vmin, c, dc, d2c, frag, distance, residual, states):
    fig, axes = plt.subplots(4, 1, figsize=(10, 12))

    axes[0].plot(lambdas, Vmin)
    axes[0].set_title("Voltage Collapse (Pre-Emptive Field Control v3)")

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
# SIMPLE SOLVER (BASELINE)
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

    return {"V": V, "theta": theta, "converged": converged}


# =========================================
# 1. SIMULATION
# =========================================

np.random.seed(42)

lambdas = np.linspace(0.5, 2.5, 120)
results = run_load_sweep(powerflow_solver, lambdas)


# =========================================
# 2. FEATURES
# =========================================

Vmin, c_list, frag_list = [], [], []

for r in results:
    V, theta = r["V"], r["theta"]

    if not r["converged"] or np.any(np.isnan(V)):
        Vmin.append(np.nan)
        c_list.append(np.nan)
        frag_list.append(np.nan)
        continue

    Vmin.append(np.min(V))
    c_val, R, spread = compute_structural_state(V, theta, r["lambda"])
    c_list.append(c_val)
    frag_list.append((1 - R) * spread)

c = np.array(c_list, dtype=float)
frag = np.array(frag_list, dtype=float)
Vmin = np.array(Vmin, dtype=float)


# =========================================
# 3. DERIVATIVES
# =========================================

def compute_derivatives_smooth(x, y):
    y = safe_fill_nan(y, fill_value=0.0)
    y_smooth = gaussian_filter1d(y, sigma=1.0)
    dy = np.gradient(y_smooth, x)
    d2y = np.gradient(dy, x)
    return dy, d2y

dc, d2c = compute_derivatives_smooth(lambdas, c)


# =========================================
# 4. MANIFOLD (ROBUST)
# =========================================

valid = np.isfinite(c) & np.isfinite(dc) & np.isfinite(d2c)

if np.sum(valid) < 20:
    print("⚠️ Not enough valid points for manifold → fallback")
    params = np.array([0.0, 0.0, 0.0])
    fit_ok = False
else:
    params = fit_manifold(c[valid], dc[valid], d2c[valid])
    fit_ok = True

print("Manifold params:", params)


# =========================================
# 5. OVERLAY (ROBUST)
# =========================================

if not fit_ok:
    residual = np.zeros_like(c)
    distance = np.zeros_like(c)
else:
    try:
        residual = compute_residual(c, dc, d2c, params)
        residual = safe_fill_nan(residual, fill_value=0.0)
    except Exception:
        print("⚠️ Residual failed → fallback")
        residual = np.zeros_like(c)

    valid_indices = np.where(valid)[0]

    if len(valid_indices) < 15:
        print("⚠️ Not enough points for rift → fallback")
        distance = np.zeros_like(c)
    else:
        try:
            rift_indices = valid_indices[-15:-5]
            rift_points = np.column_stack([
                c[rift_indices],
                dc[rift_indices]
            ])
            distance = compute_distance(c, dc, rift_points)
            distance = safe_fill_nan(distance, fill_value=0.0)
        except Exception:
            print("⚠️ Distance failed → fallback")
            distance = np.zeros_like(c)


# =========================================
# 6. CLUSTERING
# =========================================

labels, centers = cluster_overlay_safe(distance, residual)
print("Cluster centers:", centers)


# =========================================
# 6.5 PREDICTION (ROBUST)
# =========================================

try:
    pred = run_predictor(distance, d2c, labels)
except Exception:
    pred = {
        "risk": np.full_like(c, np.nan),
        "warnings": np.zeros_like(c, dtype=bool),
        "time_to_collapse": np.full_like(c, np.nan),
    }

if np.all(np.isnan(pred["risk"])):
    print("⚠️ Predictor failed → fallback risk")
    risk = np.zeros_like(c)
    warnings = np.zeros_like(c, dtype=bool)
    ttc = np.full_like(c, np.nan)
else:
    risk = np.asarray(pred["risk"], dtype=float)
    warnings = np.asarray(pred["warnings"], dtype=bool)
    ttc = np.asarray(pred["time_to_collapse"], dtype=float)

risk = safe_fill_nan(risk, fill_value=0.0)
ttc = safe_fill_nan(ttc, fill_value=np.nan)

print("Max risk:", safe_max(risk, default=0.0))
print("Warning count:", int(np.sum(warnings)))


# =========================================
# 7. DECISION (BASE STATES)
# =========================================

cluster_fallback = bool(np.all(centers == 0))

if cluster_fallback:
    print("⚠️ GH filter skipped → fallback states")
    states = []
    for i in range(len(c)):
        if not np.isfinite(c[i]):
            states.append("COLLAPSED")
        elif risk[i] > 0.7:
            states.append("CRITICAL")
        elif risk[i] > 0.4:
            states.append("WARNING")
        else:
            states.append("SAFE")
    gh_clusters = []
else:
    gh_clusters = gh_filter(labels, centers)
    print("GH clusters:", gh_clusters)
    states = classify_states(c, dc, d2c, frag, labels, gh_clusters)

print(states[:30])


# =========================================
# 8. POLICY + ADAPTIVE LAYER v3
# =========================================

policy = run_intervention_policy(risk, warnings, ttc, states)

base_actions = policy["actions"]
signal = np.asarray(policy["signal"], dtype=float)
signal = safe_fill_nan(signal, fill_value=0.0)

actions = []
state_history = []

risk_slope = np.gradient(risk)

for i in range(len(base_actions)):
    state_history.append(states[i])

    adaptive_action = run_adaptive_policy(
        base_action=base_actions[i],
        state=states[i],
        state_history=state_history,
        risk_value=risk[i],
        risk_slope=risk_slope[i],
        curvature_value=d2c[i],
        distance_value=distance[i],
    )

    actions.append(adaptive_action)

print("First 30 actions:")
print(actions[:30])


# =========================================
# 9. VISUALIZATION
# =========================================

fig = plot_all(lambdas, Vmin, c, dc, d2c, frag, distance, residual, states)

fig_risk, ax_risk = plt.subplots(figsize=(10, 4))
ax_risk.plot(lambdas, risk)
ax_risk.scatter(lambdas[warnings], risk[warnings])
ax_risk.set_title("Collapse Risk")

fig_int, ax_int = plt.subplots(figsize=(10, 4))
ax_int.plot(lambdas, signal)
ax_int.set_title("Intervention Field")


# =========================================
# 10. SAVE
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = f"APPLICATIONS/power_systems/nexah_ieee9/results/run_{timestamp}"
os.makedirs(results_dir, exist_ok=True)

np.save(os.path.join(results_dir, "risk.npy"), risk)
np.save(os.path.join(results_dir, "distance.npy"), distance)
np.save(os.path.join(results_dir, "residual.npy"), residual)
np.save(os.path.join(results_dir, "d2c.npy"), d2c)

with open(os.path.join(results_dir, "actions_base.txt"), "w") as f:
    for a in base_actions:
        f.write(f"{a}\n")

with open(os.path.join(results_dir, "actions_adaptive.txt"), "w") as f:
    for a in actions:
        f.write(f"{a}\n")

with open(os.path.join(results_dir, "states.txt"), "w") as f:
    for s in states:
        f.write(f"{s}\n")

meta = {
    "params": params.tolist(),
    "centers": centers.tolist(),
    "max_risk": safe_max(risk, default=0.0),
    "warning_count": int(np.sum(warnings)),
    "fit_ok": bool(fit_ok),
    "cluster_fallback": cluster_fallback,
    "gh_clusters": gh_clusters,
    "policy_version": "v3",
}

with open(os.path.join(results_dir, "meta.json"), "w") as f:
    import json
    json.dump(meta, f, indent=2)

fig.savefig(os.path.join(results_dir, "plot.png"))
fig_risk.savefig(os.path.join(results_dir, "risk.png"))
fig_int.savefig(os.path.join(results_dir, "intervention.png"))

print("Saved to:", results_dir)
