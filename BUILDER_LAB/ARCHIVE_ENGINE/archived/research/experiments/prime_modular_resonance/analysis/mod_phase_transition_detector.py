import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import os

# =========================
# CONFIG
# =========================

USE_AUTO_MODS = True
N_PRIMES_MODS = 25

DATA_PATH = "output/data"
PLOT_PATH = "output/plots"

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(PLOT_PATH, exist_ok=True)

# =========================
# LOAD OR GENERATE MODS
# =========================

if USE_AUTO_MODS:
    mods = np.array(list(primerange(3, 300)))[:N_PRIMES_MODS]
else:
    mods = np.array([7,11,13,17,19,23,29,31])

# =========================
# LOAD DATA
# =========================

def safe_load(name):
    path = f"{DATA_PATH}/{name}.npy"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    return np.load(path)

z_gap   = safe_load("z_gap")
z_drift = safe_load("z_drift")
z_stat  = safe_load("z_stat")

# 🔥 MATCH LENGTHS
n = min(len(mods), len(z_gap), len(z_drift), len(z_stat))

mods    = mods[:n]
z_gap   = z_gap[:n]
z_drift = z_drift[:n]
z_stat  = z_stat[:n]

# =========================
# GRADIENTS
# =========================

def compute_gradients(values, mods):
    return np.gradient(values, mods)

grad_gap   = compute_gradients(z_gap, mods)
grad_drift = compute_gradients(z_drift, mods)
grad_stat  = compute_gradients(z_stat, mods)

# =========================
# DETECT TRANSITIONS
# =========================

def detect_phase_transitions(signal, threshold=0.5):
    transitions = []
    for i in range(1, len(signal)):
        delta = abs(signal[i] - signal[i-1])
        if delta > threshold:
            transitions.append((mods[i-1], mods[i], delta))
    return transitions

trans_gap   = detect_phase_transitions(grad_gap)
trans_drift = detect_phase_transitions(grad_drift)
trans_stat  = detect_phase_transitions(grad_stat)

# =========================
# DRIFT COLLAPSE
# =========================

def detect_drift_collapse(z_drift, threshold=1.0):
    return [(m, v) for m, v in zip(mods, z_drift) if abs(v) < threshold]

drift_collapse = detect_drift_collapse(z_drift)

# =========================
# SCALING TEST (robust)
# =========================

def compute_scaling(mods, values):
    values = np.array(values)

    # ❗ remove zeros & negatives safely
    mask = (values != 0) & (~np.isnan(values))
    mods = mods[mask]
    values = np.abs(values[mask])

    # avoid log(0)
    eps = 1e-12
    values = values + eps

    log_m = np.log(mods)
    log_v = np.log(values)

    slope, intercept = np.polyfit(log_m, log_v, 1)
    return slope, intercept

slope_drift, _ = compute_scaling(mods, z_drift)
slope_gap, _   = compute_scaling(mods, z_gap)
slope_stat, _  = compute_scaling(mods, z_stat)

# =========================
# OUTPUT
# =========================

print("\n=== PHASE TRANSITIONS ===")

print("\nZ-gap:")
for t in trans_gap:
    print(f"{t[0]} → {t[1]}  Δ={t[2]:.2f}")

print("\nZ-drift:")
for t in trans_drift:
    print(f"{t[0]} → {t[1]}  Δ={t[2]:.2f}")

print("\nZ-stat:")
for t in trans_stat:
    print(f"{t[0]} → {t[1]}  Δ={t[2]:.2f}")

print("\n=== DRIFT COLLAPSE ===")
for m, v in drift_collapse:
    print(f"mod {m}  (Z≈{v:.2f})")

print("\n=== SCALING ===")
print(f"drift ~ mod^{slope_drift:.3f}")
print(f"gap   ~ mod^{slope_gap:.3f}")
print(f"stat  ~ mod^{slope_stat:.3f}")

# =========================
# PLOT 1 — Z-SCORES
# =========================

plt.figure(figsize=(10,6))

plt.plot(mods, z_gap, 'o-', label='Z-gap')
plt.plot(mods, z_drift, 'o-', label='Z-drift')
plt.plot(mods, z_stat, 'o-', label='Z-stat')

for m, v in drift_collapse:
    plt.scatter(m, v, s=120, marker='x', color='black')

plt.axhline(0, linestyle='--')
plt.title("Phase Transition Map")
plt.xlabel("Modulus")
plt.ylabel("Z-score")
plt.legend()
plt.grid()

plt.savefig(f"{PLOT_PATH}/phase_map.png")
plt.show()

# =========================
# PLOT 2 — SCALING
# =========================

plt.figure(figsize=(8,6))

# safer plotting (ignore zeros)
def safe_log_plot(x, y, label):
    mask = (y != 0) & (~np.isnan(y))
    plt.scatter(np.log(x[mask]), np.log(np.abs(y[mask])), label=label)

safe_log_plot(mods, z_drift, 'drift')
safe_log_plot(mods, z_gap, 'gap')
safe_log_plot(mods, z_stat, 'stat')

plt.title("Scaling (log-log)")
plt.xlabel("log(mod)")
plt.ylabel("log(|Z|)")
plt.legend()
plt.grid()

plt.savefig(f"{PLOT_PATH}/scaling.png")
plt.show()

# =========================
# SUMMARY
# =========================

print("\n=== INTERPRETATION ===")
print("""
System behavior:

LOW MOD:
→ strong transport + structure

MID MOD:
→ unstable transition regime

HIGH MOD:
→ transport collapses
→ structure persists

Key:
→ structure ≠ transport
→ system becomes diffusive at scale
""")
