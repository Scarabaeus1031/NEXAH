import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# CONFIG
# ============================================================

OUTPUT_PATH = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/kuramoto"
os.makedirs(OUTPUT_PATH, exist_ok=True)

T = 20000
DT = 0.01
N = 50

K_VALUES = [0.2, 0.5, 1.0, 2.0]

# ============================================================
# KURAMOTO SYSTEM
# ============================================================

def kuramoto(K):

    omega = np.random.normal(1.0, 0.1, N)
    theta = np.random.uniform(0, 2*np.pi, N)

    theta_history = []

    for t in range(T):
        theta_matrix = theta[:, None]
        coupling = np.sin(theta_matrix - theta)

        dtheta = omega + (K/N) * np.sum(coupling, axis=1)
        theta = theta + DT * dtheta

        theta_history.append(theta.copy())

    return np.array(theta_history)

# ============================================================
# ANALYSIS
# ============================================================

def compute_order_parameter(theta_history):

    r = []
    mean_phase = []

    for theta in theta_history:
        z = np.exp(1j * theta)
        r_t = np.abs(np.mean(z))
        psi = np.angle(np.mean(z))

        r.append(r_t)
        mean_phase.append(psi)

    return np.array(r), np.unwrap(mean_phase)

# ============================================================
# PLOT
# ============================================================

fig, axes = plt.subplots(len(K_VALUES), 3, figsize=(15, 10))

for i, K in enumerate(K_VALUES):

    theta_hist = kuramoto(K)
    r, psi = compute_order_parameter(theta_hist)

    dpsi = np.diff(psi)

    # ---- Order Parameter
    ax = axes[i, 0]
    ax.plot(r)
    ax.set_title(f"K = {K} — r(t)")
    ax.set_ylim(0, 1)

    # ---- Phase
    ax = axes[i, 1]
    ax.plot(psi)
    ax.set_title("Mean Phase θ(t)")

    # Plateau shading
    grad = np.abs(np.gradient(psi))
    threshold = np.percentile(grad, 20)
    mask = grad < threshold

    for j in range(len(mask)):
        if mask[j]:
            ax.axvspan(j, j+1, color='red', alpha=0.05)

    # ---- Δθ Distribution
    ax = axes[i, 2]
    ax.hist(dpsi, bins=100)
    ax.set_title("Δθ Distribution")

plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/kuramoto_phase_sweep.png", dpi=200)

print(f"[OK] saved → {OUTPUT_PATH}/kuramoto_phase_sweep.png")
