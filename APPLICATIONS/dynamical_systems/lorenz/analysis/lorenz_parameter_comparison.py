import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from datetime import datetime
import os

# -------------------------------------------------------
# OUTPUT DIRECTORY
# -------------------------------------------------------

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
# FTLE FIELD
# -------------------------------------------------------

def ftle_field(sigma, rho, beta,
               x_range=(-20, 20),
               z_range=(0, 50),
               n=200,
               eps=1e-6,
               T=2):

    xs = np.linspace(*x_range, n)
    zs = np.linspace(*z_range, n)

    ftle = np.zeros((n, n))

    for i, x in enumerate(xs):
        for j, z in enumerate(zs):

            s = np.array([x, 0, z])

            f0 = integrate(s, sigma, rho, beta, T)

            fx = integrate(s + np.array([eps, 0, 0]), sigma, rho, beta, T)
            fz = integrate(s + np.array([0, 0, eps]), sigma, rho, beta, T)

            J = np.array([
                (fx - f0)/eps,
                (fz - f0)/eps
            ]).T

            C = J.T @ J
            eig = np.max(np.linalg.eigvals(C))

            ftle[j, i] = (1/T) * np.log(np.sqrt(eig))

    return xs, zs, ftle


# -------------------------------------------------------
# PARAMETER SETS
# -------------------------------------------------------

standard = dict(sigma=10, rho=28, beta=8/3)
experimental = dict(sigma=11, rho=29, beta=16/3)


print("computing standard Lorenz FTLE...")
xs, zs, ftle_A = ftle_field(**standard)

print("computing experimental Lorenz FTLE...")
_, _, ftle_B = ftle_field(**experimental)

diff = ftle_B - ftle_A


# -------------------------------------------------------
# PLOT
# -------------------------------------------------------

fig, ax = plt.subplots(1, 3, figsize=(18, 6))

im0 = ax[0].imshow(
    ftle_A,
    extent=[xs.min(), xs.max(), zs.min(), zs.max()],
    origin="lower"
)

ax[0].set_title("Standard Lorenz (10,28,8/3)")
plt.colorbar(im0, ax=ax[0])

im1 = ax[1].imshow(
    ftle_B,
    extent=[xs.min(), xs.max(), zs.min(), zs.max()],
    origin="lower"
)

ax[1].set_title("Experimental Lorenz (11,29,16/3)")
plt.colorbar(im1, ax=ax[1])

im2 = ax[2].imshow(
    diff,
    extent=[xs.min(), xs.max(), zs.min(), zs.max()],
    origin="lower",
    cmap="seismic"
)

ax[2].set_title("Difference (B − A)")
plt.colorbar(im2, ax=ax[2])


for a in ax:
    a.set_xlabel("x")
    a.set_ylabel("z")


plt.tight_layout()


# -------------------------------------------------------
# SAVE FIGURE
# -------------------------------------------------------

filename = f"{OUTPUT_DIR}/lorenz_parameter_comparison_{timestamp}.png"

plt.savefig(filename, dpi=300)

print("saved figure to:", filename)

plt.show()
