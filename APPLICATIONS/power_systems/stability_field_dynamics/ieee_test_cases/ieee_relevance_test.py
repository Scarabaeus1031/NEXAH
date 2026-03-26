import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 🔧 IMPORT ANPASSEN!
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.ieee_adapter import run_powerflow


# --------------------------------------------------
# EXPERIMENT CONFIG
# --------------------------------------------------

loads = np.linspace(1.0, 6.0, 80)

USE_NOISE = True
NOISE_STD = 0.01

results = []

print("\n--- IEEE vs NEXAH Relevance Test ---\n")

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for load in loads:

    if USE_NOISE:
        noise = np.random.normal(0, NOISE_STD)
        load_eff = load * (1 + noise)
    else:
        load_eff = load

    # --- CLASSICAL ---
    try:
        converged, min_v = run_powerflow(load_eff)
    except Exception as e:
        print("Powerflow failed:", e)
        converged, min_v = False, np.nan

    # --- NEXAH ---
    try:
        metrics = run_single_coupling(base_load=load_eff)
    except Exception as e:
        print("Coupling failed:", e)
        metrics = {
            "C": np.nan,
            "P": np.nan,
            "R": np.nan,
            "L": np.nan,
            "gap": np.nan,
            "states": np.nan,
            "loops": np.nan,
        }

    results.append({
        "load": load,
        "load_eff": load_eff,
        "converged": converged,
        "min_v": min_v,
        "C": metrics["C"],
        "P": metrics["P"],
        "R": metrics["R"],
        "L": metrics["L"],
        "gap": metrics["gap"],
        "states": metrics["states"],
        "loops": metrics["loops"],
    })

# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_relevance_results.csv", index=False)

print("\nSaved results to ieee_relevance_results.csv")

# --------------------------------------------------
# ANALYSIS ADD-ON (WICHTIG!)
# --------------------------------------------------

print("\n--- BASIC STATISTICS ---")
print(df.describe())

print("\n--- VARIANCE CHECK ---")
print("C variance:", df["C"].var())
print("Loops variance:", df["loops"].var())
print("States variance:", df["states"].var())
print("Gap variance:", df["gap"].var())

# 👉 DAS ist dein Wahrheits-Test:
if df["C"].var() < 1e-8:
    print("\n⚠️ WARNING: Coupling metric is invariant → no sensitivity!")

# --------------------------------------------------
# PLOTS
# --------------------------------------------------

plt.figure(figsize=(14, 10))

# --- Voltage Collapse ---
plt.subplot(3, 1, 1)
plt.plot(df["load"], df["min_v"], label="Min Voltage")
plt.axhline(0.7, linestyle="--", label="Collapse Threshold")
plt.title("Voltage Collapse Curve")
plt.xlabel("Load")
plt.ylabel("Voltage")
plt.legend()

# --- Coupling ---
plt.subplot(3, 1, 2)
plt.plot(df["load"], df["C"], label="Coupling C")

# optional normalization
if df["C"].max() > 0:
    plt.plot(df["load"], df["C"] / df["C"].max(), "--", label="C (normalized)")

plt.title("NEXAH Coupling Metric")
plt.xlabel("Load")
plt.ylabel("C")
plt.legend()

# --- Structure ---
plt.subplot(3, 1, 3)
plt.plot(df["load"], df["loops"], label="Loops")
plt.plot(df["load"], df["states"], label="States")
plt.plot(df["load"], df["gap"], label="Gap")
plt.title("Structure Indicators")
plt.xlabel("Load")
plt.ylabel("Value")
plt.legend()

plt.tight_layout()
plt.savefig("ieee_relevance_plots.png", dpi=200)
plt.show()

print("\nSaved plots to ieee_relevance_plots.png")
