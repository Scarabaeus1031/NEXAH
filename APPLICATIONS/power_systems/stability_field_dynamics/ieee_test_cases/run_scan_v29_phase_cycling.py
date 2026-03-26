import os
import sys
import time
import numpy as np
import pandas as pd

sys.path.append(
os.path.abspath(
os.path.join(os.path.dirname(**file**), "../../../..")
)
)

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling

def main():
print("\n--- V29 Phase Cycling ---\n")

```
loads = [1.0, 2.0]
timesteps = 12   # ein kompletter Zyklus

results = []

for load in loads:
    print(f"\n=== Load {load} ===")

    for t in range(timesteps):

        phase = 2 * np.pi * t / timesteps

        # ---------------------------------
        # 🔥 PHASE CYCLING (DAO LOGIC)
        # ---------------------------------
        noise = 0.1 + 0.2 * np.sin(phase)
        rotation = 0.5 + 0.3 * np.cos(phase)   # gegenphasig

        damping = max(0.90, 0.975 - 0.1 * abs(np.sin(phase)))

        print(
            f"t={t:02d} | "
            f"noise={noise:.3f} | "
            f"rot={rotation:.3f} | "
            f"damp={damping:.3f}"
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

        row = {
            "load": load,
            "t": t,
            "phase": phase,
            "noise": noise,
            "rotation": rotation,
            "damping": damping,
            "time": dt,
            "C": r.get("C", np.nan),
            "states": r.get("states", np.nan),
            "loops": r.get("loops", np.nan),
            "gap": r.get("gap", np.nan),
        }

        results.append(row)

        print(
            f"→ t={dt:.2f}s | "
            f"C={row['C']:.5f} | "
            f"states={row['states']} | "
            f"loops={row['loops']}"
        )

df = pd.DataFrame(results)
df.to_csv("v29_phase_cycling.csv", index=False)

print("\nSaved: v29_phase_cycling.csv")

print("\n--- SUMMARY ---")
print("States unique:", df["states"].nunique(dropna=True))
print("Loops unique:", df["loops"].nunique(dropna=True))
print("C variance:", df["C"].var())
print("Avg runtime:", df["time"].mean())
```

if **name** == "**main**":
main()
