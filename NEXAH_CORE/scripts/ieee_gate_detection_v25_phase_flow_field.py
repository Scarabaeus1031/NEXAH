# ieee_gate_detection_v25_phase_flow_field.py

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Signal erzeugen (wie vorher)
# -----------------------------
np.random.seed(42)

T = 1000
t = np.arange(T)

signal = np.sin(0.2 * t)

# regime change
signal[600:] += np.random.normal(0, 0.5, size=T-600)

# -----------------------------
# 2. Phase space (θ, r)
# -----------------------------
theta = np.angle(signal + 1j * np.roll(signal, 1))
theta = np.unwrap(theta)

r = np.abs(signal)

# -----------------------------
# 3. Flow berechnen
# -----------------------------
dtheta = np.diff(theta)
dr = np.diff(r)

theta_mid = theta[:-1]
r_mid = r[:-1]

# -----------------------------
# 4. Downsampling (wichtig!)
# -----------------------------
step = 5
theta_mid = theta_mid[::step]
r_mid = r_mid[::step]
dtheta = dtheta[::step]
dr = dr[::step]

# -----------------------------
# 5. Plot
# -----------------------------
plt.figure(figsize=(10, 6))

# Hintergrund: Punkte
plt.scatter(theta, r, s=5, alpha=0.1, color='gray')

# Flow Vektoren
plt.quiver(
    theta_mid,
    r_mid,
    dtheta,
    dr,
    angles='xy',
    scale_units='xy',
    scale=1,
    width=0.003,
    color='blue',
    alpha=0.6
)

# Transition markieren
plt.axvline(theta[600], linestyle='--', color='black', label='true transition')

plt.xlabel("θ (unwrapped)")
plt.ylabel("r")
plt.title("V25 — Phase Flow Field")
plt.legend()

plt.tight_layout()
plt.savefig("NEXAH_CORE/outputs/ieee_gates/v25_phase_flow_field.png")
plt.show()
