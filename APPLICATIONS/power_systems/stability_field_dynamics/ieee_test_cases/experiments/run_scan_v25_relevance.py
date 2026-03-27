import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 🔥 NEU: v25 CORE
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling_v25 import run_single_coupling


# --------------------------------------------------
# SIMPLE BASELINE (klassisch)
# --------------------------------------------------

def run_powerflow(load):
    # einfache Collapse-Kurve
    if load < 4.5:
        return True, 1.0 - 0.1 * (load / 4.5)
    else:
        return False, 0.6


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

loads = np.linspace(1.0, 6.0, 25)   # etwas dichter als FAST-Test
NOISE = 0.05                        # 🔥 wichtig: jetzt aktiv!

results = []

print("\n--- V25 Relevance Test (Dynamic Perturbation) ---\n")

# --------------------------------------------------
# LOOP
# --------------------------------------------------

for i, load in enumerate(loads):

    print(f"{i+1}/{len(loads)} | Load={load:.2f}")

    # --- CLASSICAL ---
    converged, min_v = run_powerflow(load)

    # --- NEXAH v25 ---
    metrics = run_single_coupling(
        base_load=load,
        noise_strength=NOISE
    )

    results.append({
        "load": load,
        "min_v": min_v,
        "converged": converged,
        "C": metrics["C"],
        "gap": metrics["gap"],
        "loops": metrics["loops"],
        "states": metrics["states"]
    })


# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(results)
df.to_csv("v25_relevance_results.csv", index=False)

print("\nSaved results to v25_relevance_results.csv")

# --------------------------------------------------
# QUICK ANALYSIS
# --------------------------------------------------

print("\n--- VARIANCE CHECK ---")
print("C variance:", df["C"].var())
print("Loops variance:", df["loops"].var())
print("States variance:", df["states"].var())
print("Gap variance:", df["gap"].var())

# --------------------------------------------------
# PLOTS
# --------------------------------------------------

plt.figure(figsize=(14, 10))

# Voltage
plt.subplot(3, 1, 1)
plt.plot(df["load"], df["min_v"], label="Voltage")
plt.axhline(0.7, linestyle="--")
plt.title("Voltage Collapse")

# Coupling
plt.subplot(3, 1, 2)
plt.plot(df["load"], df["C"], label="C")
plt.title("Coupling (v25)")

# Structure
plt.subplot(3, 1, 3)
plt.plot(df["load"], df["loops"], label="Loops")
plt.plot(df["load"], df["states"], label="States")
plt.plot(df["load"], df["gap"], label="Gap")
plt.legend()
plt.title("Structure Response")

plt.tight_layout()
plt.savefig("v25_relevance_plots.png", dpi=200)
plt.show()

print("\nSaved plots to v25_relevance_plots.png")
