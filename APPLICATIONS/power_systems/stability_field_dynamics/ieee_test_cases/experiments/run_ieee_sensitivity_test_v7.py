import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    detect_gh_corridor
)

print("RUNNING IEEE SENSITIVITY TEST V7 (PHASE-COUPLED DYNAMICS)")

# ----------------------------
# CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)
results = []

ALPHA_THETA = 0.08
BETA_LOOPS = 2.0
GAMMA_C = 0.5

# phase thresholds
C_LOW = 0.018
C_HIGH = 0.028
L_LOW = 2.5
L_HIGH = 4.5

# ----------------------------
# PHASE CLASSIFIER
# ----------------------------

def classify_phases(c, loops):
    """
    CCC = high activity / expansion
    KKK = low activity / collapse
    GH  = interface / transition
    """
    phase = np.full(len(c), "GH", dtype=object)

    kkk_mask = (c < C_LOW) & (loops < L_LOW)
    ccc_mask = (c > C_HIGH) & (loops > L_HIGH)

    phase[kkk_mask] = "KKK"
    phase[ccc_mask] = "CCC"

    return phase

# ----------------------------
# MAIN LOOP
# ----------------------------

for load in loads:

    # --- base structure ---
    theta, c, loops = generate_phase_data(N=200)

    # ----------------------------
    # STRUCTURAL COUPLING
    # ----------------------------

    theta = theta * (1 + ALPHA_THETA * (load - 1))
    theta_std = np.std(theta)

    loops = loops + BETA_LOOPS * theta_std
    c = c * (1 + GAMMA_C * theta_std)

    # ----------------------------
    # GH DETECTION
    # ----------------------------

    gh = detect_gh_corridor(theta, c, loops)
    gh_points = len(gh["theta_corridor"])
    gh_width_theta = np.ptp(gh["theta_corridor"]) if gh_points > 0 else 0.0
    gh_width_c = np.ptp(gh["c_corridor"]) if gh_points > 0 else 0.0

    # ----------------------------
    # STRUCTURE METRICS
    # ----------------------------

    c_std = np.std(c)
    loops_mean = np.mean(loops)
    loops_std = np.std(loops)

    regime_separation = theta_std * c_std
    corridor_anisotropy = gh_width_theta / (gh_width_c + 1e-9)

    C_struct = regime_separation * loops_mean
    C_struct_norm = (
        (theta_std / (1 + theta_std))
        * (c_std / (1 + c_std))
        * (loops_mean / (1 + loops_mean))
    )

    # ----------------------------
    # PHASE METRICS
    # ----------------------------

    phase = classify_phases(c, loops)

    ccc_count = np.sum(phase == "CCC")
    gh_count = np.sum(phase == "GH")
    kkk_count = np.sum(phase == "KKK")

    total = len(phase)

    ccc_ratio = ccc_count / total
    gh_ratio = gh_count / total
    kkk_ratio = kkk_count / total

    # imbalance between extremes
    phase_tension = abs(ccc_ratio - kkk_ratio)

    # how dominant the corridor is
    gh_dominance = gh_ratio / (ccc_ratio + kkk_ratio + 1e-9)

    # balance index: high when GH is large and CCC/KKK are balanced
    phase_balance = gh_ratio * (1 - phase_tension)

    results.append({
        "load": load,

        # structure
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,
        "loops_std": loops_std,
        "regime_separation": regime_separation,
        "corridor_anisotropy": corridor_anisotropy,
        "C_struct": C_struct,
        "C_struct_norm": C_struct_norm,

        # GH corridor
        "gh_points": gh_points,
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,

        # phases
        "ccc_count": ccc_count,
        "gh_count": gh_count,
        "kkk_count": kkk_count,
        "ccc_ratio": ccc_ratio,
        "gh_ratio": gh_ratio,
        "kkk_ratio": kkk_ratio,
        "phase_tension": phase_tension,
        "gh_dominance": gh_dominance,
        "phase_balance": phase_balance
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test_v7.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(14, 10))

plt.subplot(2, 3, 1)
plt.plot(df["load"], df["C_struct"], marker="o")
plt.title("C_struct vs Load")

plt.subplot(2, 3, 2)
plt.plot(df["load"], df["phase_balance"], marker="o")
plt.title("Phase Balance vs Load")

plt.subplot(2, 3, 3)
plt.plot(df["load"], df["phase_tension"], marker="o")
plt.title("Phase Tension vs Load")

plt.subplot(2, 3, 4)
plt.plot(df["load"], df["gh_ratio"], marker="o", label="GH")
plt.plot(df["load"], df["ccc_ratio"], marker="o", label="CCC")
plt.plot(df["load"], df["kkk_ratio"], marker="o", label="KKK")
plt.title("Phase Ratios vs Load")
plt.legend()

plt.subplot(2, 3, 5)
plt.plot(df["load"], df["gh_width_theta"], marker="o")
plt.title("GH Width θ")

plt.subplot(2, 3, 6)
plt.plot(df["load"], df["corridor_anisotropy"], marker="o")
plt.title("Corridor Anisotropy")

plt.tight_layout()
plt.show()

# ----------------------------
# STACKED PHASE VIEW
# ----------------------------

plt.figure(figsize=(8, 5))
plt.stackplot(
    df["load"],
    df["ccc_ratio"],
    df["gh_ratio"],
    df["kkk_ratio"],
    labels=["CCC", "GH", "KKK"]
)
plt.title("Phase Composition vs Load")
plt.xlabel("load")
plt.ylabel("ratio")
plt.legend(loc="upper right")
plt.tight_layout()
plt.show()
