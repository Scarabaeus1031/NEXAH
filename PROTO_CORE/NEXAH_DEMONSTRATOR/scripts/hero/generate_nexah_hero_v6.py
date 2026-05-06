import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# NEXAH v6 — Cross-System Quantitative Structure Atlas
# Systems: Lorenz · Halvorsen · Rössler
#
# Output:
# NEXAH_DEMONSTRATOR/visuals/nexah_structure_cross_system_v6.png
# ============================================================

# ============================================================
# 1. SYSTEM DEFINITIONS
# ============================================================

def lorenz_step(x, y, z, s=10.0, r=28.0, b=8.0 / 3.0):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz


def halvorsen_step(x, y, z, a=1.4):
    dx = -a * x - 4.0 * y - 4.0 * z - y * y
    dy = -a * y - 4.0 * z - 4.0 * x - z * z
    dz = -a * z - 4.0 * x - 4.0 * y - x * x
    return dx, dy, dz


def rossler_step(x, y, z, a=0.2, b=0.2, c=5.7):
    dx = -y - z
    dy = x + a * y
    dz = b + z * (x - c)
    return dx, dy, dz


# ============================================================
# 2. SIMULATION
# ============================================================

def simulate(system_func, steps=18000, dt=0.01, burn=1500, init=(0.1, 0.0, 0.0)):
    xs = np.empty(steps)
    ys = np.empty(steps)
    zs = np.empty(steps)

    xs[0], ys[0], zs[0] = init

    for i in range(steps - 1):
        dx, dy, dz = system_func(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + dx * dt
        ys[i + 1] = ys[i] + dy * dt
        zs[i + 1] = zs[i] + dz * dt

    return xs[burn:], ys[burn:], zs[burn:]


# ============================================================
# 3. STRUCTURE EXTRACTION
# ============================================================

def extract_structure(xs, ys, grid_n=260):
    points = np.vstack([xs, ys])
    kde = gaussian_kde(points)

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    positions = np.vstack([X.ravel(), Y.ravel()])
    rho = np.reshape(kde(positions).T, X.shape)

    # density-gradient flow proxy
    d_rho_dx, d_rho_dy = np.gradient(rho)

    mag = np.sqrt(d_rho_dx**2 + d_rho_dy**2) + 1e-12
    Fx = d_rho_dx / mag
    Fy = d_rho_dy / mag

    vx = np.gradient(xs)
    vy = np.gradient(ys)

    def sample(field, x, y):
        xi = np.clip(
            ((x - xmin) / (xmax - xmin) * (field.shape[0] - 1)).astype(int),
            0,
            field.shape[0] - 1,
        )
        yi = np.clip(
            ((y - ymin) / (ymax - ymin) * (field.shape[1] - 1)).astype(int),
            0,
            field.shape[1] - 1,
        )
        return field[xi, yi]

    rho_t = sample(rho, xs, ys)
    Fx_t = sample(Fx, xs, ys)
    Fy_t = sample(Fy, xs, ys)

    vel_mag = np.sqrt(vx**2 + vy**2) + 1e-12
    field_mag = np.sqrt(Fx_t**2 + Fy_t**2) + 1e-12

    coherence = (vx * Fx_t + vy * Fy_t) / (vel_mag * field_mag)

    # transition / gate score:
    # high when density is low and coherence is weak
    inv_density = 1.0 / (rho_t + 1e-12)
    inv_density = (inv_density - inv_density.min()) / (inv_density.max() - inv_density.min() + 1e-12)

    low_coherence = 1.0 - np.clip((coherence + 1.0) / 2.0, 0, 1)
    gate_score = inv_density * low_coherence

    gate_threshold = np.percentile(gate_score, 98)
    gate_idx = np.where(gate_score >= gate_threshold)[0]

    # visual thinning
    if len(gate_idx) > 250:
        gate_idx = gate_idx[:: max(1, len(gate_idx) // 250)]

    # grid-level transition proxy
    transition_field = 1.0 / (rho + 1e-12)
    transition_field = (transition_field - transition_field.min()) / (
        transition_field.max() - transition_field.min() + 1e-12
    )

    return {
        "xs": xs,
        "ys": ys,
        "vx": vx,
        "vy": vy,
        "X": X,
        "Y": Y,
        "rho": rho,
        "Fx": Fx,
        "Fy": Fy,
        "coherence": coherence,
        "gate_score": gate_score,
        "gate_x": xs[gate_idx],
        "gate_y": ys[gate_idx],
        "transition_field": transition_field,
        "extent": [xmin, xmax, ymin, ymax],
        "metrics": {
            "mean_coherence": float(np.mean(coherence)),
            "std_coherence": float(np.std(coherence)),
            "gate_fraction": float(np.mean(gate_score >= gate_threshold)),
            "density_contrast": float(rho.max() / (rho.mean() + 1e-12)),
        },
    }


# ============================================================
# 4. RUN SYSTEMS
# ============================================================

systems = [
    ("Lorenz", lorenz_step, 0.01, 18000, 1500),
    ("Halvorsen", halvorsen_step, 0.005, 24000, 2500),
    ("Rössler", rossler_step, 0.01, 22000, 2000),
]

results = []

for name, func, dt, steps, burn in systems:
    xs, ys, zs = simulate(func, steps=steps, dt=dt, burn=burn)
    structure = extract_structure(xs, ys)
    results.append((name, structure))


# ============================================================
# 5. PLOTTING
# ============================================================

fig, axes = plt.subplots(3, 4, figsize=(22, 14))

for row, (name, s) in enumerate(results):
    xs = s["xs"]
    ys = s["ys"]
    X = s["X"]
    Y = s["Y"]
    rho = s["rho"]
    Fx = s["Fx"]
    Fy = s["Fy"]
    coherence = s["coherence"]
    transition_field = s["transition_field"]
    extent = s["extent"]
    metrics = s["metrics"]

    # --------------------------------------------------------
    # Col 1 — Raw dynamics
    # --------------------------------------------------------
    ax = axes[row, 0]
    ax.plot(xs, ys, lw=0.35, alpha=0.75)
    ax.set_title(f"{name}\nRaw Dynamics")
    ax.set_xticks([])
    ax.set_yticks([])

    # --------------------------------------------------------
    # Col 2 — Density + flow
    # --------------------------------------------------------
    ax = axes[row, 1]
    ax.imshow(np.rot90(rho), extent=extent, aspect="auto")
    ax.quiver(
        X[::18, ::18],
        Y[::18, ::18],
        Fx[::18, ::18],
        Fy[::18, ::18],
        scale=35,
        alpha=0.55,
        width=0.002,
    )
    ax.set_title("Field\nDensity + Flow")
    ax.set_xticks([])
    ax.set_yticks([])

    # --------------------------------------------------------
    # Col 3 — Coherence along trajectory
    # --------------------------------------------------------
    ax = axes[row, 2]
    sc = ax.scatter(xs, ys, c=coherence, s=1.0, cmap="coolwarm", alpha=0.7)
    ax.set_title("Coherence Field\nalignment with flow")
    ax.set_xticks([])
    ax.set_yticks([])

    # --------------------------------------------------------
    # Col 4 — Transition / gate score
    # --------------------------------------------------------
    ax = axes[row, 3]
    ax.imshow(np.rot90(transition_field), extent=extent, aspect="auto", alpha=0.85)
    ax.scatter(
        s["gate_x"],
        s["gate_y"],
        s=12,
        c="black",
        alpha=0.85,
        label="gate candidates",
    )

    # observed path segment
    p0 = int(len(xs) * 0.25)
    p1 = int(len(xs) * 0.42)
    ax.plot(xs[p0:p1], ys[p0:p1], lw=1.8, color="white", label="path segment")

    metric_text = (
        f"mean C = {metrics['mean_coherence']:.2f}\n"
        f"gate frac = {metrics['gate_fraction']:.3f}\n"
        f"density contrast = {metrics['density_contrast']:.1f}"
    )

    ax.text(
        0.02,
        0.03,
        metric_text,
        transform=ax.transAxes,
        fontsize=8,
        va="bottom",
        ha="left",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.75),
    )

    ax.set_title("Transition Geometry\nlow density + low coherence")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(fontsize=7, loc="upper right")

fig.suptitle(
    "NEXAH v6 — Cross-System Quantitative Structure Atlas\n"
    "Raw Dynamics → Density/Flow → Coherence → Gate Candidates",
    fontsize=16,
)

plt.tight_layout(rect=[0, 0, 1, 0.93])

out = "NEXAH_DEMONSTRATOR/visuals/nexah_structure_cross_system_v6.png"

plt.savefig(
    out,
    dpi=300,
    bbox_inches="tight",
)

print(f"Saved visual to: {out}")

plt.show()
