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
    return np.nan_to_num(x, nan=med, posinf=med, neginf=med)


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
        print("⚠️ Not enough points for clustering → fallback")
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
lambdas = np.linspace(0.9, 1.15, 120)

results = []
prev_action = None

for lam in lambdas:
    res = solver.step(lam, action=prev_action)

    results.append({
        "lambda": lam,
        "V": res["V"],
        "theta": res["theta"],
        "converged": res["converged"],
    })

    # simple bootstrap control
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
# DEBUG: RAW SIMULATION HEALTH
# =========================================

converged_flags = np.array([r["converged"] for r in results], dtype=bool)
num_converged = int(np.sum(converged_flags))

raw_vmin = []
for r in results:
    V = r["V"]
    if r["converged"] and np.all(np.isfinite(V)):
        raw_vmin.append(np.min(V))
    else:
        raw_vmin.append(np.nan)

raw_vmin = np.asarray(raw_vmin, dtype=float)

print("Converged steps:", num_converged, "/", len(results))
print("Raw Vmin nan count:", int(np.sum(~np.isfinite(raw_vmin))))
print("Raw Vmin std:", float(np.nanstd(raw_vmin)) if np.any(np.isfinite(raw_vmin)) else np.nan)

if np.any(np.isfinite(raw_vmin)):
    print("Raw Vmin min/max:", float(np.nanmin(raw_vmin)), float(np.nanmax(raw_vmin)))


# =========================================
# FEATURES (LARGE GRID MODE)
# =========================================

Vmin, c_list, frag_list = [], [], []

for r in results:
    V = r["V"]

    if not r["converged"] or np.any(np.isnan(V)):
        Vmin.append(np.nan)
        c_list.append(np.nan)
        frag_list.append(np.nan)
        continue

    vmin = np.min(V)
    vmean = np.mean(V)
    vstd = np.std(V)

    centered = V - vmean
    vskew = np.mean(centered**3)

    # robust large-grid structural signal
    c_val = vmin + 0.5 * vstd + 0.1 * vskew
    frag_val = vstd

    Vmin.append(vmin)
    c_list.append(c_val)
    frag_list.append(frag_val)

Vmin = np.asarray(Vmin, dtype=float)
c = np.asarray(c_list, dtype=float)
frag = np.asarray(frag_list, dtype=float)

print("Raw feature stds:")
print("Vmin std:", float(np.nanstd(Vmin)) if np.any(np.isfinite(Vmin)) else np.nan)
print("c std:", float(np.nanstd(c)) if np.any(np.isfinite(c)) else np.nan)
print("frag std:", float(np.nanstd(frag)) if np.any(np.isfinite(frag)) else np.nan)

# fallback if raw feature is too flat
if np.sum(np.isfinite(c)) < 20 or np.nanstd(c) < 1e-8:
    print("⚠️ Structural signal too flat → using Vmin fallback")
    c = Vmin.copy()

if np.sum(np.isfinite(frag)) < 20 or np.nanstd(frag) < 1e-8:
    print("⚠️ Fragmentation too flat → using rolling Vmin spread fallback")
    frag_fb = []
    for i in range(len(Vmin)):
        lo = max(0, i - 2)
        hi = min(len(Vmin), i + 3)
        frag_fb.append(np.nanstd(Vmin[lo:hi]))
    frag = np.asarray(frag_fb, dtype=float)


# =========================================
# DERIVATIVES
# =========================================

def compute_derivatives(x, y):
    y = safe_fill_nan(y)
    y_smooth = gaussian_filter1d(y, sigma=1.0)
    dy = np.gradient(y_smooth, x)
    d2y = np.gradient(dy, x)
    return dy, d2y

# only now fill
c = safe_fill_nan(c)
frag = safe_fill_nan(frag)
Vmin = safe_fill_nan(Vmin)

dc, d2c = compute_derivatives(lambdas, c)


# =========================================
# MANIFOLD
# =========================================

valid = np.isfinite(c) & np.isfinite(dc) & np.isfinite(d2c)

print("Valid points for manifold:", int(np.sum(valid)))
print("c std:", float(np.nanstd(c)))
print("dc std:", float(np.nanstd(dc)))
print("d2c std:", float(np.nanstd(d2c)))

if np.sum(valid) < 20 or np.nanstd(c) < 1e-10:
    print("⚠️ Not enough structure for manifold → fallback")
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
    try:
        residual = safe_fill_nan(compute_residual(c, dc, d2c, params))
    except Exception:
        print("⚠️ Residual failed → fallback")
        residual = np.zeros_like(c)

    valid_idx = np.where(valid)[0]

    if len(valid_idx) < 15:
        print("⚠️ Not enough points for rift → fallback")
        distance = np.zeros_like(c)
    else:
        try:
            rift = np.column_stack([c[valid_idx[-15:-5]], dc[valid_idx[-15:-5]]])
            distance = safe_fill_nan(compute_distance(c, dc, rift))
        except Exception:
            print("⚠️ Distance failed → fallback")
            distance = np.zeros_like(c)


# =========================================
# CLUSTERING
# =========================================

labels, centers = cluster_overlay_safe(distance, residual)
print("Cluster centers:", centers)


# =========================================
# PREDICTION
# =========================================

try:
    pred = run_predictor(distance, d2c, labels)
    risk = safe_fill_nan(pred["risk"])
    warnings = np.asarray(pred["warnings"], dtype=bool)
    ttc = np.asarray(pred["time_to_collapse"], dtype=float)
except Exception:
    print("⚠️ Predictor failed → fallback")
    risk = np.zeros_like(c)
    warnings = np.zeros_like(c, dtype=bool)
    ttc = np.full_like(c, np.nan)

if np.nanstd(risk) < 1e-8:
    print("⚠️ Risk too flat → using Vmin-based fallback risk")
    vmax = np.nanmax(Vmin)
    vmin = np.nanmin(Vmin)

    if np.isfinite(vmax) and np.isfinite(vmin) and vmax > vmin:
        risk = 1.0 - (Vmin - vmin) / (vmax - vmin)
        risk = np.clip(risk, 0.0, 1.0)
        warnings = risk > 0.4
    else:
        risk = np.zeros_like(c)
        warnings = np.zeros_like(c, dtype=bool)

print("Max risk:", safe_max(risk))
print("Warning count:", int(np.sum(warnings)))


# =========================================
# STATES
# =========================================

states = []
for i in range(len(c)):
    if not np.isfinite(raw_vmin[i]):
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
        risk_slope[i],
    )

    actions.append(act)

print("First 30 actions:")
print(actions[:30])


# =========================================
# VISUALIZATION
# =========================================

fig, axes = plt.subplots(4, 1, figsize=(10, 12))

axes[0].plot(lambdas, Vmin)
axes[0].set_title("Voltage Collapse (IEEE300)")

axes[1].plot(lambdas, c, label="c")
axes[1].plot(lambdas, d2c, label="d2c")
axes[1].plot(lambdas, frag, label="frag")
axes[1].legend()
axes[1].set_title("Structural Features")

axes[2].plot(lambdas, risk)
axes[2].scatter(lambdas[warnings], risk[warnings])
axes[2].set_title("Risk Field")

y_map = {
    "STABILIZE": 0,
    "PREEMPTIVE_STABILIZE": 1,
    "REDUCE_LOAD": 2,
    "EMERGENCY_SHED": 3,
}
y = [y_map.get(a, 0) for a in actions]

axes[3].scatter(lambdas, y)
axes[3].set_yticks([0, 1, 2, 3])
axes[3].set_yticklabels(["STAB", "PRE", "REDUCE", "SHED"])
axes[3].set_title("Actions")

fig.tight_layout()


# =========================================
# SAVE
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = f"APPLICATIONS/power_systems/nexah_ieeeX/results/run_ieee300_{timestamp}"
os.makedirs(results_dir, exist_ok=True)

np.save(os.path.join(results_dir, "risk.npy"), risk)
np.save(os.path.join(results_dir, "c.npy"), c)
np.save(os.path.join(results_dir, "d2c.npy"), d2c)
np.save(os.path.join(results_dir, "frag.npy"), frag)
np.save(os.path.join(results_dir, "Vmin.npy"), Vmin)
np.save(os.path.join(results_dir, "distance.npy"), distance)
np.save(os.path.join(results_dir, "residual.npy"), residual)

with open(os.path.join(results_dir, "actions.txt"), "w") as f:
    for a in actions:
        f.write(f"{a}\n")

with open(os.path.join(results_dir, "states.txt"), "w") as f:
    for s in states:
        f.write(f"{s}\n")

fig.savefig(os.path.join(results_dir, "plot.png"))

print("Saved to:", results_dir)
