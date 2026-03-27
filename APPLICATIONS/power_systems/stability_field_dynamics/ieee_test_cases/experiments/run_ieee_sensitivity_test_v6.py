import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    detect_gh_corridor
)

print("RUNNING IEEE SENSITIVITY TEST V6 (STRUCTURE-SENSITIVE METRICS)")

# ----------------------------
# CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)
results = []

ALPHA_THETA = 0.08
BETA_LOOPS = 2.0
GAMMA_C = 0.5

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
    # NEW STRUCTURE-SENSITIVE METRICS
    # ----------------------------

    c_std = np.std(c)
    loops_mean = np.mean(loops)
    loops_std = np.std(loops)

    regime_separation = theta_std * c_std
    corridor_anisotropy = gh_width_theta / (gh_width_c + 1e-9)

    # New coupling metric:
    # stronger when spread + field separation + loop activity rise together
    C_struct = regime_separation * loops_mean

    # Optional normalized version
    C_struct_norm = (
        (theta_std / (1 + theta_std))
        * (c_std / (1 + c_std))
        * (loops_mean / (1 + loops_mean))
    )

    results.append({
        "load": load,

        # core structure
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,
        "loops_std": loops_std,

        # GH corridor
        "gh_points": gh_points,
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "corridor_anisotropy": corridor_anisotropy,

        # new metrics
        "regime_separation": regime_separation,
        "C_struct": C_struct,
        "C_struct_norm": C_struct_norm
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test_v6.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(14, 8))

plt.subplot(2, 3, 1)
plt.plot(df["load"], df["C_struct"], marker="o")
plt.title("C_struct vs Load")

plt.subplot(2, 3, 2)
plt.plot(df["load"], df["C_struct_norm"], marker="o")
plt.title("C_struct_norm vs Load")

plt.subplot(2, 3, 3)
plt.plot(df["load"], df["gh_points"], marker="o")
plt.title("GH Points vs Load")

plt.subplot(2, 3, 4)
plt.plot(df["load"], df["gh_width_theta"], marker="o")
plt.title("GH Width θ")

plt.subplot(2, 3, 5)
plt.plot(df["load"], df["gh_width_c"], marker="o")
plt.title("GH Width C")

plt.subplot(2, 3, 6)
plt.plot(df["load"], df["corridor_anisotropy"], marker="o")
plt.title("Corridor Anisotropy")

plt.tight_layout()
plt.show()

# extra structure plot
plt.figure(figsize=(8, 5))
plt.plot(df["load"], df["theta_std"], marker="o", label="theta_std")
plt.plot(df["load"], df["c_std"], marker="o", label="c_std")
plt.plot(df["load"], df["loops_mean"], marker="o", label="loops_mean")
plt.title("Structure Components vs Load")
plt.xlabel("load")
plt.legend()
plt.tight_layout()
plt.show()
