import sys
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../..")
    )
)

from joblib import Parallel, delayed
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

np.random.seed(42)

base_loads = np.linspace(1.0, 3.0, 5)
base_noises = [0.0, 0.05, 0.10, 0.20]

trials_per_point = 4          # klein halten wegen Laufzeit
load_jitter_strength = 0.35   # echter Last-Schock
noise_jitter_strength = 0.08  # zusätzlicher Noise-Jitter

results = []

print("\n--- V27 Attractor Breaker ---\n")


# --------------------------------------------------
# SAFE RUNNER
# --------------------------------------------------

def run_trial(base_load, base_noise, trial_id):
    start = time.time()

    # harter Perturbationsraum
    load_shock = base_load * (1.0 + np.random.uniform(-load_jitter_strength, load_jitter_strength))
    noise_shock = max(0.0, base_noise + np.random.uniform(-noise_jitter_strength, noise_jitter_strength))

    try:
        metrics = run_single_coupling(
            base_load=load_shock,
            noise_strength=noise_shock
        )
    except Exception as e:
        print(
            f"ERROR | base_load={base_load:.2f}, base_noise={base_noise:.3f}, "
            f"trial={trial_id} -> {e}"
        )
        metrics = {
            "C": np.nan,
            "states": np.nan,
            "loops": np.nan,
            "gap": np.nan,
        }

    duration = time.time() - start

    out = {
        "base_load": base_load,
        "base_noise": base_noise,
        "trial": trial_id,
        "load_shock": load_shock,
        "noise_shock": noise_shock,
        "time": duration,
        "C": metrics.get("C", np.nan),
        "states": metrics.get("states", np.nan),
        "loops": metrics.get("loops", np.nan),
        "gap": metrics.get("gap", np.nan),
    }

    print(
        f"baseL={base_load:.2f}, baseN={base_noise:.3f}, trial={trial_id} | "
        f"L*={load_shock:.3f}, N*={noise_shock:.3f} | "
        f"t={duration:.2f}s | "
        f"states={out['states']}, loops={out['loops']}, C={out['C']}"
    )

    return out


# --------------------------------------------------
# MAIN
# --------------------------------------------------

jobs = []
for base_load in base_loads:
    for base_noise in base_noises:
        for trial_id in range(trials_per_point):
            jobs.append((base_load, base_noise, trial_id))

results = Parallel(n_jobs=-1)(
    delayed(run_trial)(base_load, base_noise, trial_id)
    for base_load, base_noise, trial_id in jobs
)

df = pd.DataFrame(results)
df.to_csv("v27_attractor_breaker_results.csv", index=False)

print("\nSaved: v27_attractor_breaker_results.csv")


# --------------------------------------------------
# AGGREGATION
# --------------------------------------------------

summary = (
    df.groupby(["base_load", "base_noise"])
    .agg(
        states_mean=("states", "mean"),
        states_std=("states", "std"),
        loops_mean=("loops", "mean"),
        loops_std=("loops", "std"),
        C_mean=("C", "mean"),
        C_std=("C", "std"),
        runtime_mean=("time", "mean"),
        unique_states=("states", lambda x: len(pd.unique(x.dropna()))),
        unique_loops=("loops", lambda x: len(pd.unique(x.dropna()))),
    )
    .reset_index()
)

summary.to_csv("v27_attractor_breaker_summary.csv", index=False)
print("Saved: v27_attractor_breaker_summary.csv")


# --------------------------------------------------
# DETECT POSSIBLE BREAKS
# --------------------------------------------------

print("\n--- POSSIBLE ATTRACTOR BREAKS ---")
found_break = False

for _, row in summary.iterrows():
    if (
        (row["unique_states"] > 1) or
        (row["unique_loops"] > 1) or
        (pd.notna(row["states_std"]) and row["states_std"] > 0) or
        (pd.notna(row["loops_std"]) and row["loops_std"] > 0)
    ):
        found_break = True
        print(
            f"base_load={row['base_load']:.2f}, base_noise={row['base_noise']:.3f} | "
            f"unique_states={row['unique_states']}, unique_loops={row['unique_loops']} | "
            f"states_std={row['states_std']}, loops_std={row['loops_std']}"
        )

if not found_break:
    print("No attractor break detected in this V27 scan.")


# --------------------------------------------------
# PIVOT FOR MAPS
# --------------------------------------------------

pivot_unique_states = summary.pivot(index="base_load", columns="base_noise", values="unique_states")
pivot_unique_loops = summary.pivot(index="base_load", columns="base_noise", values="unique_loops")
pivot_states_std = summary.pivot(index="base_load", columns="base_noise", values="states_std")
pivot_loops_std = summary.pivot(index="base_load", columns="base_noise", values="loops_std")


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.imshow(pivot_unique_states, aspect="auto", origin="lower")
plt.title("Unique States per Parameter Point")
plt.colorbar()

plt.subplot(2, 2, 2)
plt.imshow(pivot_unique_loops, aspect="auto", origin="lower")
plt.title("Unique Loops per Parameter Point")
plt.colorbar()

plt.subplot(2, 2, 3)
plt.imshow(np.nan_to_num(pivot_states_std.values), aspect="auto", origin="lower")
plt.title("States Std")
plt.colorbar()

plt.subplot(2, 2, 4)
plt.imshow(np.nan_to_num(pivot_loops_std.values), aspect="auto", origin="lower")
plt.title("Loops Std")
plt.colorbar()

plt.tight_layout()
plt.savefig("v27_attractor_breaker_maps.png", dpi=200)
plt.show()

print("\nSaved: v27_attractor_breaker_maps.png")


# --------------------------------------------------
# GLOBAL SUMMARY
# --------------------------------------------------

print("\n--- GLOBAL SUMMARY ---")
print("States variance:", df["states"].var())
print("Loops variance:", df["loops"].var())
print("C variance:", df["C"].var())
print("Avg runtime per run:", df["time"].mean())
print("Unique states total:", df["states"].nunique(dropna=True))
print("Unique loops total:", df["loops"].nunique(dropna=True))
