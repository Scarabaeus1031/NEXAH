import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- IMPORT YOUR PIPELINE ---
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    compute_metrics,
    detect_gh_corridor
)

print("RUNNING IEEE SENSITIVITY TEST V5 (STRUCTURE-COUPLED)")

# ----------------------------
# CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)

results = []

# coupling strength (tune this!)
ALPHA_THETA = 0.08
BETA_LOOPS = 2.0
GAMMA_C = 0.5

# ----------------------------
# MAIN LOOP
# ----------------------------

for load in loads:

    # --- BASE STRUCTURE ---
    theta, c, loops = generate_phase_data(N=200)

    # ----------------------------
    # 🔥 CORE IDEA: MODIFY STRUCTURE
    # ----------------------------

    # 1. Theta spread increases with load
    theta = theta * (1 + ALPHA_THETA * (load - 1))

    # 2. Measure spread
    theta_std = np.std(theta)

    # 3. Loops emerge from spread (NOT arbitrary scaling!)
    loops = loops + BETA_LOOPS * theta_std

    # 4. Coupling responds to structure change
    c = c * (1 + GAMMA_C * theta_std)

    # ----------------------------
    # METRICS
    # ----------------------------

    metrics = compute_metrics(theta, c, loops)
    gh = detect_gh_corridor(theta, c, loops)

    gh_width_theta = np.ptp(gh["theta_corridor"]) if len(gh["theta_corridor"]) > 0 else 0
    gh_width_c = np.ptp(gh["c_corridor"]) if len(gh["c_corridor"]) > 0 else 0

    results.append({
        "load": load,
        "pipeline_C": metrics["C"],
        "pipeline_P": metrics["P"],
        "pipeline_R": metrics["R"],
        "pipeline_L": metrics["L"],
        "gh_points": len(gh["theta_corridor"]),
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "theta_std": theta_std
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test_v5.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(df["load"], df["pipeline_C"], marker="o")
plt.title("Pipeline C vs Load")

plt.subplot(2, 2, 2)
plt.plot(df["load"], df["gh_points"], marker="o")
plt.title("GH Points vs Load")

plt.subplot(2, 2, 3)
plt.plot(df["load"], df["gh_width_theta"], marker="o")
plt.title("GH Width θ")

plt.subplot(2, 2, 4)
plt.plot(df["load"], df["gh_width_c"], marker="o")
plt.title("GH Width C")

plt.tight_layout()
plt.show()

# Extra plot (important!)
plt.figure(figsize=(6,4))
plt.plot(df["load"], df["theta_std"], marker="o")
plt.title("Theta Spread vs Load (KEY SIGNAL)")
plt.xlabel("load")
plt.ylabel("theta_std")
plt.show()
