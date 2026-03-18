import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

N_INNER = 16
N_MIDDLE = 32

RADIUS = 2

COHERENT_THRESHOLD = 0.85
INCOHERENT_THRESHOLD = 0.45

SMOOTH_WINDOW = 80


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def moving_average(x, window):
    if window <= 1:
        return x.copy()
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


def local_order_on_ring(theta_ring, radius=2):

    n = len(theta_ring)
    local_R = np.zeros(n)

    for i in range(n):

        idx = [(i + k) % n for k in range(-radius, radius + 1)]

        neighborhood = theta_ring[idx]

        local_R[i] = np.abs(np.mean(np.exp(1j * neighborhood)))

    return local_R


def classify_chimera_fraction(local_R,
                              coherent_threshold=0.85,
                              incoherent_threshold=0.45):

    coherent = local_R >= coherent_threshold
    incoherent = local_R <= incoherent_threshold

    coherent_fraction = np.sum(coherent) / len(local_R)
    incoherent_fraction = np.sum(incoherent) / len(local_R)

    mixed_fraction = 1 - coherent_fraction - incoherent_fraction

    return coherent_fraction, incoherent_fraction, mixed_fraction


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
# LOCAL ORDER ANALYSIS
# ---------------------------------------------------------

coh_frac_inner = []
inc_frac_inner = []

coh_frac_middle = []
inc_frac_middle = []

coh_frac_outer = []
inc_frac_outer = []


chimera_indicator = []

for t in range(steps):

    Ri = local_order_on_ring(inner[t], RADIUS)
    Rm = local_order_on_ring(middle[t], RADIUS)
    Ro = local_order_on_ring(outer[t], RADIUS)

    ci, ii, mi = classify_chimera_fraction(Ri,
                                           COHERENT_THRESHOLD,
                                           INCOHERENT_THRESHOLD)

    cm, im, mm = classify_chimera_fraction(Rm,
                                           COHERENT_THRESHOLD,
                                           INCOHERENT_THRESHOLD)

    co, io, mo = classify_chimera_fraction(Ro,
                                           COHERENT_THRESHOLD,
                                           INCOHERENT_THRESHOLD)

    coh_frac_inner.append(ci)
    inc_frac_inner.append(ii)

    coh_frac_middle.append(cm)
    inc_frac_middle.append(im)

    coh_frac_outer.append(co)
    inc_frac_outer.append(io)

    # Chimera indicator:
    # coexistence of coherent and incoherent
    chimera = (ci > 0.1 and ii > 0.1) or \
              (cm > 0.1 and im > 0.1) or \
              (co > 0.1 and io > 0.1)

    chimera_indicator.append(chimera)


chimera_indicator = np.array(chimera_indicator)


# ---------------------------------------------------------
# SMOOTH
# ---------------------------------------------------------

coh_inner_s = moving_average(np.array(coh_frac_inner), SMOOTH_WINDOW)
inc_inner_s = moving_average(np.array(inc_frac_inner), SMOOTH_WINDOW)

coh_middle_s = moving_average(np.array(coh_frac_middle), SMOOTH_WINDOW)
inc_middle_s = moving_average(np.array(inc_frac_middle), SMOOTH_WINDOW)

coh_outer_s = moving_average(np.array(coh_frac_outer), SMOOTH_WINDOW)
inc_outer_s = moving_average(np.array(inc_frac_outer), SMOOTH_WINDOW)


# ---------------------------------------------------------
# PLOT 1: COHERENT VS INCOHERENT
# ---------------------------------------------------------

plt.figure(figsize=(10,5))

plt.plot(coh_inner_s, label="inner coherent")
plt.plot(inc_inner_s, label="inner incoherent")

plt.plot(coh_middle_s, label="middle coherent")
plt.plot(inc_middle_s, label="middle incoherent")

plt.plot(coh_outer_s, label="outer coherent")
plt.plot(inc_outer_s, label="outer incoherent")

plt.legend()

plt.xlabel("time")
plt.ylabel("fraction")

plt.title("Local coherence fractions")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "chimera_local_coherence.png")

plt.close()


# ---------------------------------------------------------
# PLOT 2: CHIMERA INDICATOR
# ---------------------------------------------------------

plt.figure(figsize=(10,4))

plt.plot(chimera_indicator.astype(int))

plt.xlabel("time")
plt.ylabel("chimera detected")

plt.title("Chimera State Indicator")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "chimera_indicator.png")

plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

chimera_fraction = np.mean(chimera_indicator)

with open(OUTPUT_DIR / "chimera_report.txt","w") as f:

    f.write("Chimera State Report\n")
    f.write("====================\n\n")

    f.write(f"nodes: {nodes}\n")
    f.write(f"timesteps: {steps}\n\n")

    f.write(f"fraction of chimera states: {chimera_fraction:.4f}\n\n")

    if chimera_fraction > 0.05:
        f.write("Chimera behaviour detected\n")
    else:
        f.write("No persistent chimera detected\n")


print("Chimera detection complete.")
