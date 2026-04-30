import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEM (Lorenz)
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate(steps=8000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys, zs

# ============================================================
# FIELD COMPONENTS
# ============================================================

def compute_density(xs, ys):
    kde = gaussian_kde(np.vstack([xs, ys]))
    return kde(np.vstack([xs, ys]))

def compute_flow(xs, ys):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    return dx, dy

def compute_rotation(dx, dy):
    return np.abs(np.gradient(dx) - np.gradient(dy))

def compute_coherence(dx, dy):
    mag = np.sqrt(dx**2 + dy**2) + 1e-8
    return (dx/mag)**2 + (dy/mag)**2

def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-8)

def compute_gate(density, coherence, rotation):
    rho = normalize(density)
    C = normalize(coherence)
    R = normalize(rotation)
    return normalize((1 - rho) * (1 - C) * (1 - R))

# ============================================================
# SHEET DETECTION (simple radial clustering)
# ============================================================

def compute_sheets(xs, ys, num_sheets=6):
    r = np.sqrt(xs**2 + ys**2)
    bins = np.linspace(r.min(), r.max(), num_sheets + 1)
    sheet_idx = np.digitize(r, bins) - 1
    return sheet_idx

def detect_sheet_transitions(sheets):
    transitions = np.zeros(len(sheets), dtype=bool)
    transitions[1:] = sheets[1:] != sheets[:-1]
    return transitions

# ============================================================
# MAIN
# ============================================================

print("Running Experiment 3.4 — Sheet-Aware Gate")

xs, ys, zs = simulate()

density = compute_density(xs, ys)
dx, dy = compute_flow(xs, ys)
rotation = compute_rotation(dx, dy)
coherence = compute_coherence(dx, dy)

G = compute_gate(density, coherence, rotation)

sheets = compute_sheets(xs, ys)
sheet_transitions = detect_sheet_transitions(sheets)

THRESHOLD = 0.7
gate_active = G > THRESHOLD

# Sheet-aware transition condition
combined = sheet_transitions & gate_active

# ============================================================
# METRICS
# ============================================================

total_transitions = np.sum(sheet_transitions)
detected = np.sum(combined)

print("\n--- Results ---")
print(f"Total sheet transitions: {total_transitions}")
print(f"Detected (sheet + gate): {detected}")
print(f"Detection ratio: {detected / (total_transitions + 1e-9):.3f}")

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(16,5))

plt.plot(G, label="G(x)", alpha=0.7)

plt.scatter(np.where(sheet_transitions)[0], G[sheet_transitions],
            color="black", label="Sheet transitions")

plt.scatter(np.where(combined)[0], G[combined],
            color="green", label="Detected (Sheet + Gate)")

plt.axhline(THRESHOLD, linestyle="--")

plt.legend()
plt.title("Experiment 3.4 — Sheet-Aware Gate Detection")

plt.tight_layout()
plt.show()
