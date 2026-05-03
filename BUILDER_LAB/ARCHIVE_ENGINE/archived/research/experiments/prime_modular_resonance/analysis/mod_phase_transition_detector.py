import numpy as np
import matplotlib.pyplot as plt

# =========================
# INPUT (paste your results)
# =========================

mods = np.array([7,11,13,17,19,23,29,31,37,41,43,47])

z_gap   = np.array([-18.40, -28.45, -33.92, -47.72, -45.23, -55.18, -60.99, -70.80])
z_drift = np.array([26.06, 6.16, 9.48, 2.23, 4.53, 3.87, 0.22, 2.35])
z_stat  = np.array([29.89,14.76,13.55,10.17,7.89,7.61,3.88,4.23])

# =========================
# DERIVATIVES (gradient)
# =========================

def compute_gradients(values):
    return np.gradient(values, mods)

grad_gap   = compute_gradients(z_gap)
grad_drift = compute_gradients(z_drift)
grad_stat  = compute_gradients(z_stat)

# =========================
# CHANGE POINT DETECTION
# =========================

def detect_phase_transitions(signal, threshold=0.5):
    transitions = []
    for i in range(1, len(signal)):
        delta = abs(signal[i] - signal[i-1])
        if delta > threshold:
            transitions.append((mods[i-1], mods[i], delta))
    return transitions

trans_gap   = detect_phase_transitions(grad_gap, threshold=0.5)
trans_drift = detect_phase_transitions(grad_drift, threshold=0.5)
trans_stat  = detect_phase_transitions(grad_stat, threshold=0.5)

# =========================
# DRIFT COLLAPSE DETECTION
# =========================

def detect_drift_collapse(z_drift, threshold=1.0):
    collapse_points = []
    for m, val in zip(mods, z_drift):
        if abs(val) < threshold:
            collapse_points.append((m, val))
    return collapse_points

drift_collapse = detect_drift_collapse(z_drift)

# =========================
# OUTPUT
# =========================

print("\n=== PHASE TRANSITIONS ===")

print("\nZ-gap transitions:")
for t in trans_gap:
    print(f"{t[0]} → {t[1]}  Δ={t[2]:.2f}")

print("\nZ-drift transitions:")
for t in trans_drift:
    print(f"{t[0]} → {t[1]}  Δ={t[2]:.2f}")

print("\nZ-stat transitions:")
for t in trans_stat:
    print(f"{t[0]} → {t[1]}  Δ={t[2]:.2f}")

print("\n=== DRIFT COLLAPSE POINTS ===")
for m, val in drift_collapse:
    print(f"mod {m}  (Z-drift ≈ {val:.2f})")

# =========================
# VISUALIZATION
# =========================

plt.figure(figsize=(10,6))

plt.plot(mods, z_gap, 'o-', label='Z-gap')
plt.plot(mods, z_drift, 'o-', label='Z-drift')
plt.plot(mods, z_stat, 'o-', label='Z-stat')

# highlight collapse
for m, val in drift_collapse:
    plt.scatter(m, val, s=120, marker='x', label=f'collapse @ {m}')

plt.axhline(0, linestyle='--')
plt.title("Phase Transition Detection")
plt.xlabel("Modulus")
plt.ylabel("Z-score")
plt.legend()
plt.grid()

plt.savefig("output/plots/phase_transition_detection.png")
plt.show()

# =========================
# SUMMARY INTERPRETATION
# =========================

print("\n=== INTERPRETATION ===")

print("""
Detected structure:

1. Strong structural regime (low mod)
   → high drift, high stat deviation

2. Transition regime (mid mod)
   → gradients fluctuate

3. Drift collapse regime (high mod)
   → drift → 0, gap persists

Key insight:
→ system shifts from transport-dominated → structure-dominated
""")
