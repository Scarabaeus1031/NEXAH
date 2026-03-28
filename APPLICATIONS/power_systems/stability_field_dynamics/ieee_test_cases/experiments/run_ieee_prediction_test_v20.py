# run_ieee_prediction_test_v20.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)

print("RUNNING IEEE PREDICTION TEST V20 (CURVATURE EARLY WARNING)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

LOADS = np.linspace(0.6, 5.0, 60)

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def compute_c_struct(theta, c, loops):
    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)

    regime_sep = theta_std * c_std
    c_struct = regime_sep * loops_mean

    return theta_std, c_std, loops_mean, regime_sep, c_struct


def safe_gradient(y, x):
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)

    grad = np.full_like(y, np.nan, dtype=float)
    mask = np.isfinite(y)

    if np.sum(mask) >= 2:
        grad_vals = np.gradient(y[mask], x[mask])
        grad[mask] = grad_vals

    return grad


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

rows = []

for load in LOADS:
    theta, c, loops, converged = ieee_to_nexah("ieee14", load_scale=load)

    if converged:
        theta_std, c_std, loops_mean, regime_sep, c_struct = compute_c_struct(theta, c, loops)
    else:
        theta_std = np.nan
        c_std = np.nan
        loops_mean = np.nan
        regime_sep = np.nan
        c_struct = np.nan

    rows.append({
        "load": load,
        "converged": converged,
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,
        "regime_separation": regime_sep,
        "c_struct": c_struct,
    })

df = pd.DataFrame(rows)


# ------------------------------------------------------------
# DERIVATIVES / CURVATURE
# ------------------------------------------------------------

df["dc_dload"] = safe_gradient(df["c_struct"].values, df["load"].values)
df["d2c_dload2"] = safe_gradient(df["dc_dload"].values, df["load"].values)


# ------------------------------------------------------------
# COLLAPSE DETECTION
# ------------------------------------------------------------

collapsed = df[df["converged"] == False]
collapse_load = collapsed.iloc[0]["load"] if len(collapsed) > 0 else np.nan


# ------------------------------------------------------------
# THRESHOLDS
# ------------------------------------------------------------

valid = df[df["converged"] == True].copy()

if len(valid) == 0:
    raise ValueError("No converged states found.")

max_c = valid["c_struct"].max()
max_dc = valid["dc_dload"].max()
max_d2c = valid["d2c_dload2"].max()

threshold_warning = 0.60 * max_c
threshold_critical = 0.85 * max_c
threshold_accel = 0.60 * max_d2c if np.isfinite(max_d2c) else np.nan


def classify_row(row):
    if not row["converged"]:
        return "COLLAPSED"
    if np.isfinite(row["c_struct"]) and row["c_struct"] >= threshold_critical:
        return "CRITICAL"
    if np.isfinite(row["c_struct"]) and row["c_struct"] >= threshold_warning:
        return "WARNING"
    return "SAFE"


df["state"] = df.apply(classify_row, axis=1)

df["accel_warning"] = (
    (df["converged"] == True) &
    np.isfinite(df["d2c_dload2"]) &
    (df["d2c_dload2"] >= threshold_accel)
)


# ------------------------------------------------------------
# FIRST EVENT LOADS
# ------------------------------------------------------------

warning_rows = df[(df["state"] == "WARNING") & (df["converged"] == True)]
critical_rows = df[(df["state"] == "CRITICAL") & (df["converged"] == True)]
accel_rows = df[(df["accel_warning"] == True) & (df["converged"] == True)]

first_warning_load = warning_rows.iloc[0]["load"] if len(warning_rows) > 0 else np.nan
first_critical_load = critical_rows.iloc[0]["load"] if len(critical_rows) > 0 else np.nan
first_accel_load = accel_rows.iloc[0]["load"] if len(accel_rows) > 0 else np.nan

warning_lead = collapse_load - first_warning_load if np.isfinite(collapse_load) and np.isfinite(first_warning_load) else np.nan
critical_lead = collapse_load - first_critical_load if np.isfinite(collapse_load) and np.isfinite(first_critical_load) else np.nan
accel_lead = collapse_load - first_accel_load if np.isfinite(collapse_load) and np.isfinite(first_accel_load) else np.nan


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

csv_path = os.path.join(OUTPUT_DIR, "ieee_prediction_test_v20.csv")
df.to_csv(csv_path, index=False)

print("\n--- RESULTS ---")
print(df)
print(f"\nSaved: {csv_path}")

print("\n--- V20 SUMMARY ---")
print(f"Collapse load         : {collapse_load}")
print(f"Max c_struct          : {max_c:.6f}")
print(f"Max dc/dload          : {max_dc:.6f}")
print(f"Max d2c/dload2        : {max_d2c:.6f}")
print(f"WARNING threshold     : {threshold_warning:.6f}")
print(f"CRITICAL threshold    : {threshold_critical:.6f}")
print(f"ACCEL threshold       : {threshold_accel:.6f}")
print(f"First ACCEL load      : {first_accel_load}")
print(f"First WARNING load    : {first_warning_load}")
print(f"First CRITICAL load   : {first_critical_load}")
print(f"ACCEL lead time       : {accel_lead}")
print(f"WARNING lead time     : {warning_lead}")
print(f"CRITICAL lead time    : {critical_lead}")


# ------------------------------------------------------------
# PLOTS
# ------------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(13, 10))

# 1) c_struct
ax = axes[0, 0]
ax.plot(df["load"], df["c_struct"], linewidth=2, label="c_struct")
ax.axhline(threshold_warning, linestyle="--", label="WARNING threshold")
ax.axhline(threshold_critical, linestyle="--", label="CRITICAL threshold")
if np.isfinite(collapse_load):
    ax.axvline(collapse_load, linestyle="--", color="red", label="collapse")

for _, row in df.iterrows():
    if row["state"] == "SAFE":
        color = "green"
    elif row["state"] == "WARNING":
        color = "orange"
    elif row["state"] == "CRITICAL":
        color = "red"
    else:
        color = "black"
    ax.scatter(row["load"], row["c_struct"], color=color, s=30)

ax.set_title("c_struct vs Load")
ax.set_xlabel("Load")
ax.set_ylabel("c_struct")
ax.grid()
ax.legend()

# 2) first derivative
ax = axes[0, 1]
ax.plot(df["load"], df["dc_dload"], linewidth=2, label="dc/dload")
if np.isfinite(collapse_load):
    ax.axvline(collapse_load, linestyle="--", color="red", label="collapse")
ax.set_title("First Derivative")
ax.set_xlabel("Load")
ax.set_ylabel("dc/dload")
ax.grid()
ax.legend()

# 3) second derivative / curvature
ax = axes[1, 0]
ax.plot(df["load"], df["d2c_dload2"], linewidth=2, label="d2c/dload2")
if np.isfinite(threshold_accel):
    ax.axhline(threshold_accel, linestyle="--", label="ACCEL threshold")
if np.isfinite(collapse_load):
    ax.axvline(collapse_load, linestyle="--", color="red", label="collapse")

accel_plot = df[df["accel_warning"] == True]
ax.scatter(accel_plot["load"], accel_plot["d2c_dload2"], color="purple", s=40, label="ACCEL warning")

ax.set_title("Curvature / Acceleration")
ax.set_xlabel("Load")
ax.set_ylabel("d2c/dload2")
ax.grid()
ax.legend()

# 4) phase progression
ax = axes[1, 1]
state_to_y = {
    "SAFE": 1,
    "WARNING": 2,
    "CRITICAL": 3,
    "COLLAPSED": 4,
}
state_to_color = {
    "SAFE": "green",
    "WARNING": "orange",
    "CRITICAL": "red",
    "COLLAPSED": "black",
}

for _, row in df.iterrows():
    ax.scatter(
        row["load"],
        state_to_y[row["state"]],
        color=state_to_color[row["state"]],
        s=50,
    )

ax.set_yticks([1, 2, 3, 4])
ax.set_yticklabels(["SAFE", "WARNING", "CRITICAL", "COLLAPSED"])
if np.isfinite(collapse_load):
    ax.axvline(collapse_load, linestyle="--", color="red", label="collapse")
ax.set_title("Phase Progression")
ax.set_xlabel("Load")
ax.grid(axis="x")
ax.legend()

plt.tight_layout()
plt.show()
