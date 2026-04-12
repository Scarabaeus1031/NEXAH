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
from APPLICATIONS.power_systems.nexah_ieee9.decision.adaptive_policy import run_adaptive_policy

from sklearn.cluster import KMeans


# =========================================
# CONFIG
# =========================================

N_STEPS = 120
LAMBDAS = np.linspace(0.5, 2.5, N_STEPS)
CLUSTER_K = 3


# =========================================
# HELPERS
# =========================================

def safe_fill(y, default=0.0):
    y = np.asarray(y, dtype=float)
    finite = np.isfinite(y)
    if np.any(finite):
        fill = np.nanmedian(y[finite])
    else:
        fill = default
    return np.nan_to_num(y, nan=fill, posinf=fill, neginf=fill)


def safe_derivatives(x, y, sigma=1.0):
    x = np.asarray(x, dtype=float)
    y = safe_fill(y, default=0.0)

    y_smooth = gaussian_filter1d(y, sigma=sigma)
    dy = np.gradient(y_smooth, x)
    d2y = np.gradient(dy, x)
    return dy, d2y


def safe_cluster(distance, residual, k=3):
    X = np.column_stack([distance, residual])
    valid = np.isfinite(X).all(axis=1)

    labels = np.full(len(X), -1, dtype=int)

    if np.sum(valid) < max(k, 8):
        centers = np.full((k, 2), np.nan)
        return labels, centers, False

    try:
        kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X[valid])
        labels[valid] = kmeans.labels_
        return labels, kmeans.cluster_centers_, True
    except Exception:
        centers = np.full((k, 2), np.nan)
        return labels, centers, False


def safe_fit_manifold(c, dc, d2c):
    c = np.asarray(c, dtype=float)
    dc = np.asarray(dc, dtype=float)
    d2c = np.asarray(d2c, dtype=float)

    valid = np.isfinite(c) & np.isfinite(dc) & np.isfinite(d2c)
    valid &= (np.abs(c) > 1e-8)

    if np.sum(valid) < 10:
        return np.array([1.0, 1.0, 1.0]), False

    try:
        threshold = np.percentile(np.abs(d2c[valid]), 95)
        stable = valid & (np.abs(d2c) < threshold)
        if np.sum(stable) < 10:
            stable = valid

        params = fit_manifold(c[stable], dc[stable], d2c[stable])
        return params, True
    except Exception:
        return np.array([1.0, 1.0, 1.0]), False


def safe_overlay(c, dc, d2c, params):
    c = np.asarray(c, dtype=float)
    dc = np.asarray(dc, dtype=float)
    d2c = np.asarray(d2c, dtype=float)

    try:
        residual = compute_residual(c, dc, d2c, params)
    except Exception:
        residual = np.full_like(c, np.nan)

    valid = np.isfinite(c) & np.isfinite(dc)
    idx = np.where(valid)[0]

    if len(idx) >= 10:
        tail = idx[-10:]
        rift_points = np.column_stack([c[tail], dc[tail]])
        try:
            distance = compute_distance(c, dc, rift_points)
        except Exception:
            distance = np.full_like(c, np.nan)
    else:
        distance = np.full_like(c, np.nan)

    return residual, distance


def fallback_states(converged_mask, risk):
    states = []
    for ok, r in zip(converged_mask, risk):
        if not ok:
            states.append("COLLAPSED")
        elif r >= 0.75:
            states.append("CRITICAL")
        elif r >= 0.45:
            states.append("WARNING")
        else:
            states.append("SAFE")
    return states


def enhanced_predictor(distance, d2c, labels):
    """
    Wraps the existing predictor with NaN safety and curvature-aware boosting.
    """
    distance = safe_fill(distance, default=0.0)
    d2c = safe_fill(d2c, default=0.0)

    try:
        pred = run_predictor(distance, d2c, labels)
        risk = np.asarray(pred["risk"], dtype=float)
        warnings = np.asarray(pred["warnings"], dtype=bool)
        ttc = np.asarray(pred["time_to_collapse"], dtype=float)
    except Exception:
        n = len(distance)
        risk = np.zeros(n, dtype=float)
        warnings = np.zeros(n, dtype=bool)
        ttc = np.full(n, np.nan, dtype=float)

    # curvature boost
    curvature = np.abs(d2c)
    scale = np.nanmedian(curvature[np.isfinite(curvature)]) if np.any(np.isfinite(curvature)) else 1.0
    scale = max(scale, 1e-6)

    risk = risk + 0.30 * np.tanh(curvature / scale)
    risk = np.clip(risk, 0.0, 1.0)

    # refresh warnings from improved risk
    warnings = risk > 0.40

    return risk, warnings, ttc


def plot_all(lambdas, Vmin, c, dc, d2c, frag, distance, residual, states):
    fig, axes = plt.subplots(4, 1, figsize=(10, 12))

    axes[0].plot(lambdas, Vmin)
    axes[0].set_title("Voltage Collapse (Adaptive Closed Loop)")

    axes[1].plot(lambdas, c, label="c")
    axes[1].plot(lambdas, d2c, label="d2c")
    axes[1].plot(lambdas, frag, label="frag")
    axes[1].legend()

    axes[2].scatter(
        safe_fill(distance, 0.0),
        safe_fill(residual, 0.0),
        c=safe_fill(distance, 0.0),
        s=18
    )
    axes[2].set_title("Residual vs Distance")

    state_to_y = {
        "WARNING": 0,
        "CRITICAL": 1,
        "SAFE": 2,
        "COLLAPSED": 3,
    }
    y = [state_to_y.get(s, -1) for s in states]
    axes[3].scatter(np.arange(len(states)), y, s=20)
    axes[3].set_yticks([0, 1, 2, 3])
    axes[3].set_yticklabels(["WARNING", "CRITICAL", "SAFE", "COLLAPSED"])
    axes[3].set_title("NEXAH Decision Timeline")

    return fig


# =========================================
# FULL CLOSED LOOP
# =========================================

np.random.seed(42)

solver = RealPowerFlowSolver()

results = []
applied_actions = []

c_hist = []
frag_hist = []
Vmin_hist = []

risk_hist = []
warning_hist = []
ttc_hist = []
signal_hist = []
state_hist = []

prev_action = "STABILIZE"

for i, lam in enumerate(LAMBDAS):
    # -------------------------------------
    # 1. SOLVER STEP
    # -------------------------------------
    res = solver.step(lam, action=prev_action)

    results.append({
        "lambda": lam,
        "V": res["V"],
        "theta": res["theta"],
        "converged": res["converged"],
    })
    applied_actions.append(prev_action)

    # -------------------------------------
    # 2. FEATURE UPDATE
    # -------------------------------------
    if not res["converged"] or np.any(np.isnan(res["V"])):
        Vmin_hist.append(np.nan)
        c_hist.append(np.nan)
        frag_hist.append(np.nan)
    else:
        V = res["V"]
        theta = res["theta"]

        Vmin_hist.append(float(np.min(V)))

        c_val, R, spread = compute_structural_state(V, theta, lam)
        c_hist.append(float(c_val))
        frag_hist.append(float((1 - R) * spread))

    # -------------------------------------
    # 3. LOCAL FIELD MODEL
    # -------------------------------------
    x_local = LAMBDAS[:i + 1]
    c_local = np.array(c_hist, dtype=float)
    frag_local = np.array(frag_hist, dtype=float)
    converged_local = np.array([
        r["converged"] and not np.any(np.isnan(r["V"])) for r in results
    ], dtype=bool)

    dc_local, d2c_local = safe_derivatives(x_local, c_local)
    params_local, fit_ok = safe_fit_manifold(c_local, dc_local, d2c_local)
    residual_local, distance_local = safe_overlay(c_local, dc_local, d2c_local, params_local)

    labels_local, centers_local, cluster_ok = safe_cluster(distance_local, residual_local, k=CLUSTER_K)

    # -------------------------------------
    # 4. PREDICTION
    # -------------------------------------
    risk_local, warnings_local, ttc_local = enhanced_predictor(
        distance_local, d2c_local, labels_local
    )

    # slope for adaptive policy
    risk_smooth_local = gaussian_filter1d(safe_fill(risk_local, 0.0), sigma=2)
    if len(risk_smooth_local) >= 2:
        risk_slope_local = np.gradient(risk_smooth_local)
    else:
        risk_slope_local = np.zeros_like(risk_smooth_local)

    # -------------------------------------
    # 5. STATE ESTIMATION
    # -------------------------------------
    if cluster_ok and np.any(np.isfinite(centers_local)):
        try:
            gh_local = gh_filter(labels_local, centers_local)
            states_local = classify_states(
                c_local, dc_local, d2c_local, frag_local, labels_local, gh_local
            )
        except Exception:
            states_local = fallback_states(converged_local, risk_local)
    else:
        states_local = fallback_states(converged_local, risk_local)

    current_state = states_local[-1]

    # -------------------------------------
    # 6. BASE POLICY
    # -------------------------------------
    policy_local = run_intervention_policy(
        risk_local,
        warnings_local,
        ttc_local,
        states_local
    )

    signal_local = np.asarray(policy_local["signal"], dtype=float)
    if len(signal_local) > 5:
        signal_local = gaussian_filter1d(signal_local, sigma=2)

    base_action = policy_local["actions"][-1] if len(policy_local["actions"]) else "STABILIZE"

    # -------------------------------------
    # 7. ADAPTIVE POLICY WRAPPER
    # -------------------------------------
    next_action = run_adaptive_policy(
        base_action=base_action,
        state=current_state,
        state_history=state_hist,
        risk_value=float(risk_local[-1]),
        risk_slope=float(risk_slope_local[-1]),
    )

    # additional guard: never stay NONE outside safe regime
    if next_action == "NONE" and current_state != "SAFE":
        next_action = "STABILIZE"

    prev_action = next_action

    # -------------------------------------
    # 8. STORE STEP DIAGNOSTICS
    # -------------------------------------
    state_hist.append(current_state)
    risk_hist.append(float(risk_local[-1]))
    warning_hist.append(bool(warnings_local[-1]))
    ttc_hist.append(float(ttc_local[-1]) if np.isfinite(ttc_local[-1]) else np.nan)
    signal_hist.append(float(signal_local[-1]) if len(signal_local) else 0.0)


# =========================================
# POST ANALYSIS
# =========================================

lambdas = LAMBDAS
Vmin = np.array(Vmin_hist, dtype=float)
c = np.array(c_hist, dtype=float)
frag = np.array(frag_hist, dtype=float)

dc, d2c = safe_derivatives(lambdas, c)
params, fit_ok = safe_fit_manifold(c, dc, d2c)
residual, distance = safe_overlay(c, dc, d2c, params)

labels, centers, cluster_ok = safe_cluster(distance, residual, k=CLUSTER_K)

risk = np.array(risk_hist, dtype=float)
warnings = np.array(warning_hist, dtype=bool)
ttc = np.array(ttc_hist, dtype=float)
signal = np.array(signal_hist, dtype=float)
states = list(state_hist)

if cluster_ok and np.any(np.isfinite(centers)):
    try:
        gh_clusters = gh_filter(labels, centers)
    except Exception:
        gh_clusters = []
else:
    gh_clusters = []

print("Manifold params:", params)
print("Cluster centers:", centers)
print("Max risk:", np.nanmax(risk) if np.any(np.isfinite(risk)) else 0.0)
print("Warning count:", int(np.sum(warnings)))
print("GH clusters:", gh_clusters)
print(states[:30])
print("First 30 actions:")
print(applied_actions[:30])


# =========================================
# VISUALIZATION
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
# SAVE RESULTS
# =========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = f"APPLICATIONS/power_systems/nexah_ieee9/results/run_{timestamp}"
os.makedirs(results_dir, exist_ok=True)

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

with open(os.path.join(results_dir, "states.txt"), "w") as f:
    for s in states:
        f.write(f"{s}\n")

with open(os.path.join(results_dir, "actions.txt"), "w") as f:
    for a in applied_actions:
        f.write(f"{a}\n")

meta = {
    "params": params.tolist() if np.all(np.isfinite(params)) else [1.0, 1.0, 1.0],
    "centers": centers.tolist() if np.any(np.isfinite(centers)) else [],
    "gh_clusters": gh_clusters,
    "max_risk": float(np.nanmax(risk)) if np.any(np.isfinite(risk)) else 0.0,
    "warning_count": int(np.sum(warnings)),
    "max_signal": float(np.nanmax(signal)) if np.any(np.isfinite(signal)) else 0.0,
    "cluster_ok": bool(cluster_ok),
    "fit_ok": bool(fit_ok),
    "closed_loop": True,
    "adaptive_policy": True,
}

with open(os.path.join(results_dir, "meta.json"), "w") as f:
    json.dump(meta, f, indent=2)

fig.savefig(os.path.join(results_dir, "plot.png"))
fig_risk.savefig(os.path.join(results_dir, "risk.png"))
fig_int.savefig(os.path.join(results_dir, "intervention.png"))

print("Saved to:", results_dir)
