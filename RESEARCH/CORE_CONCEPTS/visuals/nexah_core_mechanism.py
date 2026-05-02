import numpy as np
import matplotlib.pyplot as plt

# =========================
# SETUP
# =========================

fig, ax = plt.subplots(figsize=(14, 6))
ax.set_facecolor("black")
plt.axis("off")

# =========================
# POSITIONS
# =========================

y = 0.5

x_state = 0.05
x_phi = 0.2
x_omega = 0.4
x_mismatch = 0.6
x_iota = 0.8

# =========================
# STATE (x)
# =========================

ax.text(x_state, y, "x(t)", color="deepskyblue", fontsize=14, ha='center')

# arrow
ax.annotate("", xy=(x_phi, y), xytext=(x_state+0.05, y),
            arrowprops=dict(arrowstyle="->", color="white"))

# =========================
# PHASE (φ)
# =========================

circle = plt.Circle((x_phi, y), 0.05, color='cyan', fill=False, linewidth=2)
ax.add_patch(circle)
ax.text(x_phi, y-0.1, "φ(t)", color="cyan", ha='center')

# =========================
# PHASE VELOCITY (ω & ω̂)
# =========================

# ω
ax.arrow(x_omega, y, 0.05, 0.1,
         head_width=0.02, color='yellow')

# ω̂
ax.arrow(x_omega, y, 0.05, 0.05,
         head_width=0.02, color='white')

ax.text(x_omega, y-0.15, "ω(t)", color="yellow", ha='center')
ax.text(x_omega+0.05, y-0.05, "ω̂(t)", color="white", ha='center')

# arrow from φ → ω
ax.annotate("", xy=(x_omega, y), xytext=(x_phi+0.05, y),
            arrowprops=dict(arrowstyle="->", color="white"))

# =========================
# MISMATCH (M)
# =========================

# draw difference line
ax.plot([x_omega+0.05, x_omega+0.05],
        [y+0.05, y+0.1],
        color="orange", linewidth=3)

ax.text(x_mismatch, y, "M = |ω - ω̂|", color="orange", fontsize=12, ha='center')

# arrow
ax.annotate("", xy=(x_mismatch, y), xytext=(x_omega+0.1, y),
            arrowprops=dict(arrowstyle="->", color="white"))

# =========================
# IOTA (EVENT)
# =========================

iota_circle = plt.Circle((x_iota, y), 0.06, color='red', fill=False, linewidth=2)
ax.add_patch(iota_circle)

ax.text(x_iota, y-0.1, "IOTA", color="red", ha='center')

# arrow
ax.annotate("", xy=(x_iota, y), xytext=(x_mismatch+0.05, y),
            arrowprops=dict(arrowstyle="->", color="white"))

# =========================
# CONTROL (s)
# =========================

ax.arrow(x_mismatch, y+0.2, -0.1, -0.1,
         head_width=0.02, color='magenta')

ax.text(x_mismatch, y+0.25, "s(φ, I)", color="magenta", ha='center')

# =========================
# TITLE
# =========================

plt.title(
    "NEXAH — Phase–Mismatch–Control Mechanism",
    color="white",
    fontsize=16
)

# =========================
# SAVE
# =========================

plt.tight_layout()
plt.savefig("nexah_core_mechanism.png", dpi=300, facecolor='black')
plt.close()

print("✅ Saved: nexah_core_mechanism.png")
