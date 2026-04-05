import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# Coherence Funktion
# -----------------------------
def compute_coherence(x, window=20):
    dx = np.diff(x)
    kernel = np.ones(window) / window
    F = np.convolve(dx, kernel, mode='same')
    dx = dx[:len(F)]
    C = (dx * F) / (np.abs(dx) * np.abs(F) + 1e-8)
    return C

# -----------------------------
# Envelope (Glättung)
# -----------------------------
def moving_avg(a, w=50):
    return np.convolve(np.abs(a), np.ones(w)/w, mode='same')

# -----------------------------
# Testsignal (ersetzen durch IEEE!)
# -----------------------------
t = np.linspace(0, 80, 2000)
x = 1 - 0.002 * t + 0.01 * np.sin(0.4 * t)

# -----------------------------
# Compute
# -----------------------------
C = compute_coherence(x)
C_env = moving_avg(C)

# -----------------------------
# Polar Mapping
# -----------------------------
theta = np.linspace(0, 2*np.pi, len(C_env))
r = C_env

# -----------------------------
# Richtungsvektoren (Flow!)
# -----------------------------
dtheta = np.gradient(theta)
dr = np.gradient(r)

# -----------------------------
# Plot
# -----------------------------
fig = plt.figure(figsize=(8,8))
ax = plt.subplot(111, projection='polar')

# Hauptkurve
ax.plot(theta, r, linewidth=2)

# Flow-Vektoren
step = 20
ax.quiver(
    theta[::step],
    r[::step],
    dtheta[::step],
    dr[::step],
    scale=50,
    width=0.003
)

ax.set_title("NEXAH Coherence Flow (v5)", pad=20)

# -----------------------------
# SAVE (robust!)
# -----------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, "..", "visuals")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "coherence_flow_v5.png")

plt.savefig(output_path, dpi=300)
plt.show()

print(f"\nSaved to: {output_path}\n")
