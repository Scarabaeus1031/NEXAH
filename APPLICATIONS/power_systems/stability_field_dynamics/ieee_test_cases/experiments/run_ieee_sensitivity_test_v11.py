import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    compute_metrics,
    detect_gh_corridor
)

print("RUNNING IEEE SENSITIVITY TEST V11 (Q° EMERGENCE DETECTION)")

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
            phase.append("CCC")
        elif dc[i] < 0 and dl[i] < 0:
            phase.append("KKK")
        else:
            phase.append("GH")

    return np.array(phase)

# ----------------------------
# MAIN LOOP
# ----------------------------

for load in loads:

    # --- BASE STRUCTURE ---
    theta, c, loops = generate_phase_data(N=200)

    # ----------------------------
    # NONLINEAR LOAD COUPLING
    # ----------------------------

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
    gh_width_theta = np.ptp(gh["theta_corridor"]) if gh_points > 0 else 0.0
    gh_width_c = np.ptp(gh["c_corridor"]) if gh_points > 0 else 0.0

    # ----------------------------
    # DYNAMIC PHASE SYSTEM
    # ----------------------------

    phases = classify_dynamic_phases(c, loops)

    total = len(phases)

    ccc_ratio = np.sum(phases == "CCC") / total
    gh_ratio  = np.sum(phases == "GH")  / total
    kkk_ratio = np.sum(phases == "KKK") / total

    # ----------------------------
    # Q° AS EMERGENT MEMBRANE
    # ----------------------------

    # Membrane intensity grows when:
    # - GH is present
    # - CCC and KKK are close enough to generate a boundary
    q0_membrane = gh_ratio * (1.0 - abs(ccc_ratio - kkk_ratio))

    # Optional sharper variant:
    q0_sharp = gh_ratio * np.minimum(ccc_ratio, kkk_ratio)

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

    C_struct = regime_separation * loops_mean
    C_struct_norm = (
        (theta_std / (1 + theta_std))
        * (c_std / (1 + c_std))
        * (loops_mean / (1 + loops_mean))
    )

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
        "regime_separation": regime_separation,
        "anisotropy": anisotropy,
        "C_struct": C_struct,
        "C_struct_norm": C_struct_norm,

        # corridor
        "gh_points": gh_points,
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,

        # phases
        "ccc_ratio": ccc_ratio,
        "gh_ratio": gh_ratio,
        "kkk_ratio": kkk_ratio,
        "phase_tension": phase_tension,
        "phase_balance": phase_balance,

        # Q°
        "q0_membrane": q0_membrane,
        "q0_sharp": q0_sharp
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test_v11.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(14, 10))

# phase composition
plt.subplot(2, 3, 1)
plt.stackplot(
    df["load"],
    df["ccc_ratio"],
    df["gh_ratio"],
    df["kkk_ratio"],
    labels=["CCC", "GH", "KKK"]
)
plt.title("Phase Composition")
plt.xlabel("load")
plt.ylabel("ratio")
plt.legend(loc="upper right")

# Q° emergence
plt.subplot(2, 3, 2)
plt.plot(df["load"], df["q0_membrane"], marker="o", label="Q° membrane")
plt.plot(df["load"], df["q0_sharp"], marker="o", label="Q° sharp")
plt.title("Q° Emergence")
plt.xlabel("load")
plt.legend()

# phase dynamics
plt.subplot(2, 3, 3)
plt.plot(df["load"], df["phase_balance"], marker="o", label="balance")
plt.plot(df["load"], df["phase_tension"], marker="o", label="tension")
plt.title("Phase Dynamics")
plt.xlabel("load")
plt.legend()

# structure
plt.subplot(2, 3, 4)
plt.plot(df["load"], df["C_struct"], marker="o", label="C_struct")
plt.plot(df["load"], df["C_struct_norm"], marker="o", label="C_struct_norm")
plt.title("Structure Metrics")
plt.xlabel("load")
plt.legend()

# corridor widths
plt.subplot(2, 3, 5)
plt.plot(df["load"], df["gh_width_theta"], marker="o", label="θ width")
plt.plot(df["load"], df["gh_width_c"], marker="o", label="C width")
plt.title("GH Corridor Widths")
plt.xlabel("load")
plt.legend()

# anisotropy
plt.subplot(2, 3, 6)
plt.plot(df["load"], df["anisotropy"], marker="o")
plt.title("Corridor Anisotropy")
plt.xlabel("load")

plt.tight_layout()
plt.show()
