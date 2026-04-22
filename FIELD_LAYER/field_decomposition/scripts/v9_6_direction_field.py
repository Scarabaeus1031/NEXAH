import numpy as np
import matplotlib.pyplot as plt

# === Load data ===
flow = np.load("FIELD_LAYER/field_decomposition/outputs/v9_0/flow_field.npy")
channels = np.load("FIELD_LAYER/field_decomposition/outputs/v9_5/orbit_entry_channels.npy")

# flow: (H, W, 2)
dx = flow[..., 0]
dy = flow[..., 1]

H, W = dx.shape

# === Mask channels ===
mask = channels > 0

# === Extract vectors ===
y_idx, x_idx = np.where(mask)

dx_c = dx[y_idx, x_idx]
dy_c = dy[y_idx, x_idx]

# === Normalize (optional, for clean viz) ===
mag = np.sqrt(dx_c**2 + dy_c**2) + 1e-8
dx_n = dx_c / mag
dy_n = dy_c / mag

# === Angle (for color mapping) ===
angles = np.arctan2(dy_n, dx_n)

# === Plot ===
plt.figure(figsize=(8, 8))
plt.imshow(mask, cmap="gray", alpha=0.3)

plt.quiver(
    x_idx,
    y_idx,
    dx_n,
    dy_n,
    angles,  # color by direction
    cmap="hsv",
    scale=50,
    width=0.003
)

plt.title("NEXAH V9.6 — Direction Field on Entry Channels")
plt.gca().invert_yaxis()
plt.colorbar(label="angle (rad)")
plt.tight_layout()

plt.savefig("FIELD_LAYER/field_decomposition/outputs/v9_6/direction_field.png")
print("✓ V9.6 done")
