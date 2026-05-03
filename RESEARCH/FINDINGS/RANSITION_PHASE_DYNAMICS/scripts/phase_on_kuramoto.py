import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# CONFIG
# ============================================================

OUTPUT_PATH = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/phase"
os.makedirs(OUTPUT_PATH, exist_ok=True)

T = 20000
DT = 0.02

N = 50          # Anzahl Oszillatoren
K = 2.0         # Kopplungsstärke (wichtig!)

# ============================================================
# KURAMOTO SYSTEM
# ============================================================

def kuramoto():

    # natürliche Frequenzen (leicht verteilt)
    omega = np.random.normal(loc=1.0, scale=0.1, size=N)

    # initiale Phasen
    theta = np.random.uniform(0, 2*np.pi, size=(T, N))

    for t in range(T-1):

        current = theta[t]

        coupling = np.zeros(N)

        for i in range(N):
            coupling[i] = np.sum(np.sin(current - current[i]))

        dtheta = omega + (K / N) * coupling

        theta[t+1] = current + DT * dtheta

    return theta


# ============================================================
# ANALYSIS
# ============================================================

def order_parameter(theta):
    """
    r(t) = Synchronisationsmaß
    """
    return np.abs(np.mean(np.exp(1j * theta), axis=1))


def phase_differences(theta):
    """
    mittlere Phasendifferenz pro Schritt
    """
    mean_theta = np.mean(theta, axis=1)
    dtheta = np.diff(mean_theta)
    return mean_theta, dtheta


# ============================================================
# RUN
# ============================================================

theta = kuramoto()

r = order_parameter(theta)
mean_theta, dtheta = phase_differences(theta)

# ============================================================
# PLOT
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(16, 4))

# ---- Synchronisation
axes[0].plot(r)
axes[0].set_title("Order Parameter r(t)")
axes[0].set_ylim(0, 1)

# ---- Phase Drift
axes[1].plot(mean_theta)
axes[1].set_title("Mean Phase θ(t)")

# ---- Δθ Distribution
axes[2].hist(dtheta, bins=100)
axes[2].set_title("Δθ Distribution")

plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/kuramoto_phase_analysis.png", dpi=200)

print("[OK] saved → kuramoto_phase_analysis.png")

# ============================================================
# INTERPRETATION
# ============================================================

print("\n=== KURAMOTO ANALYSIS ===")
print(f"Mean Δθ: {np.mean(dtheta):.6f}")
print(f"Std  Δθ: {np.std(dtheta):.6f}")
print(f"Final synchronization r: {r[-1]:.4f}")

print("\n=== INTERPRETATION ===")
print("""
If r(t) → 1:
→ system synchronizes (phase locking)

If r(t) stays low:
→ fragmented phase (Halvorsen-like)

If Δθ narrow:
→ coherent collective motion

If Δθ broad:
→ competing phase clusters
""")
