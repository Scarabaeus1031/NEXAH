# run_ieee_universal_collapse_test_v41.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah
)

CASES = ["ieee9", "ieee14", "ieee30"]
LOAD_MIN = 0.6
LOAD_MAX = 5.0
N_STEPS = 160
N_RESAMPLED = 80

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def normalize(arr):
    arr = np.asarray(arr, dtype=float)
    out = np.full_like(arr, np.nan, dtype=float)

    valid = np.isfinite(arr)
    if np.sum(valid) == 0:
        return out

    amin = np.min(arr[valid])
    amax = np.max(arr[valid])

    if np.isclose(amax - amin, 0.0):
        out[valid] = 0.0
    else:
        out[valid] = (arr[valid] - amin) / (amax - amin)

    return out


def interp_to_grid(x_old, y_old, x_new):
    x_old = np.asarray(x_old, dtype=float)
    y_old = np.asarray(y_old, dtype=float)

    valid = np.isfinite(x_old) & np.isfinite(y_old)
    x_old = x_old[valid]
    y_old = y_old[valid]

    if len(x_old) < 2:
        return np.full_like(x_new, np.nan, dtype=float)

    order = np.argsort(x_old)
    x_old = x_old[order]
    y_old = y_old[order]

    unique_x, unique_idx = np.unique(x_old, return_index=True)
    unique_y = y_old[unique_idx]

    if len(unique_x) < 2:
        return np.full_like(x_new, np.nan, dtype=float)

    return np.interp(x_new, unique_x, unique_y, left=np.nan, right=np.nan)


def compute_case(case: str):
    loads = np.linspace(LOAD_MIN, LOAD_MAX, N_STEPS)

    c_struct = []
    min_v = []
    converged = []

    for load in loads:
        theta, C, loops, conv = ieee_to_nexah(case, load)

        converged.append(conv)

        if not conv:
            c_struct.append(np.nan)
            min_v.append(np.nan)
            continue

        c_val = np.std(C) * np.mean(loops)
        c_struct.append(c_val)

        V = 1.0 - C
        min_v.append(np.min(V))

    df = pd.DataFrame({
        "load": loads,
        "c_struct": c_struct,
        "min_V": min_v,
        "converged": converged
    })

    collapse_candidates = df.loc[~df["converged"], "load"]
    collapse_load = collapse_candidates.iloc[0] if len(collapse_candidates) > 0 else np.nan

    df_valid = df[df["converged"]].copy()

    df_valid["dc"] = np.gradient(df_valid["c_struct"].values, df_valid["load"].values)
    df_valid["d2c"] = np.gradient(df_valid["dc"].values, df_valid["load"].values)

    # relative collapse coordinate:
    # tau = 0 at start, tau = 1 at collapse
    if np.isfinite(collapse_load):
        df_valid["tau"] = df_valid["load"].values / collapse_load
    else:
        df_valid["tau"] = np.nan

    # distance-to-collapse coordinate:
    # delta = 1 - tau
    df_valid["delta"] = 1.0 - df_valid["tau"].values

    # normalized coordinates in structural state space
    df_valid["c_norm"] = normalize(df_valid["c_struct"].values)
    df_valid["dc_norm"] = normalize(df_valid["dc"].values)
    df_valid["d2c_norm"] = normalize(df_valid["d2c"].values)

    return df_valid, collapse_load


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

print("RUNNING IEEE UNIVERSAL COLLAPSE TEST (V41)")

case_data = {}
summary_rows = []

for case in CASES:
    print(f"Running {case}...")
    df_valid, collapse_load = compute_case(case)
    case_data[case] = {
        "df": df_valid,
        "collapse_load": collapse_load
    }

    pre_idx = df_valid.index[-1]

    summary_rows.append({
        "case": case,
        "collapse_load": collapse_load,
        "precollapse_tau": df_valid.loc[pre_idx, "tau"],
        "precollapse_c_norm": df_valid.loc[pre_idx, "c_norm"],
        "precollapse_dc_norm": df_valid.loc[pre_idx, "dc_norm"],
        "precollapse_d2c_norm": df_valid.loc[pre_idx, "d2c_norm"],
    })


# ------------------------------------------------------------
# COMMON RESAMPLED GRID
# ------------------------------------------------------------

# compare only the shared tau range
tau_min_common = 0.0
tau_max_common = min([
    np.nanmax(case_data[c]["df"]["tau"].values)
    for c in CASES
])

tau_grid = np.linspace(tau_min_common, tau_max_common, N_RESAMPLED)

resampled = {}

for case in CASES:
    df_valid = case_data[case]["df"]

    tau = df_valid["tau"].values

    c_r = interp_to_grid(tau, df_valid["c_norm"].values, tau_grid)
    dc_r = interp_to_grid(tau, df_valid["dc_norm"].values, tau_grid)
    d2c_r = interp_to_grid(tau, df_valid["d2c_norm"].values, tau_grid)

    resampled[case] = {
        "tau": tau_grid,
        "c_norm": c_r,
        "dc_norm": dc_r,
        "d2c_norm": d2c_r,
    }


# ------------------------------------------------------------
# DISTANCE ANALYSIS
# ------------------------------------------------------------

distance_rows = []

pairs = [
    ("ieee9", "ieee14"),
    ("ieee9", "ieee30"),
    ("ieee14", "ieee30"),
]

for a, b in pairs:
    xa = resampled[a]["c_norm"]
    ya = resampled[a]["dc_norm"]
    za = resampled[a]["d2c_norm"]

    xb = resampled[b]["c_norm"]
    yb = resampled[b]["dc_norm"]
    zb = resampled[b]["d2c_norm"]

    valid = (
        np.isfinite(xa) & np.isfinite(ya) & np.isfinite(za) &
        np.isfinite(xb) & np.isfinite(yb) & np.isfinite(zb)
    )

    if np.sum(valid) == 0:
        mean_dist = np.nan
        max_dist = np.nan
    else:
        d = np.sqrt(
            (xa[valid] - xb[valid]) ** 2 +
            (ya[valid] - yb[valid]) ** 2 +
            (za[valid] - zb[valid]) ** 2
        )
        mean_dist = np.mean(d)
        max_dist = np.max(d)

    distance_rows.append({
        "pair": f"{a} vs {b}",
        "mean_distance": mean_dist,
        "max_distance": max_dist,
    })

distance_df = pd.DataFrame(distance_rows)
summary_df = pd.DataFrame(summary_rows)

summary_df.to_csv(
    os.path.join(OUTPUT_DIR, "ieee_v41_precollapse_summary.csv"),
    index=False
)
distance_df.to_csv(
    os.path.join(OUTPUT_DIR, "ieee_v41_trajectory_distances.csv"),
    index=False
)


# ------------------------------------------------------------
# PLOT 1 — COMBINED 3D PHASE SPACE
# ------------------------------------------------------------

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

for case in CASES:
    dfr = resampled[case]

    ax.plot(
        dfr["c_norm"],
        dfr["dc_norm"],
        dfr["d2c_norm"],
        linewidth=2,
        label=case.upper()
    )

    ax.scatter(
        dfr["c_norm"][-1],
        dfr["dc_norm"][-1],
        dfr["d2c_norm"][-1],
        s=50
    )

ax.set_xlabel("c_struct (norm)")
ax.set_ylabel("dc/dλ (norm)")
ax.set_zlabel("d²c/dλ² (norm)")
ax.set_title("Universal Collapse Phase Space (V41)")
ax.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# PLOT 2 — 2D PHASE: dc vs c
# ------------------------------------------------------------

plt.figure(figsize=(8, 6))
for case in CASES:
    dfr = resampled[case]
    plt.plot(dfr["c_norm"], dfr["dc_norm"], linewidth=2, label=case.upper())
    plt.scatter(dfr["c_norm"][-1], dfr["dc_norm"][-1], s=40)

plt.xlabel("c_struct (norm)")
plt.ylabel("dc/dλ (norm)")
plt.title("Phase Portrait: dc/dλ vs c_struct (V41)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# PLOT 3 — 2D PHASE: d2c vs dc
# ------------------------------------------------------------

plt.figure(figsize=(8, 6))
for case in CASES:
    dfr = resampled[case]
    plt.plot(dfr["dc_norm"], dfr["d2c_norm"], linewidth=2, label=case.upper())
    plt.scatter(dfr["dc_norm"][-1], dfr["d2c_norm"][-1], s=40)

plt.xlabel("dc/dλ (norm)")
plt.ylabel("d²c/dλ² (norm)")
plt.title("Phase Portrait: d²c/dλ² vs dc/dλ (V41)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# PLOT 4 — 2D PHASE: d2c vs c
# ------------------------------------------------------------

plt.figure(figsize=(8, 6))
for case in CASES:
    dfr = resampled[case]
    plt.plot(dfr["c_norm"], dfr["d2c_norm"], linewidth=2, label=case.upper())
    plt.scatter(dfr["c_norm"][-1], dfr["d2c_norm"][-1], s=40)

plt.xlabel("c_struct (norm)")
plt.ylabel("d²c/dλ² (norm)")
plt.title("Phase Portrait: d²c/dλ² vs c_struct (V41)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# PLOT 5 — COLLAPSE-TIME ALIGNMENT
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))
for case in CASES:
    dfr = resampled[case]
    plt.plot(dfr["tau"], dfr["c_norm"], label=f"{case.upper()} : c")
    plt.plot(dfr["tau"], dfr["dc_norm"], linestyle="--", label=f"{case.upper()} : dc")
    plt.plot(dfr["tau"], dfr["d2c_norm"], linestyle=":", label=f"{case.upper()} : d2c")

plt.xlabel("τ = load / collapse_load")
plt.ylabel("Normalized state")
plt.title("Collapse-Time Aligned Structural Signals (V41)")
plt.grid(True)
plt.legend(ncol=3, fontsize=8)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# TEXT OUTPUT
# ------------------------------------------------------------

print("\n--- V41 PREC_COLLAPSE SUMMARY ---")
print(summary_df)

print("\n--- V41 TRAJECTORY DISTANCES ---")
print(distance_df)

print(f"\nSaved: {os.path.join(OUTPUT_DIR, 'ieee_v41_precollapse_summary.csv')}")
print(f"Saved: {os.path.join(OUTPUT_DIR, 'ieee_v41_trajectory_distances.csv')}")
