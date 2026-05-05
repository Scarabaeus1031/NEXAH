import numpy as np
import matplotlib.pyplot as plt
import os

# --- Setup Output Folder ---
OUTPUT_DIR = "RESEARCH/VALIDATION/fractal_tests/scripts/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Julia Set ---
def julia(c, size=200, iterations=100):
    x = np.linspace(-1.5, 1.5, size)
    y = np.linspace(-1.5, 1.5, size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    mask = np.zeros(Z.shape, dtype=int)

    for i in range(iterations):
        Z = Z**2 + c
        mask += (np.abs(Z) < 2)

    return mask

# --- Mandelbrot (für Overlay) ---
def mandelbrot(size=400, iterations=100):
    x = np.linspace(-2, 1, size)
    y = np.linspace(-1.5, 1.5, size)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)

    mask = np.zeros(C.shape, dtype=int)

    for i in range(iterations):
        Z = Z**2 + C
        mask += (np.abs(Z) < 2)

    return mask

# --- Kreis im Parameterraum ---
def generate_circle(center, radius, steps):
    angles = np.linspace(0, 2*np.pi, steps)
    return np.array([center + radius * np.exp(1j * a) for a in angles])

# --- Δ berechnen ---
def compute_delta(j1, j2):
    return np.mean(np.abs(j1 - j2))

# --- Peak Detection ---
def detect_peaks(deltas, threshold_factor=2.0):
    mean = np.mean(deltas)
    std = np.std(deltas)
    threshold = mean + threshold_factor * std

    peaks = [i for i, d in enumerate(deltas) if d > threshold]
    return peaks, threshold

# --- Setup ---
center = -0.75 + 0j
radius = 0.3
steps = 100

circle = generate_circle(center, radius, steps)

# --- Δ entlang Kreis ---
deltas = []
prev = None

for c in circle:
    j = julia(c)

    if prev is not None:
        d = compute_delta(j, prev)
        deltas.append(d)
    else:
        deltas.append(0)

    prev = j

deltas = np.array(deltas)

# --- Peaks finden ---
peaks, threshold = detect_peaks(deltas)

# --- Save Δ data ---
np.save(os.path.join(OUTPUT_DIR, "delta_values.npy"), deltas)

# --- Plot Δ ---
plt.figure(figsize=(10,4))
plt.plot(deltas, color='red', label="Δ")

# Threshold line
plt.axhline(threshold, color='blue', linestyle='--', label="Threshold")

# Peaks markieren
plt.scatter(peaks, deltas[peaks], color='black', label="Peaks")

plt.title("Δ entlang Kreis im Parameterraum")
plt.xlabel("Position auf Kreis")
plt.ylabel("Δ")
plt.legend()
plt.grid()

plt.savefig(os.path.join(OUTPUT_DIR, "delta_circle_plot.png"), dpi=150)
plt.close()

# --- Mandelbrot Overlay ---
mandel = mandelbrot()

plt.figure(figsize=(6,6))
plt.imshow(mandel, extent=(-2,1,-1.5,1.5), cmap='magma')

# Kreis plotten
plt.plot(circle.real, circle.imag, color='cyan', linewidth=2)

# Peak-Punkte markieren
peak_points = circle[peaks]
plt.scatter(peak_points.real, peak_points.imag, color='white', s=20)

plt.title("Mandelbrot + Kreis + Δ-Peaks")

plt.savefig(os.path.join(OUTPUT_DIR, "mandelbrot_peaks_overlay.png"), dpi=150)
plt.close()

print("Done. Outputs gespeichert in:", OUTPUT_DIR)
