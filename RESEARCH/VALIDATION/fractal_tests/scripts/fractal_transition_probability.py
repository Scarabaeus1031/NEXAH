import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "RESEARCH/VALIDATION/fractal_tests/scripts/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
# JULIA
# ================================
def julia(c, size=200, iterations=120):
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
# DELTA
# ================================
def compute_delta(j1, j2):
    return np.mean(np.abs(j1 - j2))


# ================================
# STRUCTURE METRIC
# ================================
def binary_structure(j, threshold=15):
    return j > threshold

def structural_change(a, b):
    return np.mean(a != b)


# ================================
# PEAK DETECTION
# ================================
def detect_peaks(deltas, factor=2.0):
    mean = np.mean(deltas)
    std = np.std(deltas)
    threshold = mean + factor * std
    peaks = [i for i, d in enumerate(deltas) if d > threshold]
    return peaks, threshold


# ================================
# RANDOM PATHS
# ================================
def random_path(steps):
    start = np.random.uniform(-1.5, 1.5) + 1j * np.random.uniform(-1.5, 1.5)
    end = np.random.uniform(-1.5, 1.5) + 1j * np.random.uniform(-1.5, 1.5)
    return np.linspace(start, end, steps)


# ================================
# MAIN EXPERIMENT
# ================================
runs = 30
steps = 80

delta_all = []
transition_flags = []

for run in range(runs):

    path = random_path(steps)

    deltas = []
    frames = []

    prev = None

    for c in path:
        j = julia(c)
        frames.append(j)

        if prev is not None:
            d = compute_delta(j, prev)
            deltas.append(d)
        else:
            deltas.append(0)

        prev = j

    deltas = np.array(deltas)
    peaks, threshold = detect_peaks(deltas)

    for p in peaks:
        if p < 2 or p > len(path) - 3:
            continue

        before = binary_structure(frames[p - 1])
        after = binary_structure(frames[p + 1])

        change = structural_change(before, after)

        delta_all.append(deltas[p])

        # Transition if persistent change
        if change > 0.15:
            transition_flags.append(1)
        else:
            transition_flags.append(0)


delta_all = np.array(delta_all)
transition_flags = np.array(transition_flags)


# ================================
# BINNING → PROBABILITY
# ================================
bins = np.linspace(min(delta_all), max(delta_all), 10)
bin_centers = 0.5 * (bins[:-1] + bins[1:])
probabilities = []

for i in range(len(bins)-1):
    mask = (delta_all >= bins[i]) & (delta_all < bins[i+1])

    if np.sum(mask) > 0:
        prob = np.mean(transition_flags[mask])
    else:
        prob = np.nan

    probabilities.append(prob)


# ================================
# PLOT
# ================================
plt.figure(figsize=(6,5))
plt.plot(bin_centers, probabilities, marker='o')
plt.xlabel("Δ")
plt.ylabel("P(transition)")
plt.title("Transition Probability vs Δ")
plt.grid()

plt.savefig(os.path.join(OUTPUT_DIR, "transition_probability_curve.png"), dpi=150)
plt.close()


# ================================
# RAW SCATTER
# ================================
plt.figure(figsize=(6,5))
plt.scatter(delta_all, transition_flags, alpha=0.5)
plt.xlabel("Δ")
plt.ylabel("Transition (0/1)")
plt.title("Raw Transition Data")
plt.grid()

plt.savefig(os.path.join(OUTPUT_DIR, "transition_scatter.png"), dpi=150)
plt.close()


# ================================
# PRINT SUMMARY
# ================================
print("Total peaks:", len(delta_all))
print("Transitions:", np.sum(transition_flags))
print("Transition rate:", np.mean(transition_flags))
