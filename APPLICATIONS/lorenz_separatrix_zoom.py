"""
Lorenz Separatrix Fractal Zoom

Investigates basin structure near x≈0 (Separatrix).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

OUTPUT = "APPLICATIONS/outputs/lorenz_separatrix"
os.makedirs(OUTPUT, exist_ok=True)


# Lorenz system
def lorenz(state, t, sigma=10.0, rho=28.0, beta=8/3):
    x,y,z = state
    dx = sigma*(y-x)
    dy = x*(rho-z)-y
    dz = x*y-beta*z
    return [dx,dy,dz]


def simulate(initial):

    t = np.linspace(0,40,8000)

    traj = odeint(lorenz, initial, t)

    x_final = traj[-1,0]

    if x_final > 0:
        return 1
    else:
        return 0


# zoom region near separatrix
xs = np.linspace(-0.2,0.2,400)
zs = np.linspace(26,28,400)

basin = np.zeros((len(zs),len(xs)))

for i,z in enumerate(zs):

    print("row",i,"/",len(zs))

    for j,x in enumerate(xs):

        initial = [x,0,z]

        basin[i,j] = simulate(initial)


plt.figure(figsize=(8,8))

plt.imshow(
    basin,
    extent=[xs[0],xs[-1],zs[0],zs[-1]],
    origin="lower",
    cmap="coolwarm",
    aspect="auto"
)

plt.xlabel("x")
plt.ylabel("z")
plt.title("Lorenz Separatrix Basin Structure (Zoom)")

path = OUTPUT+"/separatrix_zoom.png"
plt.savefig(path,dpi=300)

print("saved:",path)

plt.show()
