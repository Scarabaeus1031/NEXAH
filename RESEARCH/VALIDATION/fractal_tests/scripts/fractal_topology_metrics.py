import numpy as np
import matplotlib.pyplot as plt
import os
import csv

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
# PATH
# ================================
def generate_circle(center, radius, steps):
    angles = np.linspace(0, 2 * np.pi, steps)
    return np.array([center + radius * np.exp(1j * a) for a in angles])


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
# TOPOLOGY-LIKE METRICS
# ================================
def binary_structure(julia_mask, threshold=20):
    return julia_mask > threshold


def area_metric(binary):
    return np.sum(binary)


def density_metric(binary):
    return np.mean(binary)


def change_metric(a, b):
    return np.mean(a != b)


def intensity_metric(julia_mask):
    return np.mean(julia_mask)


# ================================
# LOAD DELTAS
# ================================
deltas = np.load(os.path.join(OUTPUT_DIR, "circle_deltas.npy"))

center = -0.75 + 0j
radius = 0.3
steps = len(deltas)

circle = generate_circle(center, radius, steps)
peaks, threshold = detect_peaks(deltas)

rows = []

# ================================
# ANALYZE EACH PEAK
# ================================
for peak_id, p in enumerate(peaks):

    if p <= 1 or p >= len(circle) - 2:
        continue

    c_before = circle[p - 1]
    c_peak = circle[p]
    c_after = circle[p + 1]

    j_before = julia(c_before)
    j_peak = julia(c_peak)
    j_after = julia(c_after)

    b_before = binary_structure(j_before)
    b_peak = binary_structure(j_peak)
    b_after = binary_structure(j_after)

    area_before = area_metric(b_before)
    area_peak = area_metric(b_peak)
    area_after = area_metric(b_after)

    density_before = density_metric(b_before)
    density_peak = density_metric(b_peak)
    density_after = density_metric(b_after)

    intensity_before = intensity_metric(j_before)
    intensity_peak = intensity_metric(j_peak)
    intensity_after = intensity_metric(j_after)

    change_before_peak = change_metric(b_before, b_peak)
    change_peak_after = change_metric(b_peak, b_after)
    change_before_after = change_metric(b_before, b_after)

    # Simple event classification
    if change_before_after > 0.25:
        event_type = "TYPE_I_PERSISTENT_TRANSITION"
    elif change_before_peak > 0.25 and change_peak_after > 0.25:
        event_type = "TYPE_II_TRANSIENT_GRAZING"
    else:
        event_type = "TYPE_III_WEAK_VARIATION"

    rows.append({
        "peak_id": peak_id,
        "peak_index": int(p),
        "delta": float(deltas[p]),
        "c_before": str(c_before),
        "c_peak": str(c_peak),
        "c_after": str(c_after),
        "area_before": int(area_before),
        "area_peak": int(area_peak),
        "area_after": int(area_after),
        "density_before": float(density_before),
        "density_peak": float(density_peak),
        "density_after": float(density_after),
        "intensity_before": float(intensity_before),
        "intensity_peak": float(intensity_peak),
        "intensity_after": float(intensity_after),
        "change_before_peak": float(change_before_peak),
        "change_peak_after": float(change_peak_after),
        "change_before_after": float(change_before_after),
        "event_type": event_type
    })


# ================================
# SAVE CSV
# ================================
csv_path = os.path.join(OUTPUT_DIR, "topology_metrics.csv")

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)


# ================================
# VISUAL 1: CHANGE METRICS
# ================================
peak_indices = [r["peak_index"] for r in rows]
delta_values = [r["delta"] for r in rows]
change_bp = [r["change_before_peak"] for r in rows]
change_pa = [r["change_peak_after"] for r in rows]
change_ba = [r["change_before_after"] for r in rows]

plt.figure(figsize=(10, 5))
plt.plot(peak_indices, change_bp, marker="o", label="before → peak")
plt.plot(peak_indices, change_pa, marker="o", label="peak → after")
plt.plot(peak_indices, change_ba, marker="o", label="before → after")
plt.title("Topology Change Metrics at Δ Peaks")
plt.xlabel("Peak index along path")
plt.ylabel("Binary structure change")
plt.grid()
plt.legend()
plt.savefig(os.path.join(OUTPUT_DIR, "topology_change_metrics.png"), dpi=150)
plt.close()


# ================================
# VISUAL 2: AREA CHANGE
# ================================
area_before = [r["area_before"] for r in rows]
area_peak = [r["area_peak"] for r in rows]
area_after = [r["area_after"] for r in rows]

plt.figure(figsize=(10, 5))
plt.plot(peak_indices, area_before, marker="o", label="before")
plt.plot(peak_indices, area_peak, marker="o", label="peak")
plt.plot(peak_indices, area_after, marker="o", label="after")
plt.title("Julia Structure Area Around Δ Peaks")
plt.xlabel("Peak index along path")
plt.ylabel("Area above threshold")
plt.grid()
plt.legend()
plt.savefig(os.path.join(OUTPUT_DIR, "topology_area_metrics.png"), dpi=150)
plt.close()


# ================================
# VISUAL 3: Δ VS TOPOLOGY CHANGE
# ================================
plt.figure(figsize=(6, 5))
plt.scatter(delta_values, change_ba)
plt.title("Δ vs Persistent Topology Change")
plt.xlabel("Δ peak value")
plt.ylabel("before → after structural change")
plt.grid()
plt.savefig(os.path.join(OUTPUT_DIR, "delta_vs_topology_change.png"), dpi=150)
plt.close()


# ================================
# PRINT SUMMARY
# ================================
print("Topology metrics complete.")
print("Saved:", csv_path)

print("\nEvent classification:")
for r in rows:
    print(
        f"Peak {r['peak_index']}: "
        f"Δ={r['delta']:.3f} | "
        f"before-after change={r['change_before_after']:.3f} | "
        f"{r['event_type']}"
    )
