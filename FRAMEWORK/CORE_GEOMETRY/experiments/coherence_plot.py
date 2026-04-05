# -----------------------------
# COHERENCE MAGNITUDE
# -----------------------------
C_abs = np.abs(C)

# -----------------------------
# ENVELOPE (sehr wichtig!)
# -----------------------------
def moving_average(x, window=100):
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode='same')

C_env = moving_average(C_abs)

# -----------------------------
# PLOT v3
# -----------------------------
plt.figure(figsize=(12,6))

plt.plot(C_abs, alpha=0.1, label="|Coherence| raw")
plt.plot(C_env, linewidth=2, label="Coherence Envelope")

plt.title("NEXAH Coherence Envelope")
plt.legend()

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_v3.png", dpi=300)
plt.show()
