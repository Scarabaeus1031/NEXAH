import numpy as np
import matplotlib.pyplot as plt

# =========================
# Load IEEE-like signal (or CSV)
# =========================

def generate_ieee_like_signal(T=120, dt=0.1):
    t = np.arange(0, T, dt)

    # typische Voltage Collapse Kurve
    midpoint = 73
    steepness = 0.18

    voltage = 1 / (1 + np.exp(steepness * (t - midpoint)))

    # kleines Messrauschen
    voltage += np.random.normal(0, 0.002, size=len(t))

    return t, voltage


# =========================
# Classical detection
# =========================

def classical_detection(voltage, t, threshold=0.7):
    idx = np.where(voltage < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


# =========================
# NEXAH Detection (v3.6.2)
# =========================

def nexah_detection(voltage, t):

    # derivatives
    dv = np.gradient(voltage)
    d2v = np.gradient(dv)

    # normalize (z-score)
    dv_z = (dv - np.mean(dv)) / (np.std(dv) + 1e-6)
    d2v_z = (d2v - np.mean(d2v)) / (np.std(d2v) + 1e-6)

    # composite score
    score = np.abs(dv_z) + 0.7 * np.abs(d2v_z)

    # smoothing
    window = 10
    score_smooth = np.convolve(score, np.ones(window)/window, mode='same')

    # adaptive threshold
    threshold = np.mean(score_smooth) + 1.2 * np.std(score_smooth)

    split_time = None

    for i in range(len(t)):

        condition_now = score_smooth[i] > threshold

        # 🔥 NEW: voltage gate (physikalische Phase)
        voltage_gate = voltage[i] < 0.95

        if condition_now and voltage_gate:
            split_time = t[i]
            break

    return split_time, score_smooth


# =========================
# Run experiment
# =========================

t, voltage = generate_ieee_like_signal()

classic = classical_detection(voltage, t)
split, score = nexah_detection(voltage, t)

lead = None
if split is not None and classic is not None:
    lead = classic - split

# =========================
# Output
# =========================

print("\nNEXAH v3.6.2 IEEE result")
print("------------------------")
print(f"split:   {split}")
print(f"classic: {classic}")
print(f"lead:    {lead}")

# =========================
# Plot
# =========================

plt.figure(figsize=(10,5))

plt.plot(t, voltage, label="voltage")

if split is not None:
    plt.axvline(split, color='green', label="split")

if classic is not None:
    plt.axvline(classic, color='red', label="classic")

plt.axhline(0.7, linestyle='--')

plt.title("NEXAH v3.6.2 – IEEE Detection (Phase-Gated)")
plt.xlabel("time")
plt.ylabel("voltage")
plt.legend()

plt.tight_layout()
plt.show()
