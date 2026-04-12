# =========================================
# IMPORTS
# =========================================

import numpy as np
from scipy.ndimage import gaussian_filter1d
import os
from datetime import datetime
import matplotlib.pyplot as plt

# 👉 GENERIC SOLVER
from APPLICATIONS.power_systems.nexah_ieeeX.simulation.powerflow_solver_generic import RealPowerFlowSolverGeneric

# NEXAH PIPELINE
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
from APPLICATIONS.power_systems.nexah_ieee9.decision.adaptive_policy_v2 import run_adaptive_policy

from sklearn.cluster import KMeans


# =========================================
# SAFE HELPERS
# =========================================

def safe_fill_nan(x, fill_value=0.0):
    x = np.asarray(x, dtype=float)
    if np.all(np.isnan(x)):
        return np.full_like(x, fill_value)
    med = np.nanmedian(x)
    return np.nan_to_num(x, nan=med)


def safe_max(x, default=0.0):
    x = np.asarray(x, dtype=float)
    if np.all(np.isnan(x)):
        return default
    return float(np.nanmax(x))


# =========================================
# CLUSTERING
# =========================================

def cluster_overlay_safe(distance, residual, k=3):
    X = np.column_stack([distance, residual])
    valid = np.isfinite(X).all(axis=1)

    if np.sum(valid) < k:
        return np.full(len(X), -1), np.zeros((k, 2))

    X_valid = X[valid]
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X_valid)

    labels = np.full(len(X), -1)
    labels[valid] = kmeans.labels_

    return labels, kmeans.cluster_centers_


# =========================================
# REAL SIMULATION (IEEE300)
# =========================================

np.random.seed(42)

solver = RealPowerFlowSolverGeneric(case_name="ieee300")

# 🔥 important: tighter range for large grid
lambdas = np.linspace(0.8, 1.6, 60)

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

    # simple bootstrap control (same as 118)
    if not res["converged"] or np.any(np.isnan(res["V"])):
        prev_action = "EMERGENCY_SHED"
    else:
        vmin = np.min(res["V"])
        if vmin < 0.8:
            prev_action = "EMERGENCY_SHED"
        elif vmin < 0.9:
            prev_action = "REDUCE_LOAD"
        else:
            prev_action = "STABILIZE"


# =========================================
# FEATURES
# =========================================

Vmin, c_list, frag_list = [], [], []

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

c = safe_fill_nan(c_list)
frag = safe_fill_nan(frag_list)
Vmin = np.array(Vmin)


# =========================================
# DERIVATIVES
# =========================================

def compute_derivatives(x, y):
    y = safe_fill_nan(y)
    y_smooth = gaussian_filter1d(y, sigma=1.0)
    dy = np.gradient(y_smooth, x)
    d2y = np.gradient(dy, x)
    return dy, d2y

dc, d2c = compute_derivatives(lambdas, c)


# =========================================
# MANIFOLD (ROBUST)
# =========================================

valid = np.isfinite(c) & np.isfinite(dc) & np.isfinite(d2c)

if np.sum(valid) < 30:   # 👈 leicht erhöht für große Netze
    print("⚠️ Not enough valid points for manifold → fallback")
    params = np.array([0.0, 0.0, 0.0])
    fit_ok = False
else:
    try:
        params = fit_manifold(c[valid], dc[valid], d2c[valid])
        fit_ok = True
    except Exception:
        print("⚠️ Manifold fit failed → fallback")
        params = np.array([0.0, 0.0, 0.0])
        fit_ok = False

print("Manifold params:", params)

# =========================================
# OVERLAY
# =========================================

if not fit_ok:
    residual = np.zeros_like(c)
    distance = np.zeros_like(c)
else:
    residual = safe_fill_nan(compute_residual(c, dc, d2c, params))

    valid_idx = np.where(valid)[0]

    if len(valid_idx) < 15:
        distance = np.zeros_like(c)
    else:
        rift = np.column_stack([c[valid_idx[-15:-5]], dc[valid_idx[-15:-5]]])
        distance = safe_fill_nan(compute_distance(c, dc, rift))


# =========================================
# CLUSTERING
# =========================================

labels, centers = cluster_overlay_safe(distance, residual)


# =========================================
# PREDICTION
# =========================================

try:
    pred = run_predictor(distance, d2c, labels)
    risk = safe_fill_nan(pred["risk"])
    warnings = np.asarray(pred["warnings"])
    ttc = np.asarray(pred["time_to_collapse"])
except:
    risk = np.zeros_like(c)
    warnings = np.zeros_like(c, dtype=bool)
    ttc = np.full_like(c, np.nan)

print("Max risk:", safe_max(risk))
print("Warning count:", np.sum(warnings))


# =========================================
# STATES
# =========================================

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


# =========================================
# POLICY
# =========================================

policy = run_intervention_policy(risk, warnings, ttc, states)

base_actions = policy["actions"]
signal = safe_fill_nan(policy["signal"])

actions = []
state_history = []
risk_slope = np.gradient(risk)

for i in range(len(base_actions)):
    state_history.append(states[i])

    act = run_adaptive_policy(
        base_actions[i],
        states[i],
        state_history,
        risk[i],
        risk_slope[i]
    )

    actions.append(act)

print("First 30 actions:")
print(actions[:30])


# =========================================
# VISUALIZATION
# =========================================

fig, axes = plt.subplots(3, 1, figsize=(10, 10))

axes[0].plot(lambdas, Vmin)
axes[0].set_title("Voltage Collapse (IEEE300)")

axes[1].plot(lambdas, risk)
axes[1].scatter(lambdas[warnings], risk[warnings])
axes[1].set_title("Risk Field")

y_map = {"STABILIZE": 0, "PREEMPTIVE_STABILIZE": 1, "REDUCE_LOAD": 2, "EMERGENCY_SHED": 3}
y = [y_map.get(a, 0) for a in actions]

axes[2].scatter(lambdas, y)
axes[2].set_yticks([0, 1, 2, 3])
axes[2].set_yticklabels(["STAB", "PRE", "REDUCE", "SHED"])
axes[2].set_title("Actions")


# =========================================
# SAVE
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = f"APPLICATIONS/power_systems/nexah_ieeeX/results/run_ieee300_{timestamp}"
os.makedirs(results_dir, exist_ok=True)

np.save(os.path.join(results_dir, "risk.npy"), risk)

with open(os.path.join(results_dir, "actions.txt"), "w") as f:
    for a in actions:
        f.write(f"{a}\n")

fig.savefig(os.path.join(results_dir, "plot.png"))

print("Saved to:", results_dir)
