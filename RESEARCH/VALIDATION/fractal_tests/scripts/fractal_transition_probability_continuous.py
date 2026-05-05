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
# CONTINUOUS DISTANCE
# ================================
def mandelbrot_distance(c, max_iter=100):
    z = 0
    for n in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            # continuous smoothing
            return n + 1 - np.log(np.log(abs(z))) / np.log(2)
    return -1  # inside (negative region)


# ================================
# METRICS
# ================================
def compute_delta(j1, j2):
    return np.mean(np.abs(j1 - j2))

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
    return [i for i, d in enumerate(deltas) if d > threshold]


# ================================
# RANDOM PATH
# ================================
def random_path(steps):
    start = np.random.uniform(-1.5, 1.5) + 1j*np.random.uniform(-1.5, 1.5)
    end   = np.random.uniform(-1.5, 1.5) + 1j*np.random.uniform(-1.5, 1.5)
    return np.linspace(start, end, steps)


# ================================
# MAIN EXPERIMENT
# ================================
runs = 60
steps = 80

delta_list = []
distance_list = []
transition_list = []

for run in range(runs):

    path = random_path(steps)

    frames = []
    deltas = []
    prev = None

    for c in path:
        j = julia(c)
        frames.append(j)

        if prev is not None:
            deltas.append(compute_delta(j, prev))
        else:
            deltas.append(0)

        prev = j

    deltas = np.array(deltas)
    peaks = detect_peaks(deltas)

    for p in peaks:
        if p < 2 or p > len(path)-3:
            continue

        c = path[p]
        dist = mandelbrot_distance(c)

        before = binary_structure(frames[p-1])
        after  = binary_structure(frames[p+1])

        change = structural_change(before, after)

        delta_list.append(deltas[p])
        distance_list.append(dist)

        transition_list.append(1 if change > 0.15 else 0)


delta_arr = np.array(delta_list)
distance_arr = np.array(distance_list)
transition_arr = np.array(transition_list)

# ================================
# SCATTER
# ================================
plt.figure(figsize=(7,6))

colors = ["red" if t==1 else "blue" for t in transition_arr]

plt.scatter(delta_arr, distance_arr, c=colors, alpha=0.6)

plt.xlabel("Δ")
plt.ylabel("continuous distance")
plt.title("Transition Map (Δ vs Continuous Distance)")
plt.grid()

plt.savefig(os.path.join(OUTPUT_DIR, "transition_map_continuous.png"), dpi=150)
plt.close()


# ================================
# HEATMAP
# ================================
bins_x = np.linspace(min(delta_arr), max(delta_arr), 15)
bins_y = np.linspace(min(distance_arr), max(distance_arr), 15)

heat = np.zeros((len(bins_x)-1, len(bins_y)-1))
count = np.zeros_like(heat)

for d, dist, t in zip(delta_arr, distance_arr, transition_arr):
    ix = np.searchsorted(bins_x, d) - 1
    iy = np.searchsorted(bins_y, dist) - 1

    if 0 <= ix < heat.shape[0] and 0 <= iy < heat.shape[1]:
        heat[ix, iy] += t
        count[ix, iy] += 1

prob = np.divide(heat, count, where=count>0)

plt.figure(figsize=(7,6))
plt.imshow(prob.T, origin='lower', aspect='auto',
           extent=[bins_x[0], bins_x[-1], bins_y[0], bins_y[-1]])

plt.colorbar(label="P(transition)")
plt.xlabel("Δ")
plt.ylabel("continuous distance")
plt.title("Transition Probability Field (Smoothed)")

plt.savefig(os.path.join(OUTPUT_DIR, "transition_heatmap_continuous.png"), dpi=150)
plt.close()


# ================================
# SUMMARY
# ================================
print("Samples:", len(delta_arr))
print("Transitions:", np.sum(transition_arr))
print("Rate:", np.mean(transition_arr))
