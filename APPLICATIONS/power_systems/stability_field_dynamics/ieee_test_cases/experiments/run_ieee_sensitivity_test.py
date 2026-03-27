import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- IMPORT YOUR PIPELINE ---
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    compute_metrics,
    detect_gh_corridor
)

# ----------------------------
# TEST CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)

results = []

# ----------------------------
# MAIN LOOP
# ----------------------------

for load in loads:

    # 👉 SIMULATED LOAD EFFECT (placeholder!)
    theta, c, loops = generate_phase_data(N=200)

    # ⚠️ IMPORTANT:
    # This is where REAL coupling should go later
    # Currently: FAKE scaling (for sensitivity test)

    c = c * load
    loops = loops * (1 + 0.2 * (load - 1))

    # --- METRICS ---
    metrics = compute_metrics(theta, c, loops)
    gh = detect_gh_corridor(theta, c, loops)

    gh_width_theta = np.ptp(gh["theta_corridor"]) if len(gh["theta_corridor"]) > 0 else 0
    gh_width_c = np.ptp(gh["c_corridor"]) if len(gh["c_corridor"]) > 0 else 0

    results.append({
        "load": load,
        "C": metrics["C"],
        "P": metrics["P"],
        "R": metrics["R"],
        "L": metrics["L"],
        "gh_points": len(gh["theta_corridor"]),
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(10, 6))

plt.subplot(2, 2, 1)
plt.plot(df["load"], df["C"], marker="o")
plt.title("Coupling vs Load")

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
