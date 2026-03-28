import time
import numpy as np
import pandas as pd

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.ieee_loader import load_ieee14
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.stability_landscape_v2 import run_2d_stability_scan_v2
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.phase_data_pipeline import (
    generate_phase_data,
    detect_gh_corridor,
    compute_metrics,
)


def get_min_voltage(base_load: float, steps: int = 24) -> float:
    net = load_ieee14()
    load_bus = int(net.load["bus"].values[2])

    _, _, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=base_load,
        steps=steps,
    )

    return float(np.min(landscape))


def evaluate_load(base_load: float, n_points: int = 200) -> dict:
    theta, c, loops = generate_phase_data(N=n_points, seed=42)
    gh = detect_gh_corridor(theta, c, loops)
    metrics = compute_metrics(theta, c, loops)

    gh_theta = gh["theta_corridor"]
    gh_c = gh["c_corridor"]

    if len(gh_theta) > 0:
        gh_width_theta = float(np.max(gh_theta) - np.min(gh_theta))
        gh_width_c = float(np.max(gh_c) - np.min(gh_c))
        theta_center = float(np.mean(gh_theta))
        theta_std = float(np.std(gh_theta))
    else:
        gh_width_theta = 0.0
        gh_width_c = 0.0
        theta_center = np.nan
        theta_std = np.nan

    min_voltage = get_min_voltage(base_load=base_load)

    return {
        "load": float(base_load),
        "min_voltage": min_voltage,
        "C": float(metrics["C"]),
        "P": float(metrics["P"]),
        "R": float(metrics["R"]),
        "L": float(metrics["L"]),
        "gh_points": int(len(gh_theta)),
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "theta_center": theta_center,
        "theta_std": theta_std,
    }


def main():
    print("\n--- IEEE Physical Relevance Scan ---\n")

    loads = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
    rows = []

    for load in loads:
        t0 = time.time()
        row = evaluate_load(load)
        dt = time.time() - t0
        row["runtime_s"] = dt
        rows.append(row)

        print(
            f"load={row['load']:.2f} | "
            f"Vmin={row['min_voltage']:.4f} | "
            f"C={row['C']:.5f} | "
            f"GHpts={row['gh_points']} | "
            f"Wθ={row['gh_width_theta']:.3f} | "
            f"Wc={row['gh_width_c']:.5f} | "
            f"θc={row['theta_center']:.3f}"
        )

    df = pd.DataFrame(rows)
    df.to_csv("v36_ieee_physical_relevance.csv", index=False)

    print("\nSaved: v36_ieee_physical_relevance.csv")

    print("\n--- QUICK CHECKS ---")
    print(df[["load", "min_voltage", "C", "gh_points", "gh_width_theta", "gh_width_c", "theta_center"]])


if __name__ == "__main__":
    main()
