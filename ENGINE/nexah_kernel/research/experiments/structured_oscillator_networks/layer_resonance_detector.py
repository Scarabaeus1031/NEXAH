import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from fractions import Fraction

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

N_INNER = 16
N_MIDDLE = 32

SMOOTH_WINDOW = 120
MAX_DENOMINATOR = 8
RATIO_TOL = 0.08


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def moving_average(x, window):
    if window <= 1:
        return x.copy()
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


def unwrap_phase(ph):
    return np.unwrap(ph, axis=0)


def circular_mean(ph):
    return np.angle(np.mean(np.exp(1j * ph), axis=1))


def inst_frequency(phi_mean):

    dphi = np.diff(unwrap_phase(phi_mean))

    out = np.zeros(len(phi_mean))
    out[0] = dphi[0]
    out[1:] = dphi

    return out


def safe_ratio(a, b, eps=1e-12):
    return a / (b + eps)


def detect_resonance_windows(ratio_signal, max_denominator=8, tol=0.08):

    labels = []
    best_values = np.full(len(ratio_signal), np.nan)

    candidates = []

    for q in range(1, max_denominator + 1):
        for p in range(1, max_denominator + 1):

            val = p / q

            if 0.2 <= val <= 5.0:
                candidates.append((p, q, val))

    # remove duplicates
    unique = {}

    for p, q, val in candidates:

        key = round(val, 4)

        if key not in unique:
            unique[key] = (p, q, val)

    candidates = list(unique.values())

    for i, r in enumerate(ratio_signal):

        best_label = "none"
        best_val = np.nan
        best_dist = np.inf

        for p, q, val in candidates:

            dist = abs(r - val)

            if dist < best_dist and dist < tol:

                best_dist = dist
                best_label = f"{p}:{q}"
                best_val = val

        labels.append(best_label)
        best_values[i] = best_val

    return labels, best_values


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

history = np.load(PHASE_FILE)

steps, nodes = history.shape

N_OUTER = nodes - N_INNER - N_MIDDLE

inner = history[:, :N_INNER]
middle = history[:, N_INNER:N_INNER+N_MIDDLE]
outer = history[:, N_INNER+N_MIDDLE:]


# ---------------------------------------------------------
# LAYER MEAN PHASE
# ---------------------------------------------------------

phi_inner = circular_mean(inner)
phi_middle = circular_mean(middle)
phi_outer = circular_mean(outer)


# ---------------------------------------------------------
# INSTANTANEOUS FREQUENCIES
# ---------------------------------------------------------

w_inner = moving_average(inst_frequency(phi_inner), SMOOTH_WINDOW)
w_middle = moving_average(inst_frequency(phi_middle), SMOOTH_WINDOW)
w_outer = moving_average(inst_frequency(phi_outer), SMOOTH_WINDOW)


# ---------------------------------------------------------
# FREQUENCY RATIOS
# ---------------------------------------------------------

ratio_im = safe_ratio(w_inner, w_middle)
ratio_mo = safe_ratio(w_middle, w_outer)
ratio_io = safe_ratio(w_inner, w_outer)


# ---------------------------------------------------------
# DETECT RESONANCES
# ---------------------------------------------------------

labels_im, approx_im = detect_resonance_windows(ratio_im, MAX_DENOMINATOR, RATIO_TOL)
labels_mo, approx_mo = detect_resonance_windows(ratio_mo, MAX_DENOMINATOR, RATIO_TOL)
labels_io, approx_io = detect_resonance_windows(ratio_io, MAX_DENOMINATOR, RATIO_TOL)


# ---------------------------------------------------------
# PLOT RATIOS
# ---------------------------------------------------------

time = np.arange(steps)

plt.figure(figsize=(10,5))

plt.plot(time, ratio_im, label="inner/middle")
plt.plot(time, ratio_mo, label="middle/outer")
plt.plot(time, ratio_io, label="inner/outer")

plt.ylim(-5,5)

plt.legend()

plt.title("Layer Frequency Ratios")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "layer_frequency_ratios.png")

plt.close()


# ---------------------------------------------------------
# RESONANCE OCCUPANCY
# ---------------------------------------------------------

def count_labels(labels):

    counts = {}

    for l in labels:

        if l == "none":
            continue

        counts[l] = counts.get(l, 0) + 1

    return counts


counts_im = count_labels(labels_im)
counts_mo = count_labels(labels_mo)
counts_io = count_labels(labels_io)


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

with open(OUTPUT_DIR / "layer_resonance_report.txt","w") as f:

    f.write("Layer Resonance Report\n")
    f.write("======================\n\n")

    f.write("Inner/Middle\n")
    for k,v in counts_im.items():
        f.write(f"{k} : {v}\n")

    f.write("\nMiddle/Outer\n")
    for k,v in counts_mo.items():
        f.write(f"{k} : {v}\n")

    f.write("\nInner/Outer\n")
    for k,v in counts_io.items():
        f.write(f"{k} : {v}\n")


print("Layer resonance detection complete.")
