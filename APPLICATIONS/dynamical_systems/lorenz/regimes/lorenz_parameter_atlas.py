import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from datetime import datetime
import os

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


# -------------------------------------------------------
# Lorenz system
# -------------------------------------------------------

def lorenz(t, state, sigma, rho, beta):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]


def integrate(state, sigma, rho, beta, T=2.0):
    sol = solve_ivp(
        lambda t, s: lorenz(t, s, sigma, rho, beta),
        [0, T],
        state,
        max_step=0.01
    )
    return sol.y[:, -1]


# -------------------------------------------------------
# FTLE field
# -------------------------------------------------------

def ftle_field(sigma, rho, beta,
               x_range=(-20, 20),
               z_range=(0, 50),
               n=100,
               eps=1e-6,
               T=2.0):

    xs = np.linspace(*x_range, n)
    zs = np.linspace(*z_range, n)

    ftle = np.zeros((n, n))

    for i, x in enumerate(xs):
        print(f"  row {i+1}/{n}", end="\r")
        for j, z in enumerate(zs):
            s = np.array([x, 0.0, z])

            f0 = integrate(s, sigma, rho, beta, T)
            fx = integrate(s + np.array([eps, 0.0, 0.0]), sigma, rho, beta, T)
            fz = integrate(s + np.array([0.0, 0.0, eps]), sigma, rho, beta, T)

            J = np.array([
                (fx - f0) / eps,
                (fz - f0) / eps
            ]).T

            C = J.T @ J
            eig = np.max(np.real(np.linalg.eigvals(C)))
            eig = max(eig, 1e-12)

            ftle[j, i] = (1.0 / T) * np.log(np.sqrt(eig))

    print()
    return xs, zs, ftle


# -------------------------------------------------------
# Atlas plot helper
# -------------------------------------------------------

def plot_scan(param_name, param_values, fixed_sigma, fixed_rho, fixed_beta, n=100):
    cols = len(param_values)
    fig, axes = plt.subplots(1, cols, figsize=(4 * cols, 5), constrained_layout=True)

    if cols == 1:
        axes = [axes]

    all_fields = []

    for idx, val in enumerate(param_values):
        sigma = fixed_sigma
        rho = fixed_rho
        beta = fixed_beta

        if param_name == "sigma":
            sigma = val
        elif param_name == "rho":
            rho = val
        elif param_name == "beta":
            beta = val
        else:
            raise ValueError("param_name must be 'sigma', 'rho', or 'beta'")

        print(f"Computing {param_name}={val} ...")
        xs, zs, ftle = ftle_field(sigma, rho, beta, n=n)
        all_fields.append((xs, zs, ftle, sigma, rho, beta))

    vmin = min(np.min(f[2]) for f in all_fields)
    vmax = max(np.max(f[2]) for f in all_fields)

    for ax, (xs, zs, ftle, sigma, rho, beta), val in zip(axes, all_fields, param_values):
        im = ax.imshow(
            ftle,
            extent=[xs.min(), xs.max(), zs.min(), zs.max()],
            origin="lower",
            aspect="auto",
            vmin=vmin,
            vmax=vmax,
            cmap="inferno"
        )
        ax.set_title(f"{param_name} = {val}")
        ax.set_xlabel("x")
        ax.set_ylabel("z")

    cbar = fig.colorbar(im, ax=axes, shrink=0.9)
    cbar.set_label("FTLE")

    fig.suptitle(
        f"Lorenz Parameter Atlas — {param_name}-scan\n"
        f"(sigma={fixed_sigma}, rho={fixed_rho}, beta={fixed_beta}, varying {param_name})",
        fontsize=12
    )

    filename = os.path.join(
        OUTPUT_DIR,
        f"lorenz_parameter_atlas_{param_name}_{timestamp}.png"
    )
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print("saved:", filename)
    plt.show()


# -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":
    # Standard Lorenz baseline
    sigma0 = 10
    rho0 = 28
    beta0 = 8 / 3

    # Keep n moderate for first tests
    n = 90

    # 1) rho scan
    plot_scan(
        param_name="rho",
        param_values=[24, 26, 28, 30, 32],
        fixed_sigma=sigma0,
        fixed_rho=rho0,
        fixed_beta=beta0,
        n=n
    )

    # 2) sigma scan
    plot_scan(
        param_name="sigma",
        param_values=[8, 10, 12, 14],
        fixed_sigma=sigma0,
        fixed_rho=rho0,
        fixed_beta=beta0,
        n=n
    )

    # 3) beta scan
    plot_scan(
        param_name="beta",
        param_values=[2.0, 2.5, 8/3, 3.0, 4.0],
        fixed_sigma=sigma0,
        fixed_rho=rho0,
        fixed_beta=beta0,
        n=n
    )
