import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# COHERENCE CORE
# -----------------------------
def compute_coherence(x, window=20):
    dx = np.diff(x)
    kernel = np.ones(window) / window
    F = np.convolve(dx, kernel, mode='same')
    dx = dx[:len(F)]
    C = (dx * F) / (np.abs(dx) * np.abs(F) + 1e-8)
    return C

# -----------------------------
# ENVELOPE
# -----------------------------
def moving_avg(a, w=50):
    return np.convolve(np.abs(a), np.ones(w) / w, mode='same')

# -----------------------------
# TEST SIGNAL
# später durch IEEE / c(t) ersetzen
# -----------------------------
t = np.linspace(0, 80, 2000)
x = 1 - 0.002 * t + 0.01 * np.sin(0.4 * t)

# -----------------------------
# COMPUTE COHERENCE
# -----------------------------
C = compute_coherence(x)
C_env = moving_avg(C)

# -----------------------------
# POLAR MAPPING
# -----------------------------
theta = np.linspace(0, 2 * np.pi, len(C_env))
r = C_env

# -----------------------------
# RADIAL FLOW
# -----------------------------
dr = np.gradient(r)

# forward = nach außen
forward_mask = dr > 0

# backward = nach innen
backward_mask = dr < 0

# interface = fast kein radialer Wechsel
eps = 0.0005
interface_mask = np.abs(dr) <= eps

# -----------------------------
# OUTPUT PATH
# -----------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, "..", "visuals")
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# PLOT 1 — SPLIT POLAR
# -----------------------------
fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection="polar")

# Grundkurve leicht
ax.plot(theta, r, color="lightgray", linewidth=1.5, alpha=0.7)

# forward
ax.scatter(
    theta[forward_mask],
    r[forward_mask],
    s=8,
    label="Forward Field",
)

# backward
ax.scatter(
    theta[backward_mask],
    r[backward_mask],
    s=8,
    label="Backward Field",
)

# interface
ax.scatter(
    theta[interface_mask],
    r[interface_mask],
    s=16,
    label="Interface",
)

ax.set_title("NEXAH Field Split (v6)", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))

split_path = os.path.join(output_dir, "coherence_field_split_v6.png")
plt.savefig(split_path, dpi=300)
plt.show()

# -----------------------------
# PLOT 2 — RADIAL FLOW OVER TIME
# -----------------------------
plt.figure(figsize=(12, 4))
plt.plot(dr, linewidth=1.5, label="dr/dtheta (radial flow)")
plt.axhline(0, linestyle="--", color="gray", label="Interface line")
plt.title("NEXAH Radial Flow Split (v6)")
plt.legend()

flow_path = os.path.join(output_dir, "coherence_radial_flow_v6.png")
plt.savefig(flow_path, dpi=300)
plt.show()

# -----------------------------
# PLOT 3 — POLAR FLOW ARROWS
# -----------------------------
fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection="polar")

ax.plot(theta, r, linewidth=1.5, alpha=0.5)

step = 25
u = np.ones_like(theta[::step]) * 0.08   # tangential component
v = dr[::step]                           # radial component

ax.quiver(
    theta[::step],
    r[::step],
    u,
    v,
    scale=8,
    width=0.004,
)

ax.set_title("NEXAH Directional Field Flow (v6)", pad=20)

arrow_path = os.path.join(output_dir, "coherence_directional_flow_v6.png")
plt.savefig(arrow_path, dpi=300)
plt.show()

print("\nSaved files:")
print(split_path)
print(flow_path)
print(arrow_path)
print()
