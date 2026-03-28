# run_ieee_killer_plot_v38.py

import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah
)

CASE = "ieee14"  # change to ieee9 / ieee30 if needed


def run():

    loads = np.linspace(0.6, 5.0, 100)

    c_struct = []
    min_V = []
    converged = []

    for load in loads:
        theta, C, loops, conv = ieee_to_nexah(CASE, load)

        converged.append(conv)

        if not conv:
            c_struct.append(np.nan)
            min_V.append(np.nan)
            continue

        c = np.std(C) * np.mean(loops)
        c_struct.append(c)

        V = 1.0 - C
        min_V.append(np.min(V))

    c_struct = np.array(c_struct)
    min_V = np.array(min_V)

    valid = np.array(converged)

    loads_v = loads[valid]
    c_v = c_struct[valid]
    V_v = min_V[valid]

    # derivatives
    dc = np.gradient(c_v, loads_v)
    d2c = np.gradient(dc, loads_v)

    dV = np.gradient(V_v, loads_v)

    # normalize (for visual comparison only)
    d2c_norm = (d2c - np.min(d2c)) / (np.max(d2c) - np.min(d2c))
    dV_norm = (dV - np.min(dV)) / (np.max(dV) - np.min(dV))

    # collapse
    collapse_idx = np.where(~valid)[0]
    collapse_load = loads[collapse_idx[0]] if len(collapse_idx) > 0 else None

    # peaks
    peak_d2c = loads_v[np.argmax(d2c)]
    peak_dV = loads_v[np.argmin(dV)]

    # plot
    plt.figure(figsize=(10, 6))

    plt.plot(loads_v, d2c_norm, label="NEXAH (curvature d²c/dλ²)", linewidth=2)
    plt.plot(loads_v, dV_norm, label="Classical (dV/dλ)", linewidth=2)

    plt.axvline(collapse_load, linestyle="--", label="Collapse", color="black")

    plt.scatter(peak_d2c, 1.0, color="red", label="NEXAH peak")
    plt.scatter(peak_dV, 1.0, color="orange", label="Classical peak")

    plt.xlabel("Load")
    plt.ylabel("Normalized Signal")
    plt.title(f"{CASE.upper()} — Early Warning Comparison (V38)")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run()
