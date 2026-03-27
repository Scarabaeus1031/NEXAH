# --------------------------------------------------
# V26 Phase Transition Map (FAST DEBUG VERSION)
# --------------------------------------------------

import sys
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# FIXED PATH
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../..")
    )
)

from joblib import Parallel, delayed
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling


# --------------------------------------------------
# CONFIG (SUPER FAST TEST)
# --------------------------------------------------

loads = np.linspace(1.0, 3.0, 4)        # ↓ stark reduziert
noise_levels = np.linspace(0.0, 0.2, 3) # ↓ stark reduziert

print("\n--- V26 Phase Transition Map (FAST DEBUG) ---\n")


# --------------------------------------------------
# SINGLE RUN WRAPPER (TIMING)
# --------------------------------------------------

def run_point(load, noise):
    start = time.time()

    try:
        metrics = run_single_coupling(
            base_load=load,
            noise_strength=noise
        )
    except Exception as e:
        print(f"ERROR @ Load={load}, Noise={noise}:", e)
        metrics = {
            "C": np.nan,
            "states": np.nan,
            "loops": np.nan,
            "gap": np.nan,
        }

    duration = time.time() - start

    print(
        f"Load={load:.2f}, Noise={noise:.3f} | "
        f"Time={duration:.2f}s | "
        f"States={metrics.get('states')}, Loops={metrics.get('loops')}"
    )

    return {
        "load": load,
        "noise": noise,
        "time": duration,
        "C": metrics.get("C", np.nan),
        "states": metrics.get("states", np.nan),
        "loops": metrics.get("loops", np.nan),
        "gap": metrics.get("gap", np.nan),
    }


# --------------------------------------------------
# PARALLEL EXECUTION 🚀
# --------------------------------------------------

results = Parallel(n_jobs=-1)(
    delayed(run_point)(l, n)
    for l in loads for n in noise_levels
)


# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(results)
df.to_csv("v26_phase_transition_map_debug.csv", index=False)

print("\nSaved results to v26_phase_transition_map_debug.csv")


# --------------------------------------------------
# VARIANCE CHECK
# --------------------------------------------------

print("\n--- VARIANCE CHECK ---")
print("States variance:", df["states"].var())
print("Loops variance:", df["loops"].var())
print("C variance:", df["C"].var())
print("Avg runtime per run:", df["time"].mean())


# --------------------------------------------------
# PIVOT
# --------------------------------------------------

pivot_states = df.pivot(index="load", columns="noise", values="states")
pivot_loops = df.pivot(index="load", columns="noise", values="loops")


# --------------------------------------------------
# GRADIENT (BESSER ALS DIFF 🔥)
# --------------------------------------------------

grad_states = np.gradient(pivot_states.values)
grad_loops = np.gradient(pivot_loops.values)

mag_states = np.sqrt(grad_states[0]**2 + grad_states[1]**2)
mag_loops = np.sqrt(grad_loops[0]**2 + grad_loops[1]**2)


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.imshow(pivot_states, aspect='auto', origin='lower')
plt.title("States")
plt.colorbar()

plt.subplot(2, 2, 2)
plt.imshow(pivot_loops, aspect='auto', origin='lower')
plt.title("Loops")
plt.colorbar()

plt.subplot(2, 2, 3)
plt.imshow(mag_states, aspect='auto', origin='lower')
plt.title("∇ States (Phase Activity)")
plt.colorbar()

plt.subplot(2, 2, 4)
plt.imshow(mag_loops, aspect='auto', origin='lower')
plt.title("∇ Loops (Phase Activity)")
plt.colorbar()

plt.tight_layout()
plt.savefig("v26_phase_transition_maps_debug.png", dpi=200)
plt.show()

print("\nSaved plots to v26_phase_transition_maps_debug.png")
