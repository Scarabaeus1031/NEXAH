import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
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

    return xs, ys

# ============================================================
# FIELD
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
# TRANSITIONS
# ============================================================

def detect_transitions(xs):
    return np.where(np.diff(np.sign(xs)) != 0)[0]

# ============================================================
# MAIN
# ============================================================

print("Running Experiment 3.3 (independent)")

xs, ys = simulate()

density = compute_density(xs, ys)
dx, dy = compute_flow(xs, ys)
rotation = compute_rotation(dx, dy)
coherence = compute_coherence(dx, dy)

G_values = compute_gate(density, coherence, rotation)
transition_indices = detect_transitions(xs)

# ============================================================
# DETECT PEAKS
# ============================================================

THRESHOLD = 0.7
WINDOW = 50

peaks, _ = find_peaks(G_values, height=THRESHOLD, distance=20)

# ============================================================
# MATCH EVENTS
# ============================================================

TP, FP, FN = [], [], []
used_transitions = set()

for p in peaks:
    match = False
    for t in transition_indices:
        if abs(p - t) < WINDOW:
            TP.append(p)
            used_transitions.add(int(t))
            match = True
            break
    if not match:
        FP.append(p)

for t in transition_indices:
    if int(t) not in used_transitions:
        FN.append(int(t))

# ============================================================
# METRICS
# ============================================================

precision = len(TP) / (len(TP) + len(FP) + 1e-9)
recall = len(TP) / (len(TP) + len(FN) + 1e-9)

print("\n---- Experiment 3.3 Results ----")
print(f"TP: {len(TP)}")
print(f"FP: {len(FP)}")
print(f"FN: {len(FN)}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(16, 5))

plt.plot(G_values, label="G(x)", alpha=0.8)

plt.scatter(TP, G_values[TP], color="green", label="TP")
plt.scatter(FP, G_values[FP], color="red", label="FP")
plt.scatter(FN, G_values[FN], color="orange", label="FN")

plt.scatter(
    transition_indices,
    G_values[transition_indices],
    color="black",
    label="Transitions",
    s=20
)

plt.axhline(THRESHOLD, linestyle="--")

plt.title("Experiment 3.3 — False Positive Analysis")
plt.xlabel("Time")
plt.ylabel("G(x)")
plt.legend()

plt.tight_layout()

plt.show()
