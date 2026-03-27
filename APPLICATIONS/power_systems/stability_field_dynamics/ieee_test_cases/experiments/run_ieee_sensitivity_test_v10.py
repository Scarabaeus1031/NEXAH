import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    compute_metrics,
    detect_gh_corridor
)

print("RUNNING IEEE SENSITIVITY TEST V10 (Q° LAYER ACTIVE)")

# ----------------------------
# CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)
results = []

EPS = 1e-3  # threshold for Q° (null zone)

# ----------------------------
# HELPER: Dynamic Phase System WITH Q°
# ----------------------------

def classify_phases_v10(c, loops):
    dc = np.gradient(c)
    dl = np.gradient(loops)

    phase = []

    for i in range(len(c)):

        # ⚪ Q° (Null-Membran)
        if abs(dc[i]) < EPS and abs(dl[i]) < EPS:
            phase.append("Q0")

        # 🔵 CCC (Expansion)
        elif dc[i] > 0 and dl[i] > 0:
            phase.append("CCC")

        # 🟢 KKK (Collapse)
        elif dc[i] < 0 and dl[i] < 0:
            phase.append("KKK")

        # 🟠 GH (Transition Flow)
        else:
            phase.append("GH")

    return np.array(phase)

# ----------------------------
# MAIN LOOP
# ----------------------------

for load in loads:

    theta, c, loops = generate_phase_data(N=200)

    # --- NONLINEAR LOAD COUPLING ---
    theta = theta * (1 + 0.10 * (load - 1))

    c = c * (1 + 0.20 * (load - 1))
    c = c + 0.05 * load * np.sin(2 * theta)

    loops = loops * (1 + 0.15 * (load - 1))
    loops = loops + 0.10 * np.cos(load * theta)

    # ----------------------------
    # METRICS
    # ----------------------------

    metrics = compute_metrics(theta, c, loops)
    gh = detect_gh_corridor(theta, c, loops)

    gh_points = len(gh["theta_corridor"])
    gh_width_theta = np.ptp(gh["theta_corridor"]) if gh_points > 0 else 0
    gh_width_c = np.ptp(gh["c_corridor"]) if gh_points > 0 else 0

    # ----------------------------
    # PHASE SYSTEM (V10)
    # ----------------------------

    phases = classify_phases_v10(c, loops)

    total = len(phases)

    ccc_ratio = np.sum(phases == "CCC") / total
    gh_ratio  = np.sum(phases == "GH")  / total
    kkk_ratio = np.sum(phases == "KKK") / total
    q0_ratio  = np.sum(phases == "Q0")  / total

    # ----------------------------
    # STRUCTURAL METRICS
    # ----------------------------

    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)

    anisotropy = gh_width_theta / (gh_width_c + 1e-9)
    regime_separation = theta_std * c_std

    phase_tension = abs(ccc_ratio - kkk_ratio)
    phase_balance = gh_ratio * (1 - phase_tension)

    # NEW: Null stability
    null_stability = q0_ratio * (1 - phase_tension)

    results.append({
        "load": load,

        "pipeline_C": metrics["C"],

        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,

        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "anisotropy": anisotropy,

        "ccc_ratio": ccc_ratio,
        "gh_ratio": gh_ratio,
        "kkk_ratio": kkk_ratio,
        "q0_ratio": q0_ratio,

        "phase_tension": phase_tension,
        "phase_balance": phase_balance,
        "null_stability": null_stability
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test_v10.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(14, 10))

# Phase composition
plt.subplot(2, 2, 1)
plt.stackplot(
    df["load"],
    df["ccc_ratio"],
    df["gh_ratio"],
    df["kkk_ratio"],
    df["q0_ratio"],
    labels=["CCC", "GH", "KKK", "Q°"]
)
plt.title("Phase Composition (with Q°)")
plt.legend()

# Corridor
plt.subplot(2, 2, 2)
plt.plot(df["load"], df["gh_width_theta"], label="θ width")
plt.plot(df["load"], df["gh_width_c"], label="C width")
plt.title("GH Corridor")
plt.legend()

# Phase dynamics
plt.subplot(2, 2, 3)
plt.plot(df["load"], df["phase_balance"], label="Balance")
plt.plot(df["load"], df["phase_tension"], label="Tension")
plt.plot(df["load"], df["null_stability"], label="Q° stability")
plt.title("Phase Dynamics")
plt.legend()

# Anisotropy
plt.subplot(2, 2, 4)
plt.plot(df["load"], df["anisotropy"])
plt.title("Corridor Anisotropy")

plt.tight_layout()
plt.show()
