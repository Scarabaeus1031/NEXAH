import numpy as np
import matplotlib.pyplot as plt
import os

print("⚡ NEXAH — Mismatch vs IOTA (Corrected)")

# ============================================
# SETTINGS
# ============================================

OUTPUT_PATH = "RESEARCH/FIGURES/paper/fig_mismatch_iota_probability.png"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

n_steps = 5000
dt = 0.01

# ============================================
# LORENZ SYSTEM
# ============================================

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

# ============================================
# INITIAL STATE
# ============================================

x = np.array([5.0, 5.0, 25.0])

trajectory = []
phi_list = []
omega_list = []
instability_list = []

# ============================================
# SIMULATION
# ============================================

for i in range(n_steps):
    trajectory.append(x.copy())

    # phase (simple projection)
    phi = np.arctan2(x[1], x[0])
    phi_list.append(phi)

    # instability
    inst = np.linalg.norm(x[:2])
    instability_list.append(inst)

    x = x + dt * lorenz(x)

trajectory = np.array(trajectory)
phi_list = np.array(phi_list)
instability_list = np.array(instability_list)

# ============================================
# PHASE VELOCITY + MISMATCH
# ============================================

omega = np.gradient(phi_list)

# smoothing (expected phase)
window = 50
omega_hat = np.convolve(omega, np.ones(window)/window, mode='same')

mismatch = np.abs(omega - omega_hat)

# ============================================
# INDEPENDENT IOTA DEFINITION (WICHTIG!)
# ============================================

# IOTA = instabilitätsbasierter Trigger (unabhängig von mismatch)
inst_threshold = np.percentile(instability_list, 90)
iota = instability_list > inst_threshold

# ============================================
# BINNING: P(IOTA | M)
# ============================================

bins = np.linspace(np.min(mismatch), np.max(mismatch), 30)
prob = []

for i in range(len(bins) - 1):
    mask = (mismatch >= bins[i]) & (mismatch < bins[i + 1])

    if np.sum(mask) > 10:
        p = np.mean(iota[mask])
    else:
        p = np.nan

    prob.append(p)

bin_centers = 0.5 * (bins[:-1] + bins[1:])

# ============================================
# PLOT
# ============================================

plt.figure(figsize=(8, 5))
plt.plot(bin_centers, prob, 'o-', label="P(IOTA | Mismatch)")

plt.xlabel("Mismatch M")
plt.ylabel("P(IOTA)")
plt.title("Phase Mismatch vs Transition Probability")

plt.grid(True)
plt.legend()
plt.tight_layout()

# ============================================
# SAVE
# ============================================

plt.savefig(OUTPUT_PATH, dpi=300)
plt.close()

print(f"✅ Saved: {OUTPUT_PATH}")
