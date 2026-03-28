import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah
)

CASES = ["ieee9", "ieee14", "ieee30"]

N_STEPS = 120
PERTURBATIONS = [-0.02, -0.01, 0.0, 0.01, 0.02]

def normalize(x):
    x = np.array(x)
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-9)

def run_trajectory(case, load_scale_shift=0.0):
    loads = np.linspace(0.6, 5.0, N_STEPS)

    c_vals = []
    dc_vals = []
    d2c_vals = []
    valid_loads = []

    for l in loads:
        l_mod = l * (1.0 + load_scale_shift)

        theta, C, loops, conv = ieee_to_nexah(case, l_mod)

        if not conv:
            break

        c = np.std(C) * np.mean(loops)
        c_vals.append(c)
        valid_loads.append(l_mod)

    if len(c_vals) < 5:
        return None

    c_vals = np.array(c_vals)
    loads = np.array(valid_loads)

    dc = np.gradient(c_vals, loads)
    d2c = np.gradient(dc, loads)

    return {
        "c": normalize(c_vals),
        "dc": normalize(dc),
        "d2c": normalize(d2c),
        "load": loads
    }


print("RUNNING V42 — COLLAPSE MANIFOLD STABILITY TEST")

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

results = []

for case in CASES:
    print(f"\n--- {case.upper()} ---")

    for p in PERTURBATIONS:
        traj = run_trajectory(case, p)

        if traj is None:
            continue

        c = traj["c"]
        dc = traj["dc"]
        d2c = traj["d2c"]

        ax.plot(c, dc, d2c, alpha=0.6)

        # Pre-collapse point
        c_end = c[-1]
        dc_end = dc[-1]
        d2c_end = d2c[-1]

        results.append({
            "case": case,
            "perturbation": p,
            "c_end": c_end,
            "dc_end": dc_end,
            "d2c_end": d2c_end
        })

        ax.scatter(c_end, dc_end, d2c_end, s=40)

ax.set_xlabel("c_struct (norm)")
ax.set_ylabel("dc/dλ (norm)")
ax.set_zlabel("d²c/dλ² (norm)")
ax.set_title("V42 — Collapse Manifold Stability")

plt.tight_layout()
plt.show()


df = pd.DataFrame(results)

print("\n--- V42 RESULT ---")
print(df)

# Streuung messen
spread = df.groupby("case")[["c_end", "dc_end", "d2c_end"]].std()

print("\n--- MANIFOLD STABILITY (STD) ---")
print(spread)
