# run_ieee_prediction_test_v21.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)

print("RUNNING IEEE PREDICTION TEST V21 (UNIFIED COLLAPSE PREDICTOR)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

LOADS = np.linspace(0.6, 5.0, 60)
CASES = ["ieee14", "ieee9"]

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


def minmax_norm(series):
    arr = np.asarray(series, dtype=float)
    out = np.full_like(arr, np.nan, dtype=float)

    mask = np.isfinite(arr)
    if np.sum(mask) == 0:
        return out

    vmin = np.min(arr[mask])
    vmax = np.max(arr[mask])

    if np.isclose(vmax, vmin):
        out[mask] = 0.0
    else:
        out[mask] = (arr[mask] - vmin) / (vmax - vmin)

    return out


def classify_score(row, warning_thr, critical_thr):
    if not row["converged"]:
        return "COLLAPSED"
    if np.isfinite(row["score"]) and row["score"] >= critical_thr:
        return "CRITICAL"
    if np.isfinite(row["score"]) and row["score"] >= warning_thr:
        return "WARNING"
    return "SAFE"


# ------------------------------------------------------------
# CASE RUNNER
# ------------------------------------------------------------

def run_case(case_name):
    rows = []

    for load in LOADS:
        theta, c, loops, converged = ieee_to_nexah(case_name, load_scale=load)

        if converged:
            theta_std, c_std, loops_mean, regime_sep, c_struct = compute_c_struct(theta, c, loops)
        else:
            theta_std = np.nan
            c_std = np.nan
            loops_mean = np.nan
            regime_sep = np.nan
            c_struct = np.nan

        rows.append({
            "case": case_name,
            "load": load,
            "converged": converged,
            "theta_std": theta_std,
            "c_std": c_std,
            "loops_mean": loops_mean,
            "regime_separation": regime_sep,
            "c_struct": c_struct,
        })

    df = pd.DataFrame(rows)

    # Derivatives
    df["dc_dload"] = safe_gradient(df["c_struct"].values, df["load"].values)
    df["d2c_dload2"] = safe_gradient(df["dc_dload"].values, df["load"].values)

    # Normalized components
    df["c_struct_norm"] = minmax_norm(df["c_struct"].values)
    df["dc_dload_norm"] = minmax_norm(df["dc_dload"].values)
    df["d2c_dload2_norm"] = minmax_norm(df["d2c_dload2"].values)

    # Unified score
    w1, w2, w3 = 0.30, 0.20, 0.50
    df["score"] = (
        w1 * df["c_struct_norm"] +
        w2 * df["dc_dload_norm"] +
        w3 * df["d2c_dload2_norm"]
    )

    valid = df[df["converged"] == True].copy()
    if len(valid) == 0:
        raise ValueError(f"No converged states found for {case_name}")

    score_warning_thr = 0.60 * valid["score"].max()
    score_critical_thr = 0.85 * valid["score"].max()

    df["state"] = df.apply(
        lambda row: classify_score(row, score_warning_thr, score_critical_thr),
        axis=1
    )

    collapsed = df[df["converged"] == False]
    collapse_load = collapsed.iloc[0]["load"] if len(collapsed) > 0 else np.nan

    warning_rows = df[(df["state"] == "WARNING") & (df["converged"] == True)]
    critical_rows = df[(df["state"] == "CRITICAL") & (df["converged"] == True)]

    first_warning_load = warning_rows.iloc[0]["load"] if len(warning_rows) > 0 else np.nan
    first_critical_load = critical_rows.iloc[0]["load"] if len(critical_rows) > 0 else np.nan

    warning_lead = collapse_load - first_warning_load if np.isfinite(collapse_load) and np.isfinite(first_warning_load) else np.nan
    critical_lead = collapse_load - first_critical_load if np.isfinite(collapse_load) and np.isfinite(first_critical_load) else np.nan

    summary = {
        "case": case_name,
        "collapse_load": collapse_load,
        "max_c_struct": valid["c_struct"].max(),
        "max_dc_dload": valid["dc_dload"].max(),
        "max_d2c_dload2": valid["d2c_dload2"].max(),
        "max_score": valid["score"].max(),
        "warning_threshold": score_warning_thr,
        "critical_threshold": score_critical_thr,
        "first_warning_load": first_warning_load,
        "first_critical_load": first_critical_load,
        "warning_lead": warning_lead,
        "critical_lead": critical_lead,
    }

    return df, summary


# ------------------------------------------------------------
# RUN ALL CASES
# ------------------------------------------------------------

all_frames = []
summaries = []

for case_name in CASES:
    df_case, summary_case = run_case(case_name)
    all_frames.append(df_case)
    summaries.append(summary_case)

df_all = pd.concat(all_frames, ignore_index=True)
df_summary = pd.DataFrame(summaries)

# Save
csv_main = os.path.join(OUTPUT_DIR, "ieee_prediction_test_v21.csv")
csv_summary = os.path.join(OUTPUT_DIR, "ieee_prediction_test_v21_summary.csv")

df_all.to_csv(csv_main, index=False)
df_summary.to_csv(csv_summary, index=False)

print("\n--- SUMMARY TABLE ---")
print(df_summary)
print(f"\nSaved: {csv_main}")
print(f"Saved: {csv_summary}")


# ------------------------------------------------------------
# PLOTS
# ------------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for i, case_name in enumerate(CASES):
    df = df_all[df_all["case"] == case_name].copy()
    summary = df_summary[df_summary["case"] == case_name].iloc[0]

    row_idx = i

    # Unified score
    ax = axes[row_idx, 0]
    ax.plot(df["load"], df["score"], linewidth=2, label=f"{case_name} score")
    ax.axhline(summary["warning_threshold"], linestyle="--", label="WARNING threshold")
    ax.axhline(summary["critical_threshold"], linestyle="--", label="CRITICAL threshold")

    if np.isfinite(summary["collapse_load"]):
        ax.axvline(summary["collapse_load"], linestyle="--", color="red", label="collapse")

    for _, r in df.iterrows():
        if r["state"] == "SAFE":
            color = "green"
        elif r["state"] == "WARNING":
            color = "orange"
        elif r["state"] == "CRITICAL":
            color = "red"
        else:
            color = "black"

        ax.scatter(r["load"], r["score"], color=color, s=28)

    ax.set_title(f"{case_name} — Unified Score")
    ax.set_xlabel("Load")
    ax.set_ylabel("Score")
    ax.grid()
    ax.legend()

    # Components
    ax = axes[row_idx, 1]
    ax.plot(df["load"], df["c_struct_norm"], label="c_struct_norm")
    ax.plot(df["load"], df["dc_dload_norm"], label="dc_dload_norm")
    ax.plot(df["load"], df["d2c_dload2_norm"], label="d2c_dload2_norm")
    if np.isfinite(summary["collapse_load"]):
        ax.axvline(summary["collapse_load"], linestyle="--", color="red", label="collapse")

    ax.set_title(f"{case_name} — Normalized Components")
    ax.set_xlabel("Load")
    ax.set_ylabel("Normalized value")
    ax.grid()
    ax.legend()

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# OPTIONAL PHASE PLOTS
# ------------------------------------------------------------

fig, axes = plt.subplots(len(CASES), 1, figsize=(12, 4 * len(CASES)))
if len(CASES) == 1:
    axes = [axes]

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

for ax, case_name in zip(axes, CASES):
    df = df_all[df_all["case"] == case_name].copy()
    summary = df_summary[df_summary["case"] == case_name].iloc[0]

    for _, r in df.iterrows():
        ax.scatter(
            r["load"],
            state_to_y[r["state"]],
            color=state_to_color[r["state"]],
            s=50,
        )

    if np.isfinite(summary["collapse_load"]):
        ax.axvline(summary["collapse_load"], linestyle="--", color="red", label="collapse")

    ax.set_title(f"{case_name} — Phase Progression")
    ax.set_xlabel("Load")
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(["SAFE", "WARNING", "CRITICAL", "COLLAPSED"])
    ax.grid(axis="x")
    ax.legend()

plt.tight_layout()
plt.show()
