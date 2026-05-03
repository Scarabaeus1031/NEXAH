import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import os

# =========================
# CONFIG
# =========================

np.random.seed(42)

N_RUNS = 20
N_RANDOM = 500

mods = np.array(list(primerange(3, 200)))[:12]

OUTPUT_PATH = "output/plots"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# ⚠️ HIER ERSETZEN MIT DEINER LOGIK
# =========================

def compute_metrics(mod):
    # TODO: ersetze mit deinem echten Code
    gap = np.random.uniform(0.1, 0.7)
    drift = np.random.uniform(0.5, 2.0)
    stat = np.random.uniform(0.03, 0.15)
    return gap, drift, stat

def compute_random_baseline(mod):
    vals = [compute_metrics(mod) for _ in range(N_RANDOM)]
    vals = np.array(vals)

    mean = vals.mean(axis=0)
    std  = vals.std(axis=0) + 1e-9

    return mean, std

# =========================
# RUNS
# =========================

z_gap_runs = []
z_drift_runs = []
z_stat_runs = []

for run in range(N_RUNS):

    z_gap = []
    z_drift = []
    z_stat = []

    for m in mods:

        gap, drift, stat = compute_metrics(m)
        mean, std = compute_random_baseline(m)

        z_gap.append((gap - mean[0]) / std[0])
        z_drift.append((drift - mean[1]) / std[1])
        z_stat.append((stat - mean[2]) / std[2])

    z_gap_runs.append(z_gap)
    z_drift_runs.append(z_drift)
    z_stat_runs.append(z_stat)

z_gap_runs = np.array(z_gap_runs)
z_drift_runs = np.array(z_drift_runs)
z_stat_runs = np.array(z_stat_runs)

# =========================
# MEAN + STD
# =========================

gap_mean = z_gap_runs.mean(axis=0)
gap_std  = z_gap_runs.std(axis=0)

drift_mean = z_drift_runs.mean(axis=0)
drift_std  = z_drift_runs.std(axis=0)

stat_mean = z_stat_runs.mean(axis=0)
stat_std  = z_stat_runs.std(axis=0)

# =========================
# PRINT OUTPUT
# =========================

print("\n=== ROBUST VALIDATION ===\n")

for i, m in enumerate(mods):
    print(f"mod {m:2d} | "
          f"Z-gap = {gap_mean[i]:6.2f} ± {gap_std[i]:5.2f} | "
          f"Z-drift = {drift_mean[i]:6.2f} ± {drift_std[i]:5.2f} | "
          f"Z-stat = {stat_mean[i]:6.2f} ± {stat_std[i]:5.2f}")

# =========================
# SAVE DATA
# =========================

np.save("output/data/z_gap_mean.npy", gap_mean)
np.save("output/data/z_drift_mean.npy", drift_mean)
np.save("output/data/z_stat_mean.npy", stat_mean)

# =========================
# PLOT
# =========================

plt.figure(figsize=(10,6))

def plot_with_band(x, mean, std, label):
    plt.plot(x, mean, marker='o', label=label)
    plt.fill_between(x, mean-std, mean+std, alpha=0.2)

plot_with_band(mods, gap_mean, gap_std, "Z-gap")
plot_with_band(mods, drift_mean, drift_std, "Z-drift")
plot_with_band(mods, stat_mean, stat_std, "Z-stat")

plt.axhline(0, linestyle='--')
plt.title("Robust Validation (mean ± std)")
plt.xlabel("Modulus")
plt.ylabel("Z-score")
plt.legend()
plt.grid()

# ✅ SAVE
plot_file = f"{OUTPUT_PATH}/robust_validation.png"
plt.savefig(plot_file)

print(f"\n[OK] saved plot → {plot_file}")

plt.show()
