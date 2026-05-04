import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================
# SETTINGS
# ============================================

OUTPUT_PATH = "RESEARCH/FIGURES/paper/fig_phase_mismatch_transition.png"

# ============================================
# CREATE OUTPUT FOLDER (fix für deinen Fehler)
# ============================================

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# ============================================
# DEMO DATA (läuft sofort)
# 👉 später durch deine echten Daten ersetzen
# ============================================

T = 1000
t = np.arange(T)

# Fake trajectory (2D)
x = np.cumsum(np.random.randn(T, 2) * 0.1, axis=0)

# Phase
phi = np.arctan2(x[:, 1], x[:, 0])

# Phase velocity
omega = np.gradient(phi)

# Expected phase (glättung)
window = 20
omega_hat = np.convolve(omega, np.ones(window)/window, mode='same')

# Mismatch
M = np.abs(omega - omega_hat)

# Instability
I = np.linalg.norm(np.gradient(x, axis=0), axis=1)

# Transition detection (einfach)
threshold = np.percentile(M, 90)
IOTA = (M > threshold).astype(int)

# ============================================
# FIGURE
# ============================================

fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

# (A) Trajectory
axs[0].plot(x[:, 0], x[:, 1], linewidth=1)
axs[0].set_title("(A) Trajectory")
axs[0].set_xlabel("x1")
axs[0].set_ylabel("x2")

# (B) Instability
axs[1].plot(t, I, linewidth=1)
axs[1].set_title("(B) Instability I(t)")
axs[1].set_ylabel("I")

# (C) Mismatch
axs[2].plot(t, M, linewidth=1)
axs[2].scatter(t[IOTA == 1], M[IOTA == 1], s=10)
axs[2].axhline(threshold, linestyle="--")
axs[2].set_title("(C) Phase Mismatch M(t)")
axs[2].set_ylabel("M")

# (D) IOTA Events
axs[3].plot(t, IOTA, linewidth=1)
axs[3].set_title("(D) Transition Events (IOTA)")
axs[3].set_xlabel("time")
axs[3].set_ylabel("event")

plt.tight_layout()

# ============================================
# SAVE PNG
# ============================================

plt.savefig(OUTPUT_PATH, dpi=300)
plt.close()

print(f"✅ Figure saved to: {OUTPUT_PATH}")
