import os
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pandapower as pp
import pandapower.networks as pn


# ============================================================
# NEXAH v10.6 — Real IEEE9 Navigation with pandapower
# ============================================================

RESULT_DIR = "APPLICATIONS/power_systems/nexah_ieee9/results/controller_v10_6"
os.makedirs(RESULT_DIR, exist_ok=True)

STEPS = 180
LAMBDA_MIN = 0.60
LAMBDA_MAX = 2.20

# Navigation target in "field space"
TARGET_RISK = 0.03
TARGET_DISTANCE = 0.08

# Controller gains
K_FIELD = 0.90
K_TARGET = 0.55
K_DAMP = 0.18
DLAM_MAX = 0.04

# Risk / distance scaling
VM_CRIT_LOW = 0.93
VM_WARN_LOW = 0.97
LINE_WARN = 80.0
LINE_CRIT = 100.0


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def build_net():
    """Create fresh IEEE 9-bus network."""
    net = pn.case9()
    return net


def apply_lambda(net, lam):
    """
    Scale active and reactive loads with lambda.
    Generator setpoints remain unchanged for now.
    """
    if len(net.load) > 0:
        net.load["p_mw"] = net.load["p_mw"] * lam
        net.load["q_mvar"] = net.load["q_mvar"] * lam


def safe_runpp(net):
    """
    Run power flow safely and return success flag.
    """
    try:
        pp.runpp(
            net,
            init="results" if hasattr(net, "res_bus") and len(net.res_bus) else "flat",
            algorithm="nr",
            max_iteration=30,
            tolerance_mva=1e-8,
            enforce_q_lims=True,
            calculate_voltage_angles=True,
            trafo_model="t",
            check_connectivity=True,
        )
        return True
    except Exception:
        return False


def compute_metrics(net, converged):
    """
    Build real risk/distance metrics from power flow result.
    """
    if not converged:
        return {
            "risk": 1.0,
            "distance": 1.0,
            "vmin": np.nan,
            "vmax": np.nan,
            "line_max": np.nan,
            "vm_dev": np.nan,
        }

    vm = net.res_bus.vm_pu.values
    vmin = float(np.min(vm))
    vmax = float(np.max(vm))
    vm_dev = float(np.mean(np.abs(vm - 1.0)))

    if len(net.line) > 0 and "loading_percent" in net.res_line:
        line_max = float(np.max(net.res_line.loading_percent.values))
    else:
        line_max = 0.0

    # Voltage risk component
    if vmin >= VM_WARN_LOW:
        r_v = 0.0
    elif vmin <= VM_CRIT_LOW:
        r_v = 1.0
    else:
        r_v = (VM_WARN_LOW - vmin) / (VM_WARN_LOW - VM_CRIT_LOW)

    # Line loading risk component
    if line_max <= LINE_WARN:
        r_l = 0.0
    elif line_max >= LINE_CRIT:
        r_l = 1.0
    else:
        r_l = (line_max - LINE_WARN) / (LINE_CRIT - LINE_WARN)

    # Mean voltage deviation risk
    r_dev = np.clip(vm_dev / 0.08, 0.0, 1.0)

    # Combined real risk
    risk = float(np.clip(0.55 * r_v + 0.30 * r_l + 0.15 * r_dev, 0.0, 1.0))

    # Real distance to instability:
    # smaller is better, larger means further from nominal operation
    d_v = max(0.0, 1.0 - vmin)
    d_l = max(0.0, line_max / 100.0 - 1.0)
    distance = float(np.clip(0.70 * d_v + 0.30 * max(0.0, line_max / 100.0), 0.0, 2.0))

    return {
        "risk": risk,
        "distance": distance,
        "vmin": vmin,
        "vmax": vmax,
        "line_max": line_max,
        "vm_dev": vm_dev,
    }


def classify_state(risk, distance, converged):
    if not converged:
        return "DIVERGED"
    if risk < 0.08 and distance < 0.10:
        return "SAFE"
    if risk < 0.20 and distance < 0.18:
        return "WARNING"
    if risk < 0.40:
        return "CRITICAL"
    return "EMERGENCY"


def target_weight(step, steps):
    """
    Slowly increase target attraction over time.
    """
    x = step / max(1, steps - 1)
    return 0.15 + 0.85 * (1.0 - np.exp(-4.0 * x))


def field_weight(risk):
    """
    Stronger field awareness at higher risk.
    """
    return 1.0 + 1.8 * risk


# ------------------------------------------------------------
# Main closed loop
# ------------------------------------------------------------

rows = []

lam = LAMBDA_MIN
prev_risk = None
prev_dlam = 0.0

for step in range(STEPS):
    net = build_net()
    apply_lambda(net, lam)
    converged = safe_runpp(net)

    metrics = compute_metrics(net, converged)
    risk = metrics["risk"]
    distance = metrics["distance"]

    grad = 0.0 if prev_risk is None else (risk - prev_risk)

    # Field tendency:
    # - push lambda upward when system is too safe / far from target dynamics
    # - push downward when risk grows too much
    field_push = (TARGET_RISK - risk) * 0.85 + (TARGET_DISTANCE - distance) * 0.45

    # Target attraction in risk-distance space
    target_push = (TARGET_RISK - risk) * K_TARGET

    # Damping on gradient
    damp = -K_DAMP * grad

    w_f = K_FIELD * field_weight(risk)
    w_t = target_weight(step, STEPS)

    dlam = w_f * field_push + w_t * target_push + damp

    # Safety override if solver diverged or voltage too low
    if (not converged) or (metrics["vmin"] if converged else 0.0) < 0.90:
        dlam -= 0.08

    dlam = float(np.clip(dlam, -DLAM_MAX, DLAM_MAX))
    lam_next = float(np.clip(lam + dlam, LAMBDA_MIN, LAMBDA_MAX))

    state = classify_state(risk, distance, converged)

    print(
        f"[STEP {step}] "
        f"lambda={lam:.4f} risk={risk:.4f} dist={distance:.4f} "
        f"grad={grad:.4f} vmin={metrics['vmin'] if converged else np.nan:.4f} "
        f"line={metrics['line_max'] if converged else np.nan:.2f} "
        f"wF={w_f:.3f} wT={w_t:.3f} dlam={dlam:.4f} state={state}"
    )

    rows.append({
        "step": step,
        "lambda": lam,
        "risk": risk,
        "distance": distance,
        "grad": grad,
        "dlam": dlam,
        "w_field": w_f,
        "w_target": w_t,
        "vmin": metrics["vmin"],
        "vmax": metrics["vmax"],
        "line_max_loading_percent": metrics["line_max"],
        "vm_dev": metrics["vm_dev"],
        "converged": converged,
        "state": state,
    })

    prev_risk = risk
    prev_dlam = dlam
    lam = lam_next


# ------------------------------------------------------------
# Export
# ------------------------------------------------------------

df = pd.DataFrame(rows)
csv_path = os.path.join(RESULT_DIR, "output_v10_6_data.csv")
df.to_csv(csv_path, index=False)


# ------------------------------------------------------------
# Plot 1: main timeseries
# ------------------------------------------------------------

plt.figure(figsize=(14, 8))
plt.plot(df["step"], df["lambda"], label="lambda")
plt.plot(df["step"], df["risk"], label="risk")
plt.plot(df["step"], df["distance"], label="distance")
plt.plot(df["step"], df["vmin"], label="vmin")
plt.plot(df["step"], df["line_max_loading_percent"] / 100.0, label="line_loading/100")
plt.axhline(TARGET_DISTANCE, linestyle="--", label="target_distance")
plt.axhline(TARGET_RISK, linestyle="--", label="target_risk")
plt.title("NEXAH v10.6 Real IEEE9 Navigation")
plt.xlabel("Step")
plt.ylabel("Value")
plt.legend()
plt.grid(True, alpha=0.3)
plot_path = os.path.join(RESULT_DIR, "output_v10_6_plot.png")
plt.savefig(plot_path, dpi=200, bbox_inches="tight")
plt.close()


# ------------------------------------------------------------
# Plot 2: phase plot risk vs distance
# ------------------------------------------------------------

plt.figure(figsize=(10, 8))
sc = plt.scatter(
    df["risk"], df["distance"],
    c=df["step"], cmap="viridis", s=120
)
plt.plot(df["risk"], df["distance"], alpha=0.4)
plt.axhline(TARGET_DISTANCE, linestyle="--", label="target_distance")
plt.axvline(TARGET_RISK, linestyle="--", label="target_risk")
plt.xlabel("Risk")
plt.ylabel("Distance")
plt.title("NEXAH v10.6 Phase Plot (Risk vs Distance)")
plt.colorbar(sc, label="Step")
plt.legend()
plt.grid(True, alpha=0.3)
phase_path = os.path.join(RESULT_DIR, "output_v10_6_phase_risk_distance.png")
plt.savefig(phase_path, dpi=200, bbox_inches="tight")
plt.close()


print("\nSaved:")
print(csv_path)
print(plot_path)
print(phase_path)
