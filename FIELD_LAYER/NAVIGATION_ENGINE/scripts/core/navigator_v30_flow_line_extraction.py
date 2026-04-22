# navigator_v30_flow_line_extraction.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# --------------------------------------------------
# 1. Grid
# --------------------------------------------------

x = np.linspace(6, 17, 200)
y = np.linspace(22, 31, 200)
X, Y = np.meshgrid(x, y)

# --------------------------------------------------
# 2. Cluster Centers (same as before)
# --------------------------------------------------

centers = {
    "C0": (10, 25),
    "C1": (12, 24),
    "C2": (13.5, 26),
    "C3": (11, 28.5),
}

# --------------------------------------------------
# 3. Potential Field (Envelope)
# --------------------------------------------------

def gaussian(x, y, cx, cy, amp, sigma=1.2):
    return amp * np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * sigma**2))

V = (
    gaussian(X, Y, *centers["C2"], amp=3.0) +   # attractive basin
    gaussian(X, Y, *centers["C1"], amp=2.0) +
    gaussian(X, Y, *centers["C0"], amp=1.5) -
    gaussian(X, Y, *centers["C3"], amp=2.5)     # repulsive peak
)

V = gaussian_filter(V, sigma=1.0)

# --------------------------------------------------
# 4. Gradient (−∇V)
# --------------------------------------------------

dVy, dVx = np.gradient(V)
Fx = -dVx
Fy = -dVy

# --------------------------------------------------
# 5. Rotational Component
# --------------------------------------------------

def rotation_field(x, y, cx, cy, strength=2.0):
    dx = x - cx
    dy = y - cy
    return -strength * dy, strength * dx

Rx = np.zeros_like(X)
Ry = np.zeros_like(Y)

for key in centers:
    cx, cy = centers[key]
    rx, ry = rotation_field(X, Y, cx, cy, strength=0.15)
    Rx += rx
    Ry += ry

# --------------------------------------------------
# 6. Combined Field
# --------------------------------------------------

Fx_total = Fx + Rx
Fy_total = Fy + Ry

# --------------------------------------------------
# 7. Normalize for stability
# --------------------------------------------------

mag = np.sqrt(Fx_total**2 + Fy_total**2) + 1e-6
Fx_n = Fx_total / mag
Fy_n = Fy_total / mag

# --------------------------------------------------
# 8. Plot
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 8))

# Scalar field background
ax.contourf(X, Y, V, levels=40, cmap="viridis")

# Streamlines = Flow Lines (!!)
ax.streamplot(
    X, Y,
    Fx_n, Fy_n,
    color="white",
    density=2.0,
    linewidth=1.2,
    arrowsize=1.2
)

# Cluster markers
colors = {
    "C0": "blue",
    "C1": "orange",
    "C2": "green",
    "C3": "red",
}

for key, (cx, cy) in centers.items():
    ax.scatter(cx, cy, s=120, color=colors[key], edgecolor="black")
    ax.text(cx+0.1, cy+0.1, key, color="white")

ax.set_title("V30 — Flow Line Extraction (Zero-Line Structure)")
ax.set_xlabel("α")
ax.set_ylabel("β")

plt.tight_layout()

# --------------------------------------------------
# 9. Save
# --------------------------------------------------

save_path = "FIELD_LAYER/outputs/plots/v30_flow_line_extraction.png"
plt.savefig(save_path, dpi=150)
plt.close()

print(f"Saved: {save_path}")
