"""
Lorenz Flow Vector Field

Visualizes the velocity field of the Lorenz system.
Shows how trajectories move through the state space.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import datetime


# --------------------------------------------------
# output
# --------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# --------------------------------------------------
# Lorenz parameters
# --------------------------------------------------

sigma = 10
rho = 28
beta = 8/3


# --------------------------------------------------
# Lorenz field
# --------------------------------------------------

def lorenz_field(x,y,z):

    dx = sigma*(y-x)
    dy = x*(rho-z) - y
    dz = x*y - beta*z

    return dx,dy,dz


# --------------------------------------------------
# grid of sample points
# --------------------------------------------------

res = 10

x = np.linspace(-20,20,res)
y = np.linspace(-30,30,res)
z = np.linspace(0,50,res)

X,Y,Z = np.meshgrid(x,y,z)


U = np.zeros_like(X)
V = np.zeros_like(Y)
W = np.zeros_like(Z)


# --------------------------------------------------
# compute vector field
# --------------------------------------------------

for i in range(res):
    for j in range(res):
        for k in range(res):

            dx,dy,dz = lorenz_field(
                X[i,j,k],
                Y[i,j,k],
                Z[i,j,k]
            )

            U[i,j,k] = dx
            V[i,j,k] = dy
            W[i,j,k] = dz


# normalize vectors (for visualization)

mag = np.sqrt(U**2 + V**2 + W**2)

U = U/mag
V = V/mag
W = W/mag


# --------------------------------------------------
# plot
# --------------------------------------------------

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')


ax.quiver(
    X,Y,Z,
    U,V,W,
    length=2,
    normalize=True
)


ax.set_title("Lorenz Flow Vector Field")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")


file_output = f"{OUTPUT_DIR}/lorenz_flow_field_{timestamp}.png"

plt.savefig(file_output,dpi=300,bbox_inches="tight")

print("saved:",file_output)

plt.show()
