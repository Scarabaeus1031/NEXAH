# run_ieee_prediction_test_v19.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    detect_gh_corridor,
)

print("RUNNING IEEE PREDICTION TEST V19 (GH + COLLAPSE PHASE)")

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

LOADS = np.linspace(0.6, 5.0, 40)

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def compute_metrics(theta, c, loops):
    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)

    regime_separation = theta_std * c_std
    c_struct = regime_separation * loops_mean

    return theta_std, c_std, loops_mean, regime_separation, c_struct


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

results = []

for load in LOADS:
    theta, c, loops, converged = ieee_to_nexah("ieee14", load_scale=load)

    if converged:
        theta_std, c_std, loops_mean, regime_sep, c_struct = compute_metrics(theta, c, loops)

        gh = detect_gh_corridor(theta, c, loops)
        gh_points = len(gh["theta_corridor"])
        gh_width_theta = np.ptp(gh["theta_corridor"]) if gh_points > 0 else np.nan
        gh_width_c = np.ptp(gh["c_corridor"]) if gh_points > 0 else np.nan
        gh_theta_center = np.mean(gh["theta_corridor"]) if gh_points > 0 else np.nan
        gh_c_center = np.mean(gh["c_corridor"]) if gh_points > 0 else np.nan
    else:
        theta_std = np.nan
        c_std = np.nan
        loops_mean = np.nan
        regime_sep = np.nan
        c_struct = np.nan
        gh_points = np.nan
        gh_width_theta = np.nan
        gh_width_c = np.nan
        gh_theta_center = np.nan
        gh_c_center = np.nan

    results.append({
        "load": load,
        "converged": converged,
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,
        "regime_separation": regime_sep,
        "c_struct": c_struct,
        "gh_points": gh_points,
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "gh_theta_center": gh_theta_center,
        "gh_c_center": gh_c_center,
    })

df = pd.DataFrame(results)

# ------------------------------------------------------------
# THRESHOLDS + STATES
# ------------------------------------------------------------

valid = df[df["converged"] == True].copy()

if len(valid) == 0:
    raise ValueError("No converged states found.")

max_c = valid["c_struct"].max()

warning_threshold = 0.60 * max_c
critical_threshold = 0.85 * max_c

def classify_state(row):
    if not row["converged"]:
        return "COLLAPSED"
    if row["c_struct"] >= critical_threshold:
        return "CRITICAL"
    if row["c_struct"] >= warning_threshold:
        return "WARNING"
    return "SAFE"

df["state"] = df.apply(classify_state, axis=1)

collapse_rows = df[df["state"] == "COLLAPSED"]
collapse_load = collapse_rows.iloc[0]["load"] if len(collapse_rows) > 0 else np.nan

critical_rows = df[(df["state"] == "CRITICAL") & (df["converged"] == True)]
first_critical_load = critical_rows.iloc[0]["load"] if len(critical_rows) > 0 else np.nan

warning_rows = df[(df["state"] == "WARNING") & (df["converged"] == True)]
first_warning_load = warning_rows.iloc[0]["load"] if len(warning_rows) > 0 else np.nan

lead_time_critical = collapse_load - first_critical_load if np.isfinite(collapse_load) and np.isfinite(first_critical_load) else np.nan
lead_time_warning = collapse_load - first_warning_load if np.isfinite(collapse_load) and np.isfinite(first_warning_load) else np.nan

# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

csv_path = os.path.join(OUTPUT_DIR, "ieee_prediction_test_v19.csv")
df.to_csv(csv_path, index=False)

print("\n--- RESULTS ---")
print(df)
print(f"\nSaved: {csv_path}")

print("\n--- V19 SUMMARY ---")
print(f"Max c_struct          : {max_c:.6f}")
print(f"WARNING threshold     : {warning_threshold:.6f}")
print(f"CRITICAL threshold    : {critical_threshold:.6f}")
print(f"First WARNING load    : {first_warning_load}")
print(f"First CRITICAL load   : {first_critical_load}")
print(f"Collapse load         : {collapse_load}")
print(f"WARNING lead time     : {lead_time_warning}")
print(f"CRITICAL lead time    : {lead_time_critical}")

# ------------------------------------------------------------
# PLOTS
# ------------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(13, 10))

# 1) c_struct vs load
ax = axes[0, 0]
ax.plot(df["load"], df["c_struct"], linewidth=2, label="c_struct")

ax.axhline(warning_threshold, linestyle="--", label="WARNING threshold")
ax.axhline(critical_threshold, linestyle="--", label="CRITICAL threshold")

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

    ax.scatter(row["load"], row["c_struct"], color=color)

ax.set_title("c_struct vs Load")
ax.set_xlabel("Load")
ax.set_ylabel("c_struct")
ax.grid()
ax.legend()

# 2) GH points vs load
ax = axes[0, 1]
ax.plot(df["load"], df["gh_points"], linewidth=2, label="GH points")
if np.isfinite(collapse_load):
    ax.axvline(collapse_load, linestyle="--", color="red", label="collapse")
ax.set_title("GH Points vs Load")
ax.set_xlabel("Load")
ax.set_ylabel("GH points")
ax.grid()
ax.legend()

# 3) GH width theta vs load
ax = axes[1, 0]
ax.plot(df["load"], df["gh_width_theta"], linewidth=2, label="GH width theta")
if np.isfinite(collapse_load):
    ax.axvline(collapse_load, linestyle="--", color="red", label="collapse")
ax.set_title("GH Width θ vs Load")
ax.set_xlabel("Load")
ax.set_ylabel("Width θ")
ax.grid()
ax.legend()

# 4) GH width c vs load
ax = axes[1, 1]
ax.plot(df["load"], df["gh_width_c"], linewidth=2, label="GH width c")
if np.isfinite(collapse_load):
    ax.axvline(collapse_load, linestyle="--", color="red", label="collapse")
ax.set_title("GH Width C vs Load")
ax.set_xlabel("Load")
ax.set_ylabel("Width C")
ax.grid()
ax.legend()

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# OPTIONAL PHASE BAR
# ------------------------------------------------------------

plt.figure(figsize=(12, 1.8))

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
    plt.scatter(
        row["load"],
        state_to_y[row["state"]],
        color=state_to_color[row["state"]],
        s=80,
    )

plt.yticks(
    [1, 2, 3, 4],
    ["SAFE", "WARNING", "CRITICAL", "COLLAPSED"]
)
plt.xlabel("Load")
plt.title("Phase Progression")
plt.grid(axis="x")
plt.tight_layout()
plt.show()
