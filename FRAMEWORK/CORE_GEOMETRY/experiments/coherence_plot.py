# -----------------------------
# PHASE (einfach für jetzt)
# -----------------------------
t = np.arange(len(C))
theta = 2 * np.pi * t / len(C)   # Kreis

# -----------------------------
# POLAR PLOT
# -----------------------------
plt.figure(figsize=(6,6))
ax = plt.subplot(111, projection='polar')

# Radius = Coherence Envelope
ax.plot(theta, C_env, linewidth=2)

ax.set_title("NEXAH Coherence — Polar View")

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_polar.png", dpi=300)
plt.show()
