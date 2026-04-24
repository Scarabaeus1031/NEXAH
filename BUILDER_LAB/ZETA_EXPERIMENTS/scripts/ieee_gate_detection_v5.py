import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import entropy

np.random.seed(42)

# --------------------------------------------------
# 1. SIGNAL GENERATION (clear regimes)
# --------------------------------------------------
def generate_signal(t):
    x = np.zeros_like(t)

    for i, ti in enumerate(t):

        if ti < 30:
            # stable
            x[i] = 0.3 * np.sin(0.5 * ti)

        elif ti < 75:
            # oscillatory structured
            x[i] = (1 + 0.02 * ti) * np.sin(1.5 * ti)

        else:
            # chaotic / decoherence
            x[i] = np.random.normal(0, 1.0)

    return x


# --------------------------------------------------
# 2. COHERENCE (multi-lag autocorrelation)
# --------------------------------------------------
def coherence(signal, window=20, max_lag=5):
    C = np.zeros(len(signal))

    for i in range(window, len(signal)):
        segment = signal[i-window:i]

        corrs = []
        for lag in range(1, max_lag+1):
            s1 = segment[:-lag]
            s2 = segment[lag:]

            if np.std(s1) > 0 and np.std(s2) > 0:
                corr = np.corrcoef(s1, s2)[0, 1]
                corrs.append(abs(corr))

        if len(corrs) > 0:
            C[i] = np.mean(corrs)
        else:
            C[i] = 0

    return C


# --------------------------------------------------
# 3. SPECTRAL ENTROPY (structure vs noise)
# --------------------------------------------------
def spectral_entropy(signal, fs=1.0, window=40):
    S = np.zeros(len(signal))

    for i in range(window, len(signal)):
        segment = signal[i-window:i]

        f, Pxx = welch(segment, fs=fs, nperseg=len(segment))
        Pxx = Pxx + 1e-12
        Pxx_norm = Pxx / np.sum(Pxx)

        S[i] = entropy(Pxx_norm)

    return S


# --------------------------------------------------
# 4. ADAPTIVE THRESHOLDS
# --------------------------------------------------
def adaptive_thresholds(C, S):
    C_thr = np.percentile(C[np.nonzero(C)], 20)   # low coherence
    S_thr = np.percentile(S[np.nonzero(S)], 80)   # high entropy
    return C_thr, S_thr


# --------------------------------------------------
# 5. GATE DETECTION (combined condition)
# --------------------------------------------------
def detect_gates(C, S, C_thr, S_thr, min_duration=5):

    mask = (C < C_thr) & (S > S_thr)

    gates = []
    active = False
    start = 0

    for i, m in enumerate(mask):

        if m and not active:
            active = True
            start = i

        elif not m and active:
            if i - start >= min_duration:
                gates.append((start, i))
            active = False

    if active:
        gates.append((start, len(mask)))

    return gates, mask


# --------------------------------------------------
# 6. PRECURSOR (early instability)
# --------------------------------------------------
def detect_precursor(C):
    dC = np.gradient(C)
    idx = np.where(dC < -0.05)[0]

    if len(idx) > 0:
        return idx[0]
    return None


# --------------------------------------------------
# 7. RUN EXPERIMENT
# --------------------------------------------------
t = np.linspace(0, 100, 1000)

x = generate_signal(t)
C = coherence(x)
S = spectral_entropy(x)

C_thr, S_thr = adaptive_thresholds(C, S)

gates, mask = detect_gates(C, S, C_thr, S_thr)

precursor_idx = detect_precursor(C)

# --------------------------------------------------
# 8. VISUALIZATION
# --------------------------------------------------
fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

# --- signal
axs[0].plot(t, x)
axs[0].set_title("System Dynamics x(t)")

# --- coherence
axs[1].plot(t, C, label="C(t)")
axs[1].axhline(C_thr, linestyle='--', label="C threshold")

if precursor_idx is not None:
    axs[1].axvline(t[precursor_idx], color='orange', label="precursor")

axs[1].set_title("Coherence")

# --- spectral entropy
axs[2].plot(t, S, label="S(t)")
axs[2].axhline(S_thr, linestyle='--', label="entropy threshold")
axs[2].set_title("Spectral Entropy")

# --- gates
axs[3].set_title("Gate Detection")

for g in gates:
    axs[3].axvspan(t[g[0]], t[g[1]], alpha=0.3)

axs[3].set_ylim(0, 1)

# legends
for ax in axs:
    ax.legend()

plt.tight_layout()

output_path = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v5.png"
plt.savefig(output_path)

# --------------------------------------------------
# 9. LOGGING
# --------------------------------------------------
print("\n--- NEXAH IEEE Gate Detection v5 ---")

print(f"Coherence threshold: {C_thr:.3f}")
print(f"Entropy threshold: {S_thr:.3f}")

if precursor_idx:
    print(f"Precursor at t ≈ {t[precursor_idx]:.2f}")

print(f"Detected gates: {len(gates)}")

for g in gates:
    print(f"Gate: t = {t[g[0]]:.2f} → {t[g[1]]:.2f}")

print(f"\nSaved to: {output_path}")
