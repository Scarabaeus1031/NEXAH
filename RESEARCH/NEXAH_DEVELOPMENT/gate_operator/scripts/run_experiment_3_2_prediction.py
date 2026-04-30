import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# 1. SYSTEM (Lorenz)
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
# 2. FIELD CONSTRUCTION
# ============================================================

def compute_density(xs, ys):
    kde = gaussian_kde(np.vstack([xs, ys]))
    density = kde(np.vstack([xs, ys]))
    return density

def compute_flow(xs, ys):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    return dx, dy

def compute_rotation(dx, dy):
    # proxy rotation magnitude
    rot = np.abs(np.gradient(dx) - np.gradient(dy))
    return rot

def compute_coherence(dx, dy):
    mag = np.sqrt(dx**2 + dy**2) + 1e-8
    coherence = (dx/mag)**2 + (dy/mag)**2
    return coherence

def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-8)

# ============================================================
# 3. GATE OPERATOR
# ============================================================

def compute_gate(density, coherence, rotation):
    rho = normalize(density)
    C = normalize(coherence)
    R = normalize(rotation)

    G = (1 - rho) * (1 - C) * (1 - R)
    return normalize(G)

# ============================================================
# 4. TRANSITION DETECTION (LOBE SWITCH)
# ============================================================

def detect_transitions(xs):
    # Lorenz lobe switch via sign flip
    transitions = np.where(np.diff(np.sign(xs)) != 0)[0]
    return transitions

# ============================================================
# 5. PREDICTION TEST
# ============================================================

def prediction_test(G, transitions, window=50, threshold=0.8):
    hits = 0
    total = len(transitions)

    for t in transitions:
        start = max(0, t - window)
        if np.any(G[start:t] > threshold):
            hits += 1

    return hits, total, hits / total if total > 0 else 0

# ============================================================
# 6. MAIN
# ============================================================

xs, ys = simulate()

density = compute_density(xs, ys)
dx, dy = compute_flow(xs, ys)
rotation = compute_rotation(dx, dy)
coherence = compute_coherence(dx, dy)

G = compute_gate(density, coherence, rotation)
transitions = detect_transitions(xs)

# ============================================================
# 7. EVALUATION
# ============================================================

hits, total, accuracy = prediction_test(G, transitions)

print("\n=== EXPERIMENT 3.2 RESULTS ===")
print(f"Transitions detected: {total}")
print(f"Predicted (G spike before): {hits}")
print(f"Prediction accuracy: {accuracy:.3f}")

# ============================================================
# 8. VISUALIZATION
# ============================================================

plt.figure(figsize=(14, 5))

# G over time
plt.plot(G, label="G(x)", alpha=0.8)

# mark transitions
plt.scatter(transitions, G[transitions], color='red', label="Transitions")

# highlight pre-transition zones
for t in transitions:
    plt.axvspan(max(0, t-50), t, color='orange', alpha=0.1)

plt.title("Experiment 3.2 — Prediction Test (G(x) before transitions)")
plt.xlabel("Time")
plt.ylabel("G(x)")
plt.legend()

plt.tight_layout()

plt.savefig(
    "RESEARCH/NEXAH_DEVELOPMENT/gate_operator/output_results/experiment_3_2_prediction.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
