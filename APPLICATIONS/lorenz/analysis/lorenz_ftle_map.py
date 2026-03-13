import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from datetime import datetime
import os

sigma = 10
rho = 28
beta = 8/3


def lorenz(t, state):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]


def integrate(state, T=2):
    sol = solve_ivp(lorenz, [0, T], state, max_step=0.01)
    return sol.y[:, -1]


def ftle_field(x_range=(-20,20), z_range=(0,50), n=200, eps=1e-6, T=2):

    xs = np.linspace(*x_range, n)
    zs = np.linspace(*z_range, n)

    ftle = np.zeros((n,n))

    for i,x in enumerate(xs):
        for j,z in enumerate(zs):

            s = np.array([x,0,z])

            f0 = integrate(s,T)
            fx = integrate(s + np.array([eps,0,0]),T)
            fz = integrate(s + np.array([0,0,eps]),T)

            J = np.array([
                (fx - f0)/eps,
                (fz - f0)/eps
            ]).T

            C = J.T @ J
            eig = np.max(np.linalg.eigvals(C))

            ftle[j,i] = (1/T)*np.log(np.sqrt(eig))

    return xs, zs, ftle


def plot_ftle(xs,zs,ftle):

    plt.figure(figsize=(10,6))
    plt.imshow(ftle,
        extent=[xs.min(),xs.max(),zs.min(),zs.max()],
        origin="lower",
        cmap="inferno"
    )

    plt.colorbar(label="FTLE")
    plt.xlabel("x")
    plt.ylabel("z")
    plt.title("Lorenz FTLE Map")

    outdir = "../outputs/lorenz_navigation"
    os.makedirs(outdir,exist_ok=True)

    name = f"lorenz_ftle_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(outdir,name)

    plt.savefig(path,dpi=300)
    print("saved:",path)

    plt.show()


if __name__ == "__main__":

    xs,zs,ftle = ftle_field()
    plot_ftle(xs,zs,ftle)
