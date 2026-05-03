import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange

# =========================
# CONFIG
# =========================

np.random.seed(42)

N_RUNS = 20
N_RANDOM = 1000

mods = np.array(list(primerange(3, 200)))[:12]

# =========================
# PLACEHOLDER (DEIN CORE)
# =========================

def compute_metrics(mod):
    """
    HIER nutzt du deine bestehende Logik aus mod_validation_suite.py
    Muss zurückgeben:
    gap, drift, stat
    """

    # ⚠️ hier deine echte Berechnung rein
    gap = np.random.uniform(0.1, 0.7)
    drift = np.random.uniform(0.5, 2.0)
    stat = np.random.uniform(0.03, 0.15)

    return gap, drift, stat


def compute_random_baseline(mod):
    vals = [compute_metrics(mod) for _ in range(N_RANDOM)]
    vals = np.array(vals)

    mean = vals.mean(axis=0)
    std  = vals.std(axis=0)

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
# PLOT
# =========================

plt.figure(figsize=(10,6))

def plot_with_band(x, mean, std, label):
    plt.plot(x, mean, label=label)
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

plt.show()
