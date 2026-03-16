import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

# Layer structure
N_INNER = 16
N_MIDDLE = 32

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

history = np.load(PHASE_FILE)

steps, nodes = history.shape

time = np.arange(steps)

N_OUTER = nodes - N_INNER - N_MIDDLE

inner = history[:, :N_INNER]
middle = history[:, N_INNER:N_INNER+N_MIDDLE]
outer = history[:, N_INNER+N_MIDDLE:]


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def unwrap_phase(ph):

    return np.unwrap(ph, axis=0)


def estimate_frequency(ph):

    dphi = np.diff(ph, axis=0)

    return np.mean(dphi, axis=0)


def circular_mean(ph):

    return np.angle(np.mean(np.exp(1j*ph), axis=1))


# ---------------------------------------------------------
# UNWRAP PHASE
# ---------------------------------------------------------

inner_u = unwrap_phase(inner)
middle_u = unwrap_phase(middle)
outer_u = unwrap_phase(outer)

history_u = unwrap_phase(history)

# ---------------------------------------------------------
# NODE FREQUENCIES
# ---------------------------------------------------------

node_freq = estimate_frequency(history_u)

# ---------------------------------------------------------
# LAYER FREQUENCIES
# ---------------------------------------------------------

freq_inner = np.mean(node_freq[:N_INNER])
freq_middle = np.mean(node_freq[N_INNER:N_INNER+N_MIDDLE])
freq_outer = np.mean(node_freq[N_INNER+N_MIDDLE:])

# ---------------------------------------------------------
# DRIFT
# ---------------------------------------------------------

drift_im = freq_inner - freq_middle
drift_mo = freq_middle - freq_outer
drift_io = freq_inner - freq_outer


# ---------------------------------------------------------
# PLOT NODE FREQUENCIES
# ---------------------------------------------------------

plt.figure(figsize=(10,5))

plt.scatter(range(nodes), node_freq)

plt.axvline(N_INNER, linestyle="--")
plt.axvline(N_INNER + N_MIDDLE, linestyle="--")

plt.title("Node Frequency Distribution")
plt.xlabel("node")
plt.ylabel("frequency")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "frequency_nodes.png")
plt.close()

# ---------------------------------------------------------
# LAYER FREQUENCY BAR
# ---------------------------------------------------------

plt.figure(figsize=(6,4))

plt.bar(
    ["inner","middle","outer"],
    [freq_inner, freq_middle, freq_outer]
)

plt.title("Layer Frequencies")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "frequency_layers.png")
plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

report = OUTPUT_DIR / "frequency_drift_report.txt"

with open(report,"w") as f:

    f.write("Frequency Drift Report\n")
    f.write("======================\n\n")

    f.write(f"Nodes: {nodes}\n")
    f.write(f"Timesteps: {steps}\n\n")

    f.write("Layer frequencies\n")
    f.write("-----------------\n")

    f.write(f"inner  : {freq_inner:.6f}\n")
    f.write(f"middle : {freq_middle:.6f}\n")
    f.write(f"outer  : {freq_outer:.6f}\n\n")

    f.write("Layer drift\n")
    f.write("-----------\n")

    f.write(f"inner-middle : {drift_im:.6f}\n")
    f.write(f"middle-outer : {drift_mo:.6f}\n")
    f.write(f"inner-outer  : {drift_io:.6f}\n\n")

print("Frequency drift analysis complete.")
