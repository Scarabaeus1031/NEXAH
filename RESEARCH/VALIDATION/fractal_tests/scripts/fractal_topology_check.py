import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "RESEARCH/VALIDATION/fractal_tests/scripts/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
# JULIA
# ================================
def julia(c, size=300, iterations=150):
    x = np.linspace(-1.5, 1.5, size)
    y = np.linspace(-1.5, 1.5, size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    mask = np.zeros(Z.shape, dtype=int)

    for i in range(iterations):
        active = np.abs(Z) < 2
        Z[active] = Z[active]**2 + c
        mask += active

    return mask

# ================================
# LOAD DATA
# ================================
deltas = np.load(os.path.join(OUTPUT_DIR, "circle_deltas.npy"))

# recreate circle (same params as before)
def generate_circle(center, radius, steps):
    angles = np.linspace(0, 2*np.pi, steps)
    return np.array([center + radius * np.exp(1j * a) for a in angles])

center = -0.75 + 0j
radius = 0.3
steps = len(deltas)

circle = generate_circle(center, radius, steps)

# ================================
# PEAK DETECTION (same logic)
# ================================
def detect_peaks(deltas, threshold_factor=2.0):
    mean = np.mean(deltas)
    std = np.std(deltas)
    threshold = mean + threshold_factor * std
    peaks = [i for i, d in enumerate(deltas) if d > threshold]
    return peaks

peaks = detect_peaks(deltas)

# ================================
# TOPOLOGY CHECK
# ================================
for idx, p in enumerate(peaks):

    if p <= 1 or p >= len(circle)-2:
        continue

    c_before = circle[p-1]
    c_peak   = circle[p]
    c_after  = circle[p+1]

    j_before = julia(c_before)
    j_peak   = julia(c_peak)
    j_after  = julia(c_after)

    # --- Plot ---
    fig, axes = plt.subplots(1,3, figsize=(12,4))

    axes[0].imshow(j_before, cmap='magma')
    axes[0].set_title("before")

    axes[1].imshow(j_peak, cmap='magma')
    axes[1].set_title("peak")

    axes[2].imshow(j_after, cmap='magma')
    axes[2].set_title("after")

    for ax in axes:
        ax.axis('off')

    plt.suptitle(f"Topology Check — Peak {p}")

    plt.savefig(
        os.path.join(OUTPUT_DIR, f"topology_peak_{idx}.png"),
        dpi=150
    )
    plt.close()

print("Topology check complete.")
