# run_ieee_comparison_v33.py

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


print("RUNNING IEEE COMPARISON V33 (NEXAH vs CLASSICAL INDICATORS)")


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
    else:
        raise ValueError(case)


def get_classical_metrics(case, load):
    """
    Classical baseline metrics:
    - min_voltage
    - mean_voltage
    - voltage_deviation_mean
    - dq_dv_proxy ~ 1 / std(V)
    - converged
    """
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

        min_v = np.min(v)
        mean_v = np.mean(v)
        v_dev_mean = np.mean(np.abs(1.0 - v))

        v_std = np.std(v)
        dq_dv_proxy = 1.0 / (v_std + 1e-9)

        return {
            "min_voltage": min_v,
            "mean_voltage": mean_v,
            "v_dev_mean": v_dev_mean,
            "dq_dv_proxy": dq_dv_proxy,
            "converged": True,
        }

    except Exception:
        return {
            "min_voltage": np.nan,
            "mean_voltage": np.nan,
            "v_dev_mean": np.nan,
            "dq_dv_proxy": np.nan,
            "converged": False,
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


def peak_before_collapse(df, col):
    valid = df[np.isfinite(df[col])].copy()
    if len(valid) == 0:
        return np.nan

    idx = valid[col].idxmax()
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

    df["dc_struct_dload"] = safe_gradient(df["load"].values, df["c_struct"].values)
    df["d2c_struct_dload2"] = safe_gradient(df["load"].values, df["dc_struct_dload"].values)

    df["dminV_dload"] = safe_gradient(df["load"].values, df["min_voltage"].values)
    df["dvdev_dload"] = safe_gradient(df["load"].values, df["v_dev_mean"].values)

    # classical stress indicator:
    # lower min(V) -> higher stress
    df["voltage_stress"] = 1.0 - df["min_voltage"]

    # --------------------------------------------------------
    # COLLAPSE + PEAKS
    # --------------------------------------------------------

    collapsed = df[df["converged"] == False]
    collapse_load = collapsed.iloc[0]["load"] if len(collapsed) > 0 else np.nan

    peak_nexah_c = peak_before_collapse(df[df["load"] < collapse_load], "c_struct") if np.isfinite(collapse_load) else peak_before_collapse(df, "c_struct")
    peak_nexah_d2 = peak_before_collapse(df[df["load"] < collapse_load], "d2c_struct_dload2") if np.isfinite(collapse_load) else peak_before_collapse(df, "d2c_struct_dload2")
    peak_classical_stress = peak_before_collapse(df[df["load"] < collapse_load], "voltage_stress") if np.isfinite(collapse_load) else peak_before_collapse(df, "voltage_stress")
    peak_classical_dvdev = peak_before_collapse(df[df["load"] < collapse_load], "dvdev_dload") if np.isfinite(collapse_load) else peak_before_collapse(df, "dvdev_dload")

    summary_rows.append({
        "case": case,
        "collapse_load": collapse_load,
        "peak_c_struct": peak_nexah_c,
        "lead_c_struct": collapse_load - peak_nexah_c if np.isfinite(collapse_load) and np.isfinite(peak_nexah_c) else np.nan,
        "peak_d2c_struct": peak_nexah_d2,
        "lead_d2c_struct": collapse_load - peak_nexah_d2 if np.isfinite(collapse_load) and np.isfinite(peak_nexah_d2) else np.nan,
        "peak_voltage_stress": peak_classical_stress,
        "lead_voltage_stress": collapse_load - peak_classical_stress if np.isfinite(collapse_load) and np.isfinite(peak_classical_stress) else np.nan,
        "peak_dvdev": peak_classical_dvdev,
        "lead_dvdev": collapse_load - peak_classical_dvdev if np.isfinite(collapse_load) and np.isfinite(peak_classical_dvdev) else np.nan,
    })

    # save per-case
    df.to_csv(
        os.path.join(OUTPUT_DIR, f"{case}_comparison_v33.csv"),
        index=False
    )

    # --------------------------------------------------------
    # PLOTS
    # --------------------------------------------------------

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Upper: physical / classical
    ax = axes[0]
    ax.plot(df["load"], df["min_voltage"], label="min(V)")
    ax.plot(df["load"], df["voltage_stress"], label="1 - min(V)")
    ax.plot(df["load"], df["v_dev_mean"], label="mean|1-V|")
    if np.isfinite(collapse_load):
        ax.axvline(collapse_load, linestyle="--", label="collapse")
    ax.set_title(f"{case.upper()} — Classical Indicators")
    ax.set_ylabel("Value")
    ax.grid()
    ax.legend()

    # Lower: NEXAH
    ax = axes[1]
    ax.plot(df["load"], df["c_struct"], label="c_struct")
    ax.plot(df["load"], df["d2c_struct_dload2"], label="d²c_struct/dload²")
    ax.plot(df["load"], df["fragmentation"], label="fragmentation")
    if np.isfinite(collapse_load):
        ax.axvline(collapse_load, linestyle="--", label="collapse")
    ax.set_title(f"{case.upper()} — NEXAH Indicators")
    ax.set_xlabel("Load")
    ax.set_ylabel("Value")
    ax.grid()
    ax.legend()

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

summary_df = pd.DataFrame(summary_rows)

print("\n--- V33 SUMMARY ---")
print(summary_df)

summary_path = os.path.join(OUTPUT_DIR, "ieee_comparison_v33_summary.csv")
summary_df.to_csv(summary_path, index=False)

print(f"\nSaved: {summary_path}")
