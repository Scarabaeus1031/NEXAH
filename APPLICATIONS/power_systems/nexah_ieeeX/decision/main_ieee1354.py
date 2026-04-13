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
# HELPERS
# =========================================

def safe_fill_nan(x, fill_value=0.0):
    x = np.asarray(x, dtype=float)
    if np.all(np.isnan(x)):
        return np.full_like(x, fill_value)
    med = np.nanmedian(x)
    return np.nan_to_num(x, nan=med, posinf=med, neginf=med)


# =========================================
# SOLVER INIT
# =========================================

np.random.seed(42)

solver = RealPowerFlowSolverGeneric(case_name="ieee1354")

# 🔥 critical window (works best for large grids)
lambdas = np.linspace(0.92, 1.12, 120)


# =========================================
# SIMULATION
# =========================================

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

    # bootstrap control
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

    if not r["converged"] or np.any(np.isnan(V)):
        Vmin.append(np.nan)
        c_list.append(np.nan)
        frag_list.append(np.nan)
        continue

    vmin = np.min(V)
    vstd = np.std(V)

    # 🔥 robust large-grid signal
    c_val = vmin + 0.5 * vstd
    frag_val = vstd

    Vmin.append(vmin)
    c_list.append(c_val)
    frag_list.append(frag_val)

Vmin = safe_fill_nan(Vmin)
c = safe_fill_nan(c_list)
frag = safe_fill_nan(frag_list)


# =========================================
# DERIVATIVES
# =========================================

def compute_derivatives(x, y):
    y_smooth = gaussian_filter1d(y, sigma=1.0)
    dy = np.gradient(y_smooth, x)
    d2y = np.gradient(dy, x)
    return dy, d2y

dc, d2c = compute_derivatives(lambdas, c)


# =========================================
# MANIFOLD
# =========================================

valid = np.isfinite(c) & np.isfinite(dc) & np.isfinite(d2c)

if np.sum(valid) < 20:
    params = np.array([0.0, 0.0, 0.0])
    fit_ok = False
else:
    try:
        params = fit_manifold(c[valid], dc[valid], d2c[valid])
        fit_ok = True
    except:
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

    idx = np.where(valid)[0]
    if len(idx) > 20:
        rift = np.column_stack([c[idx[-20:-10]], dc[idx[-20:-10]]])
        distance = safe_fill_nan(compute_distance(c, dc, rift))
    else:
        distance = np.zeros_like(c)


# =========================================
# CLUSTERING
# =========================================

X = np.column_stack([distance, residual])
valid_cl = np.isfinite(X).all(axis=1)

if np.sum(valid_cl) > 10:
    kmeans = KMeans(n_clusters=3, random_state=0, n_init=10).fit(X[valid_cl])
    labels = np.full(len(X), -1)
    labels[valid_cl] = kmeans.labels_
else:
    labels = np.full(len(X), -1)


# =========================================
# PREDICTION
# =========================================

try:
    pred = run_predictor(distance, d2c, labels)
    risk = safe_fill_nan(pred["risk"])
    warnings = pred["warnings"]
    ttc = pred["time_to_collapse"]
except:
    risk = np.zeros_like(c)
    warnings = np.zeros_like(c, dtype=bool)
    ttc = np.full_like(c, np.nan)

# fallback
if np.nanstd(risk) < 1e-8:
    vmax = np.max(Vmin)
    vmin = np.min(Vmin)
    risk = 1.0 - (Vmin - vmin) / (vmax - vmin)
    risk = np.clip(risk, 0.0, 1.0)
    warnings = risk > 0.4

print("Max risk:", np.max(risk))


# =========================================
# POLICY
# =========================================

policy = run_intervention_policy(risk, warnings, ttc, ["SAFE"]*len(risk))

actions = []
state_hist = []
risk_slope = np.gradient(risk)

for i, a in enumerate(policy["actions"]):
    state_hist.append("SAFE")

    act = run_adaptive_policy(
        a,
        "SAFE",
        state_hist,
        risk[i],
        risk_slope[i],
    )

    actions.append(act)


# =========================================
# PLOT
# =========================================

fig, ax = plt.subplots(3, 1, figsize=(10, 10))

ax[0].plot(lambdas, Vmin)
ax[0].set_title("IEEE1354 Voltage")

ax[1].plot(lambdas, risk)
ax[1].set_title("Risk")

y_map = {"STABILIZE":0,"PREEMPTIVE_STABILIZE":1,"REDUCE_LOAD":2,"EMERGENCY_SHED":3}
y = [y_map.get(a,0) for a in actions]

ax[2].scatter(lambdas, y)
ax[2].set_yticks([0,1,2,3])
ax[2].set_yticklabels(["STAB","PRE","REDUCE","SHED"])

fig.tight_layout()


# =========================================
# SAVE
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
path = f"APPLICATIONS/power_systems/nexah_ieeeX/results/run_ieee1354_{timestamp}"
os.makedirs(path, exist_ok=True)

fig.savefig(os.path.join(path, "plot.png"))

print("Saved to:", path)
