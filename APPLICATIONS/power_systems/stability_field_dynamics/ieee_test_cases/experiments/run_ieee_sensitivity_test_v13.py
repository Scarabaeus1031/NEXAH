import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    generate_phase_data,
    compute_metrics,
    detect_gh_corridor
)

print("RUNNING IEEE SENSITIVITY TEST V13 (RESONANCE ALIGNMENT LAYER)")

# ----------------------------
# CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)
results = []

BANDS = {
    "eta1_0429": 0.429,
    "mid_0456": 0.456,
    "phi_0472": 0.472,
    "top_0487": 0.487,
}

TARGET_MIN = 0.429
TARGET_MAX = 0.487

# ----------------------------
# HELPERS
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

def nearest_band(x, bands):
    distances = [(name, abs(x - val), val) for name, val in bands.items()]
    distances.sort(key=lambda t: t[1])
    return distances[0]

def map_local_to_resonance(x, x_min, x_max, target_min=TARGET_MIN, target_max=TARGET_MAX):
    """
    Linear map from local C-range to resonance band range.
    """
    if not np.isfinite(x):
        return np.nan
    if abs(x_max - x_min) < 1e-12:
        return 0.5 * (target_min + target_max)
    alpha = (x - x_min) / (x_max - x_min)
    return target_min + alpha * (target_max - target_min)

# ----------------------------
# PASS 1: COLLECT LOCAL DATA
# ----------------------------

raw_rows = []

for load in loads:
    theta, c, loops = generate_phase_data(N=200)

    # same nonlinear coupling as v12
    theta = theta * (1 + 0.10 * (load - 1))

    c = c * (1 + 0.20 * (load - 1))
    c = c + 0.05 * load * np.sin(2 * theta)

    loops = loops * (1 + 0.15 * (load - 1))
    loops = loops + 0.10 * np.cos(load * theta)

    metrics = compute_metrics(theta, c, loops)
    gh = detect_gh_corridor(theta, c, loops)

    gh_points = len(gh["theta_corridor"])
    gh_width_theta = np.ptp(gh["theta_corridor"]) if gh_points > 0 else 0.0
    gh_width_c = np.ptp(gh["c_corridor"]) if gh_points > 0 else 0.0
    gh_c_mean = np.mean(gh["c_corridor"]) if gh_points > 0 else np.nan
    gh_c_std = np.std(gh["c_corridor"]) if gh_points > 0 else np.nan

    phases = classify_dynamic_phases(c, loops)
    total = len(phases)

    ccc_ratio = np.sum(phases == "CCC") / total
    gh_ratio = np.sum(phases == "GH") / total
    kkk_ratio = np.sum(phases == "KKK") / total

    q0_membrane = gh_ratio * (1.0 - abs(ccc_ratio - kkk_ratio))
    q0_sharp = gh_ratio * np.minimum(ccc_ratio, kkk_ratio)

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

    raw_rows.append({
        "load": load,
        "pipeline_C": metrics["C"],
        "pipeline_P": metrics["P"],
        "pipeline_R": metrics["R"],
        "pipeline_L": metrics["L"],
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,
        "regime_separation": regime_separation,
        "anisotropy": anisotropy,
        "C_struct": C_struct,
        "C_struct_norm": C_struct_norm,
        "gh_points": gh_points,
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "gh_c_mean_local": gh_c_mean,
        "gh_c_std_local": gh_c_std,
        "ccc_ratio": ccc_ratio,
        "gh_ratio": gh_ratio,
        "kkk_ratio": kkk_ratio,
        "phase_tension": phase_tension,
        "phase_balance": phase_balance,
        "q0_membrane": q0_membrane,
        "q0_sharp": q0_sharp,
    })

df = pd.DataFrame(raw_rows)

# ----------------------------
# PASS 2: MAP TO RESONANCE SPACE
# ----------------------------

x_min = np.nanmin(df["gh_c_mean_local"].values)
x_max = np.nanmax(df["gh_c_mean_local"].values)

df["gh_c_resonant"] = df["gh_c_mean_local"].apply(
    lambda x: map_local_to_resonance(x, x_min, x_max)
)

band_names = []
band_values = []
band_distances = []

for x in df["gh_c_resonant"]:
    name, dist, val = nearest_band(x, BANDS)
    band_names.append(name)
    band_values.append(val)
    band_distances.append(dist)

df["nearest_band"] = band_names
df["nearest_band_value"] = band_values
df["band_distance"] = band_distances

# critical point from Q°
peak_idx = int(df["q0_membrane"].idxmax())
critical_row = df.loc[peak_idx]

critical_load = float(critical_row["load"])
critical_q0 = float(critical_row["q0_membrane"])
critical_local_c = float(critical_row["gh_c_mean_local"])
critical_resonant_c = float(critical_row["gh_c_resonant"])
critical_band_name = str(critical_row["nearest_band"])
critical_band_value = float(critical_row["nearest_band_value"])
critical_band_distance = float(critical_row["band_distance"])

df["critical_load_global"] = critical_load
df["critical_q0_global"] = critical_q0
df["critical_local_c_global"] = critical_local_c
df["critical_resonant_c_global"] = critical_resonant_c
df["critical_band_name_global"] = critical_band_name
df["critical_band_value_global"] = critical_band_value
df["critical_band_distance_global"] = critical_band_distance

# ----------------------------
# SAVE + PRINT
# ----------------------------

df.to_csv("ieee_sensitivity_test_v13.csv", index=False)

print("\n--- RESULTS ---")
print(df)

print("\n--- CRITICAL RESONANCE ZONE ---")
print(f"Critical load            : {critical_load:.6f}")
print(f"Q° peak                  : {critical_q0:.6f}")
print(f"GH mean C (local)        : {critical_local_c:.6f}")
print(f"GH mean C (resonant)     : {critical_resonant_c:.6f}")
print(f"Nearest band             : {critical_band_name}")
print(f"Nearest band value       : {critical_band_value:.6f}")
print(f"Distance to nearest band : {critical_band_distance:.6f}")

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(14, 10))

# 1. Q° emergence
plt.subplot(2, 3, 1)
plt.plot(df["load"], df["q0_membrane"], marker="o", label="Q° membrane")
plt.plot(df["load"], df["q0_sharp"], marker="o", label="Q° sharp")
plt.axvline(critical_load, linestyle="--", alpha=0.7, label="critical load")
plt.title("Q° Emergence")
plt.xlabel("load")
plt.legend()

# 2. local vs resonant GH mean C
plt.subplot(2, 3, 2)
plt.plot(df["load"], df["gh_c_mean_local"], marker="o", label="local C")
plt.plot(df["load"], df["gh_c_resonant"], marker="o", label="resonant C")
for name, val in BANDS.items():
    plt.axhline(val, linestyle="--", alpha=0.5, label=name)
plt.title("Local / Resonant GH Mean C")
plt.xlabel("load")
plt.legend(fontsize=8)

# 3. distance to nearest band
plt.subplot(2, 3, 3)
plt.plot(df["load"], df["band_distance"], marker="o")
plt.axvline(critical_load, linestyle="--", alpha=0.7)
plt.title("Distance to Nearest Resonance Band")
plt.xlabel("load")

# 4. phase composition
plt.subplot(2, 3, 4)
plt.stackplot(
    df["load"],
    df["ccc_ratio"],
    df["gh_ratio"],
    df["kkk_ratio"],
    labels=["CCC", "GH", "KKK"]
)
plt.title("Phase Composition")
plt.xlabel("load")
plt.legend(loc="upper right")

# 5. corridor widths
plt.subplot(2, 3, 5)
plt.plot(df["load"], df["gh_width_theta"], marker="o", label="θ width")
plt.plot(df["load"], df["gh_width_c"], marker="o", label="C width")
plt.axvline(critical_load, linestyle="--", alpha=0.7)
plt.title("GH Corridor Widths")
plt.xlabel("load")
plt.legend()

# 6. structure/balance
plt.subplot(2, 3, 6)
plt.plot(df["load"], df["C_struct_norm"], marker="o", label="C_struct_norm")
plt.plot(df["load"], df["phase_balance"], marker="o", label="phase_balance")
plt.axvline(critical_load, linestyle="--", alpha=0.7)
plt.title("Structure / Balance")
plt.xlabel("load")
plt.legend()

plt.tight_layout()
plt.show()
