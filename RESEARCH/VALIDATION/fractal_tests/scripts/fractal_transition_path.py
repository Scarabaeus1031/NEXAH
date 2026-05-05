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
# DELTA
# ================================
def compute_delta(j1, j2):
    return np.mean(np.abs(j1 - j2))


# ================================
# TRANSITION PATH
# ================================
def generate_transition_path(start, end, steps):
    return np.linspace(start, end, steps)


# ================================
# SETUP
# ================================
steps = 120

# Inside Mandelbrot
start = -0.75 + 0.0j

# Outside (escape region)
end = 0.4 + 0.6j

path = generate_transition_path(start, end, steps)

# ================================
# RUN Δ
# ================================
deltas = []
julia_frames = []

prev = None

for c in path:
    j = julia(c)
    julia_frames.append(j)

    if prev is not None:
        d = compute_delta(j, prev)
        deltas.append(d)
    else:
        deltas.append(0)

    prev = j

deltas = np.array(deltas)

# ================================
# SAVE DATA
# ================================
np.save(os.path.join(OUTPUT_DIR, "transition_deltas.npy"), deltas)

# ================================
# PLOT Δ
# ================================
plt.figure(figsize=(10,4))
plt.plot(deltas, color='red')
plt.title("Δ along Transition Path (inside → outside)")
plt.xlabel("Path index")
plt.ylabel("Δ")
plt.grid()

plt.savefig(os.path.join(OUTPUT_DIR, "transition_delta_plot.png"), dpi=150)
plt.close()

# ================================
# FIND MAX Δ (critical point)
# ================================
peak_idx = np.argmax(deltas)

# ================================
# TOPOLOGY SNAPSHOT
# ================================
indices = [
    max(0, peak_idx - 5),
    peak_idx,
    min(len(path)-1, peak_idx + 5)
]

labels = ["before", "transition", "after"]

fig, axes = plt.subplots(1,3, figsize=(12,4))

for i, idx in enumerate(indices):
    axes[i].imshow(julia_frames[idx], cmap='magma')
    axes[i].set_title(labels[i])
    axes[i].axis('off')

plt.suptitle("Forced Transition (Type IV Candidate)")

plt.savefig(os.path.join(OUTPUT_DIR, "transition_topology.png"), dpi=150)
plt.close()

# ================================
# AREA TRACKING
# ================================
def area(mask, threshold=20):
    return np.sum(mask > threshold)

areas = [area(j) for j in julia_frames]

plt.figure(figsize=(10,4))
plt.plot(areas, color='blue')
plt.title("Julia Area along Transition Path")
plt.xlabel("Path index")
plt.ylabel("Area")
plt.grid()

plt.savefig(os.path.join(OUTPUT_DIR, "transition_area_plot.png"), dpi=150)
plt.close()

print("Transition path experiment complete.")
print("Peak index:", peak_idx)
