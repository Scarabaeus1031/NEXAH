import numpy as np
import matplotlib.pyplot as plt
import os

# ================================
# OUTPUT SETUP
# ================================
OUTPUT_DIR = "RESEARCH/VALIDATION/fractal_tests/scripts/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
# JULIA (stabiler)
# ================================
def julia(c, size=200, iterations=100):
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
# MANDELBROT
# ================================
def mandelbrot(size=400, iterations=100):
    x = np.linspace(-2, 1, size)
    y = np.linspace(-1.5, 1.5, size)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)

    mask = np.zeros(C.shape, dtype=int)

    for i in range(iterations):
        active = np.abs(Z) < 2
        Z[active] = Z[active]**2 + C[active]
        mask += active

    return mask

# ================================
# PATHS
# ================================
def generate_circle(center, radius, steps):
    angles = np.linspace(0, 2*np.pi, steps)
    return np.array([center + radius * np.exp(1j * a) for a in angles])

def generate_random_path(start, steps, scale=0.05):
    path = [start]
    for _ in range(steps - 1):
        step = scale * (np.random.randn() + 1j*np.random.randn())
        path.append(path[-1] + step)
    return np.array(path)

# ================================
# DELTA
# ================================
def compute_delta(j1, j2):
    return np.mean(np.abs(j1 - j2))

# ================================
# PEAK DETECTION
# ================================
def detect_peaks(deltas, threshold_factor=2.0):
    mean = np.mean(deltas)
    std = np.std(deltas)
    threshold = mean + threshold_factor * std

    peaks = np.array([i for i, d in enumerate(deltas) if d > threshold])
    return peaks, threshold

# ================================
# SIGMOID (für später)
# ================================
def sigmoid(x, k=5, tau=2.0):
    return 1 / (1 + np.exp(-k * (x - tau)))

# ================================
# CORE RUN FUNCTION
# ================================
def run_path_experiment(path, label="run"):
    deltas = []
    prev = None

    for c in path:
        j = julia(c)

        if prev is not None:
            d = compute_delta(j, prev)
            deltas.append(d)
        else:
            deltas.append(0)

        prev = j

    deltas = np.array(deltas)
    peaks, threshold = detect_peaks(deltas)

    # Save raw data
    np.save(os.path.join(OUTPUT_DIR, f"{label}_deltas.npy"), deltas)

    return deltas, peaks, threshold

# ================================
# RUN MULTIPLE EXPERIMENTS
# ================================
center = -0.75 + 0j
steps = 100

# Circle
circle = generate_circle(center, radius=0.3, steps=steps)
circle_deltas, circle_peaks, circle_thresh = run_path_experiment(circle, "circle")

# Random Runs
random_runs = []
for i in range(5):
    path = generate_random_path(center, steps)
    d, p, t = run_path_experiment(path, f"random_{i}")
    random_runs.append((d, p, t))

# ================================
# PLOT 1: Circle Δ
# ================================
plt.figure(figsize=(10,4))
plt.plot(circle_deltas, color='red', label="Δ (circle)")
plt.axhline(circle_thresh, color='blue', linestyle='--', label="Threshold")
plt.scatter(circle_peaks, circle_deltas[circle_peaks], color='black', label="Peaks")
plt.legend()
plt.title("Δ entlang Kreis")
plt.grid()
plt.savefig(os.path.join(OUTPUT_DIR, "circle_delta.png"), dpi=150)
plt.close()

# ================================
# PLOT 2: Random Runs Overlay
# ================================
plt.figure(figsize=(10,4))

for i, (d, _, _) in enumerate(random_runs):
    plt.plot(d, alpha=0.6, label=f"run {i}")

plt.title("Δ Random Paths")
plt.grid()
plt.legend()
plt.savefig(os.path.join(OUTPUT_DIR, "random_delta_overlay.png"), dpi=150)
plt.close()

# ================================
# PLOT 3: Mandelbrot Overlay (circle)
# ================================
mandel = mandelbrot()

plt.figure(figsize=(6,6))
plt.imshow(mandel, extent=(-2,1,-1.5,1.5), cmap='magma')

plt.plot(circle.real, circle.imag, color='cyan')
plt.scatter(circle[circle_peaks].real, circle[circle_peaks].imag,
            color='white', s=20)

plt.title("Mandelbrot + Δ Peaks")
plt.savefig(os.path.join(OUTPUT_DIR, "mandelbrot_overlay_circle.png"), dpi=150)
plt.close()

# ================================
# PLOT 4: Δ → Probability
# ================================
x = np.linspace(0, np.max(circle_deltas), 200)
y = sigmoid(x, k=3, tau=np.mean(circle_deltas))

plt.figure(figsize=(6,4))
plt.plot(x, y)
plt.title("P(transition) = sigmoid(Δ)")
plt.xlabel("Δ")
plt.ylabel("Probability")
plt.grid()
plt.savefig(os.path.join(OUTPUT_DIR, "delta_probability_curve.png"), dpi=150)
plt.close()

print("DONE — extended validation complete.")
