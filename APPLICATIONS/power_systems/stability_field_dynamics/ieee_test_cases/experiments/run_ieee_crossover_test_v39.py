# run_ieee_crossover_test_v39.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah
)

CASES = ["ieee9", "ieee14", "ieee30"]


def normalize(x):
    x = np.asarray(x, dtype=float)
    valid = np.isfinite(x)
    out = np.full_like(x, np.nan, dtype=float)

    if np.sum(valid) == 0:
        return out

    xmin = np.min(x[valid])
    xmax = np.max(x[valid])

    if np.isclose(xmax - xmin, 0.0):
        out[valid] = 0.0
    else:
        out[valid] = (x[valid] - xmin) / (xmax - xmin)

    return out


def compute_case(case: str):
    loads = np.linspace(0.6, 5.0, 120)

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
    df_valid["dV"] = np.gradient(df_valid["min_V"].values, df_valid["load"].values)

    # For comparison, flip classical so larger = stronger warning
    classical_signal = -df_valid["dV"].values
    nexah_signal = df_valid["d2c"].values

    df_valid["classical_norm"] = normalize(classical_signal)
    df_valid["nexah_norm"] = normalize(nexah_signal)
    df_valid["delta"] = df_valid["nexah_norm"] - df_valid["classical_norm"]

    # Peaks
    peak_d2c_idx = df_valid["nexah_norm"].idxmax()
    peak_classical_idx = df_valid["classical_norm"].idxmax()

    peak_d2c_load = df_valid.loc[peak_d2c_idx, "load"]
    peak_classical_load = df_valid.loc[peak_classical_idx, "load"]

    # First crossover: NEXAH catches/exceeds classical
    crossover_load = np.nan
    crossover_idx = np.nan

    delta_vals = df_valid["delta"].values
    load_vals = df_valid["load"].values

    for i in range(1, len(df_valid)):
        if np.isfinite(delta_vals[i - 1]) and np.isfinite(delta_vals[i]):
            if delta_vals[i - 1] < 0 and delta_vals[i] >= 0:
                crossover_idx = df_valid.index[i]
                crossover_load = load_vals[i]
                break

    # Optional: first "strong crossover" above tolerance
    strong_tol = 0.05
    strong_crossover_load = np.nan
    for i in range(len(df_valid)):
        if np.isfinite(delta_vals[i]) and delta_vals[i] >= strong_tol:
            strong_crossover_load = load_vals[i]
            break

    result = {
        "case": case,
        "collapse_load": collapse_load,
        "crossover_load": crossover_load,
        "strong_crossover_load": strong_crossover_load,
        "peak_d2c_load": peak_d2c_load,
        "peak_classical_load": peak_classical_load,
        "lead_crossover": collapse_load - crossover_load if np.isfinite(collapse_load) and np.isfinite(crossover_load) else np.nan,
        "lead_strong_crossover": collapse_load - strong_crossover_load if np.isfinite(collapse_load) and np.isfinite(strong_crossover_load) else np.nan,
        "lead_d2c": collapse_load - peak_d2c_load if np.isfinite(collapse_load) else np.nan,
        "lead_classical": collapse_load - peak_classical_load if np.isfinite(collapse_load) else np.nan,
    }

    return df_valid, result


def plot_case(df_valid: pd.DataFrame, result: dict):
    case = result["case"]
    collapse_load = result["collapse_load"]
    crossover_load = result["crossover_load"]
    strong_crossover_load = result["strong_crossover_load"]
    peak_d2c_load = result["peak_d2c_load"]
    peak_classical_load = result["peak_classical_load"]

    plt.figure(figsize=(10, 7))

    plt.plot(
        df_valid["load"],
        df_valid["nexah_norm"],
        label="NEXAH (curvature d²c/dλ²)",
        linewidth=2
    )
    plt.plot(
        df_valid["load"],
        df_valid["classical_norm"],
        label="Classical (-dV/dλ)",
        linewidth=2
    )

    if np.isfinite(collapse_load):
        plt.axvline(collapse_load, linestyle="--", color="black", label="Collapse")

    if np.isfinite(crossover_load):
        y_cross = float(df_valid.loc[df_valid["load"] == crossover_load, "nexah_norm"].iloc[0])
        plt.scatter(crossover_load, y_cross, color="purple", s=50, zorder=5, label="Crossover")

    if np.isfinite(strong_crossover_load):
        y_strong = float(df_valid.loc[df_valid["load"] == strong_crossover_load, "nexah_norm"].iloc[0])
        plt.scatter(strong_crossover_load, y_strong, color="green", s=50, zorder=5, label="Strong crossover")

    y_nexah_peak = float(df_valid.loc[df_valid["load"] == peak_d2c_load, "nexah_norm"].iloc[0])
    y_class_peak = float(df_valid.loc[df_valid["load"] == peak_classical_load, "classical_norm"].iloc[0])

    plt.scatter(peak_d2c_load, y_nexah_peak, color="red", s=50, zorder=5, label="NEXAH peak")
    plt.scatter(peak_classical_load, y_class_peak, color="orange", s=50, zorder=5, label="Classical peak")

    plt.xlabel("Load")
    plt.ylabel("Normalized Signal")
    plt.title(f"{case.upper()} — Crossover Detection (V39)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    summary = []

    for case in CASES:
        print(f"Running {case}...")
        df_valid, result = compute_case(case)
        summary.append(result)
        plot_case(df_valid, result)

    summary_df = pd.DataFrame(summary)

    print("\n--- V39 SUMMARY ---")
    print(summary_df)

    summary_df.to_csv(
        "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee_v39_crossover_summary.csv",
        index=False
    )


if __name__ == "__main__":
    main()
