import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

NODES = 64
TIMESTEPS = 4000
DT = 0.05

K_VALUES = np.linspace(0, 2.0, 40)

NOISE = 0.0

# ---------------------------------------------------------
# INITIAL NETWORK STRUCTURE
# ---------------------------------------------------------

N_INNER = 16
N_MIDDLE = 32
N_OUTER = 16

# natural frequencies
omega = np.zeros(NODES)

omega[:N_INNER] = 0.0033
omega[N_INNER:N_INNER+N_MIDDLE] = 0.0
omega[N_INNER+N_MIDDLE:] = -0.0033


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def kuramoto_order(theta):

    return np.abs(np.mean(np.exp(1j * theta)))


# ---------------------------------------------------------
# SIMULATION
# ---------------------------------------------------------

R_results = []

for K in K_VALUES:

    theta = np.random.uniform(0, 2*np.pi, NODES)

    R_history = []

    for t in range(TIMESTEPS):

        coupling = np.zeros(NODES)

        for i in range(NODES):

            phase_diff = theta - theta[i]

            coupling[i] = np.sum(np.sin(phase_diff))

        coupling = (K / NODES) * coupling

        noise = NOISE * np.random.randn(NODES)

        theta += (omega + coupling) * DT + noise

        R_history.append(kuramoto_order(theta))

    R_mean = np.mean(R_history[int(TIMESTEPS*0.5):])

    R_results.append(R_mean)

# ---------------------------------------------------------
# PLOT TRANSITION
# ---------------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(K_VALUES, R_results, marker="o")

plt.xlabel("Coupling strength K")
plt.ylabel("Mean order parameter R")

plt.title("Synchronization Transition Scan")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "synchronization_transition_scan.png")

plt.close()

# ---------------------------------------------------------
# SAVE DATA
# ---------------------------------------------------------

np.save(OUTPUT_DIR / "transition_K.npy", K_VALUES)
np.save(OUTPUT_DIR / "transition_R.npy", R_results)

print("Transition scan complete.")
