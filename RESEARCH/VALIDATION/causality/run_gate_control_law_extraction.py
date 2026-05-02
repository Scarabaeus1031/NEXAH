import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — Control Law Extraction (s*(φ))")

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

# gleiche Parameter wie im resonance scan
strength_values = np.linspace(0.0, 2.0, 20)
phase_values = np.linspace(0.0, 2*np.pi, 30)

# Datei laden (aus deinem scan)
# -> musst du ggf. anpassen
data_path = "RESEARCH/validation/causality/gate_resonance_scan_multirun.npy"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

Z = np.load(data_path)  
# shape: (len(strength_values), len(phase_values))

# --------------------------------------------------
# CONTROL LAW EXTRACTION
# --------------------------------------------------

s_star = []

for j in range(len(phase_values)):
    column = Z[:, j]
    idx = np.argmax(column)
    s_star.append(strength_values[idx])

s_star = np.array(s_star)

# --------------------------------------------------
# SMOOTH (optional aber sinnvoll)
# --------------------------------------------------

def moving_average(x, k=3):
    return np.convolve(x, np.ones(k)/k, mode='same')

s_star_smooth = moving_average(s_star, k=3)

# --------------------------------------------------
# PLOT
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(phase_values, s_star, 'o-', label="raw s*(φ)", alpha=0.5)
plt.plot(phase_values, s_star_smooth, '-', label="smoothed s*(φ)", linewidth=2)

plt.xlabel("phase φ")
plt.ylabel("optimal strength s*")
plt.title("NEXAH Control Law: s*(φ)")

plt.legend()
plt.grid()

plt.savefig("RESEARCH/validation/causality/results/control_law.png", dpi=200)
plt.close()

print("✅ Saved: control_law.png")
