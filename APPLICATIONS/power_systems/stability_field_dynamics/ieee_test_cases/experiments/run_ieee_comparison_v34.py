# run_ieee_comparison_v34.py

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


print("RUNNING IEEE COMPARISON V34 (DIVERGENCE DETECTION ENGINE)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

SYSTEMS = ["ieee9", "ieee14", "ieee30"]
LOADS = np.linspace(0.6, 5.0, 200)

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

    if np.sum(mask) >= 3:
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


def first_crossing_load(df, col, threshold):
    valid = df[np.isfinite(df[col])].copy()
    valid = valid[valid[col] >= threshold]
    if len(valid) == 0:
        return np.nan
    return valid.iloc[0]["load"]


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

    # use positive classical stress slope
    df["classical_slope"] = df["dvdev_dload"]

    # --------------------------------------------------------
    # NORMALIZED COMPARISON SIGNALS
    # --------------------------------------------------------

    df["classical_norm"] = minmax_norm(df["classical_slope"].values)
    df["nexah_norm"] = minmax_norm(df["d2c_struct_dload2"].values)
    df["fragmentation_norm"] = minmax_norm(df["fragmentation"].values)

    # pure divergence between NEXAH curvature and classical slope
    df["divergence"] = df["nexah_norm"] - df["classical_norm"]

    # augmented divergence includes fragmentation
    df["augmented_nexah"] = 0.7 * df["nexah_norm"] + 0.3 * df["fragmentation_norm"]
    df["augmented_divergence"] = df["augmented_nexah"] - df["classical_norm"]

    # --------------------------------------------------------
    # COLLAPSE + DIVERGENCE DETECTION
    # --------------------------------------------------------

    collapsed = df[df["converged"] == False]
    collapse_load = collapsed.iloc[0]["load"] if len(collapsed) > 0 else np.nan

    pre = df[df["load"] < collapse_load].copy() if np.isfinite(collapse_load) else df.copy()

    max_div = np.nanmax(pre["divergence"].values) if len(pre) else np.nan
    max_aug_div = np.nanmax(pre["augmented_divergence"].values) if len(pre) else np.nan

    div_threshold = 0.5 * max_div if np.isfinite(max_div) else np.nan
    aug_div_threshold = 0.5 * max_aug_div if np.isfinite(max_aug_div) else np.nan

    first_div_load = first_crossing_load(pre, "divergence", div_threshold) if np.isfinite(div_threshold) else np.nan
    first_aug_div_load = first_crossing_load(pre, "augmented_divergence", aug_div_threshold) if np.isfinite(aug_div_threshold) else np.nan

    lead_div = collapse_load - first_div_load if np.isfinite(collapse_load) and np.isfinite(first_div_load) else np.nan
    lead_aug_div = collapse_load - first_aug_div_load if np.isfinite(collapse_load) and np.isfinite(first_aug_div_load) else np.nan

    summary_rows.append({
        "case": case,
        "collapse_load": collapse_load,
        "max_divergence": max_div,
        "div_threshold": div_threshold,
        "first_divergence_load": first_div_load,
        "lead_divergence": lead_div,
        "max_aug_divergence": max_aug_div,
        "aug_div_threshold": aug_div_threshold,
        "first_aug_divergence_load": first_aug_div_load,
        "lead_aug_divergence": lead_aug_div,
    })

    # --------------------------------------------------------
    # SAVE PER CASE
    # --------------------------------------------------------

    df.to_csv(
        os.path.join(OUTPUT_DIR, f"{case}_comparison_v34.csv"),
        index=False
    )

    # --------------------------------------------------------
    # PLOTS
    # --------------------------------------------------------

    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    # Classical vs NEXAH normalized
    ax = axes[0]
    ax.plot(df["load"], df["classical_norm"], label="classical_norm (dvdev/dload)")
    ax.plot(df["load"], df["nexah_norm"], label="nexah_norm (d²c/dload²)")
    ax.plot(df["load"], df["fragmentation_norm"], label="fragmentation_norm")
    if np.isfinite(collapse_load):
        ax.axvline(collapse_load, linestyle="--", label="collapse")
    ax.set_title(f"{case.upper()} — Normalized Signal Comparison")
    ax.set_ylabel("Normalized")
    ax.grid()
    ax.legend()

    # Pure divergence
    ax = axes[1]
    ax.plot(df["load"], df["divergence"], label="divergence = NEXAH - Classical")
    if np.isfinite(div_threshold):
        ax.axhline(div_threshold, linestyle="--", label="divergence threshold")
    if np.isfinite(first_div_load):
        ax.axvline(first_div_load, linestyle=":", label="first divergence")
    if np.isfinite(collapse_load):
        ax.axvline(collapse_load, linestyle="--", label="collapse")
    ax.set_title(f"{case.upper()} — Divergence Detection")
    ax.set_ylabel("Divergence")
    ax.grid()
    ax.legend()

    # Augmented divergence
    ax = axes[2]
    ax.plot(df["load"], df["augmented_divergence"], label="augmented divergence")
    if np.isfinite(aug_div_threshold):
        ax.axhline(aug_div_threshold, linestyle="--", label="aug threshold")
    if np.isfinite(first_aug_div_load):
        ax.axvline(first_aug_div_load, linestyle=":", label="first aug divergence")
    if np.isfinite(collapse_load):
        ax.axvline(collapse_load, linestyle="--", label="collapse")
    ax.set_title(f"{case.upper()} — Augmented Divergence")
    ax.set_xlabel("Load")
    ax.set_ylabel("Aug. divergence")
    ax.grid()
    ax.legend()

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

summary_df = pd.DataFrame(summary_rows)

print("\n--- V34 SUMMARY ---")
print(summary_df)

summary_path = os.path.join(OUTPUT_DIR, "ieee_comparison_v34_summary.csv")
summary_df.to_csv(summary_path, index=False)

print(f"\nSaved: {summary_path}")
