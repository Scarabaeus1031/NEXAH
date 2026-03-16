import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Simulate some data for chimera state overlap (replace with your actual data)
time_steps = 10000
nodes = 64
phase_data = np.random.rand(time_steps, nodes)  # Dummy data, replace with real phase data

# Compute coherence (use actual method to compute chimera states)
coherent = np.random.rand(time_steps, nodes)  # Dummy coherence data
incoherent = 1 - coherent  # Incoherent as complement of coherent

# ---------------------------------------------------------
# PLOT Chimera State Overlap
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

# Plot the states
plt.plot(coherent.mean(axis=1), label="Coherent", color='blue')
plt.plot(incoherent.mean(axis=1), label="Incoherent", color='orange')

plt.title("Chimera State Overlap")
plt.xlabel("Time")
plt.ylabel("Fraction")
plt.legend()

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "chimera_state_overlap.png")
plt.close()

print("Chimera State Overlap visualized and saved.")
