import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

loads = np.linspace(1.0, 6.0, 25)
noise_levels = np.linspace(0.0, 0.2, 15)

results = []

print("\n--- V26 Phase Transition Map ---\n")


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for load in loads:
    for noise in noise_levels:

        print(f"Load={load:.2f} | Noise={noise:.3f}")

        try:
            metrics = run_single_coupling(
                base_load=load,
                noise_strength=noise
            )
        except Exception as e:
            print("Coupling failed:", e)
            metrics = {
                "C": np.nan,
                "states": np.nan,
                "loops": np.nan,
                "gap": np.nan,
            }

        results.append({
            "load": load,
            "noise": noise,
            "C": metrics.get("C", np.nan),
            "states": metrics.get("states", np.nan),
            "loops": metrics.get("loops", np.nan),
            "gap": metrics.get("gap", np.nan),
        })


# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(results)
df.to_csv("v26_phase_transition_map.csv", index=False)

print("\nSaved results to v26_phase_transition_map.csv")


# --------------------------------------------------
# PIVOT MAPS
# --------------------------------------------------

pivot_states = df.pivot(index="load", columns="noise", values="states")
pivot_loops = df.pivot(index="load", columns="noise", values="loops")

# Δ Maps
delta_states = pivot_states.diff().abs()
delta_loops = pivot_loops.diff().abs()


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

plt.figure(figsize=(16, 12))

plt.subplot(2, 2, 1)
plt.imshow(pivot_states, aspect='auto', origin='lower')
plt.title("States Map")
plt.colorbar()

plt.subplot(2, 2, 2)
plt.imshow(pivot_loops, aspect='auto', origin='lower')
plt.title("Loops Map")
plt.colorbar()

plt.subplot(2, 2, 3)
plt.imshow(delta_states, aspect='auto', origin='lower')
plt.title("Δ States")
plt.colorbar()

plt.subplot(2, 2, 4)
plt.imshow(delta_loops, aspect='auto', origin='lower')
plt.title("Δ Loops")
plt.colorbar()

plt.tight_layout()
plt.savefig("v26_phase_transition_maps.png", dpi=200)
plt.show()

print("\nSaved plots to v26_phase_transition_maps.png")


# --------------------------------------------------
# CRITICAL POINTS
# --------------------------------------------------

print("\n--- Critical Points ---")

for i in range(len(pivot_states.index)):
    for j in range(len(pivot_states.columns)):

        ds = delta_states.iloc[i, j]
        dl = delta_loops.iloc[i, j]

        if (ds > 0) or (dl > 0):
            print(
                f"Load={pivot_states.index[i]:.2f}, "
                f"Noise={pivot_states.columns[j]:.3f}, "
                f"ΔStates={ds}, ΔLoops={dl}"
            )
