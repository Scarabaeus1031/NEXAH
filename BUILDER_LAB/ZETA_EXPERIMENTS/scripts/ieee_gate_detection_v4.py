import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. SIGNAL GENERATION
# =========================
def generate_signal(t):
    x = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < 30:
            x[i] = 0.3 * np.sin(0.5 * ti)

        elif ti < 75:
            amp = 0.5 + 0.01 * (ti - 30)
            x[i] = amp * np.sin(1.2 * ti)

        else:
            # decoherence regime
            x[i] = np.random.normal(0, 1.0)

    return x


# =========================
# 2. COHERENCE (multi-lag)
# =========================
def compute_coherence(x, window=20):
    C = np.full_like(x, np.nan, dtype=float)

    for i in range(window, len(x)):
        segment = x[i - window:i]
        lags = [1, 2, 3, 5]

        vals = []
        for lag in lags:
            if len(segment) > lag:
                c = np.corrcoef(segment[:-lag], segment[lag:])[0, 1]
                if not np.isnan(c):
                    vals.append(c)

        if vals:
            C[i] = np.mean(vals)

    return C


# =========================
# 3. GATE DETECTION
# =========================
def detect_gates(C, threshold=0.3, min_duration=10):
    mask = C < threshold

    gates = []
    start = None

    for i, val in enumerate(mask):
        if val and start is None:
            start = i
        elif not val and start is not None:
            if i - start >= min_duration:
                gates.append((start, i))
            start = None

    return gates


# =========================
# 4. PRECURSOR (improved)
# =========================
def detect_precursor(C, drop_threshold=0.05, window=10):
    for i in range(window, len(C)):
        segment = C[i - window:i]
        if np.nanmean(np.diff(segment)) < -drop_threshold:
            return i
    return None


# =========================
# 5. MAIN
# =========================
t = np.linspace(0, 100, 1000)
x = generate_signal(t)

C = compute_coherence(x)
gates = detect_gates(C)
precursor_idx = detect_precursor(C)

# =========================
# 6. DERIVED VIEWS
# =========================

# Phase space
dx = np.gradient(x)

# Polar mapping
r = np.abs(x)
theta = np.unwrap(np.angle(x + 1j * dx))

# Spectrum
freq = np.fft.fftfreq(len(x), d=t[1] - t[0])
Xf = np.abs(np.fft.fft(x))

# =========================
# 7. PLOTTING
# =========================
fig = plt.figure(figsize=(18, 10))

# ---- 1. SIGNAL ----
ax1 = plt.subplot(3, 2, 1)
ax1.plot(t, x)
ax1.set_title("System Dynamics x(t)")

# ---- 2. COHERENCE ----
ax2 = plt.subplot(3, 2, 3)
ax2.plot(t, C)
ax2.axhline(0.3, linestyle="--", label="threshold")
if precursor_idx:
    ax2.axvline(t[precursor_idx], color="orange", label="precursor")

for s, e in gates:
    ax2.axvspan(t[s], t[e], alpha=0.2)

ax2.set_title("Coherence C(t)")
ax2.legend()

# ---- 3. GATES ----
ax3 = plt.subplot(3, 2, 5)
for s, e in gates:
    ax3.axvspan(t[s], t[e], alpha=0.5)

ax3.set_title("Gate Detection")

# ---- 4. PHASE SPACE ----
ax4 = plt.subplot(3, 2, 2)
ax4.plot(x, dx, alpha=0.7)
ax4.set_title("Phase Space (x vs dx/dt)")

# ---- 5. POLAR ----
ax5 = plt.subplot(3, 2, 4, projection="polar")
ax5.plot(theta, r, alpha=0.7)
ax5.set_title("Polar Mapping")

# ---- 6. SPECTRUM ----
ax6 = plt.subplot(3, 2, 6)
ax6.plot(np.abs(freq), Xf)
ax6.set_yscale("log")
ax6.set_title("Frequency Spectrum")

plt.tight_layout()

# =========================
# 8. SAVE
# =========================
out_path = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v4.png"
plt.savefig(out_path)

print("\n--- NEXAH IEEE Gate Detection v4 ---")
print(f"Detected gates: {len(gates)}")
if precursor_idx:
    print(f"Precursor at t ≈ {t[precursor_idx]:.2f}")

print(f"Saved to: {out_path}")

plt.show()
