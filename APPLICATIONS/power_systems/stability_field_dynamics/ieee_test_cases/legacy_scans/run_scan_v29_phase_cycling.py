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
    print("\n--- V29 Phase Cycling ---\n")

    loads = [1.0, 2.0]
    timesteps = 12

    results = []

    for load in loads:
        print(f"\n=== Load {load} ===")

        for t in range(timesteps):

            phase = 2 * np.pi * t / timesteps

            noise = 0.1 + 0.2 * np.sin(phase)
            rotation = 0.5 + 0.3 * np.cos(phase)
            damping = max(0.90, 0.975 - 0.1 * abs(np.sin(phase)))

            print(
                f"t={t:02d} | noise={noise:.3f} | rot={rotation:.3f} | damp={damping:.3f}"
            )

            start = time.time()

            try:
                r = run_single_coupling(
                    base_load=load,
                    noise_strength=noise,
                    steps=24,
                    n_particles=40,
                    advect_steps=80,
                    flow_rotation=rotation,
                    damping=damping,
                )
            except Exception as e:
                print("FAILED:", e)
                r = {
                    "C": np.nan,
                    "states": np.nan,
                    "loops": np.nan,
                    "gap": np.nan,
                }

            dt = time.time() - start

            print(
                f"→ t={dt:.2f}s | C={r.get('C')} | states={r.get('states')} | loops={r.get('loops')}"
            )

            results.append({
                "load": load,
                "t": t,
                "noise": noise,
                "rotation": rotation,
                "damping": damping,
                "time": dt,
                "C": r.get("C"),
                "states": r.get("states"),
                "loops": r.get("loops"),
                "gap": r.get("gap"),
            })

    df = pd.DataFrame(results)
    df.to_csv("v29_phase_cycling.csv", index=False)

    print("\nSaved: v29_phase_cycling.csv")


if __name__ == "__main__":
    main()
