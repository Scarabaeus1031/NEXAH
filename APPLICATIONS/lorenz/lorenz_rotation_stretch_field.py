"""
Lorenz Rotation + Stretch Field

Visualizes the Lorenz flow field with magnitude coloring
to reveal regions of rotation and stretching.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import datetime


OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# Lorenz parameters
sigma = 10
rho = 28
beta = 8/3


def lorenz(x,y,z):

    dx = sigma*(y-x)
    dy = x*(rho-z) - y
    dz = x*y - beta*z

    return dx,dy,dz


# sampling grid

res = 12

x = np.linspace(-20,20,res)
y = np.linspace(-30,30,res)
z = np.linspace(0,50,res)

X,Y,Z = np.meshgrid(x,y,z)

U = np.zeros_like(X)
V = np.zeros_like(Y)
W = np.zeros_like(Z)

mag = np.zeros_like(X)


# compute field

for i in range(res):
    for j in range(res):
        for k in range(res):

            dx,dy,dz = lorenz(
                X[i,j,k],
                Y[i,j,k],
                Z[i,j,k]
            )

            U[i,j,k] = dx
            V[i,j,k] = dy
            W[i,j,k] = dz

            mag[i,j,k] = np.sqrt(dx*dx + dy*dy + dz*dz)


# normalize vectors

U = U/mag
V = V/mag
W = W/mag


# plotting

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection="3d")

colors = mag.flatten()
colors = (colors - colors.min())/(colors.max()-colors.min())

ax.quiver(
    X,Y,Z,
    U,V,W,
    length=2,
    colors=plt.cm.plasma(colors),
    normalize=True
)

ax.set_title("Lorenz Rotation & Stretch Field")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

file_output = f"{OUTPUT_DIR}/lorenz_rotation_stretch_{timestamp}.png"

plt.savefig(file_output,dpi=300,bbox_inches="tight")

print("saved:",file_output)

plt.show()
