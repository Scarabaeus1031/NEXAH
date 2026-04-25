# ============================================================
# NEXAH CONTROL LAYER v38 (FIXED)
# Structure-Aware Return Dynamics
# ============================================================

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.interpolate import RegularGridInterpolator


# ------------------------------------------------------------
# Phase Embedding
# ------------------------------------------------------------

def phase_embedding(x, dt=1.0):
    dx = np.gradient(x, dt)

    r = np.sqrt(x**2 + dx**2)
    theta = np.arctan2(dx, x)

    return r, theta


# ------------------------------------------------------------
# Density Field
# ------------------------------------------------------------

def build_density_field(r, theta, bins=80, sigma=1.5):
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

    return rho, r_centers, th_centers, r_edges, th_edges


# ------------------------------------------------------------
# Gradient
# ------------------------------------------------------------

def gradient_field(field, r_grid, theta_grid):
    dr = np.mean(np.diff(r_grid))
    dtheta = np.mean(np.diff(theta_grid))

    grad_r, grad_theta = np.gradient(field, dr, dtheta)

    return grad_r, grad_theta


# ------------------------------------------------------------
# Interpolator
# ------------------------------------------------------------

def make_interpolator(field, r_grid, theta_grid):
    return RegularGridInterpolator(
        (r_grid, theta_grid),
        field,
        bounds_error=False,
        fill_value=0.0
    )


# ------------------------------------------------------------
# Ridge Distance
# ------------------------------------------------------------

def estimate_ridge_distance(rho):
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


# ------------------------------------------------------------
# Flow derivative
# ------------------------------------------------------------

def compute_flow_derivative(r, theta):
    dr = np.gradient(r)
    dtheta = np.gradient(theta)

    return dr / (dtheta + 1e-9)


# ------------------------------------------------------------
# IOTA Probability (FIXED)
# ------------------------------------------------------------

def estimate_iota_probability(r, theta, dr_dtheta, r_edges, theta_edges):
    threshold = np.percentile(np.abs(dr_dtheta), 98)
    iota = np.abs(dr_dtheta) > threshold

    total, _, _ = np.histogram2d(r, theta, bins=[r_edges, theta_edges])
    events, _, _ = np.histogram2d(r[iota], theta[iota], bins=[r_edges, theta_edges])

    P = events / (total + 1e-9)
    P = gaussian_filter(P, sigma=1.5)

    return P


# ------------------------------------------------------------
# Control Step
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# MAIN PIPELINE
# ------------------------------------------------------------

def run_v38_control(x, dt=1.0, bins=80):

    r, theta = phase_embedding(x, dt)
    dr_dtheta = compute_flow_derivative(r, theta)

    rho, r_grid, theta_grid, r_edges, theta_edges = build_density_field(r, theta, bins=bins)

    G = 1.0 / rho
    G = G / np.max(G)

    D = estimate_ridge_distance(rho)

    P = estimate_iota_probability(
        r,
        theta,
        dr_dtheta,
        r_edges,
        theta_edges
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

    return {
        "r": r,
        "theta": theta,
        "rho": rho,
        "G": G,
        "D": D,
        "P_IOTA": P,
        "controlled": np.array(controlled),
        "controls": np.array(controls),
        "r_grid": r_grid,
        "theta_grid": theta_grid,
    }


# ------------------------------------------------------------
# TEST RUN
# ------------------------------------------------------------

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0])

    plt.figure(figsize=(8, 8))
    plt.scatter(result["theta"], result["r"], s=2, alpha=0.3, label="original")
    plt.scatter(
        result["controlled"][:, 1],
        result["controlled"][:, 0],
        s=2,
        alpha=0.3,
        label="v38 controlled"
    )
    plt.legend()
    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v38 Control (Fixed)")
    plt.show()
