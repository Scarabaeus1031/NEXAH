# FIELD_LAYER/field_decomposition/scripts/v8_6_decision_structure_map.py

"""
NEXAH V8.6 — Decision Structure Map

Goal:
→ combine Delay, Lyapunov, and Entropy
→ detect true decision regions

Robust version:
→ handles missing filenames
→ auto-resizes inputs
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v8_6")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# HELPER: flexible loader
# ============================================================

def load_first_existing(path_list):
    for p in path_list:
        if os.path.exists(p):
            print("✓ loading:", p)
            return np.load(p)
    raise FileNotFoundError(f"None of these found: {path_list}")

# ============================================================
# LOAD DATA (robust)
# ============================================================

delay = load_first_existing([
    os.path.join(BASE, "v8_2", "decision_delay.npy"),
    os.path.join(BASE, "v8_2", "delay_map.npy"),
])

entropy = load_first_existing([
    os.path.join(BASE, "v8_5", "entropy_map.npy"),
])

lyap = load_first_existing([
    os.path.join(BASE, "v8_3", "lyapunov_map_resampled.npy"),
    os.path.join(BASE, "v8_3", "lyapunov_map.npy"),
])

# ============================================================
# RESIZE
# ============================================================

target_shape = delay.shape

def match_shape(A):
    if A.shape != target_shape:
        zoom_factors = (
            target_shape[0] / A.shape[0],
            target_shape[1] / A.shape[1]
        )
        print("↻ resizing:", A.shape, "→", target_shape)
        return zoom(A, zoom_factors, order=1)
    return A

entropy = match_shape(entropy)
lyap = match_shape(lyap)

# ============================================================
# NORMALIZATION
# ============================================================

def normalize(A):
    A = A - np.min(A)
    return A / (np.max(A) + 1e-8)

delay_n = normalize(delay)
entropy_n = normalize(entropy)
lyap_n = normalize(lyap)

# invert Lyapunov → instability
instability = 1 - lyap_n

# ============================================================
# COMBINATION
# ============================================================

decision_map = delay_n * entropy_n * instability

print("✓ decision_map stats:")
print("min:", decision_map.min())
print("max:", decision_map.max())
print("mean:", decision_map.mean())

# ============================================================
# GRID
# ============================================================

ny, nx = decision_map.shape
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

plt.contourf(X, Y, decision_map, levels=50, cmap="magma")

plt.colorbar(label="Decision Strength")

plt.title("NEXAH V8.6 — Decision Structure Map")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_6_decision_structure.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "decision_structure.npy"), decision_map)

print("✓ V8.6 done →", OUTDIR)
