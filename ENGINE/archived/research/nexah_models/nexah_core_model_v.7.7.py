# ============================================================
# NEXAH v7.7 — Lorenz + FTLE Proxy + Navigation Overlay
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, gaussian_gradient_magnitude


# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
steps = 12000
dt = 0.005

# Lorenz
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

# FTLE-like proxy
neighbor_eps = 1e-4
ridge_sigma = 1.2

# NEXAH state thresholds on projected plane
r_release = 4.0
r_lock = 12.0
r_engage = 24.0

# navigation bias
nav_gain = 0.08


# ------------------------------------------------------------
# LORENZ SYSTEM
# ------------------------------------------------------------
def lorenz_step(x, y, z, sigma=10.0, rho=28.0, beta=8.0/3.0):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


def simulate_lorenz(x0=0.1, y0=0.0, z0=20.0):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    x, y, z = x0, y0, z0

    for i in range(steps):
        dx, dy, dz = lorenz_step(x, y, z, sigma=sigma, rho=rho, beta=beta)

        x += dt * dx
        y += dt * dy
        z += dt * dz

        xs[i] = x
        ys[i] = y
        zs[i] = z

    return xs, ys, zs


# ------------------------------------------------------------
# FTLE-LIKE LOCAL INSTABILITY
# ------------------------------------------------------------
def simulate_pairwise_divergence(x0, y0, z0, eps=1e-4, horizon=30):
    x1, y1, z1 = x0, y0, z0
    x2, y2, z2 = x0 + eps, y0 + eps, z0 + eps

    d0 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) + 1e-12

    for _ in range(horizon):
        dx1, dy1, dz1 = lorenz_step(x1, y1, z1, sigma=sigma, rho=rho, beta=beta)
        dx2, dy2, dz2 = lorenz_step(x2, y2, z2, sigma=sigma, rho=rho, beta=beta)

        x1 += dt * dx1
        y1 += dt * dy1
        z1 += dt * dz1

        x2 += dt * dx2
        y2 += dt * dy2
        z2 += dt * dz2

    d1 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) + 1e-12
    ftle = (1.0 / (horizon * dt)) * np.log(d1 / d0)
    return ftle


def compute_ftle_along_trajectory(xs, ys, zs, stride=20, horizon=30):
    ftle_vals = np.full(len(xs), np.nan)

    for i in range(0, len(xs) - horizon - 1, stride):
        ftle_vals[i] = simulate_pairwise_divergence(
            xs[i], ys[i], zs[i],
            eps=neighbor_eps,
            horizon=horizon
        )

    # fill gaps by nearest previous value
    last = 0.0
    for i in range(len(ftle_vals)):
        if np.isnan(ftle_vals[i]):
            ftle_vals[i] = last
        else:
            last = ftle_vals[i]

    return ftle_vals


# ------------------------------------------------------------
# 2D PROJECTION + GRID MAP
# ------------------------------------------------------------
def project_plane(xs, ys, zs):
    """
    Simple NEXAH-like reduced plane:
    Xp = x
    Yp = z - mean(z)
    """
    xp = xs
    yp = zs - np.mean(zs)
    return xp, yp


def build_ftle_map(xp, yp, ftle, bins=220):
    x_edges = np.linspace(np.min(xp), np.max(xp), bins + 1)
    y_edges = np.linspace(np.min(yp), np.max(yp), bins + 1)

    ftle_sum = np.zeros((bins, bins))
    counts = np.zeros((bins, bins))

    x_idx = np.clip(np.digitize(xp, x_edges) - 1, 0, bins - 1)
    y_idx = np.clip(np.digitize(yp, y_edges) - 1, 0, bins - 1)

    for i in range(len(xp)):
        ftle_sum[y_idx[i], x_idx[i]] += ftle[i]
        counts[y_idx[i], x_idx[i]] += 1

    ftle_map = np.divide(
        ftle_sum,
        counts,
        out=np.zeros_like(ftle_sum),
        where=counts > 0
    )

    density_map = counts.copy()

    ftle_map = gaussian_filter(ftle_map, sigma=ridge_sigma)
    ridge_map = gaussian_gradient_magnitude(ftle_map, sigma=1.0)

    return x_edges, y_edges, ftle_map, ridge_map, density_map


# ------------------------------------------------------------
# NEXAH STATE MACHINE ON PROJECTED PLANE
# ------------------------------------------------------------
def nexah_state(x, y, vx, vy):
    r = np.sqrt(x**2 + y**2)
    speed = np.sqrt(vx**2 + vy**2)

    if r < r_release:
        return "release"   # 0100
    elif r < r_lock and speed < 4.0:
        return "lock"      # 0010
    elif r < r_engage:
        return "engage"    # 0001
    else:
        return "nexit"     # 1000


def state_index(name):
    table = {
        "engage": 0,
        "lock": 1,
        "release": 2,
        "nexit": 3
    }
    return table[name]


def apply_navigation(xp, yp, ftle):
    """
    Small corrective drift:
    - high FTLE => pull slightly inward
    - low FTLE => freer motion
    """
    xn = xp.copy()
    yn = yp.copy()

    for i in range(1, len(xn)):
        r = np.sqrt(xn[i]**2 + yn[i]**2) + 1e-9
        inward_x = -xn[i] / r
        inward_y = -yn[i] / r

        strength = nav_gain * max(ftle[i], 0.0)

        xn[i] += strength * inward_x
        yn[i] += strength * inward_y

    return xn, yn


# ------------------------------------------------------------
# MAIN ANALYSIS
# ------------------------------------------------------------
def analyze_v77():
    xs, ys, zs = simulate_lorenz()
    ftle = compute_ftle_along_trajectory(xs, ys, zs, stride=20, horizon=30)

    xp, yp = project_plane(xs, ys, zs)
    xn, yn = apply_navigation(xp, yp, ftle)

    vx = np.gradient(xn, dt)
    vy = np.gradient(yn, dt)

    states = [nexah_state(xn[i], yn[i], vx[i], vy[i]) for i in range(len(xn))]
    switches = np.array([i for i in range(1, len(states)) if states[i] != states[i - 1]], dtype=int)

    x_edges, y_edges, ftle_map, ridge_map, density_map = build_ftle_map(xp, yp, ftle, bins=220)

    return {
        "xs": xs, "ys": ys, "zs": zs,
        "xp": xp, "yp": yp,
        "xn": xn, "yn": yn,
        "ftle": ftle,
        "states": states,
        "switches": switches,
        "ftle_map": ftle_map,
        "ridge_map": ridge_map,
        "density_map": density_map,
        "x_edges": x_edges,
        "y_edges": y_edges
    }


# ------------------------------------------------------------
# PLOTTING
# ------------------------------------------------------------
def plot_v77(data):
    xp = data["xp"]
    yp = data["yp"]
    xn = data["xn"]
    yn = data["yn"]
    ftle = data["ftle"]
    switches = data["switches"]

    ftle_map = data["ftle_map"]
    ridge_map = data["ridge_map"]
    density_map = data["density_map"]
    x_edges = data["x_edges"]
    y_edges = data["y_edges"]

    state_colors = {
        "engage": "blue",
        "lock": "orange",
        "release": "green",
        "nexit": "red"
    }

    # --------------------------
    # figure 1
    # --------------------------
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    im0 = axs[0, 0].imshow(
        ftle_map,
        origin="lower",
        extent=[x_edges.min(), x_edges.max(), y_edges.min(), y_edges.max()],
        aspect="auto",
        cmap="inferno"
    )
    axs[0, 0].set_title("FTLE-like Instability Map")
    axs[0, 0].set_xlabel("projected X")
    axs[0, 0].set_ylabel("projected Y")
    plt.colorbar(im0, ax=axs[0, 0], fraction=0.046)

    im1 = axs[0, 1].imshow(
        ridge_map,
        origin="lower",
        extent=[x_edges.min(), x_edges.max(), y_edges.min(), y_edges.max()],
        aspect="auto",
        cmap="magma"
    )
    axs[0, 1].set_title("Ridge / Filament Map")
    axs[0, 1].set_xlabel("projected X")
    axs[0, 1].set_ylabel("projected Y")
    plt.colorbar(im1, ax=axs[0, 1], fraction=0.046)

    im2 = axs[1, 0].imshow(
        density_map,
        origin="lower",
        extent=[x_edges.min(), x_edges.max(), y_edges.min(), y_edges.max()],
        aspect="auto",
        cmap="Blues"
    )
    axs[1, 0].set_title("Trajectory Density")
    axs[1, 0].set_xlabel("projected X")
    axs[1, 0].set_ylabel("projected Y")
    plt.colorbar(im2, ax=axs[1, 0], fraction=0.046)

    axs[1, 1].plot(ftle, color="purple")
    for s in switches:
        axs[1, 1].axvline(s, color="gray", alpha=0.2)
    axs[1, 1].set_title("FTLE timeline + switches")
    axs[1, 1].set_xlabel("time step")
    axs[1, 1].grid(True, alpha=0.25)

    plt.tight_layout()
    plt.show()

    # --------------------------
    # figure 2
    # --------------------------
    plt.figure(figsize=(10, 8))
    plt.imshow(
        ridge_map,
        origin="lower",
        extent=[x_edges.min(), x_edges.max(), y_edges.min(), y_edges.max()],
        aspect="auto",
        cmap="Greys",
        alpha=0.55
    )

    plt.plot(xp, yp, color="lightblue", linewidth=0.7, alpha=0.35, label="Lorenz projection")
    plt.plot(xn, yn, color="white", linewidth=1.2, alpha=0.95, label="NEXAH navigation")

    if len(switches) > 0:
        plt.scatter(xn[switches], yn[switches], color="yellow", s=20, label="switches")

    plt.title("NEXAH v7.7 — Lorenz + Ridge Map + Navigation")
    plt.xlabel("projected X")
    plt.ylabel("projected Y")
    plt.grid(True, alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --------------------------
    # figure 3
    # --------------------------
    plt.figure(figsize=(10, 8))
    for name, color in state_colors.items():
        idx = [i for i, s in enumerate(data["states"]) if s == name]
        plt.scatter(xn[idx], yn[idx], s=3, color=color, alpha=0.65, label=name)

    if len(switches) > 0:
        plt.scatter(xn[switches], yn[switches], s=24, color="black", label="switches")

    plt.title("State-colored navigation on Lorenz-derived plane")
    plt.xlabel("projected X")
    plt.ylabel("projected Y")
    plt.grid(True, alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --------------------------
    # figure 4
    # --------------------------
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    stride = 8
    sc = ax.scatter(
        data["xs"][::stride],
        data["ys"][::stride],
        data["zs"][::stride],
        c=data["ftle"][::stride],
        cmap="plasma",
        s=3
    )

    ax.set_title("Lorenz attractor colored by FTLE-like instability")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    fig.colorbar(sc, ax=ax, shrink=0.7, label="FTLE proxy")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
def print_summary(data):
    unique, counts = np.unique(data["states"], return_counts=True)
    state_counts = dict(zip(unique, counts))

    print("\n=== NEXAH v7.7 Summary ===")
    print("Lorenz parameters:", f"sigma={sigma}, rho={rho}, beta={beta}")
    print("FTLE min/max/mean:", float(np.min(data["ftle"])), float(np.max(data["ftle"])), float(np.mean(data["ftle"])))
    print("switch count:", len(data["switches"]))

    print("\nState counts:")
    for k in ["engage", "lock", "release", "nexit"]:
        print(f"{k}: {state_counts.get(k, 0)}")


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
if __name__ == "__main__":
    data = analyze_v77()
    print_summary(data)
    plot_v77(data)
