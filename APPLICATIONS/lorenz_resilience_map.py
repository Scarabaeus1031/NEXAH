import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def lorenz(state, t, sigma=10, rho=28, beta=8/3):
    x,y,z = state
    return [
        sigma*(y-x),
        x*(rho-z)-y,
        x*y-beta*z
    ]


def first_switch(traj):

    x = traj[:,0]

    state = np.sign(x[0])

    for i,v in enumerate(x):

        if np.sign(v) != state:
            return i

    return len(x)


res = 200

xs = np.linspace(-4,4,res)
zs = np.linspace(15,35,res)

t = np.linspace(0,50,5000)

tau = np.zeros((res,res))


for i,z in enumerate(zs):

    print(i,res)

    for j,x in enumerate(xs):

        traj = odeint(lorenz,[x,0,z],t)

        tau[i,j] = first_switch(traj)


plt.figure(figsize=(8,8))

plt.imshow(
    tau,
    extent=[xs[0],xs[-1],zs[0],zs[-1]],
    origin="lower",
    cmap="inferno"
)

plt.colorbar(label="time until lobe switch")

plt.xlabel("X")
plt.ylabel("Z")
plt.title("Lorenz Resilience Map")

plt.show()
