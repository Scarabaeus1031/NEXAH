import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    compute_metrics,
    detect_gh_corridor
)

# ----------------------------
# CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)

results = []

# ----------------------------
# HELPER: Dynamic Phase Classification
# ----------------------------

def classify_dynamic_phases(c, loops):
    dc = np.gradient(c)
    dl = np.gradient(loops)

    phase = []

    for i in range(len(c)):
        if dc[i] > 0 and dl[i] > 0:
            phase.append("CCC")  # expansion
        elif dc[i] < 0 and dl[i] < 0:
            phase.append("KKK")  # collapse
        else:
            phase.append("GH")   # interface

    return np.array(phase)

# ----------------------------
# MAIN LOOP
# ----------------------------

for load in loads:

    # --- BASE PIPELINE ---
    theta, c, loops = generate_phase_data(N=200)

    # --- STRUCTURAL COUPLING ---
    theta_std = np.std(theta)
    loops_mean = np.mean(loops)

    c = c * (1 + 0.15 * theta_std)
    loops = loops * (1 + 0.1 * theta_std)

    # --- LOAD EFFECT ---
    c = c * (1 + 0.2 * (load - 1))
    loops = loops * (1 + 0.15 * (load - 1))

    # ----------------------------
    # METRICS
    # ----------------------------

    metrics = compute_metrics(theta, c, loops)
    gh = detect_gh_corridor(theta, c, loops)

    gh_width_theta = np.ptp(gh["theta_corridor"]) if len(gh["theta_corridor"]) > 0 else 0
    gh_width_c = np.ptp(gh["c_corridor"]) if len(gh["c_corridor"]) > 0 else 0

    # ----------------------------
    # 🔥 NEW: Dynamic Phase System
    # ----------------------------

    phases = classify_dynamic_phases(c, loops)

    ccc_ratio = np.sum(phases == "CCC") / len(phases)
    gh_ratio  = np.sum(phases == "GH") / len(phases)
    kkk_ratio = np.sum(phases == "KKK") / len(phases)

    # ----------------------------
    # STRUCTURAL METRICS
    # ----------------------------

    c_std = np.std(c)
    anisotropy = gh_width_theta / (gh_width_c + 1e-6)

    # phase tension = dominance of CCC over GH
    phase_tension = ccc_ratio - gh_ratio

    # phase balance = GH stability
    phase_balance = gh_ratio * (1 - abs(ccc_ratio - kkk_ratio))

    # ----------------------------
    # STORE
    # ----------------------------

    results.append({
        "load": load,

        # pipeline
        "pipeline_C": metrics["C"],
        "pipeline_P": metrics["P"],
        "pipeline_R": metrics["R"],
        "pipeline_L": metrics["L"],

        # structure
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,

        # corridor
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "anisotropy": anisotropy,

        # phases
        "ccc_ratio": ccc_ratio,
        "gh_ratio": gh_ratio,
        "kkk_ratio": kkk_ratio,

        # dynamics
        "phase_tension": phase_tension,
        "phase_balance": phase_balance
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test_v8.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(12, 8))

# Phase composition
plt.subplot(2, 2, 1)
plt.plot(df["load"], df["ccc_ratio"], label="CCC")
plt.plot(df["load"], df["gh_ratio"], label="GH")
plt.plot(df["load"], df["kkk_ratio"], label="KKK")
plt.title("Dynamic Phase Composition")
plt.legend()

# Corridor width
plt.subplot(2, 2, 2)
plt.plot(df["load"], df["gh_width_theta"], label="θ width")
plt.plot(df["load"], df["gh_width_c"], label="C width")
plt.title("GH Corridor Structure")
plt.legend()

# Phase tension / balance
plt.subplot(2, 2, 3)
plt.plot(df["load"], df["phase_tension"], label="Tension")
plt.plot(df["load"], df["phase_balance"], label="Balance")
plt.title("Phase Dynamics")
plt.legend()

# Anisotropy
plt.subplot(2, 2, 4)
plt.plot(df["load"], df["anisotropy"])
plt.title("Corridor Anisotropy")

plt.tight_layout()
plt.show()
