# run_ieee_comparison_v35.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)

try:
    import pandapower as pp
    import pandapower.networks as pn
except ImportError:
    raise ImportError("pandapower required: pip install pandapower")


print("RUNNING IEEE COMPARISON V35 (ROBUST DIVERGENCE VALIDATION)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

SYSTEMS = ["ieee9", "ieee14", "ieee30"]
LOADS = np.linspace(0.6, 5.0, 200)

SMOOTH_WINDOW = 9
Z_THRESHOLD = 1.5
MIN_VALID_POINTS = 7

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def build_case(case):
    if case == "ieee9":
        return pn.case9()
    elif case == "ieee14":
        return pn.case14()
    elif case == "ieee30":
        return pn.case30()
    else:
        raise ValueError(case)


def get_classical_metrics(case, load):
    net = build_case(case)

    net.load["p_mw"] *= load
    net.load["q_mvar"] *= load

    try:
        pp.runpp(
            net,
            algorithm="nr",
            max_iteration=30,
            tolerance_mva=1e-6,
            init="auto"
        )

        v = net.res_bus["vm_pu"].values

        return {
            "converged": True,
            "min_voltage": np.min(v),
            "mean_voltage": np.mean(v),
            "v_dev_mean": np.mean(np.abs(1.0 - v)),
        }

    except Exception:
        return {
            "converged": False,
            "min_voltage": np.nan,
            "mean_voltage": np.nan,
            "v_dev_mean": np.nan,
        }


def compute_nexah_metrics(theta, c, loops):
    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)
    loops_std = np.std(loops)

    c_struct = theta_std * c_std * loops_mean
    fragmentation = theta_std * loops_std

    return {
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,
        "loops_std": loops_std,
        "c_struct": c_struct,
        "fragmentation": fragmentation,
    }


def safe_gradient(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    out = np.full_like(y, np.nan, dtype=float)
    mask = np.isfinite(y)

    if np.sum(mask) >= MIN_VALID_POINTS:
        out[mask] = np.gradient(y[mask], x[mask])

    return out


def minmax_norm(values):
    arr = np.asarray(values, dtype=float)
    out = np.full_like(arr, np.nan, dtype=float)

    mask = np.isfinite(arr)
    if np.sum(mask) == 0:
        return out

    vmin = np.min(arr[mask])
    vmax = np.max(arr[mask])

    if np.isclose(vmin, vmax):
        out[mask] = 0.0
    else:
        out[mask] = (arr[mask] - vmin) / (vmax - vmin)

    return out


def rolling_mean_nan(values, window=9):
    arr = np.asarray(values, dtype=float)
    out = np.full_like(arr, np.nan, dtype=float)

    if window < 1:
        return arr.copy()

    half = window // 2

    for i in range(len(arr)):
        left = max(0, i - half)
        right = min(len(arr), i + half + 1)
        chunk = arr[left:right]
        valid = chunk[np.isfinite(chunk)]
        if len(valid) > 0:
            out[i] = np.mean(valid)

    return out


def robust_stats(values):
    arr = np.asarray(values, dtype=float)
    valid = arr[np.isfinite(arr)]

    if len(valid) == 0:
        return np.nan, np.nan

    median = np.median(valid)
    mad = np.median(np.abs(valid - median))

    # convert MAD -> std-like scale
    robust_sigma = 1.4826 * mad

    return median, robust_sigma


def first_crossing_load(df, col, threshold, start_fraction=0.15):
    valid = df[np.isfinite(df[col])].copy()
    if len(valid) == 0 or not np.isfinite(threshold):
        return np.nan

    start_idx = int(len(valid) * start_fraction)
    valid = valid.iloc[start_idx:]

    crossed = valid[valid[col] >= threshold]
    if len(crossed) == 0:
        return np.nan

    return crossed.iloc[0]["load"]


def peak_before_collapse(df, col, collapse_load):
    if np.isfinite(collapse_load):
        work = df[df["load"] < collapse_load].copy()
    else:
        work = df.copy()

    work = work[np.isfinite(work[col])]
    if len(work) == 0:
        return np.nan

    idx = work[col].idxmax()
    return df.loc[idx, "load"]


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

summary_rows = []

for case in SYSTEMS:

    rows = []

    for load in LOADS:
        classical = get_classical_metrics(case, load)
        theta, c, loops, conv_nexah = ieee_to_nexah(case, load)

        if classical["converged"] and conv_nexah:
            nexah = compute_nexah_metrics(theta, c, loops)
        else:
            nexah = {
                "theta_std": np.nan,
                "c_std": np.nan,
                "loops_mean": np.nan,
                "loops_std": np.nan,
                "c_struct": np.nan,
                "fragmentation": np.nan,
            }

        rows.append({
            "case": case,
            "load": load,
            **classical,
            **nexah,
        })

    df = pd.DataFrame(rows)

    # --------------------------------------------------------
    # DERIVATIVES
    # --------------------------------------------------------

    df["dminV_dload"] = safe_gradient(df["load"].values, df["min_voltage"].values)
    df["dvdev_dload"] = safe_gradient(df["load"].values, df["v_dev_mean"].values)

    df["dc_struct_dload"] = safe_gradient(df["load"].values, df["c_struct"].values)
    df["d2c_struct_dload2"] = safe_gradient(df["load"].values, df["dc_struct_dload"].values)

    # Classical proxy
    df["classical_slope"] = df["dvdev_dload"]

    # --------------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------------

    df["classical_norm"] = minmax_norm(df["classical_slope"].values)
    df["nexah_norm"] = minmax_norm(df["d2c_struct_dload2"].values)
    df["fragmentation_norm"] = minmax_norm(df["fragmentation"].values)

    # Raw divergence
    df["divergence_raw"] = df["nexah_norm"] - df["classical_norm"]
    df["aug_divergence_raw"] = (
        0.7 * df["nexah_norm"] +
        0.3 * df["fragmentation_norm"] -
        df["classical_norm"]
    )

    # Smoothed divergence
    df["divergence_smooth"] = rolling_mean_nan(df["divergence_raw"].values, SMOOTH_WINDOW)
    df["aug_divergence_smooth"] = rolling_mean_nan(df["aug_divergence_raw"].values, SMOOTH_WINDOW)

    # --------------------------------------------------------
    # ROBUST THRESHOLDS
    # --------------------------------------------------------

    collapsed = df[df["converged"] == False]
    collapse_load = collapsed.iloc[0]["load"] if len(collapsed) > 0 else np.nan

    if np.isfinite(collapse_load):
        pre = df[df["load"] < collapse_load].copy()
    else:
        pre = df.copy()

    med_div, sig_div = robust_stats(pre["divergence_smooth"].values)
    med_aug, sig_aug = robust_stats(pre["aug_divergence_smooth"].values)

    div_threshold = med_div + Z_THRESHOLD * sig_div if np.isfinite(med_div) and np.isfinite(sig_div) else np.nan
    aug_threshold = med_aug + Z_THRESHOLD * sig_aug if np.isfinite(med_aug) and np.isfinite(sig_aug) else np.nan

    first_div_load = first_crossing_load(pre, "divergence_smooth", div_threshold)
    first_aug_div_load = first_crossing_load(pre, "aug_divergence_smooth", aug_threshold)

    lead_div = collapse_load - first_div_load if np.isfinite(collapse_load) and np.isfinite(first_div_load) else np.nan
    lead_aug = collapse_load - first_aug_div_load if np.isfinite(collapse_load) and np.isfinite(first_aug_div_load) else np.nan

    peak_div_load = peak_before_collapse(df, "divergence_smooth", collapse_load)
    peak_aug_load = peak_before_collapse(df, "aug_divergence_smooth", collapse_load)
    peak_d2c_load = peak_before_collapse(df, "d2c_struct_dload2", collapse_load)
    peak_classical_load = peak_before_collapse(df, "classical_slope", collapse_load)

    summary_rows.append({
        "case": case,
        "collapse_load": collapse_load,
        "div_threshold": div_threshold,
        "first_divergence_load": first_div_load,
        "lead_divergence": lead_div,
        "aug_threshold": aug_threshold,
        "first_aug_divergence_load": first_aug_div_load,
        "lead_aug_divergence": lead_aug,
        "peak_divergence_load": peak_div_load,
        "peak_aug_divergence_load": peak_aug_load,
        "peak_d2c_load": peak_d2c_load,
        "peak_classical_load": peak_classical_load,
        "lead_peak_d2c": collapse_load - peak_d2c_load if np.isfinite(collapse_load) and np.isfinite(peak_d2c_load) else np.nan,
        "lead_peak_classical": collapse_load - peak_classical_load if np.isfinite(collapse_load) and np.isfinite(peak_classical_load) else np.nan,
    })

    # --------------------------------------------------------
    # SAVE PER CASE
    # --------------------------------------------------------

    df.to_csv(
        os.path.join(OUTPUT_DIR, f"{case}_comparison_v35.csv"),
        index=False
    )

    # --------------------------------------------------------
    # PLOTS
    # --------------------------------------------------------

    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    # Signals
    ax = axes[0]
    ax.plot(df["load"], df["classical_norm"], label="classical_norm")
    ax.plot(df["load"], df["nexah_norm"], label="nexah_norm")
    ax.plot(df["load"], df["fragmentation_norm"], label="fragmentation_norm")
    if np.isfinite(collapse_load):
        ax.axvline(collapse_load, linestyle="--", label="collapse")
    ax.set_title(f"{case.upper()} — Normalized Signal Comparison")
    ax.set_ylabel("Normalized")
    ax.grid()
    ax.legend()

    # Robust divergence
    ax = axes[1]
    ax.plot(df["load"], df["divergence_raw"], alpha=0.35, label="divergence_raw")
    ax.plot(df["load"], df["divergence_smooth"], linewidth=2, label="divergence_smooth")
    if np.isfinite(div_threshold):
        ax.axhline(div_threshold, linestyle="--", label="robust threshold")
    if np.isfinite(first_div_load):
        ax.axvline(first_div_load, linestyle=":", label="first divergence")
    if np.isfinite(collapse_load):
        ax.axvline(collapse_load, linestyle="--", label="collapse")
    ax.set_title(f"{case.upper()} — Robust Divergence Detection")
    ax.set_ylabel("Divergence")
    ax.grid()
    ax.legend()

    # Augmented divergence
    ax = axes[2]
    ax.plot(df["load"], df["aug_divergence_raw"], alpha=0.35, label="aug_raw")
    ax.plot(df["load"], df["aug_divergence_smooth"], linewidth=2, label="aug_smooth")
    if np.isfinite(aug_threshold):
        ax.axhline(aug_threshold, linestyle="--", label="aug threshold")
    if np.isfinite(first_aug_div_load):
        ax.axvline(first_aug_div_load, linestyle=":", label="first aug divergence")
    if np.isfinite(collapse_load):
        ax.axvline(collapse_load, linestyle="--", label="collapse")
    ax.set_title(f"{case.upper()} — Robust Augmented Divergence")
    ax.set_xlabel("Load")
    ax.set_ylabel("Aug. divergence")
    ax.grid()
    ax.legend()

    plt.tight_layout()
    plt.show()


# --------------------------------------------------------
# SUMMARY
# --------------------------------------------------------

summary_df = pd.DataFrame(summary_rows)

print("\n--- V35 SUMMARY ---")
print(summary_df)

summary_path = os.path.join(OUTPUT_DIR, "ieee_comparison_v35_summary.csv")
summary_df.to_csv(summary_path, index=False)

print(f"\nSaved: {summary_path}")
