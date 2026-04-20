import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ============================================================
# 1. CLUSTER CENTERS
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

cluster_colors = {
    "C0": "#1f77b4",
    "C1": "#ff7f0e",
    "C2": "#2ca02c",
    "C3": "#d62728",
}

# ============================================================
# 2. ENVELOPE FIELD (FROM V28)
# ============================================================

def gaussian(x, y, center, depth, sigma=1.2):
    return depth * np.exp(-((x - center[0]) ** 2 + (y - center[1]) ** 2) / (2 * sigma ** 2))


def envelope(t):
    return 1.0 + 0.4 * np.sin(0.03 * t)


def attractor_strengths(t):
    e = envelope(t)
    return {
        "C0": 1.5 * e,
        "C1": 2.0 * (1.0 + 0.4 * np.sin(0.03 * t + np.pi / 2)),
        "C2": 3.0 * (1.0 + 0.3 * np.sin(0.03 * t)),
        "C3": -2.0,  # repulsive / inverted
    }


def scalar_field(x, y, t):
    strengths = attractor_strengths(t)
    val = 0.0
    for c, pos in clusters.items():
        val += gaussian(x, y, pos, strengths[c])
    return val


def grad_scalar_field(x, y, t, eps=1e-3):
    dx = (scalar_field(x + eps, y, t) - scalar_field(x - eps, y, t)) / (2 * eps)
    dy = (scalar_field(x, y + eps, t) - scalar_field(x, y - eps, t)) / (2 * eps)
    return np.array([dx, dy])


# ============================================================
# 3. ROTATIONAL COMPONENT
# ============================================================

def rotational_field(x, y):
    """
    Hand-crafted residual / curl-like component.
    Built as superposition of local vortical terms.
    """
    p = np.array([x, y], dtype=float)
    v = np.zeros(2, dtype=float)

    # around C2: mild clockwise swirl
    c2 = clusters["C2"]
    r2 = p - c2
    d2 = np.linalg.norm(r2) + 1e-9
    swirl2 = np.array([r2[1], -r2[0]]) * np.exp(-(d2 ** 2) / (2 * 1.4 ** 2))
    v += 0.85 * swirl2

    # around C3: counter swirl / disturbance spike
    c3 = clusters["C3"]
    r3 = p - c3
    d3 = np.linalg.norm(r3) + 1e-9
    swirl3 = np.array([-r3[1], r3[0]]) * np.exp(-(d3 ** 2) / (2 * 1.1 ** 2))
    v += 1.15 * swirl3

    # corridor shear between C1 and C2
    c1 = clusters["C1"]
    mid = 0.5 * (c1 + c2)
    rm = p - mid
    dm = np.linalg.norm(rm) + 1e-9
    shear = np.array([0.0, 1.0]) * np.exp(-(dm ** 2) / (2 * 1.8 ** 2))
    v += 0.35 * shear

    return v


# ============================================================
# 4. COMBINED FIELD
# ============================================================

def potential_component(x, y, t):
    """
    Downhill component from scalar field.
    """
    return grad_scalar_field(x, y, t)


def combined_field(x, y, t, alpha=1.0, beta=0.65):
    """
    alpha = potential weight
    beta  = rotational weight
    """
    v_p = potential_component(x, y, t)
    v_r = rotational_field(x, y)
    return alpha * v_p + beta * v_r


def curl_numeric(field_fn, x, y, t=None, eps=1e-3):
    """
    2D scalar curl of vector field F=(Fx,Fy):
    curl = dFy/dx - dFx/dy
    """
    if t is None:
        fx_yplus = field_fn(x, y + eps)
        fx_yminus = field_fn(x, y - eps)
        fy_xplus = field_fn(x + eps, y)
        fy_xminus = field_fn(x - eps, y)
    else:
        fx_yplus = field_fn(x, y + eps, t)
        fx_yminus = field_fn(x, y - eps, t)
        fy_xplus = field_fn(x + eps, y, t)
        fy_xminus = field_fn(x - eps, y, t)

    dFx_dy = (fx_yplus[0] - fx_yminus[0]) / (2 * eps)
    dFy_dx = (fy_xplus[1] - fy_xminus[1]) / (2 * eps)
    return dFy_dx - dFx_dy


# ============================================================
# 5. GRID COMPUTATION
# ============================================================

def compute_grids(t=200, nx=140, ny=140):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)
    X, Y = np.meshgrid(xs, ys)

    Z = scalar_field(X, Y, t)

    Up = np.zeros_like(X)
    Vp = np.zeros_like(Y)

    Ur = np.zeros_like(X)
    Vr = np.zeros_like(Y)

    Uc = np.zeros_like(X)
    Vc = np.zeros_like(Y)

    CurlR = np.zeros_like(X)
    CurlC = np.zeros_like(X)

    for i in range(nx):
        for j in range(ny):
            x = X[j, i]
            y = Y[j, i]

            vp = potential_component(x, y, t)
            vr = rotational_field(x, y)
            vc = combined_field(x, y, t)

            Up[j, i], Vp[j, i] = vp
            Ur[j, i], Vr[j, i] = vr
            Uc[j, i], Vc[j, i] = vc

            CurlR[j, i] = curl_numeric(rotational_field, x, y)
            CurlC[j, i] = curl_numeric(combined_field, x, y, t=t)

    return X, Y, Z, Up, Vp, Ur, Vr, Uc, Vc, CurlR, CurlC


# ============================================================
# 6. TRAJECTORY ON COMBINED FIELD
# ============================================================

def simulate_trajectory(start=None, t0=0, steps=220, dt=0.10, noise=0.015):
    if start is None:
        start = np.array([9.5, 27.0], dtype=float)

    x = start.copy()
    traj = [x.copy()]

    for k in range(steps):
        t = t0 + k
        v = combined_field(x[0], x[1], t)
        x = x + dt * v + noise * np.random.randn(2)
        traj.append(x.copy())

    return np.array(traj)


# ============================================================
# 7. PLOTTING
# ============================================================

def plot_v29():
    print("Running V29 Field Decomposition...")

    t = 200
    X, Y, Z, Up, Vp, Ur, Vr, Uc, Vc, CurlR, CurlC = compute_grids(t=t)

    traj = simulate_trajectory()

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # --------------------------------------------------------
    # Q1: scalar topography + potential field
    # --------------------------------------------------------
    im1 = ax1.contourf(X, Y, Z, levels=45, cmap="viridis")
    skip = (slice(None, None, 4), slice(None, None, 4))
    ax1.quiver(
        X[skip], Y[skip], Up[skip], Vp[skip],
        color="white", alpha=0.75, scale=70
    )

    for k, v in clusters.items():
        ax1.scatter(v[0], v[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax1.text(v[0], v[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax1.set_title("Q1 — Scalar Field + Potential Component")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    # --------------------------------------------------------
    # Q2: rotational field / residual
    # --------------------------------------------------------
    im2 = ax2.contourf(X, Y, CurlR, levels=45, cmap="coolwarm")
    ax2.quiver(
        X[skip], Y[skip], Ur[skip], Vr[skip],
        color="black", alpha=0.75, scale=38
    )

    for k, v in clusters.items():
        ax2.scatter(v[0], v[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax2.text(v[0], v[1] + 0.18, k, color="black", ha="center", va="bottom", fontsize=11)

    ax2.set_title("Q2 — Rotational / Residual Component")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    # --------------------------------------------------------
    # Q3: combined field + trajectory
    # --------------------------------------------------------
    im3 = ax3.contourf(X, Y, Z, levels=45, cmap="viridis")
    ax3.quiver(
        X[skip], Y[skip], Uc[skip], Vc[skip],
        color="white", alpha=0.75, scale=55
    )
    ax3.plot(traj[:, 0], traj[:, 1], color="magenta", lw=2.0, alpha=0.95, zorder=6)
    ax3.scatter(traj[0, 0], traj[0, 1], c="lime", s=120, edgecolor="black", zorder=7)
    ax3.scatter(traj[-1, 0], traj[-1, 1], c="yellow", s=130, edgecolor="black", zorder=7)

    for k, v in clusters.items():
        ax3.scatter(v[0], v[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax3.text(v[0], v[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax3.set_title("Q3 — Combined Field + Trajectory")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    # --------------------------------------------------------
    # Q4: curl of combined field
    # --------------------------------------------------------
    im4 = ax4.contourf(X, Y, CurlC, levels=45, cmap="plasma")
    for k, v in clusters.items():
        ax4.scatter(v[0], v[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax4.text(v[0], v[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax4.set_title("Q4 — Curl / Topological Signature of Combined Field")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")
    fig.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04)

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "v29_field_decomposition.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print("\nInterpretation:")
    print("- Q1 shows the scalar envelope / potential landscape.")
    print("- Q2 isolates the rotational / residual structure.")
    print("- Q3 combines both into a navigable field.")
    print("- Q4 shows the topological signature (curl) of the combined field.")


if __name__ == "__main__":
    plot_v29()
