import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.interpolate import RegularGridInterpolator


# ============================================================
# NEXAH CONTROL LAYER v38
# Structure-Aware Return Dynamics
# ============================================================


def phase_embedding(x, dt=1.0):
    """Convert signal x(t) into state s=(r, theta)."""
    dx = np.gradient(x, dt)

    r = np.sqrt(x**2 + dx**2)
    theta = np.arctan2(dx, x)

    return r, theta


def build_density_field(r, theta, bins=80, sigma=1.5):
    """Estimate rho(r, theta) by smoothed histogram."""
    rho, r_edges, th_edges = np.histogram2d(
        r,
        theta,
        bins=bins,
        density=True
    )

    rho = gaussian_filter(rho, sigma=sigma)
    rho = rho + 1e-9

    r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    th_centers = 0.5 * (th_edges[:-1] + th_edges[1:])

    return rho, r_centers, th_centers


def gradient_field(field, r_grid, theta_grid):
    """Compute numerical gradient of a scalar field."""
    dr = np.mean(np.diff(r_grid))
    dtheta = np.mean(np.diff(theta_grid))

    grad_r, grad_theta = np.gradient(field, dr, dtheta)

    return grad_r, grad_theta


def make_interpolator(field, r_grid, theta_grid):
    """Create interpolator for field lookup."""
    return RegularGridInterpolator(
        (r_grid, theta_grid),
        field,
        bounds_error=False,
        fill_value=None
    )


def estimate_ridge_distance(rho, r_grid, theta_grid):
    """
    Approximate ridge distance D.
    Ridge = high-density cells above 90th percentile.
    """
    threshold = np.percentile(rho, 90)
    ridge_points = np.argwhere(rho >= threshold)

    D = np.zeros_like(rho)

    for i in range(rho.shape[0]):
        for j in range(rho.shape[1]):
            distances = np.sqrt(
                (ridge_points[:, 0] - i) ** 2 +
                (ridge_points[:, 1] - j) ** 2
            )
            D[i, j] = np.min(distances)

    D = D / (np.max(D) + 1e-9)

    return D


def estimate_iota_probability(r, theta, dr_dtheta, r_grid, theta_grid, bins=80):
    """
    Estimate P(IOTA | r, theta).
    IOTA = high |dr/dtheta| event.
    """
    threshold = np.percentile(np.abs(dr_dtheta), 98)
    iota = np.abs(dr_dtheta) > threshold

    total, _, _ = np.histogram2d(r, theta, bins=[r_grid, theta_grid])
    events, _, _ = np.histogram2d(r[iota], theta[iota], bins=[r_grid, theta_grid])

    P = events / (total + 1e-9)
    P = gaussian_filter(P, sigma=1.5)

    return P


def compute_flow_derivative(r, theta):
    """Compute dr/dtheta."""
    dr = np.gradient(r)
    dtheta = np.gradient(theta)

    return dr / (dtheta + 1e-9)


def control_step(
    s,
    grad_P_interp,
    grad_rho_interp,
    grad_G_interp,
    grad_D_interp,
    alpha=1.0,
    beta=1.0,
    gamma=1.0,
    delta=1.0,
    eta=0.02
):
    """
    V38 control law:

    u =
    - alpha ∇P
    + beta  ∇rho
    - gamma ∇G
    - delta ∇D
    """

    point = np.array([s])

    grad_P = np.array([
        grad_P_interp[0](point)[0],
        grad_P_interp[1](point)[0]
    ])

    grad_rho = np.array([
        grad_rho_interp[0](point)[0],
        grad_rho_interp[1](point)[0]
    ])

    grad_G = np.array([
        grad_G_interp[0](point)[0],
        grad_G_interp[1](point)[0]
    ])

    grad_D = np.array([
        grad_D_interp[0](point)[0],
        grad_D_interp[1](point)[0]
    ])

    u = (
        -alpha * grad_P
        + beta * grad_rho
        - gamma * grad_G
        - delta * grad_D
    )

    return s + eta * u, u


def run_v38_control(x, dt=1.0, bins=80):
    """Full NEXAH v38 pipeline."""

    r, theta = phase_embedding(x, dt)
    dr_dtheta = compute_flow_derivative(r, theta)

    rho, r_grid, theta_grid = build_density_field(r, theta, bins=bins)

    G = 1.0 / rho
    G = G / np.max(G)

    D = estimate_ridge_distance(rho, r_grid, theta_grid)

    P = estimate_iota_probability(
        r,
        theta,
        dr_dtheta,
        r_grid,
        theta_grid,
        bins=bins
    )

    grad_rho = gradient_field(rho, r_grid, theta_grid)
    grad_G = gradient_field(G, r_grid, theta_grid)
    grad_D = gradient_field(D, r_grid, theta_grid)
    grad_P = gradient_field(P, r_grid, theta_grid)

    grad_rho_interp = (
        make_interpolator(grad_rho[0], r_grid, theta_grid),
        make_interpolator(grad_rho[1], r_grid, theta_grid),
    )

    grad_G_interp = (
        make_interpolator(grad_G[0], r_grid, theta_grid),
        make_interpolator(grad_G[1], r_grid, theta_grid),
    )

    grad_D_interp = (
        make_interpolator(grad_D[0], r_grid, theta_grid),
        make_interpolator(grad_D[1], r_grid, theta_grid),
    )

    grad_P_interp = (
        make_interpolator(grad_P[0], r_grid, theta_grid),
        make_interpolator(grad_P[1], r_grid, theta_grid),
    )

    controlled = []
    controls = []

    for i in range(len(r)):
        s = np.array([r[i], theta[i]])

        s_new, u = control_step(
            s,
            grad_P_interp,
            grad_rho_interp,
            grad_G_interp,
            grad_D_interp
        )

        controlled.append(s_new)
        controls.append(u)

    controlled = np.array(controlled)
    controls = np.array(controls)

    return {
        "r": r,
        "theta": theta,
        "rho": rho,
        "G": G,
        "D": D,
        "P_IOTA": P,
        "controlled": controlled,
        "controls": controls,
        "r_grid": r_grid,
        "theta_grid": theta_grid,
    }


# ============================================================
# TEST RUN
# ============================================================

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0])

    r = result["r"]
    theta = result["theta"]
    controlled = result["controlled"]

    plt.figure(figsize=(8, 8))
    plt.scatter(theta, r, s=2, alpha=0.35, label="original")
    plt.scatter(
        controlled[:, 1],
        controlled[:, 0],
        s=2,
        alpha=0.35,
        label="v38 controlled"
    )
    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH Control Layer v38 — Inhale Dynamics")
    plt.legend()
    plt.tight_layout()
    plt.show()
