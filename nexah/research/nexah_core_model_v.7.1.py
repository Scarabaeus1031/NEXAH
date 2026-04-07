import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude

# === INPUT ===
# basin_map: (N x N) attractor IDs
# divergence: (N x N)
# speed: (N x N)

# 1. Basin Gradient
basin_grad = gaussian_gradient_magnitude(basin_map.astype(float), sigma=1.0)

# 2. Divergence Gradient
div_grad = gaussian_gradient_magnitude(divergence, sigma=1.0)

# 3. Speed Gradient (optional)
speed_grad = gaussian_gradient_magnitude(speed, sigma=1.0)

# === Combine ===
separatrix_strength = (
    0.5 * basin_grad +
    0.3 * div_grad +
    0.2 * speed_grad
)

# Normalize
sep = (separatrix_strength - separatrix_strength.min()) / (
    separatrix_strength.max() - separatrix_strength.min()
)

# Threshold → Separatrix mask
threshold = 0.4
sep_mask = sep > threshold

# === Plot ===
plt.figure(figsize=(6,6))
plt.imshow(sep, cmap='inferno')
plt.contour(sep_mask, colors='cyan', linewidths=0.5)
plt.title("NEXAH v7.1 — Separatrix Map")
plt.colorbar(label="boundary strength")
plt.show()
