import os
import sys
import time
import numpy as np
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../..")
    )
)

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling


def main():
    print("\n--- V28 Core Breaker ---\n")

    loads = [1.0, 2.0, 3.0]
    noises = [0.0, 0.10, 0.25, 0.50]

    results = []

    total = len(loads) * len(noises)
    k = 0

    for load in loads:
        for noise in noises:
            k += 1
            print(f"{k}/{total} | Load={load:.2f} | Noise={noise:.2f}")

            start = time.time()

            try:
                r = run_single_coupling(
                    base_load=load,
                    noise_strength=noise,
                    steps=24,
                    n_particles=40,
                    advect_steps=80,
                    flow_rotation=0.5 + 0.4 * noise,
                    damping=max(0.90, 0.975 - 0.08 * noise),
                )
            except Exception as e:
                print("FAILED:", e)
                r = {
                    "C": np.nan,
                    "P": np.nan,
                    "R": np.nan,
                    "L": np.nan,
                    "loops": np.nan,
                    "states": np.nan,
                    "gap": np.nan,
                }

            dt = time.time() - start

            row = {
                "load": load,
                "noise": noise,
                "time": dt,
                "C": r.get("C", np.nan),
                "P": r.get("P", np.nan),
                "R": r.get("R", np.nan),
                "L": r.get("L", np.nan),
                "loops": r.get("loops", np.nan),
                "states": r.get("states", np.nan),
                "gap": r.get("gap", np.nan),
            }
            results.append(row)

            print(
                f"t={dt:.2f}s | "
                f"C={row['C']:.6f} | "
                f"states={row['states']} | "
                f"loops={row['loops']} | "
                f"gap={row['gap']}"
            )

    df = pd.DataFrame(results)
    df.to_csv("v28_core_breaker_results.csv", index=False)

    print("\nSaved: v28_core_breaker_results.csv")
    print("\n--- SUMMARY ---")
    print("States variance:", df["states"].var())
    print("Loops variance:", df["loops"].var())
    print("C variance:", df["C"].var())
    print("Avg runtime:", df["time"].mean())
    print("Unique states:", df["states"].nunique(dropna=True))
    print("Unique loops:", df["loops"].nunique(dropna=True))


if __name__ == "__main__":
    main()
