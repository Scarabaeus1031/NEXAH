import numpy as np
import matplotlib.pyplot as plt

# =========================
# GRID
# =========================
N = 900
x = np.linspace(-2.0, 1.0, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

# =========================
# MANDELBROT ITERATION
# =========================
Z = np.zeros_like(C)
mask = np.ones_like(C, dtype=bool)

max_iter = 120

for i in range(max_iter):
    Z[mask] = Z[mask]**2 + C[mask]

    escaped = np.abs(Z) > 2
    Z[escaped] = np.nan   # 🔥 wichtig → verhindert overflow noise
    mask[escaped] = False

# =========================
# PHASE FIELD
# =========================
phi = np.angle(Z)
phi = np.nan_to_num(phi)

# =========================
# GRADIENT (FLOW FIELD)
# =========================
gy, gx = np.gradient(phi)

# =========================
# MISMATCH FIELD (IOTA)
# =========================
M = np.sqrt(gx**2 + gy**2)
M = (M - M.min()) / (M.max() - M.min())

# =========================
# IOTA EVENTS
# =========================
threshold = 0.65
iota_mask = M > threshold

# =========================
# PLOT
# =========================
plt.figure(figsize=(10, 12))

# --- PHASE BACKGROUND ---
plt.imshow(
    phi,
    extent=[x.min(), x.max(), y.min(), y.max()],
    cmap='twilight',
    alpha=0.9
)

# --- FLOW LINES ---
skip = 20

plt.streamplot(
    x,
    y,
    gx,
    gy,
    color='cyan',
    density=2.2,
    linewidth=0.6,
    arrowsize=0.6,
    minlength=0.05
)

# Streamplots zeigen Richtungen eines Feldes entlang der lokalen Vektoren  [oai_citation:0‡TutorialsPoint](https://www.tutorialspoint.com/matplotlib/matplotlib_stream_plot.htm?utm_source=chatgpt.com)

# --- IOTA EVENTS ---
plt.scatter(
    X[iota_mask],
    Y[iota_mask],
    s=0.4,
    c='white',
    alpha=0.6
)

# --- BOUNDARY OVERLAY ---
plt.contour(
    X,
    Y,
    M,
    levels=[0.6],
    colors='magenta',
    linewidths=0.6
)

# =========================
# STYLE
# =========================
plt.title("IOTA Flow Lines — Phase Geometry + Transition Field")
plt.xlim([-2, 1])
plt.ylim([-1.5, 1.5])
plt.axis('off')

# =========================
# SAVE
# =========================
output_path = "RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/iota_flow_lines_v2.png"

plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Saved to: {output_path}")
