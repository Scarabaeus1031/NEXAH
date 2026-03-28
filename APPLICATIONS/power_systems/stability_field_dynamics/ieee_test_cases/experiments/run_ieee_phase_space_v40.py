# run_ieee_phase_space_v40.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah
)

CASES = ["ieee9", "ieee14", "ieee30"]


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

        # structural intensity
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

    # derivatives
    df_valid["dc"] = np.gradient(df_valid["c_struct"].values, df_valid["load"].values)
    df_valid["d2c"] = np.gradient(df_valid["dc"].values, df_valid["load"].values)

    return df_valid, collapse_load


def plot_phase_space(df_valid: pd.DataFrame, collapse_load: float, case: str):
    x = df_valid["c_struct"].values
    y = df_valid["dc"].values
    z = df_valid["d2c"].values
    load = df_valid["load"].values

    # normalize load for coloring
    load_norm = (load - np.min(load)) / (np.max(load) - np.min(load))

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter(
        x, y, z,
        c=load_norm,
        cmap='viridis',
        s=20
    )

    # trajectory line
    ax.plot(x, y, z, alpha=0.4)

    # mark collapse approach (last valid point)
    ax.scatter(
        x[-1], y[-1], z[-1],
        color="red",
        s=60,
        label="Pre-collapse state"
    )

    ax.set_xlabel("c_struct (intensity)")
    ax.set_ylabel("dc/dλ (drift)")
    ax.set_zlabel("d²c/dλ² (acceleration)")

    ax.set_title(f"{case.upper()} — Phase Space (V40)")

    cbar = plt.colorbar(sc, ax=ax, shrink=0.7)
    cbar.set_label("Load progression")

    ax.legend()
    plt.tight_layout()
    plt.show()


def main():
    print("RUNNING IEEE PHASE SPACE ANALYSIS (V40)")

    for case in CASES:
        print(f"\n--- {case.upper()} ---")
        df_valid, collapse_load = compute_case(case)

        print(f"Collapse load: {collapse_load:.4f}")

        plot_phase_space(df_valid, collapse_load, case)


if __name__ == "__main__":
    main()
