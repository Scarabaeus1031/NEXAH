"""
Symmetry Resonance Detector
===========================

Detects stability / resonance regions in symmetry-drift space.

Parameter space:
    x-axis  -> symmetry order n
    y-axis  -> angular drift

For each (n, drift), the script computes simple metrics:

- closure error
- radial variance
- angular spread

This produces a resonance map highlighting stable and unstable regions.
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Configuration
# --------------------------------------------------

radius = 5.0
iterations = 1800

n_values = list(range(3, 21))
drift_values = np.linspace(0.0, 6.0, 25)   # degrees

# breathing kept same as in previous demos
def radial_profile(k):
    return radius * (0.7 + 0.3 * np.cos(k * 0.02))


# --------------------------------------------------
# Pattern generator
# --------------------------------------------------

def generate_pattern(n, drift_deg):
    base_angle = 2 * np.pi / n
    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k * (base_angle + drift)
    r = radial_profile(k)

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return x, y, r, theta


# --------------------------------------------------
# Metrics
# --------------------------------------------------

def closure_error(x, y):
    """
    Distance between start and end point, normalized by radius.
    Lower = more closed / periodic.
    """
    dx = x[-1] - x[0]
    dy = y[-1] - y[0]
    return np.sqrt(dx * dx + dy * dy) / radius


def radial_variance(r):
    """
    Variation of radius.
    Lower = cleaner ring / polygon shell.
    """
    return np.std(r) / np.mean(r)


def angular_step_irregularity(theta):
    """
    Drift uniformity measure.
    Lower = more regular stepping.
    """
    dtheta = np.diff(np.unwrap(theta))
    return np.std(dtheta) / np.mean(np.abs(dtheta))


def resonance_score(x, y, r, theta):
    """
    Combined score:
    Higher = more resonant / structured / closed.
    """
    c = closure_error(x, y)
    rv = radial_variance(r)
    ai = angular_step_irregularity(theta)

    # invert penalties into score
    score = 1.0 / (1.0 + 3.0 * c + 1.5 * rv + 2.0 * ai)
    return score, c, rv, ai


# --------------------------------------------------
# Compute phase maps
# --------------------------------------------------

score_map = np.zeros((len(drift_values), len(n_values)))
closure_map = np.zeros_like(score_map)
radial_map = np.zeros_like(score_map)
angular_map = np.zeros_like(score_map)

for i, drift in enumerate(drift_values):
    for j, n in enumerate(n_values):
        x, y, r, theta = generate_pattern(n, drift)
        score, c, rv, ai = resonance_score(x, y, r, theta)

        score_map[i, j] = score
        closure_map[i, j] = c
        radial_map[i, j] = rv
        angular_map[i, j] = ai


# --------------------------------------------------
# Plot
# --------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

extent = [
    min(n_values) - 0.5,
    max(n_values) + 0.5,
    drift_values[0],
    drift_values[-1]
]

im0 = axes[0, 0].imshow(
    score_map,
    origin="lower",
    aspect="auto",
    extent=extent
)
axes[0, 0].set_title("Resonance Score")
axes[0, 0].set_xlabel("symmetry order n")
axes[0, 0].set_ylabel("drift (deg)")
plt.colorbar(im0, ax=axes[0, 0], fraction=0.046, pad=0.04)

im1 = axes[0, 1].imshow(
    closure_map,
    origin="lower",
    aspect="auto",
    extent=extent
)
axes[0, 1].set_title("Closure Error")
axes[0, 1].set_xlabel("symmetry order n")
axes[0, 1].set_ylabel("drift (deg)")
plt.colorbar(im1, ax=axes[0, 1], fraction=0.046, pad=0.04)

im2 = axes[1, 0].imshow(
    radial_map,
    origin="lower",
    aspect="auto",
    extent=extent
)
axes[1, 0].set_title("Radial Variance")
axes[1, 0].set_xlabel("symmetry order n")
axes[1, 0].set_ylabel("drift (deg)")
plt.colorbar(im2, ax=axes[1, 0], fraction=0.046, pad=0.04)

im3 = axes[1, 1].imshow(
    angular_map,
    origin="lower",
    aspect="auto",
    extent=extent
)
axes[1, 1].set_title("Angular Irregularity")
axes[1, 1].set_xlabel("symmetry order n")
axes[1, 1].set_ylabel("drift (deg)")
plt.colorbar(im3, ax=axes[1, 1], fraction=0.046, pad=0.04)

plt.suptitle("Symmetry Resonance Detector", fontsize=14)
plt.tight_layout()
plt.show()


# --------------------------------------------------
# Print top resonance candidates
# --------------------------------------------------

flat = []
for i, drift in enumerate(drift_values):
    for j, n in enumerate(n_values):
        flat.append((score_map[i, j], n, drift))

flat.sort(reverse=True)

print("\nTop resonance candidates:\n")
for score, n, drift in flat[:15]:
    print(f"n={n:2d}   drift={drift:4.2f}°   score={score:0.4f}")
