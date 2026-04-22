import numpy as np
import matplotlib.pyplot as plt

# === LOAD CHANNELS ===
channels = np.load("FIELD_LAYER/field_decomposition/outputs/v9_5/orbit_entry_channels.npy")

# === LOAD BASE FIELD (aus früherem Step) ===
# → meist aus Phase Field / Grid
density = np.load("FIELD_LAYER/field_decomposition/outputs/v9_2/unique_density.npy")

# === COMPUTE GRADIENT ===
gy, gx = np.gradient(density)

# === ROTATE → Flow Field (orthogonal) ===
dx = -gy
dy = gx

# === MASK CHANNELS ===
mask = channels > 0
y_idx, x_idx = np.where(mask)

dx_c = dx[y_idx, x_idx]
dy_c = dy[y_idx, x_idx]

# === NORMALIZE ===
mag = np.sqrt(dx_c**2 + dy_c**2) + 1e-8
dx_n = dx_c / mag
dy_n = dy_c / mag

angles = np.arctan2(dy_n, dx_n)

# === PLOT ===
plt.figure(figsize=(8, 8))
plt.imshow(mask, cmap="gray", alpha=0.3)

plt.quiver(
    x_idx,
    y_idx,
    dx_n,
    dy_n,
    angles,
    cmap="hsv",
    scale=60,
    width=0.003
)

plt.title("NEXAH V9.6 — Direction Field (Gradient-Based)")
plt.gca().invert_yaxis()
plt.colorbar(label="angle (rad)")
plt.tight_layout()

plt.savefig("FIELD_LAYER/field_decomposition/outputs/v9_6/direction_field.png")
print("✓ V9.6 done")
