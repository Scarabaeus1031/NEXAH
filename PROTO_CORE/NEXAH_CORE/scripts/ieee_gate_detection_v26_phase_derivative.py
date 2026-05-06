# ieee_gate_detection_v26_phase_derivative.py

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Signal erzeugen
# -----------------------------
np.random.seed(42)

T = 1000
t = np.arange(T)

signal = np.sin(0.2 * t)

# regime change
signal[600:] += np.random.normal(0, 0.5, size=T-600)

# -----------------------------
# 2. Phase Space (θ, r)
# -----------------------------
theta = np.angle(signal + 1j * np.roll(signal, 1))
theta = np.unwrap(theta)

r = np.abs(signal)

# -----------------------------
# 3. Ableitungen
# -----------------------------
dtheta = np.diff(theta)
dr = np.diff(r)

# Stabilisierung (Division vermeiden)
eps = 1e-6
dr_dtheta = dr / (dtheta + eps)

theta_mid = theta[:-1]

# -----------------------------
# 4. Plot 1 — Scatter
# -----------------------------
plt.figure(figsize=(10, 5))

plt.scatter(theta_mid, dr_dtheta, s=5, alpha=0.3, color='blue')

plt.axvline(theta[600], linestyle='--', color='black', label='true transition')

plt.xlabel("θ (unwrapped)")
plt.ylabel("dr/dθ")
plt.title("V26 — Phase Derivative Field (dr/dθ)")
plt.legend()

plt.tight_layout()
plt.savefig("NEXAH_CORE/outputs/ieee_gates/v26_dr_dtheta_scatter.png")
plt.show()


# -----------------------------
# 5. Plot 2 — Density (Heatmap)
# -----------------------------
plt.figure(figsize=(10, 5))

bins_theta = 150
bins_ratio = 150

plt.hist2d(
    theta_mid,
    dr_dtheta,
    bins=[bins_theta, bins_ratio],
    cmap='viridis'
)

plt.colorbar(label="density")

plt.axvline(theta[600], linestyle='--', color='white')

plt.xlabel("θ (unwrapped)")
plt.ylabel("dr/dθ")
plt.title("V26 — Phase Derivative Density")

plt.tight_layout()
plt.savefig("NEXAH_CORE/outputs/ieee_gates/v26_dr_dtheta_density.png")
plt.show()


# -----------------------------
# 6. Optional — Clipped Version (wichtiger!)
# -----------------------------
# extreme Werte entfernen für bessere Struktur
clip_val = 5
mask = np.abs(dr_dtheta) < clip_val

plt.figure(figsize=(10, 5))

plt.scatter(theta_mid[mask], dr_dtheta[mask], s=5, alpha=0.3, color='green')

plt.axvline(theta[600], linestyle='--', color='black')

plt.xlabel("θ (unwrapped)")
plt.ylabel("dr/dθ (clipped)")
plt.title("V26 — Phase Derivative (Clipped)")

plt.tight_layout()
plt.savefig("NEXAH_CORE/outputs/ieee_gates/v26_dr_dtheta_clipped.png")
plt.show()
