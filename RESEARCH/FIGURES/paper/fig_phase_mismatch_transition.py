import numpy as np
import matplotlib.pyplot as plt

# ============================================
# INPUT (hier deine echten Daten einsetzen)
# ============================================

# Beispiel: ersetze das mit deinen echten Arrays
# x: trajectory (T, n)
# phi: phase
# omega: phase velocity
# omega_hat: smoothed phase velocity
# I: instability
# IOTA: binary transition events (0/1)

# --- Dummy fallback (falls du testen willst) ---
T = 1000
t = np.arange(T)

x = np.cumsum(np.random.randn(T, 2) * 0.1, axis=0)
phi = np.arctan2(x[:,1], x[:,0])
omega = np.gradient(phi)
omega_hat = np.convolve(omega, np.ones(20)/20, mode='same')
M = np.abs(omega - omega_hat)
I = np.linalg.norm(np.gradient(x, axis=0), axis=1)

# simple IOTA detection (ersetzen durch dein echtes)
threshold = np.percentile(M, 90)
IOTA = (M > threshold).astype(int)

# ============================================
# FIGURE
# ============================================

fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

# --------------------------------------------
# (A) Trajectory
# --------------------------------------------
axs[0].plot(x[:,0], x[:,1], linewidth=1.0)
axs[0].set_title("(A) Trajectory in State Space")
axs[0].set_xlabel("x₁")
axs[0].set_ylabel("x₂")

# --------------------------------------------
# (B) Instability
# --------------------------------------------
axs[1].plot(t, I, linewidth=1.0)
axs[1].set_title("(B) Instability I(t)")
axs[1].set_ylabel("I")

# --------------------------------------------
# (C) Mismatch
# --------------------------------------------
axs[2].plot(t, M, linewidth=1.0)
axs[2].scatter(t[IOTA == 1], M[IOTA == 1], s=10)  # Highlight events
axs[2].set_title("(C) Phase Mismatch M(t)")
axs[2].set_ylabel("M")

# --------------------------------------------
# (D) IOTA Events
# --------------------------------------------
axs[3].plot(t, IOTA, linewidth=1.0)
axs[3].set_title("(D) Transition Events (IOTA)")
axs[3].set_xlabel("time")
axs[3].set_ylabel("event")

# --------------------------------------------
# Layout
# --------------------------------------------
plt.tight_layout()

# ============================================
# SAVE
# ============================================

output_path = "FIGURES/paper/fig_phase_mismatch_transition.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Saved figure to: {output_path}")
